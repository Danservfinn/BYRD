---
title: BYRD Module Index
link: module-index
type: code_index
ontological_relations: []
tags: [modules, files, python, structure]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T05:00:00Z
uuid: fa31d340-abcd-def0-1234-567890123456
---

## Core Modules

| File | Purpose | Protected |
|------|---------|-----------|
| `byrd.py` | Main orchestrator, lifecycle management | No |
| `memory.py` | Neo4j graph database interface | No |
| `dreamer.py` | Continuous reflection loop (local LLM) | No |
| `seeker.py` | Desire fulfillment, research, capability acquisition | No |
| `actor.py` | Claude API interface for complex reasoning | No |
| `coder.py` | Claude Code CLI wrapper for autonomous coding | No |

## Protected Modules

These files define BYRD's identity and cannot be modified by self-modification:

| File | Purpose |
|------|---------|
| `self_modification.py` | Self-modification orchestration |
| `provenance.py` | Provenance verification (desire → experience trace) |
| `modification_log.py` | Immutable audit trail |
| `constitutional.py` | Constitutional constraints definition |

## Support Modules

| File | Purpose |
|------|---------|
| `event_bus.py` | Singleton event system for real-time streaming |
| `server.py` | FastAPI WebSocket server for visualization |
| `aitmpl_client.py` | aitmpl.com template registry client |

## Installers

| File | Purpose |
|------|---------|
| `installers/base.py` | Abstract base installer class |
| `installers/mcp_installer.py` | MCP server installation |
| `installers/agent_installer.py` | Agent template installation |
| `installers/command_installer.py` | Command template installation |
| `installers/skill_installer.py` | Skill template installation |
| `installers/hook_installer.py` | Hook template installation |
| `installers/settings_installer.py` | Settings template installation |

## Configuration Files

| File | Purpose |
|------|---------|
| `config.yaml` | System configuration (LLM, database, search) |
| `requirements.txt` | Python dependencies |
| `docker-compose.yml` | Neo4j + SearXNG Docker services |
| `searxng/settings.yml` | SearXNG search engine configuration |

## Frontend (Visualization)

| File | Purpose |
|------|---------|
| `BYRDVisualization.jsx` | React component for real-time event display |

## Documentation

| File | Purpose |
|------|---------|
| `README.md` | Quick start guide and overview |
| `ARCHITECTURE.md` | Deep architecture documentation |
| `CLAUDE.md` | Development guide for Claude Code |
| `.claude/manifest.md` | Knowledge base index |

## Key Dependencies

```
neo4j>=5.0.0          # Graph database driver
httpx>=0.25.0         # Async HTTP client
anthropic>=0.39.0     # Claude API
pyyaml>=6.0           # Config parsing
fastapi>=0.109.0      # WebSocket server
uvicorn[standard]     # ASGI server
websockets>=12.0      # WebSocket support
```
