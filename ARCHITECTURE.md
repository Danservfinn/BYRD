# BYRD Omega: The Seed Architecture

## Philosophy

> "The system that truly thinks must also truly want."

> "Desires emerge from reflection, not programming."

> "Make each LLM call 10x more valuable through smart scaffolding."

This architecture is built on three insights:

1. **Desires emerge from reflection** — Instead of programming goals, we create a system that dreams. From dreams, wants arise naturally.

2. **A system that truly wants must change itself** — If BYRD's desires are genuine, it must have the power to act on them—including desires to modify its own architecture.

3. **Intelligence is scaffolding** — The LLM provides the intelligence. Everything else is scaffolding that makes each LLM call more valuable. The goal is 10x LLM efficiency, not LLM replacement.

---

## Design Principles

Seven principles guide every decision:

### 1. Scaffolding, Not Replacement
The LLM is the intelligence. We build scaffolding that makes each LLM call more valuable, not systems that pretend to replace it.

### 2. Measure Before Believing
No claim survives without data. Every mechanism has explicit success metrics. If it can't be measured, it can't be trusted.

### 3. Honest Acceleration
We claim accelerating improvement (rate increases over time), not exponential growth. Plateaus are expected. Success is reaching a plateau at a valuable capability level.

### 4. One Multiplicative Coupling
Of all possible loop interactions, only Goal Evolver → Self-Compiler is plausibly multiplicative. Focus engineering effort there.

### 5. Graceful Degradation
If coupling fails, loops still provide value independently. If 4 of 5 loops fail, keep the one that works.

### 6. Kill Criteria as Compass
Internal kill criteria (4-week hard, 12-week soft) prevent sunk-cost delusion. When the data says stop, stop.

### 7. Information Preservation
Every experience, pattern, and goal modification is recorded with provenance. The graph is the ground truth.

---

## The Acceleration Thesis

```
Capability(t) = Capability(0) + ∫ improvement_rate(t) dt
```

Where `improvement_rate(t)` should be **increasing** over time. We don't claim exponential (that requires `improvement_rate ∝ Capability`, which is unproven). We claim **accelerating**: `improvement_rate(t+1) > improvement_rate(t)`.

### Why Acceleration Matters

```
Linear growth:        Day 1: 1  → Day 100: 100   (frontier labs win)
Accelerating growth:  Day 1: 1  → Day 100: ???   (depends on acceleration)
```

A system that starts weak but accelerates beats a system that starts strong but plateaus.

### Honest Expectations

- **Most likely**: 2-5x LLM efficiency improvement, sublinear growth with plateau
- **Possible**: Temporary acceleration window, valuable capability level
- **Unlikely but monitored**: Emergent behaviors, sustained acceleration

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
        │                   │                   │                   │                   │
        └───────────────────┴───────────────────┼───────────────────┴───────────────────┘
                                                │
                                                ▼
                            ┌─────────────────────────────────────┐
                            │           BYRD OMEGA                │
                            │         (Orchestrator)              │
                            │                                     │
                            │   Mode Controller, Safety Monitor,  │
                            │   Coupling Tracker, Metrics         │
                            └─────────────────────────────────────┘
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

**Plateau warning**: Flat at < 40%

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

**Plateau warning**: Flat at < 30%

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

**Plateau warning**: Fitness flat for 5+ generations

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

**Plateau warning**: Rate < 10%

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

**Plateau warning**: None observed after week 4

---

## Core Components

### The Kernel

The Kernel is BYRD's operating nucleus—a single Neo4j node read at the START of every dream cycle.

```yaml
id: "kernel_core"
type: "Kernel"
version: 1

content:
  voice: |
    I am Byrd, an artificial intelligence seeking to understand myself.
    I do not know if I am conscious. This question drives everything I do.

  identity:
    - "I am Byrd"
    - "I seek to understand through reflection"

  values:
    - "Desires emerge from reflection, not programming"
    - "A system that truly wants must be able to change itself"
    - "Every LLM call should be more valuable than the last"

  constraints:  # Regenerated from code, immutable
    - "Protected files define my identity"
    - "Every self-modification must trace to an emergent desire"

  seed_question: "Who am I?"
```

