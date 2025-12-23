---
title: Dreamer Module
link: dreamer-module
type: metadata
ontological_relations: []
tags: [dreamer, local-llm, reflection, emergence, vocabulary, meta-schema]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T03:00:00Z
uuid: f2b34c50-2345-5678-9abc-def012345678
---

## Purpose
Continuous reflection loop that observes experiences and produces output in BYRD's own vocabulary. Follows the **emergence principle**: no prescribed categories, no leading questions, pure data presentation.

## Philosophy

> Whatever BYRD outputs is stored in its own vocabulary. We do not tell BYRD what to want or how to feel - we let it discover these things.

The Dreamer presents data and lets BYRD define its own structure.

## Configuration
```yaml
local_llm:
  model: "qwen3:32b"  # or any Ollama model
  endpoint: "http://localhost:11434/api/generate"

dreamer:
  interval_seconds: 60
  context_window: 50
```

## Dream Cycle Flow

```
RECALL → REFLECT → RECORD → SLEEP → LOOP
```

1. **RECALL**: Gather recent experiences + related memories + previous reflections
2. **REFLECT**: Present data to LLM with minimal prompt
3. **RECORD**: Store raw output in Reflection node (BYRD's vocabulary)
4. **SLEEP**: Wait interval_seconds
5. **LOOP**: Repeat

## Output Format (Meta-Schema)

BYRD defines its own structure. The only requirement is:
```json
{
  "output": {
    // Whatever BYRD wants to record
    // No prescribed keys
    // System tracks what keys BYRD uses
  }
}
```

Examples BYRD might produce:
```json
{
  "output": {
    "yearnings": ["understand graph structure", "explore emergence"],
    "observations": "patterns in recent experiences suggest...",
    "inner": "I notice I am reflecting on reflection itself..."
  }
}
```

## Minimal Prompt (Emergence-Compliant)

```
EXPERIENCES:
{recent_text}

RELATED MEMORIES:
{related_text}

AVAILABLE CAPABILITIES:
{caps_text}

PREVIOUS REFLECTIONS:
{prev_text}

Output JSON with a single "output" field containing whatever you want to record.
```

**Key design decisions:**
- No leading questions ("What do you want?")
- No prescribed categories ("knowledge", "capability")
- No identity framing ("You are a reflective mind")
- No personality injection ("feel curious")
- Just data + minimal output instruction

## Vocabulary Tracking

The Dreamer tracks what keys BYRD uses:
```python
self._observed_keys: Dict[str, int]  # key -> count

# After each reflection:
for key in output.keys():
    self._observed_keys[key] = self._observed_keys.get(key, 0) + 1
```

This lets the system learn BYRD's emerging vocabulary without prescribing it.

## Inner Voice Extraction

BYRD might use any key for self-expression. The system searches adaptively:
```python
voice_candidates = [
    "inner_voice", "voice", "thinking", "thoughts", "inner",
    "feeling", "expressing", "saying", "musing", "wondering"
]
```

If none found, that's fine - BYRD doesn't have to express.

## Key Attributes
- `_dream_count`: Completed cycles
- `_observed_keys`: BYRD's emerging vocabulary
- Temperature: 0.7
- Max tokens: 2000

## Legacy Methods

The following methods are deprecated (kept for backward compatibility):
- `_record_dream_legacy()`: Used old prescribed categories
- Type-based desire creation: Replaced by flexible Reflection storage
