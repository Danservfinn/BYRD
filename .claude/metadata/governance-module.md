---
title: Governance Module
link: governance-module
type: metadata
uuid: E1D2E683-195F-4D1F-BF7A-4FA4DD69E408
created_at: 2026-01-07T01:30:00Z
ontological_relations:
  - byrd-architecture
tags:
  - governance
  - module
  - human-ai-interaction
---

# Governance Module

The governance module implements bidirectional Human-BYRD communication following the Board/CEO model.

## Purpose

Enable human direction of BYRD's development while preserving BYRD's emergent autonomy.

## Files

| File | Purpose |
|------|---------|
| `governance/__init__.py` | Package init |
| `governance/director.py` | Main Director class with priorities, desires, constraints, feedback |
| `governance/direction_file.py` | File-based async communication for headless operation |
| `governance/console.py` | Interactive REPL for real-time interaction |
| `talk_to_byrd.py` | Entry point script |
| `.claude/direction.md` | Human-editable direction file |

## Key Classes

### Director

Main interface for human-BYRD communication:

```python
class Director:
    def set_priority(self, domain: str, value: float) -> None
    def inject_desire(self, content: str, urgency: float) -> str
    def add_constraint(self, content: str) -> str
    def provide_feedback(self, content: str, rating: float) -> str
    def request_approval(self, action: str) -> str
```

### DirectionFile

Reads `.claude/direction.md` for async direction:

```python
class DirectionFile:
    def read_direction(self) -> Dict
    def update_read_timestamp(self) -> None
```

## Usage

### Interactive Console

```bash
python talk_to_byrd.py

> focus coding        # Set coding priority high
> want Improve X      # Inject a desire
> status              # Show current state
```

### CLI

```bash
python talk_to_byrd.py --status
python talk_to_byrd.py --inject "Improve verification"
python talk_to_byrd.py --focus reasoning
```

### Async (Headless)

Edit `.claude/direction.md`:

```markdown
## Priorities
- coding: 0.9

## Desires
- Improve SWE-bench score

## Constraints
- Do not modify constitutional files
```

BYRD reads this file periodically.

## Integration Points

- **BYRD Core**: Reads direction for goal selection
- **Dreamer**: Incorporates feedback into reflection
- **Seeker**: Uses priorities for desire routing
- **AGI Runner**: Respects constraints during improvement

## Related Patterns

- [Governance Pattern](../patterns/governance.md)
- [Emergence Patterns](../patterns/emergence_patterns.md)