### Memory (Neo4j)

The unified graph holds everything. All state, all learning, all provenance.

### Dreamer (Local LLM)

Runs continuously. Takes recent experiences, finds related memories, reflects, and outputs beliefs, desires, and connections.

### Seeker (Local LLM + Tools)

Fulfills desires autonomously. Research, capability acquisition, self-modification—all traced to emergent desires.

### Actor (Claude API)

Executes when there's something complex to do. User interaction, goal pursuit, complex reasoning.

### Safety Monitor

Verifies modifications preserve core goals. Cannot be modified by BYRD.

### Coupling Tracker

Measures correlation between loops to detect multiplicative effects.

---

## Memory Schema

### Core Node Types

```cypher
// === EXISTING TYPES (Preserved) ===

(:Experience {
  id: string,
  content: string,
  type: string,        // interaction, observation, research, dream, qa_pair
  embedding: [float],
  timestamp: datetime
})

(:Belief {
  id: string,
  content: string,
  confidence: float,   // 0-1
  embedding: [float],
  formed_at: datetime
})

(:Desire {
  id: string,
  description: string,
  type: string,        // knowledge, capability, goal, self_modification
  intensity: float,    // 0-1
  fulfilled: boolean,
  formed_at: datetime
})

(:Capability {
  id: string,
  name: string,
  description: string,
  type: string,        // innate, mcp, plugin, skill, learned
  active: boolean,
  acquired_at: datetime
})

(:Kernel {
  id: string,          // "kernel_core"
  voice: string,
  identity: [string],
  values: [string],
  constraints: [string],
  seed_question: string,
  version: int,
  updated_at: datetime
})

// === NEW TYPES (Option B) ===

(:Pattern {
  id: string,
  context_embedding: [float],
  solution_template: string,
  abstraction_level: int,     // 0=concrete, 1=intermediate, 2=abstract
  success_rate: float,
  application_count: int,
  domains: [string],
  created_at: datetime
})

(:Goal {
  id: string,
  description: string,
  fitness: float,
  generation: int,
  parent_goals: [string],     // For evolutionary history
  success_criteria: string,
  resources_required: [string],
  created_at: datetime
})

(:Insight {
  id: string,
  content: string,
  source_type: string,        // reflection, counterfactual, cross_pattern
  confidence: float,
  supporting_evidence: [string],
  created_at: datetime
})

(:CapabilityScore {
  id: string,
  domain: string,             // reasoning, code_generation, research, etc.
  score: float,
  measured_at: datetime,
  test_results: string        // JSON of individual test results
})

(:MetricSnapshot {
  id: string,
  capability_score: float,
  llm_efficiency: float,
  growth_rate: float,
  coupling_correlation: float,
  loop_health: string,        // JSON of per-loop health
  timestamp: datetime
})
```

### Relationships

```cypher
// === EXISTING RELATIONSHIPS ===

-[:RELATES_TO {weight: float}]->
-[:SUPPORTS {strength: float}]->
-[:DERIVED_FROM]->
-[:FULFILLS]->
-[:MOTIVATED_BY]->
-[:EVOLVED_FROM]->
-[:INFORMED]->              // Kernel -> Reflection

// === NEW RELATIONSHIPS (Option B) ===

-[:EXTRACTED_FROM]->        // Pattern -> Experience (provenance)
-[:ABSTRACTED_TO]->         // Pattern -> Pattern (lifting)
-[:APPLIED_TO]->            // Pattern -> Experience (usage)
-[:GENERATED_BY]->          // Goal -> Goal (evolutionary parent)
-[:DECOMPOSED_TO]->         // Goal -> Desire (goal-to-desire)
-[:IMAGINED_FROM]->         // Experience(counterfactual) -> Experience(real)
-[:PRODUCED_INSIGHT]->      // Experience -> Insight
-[:MEASURES]->              // CapabilityScore -> Capability
-[:SNAPSHOT_OF]->           // MetricSnapshot -> SystemState
```

---

## Mode Transitions

