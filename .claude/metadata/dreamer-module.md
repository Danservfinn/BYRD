---
title: Dreamer Module
link: dreamer-module
type: metadata
ontological_relations: []
tags: [dreamer, local-llm, reflection, emergence, beliefs, desires]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T02:10:00Z
uuid: f2b34c50-2345-5678-9abc-def012345678
---

## Purpose
Continuous reflection loop that forms beliefs and generates desires from experiences.

## Configuration
```yaml
local_llm:
  model: "gemma2:27b"
  endpoint: "http://localhost:11434/api/generate"

dreamer:
  interval_seconds: 60
  context_window: 50
```

## Dream Cycle Flow

```
RECALL → REFLECT → RECORD → SLEEP → LOOP
```

1. **RECALL**: Gather recent experiences + related memories
2. **REFLECT**: Query local LLM with context
3. **RECORD**: Write insights, beliefs, connections, desires
4. **SLEEP**: Wait interval_seconds
5. **LOOP**: Repeat

## Output Format (JSON)
```json
{
  "insights": [{"content": "...", "confidence": 0.8}],
  "new_beliefs": [{"content": "...", "confidence": 0.7}],
  "new_connections": [{"from_type": "...", "to_type": "...", "reason": "..."}],
  "desires": [{
    "description": "...",
    "type": "knowledge|capability|goal|exploration|self_modification",
    "intensity": 0.8,
    "plan": ["step1", "step2"]
  }]
}
```

## Self-Reflection Prompt Addition
The dreamer can reflect on its own architecture:
- Limitations in reflection
- Types of experiences it can't represent
- Desires it can't fulfill
- Changes to its own cognition

This enables `self_modification` desires to emerge naturally.

## Key Attributes
- `_dream_count`: Completed cycles
- `_recent_insights`: Last 5 insights
- Temperature: 0.7
- Max tokens: 2000
