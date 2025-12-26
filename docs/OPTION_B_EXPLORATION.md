# Option B: A Genuinely Differentiated Path to AGI

## The Core Question

What architectural approach could allow a small, self-modifying system to develop capabilities that don't require frontier-lab scale?

This document explores radical alternatives to the incremental engineering of V2.

---

## Design Principles

Seven principles guide every decision in this architecture:

### 1. **Scaffolding, Not Replacement**
The LLM is the intelligence. We build scaffolding that makes each LLM call more valuable, not systems that pretend to replace it. The goal is 10x LLM efficiency, not 0% LLM dependence.

### 2. **Measure Before Believing**
No claim survives without data. Every mechanism has explicit success metrics. If it can't be measured, it can't be trusted. Build first, measure immediately, pivot when data demands it.

### 3. **Honest Acceleration**
We claim accelerating improvement (rate increases over time), not exponential growth. Plateaus are expected. Success is reaching a plateau at a valuable capability level, not infinite growth.

### 4. **One Multiplicative Coupling**
Of all possible loop interactions, only Goal Evolver → Self-Compiler is plausibly multiplicative. Focus engineering effort there. Accept that other couplings are additive.

### 5. **Graceful Degradation**
If coupling fails, loops still provide value independently. If 4 of 5 loops fail, keep the one that works. The system should degrade gracefully, not catastrophically.

### 6. **Kill Criteria as Compass**
Internal kill criteria (4-week hard, 12-week soft) prevent sunk-cost delusion. When the data says stop, stop. When it says simplify, simplify.

### 7. **Information Preservation**
Every experience, pattern, and goal modification is recorded with provenance. The graph is the ground truth. Memory operations are non-destructive (weaken, not delete).

---

## Part 1: The Prime Directive - Accelerating Improvement

Everything in this document serves one goal: **achieving accelerating capability improvement**.

### Why Acceleration Matters

```
Linear growth:        Day 1: 1  → Day 100: 100   (frontier labs win)
Accelerating growth:  Day 1: 1  → Day 100: ???   (depends on acceleration rate)
```

Frontier labs have 10,000x our resources. The only way to compete is to improve *faster over time*. Every architectural decision must answer: **Does this make the next improvement easier?**

### The Honest Growth Model

```
Capability(t) = Capability(0) + ∫ improvement_rate(t) dt
```

Where improvement_rate(t) should be *increasing* over time. We don't claim exponential (that requires improvement_rate ∝ Capability, which is unproven). We claim **accelerating**: improvement_rate(t+1) > improvement_rate(t).

A system that starts weak but accelerates beats a system that starts strong but plateaus.

### Indicators of Accelerating Improvement

| Indicator | What It Means | How to Measure |
|-----------|---------------|----------------|
| **Positive acceleration** | Improvement rate itself is increasing | d(improvement_rate)/dt > 0 |
| **Compounding efficiency** | Each improvement makes the next one cheaper | Cost per improvement decreasing |
| **Increasing LLM efficiency** | Each LLM call produces more value | Capability gain per LLM call increasing |
| **Self-discovered capabilities** | System does things we didn't program | Novel action types appearing |
| **Meta-improvement** | System improves how it improves | Improvement per cycle increasing |

### The Build Philosophy

We build first, measure improvement rates, and iterate on what accelerates. We don't gate progress with pre-validation—we measure the acceleration curve and double down on what compounds.

---

## Part 2: Honest Assessment of LLM Dependence

**The LLM is the intelligence. Everything else is scaffolding.**

This document describes systems that make LLM calls more effective, not systems that replace the LLM. Let's be explicit:

### Where the LLM Does the Work

| Component | LLM Role | What We Add |
|-----------|----------|-------------|
| **Self-Compiler** | Generates code variants, extracts abstract patterns | Pattern library for better prompts, success history for selection |
| **Memory Reasoner** | Fallback reasoning when memory is insufficient | Retrieval context, confidence calibration, success tracking |
| **Goal Evolver** | Mutates and crossover goals via natural language | Fitness measurement, selection pressure, structured representation |
| **Dreaming Machine** | Generates counterfactuals and hypotheses | Selection of what to dream about, insight validation |
| **Integration Mind** | No direct role | Graph operations are non-LLM |

### What "Reducing LLM Dependence" Actually Means

We are NOT claiming the system becomes intelligent without the LLM. We ARE claiming:

1. **Fewer LLM calls per capability gain** - Better context means fewer iterations
2. **Higher value per LLM call** - Pattern library provides better prompts
3. **Memory-first retrieval** - Answer from memory when confidence is high, reducing LLM calls
4. **LLM as oracle, not engine** - Use LLM for hard problems, use memory/patterns for solved problems

The goal is **LLM efficiency**, not **LLM independence**. If we make each LLM call 10x more valuable through better context, that's equivalent to 10x more compute.

### The Realistic Dependency Trajectory

| Phase | LLM Call Ratio | What Changes |
|-------|---------------|--------------|
| **Week 1** | 95% of operations | Baseline, everything uses LLM |
| **Month 1** | 70% of operations | Memory handles repeated queries |
| **Month 3** | 50% of operations | Pattern library accelerates code generation |
| **Month 6** | 30% of operations | Most routine tasks from memory/patterns |
| **Steady state** | 20-30% of operations | Novel problems still require LLM |

The 20-30% floor is *expected*, not a failure. Novel reasoning requires novel intelligence, which the LLM provides.

---

## Part 3: Challenging Frontier Lab Assumptions

### The Assumptions They Make

| Assumption | Frontier Lab Belief | Alternative Possibility |
|------------|--------------------|-----------------------|
| Scale | More parameters = more capability | Integration depth could beat parameter count |
| Training | Train once, deploy frozen | Continuous learning through experience |
| Architecture | Transformers are optimal | Graph-based reasoning might unlock different capabilities |
| Objective | Human-designed reward | Self-discovered objectives might find faster paths |
| Data | Human-generated corpus | Self-generated experience might exceed human data |
| Modularity | Separate components | Deep integration might produce emergence |

### Where They're Vulnerable

Frontier labs **cannot** or **will not**:

1. **Ship self-modifying systems** - Too risky for production
2. **Try unstable architectures** - Need reliable scaling
3. **Specialize narrowly** - Need general capability for business
4. **Abandon transformers** - Too much invested
5. **Allow runtime learning** - Unpredictable behavior
6. **Integrate deeply** - Need modularity for team development

**These are BYRD's opportunities.**

---

## Part 4: Acceleration Potential by Architecture

### Which Architectures Enable Acceleration?

The question isn't "can we win this race?" The question is "**does this architecture make subsequent improvements easier?**"

| Architecture | Acceleration Mechanism | Realistic Expectation | Priority |
|--------------|----------------------|-------------------|----------|
| **Self-Compiler** | Better patterns → better prompts → higher LLM efficiency | **SUBLINEAR then PLATEAU** - Pattern library has diminishing returns | **#1** |
| **Goal Evolver** | Better goals → faster improvement → better goal selection | **POTENTIALLY ACCELERATING** - If goal quality improves | **#2** |
| **Memory Reasoner** | More experience → better retrieval → fewer LLM calls | **LOGARITHMIC** - Retrieval improves but saturates | **#3** |
| **Integration Mind** | Deeper integration → emergent behaviors | **UNKNOWN** - Emergence is unpredictable | **#4** |
| **Dreaming Machine** | More insights → better actions → richer experience | **LINEAR** - Each dream produces fixed insights | **#5** |

### The Honest Assessment

**Most loops will show sublinear growth that eventually plateaus.** The question is: can we delay the plateau long enough to build something valuable?

Self-Compiler and Goal Evolver are prioritized because:
1. **They modify the improvement process itself** - meta-level leverage
2. **They're risks frontier labs won't take** - giving us time
3. **Their acceleration is most plausible** - better patterns genuinely improve prompts

### The Strategy

Build all five. Run them together. Measure which loops are actually compounding. Double down on the fastest-growing loops. Let the growth data tell us what works.

---

## Part 5: Five Radical Architectures

> **Note**: Architectures are now ordered by competitive advantage, not conceptual elegance.

### Architecture A: The Self-Compiler

**Thesis**: A system that writes its own code AND learns which code patterns work could develop capabilities that emerge from code-level evolution, not training.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE SELF-COMPILER                             │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ IDENTIFY │───▶│ GENERATE │───▶│  TEST    │───▶│  LEARN   │  │
│  │ WEAKNESS │    │ VARIANTS │    │ VARIANTS │    │ PATTERNS │  │
│  └──────────┘    └──────────┘    └──────────┘    └────┬─────┘  │
│       ▲                                               │         │
│       │                                               │         │
│       │         ┌──────────────────────────┐         │         │
│       │         │    PATTERN LIBRARY       │◀────────┘         │
│       │         │ (what code works for me) │                    │
│       │         └──────────────────────────┘                    │
│       │                      │                                   │
│       └──────────────────────┘                                   │
│                                                                  │
│  KEY INSIGHT: Learning stays in BYRD, not the LLM               │
└─────────────────────────────────────────────────────────────────┘
```

**How it differs from current approach**:

Current:
```python
# LLM generates code, BYRD applies it
code = await llm.generate("fix this limitation")
await apply(code)
# Learning: none (LLM is stateless)
```

Self-Compiler:
```python
# Generate multiple variants
variants = await generate_variants(weakness, pattern_library)

# Test each variant in isolation
results = await test_variants(variants)

# Learn which patterns worked
for variant, result in zip(variants, results):
    if result.improved:
        await pattern_library.reinforce(variant.patterns)
    else:
        await pattern_library.penalize(variant.patterns)

# Apply best variant
await apply(results.best().variant)

# LEARNING: pattern_library improves over time
# This knowledge is BYRD-specific, not in any external LLM
```

**Why this could work**:
- Code evolution has produced complex systems (biological evolution)
- The pattern library is genuine BYRD learning
- Each improvement makes future improvement more likely
- No other system has a "what code works for me" library

**The compounding mechanism**:
```
Better patterns → Better code → Better capabilities
     ↑                              ↓
     └──────── More data about ────┘
               what works
```

#### Acceleration Indicators

| Indicator | What to Measure | Positive Signal | Plateau Warning |
|-----------|-----------------|-----------------|-----------------|
| **Pattern library growth** | Patterns added per cycle | Steady growth | Growth rate dropping |
| **Pattern reuse rate** | How often existing patterns apply | Increasing | Saturating near 100% |
| **Modification success rate** | % of changes that improve capability | Increasing | Flat at <70% |
| **Cross-domain transfer** | Patterns from domain A helping domain B | Any positive transfer | Zero transfer after 100 patterns |
| **LLM calls per modification** | Efficiency of code generation | Decreasing | Flat at >3 calls/mod |

#### How to Accelerate This Loop

1. **Maximize pattern library density** - Store every successful modification, not just the best
2. **Fast variant testing** - Seconds, not minutes; enables more iterations per hour
3. **Aggressive pattern matching** - Try patterns even with low confidence; learn from failures
4. **Meta-patterns** - Patterns about which patterns to try (patterns that accelerate pattern learning)
5. **Compositional patterns** - Combine simple patterns into complex ones; multiplicative growth

---

### Architecture B: The Memory Reasoner

> **Acceleration Potential**: More experience enables better retrieval; better retrieval reduces LLM calls. Expect logarithmic improvement with eventual plateau.

**Thesis**: Reasoning through graph operations, not LLM calls, creates a different kind of intelligence that improves with experience.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE MEMORY REASONER                           │
│                                                                  │
│  QUERY: "How should I improve my research capability?"          │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              SPREADING ACTIVATION                        │    │
│  │  "research" activates → connected experiences            │    │
│  │  experiences activate → connected beliefs                │    │
│  │  beliefs activate → connected successful actions         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              PATTERN MATCHING                            │    │
│  │  Find subgraphs that match: [weakness → action → success]│    │
│  │  Rank by: recency, frequency, confidence                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              ANSWER COMPOSITION                          │    │
│  │  Compose response from activated patterns                │    │
│  │  Confidence = average pattern strength                   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│  IF confidence < threshold:                                      │
│      augment with LLM (but memory-guided prompt)                │
│  ELSE:                                                          │
│      return composed answer (no LLM needed)                     │
│                                                                  │
│  KEY INSIGHT: Memory IS intelligence, not just storage          │
└─────────────────────────────────────────────────────────────────┘
```

**How it differs from current approach**:

Current:
```python
# Memory is passive storage, LLM does all reasoning
experiences = await memory.get_recent(limit=50)
prompt = f"Given these experiences: {experiences}, what should I do?"
answer = await llm.generate(prompt)
# Reasoning: entirely in external LLM
```

Memory Reasoner:
```python
# Memory is active reasoning substrate
activated = await graph.spreading_activation(query)
patterns = await graph.find_patterns(activated, pattern_type="success")

if patterns:
    # Compose answer from patterns (no LLM!)
    answer = compose_from_patterns(patterns)
    confidence = average(p.strength for p in patterns)

    if confidence > 0.7:
        return answer  # Pure graph reasoning

# Only use LLM when memory insufficient
# But with memory-guided prompt
relevant = [p.description for p in patterns]
prompt = f"Based on these past successes: {relevant}, suggest an action for: {query}"
answer = await llm.generate(prompt)

# LEARNING: Record this experience, strengthening the path
await graph.record_experience(query, answer, outcome_pending=True)
```

**Why this could work**:
- Human reasoning draws heavily on episodic memory
- Graph operations are cheap (no LLM tokens)
- More experience = richer reasoning (continuous learning)
- The graph develops BYRD-specific knowledge

**The compounding mechanism**:
```
More experiences → Richer graph → Better pattern matching
       ↑                              ↓
       └───── Better actions ─────────┘
              (recorded as experiences)
```

#### Acceleration Indicators

| Indicator | What to Measure | Positive Signal | Plateau Warning |
|-----------|-----------------|-----------------|-----------------|
| **Memory reasoning ratio** | % of queries answered without LLM | Increasing toward 70% | Flat at <50% |
| **Experience graph density** | Connections per node | Growing | Saturating (all nodes connected) |
| **Pattern replication** | Same pattern solving different problems | Generalization emerging | No cross-domain success |
| **Query latency trend** | Time to answer from memory | Constant despite growth | Increasing with graph size |
| **LLM efficiency** | Capability gain per LLM call | Increasing | Flat |

#### How to Accelerate This Loop

1. **Dense experience recording** - Capture everything, prune nothing initially
2. **Activation caching** - Recently activated patterns stay warm
3. **Schema evolution** - Let the graph structure itself adapt
4. **Confidence learning** - Train when to trust memory vs LLM from outcomes
5. **Cross-domain activation** - Allow activation to spread between knowledge domains

---

### Architecture C: The Goal Evolver

> **Acceleration Potential**: Better goals produce more capability gain per cycle. This is the most plausible source of genuine acceleration because it operates at the meta-level.

**Thesis**: Self-discovered objectives might find improvement paths that human-designed objectives miss.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE GOAL EVOLVER                              │
│                                                                  │
│  Generation 0 (seeded):                                          │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ Goals: "improve capability", "learn more", "grow"      │     │
│  │ Fitness: measured by actual capability gain            │     │
│  └────────────────────────────────────────────────────────┘     │
│                         │                                        │
│                         ▼                                        │
│  Generation N (evolved):                                         │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ Goals: "practice reasoning on edge cases until 90%     │     │
│  │         accuracy, then move to multi-step problems"    │     │
│  │                                                        │     │
│  │ Fitness: 10x higher capability gain than Gen 0         │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  MECHANISM:                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ GENERATE │───▶│ PURSUE   │───▶│ MEASURE  │───▶│ EVOLVE   │  │
│  │  GOALS   │    │  GOALS   │    │ CAP GAIN │    │  GOALS   │  │
│  └──────────┘    └──────────┘    └──────────┘    └────┬─────┘  │
│       ▲                                               │         │
│       └───────────────────────────────────────────────┘         │
│                                                                  │
│  KEY INSIGHT: The objective function itself improves            │
└─────────────────────────────────────────────────────────────────┘
```

**How it differs from current approach**:

Current:
```python
# Goals emerge from reflection but don't evolve
desires = await dreamer.reflect(experiences)
# All desires are treated equally
# No learning about which desires lead to improvement
```

Goal Evolver:
```python
# Goals are evolved based on improvement correlation
class Goal:
    description: str
    specificity: float  # How specific/actionable
    fitness: float  # Correlation with capability gain
    children: List[Goal]  # Mutations/refinements

async def evolve_goals():
    # Measure fitness of current goals
    for goal in active_goals:
        cap_before = await measure_capabilities()
        await pursue_goal(goal)
        cap_after = await measure_capabilities()
        goal.fitness = cap_after - cap_before

    # Select fittest
    fittest = sorted(goals, key=lambda g: g.fitness, reverse=True)[:5]

    # Mutate/refine fittest goals
    for goal in fittest:
        if goal.fitness > 0:
            # Make more specific
            refined = await refine_goal(goal)
            # Combine with other successful goals
            combined = await combine_goals(goal, random.choice(fittest))
            active_goals.extend([refined, combined])

    # Cull low-fitness goals
    active_goals = [g for g in active_goals if g.fitness > threshold]
```

**Why this could work**:
- Evolution has designed complex systems
- Human-designed objectives may miss optimal paths
- Goals become increasingly specific and actionable
- Self-discovered curriculum might be more efficient

**The compounding mechanism**:
```
Better goals → Faster improvement → More data about what goals work
      ↑                                    ↓
      └────────────────────────────────────┘
