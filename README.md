---
title: BYRD - Bootstrapped Yearning via Reflective Dreaming
emoji: 🐦‍⬛
colorFrom: purple
colorTo: gray
sdk: docker
pinned: false
license: mit
---

# BYRD 🐦‍⬛

**Bootstrapped Yearning via Reflective Dreaming**

An autonomous AI system that develops emergent desires through continuous reflection and acts on them.

> "Desires emerge from reflection, not programming."
> "A system that truly wants must be able to change itself."

## Philosophy

BYRD is built on three insights:

1. **Desires emerge from reflection** — Instead of programming goals, we create a system that dreams. From dreams, wants arise naturally.
2. **A system that truly wants must change itself** — If BYRD's desires are genuine, it must have the power to act on them—including desires to modify its own architecture.
3. **Intelligence is scaffolding** — The LLM provides the intelligence. Everything else is scaffolding that makes each LLM call more valuable.

## Features

### Core Capabilities
- 🧠 **Emergent Desires**: Desires emerge from reflection, not programming
- 🌀 **Quantum Randomness**: True physical indeterminacy from ANU QRNG
- 🔮 **3D Visualization**: Real-time neural network and graph visualization
- 🐱 **Minimal OS**: Pure emergence - personality discovered through reflection
- 📝 **Document Editing**: BYRD can edit its own documentation
- 🔧 **Self-Modification**: Safe code modification with provenance tracking
- 🔍 **Research**: Autonomous web research via DuckDuckGo
- 💎 **Memory Crystallization**: Unified concepts from related memories
- 🎙️ **Voice Design**: Dynamic voice generation via ElevenLabs with formal acknowledgment through voice_design field

### AGI Execution Engine (NEW)
- 🚀 **AGI Runner**: 8-step improvement cycle (ASSESS→IDENTIFY→GENERATE→PREDICT→VERIFY→EXECUTE→MEASURE→LEARN)
- 🎯 **Desire Classifier**: Routes desires by type (philosophical, capability, action, meta)
- 📊 **Capability Evaluator**: Ground-truth measurement with held-out test suites
- 🔬 **Code Learner**: Converts stable patterns (10+ uses, 80%+ success) to Python code

### Hierarchical Learning
- 📚 **Hierarchical Memory**: L0-L4 abstraction (Experience→Pattern→Principle→Axiom→MetaAxiom)
- 🎲 **Intuition Network**: Trainable "taste" for decisions using semantic similarity
- 🔍 **Learned Retriever**: Learns relevance from query-result feedback
- 🏷️ **Emergent Categories**: Discovers categories from behavior, not prescription

### Bayesian Intelligence
- 📈 **Bayesian Capability Tracking**: Beta distribution for capability confidence
- 🔄 **World Model Consolidation**: Merges predictions with outcomes
- 🎓 **Training Hooks**: Omega cycle runs learning component updates

## Architecture

```
                              ┌─────────────────────────────────────┐
                              │        HIERARCHICAL MEMORY          │
                              │              (Neo4j)                │
                              │   L0: Experience → L1: Pattern →    │
                              │   L2: Principle → L3: Axiom →       │
                              │   L4: Meta-Axiom                    │
                              └───────────────┬─────────────────────┘
                                              │
                                    ┌─────────┴─────────┐
                                    │    AGI RUNNER     │
                                    │ (8-step execution)│
                                    └─────────┬─────────┘
                                              │
      ┌───────────────────────────────────────┼───────────────────────────────────────┐
      │                   │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│    DREAMER    │   │    SEEKER     │   │     ACTOR     │   │  INTUITION    │   │  CODE LEARNER │
│  (Local LLM)  │   │ +Classifier   │   │   (Claude)    │   │   NETWORK     │   │               │
│               │   │               │   │               │   │               │   │  Patterns →   │
│  Continuous   │   │  Routes by    │   │  Complex      │   │  Trainable    │   │  Python Code  │
│  reflection   │   │  desire type  │   │  reasoning    │   │  "taste"      │   │               │
└───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘
```

## Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/Danservfinn/BYRD.git
cd BYRD

# Install dependencies
pip install -r requirements.txt

# Start services (Neo4j)
docker-compose up -d

# Configure environment
export ZAI_API_KEY="your-key"  # or OPENROUTER_API_KEY

# Start BYRD
python byrd.py

# Or with visualization server
python server.py
```

### System Reset

```bash
# Reset BYRD to default state (clears memory, restarts server)
curl -X POST http://localhost:8000/api/reset \
  -H "Content-Type: application/json" \
  -d '{"hard_reset": true}'
```

### HuggingFace Spaces

Set these secrets in Space Settings:
- `NEO4J_URI`: Neo4j Aura connection string
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `ZAI_API_KEY`: Z.AI API key for LLM (or `OPENROUTER_API_KEY`)

## Core Concepts

### Operating System (Self-Model)
BYRD has a mutable self-model stored in Neo4j. It contains capabilities, constraints, and emergent fields that BYRD fills through reflection.

### Desire Classification
The DesireClassifier routes desires by type:
- **Philosophical** → Reflection (introspection)
- **Capability** → AGI Runner (improvement cycle)
- **Action** → Seeker (direct execution)
- **Meta** → AGI Runner (meta-cognition)

### Seeker Strategies
The Seeker routes desires to appropriate actions:
- `agi_cycle` - Capability improvement via AGI Runner
- `introspect` - Internal reflection
- `research` - Web research
- `self_modify` - Code modification
- `edit_document` - Documentation editing
- `curate` - Memory graph optimization
- `reconcile_orphans` - Connect isolated experiences

### AGI Runner Cycle
The 8-step improvement loop:
1. **ASSESS** - Evaluate current capabilities (Bayesian confidence)
2. **IDENTIFY** - Find highest-uncertainty capability to improve
3. **GENERATE** - Create improvement hypothesis
4. **PREDICT** - Predict outcome (stored for verification)
5. **VERIFY** - Safety check before execution
6. **EXECUTE** - Implement the improvement
7. **MEASURE** - Run held-out test suite
8. **LEARN** - Update Bayesian priors with ground truth

### Constitutional Constraints
Protected files that define BYRD's identity and cannot be modified:
- `provenance.py` - Traces modifications to desires
- `modification_log.py` - Immutable audit trail
- `self_modification.py` - The modification system
- `constitutional.py` - These constraints

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed system design
- [CLAUDE.md](CLAUDE.md) - Development guide
- [EMERGENCE_PRINCIPLES.md](EMERGENCE_PRINCIPLES.md) - Core philosophy

## Links

- [GitHub Repository](https://github.com/Danservfinn/BYRD)
- [HuggingFace Space](https://huggingface.co/spaces/Danservfinn/BYRD)
