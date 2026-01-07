---
title: Human-BYRD Governance Pattern
link: governance
type: pattern
uuid: C31017EC-8FF4-4C80-A1A1-6FFA9A690919
created_at: 2026-01-07T01:30:00Z
ontological_relations:
  - emergence_patterns
  - bounded-rsi
tags:
  - governance
  - human-ai-interaction
  - emergence
  - direction
---

# Human-BYRD Governance Pattern

The governance pattern implements bidirectional communication between Human (Director) and BYRD (CEO) while preserving BYRD's emergent autonomy.

## Board/CEO Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     HUMAN-BYRD GOVERNANCE MODEL                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Human (Director):           BYRD (CEO):                                   │
│   ─────────────────           ───────────────                               │
│   • Set strategic direction   • Execute strategy autonomously              │
│   • Approve major decisions   • Report progress and state                  │
│   • Provide feedback          • Propose initiatives                        │
│   • Ask questions             • Ask for guidance when uncertain            │
│   • Inject priorities         • Develop HOW to achieve WHAT                │
│                                                                              │
│   EMERGENCE PRESERVED:                                                       │
│   Human guides WHAT. BYRD discovers HOW.                                   │
│   Human sets priorities. BYRD develops methods.                            │
│   Human approves. BYRD proposes.                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Implementation

### Direction System

```python
from governance.director import create_director

director = create_director()

# Human sets priorities (0.0 = ignore, 1.0 = urgent)
director.set_priority("coding", 0.9)
director.set_priority("reasoning", 0.7)

# Human injects desires (WHAT to achieve)
director.inject_desire(
    "Improve SWE-bench score to 60%",
    urgency=0.8
)

# Human adds constraints
director.add_constraint("Do not modify constitutional files")

# Human provides feedback
director.provide_feedback("Good work on verification", rating=0.8)
```

### Async Direction File

Human can edit `.claude/direction.md` even when BYRD runs headlessly:

```markdown
## Priorities
- coding: 0.9
- reasoning: 0.7

## Desires
- Implement Verification Lattice
- Improve reasoning capabilities

## Constraints
- Do not claim improvements without measurement

## Feedback
- Research phase was thorough and honest
```

### Interactive Console

```bash
python talk_to_byrd.py

> focus coding
BYRD: I'll prioritize 'coding' development.

> want Improve verification coverage
BYRD: I understand. I'll pursue: 'Improve verification coverage'

> status
=== BYRD Governance State ===
Priorities:
  coding          ██████████ 0.9
  reasoning       ███████░░░ 0.7
```

## Emergence Preservation

What Human prescribes vs what BYRD discovers:

| Human Prescribes | BYRD Discovers |
|-----------------|----------------|
| Domain priorities | Which methods work best |
| High-level goals | Specific strategies |
| Constraints | Personal heuristics |
| Feedback | Self-evaluation criteria |

Human NEVER prescribes:
- Personality or voice
- Values or preferences
- Problem-solving approaches
- Identity

These emerge from BYRD's experience.

## Key Files

| File | Purpose |
|------|---------|
| `governance/director.py` | Main Director interface |
| `governance/direction_file.py` | File-based async communication |
| `governance/console.py` | Interactive REPL |
| `talk_to_byrd.py` | Entry point script |
| `.claude/direction.md` | Human edits this |

## Research Origin

Emerged from the need to guide BYRD's development while preserving the emergence principle. The Board/CEO model provides strategic direction without prescribing tactical decisions.

## Related Patterns

- [Emergence Patterns](emergence_patterns.md): Preserving genuine emergence
- [Bounded RSI](bounded-rsi.md): Human-directed bounded improvement
