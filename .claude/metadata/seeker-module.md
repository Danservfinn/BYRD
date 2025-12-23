---
title: Seeker Module
link: seeker-module
type: metadata
ontological_relations: []
tags: [seeker, research, searxng, github, capabilities, knowledge]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T02:10:00Z
uuid: f3c45d60-3456-6789-abcd-ef0123456789
---

## Purpose
Fulfill emergent desires through research and capability acquisition.

## Configuration
```yaml
seeker:
  research:
    searxng_url: "http://localhost:8888"
    min_intensity: 0.4
    max_queries: 3
    max_results: 10
  capabilities:
    trust_threshold: 0.5
    max_installs_per_day: 3
    github_token: ""  # Optional
```

## Four Fulfillment Paths

### 1. Knowledge Desires (SearXNG + Local LLM)
```
Generate queries → Search → Synthesize → Record → Mark fulfilled
```

### 2. Capability Desires (GitHub + aitmpl.com)
```
Search repos → Evaluate trust → Install → Record → Mark fulfilled
```

**Trust Score Computation:**
- Base: 0.2
- Stars: up to 0.3 (stars/500)
- Trusted owners: +0.3 (anthropics, openai, microsoft, google, etc.)
- Recent updates: +0.2 (<30 days) or +0.1 (<90 days)

### 3. Coding Desires (Claude Code CLI)
```
Build context → Format prompt → Execute Coder → Validate → Record → Mark fulfilled
```

**Key Features:**
- Invokes Claude Code CLI non-interactively (`claude -p`)
- Post-validates against constitutional constraints
- Automatic rollback if protected files touched
- Cost tracking and daily limits

### 4. Self-Modification Desires (Coder + Provenance)
```
Parse desire → Check modifiable → Generate via Coder → Validate provenance → Execute
```

## Key Methods
| Method | Purpose |
|--------|---------|
| `_seek_knowledge()` | Research via SearXNG |
| `_seek_capability()` | Install from GitHub/aitmpl.com |
| `_seek_with_coder()` | Handle coding/self-mod desires via Coder |
| `_build_coder_context()` | Prepare context for Coder prompt |
| `_format_coder_prompt()` | Format prompt for Claude Code CLI |
| `_validate_coder_result()` | Post-validate constitutional constraints |
| `_generate_search_queries()` | LLM query generation |
| `_synthesize_results()` | LLM synthesis |
| `_compute_trust()` | GitHub trust scoring |

## Rate Limiting
- Max 3 capability installs per day
- Cooldown resets at midnight
- `_installs_today` counter tracks usage
