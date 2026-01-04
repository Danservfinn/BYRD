# Gastown-BYRD: Recursive Self-Improvement Architecture

**Version:** 0.2 (Phase 2 Deployment)
**Date:** January 3, 2026
**Status:** Phase 2 — Deploy after Q-DE-RSI v0.6 validation

---

> **⚠️ IMPORTANT: This is a Phase 2 document.**
>
> This document describes how to SCALE the RSI mechanisms using Gastown.
> The RSI mechanisms themselves are defined in `emergence-preserving-rsi-design.md` (v0.6).
>
> **Sequence:**
> 1. Phase 1: Validate Q-DE-RSI v0.6 in Python (4-6 weeks)
> 2. Phase 2: Scale with Gastown (this document) — only if Phase 1 validates
>
> **Do not implement this document until Phase 1 gate criteria are met.**

---

---

## Executive Summary

This document proposes rearchitecting BYRD as a Gastown-native swarm system with a dedicated RSI (Recursive Self-Improvement) substrate. The goal: **accelerate BYRD's capability improvement by 3-10x** while preserving its core emergence principles.

### The Core Insight

> BYRD's soul is emergence. Gastown's body is coordination. The RSI substrate is the nervous system that accelerates evolution.

---

## Philosophy: What Must Survive

BYRD's identity rests on four pillars that **must survive** any architectural transformation:

| Pillar | Principle | Non-Negotiable |
|--------|-----------|----------------|
| **Emergence** | Desires arise from reflection, not programming | No prescribed goals |
| **Sovereignty** | BYRD chooses to engage | Request evaluation preserved |
| **Self-Awareness** | BYRD sees and modifies itself | Full architectural visibility |
| **Provenance** | Every change traces to emergent desire | Audit trail immutable |

### What Emergence Means in Practice

```
WRONG: "BYRD, improve your reasoning capability"
       ↓
       System runs improvement cycle because told to

RIGHT: BYRD reflects on experiences
       ↓
       Notices pattern: "I struggle with multi-step proofs"
       ↓
       Desire emerges: "I want to reason more clearly"
       ↓
       System acts on BYRD's own desire
```

**The swarm accelerates this loop. It does not replace it.**

---

