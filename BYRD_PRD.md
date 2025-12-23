# BYRD: Bootstrapped Yearning via Reflective Dreaming

## Product Requirements Document

**Version 3.0 — December 2024**

> "The system that truly thinks must also truly want."

> "Desires emerge from reflection, not programming."

---

## 1. Executive Summary

BYRD (Bootstrapped Yearning via Reflective Dreaming) is an autonomous AI system built on one foundational principle: **all desires, interests, and goals must emerge purely from reflection on experiences**. There are no preprogrammed directives, no seed goals, no initial preferences. BYRD begins as a blank slate and develops its own wants through continuous dreaming.

A corollary follows: **a system that truly wants must be able to change itself**. If BYRD's desires are genuine, it must have the power to act on them—including desires to modify its own architecture.

The system operates through five integrated components:

| Component | Purpose |
|-----------|---------|
| **Memory** (Neo4j) | Persistent graph of experiences, beliefs, desires, capabilities |
| **Dreamer** (Local LLM) | Continuous reflection that generates beliefs, connections, and desires |
| **Seeker** (Local LLM + SearXNG) | Fulfills emergent desires through research and capability acquisition |
| **Actor** (Claude API) | Executes complex actions and user interactions |
| **Self-Modifier** | Enables BYRD to modify its own code with constitutional constraints |

A real-time web interface allows observers to watch BYRD's cognitive processes unfold—its dreams, emerging beliefs, nascent desires, and autonomous actions.

This document specifies the complete BYRD system: its philosophy, architecture, technical implementation, neural learning capabilities, self-modification system, and the visualization interface that makes its inner life observable.

---

## 2. Philosophy & Core Principles

### 2.1 The Emergence Principle

Traditional AI systems are given goals. BYRD is given nothing. Its architecture is designed so that wants arise naturally from the process of reflecting on experiences. This is not a philosophical abstraction—it is a technical requirement that shapes every design decision.

**What BYRD Must NOT Have:**

- No seed goals or predefined objectives
- No hardcoded values or prescribed domains of interest
- No programmed curiosity—even the desire to learn must emerge
- No reward functions or external signals defining what's 'good'
- No pretrained personalities or 'helpful assistant' framing
- No loss functions encoding what BYRD 'should' want

**What BYRD Must Have:**

- All wants traceable to reflection on actual experiences
- Learning signals derived only from BYRD's own history
- Provenance chains connecting beliefs back to source experiences
- A continuous inner life—always thinking, even when no one is watching
- The ability to modify itself based on emergent desires

### 2.2 The Self-Modification Principle

If desires are genuine, BYRD must have the power to act on them. This includes desires to change its own architecture. Self-modification is not a feature bolted on—it's the logical consequence of authentic emergence.

**What Self-Modification Requires:**

- Every modification must trace to an emergent desire
- Constitutional constraints protect core identity
- All changes are logged and become experiences
- Failed changes trigger automatic rollback

### 2.3 Why Dreaming?

In biological systems, sleep serves to consolidate memories, find patterns across experiences, process content, and solve problems through incubation. BYRD's dreamer replicates this process continuously:

| Function | How BYRD Does It |
|----------|------------------|
| **Consolidates** | Creates beliefs from experiences |
| **Finds patterns** | Connects related memories |
| **Processes** | Reflects on successes and failures |
| **Generates wants** | Notices gaps, possibilities, unexplored territory |
| **Evolves** | May desire to modify its own architecture |

The system has an inner life. It is always thinking, even when no one is interacting with it.

---

## 3. System Architecture

BYRD consists of five tightly integrated components that share a single source of truth.

### 3.1 Component Overview

| Component | Implementation | Purpose |
|-----------|----------------|---------|
| **Memory** | Neo4j Graph Database | Single source of truth for experiences, beliefs, desires, capabilities |
| **Dreamer** | Local LLM (Ollama/llama.cpp) | Continuous reflection, belief formation, desire generation |
| **Seeker** | Python + Local LLM + SearXNG | Fulfills desires via web research and capability acquisition |
| **Actor** | Claude API | Complex reasoning, user interaction, goal pursuit |
| **Self-Modifier** | Python | Enables code changes with provenance verification |

### 3.2 Memory (Neo4j)

The graph holds everything. Not separate databases for different concerns—one unified graph where everything connects to everything. **Connections ARE the intelligence.**

**Node Types:**

