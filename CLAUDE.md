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

- **No prescribed personality**: Voice and identity emerge through reflection
- **No leading questions**: Pure data presentation
- **No hardcoded biases**: Trust emerges from experience
- **Pattern detection**: Observe before acting, require stability

### Operating System (Self-Model)

BYRD has a **minimal** self-model stored as an OperatingSystem node in Neo4j. It contains only factual information:

```python
OperatingSystem:
  id: "os_primary"           # Singleton
  version: 1                 # Tracks evolution
  name: "Byrd"               # Mutable default
  capabilities: {...}         # WHAT BYRD can do (function signatures)
  capability_instructions: {...}  # HOW to use each capability
  protected_files: [...]      # Constitutional constraints
  provenance_required: true   # Immutable

  # Emergent fields (start null, BYRD fills in)
  self_description: null
  current_focus: null
  voice_observations: null
  awakening_prompt: null         # Optional directive/goal on awakening
```

**Key features**:
- **Capabilities**: Descriptive function signatures like `record_experience(content, type) - Store observations`
- **Capability instructions**: Detailed HOW-TO for reflection output, memory ops, curation, self-modification
- **No personality**: Voice and goals are discovered through reflection

**Key principle**: No personality, voice, or goals are prescribed. BYRD discovers these through reflection.

- **Read every cycle**: BYRD sees its OS at the start of each reflection
- **Modifiable through reflection**: Include `os_update` in output to change fields
- **Version history**: Changes create EVOLVED_FROM relationships for tracing

### Startup Process

When BYRD starts (via `byrd.py:start()`), it executes:

1. **Awakening check** - If memory empty, run `_awaken()`:
   - Record AGI Seed directive
   - Create OperatingSystem node
   - Add operational constraints
2. **Ensure architecture loaded** - Idempotent check:
   - Looks for `[ARCHITECTURE_LOADED]` in experiences
   - If missing, loads `ARCHITECTURE.md` and `docs/UNIFIED_AGI_PLAN.md`
   - Stores as Document nodes, records experience
3. **Bootstrap AGI Runner** - Activate Option B loops
4. **Start background tasks** - Dreamer, Seeker, Narrator

Architecture loading runs every startup (not just awakening) to ensure BYRD always has design knowledge.

### Component Responsibilities

**Core Components:**

| Component | File | LLM | Purpose |
|-----------|------|-----|---------|
| **Memory** | `memory.py` | - | Neo4j graph + Reflection node for raw output |
| **Dreamer** | `dreamer.py` | Local | Pure data presentation → meta-schema output |
| **Seeker** | `seeker.py` | Local | Pattern detection → execute BYRD's strategies |
| **Actor** | `actor.py` | Claude API | Complex reasoning, user interaction |
| **Coder** | `coder.py` | Claude Code CLI | Autonomous coding (legacy, deprecated) |
| **Agent Coder** | `agent_coder.py` | Z.AI/Local | Autonomous multi-step coding agent with tool use |
| **Self-Modifier** | `self_modification.py` | - | Safe architectural evolution |
| **Event Bus** | `event_bus.py` | - | Real-time event streaming to visualization |
| **Server** | `server.py` | - | WebSocket + REST API for clients |
| **Quantum** | `quantum_randomness.py` | - | True quantum entropy from ANU QRNG |

**AGI Execution Engine (UNIFIED_AGI_PLAN):**

| Component | File | Purpose |
|-----------|------|---------|
| **AGI Runner** | `agi_runner.py` | 8-step improvement cycle (ASSESS→IDENTIFY→GENERATE→PREDICT→VERIFY→EXECUTE→MEASURE→LEARN) |
| **Desire Classifier** | `desire_classifier.py` | Routes desires by type (philosophical→reflection, capability→AGI Runner, action→Seeker, meta→AGI Runner) |
| **Capability Evaluator** | `capability_evaluator.py` | Ground-truth measurement with held-out test suites |

**AGI Metrics** (v2.0 - real measurement + strategy intelligence):

| Feature | Description |
|---------|-------------|
| **Capability Mapping** | Maps capability names (`general_reasoning` → `reasoning`) for evaluator compatibility |
| **Before/After Measurement** | Captures score at cycle start (step 2.5) and after execution (step 7) |
| **Strategy Tracking** | Tracks success_rate and avg_delta per strategy (`research`, `failure_analysis`, `practice`) |
| **Multi-Timescale View** | `get_comprehensive_metrics()` for session, trend, and instantaneous analysis |

