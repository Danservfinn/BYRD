---
title: Event Bus System
link: event-bus
type: metadata
ontological_relations: []
tags: [events, streaming, ui, debugging, async]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-24T16:00:00Z
uuid: f5e67f80-5678-89ab-cdef-012345678901
---

## Purpose
Real-time event emission for UI streaming and debugging.

## File
`/Users/kurultai/BYRD/event_bus.py`

## Event Types

### Memory Events
- `EXPERIENCE_CREATED`
- `BELIEF_CREATED`
- `DESIRE_CREATED`
- `DESIRE_FULFILLED`
- `CAPABILITY_ADDED`
- `CONNECTION_CREATED`
- `CONNECTION_HEURISTIC` - Generic heuristic events (e.g., orphan reconciliation)
- `CONNECTION_HEURISTIC_APPLIED`

### Dynamic Ontology Events
- `NODE_TYPE_DISCOVERED` - First use of a new node type
- `CUSTOM_NODE_CREATED` - Node of emergent type created

### Desire Lifecycle Events
- `DESIRE_ATTEMPT_FAILED`
- `DESIRE_STUCK` - Needs Dreamer reflection
- `DESIRE_REFLECTED` - Dreamer processed stuck desire
- `DESIRE_INTENSITY_CHANGED`

### Dreamer Events
- `DREAM_CYCLE_START`
- `DREAM_CYCLE_END`
- `REFLECTION_TEXT`
- `REFLECTION_CREATED` - Emergence-compliant storage
- `MEMORIES_ACCESSED` - When memories are being considered during reflection
- `INNER_VOICE` - BYRD's inner narration (last event before cycle end)

### Seeker Events
- `SEEK_CYCLE_START`
- `SEEK_CYCLE_END`
- `RESEARCH_START`
- `RESEARCH_COMPLETE`
- `INTROSPECTION_COMPLETE` - Self-observation strategy completed

### Self-Modification Events
- `MODIFICATION_PROPOSED`
- `MODIFICATION_EXECUTED`
- `MODIFICATION_BLOCKED`

### Coder Events (Claude Code CLI)
- `CODER_INVOKED`
- `CODER_COMPLETE`
- `CODER_FAILED`
- `CODER_VALIDATION_FAILED`

### System Events
- `SYSTEM_STARTED`
- `SYSTEM_STOPPED`
- `SYSTEM_RESET`
- `AWAKENING`

### Orientation Events
- `ORIENTATION_START`
- `ORIENTATION_DISCOVERY`
- `ORIENTATION_COMPLETE`

### Narrator Events
- `NARRATOR_UPDATE` - BYRD's inner voice for UI

### Quantum Randomness Events
- `QUANTUM_INFLUENCE` - Quantum value affected temperature
- `QUANTUM_POOL_LOW` - Entropy pool below threshold
- `QUANTUM_FALLBACK` - Switched to classical entropy
- `QUANTUM_MOMENT_CREATED` - Significant moment recorded

### Hierarchical Memory Events
- `MEMORY_SUMMARIZED` - Older experiences compressed into summary

### Identity Events (Emergent Self-Discovery)
- `IDENTITY_CREATED` - New identity facet emerged
- `IDENTITY_EVOLVED` - Identity facet evolved with history
- `IDENTITY_DEPRECATED` - Identity facet retired
- `SELF_NAMED` - BYRD chose a name for itself
- `VOICE_CRYSTALLIZED` - Voice synthesized from beliefs

## Implementation
- Singleton pattern
- Sync and async subscribers
- Event history (max 1000)
- Real-time filtering by event type

## Usage
```python
# Subscribe
event_bus.subscribe("DREAM_CYCLE_END", callback)

# Get history
events = event_bus.get_history(limit=100, event_types=["DESIRE_CREATED"])
```
