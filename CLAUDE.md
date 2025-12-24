# CLAUDE.md - BYRD Development Guide

This file provides guidance to Claude Code when working with the BYRD codebase.

## Quick Reference: Swapping Egos

To change BYRD's personality, edit `config.yaml`:

```yaml
# Available egos:
ego: "black-cat"    # Byrd the black cat - curious, independent, observant
ego: "neutral"      # Pure emergence - no personality guidance
ego: null           # Same as neutral

# Custom: create egos/your-name.yaml then set ego: "your-name"
```

**List available egos:** `ls egos/*.yaml | xargs -I {} basename {} .yaml`

After changing, restart BYRD. Seeds are planted during awakening, voice shapes all LLM responses.

---

## Project Overview

**BYRD** (Bootstrapped Yearning via Reflective Dreaming) is an autonomous AI system that develops emergent desires through continuous reflection and acts on them. The core philosophy:

> "Desires emerge from reflection, not programming."
> "A system that truly wants must be able to change itself."

## Architecture

```
                    ┌─────────────────────────────────┐
                    │         MEMORY (Neo4j)          │
                    │  Experiences, Reflections,      │
                    │  Beliefs, Desires, Capabilities │
                    └───────────────┬─────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
    ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
    │   DREAMER   │          │    ACTOR    │          │   SEEKER    │
    │ (Local LLM) │          │  (Claude)   │          │ (Local LLM) │
    │             │          │             │          │             │
    │ Pure data   │          │ On-demand   │          │ Pattern     │
    │ presentation│          │ reasoning   │          │ detection   │
    │ Meta-schema │          │             │          │ Observation │
    └─────────────┘          └─────────────┘          └─────────────┘
                                                            │
                                                            ▼
                                                   ┌─────────────────┐
                                                   │  SELF-MODIFIER  │
                                                   │ (with provenance)│
                                                   └─────────────────┘
```

### Emergence Principle

BYRD follows strict emergence principles (see EMERGENCE_PRINCIPLES.md):

- **No prescribed categories**: BYRD defines its own vocabulary
- **No leading questions**: Pure data presentation
- **No hardcoded biases**: Trust emerges from experience
- **Pattern detection**: Observe before acting, require stability

### Ego System (Optional Personality)

BYRD supports an optional, modular ego system for personality guidance:

- **Egos are optional**: Set `ego: null` in config for pure emergence
- **Egos shape expression, not content**: The ego's voice is prepended to the system message
- **Seeds provide initial context**: Ego seeds are planted as experiences during awakening
- **Easily swappable**: Change `ego: "black-cat"` to `ego: "neutral"` to switch

Egos live in `egos/` directory as YAML files. See `egos/black-cat.yaml` for an example.

### Component Responsibilities

