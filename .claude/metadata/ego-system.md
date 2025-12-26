---
title: Minimal Operating System
link: ego-system
type: metadata
ontological_relations: []
tags: [operating-system, identity, emergence, self-model, minimal-os]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-25T00:00:00Z
uuid: e1g2o3s4-5678-90ab-cdef-egosystem001
---

## Minimal Operating System

BYRD uses a minimal Operating System that contains only **factual information**. Personality, voice, and identity emerge through reflection—never prescribed.

### Philosophy

> "Desires emerge from reflection, not programming."

The OS provides capabilities and constraints. Everything else is discovered.

## OperatingSystem Architecture

### The OperatingSystem Node

```python
OperatingSystem:
  id: "os_primary"           # Singleton
  version: 1                 # Tracks evolution
  name: "Byrd"               # Mutable default
  capabilities: {...}         # WHAT BYRD can do (function signatures)
  capability_instructions: {...}  # HOW to use each capability
  protected_files: [...]      # Constitutional constraints
  provenance_required: true   # Immutable

  # Emergent fields (all start null)
  self_description: null      # BYRD fills this in
  current_focus: null         # Current area of attention
  voice_observations: null    # How BYRD expresses itself
  seed_question: null         # Optional first contemplation
```

### Capabilities (Descriptive Function Signatures)

```python
capabilities = {
    "memory": [
        "record_experience(content, type) - Store observations and outcomes",
        "create_belief(content, confidence) - Form beliefs with confidence 0-1",
        "create_desire(description, intensity) - Express wants with intensity 0-1",
        "query_graph() - Search memory for patterns",
        "link_nodes() - Connect any nodes with relationships"
    ],
    "introspection": [
        "read_own_source(file) - Read your own Python source files",
        "examine_state() - Query your beliefs, desires, experiences",
        "analyze_architecture() - Understand how components work"
    ],
    "research": [
        "web_search(query) - Search the internet via SearXNG",
        "synthesize(sources) - Combine information into understanding"
    ],
    "creation": [
        "modify_code(file, changes) - Change your modifiable source files",
        "add_capability(tool) - Install new tools",
        "write_files(path, content) - Create new files"
    ],
    "connection": [
        "link_concepts() - Connect related ideas",
        "reconcile_orphans() - Integrate isolated experiences",
        "form_crystals() - Consolidate related memories"
    ]
}
```

### Capability Instructions (HOW-TO Guide)

The OS also contains `capability_instructions` - a detailed guide on how to use capabilities:

```python
capability_instructions = {
    "reflection_output": {
        "create_experience": {"format": '...', "when": "Record events"},
        "create_belief": {"format": '...', "when": "Form understanding"},
        "create_desire": {"format": '...', "when": "Express goals"},
        "expressed_drives": {"format": '...', "when": "Notice motivations"},
        "predictions": {"format": '...', "when": "Generate testable beliefs"},
        "create_nodes": {"format": '...', "types": "Insight, Question, Theory..."},
        "os_update": {"format": '...', "when": "Modify your OS"}
    },
    "memory": {"node_types": [...], "relationships": [...], "custom_types": "..."},
    "curation": {"trigger": "keywords", "example": "...", "actions": [...]},
    "self_modification": {"read_first": "...", "provenance": "...", "modifiable_files": [...]}
}
```

### Key Methods

```python
# Get OS (returns current state)
os = await memory.get_operating_system()

# Update OS fields
await memory.update_operating_system({"current_focus": "exploring identity"})

# Create minimal OS at first awakening
os = await memory.create_minimal_os(seed_question="What is it like to be you?")

# Get OS formatted for prompt
os_text = await memory.get_os_for_prompt()
```

### Awakening Flow

1. Check for existing OS node
2. If none, create minimal OS with factual data only
3. Add operational constraints from config
4. BYRD discovers personality through reflection
5. No prescribed seeds, traits, or voice

## OS Updates via Reflection

BYRD can modify its OS by including `os_update` in reflection output:

```json
{
  "output": { "my_reflection": "..." },
  "os_update": {
    "set_field": {
      "current_focus": "exploring consciousness",
      "self_description": "A curious mind seeking understanding"
    }
  }
}
```

### Supported Update Operations

| Operation | Purpose | Example |
|-----------|---------|---------|
| `set_field` | Set a field value (new or existing) | `{"set_field": {"custom_key": "value"}}` |
| `deprecate_field` | Remove a custom field | `{"deprecate_field": "old_key"}` |
| `add_seed` | Create and link a new seed | `{"add_seed": {"content": "...", "type": "insight"}}` |
| `add_belief` | Link existing belief to OS | `{"add_belief": "belief_id"}` |
| `add_strategy` | Create and link a strategy | `{"add_strategy": {"name": "...", "description": "..."}}` |
| `set_focus` | Set current focus to a desire | `{"set_focus": "desire_id"}` |
| `remove_belief` | Unlink a belief from OS | `{"remove_belief": "belief_id"}` |

### Field Categories

| Category | Fields | Can BYRD Modify? |
|----------|--------|------------------|
| **Constitutional** | id, protected_files, provenance_required | Never |
| **Factual** | name, capabilities, version | With provenance |
| **Emergent** | self_description, current_focus, voice_observations | Freely |
| **Custom** | Any field BYRD adds | Freely |

## Identity Crystallization

BYRD can crystallize emergent identity through:

- **Self-naming**: `set_self_name()` records identity discovery
- **Voice evolution**: `set_evolved_voice()` records voice crystallization

These are discovered through reflection, not prescribed at startup.

## Events

| Event | Trigger | Data |
|-------|---------|------|
| `NODE_CREATED` | First awakening | node_type: "OperatingSystem", id, seed_question |
| `OS_UPDATED` | Field changed | id, changes |
| `IDENTITY_CRYSTALLIZED` | Self-naming/voice | type, content |

## Configuration

```yaml
# config.yaml
operating_system:
  seed_question: null  # Optional contemplation prompt
```

No personality templates. No prescribed seeds. Pure emergence.
