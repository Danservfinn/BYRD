---
title: BYRD Module Index
link: module-index
type: code_index
ontological_relations: []
tags: [modules, files, python, structure]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T02:10:00Z
uuid: fa31d340-abcd-def0-1234-567890123456
---

## Core Modules

| File | Purpose | Protected |
|------|---------|-----------|
| `byrd.py` | Main orchestrator | No |
| `memory.py` | Neo4j interface | No |
| `dreamer.py` | Reflection loop | No |
| `seeker.py` | Desire fulfillment | No |
| `actor.py` | Claude API interface | No |

## Protected Modules

| File | Purpose |
|------|---------|
| `self_modification.py` | Self-modification system |
| `provenance.py` | Provenance verification |
| `modification_log.py` | Immutable audit trail |
| `constitutional.py` | Constitutional constraints |

## Support Modules

| File | Purpose |
|------|---------|
| `event_bus.py` | Real-time event emission |

## Configuration Files

| File | Purpose |
|------|---------|
| `config.yaml` | System configuration |
| `requirements.txt` | Python dependencies |
| `docker-compose.yml` | Neo4j + SearXNG services |
| `settings.yml` | SearXNG configuration |

## Frontend (Visualization)

| File | Purpose |
|------|---------|
| `frontend/MemoryGraph.tsx` | React graph visualization |
| `visualization.html` | Standalone HTML viewer |

## Key Dependencies

```
neo4j>=5.0.0
httpx>=0.25.0
anthropic>=0.39.0
pyyaml>=6.0
```
