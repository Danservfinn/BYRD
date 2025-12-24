---
title: BYRD Quick Commands
link: quick-commands
type: cheatsheets
ontological_relations: []
tags: [commands, cli, docker, ollama, startup, debugging, cloud, huggingface]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-24T18:00:00Z
uuid: f8190b12-89ab-bcde-f012-345678901234
---

## Cloud Deployment (HuggingFace)

```bash
# Deploy to HuggingFace Spaces (free)
export HF_TOKEN="hf_your_token"
python deploy_huggingface.py

# Control live instance
curl -X POST https://omoplatapus-byrd-ai.hf.space/api/start
curl -X POST https://omoplatapus-byrd-ai.hf.space/api/stop
curl -X POST https://omoplatapus-byrd-ai.hf.space/api/awaken
curl https://omoplatapus-byrd-ai.hf.space/api/status
```

## Setup

```bash
# Clone and setup
git clone https://github.com/Danservfinn/BYRD.git
cd BYRD
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Startup

```bash
# Start services
docker-compose up -d

# Start Ollama (local LLM)
ollama pull gemma2:27b
ollama serve

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run BYRD
python byrd.py          # Default: continuous dreaming
python byrd.py --chat   # Interactive chat mode
python byrd.py --status # Show status and exit

# Start visualization server
python server.py
```

## Service URLs

### Cloud (Live Instance)
| Service | URL | Purpose |
|---------|-----|---------|
| Visualization | https://omoplatapus-byrd-ai.hf.space/byrd-3d-visualization.html | 3D mind view |
| API | https://omoplatapus-byrd-ai.hf.space/api/status | REST API |
| WebSocket | wss://omoplatapus-byrd-ai.hf.space/ws/events | Event streaming |
| Neo4j Aura | neo4j+s://e67da195.databases.neo4j.io | Cloud graph DB |

### Local Development
| Service | URL | Purpose |
|---------|-----|---------|
| Neo4j Browser | http://localhost:7474 | Graph database UI |
| Neo4j Bolt | bolt://localhost:7687 | Database connection |
| SearXNG | http://localhost:8888 | Self-hosted search |
| Ollama | http://localhost:11434 | Local LLM API |
| Server | http://localhost:8000 | REST + WebSocket |

## Verification

```bash
# Check Neo4j
docker ps | grep neo4j

# Check Ollama
curl http://localhost:11434/api/tags

# Check SearXNG
curl "http://localhost:8888/search?q=test&format=json"

# Test LLM
curl http://localhost:11434/api/generate \
  -d '{"model": "gemma2:27b", "prompt": "Hello"}'
```

## Debugging (Python)

```python
# Memory stats
await memory.stats()

# System status
status = await byrd.status()

# Recent insights
dreamer.recent_insights()

# Unfulfilled desires
await memory.get_unfulfilled_desires(limit=5)

# Modification history
self_mod.get_modification_history(limit=10)

# Self-mod statistics
self_mod.get_statistics()

# aitmpl client stats
aitmpl_client.get_statistics()
```

## Neo4j Queries

```cypher
-- Count all nodes by type
MATCH (n) RETURN labels(n)[0] as type, count(n) as count

-- Recent experiences
MATCH (e:Experience)
RETURN e.content, e.type, e.timestamp
ORDER BY e.timestamp DESC
LIMIT 10

-- Unfulfilled desires
MATCH (d:Desire {fulfilled: false})
RETURN d.description, d.type, d.intensity
ORDER BY d.intensity DESC

-- Beliefs with confidence
MATCH (b:Belief)
RETURN b.content, b.confidence
ORDER BY b.confidence DESC
LIMIT 10

-- Trace modification provenance
MATCH (m:Modification)-[:MOTIVATED_BY]->(d:Desire)
OPTIONAL MATCH (d)<-[:GENERATED]-(dream:Experience {type: 'dream'})
RETURN m.change_description, d.description, dream.content

-- Research that fulfilled desires
MATCH (e:Experience {type: 'research'})-[:FULFILLS]->(d:Desire)
RETURN e.content, d.description, e.timestamp
ORDER BY e.timestamp DESC

-- All capabilities
MATCH (c:Capability {active: true})
RETURN c.name, c.type, c.description
```

## Reset

```bash
# Clear Neo4j (destructive!)
# This triggers a fresh awakening on next run
docker-compose down -v
docker-compose up -d
```

## Logs

```bash
# Watch BYRD output
python byrd.py 2>&1 | tee byrd.log

# Docker logs
docker-compose logs -f neo4j
docker-compose logs -f searxng
```
