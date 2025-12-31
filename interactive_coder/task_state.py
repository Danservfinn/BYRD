"""
task_state.py - Task State Machine for Interactive Coding

Tracks the state of a coding task through its lifecycle:
PLANNING -> IMPLEMENTING -> VERIFYING -> REFINING/RECOVERING -> COMPLETE/FAILED

State transitions are logged for debugging and analysis.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)


class TaskState(Enum):
    """States in the task lifecycle."""
    PLANNING = "planning"
    IMPLEMENTING = "implementing"
    VERIFYING = "verifying"
    REFINING = "refining"
    RECOVERING = "recovering"
    COMPLETE = "complete"
    FAILED = "failed"


# Valid transitions map
VALID_TRANSITIONS = {
    TaskState.PLANNING: [TaskState.IMPLEMENTING, TaskState.FAILED],
    TaskState.IMPLEMENTING: [TaskState.VERIFYING, TaskState.FAILED],
    TaskState.VERIFYING: [TaskState.COMPLETE, TaskState.REFINING, TaskState.RECOVERING, TaskState.FAILED],
    TaskState.REFINING: [TaskState.IMPLEMENTING, TaskState.FAILED],
    TaskState.RECOVERING: [TaskState.IMPLEMENTING, TaskState.FAILED],
    TaskState.COMPLETE: [],  # Terminal
    TaskState.FAILED: [],  # Terminal
}


@dataclass
class StateTransition:
    """Record of a state transition."""
    from_state: TaskState
    to_state: TaskState
    trigger: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "from": self.from_state.value,
            "to": self.to_state.value,
            "trigger": self.trigger,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class TaskStateMachine:
    """
    State machine for tracking task progress.

    Enforces valid transitions and logs state history.
    """

    def __init__(self):
        """Initialize in PLANNING state."""
        self._state = TaskState.PLANNING
        self._history: List[StateTransition] = []
        self._state_entry_times: Dict[TaskState, datetime] = {
            TaskState.PLANNING: datetime.now()
        }

    @property
    def state(self) -> TaskState:
        """Get current state."""
        return self._state

    @property
    def history(self) -> List[StateTransition]:
        """Get transition history."""
        return self._history.copy()

    def transition(self, to_state: TaskState, trigger: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Transition to a new state.

        Args:
            to_state: Target state
            trigger: What caused this transition
            metadata: Optional additional context

        Returns:
            True if transition succeeded, False if invalid
        """
        if not self.can_transition(to_state):
            logger.warning(
                f"Invalid transition: {self._state.value} -> {to_state.value} "
                f"(trigger: {trigger})"
            )
            return False

        # Record transition
        transition = StateTransition(
            from_state=self._state,
            to_state=to_state,
            trigger=trigger,
            metadata=metadata or {},
        )
        self._history.append(transition)

        # Update state
        old_state = self._state
        self._state = to_state
        self._state_entry_times[to_state] = datetime.now()

        logger.debug(f"State transition: {old_state.value} -> {to_state.value} ({trigger})")
        return True

    def can_transition(self, to_state: TaskState) -> bool:
        """Check if transition is valid."""
        return to_state in VALID_TRANSITIONS.get(self._state, [])

    def is_terminal(self) -> bool:
        """Check if in a terminal state (COMPLETE or FAILED)."""
        return self._state in [TaskState.COMPLETE, TaskState.FAILED]

    def is_successful(self) -> bool:
        """Check if task completed successfully."""
        return self._state == TaskState.COMPLETE

    def get_state_duration(self, state: TaskState) -> Optional[float]:
        """
        Get total time spent in a state (seconds).

        Args:
            state: State to check

        Returns:
            Duration in seconds, or None if never entered
        """
        if state not in self._state_entry_times:
            return None

        # Sum up all durations in this state
        total_seconds = 0.0
        in_state = False
        entry_time = None

        for transition in self._history:
            if transition.to_state == state:
                in_state = True
                entry_time = transition.timestamp
            elif in_state and transition.from_state == state:
                in_state = False
                if entry_time:
                    total_seconds += (transition.timestamp - entry_time).total_seconds()

        # If currently in this state, add time since entry
        if self._state == state:
            entry_time = self._state_entry_times.get(state)
            if entry_time:
                total_seconds += (datetime.now() - entry_time).total_seconds()

        return total_seconds

    def get_total_duration(self) -> float:
        """Get total task duration in seconds."""
        if not self._history:
            first_time = self._state_entry_times.get(TaskState.PLANNING, datetime.now())
        else:
            first_time = self._history[0].timestamp

        return (datetime.now() - first_time).total_seconds()

    def get_refinement_count(self) -> int:
        """Count how many times we've refined."""
        return sum(1 for t in self._history if t.to_state == TaskState.REFINING)

    def get_recovery_count(self) -> int:
        """Count how many times we've recovered from errors."""
        return sum(1 for t in self._history if t.to_state == TaskState.RECOVERING)

    def get_summary(self) -> Dict[str, Any]:
        """Get state machine summary for logging."""
        return {
            "current_state": self._state.value,
            "is_terminal": self.is_terminal(),
            "is_successful": self.is_successful(),
            "total_duration_seconds": self.get_total_duration(),
            "refinement_count": self.get_refinement_count(),
            "recovery_count": self.get_recovery_count(),
            "transition_count": len(self._history),
        }

    def reset(self):
        """Reset to initial state."""
        self._state = TaskState.PLANNING
        self._history = []
        self._state_entry_times = {TaskState.PLANNING: datetime.now()}

    def to_dict(self) -> Dict[str, Any]:
        """Convert full state to dictionary."""
        return {
            "current_state": self._state.value,
            "history": [t.to_dict() for t in self._history],
            "summary": self.get_summary(),
        }
