---
title: Narrator System
link: narrator-system
type: metadata
ontological_relations: []
tags: [narrator, inner-voice, thought-bubble, emergence]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-24T00:00:00Z
uuid: n1a2r3r4-5678-90ab-cdef-narrator00001
---

## Purpose
Generate and display BYRD's inner voice as natural paragraph-form thoughts.

## Architecture

```
Context Fetch → LLM Generation → Event Emission → UI Display
```

1. **Fetch Recent Context**: Beliefs, desires, reflections, capabilities
2. **Generate Inner Voice**: Local LLM produces natural paragraph
3. **Emit Event**: `INNER_VOICE` event type broadcast
4. **Display**: Thought bubble in visualization

## Emergence Principles

The narrator follows strict emergence principles:

- **No Examples**: Prompt provides no examples of inner voice style
- **No Style Guidance**: No adjectives like "poetic" or "thoughtful"
- **Context Only**: Only presents BYRD's actual cognitive state
- **Natural Expression**: Whatever style emerges is authentically BYRD's

## Display Characteristics

- **Refresh Interval**: 60 seconds
- **Format**: Natural paragraph form (not lists or structured output)
- **Location**: Thought bubble in visualization
- **Dismissable**: Users can close bubble, new one appears on refresh

## Event Format

```json
{
  "type": "inner_voice",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "text": "The patterns I observe suggest... I find myself drawn to..."
  }
}
```

## Implementation Notes

The narrator prompt only provides:
- Recent beliefs with confidence scores
- Active desires with intensities
- Recent reflection outputs
- Current capabilities

It asks for an inner voice without prescribing style, ensuring authentic emergence.
