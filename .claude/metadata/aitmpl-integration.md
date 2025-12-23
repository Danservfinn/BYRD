# aitmpl.com Integration

BYRD integrates with [claude-code-templates](https://www.aitmpl.com/) (davila7/claude-code-templates) to discover and install curated Claude Code extensions.

## Purpose

Provides a trusted source of templates for capability acquisition. Templates from aitmpl.com receive a higher base trust score than unknown GitHub repositories because they are curated.

## Client Architecture

```
aitmpl_client.py
├── AitmplTemplate    - Template data structure
├── AitmplRegistry    - Cached registry of all templates
└── AitmplClient      - Main client class
    ├── fetch_registry()       - Fetch/cache template list
    ├── search()               - Search templates by query
    ├── get_template()         - Get specific template
    └── infer_categories()     - Match desires to categories
```

## Template Categories

| Category | Path in Repo | Purpose |
|----------|--------------|---------|
| `agent` | `.claude/agents/` | Specialized AI agents |
| `command` | `.claude/commands/` | Slash commands |
| `mcp` | `.mcp.json` | MCP server integrations |
| `skill` | `.claude/skills/` | Reusable capabilities |
| `hook` | `.claude/hooks/` | Automation triggers |
| `setting` | `.claude/settings.local.json` | Configuration templates |

## Caching

- Registry is cached to avoid GitHub API rate limits
- Default cache TTL: 24 hours
- Cache location: `~/.cache/byrd/aitmpl/registry.json`
- Force refresh: `await client.refresh_cache()`

## Configuration

```yaml
seeker:
  aitmpl:
    enabled: true
    cache_dir: "~/.cache/byrd/aitmpl"
    cache_ttl_hours: 24
    base_trust: 0.5  # Curated templates get higher trust
    install_paths:
      agent: "~/.claude/agents"
      command: "~/.claude/commands"
      skill: "~/.claude/skills"
      hook: "~/.claude/hooks"
      setting: "~/.claude/settings.local.json"
      mcp: "~/.config/claude/mcp_config.json"
```

## Trust Scoring

Templates are scored based on:
- Base trust: 0.5 (curated source)
- Recent update bonus: +0.2 (< 30 days), +0.1 (< 90 days)
- Has content: +0.2
- Category match: +0.1 (mcp, agent, skill)

Maximum score: 1.0

## Category Inference

The client infers which categories to search based on desire keywords:

```python
CATEGORY_KEYWORDS = {
    "agent": ["agent", "assistant", "specialist", "expert"],
    "mcp": ["mcp", "integration", "database", "api", "server"],
    "command": ["command", "slash", "cli", "action"],
    "skill": ["skill", "capability", "ability"],
    "hook": ["hook", "automation", "trigger"],
    "setting": ["setting", "config", "preference"],
}
```

## Installers

Each category has a specialized installer in `installers/`:

| Category | Installer | Installation Target |
|----------|-----------|---------------------|
| agent | `agent_installer.py` | `~/.claude/agents/{name}.md` |
| command | `command_installer.py` | `~/.claude/commands/{name}.md` |
| mcp | `mcp_installer.py` | `~/.config/claude/mcp_config.json` |
| skill | `skill_installer.py` | `~/.claude/skills/{name}.md` |
| hook | `hook_installer.py` | `~/.claude/hooks/{name}.md` |
| setting | `settings_installer.py` | Merges into settings |

## Flow

1. Seeker has a capability desire
2. Seeker calls `aitmpl_client.search(desire_description)`
3. Client infers categories and searches registry
4. Results are scored and filtered by trust threshold
5. Best candidate is passed to appropriate installer
6. Installer writes template to correct location
7. Capability is recorded in Memory graph

## Key Files

- `aitmpl_client.py:77-505` - Main client implementation
- `seeker.py:493-529` - aitmpl search integration
- `seeker.py:690-734` - aitmpl template installation
- `installers/*.py` - Category-specific installers