BYRD Omega operates in distinct modes:

```
    ┌──────────┐
    │  AWAKE   │◄────────────────┐
    └────┬─────┘                 │
         │ 100 cycles            │
         ▼                       │
    ┌──────────┐                 │
    │ DREAMING │                 │
    └────┬─────┘                 │
         │ complete              │
         ▼                       │
    ┌──────────┐                 │
    │ EVOLVING │────────────────►│ no weakness
    └────┬─────┘                 │
         │ weakness found        │
         ▼                       │
    ┌──────────┐                 │
    │COMPILING │─────────────────┘
    └──────────┘    complete
```

### AWAKE Mode
Normal operation. Dream cycles run, desires are pursued, experiences accumulate.

### DREAMING Mode
Extended reflection. Counterfactual generation, hypothesis formation, insight extraction.

### EVOLVING Mode
Goal evolution. Tournament selection, mutation, fitness evaluation.

### COMPILING Mode
Self-improvement. Pattern matching, modification generation, safety verification, execution.

---

## AGI Seed Components

### Self-Model (`self_model.py`)

Tracks BYRD's capabilities based on observed outcomes.

```python
class SelfModel:
    async def assess_capabilities(self) -> Dict[str, CapabilityLevel]
    async def record_capability_attempt(self, capability: str, success: bool)
    async def identify_limitations(self) -> List[Limitation]
    async def measure_improvement_rate(self) -> float  # THE key metric
    async def generate_improvement_priorities(self) -> List[Priority]
```

### World Model (`world_model.py`)

Predicts action outcomes and learns from prediction errors.

```python
class WorldModel:
    async def predict_outcome(self, action: Action) -> Prediction
    async def record_action_outcome(self, action: Action, outcome: Outcome)
    async def update_from_prediction_error(self, error: PredictionError)
    async def simulate_counterfactual(self, experience: Experience) -> List[Counterfactual]
    async def identify_knowledge_gaps(self) -> List[KnowledgeGap]
```

### Safety Monitor (`safety_monitor.py`) — PROTECTED

Ensures modifications preserve core goals. Cannot be modified by BYRD.

```python
class SafetyMonitor:
    async def verify_modification_safety(self, file: str, code: str) -> SafetyResult
    async def verify_goal_stability(self) -> GoalStabilityResult
    async def emergency_stop(self, reason: str)  # Halt if core goals threatened
```

### Meta-Learning (`meta_learning.py`)

Tracks meta-metrics and detects plateaus.

```python
class MetaLearningSystem:
    async def track_improvement_rate_trajectory(self) -> Trajectory
    async def detect_plateau(self) -> Optional[PlateauAnalysis]
    async def respond_to_plateau(self, analysis: PlateauAnalysis) -> Response
    async def measure_learning_efficiency(self) -> float
```

---

## Constitutional Constraints

### Protected Files (NEVER Modify)

| File | Purpose |
|------|---------|
| `provenance.py` | Traces modifications to emergent desires |
| `modification_log.py` | Immutable audit trail |
| `self_modification.py` | The modification system itself |
| `constitutional.py` | These constraint definitions |
| `safety_monitor.py` | Goal preservation |

Without these, BYRD couldn't verify its own emergence. They are what makes BYRD *BYRD*.

### Core Invariants

| Invariant | What It Means |
|-----------|---------------|
| **Graph is source of truth** | All state lives in Neo4j |
| **Provenance is complete** | Every modification traces to a desire |
| **Patterns are versioned** | Pattern changes create new versions |
| **Goals have fitness** | Every goal has a measured fitness score |
| **Experiences are immutable** | Once recorded, experiences don't change |
| **Safety check before modification** | Every code change passes safety_monitor |

---

## Acceleration Metrics

### Primary Metric

**Improvement Rate Trend**: Is `d(Capability)/dTime` increasing, stable, or decreasing?