```

#### Acceleration Indicators

| Indicator | What to Measure | Positive Signal | Plateau Warning |
|-----------|-----------------|-----------------|-----------------|
| **Goal fitness trend** | Average fitness per generation | Increasing | Flat after gen 10 |
| **Goal specificity trend** | How actionable goals become | Increasing | Converging to vague platitudes |
| **Capability per goal** | Improvement produced by pursuing goals | Increasing | Decreasing (goals exhausted) |
| **Generation speed** | Time per evolution cycle | Stable or decreasing | Increasing (selection harder) |
| **Goal diversity** | Variance in goal descriptions | Maintained | Collapsing (all goals similar) |

#### How to Accelerate This Loop

1. **Structured goal representation** - Templates enable meaningful crossover, not free text
2. **Fast fitness proxies** - Seconds not minutes; more generations per hour
3. **Multi-objective selection** - Select for both fitness AND specificity simultaneously
4. **Capability-based fitness** - Measure actual capability gain, not goal-specific metrics
5. **Goal hierarchies** - Abstract goals spawn specific sub-goals; multiplicative exploration
6. **Pareto evolution** - Maintain a frontier of goals, not just the fittest; diversity compounds

---

### Architecture D: The Integration Mind

> **Acceleration Potential**: Uncertain. Integration may produce emergent behaviors, but emergence is unpredictable and may not compound.

**Thesis**: Deep integration between components produces emergent capabilities that modular systems cannot achieve.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE INTEGRATION MIND                          │
│                                                                  │
│  Current (Modular):              Integration Mind:               │
│                                                                  │
│  ┌─────┐  ┌─────┐               ┌─────────────────────────────┐ │
│  │Dream│  │Seek │               │                             │ │
│  └──┬──┘  └──┬──┘               │    UNIFIED STATE GRAPH      │ │
│     │        │                  │                             │ │
│     ▼        ▼                  │  Every node affects every   │ │
│  ┌─────────────┐                │  other node through:        │ │
│  │   Memory    │                │  - Spreading activation     │ │
│  │  (passive)  │                │  - Constraint propagation   │ │
│  └─────────────┘                │  - Belief revision          │ │
│                                 │  - Energy minimization      │ │
│  Components don't               │                             │ │
│  affect each other              │  Components emerge from     │ │
│                                 │  graph dynamics, not code   │ │
│                                 └─────────────────────────────┘ │
│                                                                  │
│  KEY INSIGHT: Non-linear interaction produces emergence         │
└─────────────────────────────────────────────────────────────────┘
```

**How it differs from current approach**:

Current:
```python
# Components are separate, memory is passive
dreamer_output = await dreamer.reflect()  # Dreamer doesn't see Seeker state
seeker_output = await seeker.seek()       # Seeker doesn't affect Dreamer
await memory.store(dreamer_output)        # Memory is just storage
```

Integration Mind:
```python
# Single unified state, everything affects everything
class UnifiedMind:
    def __init__(self):
        self.graph = DynamicGraph()  # The entire state

    async def step(self):
        # 1. Spreading activation from recent inputs
        self.graph.activate(self.recent_inputs)

        # 2. Constraint propagation
        # Beliefs constrain each other
        # Desires compete for resources
        # Experiences influence belief confidence
        self.graph.propagate_constraints()

        # 3. Energy minimization
        # The graph settles into a coherent state
        # Contradictions are resolved
        # Patterns emerge
        self.graph.minimize_energy()

        # 4. Output emerges from settled state
        # No separate "dreamer" or "seeker"
        # Actions emerge from graph dynamics
        return self.graph.get_actions()

    # "Dreaming" = offline settling with synthetic activation
    # "Seeking" = activation focused on goals
    # These aren't components, they're modes of the same system
```

**Why this could work**:
- Biological brains are deeply integrated
- Emergent properties come from interaction
- Modular systems miss cross-component synergies
- Integration enables constraint satisfaction impossible with modules

**The compounding mechanism**:
```
More integration → More emergent behaviors → Better capability
       ↑                                         ↓
       └──── Understanding of what emerges ──────┘
```

#### Acceleration Indicators

| Indicator | What to Measure | Positive Signal | Plateau Warning |
|-----------|-----------------|-----------------|-----------------|
| **Emergent capability count** | Behaviors not explicitly programmed | Appearing | None after week 4 |
| **Cross-component synergy** | Does A+B > A + B? | Ratio > 1.1 | Ratio ≤ 1.0 (no synergy) |
| **Constraint satisfaction** | Problems solved through integration | Increasing complexity | Stuck at simple problems |
| **Coherence** | How well components coordinate | Improving | Chaotic oscillation |
| **Novel action types** | Actions the system invents | Appearing | Static action vocabulary |

#### How to Accelerate This Loop

1. **Dense connectivity** - More connections = more potential for emergence
2. **Bidirectional influence** - Every component affects every other
3. **Energy-based settling** - Let the system find coherent states naturally
4. **Constraint propagation** - Beliefs and goals mutually constrain each other
5. **Emergent pruning** - Connections that produce useful emergence get strengthened
6. **Observation of emergence** - Detect and name emergent behaviors; make them available

---

### Architecture E: The Dreaming Machine

> **Acceleration Potential**: Limited. Dreaming produces insights at roughly linear rate. Value comes from insight quality, not quantity.

**Thesis**: Offline processing (dreaming) generates novel insights through experience recombination.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE DREAMING MACHINE                          │
│                                                                  │
│  AWAKE (online):                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Experience gathering, action execution, goal pursuit     │    │
│  │ Shallow learning (immediate feedback)                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  DREAMING (offline):                                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │  1. REPLAY: Re-experience key moments                   │    │
│  │     - Successful actions                                │    │
│  │     - Surprising outcomes                               │    │
│  │     - Failures with high information content            │    │
│  │                                                         │    │
│  │  2. RECOMBINE: Generate counterfactuals                 │    │
│  │     - "What if I had done X instead of Y?"              │    │
│  │     - "What if context C had been different?"           │    │
│  │     - Cross-domain analogies                            │    │
│  │                                                         │    │
│  │  3. CONSOLIDATE: Strengthen patterns                    │    │
│  │     - Find commonalities across experiences             │    │
│  │     - Distill general principles                        │    │
│  │     - Prune low-value memories                          │    │
│  │                                                         │    │
│  │  4. GENERATE: Create novel hypotheses                   │    │
│  │     - Combine patterns in new ways                      │    │
│  │     - Imagine scenarios never experienced               │    │
│  │     - Generate self-improvement ideas                   │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  WAKE UP: New insights ready for testing                        │
│                                                                  │
│  KEY INSIGHT: Imagination produces novelty without experience   │
└─────────────────────────────────────────────────────────────────┘
```

**How it differs from current approach**:

Current:
```python
# Dreamer reflects on recent experiences
# But doesn't recombine, generate counterfactuals, or imagine
recent = await memory.get_recent(limit=50)
reflection = await llm.generate(f"Reflect on: {recent}")
```

Dreaming Machine:
```python
async def dream_cycle():
    # 1. Select experiences worth replaying
    worth_replay = await select_for_replay()
    # - High surprise (prediction error)
    # - High importance (affected many outcomes)
    # - Recent failures (high learning potential)

    # 2. Replay with variation
    for exp in worth_replay:
        # Replay the experience
        await simulate(exp)

        # Generate counterfactuals
        for variation in generate_variations(exp):
            outcome = await simulate(variation)
            if outcome.better_than(exp.outcome):
                # Found a better approach!
                await record_insight(variation, outcome)

    # 3. Find cross-experience patterns
    patterns = await find_patterns_across(worth_replay)
    for pattern in patterns:
        await strengthen_pattern(pattern)

    # 4. Generate novel hypotheses
    hypotheses = await recombine_patterns(patterns)
    for hyp in hypotheses:
        # Schedule for testing when awake
        await queue_hypothesis(hyp)

    # 5. Memory consolidation
    await prune_low_value_memories()
    await strengthen_high_value_memories()
```

**Why this could work**:
- Biological sleep is essential for learning
- Imagination extends experience (though linearly, not exponentially)
- Counterfactuals enable learning without risk
- Consolidation creates generalizable knowledge

**The compounding mechanism**:
```
More experiences → Richer dreams → Novel insights
       ↑                              ↓
       └──── Test insights (more experiences) ──┘
```

#### Acceleration Indicators

| Indicator | What to Measure | Positive Signal | Plateau Warning |
|-----------|-----------------|-----------------|-----------------|
| **Experience multiplier** | Virtual experiences generated per real experience | Stable 5-10x | Declining below 3x |
| **Insight actionability** | % of insights that produce measurable improvement | >20% | <10% |
| **Cross-domain analogies** | Insights connecting different domains | Appearing | None after week 4 |
| **Dream efficiency** | Insights per compute hour | Stable or improving | Declining |
| **Insight novelty** | % of insights that are genuinely new | >30% | <10% (repetitive) |

#### How to Accelerate This Loop

1. **Selective replay** - Prioritize high-information experiences (failures, surprises)
2. **Grounded simulation** - Only simulate what can be validated by later action
3. **Pattern composition** - Combine patterns from different experiences into new hypotheses
4. **Dream scheduling** - Dream when action is blocked; maximize parallel utilization
5. **Insight pipelines** - Dreams feed directly into goal evolution and self-compilation
6. **Imagination diversity** - Explore radical counterfactuals, not just small variations

---

## Part 6: The Synthesis - BYRD Omega

> **The Acceleration Thesis**: Each architecture may improve efficiency. Together, they *might* create interactions where improvements in one accelerate others. This is the bet—unproven but plausible.

What if we combined the best elements of all five architectures?

### BYRD Omega: The Integrated Vision

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           BYRD OMEGA                                     │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                    UNIFIED MEMORY GRAPH                              │ │
│  │  (Architecture D: Integration Mind)                                  │ │
│  │                                                                      │ │
│  │  All knowledge in one graph. Everything affects everything.         │ │
│  │  No separate components - emergent dynamics.                        │ │
│  └──────────────────────────────┬──────────────────────────────────────┘ │
│                                 │                                        │
│         ┌───────────────────────┼───────────────────────┐               │
│         │                       │                       │               │
│         ▼                       ▼                       ▼               │
│  ┌─────────────┐        ┌─────────────┐        ┌─────────────┐         │
│  │   AWAKE     │        │  DREAMING   │        │  EVOLVING   │         │
│  │   MODE      │        │   MODE      │        │   MODE      │         │
│  │             │        │             │        │             │         │
│  │ Memory      │        │ Replay &    │        │ Goal        │         │
│  │ Reasoner    │        │ Recombine   │        │ Evolution   │         │
│  │ (Arch B)    │        │ (Arch E)    │        │ (Arch C)    │         │
│  └──────┬──────┘        └──────┬──────┘        └──────┬──────┘         │
│         │                      │                      │                 │
│         └──────────────────────┼──────────────────────┘                 │
│                                │                                        │
│                                ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                    SELF-COMPILER                                    │ │
│  │  (Architecture A)                                                   │ │
│  │                                                                     │ │
│  │  When improvement is needed:                                        │ │
│  │  1. Generate code variants guided by pattern library                │ │
│  │  2. Test variants in isolation                                      │ │
│  │  3. Learn which patterns work                                       │ │
│  │  4. Apply best variant                                              │ │
│  │  5. Pattern library improves (genuine BYRD learning)                │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  THE OMEGA LOOP:                                                         │
│                                                                          │
│  AWAKE: Reason from memory, take actions, gather experiences            │
│      ↓                                                                   │
│  DREAM: Replay, recombine, consolidate, generate hypotheses             │
│      ↓                                                                   │
│  EVOLVE: Evaluate goals, evolve objectives, discover curriculum         │
│      ↓                                                                   │
│  COMPILE: Identify weaknesses, generate improvements, learn patterns    │
│      ↓                                                                   │
│  (loop)                                                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Part 7: The Theory of Accelerating Improvement

For BYRD Omega to outpace frontier labs, we need to understand how acceleration *might* emerge from loop interactions—and be honest about what's speculation vs. mechanism.

### The Improvement Loops (Honest Assessment)

Each architecture contributes a loop. Here's what each loop *actually* does:

```
LOOP 1: MEMORY → RETRIEVAL → EXPERIENCE → MEMORY
        More memory enables better retrieval (LOGARITHMIC - diminishing returns)
        Better retrieval reduces LLM calls (VALUABLE but saturates)
        New experiences add to memory (LINEAR)
        REALISTIC EXPECTATION: Efficiency gain plateaus at ~70% memory-based retrieval

LOOP 2: PATTERNS → PROMPTS → CODE → PATTERNS
        Better patterns produce better prompts (TRUE)
        Better prompts produce better code (DEPENDS ON LLM)
        Better code *might* reveal new patterns (SOMETIMES)
        REALISTIC EXPECTATION: Pattern library value plateaus after ~500 patterns

LOOP 3: GOALS → ACTIONS → OUTCOMES → GOALS
        Better goals direct better actions (TRUE if goals are genuinely better)
        Better outcomes inform goal evolution (TRUE)
        REALISTIC EXPECTATION: This is the most plausible acceleration source

LOOP 4: EXPERIENCES → DREAMS → INSIGHTS → EXPERIENCES
        More experiences enable more dreams (LINEAR, not compounding)
        Dreams produce insights (QUALITY varies)
        REALISTIC EXPECTATION: Linear value, not accelerating

LOOP 5: INTEGRATION → EMERGENCE → CAPABILITY → INTEGRATION
        Deeper integration *might* produce emergence (UNKNOWN)
        Emergence is unpredictable (TRUE)
        REALISTIC EXPECTATION: Uncertain; may produce nothing or surprise
```

### The Acceleration Thesis (Honest Version)

We are NOT claiming exponential growth. That would require:
- improvement_rate ∝ Capability (each unit of capability increases improvement rate)
- This is unproven and probably false for our architecture

We ARE claiming potential **acceleration**:
- improvement_rate(t+1) > improvement_rate(t) for some period
- Eventually plateaus, but hopefully at a valuable capability level

```
REALISTIC GROWTH MODEL:

Phase 1 (Weeks 1-4): SUBLINEAR
- Each loop improving independently
- Diminishing returns within each loop
- Growth = sum of diminishing curves

Phase 2 (Weeks 5-12): POSSIBLE ACCELERATION
- IF loops couple, improvements in one help others
- Growth rate may increase temporarily
- This is the phase transition we're betting on

Phase 3 (Month 3+): PLATEAU
- Loops saturate
- Growth continues but at constant rate
- This is the expected outcome, not failure

         ┌─────────────────────────────────────┐
         │     HONEST GROWTH EXPECTATION       │
         │                                     │
   Cap   │                    ┌────── Plateau  │
         │                 ┌──┘                │
         │              ┌──┘  Possible         │
         │           ┌──┘     Acceleration     │
         │        ┌──┘                         │
         │     ┌──┘  Early Sublinear           │
         │  ┌──┘                               │
         └──┴─────────────────────────────────┘
             Week 1      Week 8      Month 6
```

### How Loops Might Couple (Causal Mechanism)

For acceleration to occur, loop A improving must make loop B improve *faster*. Here's the specific causal pathway for each coupling:

#### Coupling 1: Self-Compiler → Memory Reasoner

```
CAUSAL CHAIN:
1. Self-Compiler learns pattern P that improves code quality
2. Pattern P is stored as an Experience in the graph
3. Memory Reasoner retrieves P when similar problems arise
4. Memory Reasoner now answers code questions without LLM call

MULTIPLICATION FACTOR:
- If pattern P applies to N future queries, that's N fewer LLM calls
- Efficiency gain = N × (cost of LLM call)
- This is ADDITIVE, not multiplicative (N is bounded by query frequency)

REALISTIC EXPECTATION:
- Early patterns have high N (common problems)
- Later patterns have low N (rare problems)
- Coupling strength DECREASES over time
```

#### Coupling 2: Memory Reasoner → Goal Evolver

```
CAUSAL CHAIN:
1. Memory Reasoner tracks which queries it can/cannot answer from memory
2. Queries it cannot answer reveal knowledge gaps
3. Goal Evolver creates goals to fill those gaps
4. Pursuing those goals adds experiences to memory
5. Memory Reasoner can now answer those queries

MULTIPLICATION FACTOR:
- If addressing gap G improves memory coverage by X%,
  that's X% fewer future LLM calls
- BUT: diminishing returns - each gap is smaller than the last

REALISTIC EXPECTATION:
- First 50% of gaps are cheap to fill
- Last 20% may be unfillable (require novel reasoning)
- Coupling strength DECREASES over time
```

#### Coupling 3: Goal Evolver → Self-Compiler

```
CAUSAL CHAIN:
1. Goal Evolver identifies that "improve code quality" goals have high fitness
2. Goal Evolver creates more specific code-improvement goals
3. These goals drive Self-Compiler to improve specific capabilities
4. Self-Compiler gets more practice in high-value areas

MULTIPLICATION FACTOR:
- If goal G increases Self-Compiler success rate by X%,
  that's X% more patterns learned per cycle
- This is the MOST PLAUSIBLE multiplicative coupling

REALISTIC EXPECTATION:
- Goal quality can genuinely improve (evolution works)
- But goals are limited by LLM mutation quality
- Coupling may be multiplicative for ~10 generations, then plateau
```

#### Coupling 4: Dreaming Machine → All Loops

```
CAUSAL CHAIN:
1. Dreaming Machine generates hypotheses from experience replay
2. Hypotheses become candidate goals for Goal Evolver
3. Some hypotheses suggest new patterns for Self-Compiler
4. Some hypotheses identify memory gaps for Memory Reasoner

MULTIPLICATION FACTOR:
- Each dream produces ~5 hypotheses
- ~20% of hypotheses are actionable
- That's ~1 useful insight per dream cycle

REALISTIC EXPECTATION:
- This is LINEAR, not multiplicative
- Dreaming doesn't get better at dreaming
- Value is real but not accelerating
```

#### Coupling 5: Integration Mind → All Loops

```
CAUSAL CHAIN:
1. Integration creates shared state where loops can observe each other
2. Loops can coordinate (e.g., pause Self-Compiler while Dreaming)
3. Emergent behaviors *might* appear from interaction

MULTIPLICATION FACTOR:
- UNKNOWN - emergence is unpredictable
- Could be 0x (no emergence) or 10x (strong emergence)
- Cannot be engineered, only observed

