# BYRD Seed Architecture: The Five Compounding Loops

> "Make each LLM call 10x more valuable through smart scaffolding."

This document defines BYRD's core architecture: five compounding loops that work together to accelerate capability growth.

---

## The Acceleration Thesis

```
Capability(t) = Capability(0) + ∫ improvement_rate(t) dt
```

Where `improvement_rate(t)` should be **increasing** over time. We claim **accelerating**: `improvement_rate(t+1) > improvement_rate(t)`.

A system that starts weak but accelerates beats a system that starts strong but plateaus.

---

## Architecture Overview

BYRD Omega synthesizes five compounding loops with a unified memory graph:

```
                                ┌─────────────────────────────────────┐
                                │           UNIFIED MEMORY            │
                                │              (Neo4j)                │
                                │                                     │
                                │   Experiences, Patterns, Goals,     │
                                │   Beliefs, Capabilities, Insights   │
                                └───────────────┬─────────────────────┘
                                                │
        ┌───────────────────────────────────────┼───────────────────────────────────────┐
        │                   │                   │                   │                   │
        ▼                   ▼                   ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ SELF-COMPILER │   │MEMORY REASONER│   │ GOAL EVOLVER  │   │   DREAMING    │   │ INTEGRATION   │
│               │   │               │   │               │   │   MACHINE     │   │     MIND      │
│ Patterns make │   │ Graph answers │   │ Goals evolve  │   │               │   │               │
│ future mods   │   │ before LLM    │   │ via fitness   │   │ Counterfacts  │   │ Cross-loop    │
│ more likely   │   │ calls         │   │               │   │ multiply exp  │   │ synergies     │
│               │   │               │   │               │   │               │   │               │
└───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘
```

---

## The Five Compounding Loops

### Loop 1: The Self-Compiler

**What it does**: Extracts reusable patterns from successful modifications, making future modifications more likely to succeed.

**Acceleration mechanism**: Pattern library grows → future problems have more relevant patterns → higher success rate → more patterns extracted.

```
Problem → Match Patterns → Generate Solution → Execute → SUCCESS?
                ↑                                           │
                │         Pattern Library                   │
                └───────────── Extract ←────────────────────┘
```

**Key components**:
- **Pattern Library**: Stores `(context_embedding, solution_template)` pairs
- **Adaptive Threshold**: Confidence threshold adjusts based on recent success rate
- **Abstraction Lifting**: Successful patterns get generalized (concrete → intermediate → abstract)

**Success metric**: Modification success rate > 50%

---

### Loop 2: The Memory Reasoner

**What it does**: Answers queries from the graph before calling the LLM, making each LLM call more valuable.

**Acceleration mechanism**: More experiences → richer graph → more queries answered from memory → LLM calls reserved for truly novel problems.

```
Query → Embed → Spreading Activation → Confidence Check
                        │                    │
                        │          High? ────┴──→ Return Memory Answer
                        │          Low?  ────────→ Call LLM → Cache Answer
                        ↓
                  Update Graph
```

**Key components**:
- **Spreading Activation**: Activates semantically related nodes
- **Confidence Estimation**: Tracks retrieval accuracy over time
- **Answer Caching**: LLM answers become future memory answers

**Success metric**: Memory reasoning ratio > 50%

---

### Loop 3: The Goal Evolver

**What it does**: Goals evolve through fitness selection, producing increasingly effective goals.

**Acceleration mechanism**: Fitness-weighted selection → better goals survive → system pursues more valuable objectives.

```
Goal Population → Select by Fitness → Mutate/Recombine → Evaluate
       ↑                                                    │
       └─────────────── Next Generation ←───────────────────┘
```

**Key components**:
- **Goal Genome**: Structure, resources, success criteria, learned_from
- **Fitness Function**: Combines completion, capability_gain, efficiency
- **Evolutionary Operators**: Tournament selection, crossover, mutation

**Success metric**: Average fitness increasing per generation

---

### Loop 4: The Dreaming Machine

**What it does**: Generates counterfactual experiences and hypotheses, multiplying learning from each real experience.

**Acceleration mechanism**: One experience → N imagined variations → N+1 learning opportunities.

```
Real Experience → Generate Counterfactuals → Simulate Outcomes
                                                    │
                          ┌─────────────────────────┴─────────────────────────┐
                          ↓                         ↓                         ↓
                   "What if I had..."        "What if the..."        "What if instead..."
                          │                         │                         │
                          └─────────────────────────┴─────────────────────────┘
                                                    │
                                             Extract Insights
```

**Key components**:
- **Counterfactual Generator**: Varies actions, contexts, parameters
- **Outcome Simulator**: Predicts what would have happened
- **Insight Extractor**: Identifies patterns across real + imagined experiences

**Success metric**: Insight extraction rate > 15%

---

### Loop 5: The Integration Mind

**What it does**: Enables cross-loop synergies that produce emergent behaviors.

**Acceleration mechanism**: If loops reinforce each other, combined value > sum of parts.

**Key couplings**:

| Coupling | Mechanism | Type |
|----------|-----------|------|
| Goal → Compiler | Better goals direct pattern learning to higher-leverage areas | **MULTIPLICATIVE** |
| Memory → Dreamer | Rich memory enables richer counterfactuals | Additive |
| Compiler → Memory | Successful patterns become retrievable knowledge | Additive |
| Dreamer → Goal | Imagined outcomes inform goal fitness | Additive |

**The Critical Coupling**: Only **Goal → Compiler** is plausibly multiplicative. If fitness-selected goals direct the Self-Compiler to learn patterns in areas that improve goal fitness, we get a feedback loop:

```
Better goals → Better patterns → Higher success → Better goals → ...
```

**Success metric**: Emergent behaviors > 0 (behaviors not present in individual loops)

---

## Implementation Mapping

| Loop | Primary Module | Memory Node Types |
|------|----------------|-------------------|
| Self-Compiler | `omega.py` | Pattern, ModificationAttempt |
| Memory Reasoner | `memory.py` | All nodes (spreading activation) |
| Goal Evolver | `goal_evolver.py` | Desire, GoalCandidate |
| Dreaming Machine | `dreamer.py`, `dreaming_machine.py` | Reflection, Counterfactual |
| Integration Mind | `omega.py` | CouplingMeasurement |

---

## Design Principles

1. **Scaffolding, Not Replacement** - The LLM is the intelligence. We build scaffolding that makes each LLM call more valuable.

2. **Measure Before Believing** - No claim survives without data. Every mechanism has explicit success metrics.

3. **One Multiplicative Coupling** - Of all possible loop interactions, only Goal Evolver → Self-Compiler is plausibly multiplicative.

4. **Graceful Degradation** - If coupling fails, loops still provide value independently.

5. **Information Preservation** - Every experience, pattern, and goal modification is recorded with provenance.

---

## See Also

- `ARCHITECTURE.md` - Full architecture documentation
- `kernel/agi_seed.yaml` - AGI Seed directive and core imperatives
- `docs/OMEGA_INTEGRATION_PLAN.md` - Omega integration details
