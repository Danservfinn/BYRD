---
title: Configuration Reference
link: configuration-reference
type: metadata
ontological_relations: []
tags: [config, yaml, settings, neo4j, ollama, searxng, zai, cloud, huggingface]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-24T18:00:00Z
uuid: f6f78090-6789-9abc-def0-123456789012
---

## Files
- `/Users/kurultai/BYRD/config.yaml` - Main configuration
- `/Users/kurultai/BYRD/.env` - Environment variables (not in git)
- `/Users/kurultai/BYRD/.env.example` - Environment template

## Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `NEO4J_URI` | Neo4j connection string | Yes |
| `NEO4J_USER` | Neo4j username | Yes |
| `NEO4J_PASSWORD` | Neo4j password | Yes |
| `ZAI_API_KEY` | Z.AI LLM API key | For cloud LLM |
| `OPENROUTER_API_KEY` | OpenRouter API key | Alternative LLM |
| `ANTHROPIC_API_KEY` | Claude API access | For Actor |
| `CLOUD_DEPLOYMENT` | Enable cloud features | For HuggingFace |
| `HF_TOKEN` | HuggingFace token | For deployment |

## LLM Providers

```yaml
local_llm:
  # Provider options: "ollama", "openrouter", "zai"
  provider: "zai"

  # Z.AI models: "glm-4-flash", "glm-4.7", "glm-4-plus"
  # OpenRouter models: "deepseek/deepseek-v3.2-speciale", etc.
  # Ollama models: "gemma2:27b", "llama3:70b", etc.
  model: "glm-4.7"

  # Ollama endpoint (only used when provider: ollama)
  endpoint: "http://localhost:11434/api/generate"

  timeout: 600.0
```

## Neo4j Configuration

```yaml
memory:
  # Local: bolt://localhost:7687
  # Cloud (Neo4j Aura): neo4j+s://xxxxx.databases.neo4j.io
  neo4j_uri: "${NEO4J_URI:-bolt://localhost:7687}"
  neo4j_user: "${NEO4J_USER:-neo4j}"
  neo4j_password: "${NEO4J_PASSWORD:-prometheus}"
```

## Complete Configuration

```yaml
# Neo4j Memory Graph
memory:
  neo4j_uri: "${NEO4J_URI:-bolt://localhost:7687}"
  neo4j_user: "${NEO4J_USER:-neo4j}"
  neo4j_password: "${NEO4J_PASSWORD:-prometheus}"

# Ego (optional personality)
ego: "black-cat"  # or null for pure emergence

# LLM Provider (shared by Dreamer and Seeker)
local_llm:
  provider: "zai"  # "ollama", "openrouter", or "zai"
  model: "glm-4.7"
  timeout: 600.0

# Dreamer Settings
dreamer:
  interval_seconds: 60      # Dream every 60 seconds
  context_window: 50        # Recent experiences to consider
  adaptive_interval: false  # Fixed interval for consistency

# Quantum Randomness
quantum:
  enabled: true
  pool_size: 256
  temperature_max_delta: 0.15
  significance_threshold: 0.05

# Seeker Settings
seeker:
  interval_seconds: 10
  research:
    searxng_url: "http://localhost:8888"
    min_intensity: 0.3
    max_queries: 5
    max_results: 15

# Actor Settings (Claude API)
actor:
  model: "claude-sonnet-4-20250514"

# Coder Settings (Claude Code CLI)
coder:
  enabled: true
  max_turns: 10
  timeout_seconds: 300
  max_cost_per_day_usd: 10.0

# Self-Modification Settings
self_modification:
  enabled: true
  require_health_check: true
  auto_rollback_on_failure: true
```

## Cloud Deployment

For HuggingFace Spaces deployment:

```bash
# .env file (never commit!)
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
ZAI_API_KEY=your-zai-key
CLOUD_DEPLOYMENT=true
```

## Docker Services (Local)

| Service | Port | Purpose |
|---------|------|---------|
| Neo4j Browser | 7474 | Web UI |
| Neo4j Bolt | 7687 | Database connection |
| SearXNG | 8888 | Self-hosted search |
| BYRD Server | 8000 | REST + WebSocket |

## Cloud Services

| Service | URL |
|---------|-----|
| HuggingFace Space | https://omoplatapus-byrd-ai.hf.space |
| Neo4j Aura Console | https://console.neo4j.io |
| Z.AI Console | https://open.bigmodel.cn |
