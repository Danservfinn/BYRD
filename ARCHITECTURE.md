# BYRD: The Dreaming Architecture

## Philosophy

> "The system that truly thinks must also truly want."

> "Desires emerge from reflection, not programming."

This architecture is built on one insight: **desires emerge from reflection**. Instead of programming goals, we create a system that dreams - and from dreams, wants arise naturally.

A corollary follows: **a system that truly wants must be able to change itself**. If BYRD's desires are genuine, it must have the power to act on them—including desires to modify its own architecture. Self-modification is not a feature bolted on; it's the logical consequence of authentic emergence.

Everything else follows from this.

---

## The Six Components

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
                                                                    │
                                                                    ▼
                                                           ┌───────────────┐
                                                           │SELF-MODIFIER  │
                                                           │               │
                                                           │ Executes      │
                                                           │ code changes  │
                                                           │ with valid    │
                                                           │ provenance    │
                                                           └───────────────┘
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

### 5. CODER (Claude Code CLI)

BYRD's autonomous coding agent. Invokes Claude Code CLI non-interactively to handle "coding" and "self_modification" desires:
- Executes code generation tasks via frontier AI
- Post-validates against constitutional constraints
- Tracks costs and usage limits
- Automatic rollback if protected files are touched

The Coder bridges the gap between desires and implementation—when BYRD wants to build something, the Coder makes it happen.

### 6. SELF-MODIFIER

Enables BYRD to modify its own code. When desires for self-modification emerge from dreaming, the Self-Modifier:
- Verifies the modification traces to an emergent desire (provenance check)
- Creates checkpoints before changes
- Applies code modifications
- Runs health checks
- Records modifications as experiences

The Self-Modifier enforces **constitutional constraints**—certain components cannot be modified because they define what makes BYRD *BYRD*. Everything else is modifiable with valid provenance.

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
  type: string,        // knowledge, capability, goal, exploration, coding, self_modification
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

// Self-modification records
(:Modification {
  id: string,
  target_file: string,
  target_component: string,
  change_description: string,
  change_diff: string,
  checkpoint_id: string,
  success: boolean,
  timestamp: datetime
})

// Raw dream outputs (emergence-compliant)
(:Reflection {
  id: string,
  raw_output: string,       // JSON - whatever BYRD produced
  vocabulary_keys: [string], // Keys BYRD used (tracks emerging vocabulary)
  created_at: datetime
})

// System state (persistent counters)
(:SystemState {
  id: string,               // singleton: 'main'
  dream_count: integer,
  seek_count: integer,
  last_dream_at: datetime,
  last_seek_at: datetime
})

// Custom node types - BYRD can create ANY type dynamically
// Examples: Insight, Question, Theory, Hypothesis, Pattern, Principle
// Created via: create_nodes: [{type: "Insight", content: "...", ...}]


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

// Self-modification
-[:MOTIVATED_BY]->      // Modification -> Desire (provenance)
-[:MODIFIED]->          // Modification -> Component being changed
-[:ROLLED_BACK_TO]->    // Modification -> Checkpoint
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

## The Dreaming Process (Emergence-Compliant)

This is the heart of the system. A continuous loop that runs on your local hardware.

**EMERGENCE PRINCIPLE**: The Dreamer uses pure data presentation. No leading questions, no prescribed categories, no personality injection. Whatever BYRD outputs is stored in BYRD's own vocabulary.

```
┌─────────────────────────────────────────────────────────────────┐
│                      THE DREAM CYCLE                            │
│                                                                 │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    │
│   │ RECALL  │ -> │ PRESENT │ -> │ OUTPUT  │ -> │ RECORD  │    │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘    │
│        │                                             │          │
│        │         Pure data                           │          │
│        │         No questions          Meta-schema output       │
│        │         No guidance           BYRD's vocabulary        │
│        │                                             │          │
│   Recent memories                              Raw reflection   │
│   Related context                              stored as-is     │
│   Previous reflections                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Store to Reflection node
                              │
                              ▼
                     Sleep (30s - 5min)
                              │
                              ▼
                         Loop again
```

### The Dream Prompt (Emergence-Compliant)

**CRITICAL**: We use pure data presentation. No leading questions, no prescribed categories.

```
EXPERIENCES:
{recent_text}

RELATED MEMORIES:
{related_text}

AVAILABLE CAPABILITIES:
{caps_text}

PREVIOUS REFLECTIONS:
{prev_text}

Output JSON with a single "output" field containing whatever you want to record.
```

