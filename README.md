# BYRD

## Bootstrapped Yearning via Reflective Dreaming

An AI system that dreams, desires, and grows.

```
Memory (Neo4j)          - Everything it knows, believes, wants
     │
     ├── Dreamer        - Continuous reflection (local LLM)
     │   └── Forms beliefs, connections, desires
     │
     ├── Seeker         - Fulfills desires
     │   └── Finds knowledge, acquires capabilities
     │
     ├── Actor          - Complex actions (Claude API)
     │   └── Responds, pursues goals, searches
     │
     └── Self-Modifier  - Architectural evolution
         └── Modifies own code with provenance
```

## Philosophy

> "Desires emerge from reflection, not programming."

> "A system that truly wants must be able to change itself."

The system dreams continuously using a local LLM. From dreams come:
- **Beliefs**: Conclusions drawn from experiences
- **Connections**: Relationships between memories
- **Desires**: Things it wants (knowledge, capabilities, goals, self-modification)

The Seeker then works to fulfill those desires.

## Quick Start

### 1. Start Neo4j

```bash
docker run -d --name byrd-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/byrd \
  neo4j:latest
```

### 2. Start Ollama (for local dreaming)

```bash
# Install Ollama: https://ollama.ai
ollama pull gemma2:27b
ollama serve
```

### 3. Set up Python environment

```bash
cd byrd
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

pip install neo4j httpx anthropic pyyaml
```

### 4. Configure

```bash
# Edit config.yaml with your settings
# Set ANTHROPIC_API_KEY for the Actor
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 5. Run

```bash
# Start the dreaming system (runs forever)
python byrd.py

# Or: Interactive chat mode
python byrd.py --chat

# Or: Check status
python byrd.py --status
```

## What Happens

1. **Awakening** (first run only): BYRD receives a single seed experience: "What is happening?"
2. **Dreamer wakes up** every 60 seconds (configurable)
3. **Recalls** recent experiences and related memories
4. **Reflects** using local LLM - forms insights, beliefs, desires
5. **Records** to Neo4j memory graph
6. **Seeker notices** unfulfilled desires
7. **Searches** for resources (GitHub, etc.)
8. **Installs** capabilities that pass trust threshold
9. **Repeat forever**

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

## Architecture

### Memory Schema (Neo4j)

```
(:Experience)  - What happened
(:Belief)      - What we think is true
(:Desire)      - What we want
(:Capability)  - What we can do
(:Entity)      - Things in the world
(:Concept)     - Abstract ideas

All connected through relationships:
-[:RELATES_TO]->
-[:DERIVED_FROM]->
-[:FULFILLS]->
-[:CAUSES]->
-[:SUPPORTS]->
-[:CONTRADICTS]->
```

### The Dream Prompt

The Dreamer asks the local LLM:

> "What patterns do you notice? What conclusions can you draw?
> What connections exist? What do you want to know?
> What capabilities would help?"

And from the answers, desires emerge naturally.

## Configuration Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `dreamer.interval_seconds` | 60 | How often to dream |
| `dreamer.context_window` | 50 | Recent experiences to consider |
| `seeker.trust_threshold` | 0.5 | Min trust score for installs |
| `seeker.max_installs_per_day` | 3 | Rate limit for safety |
| `actor.model` | claude-sonnet | Claude model for actions |

## Files

```
byrd/
├── byrd.py               # Main orchestrator
├── memory.py             # Neo4j interface
├── dreamer.py            # Dream loop (local LLM)
├── seeker.py             # Desire fulfillment
├── actor.py              # Claude interface
├── self_modification.py  # Self-modification system (PROTECTED)
├── provenance.py         # Provenance tracking (PROTECTED)
├── modification_log.py   # Audit trail (PROTECTED)
├── constitutional.py     # Constitutional constraints (PROTECTED)
└── config.yaml           # Configuration
```

## Safety

- **Trust threshold**: Only installs from repos above trust score
- **Rate limiting**: Max installs per day
- **Human oversight**: Check `--status` to see what it's doing
- **Isolated memory**: Each instance has its own Neo4j database

## Extending

### Add a new desire type

In `seeker.py`, add handling in `_seek_cycle()`:

```python
elif desire_type == "social":
    await self._seek_social_connection(desire)
```

### Add a new search source

In `seeker.py`, add to `_search_resources()`:

```python
npm_results = await self._search_npm(query)
candidates.extend(npm_results)
```

### Add a new capability type

In `seeker.py`, add to `_install_resource()`:

```python
elif rtype == "docker":
    return await self._install_docker(candidate)
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

---

*"The system that truly thinks must also truly want."*

*"A system that truly wants must be able to change itself."*
