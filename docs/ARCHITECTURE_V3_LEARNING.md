# BYRD Architecture V3: Learning-Enabled AGI System

> **⚠️ SUPERSEDED**: This document has been merged into [UNIFIED_AGI_PLAN.md](./UNIFIED_AGI_PLAN.md).
> The unified plan combines this document's learning components with AGI_SEED_V2's execution engine.

## Overview

This document describes the target architecture after implementing both:
1. **Option B** - Five compounding loops for capability acceleration
2. **Learning Extensions** - Components that enable genuine learning despite a frozen LLM

**The Hypothesis:** AGI can emerge from architecture + memory + learning components, not LLM intelligence alone.

---

## Architectural Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LAYER 4: LEARNING SUBSTRATE                          │
│                                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐               │
│  │   INTUITION     │ │     WORLD       │ │    LEARNED      │               │
│  │    NETWORK      │ │     MODEL       │ │   RETRIEVER     │               │
│  │  (learns taste) │ │(learns causality)│ │(learns relevance)│              │
│  └────────┬────────┘ └────────┬────────┘ └────────┬────────┘               │
│           │                   │                   │                         │
│           └───────────────────┼───────────────────┘                         │
│                               ▼                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                      LAYER 3: OPTION B (Five Loops)                         │
│                                                                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   MEMORY     │ │    SELF-     │ │    GOAL      │ │   DREAMING   │       │
│  │  REASONER    │ │  COMPILER    │ │   EVOLVER    │ │   MACHINE    │       │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘       │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                         │
│                          ┌────────▼────────┐                               │
│                          │   BYRD OMEGA    │                               │
│                          │  (Integration)  │                               │
│                          └────────┬────────┘                               │
├────────────────────────────────────┼────────────────────────────────────────┤
│                      LAYER 2: CORE AGENTS                                   │
│                                                                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   DREAMER    │ │    SEEKER    │ │    ACTOR     │ │    CODER     │       │
│  │ (reflection) │ │ (fulfillment)│ │  (reasoning) │ │   (coding)   │       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                      LAYER 1: MEMORY + LLM                                  │
│                                                                             │
│  ┌─────────────────────────────────────┐  ┌───────────────────────────────┐│
│  │         HIERARCHICAL MEMORY         │  │         LLM CLIENT            ││
│  │              (Neo4j)                │  │    (with optional LoRA)       ││
│  │                                     │  │                               ││
│  │  L0: Experiences                    │  │  ┌─────────┐ ┌─────────┐     ││
│  │  L1: Patterns                       │  │  │  Base   │ │  LoRA   │     ││
│  │  L2: Principles                     │  │  │  Model  │ │ Adapter │     ││
│  │  L3: Axioms                         │  │  └─────────┘ └─────────┘     ││
│  │  L4: Meta-Axioms                    │  │                               ││
│  │                                     │  │  + Code-as-Memory            ││
│  └─────────────────────────────────────┘  └───────────────────────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Integration Analysis

### How Learning Components Extend Option B

| Option B Loop | Learning Extension | Integration Point |
|---------------|-------------------|-------------------|
| **Memory Reasoner** | Learned Retriever | Replaces embedding similarity with trainable attention |
| **Self-Compiler** | Code Learner | Extends patterns to executable code files |
| **Goal Evolver** | Intuition Network | Guides goal fitness with learned preferences |
| **Dreaming Machine** | World Model | Uses causal predictions for counterfactuals |
| **Integration Mind** | All of above | Orchestrates learning during DREAMING mode |

### File-Level Integration

| Existing File | Extension | Change Type |
|---------------|-----------|-------------|
| `memory.py` | Add AbstractionLevel, promote() | Extend |
| `memory_reasoner.py` | Add LearnedRetriever as scorer | Extend |
| `accelerators.py` | Add CodeLearner for codification | Extend |
| `omega.py` | Add IntuitionNetwork, WorldModel | Extend |
| `llm_client.py` | Add LoRA adapter loading | Extend |
| `dreaming_machine.py` | Use WorldModel predictions | Extend |
| `goal_evolver.py` | Use IntuitionNetwork for fitness | Extend |
| N/A | `world_model.py` | New |
| N/A | `intuition_network.py` | New |
| N/A | `learned_retriever.py` | New |
| N/A | `code_learner.py` | New |
| N/A | `continuous_learner.py` | New |
| N/A | `learned_strategies/` | New directory |