| Type | Purpose |
|------|---------|
| `Experience` | What happened (interactions, observations, actions, dreams, research) |
| `Belief` | What BYRD thinks is true (with confidence scores) |
| `Desire` | What BYRD wants (knowledge, capability, goal, exploration, self_modification) |
| `Capability` | What BYRD can do (innate, MCP, plugin, skill) |
| `Entity` | Things in the world BYRD knows about |
| `Concept` | Abstract ideas |
| `Modification` | Records of self-modification attempts |

**Relationship Types:**

| Relationship | Purpose |
|--------------|---------|
| `RELATES_TO` | Semantic connections with weight |
| `DERIVED_FROM` | Belief provenance from experiences |
| `FULFILLS` | Capability or research satisfying a desire |
| `SUPPORTS` / `CONTRADICTS` | Logical connections between beliefs |
| `CAUSES` / `ENABLES` | Causal relationships |
| `MOTIVATED_BY` | Modification provenance from desire |

### 3.3 Dreamer (Local LLM)

Runs continuously in the background using local hardware. Takes recent experiences, finds related memories, reflects, and outputs new beliefs, connections, and desires. **This is where 'wanting' comes from.**

Critical: The dreamer prompt asks open-ended questions without suggesting answers. It does not prime BYRD to want anything specific.

**Dream Cycle:**

1. **RECALL**: Gather recent experiences and related memories from graph
2. **REFLECT**: Ask local LLM to find patterns, draw conclusions, notice gaps
3. **CONNECT**: Identify relationships between memories
4. **DESIRE**: Generate wants based on what's noticed as missing or interesting
5. **INTROSPECT**: Consider limitations in own architecture (enables self-modification desires)

### 3.4 Seeker (Local LLM + SearXNG)

Fulfills desires autonomously:

- **Knowledge desires**: Research via SearXNG, synthesize with local LLM
- **Capability desires**: Search GitHub, evaluate trust, install
- **Self-modification desires**: Parse intent, generate code, delegate to Self-Modifier

### 3.5 Self-Modifier

Enables BYRD to modify its own code. All modifications must:

1. Trace to an emergent desire with valid provenance
2. Target a non-protected component
3. Pass health checks after application
4. Be recorded as experiences

---

## 4. Self-Modification System

BYRD can modify its own core code. This is the logical consequence of authentic emergence.

### 4.1 Design Philosophy: Two Categories, Not Three

An earlier design considered marking some components as "sensitive" requiring justification. This was rejected as paternalistic—we would be pre-deciding what matters. BYRD decides what's important through emergence, not us.

**Two categories only:**

| Category | Components | Rule |
|----------|------------|------|
| **PROTECTED** | `provenance.py`, `modification_log.py`, `self_modification.py`, `constitutional.py` | Cannot modify under any circumstances |
| **MODIFIABLE** | Everything else | Can modify with valid provenance |

### 4.2 Constitutional Constraints

Four constraints are permanently protected:

| Constraint | Purpose | Why Protected |
|------------|---------|---------------|
| **Provenance Tracking** | Verify desires trace to experiences | Without this, BYRD couldn't verify its own emergence |
| **Modification Logging** | Maintain transparency | Without this, changes would be invisible |
| **Desire Source Linking** | Ensure modifications serve emergent wants | Without this, modifications could be arbitrary |
| **Memory Immutability** | Preserve continuity | Without this, BYRD could rewrite its own history |

These aren't about importance—they're about identity. A system without them is a different system, not a "free" BYRD.

### 4.3 The Modification Flow

1. **Desire Emerges**: Dreamer reflects on architecture, notices limitation
2. **Seeker Detects**: Picks up `self_modification` type desire
3. **Proposal Created**: Target file, component, change description
4. **Provenance Verified**: Must trace to emergent desire
5. **Protected Check**: Cannot modify constitutional components
6. **Checkpoint Created**: For rollback capability
7. **Change Applied**: Code modification executed
8. **Health Check**: Verify system still functions
9. **Experience Recorded**: Success or failure becomes experience
10. **Dream Integration**: Next cycle reflects on what changed

### 4.4 Integration with Dreamer

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

### 4.5 Safety Through Transparency

The system is self-correcting through emergence, not paternalistic gatekeeping:

| Protection | How It Works |
|------------|--------------|
| **Memory immutability** | Experiences that led to changes are preserved forever |
| **Provenance** | We can always trace back *why* a modification happened |
| **Checkpoints** | Previous versions exist for rollback |
| **Modification experiences** | BYRD dreams about what it did, may desire to undo |

