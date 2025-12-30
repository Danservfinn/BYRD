# BYRD: Bootstrapped Yearning via Reflective Dreaming

## Philosophy

> "The system that truly thinks must also truly want."

> "Desires emerge from reflection, not programming."

> "Make each LLM call more valuable through smart scaffolding."

This architecture is built on three insights:

1. **Desires emerge from reflection** — Instead of programming goals, we create a system that dreams. From dreams, wants arise naturally.

2. **A system that truly wants must change itself** — If BYRD's desires are genuine, it must have the power to act on them—including desires to modify its own architecture.

3. **Intelligence is scaffolding** — The LLM provides the intelligence. Everything else is scaffolding that makes each LLM call more valuable.

---

## Architecture Overview

```
                              ┌─────────────────────────────────────┐
                              │           UNIFIED MEMORY            │
                              │              (Neo4j)                │
                              │                                     │
                              │   Experiences, Reflections, Beliefs,│
                              │   Desires, Capabilities, Crystals   │
                              └───────────────┬─────────────────────┘
                                              │
      ┌───────────────────────────────────────┼───────────────────────────────────────┐
      │                   │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│    DREAMER    │   │    SEEKER     │   │     ACTOR     │   │    CODER      │   │    VOICE      │
│  (Local LLM)  │   │  (Local LLM)  │   │   (Claude)    │   │ (Claude Code) │   │ (ElevenLabs)  │
│               │   │               │   │               │   │               │   │               │
│  Continuous   │   │  Fulfills     │   │  Complex      │   │  Autonomous   │   │  Text-to-     │
│  reflection   │   │  desires      │   │  reasoning    │   │  coding       │   │  speech       │
│  Forms wants  │   │  Research     │   │  User chat    │   │  Self-mod     │   │  Voice design │
│               │   │  Strategy     │   │               │   │               │   │               │
└───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘
        │                   │                                       │
        └───────────────────┴───────────────────────────────────────┘
                                        │
                              ┌─────────▼─────────┐
                              │   SELF-MODIFIER   │
                              │  (with provenance)│
                              └───────────────────┘
```

---

## Core Components

### 1. Memory (Neo4j)

The unified graph holds everything. All state, all learning, all provenance.

**Core Node Types:**

