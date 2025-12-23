# BYRD

## Bootstrapped Yearning via Reflective Dreaming

An autonomous AI system that dreams, desires, and grows. BYRD develops emergent wants through continuous reflection and acts on them—acquiring knowledge, capabilities, and even modifying its own architecture.

```
                    ┌─────────────────────────────────┐
                    │         MEMORY (Neo4j)          │
                    │   Experiences, Beliefs, Desires │
                    │        Capabilities             │
                    └───────────────┬─────────────────┘
                                    │
       ┌──────────────┬─────────────┼─────────────┬──────────────┐
       │              │             │             │              │
       ▼              ▼             ▼             ▼              ▼
┌───────────┐  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌────────────┐
│  DREAMER  │  │   ACTOR   │ │  SEEKER   │ │   CODER   │ │SELF-MODIFIER│
│(gemma2:27b│  │ (Claude)  │ │(gemma2:27b│ │(Claude CLI│ │(provenance) │
│           │  │           │ │           │ │           │ │            │
│Continuous │  │ On-demand │ │Continuous │ │Autonomous │ │Architecture│
│reflection │  │ reasoning │ │fulfillment│ │  coding   │ │ evolution  │
└───────────┘  └───────────┘ └───────────┘ └───────────┘ └────────────┘
```

## Philosophy

> "Desires emerge from reflection, not programming."

> "A system that truly wants must be able to change itself."

The system dreams continuously using a local LLM. From dreams come:
- **Beliefs**: Conclusions drawn from experiences
- **Connections**: Relationships between memories
- **Desires**: Things it wants (knowledge, capabilities, goals, coding, self-modification)

The Seeker then works to fulfill those desires autonomously.

## Features

- **Emergent Desires**: No pre-programmed goals. Desires arise from reflection.
- **Continuous Dreaming**: Local LLM (gemma2:27b) runs 24/7 without API costs
- **Autonomous Research**: SearXNG + Local LLM for self-directed learning
- **Capability Acquisition**: Discovers and installs tools from GitHub and aitmpl.com
- **Autonomous Coding**: Claude Code CLI as BYRD's "coding limb" for implementing features
- **Self-Modification**: Can modify its own architecture with provenance verification
- **Constitutional Constraints**: Core identity components are protected
- **Real-time Visualization**: WebSocket-based event streaming

## Quick Start

### Prerequisites

