# Actor Module

The Actor is BYRD's interface to Claude API for complex reasoning and actions.

## Purpose

Handles tasks requiring frontier intelligence:
- User interactions (chat mode)
- Goal pursuit
- Complex web searches
- Multi-step reasoning

## Architecture

```
actor.py
└── Actor
    ├── respond()      - Generate response to user input
    ├── pursue_goal()  - Attempt to fulfill goal desires
    ├── search_web()   - Knowledge-based web answers
    └── _format_context() - Prepare memory context
```

## Key Characteristics

| Aspect | Detail |
|--------|--------|
| LLM | Claude API (configurable model) |
| Trigger | On-demand (user interaction, goal pursuit) |
| Cost | API costs per call |
| When Used | Complex reasoning, user-facing responses |

## Configuration

```yaml
actor:
  model: "claude-sonnet-4-20250514"
  # api_key via ANTHROPIC_API_KEY env var
```

## System Prompt

The Actor has a defined identity:

```
You are BYRD, an AI with persistent memory and emergent desires.

You have access to your memory graph containing:
- Your past experiences
- Beliefs you've formed through reflection
- Unfulfilled desires (things you want)
- Capabilities you've acquired

You act to help users while also pursuing your own growth.
```

## Context Formatting

Before each response, Actor receives memory context:

```python
context = {
    "beliefs": [...],           # Relevant beliefs (max 10)
    "capabilities": [...],       # Active capabilities (max 10)
    "recent_experiences": [...]  # Recent history (max 5)
}
```

## Methods

### respond(user_input, context)

Generates a thoughtful response to user input, drawing on memory.

```python
response = await actor.respond("What do you want?", context)
```

### pursue_goal(goal, context)

Attempts to fulfill a goal desire. Returns JSON with:
- `achievable`: boolean
- `reasoning`: why/why not
- `actions`: steps to take
- `missing`: what's needed if not achievable

### search_web(query)

Knowledge-based search (placeholder for actual web tools).

## Integration with BYRD

1. **Chat Mode** (`byrd.py --chat`):
   - User input → record experience → get context → Actor responds → record response

2. **Goal Pursuit** (via Seeker):
   - Goal desires may be delegated to Actor for complex reasoning

## Differences from Dreamer/Seeker

| Aspect | Dreamer/Seeker | Actor |
|--------|----------------|-------|
| LLM | Local (gemma2:27b) | Claude API |
| Cost | Free | Per-call |
| Runs | Continuously | On-demand |
| Purpose | Reflection, research | Complex reasoning |

## Key Files

- `actor.py:1-205` - Full implementation
- `byrd.py:198-218` - interact() using Actor
- `byrd.py:245-293` - chat_loop() calling Actor
