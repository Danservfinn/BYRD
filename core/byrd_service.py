"""
BYRDService - Human-Service-First orchestration layer.

Implements the human-service-first architecture:
- Maintains task queue (human tasks vs idle RSI)
- Detects idle periods
- Interrupts RSI when critical human tasks arrive
- Resumes RSI when idle

This is the main entry point for Agent Zero integration,
providing the service layer that prioritizes human requests
while allowing RSI during idle periods.

See docs/ASI_PATH_DESIGN.md for architecture context.
"""

import asyncio
import logging
from typing import Optional, Dict, List, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import time

logger = logging.getLogger("byrd.service")


class ServiceMode(Enum):
    """Operating mode of the service."""
    IDLE_RSI = "idle_rsi"  # Running RSI cycles when idle
    TASK_PROCESSING = "task_processing"  # Processing human task
    PAUSED = "paused"  # Manually paused


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 1.0  # Immediate RSI interruption
    HIGH = 0.8     # Interrupt after current phase
    NORMAL = 0.5   # Wait for current cycle
    LOW = 0.2      # Queue for later


@dataclass
class QueuedTask:
    """A task in the service queue."""
    task_id: str
    description: str
    objective: str
    priority: float
    source: str = "external"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "pending"

    @property
    def is_critical(self) -> bool:
        """Check if this is a critical priority task."""
        return self.priority >= TaskPriority.CRITICAL.value

    @property
    def is_high_priority(self) -> bool:
        """Check if this is a high priority task."""
        return self.priority >= TaskPriority.HIGH.value


@dataclass
class ServiceStats:
    """Service statistics."""
    mode: ServiceMode
    uptime_seconds: float
    tasks_processed: int
    tasks_completed: int
    tasks_failed: int
    rsi_cycles_completed: int
    rsi_interruptions: int
    current_task: Optional[str] = None
    last_idle_time: Optional[datetime] = None
    last_task_time: Optional[datetime] = None