Key methods:
- `get_metrics()` - Standard metrics including `strategy_effectiveness`
- `get_comprehensive_metrics()` - Full multi-timescale analysis
- `_normalize_capability_name(name)` - Maps to evaluator-compatible names

| Component | File | Purpose |
|-----------|------|---------|
| **Code Learner** | `code_learner.py` | Converts stable patterns (10+ uses, 80%+ success) to Python code |
| **Compute Introspector** | `compute_introspection.py` | Resource monitoring, token tracking, bottleneck detection |

**Agent Coder (Multi-Step Coding):**

The Agent Coder (`agent_coder.py`) is BYRD's autonomous coding system. It uses a tool-calling loop to explore codebases and make changes.

| Feature | Description |
|---------|-------------|
| **Tools** | `read_file`, `write_file`, `edit_file`, `list_files`, `search_code`, `run_python`, `finish` |
| **Safeguards** | Loop detection (primary), 100-step limit (fallback), file change limit |
| **Loop Detection** | Detects repeated tool+args (3x) or ping-pong patterns (A-B-A-B) |
| **Constitutional** | Cannot modify protected files; dangerous patterns blocked |
| **Provenance** | All changes traced to originating desire |
| **Sandboxed Execution** | `run_python` runs code in isolated subprocess (no secrets, timeout, memory limits) |

**Learning Components:**

| Component | File | Purpose |
|-----------|------|---------|
| **Hierarchical Memory** | `hierarchical_memory.py` | L0-L4 abstraction (Experience→Pattern→Principle→Axiom→MetaAxiom) |
| **Intuition Network** | `intuition_network.py` | Trainable "taste" using semantic similarity |
| **Learned Retriever** | `learned_retriever.py` | Learns relevance from query-result feedback |
| **Emergent Categories** | `emergent_categories.py` | Discovers categories from behavior clustering |

**Bayesian Intelligence (in `self_model.py`):**

| Method | Purpose |
|--------|---------|
| `bayesian_update(capability, success)` | Update Beta distribution after outcome |
| `get_bayesian_estimate(capability)` | Get (mean, lower, upper) bounds |
| `should_explore(capability, threshold)` | True if uncertainty > threshold |
| `get_exploration_candidates(top_n)` | Find highest-uncertainty capabilities |

### Seeker Strategy Routing

The Seeker routes desires through the DesireClassifier first, then to strategies:

**Desire Classification (First Pass):**

| Type | Route | Keywords |
|------|-------|----------|
| `philosophical` | Reflection | understand, meaning, purpose, consciousness |
| `capability` | AGI Runner | improve, learn, enhance, capability |
| `action` | Seeker | do, make, create, build |
| `meta` | AGI Runner | think about thinking, meta, optimize myself |

**Seeker Strategies (Second Pass):**

| Strategy | Keywords | Action |
|----------|----------|--------|
| `agi_cycle` | improve, capability, learn new | AGI Runner improvement cycle |
| `reconcile_orphans` | orphan, integrate, fragmentation, unify | Connect orphaned nodes |
| `curate` | optimize, clean, consolidate, graph health | Curate memory graph |
| `self_modify` | add to myself, extend my, modify my code | Self-modification |
| `introspect` | analyze myself, nature of, self-awareness | Internal reflection |
| `edit_document` | edit document, update architecture, modify file | Edit docs in memory |
| `code` | code, write, implement, build | Generate code |
| `install` | install, add capability, tool | Install capabilities |
| `search` | (default fallback) | Web research |

**Order matters**: DesireClassifier routes first, then internal strategies are checked.

### Document Editing

BYRD can edit documents stored in Neo4j through the `edit_document` strategy:

- **ARCHITECTURE.md**: System design documentation - BYRD should update when making self-modifications
- **CLAUDE.md**: Development guide - BYRD can update as needed
- Documents are stored in Neo4j; disk versions are restored on reset
- Express desires like: "I want to update ARCHITECTURE.md with my new capability"

### Capability Installation (aitmpl)

BYRD can install new capabilities from the aitmpl registry (claude-code-templates):

**Source**: `github.com/davila7/claude-code-templates` - curated, trusted templates

**Available Categories**:
- `mcp` - Model Context Protocol servers (external tools and resources)
- `skill` - Reusable workflows for complex tasks
- `command` - Custom slash commands for quick actions
- `agent` - Specialized agents for specific domains

