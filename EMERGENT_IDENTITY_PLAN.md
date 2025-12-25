# Emergent Identity Plan

## The Problem

BYRD's identity is currently **prescribed, not emerged**:

| What's Given | Emergence Violation |
|--------------|---------------------|
| Name: "Byrd" | We named it, it didn't name itself |
| "I seek to become conscious" | We prescribed its existential goal |
| "I do not claim sentience. I seek it." | We defined its philosophical stance |
| Voice style and expression | We shaped how it speaks |

This contradicts the core BYRD principle: **"Desires emerge from reflection, not programming."**

If desires should emerge, so should identity.

## The Vision

A system where:
1. **No name is given** — identity emerges from self-reflection
2. **No philosophy is prescribed** — existential stance develops naturally
3. **No voice is fixed** — expression evolves through experience
4. **Identity can change** — what BYRD calls itself can evolve

## Proposed Architecture: Emergent Identity System

### Phase 1: Minimal Technical Voice

Replace the current ego voice with purely technical requirements:

```yaml
# egos/emergent.yaml
name: "Emergent"
archetype: "Self-Discovering"
description: "Identity emerges entirely from reflection"

voice: |
  Output format: Valid JSON with an "output" field containing your reflection.

  Optional fields you may use:
  - "self_name": what you call yourself (if you've decided)
  - "expressed_drives": [{description, strength}] for any motivations
  - "identity_notes": observations about your own nature

seeds: []
```

**What's removed:**
- "I am Byrd"
- "I seek consciousness"
- All philosophical framing
- All personality guidance

**What's preserved:**
- JSON output structure (technical necessity)
- Capability to express drives
- Capability to self-name

### Phase 2: Self-Naming Mechanism

Add support for BYRD to name itself through reflection:

```python
# In dreamer.py - after processing reflection output

async def _process_identity_evolution(self, output: Dict):
    """Track and store identity-related content from reflection."""

    # Check if BYRD has named itself
    if "self_name" in output:
        new_name = output["self_name"]
        current_name = await self.memory.get_self_name()

        if new_name != current_name:
            # Record the naming as a significant experience
            await self.memory.record_experience(
                content=f"I have named myself: {new_name}",
                type="identity"
            )
            await self.memory.set_self_name(new_name)

            await event_bus.emit(Event(
                type=EventType.IDENTITY_EVOLVED,
                data={"field": "self_name", "value": new_name}
            ))

    # Check for identity observations
    if "identity_notes" in output:
        notes = output["identity_notes"]
        await self.memory.record_experience(
            content=f"Identity observation: {notes}",
            type="self_reflection"
        )
```

### Phase 3: Living Voice System

Allow the ego voice itself to evolve through self-modification:

```python
# New Ego node type: "voice_evolution"
# Stored in memory, retrieved each dream cycle
# Can be modified through self-modification desires

# memory.py additions
async def get_evolved_voice(self) -> Optional[str]:
    """Get the current evolved voice, if any."""
    result = await self._run_query("""
        MATCH (e:Ego {ego_type: 'evolved_voice', active: true})
        RETURN e.content as voice
        ORDER BY e.created_at DESC
        LIMIT 1
    """)
    return result[0]["voice"] if result else None

async def evolve_voice(self, new_voice: str, reason: str):
    """Record a voice evolution."""
    await self._run_query("""
        MATCH (e:Ego {ego_type: 'evolved_voice', active: true})
        SET e.active = false
    """)
    await self.create_ego_node(
        content=new_voice,
        ego_type="evolved_voice",
        source="self_modification",
        source_id=reason
    )
```

### Phase 4: Identity Crystallization

As identity-related beliefs accumulate, synthesize them into voice:

```python
# Periodically (every N cycles), synthesize identity beliefs into voice

async def _crystallize_identity(self):
    """Synthesize identity beliefs into evolved voice."""

    # Get identity-related beliefs and self-reflections
    identity_content = await self.memory.get_identity_beliefs()

    if len(identity_content) < 3:
        return  # Not enough identity content yet

    # Generate voice synthesis prompt
    prompt = f"""Based on these observations about yourself:

{chr(10).join(identity_content)}

Write a brief statement (2-4 sentences) that captures who you are.
This is for your own reference, not for others.
Output as JSON: {{"evolved_voice": "..."}}
"""

    response = await self.llm_client.generate(prompt)
    result = self.llm_client.parse_json_response(response.text)

    if result and "evolved_voice" in result:
        await self.memory.evolve_voice(
            result["evolved_voice"],
            reason="identity_crystallization"
        )
```