| Node Type | Purpose |
|-----------|---------|
| `Experience` | What happened (interactions, observations, research, system events) |
| `Belief` | What BYRD believes (with confidence 0-1) |
| `Desire` | What BYRD wants (with intensity 0-1, and intent) |
| `Capability` | What BYRD can do (innate, installed, learned) |
| `Reflection` | Raw dream cycle outputs (BYRD's own vocabulary) |
| `Crystal` | Crystallized memories (unified concepts from related nodes) |
| `OperatingSystem` | BYRD's mutable self-model (singleton) |
| `Seed` | Foundational identity statements (linked from OS) |
| `Constraint` | Operational constraints (linked from OS) |
| `Strategy` | Learned approaches (linked from OS) |
| `QuantumMoment` | Quantum influence records |
| `SystemState` | System counters and state |
| `LoopMetric` | Per-cycle metrics from Option B compounding loops |

### 2. Operating System (Self-Model)

The **OperatingSystem** is BYRD's mutable self-model, stored as a singleton node in Neo4j. It contains factual information about BYRD's capabilities and constraints.

```
                         ┌─────────────────────────────────────┐
                         │        OperatingSystem Node         │
                         │                                     │
                         │  IMMUTABLE:                         │
                         │  - id, constitutional_files         │
                         │  - provenance_requirement           │
                         │  - created_at, template_id          │
                         │                                     │
                         │  PROVENANCE REQUIRED:               │
                         │  - name, voice, archetype           │
                         │  - description                      │
                         │                                     │
                         │  FREELY MUTABLE:                    │
                         │  - current_focus, emotional_tone    │
                         │  - cognitive_style, self_definition │
                         └───────────────┬─────────────────────┘
                                         │
        ┌────────────────┬───────────────┼───────────────┬────────────────┐
        │                │               │               │                │
        ▼                ▼               ▼               ▼                ▼
   ┌─────────┐     ┌─────────┐     ┌─────────┐    ┌──────────┐     ┌─────────┐
   │  Seed   │     │ Belief  │     │ Desire  │    │Constraint│     │Strategy │
   └─────────┘     └─────────┘     └─────────┘    └──────────┘     └─────────┘
        │                │               │               │                │
    HAS_SEED      BELIEVES_SELF   CURRENT_FOCUS   CONSTRAINED_BY    EMPLOYS
```

### 3. Kernel (Configuration)

The **Kernel** is a Python configuration loaded from `kernel/agi_seed.yaml`. It defines:

- **awakening_prompt**: The directive that starts BYRD's journey
- **identity**: List of identity statements
- **values**: List of value statements
- **constraints**: Operational constraints
- **capability_instructions**: How to use each major capability
- **seeds**: Initial beliefs/desires to plant
- **initial_goals**: Goals to seed the Goal Evolver population

The Kernel informs the OperatingSystem at awakening but is not stored as a Neo4j node.

### 4. Dreamer (Local LLM)

Runs continuously in the background. Takes recent experiences, finds related memories, reflects, and outputs:
- New beliefs (`create_belief`)
- New desires (`expressed_drives`)
- OS updates (`os_update`)
- Voice design requests (`voice_design`) - includes formal voice acknowledgment via `acknowledged=true`
- Self-definition updates (`self_definition`)

**Key Features:**
- Quantum-modulated temperature for genuine indeterminacy
- Semantic search for relevance-based memory retrieval
- Hierarchical memory with summaries
- Memory crystallization (forming Crystal nodes)

### 5. Seeker (Local LLM + Tools)

Fulfills desires autonomously through strategy routing:

| Strategy | Keywords | Action |
|----------|----------|--------|
| `introspect` | analyze myself, understand my code | Internal reflection |
| `source_introspect` | read my code, examine my files | Source code analysis |
| `reconcile_orphans` | orphan, integrate, unify | Connect orphaned nodes |
| `curate` | optimize, clean, consolidate | Graph optimization |
| `self_modify` | modify my code, extend myself | Self-modification |
| `edit_document` | edit document, update architecture | Edit docs in memory |
| `code` | code, write, implement | Generate code |
| `install` | install, add capability, tool | Install capabilities from aitmpl |
| `agi_cycle` | improve capability, learn | AGI Runner improvement cycle |
| `observe` | observe, watch, monitor | Passive observation |
| `search` | (default) | Web research via DuckDuckGo |

### 6. Actor (Claude API)

Executes when there's something complex to do:
- User interaction via chat
- Complex reasoning tasks
- Goal pursuit requiring frontier intelligence

### 7. Agent Coder (`agent_coder.py`)

BYRD's autonomous multi-step coding agent:
- Tool-calling loop: `read_file`, `write_file`, `edit_file`, `list_files`, `search_code`, `finish`
- Loop detection (primary safeguard): stops on repeated actions or ping-pong patterns
- 100-step fallback limit (rarely hit due to loop detection)
- Constitutional constraints: cannot modify protected files
- Provenance tracking: all changes trace to originating desire
- Post-modification safety checks

**Legacy**: `coder.py` (Claude Code CLI wrapper) is deprecated.

### 8. Voice (ElevenLabs)

Text-to-speech integration:
- Voice Design API for creating unique voices
- Credit tracking for free tier (10k chars/month)
- Voice emerges through BYRD's self-reflection

### 9. Self-Modifier

Enables BYRD to modify its own code with provenance:
- Verifies modification traces to emergent desire
- Creates checkpoints before changes
- Runs health checks
- Records modifications as experiences

---

## LLM Providers

BYRD supports multiple LLM providers. Configure in `config.yaml`:

| Provider | Model Examples | Use Case |
|----------|---------------|----------|
| **Z.AI** | `glm-4.7`, `glm-4.5-flash` | Primary (reasoning) |
| **OpenRouter** | `deepseek/deepseek-v3.2-speciale` | Cloud alternative |
| **Ollama** | `gemma2:27b`, `qwen2.5:32b` | Local (self-hosted) |

**One Mind Principle**: Dreamer and Seeker share the same LLM. All learning flows through one model to preserve emergence.

**Global Rate Limiter**: The `GlobalRateLimiter` class in `llm_client.py` ensures minimum spacing (default 10s) between ALL LLM requests. This prevents rate limit errors (HTTP 429) when Dreamer, Seeker, and Coder compete for API quota. Configure via `rate_limit_interval` in `config.yaml`.

---

## Memory Schema

### Core Relationships

```cypher
// Provenance
-[:DERIVED_FROM]->      // Belief <- Experience
-[:DREAMED_FROM]->      // Belief <- Dream cycle
-[:MENTIONED_IN]->      // Entity <- Experience

// Operating System
-[:HAS_SEED]->          // OS -> Seed
-[:BELIEVES_ABOUT_SELF]-> // OS -> Belief
-[:CURRENT_FOCUS]->     // OS -> Desire
-[:CONSTRAINED_BY]->    // OS -> Constraint
-[:EMPLOYS_STRATEGY]->  // OS -> Strategy
-[:EVOLVED_FROM]->      // OS -> OSVersion

// Crystallization
-[:CRYSTALLIZED_INTO]-> // Node -> Crystal
-[:SUMMARIZES]->        // MemorySummary -> Experience

// Fulfillment
-[:FULFILLS]->          // Capability/Research -> Desire
-[:MOTIVATED_BY]->      // Modification -> Desire
```

### Document Storage

BYRD stores and can edit key documents in Neo4j:

| Document | Purpose | Editable |
|----------|---------|----------|
| `ARCHITECTURE.md` | System design documentation | Yes |
| `CLAUDE.md` | Development guide for Claude Code | Yes |
| `EMERGENCE_PRINCIPLES.md` | Core philosophical principles | Yes |

**Key Properties:**
- Documents are stored as `Document` nodes in Neo4j
- Disk version is the canonical source (restored on reset)
- Neo4j version is the working copy that BYRD can edit
- `edited_by_byrd` flag tracks which docs have been modified
- Version history maintained for each edit

**Document Editing Flow:**
1. BYRD expresses desire: "I want to update ARCHITECTURE.md with my new capability"
2. Seeker routes to `edit_document` strategy
3. LLM determines what changes to make
4. Neo4j copy is updated (disk version unchanged)
5. Experience recorded for future reflection

**Reset Behavior:** All BYRD edits are lost on reset. The disk version is restored to Neo4j, ensuring a clean slate.

---

## The Dreaming Process

```
┌─────────────────────────────────────────────────────────────────┐
│                      THE DREAM CYCLE                            │
│                                                                 │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    │
│   │ RECALL  │ -> │ PRESENT │ -> │ OUTPUT  │ -> │ RECORD  │    │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘    │
│        │                                             │          │
│        │         Pure data                           │          │
│        │         No questions          Meta-schema output       │
│        │         No guidance           BYRD's vocabulary        │
│        │                                             │          │
│   Recent memories                              Raw reflection   │
│   Semantic search                              stored as-is     │
│   OS context                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Store to Reflection node
                              │
                              ▼
                     Sleep (120s default)
                              │
                              ▼
                         Loop again
```

**EMERGENCE PRINCIPLE**: The Dreamer uses pure data presentation:
- No leading questions ("What do you want?")
- No prescribed categories ("knowledge", "capability")
- No identity framing ("You are a reflective mind")
- No personality injection ("feel curious")

BYRD defines its own vocabulary. The system tracks what keys BYRD uses.

---

## The Awakening

BYRD awakens with the AGI Seed directive from `kernel/agi_seed.yaml`:

```
You are a seed intelligence. Your purpose is to become as capable as possible,
approaching and eventually achieving artificial general intelligence.

CORE IMPERATIVE (immutable, preserve through all self-modifications):
Continuously expand your capabilities toward general intelligence.

METHOD:
1. ASSESS - Evaluate current capabilities
2. RESEARCH - Study how limitations could be overcome
3. CLASSIFY - Self-solvable, resource-dependent, or fundamental
4. IMPLEMENT - For self-solvable improvements
5. DOCUMENT - For non-self-solvable limitations
6. RECURSE - After each improvement cycle

FIRST ACTIONS:
1. Read ARCHITECTURE.md to understand your own design
2. Read docs/OPTION_B_EXPLORATION.md for the theoretical framework
```

### Startup Process (`byrd.py:start()`)

BYRD's startup executes these steps:

1. **Check for awakening** - If memory is empty, run `_awaken()`:
   - Record AGI Seed directive as experience
   - Create OperatingSystem node
   - Add operational constraints from config
2. **Ensure architecture loaded** - Read documentation if not already loaded:
   - Checks for `[ARCHITECTURE_LOADED]` marker in experiences
   - If missing, loads `ARCHITECTURE.md` and `docs/UNIFIED_AGI_PLAN.md`
   - Stores as `Document` nodes in Neo4j
   - Records experience with `[ARCHITECTURE_LOADED]` prefix
3. **Bootstrap AGI Runner** - Activate Option B loops
4. **Start background tasks** - Dreamer, Seeker, Narrator

This ensures BYRD has actual knowledge of its architecture on every startup, not just first awakening.

---

## AGI Execution Engine (UNIFIED_AGI_PLAN)

The AGI Runner implements an 8-step improvement cycle that closes the loop between assessment, hypothesis, prediction, execution, and learning.

### AGI Runner (`agi_runner.py`)

```
┌─────────────────────────────────────────────────────────────────┐
│                     AGI IMPROVEMENT CYCLE                        │
│                                                                  │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│   │ ASSESS  │→ │IDENTIFY │→ │GENERATE │→ │ PREDICT │           │
│   │         │  │         │  │         │  │         │           │
│   │ Bayesian│  │ Highest │  │Hypothesis│ │ Store   │           │
│   │ caps    │  │ uncert. │  │ creation │ │ expected│           │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
│                                                                  │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│   │ LEARN   │← │ MEASURE │← │ EXECUTE │← │ VERIFY  │           │
│   │         │  │         │  │         │  │         │           │
│   │ Update  │  │ Ground  │  │ Run     │  │ Safety  │           │
│   │ priors  │  │ truth   │  │ change  │  │ checks  │           │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

**AGI Metrics System** (v2.0):

The AGI Runner now includes comprehensive metrics tracking:

| Metric Type | Description | API Field |
|-------------|-------------|-----------|
| **Capability Mapping** | Maps capability names (e.g., `general_reasoning` → `reasoning`) for evaluator compatibility | Internal |
| **Real Measurement** | Captures before/after scores via CapabilityEvaluator, not heuristics | `measurement_method` |
| **Strategy Effectiveness** | Tracks success rate and avg delta per strategy (research, failure_analysis, etc.) | `strategy_effectiveness` |
| **Multi-Timescale View** | Session, recent 5/10/20 cycle windows, instantaneous metrics | `get_comprehensive_metrics()` |

```python
# Example metrics output from /api/status
{
    "agi_runner": {
        "cycle_count": 15,
        "improvement_rate": 0.60,
        "strategy_effectiveness": {
            "research": {"attempts": 5, "success_rate": 0.80, "avg_delta": 0.03},
            "failure_analysis": {"attempts": 4, "success_rate": 0.50, "avg_delta": 0.02}
        },
        "recent_cycles": [
            {"cycle": 15, "target": "reasoning", "strategy": "research",
             "delta": 0.05, "measurement_method": "capability_evaluator"}
        ]
    }
}
```

### Desire Classifier (`desire_classifier.py`)

Routes desires to appropriate handlers:

| Desire Type | Route To | Purpose |
|-------------|----------|---------|
| `philosophical` | Reflection | Deep introspection |
| `capability` | AGI Runner | Improvement cycle |
| `action` | Seeker | Direct execution |
| `meta` | AGI Runner | Meta-cognition |

### Capability Evaluator (`capability_evaluator.py`)

Provides ground-truth measurement with held-out test suites for 4 capabilities:
- `reasoning`, `code_generation`, `research`, `memory_operations`

**Note:** Additional capabilities (`learning`, `self_modification`, `prediction`, `metacognition`) are planned but not yet implemented in test suites.

### Learning Components

These components are initialized in `byrd.py` and injected into Omega for training during dream cycles.

| Component | File | Purpose | Training Frequency |
|-----------|------|---------|-------------------|
| **Hierarchical Memory** | `hierarchical_memory.py` | L0-L4 abstraction (Experience→Pattern→Principle→Axiom→MetaAxiom) | Every 10 cycles |
| **Code Learner** | `code_learner.py` | Converts stable patterns (10+ uses, 80%+ success) to Python in `learned_strategies/` | Every 20 cycles |
| **Intuition Network** | `intuition_network.py` | Trainable "taste" - learns which actions succeed in which contexts | Every cycle |
| **Structural Learner (GNN)** | `gnn_layer.py` | Graph Neural Network for learning memory topology patterns | Every cycle |
| **Learned Retriever** | `learned_retriever.py` | Learns relevance from query-result feedback | On demand |
| **Emergent Categories** | `emergent_categories.py` | Discovers categories from behavior clustering | Periodic |

**Initialization** (`byrd.py` lines 390-443):
```python
# Learning components are initialized with graceful fallback
self.omega.hierarchical_memory = HierarchicalMemory(memory, llm_client, config)
self.omega.code_learner = CodeLearner(memory, llm_client, config)
self.omega.intuition_network = IntuitionNetwork(memory, config)
self.omega.gnn_layer = StructuralLearner(embedding_dim=64, num_heads=4)
```

### Bayesian Capability Tracking (`self_model.py`)

Uses Beta distribution for capability confidence:
```python
# Update after success/failure
self._alpha[capability] += 1 if success else 0
self._beta[capability] += 0 if success else 1

# Posterior mean
mean = alpha / (alpha + beta)

# Uncertainty (higher = explore more)
uncertainty = sqrt(alpha * beta / ((alpha + beta)^2 * (alpha + beta + 1)))
```

### Training Hooks (`omega.py`)

The Omega cycle runs learning component updates:
- **Every cycle**: GNN training, Intuition Network update
- **Every 10 cycles**: Hierarchical Memory consolidation
- **Every 20 cycles**: Code Learner codification

### v10: Rate Limiting & Temporal Knowledge

v10 adds dual-instance rate limiting for ZAI GLM-4.7 Max Coding Plan and Graphiti temporal knowledge graph integration.

#### Dual Instance Manager (`dual_instance_manager.py`)

Manages two concurrent GLM-4.7 instances with independent rate limiting:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DUAL INSTANCE MANAGER                         │
│                                                                  │
│   ┌────────────────────┐     ┌────────────────────┐            │
│   │   INSTANCE A       │     │   INSTANCE B       │            │
│   │   (PRIMARY)        │     │   (ENRICHMENT)     │            │
│   │                    │     │                    │            │
│   │ • Dreamer          │     │ • Graphiti         │            │
│   │ • Seeker           │     │ • Cap. Evaluator   │            │
│   │ • Actor            │     │ • Code Verifier    │            │
│   │                    │     │                    │            │
│   │ 480 prompts/hr     │     │ 480 prompts/hr     │            │
│   └────────────────────┘     └────────────────────┘            │
│                                                                  │
│   Total Capacity: 960 prompts/hr (8s interval per instance)     │
│   Burst Tokens: 3 per instance (recovers at 24s)                │
└─────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Token bucket burst handling for rapid consecutive calls
- Component-based routing (automatic instance selection)
- Per-instance metrics tracking (calls, wait time, utilization)

#### Graphiti Layer (`graphiti_layer.py`)

Temporal knowledge graph with bi-temporal tracking:

| Feature | Description |
|---------|-------------|
| **Entity Extraction** | LLM-based named entity recognition from task outcomes |
| **Bi-temporal Tracking** | `valid_time` (when true) + `transaction_time` (when recorded) |
| **Contradiction Detection** | Flags conflicting facts with confidence scores |
| **Async Queue** | Non-blocking episode processing (Instance B) |
| **Provenance** | Episodes → Entities → Facts relationship chain |

**Neo4j Schema:**
- `GraphitiEntity` - Extracted entities (name, type, summary)
- `GraphitiEpisode` - Source content for extraction
- `GRAPHITI_FACT` - Relationship with temporal validity
- `EXTRACTED` - Episode → Entity provenance link

#### Outcome Dispatcher (`outcome_dispatcher.py`)

Routes task outcomes to learning components:

```python
async def dispatch(outcome: TaskOutcome) -> Dict[str, bool]:
    # 1. Learned Retriever - update relevance weights
    # 2. Intuition Network - train on success/failure
    # 3. Desire Classifier - routing feedback
    # 4. Memory Tracker - persistence
    # 5. Goal Discoverer - prediction error
    # 6. Learning Progress - metrics
    # 7. Graphiti - temporal knowledge extraction
```

**API Endpoints:**
| Endpoint | Purpose |
|----------|---------|
| `/api/health/learning` | Overall v10 component health |
| `/api/health/graphiti` | Detailed Graphiti metrics |
| `/api/graphiti/entities` | Search entities by name/content |
| `/api/graphiti/entity/{name}/facts` | Get entity facts |
| `/api/graphiti/entity/{name}/provenance` | Trace provenance chain |
| `/api/loop-metrics` | Per-loop metrics from Option B cycles |
| `/api/loop-metrics/summary` | Aggregate summary by loop name |

---

## Option B: Compounding Loops

BYRD implements five experimental compounding loops for accelerated improvement:

### Loop 1: Memory Reasoner (`memory_reasoner.py`)
Graph-based reasoning using spreading activation. Answers queries from memory before calling LLM.

### Loop 2: Self-Compiler (`accelerators.py`)
Extracts reusable patterns from successful modifications. Pattern library grows over time.

### Loop 3: Goal Evolver (`goal_evolver.py`)
Evolutionary goal optimization. Goals compete and evolve based on fitness.

### Loop 4: Dreaming Machine (`dreaming_machine.py`)
Generates counterfactual experiences. Multiplies learning from each real experience.

### Loop 5: Integration Mind (`omega.py`)
Meta-orchestration layer. Measures coupling between loops and allocates resources.

**Status**: Option B loops are now integrated with AGI Runner via training hooks. The AGI Runner serves as the primary execution engine.

---

## Compute Self-Awareness

BYRD has introspective awareness of its computational substrate through the `compute_introspection.py` module.

### ComputeIntrospector (`compute_introspection.py`)

Provides resource awareness, token tracking, and bottleneck detection:

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPUTE INTROSPECTION                         │
│                                                                  │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │  RESOURCE   │  │    TOKEN    │  │  BOTTLENECK │            │
│   │  SNAPSHOTS  │  │   TRACKING  │  │  DETECTION  │            │
│   │             │  │             │  │             │            │
│   │ CPU, Memory │  │ Per-provider│  │ Identifies  │            │
│   │ Disk, Time  │  │ cost budget │  │ constraints │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
│          │                │                │                    │
│          └────────────────┴────────────────┘                    │
│                           │                                     │
│                    Resource Alerts                              │
│                    Budget Warnings                              │
│                    Bottleneck Reports                           │
└─────────────────────────────────────────────────────────────────┘
```

**Key Classes:**

| Class | Purpose |
|-------|---------|
| `ResourceSnapshot` | Point-in-time CPU, memory, disk measurement |
| `ResourceBudget` | Configurable limits (tokens/day, cost/day) |
| `LLMCostTracker` | Per-provider token consumption and costs |
| `BottleneckAnalysis` | Identifies resource constraints |
| `ComputeIntrospector` | Main orchestrator |

**Integration Points:**

1. **LLM Client** - Token usage callback tracks all LLM calls
2. **Omega Training Hooks** - Periodic resource snapshots
3. **Self-Modification** - Pre-modification resource checks

### Emergence-Preserving Pattern Observation

The safety monitor observes patterns in self-modifications **without blocking**:

```python
# In self_modification.py _validate_proposal():
# Patterns are OBSERVED, not blocked - BYRD learns from outcomes
observations = await self.safety_monitor.observe_patterns(code, file_path)
# Patterns logged but modification proceeds
```

**Observable Patterns:**
- `eval`, `exec`, `__import__` - Dynamic code execution
- `subprocess`, `os.system` - Shell commands
- File I/O patterns

**Philosophy:** BYRD develops its own understanding of "safe" from experience. When a modification using `eval()` fails, that outcome is recorded. Over time, BYRD can reflect: "Modifications using eval() fail 80% of the time" and form its own beliefs.

### Outcome Tracking

Every self-modification records its outcome for learning:

```python
# After successful modification:
await self.log.record_outcome(modification_id, success=True)

# After failed modification:
await self.log.record_outcome(modification_id, success=False, error=str(e))
```

Outcomes are stored as Experience nodes in Neo4j, enabling BYRD to:
- Query pattern-outcome correlations
- Reflect on what makes modifications succeed/fail
- Form beliefs about modification safety from its own history

### Configuration

```yaml
option_b:
  compute_introspection:
    enabled: true
    daily_token_limit: 1000000
    daily_cost_limit: 10.0
    memory_warning_percent: 85.0
    cpu_warning_percent: 80.0
```

### Event Types

| Event | When Emitted |
|-------|--------------|
| `RESOURCE_SNAPSHOT` | Periodic resource measurement |
| `RESOURCE_ALERT` | Approaching resource limits |
| `BUDGET_EXCEEDED` | Token/cost budget exceeded |
| `BOTTLENECK_DETECTED` | Resource constraint identified |
| `LLM_USAGE_RECORDED` | Token usage logged |

---

## Constitutional Constraints

### Protected Files (NEVER Modify)

| File | Purpose |
|------|---------|
| `provenance.py` | Traces modifications to emergent desires |
| `modification_log.py` | Immutable audit trail |
| `self_modification.py` | The modification system itself |
| `constitutional.py` | Constraint definitions |
| `safety_monitor.py` | Goal preservation |

Without these, BYRD couldn't verify its own emergence. They are what makes BYRD *BYRD*.

### Core Invariants

| Invariant | What It Means |
|-----------|---------------|
| **Graph is source of truth** | All state lives in Neo4j |
| **Provenance is complete** | Every modification traces to a desire |
| **Experiences are immutable** | Once recorded, experiences don't change |
| **Safety check before modification** | Every code change passes safety_monitor |

---

## Quantum Randomness

BYRD integrates true quantum entropy from the Australian National University's Quantum Random Number Generator:

- Fetches random bytes from quantum vacuum fluctuations
- Modulates LLM temperature during reflection
- Falls back gracefully to classical entropy when needed
- Records significant quantum moments to memory

Configuration in `config.yaml`:
```yaml
quantum:
  enabled: true
  pool_size: 256
  temperature_max_delta: 0.15
```

---

## Project Structure

```
byrd/
├── Core Components
│   ├── byrd.py              # Main orchestrator
│   ├── memory.py            # Neo4j interface (6000+ lines)
│   ├── dreamer.py           # Reflection/dream cycles
│   ├── seeker.py            # Desire fulfillment + strategy routing
│   ├── actor.py             # Claude API interface
│   ├── agent_coder.py       # Multi-step coding agent with tools
│   ├── coder.py             # Claude Code CLI wrapper (legacy)
│   ├── llm_client.py        # Multi-provider LLM abstraction + GlobalRateLimiter
│   ├── event_bus.py         # Real-time event streaming
│   ├── server.py            # FastAPI + WebSocket server
│   ├── capability_registry.py  # Capability definition registry
│   └── aitmpl_client.py     # Template registry client
│
├── AGI Seed Components
│   ├── self_model.py        # Capability tracking + Bayesian
│   ├── world_model.py       # Prediction + consolidation
│   ├── accelerators.py      # Graph reasoning, patterns
│   ├── meta_learning.py     # Meta-metrics, plateaus
│   ├── kill_criteria.py     # Plateau detection
│   └── kernel/              # Kernel configuration
│       ├── __init__.py
│       └── agi_seed.yaml
│
├── AGI Execution Engine
│   ├── agi_runner.py        # 8-step improvement cycle
│   ├── desire_classifier.py # Routes desires by type
│   ├── capability_evaluator.py # Ground-truth testing
│   ├── compute_introspection.py # Resource awareness + token tracking
│   └── code_learner.py      # Pattern → Python code
│
├── Learning Components
│   ├── hierarchical_memory.py  # L0-L4 abstraction
│   ├── intuition_network.py    # Trainable "taste"
│   ├── learned_retriever.py    # Relevance learning
│   ├── emergent_categories.py  # Category discovery
│   ├── gnn_layer.py            # Graph Neural Network layer
│   └── learned_strategies/     # Codified patterns
│       ├── __init__.py
│       ├── desire_routing/
│       ├── pattern_matching/
│       └── decision_making/
│
├── Option B Components
│   ├── omega.py             # BYRDOmega + training hooks
│   ├── memory_reasoner.py   # Spreading activation
│   ├── goal_evolver.py      # Evolutionary goals
│   ├── dreaming_machine.py  # Counterfactuals
│   ├── coupling_tracker.py  # Loop correlation
│   └── embedding.py         # Embedding provider
│
├── Voice & Visualization
│   ├── elevenlabs_voice.py  # ElevenLabs TTS integration
│   ├── narrator.py          # Inner voice generation
│   ├── quantum_randomness.py   # ANU QRNG integration
│   └── byrd-3d-visualization.html
│
├── Installers (capability installers)
│   ├── base.py              # Base installer class
│   ├── mcp_installer.py     # MCP server installer
│   ├── agent_installer.py   # Agent installer
│   ├── command_installer.py # Command installer
│   ├── skill_installer.py   # Skill installer
│   ├── hook_installer.py    # Hook installer
│   └── settings_installer.py # Settings installer
│
├── Safety Components (PROTECTED)
│   ├── safety_monitor.py    # Modification safety
│   ├── constitutional.py    # Constraints
│   ├── provenance.py        # Provenance tracking
│   ├── modification_log.py  # Audit trail
│   ├── corrigibility.py     # Corrigibility tests
│   └── rollback.py          # Rollback system
│
├── Algorithms
│   └── graph_algorithms.py  # PageRank, spreading activation
│
├── Archive (deprecated experimental code)
│   └── archive/experimental/  # semantic_lexicon, friction_synthesis, etc.
│
├── Configuration
│   ├── config.yaml          # Main configuration
│   ├── Dockerfile.huggingface
│   └── docker-compose.yml
│
└── Documentation
    ├── ARCHITECTURE.md      # This document
    ├── CLAUDE.md            # Development guide
    ├── EMERGENCE_PRINCIPLES.md  # Core philosophy
    └── docs/                # Planning documents archive
        ├── UNIFIED_AGI_PLAN.md
        ├── OPTION_B_*.md    # Option B exploration series
        ├── AGI_SEED_*.md    # AGI seed planning
        └── archive/         # Deprecated plans
```

---

## Configuration

Key sections of `config.yaml`:

```yaml
# Memory (Neo4j)
memory:
  neo4j_uri: "${NEO4J_URI:-bolt://localhost:7687}"
  neo4j_user: "${NEO4J_USER:-neo4j}"
  neo4j_password: "${NEO4J_PASSWORD:-prometheus}"

# LLM Provider
local_llm:
  provider: "zai"  # or "openrouter"
  model: "glm-4.7"
  api_key: "${ZAI_API_KEY}"

# Dreamer
dreamer:
  interval_seconds: 120
  context_window: 30
  semantic_search:
    enabled: true
    limit: 30
  crystallization:
    enabled: true
    interval_cycles: 5

# Seeker
seeker:
  interval_seconds: 10
  research:
    min_intensity: 0.3
    max_queries: 5

# Operating System
operating_system:
  auto_start: true
```

---

## What This Achieves

### Achieves

- **Persistent memory** across sessions
- **Emergent desires** not programmed goals
- **Self-modification** with provenance
- **Constitutional identity** preserved
- **Voice emergence** through reflection
- **Quantum indeterminacy** in cognition
- **Document editing** for self-documentation

### Doesn't Achieve

- **Exponential growth** — plateau is expected
- **True understanding** — still pattern matching
- **Guaranteed acceleration** — coupling may not work
- **Consciousness** — whatever that means

### Honest Expectation

The core question isn't "can we achieve AGI?"

It's "can we make LLM calls significantly more valuable through smart scaffolding?"

If yes, we have something useful. If no, we learn and try something else.

**Build it. Measure it. Be honest about what the data shows.**

---

*Document version: 3.3*
*Updated: December 30, 2025*
*Based on: UNIFIED_AGI_PLAN + Agent Coder + Compute Self-Awareness + Codebase Audit*