---

## Layer 1: Hierarchical Memory

### Extended Memory Schema

```cypher
// Abstraction Hierarchy
(:Experience {abstraction_level: 0})
  -[:PROMOTED_TO]->
(:Pattern {abstraction_level: 1})
  -[:PROMOTED_TO]->
(:Principle {abstraction_level: 2})
  -[:PROMOTED_TO]->
(:Axiom {abstraction_level: 3})
  -[:PROMOTED_TO]->
(:MetaAxiom {abstraction_level: 4})

// Promotion triggers when N similar nodes exist
// Lower levels are specific, higher levels are general
// Retrieval prefers higher levels for familiar situations
// Retrieval uses lower levels for novel situations
```

### Abstraction Level Properties

| Level | Node Type | Example | Promotion Threshold |
|-------|-----------|---------|---------------------|
| L0 | Experience | "Searched for 'consciousness', got 0 results" | N/A (base) |
| L1 | Pattern | "Abstract philosophical terms return no search results" | 3 similar experiences |
| L2 | Principle | "Route philosophical desires to introspection, not search" | 3 related patterns |
| L3 | Axiom | "Match capability type to desire type for success" | 3 connected principles |
| L4 | Meta-Axiom | "Abstractions that predict outcomes are valuable" | 2 meta-observations |

### Code-as-Memory

```
learned_strategies/
├── desire_routing/
│   ├── philosophical_to_introspection.py
│   ├── research_to_ddg_search.py
│   └── self_understanding_to_source_introspect.py
├── pattern_matching/
│   ├── orphan_threshold_check.py
│   └── belief_consolidation_trigger.py
└── decision_making/
    ├── should_reconcile_first.py
    └── when_to_crystallize.py
```

When BYRD learns a stable pattern, it **writes code** that embodies the pattern. Future decisions execute code instead of re-reasoning.

---

## Layer 2: LLM with Learning

### LoRA Adapter System

```python
class AdaptiveLLMClient:
    """LLM client with optional LoRA fine-tuning."""

    def __init__(self, base_model, config):
        self.base_model = base_model
        self.adapters = {}  # domain -> LoRA adapter
        self.training_buffer = []

    async def generate(self, prompt, domain=None):
        """Generate with appropriate adapter."""
        adapter = self.adapters.get(domain)
        return await self._generate_with_adapter(prompt, adapter)

    async def record_outcome(self, prompt, response, outcome, quality):
        """Record for future training."""
        if quality > 0.8 and outcome == "success":
            self.training_buffer.append({
                'input': prompt,
                'output': response,
                'domain': self._classify_domain(prompt)
            })

        if len(self.training_buffer) >= 100:
            await self._train_adapters()
```

### Training Schedule

| Mode | Training Activity | Frequency |
|------|-------------------|-----------|
| AWAKE | Collect training examples | Continuous |
| DREAMING | LoRA fine-tuning | Every 100 examples |
| EVOLVING | Evaluate adapter effectiveness | Per generation |
| COMPILING | Use specialized adapters | As needed |

---

## Layer 3: Option B Loops (Extended)

### Loop 1: Memory Reasoner + Learned Retriever