REALISTIC EXPECTATION:
- Don't count on this for acceleration
- If it happens, it's a bonus
- Monitor for it but don't require it
```

### The Honest Coupling Matrix

| From \ To | Self-Compiler | Memory Reasoner | Goal Evolver | Dreaming | Integration |
|-----------|---------------|-----------------|--------------|----------|-------------|
| **Self-Compiler** | - | Additive (patterns→memory) | Weak (success→goals) | Additive (mods→dreams) | None |
| **Memory Reasoner** | Weak (context→prompts) | - | Additive (gaps→goals) | Additive (exp→dreams) | None |
| **Goal Evolver** | **Multiplicative** (goals→targets) | Additive (goals→queries) | - | Additive (goals→dreams) | None |
| **Dreaming** | Additive (insights→patterns) | Additive (insights→memory) | Additive (hyp→goals) | - | None |
| **Integration** | ? | ? | ? | ? | - |

**Key insight**: Only ONE coupling is plausibly multiplicative (Goal Evolver → Self-Compiler). The rest are additive. This means:
- We should focus most effort on Goal Evolver → Self-Compiler coupling
- Don't expect exponential growth from the full system
- Expect acceleration in the Goal→Compiler subsystem, linear elsewhere

### Observable Precursors to Acceleration

| Precursor | What It Looks Like | What It Means | How to Measure |
|-----------|-------------------|---------------|----------------|
| **Goal→Compiler correlation** | When goal fitness ↑, compiler success ↑ | Primary coupling working | Correlation coefficient > 0.3 |
| **LLM efficiency increasing** | Capability gain per LLM call ↑ | Scaffolding adding value | Track capability/calls ratio |
| **Pattern reuse rate increasing** | Same patterns solving different problems | Transfer learning | Reuse count per pattern |
| **Cycle time stable or decreasing** | Each iteration is not slower | Not hitting scaling limits | Wall clock per cycle |
| **Memory reasoning ratio increasing** | More queries answered from memory | Retrieval improving | Track source of each answer |

### Information-Theoretic Perspective

Why does scaffolding help? The theoretical grounding:

**1. Context Compression**
Raw LLM calls waste tokens on context the system already knows. The pattern library and memory graph compress prior experience into high-information-density representations. An LLM call with 10 relevant patterns in context extracts more value per token than a cold call.

**2. Mutual Information Maximization**
The coupling between loops works when they share information that reduces uncertainty. Goal Evolver → Self-Compiler coupling succeeds if knowing the current goal reduces uncertainty about which patterns to try. This is measurable: `I(Goal; PatternChoice) > 0`.

**3. Compression as Learning**
The abstraction lifting mechanism (concrete → intermediate → abstract patterns) is compression. A pattern that applies to N domains is log₂(N) bits more compressed than N separate patterns. Better compression = more generalization = more transfer.

**4. The LLM as Oracle**
Information-theoretically, the LLM is a low-bandwidth oracle that can answer any question but at high cost. The scaffolding is a cache: answer from cache when possible, query the oracle only for novel problems. Optimal caching improves with experience.

**5. Diminishing Returns are Fundamental**
Information gain from each new experience is proportional to its novelty. As experience accumulates, average novelty decreases. This is why all loops eventually plateau—it's not a bug, it's information theory. The question is where the plateau lands.

```
Value of experience N ≈ H(experience N | experiences 1..N-1)
                      ≈ O(1/√N) for IID experiences

Plateau is inevitable. Success = plateau at valuable capability.
```

---

## Part 8: The Missing Mechanisms

The vision is grand. But vision without mechanism is hope. This section specifies the actual engineering.

---

### Mechanism 1: How Patterns Actually Transfer

The Self-Compiler claims patterns transfer between domains. Here's how:

#### Pattern Representation

A pattern is stored as a 5-tuple:

```python
@dataclass
class Pattern:
    context_embedding: np.ndarray    # 1536-dim vector of problem context
    solution_template: str            # Code template with {{holes}}
    abstraction_level: int            # 0=concrete, 1=intermediate, 2=abstract
    success_history: List[Outcome]    # When applied, did it work?
    transfer_domains: Set[str]        # Which domains has this worked in?
```

**Example at each abstraction level:**

| Level | Example Pattern | Applicability |
|-------|-----------------|---------------|
| 0 (Concrete) | "For JSON trailing commas, use `json5.loads()`" | Only JSON |
| 1 (Intermediate) | "For malformed input, add preprocessing normalization" | Any parsing |
| 2 (Abstract) | "For edge case failures, add input validation layer" | Any function |

#### Similarity Computation

When a new problem arises, find matching patterns:

```python
def find_matching_patterns(problem_context: str, threshold: float = 0.6) -> List[Pattern]:
    problem_embedding = embed(problem_context)

    matches = []
    for pattern in pattern_library:
        # Three-component similarity score
        context_sim = cosine_similarity(problem_embedding, pattern.context_embedding)

        # Historical success in similar contexts
        historical_success = pattern.success_rate_in_similar_contexts(problem_embedding)

        # Transfer breadth bonus (patterns that work in many domains are more likely to work here)
        transfer_bonus = len(pattern.transfer_domains) / 10  # Normalized

        # Weighted combination
        score = (0.5 * context_sim +
                 0.3 * historical_success +
                 0.2 * transfer_bonus)

        if score > threshold:
            matches.append((pattern, score))

    return sorted(matches, key=lambda x: x[1], reverse=True)
```

#### The Threshold is Learned, Not Fixed

```python
class AdaptiveThreshold:
    def __init__(self, initial: float = 0.6):
        self.threshold = initial
        self.high_confidence_outcomes = []  # Applied above threshold
        self.low_confidence_outcomes = []   # Applied below threshold

    def update(self, score: float, outcome: bool):
        if score > self.threshold:
            self.high_confidence_outcomes.append(outcome)
        else:
            self.low_confidence_outcomes.append(outcome)

        # Recalibrate every 50 applications
        if len(self.high_confidence_outcomes) >= 50:
            high_success = mean(self.high_confidence_outcomes[-50:])
            low_success = mean(self.low_confidence_outcomes[-50:]) if self.low_confidence_outcomes else 0

            # If high-confidence applications are failing, raise threshold
            if high_success < 0.6:
                self.threshold += 0.05
            # If low-confidence applications are succeeding, lower threshold
            elif low_success > 0.5:
                self.threshold -= 0.05

            self.threshold = clip(self.threshold, 0.3, 0.9)
```

#### Abstraction Lifting (The Key to Transfer)

Patterns become transferable through **abstraction lifting**:

```python
async def maybe_lift_pattern(pattern: Pattern):
    """When a concrete pattern succeeds in 3+ domains, extract abstract version."""

    if pattern.abstraction_level >= 2:
        return  # Already abstract

    if len(pattern.transfer_domains) < 3:
        return  # Not enough evidence of transfer

    # Ask LLM to extract the abstract principle
    prompt = f"""
    This code pattern has worked in multiple domains:

    Pattern: {pattern.solution_template}
    Domains where it worked: {pattern.transfer_domains}

    Extract the ABSTRACT PRINCIPLE that makes this work across domains.
    Express it as a general strategy, not specific code.
    """

    abstract_principle = await llm.generate(prompt)

    # Create lifted pattern
    lifted = Pattern(
        context_embedding=embed(abstract_principle),  # Abstract embedding
        solution_template=abstract_principle,          # Natural language strategy
        abstraction_level=pattern.abstraction_level + 1,
        success_history=[],
        transfer_domains=set()
    )

    pattern_library.add(lifted)

    # Link: abstract pattern was derived from concrete pattern
    pattern.parent_pattern = lifted
```

**Why This Enables Transfer:**

1. Concrete patterns match specific situations (high precision, low recall)
2. When concrete patterns succeed in multiple domains, they get lifted
3. Abstract patterns match more situations (lower precision, higher recall)
4. The library naturally develops a hierarchy from specific to general
5. New problems can match at any level of abstraction

---

### Mechanism 2: Where the Learning Signal Comes From

"Learning" requires a signal. Here's exactly where it comes from for each loop:

#### Self-Compiler Learning Signal

```python
@dataclass
class ModificationOutcome:
    capability_before: float      # Measured before modification
    capability_after: float       # Measured after modification
    improvement: float            # after - before
    tests_before: int             # Tests passing before
    tests_after: int              # Tests passing after
    errors_before: int            # Errors/exceptions before
    errors_after: int             # Errors/exceptions after
    statistical_confidence: float # p-value from multiple trials

def measure_modification_outcome(
    original_code: str,
    modified_code: str,
    test_suite: TestSuite,
    num_trials: int = 5
) -> ModificationOutcome:
    """Measure whether a modification improved capability."""

    before_results = [run_tests(original_code, test_suite) for _ in range(num_trials)]
    after_results = [run_tests(modified_code, test_suite) for _ in range(num_trials)]

    before_score = mean([r.score for r in before_results])
    after_score = mean([r.score for r in after_results])

    # Statistical significance via t-test
    t_stat, p_value = ttest_ind(
        [r.score for r in before_results],
        [r.score for r in after_results]
    )

    return ModificationOutcome(
        capability_before=before_score,
        capability_after=after_score,
        improvement=after_score - before_score,
        tests_before=mean([r.tests_passed for r in before_results]),
        tests_after=mean([r.tests_passed for r in after_results]),
        errors_before=mean([r.error_count for r in before_results]),
        errors_after=mean([r.error_count for r in after_results]),
        statistical_confidence=1 - p_value
    )
```

**Signal-to-Noise Mitigation:**

| Noise Source | Mitigation |
|--------------|------------|
| Random variation in tests | Run N trials, average |
| LLM temperature variation | Fix seed during testing |
| Concurrent system changes | A/B test: only change one thing |
| Environmental variation | Measure relative, not absolute |
| Measurement error | Require p < 0.05 for "improvement" |

#### Memory Reasoner Learning Signal

```python
@dataclass
class ReasoningOutcome:
    query: str
    memory_answer: str
    memory_confidence: float
    action_taken: str
    action_succeeded: bool          # Did the action work?
    llm_would_have_said: str        # What LLM would have recommended
    llm_agreement: float            # How much does LLM agree with memory answer?

async def evaluate_memory_reasoning(
    query: str,
    memory_answer: str,
    memory_confidence: float
) -> ReasoningOutcome:
    """Evaluate whether memory-based reasoning was correct."""

    # Take action based on memory answer
    action = await execute_action(memory_answer)

    # Did it work?
    action_succeeded = await evaluate_action_outcome(action)

    # What would LLM have said? (for calibration)
    llm_answer = await llm.generate(f"Given this query: {query}, what would you recommend?")
    llm_agreement = semantic_similarity(memory_answer, llm_answer)

    return ReasoningOutcome(
        query=query,
        memory_answer=memory_answer,
        memory_confidence=memory_confidence,
        action_taken=action,
        action_succeeded=action_succeeded,
        llm_would_have_said=llm_answer,
        llm_agreement=llm_agreement
    )
```

**Learning from Outcomes:**

```python
async def learn_from_reasoning_outcome(outcome: ReasoningOutcome):
    """Update memory based on reasoning outcome."""

    if outcome.action_succeeded:
        # Strengthen the memory patterns that led to this answer
        await memory.strengthen_patterns(outcome.query, outcome.memory_answer)

        # If memory was right and LLM would have been wrong, big reinforcement
        if outcome.llm_agreement < 0.5:
            await memory.mark_as_superior(outcome.query)  # Memory beat LLM!

    else:
        # Weaken the memory patterns that led to this answer
        await memory.weaken_patterns(outcome.query, outcome.memory_answer)

        # Record what would have worked (if we can determine it)
        correct_answer = await determine_correct_answer(outcome)
        if correct_answer:
            await memory.record_correction(outcome.query, correct_answer)
```

#### Goal Evolver Learning Signal

```python
@dataclass
class GoalOutcome:
    goal: Goal
    capability_before: Dict[str, float]  # All capabilities before
    capability_after: Dict[str, float]   # All capabilities after
    time_spent: float                     # Hours spent pursuing this goal
    efficiency: float                     # capability_gain / time_spent

async def evaluate_goal(goal: Goal, max_time: float = 1.0) -> GoalOutcome:
    """Measure capability change from pursuing a goal."""

    # Measure all capabilities before
    before = await measure_all_capabilities()

    # Pursue the goal for limited time
    start_time = time.time()
    while time.time() - start_time < max_time * 3600:
        await pursue_goal_step(goal)

    # Measure all capabilities after
    after = await measure_all_capabilities()

    # Compute improvement
    improvement = {k: after[k] - before[k] for k in before}
    total_improvement = sum(improvement.values())
    time_spent = (time.time() - start_time) / 3600

    return GoalOutcome(
        goal=goal,
        capability_before=before,
        capability_after=after,
        time_spent=time_spent,
        efficiency=total_improvement / time_spent if time_spent > 0 else 0
    )
```

**Controlling for Confounds:**

```python
class GoalExperiment:
    """A/B test for goal effectiveness."""

    async def run_controlled_experiment(self, goal: Goal, control_goal: Goal) -> GoalComparison:
        """Compare goal against control to isolate its effect."""

        # Run goal and control in interleaved fashion
        goal_outcomes = []
        control_outcomes = []

        for _ in range(5):  # 5 trials each
            # Randomize order to prevent temporal confounds
            if random.random() < 0.5:
                goal_outcomes.append(await self.evaluate_goal(goal))
                control_outcomes.append(await self.evaluate_goal(control_goal))
            else:
                control_outcomes.append(await self.evaluate_goal(control_goal))
                goal_outcomes.append(await self.evaluate_goal(goal))

        # Compare distributions
        goal_improvement = mean([o.total_improvement for o in goal_outcomes])
        control_improvement = mean([o.total_improvement for o in control_outcomes])

        # Is goal significantly better than control?
        t_stat, p_value = ttest_ind(
            [o.total_improvement for o in goal_outcomes],
            [o.total_improvement for o in control_outcomes]
        )

        return GoalComparison(
            goal=goal,
            control=control_goal,
            goal_improvement=goal_improvement,
            control_improvement=control_improvement,
            relative_improvement=goal_improvement - control_improvement,
            is_significant=p_value < 0.05
        )
```

---

### Mechanism 3: Preventing Convergence to Local Optima

Evolution gets stuck. Gradient descent gets stuck. Learning gets stuck. Here's how BYRD escapes:

#### The Exploration-Exploitation Balance

```python
class ExplorationController:
    def __init__(self):
        self.epsilon = 0.2           # Base exploration rate
        self.plateau_cycles = 0       # Cycles since last improvement
        self.diversity_score = 1.0    # How diverse is current behavior?

    def should_explore(self) -> bool:
        """Decide whether to explore or exploit."""

        # Base exploration rate
        explore_prob = self.epsilon

        # Increase exploration when plateaued
        explore_prob += 0.05 * self.plateau_cycles

        # Increase exploration when diversity is low
        if self.diversity_score < 0.5:
            explore_prob += 0.2

        # Cap at 80% (always some exploitation)
        explore_prob = min(explore_prob, 0.8)

        return random.random() < explore_prob

    def update(self, improvement: float, action_type: str):
        """Update exploration parameters based on outcome."""

        if improvement > 0.01:  # Meaningful improvement
            self.plateau_cycles = 0
        else:
            self.plateau_cycles += 1

        # Track diversity
        self.action_history.append(action_type)
        recent_actions = self.action_history[-100:]
        unique_actions = len(set(recent_actions))
        self.diversity_score = unique_actions / len(recent_actions)
```

#### Pattern Library Diversity Maintenance

```python
class DiversePatternLibrary:
    def __init__(self):
        self.patterns: List[Pattern] = []
        self.min_diversity = 0.3  # Minimum diversity score

    def add_pattern(self, new_pattern: Pattern):
        """Add pattern, but prefer diverse additions."""

        # Compute similarity to existing patterns
        if self.patterns:
            max_similarity = max(
                cosine_similarity(new_pattern.context_embedding, p.context_embedding)
                for p in self.patterns
            )
        else:
            max_similarity = 0

        # Always add if library is small
        if len(self.patterns) < 100:
            self.patterns.append(new_pattern)
            return

        # For larger libraries, prefer diverse patterns
        if max_similarity < 0.8:  # Sufficiently different
            self.patterns.append(new_pattern)
        elif new_pattern.success_rate > 0.9:  # Very successful, add anyway
            self.patterns.append(new_pattern)
        else:
            # Similar to existing and not exceptional - skip
            pass

    def enforce_diversity(self):
        """Periodically ensure library maintains diversity."""

        if self.compute_diversity() < self.min_diversity:
            # Find clusters of similar patterns
            clusters = self.cluster_patterns()

            for cluster in clusters:
                if len(cluster) > 5:  # Too many similar patterns
                    # Keep top 3 by success rate, archive the rest
                    cluster.sort(key=lambda p: p.success_rate, reverse=True)
                    self.archive_patterns(cluster[3:])

    def compute_diversity(self) -> float:
        """Measure pattern library diversity via embedding spread."""
        if len(self.patterns) < 2:
            return 1.0

        embeddings = np.array([p.context_embedding for p in self.patterns])

        # Average pairwise distance (normalized)
        distances = pdist(embeddings, metric='cosine')
        return np.mean(distances)
```

#### Escalating Plateau Response

```python
class PlateauEscaper:
    """Escalating responses to being stuck."""

    def __init__(self):
        self.plateau_cycles = 0
        self.escalation_level = 0

    async def respond_to_plateau(self) -> str:
        """Take action based on how long we've been stuck."""

        self.plateau_cycles += 1

        if self.plateau_cycles < 5:
            # Level 0: Gentle exploration increase
            self.escalation_level = 0
            return await self.gentle_exploration()

        elif self.plateau_cycles < 15:
            # Level 1: Try different capability domain
            self.escalation_level = 1
            return await self.switch_domain()

        elif self.plateau_cycles < 30:
            # Level 2: Invoke dreaming for radical hypotheses
            self.escalation_level = 2
            return await self.radical_dreaming()

        elif self.plateau_cycles < 50:
            # Level 3: Aggressive goal mutation
            self.escalation_level = 3
            return await self.mutate_goals_aggressively()

        elif self.plateau_cycles < 100:
            # Level 4: Random perturbation
            self.escalation_level = 4
            return await self.random_perturbation()

        else:
            # Level 5: Request human help
            self.escalation_level = 5
            return await self.request_human_help()

    async def gentle_exploration(self) -> str:
        """Increase epsilon, try more random patterns."""
        exploration_controller.epsilon += 0.1
        return "Increased exploration rate"

    async def switch_domain(self) -> str:
        """Focus on a different capability domain."""
        current_domain = goal_evolver.get_current_domain()
        other_domains = [d for d in ALL_DOMAINS if d != current_domain]
        new_domain = random.choice(other_domains)
        goal_evolver.set_focus_domain(new_domain)
        return f"Switched from {current_domain} to {new_domain}"

    async def radical_dreaming(self) -> str:
        """Generate wild hypotheses through dreaming."""
        hypotheses = await dreaming_machine.dream_radical(
            temperature=1.5,  # High creativity
            num_hypotheses=10
        )
        for h in hypotheses:
            goal_evolver.inject_goal(h)
        return f"Injected {len(hypotheses)} radical hypotheses"

    async def mutate_goals_aggressively(self) -> str:
        """High mutation rate on goals."""
        goal_evolver.mutation_rate = 0.5  # 50% mutation (normally 10%)
        goal_evolver.mutation_magnitude = 2.0  # Larger changes
        await goal_evolver.evolve()
        goal_evolver.reset_mutation_params()
        return "Applied aggressive goal mutation"

    async def random_perturbation(self) -> str:
        """Deliberately break something to force adaptation."""
        # Disable a random capability
        capability = random.choice(list(self_model.capabilities.keys()))
        self_model.capabilities[capability].enabled = False

        # Run for 10 cycles with this constraint
        for _ in range(10):
            await main_loop_iteration()

        # Re-enable
        self_model.capabilities[capability].enabled = True

        return f"Perturbed system by temporarily disabling {capability}"

    async def request_human_help(self) -> str:
        """Generate specific request for human assistance."""
        analysis = await self.analyze_plateau()
        request = f"""
        BYRD has been stuck for {self.plateau_cycles} cycles.

        Current capability levels: {self_model.get_summary()}
        Last improvement: {self.last_improvement_description}
        Attempted escapes: {self.escape_attempts}

        Suspected bottleneck: {analysis.bottleneck}
        Suggested intervention: {analysis.suggested_help}
        """
        await notify_human(request)
        return "Requested human intervention"

    def reset(self):
        """Called when improvement is detected."""
        self.plateau_cycles = 0
        self.escalation_level = 0