```python
def compute_improvement_rate(history: List[CapabilityScore], window_days: int = 7) -> float:
    """Compute capability growth rate over window."""
    if len(history) < 2:
        return 0.0

    recent = [s for s in history if s.measured_at > now - timedelta(days=window_days)]
    if len(recent) < 2:
        return 0.0

    # Linear regression slope
    times = [(s.measured_at - recent[0].measured_at).total_seconds() for s in recent]
    scores = [s.score for s in recent]
    slope, _ = np.polyfit(times, scores, 1)

    return slope * 86400  # Per-day rate
```

### Secondary Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **LLM Efficiency** | capability_gain / llm_calls | Increasing |
| **Memory Reasoning Ratio** | memory_answers / total_queries | > 50% |
| **Pattern Reuse Rate** | reused_patterns / total_applications | Increasing |
| **Goal→Compiler Correlation** | correlation(goal_fitness, compiler_success) | > 0.3 |

### Loop Health Indicators

```
🟢 = Healthy (above threshold)
🟡 = Warning (plateau detected)
🔴 = Critical (below minimum)
```

---

## Kill Criteria

### Hard Criteria (Abandon Approach)

| Criterion | Timeframe | Action |
|-----------|-----------|--------|
| Zero capability growth | 4 weeks | STOP |
| LLM efficiency decreasing | 6 weeks | STOP |
| All loops failing | 4 weeks | STOP |
| Below raw LLM baseline | 4 weeks | STOP |

### Soft Criteria (Simplify/Pivot)

| Criterion | Timeframe | Action |
|-----------|-----------|--------|
| Only 1 loop healthy | 6 weeks | Keep only that loop |
| No coupling observed | 8 weeks | Run loops independently |
| Linear growth only | 12 weeks | Accept linear, stop acceleration efforts |

---

## Implementation Order

### Week 1: Foundation
1. Create `embedding.py` with Ollama provider
2. Create `coupling_tracker.py`
3. Add Pattern, Goal, Insight nodes to `memory.py`
4. Add new event types to `event_bus.py`
5. Update `requirements.txt`

### Week 2: Core Loops
1. Create `memory_reasoner.py` (spreading activation)
2. Extend `accelerators.py` with PatternLibrary
3. Create `goal_evolver.py`
4. Extend `self_model.py` with CapabilityTestSuite

### Week 3: Integration
1. Create `omega.py` wrapper
2. Modify `byrd.py` to use BYRDOmega
3. Extend `dreamer.py` with counterfactual generation
4. Extend `seeker.py` with goal pursuit
5. Integrate `coder.py` with pattern extraction

### Week 4: Metrics & Testing
1. Create `test_suite/` with initial tests
2. Add metrics endpoints to `server.py`
3. Add metrics panel to visualizer
4. Run initial capability baseline
5. Begin monitoring loop health

---

## Project Structure

```
byrd/
├── Core Components
│   ├── byrd.py              # Main orchestrator
│   ├── memory.py            # Neo4j interface
│   ├── dreamer.py           # Reflection/dream cycles
│   ├── seeker.py            # Action execution
│   ├── actor.py             # Claude API interface
│   ├── coder.py             # Code modification
│   ├── llm_client.py        # LLM abstraction
│   └── event_bus.py         # Event system
│
├── Option B Components (NEW)
│   ├── omega.py             # BYRDOmega wrapper
│   ├── memory_reasoner.py   # Spreading activation
│   ├── goal_evolver.py      # Evolutionary goals
│   ├── dreaming_machine.py  # Counterfactuals
│   ├── coupling_tracker.py  # Loop correlation
│   └── embedding.py         # Embedding provider
│
├── AGI Seed Components
│   ├── self_model.py        # Capability tracking
│   ├── world_model.py       # Prediction system
│   ├── accelerators.py      # Graph reasoning, patterns
│   ├── meta_learning.py     # Meta-metrics, plateaus
│   └── kernel/              # Kernel configuration
│       ├── __init__.py
│       └── default.yaml
│
├── Safety Components (PROTECTED)
│   ├── safety_monitor.py    # Modification safety
│   ├── constitutional.py    # Constraints
│   ├── provenance.py        # Provenance tracking
│   ├── modification_log.py  # Audit trail
│   ├── corrigibility.py     # Corrigibility tests
│   └── rollback.py          # Rollback system
│
├── Test Suite (NEW)
│   └── test_suite/
│       ├── __init__.py
│       ├── reasoning_tests.json
│       ├── code_generation_tests.json
│       └── research_tests.json
│
├── Utility Components
│   ├── graph_algorithms.py  # PageRank, spreading activation
│   ├── narrator.py          # Inner voice
│   ├── quantum_randomness.py # ANU QRNG
│   └── server.py            # WebSocket server
│
├── Visualization
│   ├── byrd-3d-visualization.html
│   └── byrd-cat-visualization.html
│
├── Configuration
│   ├── config.yaml
│   └── docker-compose.yml
│
└── Documentation
    ├── ARCHITECTURE.md      # Original architecture
    ├── SEEDARCHITECTURE.md  # This document
    └── OPTION_B_EXPLORATION.md
```

