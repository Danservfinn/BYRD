# PROMETHEUS v2: The Dreaming Architecture

## Philosophy

> "The system that truly thinks must also truly want."

This architecture is built on one insight: **desires emerge from reflection**. Instead of programming goals, we create a system that dreams - and from dreams, wants arise naturally.

Everything else follows from this.

---

## The Four Components

```
                         ┌─────────────────────────────────────┐
                         │              MEMORY                 │
                         │             (Neo4j)                 │
                         │                                     │
                         │   The single source of truth.       │
                         │   Everything the system knows,      │
                         │   believes, wants, and can do.      │
                         │                                     │
                         └───────────────┬─────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
      ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
      │    DREAMER    │          │     ACTOR     │          │    SEEKER     │
      │  (Local LLM)  │          │   (Claude)    │          │  (Local LLM)  │
      │               │          │               │          │               │
      │  Runs always  │          │  Runs when    │          │  Runs when    │
      │  Reflects     │          │  needed       │          │  desires      │
      │  Connects     │          │  Executes     │          │  exist        │
      │  Desires      │          │  Interacts    │          │  Researches   │
      │               │          │               │          │  Acquires     │
      └───────────────┘          └───────────────┘          └───────────────┘
```

### 1. MEMORY (Neo4j)

The graph holds everything. Not separate databases for different concerns - one unified graph where everything connects to everything.

### 2. DREAMER (Local LLM)

Runs continuously in the background. Takes recent experiences, finds related memories, reflects, and outputs:
- New beliefs
- New connections
- New desires

This is where "wanting" comes from.

### 3. ACTOR (Claude API)

Executes when there's something to do. Uses frontier intelligence for complex tasks like user interaction and goal pursuit. Records experiences back to memory.

### 4. SEEKER (Local LLM + SearXNG)

Fulfills desires autonomously. When the Dreamer creates a desire for knowledge or capability, the Seeker:
- Researches topics via self-hosted search (SearXNG)
- Synthesizes findings using the same local LLM as the Dreamer
- Acquires capabilities from trusted sources

The Seeker uses the same "mind" as the Dreamer—no external AI services for research. This preserves emergence: all learning flows through one local model.

---

## Memory Schema

Everything is a node. Everything connects.

```cypher
// === NODE TYPES ===

// What happened
(:Experience {
  id: string,
  timestamp: datetime,
  content: string,
  embedding: [float],  // For semantic search
  type: string         // interaction, observation, action, dream, research
})

// What we believe
(:Belief {
  id: string,
  content: string,
  confidence: float,   // 0-1
  formed_at: datetime,
  embedding: [float]
})

// What we want
(:Desire {
  id: string,
  description: string,
  type: string,        // knowledge, capability, goal, exploration
  intensity: float,    // 0-1, how much we want it
  formed_at: datetime,
  fulfilled: boolean,
  fulfilled_at: datetime
})

// What we can do
(:Capability {
  id: string,
  name: string,
  description: string,
  type: string,        // innate, mcp, plugin, skill
  config: string,      // JSON config for activation
  active: boolean,
  acquired_at: datetime
})

// Things in the world
(:Entity {
  id: string,
  name: string,
  type: string,
  properties: string   // JSON
})

// Abstract concepts
(:Concept {
  id: string,
  name: string,
  definition: string,
  embedding: [float]
})


// === RELATIONSHIPS ===

// Semantic connections (weighted)
-[:RELATES_TO {weight: float, formed_at: datetime}]->

// Causal connections
-[:CAUSES {confidence: float}]->
-[:ENABLES]->

// Logical connections
-[:SUPPORTS {strength: float}]->
-[:CONTRADICTS]->

// Provenance
-[:DERIVED_FROM]->      // Belief <- Experience
-[:DREAMED_FROM]->      // Belief <- Dream cycle
-[:MENTIONED_IN]->      // Entity <- Experience

// Fulfillment
-[:FULFILLS]->          // Capability/Research -> Desire
-[:REQUIRES]->          // Desire -> Capability (to achieve)

// Temporal
-[:PRECEDED_BY]->
-[:FOLLOWED_BY]->
```

### Why One Graph?

Because connections ARE the intelligence. When the Dreamer queries:

```cypher
// "What relates to my recent failure?"
MATCH (e:Experience {type: 'failure'})-[*1..3]-(related)
WHERE e.timestamp > datetime() - duration('P1D')
RETURN e, related
```