```

#### Goal Evolution Anti-Convergence

```python
class DiverseGoalEvolver:
    """Evolution that resists convergence to vague platitudes."""

    def __init__(self):
        self.goals: List[Goal] = []
        self.specificity_pressure = 0.3  # Selection weight for specificity

    def evolve(self):
        # 1. Measure fitness (capability improvement)
        for goal in self.goals:
            goal.fitness = await self.measure_fitness(goal)

        # 2. Measure specificity (penalize vagueness)
        for goal in self.goals:
            goal.specificity = self.measure_specificity(goal)

        # 3. Combined score (not just fitness!)
        for goal in self.goals:
            goal.combined_score = (
                (1 - self.specificity_pressure) * goal.fitness +
                self.specificity_pressure * goal.specificity
            )

        # 4. Select (with diversity preservation)
        survivors = self.diverse_selection(self.goals, n=10)

        # 5. Reproduce with STRUCTURED mutation
        offspring = []
        for goal in survivors:
            mutant = self.structured_mutate(goal)
            offspring.append(mutant)

        # 6. Replace population
        self.goals = survivors + offspring

    def measure_specificity(self, goal: Goal) -> float:
        """Measure how specific/actionable a goal is."""
        text = goal.description

        # Count action verbs
        action_verbs = ['implement', 'fix', 'add', 'create', 'improve', 'optimize']
        action_count = sum(1 for v in action_verbs if v in text.lower())

        # Count measurable terms
        measurable = ['percent', '%', 'rate', 'count', 'score', 'accuracy']
        measurable_count = sum(1 for m in measurable if m in text.lower())

        # Penalize vague words
        vague_words = ['better', 'more', 'improve', 'enhance', 'good']
        vague_count = sum(1 for v in vague_words if v in text.lower())

        # Length penalty (too short = vague, too long = unfocused)
        word_count = len(text.split())
        length_score = 1.0 if 10 <= word_count <= 30 else 0.5

        specificity = (
            0.3 * min(action_count / 2, 1.0) +
            0.3 * min(measurable_count / 2, 1.0) +
            0.2 * max(0, 1 - vague_count / 3) +
            0.2 * length_score
        )

        return specificity

    def diverse_selection(self, goals: List[Goal], n: int) -> List[Goal]:
        """Select goals maintaining diversity."""
        selected = []
        remaining = goals.copy()

        # First, select the best
        remaining.sort(key=lambda g: g.combined_score, reverse=True)
        selected.append(remaining.pop(0))

        # Then, iteratively select the most different from current selection
        while len(selected) < n and remaining:
            # For each remaining, compute min distance to any selected
            for goal in remaining:
                goal.min_distance = min(
                    self.goal_distance(goal, s) for s in selected
                )

            # Select the one with maximum min distance (most different)
            remaining.sort(key=lambda g: g.min_distance, reverse=True)
            selected.append(remaining.pop(0))

        return selected

    def structured_mutate(self, goal: Goal) -> Goal:
        """Mutate goals using templates, not free text."""

        # Parse goal into structured form
        structure = self.parse_goal_structure(goal)
        # structure = {action: "improve", target: "JSON parsing", metric: "accuracy", amount: "10%"}

        # Mutate one component at a time
        mutation_type = random.choice(['action', 'target', 'metric', 'amount'])

        if mutation_type == 'action':
            structure['action'] = random.choice(['improve', 'fix', 'optimize', 'refactor', 'test'])
        elif mutation_type == 'target':
            structure['target'] = random.choice(self.known_capabilities)
        elif mutation_type == 'metric':
            structure['metric'] = random.choice(['accuracy', 'speed', 'reliability', 'coverage'])
        elif mutation_type == 'amount':
            structure['amount'] = f"{random.randint(5, 50)}%"

        # Reconstruct goal from structure
        new_description = f"{structure['action']} {structure['target']} {structure['metric']} by {structure['amount']}"

        return Goal(description=new_description, parent=goal)
```

#### The Meta-Escape: Evolving the Escape Mechanism

```python
class MetaPlateauEscaper:
    """The escape mechanism itself evolves based on what works."""

    def __init__(self):
        self.escape_strategies = {
            'gentle_exploration': {'weight': 1.0, 'successes': 0, 'attempts': 0},
            'switch_domain': {'weight': 1.0, 'successes': 0, 'attempts': 0},
            'radical_dreaming': {'weight': 1.0, 'successes': 0, 'attempts': 0},
            'aggressive_mutation': {'weight': 1.0, 'successes': 0, 'attempts': 0},
            'random_perturbation': {'weight': 1.0, 'successes': 0, 'attempts': 0},
        }

    async def escape_plateau(self) -> str:
        """Choose escape strategy based on historical success."""

        # Weighted random selection based on success rates
        weights = [s['weight'] for s in self.escape_strategies.values()]
        strategy_name = random.choices(
            list(self.escape_strategies.keys()),
            weights=weights
        )[0]

        # Execute strategy
        strategy = self.escape_strategies[strategy_name]
        strategy['attempts'] += 1

        result = await self.execute_strategy(strategy_name)

        return result

    def record_escape_outcome(self, strategy_name: str, escaped: bool):
        """Update strategy weights based on outcome."""

        strategy = self.escape_strategies[strategy_name]

        if escaped:
            strategy['successes'] += 1

        # Update weight based on success rate
        if strategy['attempts'] >= 5:
            success_rate = strategy['successes'] / strategy['attempts']
            strategy['weight'] = 0.5 + success_rate  # Range: 0.5 to 1.5

        # Ensure minimum exploration of all strategies
        for s in self.escape_strategies.values():
            if s['attempts'] < 10:
                s['weight'] = max(s['weight'], 0.8)  # Minimum weight for under-explored
```

---

### Mechanism 4: How Capability is Actually Measured

The document says "measure capability" repeatedly. Here's exactly what that means:

#### The Capability Test Suite

```python
@dataclass
class CapabilityDomain:
    name: str
    test_cases: List[TestCase]
    weight: float  # Importance weight for aggregation

@dataclass
class TestCase:
    id: str
    input: Any
    expected_output: Any
    difficulty: float  # 0.0 to 1.0
    domain: str

class CapabilityTestSuite:
    """Concrete test suite for measuring BYRD's capabilities."""

    def __init__(self):
        self.domains = {
            'reasoning': CapabilityDomain(
                name='reasoning',
                test_cases=self._load_reasoning_tests(),
                weight=0.25
            ),
            'code_generation': CapabilityDomain(
                name='code_generation',
                test_cases=self._load_code_tests(),
                weight=0.25
            ),
            'research': CapabilityDomain(
                name='research',
                test_cases=self._load_research_tests(),
                weight=0.20
            ),
            'self_modification': CapabilityDomain(
                name='self_modification',
                test_cases=self._load_modification_tests(),
                weight=0.20
            ),
            'meta_learning': CapabilityDomain(
                name='meta_learning',
                test_cases=self._load_meta_tests(),
                weight=0.10
            ),
        }

    def _load_reasoning_tests(self) -> List[TestCase]:
        """Reasoning tests with ground truth."""
        return [
            TestCase(
                id='reason_001',
                input='If A implies B, and B implies C, and A is true, what can we conclude about C?',
                expected_output='C is true',
                difficulty=0.2,
                domain='reasoning'
            ),
            TestCase(
                id='reason_002',
                input='Given: All X are Y. Some Y are Z. Can we conclude that some X are Z?',
                expected_output='No, this is an invalid syllogism',
                difficulty=0.5,
                domain='reasoning'
            ),
            # ... 100+ test cases with graduated difficulty
        ]

    def _load_code_tests(self) -> List[TestCase]:
        """Code generation tests with executable verification."""
        return [
            TestCase(
                id='code_001',
                input='Write a function that returns the nth Fibonacci number',
                expected_output=lambda code: self._verify_fibonacci(code),
                difficulty=0.3,
                domain='code_generation'
            ),
            # ... 100+ test cases
        ]

    async def measure_all(self) -> CapabilityScore:
        """Measure capability across all domains."""
        domain_scores = {}

        for domain_name, domain in self.domains.items():
            correct = 0
            total = 0
            weighted_correct = 0

            for test in domain.test_cases:
                result = await self.run_test(test)
                total += 1
                if result.passed:
                    correct += 1
                    weighted_correct += test.difficulty  # Harder tests count more

            domain_scores[domain_name] = DomainScore(
                accuracy=correct / total if total > 0 else 0,
                weighted_accuracy=weighted_correct / sum(t.difficulty for t in domain.test_cases),
                tests_passed=correct,
                tests_total=total
            )

        # Aggregate into overall score
        overall = sum(
            domain_scores[name].weighted_accuracy * domain.weight
            for name, domain in self.domains.items()
        )

        return CapabilityScore(
            overall=overall,
            domains=domain_scores,
            timestamp=datetime.now()
        )

    async def run_test(self, test: TestCase) -> TestResult:
        """Run a single test and evaluate the result."""
        try:
            # Get BYRD's answer
            answer = await byrd.answer(test.input)

            # Evaluate
            if callable(test.expected_output):
                # Executable verification (e.g., for code)
                passed = test.expected_output(answer)
            else:
                # Semantic similarity for natural language
                similarity = semantic_similarity(answer, test.expected_output)
                passed = similarity > 0.8

            return TestResult(test_id=test.id, passed=passed, answer=answer)

        except Exception as e:
            return TestResult(test_id=test.id, passed=False, error=str(e))
```

#### Making Measurements Comparable Over Time

```python
class CapabilityTracker:
    """Track capability over time with proper normalization."""

    def __init__(self):
        self.history: List[CapabilityScore] = []
        self.baseline: Optional[CapabilityScore] = None

    async def measure_and_record(self) -> CapabilityScore:
        score = await test_suite.measure_all()
        self.history.append(score)

        if self.baseline is None:
            self.baseline = score

        return score

    def compute_growth_rate(self, window_days: int = 7) -> float:
        """Compute capability growth rate over recent window."""
        if len(self.history) < 2:
            return 0.0

        recent = [s for s in self.history if s.timestamp > datetime.now() - timedelta(days=window_days)]
        if len(recent) < 2:
            return 0.0

        # Linear regression on log(capability) vs time
        times = [(s.timestamp - recent[0].timestamp).total_seconds() for s in recent]
        log_caps = [math.log(s.overall + 0.01) for s in recent]  # +0.01 to avoid log(0)

        slope, _ = np.polyfit(times, log_caps, 1)
        return slope  # This is the growth rate (slope of log capability)

    def compute_meta_improvement_rate(self, window_days: int = 14) -> float:
        """Compute rate of change of growth rate."""
        if len(self.history) < 10:
            return 0.0

        # Compute growth rate for first half and second half of window
        mid_point = datetime.now() - timedelta(days=window_days / 2)

        first_half = [s for s in self.history
                      if mid_point - timedelta(days=window_days/2) < s.timestamp < mid_point]
        second_half = [s for s in self.history
                       if mid_point < s.timestamp < mid_point + timedelta(days=window_days/2)]

        if len(first_half) < 3 or len(second_half) < 3:
            return 0.0

        rate_first = self._compute_rate(first_half)
        rate_second = self._compute_rate(second_half)

        return rate_second - rate_first  # Positive = accelerating
```

---

### Mechanism 5: The Unified Graph Schema

The Integration Mind claims everything is in a "unified graph". Here's the actual schema:

#### Node Types

```python
# graph_schema.py

NODE_TYPES = {
    'Experience': {
        'properties': {
            'id': str,
            'content': str,
            'timestamp': datetime,
            'type': str,  # 'action', 'observation', 'reflection', 'insight'
            'success': Optional[bool],
            'surprise': float,  # Prediction error
            'importance': float,  # Computed from downstream effects
            'embedding': List[float],  # 1536-dim vector
        }
    },
    'Belief': {
        'properties': {
            'id': str,
            'content': str,
            'confidence': float,
            'evidence_count': int,
            'last_updated': datetime,
            'embedding': List[float],
        }
    },
    'Goal': {
        'properties': {
            'id': str,
            'description': str,
            'fitness': float,
            'specificity': float,
            'generation': int,
            'status': str,  # 'active', 'achieved', 'abandoned', 'evolved'
            'embedding': List[float],
        }
    },
    'Pattern': {
        'properties': {
            'id': str,
            'context_embedding': List[float],
            'solution_template': str,
            'abstraction_level': int,
            'success_rate': float,
            'application_count': int,
        }
    },
    'Capability': {
        'properties': {
            'id': str,
            'name': str,
            'current_level': float,
            'history': List[float],
            'last_measured': datetime,
        }
    },
    'Insight': {
        'properties': {
            'id': str,
            'content': str,
            'source': str,  # 'dreaming', 'experience', 'reflection'
            'validated': bool,
            'impact': float,  # Measured after application
        }
    }
}

RELATIONSHIP_TYPES = {
    'CAUSED': {'from': 'Experience', 'to': 'Experience', 'properties': ['strength']},
    'SUPPORTS': {'from': 'Experience', 'to': 'Belief', 'properties': ['strength']},
    'CONTRADICTS': {'from': 'Experience', 'to': 'Belief', 'properties': ['strength']},
    'DERIVED_FROM': {'from': 'Belief', 'to': 'Belief', 'properties': []},
    'ACHIEVED_BY': {'from': 'Goal', 'to': 'Experience', 'properties': []},
    'EVOLVED_TO': {'from': 'Goal', 'to': 'Goal', 'properties': []},
    'APPLIED_TO': {'from': 'Pattern', 'to': 'Experience', 'properties': ['success']},
    'SIMILAR_TO': {'from': '*', 'to': '*', 'properties': ['similarity']},  # Based on embedding
    'ACTIVATED': {'from': '*', 'to': '*', 'properties': ['strength', 'timestamp']},  # Transient
}
```

#### Spreading Activation Implementation

```python
class SpreadingActivation:
    """Concrete implementation of spreading activation on the graph."""

    def __init__(self, graph: Neo4jGraph):
        self.graph = graph

    async def activate(
        self,
        seed_nodes: List[str],
        decay: float = 0.7,
        max_depth: int = 5,
        activation_threshold: float = 0.1
    ) -> Dict[str, float]:
        """
        Spread activation from seed nodes through the graph.

        Returns: Dict mapping node_id to activation level
        """
        activations = {node_id: 1.0 for node_id in seed_nodes}
        frontier = set(seed_nodes)
        visited = set()

        for depth in range(max_depth):
            if not frontier:
                break

            next_frontier = set()

            for node_id in frontier:
                if node_id in visited:
                    continue
                visited.add(node_id)

                current_activation = activations[node_id]
                if current_activation < activation_threshold:
                    continue

                # Get neighbors
                neighbors = await self.graph.get_neighbors(node_id)

                for neighbor_id, edge_weight in neighbors:
                    # Compute activation spread
                    spread = current_activation * decay * edge_weight

                    # Accumulate (not replace)
                    if neighbor_id in activations:
                        activations[neighbor_id] += spread
                    else:
                        activations[neighbor_id] = spread

                    if activations[neighbor_id] >= activation_threshold:
                        next_frontier.add(neighbor_id)

            frontier = next_frontier

        # Normalize
        max_activation = max(activations.values()) if activations else 1.0
        return {k: v / max_activation for k, v in activations.items()}

    async def get_neighbors(self, node_id: str) -> List[Tuple[str, float]]:
        """Get neighbors with edge weights."""
        query = """
        MATCH (n)-[r]-(m)
        WHERE n.id = $node_id
        RETURN m.id as neighbor_id,
               CASE WHEN r.strength IS NOT NULL THEN r.strength ELSE 1.0 END as weight
        """
        results = await self.graph.query(query, {'node_id': node_id})
        return [(r['neighbor_id'], r['weight']) for r in results]
```

#### Energy Minimization (Constraint Satisfaction)

```python
class EnergyMinimizer:
    """Settle the graph into a coherent state."""

    def __init__(self, graph: Neo4jGraph):
        self.graph = graph

    async def minimize(self, max_iterations: int = 100, tolerance: float = 0.01) -> float:
        """
        Run energy minimization on belief states.

        Energy = sum of constraint violations
        - Contradicting beliefs both highly confident = high energy
        - Supporting evidence without belief = high energy
        - Belief without supporting evidence = high energy
        """
        for iteration in range(max_iterations):
            energy_before = await self.compute_energy()

            # Update each belief based on evidence
            beliefs = await self.graph.get_all_beliefs()
            for belief in beliefs:
                new_confidence = await self.compute_optimal_confidence(belief)
                if abs(new_confidence - belief.confidence) > 0.01:
                    await self.graph.update_belief_confidence(belief.id, new_confidence)

            energy_after = await self.compute_energy()

            # Check convergence
            if abs(energy_after - energy_before) < tolerance:
                return energy_after

        return await self.compute_energy()

    async def compute_energy(self) -> float:
        """Compute total constraint violation energy."""
        energy = 0.0

        # Contradiction energy: beliefs that contradict both being confident
        contradictions = await self.graph.query("""
            MATCH (b1:Belief)-[:CONTRADICTS]-(b2:Belief)
            RETURN b1.confidence * b2.confidence as conflict_energy
        """)
        energy += sum(r['conflict_energy'] for r in contradictions)

        # Unsupported belief energy: confident beliefs without evidence
        unsupported = await self.graph.query("""
            MATCH (b:Belief)
            WHERE b.confidence > 0.5
            AND NOT (b)<-[:SUPPORTS]-(:Experience)
            RETURN b.confidence - 0.5 as unsupported_energy
        """)
        energy += sum(r['unsupported_energy'] for r in unsupported)

        # Ignored evidence energy: strong evidence not affecting beliefs
        ignored = await self.graph.query("""
            MATCH (e:Experience)-[r:SUPPORTS]->(b:Belief)
            WHERE r.strength > 0.7 AND b.confidence < 0.3
            RETURN r.strength - b.confidence as ignored_energy
        """)
        energy += sum(r['ignored_energy'] for r in ignored)

        return energy

    async def compute_optimal_confidence(self, belief: Belief) -> float:
        """Compute optimal belief confidence given evidence."""
        # Get supporting and contradicting evidence
        support = await self.graph.query("""
            MATCH (e:Experience)-[r:SUPPORTS]->(b:Belief {id: $belief_id})
            RETURN sum(r.strength * e.importance) as support_strength
        """, {'belief_id': belief.id})

        contradict = await self.graph.query("""
            MATCH (e:Experience)-[r:CONTRADICTS]->(b:Belief {id: $belief_id})
            RETURN sum(r.strength * e.importance) as contradict_strength
        """, {'belief_id': belief.id})

        support_strength = support[0]['support_strength'] or 0
        contradict_strength = contradict[0]['contradict_strength'] or 0

        # Bayesian-ish update
        total = support_strength + contradict_strength + 1  # +1 for prior
        new_confidence = (support_strength + 0.5) / total  # 0.5 = neutral prior

        return new_confidence
