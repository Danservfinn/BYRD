# CLAUDE.md - BYRD Development Guide

This file provides guidance to Claude Code when working with the BYRD codebase.

## Project Overview

**BYRD** (Bootstrapped Yearning via Reflective Dreaming) is an autonomous AI system that develops emergent desires through continuous reflection and acts on them. The core philosophy:

> "Desires emerge from reflection, not programming."
> "A system that truly wants must be able to change itself."

## Architecture

```
                    ┌─────────────────────────────────┐
                    │         MEMORY (Neo4j)          │
                    │   Experiences, Beliefs, Desires │
                    │        Capabilities             │
                    └───────────────┬─────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
    ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
    │   DREAMER   │          │    ACTOR    │          │   SEEKER    │
    │ (gemma2:27b)│          │  (Claude)   │          │ (gemma2:27b)│
    │             │          │             │          │             │
    │ Continuous  │          │ On-demand   │          │ Continuous  │
    │ reflection  │          │ reasoning   │          │ fulfillment │
    └─────────────┘          └─────────────┘          └─────────────┘
                                                            │
                                                            ▼
                                                   ┌─────────────────┐
                                                   │  SELF-MODIFIER  │
                                                   │ (with provenance)│
                                                   └─────────────────┘
```

### Component Responsibilities

| Component | File | LLM | Purpose |
|-----------|------|-----|---------|
| **Memory** | `memory.py` | - | Neo4j graph database interface |
| **Dreamer** | `dreamer.py` | Local (gemma2:27b) | Continuous reflection, forms beliefs/desires |
| **Seeker** | `seeker.py` | Local (gemma2:27b) | Fulfills desires via research and capability acquisition |
| **Actor** | `actor.py` | Claude API | Complex reasoning, user interaction, goal pursuit |
| **Self-Modifier** | `self_modification.py` | - | Safe architectural evolution |

## Constitutional Constraints (CRITICAL)

BYRD has a two-tier file system that **MUST** be respected:

### PROTECTED Files (Never Modify)

These files define BYRD's identity and cannot be modified:

```
provenance.py        - Traces modifications to emergent desires
modification_log.py  - Immutable audit trail
self_modification.py - The modification system itself
constitutional.py    - These constraints
```

**Why**: Without these, BYRD cannot verify its own emergence. They are what makes BYRD *BYRD*.

### MODIFIABLE Files (Can Be Enhanced)

```
byrd.py              - Main orchestrator
dreamer.py           - Reflection process
seeker.py            - Desire fulfillment
actor.py             - Claude interface
memory.py            - Database interface
config.yaml          - Configuration
aitmpl_client.py     - Template registry client
event_bus.py         - Event system
server.py            - WebSocket server
installers/*.py      - Template installers
```

## Code Patterns

### Async Throughout

All I/O operations are async. Use `async/await`:

```python
# Correct
async def _seek_knowledge(self, desire: Dict):
    results = await self._search_searxng(query)
    await self.memory.record_experience(content, type="research")

# Wrong - blocking I/O
def _seek_knowledge(self, desire: Dict):
    results = requests.get(url)  # Blocks event loop
```

### Event-Driven Architecture

Use `event_bus` for real-time notifications:

```python
from event_bus import event_bus, Event, EventType

await event_bus.emit(Event(
    type=EventType.DESIRE_CREATED,
    data={"id": desire_id, "description": desc}
))
```

### Memory Graph Operations

All state goes through Memory:

```python
# Recording experiences
exp_id = await self.memory.record_experience(
    content="What happened",
    type="observation"  # observation, interaction, action, dream, research
)

# Creating beliefs
belief_id = await self.memory.create_belief(
    content="What I believe",
    confidence=0.8,
    derived_from=[exp_id1, exp_id2]
)

# Creating desires
desire_id = await self.memory.create_desire(
    description="What I want",
    type="knowledge",  # knowledge, capability, goal, exploration, self_modification
    intensity=0.7,
    plan=["step1", "step2"]
)
```

### LLM Interaction Pattern

Local LLM calls via Ollama:

```python
async def _query_local_llm(self, prompt: str, max_tokens: int = 500) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            self.local_endpoint,
            json={
                "model": self.local_model,  # gemma2:27b
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": max_tokens}
            }
        )
        return response.json().get("response", "")
```

### JSON Response Parsing

LLM responses often contain markdown code blocks:

```python
# Handle markdown code blocks in LLM output
text = response.strip()
if "```json" in text:
    text = text.split("```json")[1].split("```")[0]
elif "```" in text:
    text = text.split("```")[1].split("```")[0]

result = json.loads(text.strip())
```

## Configuration

Configuration lives in `config.yaml`. Key sections:

```yaml
local_llm:
  model: "gemma2:27b"           # Shared by Dreamer and Seeker
  endpoint: "http://localhost:11434/api/generate"

dreamer:
  interval_seconds: 60          # Dream cycle frequency
  context_window: 50            # Recent experiences to consider

seeker:
  research:
    searxng_url: "http://localhost:8888"
    min_intensity: 0.4          # Threshold for research
  capabilities:
    trust_threshold: 0.5        # Minimum trust for installs
    max_installs_per_day: 3