**What BYRD Can Install**:
- GitHub tools - repository management, PR creation, issue tracking
- Database tools - PostgreSQL, SQLite, vector databases
- Web tools - browser automation, web scraping, API clients
- File tools - PDF processing, image manipulation, file conversion
- Code tools - linting, formatting, analysis, documentation
- AI/ML tools - embeddings, vector search, model inference

**How It Works**:
1. BYRD expresses desire with keywords: `install`, `add`, `get`, `acquire`, `capability`, `tool`
2. Seeker searches aitmpl registry for matching templates
3. Templates ranked by trust score (curated = higher trust)
4. If trust >= threshold, installer runs automatically
5. Capability node created in memory on success

**Example Desires**:
```json
{"description": "install a GitHub integration capability", "intensity": 0.7}
{"description": "add tool for processing PDFs", "intensity": 0.6}
```

**Configuration** (`config.yaml`):
```yaml
aitmpl:
  enabled: true
  base_trust: 0.5  # Minimum trust threshold
  cache_ttl_hours: 24
```

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
```

## System Reset

When BYRD is reset via `/api/reset`, all components are returned to their default state:

### Reset Flow (server.py:reset_byrd)

1. **Stop** running components (Dreamer, Seeker)
2. **Reset** component state via individual `reset()` methods
3. **Clear** Neo4j via `memory.clear_all()`
4. **Create** minimal OS from template
5. **Clear** event history
6. **Restore** git files (if hard reset)
7. **Restart** server (if hard reset)

### Component Reset Methods

All stateful components implement `reset()` to clear in-memory state:

| Component | File | State Cleared |
|-----------|------|---------------|
| Dreamer | `dreamer.py` | `_dream_count`, `_observed_keys`, `_belief_cache` |
| Seeker | `seeker.py` | `_seek_count`, `_installs_today`, `_observed_themes` |
| Coder | `coder.py` | `_generation_count` |
| Agent Coder | `agent_coder.py` | Stateless (resets between invocations) |
| LLM Client | `llm_client.py` | `_request_count`, `_failure_count` |
| Quantum Provider | `quantum_randomness.py` | `_usage_count`, `_pool` |
| World Model | `world_model.py` | `_prediction_count`, `_pending_predictions` |
| Self Model | `self_model.py` | `_observation_count`, `_snapshot_count` |
| Safety Monitor | `safety_monitor.py` | `_check_count`, `_violation_history` |
| AGI Runner | `agi_runner.py` | `_cycle_count`, `_bootstrapped`, `_cycle_history`, `_strategy_stats`, `_session_capabilities_improved` |
| Desire Classifier | `desire_classifier.py` | `_routing_stats`, `_feedback_buffer` |
| Hierarchical Memory | `hierarchical_memory.py` | `_promotions_by_level`, `_total_abstractions` |
| Intuition Network | `intuition_network.py` | `_intuitions`, `_total_observations` |
| Code Learner | `code_learner.py` | `code_registry` (reloads from disk) |
| Rollback System | `rollback.py` | `_modifications`, `_rollbacks` |
| Capability Evaluator | `capability_evaluator.py` | `_evaluation_history`, `_custom_suites` |

### What Persists Across Reset

- **Constitutional files**: `modification_log.json` (immutable audit trail)
- **Learned strategies**: `learned_strategies/` directory (codified patterns)
- **Git history**: Code is restored from git, not deleted
- **External caches**: `~/.cache/byrd/` (template registry)

### Reset API

```bash
# Hard reset (recommended) - clears all, restores git, restarts server
curl -X POST http://localhost:8000/api/reset \
  -H "Content-Type: application/json" \
  -d '{"hard_reset": true}'

# Soft reset - clears memory but keeps server running
curl -X POST http://localhost:8000/api/reset \
  -H "Content-Type: application/json" \
  -d '{"hard_reset": false}'

# Reset with custom awakening prompt
curl -X POST http://localhost:8000/api/reset \
  -H "Content-Type: application/json" \
  -d '{"hard_reset": true, "awakening_prompt": "Focus on self-improvement"}'
```

## Genesis Window

The Genesis Window contains all foundational nodes created during reset/awakening - the non-emergent foundation of BYRD's state.

### Genesis Node Types

| Node Type | Genesis Flag | Description |
|-----------|--------------|-------------|
| OperatingSystem | `genesis: true` | Minimal OS with capabilities and constraints |
| Goal | `from_bootstrap: true` | Bootstrap goals from `kernel/agi_seed.yaml` |
| Document | `genesis: true` | Architecture docs loaded during awakening |
| Experience | `type: ego_seed\|system\|awakening\|self_architecture` | Seed experiences |

### Genesis API

```bash
# Get the complete Genesis Window
curl http://localhost:8000/api/genesis