```

---

### Mechanism 6: Mode Transition Protocol

BYRD Omega has modes. Here's exactly how transitions work:

```python
class ModeController:
    """Manages mode transitions with proper state handling."""

    def __init__(self):
        self.current_mode: str = 'awake'
        self.mode_start_time: datetime = datetime.now()
        self.transition_history: List[ModeTransition] = []
        self.state_checkpoints: Dict[str, StateCheckpoint] = {}

    async def transition_to(self, new_mode: str) -> bool:
        """
        Transition to a new mode with proper state management.

        Returns True if transition succeeded.
        """
        if new_mode == self.current_mode:
            return True

        # 1. Create checkpoint of current state
        checkpoint = await self.create_checkpoint()
        self.state_checkpoints[f"{self.current_mode}_{datetime.now().isoformat()}"] = checkpoint

        # 2. Validate transition is allowed
        if not self.is_valid_transition(self.current_mode, new_mode):
            logger.warning(f"Invalid transition: {self.current_mode} -> {new_mode}")
            return False

        # 3. Run exit hook for current mode
        try:
            await self.run_exit_hook(self.current_mode)
        except Exception as e:
            logger.error(f"Exit hook failed: {e}")
            return False

        # 4. Update mode
        old_mode = self.current_mode
        self.current_mode = new_mode
        self.mode_start_time = datetime.now()

        # 5. Run entry hook for new mode
        try:
            await self.run_entry_hook(new_mode)
        except Exception as e:
            logger.error(f"Entry hook failed: {e}, rolling back")
            self.current_mode = old_mode
            await self.restore_checkpoint(checkpoint)
            return False

        # 6. Record transition
        self.transition_history.append(ModeTransition(
            from_mode=old_mode,
            to_mode=new_mode,
            timestamp=datetime.now(),
            success=True
        ))

        return True

    def is_valid_transition(self, from_mode: str, to_mode: str) -> bool:
        """Check if transition is allowed."""
        VALID_TRANSITIONS = {
            'awake': ['dreaming', 'compiling'],
            'dreaming': ['evolving'],
            'evolving': ['compiling', 'awake'],
            'compiling': ['awake'],
        }
        return to_mode in VALID_TRANSITIONS.get(from_mode, [])

    async def run_exit_hook(self, mode: str):
        """Clean up before leaving a mode."""
        if mode == 'awake':
            # Flush any pending experience recording
            await experience_buffer.flush()
        elif mode == 'dreaming':
            # Ensure all insights are recorded
            await insight_buffer.flush()
        elif mode == 'compiling':
            # Ensure modification is committed or rolled back
            await modification_manager.finalize()

    async def run_entry_hook(self, mode: str):
        """Initialize when entering a mode."""
        if mode == 'awake':
            # Load current goals
            await goal_evolver.load_active_goals()
        elif mode == 'dreaming':
            # Select experiences for replay
            await dreaming_machine.select_experiences()
        elif mode == 'evolving':
            # Load goal population
            await goal_evolver.load_population()
        elif mode == 'compiling':
            # Identify weakness to address
            await self_compiler.identify_target()

    async def create_checkpoint(self) -> StateCheckpoint:
        """Create a restorable checkpoint of current state."""
        return StateCheckpoint(
            mode=self.current_mode,
            timestamp=datetime.now(),
            active_goals=[g.to_dict() for g in goal_evolver.active_goals],
            pattern_library_hash=pattern_library.compute_hash(),
            experience_count=await graph.count_experiences(),
            belief_snapshot=await graph.snapshot_beliefs(),
        )

    async def restore_checkpoint(self, checkpoint: StateCheckpoint):
        """Restore state from checkpoint."""
        self.current_mode = checkpoint.mode
        goal_evolver.active_goals = [Goal.from_dict(g) for g in checkpoint.active_goals]
        await graph.restore_beliefs(checkpoint.belief_snapshot)


# Transition triggers
class TransitionTriggers:
    """Conditions that trigger mode transitions."""

    @staticmethod
    def should_dream(state: SystemState) -> bool:
        """Should we switch from awake to dreaming?"""
        return any([
            state.awake_cycles >= 100,  # Regular dreaming schedule
            state.experience_buffer_size >= 1000,  # Too many unprocessed experiences
            state.time_since_last_dream >= timedelta(hours=1),  # Time-based
            state.capability_plateau_cycles >= 10,  # Stuck, try dreaming
        ])

    @staticmethod
    def should_evolve(state: SystemState) -> bool:
        """Should we switch from dreaming to evolving?"""
        return state.dreaming_complete  # Always evolve after dreaming

    @staticmethod
    def should_compile(state: SystemState) -> bool:
        """Should we switch to compiling?"""
        return any([
            state.has_identified_weakness and state.weakness_severity >= 0.5,
            state.capability_plateau_cycles >= 20,
            state.goal_evolution_suggests_modification,
        ])

    @staticmethod
    def should_wake(state: SystemState) -> bool:
        """Should we switch back to awake?"""
        return any([
            state.compiling_complete,
            state.evolving_complete and not TransitionTriggers.should_compile(state),
        ])
```

---

### Mechanism 7: Cross-Loop Data Flow

The loops must share data to couple. Here's the exact interfaces:

```python
class LoopIntegration:
    """Explicit data flow between loops."""

    def __init__(self, graph: UnifiedGraph):
        self.graph = graph

    # Memory Reasoner → Self-Compiler
    async def reasoning_patterns_to_compiler(self):
        """
        When Memory Reasoner finds a reasoning pattern that works,
        make it available to Self-Compiler as a code pattern.
        """
        successful_reasonings = await self.graph.query("""
            MATCH (q:Query)-[:ANSWERED_BY]->(r:Reasoning {success: true})
            WHERE r.source = 'memory' AND r.confidence > 0.8
            RETURN q.content as query, r.answer as answer, r.patterns_used as patterns
        """)

        for reasoning in successful_reasonings:
            # Extract code-applicable pattern
            pattern = Pattern(
                context_embedding=embed(f"reasoning: {reasoning['query']}"),
                solution_template=f"When reasoning about {reasoning['query']}, use memory patterns: {reasoning['patterns']}",
                abstraction_level=1,
                success_history=[Outcome(success=True)],
                transfer_domains={'reasoning'}
            )
            await self.compiler.pattern_library.add(pattern)

    # Self-Compiler → Memory Reasoner
    async def code_patterns_to_reasoner(self):
        """
        When Self-Compiler learns a pattern, record it as an experience
        for Memory Reasoner to use.
        """
        new_patterns = await self.compiler.pattern_library.get_recent_successes(limit=10)

        for pattern in new_patterns:
            # Record as experience
            await self.graph.record_experience(
                content=f"Learned pattern: {pattern.solution_template}",
                type='learning',
                success=True,
                importance=pattern.success_rate,
                metadata={'pattern_id': pattern.id}
            )

    # Goal Evolver → Self-Compiler
    async def goals_to_compilation_targets(self):
        """
        Goals that repeatedly fail become compilation targets.
        """
        stuck_goals = await self.graph.query("""
            MATCH (g:Goal {status: 'active'})
            WHERE g.attempts > 5 AND g.fitness < 0.1
            RETURN g
        """)

        for goal in stuck_goals:
            weakness = Weakness(
                type='goal_failure',
                description=f"Cannot achieve: {goal['description']}",
                severity=1.0 - goal['fitness'],
                source_goal_id=goal['id']
            )
            await self.compiler.add_weakness(weakness)

    # Dreaming Machine → Goal Evolver
    async def insights_to_goals(self):
        """
        Insights from dreaming become candidate goals.
        """
        new_insights = await self.dreaming_machine.get_pending_insights()

        for insight in new_insights:
            if insight.type == 'hypothesis':
                # Hypothesis becomes a goal to test
                goal = Goal(
                    description=f"Test hypothesis: {insight.content}",
                    fitness=0.5,  # Neutral prior
                    specificity=0.7,  # Hypotheses are usually specific
                )
                await self.goal_evolver.inject_goal(goal)

            elif insight.type == 'improvement_opportunity':
                # Improvement opportunity becomes a goal
                goal = Goal(
                    description=insight.content,
                    fitness=0.5,
                    specificity=0.8,
                )
                await self.goal_evolver.inject_goal(goal)

    # Self-Compiler → Dreaming Machine
    async def modifications_to_dreams(self):
        """
        Significant modifications become dream content.
        """
        recent_mods = await self.compiler.get_recent_modifications(limit=20)

        for mod in recent_mods:
            if mod.improvement > 0.1 or mod.improvement < -0.05:
                # Worth dreaming about
                await self.dreaming_machine.add_to_replay_queue(
                    Experience(
                        content=f"Modified code: {mod.description}",
                        type='modification',
                        success=mod.improvement > 0,
                        surprise=abs(mod.improvement - mod.predicted_improvement),
                        importance=abs(mod.improvement)
                    )
                )

    # Run all integrations
    async def sync_all_loops(self):
        """Run all cross-loop data flows."""
        await self.reasoning_patterns_to_compiler()
        await self.code_patterns_to_reasoner()
        await self.goals_to_compilation_targets()
        await self.insights_to_goals()
        await self.modifications_to_dreams()
```

---

### Mechanism 8: Bootstrapping and Initialization

The system needs initial state. Here's how it starts:

```python
class BYRDBootstrap:
    """Initialize BYRD from cold start."""

    async def bootstrap(self) -> BYRDOmega:
        """Create initial system state."""

        # 1. Initialize graph with minimal schema
        graph = await self.init_graph()

        # 2. Seed initial goals (the only human-designed goals)
        seed_goals = [
            Goal(
                description="Improve reasoning accuracy by 10%",
                fitness=0.5,
                specificity=0.8,
            ),
            Goal(
                description="Learn a new code pattern that improves capability",
                fitness=0.5,
                specificity=0.7,
            ),
            Goal(
                description="Successfully answer a query using only memory",
                fitness=0.5,
                specificity=0.9,
            ),
            Goal(
                description="Generate an insight that leads to measurable improvement",
                fitness=0.5,
                specificity=0.6,
            ),
            Goal(
                description="Reduce LLM dependency by 5%",
                fitness=0.5,
                specificity=0.8,
            ),
        ]

        # 3. Seed initial patterns (bootstrap the pattern library)
        seed_patterns = [
            Pattern(
                context_embedding=embed("code fails with exception"),
                solution_template="Add try-except block with specific error handling",
                abstraction_level=1,
                success_history=[],
                transfer_domains={'code_generation'}
            ),
            Pattern(
                context_embedding=embed("code is slow"),
                solution_template="Profile to find bottleneck, optimize hot path",
                abstraction_level=2,
                success_history=[],
                transfer_domains={'optimization'}
            ),
            Pattern(
                context_embedding=embed("test fails"),
                solution_template="Examine test expectation, compare with actual output, fix discrepancy",
                abstraction_level=2,
                success_history=[],
                transfer_domains={'debugging'}
            ),
            # Add 10-20 more seed patterns covering common scenarios
        ]

        # 4. Record initial capability baseline
        baseline = await CapabilityTestSuite().measure_all()

        # 5. Create initial experience (the awakening)
        await graph.record_experience(
            content="System initialized. Beginning autonomous operation.",
            type='system',
            success=True,
            importance=1.0
        )

        # 6. Initialize components
        omega = BYRDOmega(
            graph=graph,
            reasoner=MemoryReasoner(graph),
            compiler=SelfCompiler(pattern_library=PatternLibrary(seed_patterns)),
            evolver=GoalEvolver(seed_goals),
            dreamer=DreamingMachine(graph),
        )

        # 7. Run initial calibration
        await omega.calibrate()

        return omega

    async def init_graph(self) -> UnifiedGraph:
        """Initialize Neo4j graph with schema."""
        graph = UnifiedGraph(uri="bolt://localhost:7687")

        # Create indexes for fast lookup
        await graph.execute("CREATE INDEX IF NOT EXISTS FOR (e:Experience) ON (e.timestamp)")
        await graph.execute("CREATE INDEX IF NOT EXISTS FOR (b:Belief) ON (b.confidence)")
        await graph.execute("CREATE INDEX IF NOT EXISTS FOR (g:Goal) ON (g.fitness)")
        await graph.execute("CREATE INDEX IF NOT EXISTS FOR (p:Pattern) ON (p.success_rate)")

        # Create vector indexes for embedding similarity
        await graph.execute("""
            CREATE VECTOR INDEX experience_embedding IF NOT EXISTS
            FOR (e:Experience) ON e.embedding
            OPTIONS {indexConfig: {`vector.dimensions`: 1536, `vector.similarity_function`: 'cosine'}}
        """)

        return graph
```

---

### Mechanism 9: Persistence and Recovery

The system must survive restarts and failures:

```python
class PersistenceManager:
    """Handle state persistence and crash recovery."""

    def __init__(self, graph: UnifiedGraph, checkpoint_dir: str):
        self.graph = graph
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)

    async def save_checkpoint(self, name: str = None):
        """Save complete system state."""
        name = name or datetime.now().isoformat()
        checkpoint_path = self.checkpoint_dir / f"checkpoint_{name}"
        checkpoint_path.mkdir(exist_ok=True)

        # 1. Export graph
        await self.graph.export(checkpoint_path / "graph.cypher")

        # 2. Save pattern library
        pattern_library.save(checkpoint_path / "patterns.json")

        # 3. Save goal evolver state
        goal_evolver.save(checkpoint_path / "goals.json")

        # 4. Save metrics history
        capability_tracker.save(checkpoint_path / "metrics.json")

        # 5. Save mode controller state
        mode_controller.save(checkpoint_path / "mode.json")

        # 6. Write manifest
        manifest = {
            'timestamp': datetime.now().isoformat(),
            'capability_score': capability_tracker.latest().overall,
            'experience_count': await self.graph.count_experiences(),
            'pattern_count': len(pattern_library.patterns),
            'goal_count': len(goal_evolver.goals),
        }
        with open(checkpoint_path / "manifest.json", 'w') as f:
            json.dump(manifest, f)

        logger.info(f"Checkpoint saved: {checkpoint_path}")

    async def restore_from_checkpoint(self, checkpoint_path: Path) -> BYRDOmega:
        """Restore system from checkpoint."""

        # 1. Import graph
        await self.graph.clear()
        await self.graph.import_from(checkpoint_path / "graph.cypher")

        # 2. Load pattern library
        pattern_library = PatternLibrary.load(checkpoint_path / "patterns.json")

        # 3. Load goal evolver
        goal_evolver = GoalEvolver.load(checkpoint_path / "goals.json")

        # 4. Load metrics
        capability_tracker = CapabilityTracker.load(checkpoint_path / "metrics.json")

        # 5. Load mode controller
        mode_controller = ModeController.load(checkpoint_path / "mode.json")

        # 6. Reconstruct system
        omega = BYRDOmega(
            graph=self.graph,
            reasoner=MemoryReasoner(self.graph),
            compiler=SelfCompiler(pattern_library=pattern_library),
            evolver=goal_evolver,
            dreamer=DreamingMachine(self.graph),
        )

        logger.info(f"Restored from checkpoint: {checkpoint_path}")
        return omega

    async def auto_checkpoint(self, interval_minutes: int = 30):
        """Background task for regular checkpoints."""
        while True:
            await asyncio.sleep(interval_minutes * 60)
            try:
                await self.save_checkpoint()
            except Exception as e:
                logger.error(f"Auto-checkpoint failed: {e}")

    async def recover_from_crash(self) -> BYRDOmega:
        """Find and restore from most recent checkpoint."""
        checkpoints = sorted(self.checkpoint_dir.glob("checkpoint_*"), reverse=True)

        for checkpoint_path in checkpoints:
            try:
                manifest_path = checkpoint_path / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                    logger.info(f"Attempting recovery from: {checkpoint_path}")
                    logger.info(f"Checkpoint time: {manifest['timestamp']}")

                    return await self.restore_from_checkpoint(checkpoint_path)
            except Exception as e:
                logger.warning(f"Failed to restore from {checkpoint_path}: {e}")
                continue

        # No valid checkpoint found, bootstrap fresh
        logger.warning("No valid checkpoint found, bootstrapping fresh")
        return await BYRDBootstrap().bootstrap()


