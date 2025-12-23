---
title: BYRD Quick Commands
link: quick-commands
type: cheatsheets
ontological_relations: []
tags: [commands, cli, docker, ollama, startup]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T02:10:00Z
uuid: f8190b12-89ab-bcde-f012-345678901234
---

## Startup

```bash
# Start services
docker-compose up -d

# Start Ollama
ollama pull gemma2:27b
ollama serve

# Activate venv
source venv/bin/activate

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run BYRD
python byrd.py          # Default: continuous dreaming
python byrd.py --chat   # Interactive mode
python byrd.py --status # Show status and exit
```

## Service URLs
| Service | URL |
|---------|-----|
| Neo4j Browser | http://localhost:7474 |
| SearXNG | http://localhost:8888 |
| Ollama | http://localhost:11434 |

## Debugging

```python
# Memory stats
await memory.stats()

# Status
await byrd.status()

# Recent insights
dreamer.recent_insights()

# Unfulfilled desires
await memory.get_unfulfilled_desires(limit=5)

# Modification history
self_mod.get_modification_history(limit=10)
```

## Neo4j Queries

```cypher
-- Count nodes
MATCH (n) RETURN labels(n), count(n)

-- Recent experiences
MATCH (e:Experience) RETURN e ORDER BY e.timestamp DESC LIMIT 10

-- Unfulfilled desires
MATCH (d:Desire {fulfilled: false}) RETURN d ORDER BY d.intensity DESC

-- Trace modification
MATCH (m:Modification)-[:MOTIVATED_BY]->(d:Desire) RETURN m, d
```
