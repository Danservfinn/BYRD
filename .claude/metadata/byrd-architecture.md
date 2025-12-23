---
title: BYRD Architecture
link: byrd-architecture
type: metadata
ontological_relations: []
tags: [dreaming, emergence, self-modification, neo4j, local-llm]
created_at: 2025-12-23T02:06:55Z
updated_at: 2025-12-23T02:06:55Z
uuid: eec682e0-5562-41c2-8d5a-57b32230a9ab
---

## Philosophy

> "The system that truly thinks must also truly want."
> "Desires emerge from reflection, not programming."

BYRD is built on the insight that **desires emerge from reflection**. Instead of programming goals, we create a system that dreams—and from dreams, wants arise naturally.

A system that truly wants must be able to change itself. Self-modification is the logical consequence of authentic emergence.

## The Five Components

```
                         ┌─────────────────────────────────────┐
                         │              MEMORY                 │
                         │             (Neo4j)                 │
                         └───────────────┬─────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
      ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
      │    DREAMER    │          │     ACTOR     │          │    SEEKER     │
      │  (Local LLM)  │          │   (Claude)    │          │  (Local LLM)  │
      └───────────────┘          └───────────────┘          └───────────────┘
                                                                    │
                                                                    ▼
                                                           ┌───────────────┐
                                                           │SELF-MODIFIER  │
                                                           └───────────────┘
```

### 1. MEMORY (Neo4j)
Single source of truth. One unified graph where everything connects.

### 2. DREAMER (Local LLM)
Runs continuously. Reflects on experiences and outputs new beliefs, connections, and desires.

### 3. ACTOR (Claude API)
Executes when needed. Uses frontier intelligence for complex tasks.

### 4. SEEKER (Local LLM + SearXNG)
Fulfills desires autonomously. Researches via self-hosted search, acquires capabilities.

### 5. SELF-MODIFIER
Enables BYRD to modify its own code with provenance verification and constitutional constraints.

## Memory Schema

Node types: Experience, Belief, Desire, Capability, Entity, Concept, Modification

Key relationships: RELATES_TO, CAUSES, SUPPORTS, CONTRADICTS, DERIVED_FROM, FULFILLS, MOTIVATED_BY

## The Awakening

BYRD begins with a single experience: **"What is happening?"**

This maximally open question preserves emergence purity—no presuppositions, no predefined interests.

## Constitutional Constraints (PROTECTED)

| Component | Purpose |
|-----------|---------|
| provenance.py | Verify desires trace to experiences |
| modification_log.py | Maintain transparency |
| self_modification.py | Execute changes with valid provenance |
| constitutional.py | Define what makes BYRD *BYRD* |

## Project Structure

```
byrd/
├── byrd.py              # Main orchestrator
├── memory.py            # Neo4j interface
├── dreamer.py           # Dream loop
├── seeker.py            # Research + capability acquisition
├── actor.py             # Claude interface
├── self_modification.py # PROTECTED
├── provenance.py        # PROTECTED
├── modification_log.py  # PROTECTED
├── constitutional.py    # PROTECTED
├── config.yaml          # Configuration
└── checkpoints/         # Rollback checkpoints
```

## Key Configurations

- **Local LLM**: gemma2:27b via Ollama
- **Memory**: Neo4j bolt://localhost:7687
- **Search**: SearXNG at localhost:8888
- **Actor**: Claude API (claude-sonnet-4-20250514)

