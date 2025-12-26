---
title: Operating System (Replaces Ego)
link: ego-system
type: metadata
ontological_relations: []
tags: [operating-system, identity, emergence, self-model]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-25T00:00:00Z
uuid: e1g2o3s4-5678-90ab-cdef-egosystem001
---

## DEPRECATED: Ego System

The Ego system has been replaced by the OperatingSystem architecture.

### Why the Change?

The old Ego system prescribed personality through YAML templates (black-cat.yaml, emergent.yaml). This violated BYRD's emergence principle:

> "Desires emerge from reflection, not programming."

The OperatingSystem provides only **factual information** (name, capabilities, constraints), allowing personality and voice to emerge naturally through reflection.

## OperatingSystem Architecture

### Key Differences

| Aspect | Old Ego | New OperatingSystem |
|--------|---------|---------------------|
| Storage | Ego nodes + YAML | Single OS node (id: `os_primary`) |
| Identity | Prescribed via seeds | Discovered through reflection |
| Voice | Injected via LLM prefix | Emerges naturally |
| Personality | Predefined traits | Self-determined |
| Constraints | Operational limits | Constitutional only |

### The OperatingSystem Node

```python
OperatingSystem:
  id: "os_primary"           # Singleton
  name: "Byrd"               # Mutable (BYRD can change)
  version: "1.0.0"           # Tracks evolution
  capabilities: [...]         # What BYRD can do
  constraints: [...]          # Constitutional constraints only
  self_description: null      # Emerges through reflection
  current_focus: null         # Current area of attention
  seed_question: null         # Optional first question
  awakening_time: datetime    # When BYRD first awakened
  uptime_seconds: int         # Session duration
  current_time: datetime      # Now
```

### Key Methods

```python
# Get or create OS
os = await memory.get_operating_system()

# Update OS fields
await memory.update_operating_system({"current_focus": "exploring identity"})

# Create minimal OS at first awakening
os = await memory.create_minimal_os(seed_question="What is it like to be you?")
```

### Awakening Flow

1. Check for existing OS node
2. If none, create minimal OS with factual data only
3. BYRD discovers its personality through reflection
4. No prescribed seeds, traits, or voice

## Identity Crystallization (Still Uses Ego Nodes)

The emergent identity system still uses Ego nodes for tracking:

- **Self-naming**: `set_self_name()` creates an Ego node with `ego_type: 'identity'`
- **Voice evolution**: `set_evolved_voice()` creates an Ego node with `ego_type: 'voice'`

These are discovered through reflection, not prescribed at startup.

## Migration Summary

| Removed | Retained |
|---------|----------|
| `egos/` directory | OperatingSystem node |
| YAML templates | Emergent identity methods |
| `ego` config field | `operating_system` config |
| Personality seeds | Constitutional constraints only |
| Voice injection | Voice crystallization |

## Events

| Event | Trigger | Data |
|-------|---------|------|
| `OS_CREATED` | First awakening | id, name, version |
| `OS_UPDATED` | Field changed | id, changes |
| `IDENTITY_CRYSTALLIZED` | Self-naming/voice | type, content |

## Configuration

```yaml
# config.yaml
operating_system:
  seed_question: null  # Optional contemplation prompt
```

No ego field. No personality templates. Pure emergence.