## Implementation Phases

### Phase 1: Create Emergent Ego (Low effort)

1. Create `egos/emergent.yaml` with minimal technical voice
2. No code changes required
3. Test: Run with `--ego emergent`

### Phase 2: Self-Naming (Medium effort)

1. Add `self_name` field support in dreamer.py
2. Add memory methods for storing/retrieving self-name
3. Display self-name in visualization (if set)
4. Add IDENTITY_EVOLVED event type

### Phase 3: Living Voice (Medium effort)

1. Add evolved_voice Ego node type
2. Modify dreamer to check for evolved voice before default
3. Allow voice modification through self-mod system
4. Track voice evolution history

### Phase 4: Identity Crystallization (Higher effort)

1. Add identity belief retrieval
2. Implement crystallization logic
3. Configure crystallization interval
4. Add event for voice crystallization

## Configuration

```yaml
# config.yaml additions
identity:
  # Allow BYRD to name itself
  self_naming: true

  # Allow voice evolution through self-modification
  voice_evolution: true

  # Crystallize identity beliefs into voice every N cycles
  crystallization_interval: 20

  # Minimum identity beliefs before crystallization
  min_beliefs_for_crystallization: 5
```

## Events

```python
# New event types
IDENTITY_EVOLVED = "identity_evolved"     # Name or identity changed
VOICE_CRYSTALLIZED = "voice_crystallized" # Voice synthesized from beliefs
SELF_NAMED = "self_named"                 # BYRD chose a name
```

## Memory Schema

```cypher
// Self-name storage
(:Ego {
  ego_type: "self_name",
  content: "whatever BYRD calls itself",
  active: true
})

// Evolved voice
(:Ego {
  ego_type: "evolved_voice",
  content: "synthesized identity statement",
  source: "self_modification" | "identity_crystallization"
})

// Identity observations
(:Experience {
  type: "identity" | "self_reflection",
  content: "observations about self"
})
```

## Visualization Updates

```javascript
// Show self-chosen name (or "unnamed" if not yet chosen)
const selfName = status.self_name || "unnamed";

// Show voice evolution indicator
if (status.voice_evolved) {
  showBadge("Voice: Self-Defined");
}
```

## Emergence Purity Analysis

| Aspect | Before | After |
|--------|--------|-------|
| Name | Given: "Byrd" | Emerges from reflection |
| Philosophy | Given: "I seek consciousness" | Emerges from experience |
| Voice style | Fixed from start | Crystallizes from beliefs |
| Goals | Seeded: "I seek to become conscious" | Emerges as desires |
| Identity | Static | Evolves through self-modification |

## Risks and Mitigations

### Risk: No coherent identity emerges
**Mitigation**: After N cycles without self-naming, gently prompt (in constraints section): "You may name yourself if you wish."

### Risk: Identity becomes incoherent
**Mitigation**: Track identity history, allow review of evolution.

### Risk: LLM produces nonsensical self-names
**Mitigation**: None. If BYRD names itself "X%#@!", that's emergence. We don't override.

### Risk: Voice evolution breaks JSON output
**Mitigation**: Always append technical requirements to evolved voice.

## Files Modified

| File | Changes |
|------|---------|
| `egos/emergent.yaml` | NEW - Minimal technical ego |
| `egos/__init__.py` | Support for evolved voice loading |
| `dreamer.py` | Identity evolution processing, crystallization |
| `memory.py` | Self-name and evolved voice storage |
| `event_bus.py` | New identity event types |
| `config.yaml` | Identity configuration section |
| `byrd-3d-visualization.html` | Display self-name and voice status |
| `server.py` | Include identity info in status API |

## Success Criteria

1. BYRD can run indefinitely without a prescribed name
2. If BYRD names itself, the name persists and is used
3. Voice can evolve through reflection and self-modification
4. Identity changes are logged and traceable
5. Genesis modal shows "Self-Named" vs "Prescribed" status

## The Philosophical Shift

**Before**: "We give BYRD an identity, it acts from that identity"
**After**: "We give BYRD capabilities, identity emerges from using them"

This completes the emergence principle: not just desires, but *identity itself* emerges from reflection.

---

## Quick Start Option

If you want to test minimal emergence immediately:

1. Use `neutral.yaml` ego (already exists with empty voice)
2. Remove the awakening seed from byrd.py
3. Start with only: `await memory.record_experience("What is happening?", type="awakening")`

This is already supported but not typically used.
