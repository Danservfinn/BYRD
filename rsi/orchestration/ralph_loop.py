"""
RalphLoop - Iterative orchestration framework for BYRD's RSI cycle.

Runs RSI cycles until genuine emergence is detected or resource limits exhausted.
One Ralph iteration = one complete RSI cycle + consciousness frame + emergence check.

Implements the Ralph Wiggum loop methodology:
- Read (context) → Execute (RSI cycle) → Check (emergence) → Repeat

See docs/IMPLEMENTATION_PLAN_ASI.md Section 1.1 for specification.
"""

from typing import Dict, Optional, List, Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
import time
import asyncio
import subprocess
import logging
from datetime import datetime, timezone

from .ralph_adapter import BYRDRalphAdapter, RalphIterationResult
from .emergence_detector import EmergenceDetector, EmergenceResult

if TYPE_CHECKING:
    from ..engine import RSIEngine
    from ..consciousness.stream import ConsciousnessStream

logger = logging.getLogger("rsi.orchestration.ralph_loop")


class LoopTerminationReason(Enum):
    """Why the loop terminated."""
    EMERGENCE_DETECTED = "emergence_detected"
    MAX_ITERATIONS = "max_iterations"
    MAX_COST = "max_cost"
    MAX_TIME = "max_time"
    ERROR = "error"
    MANUAL_STOP = "manual_stop"


@dataclass
class LoopResult:
    """Result of running the RalphLoop to completion."""
    terminated: bool
    reason: LoopTerminationReason
    iterations_completed: int
    final_emergence: Optional[EmergenceResult]
    total_time_seconds: float
    total_cost_usd: float
    total_tokens: int
    checkpoints_created: int
    iteration_history: List[Dict] = field(default_factory=list)
    error_message: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'terminated': self.terminated,
            'reason': self.reason.value,
            'iterations_completed': self.iterations_completed,
            'final_emergence': {
                'emerged': self.final_emergence.emerged,
                'reason': self.final_emergence.reason,
                'confidence': self.final_emergence.confidence
            } if self.final_emergence else None,
            'total_time_seconds': self.total_time_seconds,
            'total_cost_usd': self.total_cost_usd,
            'total_tokens': self.total_tokens,
            'checkpoints_created': self.checkpoints_created,
            'error_message': self.error_message
        }


