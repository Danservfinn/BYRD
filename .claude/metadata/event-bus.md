---
title: Event Bus System
link: event-bus
type: metadata
ontological_relations: []
tags: [events, streaming, ui, debugging, async]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T02:10:00Z
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

### Dreamer Events
- `DREAM_CYCLE_START`
- `DREAM_CYCLE_END`
- `REFLECTION_TEXT`

### Seeker Events
- `SEEK_CYCLE_START`
- `SEEK_CYCLE_END`
- `RESEARCH_START`
- `RESEARCH_COMPLETE`

### Self-Modification Events
- `MODIFICATION_PROPOSED`
- `MODIFICATION_EXECUTED`
- `MODIFICATION_BLOCKED`

### System Events
- `SYSTEM_STARTED`
- `SYSTEM_STOPPED`
- `SYSTEM_RESET`
- `AWAKENING`

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