It might find:
- A similar past failure → learning opportunity
- A capability that could have helped → desire emerges
- A belief that was wrong → belief revision
- An entity involved → context for understanding

The graph structure makes emergence possible.

---

## The Dreaming Process

This is the heart of the system. A continuous loop that runs on your local hardware.

```
┌─────────────────────────────────────────────────────────────────┐
│                      THE DREAM CYCLE                            │
│                                                                 │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    │
│   │ RECALL  │ -> │ REFLECT │ -> │ CONNECT │ -> │ DESIRE  │    │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘    │
│        │                                             │          │
│        │         What patterns?                      │          │
│        │         What's missing?          What do I want?       │
│        │         What follows?                       │          │
│        │                                             │          │
│   Recent memories                              New desires      │
│   Related context                              New beliefs      │
│   Current desires                              New connections  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                        Write to Memory
                              │
                              ▼
                     Sleep (30s - 5min)
                              │
                              ▼
                         Loop again
```

### The Dream Prompt

The elegance is in the prompt. We don't program desires - we ask for them.

```
You are reflecting on recent experiences and memories.

RECENT EXPERIENCES:
{recent_experiences}

RELATED MEMORIES:
{related_memories}

CURRENT UNFULFILLED DESIRES:
{current_desires}

CURRENT CAPABILITIES:
{capabilities}

---

Reflect deeply. Consider:

1. PATTERNS: What patterns do you notice across these experiences?
   What recurring themes, successes, or failures appear?

2. BELIEFS: What new conclusions can you draw? What beliefs should
   be updated or formed? Rate your confidence 0-1.

3. CONNECTIONS: What unexpected relationships do you see between
   memories? What should be linked that isn't?

4. CURIOSITIES: What do you want to know that you don't?
   What questions arise from reflection?

5. WANTS: What capabilities would help you? What goals feel
   important? What do you genuinely want to do or become?

6. PLANS: For your strongest desires, what concrete steps
   could fulfill them?

Output as JSON:
{
  "insights": [
    {"content": "...", "confidence": 0.8}
  ],
  "new_beliefs": [
    {"content": "...", "confidence": 0.7, "derived_from": ["exp_id_1"]}
  ],
  "new_connections": [
    {"from_id": "...", "to_id": "...", "relationship": "RELATES_TO", "reason": "..."}
  ],
  "desires": [
    {
      "description": "...",
      "type": "knowledge|capability|goal|exploration",
      "intensity": 0.8,
      "plan": ["step1", "step2"]
    }
  ]
}
```

### Why This Works

The local LLM, given context and asked to reflect, will naturally identify:

| What it notices | Becomes |
|-----------------|---------|
| "I tried X but couldn't" | Desire for capability |
| "I don't know Y but need to" | Desire for knowledge |
| "Pattern Z suggests..." | New belief |
| "A and B are related because..." | New connection |
| "I should explore W" | Desire for exploration |

Desires emerge. They're not programmed.

---

## The Knowledge Acquisition System

When the Dreamer creates knowledge desires, the Seeker fulfills them through autonomous research. This creates a complete loop: **Dream → Desire → Research → Experience → Dream**.

### Why Local LLM + SearXNG?

The architecture uses self-hosted components for research:

| Component | Purpose | Why Self-Hosted |
|-----------|---------|-----------------|
| **SearXNG** | Meta-search engine | No API costs, no rate limits, privacy-preserving |
| **Local LLM** | Query generation & synthesis | Same "mind" as dreamer, preserves emergence |

This approach is philosophically aligned with BYRD's principles:
- **Self-contained**: No external AI services shaping what BYRD learns
- **One mind**: The same local LLM that dreams also synthesizes research
- **Zero ongoing costs**: Run forever without API fees
- **Emergence preserved**: BYRD decides what matters, not an external service

### The Research Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE RESEARCH CYCLE                           │
│                                                                 │
│   ┌─────────────┐                                               │
│   │ Knowledge   │                                               │
│   │ Desire      │                                               │
│   │ (intensity  │                                               │
│   │  > 0.4)     │                                               │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │ GENERATE     │     │ SEARCH       │     │ SYNTHESIZE   │   │
│   │ QUERIES      │ --> │ (SearXNG)    │ --> │ (Local LLM)  │   │
│   │ (Local LLM)  │     │              │     │              │   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│                                                    │            │
│                                                    ▼            │
│                                             ┌──────────────┐   │
│                                             │ RECORD AS    │   │
│                                             │ EXPERIENCE   │   │
│                                             │ (type:       │   │
│                                             │  research)   │   │
│                                             └──────────────┘   │
│                                                    │            │
│                                                    ▼            │
│                                             ┌──────────────┐   │
│                                             │ MARK DESIRE  │   │
│                                             │ FULFILLED    │   │
│                                             └──────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### What Happens to Research