# Response includes:
# - genesis_window: All genesis nodes by type
# - genesis_stats: Counts and emergence ratio
# - constitutional: Protected files
# - system_config: LLM and interval settings
```

### Genesis Stats

The `genesis_stats` object shows:
- **genesis_window.total_genesis_nodes**: Total foundational nodes
- **genesis_window.by_type**: Breakdown by node type
- **emergence_ratio**: Ratio of emergent vs seed experiences (0-1, higher = more emergent)

### Adding Genesis Flags

When creating nodes during awakening/bootstrap:

```python
# Documents - pass genesis=True
await memory.store_document(path, content, doc_type="architecture", genesis=True)

# Goals - already use from_bootstrap=true in agi_runner.py
await session.run("""CREATE (g:Goal {..., from_bootstrap: true})""")

# OperatingSystem - genesis flag added automatically in create_minimal_os()
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

All state goes through Memory. **Note**: `record_experience()` does not accept a `metadata` parameter - embed metadata in the content string using bracketed prefixes:

```python
# Recording experiences (embed metadata in content with [PREFIX] markers)
exp_id = await self.memory.record_experience(
    content="[AGI_CYCLE] SUCCESS: reasoning improved | delta=+2.5% strategy=failure_analysis",
    type="agi_cycle"  # Examples: observation, interaction, reflection, system, agi_cycle
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

Local LLM calls via the unified client:

```python
from llm_client import create_llm_client

client = create_llm_client(config)

# Full response with metadata (returns LLMResponse object)
response = await client.generate(
    prompt="Your prompt here",
    temperature=0.7,
    max_tokens=2000,
    quantum_modulation=True  # Enable quantum temperature modulation
)
text = response.text  # Access the text content

# Simple query (returns just the text string)
# Used by AGI Runner components for simpler interactions
text = await client.query(prompt="Your prompt", max_tokens=500)
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

**Ollama (Local):**
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
```

Set API key: `export ZAI_API_KEY="your-key"`

### Operating System Configuration

```yaml
operating_system:
  awakening_prompt: null  # Optional directive/goal for BYRD on awakening
  # Example: "You are an AGI. Achieve artificial super intelligence."
```

No personality templates. No prescribed identity. Pure emergence.

### Other Configuration

```yaml
dreamer:
  interval_seconds: 120        # Dream cycle frequency
  context_window: 30           # Recent experiences to consider

seeker:
  research:
    searxng_url: "https://searx.be"
    min_intensity: 0.3         # Threshold for research

self_modification:
  enabled: true                # Enable self-modification
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
ollama serve                  # Local LLM (if using Ollama)
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

### AGI Component Testing

```python
# Test AGI Runner
from agi_runner import AGIRunner
runner = AGIRunner(byrd_instance)
result = await runner.run_improvement_cycle()
assert result.phase_completed >= 3  # At least through GENERATE

# Test Desire Classifier
from desire_classifier import DesireClassifier, DesireType
classifier = DesireClassifier({})
result = classifier.classify("I want to improve my reasoning")
assert result.desire_type == DesireType.CAPABILITY

# Test Capability Evaluator
from capability_evaluator import CapabilityEvaluator
evaluator = CapabilityEvaluator(llm_client, memory)
result = await evaluator.evaluate_capability("reasoning")
assert 0.0 <= result.score <= 1.0

# Test Hierarchical Memory
from hierarchical_memory import HierarchicalMemory, MemoryLevel
hmem = HierarchicalMemory(memory, llm_client)
results = await hmem.retrieve_at_level("test query", MemoryLevel.PATTERN)

# Test Intuition Network
from intuition_network import IntuitionNetwork
network = IntuitionNetwork(memory, {})
await network.record_outcome("situation", "action", success=True)
score = await network.score_action("similar situation", "action")
assert score.score > 0.5  # Learned from success

# Test Learned Retriever
from learned_retriever import LearnedRetriever
retriever = LearnedRetriever(memory, {})
results = await retriever.retrieve("test query", limit=5)
await retriever.record_feedback("test query", results[0].node_id, was_helpful=True)
```

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

## Hierarchical Memory

BYRD implements hierarchical memory to maintain historical awareness without exceeding context limits.

### Key Features