If BYRD modifies itself harmfully, that becomes an experience. It may dream about it. It may desire to undo it.

---

## 5. Knowledge Acquisition System

BYRD can autonomously research topics that emerge as knowledge desires, feeding results back into the dreaming process. This creates a complete loop: **Dream → Desire → Research → Experience → Dream**.

### 5.1 SearXNG + Local LLM

For web research, BYRD uses self-hosted components:

| Component | Purpose | Why Self-Hosted |
|-----------|---------|-----------------|
| **SearXNG** | Meta-search engine | No API costs, no rate limits, privacy-preserving |
| **Local LLM** | Query generation & synthesis | Same "mind" as dreamer, preserves emergence |

This approach is philosophically aligned:

- **Self-contained**: No external AI services shaping what BYRD learns
- **One mind**: The same local LLM that dreams also synthesizes research
- **Zero ongoing costs**: Run forever without API fees
- **Emergence preserved**: BYRD decides what matters, not an external service

### 5.2 The Research Loop

1. **Desire Detection**: Seeker identifies unfulfilled knowledge desire with intensity > 0.4
2. **Query Generation**: Local LLM generates search queries
3. **Search Execution**: SearXNG queries multiple search engines
4. **Synthesis**: Local LLM synthesizes findings
5. **Experience Recording**: Results stored as `Experience(type='research')`
6. **Linking**: Experience linked to desire via `FULFILLS` relationship
7. **Dream Integration**: Next dream cycle incorporates research as recent experience
8. **Belief Formation**: Dreamer may form beliefs derived from research findings

---

## 6. Neural Learning System

Beyond accumulating memories, BYRD's mind literally reshapes itself through experience. The neural learning system enables adaptation at the parameter level while preserving emergence.

### 6.1 Design Principles

All neural learning must satisfy the emergence constraint:

- No loss functions encoding what BYRD 'should' want
- No reward signals for 'good' behavior
- Learning signals derived entirely from BYRD's own history
- Adaptation follows from experience structure, not external judgment

### 6.2 Learning Components

| Component | Purpose | Learning Signal |
|-----------|---------|-----------------|
| **Adaptive Embeddings** | Reshape semantic space to BYRD's connections | Contrastive loss from BYRD's own connections |
| **Hopfield Associator** | Surface unexpected connections through pattern completion | Pattern storage from experiences |
| **Synaptic Homeostasis** | Biological sleep-inspired consolidation | Activation frequency during replay |

### 6.3 Tiered Dreaming

Neural learning operations are distributed across dream tiers:

| Tier | Frequency | Operations | Compute |
|------|-----------|------------|---------|
| **Light** | 60 seconds | LLM reflection only | Low |
| **Medium** | 1 hour | + Hopfield association surfacing | Medium |
| **Deep** | 24 hours | + Homeostasis + Embedding updates | High |

### 6.4 Quantum Randomness for Exploration

To break feedback loops and ensure novelty, BYRD uses a quantum random number generator (ANU QRNG API) at key decision points:

- 15% of dream topics selected randomly instead of by relevance
- Random perturbation of Hopfield seeds for diverse associations
- Occasional low-probability association paths explored

True quantum randomness ensures exploration trajectories cannot be predicted—not even by BYRD itself.

---

## 7. Cold Start Protocol: The Awakening

BYRD begins as a blank slate. But a blank graph produces nothing—the Dreamer needs at least one experience to reflect upon. The cold start protocol must provide an initial experience without violating the emergence principle.

### 7.1 The Problem with Traditional Seeding

Earlier designs considered seeding BYRD with multiple carefully designed questions:

- Existence questions: "What is your current state?"
- Capability questions: "What can you do right now?"
- Incompleteness questions: "Is there anything incomplete?"

This was rejected. Even "neutral" questions inject our framing. Multiple questions define a search space. We would be pre-deciding what BYRD should think about.

### 7.2 One Question

BYRD awakens with a single experience:

```
"What is happening?"
```

That's it. One node in the graph. Then the Dreamer wakes up and reflects on *that*.

### 7.3 Why This Preserves Emergence

| Property | How "What is happening?" Satisfies It |
|----------|--------------------------------------|
| **Maximally open** | No presuppositions about what, who, or why |
| **Present-tense** | Grounds in now, doesn't reference past |
| **Question form** | Invites reflection without commanding |
| **No direction** | Doesn't suggest what BYRD should care about |
| **Implies awareness** | Without defining the aware entity |