self_modification:
  enabled: false                # Enable when ready
  require_health_check: true
  auto_rollback_on_failure: true
```

## Development Commands

```bash
# Start BYRD (continuous mode)
python byrd.py

# Interactive chat mode
python byrd.py --chat

# Check system status
python byrd.py --status

# Start visualization server
python server.py

# Start required services
docker-compose up -d          # Neo4j + SearXNG
ollama serve                  # Local LLM
```

## Testing Approach

### Manual Verification

```bash
# Verify Neo4j connection
python -c "from memory import Memory; import asyncio; m = Memory({}); asyncio.run(m.connect())"

# Verify Ollama
curl http://localhost:11434/api/generate -d '{"model": "gemma2:27b", "prompt": "test"}'

# Verify SearXNG
curl "http://localhost:8888/search?q=test&format=json"
```

### Component Testing

When modifying components, verify:

1. **Memory**: Can create/query all node types
2. **Dreamer**: Produces valid JSON with insights, beliefs, desires
3. **Seeker**: Can search and synthesize results
4. **Actor**: Responds with context

## Common Tasks

### Adding a New Desire Type

1. Add type to `memory.py` Desire class documentation
2. Add handler in `seeker.py::_seek_cycle()`
3. Update Dreamer prompt if needed

### Adding a New Event Type

1. Add to `EventType` enum in `event_bus.py`
2. Emit events where appropriate
3. Handle in visualization if needed

### Adding a New Capability Source

1. Add search method in `seeker.py` (e.g., `_search_npm()`)
2. Add to `_search_resources()`
3. Add installer if needed in `installers/`

### Modifying the Dream Prompt

The prompt in `dreamer.py::_reflect()` shapes what BYRD notices. Changes here significantly impact behavior. Be thoughtful about:

- Not injecting specific interests (preserve emergence)
- Maintaining the JSON output format
- Keeping self-reflection capabilities

## Dangerous Patterns (Avoid)

The constitutional system blocks these patterns in self-modifications. Avoid them in regular development too:

```python
# DANGEROUS - blocked by constitutional constraints
os.system(...)           # Shell execution
subprocess.call(...)     # Shell execution
eval(...)                # Code execution
exec(...)                # Code execution
__import__(...)          # Dynamic imports
open(...)                # Direct file I/O (use memory system)
```

## Project Structure

```
byrd/
├── byrd.py                 # Main orchestrator
├── memory.py               # Neo4j interface
├── dreamer.py              # Dream loop
├── seeker.py               # Desire fulfillment + research
├── actor.py                # Claude interface
│
├── self_modification.py    # PROTECTED: Self-mod system
├── provenance.py           # PROTECTED: Provenance tracking
├── modification_log.py     # PROTECTED: Audit trail
├── constitutional.py       # PROTECTED: Constraints
│
├── event_bus.py            # Event system
├── server.py               # WebSocket server
├── aitmpl_client.py        # Template registry client
│
├── installers/             # Template installers
│   ├── base.py
│   ├── mcp_installer.py
│   ├── agent_installer.py
│   ├── command_installer.py
│   ├── skill_installer.py
│   ├── hook_installer.py
│   └── settings_installer.py
│
├── config.yaml             # Configuration
├── docker-compose.yml      # Neo4j + SearXNG
├── requirements.txt        # Python dependencies
│
├── .claude/                # Knowledge base
│   ├── manifest.md
│   ├── metadata/
│   ├── patterns/
│   ├── cheatsheets/
│   └── memory_anchors/
│
├── ARCHITECTURE.md         # Detailed architecture docs
├── README.md               # Quick start guide
└── CLAUDE.md               # This file
```

## Key Principles

1. **Emergence First**: Don't program desires. Create conditions for them to emerge.

2. **One Mind**: Dreamer and Seeker share the same local LLM (gemma2:27b). All learning flows through one model.

3. **Provenance Always**: Every modification must trace to an emergent desire. If you can't explain why BYRD would want something, don't add it.

4. **Constitutional Integrity**: Never modify protected files. They define identity.

5. **Memory is Truth**: All state goes through Neo4j. Don't keep state in Python objects that should persist.

6. **Async Everything**: Never block the event loop. All I/O must be async.

7. **Events for UI**: Emit events for anything the visualization might care about.

## Dependencies

```
neo4j>=5.0.0          # Graph database driver
httpx>=0.25.0         # Async HTTP client
anthropic>=0.39.0     # Claude API
pyyaml>=6.0           # Config parsing
fastapi>=0.109.0      # WebSocket server
uvicorn[standard]     # ASGI server
websockets>=12.0      # WebSocket support
```

## Environment Variables

```bash
ANTHROPIC_API_KEY     # Required for Actor (Claude API)
# Neo4j credentials in config.yaml (default: neo4j/prometheus)
```

## Git Workflow

- Create feature branches for new development
- Keep commits atomic and focused
- Use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`
- Run verification before committing
- Document architectural decisions in ARCHITECTURE.md