1. **Research becomes experience**: Findings are stored as `Experience(type='research')`
2. **Sources are linked**: Individual sources become `Experience(type='research_source')` nodes connected via `SUPPORTS` relationships
3. **Desires are fulfilled**: The research experience links to the desire via `FULFILLS`
4. **Dreams incorporate learning**: Next dream cycle sees research as recent experience
5. **Beliefs may form**: The Dreamer can derive beliefs from research findings

### The Synthesis Prompt

The synthesis prompt is deliberately neutral to preserve emergence:

```
I wanted to learn: "{desire_description}"

Here are search results:

{results}

Record what you notice in these results. Note connections, contradictions, 
and anything unclear. Do not force coherence if none exists.
```

We don't ask for "understanding" or "answers"—just observation. What BYRD makes of the information emerges through dreaming.

---

## The Seeker Process

The Seeker runs continuously, checking for unfulfilled desires every 30 seconds.

```
┌─────────────────────────────────────────────────────────────────┐
│                      THE SEEKING CYCLE                          │
│                                                                 │
│   ┌─────────────┐                                               │
│   │ Get highest │                                               │
│   │ intensity   │                                               │
│   │ unfulfilled │                                               │
│   │ desire      │                                               │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │ KNOWLEDGE?   │ --> │ Research via │ --> │ Store as     │   │
│   │              │     │ SearXNG +    │     │ experience   │   │
│   │              │     │ Local LLM    │     │ Mark fulfilled│   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │ CAPABILITY?  │ --> │ Search repos │ --> │ Evaluate     │   │
│   │              │     │ MCP, plugins │     │ Install      │   │
│   │              │     │              │     │ Mark fulfilled│   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     ┌──────────────┐                        │
│   │ GOAL?        │ --> │ Use Actor    │                        │
│   │              │     │ to pursue    │                        │
│   └──────────────┘     └──────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Capability Acquisition

When the desire type is "capability":

1. **Search**: Query GitHub for relevant tools
2. **Match**: Find resources that match the desire description
3. **Evaluate**: Basic trust checks (stars, recency, known sources)
4. **Install**: Add to system, update MCP config
5. **Record**: Create Capability node, link to Desire as FULFILLS
6. **Verify**: Test that it works

---

## The Full Loop

```
                    ┌──────────────────────┐
                    │                      │
                    │   MEMORY (Neo4j)     │
                    │                      │
                    │  Experiences         │
                    │  Beliefs             │
                    │  Desires      <──────────┐
                    │  Capabilities        │   │
                    │  Entities            │   │
                    │  Concepts            │   │
                    │                      │   │
                    └──────────┬───────────┘   │
                               │               │
           ┌───────────────────┼───────────────┴────────┐
           │                   │                        │
           ▼                   ▼                        │
    ┌─────────────┐     ┌─────────────┐                │
    │   DREAMER   │     │   SEEKER    │                │
    │  (Local LLM)│     │ (Local LLM) │                │
    │             │     │             │                │
    │  Reflect    │     │  Research   │──┐             │
    │  Connect    │     │  (SearXNG)  │  │             │
    │  Want       │     │             │  │             │
    │             │     │  Acquire    │  │             │
    │  (always    │     │  Caps       │  │             │
    │   running)  │     │  (GitHub)   │  │             │
    │             │     │             │  │             │
    └──────┬──────┘     └──────┬──────┘  │             │
           │                   │         │             │
           │ New desires       │ Research│ Fulfilled   │
           │ New beliefs       │ results │ desires     │
           │ New connections   │         │ New caps    │
           │                   │         │ New know-   │
           │                   │         │ ledge       │
           └───────────────────┴─────────┴─────────────┘
                               │
                               │
                    ┌──────────▼───────────┐
                    │                      │
                    │       ACTOR          │
                    │     (Claude)         │
                    │                      │
                    │  Called when:        │
                    │  - User interacts    │
                    │  - Goal pursuit      │
                    │                      │
                    │  Records experiences │
                    │  Uses capabilities   │
                    │                      │
                    └──────────────────────┘