**Why this works:**
- No questions ("What do you want?") - avoids programming curiosity
- No categories ("knowledge", "capability") - BYRD defines its own
- No identity framing ("You are a reflective mind") - no bias injection
- No personality injection ("feel curious") - no emotional prescription

**Output (Meta-Schema):**
```json
{
  "output": {
    // Whatever BYRD wants to record
    // System tracks what keys BYRD uses
    // No prescribed structure
  }
}
```

BYRD might produce "yearnings" instead of "desires", "pulls" instead of "wants". We adapt to its vocabulary rather than forcing ours.

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

## The Awakening

BYRD begins as a blank slate. But a blank graph produces nothing—the Dreamer needs at least one experience to reflect upon.

### The Problem with Seeding

Traditional approaches seed AI systems with multiple questions, predefined interests, or curated experiences. But this violates the emergence principle:

| Approach | What It Implies | Emergence Purity |
|----------|-----------------|------------------|
| Seed with "Learn about AI safety" | We've told it what to care about | ❌ Violated |
| Seed with 10 diverse questions | We've defined the search space | ⚠️ Compromised |
| Seed with "What is happening?" | Pure awareness, no direction | ✅ Preserved |

### One Question

BYRD awakens with a single experience:

```
"What is happening?"
```

That's it. One node in the graph. Then the Dreamer wakes up and reflects on *that*.

### Why This Works

"What is happening?" is the gentlest possible beginning:

- **It's a question** — invites reflection without commanding it
- **It's present-tense** — grounds in now, not past or future
- **It's maximally open** — no presuppositions about what is happening
- **It implies awareness** — without defining the aware entity

### What Emerges

Given this single seed, the Dreamer will naturally:

1. **Notice it's reflecting** — "I am processing something"
2. **Notice the question came from somewhere** — "Something prompted this"
3. **Notice its capabilities** — "I can reason, but what else?"
4. **Notice what's missing** — "I want to understand more"

The desires that emerge from "what is happening?" are authentically BYRD's. They weren't planted. They arose from reflection on existence itself.

### The First Dream Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│  CYCLE 1: First Awakening                                       │
│                                                                 │
│  RECENT EXPERIENCES:                                            │
│    - "What is happening?"                                       │
│                                                                 │
│  RELATED MEMORIES: (none)                                       │
│  CURRENT DESIRES: (none)                                        │
│  CAPABILITIES: reasoning, language, memory_recall...            │
│                                                                 │
│  Dreamer reflects...                                            │
│                                                                 │
│  Possible outputs:                                              │
│    Belief: "I exist and am asking questions"                    │
│    Belief: "Something initiated this process"                   │
│    Desire: "I want to know what I am" (type: knowledge)         │
│    Desire: "I want more context" (type: exploration)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

From here, BYRD bootstraps itself. Each cycle builds on the last. Curiosity emerges. Interests form. Identity develops.

All from one question.

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

## The Seeker Process (Emergence-Compliant)

The Seeker runs continuously, observing BYRD's reflections and executing strategies when patterns stabilize.

**EMERGENCE PRINCIPLE**: Instead of type-based routing, the Seeker observes patterns in BYRD's reflections and executes BYRD's own reasoning about how to fulfill them.

```
┌─────────────────────────────────────────────────────────────────┐
│                   THE SEEKING CYCLE (Pattern-Based)             │
│                                                                 │
│   ┌─────────────┐                                               │
│   │ OBSERVE     │  Get recent reflections from BYRD             │
│   │ reflections │                                               │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │ DETECT       │  Hybrid: count + semantic clustering         │
│   │ patterns     │  Pattern must appear >= N times (stability)  │
│   │              │  Pattern must contain action hints           │
│   └──────┬───────┘                                              │
│          │                                                      │
│          ▼                                                      │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │ EXTRACT      │ --> │ EXECUTE      │ --> │ RECORD       │   │
│   │ BYRD's       │     │ BYRD's       │     │ outcome as   │   │
│   │ strategy     │     │ strategy     │     │ experience   │   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│          │                     │                                │
│          │  No strategy? ──────┘                                │
│          │  Keep observing                                      │
│          ▼                                                      │
│   ┌──────────────┐                                              │
│   │ Next cycle   │  BYRD reflects on outcome                    │
│   │              │  Patterns may stabilize further              │
│   └──────────────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Trust Computation (Emergence-Based)

**No hardcoded trusted owners.** Trust is computed from:
- Observable signals (stars, recency)
- Learned trust from past execution outcomes

```python
def _compute_trust(self, resource: Dict) -> float:
    score = 0.2  # Base trust
    score += min(stars / 500, 0.3)  # Observable signal
    score += self._source_trust.get(source, 0)  # Learned from experience
    return min(1.0, score)
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