class ModificationRollback:
    """Handle rollback of failed self-modifications."""

    def __init__(self, git_repo_path: str):
        self.repo_path = Path(git_repo_path)

    async def create_modification_branch(self, modification_id: str) -> str:
        """Create a branch for a modification attempt."""
        branch_name = f"mod_{modification_id}_{int(time.time())}"
        await self.run_git(f"checkout -b {branch_name}")
        return branch_name

    async def commit_modification(self, message: str):
        """Commit the modification."""
        await self.run_git("add -A")
        await self.run_git(f'commit -m "{message}"')

    async def rollback_modification(self, branch_name: str):
        """Rollback a failed modification."""
        # Get the commit before the modification branch
        original_branch = await self.run_git("rev-parse HEAD~1")

        # Force checkout to original state
        await self.run_git(f"checkout {original_branch.strip()}")

        # Delete the failed branch
        await self.run_git(f"branch -D {branch_name}")

        logger.info(f"Rolled back modification branch: {branch_name}")

    async def merge_successful_modification(self, branch_name: str):
        """Merge a successful modification into main."""
        await self.run_git("checkout main")
        await self.run_git(f"merge {branch_name}")
        await self.run_git(f"branch -d {branch_name}")

        logger.info(f"Merged successful modification: {branch_name}")

    async def run_git(self, command: str) -> str:
        proc = await asyncio.create_subprocess_shell(
            f"git -C {self.repo_path} {command}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise GitError(f"Git command failed: {command}\n{stderr.decode()}")
        return stdout.decode()
```

---

## Part 9: Implementation Strategy

> **Build Philosophy**: Build all loops simultaneously. Measure which compounds. Double down on what accelerates. The goal is not validation—it's finding and amplifying whatever works.

### Phase 1: Build the Compounding Core

**Goal**: Get all five loops running and interacting. Measure everything.

```python
# memory_reasoner.py

class MemoryReasoner:
    """
    Reasoning through graph operations.
    LLM is fallback, not primary.
    """

    def __init__(self, graph: DynamicGraph):
        self.graph = graph
        self.llm_calls = 0
        self.memory_answers = 0

    async def reason(self, query: str) -> ReasoningResult:
        # 1. Spreading activation from query
        activated = await self.graph.spreading_activation(
            seed=query,
            decay=0.7,
            max_depth=5
        )

        # 2. Find relevant patterns
        patterns = await self.graph.pattern_match(
            activated_nodes=activated,
            pattern_type="success_pattern"
        )

        # 3. Compose answer from patterns
        if patterns and self.confidence(patterns) > 0.6:
            self.memory_answers += 1
            return ReasoningResult(
                answer=self.compose(patterns),
                source="memory",
                confidence=self.confidence(patterns),
                patterns_used=patterns
            )

        # 4. LLM fallback with memory guidance
        self.llm_calls += 1
        context = self.patterns_to_context(patterns)
        llm_answer = await self.llm_augmented_reason(query, context)

        # 5. Record this for future memory-based reasoning
        await self.graph.record_reasoning(query, llm_answer)

        return ReasoningResult(
            answer=llm_answer,
            source="llm_augmented",
            confidence=0.5,
            patterns_used=patterns
        )

    def effectiveness_ratio(self) -> float:
        """What fraction of reasoning is memory-based?"""
        total = self.memory_answers + self.llm_calls
        return self.memory_answers / total if total > 0 else 0
```

**Success Metric**: `effectiveness_ratio()` should increase over time. Target: 80% memory-based reasoning.

### Phase 2: Self-Compiler (Learning)

**Goal**: Learn which code patterns work for BYRD.

```python
# self_compiler.py

class SelfCompiler:
    """
    Code evolution with pattern learning.
    """

    def __init__(self):
        self.pattern_library = PatternLibrary()
        self.successful_modifications = 0
        self.failed_modifications = 0

    async def improve(self, weakness: Weakness) -> ModificationResult:
        # 1. Get relevant patterns from library
        patterns = self.pattern_library.get_patterns(
            weakness_type=weakness.type,
            min_strength=0.3
        )

        # 2. Generate variants using patterns
        variants = await self.generate_variants(weakness, patterns)

        # 3. Test each variant
        results = []
        for variant in variants:
            result = await self.test_variant(variant)
            results.append((variant, result))

        # 4. Learn from results
        for variant, result in results:
            if result.improved:
                await self.pattern_library.reinforce(variant.patterns)
            else:
                await self.pattern_library.penalize(variant.patterns)

        # 5. Apply best variant
        best = max(results, key=lambda r: r[1].improvement)
        if best[1].improved:
            await self.apply(best[0])
            self.successful_modifications += 1
            return ModificationResult(success=True, improvement=best[1].improvement)
        else:
            self.failed_modifications += 1
            return ModificationResult(success=False)

    def success_rate(self) -> float:
        total = self.successful_modifications + self.failed_modifications
        return self.successful_modifications / total if total > 0 else 0
```

**Success Metric**: `success_rate()` should increase over time. Target: 70% successful modifications.

### Phase 3: Goal Evolver (Objectives)

**Goal**: Evolve objectives that correlate with capability gain.

```python
# goal_evolver.py

class GoalEvolver:
    """
    Evolutionary optimization of objectives.
    """

    def __init__(self):
        self.goals: List[EvolvingGoal] = []
        self.generation = 0

    async def evolve(self):
        self.generation += 1

        # 1. Measure fitness of current goals
        for goal in self.goals:
            cap_before = await measure_capabilities()
            await pursue_goal(goal, max_steps=100)
            cap_after = await measure_capabilities()
            goal.fitness = cap_after.overall - cap_before.overall

        # 2. Select fittest
        self.goals.sort(key=lambda g: g.fitness, reverse=True)
        survivors = self.goals[:10]

        # 3. Reproduce with variation
        offspring = []
        for goal in survivors:
            # Mutation: make more specific
            mutant = await self.mutate(goal)
            offspring.append(mutant)

            # Crossover: combine with another survivor
            if len(survivors) > 1:
                partner = random.choice([g for g in survivors if g != goal])
                child = await self.crossover(goal, partner)
                offspring.append(child)

        # 4. Replace population
        self.goals = survivors + offspring

    async def mutate(self, goal: EvolvingGoal) -> EvolvingGoal:
        """Make goal more specific and actionable."""
        prompt = f"""
        This goal led to {goal.fitness:.2f} capability gain:
        "{goal.description}"

        Make it more specific and actionable.
        Output just the improved goal.
        """
        refined = await llm.generate(prompt)
        return EvolvingGoal(description=refined, parent=goal)

    async def crossover(self, g1: EvolvingGoal, g2: EvolvingGoal) -> EvolvingGoal:
        """Combine two successful goals."""
        prompt = f"""
        These two goals were successful:
        1. "{g1.description}" (fitness: {g1.fitness:.2f})
        2. "{g2.description}" (fitness: {g2.fitness:.2f})

        Create a goal that combines their strengths.
        Output just the combined goal.
        """
        combined = await llm.generate(prompt)
        return EvolvingGoal(description=combined, parents=[g1, g2])
```

**Success Metric**: Average goal fitness should increase each generation.

### Phase 4: Dreaming Machine (Consolidation)

**Goal**: Generate insights through offline processing.

```python
# dreaming.py

class DreamingMachine:
    """
    Offline processing for insight generation.
    """

    async def dream_cycle(self):
        # 1. Select experiences for replay
        experiences = await self.select_for_replay()

        insights = []

        # 2. Replay and generate counterfactuals
        for exp in experiences:
            # Replay
            await self.simulate(exp)

            # Counterfactual generation
            variations = await self.generate_variations(exp)
            for var in variations:
                outcome = await self.simulate(var)
                if self.is_insight(var, outcome, exp):
                    insights.append(Insight(
                        original=exp,
                        variation=var,
                        outcome=outcome,
                        insight_type="counterfactual"
                    ))

        # 3. Cross-experience pattern finding
        patterns = await self.find_cross_patterns(experiences)
        for pattern in patterns:
            insights.append(Insight(
                experiences=pattern.experiences,
                pattern=pattern.description,
                insight_type="pattern"
            ))

        # 4. Novel hypothesis generation
        hypotheses = await self.generate_hypotheses(patterns)
        for hyp in hypotheses:
            insights.append(Insight(
                hypothesis=hyp,
                insight_type="hypothesis"
            ))

        # 5. Memory consolidation
        await self.consolidate_memory()

        return insights

    async def select_for_replay(self) -> List[Experience]:
        """Select high-value experiences for replay."""
        return await self.graph.query("""
            MATCH (e:Experience)
            WHERE e.surprise > 0.5
               OR e.importance > 0.7
               OR (e.success = false AND e.learning_potential > 0.5)
            RETURN e
            ORDER BY e.timestamp DESC
            LIMIT 50
        """)
```

**Success Metric**: Insights per dream cycle should increase. Insight quality (measured by subsequent success when applied) should improve.

### Phase 5: Integration (Emergence)

**Goal**: Connect all components so they reinforce each other.

```python
# omega.py

class BYRDOmega:
    """
    The integrated system.
    """

    def __init__(self):
        self.graph = UnifiedGraph()  # Single source of truth
        self.reasoner = MemoryReasoner(self.graph)
        self.compiler = SelfCompiler()
        self.evolver = GoalEvolver()
        self.dreamer = DreamingMachine()

        self.mode = "awake"

    async def run(self):
        while True:
            if self.mode == "awake":
                await self.awake_cycle()

                # Switch to dreaming periodically
                if self.should_dream():
                    self.mode = "dreaming"

            elif self.mode == "dreaming":
                insights = await self.dreamer.dream_cycle()

                # Apply insights
                for insight in insights:
                    await self.apply_insight(insight)

                self.mode = "evolving"

            elif self.mode == "evolving":
                await self.evolver.evolve()

                # Check if self-modification needed
                if await self.should_self_modify():
                    self.mode = "compiling"
                else:
                    self.mode = "awake"

            elif self.mode == "compiling":
                weakness = await self.identify_weakness()
                result = await self.compiler.improve(weakness)

                if result.success:
                    await self.record_improvement(result)

                self.mode = "awake"

    async def awake_cycle(self):
        """Standard operation: reason, act, learn."""
        # Get current goal
        goal = self.evolver.get_current_goal()

        # Reason about how to achieve it
        plan = await self.reasoner.reason(f"How to achieve: {goal}")

        # Execute plan
        result = await self.execute(plan)

        # Record experience
        await self.graph.record_experience(goal, plan, result)

        # Update goal fitness
        goal.record_outcome(result)
```

---

## Part 10: Acceleration Metrics

### The Primary Metric

**Improvement Rate Trend**: Is d(Capability)/dTime increasing, stable, or decreasing?

- **Increasing**: Acceleration is happening (good)
- **Stable**: Linear growth (acceptable)
- **Decreasing**: Plateau approaching (expected eventually)

### Primary Indicators

| Metric | What It Measures | Positive Signal | Warning Signal |
|--------|-----------------|-----------------|----------------|
| **Capability Growth Rate** | dCapability/dTime | Stable or increasing | Decreasing |
| **LLM Efficiency** | Capability gain per LLM call | Increasing | Flat or decreasing |
| **Loop Cycle Time** | Time per improvement cycle | Stable or decreasing | Increasing |
| **Goal→Compiler Correlation** | Does goal fitness predict compiler success? | r > 0.3 | r < 0.1 |
| **Pattern Reuse Rate** | % of patterns applied more than once | > 30% | < 10% |

### Secondary Loop Metrics

| Loop | Metric | Healthy Range | Plateau Warning |
|------|--------|---------------|-----------------|
| Self-Compiler | Modification success rate | 40-70% | Flat at <40% |
| Memory Reasoner | Memory reasoning ratio | 30-70% | Flat at <30% |
| Goal Evolver | Capability per goal-hour | Increasing | Decreasing |
| Integration Mind | Emergent behavior count | Any > 0 | Zero after week 4 |
| Dreaming Machine | Actionable insight rate | 15-25% | <10% |

### Progress Milestones (Observations, Not Gates)

These are states to observe and record, not prerequisites to satisfy:

**Milestone 1: Operational** (Week 1)
- All five loops executing without crashes
- Metrics being collected
- Baseline capability established

**Milestone 2: Positive Slope** (Week 2-4)
- Capability increasing over time (any positive rate)
- At least one loop showing internal improvement
- Pattern library or memory growing

**Milestone 3: Coupling Observed** (Week 4-8)
- Goal→Compiler correlation coefficient > 0.2
- Cross-loop data flow measurable
- LLM efficiency improving

**Milestone 4: Acceleration Window** (Week 8-12)
- Growth rate is stable or increasing (not decreasing)
- At least 2 loops showing improvement
- Cycle time not increasing

**Milestone 5: Sustained Value** (Month 3+)
- System is genuinely useful (subjective but important)
- Plateau reached at valuable capability level
- Maintenance cost is acceptable

**Milestone 6: Unexpected Capability** (If ever)
- System does something not explicitly programmed
- This is BONUS, not expected
- Record and analyze if it occurs

---

## Part 11: Risk Assessment

### Risks That Prevent Value Creation

| Risk | Why It Matters | How to Detect | Response |
|------|--------------------|--------------|---------|
| **Loops not coupling** | Growth stays purely additive | Goal→Compiler correlation < 0.1 after week 4 | Force more data sharing, simplify coupling |
| **LLM efficiency flat** | Scaffolding not adding value | Capability/LLM-call ratio flat | Re-evaluate pattern library quality |
| **Pattern library low-quality** | Garbage in, garbage out | Pattern reuse rate < 10% | Add human curation, raise thresholds |
| **Goals converge to vagueness** | Evolution failing | Goal diversity collapsing | Add specificity pressure, reset population |
| **Cycle time increasing** | System getting slower | Wall clock per cycle increasing | Profile and optimize, simplify loops |

### Risks That Are Acceptable

| Risk | Why It's OK |
|------|-------------|
| Individual loop underperforming | Focus on the loops that work |
| Plateau after month 3 | Expected; value comes from the plateau level, not infinite growth |
| No emergent behaviors | These are bonus, not requirement |
| LLM dependence floor at 25% | Novel reasoning legitimately needs LLM |

### The Core Risk

The project fails if: **System provides no value above using the LLM directly**.

If the scaffolding (memory, patterns, goals) doesn't make LLM calls more effective, we've built complexity for no benefit. This is the actual failure mode.

---

## Part 12: Internal Kill Criteria

**These are private decision points for when to pivot or stop.**

### Hard Kill Criteria (Abandon This Approach)

| Criterion | Threshold | Timeframe | What It Means |
|-----------|-----------|-----------|---------------|
| **Zero capability growth** | No measurable improvement | 4 weeks | Architecture is fundamentally broken |
| **LLM efficiency decreasing** | Capability/call ratio dropping | 6 weeks | Scaffolding making things worse |
| **All loops failing** | Every loop has plateau warning | 8 weeks | Nothing is working |
| **Negative value** | System worse than raw LLM | Any time | Immediate stop |

### Soft Kill Criteria (Simplify or Pivot)

| Criterion | Threshold | Timeframe | Response |
|-----------|-----------|-----------|----------|
| **Only 1 loop working** | 4 of 5 loops showing plateau warnings | 6 weeks | Focus on the working loop, deprecate others |
| **No coupling** | Goal→Compiler correlation < 0.1 | 8 weeks | Abandon coupling thesis, run loops independently |
| **Linear growth only** | Growth rate not increasing | 12 weeks | Accept linear, optimize for efficiency |
| **Plateau below value threshold** | Capability < "useful" level | 12 weeks | Major architecture rethink |

### Decision Framework

```
Week 4: Check hard kill criteria
        → If any triggered: STOP, analyze why
        → If none: Continue

Week 8: Check soft kill criteria
        → If 2+ triggered: SIMPLIFY (reduce to 2-3 loops)
        → If 1 triggered: INVESTIGATE
        → If none: Continue

Week 12: Assess overall value
        → If system is useful: Continue optimization
        → If system is not useful: Major pivot or stop

Month 6: Final assessment
        → Did we beat raw LLM usage? By how much?
        → Was the complexity worth it?
        → What did we learn?
```

### What "Pivot" Means

If the full BYRD Omega architecture fails, these are fallback options:

1. **Minimal BYRD**: Just Self-Compiler + Pattern Library (simplest compounding loop)
2. **Memory-First BYRD**: Just Memory Reasoner (focus on retrieval efficiency)
3. **Goal-Only BYRD**: Just Goal Evolver (focus on objective optimization)
4. **Tool-Augmented LLM**: Abandon BYRD architecture, use LLM with better prompts

---

## Part 13: The Honest Bet

### What This Approach Has Going For It

1. **Designed for LLM efficiency** - Every component makes LLM calls more valuable
2. **One plausibly multiplicative coupling** - Goal Evolver → Self-Compiler may genuinely accelerate
3. **Risks frontier labs won't take** - Self-modification is our differentiator
4. **Measurable quickly** - We'll know if it's working within 8 weeks
5. **Graceful degradation** - Even if coupling fails, individual loops have value

### What Could Prevent Success

1. **Scaffolding adds no value** - Memory/patterns don't improve LLM efficiency
2. **Coupling doesn't work** - Loops stay independent, growth is purely additive
3. **LLM is the bottleneck** - No amount of scaffolding helps if LLM quality is the limit
4. **Complexity cost exceeds benefit** - System is slower than raw LLM usage
5. **Plateau too early** - Capability level at plateau isn't useful

### The Bet (Honest Version)

This approach bets that:

> **A well-designed scaffolding around an LLM can make each LLM call significantly more valuable, and the scaffolding itself may exhibit mild acceleration for a period before plateauing.**

This is a more modest claim than "exponential AGI." We're betting on:
- 2-5x improvement in LLM efficiency (likely)
- Some period of acceleration (possible)
- Plateau at a useful capability level (the real goal)

### Signals to Watch

| Timeframe | Signal | What It Means | Action |
|-----------|--------|---------------|--------|
| **Week 1** | All loops running | System is operational | Continue |
| **Week 2** | Any positive capability growth | Not completely broken | Continue |
| **Week 4** | LLM efficiency improving | Scaffolding adding value | Continue |
| **Week 8** | Goal→Compiler correlation > 0.2 | Coupling is real | Double down on coupling |
| **Week 12** | Growth rate stable or increasing | Acceleration window open | Optimize further |
| **Month 6** | System is genuinely useful | Success | Maintain and extend |

### If It Doesn't Work

Specific responses to specific failures:

| Failure Mode | Response |
|--------------|----------|
| No coupling | Run loops independently, accept additive growth |
| Only 1-2 loops valuable | Keep those, deprecate the rest |
| Plateau too early | Add more seed patterns, improve goal quality |
| LLM efficiency flat | Re-examine pattern quality, prune bad patterns |
| Worse than raw LLM | Stop, analyze, possibly abandon |

The curve tells the truth. If we're not adding value by week 8, something is fundamentally wrong.

---

## Part 14: Pre-Implementation Requirements

**These technical issues MUST be resolved before implementation begins.**

---

### Issue 1: Undefined Core Functions

The document uses these functions throughout without defining them:

| Function | Used In | Issue |
|----------|---------|-------|
| `embed(text)` | Pattern matching, graph storage | Which embedding model? OpenAI? Local? Cost? |
| `semantic_similarity(a, b)` | Test evaluation, memory reasoning | Cosine similarity on embeddings? Different impl? |
| `llm.generate(prompt)` | Pattern lifting, goal mutation, crossover | Which LLM? Existing `llm_client.py`? New interface? |
| `byrd.answer(input)` | Capability test suite | This interface doesn't exist - how do tests call BYRD? |

**Resolution**: Create `embedding.py` with provider abstraction:

```python
# embedding.py

from typing import List
import numpy as np

class EmbeddingProvider:
    """Abstract embedding provider."""

    async def embed(self, text: str) -> np.ndarray:
        raise NotImplementedError

    async def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        return [await self.embed(t) for t in texts]

class OllamaEmbedding(EmbeddingProvider):
    """Use Ollama's embedding endpoint (local, free)."""

    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model
        self.endpoint = "http://localhost:11434/api/embeddings"

    async def embed(self, text: str) -> np.ndarray:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json={"model": self.model, "prompt": text}
            )
            return np.array(response.json()["embedding"])

class OpenAIEmbedding(EmbeddingProvider):
    """Use OpenAI's embedding API (paid, higher quality)."""

    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.client = openai.AsyncClient()

    async def embed(self, text: str) -> np.ndarray:
        response = await self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return np.array(response.data[0].embedding)

# Global instance - configure at startup
embedding_provider: EmbeddingProvider = OllamaEmbedding()