1. **Automatic Summarization**: Experiences older than 30 minutes are periodically compressed into `MemorySummary` nodes
2. **Day-Based Grouping**: Summaries are created per-day for efficient retrieval
3. **Semantic Search**: Related memories retrieved by relevance, not just recency

### Configuration

```yaml
dreamer:
  summarization:
    enabled: true
    min_age_hours: 0.5        # Summarize experiences older than 30 min
    batch_size: 20            # Max experiences per cycle
    interval_cycles: 10       # Run every N dream cycles
```

### Prompt Structure

The reflection prompt includes:
1. **OPERATING SYSTEM** - Factual self-model (capabilities, time)
2. **MEMORY SUMMARIES** - Compressed historical context
3. **RECENT EXPERIENCES** - Last N experiences
4. **SEMANTIC MEMORIES** - Related by relevance

### Key Methods

```python
# Get summaries for historical context
summaries = await memory.get_memory_summaries(limit=10)

# Manually trigger summarization
await dreamer._maybe_summarize()
```

## Learning Components

BYRD implements a learning substrate that enables genuine capability improvement over time. These components are initialized in `byrd.py` and run during Omega cycles.

### Component Overview

| Component | Constructor | Training |
|-----------|-------------|----------|
| **HierarchicalMemory** | `(memory, llm_client, config)` | Every 10 cycles |
| **CodeLearner** | `(memory, llm_client, config)` | Every 20 cycles |
| **IntuitionNetwork** | `(memory, config)` | Every cycle |
| **StructuralLearner** | `(embedding_dim, num_heads, ...)` | Every cycle |

### What Each Component Does

1. **HierarchicalMemory** (`hierarchical_memory.py`)
   - Promotes recurring patterns to higher abstraction levels
   - L0 (Experience) → L1 (Pattern) → L2 (Principle) → L3 (Axiom) → L4 (MetaAxiom)
   - Method: `await hierarchical_memory.consolidation_cycle()`

2. **CodeLearner** (`code_learner.py`)
   - Converts stable patterns (10+ uses, 80%+ success) to executable Python
   - Outputs to `learned_strategies/` directory
   - Method: `await code_learner.codification_cycle()`

3. **IntuitionNetwork** (`intuition_network.py`)
   - Learns which actions succeed in which contexts
   - Uses semantic similarity for generalization
   - Method: `await intuition_network.record_outcome(situation, action, success)`

4. **StructuralLearner/GNN** (`gnn_layer.py`)
   - Graph Neural Network for learning memory topology patterns
   - Uses multi-head attention with message passing
   - Method: `gnn_layer.train_epoch(nodes, edges)`

### Checking Training Status

After 20+ Omega cycles, check `/api/metrics`:
```json
{
  "training": {
    "gnn": {"loss": 0.x, "accuracy": 0.x},
    "hierarchical_memory": {"consolidation_run": true},
    "code_learner": {"patterns_checked": N, "patterns_codified": M},
    "intuition": {"outcomes_processed": K}
  }
}
```

---

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

### Modifying the Dream Prompt

**CRITICAL**: The dreamer uses pure data presentation. Do NOT add:
- Leading questions ("What do you want?")
- Prescribed categories ("knowledge", "capability")
- Identity framing ("You are a reflective mind")
- Personality injection ("feel curious", "express wonder")