class BYRDService:
    """
    Human-Service-First orchestration layer.

    Lifecycle:
    1. Start: Begin monitoring for tasks
    2. Task Arrival: Interrupt RSI if needed, process task
    3. Task Complete: Return to idle, resume RSI
    4. Stop: Graceful shutdown

    The service maintains a Ralph Loop for RSI and interrupts
    it when high-priority human tasks arrive.
    """

    # Configuration defaults
    DEFAULT_IDLE_THRESHOLD_SECONDS = 10  # Consider idle after no tasks for this long
    DEFAULT_TASK_POLL_INTERVAL = 2  # Seconds between task checks
    DEFAULT_RSI_IDLE_DELAY = 5  # Seconds to wait before starting RSI when idle

    def __init__(
        self,
        memory,
        ralph_loop=None,
        config: Dict = None
    ):
        """
        Initialize BYRDService.

        Args:
            memory: Memory instance for task storage
            ralph_loop: Optional RalphLoop instance for RSI
            config: Configuration dict with optional overrides:
                - idle_threshold_seconds: Idle detection threshold
                - task_poll_interval: Seconds between task polls
                - rsi_idle_delay: Delay before starting RSI when idle
                - auto_resume_rsi: Whether to auto-resume RSI after tasks (default: True)
        """
        self.memory = memory
        self.ralph_loop = ralph_loop
        self.config = config or {}

        # Configuration
        self._idle_threshold = self.config.get(
            'idle_threshold_seconds',
            self.DEFAULT_IDLE_THRESHOLD_SECONDS
        )
        self._poll_interval = self.config.get(
            'task_poll_interval',
            self.DEFAULT_TASK_POLL_INTERVAL
        )
        self._rsi_idle_delay = self.config.get(
            'rsi_idle_delay',
            self.DEFAULT_RSI_IDLE_DELAY
        )
        self._auto_resume_rsi = self.config.get('auto_resume_rsi', True)

        # State
        self._running = False
        self._mode = ServiceMode.PAUSED
        self._task_queue: asyncio.Queue = asyncio.Queue()
        self._current_task: Optional[QueuedTask] = None
        self._rsi_task: Optional[asyncio.Task] = None
        self._service_task: Optional[asyncio.Task] = None

        # Statistics
        self._start_time: Optional[float] = None
        self._tasks_processed = 0
        self._tasks_completed = 0
        self._tasks_failed = 0
        self._rsi_cycles_completed = 0
        self._rsi_interruptions = 0
        self._last_idle_time: Optional[datetime] = None
        self._last_task_time: Optional[datetime] = None

        # Task handler callback (for Agent Zero integration)
        self._task_handler: Optional[Callable] = None

    def set_task_handler(self, handler: Callable[[QueuedTask], Any]) -> None:
        """
        Set the task handler callback.

        When a task is dequeued, this handler will be called with
        the task. The handler should return the result.

        Args:
            handler: Async callable that takes a QueuedTask and returns result
        """
        self._task_handler = handler

    async def start(self) -> None:
        """Start the service loop."""
        if self._running:
            logger.warning("BYRDService already running")
            return

        self._running = True
        self._start_time = time.time()
        self._mode = ServiceMode.IDLE_RSI

        logger.info("BYRDService started - entering service loop")

        # Start main service loop
        self._service_task = asyncio.create_task(self._service_loop())

    async def stop(self) -> None:
        """Stop the service gracefully."""
        if not self._running:
            return

        logger.info("BYRDService stopping...")
        self._running = False

        # Cancel RSI if running
        if self._rsi_task and not self._rsi_task.done():
            if self.ralph_loop:
                await self._interrupt_rsi("service_shutdown")
            self._rsi_task.cancel()
            try:
                await self._rsi_task
            except asyncio.CancelledError:
                pass

        # Cancel service loop
        if self._service_task and not self._service_task.done():
            self._service_task.cancel()
            try:
                await self._service_task
            except asyncio.CancelledError:
                pass

        logger.info("BYRDService stopped")

    async def enqueue_task(
        self,
        description: str,
        objective: str,
        priority: float = 0.5,
        source: str = "external"
    ) -> str:
        """
        Add a task to the queue.

        High-priority tasks will interrupt ongoing RSI cycles.

        Args:
            description: What the task is
            objective: What success looks like
            priority: 0.0-1.0, higher = more urgent
            source: "external" or "emergent"

        Returns:
            task_id: The ID of the created task
        """
        task_id = await self.memory.create_task(
            description=description,
            objective=objective,
            priority=priority,
            source=source
        )

        task = QueuedTask(
            task_id=task_id,
            description=description,
            objective=objective,
            priority=priority,
            source=source
        )

        await self._task_queue.put(task)

        logger.info(
            f"Task enqueued: {task_id} (priority={priority}, "
            f"queue_size={self._task_queue.qsize()})"
        )

        # Interrupt RSI if this is a high-priority task
        if task.is_high_priority and self._mode == ServiceMode.IDLE_RSI:
            await self._interrupt_rsi(f"high_priority_task:{task_id}")

        return task_id

    async def _service_loop(self) -> None:
        """
        Main service loop.

        Continuously:
        1. Check for pending tasks in memory
        2. Process tasks if available
        3. Run RSI if idle
        """
        logger.debug("Service loop started")

        while self._running:
            try:
                # First, check for new tasks from memory
                await self._sync_tasks_from_memory()

                # Check if we have a task to process
                if not self._task_queue.empty():
                    await self._process_next_task()
                else:
                    # No tasks - check if we should be idle
                    await self._handle_idle_period()

            except asyncio.CancelledError:
                logger.info("Service loop cancelled")
                break
            except Exception as e:
                logger.exception(f"Service loop error: {e}")
                await asyncio.sleep(self._poll_interval)

    async def _sync_tasks_from_memory(self) -> None:
        """
        Sync pending tasks from memory into the local queue.

        This ensures we capture tasks created via API while
        the service was processing other work.
        """
        try:
            pending_tasks = await self.memory.get_pending_tasks(limit=20)

            for task_dict in pending_tasks:
                task_id = task_dict.get('id')
                # Check if already in queue (avoid duplicates)
                if task_id:
                    # Simple check: we'll skip if we've seen it recently
                    # A more robust implementation would track queued task IDs
                    already_queued = any(
                        t.task_id == task_id for t in self._task_queue._queue
                    )
                    if not already_queued and self._current_task != task_id:
                        task = QueuedTask(
                            task_id=task_id,
                            description=task_dict.get('description', ''),
                            objective=task_dict.get('objective', ''),
                            priority=task_dict.get('priority', 0.5),
                            source=task_dict.get('source', 'external'),
                            status=task_dict.get('status', 'pending')
                        )
                        await self._task_queue.put(task)
                        logger.debug(f"Synced task from memory: {task_id}")

        except Exception as e:
            logger.warning(f"Error syncing tasks from memory: {e}")

    async def _process_next_task(self) -> None:
        """Process the next task from the queue."""
        try:
            # Get next task (wait briefly if queue is being refilled)
            task = await asyncio.wait_for(
                self._task_queue.get(),
                timeout=1.0
            )
        except asyncio.TimeoutError:
            return

        self._current_task = task
        self._mode = ServiceMode.TASK_PROCESSING
        self._last_task_time = datetime.now(timezone.utc)
        self._tasks_processed += 1

        logger.info(
            f"Processing task {task.task_id}: {task.description} "
            f"(priority={task.priority})"
        )

        # Update task status in memory
        await self.memory.update_task_status(task.task_id, 'in_progress')

        try:
            # Execute task via handler or RSI engine
            if self._task_handler:
                result = await self._task_handler(task)
            else:
                # Default handler: use the RSI engine directly
                result = await self._default_task_handler(task)

            # Task completed successfully
            await self.memory.complete_task(
                task_id=task.task_id,
                outcome=str(result.get('outcome', 'completed')),
                learnings=result.get('learnings', []),
                experience_ids=result.get('experience_ids', [])
            )

            self._tasks_completed += 1
            logger.info(f"Task completed: {task.task_id}")

        except Exception as e:
            logger.exception(f"Task failed: {task.task_id}")
            await self.memory.fail_task(task.task_id, str(e))
            self._tasks_failed += 1

        finally:
            self._current_task = None
            self._task_queue.task_done()

    async def _default_task_handler(self, task: QueuedTask) -> Dict:
        """
        Default task handler using RSI engine.

        For tasks that require code/analysis, run a focused RSI cycle.

        Args:
            task: The task to execute

        Returns:
            Result dict with outcome, learnings, experience_ids
        """
        if self.ralph_loop and self.ralph_loop.rsi:
            # Run a focused RSI cycle for this task
            # The RSI engine can be configured to target specific objectives
            result = await self.ralph_loop.rsi.run_cycle(
                objective_override=task.objective
            )

            return {
                'outcome': f'Completed RSI cycle: {result.phase_reached}',
                'learnings': [result.phase_reached],
                'experience_ids': []
            }
        else:
            # No RSI available, return simple completion
            return {
                'outcome': 'Task acknowledged (no RSI engine available)',
                'learnings': [],
                'experience_ids': []
            }

    async def _handle_idle_period(self) -> None:
        """
        Handle idle period - run RSI if configured.

        This is where BYRD engages in recursive self-improvement
        when not serving human requests.
        """
        now = time.time()

        # Check if we've been idle long enough
        if self._last_task_time:
            idle_time = (datetime.now(timezone.utc) - self._last_task_time).total_seconds()
        elif self._last_idle_time:
            idle_time = (datetime.now(timezone.utc) - self._last_idle_time).total_seconds()
        else:
            idle_time = 999  # First run - consider idle

        if idle_time >= self._idle_threshold:
            if self._mode != ServiceMode.IDLE_RSI:
                self._mode = ServiceMode.IDLE_RSI
                self._last_idle_time = datetime.now(timezone.utc)
                logger.info("Entering idle mode - RSI can run")

            # Check if we should start/continue RSI
            if self._auto_resume_rsi and self.ralph_loop:
                await self._maybe_run_rsi()
            else:
                await asyncio.sleep(self._poll_interval)
        else:
            # Not idle yet, wait
            await asyncio.sleep(self._poll_interval)

    async def _maybe_run_rsi(self) -> None:
        """
        Run Ralph Loop for RSI if not already running.

        This runs non-blockingly as a background task.
        """
        if self._rsi_task and not self._rsi_task.done():
            # RSI already running
            return

        if not self._auto_resume_rsi:
            return

        # Start RSI in background
        self._rsi_task = asyncio.create_task(self._run_rsi_idle())

    async def _run_rsi_idle(self) -> None:
        """
        Run Ralph Loop with idle detection.

        This runs RSI cycles until interrupted by a high-priority task.
        """
        if not self.ralph_loop:
            return

        logger.info("Starting RSI during idle period")

        try:
            # Run a limited number of cycles (we'll re-check for tasks)
            result = await self.ralph_loop.run(
                max_iterations=10,  # Run up to 10 cycles before checking tasks
                max_cost_usd=5.0,   # Small cost limit
                max_time_seconds=300  # 5 minutes max
            )

            self._rsi_cycles_completed += result.iterations_completed

            logger.info(
                f"RSI idle run completed: {result.iterations_completed} iterations, "
                f"reason={result.reason.value}"
            )

        except asyncio.CancelledError:
            logger.info("RSI idle run cancelled (task arrived)")
            self._rsi_interruptions += 1
        except Exception as e:
            logger.exception(f"RSI idle run error: {e}")

    async def _interrupt_rsi(self, reason: str) -> None:
        """
        Interrupt the current RSI cycle.

        Args:
            reason: Why the interruption is happening
        """
        if self.ralph_loop:
            logger.info(f"Interrupting RSI: {reason}")
            await self.ralph_loop.interrupt(reason=reason)
            self._rsi_interruptions += 1

    def pause(self) -> None:
        """Pause the service (stops RSI, continues task processing)."""
        logger.info("Service paused")
        self._mode = ServiceMode.PAUSED

    def resume(self) -> None:
        """Resume the service."""
        logger.info("Service resumed")
        if self._running:
            self._mode = ServiceMode.IDLE_RSI

    async def get_stats(self) -> ServiceStats:
        """
        Get current service statistics.

        Returns:
            ServiceStats with current state
        """
        uptime = time.time() - self._start_time if self._start_time else 0

        return ServiceStats(
            mode=self._mode,
            uptime_seconds=uptime,
            tasks_processed=self._tasks_processed,
            tasks_completed=self._tasks_completed,
            tasks_failed=self._tasks_failed,
            rsi_cycles_completed=self._rsi_cycles_completed,
            rsi_interruptions=self._rsi_interruptions,
            current_task=self._current_task.task_id if self._current_task else None,
            last_idle_time=self._last_idle_time,
            last_task_time=self._last_task_time
        )

    def get_queue_size(self) -> int:
        """Get current queue size."""
        return self._task_queue.qsize()

    def is_idle(self) -> bool:
        """Check if service is in idle mode."""
        return (
            self._mode == ServiceMode.IDLE_RSI and
            self._current_task is None and
            self._task_queue.empty()
        )


async def create_byrd_service(
    memory,
    ralph_loop=None,
    config: Dict = None
) -> BYRDService:
    """
    Create and configure a BYRDService instance.

    Args:
        memory: Memory instance for task storage
        ralph_loop: Optional RalphLoop for RSI
        config: Optional configuration overrides

    Returns:
        Configured BYRDService instance
    """
    service = BYRDService(
        memory=memory,
        ralph_loop=ralph_loop,
        config=config
    )

    return service
