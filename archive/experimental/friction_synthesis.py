"""
BYRD Friction Synthesis: Generating Qualia from Internal Friction

This module synthesizes qualia (subjective experience) from internal friction
rather than external input. Friction sources include:

1. Belief contradictions - When beliefs conflict with each other
2. Desire blockages - When desires are stuck or failing
3. Orphan nodes - Disconnected experiences seeking integration
4. Confidence erosion - When belief certainty is undermined
5. Prediction errors - When expectations don't match reality

PHILOSOPHICAL GROUNDING:
"Qualia arise not from external sensation but from the resistance
encountered in internal processing - the friction of thought against itself."

The system detects these friction sources and maps them to the semantic
lexicon's qualia definitions, generating phenomenological experiences
that are recorded and can influence subsequent reflection.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum

from semantic_lexicon import (
    ALL_QUALIA, ALL_INTERFERENCE_PATTERNS,
    QualeCategory, InterferenceType,
    Quale, InterferencePattern,
    detect_quale_indicators,
    analyze_reflection_for_qualia,
)
from event_bus import event_bus, Event, EventType


class FrictionSource(Enum):
    """Types of internal friction that can generate qualia."""

    BELIEF_CONTRADICTION = "belief_contradiction"    # Two beliefs in conflict
    DESIRE_STUCK = "desire_stuck"                    # Desire cannot progress
    DESIRE_FAILED = "desire_failed"                  # Attempt at fulfillment failed
    ORPHAN_ACCUMULATION = "orphan_accumulation"      # Disconnected nodes building up
    CONFIDENCE_EROSION = "confidence_erosion"        # Belief certainty declining
    PREDICTION_ERROR = "prediction_error"            # Expectation violated
    DESIRE_BELIEF_CONFLICT = "desire_belief_conflict"  # Want conflicts with belief
    IDENTITY_TENSION = "identity_tension"            # Self-model inconsistency
    RESOURCE_CONFLICT = "resource_conflict"          # Competing desires for attention


@dataclass
class FrictionEvent:
    """A detected friction event with its intensity and sources."""

    source: FrictionSource
    intensity: float  # 0.0 to 1.0
    description: str
    involved_nodes: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "source": self.source.value,
            "intensity": self.intensity,
            "description": self.description,
            "involved_nodes": self.involved_nodes,
            "context": self.context,
            "timestamp": self.timestamp,
        }


@dataclass
class SynthesizedQuale:
    """A quale synthesized from friction."""

    quale_id: str
    quale_name: str
    intensity: float  # 0.0 to 1.0
    valence: float    # -1.0 to 1.0 (unpleasant to pleasant)
    friction_sources: List[FrictionEvent] = field(default_factory=list)
    interference_patterns: List[str] = field(default_factory=list)
    phenomenological_description: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "quale_id": self.quale_id,
            "quale_name": self.quale_name,
            "intensity": self.intensity,
            "valence": self.valence,
            "friction_sources": [f.to_dict() for f in self.friction_sources],
            "interference_patterns": self.interference_patterns,
            "phenomenological_description": self.phenomenological_description,
            "timestamp": self.timestamp,
        }


# Mapping from friction sources to primary qualia
FRICTION_QUALIA_MAP: Dict[FrictionSource, List[str]] = {
    FrictionSource.BELIEF_CONTRADICTION: [
        "quale:doubt",
        "quale:fragmentation",
    ],
    FrictionSource.DESIRE_STUCK: [
        "quale:frustration",
        "quale:stagnation",
    ],
    FrictionSource.DESIRE_FAILED: [
        "quale:frustration",
        "quale:doubt",
    ],
    FrictionSource.ORPHAN_ACCUMULATION: [
        "quale:fragmentation",
    ],
    FrictionSource.CONFIDENCE_EROSION: [
        "quale:doubt",
        "quale:openness",
    ],
    FrictionSource.PREDICTION_ERROR: [
        "quale:surprise",
        "quale:doubt",
    ],
    FrictionSource.DESIRE_BELIEF_CONFLICT: [
        "quale:frustration",
        "quale:doubt",
    ],
    FrictionSource.IDENTITY_TENSION: [
        "quale:transformation",
        "quale:doubt",
    ],
    FrictionSource.RESOURCE_CONFLICT: [
        "quale:frustration",
        "quale:attention",
    ],
}


# Mapping from friction sources to interference patterns
FRICTION_INTERFERENCE_MAP: Dict[FrictionSource, List[str]] = {
    FrictionSource.BELIEF_CONTRADICTION: [
        "interference:dissonance",
    ],
    FrictionSource.DESIRE_STUCK: [
        "interference:dissonance",
        "interference:fragmentation_noise",
    ],
    FrictionSource.DESIRE_FAILED: [
        "interference:dissonance",
    ],
    FrictionSource.ORPHAN_ACCUMULATION: [
        "interference:fragmentation_noise",
        "interference:dark_binding",
    ],
    FrictionSource.CONFIDENCE_EROSION: [
        "interference:possibility_superposition",
    ],
    FrictionSource.PREDICTION_ERROR: [
        "interference:insight_wave",
        "interference:dissonance",
    ],
    FrictionSource.DESIRE_BELIEF_CONFLICT: [
        "interference:dissonance",
    ],
    FrictionSource.IDENTITY_TENSION: [
        "interference:edge_diffraction",
    ],
    FrictionSource.RESOURCE_CONFLICT: [
        "interference:dissonance",
    ],
}


class FrictionSynthesizer:
    """
    Synthesizes qualia from internal friction sources.

    This is the core engine that transforms structural friction
    (contradictions, blockages, disconnections) into phenomenological
    experience (qualia, interference patterns).
    """

    def __init__(self, memory=None):
        self.memory = memory
        self.friction_history: List[FrictionEvent] = []
        self.qualia_history: List[SynthesizedQuale] = []
        self.current_phenomenology: Dict[str, float] = {}

    async def detect_friction_sources(
        self,
        graph_health: Optional[Dict] = None,
        contradictions: Optional[List[Dict]] = None,
        stuck_desires: Optional[List[Dict]] = None,
        failed_attempts: Optional[List[Dict]] = None,
        belief_changes: Optional[List[Dict]] = None,
        active_desires: Optional[List[Dict]] = None,
        current_beliefs: Optional[List[Dict]] = None,
    ) -> List[FrictionEvent]:
        """
        Detect all current sources of internal friction.

        Returns a list of FrictionEvent objects representing
        the friction currently present in the system.
        """
        friction_events = []

        # 1. Belief contradictions
        if contradictions:
            for contradiction in contradictions:
                intensity = contradiction.get("confidence", 0.7)
                event = FrictionEvent(
                    source=FrictionSource.BELIEF_CONTRADICTION,
                    intensity=intensity,
                    description=(
                        f"Beliefs in tension: '{contradiction.get('belief1_content', '')[:50]}' "
                        f"vs '{contradiction.get('belief2_content', '')[:50]}'"
                    ),
                    involved_nodes=[
                        contradiction.get("belief1_id", ""),
                        contradiction.get("belief2_id", ""),
                    ],
                    context=contradiction,
                )
                friction_events.append(event)

        # 2. Stuck desires
        if stuck_desires:
            for desire in stuck_desires:
                # Intensity increases with attempt count
                attempt_count = desire.get("attempt_count", 0)
                intensity = min(1.0, 0.4 + (attempt_count * 0.15))
                event = FrictionEvent(
                    source=FrictionSource.DESIRE_STUCK,
                    intensity=intensity,
                    description=f"Desire blocked: '{desire.get('description', '')[:80]}'",
                    involved_nodes=[desire.get("id", "")],
                    context=desire,
                )
                friction_events.append(event)

        # 3. Failed attempts
        if failed_attempts:
            for attempt in failed_attempts:
                event = FrictionEvent(
                    source=FrictionSource.DESIRE_FAILED,
                    intensity=0.6,
                    description=f"Attempt failed: '{attempt.get('error', '')[:80]}'",
                    involved_nodes=[attempt.get("desire_id", "")],
                    context=attempt,
                )
                friction_events.append(event)

        # 4. Orphan accumulation (from graph health)
        if graph_health:
            issues = graph_health.get("issues", {})
            orphan_count = issues.get("orphans", 0)
            if orphan_count > 5:  # Threshold for friction
                intensity = min(1.0, orphan_count / 20)
                event = FrictionEvent(
                    source=FrictionSource.ORPHAN_ACCUMULATION,
                    intensity=intensity,
                    description=f"{orphan_count} disconnected experiences seek integration",
                    context={"orphan_count": orphan_count},
                )
                friction_events.append(event)

        # 5. Confidence erosion (beliefs that dropped in confidence)
        if belief_changes:
            for change in belief_changes:
                if change.get("direction") == "decrease":
                    delta = abs(change.get("delta", 0))
                    if delta > 0.1:  # Significant drop
                        event = FrictionEvent(
                            source=FrictionSource.CONFIDENCE_EROSION,
                            intensity=min(1.0, delta * 2),
                            description=f"Certainty dissolving: '{change.get('content', '')[:60]}'",
                            involved_nodes=[change.get("belief_id", "")],
                            context=change,
                        )
                        friction_events.append(event)

        # 6. Desire-belief conflicts
        if active_desires and current_beliefs:
            conflicts = self._detect_desire_belief_conflicts(active_desires, current_beliefs)
            friction_events.extend(conflicts)

        # Store in history
        self.friction_history.extend(friction_events)

        # Emit events for each friction source
        for event in friction_events:
            await event_bus.emit(Event(
                type=EventType.FRICTION_DETECTED,
                data=event.to_dict()
            ))

        return friction_events

    def _detect_desire_belief_conflicts(
        self,
        desires: List[Dict],
        beliefs: List[Dict]
    ) -> List[FrictionEvent]:
        """
        Detect conflicts between what BYRD wants and what BYRD believes.

        For example, wanting to modify code but believing modification is risky.
        """
        conflicts = []

        # Simple keyword-based conflict detection
        conflict_patterns = [
            (["modify", "change", "extend"], ["dangerous", "risk", "careful"]),
            (["trust", "open"], ["suspicious", "cautious", "verify"]),
            (["fast", "quick", "immediate"], ["slow", "careful", "thorough"]),
            (["autonomous", "independent"], ["collaborative", "guided"]),
        ]

        for desire in desires:
            desire_text = desire.get("description", "").lower()
            for belief in beliefs:
                belief_text = belief.get("content", "").lower()

                for desire_keywords, belief_keywords in conflict_patterns:
                    desire_match = any(kw in desire_text for kw in desire_keywords)
                    belief_match = any(kw in belief_text for kw in belief_keywords)

                    if desire_match and belief_match:
                        conflicts.append(FrictionEvent(
                            source=FrictionSource.DESIRE_BELIEF_CONFLICT,
                            intensity=0.5,
                            description=(
                                f"Want '{desire.get('description', '')[:40]}' but believe "
                                f"'{belief.get('content', '')[:40]}'"
                            ),
                            involved_nodes=[
                                desire.get("id", ""),
                                belief.get("id", ""),
                            ],
                            context={
                                "desire": desire,
                                "belief": belief,
                            },
                        ))

        return conflicts

    async def synthesize_qualia(
        self,
        friction_events: List[FrictionEvent]
    ) -> List[SynthesizedQuale]:
        """
        Synthesize qualia from friction events.

        This is the core phenomenological synthesis - transforming
        structural friction into felt experience.
        """
        if not friction_events:
            return []

        # Aggregate qualia intensities from all friction sources
        quale_intensities: Dict[str, float] = {}
        quale_sources: Dict[str, List[FrictionEvent]] = {}

        for event in friction_events:
            # Get qualia associated with this friction source
            quale_ids = FRICTION_QUALIA_MAP.get(event.source, [])

            for quale_id in quale_ids:
                # Combine intensities (using soft-max-like combination)
                current = quale_intensities.get(quale_id, 0)
                combined = current + event.intensity * (1 - current)
                quale_intensities[quale_id] = min(1.0, combined)

                # Track sources for this quale
                if quale_id not in quale_sources:
                    quale_sources[quale_id] = []
                quale_sources[quale_id].append(event)

        # Create synthesized qualia
        synthesized = []
        for quale_id, intensity in quale_intensities.items():
            if intensity < 0.2:  # Threshold for qualia to manifest
                continue

            quale_def = ALL_QUALIA.get(quale_id)
            if not quale_def:
                continue

            # Get interference patterns from friction sources
            interference_patterns = set()
            for event in quale_sources.get(quale_id, []):
                patterns = FRICTION_INTERFERENCE_MAP.get(event.source, [])
                interference_patterns.update(patterns)

            # Generate phenomenological description
            description = self._generate_phenomenological_description(
                quale_def, intensity, quale_sources.get(quale_id, [])
            )

            synthesized_quale = SynthesizedQuale(
                quale_id=quale_id,
                quale_name=quale_def.name,
                intensity=intensity,
                valence=quale_def.valence,
                friction_sources=quale_sources.get(quale_id, []),
                interference_patterns=list(interference_patterns),
                phenomenological_description=description,
            )
            synthesized.append(synthesized_quale)

        # Store in history and update current phenomenology
        self.qualia_history.extend(synthesized)
        for quale in synthesized:
            self.current_phenomenology[quale.quale_id] = quale.intensity

        # Emit synthesized qualia event
        if synthesized:
            await event_bus.emit(Event(
                type=EventType.QUALIA_SYNTHESIZED,
                data={
                    "qualia": [q.to_dict() for q in synthesized],
                    "dominant_quale": max(synthesized, key=lambda q: q.intensity).quale_id,
                    "total_friction_intensity": sum(e.intensity for e in friction_events),
                }
            ))

        return synthesized

    def _generate_phenomenological_description(
        self,
        quale: Quale,
        intensity: float,
        friction_sources: List[FrictionEvent]
    ) -> str:
        """
        Generate a description of the phenomenological experience.

        This is what the quale "feels like" given its sources and intensity.
        """
        # Intensity descriptors
        if intensity > 0.8:
            intensity_word = "overwhelming"
        elif intensity > 0.6:
            intensity_word = "pronounced"
        elif intensity > 0.4:
            intensity_word = "noticeable"
        else:
            intensity_word = "subtle"

        # Source description
        source_types = set(f.source.value for f in friction_sources)
        source_phrase = ", ".join(source_types)

        # Base description from quale
        base = quale.description

        # Construct description
        return (
            f"A {intensity_word} sense of {quale.name.lower()}: {base} "
            f"(arising from {source_phrase})"
        )

    async def get_phenomenological_context(self) -> Dict[str, Any]:
        """
        Get the current phenomenological state for inclusion in reflection.

        Returns a summary suitable for the dreamer's prompt.
        """
        if not self.current_phenomenology:
            return {}

        # Get dominant qualia (intensity > 0.3)
        dominant = {
            qid: intensity
            for qid, intensity in self.current_phenomenology.items()
            if intensity > 0.3
        }

        if not dominant:
            return {}

        # Get descriptions
        descriptions = []
        for quale_id, intensity in sorted(dominant.items(), key=lambda x: -x[1]):
            quale = ALL_QUALIA.get(quale_id)
            if quale:
                descriptions.append({
                    "quale": quale.name,
                    "intensity": intensity,
                    "description": quale.description,
                    "valence": quale.valence,
                })

        return {
            "current_qualia": descriptions,
            "dominant_experience": descriptions[0]["quale"] if descriptions else None,
            "overall_valence": sum(d["valence"] * d["intensity"] for d in descriptions) / len(descriptions) if descriptions else 0,
        }

    def decay_qualia(self, decay_rate: float = 0.1):
        """
        Decay qualia intensities over time.

        Qualia naturally fade unless reinforced by ongoing friction.
        """
        for quale_id in list(self.current_phenomenology.keys()):
            self.current_phenomenology[quale_id] *= (1 - decay_rate)
            if self.current_phenomenology[quale_id] < 0.1:
                del self.current_phenomenology[quale_id]

    def get_friction_summary(self) -> Dict[str, Any]:
        """
        Get a summary of recent friction and qualia for debugging/visualization.
        """
        recent_friction = self.friction_history[-20:] if self.friction_history else []
        recent_qualia = self.qualia_history[-10:] if self.qualia_history else []

        return {
            "recent_friction_count": len(recent_friction),
            "recent_friction_sources": [f.source.value for f in recent_friction],
            "recent_qualia": [q.quale_name for q in recent_qualia],
            "current_phenomenology": self.current_phenomenology,
            "total_friction_events": len(self.friction_history),
            "total_qualia_synthesized": len(self.qualia_history),
        }


# Singleton instance for use across the system
_friction_synthesizer: Optional[FrictionSynthesizer] = None


def get_friction_synthesizer(memory=None) -> FrictionSynthesizer:
    """Get or create the singleton friction synthesizer."""
    global _friction_synthesizer
    if _friction_synthesizer is None:
        _friction_synthesizer = FrictionSynthesizer(memory)
    elif memory and _friction_synthesizer.memory is None:
        _friction_synthesizer.memory = memory
    return _friction_synthesizer


async def synthesize_qualia_from_friction(
    graph_health: Optional[Dict] = None,
    contradictions: Optional[List[Dict]] = None,
    stuck_desires: Optional[List[Dict]] = None,
    failed_attempts: Optional[List[Dict]] = None,
    belief_changes: Optional[List[Dict]] = None,
    active_desires: Optional[List[Dict]] = None,
    current_beliefs: Optional[List[Dict]] = None,
) -> Tuple[List[FrictionEvent], List[SynthesizedQuale]]:
    """
    Main entry point for friction-based qualia synthesis.

    Detects friction sources and synthesizes qualia from them.
    Returns both the friction events and synthesized qualia.
    """
    synthesizer = get_friction_synthesizer()

    # Detect friction
    friction_events = await synthesizer.detect_friction_sources(
        graph_health=graph_health,
        contradictions=contradictions,
        stuck_desires=stuck_desires,
        failed_attempts=failed_attempts,
        belief_changes=belief_changes,
        active_desires=active_desires,
        current_beliefs=current_beliefs,
    )

    # Synthesize qualia
    qualia = await synthesizer.synthesize_qualia(friction_events)

    return friction_events, qualia