```python
class EnhancedMemoryReasoner:
    """Memory Reasoner with learned retrieval."""

    def __init__(self, memory, llm_client, config):
        self.memory = memory
        self.llm_client = llm_client
        self.learned_retriever = LearnedRetriever()  # NEW

    async def reason(self, query):
        # 1. Get retrieval candidates
        candidates = await self.memory.get_candidates(query, limit=100)

        # 2. Score with LEARNED retriever (not just embedding similarity)
        scored = await self.learned_retriever.score(query, candidates)

        # 3. Take top-k
        top_k = sorted(scored, key=lambda x: x['score'], reverse=True)[:10]

        # 4. Compose answer or fall back to LLM
        answer, confidence = await self._compose_from_memory(top_k)

        if confidence >= self.threshold:
            return MemoryAnswer(answer, confidence, source="memory")

        # 5. LLM fallback with top-k as context
        llm_answer = await self._llm_with_context(query, top_k)

        # 6. Record outcome for retriever training
        await self.learned_retriever.record_feedback(
            query, top_k, llm_answer, was_helpful=[...]
        )

        return MemoryAnswer(llm_answer, 0.5, source="llm_augmented")
```

### Loop 2: Self-Compiler + Code Learner

```python
class EnhancedSelfCompiler:
    """Self-Compiler that produces executable code."""

    def __init__(self, memory, coder, config):
        self.pattern_library = PatternLibrary(memory)
        self.code_learner = CodeLearner(memory)  # NEW

    async def learn_from_success(self, context, solution, domain):
        # 1. Extract pattern (existing)
        pattern_id = await self.pattern_library.extract_pattern(
            context, solution, domain, success=True
        )

        # 2. Check if pattern is stable enough to codify (NEW)
        pattern = await self.pattern_library.get(pattern_id)

        if pattern.usage_count >= 10 and pattern.success_rate >= 0.8:
            # 3. Generate executable code from pattern
            code = await self.code_learner.codify(pattern)

            if code:
                # 4. Save to learned_strategies/
                await self.code_learner.save(pattern.id, code)

                # 5. Register as capability
                await self.memory.register_code_capability(
                    pattern.id,
                    f"learned_strategies/{pattern.id}.py"
                )
```

### Loop 3: Goal Evolver + Intuition Network

```python
class EnhancedGoalEvolver:
    """Goal Evolver with learned intuition for fitness."""

    def __init__(self, memory, llm_client, config):
        self.memory = memory
        self.llm_client = llm_client
        self.intuition = IntuitionNetwork()  # NEW

    async def evaluate_fitness(self, goal):
        # 1. Objective metrics (existing)
        completion = await self._measure_completion(goal)
        capability_gain = await self._measure_capability_gain(goal)
        efficiency = await self._measure_efficiency(goal)

        objective_fitness = (
            0.4 * completion +
            0.4 * capability_gain +
            0.2 * efficiency
        )

        # 2. Intuition adjustment (NEW)
        intuition_score = await self.intuition.evaluate(goal.description)

        # 3. Blend objective and intuitive
        final_fitness = 0.7 * objective_fitness + 0.3 * intuition_score

        # 4. Record for intuition training
        await self.intuition.record_outcome(
            goal.description,
            action="pursue",
            success=(completion > 0.5)
        )

        return final_fitness
```

### Loop 4: Dreaming Machine + World Model

```python
class EnhancedDreamingMachine:
    """Dreaming Machine with causal world model."""

    def __init__(self, memory, llm_client, config):
        self.memory = memory
        self.llm_client = llm_client
        self.world_model = WorldModel()  # NEW

    async def generate_counterfactual(self, experience):
        # 1. Get world model prediction for original action
        original_prediction = await self.world_model.predict(
            action=experience.action,
            context=experience.context
        )

        # 2. Generate alternative actions
        alternatives = await self._generate_alternatives(experience)

        # 3. Use world model to predict counterfactual outcomes
        counterfactuals = []
        for alt_action in alternatives:
            predicted_outcome = await self.world_model.predict(
                action=alt_action,
                context=experience.context
            )

            counterfactuals.append({
                'action': alt_action,
                'predicted_outcome': predicted_outcome,
                'confidence': predicted_outcome.confidence
            })

        # 4. Update world model with actual outcome
        await self.world_model.update(
            action=experience.action,
            context=experience.context,
            actual_outcome=experience.outcome
        )

        return counterfactuals
```