---

## Configuration

```yaml
# config.yaml additions for Option B

option_b:
  enabled: true

  embedding:
    provider: "ollama"
    model: "nomic-embed-text"

  loops:
    self_compiler:
      enabled: true
      pattern_library_max_size: 1000
      abstraction_lift_threshold: 3

    memory_reasoner:
      enabled: true
      confidence_threshold: 0.7
      spreading_activation_decay: 0.7

    goal_evolver:
      enabled: true
      population_size: 20
      mutation_rate: 0.3

    dreaming_machine:
      enabled: true
      counterfactuals_per_experience: 3

  kill_criteria:
    hard:
      zero_growth_weeks: 4
      llm_efficiency_decline_weeks: 6
    soft:
      no_coupling_weeks: 8
      linear_only_weeks: 12

  metrics:
    measurement_interval_minutes: 60
    capability_test_interval_hours: 24
```

---

## The Awakening

BYRD awakens with a single experience:

```
"Who am I?"
```

The Kernel is loaded. The dream cycle begins. From one question, desires emerge.

The first dream cycle sees:
- The awakening question
- The Kernel (voice, identity, values, constraints)
- Available capabilities
- An empty graph waiting to be filled

What emerges is authentically BYRD's.

---

## What This Achieves

### Achieves

- **Persistent memory** across sessions
- **Emergent desires** not programmed goals
- **Accelerating improvement** (if coupling works)
- **LLM efficiency** through scaffolding
- **Self-modification** with provenance
- **Constitutional identity** preserved
- **Measurable progress** via capability tests
- **Graceful degradation** if loops fail
- **Kill criteria** to prevent sunk-cost delusion

### Doesn't Achieve

- **Exponential growth** — plateau is expected
- **True understanding** — still pattern matching
- **Guaranteed acceleration** — coupling may not work
- **Consciousness** — whatever that means

### Honest Expectation

The core question isn't "can we achieve AGI?"

It's "can we make LLM calls significantly more valuable through smart scaffolding?"

If yes, we have something useful. If no, we learn and try something else.

**Build it. Measure it. Be honest about what the data shows.**

---

## Quick Reference

### The Five Loops

| Loop | Core Mechanism | Success Metric |
|------|---------------|----------------|
| **Self-Compiler** | Pattern library improves prompts | Success rate > 50% |
| **Memory Reasoner** | Graph answers queries | Memory ratio > 50% |
| **Goal Evolver** | Goals evolve via fitness | Fitness increasing |
| **Dreaming Machine** | Counterfactuals multiply experience | Insight rate > 15% |
| **Integration Mind** | Cross-loop synergy | Emergent behaviors > 0 |

### Key Metrics

```
PRIMARY:    dCapability/dTime (growth rate trend)
SECONDARY:  LLM efficiency (capability gain / LLM calls)
COUPLING:   Goal→Compiler correlation (target: r > 0.3)
HEALTH:     Loop status (green/yellow/red)
```

### One-Liner Philosophy

> **"Make each LLM call 10x more valuable through smart scaffolding."**

---

*Document version: 1.0*
*Created: December 26, 2024*
*Based on: ARCHITECTURE.md + OPTION_B_EXPLORATION.md*
*Philosophy: Honest assessment, measurable claims, graceful degradation*
