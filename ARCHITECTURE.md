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
- Voice design requests (`voice_design`)
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
| `introspection` | analyze myself, understand my code | Internal reflection |
| `source_introspect` | read my code, examine my files | Source code analysis |
| `reconcile_orphans` | orphan, integrate, unify | Connect orphaned nodes |
| `curate` | optimize, clean, consolidate | Graph optimization |
| `crystallize` | crystallize, form crystal | Create unified concepts |
| `self_modify` | modify my code, extend myself | Self-modification |
| `edit_document` | edit document, update architecture | Edit docs in memory |
| `code` | code, write, implement | Generate code |
| `research` | (default) | Web research via DuckDuckGo |

### 6. Actor (Claude API)

Executes when there's something complex to do:
- User interaction via chat
- Complex reasoning tasks
- Goal pursuit requiring frontier intelligence

### 7. Coder (Claude Code CLI)

BYRD's autonomous coding agent:
- Executes code generation via Claude Code CLI
- Post-validates against constitutional constraints
- Tracks costs and usage limits
- Automatic rollback if protected files are touched

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

**Status**: These components exist but are experimental. The primary flow uses `byrd.py` as orchestrator.

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
│   ├── coder.py             # Claude Code CLI wrapper
│   ├── agent_coder.py       # Agent-based coding
│   ├── llm_client.py        # Multi-provider LLM abstraction
│   ├── event_bus.py         # Real-time event streaming
│   └── server.py            # FastAPI + WebSocket server
│
├── AGI Seed Components
│   ├── self_model.py        # Capability tracking
│   ├── world_model.py       # Prediction system
│   ├── accelerators.py      # Graph reasoning, patterns
│   ├── meta_learning.py     # Meta-metrics, plateaus
│   ├── kill_criteria.py     # Plateau detection
│   └── kernel/              # Kernel configuration
│       ├── __init__.py
│       └── agi_seed.yaml
│
├── Option B Components
│   ├── omega.py             # BYRDOmega wrapper
│   ├── memory_reasoner.py   # Spreading activation
│   ├── goal_evolver.py      # Evolutionary goals
│   ├── dreaming_machine.py  # Counterfactuals
│   ├── coupling_tracker.py  # Loop correlation
│   └── embedding.py         # Embedding provider
│
├── Voice & Visualization
│   ├── elevenlabs_voice.py  # ElevenLabs TTS integration
│   ├── narrator.py          # Inner voice generation
│   └── byrd-3d-visualization.html
│
├── Safety Components (PROTECTED)
│   ├── safety_monitor.py    # Modification safety
│   ├── constitutional.py    # Constraints
│   ├── provenance.py        # Provenance tracking
│   ├── modification_log.py  # Audit trail
│   ├── corrigibility.py     # Corrigibility tests
│   └── rollback.py          # Rollback system
│
├── Experimental
│   ├── semantic_lexicon.py  # Semantic type system
│   ├── friction_synthesis.py # Friction-based learning
│   ├── phase_transition.py  # Phase transition detection
│   ├── gnn_layer.py         # Graph neural network layer
│   └── graph_algorithms.py  # PageRank, spreading activation
│
├── Configuration
│   ├── config.yaml          # Main configuration
│   ├── Dockerfile.huggingface
│   └── docker-compose.yml
│
└── Documentation
    ├── ARCHITECTURE.md      # This document
    ├── CLAUDE.md            # Development guide
    └── docs/
        └── OPTION_B_EXPLORATION.md
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
  provider: "zai"  # or "ollama", "openrouter"
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

*Document version: 2.0*
*Updated: December 28, 2024*
*Based on: Codebase audit of actual implementation*