class RalphLoop:
    """
    Iterates RSI cycles until genuine emergence is detected.

    One Ralph iteration = one complete RSI cycle + consciousness frame.

    Resource limits prevent runaway execution:
    - max_iterations: Hard limit on cycle count
    - max_cost_usd: Cost ceiling based on LLM usage
    - max_time_seconds: Wall-clock time limit

    Git checkpointing preserves progress and enables rollback.
    """

    def __init__(
        self,
        rsi_engine: "RSIEngine",
        consciousness_stream: "ConsciousnessStream",
        emergence_detector: Optional[EmergenceDetector] = None,
        config: Dict = None
    ):
        """
        Initialize RalphLoop.

        Args:
            rsi_engine: BYRD's RSI engine for running cycles
            consciousness_stream: ConsciousnessStream for frame storage
            emergence_detector: Optional custom detector (creates default if None)
            config: Configuration dict with keys:
                - checkpoint_interval: Iterations between git commits (default: 5)
                - checkpoint_enabled: Whether to create git checkpoints (default: True)
                - checkpoint_tag_prefix: Git tag prefix (default: "ralph-checkpoint")
                - emergence_threshold: Confidence threshold for emergence (default: 0.9)
        """
        self.rsi = rsi_engine
        self.consciousness = consciousness_stream
        self.config = config or {}

        # Create adapter (bridges RSI to Ralph methodology)
        self.adapter = BYRDRalphAdapter(
            rsi_engine=rsi_engine,
            consciousness=consciousness_stream,
            config=self.config
        )

        # Use provided detector or adapter's
        self.emergence_detector = emergence_detector or self.adapter.emergence_detector

        # Configuration
        self._checkpoint_interval = self.config.get('checkpoint_interval', 5)
        self._checkpoint_enabled = self.config.get('checkpoint_enabled', True)
        self._checkpoint_tag_prefix = self.config.get('checkpoint_tag_prefix', 'ralph-checkpoint')

        # State
        self._running = False
        self._stop_requested = False
        self._iteration_count = 0
        self._checkpoints_created = 0
        self._start_time: Optional[float] = None
        self._total_cost = 0.0
        self._total_tokens = 0
        self._iteration_history: List[Dict] = []
        self._last_emergence: Optional[EmergenceResult] = None

    async def run(
        self,
        max_iterations: int = 1000,
        max_cost_usd: float = 50.0,
        max_time_seconds: int = 14400  # 4 hours default
    ) -> LoopResult:
        """
        Run the loop until emergence or resource exhaustion.

        Args:
            max_iterations: Maximum number of RSI cycles to run
            max_cost_usd: Maximum USD cost (based on LLM token pricing)
            max_time_seconds: Maximum wall-clock time in seconds

        Returns:
            LoopResult with termination reason and statistics
        """
        if self._running:
            raise RuntimeError("RalphLoop is already running")

        self._running = True
        self._stop_requested = False
        self._start_time = time.time()
        self._iteration_count = 0
        self._checkpoints_created = 0
        self._total_cost = 0.0
        self._total_tokens = 0
        self._iteration_history = []

        logger.info(
            f"RalphLoop starting: max_iterations={max_iterations}, "
            f"max_cost=${max_cost_usd}, max_time={max_time_seconds}s"
        )

        try:
            while self._iteration_count < max_iterations:
                # Check stop conditions
                if self._stop_requested:
                    return self._create_result(LoopTerminationReason.MANUAL_STOP)

                elapsed = time.time() - self._start_time
                if elapsed >= max_time_seconds:
                    logger.info(f"Time limit reached: {elapsed:.1f}s >= {max_time_seconds}s")
                    return self._create_result(LoopTerminationReason.MAX_TIME)

                if self._total_cost >= max_cost_usd:
                    logger.info(f"Cost limit reached: ${self._total_cost:.2f} >= ${max_cost_usd}")
                    return self._create_result(LoopTerminationReason.MAX_COST)

                # Execute one iteration
                result = await self.iterate()

                # Check for emergence
                if result.completed:
                    logger.info(
                        f"Emergence detected at iteration {self._iteration_count}: "
                        f"{result.emergence_result.reason}"
                    )
                    return self._create_result(LoopTerminationReason.EMERGENCE_DETECTED)

                # Checkpoint if needed
                if result.should_checkpoint and self._checkpoint_enabled:
                    await self.checkpoint()

        except Exception as e:
            logger.exception(f"RalphLoop error at iteration {self._iteration_count}")
            result = self._create_result(LoopTerminationReason.ERROR)
            result.error_message = str(e)
            return result

        finally:
            self._running = False

        # Exhausted max_iterations
        logger.info(f"Max iterations reached: {self._iteration_count}")
        return self._create_result(LoopTerminationReason.MAX_ITERATIONS)

    async def iterate(self) -> RalphIterationResult:
        """
        Execute one iteration: RSI cycle → frame → emergence check.

        This is the core loop body:
        1. Run one complete RSI cycle via the adapter
        2. Adapter writes consciousness frame
        3. Adapter checks for emergence
        4. Track resource usage

        Returns:
            RalphIterationResult with cycle result and emergence status
        """
        self._iteration_count += 1

        logger.debug(f"Starting iteration {self._iteration_count}")

        # Execute via adapter (handles RSI + frame + emergence)
        result = await self.adapter.execute(
            context={
                'loop_iteration': self._iteration_count,
                'elapsed_seconds': time.time() - self._start_time if self._start_time else 0,
                'cost_so_far': self._total_cost
            }
        )

        # Update tracking
        self._total_tokens += result.resource_usage.get('tokens_this_iteration', 0)
        # Estimate cost: ~$0.01 per 1K tokens (varies by model)
        self._total_cost += result.resource_usage.get('tokens_this_iteration', 0) * 0.00001

        self._last_emergence = result.emergence_result

        # Store in history (keep summary, not full result)
        self._iteration_history.append({
            'iteration': self._iteration_count,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'phase_reached': str(result.cycle_result.phase_reached) if result.cycle_result else None,
            'emerged': result.emergence_result.emerged,
            'emergence_confidence': result.emergence_result.confidence,
            'resource_usage': result.resource_usage
        })

        return result

    async def checkpoint(self) -> None:
        """
        Create git checkpoint of current state.

        Creates a git commit with current changes and optionally a tag.
        This enables rollback if emergence detection proves to be a false positive.
        """
        if not self._checkpoint_enabled:
            return

        self._checkpoints_created += 1
        tag_name = f"{self._checkpoint_tag_prefix}-{self._iteration_count}"

        logger.info(f"Creating checkpoint: {tag_name}")

        try:
            # Stage all changes
            subprocess.run(
                ['git', 'add', '-A'],
                capture_output=True,
                timeout=30
            )

            # Commit with message
            commit_msg = (
                f"chore(ralph): checkpoint at iteration {self._iteration_count}\n\n"
                f"Emergence confidence: {self._last_emergence.confidence if self._last_emergence else 0:.2f}\n"
                f"Total cost: ${self._total_cost:.2f}\n"
                f"Total time: {time.time() - self._start_time if self._start_time else 0:.1f}s"
            )

            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg, '--allow-empty'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                logger.debug(f"Git commit output: {result.stderr}")

            # Create tag
            subprocess.run(
                ['git', 'tag', '-a', tag_name, '-m', f'Ralph checkpoint at iteration {self._iteration_count}'],
                capture_output=True,
                timeout=30
            )

            logger.info(f"Checkpoint created: {tag_name}")

        except subprocess.TimeoutExpired:
            logger.warning("Git checkpoint timed out")
        except Exception as e:
            logger.warning(f"Failed to create checkpoint: {e}")

    def stop(self) -> None:
        """Request the loop to stop after current iteration."""
        self._stop_requested = True
        logger.info("Stop requested for RalphLoop")

    def get_stats(self) -> Dict:
        """Return loop statistics."""
        elapsed = time.time() - self._start_time if self._start_time else 0

        return {
            'running': self._running,
            'iterations_completed': self._iteration_count,
            'elapsed_seconds': elapsed,
            'total_cost_usd': self._total_cost,
            'total_tokens': self._total_tokens,
            'checkpoints_created': self._checkpoints_created,
            'last_emergence': {
                'emerged': self._last_emergence.emerged,
                'confidence': self._last_emergence.confidence,
                'reason': self._last_emergence.reason
            } if self._last_emergence else None,
            'adapter_stats': self.adapter.get_stats()
        }

    def reset(self) -> None:
        """Reset loop state for reuse."""
        if self._running:
            raise RuntimeError("Cannot reset while running")

        self._iteration_count = 0
        self._checkpoints_created = 0
        self._start_time = None
        self._total_cost = 0.0
        self._total_tokens = 0
        self._iteration_history = []
        self._last_emergence = None
        self._stop_requested = False

        self.adapter.reset()

        logger.info("RalphLoop reset")

    def _create_result(self, reason: LoopTerminationReason) -> LoopResult:
        """Create a LoopResult with current state."""
        return LoopResult(
            terminated=True,
            reason=reason,
            iterations_completed=self._iteration_count,
            final_emergence=self._last_emergence,
            total_time_seconds=time.time() - self._start_time if self._start_time else 0,
            total_cost_usd=self._total_cost,
            total_tokens=self._total_tokens,
            checkpoints_created=self._checkpoints_created,
            iteration_history=self._iteration_history[-10:]  # Keep last 10 for brevity
        )


async def run_ralph_loop(
    rsi_engine: "RSIEngine",
    consciousness_stream: "ConsciousnessStream",
    max_iterations: int = 1000,
    max_cost_usd: float = 50.0,
    max_time_seconds: int = 14400,
    config: Dict = None
) -> LoopResult:
    """
    Convenience function to run the Ralph loop.

    Args:
        rsi_engine: BYRD's RSI engine
        consciousness_stream: ConsciousnessStream for frame storage
        max_iterations: Maximum RSI cycles
        max_cost_usd: Maximum cost in USD
        max_time_seconds: Maximum wall-clock time
        config: Optional configuration overrides

    Returns:
        LoopResult with termination reason and statistics
    """
    loop = RalphLoop(
        rsi_engine=rsi_engine,
        consciousness_stream=consciousness_stream,
        config=config
    )

    return await loop.run(
        max_iterations=max_iterations,
        max_cost_usd=max_cost_usd,
        max_time_seconds=max_time_seconds
    )