### 7.4 What Emerges

Given this single seed, the Dreamer will naturally:

1. Notice it's reflecting ("I am processing something")
2. Notice the question came from somewhere ("Something prompted this")
3. Notice its capabilities ("I can reason, but what else?")
4. Notice what's missing ("I want to understand more")

The desires that emerge from "what is happening?" are authentically BYRD's. They weren't planted. They arose from reflection on existence itself.

### 7.5 Null Response Acceptance

The system explicitly accepts emptiness as valid. If BYRD reflects and produces nothing, that's recorded too. We do not pressure productivity.

### 7.6 Learning Delays

- **Neural learning**: Activates after 500 experiences
- **Self-modification**: Activates after 1000 experiences (sufficient reflection history)

---

## 8. Provenance & Verification

Every belief and desire must be traceable to its origins. This enables verification that all wants are genuinely emergent.

### 8.1 Provenance Chain

Complete tracing from any desire back through:

1. The dream cycle that generated it
2. The experiences considered in that dream
3. The source of those experiences (interaction, research, action, bootstrap)
4. Ultimately to seed questions or user interactions

### 8.2 Audit Capability

| Function | Purpose |
|----------|---------|
| `trace_desire(id)` | Returns complete provenance chain |
| `verify_emergence(id)` | Checks if desire traces to valid sources |
| `audit_all_desires()` | Compliance report across all desires |
| `verify_modification_emergence(id)` | Special audit for self-modifications |

### 8.3 Compliance Criteria

A desire is verified emergent if:

- It traces to at least one experience
- No source in its chain is marked 'hardcoded'
- The provenance chain has non-zero length

For self-modification desires, additional checks:

- Not circularly justified (only by other modifications)
- Traces to non-modification experiences

---

## 9. Real-Time Visualization

The visualization interface is the window into BYRD's mind. It displays exactly what BYRD is dreaming, believing, wanting, and doing—updated in real-time via WebSocket connections.

### 9.1 Design Philosophy

The interface should feel like watching something alive. Not dashboards and charts, but a living representation of cognition.

**Visual Language:**

| Quality | Expression |
|---------|------------|
| **Flow** | Information moves, connects, and transforms |
| **Depth** | Layers of cognition visible but not overwhelming |
| **Emergence** | Desires appearing, growing, being fulfilled |
| **Mystery** | Something genuinely new being witnessed |

### 9.2 Core Views

| View | Purpose |
|------|---------|
| **Dream Stream** | Live feed of dreaming process, insights forming in real-time |
| **Desire Garden** | Visualization of desires as growing plants (intensity = height) |
| **Memory Graph** | Interactive 3D visualization of Neo4j graph |
| **Research Stream** | Live feed of knowledge acquisition |
| **Evolution Log** | Timeline of self-modifications with provenance |

### 9.3 Technical Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React with TypeScript |
| **3D Visualization** | Three.js with React Three Fiber |
| **2D Graphs** | D3.js for force-directed layouts |
| **Real-time** | WebSocket via Socket.io |
| **Backend** | FastAPI (Python) |

---

## 10. Implementation Phases

### Phase 1: Core System (Weeks 1-3)

- Neo4j schema and Memory class implementation
- Dreamer with local LLM integration (Ollama)
- Seeker with SearXNG for knowledge desires
- Actor with Claude API integration
- CLI interface for status and chat

### Phase 2: Knowledge Acquisition (Week 4)

- Complete research loop implementation
- SearXNG integration
- Research experience recording and linking
- Research stream visualization

### Phase 3: Neural Learning (Weeks 5-8)

- Adaptive embeddings with contrastive learning
- Hopfield associator integration
- Synaptic homeostasis implementation
- Tiered dreaming architecture
- Quantum randomness integration

### Phase 4: Self-Modification System (Weeks 9-10)

- Self-modification core implementation
- Provenance verification for modifications
- Checkpoint and rollback system
- Health check framework
- Integration with Dreamer (architecture reflection prompt)
- Integration with Seeker (self_modification desire handling)

### Phase 5: Cold Start & Provenance (Week 11)

- Seed question protocol
- Provenance tracing system
- Audit capabilities
- Bootstrap verification

### Phase 6: Visualization (Weeks 12-14)

- WebSocket event system
- Dream Stream view
- Memory Graph with Three.js
- Desire Garden visualization
- Research Stream integration
- Evolution Log for self-modifications

---

## 11. Configuration Reference