### Loop 5: Integration Mind (Omega) - Extended

```python
class EnhancedBYRDOmega:
    """BYRD Omega with learning orchestration."""

    def __init__(self, memory, llm_client, components, config):
        # Existing components
        self.memory_reasoner = components['memory_reasoner']
        self.self_compiler = components['self_compiler']
        self.goal_evolver = components['goal_evolver']
        self.dreaming_machine = components['dreaming_machine']

        # Learning components (NEW)
        self.world_model = WorldModel()
        self.intuition = IntuitionNetwork()
        self.learned_retriever = LearnedRetriever()
        self.code_learner = CodeLearner()
        self.continuous_learner = ContinuousLearner() if config.get('lora_enabled') else None

        # Inject learning components into loops
        self.memory_reasoner.learned_retriever = self.learned_retriever
        self.goal_evolver.intuition = self.intuition
        self.dreaming_machine.world_model = self.world_model
        self.self_compiler.code_learner = self.code_learner

    async def run_dreaming_mode(self):
        """Extended DREAMING mode with training."""

        # 1. Standard dreaming (counterfactuals, insights)
        await self._run_standard_dreaming()

        # 2. Training activities (NEW)

        # Train learned retriever on recent feedback
        if self.learned_retriever.should_train():
            await self.learned_retriever.train_cycle()

        # Train intuition network on recent outcomes
        if self.intuition.should_train():
            await self.intuition.train_cycle()

        # Consolidate world model (prune weak causal rules)
        await self.world_model.consolidate()

        # LoRA fine-tuning if enabled
        if self.continuous_learner and self.continuous_learner.should_train():
            await self.continuous_learner.train_cycle()

        # Codify stable patterns
        stable_patterns = await self.self_compiler.get_stable_patterns()
        for pattern in stable_patterns:
            await self.code_learner.maybe_codify(pattern)
```

---

## Layer 4: Learning Substrate

### Component 1: World Model

```python
class WorldModel:
    """Explicit causal model updated by prediction errors."""

    def __init__(self):
        self.causal_rules = {}  # (action, context) -> outcome distribution

    async def predict(self, action, context):
        """Predict outcome before acting."""
        features = self._extract_features(context)
        key = (action, features)

        if key in self.causal_rules:
            return self.causal_rules[key]

        return Prediction(outcome="unknown", confidence=0.1)

    async def update(self, action, context, actual_outcome):
        """Update based on prediction error."""
        features = self._extract_features(context)
        key = (action, features)

        prediction = await self.predict(action, context)
        error = (prediction.outcome != actual_outcome)

        # Bayesian update of causal rule
        if key not in self.causal_rules:
            self.causal_rules[key] = {'outcomes': {}, 'total': 0}

        rule = self.causal_rules[key]
        rule['outcomes'][actual_outcome] = rule['outcomes'].get(actual_outcome, 0) + 1
        rule['total'] += 1

        if error:
            print(f"🎯 World model corrected: {action} -> {actual_outcome}")
```

### Component 2: Intuition Network

```python
class IntuitionNetwork:
    """Small trainable network for fast decision guidance."""

    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.decision_head = nn.Linear(384, len(POSSIBLE_ACTIONS))
        self.training_buffer = []

    async def get_intuition(self, situation):
        """Fast intuitive assessment."""
        emb = self.encoder.encode(situation)
        scores = self.decision_head(torch.tensor(emb))
        return torch.softmax(scores, dim=0)

    async def record_outcome(self, situation, action, success):
        """Learn from outcomes."""
        self.training_buffer.append({
            'situation': situation,
            'action': action,
            'reward': 1.0 if success else 0.0
        })

    async def train_cycle(self):
        """Train on collected examples."""
        # Simple gradient descent on reward prediction
        ...
```

### Component 3: Learned Retriever