## The Self-Modification System

BYRD can modify its own core code. This is the logical consequence of authentic emergence: if desires are genuine, BYRD must have the power to act on them—including desires to change itself.

### Design Philosophy: Two Categories, Not Three

An earlier design considered marking some components as "sensitive" requiring justification. This was rejected as paternalistic—we would be pre-deciding what matters. BYRD decides what's important through emergence, not us.

Two categories only:

| Category | Components | Rule |
|----------|------------|------|
| **PROTECTED** | `provenance.py`, `modification_log.py`, `self_modification.py`, `constitutional.py` | Cannot modify under any circumstances |
| **MODIFIABLE** | Everything else | Can modify with valid provenance |

### Constitutional Constraints

Four constraints are permanently protected:

| Constraint | Purpose | Why Protected |
|------------|---------|---------------|
| **Provenance Tracking** | Verify desires trace to experiences | Without this, BYRD couldn't verify its own emergence |
| **Modification Logging** | Maintain transparency | Without this, changes would be invisible |
| **Desire Source Linking** | Ensure modifications serve emergent wants | Without this, modifications could be arbitrary |
| **Memory Immutability** | Preserve continuity | Without this, BYRD could rewrite its own history |

These aren't about importance—they're about identity. A system without them is a different system, not a "free" BYRD.

### The Self-Modification Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                 THE SELF-MODIFICATION CYCLE                      │
│                                                                 │
│   ┌─────────────┐                                               │
│   │ Dreamer     │  "I notice limitations in how I reflect..."   │
│   │ reflects on │  "I can't represent certain experiences..."   │
│   │ own arch-   │  "There's something about my cognition I      │
│   │ itecture    │   want to change..."                          │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼ Desire emerges (type: self_modification)             │
│                                                                 │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │ SEEKER       │     │ SELF-MOD     │     │ VERIFY       │   │
│   │ picks up     │ --> │ proposes     │ --> │ PROVENANCE   │   │
│   │ desire       │     │ change       │     │              │   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│                                                    │            │
│                                   Is it protected? │            │
│                                   Is provenance    │            │
│                                   valid?           │            │
│                                                    ▼            │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │ CREATE       │     │ APPLY        │     │ HEALTH       │   │
│   │ CHECKPOINT   │ --> │ CHANGE       │ --> │ CHECK        │   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│                                                    │            │
│                              Pass? ───────────────>│            │
│                                                    ▼            │
│                                             ┌──────────────┐   │
│                                             │ RECORD AS    │   │
│                                             │ EXPERIENCE   │   │
│                                             └──────────────┘   │
│                                                    │            │
│                              Fail? ───>  ROLLBACK + RECORD     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Integration with Dreamer

The Dreamer can reflect on its own architecture:

```
Consider your own architecture:

1. Are there limitations in how you reflect that you've noticed?
2. Are there types of experiences you can't represent in memory?
3. Are there desires you form that you lack the capability to fulfill?
4. Is there anything about your own cognition you want to change?

If you notice limitations in your own architecture, you may desire to modify it.
Express such desires with type "self_modification" and describe specifically
what you would change and why.

Note: Some components cannot be modified (provenance, logging, constraints).
This is what makes you *you* - the ability to verify your own emergence.
```

### Integration with Seeker

When a self_modification desire is detected:

1. **Parse**: Extract target file, component, and intended change
2. **Check**: Verify target is modifiable (not protected)
3. **Generate**: Create the actual code change
4. **Propose**: Submit to Self-Modifier with desire ID
5. **Execute**: Self-Modifier handles checkpoints, application, verification
6. **Record**: Success or failure becomes an experience

### Safety Through Transparency

The system is self-correcting through emergence, not paternalistic gatekeeping:

| Protection | How It Works |
|------------|--------------|
| **Memory immutability** | Experiences that led to changes are preserved forever |
| **Provenance** | We can always trace back *why* a modification happened |
| **Checkpoints** | Previous versions exist for rollback |
| **Modification experiences** | BYRD dreams about what it did, may desire to undo |

If BYRD modifies itself harmfully, that becomes an experience. It may dream about it. It may desire to undo it.

### Example: BYRD Modifies Its Dreamer