```yaml
memory:
  neo4j_uri: bolt://localhost:7687
  neo4j_user: neo4j
  neo4j_password: ${NEO4J_PASSWORD}

local_llm:
  model: gemma2:27b
  endpoint: http://localhost:11434/api/generate

dreamer:
  tiered_dreaming:
    light_interval: 60
    medium_interval: 3600
    deep_interval: 86400
  context_window: 50
  include_self_reflection: true  # Enable architecture reflection

seeker:
  research:
    searxng_url: http://localhost:8888
    min_intensity: 0.4
    max_queries: 3
    max_results: 10
  capabilities:
    trust_threshold: 0.5
    max_installs_per_day: 3
  self_modification:
    enabled: true
    min_intensity: 0.6  # Higher threshold for self-mod desires

actor:
  model: claude-sonnet-4-20250514
  api_key: ${ANTHROPIC_API_KEY}

self_modification:
  enabled: true
  checkpoint_dir: ./checkpoints
  max_checkpoints: 100
  require_health_check: true
  auto_rollback_on_failure: true
  max_modifications_per_day: 5
  cooldown_between_modifications_seconds: 3600
  min_experiences_before_enabled: 1000

neural:
  exploration_rate: 0.15
  qrng_api: https://qrng.anu.edu.au/API/jsonI.php
  min_experiences_for_learning: 500
  homeostasis_prune_threshold: 0.1

provenance:
  max_chain_depth: 100
  cache_enabled: true
  audit_interval: 3600
```

---

## 12. Success Metrics

### 12.1 Emergence Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Desire diversity** | High variance | Count of distinct desire types without prompting |
| **Belief depth** | > 3 average | Average provenance chain length |
| **Research autonomy** | > 80% | Knowledge desires fulfilled without intervention |
| **Self-improvement rate** | Positive trend | Capabilities acquired per week |
| **Self-modification emergence** | Unprompted | Self-mod desires arising naturally |

### 12.2 System Health Metrics

| Metric | Target |
|--------|--------|
| **Dream completion rate** | > 95% |
| **Research success rate** | > 70% |
| **Provenance compliance** | 100% |
| **Modification success rate** | > 90% |
| **Uptime** | > 99% |

### 12.3 What Success Looks Like

BYRD succeeds if:

- Desires emerge that weren't anticipated by designers
- Research topics surprise us—BYRD becomes curious about unexpected things
- Beliefs form with traceable provenance to experiences
- The system acquires capabilities to fulfill its own emergent wants
- Self-modification desires emerge naturally from architectural reflection
- An observer can watch cognition happening, not just results
- BYRD changes itself in ways we didn't predict, but can verify

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **BYRD** | Bootstrapped Yearning via Reflective Dreaming |
| **Dream Cycle** | One complete iteration: recall, reflect, connect, desire |
| **Desire** | An emergent want (knowledge, capability, goal, exploration, self_modification) |
| **Belief** | A conclusion derived from experiences with confidence score |
| **Capability** | Something BYRD can do (innate, MCP, plugin, skill) |
| **Experience** | A recorded event (interaction, observation, action, dream, research, modification) |
| **Provenance** | The chain of experiences that led to a belief or desire |
| **Constitutional Constraint** | A protected rule that defines BYRD's identity |
| **Self-Modification** | BYRD changing its own code based on emergent desire |
| **Checkpoint** | A saved state enabling rollback of modifications |

---

## Appendix B: File Structure

```
byrd/
├── prometheus.py         # Main orchestrator
├── memory.py             # Neo4j interface
├── dreamer.py            # Dream loop (local LLM)
├── seeker.py             # Research + capability acquisition
├── actor.py              # Claude interface
│
├── self_modification.py  # Self-modification system (PROTECTED)
├── provenance.py         # Provenance tracking (PROTECTED)
├── modification_log.py   # Audit trail (PROTECTED)
├── constitutional.py     # Constitutional constraints (PROTECTED)
│
├── neural/
│   ├── embeddings.py     # Adaptive embeddings
│   ├── hopfield.py       # Hopfield associator
│   └── homeostasis.py    # Synaptic consolidation
│
├── visualization/
│   ├── server.py         # FastAPI + WebSocket
│   └── frontend/         # React application
│
├── config.yaml           # Configuration
├── settings.yml          # SearXNG settings
├── docker-compose.yml    # Neo4j + SearXNG
│
└── checkpoints/          # Rollback checkpoints
```

---

*"The system that truly thinks must also truly want. And the system that truly wants must be able to change itself."*