```python
class LearnedRetriever:
    """Retriever that learns what's actually helpful."""

    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.retrieval_head = nn.Linear(384, 384)  # Trainable
        self.feedback_buffer = []

    async def score(self, query, candidates):
        """Score candidates with learned preference."""
        query_emb = self.retrieval_head(self.encoder.encode(query))

        scores = []
        for candidate in candidates:
            cand_emb = self.encoder.encode(candidate['content'])
            score = cosine_similarity(query_emb, cand_emb)
            scores.append({'candidate': candidate, 'score': score})

        return scores

    async def record_feedback(self, query, retrieved, outcome, helpful_items):
        """Learn which retrievals were actually helpful."""
        self.feedback_buffer.append({
            'query': query,
            'helpful': helpful_items,
            'not_helpful': [r for r in retrieved if r['id'] not in helpful_items]
        })

    async def train_cycle(self):
        """Contrastive learning on feedback."""
        # Pull helpful items closer, push unhelpful away
        ...
```

### Component 4: Code Learner

```python
class CodeLearner:
    """Convert stable patterns to executable code."""

    def __init__(self, memory, llm_client):
        self.memory = memory
        self.llm_client = llm_client
        self.code_registry = {}

    async def maybe_codify(self, pattern):
        """Codify if stable enough."""
        if pattern.usage_count < 10 or pattern.success_rate < 0.8:
            return

        if pattern.id in self.code_registry:
            return  # Already codified

        # Generate code from pattern
        prompt = f"""
        Convert this learned pattern into a Python function.

        Pattern: {pattern.description}
        Trigger: {pattern.trigger_conditions}
        Action: {pattern.action}
        Success rate: {pattern.success_rate}

        Write a function that:
        1. Takes relevant context as input
        2. Returns a decision or action
        3. Is deterministic and testable
        4. Includes a docstring with provenance
        """

        code = await self.llm_client.generate(prompt)

        if await self._validate_code(code):
            path = f"learned_strategies/{pattern.id}.py"
            await self._save_code(path, code)
            self.code_registry[pattern.id] = path

            print(f"📝 Codified pattern: {pattern.description[:50]}...")
```

---

## Data Flow

### Learning Flow During Normal Operation

```
User Query
    │
    ▼
┌─────────────────┐
│ Learned Retriever│ ◄── Trains on (query, helpful_items)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Memory Reasoner │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   World Model   │ ◄── Updates on (action, outcome)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Action      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Outcome      │ ──► Training signals to all learning components
└─────────────────┘
```

### Learning Flow During DREAMING Mode

```
DREAMING Mode Starts
         │
         ▼
┌─────────────────────────────────────────────────┐
│              LEARNING CONSOLIDATION              │
│                                                  │
│  1. World Model consolidation (prune weak rules) │
│  2. Intuition Network training                   │
│  3. Learned Retriever training                   │
│  4. Pattern → Code codification                  │
│  5. Abstraction hierarchy promotion              │
│  6. LoRA fine-tuning (if enabled)               │
│                                                  │
└─────────────────────────────────────────────────┘
         │
         ▼
DREAMING Mode Ends
```

---

## Metrics and Benchmarks

### Learning Health Metrics

| Component | Metric | Healthy Range |
|-----------|--------|---------------|
| World Model | Prediction accuracy | > 60% |
| Intuition Network | Decision agreement with outcome | > 70% |
| Learned Retriever | Helpful retrieval rate | > 50% |
| Code Learner | Codified patterns | Growing |
| Abstraction Hierarchy | Max level reached | L2+ |
| LoRA Adapter | Regression rate | < 5% |

### AGI Progress Benchmarks

| Benchmark | What It Measures | Target |
|-----------|------------------|--------|
| Abstraction Depth | Max level in hierarchy | L3 (axioms) |
| Transfer Rate | Cross-domain pattern application | > 40% |
| Composition Depth | Capability composition levels | 3+ |
| Compilation Rate | Patterns codified | > 30% |
| Novel Problem Solving | Problems outside seed goals | 3+ |

---

## Configuration

### Extended config.yaml