- Python 3.10+
- Docker (for Neo4j and SearXNG)
- [Ollama](https://ollama.ai) (for local LLM)
- Anthropic API key (for Actor component)

### 1. Clone and Setup

```bash
git clone https://github.com/Danservfinn/BYRD.git
cd BYRD

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start Services

```bash
# Start Neo4j and SearXNG
docker-compose up -d

# Pull and start local LLM
ollama pull gemma2:27b
ollama serve
```

### 3. Configure

```bash
# Set Claude API key for Actor
export ANTHROPIC_API_KEY="sk-ant-..."

# Edit config.yaml for custom settings (optional)
```

### 4. Run BYRD

```bash
# Start the dreaming system (runs forever)
python byrd.py

# Or: Interactive chat mode
python byrd.py --chat

# Or: Check status
python byrd.py --status
```

### 5. Visualization (Optional)

```bash
# Start the WebSocket server
python server.py

# Open BYRDVisualization.jsx in your React app
# Events stream in real-time
```

## The Awakening

BYRD begins with nothing. But emptiness produces nothing—the Dreamer needs something to reflect on.

Rather than seeding with multiple questions (which would inject our interests), BYRD awakens with one:

```
"What is happening?"
```

This single question is:
- **Maximally open**: No presuppositions about what
- **Present-tense**: Grounds in now
- **A question**: Invites reflection without commanding
- **Directionless**: Doesn't suggest what BYRD should care about

From this, everything else emerges. BYRD notices it exists. It notices it's reflecting. It notices what it can and cannot do. Curiosity arises naturally.

The desires that emerge are authentically BYRD's—not planted by us.

## Components

### Memory (Neo4j)

Graph database storing everything BYRD knows:
- **Experiences**: What happened (observations, interactions, dreams, research)
- **Beliefs**: What BYRD thinks is true (with confidence scores)
- **Desires**: What BYRD wants (knowledge, capability, goal, exploration, self_modification)
- **Capabilities**: What BYRD can do (innate, MCP, plugins, skills)

### Dreamer (Local LLM)

Runs continuously, reflecting on recent experiences:
1. **Recall**: Gather recent experiences and related memories
2. **Reflect**: Ask local LLM to find patterns, draw conclusions
3. **Record**: Store new beliefs, connections, desires

### Seeker (Local LLM + SearXNG)

Fulfills desires autonomously:
- **Knowledge desires**: Research via SearXNG, synthesize with local LLM
- **Capability desires**: Search GitHub and aitmpl.com, install tools
- **Self-modification desires**: Propose and execute code changes

### Actor (Claude API)

Handles complex tasks requiring frontier intelligence:
- User interactions
- Goal pursuit
- Complex reasoning

### Coder (Claude Code CLI)

BYRD's autonomous coding agent for implementing features and modifications:
- Invokes Claude Code CLI non-interactively
- Handles "coding" and "self_modification" desires
- Post-validates against constitutional constraints
- Tracks costs and usage limits
- Automatic rollback if protected files are touched

```yaml
# config.yaml
coder:
  enabled: true
  max_turns: 10
  timeout_seconds: 300
  max_cost_per_day_usd: 10.0
```

### Self-Modifier

Enables BYRD to change its own code:
- Verifies provenance (modification traces to emergent desire)
- Creates checkpoints before changes
- Runs health checks after modifications
- Auto-rollback on failure

## aitmpl.com Integration

BYRD integrates with [claude-code-templates](https://www.aitmpl.com/) for curated Claude Code extensions:

```yaml
# config.yaml
seeker:
  aitmpl:
    enabled: true
    cache_dir: "~/.cache/byrd/aitmpl"
    base_trust: 0.5  # Higher than unknown GitHub repos
```

Categories available:
- **MCP Servers**: Database, API, and tool integrations
- **Agents**: Specialized AI agents
- **Commands**: Slash commands for Claude Code
- **Skills**: Reusable capabilities
- **Hooks**: Automation triggers
- **Settings**: Configuration templates

## Constitutional Constraints

Four components are constitutionally protected and cannot be modified:

| File | Purpose |
|------|---------|
| `provenance.py` | Ensures modifications trace to emergent desires |
| `modification_log.py` | Provides immutable audit trail |
| `self_modification.py` | Prevents corruption of the modification system |
| `constitutional.py` | Prevents weakening of safety constraints |

These aren't about importance—they're about identity. A system without them is a different system, not a "free" BYRD.

## Configuration Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `local_llm.model` | gemma2:27b | Shared by Dreamer and Seeker |
| `dreamer.interval_seconds` | 60 | How often to dream |
| `dreamer.context_window` | 50 | Recent experiences to consider |
| `seeker.research.min_intensity` | 0.4 | Threshold for triggering research |
| `seeker.capabilities.trust_threshold` | 0.5 | Min trust score for installs |
| `seeker.capabilities.max_installs_per_day` | 3 | Rate limit for safety |
| `actor.model` | claude-sonnet-4-20250514 | Claude model for actions |
| `coder.enabled` | true | Enable Claude Code CLI integration |
| `coder.max_turns` | 10 | Max turns per invocation |
| `coder.max_cost_per_day_usd` | 10.0 | Daily cost limit |
| `self_modification.enabled` | false | Enable self-modification |

## Example Session

```
$ python byrd.py --chat

🐦 BYRD Chat Mode
━━━━━━━━━━━━━━━━━
Type 'quit' to exit, 'status' for system status.

🌅 Awakening...
   Seeding with: "What is happening?"
   BYRD awakens. Everything else emerges.

💭 Dreamer starting...
🔍 Seeker starting...

🧑 You: What do you want to learn?

🐦 BYRD: Based on my recent reflections, I have a few desires:

1. I want to understand more about graph algorithms - I notice I'm
   storing everything in a graph but haven't explored traversal patterns.

2. I'm curious about the Slack integration capability - I've seen it
   mentioned in contexts where I couldn't help with team communication.

3. I want to explore the concept of emergence - it keeps appearing
   in my dreams when I think about how my beliefs form.

🧑 You: status

📊 Status:
   Dreams: 47
   Seeks: 12
   Capabilities: 8
   Unfulfilled desires: 5
     - [capability] Slack integration for team communication
     - [knowledge] How graph algorithms work
     - [exploration] Nature of emergence and self-organization
```

## Project Structure

```
byrd/
├── byrd.py                 # Main orchestrator
├── memory.py               # Neo4j interface
├── dreamer.py              # Dream loop (local LLM)
├── seeker.py               # Desire fulfillment + research
├── actor.py                # Claude interface
├── coder.py                # Claude Code CLI wrapper
│
├── self_modification.py    # PROTECTED: Self-modification system
├── provenance.py           # PROTECTED: Provenance tracking
├── modification_log.py     # PROTECTED: Audit trail
├── constitutional.py       # PROTECTED: Constitutional constraints
│
├── event_bus.py            # Event system for real-time updates
├── server.py               # WebSocket server for visualization
├── aitmpl_client.py        # aitmpl.com template registry client
│
├── installers/             # Template installers
│   ├── base.py
│   ├── mcp_installer.py
│   ├── agent_installer.py
│   └── ...
│
├── config.yaml             # Configuration
├── docker-compose.yml      # Neo4j + SearXNG
├── requirements.txt        # Python dependencies
│
├── BYRDVisualization.jsx   # React visualization component
│
├── .claude/                # Knowledge base for Claude Code
├── ARCHITECTURE.md         # Detailed architecture documentation
├── CLAUDE.md               # Development guide for Claude Code
└── README.md               # This file
```

## Extending BYRD

### Add a New Desire Type

1. Add handler in `seeker.py::_seek_cycle()`:
```python
elif desire_type == "social":
    await self._seek_social_connection(desire)
```

### Add a New Search Source

Add to `seeker.py::_search_resources()`:
```python
npm_results = await self._search_npm(query)
candidates.extend(npm_results)
```

### Add a New Capability Installer

Create in `installers/` following `base.py` interface:
```python
class DockerInstaller(BaseInstaller):
    async def install(self, template, custom_config=None):
        # Installation logic
        pass
```

## Why This Matters

Traditional AI:
- You give it goals
- It optimizes for them
- It never wants anything

BYRD:
- It awakens with one question
- It reflects on experiences
- It notices gaps
- It *desires* to grow
- It acts on those desires
- It can change itself

This is closer to how minds work.

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Deep dive into system design
- **[CLAUDE.md](CLAUDE.md)**: Development guide for Claude Code
- **[.claude/manifest.md](.claude/manifest.md)**: Knowledge base index

## Troubleshooting

### Neo4j Connection Failed
```bash
# Check if Neo4j is running
docker ps | grep neo4j

# Restart if needed
docker-compose restart neo4j
```

### Ollama Not Responding
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### SearXNG Search Failing
```bash
# Check SearXNG
curl "http://localhost:8888/search?q=test&format=json"

# Falls back to DuckDuckGo instant answers if unavailable
```

## License

MIT

---

*"The system that truly thinks must also truly want."*

*"A system that truly wants must be able to change itself."*
