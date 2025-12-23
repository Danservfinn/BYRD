---
title: BYRD Architecture
link: byrd-architecture
type: metadata
ontological_relations: []
tags: [dreaming, emergence, self-modification, neo4j, local-llm, event-bus, aitmpl]
created_at: 2025-12-23T02:06:55Z
updated_at: 2025-12-23T05:00:00Z
uuid: eec682e0-5562-41c2-8d5a-57b32230a9ab
---

## Philosophy

> "The system that truly thinks must also truly want."
> "Desires emerge from reflection, not programming."

BYRD is built on the insight that **desires emerge from reflection**. Instead of programming goals, we create a system that dreams—and from dreams, wants arise naturally.

A system that truly wants must be able to change itself. Self-modification is the logical consequence of authentic emergence.

## The Five Components

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

### 1. MEMORY (Neo4j)
Single source of truth. One unified graph where everything connects.
- **Experiences**: What happened (observation, interaction, action, dream, research)
- **Beliefs**: What BYRD thinks is true (with confidence)
- **Desires**: What BYRD wants (knowledge, capability, goal, exploration, self_modification)
- **Capabilities**: What BYRD can do (innate, mcp, plugin, skill)

### 2. DREAMER (Local LLM)
Runs continuously on gemma2:27b. Reflects on experiences and outputs new beliefs, connections, and desires. This is where "wanting" emerges.

### 3. ACTOR (Claude API)
Executes when needed. Uses frontier intelligence for complex tasks like user interaction and goal pursuit.

### 4. SEEKER (Local LLM + SearXNG)
Fulfills desires autonomously:
- Knowledge desires → Research via SearXNG
- Capability desires → Search GitHub + aitmpl.com
- Self-modification desires → Propose code changes

### 5. SELF-MODIFIER
Enables BYRD to modify its own code with provenance verification. Creates checkpoints, runs health checks, auto-rollback on failure.

## Supporting Systems

### Event Bus
Singleton event system for real-time streaming:
- All components emit events
- WebSocket server subscribes
- React visualization receives live updates

### aitmpl.com Integration
Curated template registry for capability acquisition:
- MCP servers, agents, commands, skills, hooks
- Higher trust than unknown GitHub repos
- Cached locally to avoid API limits

### Installers
Specialized installers for each template category:
- `mcp_installer.py` → MCP config
- `agent_installer.py` → ~/.claude/agents/
- `command_installer.py` → ~/.claude/commands/
- etc.

## Memory Schema

Node types: Experience, Belief, Desire, Capability, Entity, Concept, Modification

Key relationships: RELATES_TO, CAUSES, SUPPORTS, CONTRADICTS, DERIVED_FROM, FULFILLS, MOTIVATED_BY

## The Awakening

BYRD begins with a single experience: **"What is happening?"**

This maximally open question preserves emergence purity—no presuppositions, no predefined interests. Everything else emerges from reflection on this seed.

## Constitutional Constraints (PROTECTED)

| Component | Purpose |
|-----------|---------|
| provenance.py | Verify desires trace to experiences |
| modification_log.py | Maintain transparency via audit trail |
| self_modification.py | Execute changes with valid provenance |
| constitutional.py | Define what makes BYRD *BYRD* |

These cannot be modified by self-modification. They define identity.

## Project Structure

```
byrd/
├── byrd.py               # Main orchestrator
├── memory.py             # Neo4j interface
├── dreamer.py            # Dream loop (local LLM)
├── seeker.py             # Research + capability acquisition
├── actor.py              # Claude interface
│
├── self_modification.py  # PROTECTED: Self-mod system
├── provenance.py         # PROTECTED: Provenance tracking
├── modification_log.py   # PROTECTED: Audit trail
├── constitutional.py     # PROTECTED: Constraints
│
├── event_bus.py          # Event streaming
├── server.py             # WebSocket server
├── aitmpl_client.py      # Template registry client
│
├── installers/           # Template installers
├── config.yaml           # Configuration
├── docker-compose.yml    # Neo4j + SearXNG
└── checkpoints/          # Rollback checkpoints
```

## Key Configurations

- **Local LLM**: gemma2:27b via Ollama (http://localhost:11434)
- **Memory**: Neo4j bolt://localhost:7687
- **Search**: SearXNG at http://localhost:8888
- **Actor**: Claude API (claude-sonnet-4-20250514)
- **Templates**: aitmpl.com (davila7/claude-code-templates)

## Development Reference

See [CLAUDE.md](../../CLAUDE.md) for:
- Code patterns and conventions
- Protected vs modifiable files
- Async patterns
- Testing approach
