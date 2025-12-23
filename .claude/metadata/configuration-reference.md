---
title: Configuration Reference
link: configuration-reference
type: metadata
ontological_relations: []
tags: [config, yaml, settings, neo4j, ollama, searxng]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T02:10:00Z
uuid: f6f78090-6789-9abc-def0-123456789012
---

## File
`/Users/kurultai/BYRD/config.yaml`

## Complete Configuration

```yaml
# Neo4j Memory Graph
memory:
  neo4j_uri: "bolt://localhost:7687"
  neo4j_user: "neo4j"
  neo4j_password: "prometheus"

# Local LLM (shared by Dreamer and Seeker)
local_llm:
  model: "gemma2:27b"
  endpoint: "http://localhost:11434/api/generate"

# Dreamer Settings
dreamer:
  interval_seconds: 60      # Dream every minute
  context_window: 50        # Recent experiences to consider

# Seeker Settings
seeker:
  research:
    searxng_url: "http://localhost:8888"
    min_intensity: 0.4      # Only research desires above threshold
    max_queries: 3          # Queries per desire
    max_results: 10         # Results to synthesize
  capabilities:
    trust_threshold: 0.5
    max_installs_per_day: 3
    github_token: ""        # Optional for higher rate limits

# Actor Settings (Claude API)
actor:
  model: "claude-sonnet-4-20250514"
  # api_key via ANTHROPIC_API_KEY env var

# Self-Modification Settings
self_modification:
  enabled: true
  checkpoint_dir: "./checkpoints"
  max_checkpoints: 100
  require_health_check: true
  auto_rollback_on_failure: true
  max_modifications_per_day: 5
  cooldown_between_modifications_seconds: 3600
```

## Environment Variables
| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Claude API access |

## Docker Services
| Service | Port | Purpose |
|---------|------|---------|
| Neo4j Browser | 7474 | Web UI |
| Neo4j Bolt | 7687 | Database connection |
| SearXNG | 8888 | Self-hosted search |