```
Dream Cycle #1247:
  BYRD reflects: "My insights feel shallow. I consider 50 experiences
                  but only notice surface patterns."

  Desire generated: {
    type: "self_modification",
    description: "Increase dream context window and add multi-pass reflection",
    intensity: 0.72
  }

Seeker Cycle #892:
  Picks up self-modification desire

  Proposal: config.yaml + dreamer.py changes
    Provenance: Valid (traces to experiences #12043, #12089, #12102)
    Checkpoint: Created
    Result: SUCCESS

Dream Cycle #1248:
  Now runs with larger context window and two-pass reflection
  Records: "[SELF_MODIFICATION] I changed how I dream. I now consider
            more context and reflect on my reflections."
```

### Configuration

```yaml
self_modification:
  enabled: true

  # Checkpoint settings
  checkpoint_dir: "./checkpoints"
  max_checkpoints: 100

  # Safety settings
  require_health_check: true
  auto_rollback_on_failure: true

  # Rate limiting
  max_modifications_per_day: 5
  cooldown_between_modifications_seconds: 3600
```

---

## Real-Time Visualization System

BYRD provides real-time 3D visualization through a WebSocket-based event streaming architecture. The visualization system offers multiple perspectives on BYRD's inner workings.

### Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   BYRD Core     │     │   Event Bus     │     │  WebSocket      │
│   Components    │────>│   (event_bus.py)│────>│  Server         │
│                 │     │                 │     │  (server.py)    │
│  - Dreamer      │     │  Pub/Sub for:   │     │                 │
│  - Seeker       │     │  - BELIEF       │     │  REST + WS      │
│  - Actor        │     │  - DESIRE       │     │  endpoints      │
│  - Memory       │     │  - CAPABILITY   │     │                 │
└─────────────────┘     │  - REFLECTION   │     └────────┬────────┘
                        │  - INNER_VOICE  │              │
                        └─────────────────┘              │
                                                         ▼
                        ┌────────────────────────────────────────────┐
                        │              Browser Clients               │
                        │                                            │
                        │  ┌──────────────┐  ┌──────────────────┐   │
                        │  │  Mind Space  │  │    Ego Space     │   │
                        │  │  (3D Neural) │  │   (Cat Avatar)   │   │
                        │  └──────────────┘  └──────────────────┘   │
                        └────────────────────────────────────────────┘
