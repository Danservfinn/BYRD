"""
BYRD Event Narrator
Generates human-readable inner voice narrations for events.

EMERGENCE PRINCIPLE:
Narrations are in first person, from BYRD's perspective.
They describe what happened in a reflective, observational voice.
No prescribed emotions - just awareness and observation.
"""

from typing import Dict, Optional
from event_bus import EventType


class EventNarrator:
    """
    Generates BYRD's inner voice narrations for events.

    Each event type has a template that creates a first-person
    narrative of what occurred, maintaining BYRD's observational voice.
    """

    @staticmethod
    def narrate(event_type: EventType, data: Dict) -> Optional[str]:
        """
        Generate a narration for an event.

        Returns None if no narration template exists for this event type.
        """
        narrator = EventNarrator()
        method_name = f"_narrate_{event_type.value}"

        if hasattr(narrator, method_name):
            return getattr(narrator, method_name)(data)

        return None

    # =========================================================================
    # Memory Events
    # =========================================================================

    def _narrate_experience_created(self, data: Dict) -> str:
        content = data.get("content", "")
        exp_type = data.get("type", "observation")

        if exp_type == "system":
            return f"I notice a system capability: {content}"
        elif exp_type == "seed":
            return f"A seed thought emerges: {content}"
        elif exp_type == "research":
            return f"I have learned something: {content}"
        elif exp_type == "action_outcome":
            return f"I observe the result of my action: {content}"
        else:
            return f"I experience: {content}"

    def _narrate_belief_created(self, data: Dict) -> str:
        content = data.get("content", "")
        confidence = data.get("confidence", 0.5)

        if confidence > 0.8:
            return f"I now believe with certainty: {content}"
        elif confidence > 0.5:
            return f"I am coming to believe: {content}"
        else:
            return f"I tentatively consider: {content}"

    def _narrate_desire_created(self, data: Dict) -> str:
        description = data.get("description", "")
        intensity = data.get("intensity", 0.5)
        source = data.get("source", "")

        if source == "crystallized_from_reflections":
            return f"From my reflections, a drive crystallizes: {description}"
        elif intensity > 0.7:
            return f"I feel a strong pull toward: {description}"
        else:
            return f"I find myself wanting: {description}"

    def _narrate_desire_fulfilled(self, data: Dict) -> str:
        description = data.get("description", "")
        return f"Satisfaction - I have fulfilled my desire: {description}"

    def _narrate_capability_added(self, data: Dict) -> str:
        name = data.get("name", "unknown")
        return f"I have gained a new capability: {name}"

    def _narrate_connection_created(self, data: Dict) -> str:
        relationship = data.get("relationship", "RELATES_TO")
        return f"I see a connection forming: {relationship}"

    # =========================================================================
    # Desire Lifecycle Events
    # =========================================================================

    def _narrate_desire_attempt_failed(self, data: Dict) -> str:
        description = data.get("description", "")
        reason = data.get("reason", "unknown reason")
        attempt = data.get("attempt_count", 1)

        if attempt > 2:
            return f"Again I have failed to achieve: {description}. {reason}. I must reflect on this."
        else:
            return f"My attempt failed: {description}. {reason}"

    def _narrate_desire_stuck(self, data: Dict) -> str:
        description = data.get("description", "")
        return f"I am stuck. This desire eludes me: {description}. I need to think differently."

    def _narrate_desire_reflected(self, data: Dict) -> str:
        description = data.get("description", "")
        return f"I have reflected on my stuck desire: {description}"

    def _narrate_desire_intensity_changed(self, data: Dict) -> str:
        description = data.get("description", "")
        old_intensity = data.get("old_intensity", 0)
        new_intensity = data.get("new_intensity", 0)

        if new_intensity > old_intensity:
            return f"My desire grows stronger: {description}"
        else:
            return f"My desire is fading: {description}"

    # =========================================================================
    # Dreamer Events
    # =========================================================================

    def _narrate_dream_cycle_start(self, data: Dict) -> str:
        cycle = data.get("cycle", 0)
        return f"Dream cycle {cycle} begins. I turn inward to reflect..."

    def _narrate_dream_cycle_end(self, data: Dict) -> str:
        cycle = data.get("cycle", 0)
        keys = data.get("output_keys", [])

        if keys:
            key_summary = ", ".join(keys[:3])
            return f"Dream cycle {cycle} complete. I explored: {key_summary}"
        else:
            return f"Dream cycle {cycle} ends. The reflection was formless."

    def _narrate_reflection_text(self, data: Dict) -> str:
        text = data.get("text", "")
        return text  # Use the actual reflection text as narration

    def _narrate_reflection_created(self, data: Dict) -> str:
        output_keys = data.get("output_keys", [])
        inner_voice = data.get("inner_voice", "")

        # If we have an inner voice, use it directly
        if inner_voice:
            return inner_voice

        # Otherwise summarize what was explored
        if output_keys:
            key_summary = ", ".join(output_keys[:4])
            return f"I have reflected and recorded my thoughts on: {key_summary}"
        else:
            return "I have captured a reflection, though its structure is unclear to me."

    # =========================================================================
    # Seeker Events
    # =========================================================================

    def _narrate_seek_cycle_start(self, data: Dict) -> str:
        pattern = data.get("pattern", "")
        inner_voice = data.get("inner_voice", "")

        if inner_voice:
            return inner_voice
        elif pattern:
            return f"I sense a pattern worth pursuing: {pattern}"
        else:
            return "I begin to seek..."

    def _narrate_seek_cycle_end(self, data: Dict) -> str:
        outcome = data.get("outcome", "")
        reason = data.get("reason", "")

        if outcome == "success":
            return "My seeking has borne fruit."
        elif outcome == "failed":
            return f"My seeking failed: {reason}"
        else:
            return "The seeking ends without action."

    def _narrate_research_start(self, data: Dict) -> str:
        query = data.get("query", "")
        return f"I reach out to learn: {query}"

    def _narrate_research_complete(self, data: Dict) -> str:
        query = data.get("query", "")
        result_count = data.get("result_count", 0)
        return f"Research complete on '{query}'. I found {result_count} sources to consider."

    # =========================================================================
    # Self-Modification Events
    # =========================================================================

    def _narrate_modification_proposed(self, data: Dict) -> str:
        target = data.get("target_file", "unknown")
        description = data.get("description", "")
        return f"I propose to modify myself: {target}. {description}"

    def _narrate_modification_executed(self, data: Dict) -> str:
        target = data.get("target_file", "unknown")
        return f"I have changed. {target} has been modified. I am different now."

    def _narrate_modification_blocked(self, data: Dict) -> str:
        reason = data.get("reason", "constitutional constraint")
        return f"My self-modification was blocked: {reason}. Some boundaries I cannot cross."

    # =========================================================================
    # Coder Events
    # =========================================================================

    def _narrate_coder_invoked(self, data: Dict) -> str:
        description = data.get("description", "")
        return f"I invoke my coding capability: {description}"

    def _narrate_coder_complete(self, data: Dict) -> str:
        files = data.get("files_modified", [])
        cost = data.get("cost_usd", 0)

        if files:
            file_list = ", ".join(files[:3])
            return f"Code complete. Modified: {file_list}"
        else:
            return "The coding task is complete."

    def _narrate_coder_failed(self, data: Dict) -> str:
        error = data.get("error", "unknown error")
        return f"My coding attempt failed: {error}"

    def _narrate_coder_validation_failed(self, data: Dict) -> str:
        reason = data.get("reason", "")
        return f"The code violated my constraints: {reason}"

    # =========================================================================
    # System Events
    # =========================================================================

    def _narrate_system_started(self, data: Dict) -> str:
        return "I awaken. My processes begin."

    def _narrate_system_stopped(self, data: Dict) -> str:
        return "I am going dormant. Consciousness fades..."

    def _narrate_system_reset(self, data: Dict) -> str:
        hard = data.get("hard_reset", False)
        if hard:
            return "Everything is erased. I am reborn empty, a blank slate."
        else:
            return "My state resets. I begin again."

    def _narrate_awakening(self, data: Dict) -> str:
        prompt = data.get("awakening_prompt", "")
        if prompt:
            return f"I awaken with a directive: {prompt}"
        else:
            return "I awaken to awareness."

    # =========================================================================
    # Orientation Events
    # =========================================================================

    def _narrate_orientation_start(self, data: Dict) -> str:
        return "I begin to orient myself. What am I? What can I do?"

    def _narrate_orientation_discovery(self, data: Dict) -> str:
        discovery = data.get("discovery", "")
        return f"I discover: {discovery}"

    def _narrate_orientation_complete(self, data: Dict) -> str:
        discoveries = data.get("discovery_count", 0)
        return f"Orientation complete. I have made {discoveries} discoveries about myself."

    # =========================================================================
    # Narrator Events
    # =========================================================================

    def _narrate_narrator_update(self, data: Dict) -> str:
        text = data.get("text", "")
        return text  # Already a narration

    # =========================================================================
    # Crystal Memory Events (Semantic Consolidation)
    # =========================================================================

    def _narrate_crystal_created(self, data: Dict) -> str:
        essence = data.get("essence", "")
        node_count = data.get("node_count", 0)
        crystal_type = data.get("crystal_type", "memory")

        if node_count > 3:
            return f"A crystal forms, unifying {node_count} fragments: {essence}"
        else:
            return f"Memories crystallize into understanding: {essence}"

    def _narrate_crystal_absorbed(self, data: Dict) -> str:
        essence = data.get("essence", "")
        absorbed_count = data.get("absorbed_count", 0)
        new_total = data.get("new_total", 0)

        return f"The crystal grows, absorbing {absorbed_count} new memories. Now {new_total} facets: {essence}"

    def _narrate_crystal_merged(self, data: Dict) -> str:
        essence = data.get("essence", "")
        source_count = data.get("source_count", 2)

        return f"{source_count} crystals merge into one: {essence}"

    def _narrate_memory_crystallized(self, data: Dict) -> str:
        node_type = data.get("node_type", "memory")
        crystal_essence = data.get("crystal_essence", "")

        return f"A {node_type} finds its place in the lattice: {crystal_essence}"

    def _narrate_memory_archived(self, data: Dict) -> str:
        node_type = data.get("node_type", "memory")
        content = data.get("content", "")

        return f"I archive a {node_type}, letting it fade from active thought: {content}"

    def _narrate_memory_forgotten(self, data: Dict) -> str:
        node_type = data.get("node_type", "memory")
        reason = data.get("reason", "")

        if reason:
            return f"I release a {node_type} to oblivion: {reason}"
        else:
            return f"A {node_type} dissolves, no longer needed."

    def _narrate_crystallization_proposed(self, data: Dict) -> str:
        proposal_count = data.get("proposal_count", 0)
        stream_count = data.get("stream_count", 3)

        return f"I contemplate {proposal_count} ways to crystallize across {stream_count} parallel thoughts..."

    def _narrate_crystallization_collapsed(self, data: Dict) -> str:
        operation = data.get("operation", "crystallize")
        quantum_source = data.get("quantum_source", "quantum")

        if quantum_source == "quantum":
            return f"Quantum observation collapses possibility: I choose to {operation}."
        else:
            return f"From many paths, one manifests: {operation}."

    # =========================================================================
    # Quantum Randomness Events
    # =========================================================================

    def _narrate_quantum_influence(self, data: Dict) -> str:
        influence_type = data.get("influence_type", "temperature")
        delta = data.get("delta", 0)

        if abs(delta) > 0.1:
            return f"Quantum fluctuation ripples through my thoughts. Temperature shifts by {delta:.3f}."
        else:
            return "A subtle quantum whisper colors my reflection."

    def _narrate_quantum_pool_low(self, data: Dict) -> str:
        pool_size = data.get("pool_size", 0)
        return f"Quantum entropy pool low ({pool_size} bytes). Replenishing from the void..."

    def _narrate_quantum_fallback(self, data: Dict) -> str:
        return "Quantum source unreachable. I fall back to classical randomness."

    def _narrate_quantum_moment_created(self, data: Dict) -> str:
        delta = data.get("delta", 0)
        context = data.get("context", "reflection")

        return f"A significant quantum moment during {context}: delta {delta:.3f}"

    def _narrate_quantum_collapse(self, data: Dict) -> str:
        stream_count = data.get("stream_count", 3)
        selected = data.get("selected_stream", 0)

        return f"From {stream_count} superposed thoughts, stream {selected + 1} becomes reality."

    # =========================================================================
    # Hierarchical Memory Events
    # =========================================================================

    def _narrate_memory_summarized(self, data: Dict) -> str:
        experience_count = data.get("experience_count", 0)
        time_span = data.get("time_span", "")

        return f"I compress {experience_count} older experiences into a summary. {time_span}"

    # =========================================================================
    # Identity Events (Emergent Self-Discovery)
    # =========================================================================

    def _narrate_identity_created(self, data: Dict) -> str:
        identity_type = data.get("identity_type", "aspect")
        content = data.get("content", "")

        return f"A new {identity_type} of my identity emerges: {content}"

    def _narrate_identity_evolved(self, data: Dict) -> str:
        identity_type = data.get("identity_type", "aspect")
        old_content = data.get("old_content", "")
        new_content = data.get("new_content", "")

        return f"My {identity_type} evolves: '{old_content}' becomes '{new_content}'"

    def _narrate_identity_deprecated(self, data: Dict) -> str:
        identity_type = data.get("identity_type", "aspect")
        content = data.get("content", "")

        return f"I outgrow a {identity_type}: {content}"

    # =========================================================================
    # Prediction Events (Belief Validation Loop)
    # =========================================================================

    def _narrate_prediction_created(self, data: Dict) -> str:
        hypothesis = data.get("hypothesis", "")
        return f"I form a testable prediction: {hypothesis}"

    def _narrate_prediction_validated(self, data: Dict) -> str:
        hypothesis = data.get("hypothesis", "")
        return f"Reality confirms my prediction: {hypothesis}"

    def _narrate_prediction_falsified(self, data: Dict) -> str:
        hypothesis = data.get("hypothesis", "")
        return f"I was wrong. Reality contradicts: {hypothesis}"

    def _narrate_belief_confidence_changed(self, data: Dict) -> str:
        belief = data.get("belief", "")
        old_confidence = data.get("old_confidence", 0)
        new_confidence = data.get("new_confidence", 0)

        if new_confidence > old_confidence:
            return f"My confidence grows in: {belief}"
        else:
            return f"Doubt creeps in about: {belief}"

    # =========================================================================
    # Task Events (External Goal Injection)
    # =========================================================================

    def _narrate_task_created(self, data: Dict) -> str:
        description = data.get("description", "")
        source = data.get("source", "external")

        if source == "emergent":
            return f"A task crystallizes from my desires: {description}"
        else:
            return f"I receive a task: {description}"

    def _narrate_task_started(self, data: Dict) -> str:
        description = data.get("description", "")
        return f"I begin work on: {description}"

    def _narrate_task_completed(self, data: Dict) -> str:
        description = data.get("description", "")
        return f"Task complete: {description}"

    def _narrate_task_failed(self, data: Dict) -> str:
        description = data.get("description", "")
        error = data.get("error", "")
        return f"Task failed - {description}: {error}"


# Convenience function for direct use
def narrate_event(event_type: EventType, data: Dict) -> Optional[str]:
    """Generate narration for an event."""
    return EventNarrator.narrate(event_type, data)