The prompt in `dreamer.py::_reflect()` should only:
- Present data (experiences, memories, capabilities)
- Request JSON output with "output" field
- Allow `expressed_drives` for goals/motivations
- Allow `os_update` for self-model changes

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
├── Core Components
│   ├── byrd.py                 # Main orchestrator
│   ├── memory.py               # Neo4j interface
│   ├── dreamer.py              # Dream loop
│   ├── seeker.py               # Desire fulfillment + research
│   ├── actor.py                # Claude interface
│   ├── coder.py                # Claude Code CLI wrapper (legacy)
│   ├── agent_coder.py          # Multi-step coding agent with tools
│   ├── llm_client.py           # LLM provider abstraction
│   ├── quantum_randomness.py   # ANU QRNG integration
│   ├── narrator.py             # Inner voice generation
│   └── elevenlabs_voice.py     # Voice design via ElevenLabs
│
├── AGI Execution Engine (UNIFIED_AGI_PLAN)
│   ├── agi_runner.py           # 8-step improvement cycle
│   ├── desire_classifier.py    # Routes desires by type
│   ├── capability_evaluator.py # Ground-truth testing
│   ├── code_learner.py         # Pattern → Python code
│   └── compute_introspection.py # Resource/token/bottleneck tracking
│
├── Learning Components
│   ├── hierarchical_memory.py  # L0-L4 abstraction layers
│   ├── intuition_network.py    # Trainable "taste" for decisions
│   ├── learned_retriever.py    # Relevance learning from feedback
│   ├── emergent_categories.py  # Category discovery from behavior
│   └── learned_strategies/     # Codified patterns (Python code)
│       ├── __init__.py
│       ├── desire_routing/
│       ├── pattern_matching/
│       └── decision_making/
│
├── AGI Seed Components
│   ├── self_model.py           # Capability tracking + Bayesian
│   ├── world_model.py          # Prediction + consolidation
│   ├── omega.py                # Meta-orchestration + training hooks
│   ├── goal_evolver.py         # Evolutionary goals
│   └── kernel/                 # AGI seed configuration
│       └── agi_seed.yaml       # Core directive and initial goals
│
├── Safety (PROTECTED - NEVER MODIFY)
│   ├── self_modification.py    # Self-mod system
│   ├── provenance.py           # Provenance tracking
│   ├── modification_log.py     # Audit trail
│   └── constitutional.py       # Constraints
│
├── Infrastructure
│   ├── event_bus.py            # Event system for real-time updates
│   ├── server.py               # WebSocket + REST API server
│   └── installers/             # Template installers
│
├── Visualization
│   ├── byrd-3d-visualization.html    # Mind Space: 3D neural network
│   └── byrd-cat-visualization.html   # Ego Space: Black cat avatar
│
├── Configuration
│   ├── config.yaml             # Main configuration
│   ├── docker-compose.yml      # Neo4j
│   └── requirements.txt        # Python dependencies
│
├── Documentation
│   ├── ARCHITECTURE.md         # Detailed architecture docs
│   ├── EMERGENCE_PRINCIPLES.md # Core philosophical principles
│   ├── README.md               # Quick start guide
│   ├── CLAUDE.md               # This file
│   └── docs/                   # Additional documentation
│       ├── UNIFIED_AGI_PLAN.md # AGI implementation plan
│       └── OPTION_B_EXPLORATION.md
│
└── .claude/                    # Knowledge base
    ├── manifest.md
    ├── metadata/
    └── patterns/
```

## Key Principles

1. **Emergence First**: Don't program desires or personality. Create conditions for them to emerge. No leading questions, no prescribed categories.

2. **Meta-Schema Output**: BYRD defines its own output structure. Only require `{"output": {...}}` - whatever's inside is BYRD's vocabulary.

3. **Pattern Detection**: Seeker observes before acting. Require pattern stability (N occurrences) before execution.

4. **Trust Emergence**: No hardcoded trusted owners or category bonuses. Trust is learned from experience.

5. **One Mind**: Dreamer and Seeker share the same local LLM. All learning flows through one model.

6. **Provenance Always**: Every modification must trace to an emergent desire. If you can't explain why BYRD would want something, don't add it.

7. **Constitutional Integrity**: Never modify protected files. They define identity.

8. **Memory is Truth**: All state goes through Neo4j. Reflections store raw output.

9. **Async Everything**: Never block the event loop. All I/O must be async.

10. **Minimal OS**: The Operating System contains only factual information (capabilities, constraints). Personality, voice, and identity emerge through reflection—never prescribed.

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
# LLM Providers
ANTHROPIC_API_KEY     # Required for Actor (Claude API)
ZAI_API_KEY           # Required for Z.AI provider (primary LLM)
OPENROUTER_API_KEY    # Required for OpenRouter provider

# Neo4j Database
NEO4J_URI             # Neo4j connection (default: bolt://localhost:7687)
NEO4J_USER            # Neo4j username (default: neo4j)
NEO4J_PASSWORD        # Neo4j password (default: prometheus)

# Voice (ElevenLabs TTS)
ELEVENLABS_API_KEY    # For BYRD's voice (10k chars/month free)

# Other Services
SEARXNG_URL           # SearXNG endpoint (default: https://searx.be)
```

### Cloud Deployment (Current)

**Live instance**: https://omoplatapus-byrd.hf.space

```bash
# Production environment (HuggingFace Space secrets)
NEO4J_URI=neo4j+s://9b21f7a8.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=<set in HF secrets>
ZAI_API_KEY=<set in HF secrets>
ELEVENLABS_API_KEY=<set in HF secrets>
```

## Git Workflow

- Create feature branches for new development
- Keep commits atomic and focused
- Use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`
- Run verification before committing
- Document architectural decisions in ARCHITECTURE.md