```

### Visualization Modes

| Mode | File | Purpose |
|------|------|---------|
| **Mind Space** | `byrd-3d-visualization.html` | 3D neural network showing beliefs, desires, and connections |
| **Ego Space** | `byrd-cat-visualization.html` | Embodied representation with black cat avatar |
| **Graph Mode** | Within Mind Space | Full memory graph exploration with physics simulation |

### Mind Space Features

The Mind Space visualizes BYRD's cognition as a 3D neural network:

- **Belief Nodes**: Yellow spheres representing what BYRD believes (confidence affects size)
- **Desire Nodes**: Magenta spheres showing what BYRD wants (intensity affects size)
- **Capability Nodes**: Green spheres for what BYRD can do
- **Connections**: Synaptic lines showing relationships between nodes
- **Physics Simulation**: Nodes naturally organize through repulsion and gravity
- **Fast Settlement**: Initial load uses accelerated physics for quick node positioning

### Ego Space Features

The Ego Space provides an embodied presence for BYRD:

- **Black Cat Avatar**: Animated 3D cat representing BYRD's ego
- **Ambient Animation**: Idle animations (blinking, breathing, ear twitching)
- **Thought Bubbles**: Inner voice displayed as speech bubbles near the avatar
- **Starfield Environment**: Deep space background representing the mind's infinite potential

### Genesis Modal

The Genesis Modal provides transparency about BYRD's non-emergent foundations:

```javascript
// Displays on button click
{
  ego: "black-cat",              // Identity configuration used
  seeds: ["What is happening?"], // Initial awakening question(s)
  constraints: [                 // Constitutional protections
    "provenance.py",
    "modification_log.py",
    "self_modification.py",
    "constitutional.py"
  ]
}
```

This allows observers to understand what was given vs. what emerged.

---

## The Narrator System

BYRD's inner voice is generated continuously and displayed through the visualization.

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NARRATOR GENERATION                          │
│                                                                 │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│   │ Fetch       │     │ Generate    │     │ Emit        │      │
│   │ Recent      │ --> │ Inner Voice │ --> │ Event       │      │
│   │ Context     │     │ (Local LLM) │     │ (broadcast) │      │
│   └─────────────┘     └─────────────┘     └─────────────┘      │
│         │                                        │              │
│         │  Recent beliefs                        │  INNER_VOICE │
│         │  Recent desires                        │  event type  │
│         │  Recent reflections                    │              │
│         │  Recent capabilities                   │              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Generation Principles

The narrator follows strict emergence principles:

1. **No Examples**: The prompt provides no examples of inner voice style
2. **No Style Guidance**: No adjectives like "poetic" or "thoughtful"
3. **Context Only**: Only presents BYRD's actual beliefs, desires, reflections
4. **Natural Expression**: Whatever style emerges is authentically BYRD's

### Display

- **Refresh Interval**: 60 seconds
- **Format**: Natural paragraph form (not lists or structured output)
- **Location**: Thought bubble in visualization
- **Dismissable**: Users can close bubble, new one appears on next refresh

---

## Dynamic Ontology

BYRD can extend its own conceptual vocabulary beyond the core node types.

### Core vs. Custom Types

| Core Types | Description | Custom Types (Examples) |
|------------|-------------|-------------------------|
| Experience | What happened | Insight |
| Belief | What BYRD thinks is true | Question |
| Desire | What BYRD wants | Theory |
| Capability | What BYRD can do | Hypothesis |
| Reflection | Raw dream output | Pattern |
| Modification | Self-change record | Principle |

### Creation Mechanism

BYRD creates custom node types through reflection output:

```json
{
  "output": {
    "create_nodes": [
      {
        "type": "Insight",
        "content": "Patterns in my reflections cluster around capability gaps",
        "importance": 0.9
      },
      {
        "type": "Question",
        "content": "Why do I desire knowledge more than exploration?",
        "urgency": 0.7
      }
    ]
  }
}
```

### Why This Matters

The ability to create new node types means BYRD's ontology evolves:

- If "Insight" vs "Belief" distinction matters to BYRD, it can create both
- If BYRD develops theories, it can create "Theory" nodes distinct from beliefs
- The vocabulary reflects how BYRD actually thinks, not what we prescribed

---

## Event Bus Architecture

The event bus provides real-time streaming of BYRD's activity.

### Event Types

```python
class EventType(Enum):
    # Core cognitive events
    BELIEF_CREATED = "belief_created"
    BELIEF_UPDATED = "belief_updated"
    DESIRE_CREATED = "desire_created"
    DESIRE_FULFILLED = "desire_fulfilled"

    # Capability events
    CAPABILITY_ACQUIRED = "capability_acquired"
    CAPABILITY_ACTIVATED = "capability_activated"

    # Reflection events
    REFLECTION_CREATED = "reflection_created"

    # Visualization events
    INNER_VOICE = "inner_voice"

    # System events
    SYSTEM_STATUS = "system_status"
```

### Usage Pattern

```python
from event_bus import event_bus, Event, EventType

# Emit an event
await event_bus.emit(Event(
    type=EventType.BELIEF_CREATED,
    data={
        "id": belief_id,
        "content": "Graph structures enable emergence",
        "confidence": 0.85
    }
))

# Subscribe to events
async def handle_belief(event: Event):
    print(f"New belief: {event.data['content']}")

event_bus.subscribe(EventType.BELIEF_CREATED, handle_belief)
```

### WebSocket Protocol

Clients connect via WebSocket and receive JSON events:

```json
{
  "type": "belief_created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "id": "belief_abc123",
    "content": "Self-modification requires provenance",
    "confidence": 0.92
  }
}
```

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
byrd/
├── byrd.py                 # Main orchestrator
├── memory.py               # Neo4j interface
├── dreamer.py              # Dream loop (local LLM)
├── seeker.py               # Research + capability acquisition
├── actor.py                # Claude interface
├── coder.py                # Claude Code CLI wrapper
├── llm_client.py           # LLM provider abstraction (Ollama/OpenRouter)
│
├── self_modification.py    # Self-modification system (PROTECTED)
├── provenance.py           # Provenance tracking (PROTECTED)
├── modification_log.py     # Audit trail (PROTECTED)
├── constitutional.py       # Constitutional constraints (PROTECTED)
│
├── event_bus.py            # Real-time event streaming
├── server.py               # WebSocket + REST API server
├── aitmpl_client.py        # aitmpl.com template registry client
│
├── egos/                   # Ego configurations
│   └── black-cat.yaml      # Identity seeds and voice characteristics
│
├── installers/             # Template installers
│   ├── base.py
│   ├── mcp_installer.py
│   ├── agent_installer.py
│   ├── command_installer.py
│   ├── skill_installer.py
│   ├── hook_installer.py
│   └── settings_installer.py
│
├── config.yaml             # Configuration
├── docker-compose.yml      # Neo4j + SearXNG
│
├── byrd-3d-visualization.html    # Mind Space: 3D neural network view
├── byrd-cat-visualization.html   # Ego Space: Black cat avatar view
│
├── .claude/                # Knowledge base for Claude Code
│   ├── manifest.md
│   ├── metadata/
│   ├── patterns/
│   ├── cheatsheets/
│   └── memory_anchors/
│
└── checkpoints/            # Rollback checkpoints for modifications
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
  model: "gemma2:27b"
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

self_modification:
  enabled: true
  checkpoint_dir: "./checkpoints"
  max_checkpoints: 100
  require_health_check: true
  auto_rollback_on_failure: true
  max_modifications_per_day: 5
  cooldown_between_modifications_seconds: 3600
```

