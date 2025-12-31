"""
ralph_loop.py - Interactive Coding Loop (Ralph Loop)

The main loop controller that executes coding tasks until BYRD is satisfied.

Inspired by:
- Oh My OpenCode's Ralph Loop pattern
- Vibe Kanban's task orchestration

Flow:
1. INITIALIZE: Create session, build initial context
2. EXECUTE: Run coder with context
3. VALIDATE: Evaluate satisfaction, extract TODOs
4. DECIDE: Satisfied? Complete. Errors? Recover. Gaps? Refine.
5. REFINE: Build new context, go to step 2
6. FINALIZE: Save transcript, record to memory
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, List

from .task_state import TaskState, TaskStateMachine
from .satisfaction_evaluator import SatisfactionEvaluator, SatisfactionResult
from .session_transcript import SessionTranscript
from .todo_continuation import TodoContinuation
from .error_recovery import ErrorRecovery, ErrorType
from .context_injector import ContextInjector

logger = logging.getLogger(__name__)


@dataclass
class RalphLoopConfig:
    """Configuration for the Ralph Loop."""
    max_turns: int = 10
    satisfaction_threshold: float = 0.8
    enable_todo_continuation: bool = True
    enable_error_recovery: bool = True
    use_llm_evaluation: bool = True
    session_dir: Path = field(default_factory=lambda: Path("coding_sessions"))


@dataclass
class RalphLoopResult:
    """Result of a Ralph Loop execution."""
    success: bool
    turns: int
    final_result: Any  # CoderResult
    satisfaction_score: float
    transcript_path: Optional[Path]
    todos_completed: int = 0
    errors_recovered: int = 0
    state_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "success": self.success,
            "turns": self.turns,
            "satisfaction_score": self.satisfaction_score,
            "transcript_path": str(self.transcript_path) if self.transcript_path else None,
            "todos_completed": self.todos_completed,
            "errors_recovered": self.errors_recovered,
            "state_summary": self.state_summary,
        }


class RalphLoop:
    """
    Interactive coding loop that executes until satisfaction.

    The loop continues until:
    1. Satisfaction threshold is met, OR
    2. Max turns is reached, OR
    3. Unrecoverable error occurs
    """

    def __init__(
        self,
        coder,
        llm_client=None,
        memory=None,
        config: RalphLoopConfig = None,
        event_bus=None,
    ):
        """
        Initialize the Ralph Loop.

        Args:
            coder: OpenCodeCoder instance for executing code
            llm_client: LLM client for evaluation
            memory: Memory instance for context
            config: Loop configuration
            event_bus: Event bus for notifications
        """
        self.coder = coder
        self.llm_client = llm_client
        self.memory = memory
        self.config = config or RalphLoopConfig()
        self.event_bus = event_bus

        # Initialize sub-components
        self.evaluator = SatisfactionEvaluator(
            llm_client=llm_client,
            threshold=self.config.satisfaction_threshold,
        )
        self.transcript = SessionTranscript(session_dir=self.config.session_dir)
        self.todo_handler = TodoContinuation(llm_client=llm_client)
        self.recovery = ErrorRecovery()
        self.context = ContextInjector(memory=memory)
        self.state = TaskStateMachine()

        # Session state
        self._current_session_id: Optional[str] = None
        self._loop_count = 0

    async def execute_until_satisfied(
        self,
        desire: Dict,
        initial_context: Optional[Dict] = None,
    ) -> RalphLoopResult:
        """
        Main entry point - run until BYRD is satisfied.

        Args:
            desire: The desire to fulfill
            initial_context: Optional initial context

        Returns:
            RalphLoopResult with final state
        """
        self._loop_count += 1
        desire_id = desire.get("id", datetime.now().strftime("%Y%m%d%H%M%S"))
        desire_desc = desire.get("description", "Unknown desire")

        # Initialize
        self.state.reset()
        self.recovery.reset()
        self.todo_handler.reset()

        session_id = self.transcript.start_session(desire_id, desire_desc)
        self._current_session_id = session_id

        await self._emit_event("ralph_loop_started", {
            "session_id": session_id,
            "desire_id": desire_id,
            "desire_description": desire_desc,
        })

        # Build initial context
        context = await self.context.build_initial_context(desire)
        if initial_context:
            context.update(initial_context)

        # State: PLANNING -> IMPLEMENTING
        self.state.transition(TaskState.IMPLEMENTING, "initial_execution")
        self.transcript.log_state_transition("planning", "implementing", "initial_execution")

        turn = 0
        last_result = None
        last_evaluation = None
        accumulated_files = []
        turn_history = []

        try:
            while turn < self.config.max_turns:
                turn += 1

                # Build prompt
                prompt = self.context.format_for_prompt(context)

                # Add TODO context if we have pending items
                if self.config.enable_todo_continuation and self.todo_handler.has_pending_todos():
                    todo_summary = self.todo_handler.get_todo_summary()
                    prompt = f"{prompt}\n\n{todo_summary}"

                # Execute turn
                logger.info(f"Ralph Loop turn {turn}/{self.config.max_turns}")
                result = await self.coder.execute(
                    prompt=prompt,
                    desire_id=desire_id,
                )

                # Track files
                accumulated_files.extend(result.files_modified)
                accumulated_files.extend(result.files_created)
                accumulated_files = list(set(accumulated_files))

                # Log turn
                self.transcript.log_turn(turn, prompt[:2000], result)
                turn_history.append({
                    "turn_number": turn,
                    "success": result.success,
                    "files": result.files_modified + result.files_created,
                    "output": result.output[:500] if result.output else "",
                })

                await self._emit_event("ralph_loop_turn", {
                    "session_id": session_id,
                    "turn": turn,
                    "success": result.success,
                    "files_modified": result.files_modified,
                })

                # State: IMPLEMENTING -> VERIFYING
                self.state.transition(TaskState.VERIFYING, f"turn_{turn}_complete")

                # Handle execution failure
                if not result.success:
                    if self.config.enable_error_recovery:
                        recovery_result = await self._attempt_recovery(
                            result, desire, turn
                        )
                        if recovery_result:
                            context = recovery_result
                            continue
                    # Cannot recover
                    break

                # Extract TODOs
                if self.config.enable_todo_continuation:
                    todos = self.todo_handler.extract_todos(result.output, turn)
                    if todos:
                        self.transcript.log_todo_extraction(turn, [t.to_dict() for t in todos])

                # Evaluate satisfaction
                evaluation = await self.evaluator.evaluate(
                    desire=desire,
                    result=result,
                    previous_evaluation=last_evaluation,
                    use_llm=self.config.use_llm_evaluation,
                )

                self.transcript.log_evaluation(turn, evaluation)
                await self._emit_event("ralph_loop_evaluation", {
                    "session_id": session_id,
                    "turn": turn,
                    "satisfaction": evaluation.score,
                    "satisfied": evaluation.satisfied,
                    "gaps": evaluation.gaps,
                })

                last_result = result
                last_evaluation = evaluation

                # Decision point
                if evaluation.satisfied:
                    # SUCCESS!
                    self.state.transition(TaskState.COMPLETE, "satisfied")
                    break

                # Check if we have pending TODOs to complete
                if self.config.enable_todo_continuation and self.todo_handler.has_pending_todos():
                    next_todo = self.todo_handler.get_next_todo()
                    if next_todo:
                        # Mark current as done, work on next
                        self.todo_handler.mark_current_completed(turn)
                        # Context will include TODO in next iteration
                        self.state.transition(TaskState.REFINING, "todo_continuation")
                        context = self.context.build_turn_context(
                            desire=desire,
                            previous_turns=turn_history,
                            gaps=[next_todo.content],
                            current_files=accumulated_files,
                            pending_todos=[t.content for t in self.todo_handler.get_pending_todos()[:3]],
                        )
                        continue

                # Refine based on gaps
                if evaluation.gaps:
                    self.state.transition(TaskState.REFINING, "gaps_identified")
                    self.transcript.log_refinement(
                        turn,
                        evaluation.next_instruction or "Address gaps",
                        {"gaps": evaluation.gaps},
                    )

                    await self._emit_event("ralph_loop_refinement", {
                        "session_id": session_id,
                        "turn": turn,
                        "instruction": evaluation.next_instruction,
                        "gaps": evaluation.gaps,
                    })

                    context = self.context.build_turn_context(
                        desire=desire,
                        previous_turns=turn_history,
                        gaps=evaluation.gaps,
                        current_files=accumulated_files,
                    )

                    # State: REFINING -> IMPLEMENTING
                    self.state.transition(TaskState.IMPLEMENTING, "refinement_prepared")
                else:
                    # No specific gaps, just try again
                    self.state.transition(TaskState.REFINING, "generic_refinement")
                    context = self.context.build_turn_context(
                        desire=desire,
                        previous_turns=turn_history,
                        gaps=["Complete any remaining work"],
                        current_files=accumulated_files,
                    )
                    self.state.transition(TaskState.IMPLEMENTING, "retry")

            # End of loop
            if not self.state.is_terminal():
                if turn >= self.config.max_turns:
                    self.state.transition(TaskState.FAILED, "max_turns_reached")
                else:
                    self.state.transition(TaskState.FAILED, "loop_exited")

        except Exception as e:
            logger.error(f"Ralph Loop error: {e}")
            self.state.transition(TaskState.FAILED, f"exception: {str(e)[:50]}")

        # Finalize
        final_satisfaction = last_evaluation.score if last_evaluation else 0.0
        success = self.state.is_successful()

        self.transcript.end_session(
            success=success,
            final_satisfaction=final_satisfaction,
            summary=self.state.get_summary(),
        )

        await self._emit_event("ralph_loop_complete" if success else "ralph_loop_failed", {
            "session_id": session_id,
            "success": success,
            "turns": turn,
            "satisfaction": final_satisfaction,
        })

        # Record to memory
        if self.memory and last_result:
            await self._record_to_memory(desire, last_result, success, turn)

        result = RalphLoopResult(
            success=success,
            turns=turn,
            final_result=last_result,
            satisfaction_score=final_satisfaction,
            transcript_path=self.transcript.get_session_path(),
            todos_completed=len(self.todo_handler.get_completed_todos()),
            errors_recovered=self.recovery.get_stats()["total_attempts"],
            state_summary=self.state.get_summary(),
        )

        return result

    async def _attempt_recovery(
        self,
        result: Any,
        desire: Dict,
        turn: int,
    ) -> Optional[Dict]:
        """
        Attempt to recover from an error.

        Returns new context if recovery is possible, None otherwise.
        """
        error = result.error or "Unknown error"
        error_type = self.recovery.analyze_error(error, result.output)

        self.transcript.log_error_recovery(
            turn_number=turn,
            error_type=error_type,
            recovery_strategy="pending",
            recovered=False,
        )

        if not self.recovery.can_recover(error_type):
            return None

        # State: VERIFYING -> RECOVERING
        self.state.transition(TaskState.RECOVERING, f"error_{error_type}")

        recovery = await self.recovery.recover(
            error_type=error_type,
            original_prompt="",  # We'll use context instead
            error=error,
            output=result.output,
        )

        if recovery.wait_seconds > 0:
            logger.info(f"Waiting {recovery.wait_seconds}s before retry")
            await asyncio.sleep(recovery.wait_seconds)

        self.transcript.log_error_recovery(
            turn_number=turn,
            error_type=error_type,
            recovery_strategy=recovery.strategy_used,
            recovered=recovery.recovered,
        )

        if recovery.recovered and recovery.should_retry:
            # Build recovery context
            context = self.context.build_error_context(
                desire=desire,
                error_type=error_type,
                error_message=error,
                recovery_strategy=recovery.strategy_used,
                previous_output=result.output,
            )

            # State: RECOVERING -> IMPLEMENTING
            self.state.transition(TaskState.IMPLEMENTING, "recovery_prepared")
            return context

        return None

    async def _record_to_memory(
        self,
        desire: Dict,
        result: Any,
        success: bool,
        turns: int,
    ):
        """Record session outcome to memory."""
        try:
            status = "SUCCESS" if success else "PARTIAL"
            content = (
                f"[INTERACTIVE_CODING] {status}: {desire.get('description', '')[:100]}\n"
                f"Turns: {turns}, Files: {', '.join(result.files_modified[:5])}"
            )

            await self.memory.record_experience(
                content=content,
                type="interactive_coding",
            )

        except Exception as e:
            logger.warning(f"Failed to record to memory: {e}")

    async def _emit_event(self, event_type: str, data: Dict):
        """Emit event to event bus if available."""
        if self.event_bus:
            try:
                from event_bus import Event, EventType

                # Map to EventType enum if possible
                type_mapping = {
                    "ralph_loop_started": EventType.RALPH_LOOP_STARTED,
                    "ralph_loop_turn": EventType.RALPH_LOOP_TURN,
                    "ralph_loop_evaluation": EventType.RALPH_LOOP_EVALUATION,
                    "ralph_loop_refinement": EventType.RALPH_LOOP_REFINEMENT,
                    "ralph_loop_complete": EventType.RALPH_LOOP_COMPLETE,
                    "ralph_loop_failed": EventType.RALPH_LOOP_FAILED,
                }

                if event_type in type_mapping:
                    await self.event_bus.emit(Event(
                        type=type_mapping[event_type],
                        data=data,
                    ))
            except Exception as e:
                logger.debug(f"Event emission failed: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get loop statistics."""
        return {
            "loop_count": self._loop_count,
            "current_session": self._current_session_id,
            "evaluator": self.evaluator.get_stats(),
            "recovery": self.recovery.get_stats(),
            "todos": self.todo_handler.get_stats(),
        }

    def reset(self):
        """Reset loop state."""
        self.state.reset()
        self.recovery.reset()
        self.todo_handler.reset()
        self.transcript.reset()
        self._current_session_id = None


# Convenience function
def create_ralph_loop(
    coder,
    llm_client=None,
    memory=None,
    config: Dict = None,
    event_bus=None,
) -> RalphLoop:
    """Create a new RalphLoop instance."""
    loop_config = RalphLoopConfig(
        max_turns=config.get("max_turns", 10) if config else 10,
        satisfaction_threshold=config.get("satisfaction_threshold", 0.8) if config else 0.8,
        enable_todo_continuation=config.get("todo_continuation", True) if config else True,
        enable_error_recovery=config.get("error_recovery", True) if config else True,
        use_llm_evaluation=config.get("use_llm_evaluation", True) if config else True,
    )

    return RalphLoop(
        coder=coder,
        llm_client=llm_client,
        memory=memory,
        config=loop_config,
        event_bus=event_bus,
    )