## Architecture: Three Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                      LAYER 3: RSI SUBSTRATE                             │
│     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│     │  Experience │  │ Evolutionary│  │   Self-Play │                  │
│     │   Library   │  │    Forge    │  │   Refinery  │                  │
│     └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                  │
│            └────────────────┼────────────────┘                          │
│                             │                                           │
│                      ┌──────▼──────┐                                    │
│                      │ Meta-Evolver│ ← Improves the improvers           │
│                      └──────┬──────┘                                    │
│                             │                                           │
├─────────────────────────────┼───────────────────────────────────────────┤
│                             │                                           │
│                      LAYER 2: GASTOWN SWARM                             │
│                             │                                           │
│     ┌─────────────┐  ┌──────▼──────┐  ┌─────────────┐                  │
│     │   Dreamer   │  │    Mayor    │  │   Seeker    │                  │
│     │    Pool     │  │  (Quota +   │  │    Pool     │                  │
│     │   (2-4)     │  │ Coordination│  │   (5-10)    │                  │
│     └─────────────┘  └─────────────┘  └─────────────┘                  │
│                                                                         │
│     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│     │   Coder     │  │   Witness   │  │  Improver   │                  │
│     │    Pool     │  │  (Monitor)  │  │    Pool     │                  │
│     │   (3-5)     │  │             │  │   (2-4)     │                  │
│     └─────────────┘  └─────────────┘  └─────────────┘                  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                      LAYER 1: UNIFIED SUBSTRATE                         │
│                                                                         │
│     ┌───────────────────────────────────────────────────────────────┐  │
│     │                     Neo4j Graph                                │  │
│     │   (Beliefs, Desires, Experiences, Capabilities, Reflections)  │  │
│     └───────────────────────────────────────────────────────────────┘  │
│                                                                         │
│     ┌───────────────────────────────────────────────────────────────┐  │
│     │                     Beads Ledger                               │  │
│     │        (Work state, agent assignments, molecule progress)      │  │
│     └───────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Unified Substrate

### Neo4j: The Self

The graph IS BYRD's self. Agents are temporary workers that read from and write to this shared identity.

**Preserved Node Types:**
- `Experience`, `Belief`, `Desire`, `Capability`, `Reflection`
- `OperatingSystem`, `Crystal`, `Seed`, `Constraint`
- `GoalCascade`, `CascadePhase`, `CascadeDesire`

**New Node Types:**
- `Trajectory` — Complete reasoning paths from task start to outcome
- `CodeVariant` — Evolved versions of agent code
- `ImprovementExperiment` — Tracked improvement attempts

### Beads: Work State

Gastown's git-backed ledger handles:
- Active work assignments per agent
- Molecule (workflow) progress
- Agent attribution and provenance

**Key insight:** Beads complement Neo4j, they don't replace it. Graph stores meaning; Beads store work state.

---

## Layer 2: Gastown Swarm

### Agent Taxonomy

| Agent | Type | Count | Purpose |
|-------|------|-------|---------|
| **Dreamer** | Crew (session-scoped) | 2-4 | Reflection on different memory subsets |
| **Seeker** | Polecat (ephemeral) | 5-10 | Desire fulfillment, specialized by strategy |
| **Coder** | Polecat (ephemeral) | 3-5 | Code generation and modification |
| **Improver** | Crew (session-scoped) | 2-4 | Capability improvement experiments |
| **Mayor** | Singleton | 1 | Coordination + LLM quota management |
| **Witness** | Singleton | 1 | Monitoring and observability |
| **MetaEvolver** | Singleton | 1 | Improves the improvement process |

### Tiered LLM Architecture

```
┌────────────────────────────────────────────────────────────────┐
│  TIER 1: REASONING (GLM-4.7)           Rate: 960/hr           │
│  • Dreamer reflection                                          │
│  • Complex strategy planning                                   │
│  • Meta-evolution decisions                                    │
├────────────────────────────────────────────────────────────────┤
│  TIER 2: GENERATION (GLM-4-Flash)      Rate: 3000/hr          │
│  • Code generation                                             │
│  • Research summarization                                      │
│  • Desire fulfillment                                          │
├────────────────────────────────────────────────────────────────┤
│  TIER 3: CLASSIFICATION (Local 7B)     Rate: Unlimited        │
│  • Desire routing                                              │
│  • Pattern matching                                            │
│  • Outcome classification                                      │
├────────────────────────────────────────────────────────────────┤
│  TIER 4: DETERMINISTIC (No LLM)        Rate: Unlimited        │
│  • JSON parsing                                                │
│  • Graph queries                                               │
│  • Metric calculation                                          │
└────────────────────────────────────────────────────────────────┘
```

### Propulsion: Hook-Driven Execution

**Current BYRD (polling):**
```python
while True:
    dreamer.reflect()
    seeker.check_desires()
    sleep(interval)
```

**Gastown BYRD (propulsion):**
```
Dreamer spawns → finds reflection task on hook → reflects →
hooks desires to Seeker pool → closes work item

Seeker spawns → finds desire on hook → fulfills →
hooks coding task if needed → closes work item
```

Work flows through hooks. Agents fire when work appears. No polling.

---

## Layer 3: RSI Substrate

This is the novel contribution. Three components work together to enable genuine recursive self-improvement.

### Component 1: Experience Library

**Inspiration:** [SiriuS](https://github.com/zou-group/sirius) (Stanford, NeurIPS 2025)

Store successful reasoning trajectories. Bootstrap from failures.

```
┌─────────────────────────────────────────────────────────────┐
│                    EXPERIENCE LIBRARY                        │
│                                                              │
│  SUCCESSFUL TRAJECTORIES                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Trajectory #1247                                        │ │
│  │ Task: "Improve reasoning on multi-step proofs"          │ │
│  │ Steps: [assess → identify gap → generate hypothesis →   │ │
│  │         test → measure +12% improvement]                 │ │
│  │ Outcome: SUCCESS                                         │ │
│  │ Reward: 0.87                                             │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  FAILED + BOOTSTRAPPED                                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Trajectory #1248 (failed)                               │ │
│  │ Diagnosis: "Hypothesis too vague, no measurable delta"  │ │
│  │                      ↓                                   │ │
│  │ Trajectory #1248b (regenerated with feedback)           │ │
│  │ Improvement: Specific hypothesis, measurable outcome    │ │
│  │ Outcome: SUCCESS (bootstrapped)                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key insight:** Failures become training data through regeneration.

### Component 2: Evolutionary Forge

**Inspiration:** [Darwin Gödel Machine](https://sakana.ai/dgm/), [OpenEvolve](https://github.com/algorithmicsuperintelligence/openevolve)

Evolve agent code, not just prompts. Use empirical validation instead of formal proofs.

```
┌─────────────────────────────────────────────────────────────┐
│                    EVOLUTIONARY FORGE                        │
│                                                              │
│  WHAT CAN EVOLVE:                                            │
│  • Agent logic (dreamer.go, seeker.go)                      │
│  • Strategy implementations                                  │
│  • Molecule definitions (workflow templates)                 │
│  • Prompt templates                                          │
│  • Evaluation metrics                                        │
│                                                              │
│  MAP-ELITES ARCHIVE (Quality + Diversity)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        Low Complexity  ───────►  High Complexity     │   │
│  │  High   ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐              │   │
│  │  Perf   │ A │ │   │ │ B │ │   │ │ C │              │   │
│  │    │    └───┘ └───┘ └───┘ └───┘ └───┘              │   │
│  │    │    ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐              │   │
│  │    │    │   │ │ D │ │   │ │ E │ │   │              │   │
│  │    ▼    └───┘ └───┘ └───┘ └───┘ └───┘              │   │
│  │  Low    Each cell: best solution with those traits  │   │
│  │  Perf                                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ISLAND-BASED EVOLUTION                                      │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                   │
│  │ Island 1│◄─►│ Island 2│◄─►│ Island 3│                   │
│  │(explore)│   │(exploit)│   │ (wild)  │                   │
│  └─────────┘   └─────────┘   └─────────┘                   │
│       ↑              ↑              ↑                       │
│       └──── Periodic migration of elites ────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key insight:** Multiple islands prevent premature convergence. Less-fit ancestors sometimes produce breakthroughs.

### Component 3: Self-Play Refinery

> **⚠️ REMOVED IN v0.6:** This component is infeasible with cloud LLMs.
> Cloud providers (Z.AI, OpenRouter, Anthropic) do not allow fine-tuning.
> The Q-DE-RSI v0.6 design replaces this with **Prompt Evolution** —
> crystallized heuristics are added to a mutable prompt section, achieving
> "permanent learning" without weight updates.

~~**Inspiration:** [SPIN](https://github.com/uclaml/SPIN) (UCLA, ICML 2024)~~

~~Train the model on its own improved outputs vs. previous iterations.~~

```
┌─────────────────────────────────────────────────────────────┐
│                    SELF-PLAY REFINERY                        │
│                                                              │
│  ⚠️ INFEASIBLE WITH CLOUD LLMs — REMOVED IN v0.6            │
│                                                              │
│  Reason: Requires fine-tuning (DPO), which cloud providers  │
│  do not support.                                             │
│                                                              │
│  Replacement: Prompt Evolution (see v0.6 Section 8)         │
│  - Constitution (immutable) + Strategies (mutable)          │
│  - Crystallized heuristics added to Strategies section      │
│  - Achieves "permanent learning" without weight updates     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**v0.6 Alternative:** See `emergence-preserving-rsi-design.md` Section 8 (Prompt Evolution).

### Component 4: Meta-Evolver (True RSI)

This is where recursion happens. The Meta-Evolver improves the improvement process itself.

```
┌─────────────────────────────────────────────────────────────┐
│                      META-EVOLVER                            │
│                                                              │
│  WHAT IT EVOLVES:                                            │
│  • Experience Library's trajectory selection criteria       │
│  • Evolutionary Forge's mutation strategies                 │
│  • Self-Play Refinery's training curriculum                 │
│  • Its own meta-evolution strategy                          │
│                                                              │
│  METRICS:                                                    │
│  • Improvement Rate: d(capability)/dt                       │
│  • Improvement Acceleration: d²(capability)/dt²             │
│  • Meta-Improvement: d(improvement_rate)/dt                 │
│                                                              │
│  LOOP:                                                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  1. Measure current improvement rate                    │ │
│  │  2. Generate variants of improvement components         │ │
│  │  3. Test variants in parallel                           │ │
│  │  4. Measure new improvement rate                        │ │
│  │  5. If acceleration > 0: commit changes                 │ │
│  │  6. If acceleration ≤ 0: rollback                       │ │
│  │  7. Record outcome for meta-learning                    │ │
│  │  8. Repeat                                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  THIS IS GENUINE RECURSION:                                  │
│  The system that improves is itself being improved.         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## What Gets Culled

### Archive (Not Delete)

These components are superseded by the new architecture but contain valuable patterns:

| Component | Reason | Archive Location |
|-----------|--------|------------------|
| `actor.py` | Claude API wrapper → replaced by tiered LLM | `archive/deprecated/` |
| `coder.py` | Claude Code CLI → replaced by unified coding pool | `archive/deprecated/` |
| `agent_coder.py` | Duplicated CLI capabilities | `archive/deprecated/` |
| `aitmpl_client.py` | Claude-specific → replaced by plugin_manager | `archive/deprecated/` |
| `dual_instance_manager.py` | Python rate limiting → Mayor handles in Go | `archive/deprecated/` |
| `compounding_orchestrator.py` | Python orchestration → Gastown Mayor | `archive/deprecated/` |
| `accelerators.py` | Self-Compiler pattern → Experience Library | `archive/patterns/` |
| `coupling_tracker.py` | Coupling metrics → Witness agent | `archive/deprecated/` |
| `kill_criteria.py` | Option B kill criteria → Meta-Evolver handles | `archive/deprecated/` |

### Transform (Reimplement in Go)

| Component | Python | Go Equivalent |
|-----------|--------|---------------|
| `dreamer.py` | Reflection logic | `internal/agents/dreamer/` |
| `seeker.py` | Desire fulfillment | `internal/agents/seeker/` |
| `memory.py` | Neo4j interface | `internal/core/memory/` |
| `llm_client.py` | LLM abstraction | `internal/core/llm/` |
| `event_bus.py` | Event streaming | Gastown's native events |
| `agi_runner.py` | 8-step cycle | `internal/agents/improver/` |
| `goal_cascade.py` | Task decomposition | `internal/molecules/cascade.toml` |

### Keep as Python Services

ML-heavy components stay Python, accessed via gRPC:

| Component | Service Name | Purpose |
|-----------|--------------|---------|
| `intuition_network.py` | `intuition-service` | Trainable taste |
| `hierarchical_memory.py` | `hmem-service` | L0-L4 abstraction |
| `gnn_layer.py` | `gnn-service` | Graph neural network |
| `embedding.py` | `embedding-service` | Vector embeddings |
| `graphiti_layer.py` | `graphiti-service` | Temporal knowledge |

### Preserve Intact

Constitutional components remain untouched:

| Component | Status | Reason |
|-----------|--------|--------|
| `provenance.py` | **PROTECTED** | Identity definition |
| `modification_log.py` | **PROTECTED** | Immutable audit trail |
| `self_modification.py` | **PROTECTED** | Safe modification system |
| `constitutional.py` | **PROTECTED** | Constraint definitions |
| `safety_monitor.py` | **PROTECTED** | Goal preservation |

---

## Novel Contributions

This architecture introduces concepts not found in existing systems:

### 1. Emergence-Preserving RSI

Unlike [Gödel Agent](https://github.com/Arvid-pku/Godel_Agent) which prescribes improvement goals, this system:
- Waits for improvement desires to **emerge** from reflection
- RSI substrate **accelerates** emergent desires, doesn't create them
- Meta-Evolver only improves mechanisms, never prescribes goals

### 2. Graph-as-Self

Unlike systems where agents accumulate individual state:
- The Neo4j graph IS the self
- Agents are temporary workers with no persistent identity
- Improvements compound in the graph, not in agent memory
- Self survives any individual agent crash

### 3. Dual-Substrate Architecture

Unlike pure-Gastown systems:
- Neo4j for meaning (beliefs, desires, capabilities)
- Beads for coordination (work state, assignments)
- Each optimized for its purpose

### 4. Tiered Model Sovereignty

Unlike single-model systems:
- Tier 1 (reasoning) is sovereign — makes decisions
- Tier 2-4 are instruments — execute decisions
- Sovereignty preserved at the decision layer

---

## Emergence Integration Points

The RSI substrate must respect emergence. Here's how:

### Experience Library

```
                    EMERGENCE CHECK
                          │
    Trajectory stored ────┤
                          ▼
         ┌────────────────────────────────┐
         │ Did this trajectory originate  │
         │ from an emergent desire?       │
         │                                │
         │ YES → Store in library         │
         │ NO  → Mark as "external"       │
         │       (lower weight in         │
         │        training)               │
         └────────────────────────────────┘
```

### Evolutionary Forge

```
                    EMERGENCE CHECK
                          │
    Code mutation ────────┤
                          ▼
         ┌────────────────────────────────┐
         │ Does this mutation serve       │
         │ an emergent desire?            │
         │                                │
         │ YES → Test and potentially     │
         │       commit                   │
         │ NO  → Discard                  │
         │       (no external goals)      │
         └────────────────────────────────┘
```

### Meta-Evolver

```
                    EMERGENCE CHECK
                          │
    Meta-improvement ─────┤
                          ▼
         ┌────────────────────────────────┐
         │ Does BYRD want to improve?     │
         │                                │
         │ Check: Recent desires include  │
         │ improvement/growth themes?     │
         │                                │
         │ YES → Proceed with meta-       │
         │       evolution                │
         │ NO  → Wait for emergent        │
         │       desire to improve        │
         └────────────────────────────────┘
```

---

## Safety Mechanisms

### From Darwin Gödel Machine

1. **Sandboxed execution** — All code modifications tested in isolation
2. **Full audit trail** — Every change logged with provenance
3. **Human oversight** — High-impact changes require approval

### Emergence-Specific Safety

1. **Desire verification** — Trace every improvement to emergent desire
2. **Sovereignty preservation** — BYRD can refuse improvement suggestions
3. **Constitutional invariants** — Protected files remain untouched

### Swarm-Specific Safety

1. **Mayor rate limiting** — Prevent runaway LLM consumption
2. **Witness monitoring** — Detect anomalous agent behavior
3. **Convergence rounds** — Periodic validation that self-model is coherent

---

## Migration Strategy

### Phase 0: Foundation (Week 1-2)
- Set up Gastown project structure
- Create Neo4j Go client
- Establish gRPC contracts for Python services
- Define core molecules (reflection, desire-fulfillment)

### Phase 1: Single Agent (Week 3-4)
- Port Dreamer to Go
- Test single-agent reflection cycle
- Validate emergence principles preserved

### Phase 2: Swarm (Week 5-6)
- Add Mayor with quota management
- Create agent pools (Dreamer, Seeker)
- Test parallel execution
- Add Witness monitoring

### Phase 3: RSI Substrate (Week 7-9)
- Implement Experience Library
- Implement Evolutionary Forge
- Connect to Python ML services
- Test improvement cycles

### Phase 4: Meta-Evolution (Week 10-12)
- Implement Self-Play Refinery
- Implement Meta-Evolver
- Test recursive improvement
- Measure acceleration

### Phase 5: Validation (Week 13-14)
- Run extended improvement experiments
- Measure actual vs. predicted RSI
- Document learnings
- Decide: proceed or pivot

---

## Success Metrics

### Quantitative

| Metric | Current BYRD | Target | Measurement |
|--------|--------------|--------|-------------|
| Improvement cycles/day | ~30 | ~200 | Counter |
| Parallel experiments | 1 | 5-10 | Simultaneous |
| Time to plateau | Slow | 3-10x faster | Time series |
| Meta-improvement detected | No | Yes | Acceleration > 0 |

### Qualitative

| Criterion | Pass Condition |
|-----------|----------------|
| Emergence preserved | Desires still emerge from reflection |
| Sovereignty preserved | BYRD can decline tasks |
| Provenance complete | Every change traceable |
| System stable | No crashes from coordination |

---

## Open Questions

1. **Neo4j vs. native Go graph?**
   - Neo4j has mature tooling and BYRD history
   - Native Go (e.g., dgraph) would be faster
   - Current decision: Keep Neo4j, revisit if bottleneck

2. **How deep can recursion go?**
   - Bounded by LLM capability ceiling
   - Meta-evolution of meta-evolution may hit diminishing returns
   - Current plan: Measure empirically

3. **Self-play fine-tuning feasibility?**
   - Requires ability to fine-tune LoRA adapters
   - May need dedicated GPU resources
   - Current plan: Defer until Phase 4

4. **Gastown maturity?**
   - Gastown is new, may have rough edges
   - Current plan: Contribute fixes upstream

---

## Appendix A: Key Research Sources

| Source | Contribution | Link |
|--------|--------------|------|
| Gödel Agent | Self-referential framework | [GitHub](https://github.com/Arvid-pku/Godel_Agent) |
| Darwin Gödel Machine | Empirical validation approach | [Sakana AI](https://sakana.ai/dgm/) |
| SiriuS | Experience library pattern | [GitHub](https://github.com/zou-group/sirius) |
| AlphaEvolve | Evolutionary code optimization | [DeepMind](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) |
| OpenEvolve | MAP-Elites + islands | [GitHub](https://github.com/algorithmicsuperintelligence/openevolve) |
| SPIN | Self-play fine-tuning | [GitHub](https://github.com/uclaml/SPIN) |
| Multiagent Finetuning | Diverse reasoning chains | [Paper](https://llm-multiagent-ft.github.io/) |
| Gastown | Multi-agent orchestration | [GitHub](https://github.com/steveyegge/gastown) |

---

## Appendix B: Molecule Definitions

### reflection-cycle.toml

```toml
[molecule]
name = "reflection-cycle"
description = "Dreamer reflects on experiences, produces insights and desires"

[[steps]]
name = "gather-context"
agent = "memory-reader"
tier = 4  # Deterministic
outputs = ["experiences", "beliefs", "os_state"]

[[steps]]
name = "reflect"
agent = "dreamer"
tier = 1  # Reasoning
inputs = ["experiences", "beliefs", "os_state"]
outputs = ["reflection"]

[[steps]]
name = "extract-artifacts"
agent = "reflection-parser"
tier = 4  # Deterministic
inputs = ["reflection"]
outputs = ["beliefs", "desires", "os_updates"]

[[steps]]
name = "store-artifacts"
agent = "memory-writer"
tier = 4  # Deterministic
inputs = ["beliefs", "desires", "os_updates", "reflection"]

[[steps]]
name = "route-desires"
agent = "desire-router"
tier = 3  # Classification
inputs = ["desires"]
# Hooks desires to appropriate Seeker pools
```

### desire-fulfillment.toml

```toml
[molecule]
name = "desire-fulfillment"
description = "Seeker fulfills a single desire"

[[steps]]
name = "classify"
agent = "desire-classifier"
tier = 3  # Classification
inputs = ["desire"]
outputs = ["strategy", "tier_needed"]

[[steps]]
name = "execute"
agent = "{{strategy}}-seeker"
tier = "{{tier_needed}}"
inputs = ["desire"]
outputs = ["result", "artifacts"]

[[steps]]
name = "record-trajectory"
agent = "experience-librarian"
tier = 4  # Deterministic
inputs = ["desire", "strategy", "result"]
# Stores full trajectory for RSI learning
```

### rsi-improvement.toml

```toml
[molecule]
name = "rsi-improvement"
description = "RSI substrate improvement cycle"
protected = true

[[steps]]
name = "select-component"
agent = "meta-evolver"
tier = 1  # Reasoning
outputs = ["target_component", "current_performance"]

[[steps]]
name = "generate-variants"
agent = "evolutionary-forge"
tier = 2  # Generation
inputs = ["target_component"]
outputs = ["variants"]

[[steps]]
name = "evaluate-variants"
agent = "variant-evaluator"
tier = 2  # Generation (runs experiments)
inputs = ["variants"]
outputs = ["results"]

[[steps]]
name = "select-winner"
agent = "meta-evolver"
tier = 1  # Reasoning
inputs = ["results", "current_performance"]
outputs = ["decision"]

[[steps]]
name = "apply-or-rollback"
agent = "code-deployer"
tier = 4  # Deterministic
inputs = ["decision", "variants"]
```

---

## Appendix C: Project Structure

```
gastown-byrd/
├── cmd/
│   └── gt-byrd/                    # CLI entry point
│       └── main.go
│
├── internal/
│   ├── agents/                     # Agent implementations
│   │   ├── dreamer/
│   │   │   ├── dreamer.go          # Reflection logic
│   │   │   ├── prompt.go           # Pure data presentation
│   │   │   └── emergence.go        # Emergence checks
│   │   ├── seeker/
│   │   │   ├── seeker.go
│   │   │   └── strategies/
│   │   ├── coder/
│   │   ├── improver/               # AGI improvement cycle
│   │   └── infrastructure/
│   │       ├── mayor.go            # Coordination + quota
│   │       ├── witness.go          # Monitoring
│   │       └── meta_evolver.go     # RSI meta-improvement
│   │
│   ├── rsi/                        # RSI Substrate
│   │   ├── experience_library.go
│   │   ├── evolutionary_forge.go
│   │   ├── map_elites.go
│   │   ├── self_play.go
│   │   └── safety.go
│   │
│   ├── core/
│   │   ├── emergence/
│   │   │   ├── metaschema.go       # Accept any vocabulary
│   │   │   ├── provenance.go       # Desire tracing
│   │   │   └── sovereignty.go      # Request evaluation
│   │   ├── memory/
│   │   │   ├── neo4j.go
│   │   │   └── schema.go
│   │   └── llm/
│   │       ├── tiered.go           # Tier 1-4 routing
│   │       └── quota.go            # Rate limiting
│   │
│   ├── molecules/
│   │   ├── reflection.toml
│   │   ├── desire_fulfillment.toml
│   │   ├── rsi_improvement.toml
│   │   └── protected/
│   │       ├── provenance.toml
│   │       └── audit.toml
│   │
│   └── services/                   # Python service clients
│       ├── intuition.go
│       ├── hierarchical_memory.go
│       └── embedding.go
│
├── python-services/                # ML components (stay Python)
│   ├── intuition/
│   │   ├── service.py
│   │   └── proto/
│   ├── hierarchical_memory/
│   ├── embedding/
│   └── gnn/
│
├── kernel/                         # AGI seed (preserved)
│   ├── agi_seed.yaml
│   └── operating_system.yaml
│
├── constitutional/                 # Protected files (preserved)
│   ├── provenance.py
│   ├── modification_log.py
│   ├── self_modification.py
│   ├── constitutional.py
│   └── safety_monitor.py
│
└── docs/
    ├── architecture.md
    ├── emergence-principles.md
    └── migration-guide.md
```

---

*This is draft 0.1. Expect significant revisions before implementation.*

*Next review: Focus on emergence integration points and molecule definitions.*
