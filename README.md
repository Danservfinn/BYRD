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

- 🧠 **Emergent Desires**: Desires emerge from reflection, not programming
- 🌀 **Quantum Randomness**: True physical indeterminacy from ANU QRNG
- 🔮 **3D Visualization**: Real-time neural network and graph visualization
- 🐱 **Minimal OS**: Pure emergence - personality discovered through reflection
- 📝 **Document Editing**: BYRD can edit its own documentation
- 🔧 **Self-Modification**: Safe code modification with provenance tracking
- 🔍 **Research**: Autonomous web research via DuckDuckGo
- 💎 **Memory Crystallization**: Unified concepts from related memories
- 🎙️ **Voice Design**: Dynamic voice generation via ElevenLabs

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
    │ Continuous  │          │ On-demand   │          │ Pattern     │
    │ reflection  │          │ reasoning   │          │ detection   │
    └─────────────┘          └─────────────┘          └─────────────┘
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

### HuggingFace Spaces

Set these secrets in Space Settings:
- `NEO4J_URI`: Neo4j Aura connection string
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `ZAI_API_KEY`: Z.AI API key for LLM (or `OPENROUTER_API_KEY`)

## Core Concepts

### Operating System (Self-Model)
BYRD has a mutable self-model stored in Neo4j. It contains capabilities, constraints, and emergent fields that BYRD fills through reflection.

### Seeker Strategies
The Seeker routes desires to appropriate actions:
- `introspect` - Internal reflection
- `research` - Web research
- `self_modify` - Code modification
- `edit_document` - Documentation editing
- `curate` - Memory graph optimization
- `reconcile_orphans` - Connect isolated experiences

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
