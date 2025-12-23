"""
BYRD Event Bus
Centralized event emission for real-time UI streaming.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class EventType(Enum):
    """All event types that can be emitted in BYRD."""

    # Memory events
    EXPERIENCE_CREATED = "experience_created"
    BELIEF_CREATED = "belief_created"
    DESIRE_CREATED = "desire_created"
    DESIRE_FULFILLED = "desire_fulfilled"
    CAPABILITY_ADDED = "capability_added"
    CONNECTION_CREATED = "connection_created"

    # Dreamer events
    DREAM_CYCLE_START = "dream_cycle_start"
    DREAM_CYCLE_END = "dream_cycle_end"
    REFLECTION_TEXT = "reflection_text"

    # Seeker events
    SEEK_CYCLE_START = "seek_cycle_start"
    SEEK_CYCLE_END = "seek_cycle_end"
    RESEARCH_START = "research_start"
    RESEARCH_COMPLETE = "research_complete"

    # Self-modification events
    MODIFICATION_PROPOSED = "modification_proposed"
    MODIFICATION_EXECUTED = "modification_executed"
    MODIFICATION_BLOCKED = "modification_blocked"

    # Coder events (Claude Code CLI)
    CODER_INVOKED = "coder_invoked"
    CODER_COMPLETE = "coder_complete"
    CODER_FAILED = "coder_failed"
    CODER_VALIDATION_FAILED = "coder_validation_failed"

    # System events
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"
    SYSTEM_RESET = "system_reset"
    AWAKENING = "awakening"


@dataclass
class Event:
    """A single event in the BYRD system."""

    type: EventType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


class EventBus:
    """
    Singleton event bus for BYRD.

    All components emit events here; WebSocket connections subscribe
    to receive real-time updates.
    """

    _instance: Optional["EventBus"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._subscribers: List[Callable[[Event], None]] = []
        self._async_subscribers: List[Callable[[Event], Any]] = []
        self._history: List[Event] = []
        self._max_history = 1000

    def subscribe(self, callback: Callable[[Event], None]):
        """Subscribe a sync callback to all events."""
        self._subscribers.append(callback)

    def subscribe_async(self, callback: Callable[[Event], Any]):
        """Subscribe an async callback to all events."""
        self._async_subscribers.append(callback)

    def unsubscribe(self, callback):
        """Remove a subscriber."""
        if callback in self._subscribers:
            self._subscribers.remove(callback)
        if callback in self._async_subscribers:
            self._async_subscribers.remove(callback)

    async def emit(self, event: Event):
        """Emit an event to all subscribers."""
        # Store in history
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

        # Notify sync subscribers
        for callback in self._subscribers:
            try:
                callback(event)
            except Exception as e:
                print(f"Event subscriber error: {e}")

        # Notify async subscribers
        for callback in self._async_subscribers:
            try:
                await callback(event)
            except Exception as e:
                print(f"Async event subscriber error: {e}")

    def emit_sync(self, event: Event):
        """Emit event synchronously (for non-async contexts)."""
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

        for callback in self._subscribers:
            try:
                callback(event)
            except Exception as e:
                print(f"Event subscriber error: {e}")

    def get_history(
        self,
        limit: int = 100,
        event_types: Optional[List[EventType]] = None
    ) -> List[Event]:
        """Get recent event history, optionally filtered by type."""
        history = self._history
        if event_types:
            history = [e for e in history if e.type in event_types]
        return history[-limit:]

    def clear_history(self):
        """Clear event history (used on reset)."""
        self._history = []


# Global singleton instance
event_bus = EventBus()