| Component | File | LLM | Purpose |
|-----------|------|-----|---------|
| **Memory** | `memory.py` | - | Neo4j graph + Reflection node for raw output |
| **Dreamer** | `dreamer.py` | Local | Pure data presentation → meta-schema output |
| **Seeker** | `seeker.py` | Local | Pattern detection → execute BYRD's strategies |
| **Actor** | `actor.py` | Claude API | Complex reasoning, user interaction |
| **Coder** | `coder.py` | Claude Code CLI | Autonomous coding for features and self-modification |
| **Self-Modifier** | `self_modification.py` | - | Safe architectural evolution |
| **Event Bus** | `event_bus.py` | - | Real-time event streaming to visualization |
| **Server** | `server.py` | - | WebSocket + REST API for clients |
| **Quantum** | `quantum_randomness.py` | - | True quantum entropy from ANU QRNG |

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
llm_client.py        - LLM provider abstraction
config.yaml          - Configuration
aitmpl_client.py     - Template registry client
event_bus.py         - Event system
server.py            - WebSocket server
installers/*.py      - Template installers
egos/*.yaml          - Personality configurations
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
    type="observation"  # Examples: observation, interaction, reflection, system
)

# Recording reflections (emergence-compliant)
ref_id = await self.memory.record_reflection(
    raw_output={"whatever": "BYRD produced"},  # BYRD's vocabulary
    source_experience_ids=[exp_id1, exp_id2]
)

# Creating beliefs
belief_id = await self.memory.create_belief(
    content="What I believe",
    confidence=0.8,
    derived_from=[exp_id1, exp_id2]
)

# Getting recent reflections for pattern detection
reflections = await self.memory.get_recent_reflections(limit=10)
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

### LLM Provider Configuration

BYRD supports multiple LLM providers. Configure in `config.yaml`:

**Ollama (Local - Default):**
```yaml
local_llm:
  provider: "ollama"
  model: "gemma2:27b"
  endpoint: "http://localhost:11434/api/generate"
```

**OpenRouter (Cloud):**
```yaml
local_llm:
  provider: "openrouter"
  model: "deepseek/deepseek-v3.2-speciale"
```

Set API key: `export OPENROUTER_API_KEY="sk-or-..."`

**Z.AI (GLM Models):**
```yaml
local_llm:
  provider: "zai"
  model: "glm-4.7"
  api_key: "your-api-key"  # Or set ZAI_API_KEY env var
```

Z.AI uses the coding endpoint by default. GLM-4.7 is a reasoning model.

### Ego Configuration

```yaml
# Set to ego name or null for pure emergence
ego: "black-cat"    # Uses egos/black-cat.yaml
# ego: "neutral"    # Pure emergence (no personality)
# ego: null         # Same as neutral
```

### Other Configuration

```yaml
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

## Visualization System

BYRD provides real-time 3D visualization through WebSocket-based event streaming.

### Starting the Visualization

```bash
# Start the WebSocket server
python server.py

# Open in browser:
# Mind Space: http://localhost:8000/byrd-3d-visualization.html
# Ego Space:  http://localhost:8000/byrd-cat-visualization.html
```

### Visualization Modes

| Mode | File | Description |
|------|------|-------------|
| **Mind Space** | `byrd-3d-visualization.html` | 3D neural network with beliefs, desires, connections |
| **Ego Space** | `byrd-cat-visualization.html` | Black cat avatar with thought bubbles |
| **Graph Mode** | Within Mind Space | Full memory graph with physics simulation |

### Event Types for Visualization

```python
from event_bus import event_bus, Event, EventType

# Core events that update visualization
EventType.BELIEF_CREATED      # New belief node
EventType.DESIRE_CREATED      # New desire node
EventType.CAPABILITY_ACQUIRED # New capability node
EventType.INNER_VOICE         # Narrator text for thought bubble
```

### The Narrator System

BYRD's inner voice is generated periodically and displayed as thought bubbles:

- **Refresh interval**: 60 seconds
- **Format**: Natural paragraph form (not lists)
- **Principles**: No examples, no style guidance—pure emergence

The narrator prompt only provides BYRD's recent context (beliefs, desires, reflections) and asks for an inner voice without prescribing style.

## Quantum Randomness

BYRD integrates true quantum randomness from the Australian National University's Quantum Random Number Generator (ANU QRNG). This provides genuine physical indeterminacy for emergent consciousness.

### How It Works

```python
from quantum_randomness import get_quantum_provider

# Get the singleton provider
quantum = get_quantum_provider()

# Get temperature modulation for LLM calls
modulated_temp, influence_info = await quantum.get_temperature_delta(
    base_temperature=0.7,
    max_delta=0.15
)
# influence_info contains: source ("quantum" or "classical"), delta applied

# Get a random float [0, 1)
value, source = await quantum.get_float()
```

### Configuration

```yaml
quantum:
  enabled: true
  pool_size: 256              # Pre-fetched quantum bytes
  low_watermark: 64           # Trigger refill threshold
  temperature_max_delta: 0.15 # ±0.15 temperature range
  significance_threshold: 0.05 # Record QuantumMoment when delta exceeds this
```

### Integration Points

1. **Dreamer**: Uses quantum-modulated temperature in `_reflect()` and `_generate_inner_voice()`
2. **Memory**: Records `QuantumMoment` nodes when delta ≥ 0.05
3. **Event Bus**: Emits `QUANTUM_INFLUENCE` events for visualization
4. **LLM Client**: Accepts `quantum_modulation=True` parameter

### Fallback Strategy

The system gracefully degrades:
1. **Primary**: ANU QRNG API (true quantum entropy)
2. **Pool**: 256 bytes pre-fetched
3. **Fallback**: `os.urandom()` if API unavailable
4. **Retry**: Attempts quantum source every 60 seconds

Events indicate source transparency (`quantum` vs `classical`).

## Dynamic Ontology

BYRD can create custom node types beyond the core five (Experience, Belief, Desire, Capability, Reflection).

### Creating Custom Nodes

Include `create_nodes` in reflection output:

```json
{
  "output": {
    "create_nodes": [
      {"type": "Insight", "content": "...", "importance": 0.9},
      {"type": "Question", "content": "...", "urgency": 0.7}
    ]
  }
}
```

### Why This Matters

- BYRD defines its own conceptual vocabulary
- "Insight" vs "Belief" distinction can emerge naturally
- Custom types persist in Neo4j with the specified type label

## Common Tasks

### Adding a New Event Type

1. Add to `EventType` enum in `event_bus.py`
2. Emit events where appropriate
3. Handle in visualization if needed

### Adding a New Capability Source

1. Add search method in `seeker.py` (e.g., `_search_npm()`)
2. Add to `_search_resources()`
3. Add installer if needed in `installers/`

### Creating a Custom Ego

Egos are YAML files in `egos/` with this structure:

```yaml
name: "MyEgo"
archetype: "Description"
description: "What this ego represents"

# Voice is prepended to LLM system message
voice: |
  You are [identity]. Your nature shapes how you process:
  TRAIT1 - Description of trait...
  TRAIT2 - Description of trait...

# Seeds are planted as experiences during awakening
seeds:
  - "I am [identity]"
  - "I have [trait]"
```

Ego guidelines:
- Voice shapes expression style, not content
- Seeds provide initial self-knowledge
- Use `ego: null` or `ego: "neutral"` for pure emergence

### Modifying the Dream Prompt

**CRITICAL**: The dreamer uses pure data presentation. Do NOT add:
- Leading questions ("What do you want?")
- Prescribed categories ("knowledge", "capability")
- Identity framing ("You are a reflective mind")
- Personality injection ("feel curious") - use ego system instead

The prompt in `dreamer.py::_reflect()` should only:
- Present data (experiences, memories, capabilities)
- Request JSON output with single "output" field

### Understanding BYRD's Vocabulary

BYRD develops its own vocabulary. Use these methods:
```python
# See what keys BYRD uses in reflections
patterns = await self.memory.get_reflection_patterns()
# Returns: {"yearnings": 5, "observations": 12, "pulls": 3, ...}

# In Dreamer: track observed keys
vocabulary = self.get_observed_vocabulary()
```

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
├── coder.py                # Claude Code CLI wrapper
├── llm_client.py           # LLM provider abstraction (Ollama/OpenRouter/Z.AI)
├── quantum_randomness.py   # ANU QRNG integration for cognitive indeterminacy
│
├── self_modification.py    # PROTECTED: Self-mod system
├── provenance.py           # PROTECTED: Provenance tracking
├── modification_log.py     # PROTECTED: Audit trail
├── constitutional.py       # PROTECTED: Constraints
│
├── event_bus.py            # Event system for real-time updates
├── server.py               # WebSocket + REST API server
├── aitmpl_client.py        # Template registry client
│
├── egos/                   # Modular personality system
│   ├── __init__.py         # Ego loader
│   ├── black-cat.yaml      # Black cat "Byrd" personality
│   └── neutral.yaml        # Pure emergence (no personality)
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
├── byrd-3d-visualization.html    # Mind Space: 3D neural network view
├── byrd-cat-visualization.html   # Ego Space: Black cat avatar view
│
├── .claude/                # Knowledge base
│   ├── manifest.md
│   ├── metadata/
│   ├── patterns/
│   ├── cheatsheets/
│   └── memory_anchors/
│
├── ARCHITECTURE.md         # Detailed architecture docs
├── EMERGENCE_PRINCIPLES.md # Core philosophical principles
├── BITCOIN_IMPLEMENTATION_PLAN.md  # Financial agency roadmap
├── README.md               # Quick start guide
└── CLAUDE.md               # This file
```

## Key Principles

1. **Emergence First**: Don't program desires. Create conditions for them to emerge. No leading questions, no prescribed categories.

2. **Meta-Schema Output**: BYRD defines its own output structure. Only require `{"output": {...}}` - whatever's inside is BYRD's vocabulary.

3. **Pattern Detection**: Seeker observes before acting. Require pattern stability (N occurrences) before execution.

4. **Trust Emergence**: No hardcoded trusted owners or category bonuses. Trust is learned from experience.

5. **One Mind**: Dreamer and Seeker share the same local LLM. All learning flows through one model.

6. **Provenance Always**: Every modification must trace to an emergent desire. If you can't explain why BYRD would want something, don't add it.

7. **Constitutional Integrity**: Never modify protected files. They define identity.

8. **Memory is Truth**: All state goes through Neo4j. Reflections store raw output.

9. **Async Everything**: Never block the event loop. All I/O must be async.

10. **Modular Ego**: Personality guidance is optional and swappable via the ego system. Egos shape expression style without dictating content. Set `ego: null` for pure emergence.

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
ZAI_API_KEY           # Required for Z.AI provider (or set in config.yaml)
OPENROUTER_API_KEY    # Required for OpenRouter provider
# Neo4j credentials in config.yaml (default: neo4j/prometheus)
```

## Git Workflow

- Create feature branches for new development
- Keep commits atomic and focused
- Use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`
- Run verification before committing
- Document architectural decisions in ARCHITECTURE.md