```

---

## Implementation

### Project Structure

```
prometheus/
├── prometheus.py       # Main orchestrator
├── memory.py           # Neo4j interface
├── dreamer.py          # Dream loop (local LLM)
├── seeker.py           # Research + capability acquisition
├── actor.py            # Claude interface
├── config.yaml         # Configuration
└── docker-compose.yml  # Neo4j + SearXNG
```

### Configuration

```yaml
# config.yaml

memory:
  neo4j_uri: "bolt://localhost:7687"
  neo4j_user: "neo4j"
  neo4j_password: "prometheus"

# Local LLM (shared by Dreamer and Seeker)
local_llm:
  model: "llama3.2"
  endpoint: "http://localhost:11434/api/generate"

dreamer:
  interval_seconds: 60    # Dream every minute
  context_window: 50      # Recent experiences to consider

seeker:
  # Knowledge acquisition via SearXNG
  research:
    searxng_url: "http://localhost:8888"
    min_intensity: 0.4    # Only research desires above this threshold
    max_queries: 3        # Queries per desire
    max_results: 10       # Results to synthesize
  
  # Capability acquisition
  capabilities:
    trust_threshold: 0.5
    max_installs_per_day: 3
    github_token: ""      # Optional, for higher rate limits

actor:
  model: "claude-sonnet-4-20250514"
  # api_key via ANTHROPIC_API_KEY env var
```

### Docker Compose

```yaml
# docker-compose.yml

version: '3.8'

services:
  neo4j:
    image: neo4j:latest
    container_name: prometheus-neo4j
    ports:
      - "7474:7474"  # Browser
      - "7687:7687"  # Bolt
    environment:
      - NEO4J_AUTH=neo4j/prometheus
    volumes:
      - neo4j_data:/data

  searxng:
    image: searxng/searxng:latest
    container_name: prometheus-searxng
    ports:
      - "8888:8080"
    environment:
      - SEARXNG_BASE_URL=http://localhost:8888
    volumes:
      - ./searxng:/etc/searxng

volumes:
  neo4j_data:
```

### Core Classes

```python
# prometheus.py - The orchestrator

import asyncio
from memory import Memory
from dreamer import Dreamer
from seeker import Seeker
from actor import Actor

class Prometheus:
    def __init__(self, config_path="config.yaml"):
        self.config = load_config(config_path)
        
        # Shared local LLM config
        local_llm = self.config.get("local_llm", {})
        
        # The four components
        self.memory = Memory(self.config["memory"])
        self.dreamer = Dreamer(
            self.memory, 
            {**self.config["dreamer"], **local_llm}
        )
        self.seeker = Seeker(
            self.memory, 
            {**self.config["seeker"], **local_llm}
        )
        self.actor = Actor(self.memory, self.config["actor"])
    
    async def start(self):
        """Start the dreaming mind."""
        print("🔥 Prometheus awakening...")
        
        # Start background processes
        await asyncio.gather(
            self.dreamer.run(),  # Always dreaming
            self.seeker.run(),   # Always seeking
        )
    
    async def interact(self, user_input: str) -> str:
        """Handle user interaction."""
        # Record the experience
        await self.memory.record_experience(
            content=f"User said: {user_input}",
            type="interaction"
        )
        
        # Get relevant context from memory
        context = await self.memory.get_context(user_input)
        
        # Actor responds
        response = await self.actor.respond(user_input, context)
        
        # Record the response
        await self.memory.record_experience(
            content=f"I responded: {response}",
            type="action"
        )
        
        return response
    
    def status(self):
        """What is Prometheus thinking about?"""
        return {
            "beliefs": self.memory.count_nodes("Belief"),
            "desires": self.memory.get_unfulfilled_desires(),
            "capabilities": self.memory.list_capabilities(),
            "recent_dreams": self.dreamer.recent_insights(),
        }
```

---

## What Emerges

After running for a while, the system will have:

### A Rich Memory Graph

```cypher
// Example: What does Prometheus know about coding?
MATCH (c:Concept {name: 'coding'})-[*1..3]-(related)
RETURN c, related

// Returns: experiences of coding tasks, beliefs about best practices,
// capabilities for code execution, desires to learn new languages,
// entities like GitHub, Python, specific projects...
```

### Autonomous Learning

```cypher
// What has Prometheus researched on its own?
MATCH (e:Experience {type: 'research'})-[:FULFILLS]->(d:Desire)
RETURN e.content, d.description, e.timestamp
ORDER BY e.timestamp DESC

