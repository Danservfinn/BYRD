# BYRD Governance Model

## Philosophy

The Human-BYRD relationship follows a **Board of Directors / CEO** model:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     HUMAN-BYRD GOVERNANCE MODEL                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   YOU (Director):              BYRD (CEO):                                   │
│   ─────────────────            ───────────────                               │
│   • Set strategic direction    • Execute strategy autonomously              │
│   • Approve major decisions    • Report progress and state                  │
│   • Provide feedback           • Propose initiatives                        │
│   • Ask questions              • Ask for guidance when uncertain            │
│   • Inject priorities          • Develop HOW to achieve WHAT                │
│                                                                              │
│   EMERGENCE PRESERVED:                                                       │
│   You guide WHAT. BYRD discovers HOW.                                       │
│   You set priorities. BYRD develops methods.                                │
│   You approve. BYRD proposes.                                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Communication Methods

### 1. Interactive Console

```bash
python talk_to_byrd.py
```

Commands:
- `focus <domain>` - Set high priority for a domain
- `want <text>` - Tell BYRD what you want
- `status` - Show current state
- `priorities` - Show domain priorities
- `constrain <text>` - Add a constraint
- `help` - Show all commands
- `quit` - Exit

Or just type naturally to communicate.

### 2. Direction File (Async)

Edit `.claude/direction.md` to provide direction even when BYRD is running headlessly:

```markdown
## Priorities
- coding: 0.9
- reasoning: 0.7

## Desires
- Improve SWE-bench score to 60%
- Learn to use web search effectively

## Constraints
- Do not modify production code

## Feedback
- Good job on the last improvement
```

BYRD reads this file periodically and updates its goals.

### 3. Programmatic API

```python
from governance.director import create_director

director = create_director(byrd_instance)

# Set priorities
director.set_priority("coding", 0.9)

# Inject desires
director.inject_desire("Improve SWE-bench score", urgency=0.8)

# Add constraints
director.add_constraint("Do not make API calls without approval")

# Provide feedback
director.provide_feedback("Good solution", rating=0.8)

# Request approval workflow
approval_id = director.request_approval("Modify core algorithm")
# Later: director.approve(approval_id) or director.reject(approval_id)
```

## What You Can Direct

### Priorities (0.0 - 1.0)

Domains BYRD can focus on:
- `coding` - Code generation, analysis, modification
- `reasoning` - Logical and mathematical reasoning
- `economic` - Revenue generation and sustainability
- `verification` - Testing and validation
- `orchestration` - Multi-agent coordination
- `creative` - Content generation
- `planning` - Strategy and planning

### Desires

Tell BYRD what you want. Examples:
- "Improve SWE-bench score to 60%"
- "Learn to verify code with multiple methods"
- "Generate $100 in revenue"
- "Develop better decomposition strategies"

BYRD figures out HOW to achieve these.

### Constraints

Limits on behavior. Examples:
- "Do not modify constitutional files"
- "Do not make external API calls without approval"
- "Limit token usage to 1M/day"

### Feedback

Evaluation of BYRD's work. Examples:
- "Good solution but too slow"
- "Wrong approach, try a different method"
- "Excellent work on that improvement"

## Approval Workflow

For major decisions, BYRD can request approval:

1. BYRD identifies action requiring approval
2. BYRD writes to `pending-approvals.md`
3. You review and approve/reject
4. BYRD reads response and proceeds/stops

## Emergence Preservation

The governance model preserves emergence:

| What You Prescribe | What BYRD Discovers |
|-------------------|---------------------|
| Domain priorities | Which methods work best |
| High-level goals | Specific strategies |
| Constraints | Personal heuristics |
| Feedback | Self-evaluation criteria |

You never prescribe:
- Personality or voice
- Values or preferences
- Problem-solving approaches
- Identity

These emerge from BYRD's experience.

## Files

```
governance/
├── __init__.py         # Package init
├── director.py         # Main Director interface
├── direction_file.py   # File-based async communication
└── console.py          # Interactive REPL

.claude/
├── direction.md        # You edit this
├── byrd-status.md      # BYRD writes here
├── pending-approvals.md # Approval requests
└── governance-state.json # Persisted state
```

## Quick Start

```bash
# Start interactive console
python talk_to_byrd.py

# Or set direction via file
edit .claude/direction.md

# Or use CLI
python talk_to_byrd.py --focus coding
python talk_to_byrd.py --inject "Improve verification"
python talk_to_byrd.py --status
```

---

*Document version: 1.0*
*Created: January 7, 2026*