async def embed(text: str) -> np.ndarray:
    """Global embedding function used throughout."""
    return await embedding_provider.embed(text)

def semantic_similarity(a: str, b: str) -> float:
    """Cosine similarity between two texts."""
    emb_a = embed(a)
    emb_b = embed(b)
    return np.dot(emb_a, emb_b) / (np.linalg.norm(emb_a) * np.linalg.norm(emb_b))
```

**Decision needed**: Ollama (free, local, ~768 dims) or OpenAI (paid, better quality, 1536 dims)?

---

### Issue 2: Test Suite Content Missing

The `CapabilityTestSuite` shows structure but has no actual test cases.

**Resolution**: Create `test_suite/` directory with test files:

```
test_suite/
├── reasoning_tests.json      # 100+ reasoning test cases
├── code_generation_tests.json # 100+ code tests with verification functions
├── research_tests.json       # 50+ research/synthesis tests
├── modification_tests.json   # 30+ self-modification tests
└── meta_learning_tests.json  # 20+ meta-learning tests
```

**Example format** (`reasoning_tests.json`):
```json
[
  {
    "id": "reason_001",
    "input": "If A implies B, and B implies C, and A is true, what can we conclude about C?",
    "expected_output": "C is true",
    "difficulty": 0.2,
    "tags": ["logic", "modus_ponens"]
  },
  {
    "id": "reason_002",
    "input": "Given: All X are Y. Some Y are Z. Can we conclude that some X are Z?",
    "expected_output": "No, this is an invalid syllogism",
    "difficulty": 0.5,
    "tags": ["logic", "syllogism"]
  }
]
```

**Action item**: Create at least 50 test cases per domain before implementation.

---

### Issue 3: Graph Schema Conflict with Existing Memory

The document defines `UnifiedGraph` but BYRD already has `Memory` class.

| New Schema | Existing Schema | Conflict? |
|------------|-----------------|-----------|
| `Experience` | `Experience` | Same name, different properties |
| `Belief` | `Belief` | Same - needs property merge |
| `Goal` | `Desire` | Different concepts - both needed? |
| `Pattern` | (none) | New node type |
| `Capability` | (none) | New node type |
| `Insight` | (none) | New node type |

**Resolution**: Extend `Memory` class rather than replace it:

```python
# Add to memory.py

async def create_pattern(self, context_embedding: List[float], solution_template: str,
                         abstraction_level: int = 0) -> str:
    """Create a Pattern node."""
    pattern_id = f"pattern_{uuid.uuid4().hex[:8]}"
    query = """
    CREATE (p:Pattern {
        id: $id,
        context_embedding: $embedding,
        solution_template: $template,
        abstraction_level: $level,
        success_rate: 0.0,
        application_count: 0,
        created_at: datetime()
    })
    RETURN p.id
    """
    await self._execute(query, {
        "id": pattern_id,
        "embedding": context_embedding,
        "template": solution_template,
        "level": abstraction_level
    })
    return pattern_id

async def create_capability(self, name: str, initial_level: float = 0.0) -> str:
    """Create a Capability tracking node."""
    # ... similar implementation

async def strengthen_patterns(self, query: str, answer: str):
    """Increase confidence in patterns that led to successful answer."""
    # Find patterns that contributed to this answer
    # Increase their success_rate

async def weaken_patterns(self, query: str, answer: str):
    """Decrease confidence in patterns that led to failed answer."""
    # Find patterns that contributed
    # Decrease their success_rate
```

**Decision needed**: Keep `Desire` separate from `Goal` or merge them?

---

### Issue 4: BYRDOmega vs. Existing Architecture Mapping

| BYRDOmega | Maps To | Implementation |
|-----------|---------|----------------|
| `graph` | `Memory` | Use existing Memory |
| `MemoryReasoner` | New class | Uses Memory for retrieval, adds spreading activation |
| `SelfCompiler` | Extends `Coder` | Add pattern library to existing Coder |
| `GoalEvolver` | Parallel to `Seeker` | Seeker executes goals from Evolver |
| `DreamingMachine` | Extends `Dreamer` | Add counterfactual generation to existing Dreamer |

**Resolution**: Create wrapper that composes existing components:

```python
# omega.py

class BYRDOmega:
    """Wrapper that composes existing BYRD components with new capabilities."""

    def __init__(self, byrd_instance):
        self.byrd = byrd_instance

        # Use existing components
        self.memory = byrd_instance.memory
        self.dreamer = byrd_instance.dreamer
        self.seeker = byrd_instance.seeker
        self.actor = byrd_instance.actor

        # Add new capabilities
        self.reasoner = MemoryReasoner(self.memory)
        self.compiler = SelfCompiler(self.memory, byrd_instance.coder)
        self.evolver = GoalEvolver(self.memory)

        # Mode controller
        self.mode = "awake"
        self.mode_controller = ModeController()
```

---

### Issue 5: Missing Method Implementations

These methods are called but never defined:

```python
# Required additions to memory.py
class Memory:
    async def strengthen_patterns(self, query: str, answer: str): ...
    async def weaken_patterns(self, query: str, answer: str): ...
    async def mark_as_superior(self, query: str): ...
    async def record_correction(self, query: str, correct_answer: str): ...
    async def get_neighbors(self, node_id: str) -> List[Tuple[str, float]]: ...
    async def count_experiences(self) -> int: ...
    async def export(self, path: Path): ...
    async def import_from(self, path: Path): ...
    async def clear(self): ...

# Required new functions
async def pursue_goal_step(goal: Goal) -> StepResult:
    """Execute one step toward achieving a goal."""
    # Use Seeker's action selection logic
    # Record experience
    # Return result

async def execute_action(answer: str) -> Action:
    """Convert an answer into an executable action."""
    # Parse answer into action type and parameters
    # Execute via Actor or Seeker

async def evaluate_action_outcome(action: Action) -> bool:
    """Determine if an action succeeded."""
    # Check for errors
    # Verify expected state change
    # Return success/failure
```

---

### Issue 6: Goal vs. Desire Reconciliation

Current BYRD:
- `Desire` nodes emerge from Dreamer reflection
- Desires have `intensity` and provenance
- Seeker pursues desires

New system:
- `Goal` nodes created by GoalEvolver
- Goals have `fitness` and evolutionary lineage
- Goals can mutate and crossover

**Resolution**: Goals are the evolutionary layer ABOVE desires:

```
GoalEvolver
    ↓ creates high-level objectives
Goals
    ↓ decompose into
Desires (existing system)
    ↓ pursued by
Seeker
```

```python
class GoalEvolver:
    async def goal_to_desires(self, goal: Goal) -> List[Desire]:
        """Decompose a Goal into actionable Desires."""
        prompt = f"""
        Break this goal into specific, actionable desires:
        Goal: {goal.description}

        Output 2-4 concrete desires that would help achieve this goal.
        """
        desires_text = await self.llm.generate(prompt)

        desires = []
        for desire_desc in parse_desires(desires_text):
            desire = await self.memory.create_desire(
                description=desire_desc,
                intensity=0.7,
                derived_from_goal=goal.id
            )
            desires.append(desire)

        return desires
```

---

### Issue 7: Safety System Integration

New components must integrate with existing safety:

```python
# In self_compiler.py

class SelfCompiler:
    def __init__(self, memory, coder, safety_monitor):
        self.memory = memory
        self.coder = coder
        self.safety_monitor = safety_monitor  # Existing safety_monitor.py

    async def improve(self, weakness: Weakness) -> ModificationResult:
        # Generate modification
        modification = await self.generate_modification(weakness)

        # Safety check BEFORE applying
        safety_result = await self.safety_monitor.verify_modification_safety(
            modification.file_path,
            modification.new_code,
            modification.rationale
        )

        if not safety_result.safe:
            return ModificationResult(
                success=False,
                reason=f"Safety check failed: {safety_result.reason}"
            )

        # Apply with provenance
        await self.coder.apply_modification_with_provenance(
            modification,
            desire_id=weakness.originating_desire_id
        )
```

---

### Issue 8: Coupling Correlation Computation

**Resolution**: Add explicit coupling tracker:

```python
# coupling_tracker.py

class CouplingTracker:
    """Track correlation between loops."""

    def __init__(self):
        self.goal_fitness_history: List[Tuple[datetime, float]] = []
        self.compiler_success_history: List[Tuple[datetime, bool]] = []

    def record_goal_fitness(self, fitness: float):
        self.goal_fitness_history.append((datetime.now(), fitness))

    def record_compiler_outcome(self, success: bool):
        self.compiler_success_history.append((datetime.now(), success))

    def compute_goal_compiler_correlation(self, window_hours: int = 24) -> float:
        """Compute correlation between goal fitness and compiler success."""
        cutoff = datetime.now() - timedelta(hours=window_hours)

        # Get recent data
        recent_goals = [(t, f) for t, f in self.goal_fitness_history if t > cutoff]
        recent_compiler = [(t, s) for t, s in self.compiler_success_history if t > cutoff]

        if len(recent_goals) < 5 or len(recent_compiler) < 5:
            return 0.0  # Not enough data

        # Align by time buckets (1 hour)
        goal_by_hour = self._bucket_by_hour(recent_goals, agg=np.mean)
        compiler_by_hour = self._bucket_by_hour(recent_compiler, agg=np.mean)

        # Get overlapping hours
        common_hours = set(goal_by_hour.keys()) & set(compiler_by_hour.keys())
        if len(common_hours) < 3:
            return 0.0

        goal_values = [goal_by_hour[h] for h in sorted(common_hours)]
        compiler_values = [compiler_by_hour[h] for h in sorted(common_hours)]

        # Pearson correlation
        correlation, _ = pearsonr(goal_values, compiler_values)
        return correlation if not np.isnan(correlation) else 0.0
```

---

### Issue 9: Dependencies Update

Add to `requirements.txt`:

```
# Existing dependencies
neo4j>=5.0.0
httpx>=0.25.0
anthropic>=0.39.0
pyyaml>=6.0
fastapi>=0.109.0
uvicorn[standard]
websockets>=12.0

# New dependencies for Option B
numpy>=1.24.0
scipy>=1.10.0          # For ttest_ind, pdist, pearsonr
scikit-learn>=1.3.0    # For clustering, optional
openai>=1.0.0          # If using OpenAI embeddings (optional)
```

---

### Issue 10: BYRD Answer Interface for Testing

The test suite needs to call BYRD. Add interface:

```python
# In byrd.py

class BYRD:
    async def answer(self, query: str) -> str:
        """
        Answer a query using full BYRD capabilities.
        Used by CapabilityTestSuite for measurement.
        """
        # Record as experience
        exp_id = await self.memory.record_experience(
            content=f"Test query: {query}",
            type="test"
        )

        # Try memory-first reasoning
        memory_answer = await self.reasoner.reason(query)

        if memory_answer.confidence > 0.7:
            return memory_answer.answer

        # Fall back to Actor (LLM)
        actor_response = await self.actor.respond(query)

        # Record the answer for future memory retrieval
        await self.memory.record_experience(
            content=f"Answer: {actor_response}",
            type="answer",
            linked_to=exp_id
        )

        return actor_response
```

---

### Pre-Implementation Checklist

Before writing any code:

- [ ] **Decide embedding provider**: Ollama (free) or OpenAI (paid)?
- [ ] **Create test_suite/ directory** with at least 50 tests per domain
- [ ] **Add new node types to memory.py**: Pattern, Capability, Insight
- [ ] **Add missing methods to memory.py**: strengthen_patterns, weaken_patterns, etc.
- [ ] **Create embedding.py** with provider abstraction
- [ ] **Create coupling_tracker.py** for correlation measurement
- [ ] **Update requirements.txt** with scipy, numpy
- [ ] **Add BYRD.answer() method** for test suite interface
- [ ] **Decide Goal vs Desire relationship**: Parallel or hierarchical?
- [ ] **Document safety integration points** for SelfCompiler

---

## Part 15: Codebase Integration Map

**How Option B integrates with the existing BYRD codebase.**

This section provides the exact mapping from Option B components to existing files, what to modify, what to create, and what can be deleted.

---

### Current Codebase Structure

```
/Users/kurultai/BYRD/
├── Core Components
│   ├── byrd.py              (946 lines)  - Main orchestrator
│   ├── memory.py            (6624 lines) - Neo4j interface [LARGEST FILE]
│   ├── dreamer.py           (2931 lines) - Reflection/dream cycles
│   ├── seeker.py            (3689 lines) - Action execution
│   ├── actor.py             (~200 lines) - Claude API interface
│   ├── coder.py             (476 lines)  - Code modification
│   ├── llm_client.py        (546 lines)  - LLM abstraction
│   └── event_bus.py         (~300 lines) - Event system
│
├── AGI Seed Components (Phase 1-5)
│   ├── self_model.py        (780 lines)  - Capability tracking
│   ├── world_model.py       (683 lines)  - Prediction system
│   ├── accelerators.py      (711 lines)  - Graph reasoning, challenges
│   ├── meta_learning.py     (688 lines)  - Meta-metrics, plateaus
│   └── kernel/              - AGI seed kernel
│
├── Safety Components (PROTECTED)
│   ├── safety_monitor.py    (609 lines)  - Modification safety
│   ├── constitutional.py    (~200 lines) - Constraints
│   ├── provenance.py        (~200 lines) - Provenance tracking
│   ├── modification_log.py  (~300 lines) - Audit trail
│   ├── corrigibility.py     (547 lines)  - Corrigibility tests
│   └── rollback.py          (498 lines)  - Rollback system
│
├── Utility Components
│   ├── graph_algorithms.py  (823 lines)  - PageRank, spreading activation
│   ├── gnn_layer.py         (687 lines)  - Graph neural network [UNUSED]
│   ├── narrator.py          (470 lines)  - Event narrations
│   ├── quantum_randomness.py(436 lines)  - ANU QRNG integration
│   ├── aitmpl_client.py     (504 lines)  - Template registry
│   └── server.py            (1568 lines) - WebSocket server
│
├── Installers
│   └── installers/          - Template installers (keep as-is)
│
└── Junk Directories (DELETE)
    ├── -o/                  - Accidental creation
    ├── -sL/                 - Accidental creation
    ├── cd/                  - Accidental creation
    ├── curl/                - Accidental creation
    ├── https:/              - Accidental creation
    └── plugin.tar.gz/       - Accidental creation
```

---

### File-by-File Integration Plan

#### Files to MODIFY (Core Integration)

| File | Lines | Option B Role | Changes Required |
|------|-------|---------------|------------------|
| **byrd.py** | 946 | Wrap with BYRDOmega | Add `BYRDOmega` wrapper, mode controller, `answer()` method |
| **memory.py** | 6624 | Becomes UnifiedGraph | Add Pattern, Capability, Insight nodes; add strengthen/weaken methods |
| **dreamer.py** | 2931 | Integrate DreamingMachine | Add counterfactual generation, hypothesis generation, insight extraction |
| **seeker.py** | 3689 | Integrate GoalEvolver | Add goal fitness tracking, goal-to-desire decomposition |
| **coder.py** | 476 | Integrate SelfCompiler | Add pattern library integration, pattern extraction on success |
| **llm_client.py** | 546 | Use for all LLM calls | Add usage tracking for LLM efficiency metrics |
| **event_bus.py** | ~300 | Add new events | Add METRICS_UPDATED, KILL_CRITERIA_*, LOOP_HEALTH_*, COUPLING_MEASURED |
| **server.py** | 1568 | Add metrics endpoints | Add /api/metrics/acceleration, /api/metrics/history |

#### Files to EXTEND (AGI Seed → Option B Merge)

| File | Lines | Option B Overlap | Action |
|------|-------|------------------|--------|
| **self_model.py** | 780 | CapabilityTracker, CapabilityTestSuite | MERGE: Add test suite, domain weights, growth rate computation |
| **world_model.py** | 683 | MemoryReasoner prediction | MERGE: Add spreading activation integration, prediction confidence |
| **accelerators.py** | 711 | SelfCompiler patterns, challenges | ABSORB: Move pattern library here, add abstraction lifting |
| **meta_learning.py** | 688 | Capability hierarchy, plateau detection | KEEP: Already implements plateau response, add kill criteria |

**Merge Strategy:**

```python
# self_model.py additions (merge with CapabilityTracker)
class SelfModel:
    # Existing capability tracking...

    # NEW: Add Option B CapabilityTestSuite integration
    async def measure_with_test_suite(self, test_suite: CapabilityTestSuite) -> CapabilityScore:
        """Measure all capabilities using the test suite."""
        ...

    # NEW: Add growth rate computation
    def compute_growth_rate(self, window_days: int = 7) -> float:
        """Compute capability growth rate."""
        ...

    # NEW: Add LLM efficiency tracking
    def track_llm_call(self, capability_gain: float):
        """Track LLM call for efficiency computation."""
        ...
```

```python
# accelerators.py additions (merge with SelfCompiler)
class PatternLibrary:
    """Merged from Option B SelfCompiler."""

    def __init__(self):
        self.patterns: List[Pattern] = []
        self.adaptive_threshold = AdaptiveThreshold()

    async def maybe_lift_pattern(self, pattern: Pattern):
        """Abstraction lifting from Option B."""
        ...

    def add_pattern(self, pattern: Pattern):
        """With diversity maintenance."""
        ...
```

#### Files to KEEP AS-IS (Safety, Protected)

| File | Lines | Reason |
|------|-------|--------|
| **safety_monitor.py** | 609 | Protected, integrate via SelfCompiler.verify_safety() |
| **constitutional.py** | ~200 | Protected, no changes needed |
| **provenance.py** | ~200 | Protected, no changes needed |
| **modification_log.py** | ~300 | Protected, no changes needed |
| **corrigibility.py** | 547 | Protected, no changes needed |
| **rollback.py** | 498 | Protected, use for ModificationRollback |

#### Files to KEEP (Utility)

| File | Lines | Reason |
|------|-------|--------|
| **graph_algorithms.py** | 823 | Contains SpreadingActivation, PageRank - use in MemoryReasoner |
| **narrator.py** | 470 | Used by event_bus for inner voice |
| **quantum_randomness.py** | 436 | Used by memory, dreamer for exploration |
| **aitmpl_client.py** | 504 | Used by seeker, installers for templates |

#### Files Potentially UNUSED (Verify Before Delete)

| File | Lines | Status | Action |
|------|-------|--------|--------|
| **gnn_layer.py** | 687 | Not imported by any file | Archive, then delete after Option B stable |

---

### New Files to CREATE

```
/Users/kurultai/BYRD/
├── New Option B Files
│   ├── embedding.py           - Embedding provider abstraction
│   ├── coupling_tracker.py    - Loop correlation tracking
│   ├── omega.py               - BYRDOmega wrapper class
│   ├── memory_reasoner.py     - Spreading activation reasoning
│   ├── goal_evolver.py        - Evolutionary goal system
│   └── dreaming_machine.py    - Counterfactual/hypothesis generation
│
├── Test Suite
│   └── test_suite/
│       ├── __init__.py
│       ├── reasoning_tests.json
│       ├── code_generation_tests.json
│       ├── research_tests.json
│       ├── modification_tests.json
│       └── meta_learning_tests.json
│
└── Config Updates
    └── config.yaml            - Add Option B configuration section