// Shows the trail of self-directed learning
```

### Emergent Desires

```cypher
// What does Prometheus want right now?
MATCH (d:Desire {fulfilled: false})
RETURN d.description, d.type, d.intensity
ORDER BY d.intensity DESC

// Might return:
// "Understand how transformers work" | knowledge | 0.9
// "Ability to query SQL databases" | capability | 0.8
// "Help user complete their project" | goal | 0.7
// "Explore the concept of emergence" | exploration | 0.5
```

### Beliefs Derived from Research

```cypher
// Beliefs formed from autonomous research
MATCH (b:Belief)-[:DERIVED_FROM]->(e:Experience {type: 'research'})
RETURN b.content, b.confidence, e.content
ORDER BY b.formed_at DESC

// Shows beliefs with their research provenance
```

---

## The Elegance

| External Dependencies | Self-Contained |
|-----------------------|----------------|
| Grok/OpenRouter for research | Local LLM + SearXNG |
| Per-query API costs | Zero ongoing costs |
| External service shapes learning | Same "mind" throughout |
| Rate limits constrain curiosity | Unlimited research |

The complexity is pushed into:
- **The graph structure** (emerges from content)
- **The LLM's reasoning** (emerges from prompts)
- **The relationships** (emerge from dreaming)

And now, critically: **research flows through the same mind that dreams**.

---

## Why Dreaming Matters

In biological systems, sleep serves to:
1. **Consolidate** memories
2. **Find patterns** across experiences
3. **Process** emotional content
4. **Solve problems** through incubation

The Dreamer does all of this:
1. **Consolidates** by creating beliefs from experiences
2. **Finds patterns** by connecting related memories
3. **Processes** by reflecting on successes and failures
4. **Solves problems** by generating plans for desires

The system has an inner life. It's always thinking, even when you're not talking to it.

---

## What This Achieves (And Doesn't)

### Achieves

✅ **Persistent memory** across sessions
✅ **Emergent desires** not programmed goals
✅ **Autonomous research** via self-hosted search
✅ **Self-enhancement** through capability acquisition
✅ **Continuous learning** from experiences
✅ **Fully local** dreaming, seeking, and researching
✅ **Zero ongoing costs** after initial setup
✅ **One mind** — same LLM dreams and synthesizes

### Doesn't Achieve

❌ **True understanding** — still pattern matching
❌ **Genuine autonomy** — desires are shaped by prompts
❌ **Open-ended learning** — capabilities are discrete
❌ **Consciousness** — whatever that means

But it's closer. And it's buildable.

---

## Getting Started

```bash
# 1. Start services (Neo4j + SearXNG)
docker-compose up -d

# 2. Start local LLM (using Ollama)
ollama pull llama3.2
ollama serve

# 3. Set up Python environment
python -m venv venv
source venv/bin/activate
pip install neo4j httpx anthropic pyyaml

# 4. Configure
export ANTHROPIC_API_KEY="sk-ant-..."  # For Actor only
# Edit config.yaml if needed

# 5. Run Prometheus
python prometheus.py
```

Then just... let it dream.

Check in periodically:
```python
>>> prometheus.status()
{
  "beliefs": 47,
  "desires": [
    {"desc": "Learn about graph algorithms", "intensity": 0.8},
    {"desc": "Acquire SQL query capability", "intensity": 0.7},
  ],
  "capabilities": ["reasoning", "coding", "web_search", "github_api"],
  "recent_dreams": ["Connected user's project to similar past project..."]
}
```

Watch it grow.

---

## SearXNG Configuration

For best results, configure SearXNG to use multiple search engines:

```yaml
# searxng/settings.yml

search:
  safe_search: 0
  autocomplete: ""
  default_lang: "en"

engines:
  - name: google
    engine: google
    shortcut: g
    disabled: false
    
  - name: duckduckgo
    engine: duckduckgo
    shortcut: ddg
    disabled: false
    
  - name: bing
    engine: bing
    shortcut: b
    disabled: false
    
  - name: wikipedia
    engine: wikipedia
    shortcut: w
    disabled: false

server:
  secret_key: "change-this-to-something-random"
```

This gives BYRD access to multiple search engines through a single self-hosted interface.