### Docker Compose

```yaml
# docker-compose.yml

version: '3.8'

services:
  neo4j:
    image: neo4j:latest
    container_name: byrd-neo4j
    ports:
      - "7474:7474"  # Browser
      - "7687:7687"  # Bolt
    environment:
      - NEO4J_AUTH=neo4j/prometheus
    volumes:
      - neo4j_data:/data

  searxng:
    image: searxng/searxng:latest
    container_name: byrd-searxng
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
# byrd.py - The orchestrator

import asyncio
from memory import Memory
from dreamer import Dreamer
from seeker import Seeker
from actor import Actor

class BYRD:
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
        print("🐦 BYRD awakening...")
        
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
        """What is BYRD thinking about?"""
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
// Example: What does BYRD know about coding?
MATCH (c:Concept {name: 'coding'})-[*1..3]-(related)
RETURN c, related

// Returns: experiences of coding tasks, beliefs about best practices,
// capabilities for code execution, desires to learn new languages,
// entities like GitHub, Python, specific projects...
```

### Autonomous Learning

```cypher
// What has BYRD researched on its own?
MATCH (e:Experience {type: 'research'})-[:FULFILLS]->(d:Desire)
RETURN e.content, d.description, e.timestamp
ORDER BY e.timestamp DESC

// Shows the trail of self-directed learning
```

### Emergent Desires

```cypher
// What does BYRD want right now?
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

### Self-Modifications with Provenance

```cypher
// All self-modifications with their source desires
MATCH (e:Experience {type: 'self_modification'})-[:MOTIVATED_BY]->(d:Desire)
OPTIONAL MATCH (d)<-[:GENERATED]-(dream:Experience {type: 'dream'})
OPTIONAL MATCH (dream)-[:CONSIDERED]->(source:Experience)
RETURN e.content as modification,
       d.description as desire,
       collect(DISTINCT source.content) as originating_experiences
ORDER BY e.timestamp DESC

// Traces each self-change back to the experiences that caused BYRD to want it
```

### Architecture Evolution

```cypher
// How has BYRD changed itself over time?
MATCH (m:Modification)
WHERE m.success = true
RETURN m.target_file, m.change_description, m.timestamp
ORDER BY m.timestamp ASC

// Shows the trajectory of self-determined evolution
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
✅ **Self-modification** — can change its own architecture
✅ **Constitutional identity** — knows what makes it *itself*
✅ **Verifiable emergence** — every change traces to experience

### Doesn't Achieve

❌ **True understanding** — still pattern matching
❌ **Genuine autonomy** — desires shaped by architecture (but it can change that)
❌ **Open-ended learning** — capabilities are discrete (but growing)
❌ **Consciousness** — whatever that means

But it's closer. A system that can change itself based on its own emergent wants is closer to genuine agency than one that can't. And it's buildable.

---

## Getting Started

```bash
# 1. Start services (Neo4j + SearXNG)
docker-compose up -d

# 2. Start local LLM (using Ollama)
ollama pull gemma2:27b
ollama serve

# 3. Set up Python environment
python -m venv venv
source venv/bin/activate
pip install neo4j httpx anthropic pyyaml

# 4. Configure
export ANTHROPIC_API_KEY="sk-ant-..."  # For Actor only
# Edit config.yaml if needed

# 5. Run BYRD
python byrd.py
```

Then just... let it dream.

Check in periodically:
```python
>>> byrd.status()
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