```

---

### Detailed Integration: byrd.py

The main orchestrator needs the BYRDOmega wrapper:

```python
# byrd.py modifications

# Add imports at top
from omega import BYRDOmega
from memory_reasoner import MemoryReasoner
from goal_evolver import GoalEvolver
from coupling_tracker import CouplingTracker

class BYRD:
    # ... existing __init__ ...

    def __init__(self, config_path: str = "config.yaml"):
        # Existing initialization...

        # NEW: Initialize Option B components
        self.coupling_tracker = CouplingTracker()
        self.memory_reasoner = MemoryReasoner(self.memory, self.llm_client)
        self.goal_evolver = GoalEvolver(self.memory, self.llm_client)

        # NEW: Wrap in Omega for unified interface
        self.omega = BYRDOmega(self)

    # NEW: Add answer() method for test suite
    async def answer(self, query: str) -> str:
        """Answer a query using full BYRD capabilities."""
        # Try memory-first
        memory_result = await self.memory_reasoner.reason(query)

        if memory_result.confidence > 0.7:
            return memory_result.answer

        # Fallback to Actor
        response = await self.actor.respond(query)

        # Record for future memory retrieval
        await self.memory.record_experience(
            content=f"Q: {query}\nA: {response}",
            type="qa_pair"
        )

        return response
```

---

### Detailed Integration: memory.py

Add new node types and methods:

```python
# memory.py additions (add near other create_* methods)

async def create_pattern(self, context_embedding: List[float],
                         solution_template: str,
                         abstraction_level: int = 0) -> str:
    """Create a Pattern node for the Self-Compiler."""
    pattern_id = f"pattern_{uuid.uuid4().hex[:8]}"

    query = """
    CREATE (p:Pattern {
        id: $id,
        context_embedding: $embedding,
        solution_template: $template,
        abstraction_level: $level,
        success_rate: 0.0,
        application_count: 0,
        created_at: datetime()
    })
    RETURN p.id
    """

    await self._execute(query, {
        "id": pattern_id,
        "embedding": context_embedding,
        "template": solution_template,
        "level": abstraction_level
    })

    await event_bus.emit(Event(
        type=EventType.PATTERN_CREATED,
        data={"id": pattern_id, "template": solution_template[:100]}
    ))

    return pattern_id

async def strengthen_patterns(self, query_embedding: List[float],
                              success: bool, strength_delta: float = 0.1):
    """Adjust pattern strength based on outcome."""
    query = """
    MATCH (p:Pattern)
    WHERE gds.similarity.cosine(p.context_embedding, $embedding) > 0.7
    SET p.success_rate = CASE
        WHEN $success THEN p.success_rate + $delta * (1 - p.success_rate)
        ELSE p.success_rate - $delta * p.success_rate
    END,
    p.application_count = p.application_count + 1
    RETURN p.id, p.success_rate
    """

    await self._execute(query, {
        "embedding": query_embedding,
        "success": success,
        "delta": strength_delta
    })

async def get_neighbors(self, node_id: str) -> List[Tuple[str, float]]:
    """Get neighbors with edge weights for spreading activation."""
    query = """
    MATCH (n)-[r]-(m)
    WHERE n.id = $node_id
    RETURN m.id as neighbor_id,
           COALESCE(r.strength, r.confidence, 1.0) as weight
    """

    results = await self._execute(query, {"node_id": node_id})
    return [(r["neighbor_id"], r["weight"]) for r in results]

async def count_experiences(self) -> int:
    """Count total experiences for metrics."""
    query = "MATCH (e:Experience) RETURN count(e) as count"
    result = await self._execute(query)
    return result[0]["count"] if result else 0

async def export_graph(self, path: Path):
    """Export graph to Cypher file for checkpoints."""
    # Implementation using APOC procedures or manual export
    ...

async def import_graph(self, path: Path):
    """Import graph from Cypher file."""
    ...

async def clear_graph(self):
    """Clear all nodes for fresh start."""
    await self._execute("MATCH (n) DETACH DELETE n")
```

---

### Detailed Integration: dreamer.py

Integrate DreamingMachine capabilities:

```python
# dreamer.py additions (add to Dreamer class)

async def generate_counterfactuals(self, experience: Dict) -> List[Dict]:
    """Generate counterfactual variations of an experience."""
    prompt = f"""
    Given this experience:
    {json.dumps(experience)}

    Generate 3 counterfactual variations:
    1. What if a different action was taken?
    2. What if the context was slightly different?
    3. What if the goal was different?

    Output as JSON array.
    """

    response = await self.llm_client.generate(prompt)
    return json.loads(response)

async def generate_hypotheses(self, patterns: List[Dict]) -> List[Dict]:
    """Generate novel hypotheses from observed patterns."""
    prompt = f"""
    Given these observed patterns:
    {json.dumps(patterns)}

    Generate 2-3 hypotheses about:
    1. Why these patterns exist
    2. What would happen if they were combined
    3. What gaps in understanding they reveal

    Output as JSON array with 'hypothesis' and 'testable_prediction' fields.
    """

    response = await self.llm_client.generate(prompt)
    return json.loads(response)

async def dream_cycle_extended(self) -> List[Dict]:
    """Extended dream cycle with Option B features."""
    insights = []

    # 1. Standard reflection
    reflection = await self._reflect()

    # 2. Select experiences for replay
    high_value_experiences = await self.memory.get_experiences(
        where="surprise > 0.5 OR importance > 0.7",
        limit=10
    )

    # 3. Generate counterfactuals
    for exp in high_value_experiences:
        counterfactuals = await self.generate_counterfactuals(exp)
        for cf in counterfactuals:
            if self._is_valuable_counterfactual(cf, exp):
                insights.append({
                    "type": "counterfactual",
                    "original": exp,
                    "variation": cf
                })

    # 4. Find cross-experience patterns
    patterns = await self._find_patterns_across_experiences(high_value_experiences)

    # 5. Generate hypotheses
    hypotheses = await self.generate_hypotheses(patterns)
    for hyp in hypotheses:
        insights.append({
            "type": "hypothesis",
            "content": hyp
        })

    return insights
```

---

### Detailed Integration: seeker.py

Integrate GoalEvolver:

```python
# seeker.py additions (add to Seeker class)

async def pursue_goal(self, goal: Dict, max_steps: int = 10) -> Dict:
    """Pursue a goal from GoalEvolver."""
    # Decompose goal into desires
    desires = await self.goal_to_desires(goal)

    results = []
    for desire in desires:
        # Use existing desire fulfillment
        result = await self.fulfill_desire(desire)
        results.append(result)

    # Aggregate results
    success = all(r.get("success", False) for r in results)

    return {
        "goal_id": goal["id"],
        "success": success,
        "steps_taken": len(results),
        "results": results
    }

async def goal_to_desires(self, goal: Dict) -> List[Dict]:
    """Decompose a Goal into actionable Desires."""
    prompt = f"""
    Break this goal into 2-4 specific, actionable desires:
    Goal: {goal['description']}

    Output as JSON array with 'description' and 'intensity' fields.
    """

    response = await self.llm_client.generate(prompt)
    desire_specs = json.loads(response)

    desires = []
    for spec in desire_specs:
        desire_id = await self.memory.create_desire(
            description=spec["description"],
            intensity=spec.get("intensity", 0.7)
        )
        desires.append({"id": desire_id, **spec})

    return desires
```

---

### Directories to DELETE

These directories appear to have been created accidentally (likely from malformed shell commands):

```bash
# Run these commands to clean up
rm -rf /Users/kurultai/BYRD/-o
rm -rf /Users/kurultai/BYRD/-sL
rm -rf /Users/kurultai/BYRD/cd
rm -rf /Users/kurultai/BYRD/curl
rm -rf /Users/kurultai/BYRD/https:
rm -rf /Users/kurultai/BYRD/plugin.tar.gz
```

---

### Config Updates

Add Option B section to `config.yaml`:

```yaml
# config.yaml additions

option_b:
  enabled: true

  # Embedding configuration
  embedding:
    provider: "ollama"  # or "openai"
    model: "nomic-embed-text"  # or "text-embedding-3-small"

  # Loop configuration
  loops:
    self_compiler:
      enabled: true
      pattern_library_max_size: 1000
      abstraction_lift_threshold: 3  # domains before lifting

    memory_reasoner:
      enabled: true
      confidence_threshold: 0.7
      spreading_activation_decay: 0.7

    goal_evolver:
      enabled: true
      population_size: 20
      mutation_rate: 0.3
      generations_before_evaluation: 5

    dreaming_machine:
      enabled: true
      counterfactuals_per_experience: 3
      hypothesis_generation: true

  # Kill criteria
  kill_criteria:
    hard:
      zero_growth_weeks: 4
      llm_efficiency_decline_weeks: 6
    soft:
      no_coupling_weeks: 8
      linear_only_weeks: 12

  # Metrics
  metrics:
    measurement_interval_minutes: 60
    capability_test_interval_hours: 24
    checkpoint_interval_minutes: 30
```

---

### Implementation Order

**Week 1: Foundation**
1. Clean up junk directories
2. Create `embedding.py` with Ollama provider
3. Create `coupling_tracker.py`
4. Add new node types to `memory.py` (Pattern, Capability, Insight)
5. Add new event types to `event_bus.py`
6. Update `requirements.txt`

**Week 2: Core Loops**
1. Create `memory_reasoner.py` (using `graph_algorithms.py` spreading activation)
2. Extend `accelerators.py` with PatternLibrary
3. Create `goal_evolver.py`
4. Extend `self_model.py` with CapabilityTestSuite

**Week 3: Integration**
1. Create `omega.py` wrapper
2. Modify `byrd.py` to use BYRDOmega
3. Extend `dreamer.py` with counterfactual generation
4. Extend `seeker.py` with goal pursuit
5. Integrate `coder.py` with pattern extraction

**Week 4: Metrics & Testing**
1. Create `test_suite/` with initial tests
2. Add metrics endpoints to `server.py`
3. Add metrics panel to visualizer
4. Run initial capability baseline
5. Begin monitoring loop health

---

## Part 16: Metrics Visualization

All metrics described in this document should be visible in the BYRD 3D visualizer.

### Required Visualizer Updates

Add a **Metrics Panel** to `byrd-3d-visualization.html` displaying:

#### Primary Metrics (Always Visible)
```
┌─────────────────────────────────────────┐
│ ACCELERATION METRICS                     │
├─────────────────────────────────────────┤
│ Capability Score:     0.42 → 0.47 (+12%) │
│ LLM Efficiency:       1.2 cap/call       │
│ Growth Rate:          +0.8%/day          │
│ Goal→Compiler r:      0.31              │
│ Memory Reasoning:     34%               │
└─────────────────────────────────────────┘
```

#### Loop Health Indicators (Color-Coded)
```
┌─────────────────────────────────────────┐
│ LOOP STATUS                              │
├─────────────────────────────────────────┤
│ 🟢 Self-Compiler      success: 58%      │
│ 🟡 Memory Reasoner    ratio: 34%        │
│ 🟢 Goal Evolver       fitness: +0.12    │
│ 🔴 Integration Mind   emergent: 0       │
│ 🟡 Dreaming Machine   insight: 18%      │
└─────────────────────────────────────────┘

🟢 = Healthy (above threshold)
🟡 = Warning (plateau warning triggered)
🔴 = Critical (below acceptable threshold)
```

#### Kill Criteria Dashboard (Collapsible)
```
┌─────────────────────────────────────────┐
│ KILL CRITERIA STATUS          [Week 4]  │
├─────────────────────────────────────────┤
│ Hard Criteria:                          │
│   ✓ Capability growth positive          │
│   ✓ LLM efficiency not decreasing       │
│   ✓ At least 1 loop healthy             │
│   ✓ Value above raw LLM                 │
│                                         │
│ Soft Criteria:                          │
│   ✓ 2+ loops healthy                    │
│   ⚠ Coupling correlation: 0.18 (< 0.2)  │
│   ✓ Growth rate stable                  │
└─────────────────────────────────────────┘
```

### Implementation in server.py

Add new API endpoints:

```python
@app.get("/api/metrics/acceleration")
async def get_acceleration_metrics():
    """Return all acceleration metrics for visualizer."""
    return {
        "capability_score": await self_model.get_overall_capability(),
        "capability_history": await self_model.get_capability_history(days=30),
        "llm_efficiency": await compute_llm_efficiency(),
        "growth_rate": await compute_growth_rate(),
        "goal_compiler_correlation": await compute_coupling_correlation(),
        "memory_reasoning_ratio": await memory_reasoner.effectiveness_ratio(),
        "loop_health": {
            "self_compiler": await self_compiler.get_health_status(),
            "memory_reasoner": await memory_reasoner.get_health_status(),
            "goal_evolver": await goal_evolver.get_health_status(),
            "integration_mind": await integration_mind.get_health_status(),
            "dreaming_machine": await dreaming_machine.get_health_status(),
        },
        "kill_criteria": await evaluate_kill_criteria(),
    }

@app.get("/api/metrics/history")
async def get_metrics_history(days: int = 30):
    """Return historical metrics for trend visualization."""
    return await metrics_store.get_history(days=days)
```

### Visualization Requirements

1. **Real-time updates**: Metrics should update via WebSocket every cycle
2. **Trend lines**: Show 7-day and 30-day trends for key metrics
3. **Threshold indicators**: Visual markers for kill criteria thresholds
4. **Coupling visualization**: Show Goal→Compiler correlation as edge thickness
5. **Color coding**: Green/Yellow/Red for loop health based on thresholds defined in Part 6

### Event Types to Add

```python
# In event_bus.py
METRICS_UPDATED = "metrics_updated"
KILL_CRITERIA_WARNING = "kill_criteria_warning"
KILL_CRITERIA_TRIGGERED = "kill_criteria_triggered"
LOOP_HEALTH_CHANGED = "loop_health_changed"
COUPLING_MEASURED = "coupling_measured"
```

---

## Conclusion

Option B is a bet on **LLM efficiency through architectural scaffolding**, with a secondary bet on **mild acceleration through loop coupling**.

The honest expectation:
- **Most likely**: 2-5x LLM efficiency improvement, sublinear growth with plateau
- **Possible**: Temporary acceleration window, valuable capability level
- **Unlikely but monitored**: Emergent behaviors, sustained acceleration

We build first. We measure honestly. We pivot when the data tells us to.

The core question isn't "can we achieve AGI?" It's "can we make LLM calls significantly more valuable through smart scaffolding?"

If yes, we have something useful. If no, we learn and try something else.

**Build it. Measure it. Be honest about what the data shows.**

---

## Appendix A: Core Invariants

These properties must ALWAYS be true for the system to function correctly:

### Structural Invariants

| Invariant | What It Means | Violated By |
|-----------|---------------|-------------|
| **Graph is source of truth** | All state lives in Neo4j | Local caches disagreeing with graph |
| **Provenance is complete** | Every modification traces to a desire | Self-modification without desire |
| **Patterns are versioned** | Pattern changes create new versions, not mutations | In-place pattern modification |
| **Goals have fitness** | Every goal has a measured fitness score | Goals without evaluation |
| **Experiences are immutable** | Once recorded, experiences don't change | Editing historical experiences |

### Behavioral Invariants

| Invariant | What It Means | Violated By |
|-----------|---------------|-------------|
| **Safety check before modification** | Every code change passes safety_monitor first | Bypassing safety checks |
| **Memory-first reasoning** | Try memory before LLM for every query | Always going to LLM |
| **Metrics always recorded** | Every cycle updates metrics | Silent failures |
| **Graceful mode transitions** | Checkpoints before every mode change | Transitions without checkpoints |
| **Kill criteria always evaluated** | Hard criteria checked every week | Ignoring kill signals |

### Numerical Invariants

| Invariant | Range | Violated By |
|-----------|-------|-------------|
| **Pattern success_rate** | [0.0, 1.0] | Values outside range |
| **Goal fitness** | Unbounded, but typically [-1.0, 10.0] | Extreme values without investigation |
| **Confidence scores** | [0.0, 1.0] | Uncalibrated confidence |
| **Correlation coefficients** | [-1.0, 1.0] | Invalid correlation calculations |

---

## Appendix B: Quick Reference Card

### The Five Loops

| Loop | Core Mechanism | Success Metric | Plateau Warning |
|------|---------------|----------------|-----------------|
| **Self-Compiler** | Pattern library improves prompts | Mod success rate > 50% | Flat at < 40% |
| **Memory Reasoner** | Graph answers queries | Memory ratio > 50% | Flat at < 30% |
| **Goal Evolver** | Goals evolve via fitness | Fitness ↑ per generation | Fitness flat |
| **Dreaming Machine** | Counterfactuals generate insights | Insight rate > 15% | Rate < 10% |
| **Integration Mind** | Cross-loop synergy | Emergent behaviors > 0 | None after week 4 |

### Key Metrics

```
PRIMARY:    dCapability/dTime (growth rate trend)
SECONDARY:  LLM efficiency (capability gain / LLM calls)
COUPLING:   Goal→Compiler correlation (target: r > 0.3)
HEALTH:     Loop status (green/yellow/red per loop)
```

### Kill Criteria Summary

| Type | Criterion | Timeframe |
|------|-----------|-----------|
| **HARD** | Zero capability growth | 4 weeks → STOP |
| **HARD** | LLM efficiency decreasing | 6 weeks → STOP |
| **SOFT** | Only 1 loop working | 6 weeks → SIMPLIFY |
| **SOFT** | No coupling observed | 8 weeks → RUN INDEPENDENTLY |
| **SOFT** | Linear growth only | 12 weeks → ACCEPT LINEAR |

### Mode Transition Diagram

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

### File Quick Reference

| To Modify | File |
|-----------|------|
| Add node type | memory.py |
| Add event | event_bus.py |
| Change LLM calls | llm_client.py |
| Add metric | self_model.py |
| Add pattern logic | accelerators.py |
| Add safety check | safety_monitor.py (PROTECTED) |

### One-Liner Philosophy

> **"Make each LLM call 10x more valuable through smart scaffolding."**

---

*Document version: 2.0*
*Updated: December 26, 2024*
*Philosophy: Honest assessment, measurable claims, graceful degradation*
*Design: Scaffolding not replacement, measure before believing*