```yaml
option_b:
  enabled: true

  # Existing Option B config...

  # Learning extensions
  learning:
    enabled: true

    world_model:
      enabled: true
      consolidation_threshold: 0.3
      max_rules: 10000

    intuition_network:
      enabled: true
      training_batch_size: 50
      learning_rate: 0.001

    learned_retriever:
      enabled: true
      training_batch_size: 100
      learning_rate: 0.0001

    code_learner:
      enabled: true
      codification_threshold: 10  # usage count
      min_success_rate: 0.8

    abstraction_hierarchy:
      enabled: true
      promotion_threshold: 3
      max_level: 4

    lora:
      enabled: false  # Requires GPU
      adapter_rank: 8
      training_batch_size: 100
      regression_threshold: 0.05
```

---

## Implementation Roadmap

### Phase 1: No-Training Extensions (Week 1-2)

| Component | Effort | Files |
|-----------|--------|-------|
| World Model | 2-3 days | `world_model.py` (new) |
| Code Learner | 2-3 days | `code_learner.py` (new), extend `accelerators.py` |
| Abstraction Hierarchy | 2-3 days | extend `memory.py` |

### Phase 2: Lightweight Training (Week 3-4)

| Component | Effort | Requirements |
|-----------|--------|--------------|
| Learned Retriever | 3-4 days | sentence-transformers, PyTorch |
| Intuition Network | 2-3 days | PyTorch, ~100MB model |

### Phase 3: Full Training (Week 5-6)

| Component | Effort | Requirements |
|-----------|--------|--------------|
| LoRA Fine-Tuning | 1 week | GPU preferred, careful evaluation |
| Integration Testing | 3-4 days | Full system testing |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| World model learns wrong rules | Confidence thresholds, periodic validation |
| Intuition network overfits | Hold-out evaluation, regularization |
| Retriever degrades | A/B testing against baseline |
| Codified patterns have bugs | Automated testing before deployment |
| LoRA causes regression | Checkpoint + regression testing |
| Training interferes with operation | Training during DREAMING mode only |

---

## Success Criteria

### Minimum Viable Learning

The system is considered "learning-enabled" when:

1. World Model prediction accuracy > 50% (better than random)
2. At least one pattern codified and executing
3. Abstraction hierarchy reaches L2 (principles)
4. Retriever shows improvement over baseline

### Full Learning

The system demonstrates genuine learning when:

1. Novel problems solved (not in seed goals)
2. Abstraction hierarchy reaches L3 (axioms)
3. Cross-domain transfer observed
4. Capability score increasing over time

---

## Relationship to Existing Plans

```
OPTION_B_FIX_PLAN          ✅ COMPLETE
├── Working search
├── Goal seeding
└── Basic routing

CAPABILITY_GROWTH_PLAN     ✅ COMPLETE
├── Instrumentation
├── Benchmarks
└── Goal Evolver verification

ARCHITECTURE_FIRST_AGI     📋 REFERENCE
├── Hierarchical abstraction
├── Analogical transfer
├── Capability composition
└── (Theoretical framework)

ARCHITECTURE_V3_LEARNING   ← THIS DOCUMENT
├── Extends Option B with learning
├── Concrete integration points
├── Implementation roadmap
└── (Practical architecture)
```

---

## Conclusion

This architecture extends BYRD from a knowledge accumulation system to a genuine learning system by adding:

1. **World Model** - Learns causality from experience
2. **Intuition Network** - Learns quality/taste from outcomes
3. **Learned Retriever** - Learns relevance from feedback
4. **Code Learner** - Externalizes knowledge as executable code
5. **Hierarchical Memory** - Compresses experience into abstractions
6. **LoRA Adapters** - Updates LLM reasoning (optional)

These components wrap around the frozen LLM, creating learning where the LLM itself cannot learn. The key insight: **intelligence can grow through structure even when the substrate is fixed**.

---

*Document version: 3.0*
*Created: December 28, 2024*
*Status: Target architecture for learning-enabled BYRD*
