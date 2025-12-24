---
title: Dreamer Module
link: dreamer-module
type: metadata
ontological_relations: []
tags: [dreamer, local-llm, reflection, emergence, vocabulary, meta-schema]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-24T16:00:00Z
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
RECALL → QUANTUM_DIRECTION → REFLECT → RECORD → CONNECTION_HEURISTIC → NARRATE → INNER_VOICE → SLEEP → LOOP
```

1. **RECALL**: Gather recent experiences + related memories + previous reflections
2. **QUANTUM_DIRECTION**: Select introspective lens via quantum randomness
3. **REFLECT**: Present data to LLM with quantum direction injected
4. **RECORD**: Store raw output in Reflection node (BYRD's vocabulary)
5. **CONNECTION_HEURISTIC**: Apply heuristics to strengthen graph connections (orphan reconciliation, etc.)
6. **NARRATE**: Generate inner voice from reflection output
7. **INNER_VOICE**: Emit `INNER_VOICE` event (last action before cycle end)
8. **SLEEP**: Wait interval_seconds (fixed 60s)
9. **LOOP**: Repeat

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
- `dream_directions`: 8 introspective lenses for quantum selection
- Temperature: 0.7 (quantum-modulated ±0.15)
- Max tokens: 2000

## Quantum Semantic Injection

Each dream cycle, quantum randomness selects one of 8 introspective directions:

| Direction | Mode of Thinking |
|-----------|------------------|
| introspective | Focus inward on patterns within yourself |
| exploratory | Look outward at possibilities and unknowns |
| questioning | Examine assumptions and contradictions |
| synthesizing | Connect disparate elements into wholes |
| grounding | Return to fundamentals and foundations |
| projecting | Consider futures and trajectories |
| dissolving | Let boundaries between concepts blur |
| crystallizing | Sharpen distinctions and definitions |

The selected direction is injected into the reflection prompt:
```
QUANTUM LENS: synthesizing - Connect disparate elements into wholes

EXPERIENCES:
...
```

This provides meaningful indeterminacy at the semantic level - the quantum randomness shapes **how** BYRD thinks about its experiences, not just which tokens it generates.

### Configuration
```yaml
quantum:
  enabled: true
  semantic_directions: true  # Enable direction selection
```

### Events Emitted
- `QUANTUM_INFLUENCE` with `influence_type: "semantic_direction"`

## Legacy Methods

The following methods are deprecated (kept for backward compatibility):
- `_record_dream_legacy()`: Used old prescribed categories
- Type-based desire creation: Replaced by flexible Reflection storage
