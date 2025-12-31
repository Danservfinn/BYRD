"""
interactive_coder - Interactive OpenCode CLI System for BYRD

Implements the Ralph Loop pattern for multi-turn coding interactions
until BYRD is satisfied with the result.

Components:
- RalphLoop: Main loop controller (execute until satisfied)
- SatisfactionEvaluator: Multi-method output evaluation
- SessionTranscript: JSONL session logging
- TodoContinuation: Extract and complete TODOs
- ErrorRecovery: Automatic error recovery
- ContextInjector: Context building for turns
- TaskStateMachine: State tracking
"""

from .task_state import TaskState, TaskStateMachine, StateTransition
from .satisfaction_evaluator import SatisfactionEvaluator, SatisfactionResult
from .session_transcript import SessionTranscript
from .todo_continuation import TodoContinuation, ExtractedTodo
from .error_recovery import ErrorRecovery, RecoveryResult
from .context_injector import ContextInjector
from .ralph_loop import RalphLoop, RalphLoopConfig, RalphLoopResult

__all__ = [
    # Core loop
    "RalphLoop",
    "RalphLoopConfig",
    "RalphLoopResult",
    # State machine
    "TaskState",
    "TaskStateMachine",
    "StateTransition",
    # Evaluation
    "SatisfactionEvaluator",
    "SatisfactionResult",
    # Session management
    "SessionTranscript",
    # TODO handling
    "TodoContinuation",
    "ExtractedTodo",
    # Error recovery
    "ErrorRecovery",
    "RecoveryResult",
    # Context
    "ContextInjector",
]
