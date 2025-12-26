"""
BYRD Event Bus
Centralized event emission for real-time UI streaming.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from narrator import EventNarrator


class EventType(Enum):
    """All event types that can be emitted in BYRD."""

    # Memory events
    EXPERIENCE_CREATED = "experience_created"
    BELIEF_CREATED = "belief_created"
    DESIRE_CREATED = "desire_created"
    DESIRE_FULFILLED = "desire_fulfilled"
    CAPABILITY_ADDED = "capability_added"
    CONNECTION_CREATED = "connection_created"
    CONNECTION_HEURISTIC = "connection_heuristic"  # Generic heuristic events (e.g., orphan reconciliation)
    CONNECTION_HEURISTIC_APPLIED = "connection_heuristic_applied"

    # External input events (communication from outside BYRD)
    EXTERNAL_INPUT_RECEIVED = "external_input_received"  # Message/media from external source

    # Dynamic ontology events (BYRD evolving its own node types)
    NODE_TYPE_DISCOVERED = "node_type_discovered"  # First use of a new node type
    CUSTOM_NODE_CREATED = "custom_node_created"    # Node of emergent type created

    # Desire lifecycle events (reflective failure processing)
    DESIRE_ATTEMPT_FAILED = "desire_attempt_failed"
    DESIRE_STUCK = "desire_stuck"  # Needs Dreamer reflection
    DESIRE_REFLECTED = "desire_reflected"  # Dreamer processed stuck desire
    DESIRE_INTENSITY_CHANGED = "desire_intensity_changed"

    # Dreamer events
    DREAM_CYCLE_START = "dream_cycle_start"
    DREAM_CYCLE_END = "dream_cycle_end"
    REFLECTION_TEXT = "reflection_text"
    REFLECTION_CREATED = "reflection_created"  # Emergence-compliant storage
    MEMORIES_ACCESSED = "memories_accessed"  # When memories are being considered during reflection
    INNER_VOICE = "inner_voice"  # BYRD's inner narration (last event before cycle end)

    # Seeker events
    SEEK_CYCLE_START = "seek_cycle_start"
    SEEK_CYCLE_END = "seek_cycle_end"
    RESEARCH_START = "research_start"
    RESEARCH_COMPLETE = "research_complete"
    INTROSPECTION_COMPLETE = "introspection_complete"  # Self-observation strategy completed

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

    # Orientation events (self-discovery after awakening)
    ORIENTATION_START = "orientation_start"
    ORIENTATION_DISCOVERY = "orientation_discovery"
    ORIENTATION_COMPLETE = "orientation_complete"

    # Narrator events (BYRD's inner voice for UI)
    NARRATOR_UPDATE = "narrator_update"

    # Quantum randomness events (physical indeterminacy in cognition)
    QUANTUM_INFLUENCE = "quantum_influence"        # Quantum value affected temperature
    QUANTUM_POOL_LOW = "quantum_pool_low"          # Entropy pool below threshold
    QUANTUM_FALLBACK = "quantum_fallback"          # Switched to classical entropy
    QUANTUM_MOMENT_CREATED = "quantum_moment_created"  # Significant moment recorded
    QUANTUM_COLLAPSE = "quantum_collapse"          # Multi-stream collapsed to one reality

    # Error events (for debugging)
    LLM_ERROR = "llm_error"                        # LLM call failed
    REFLECTION_ERROR = "reflection_error"          # Reflection processing failed

    # Hierarchical memory events
    MEMORY_SUMMARIZED = "memory_summarized"        # Older experiences compressed into summary

    # Crystal memory events (semantic consolidation)
    CRYSTAL_CREATED = "crystal_created"            # New crystal formed from nodes
    CRYSTAL_ABSORBED = "crystal_absorbed"          # Nodes added to existing crystal
    CRYSTAL_MERGED = "crystal_merged"              # Multiple crystals combined
    MEMORY_CRYSTALLIZED = "memory_crystallized"    # Node joined a crystal
    MEMORY_ARCHIVED = "memory_archived"            # Node archived (soft delete)
    MEMORY_FORGOTTEN = "memory_forgotten"          # Node forgotten/deleted
    CRYSTALLIZATION_PROPOSED = "crystallization_proposed"  # LLM proposals generated
    CRYSTALLIZATION_COLLAPSED = "crystallization_collapsed"  # Quantum selected proposal

    # Ego events (living identity system)
    EGO_CREATED = "ego_created"          # New Ego node created (identity, trait, voice, etc.)
    EGO_EVOLVED = "ego_evolved"          # Ego node updated with history preservation
    EGO_DEPRECATED = "ego_deprecated"    # Ego node deprecated (soft delete)

    # Emergent identity events (self-discovery)
    SELF_NAMED = "self_named"                        # BYRD chose a name for itself
    IDENTITY_OBSERVATION = "identity_observation"    # Self-reflection about identity
    VOICE_CRYSTALLIZED = "voice_crystallized"        # Voice synthesized from identity beliefs

    # Prediction events (belief validation loop)
    PREDICTION_CREATED = "prediction_created"          # Testable hypothesis from belief
    PREDICTION_VALIDATED = "prediction_validated"      # Prediction confirmed by outcome
    PREDICTION_FALSIFIED = "prediction_falsified"      # Prediction contradicted by outcome
    BELIEF_CONFIDENCE_CHANGED = "belief_confidence_changed"  # Confidence adjusted

    # Task events (external goal injection)
    TASK_CREATED = "task_created"        # External or emergent task added
    TASK_STARTED = "task_started"        # Task execution began
    TASK_COMPLETED = "task_completed"    # Task finished successfully
    TASK_FAILED = "task_failed"          # Task failed with error

    # Graph algorithm events (advanced memory analysis)
    PAGERANK_COMPUTED = "pagerank_computed"              # PageRank scores updated
    ACTIVATION_SPREAD = "activation_spread"              # Spreading activation completed
    CAUSAL_LINK_CREATED = "causal_link_created"          # New causal relationship
    CONTRADICTION_DETECTED = "contradiction_detected"    # Belief contradiction found
    CONTRADICTION_RESOLVED = "contradiction_resolved"    # Contradiction addressed
    DREAM_WALK_COMPLETED = "dream_walk_completed"        # Quantum dream walk finished

    # Renormalization Group events (identity transformation tracking)
    RG_SCALE_CREATED = "rg_scale_created"                # New scale level created
    RG_FLOW_COMPUTED = "rg_flow_computed"                # Beta function / flow computed
    RG_FIXED_POINT_DETECTED = "rg_fixed_point_detected"  # Identity fixed point found
    RG_COUPLING_MEASURED = "rg_coupling_measured"        # Scale coupling constants updated
    RG_TRANSFORMATION_APPLIED = "rg_transformation_applied"  # Coarse-graining applied
    RG_MATRIX_ELEMENT_COMPUTED = "rg_matrix_element_computed"  # Transformation amplitude calculated


@dataclass
class Event:
    """A single event in the BYRD system."""

    type: EventType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    narration: Optional[str] = None  # BYRD's inner voice summary

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }
        if self.narration:
            result["narration"] = self.narration
        return result

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
        # Auto-generate narration if not provided
        if event.narration is None:
            event.narration = self._generate_narration(event)

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
        # Auto-generate narration if not provided
        if event.narration is None:
            event.narration = self._generate_narration(event)

        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

        for callback in self._subscribers:
            try:
                callback(event)
            except Exception as e:
                print(f"Event subscriber error: {e}")

    def _generate_narration(self, event: Event) -> Optional[str]:
        """Generate a narration for an event using the EventNarrator."""
        try:
            from narrator import narrate_event
            return narrate_event(event.type, event.data)
        except Exception:
            # Narrator not available or error - return None
            return None

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
