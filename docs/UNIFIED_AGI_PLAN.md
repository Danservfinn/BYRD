# BYRD Unified AGI Plan

## Executive Summary

This document unifies two complementary plans into a single coherent AGI architecture:

- **AGI_SEED_V2**: Provided the *execution engine* - the closed loop that actually drives improvement
- **ARCHITECTURE_V3_LEARNING**: Provided the *learning mechanisms* - components that enable genuine capability growth

**The Insight**: Neither plan alone achieves AGI. V2's engine has nothing to improve with. V3's learning has no driver. Together, they form a complete system.

**The Goal**: An elegant, minimal architecture where recursive self-improvement emerges from the interaction of execution and learning.

---

## The Problem

BYRD currently has sophisticated components that exist as islands:

```
Current State:
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Dreamer │  │  Seeker  │  │  Memory  │  │  Option B│
└──────────┘  └──────────┘  └──────────┘  └──────────┘
     ?              ?              ?              ?

No execution engine connects them into improvement cycles.
The LLM doesn't learn, so capability is bounded.
```

**Two Missing Pieces**:
1. An execution engine that drives improvement cycles (from V2)
2. Learning mechanisms that work despite frozen LLM weights (from V3)

---

## Unified Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           UNIFIED AGI SYSTEM                                 │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         AGI RUNNER                                      │ │
│  │                    (The Execution Engine)                               │ │
│  │                                                                         │ │
│  │    ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   │ │
│  │    │ASSESS│──▶│IDENT-│──▶│GENER-│──▶│PRED- │──▶│VERIFY│──▶│EXEC- │   │ │
│  │    │      │   │IFY   │   │ATE   │   │ICT   │   │      │   │UTE   │   │ │
│  │    └──────┘   └──────┘   └──────┘   └──────┘   └──────┘   └──────┘   │ │
│  │         ▲                                                     │        │ │
│  │         │      ┌──────┐                        ┌──────┐      │        │ │
│  │         └──────│LEARN │◀───────────────────────│MEAS- │◀─────┘        │ │
│  │                │      │                        │URE   │               │ │
│  │                └──────┘                        └──────┘               │ │
│  └─────────────────────────────────┬──────────────────────────────────────┘ │
│                                    │                                         │
│  ┌─────────────────────────────────▼──────────────────────────────────────┐ │
│  │                       LEARNING SUBSTRATE                                │ │
│  │                                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │   WORLD     │  │  INTUITION  │  │   LEARNED   │  │    CODE     │   │ │
│  │  │   MODEL     │  │   NETWORK   │  │  RETRIEVER  │  │   LEARNER   │   │ │
│  │  │             │  │             │  │             │  │             │   │ │
│  │  │ Causality   │  │   Taste/    │  │  Relevance  │  │  Pattern→   │   │ │
│  │  │ Prediction  │  │ Preference  │  │   Scoring   │  │    Code     │   │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │ │
│  │         └─────────────────┴─────────────────┴─────────────────┘        │ │
│  └─────────────────────────────────┬──────────────────────────────────────┘ │
│                                    │                                         │
│  ┌─────────────────────────────────▼──────────────────────────────────────┐ │
│  │                         OPTION B LOOPS                                  │ │
│  │                                                                         │ │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐           │ │
│  │  │  MEMORY   │  │   SELF-   │  │   GOAL    │  │ DREAMING  │           │ │
│  │  │ REASONER  │  │ COMPILER  │  │  EVOLVER  │  │  MACHINE  │           │ │
│  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘           │ │
│  │        └──────────────┴──────────────┴──────────────┘                  │ │
│  │                              │                                          │ │
│  │                     ┌────────▼────────┐                                │ │
│  │                     │   BYRD OMEGA    │                                │ │
│  │                     └─────────────────┘                                │ │
│  └─────────────────────────────────┬──────────────────────────────────────┘ │
│                                    │                                         │
│  ┌─────────────────────────────────▼──────────────────────────────────────┐ │
│  │                       ENHANCED MEMORY                                   │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │              HIERARCHICAL ABSTRACTION (L0-L4)                    │   │ │
│  │  │                                                                   │   │ │
│  │  │  L0: Experience ─▶ L1: Pattern ─▶ L2: Principle ─▶ L3: Axiom    │   │ │
│  │  │                                                         │        │   │ │
│  │  │                                                   L4: Meta-Axiom │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │    GRAPH    │  │  BAYESIAN   │  │  EMERGENT   │  │  CODE-AS-   │   │ │
│  │  │ ALGORITHMS  │  │  TRACKING   │  │ CATEGORIES  │  │   MEMORY    │   │ │
│  │  │   (GDS)     │  │             │  │             │  │             │   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │ │
│  └─────────────────────────────────┬──────────────────────────────────────┘ │
│                                    │                                         │
│  ┌─────────────────────────────────▼──────────────────────────────────────┐ │
│  │                      VERIFICATION LAYER                                 │ │
│  │                                                                         │ │
│  │  ┌─────────────────────┐        ┌─────────────────────┐                │ │
│  │  │ CAPABILITY EVALUATOR│        │ INFORMATION THEORY  │                │ │
│  │  │                     │        │                     │                │ │
│  │  │  • Held-out tests   │        │  • Shannon entropy  │                │ │
│  │  │  • Ground truth     │        │  • Bayesian updates │                │ │
│  │  │  • Before/after     │        │  • Wilson intervals │                │ │
│  │  └─────────────────────┘        └─────────────────────┘                │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. AGI Runner (The Engine)

The AGI Runner is the core execution engine that drives recursive self-improvement. Without it, all other components are islands.

```python
class AGIRunner:
    """
    The execution engine that drives recursive self-improvement.

    This connects: assessment → hypothesis → prediction → verification →
    execution → measurement → learning in a closed loop.
    """

    def __init__(self, byrd):
        self.byrd = byrd

        # Core dependencies
        self.world_model = byrd.world_model
        self.intuition = byrd.intuition
        self.evaluator = byrd.evaluator
        self.bayesian_tracker = byrd.bayesian_tracker

        # Cycle tracking
        self._cycle_count = 0
        self._improvement_rate = 0.0

    async def run_improvement_cycle(self) -> CycleResult:
        """Execute one complete improvement cycle."""
        self._cycle_count += 1

        # 1. ASSESS: Get current capability state
        inventory = await self._assess_capabilities()

        # 2. IDENTIFY: Select improvement target
        target = await self._identify_target(inventory)
        if not target:
            return CycleResult(success=False, reason="No target identified")

        # 3. GENERATE: Create improvement hypotheses
        hypotheses = await self._generate_hypotheses(target, inventory)

        # 4. PREDICT: Use world model to rank hypotheses
        ranked = await self._predict_outcomes(hypotheses)

        # 5. VERIFY: Safety check
        best = ranked[0]
        if not await self._verify_safety(best):
            return CycleResult(success=False, reason="Safety check failed")

        # 6. EXECUTE: Apply improvement
        await self._execute(best)

        # 7. MEASURE: Evaluate outcome with held-out tests
        measurement = await self._measure_improvement(target, inventory)

        # 8. LEARN: Update all learning components
        await self._learn_from_outcome(best, measurement)

        return CycleResult(
            success=measurement.improved,
            target=target.name,
            delta=measurement.delta,
            cycle=self._cycle_count
        )

    async def _identify_target(self, inventory) -> Optional[ImprovementTarget]:
        """
        Select highest-value improvement target.

        Priority:
        1. Declining capabilities (urgent)
        2. Capabilities with high uncertainty (epistemic value)
        3. Weakest capabilities (highest potential)
        4. Meta-capabilities (highest leverage)
        """
        # Use Bayesian tracker for uncertainty-aware targeting
        for cap_name, cap in inventory.capabilities.items():
            mean, lower, upper = self.bayesian_tracker.get_estimate(cap_name)
            uncertainty = upper - lower

            # High uncertainty = high information value
            if uncertainty > 0.4:
                return ImprovementTarget(
                    name=cap_name,
                    current_level=mean,
                    priority="high",
                    reason=f"High uncertainty ({uncertainty:.2f})"
                )

        # Fall back to weakest capability
        if inventory.weakest:
            return ImprovementTarget(
                name=inventory.weakest[0],
                current_level=inventory.capabilities[inventory.weakest[0]].success_rate,
                priority="medium",
                reason="Weakest capability"
            )

        return None

    async def _generate_hypotheses(self, target, inventory) -> List[ImprovementHypothesis]:
        """
        Generate concrete improvement hypotheses.

        Strategies:
        1. Fix known limitations
        2. Apply successful patterns (from Self-Compiler)
        3. Compose with stronger capabilities
        4. Use intuition network for novel approaches
        """
        hypotheses = []

        # Strategy 1: Pattern application
        patterns = await self.byrd.self_compiler.get_patterns_for(target.name)
        for pattern in patterns[:3]:
            hypotheses.append(ImprovementHypothesis(
                description=f"Apply pattern: {pattern.name}",
                target=target.name,
                strategy="pattern_application",
                code_change=await self._generate_pattern_code(pattern),
                expected_improvement=pattern.avg_improvement
            ))

        # Strategy 2: Intuition-guided
        intuition_score = await self.intuition.evaluate(target.name)
        if intuition_score.suggested_action:
            hypotheses.append(ImprovementHypothesis(
                description=f"Intuition: {intuition_score.suggested_action}",
                target=target.name,
                strategy="intuition_guided",
                code_change=await self._generate_intuition_code(intuition_score),
                expected_improvement=0.1
            ))

        # Strategy 3: Composition
        composable = await self._find_composable(target.name, inventory)
        for comp in composable[:2]:
            hypotheses.append(ImprovementHypothesis(
                description=f"Compose with {comp.name}",
                target=target.name,
                strategy="composition",
                code_change=await self._generate_composition_code(target, comp),
                expected_improvement=0.05
            ))

        return hypotheses

    async def _predict_outcomes(self, hypotheses) -> List[ImprovementHypothesis]:
        """Use world model to predict and rank hypotheses."""
        for hyp in hypotheses:
            prediction = await self.world_model.predict(
                action=hyp.description,
                context={"target": hyp.target, "strategy": hyp.strategy}
            )
            hyp.predicted_success = prediction.success_probability
            hyp.prediction_confidence = prediction.confidence

        # Rank by expected value
        return sorted(
            hypotheses,
            key=lambda h: h.predicted_success * h.expected_improvement,
            reverse=True
        )

    async def _measure_improvement(self, target, before_inventory) -> MeasurementResult:
        """
        Measure improvement using held-out evaluation.

        This is critical - without measurement, learning is impossible.
        """
        # Use CapabilityEvaluator for ground truth
        before_score = await self.evaluator.evaluate_capability(target.name)

        # Re-assess after change
        after_inventory = await self._assess_capabilities()
        after_score = await self.evaluator.evaluate_capability(target.name)

        delta = after_score.accuracy - before_score.accuracy

        # Bayesian update
        self.bayesian_tracker.update(target.name, success=(delta > 0))

        # Rollback on regression
        if delta < -0.05:
            await self.byrd.rollback.rollback_last(RollbackReason.CAPABILITY_REGRESSION)
            return MeasurementResult(improved=False, delta=delta, reason="Rolled back")

        return MeasurementResult(improved=(delta > 0.01), delta=delta)

    async def _learn_from_outcome(self, hypothesis, measurement):
        """Update all learning components from outcome."""

        # 1. World model: prediction error
        await self.world_model.update(
            action=hypothesis.description,
            context={"strategy": hypothesis.strategy},
            actual_outcome="improved" if measurement.improved else "not_improved",
            predicted_success=hypothesis.predicted_success
        )

        # 2. Intuition network: outcome feedback
        await self.intuition.record_outcome(
            situation=hypothesis.target,
            action=hypothesis.strategy,
            success=measurement.improved
        )

        # 3. Record as experience for memory system
        await self.byrd.memory.record_experience(
            content=f"[AGI_CYCLE] {'SUCCESS' if measurement.improved else 'FAILURE'}: "
                    f"{hypothesis.description} (delta: {measurement.delta:+.2%})",
            type="agi_cycle",
            metadata={
                "cycle": self._cycle_count,
                "target": hypothesis.target,
                "strategy": hypothesis.strategy,
                "improved": measurement.improved,
                "delta": measurement.delta
            }
        )
```

### 2. Learning Substrate

#### 2.1 World Model

```python
class WorldModel:
    """
    Learns causality from prediction errors.

    Core insight: If we can predict what actions lead to what outcomes,
    we can plan improvements without trial-and-error.
    """

    def __init__(self):
        self.causal_rules: Dict[Tuple[str, str], OutcomeDistribution] = {}
        self.prediction_errors: List[PredictionError] = []

    async def predict(self, action: str, context: Dict) -> Prediction:
        """Predict outcome before acting."""
        key = self._make_key(action, context)

        if key in self.causal_rules:
            distribution = self.causal_rules[key]
            most_likely = max(distribution.outcomes, key=distribution.outcomes.get)
            confidence = distribution.outcomes[most_likely] / distribution.total
            return Prediction(
                outcome=most_likely,
                success_probability=confidence,
                confidence=min(1.0, distribution.total / 10)  # Confidence grows with observations
            )

        return Prediction(outcome="unknown", success_probability=0.5, confidence=0.1)

    async def update(self, action: str, context: Dict, actual_outcome: str, predicted_success: float):
        """Learn from prediction error."""
        key = self._make_key(action, context)

        if key not in self.causal_rules:
            self.causal_rules[key] = OutcomeDistribution()

        distribution = self.causal_rules[key]
        distribution.outcomes[actual_outcome] = distribution.outcomes.get(actual_outcome, 0) + 1
        distribution.total += 1

        # Track prediction error for meta-learning
        prediction = await self.predict(action, context)
        error = abs(predicted_success - (1.0 if actual_outcome == "improved" else 0.0))

        if error > 0.3:
            self.prediction_errors.append(PredictionError(
                action=action,
                context=context,
                predicted=predicted_success,
                actual=actual_outcome,
                error=error
            ))
            print(f"🎯 World model corrected: {action} -> {actual_outcome}")

    async def consolidate(self):
        """Prune weak rules, strengthen confident ones."""
        weak_keys = [
            key for key, dist in self.causal_rules.items()
            if dist.total < 3 or dist.get_entropy() > 0.9
        ]
        for key in weak_keys:
            del self.causal_rules[key]
```

#### 2.2 Intuition Network

```python
class IntuitionNetwork:
    """
    Small trainable network for fast decision guidance.

    This is the "taste" component - learns what goals are worth pursuing,
    what actions feel right, without explicit reasoning.

    Size: ~80MB (sentence-transformers + small head)
    """

    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.value_head = nn.Sequential(
            nn.Linear(384, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
        self.training_buffer: List[IntuitionExample] = []
        self.optimizer = torch.optim.Adam(self.value_head.parameters(), lr=0.001)

    async def evaluate(self, situation: str) -> IntuitionScore:
        """Fast intuitive assessment of a situation/goal."""
        with torch.no_grad():
            emb = torch.tensor(self.encoder.encode(situation))
            value = self.value_head(emb).item()

        return IntuitionScore(
            value=value,
            suggested_action="pursue" if value > 0.6 else "reconsider" if value < 0.4 else "neutral"
        )

    async def record_outcome(self, situation: str, action: str, success: bool):
        """Learn from outcomes."""
        self.training_buffer.append(IntuitionExample(
            situation=situation,
            action=action,
            reward=1.0 if success else 0.0
        ))

    def should_train(self) -> bool:
        return len(self.training_buffer) >= 50

    async def train_cycle(self):
        """Train on collected examples during DREAMING mode."""
        if len(self.training_buffer) < 50:
            return

        # Simple supervised learning on value prediction
        for example in self.training_buffer[-100:]:
            emb = torch.tensor(self.encoder.encode(example.situation))
            predicted = self.value_head(emb)
            target = torch.tensor([example.reward])

            loss = nn.MSELoss()(predicted, target)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        self.training_buffer = self.training_buffer[-50:]  # Keep recent
        print("🧠 Intuition network trained")
```

#### 2.3 Learned Retriever

```python
class LearnedRetriever:
    """
    Learns what memories are actually relevant for a query.

    Standard embedding similarity often retrieves irrelevant context.
    This learns from feedback: which retrievals actually helped?
    """

    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        # Trainable projection layer
        self.query_projection = nn.Linear(384, 384)
        self.feedback_buffer: List[RetrievalFeedback] = []
        self.optimizer = torch.optim.Adam(self.query_projection.parameters(), lr=0.0001)

    async def score(self, query: str, candidates: List[Dict]) -> List[ScoredCandidate]:
        """Score candidates with learned relevance."""
        with torch.no_grad():
            # Project query through learned layer
            query_emb = torch.tensor(self.encoder.encode(query))
            projected_query = self.query_projection(query_emb)

            scores = []
            for candidate in candidates:
                cand_emb = torch.tensor(self.encoder.encode(candidate['content']))
                score = torch.cosine_similarity(projected_query, cand_emb, dim=0).item()
                scores.append(ScoredCandidate(candidate=candidate, score=score))

        return sorted(scores, key=lambda x: x.score, reverse=True)

    async def record_feedback(self, query: str, retrieved: List[Dict], helpful_ids: Set[str]):
        """Learn which retrievals were actually helpful."""
        for item in retrieved:
            self.feedback_buffer.append(RetrievalFeedback(
                query=query,
                content=item['content'],
                was_helpful=item['id'] in helpful_ids
            ))

    def should_train(self) -> bool:
        return len(self.feedback_buffer) >= 100

    async def train_cycle(self):
        """Contrastive learning: pull helpful items closer, push unhelpful away."""
        if not self.should_train():
            return

        helpful = [f for f in self.feedback_buffer if f.was_helpful]
        unhelpful = [f for f in self.feedback_buffer if not f.was_helpful]

        if not helpful or not unhelpful:
            return

        # Contrastive loss
        for h in helpful[-50:]:
            query_emb = torch.tensor(self.encoder.encode(h.query))
            projected = self.query_projection(query_emb)

            positive_emb = torch.tensor(self.encoder.encode(h.content))
            negative = random.choice(unhelpful)
            negative_emb = torch.tensor(self.encoder.encode(negative.content))

            pos_sim = torch.cosine_similarity(projected, positive_emb, dim=0)
            neg_sim = torch.cosine_similarity(projected, negative_emb, dim=0)

            # Margin loss: positive should be closer by margin
            loss = torch.relu(0.2 - pos_sim + neg_sim)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        self.feedback_buffer = self.feedback_buffer[-100:]
        print("🔍 Learned retriever trained")
```

#### 2.4 Code Learner

```python
class CodeLearner:
    """
    Converts stable patterns into executable code.

    Key insight: Knowledge externalized as code is:
    - Deterministic (no LLM variance)
    - Fast (no inference cost)
    - Inspectable (can be reviewed/debugged)
    - Persistent (survives context limits)
    """

    def __init__(self, memory, llm_client):
        self.memory = memory
        self.llm_client = llm_client
        self.code_registry: Dict[str, str] = {}  # pattern_id -> file_path

    async def maybe_codify(self, pattern: Pattern):
        """Codify pattern if stable enough."""
        # Thresholds for codification
        if pattern.usage_count < 10:
            return  # Not enough evidence
        if pattern.success_rate < 0.8:
            return  # Not reliable enough
        if pattern.id in self.code_registry:
            return  # Already codified

        code = await self._generate_code(pattern)

        if code and await self._validate_code(code):
            path = f"learned_strategies/{pattern.domain}/{pattern.id}.py"
            await self._save_code(path, code)
            self.code_registry[pattern.id] = path

            # Register as capability
            await self.memory.record_experience(
                content=f"[CODE_LEARNER] Codified pattern: {pattern.description}",
                type="codification",
                metadata={"pattern_id": pattern.id, "path": path}
            )

            print(f"📝 Codified: {pattern.description[:50]}...")

    async def _generate_code(self, pattern: Pattern) -> Optional[str]:
        """Use LLM to convert pattern to code."""
        prompt = f"""Convert this learned pattern into a Python function.

Pattern: {pattern.description}
Trigger conditions: {pattern.trigger_conditions}
Action: {pattern.action}
Success rate: {pattern.success_rate:.0%}
Usage count: {pattern.usage_count}

Write a function that:
1. Takes relevant context as input (Dict)
2. Returns a decision or action (str or Dict)
3. Is deterministic and testable
4. Includes a docstring documenting its provenance

Example format:
```python
def {pattern.id}(context: Dict) -> str:
    \"\"\"
    {pattern.description}

    Provenance: Learned from {pattern.usage_count} experiences.
    Success rate: {pattern.success_rate:.0%}
    Codified: {{date}}
    \"\"\"
    # Implementation
    return "action"
```

Output only the Python code, no explanation."""

        response = await self.llm_client.generate(prompt=prompt, max_tokens=500, temperature=0.1)
        return self._extract_code(response.text)

    async def _validate_code(self, code: str) -> bool:
        """Validate generated code is safe and syntactically correct."""
        # Syntax check
        try:
            ast.parse(code)
        except SyntaxError:
            return False

        # Safety check - no dangerous patterns
        dangerous = ['os.system', 'subprocess', 'eval', 'exec', '__import__', 'open(']
        for pattern in dangerous:
            if pattern in code:
                return False

        return True

    async def execute_learned(self, pattern_id: str, context: Dict) -> Optional[str]:
        """Execute a codified pattern."""
        if pattern_id not in self.code_registry:
            return None

        path = self.code_registry[pattern_id]
        # Dynamic import and execution
        spec = importlib.util.spec_from_file_location(pattern_id, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        func = getattr(module, pattern_id)
        return func(context)
```

### 3. Enhanced Memory

#### 3.1 Hierarchical Abstraction

```python
class HierarchicalMemory:
    """
    Memory with abstraction hierarchy.

    L0: Experience  - Raw observations
    L1: Pattern     - Recurring themes (3+ similar experiences)
    L2: Principle   - Generalizations (3+ related patterns)
    L3: Axiom       - Fundamental truths (3+ connected principles)
    L4: Meta-Axiom  - Truths about truths (2+ meta-observations)

    Higher levels are preferred for familiar situations.
    Lower levels are used for novel situations.
    """

    PROMOTION_THRESHOLDS = {
        0: 3,   # 3 similar experiences -> pattern
        1: 3,   # 3 related patterns -> principle
        2: 3,   # 3 connected principles -> axiom
        3: 2,   # 2 meta-observations -> meta-axiom
    }

    async def maybe_promote(self, node_id: str, current_level: int) -> Optional[str]:
        """Check if node should be promoted to higher abstraction level."""
        if current_level >= 4:
            return None  # Already at max

        threshold = self.PROMOTION_THRESHOLDS[current_level]

        # Find similar nodes at same level
        similar = await self._find_similar_nodes(node_id, current_level)

        if len(similar) >= threshold:
            # Promote: create higher-level node that generalizes
            promoted = await self._create_promoted_node(node_id, similar, current_level + 1)

            # Link lower nodes to promoted node
            for similar_id in similar:
                await self._create_relationship(similar_id, promoted, "PROMOTED_TO")

            return promoted

        return None

    async def retrieve_for_query(self, query: str, prefer_level: int = None) -> List[Dict]:
        """
        Retrieve relevant nodes, preferring higher abstraction for familiar queries.
        """
        # Check if query matches known patterns (familiar)
        familiarity = await self._assess_familiarity(query)

        if prefer_level is None:
            # Familiar queries -> prefer higher abstraction
            # Novel queries -> prefer lower abstraction (raw experiences)
            prefer_level = 2 if familiarity > 0.7 else 0

        results = await self._query_nodes(query, min_level=prefer_level)

        if not results and prefer_level > 0:
            # Fall back to lower levels if nothing found
            results = await self._query_nodes(query, min_level=0)

        return results
```

#### 3.2 Real Graph Algorithms (Neo4j GDS)

```python
class GraphAlgorithms:
    """
    Real graph algorithms using Neo4j Graph Data Science.

    Replaces fake "PageRank" (degree * weight) with actual algorithms.
    """

    async def ensure_projection(self):
        """Create graph projection for GDS algorithms."""
        await self.memory._execute_query("""
            CALL gds.graph.drop('byrd-mind', false)
        """)

        await self.memory._execute_query("""
            CALL gds.graph.project(
                'byrd-mind',
                ['Experience', 'Pattern', 'Principle', 'Axiom', 'Belief', 'Desire'],
                {
                    DERIVED_FROM: {orientation: 'UNDIRECTED'},
                    SUPPORTS: {orientation: 'UNDIRECTED'},
                    CONFLICTS_WITH: {orientation: 'UNDIRECTED'},
                    PROMOTED_TO: {orientation: 'NATURAL'},
                    LED_TO: {orientation: 'NATURAL'}
                },
                {nodeProperties: ['confidence', 'abstraction_level']}
            )
        """)

    async def pagerank(self, limit: int = 20) -> List[Dict]:
        """Find most important nodes by graph centrality."""
        await self.ensure_projection()

        result = await self.memory._execute_query("""
            CALL gds.pageRank.stream('byrd-mind', {
                maxIterations: 20,
                dampingFactor: 0.85
            })
            YIELD nodeId, score
            WITH gds.util.asNode(nodeId) AS node, score
            RETURN
                elementId(node) as id,
                labels(node)[0] as type,
                node.content as content,
                node.abstraction_level as level,
                score as importance
            ORDER BY score DESC
            LIMIT $limit
        """, {"limit": limit})

        return [dict(r) for r in result]

    async def community_detection(self) -> Dict[str, List[str]]:
        """Find communities of related concepts using Louvain."""
        await self.ensure_projection()

        result = await self.memory._execute_query("""
            CALL gds.louvain.stream('byrd-mind')
            YIELD nodeId, communityId
            WITH gds.util.asNode(nodeId) AS node, communityId
            RETURN
                communityId,
                collect(node.content)[..10] as members,
                count(*) as size
            ORDER BY size DESC
            LIMIT 10
        """)

        return {f"community_{r['communityId']}": r['members'] for r in result}

    async def betweenness_centrality(self, limit: int = 10) -> List[Dict]:
        """Find bridge nodes between communities."""
        await self.ensure_projection()

        result = await self.memory._execute_query("""
            CALL gds.betweennessCentrality.stream('byrd-mind')
            YIELD nodeId, score
            WITH gds.util.asNode(nodeId) AS node, score
            WHERE score > 0
            RETURN
                elementId(node) as id,
                node.content as content,
                labels(node)[0] as type,
                score as centrality
            ORDER BY score DESC
            LIMIT $limit
        """, {"limit": limit})

        return [dict(r) for r in result]
```

#### 3.3 Bayesian Capability Tracker

```python
class BayesianCapabilityTracker:
    """
    Track capabilities using proper Bayesian inference.

    Replaces simple success/total with Beta distribution.
    Provides uncertainty quantification and principled updates.
    """

    def __init__(self):
        # Prior: Beta(1, 1) = uniform (maximum uncertainty)
        self.alpha: Dict[str, float] = {}  # successes + 1
        self.beta: Dict[str, float] = {}   # failures + 1

    def update(self, capability: str, success: bool):
        """Bayesian update after observation."""
        if capability not in self.alpha:
            self.alpha[capability] = 1.0
            self.beta[capability] = 1.0

        if success:
            self.alpha[capability] += 1
        else:
            self.beta[capability] += 1

    def get_estimate(self, capability: str) -> Tuple[float, float, float]:
        """
        Get capability estimate with 95% credible interval.

        Returns: (mean, lower_95, upper_95)
        """
        if capability not in self.alpha:
            return (0.5, 0.0, 1.0)  # Maximum uncertainty

        a, b = self.alpha[capability], self.beta[capability]

        # Mean of Beta distribution
        mean = a / (a + b)

        # 95% credible interval
        lower = scipy.stats.beta.ppf(0.025, a, b)
        upper = scipy.stats.beta.ppf(0.975, a, b)

        return (mean, lower, upper)

    def get_uncertainty(self, capability: str) -> float:
        """Get uncertainty (normalized entropy) of belief."""
        if capability not in self.alpha:
            return 1.0

        a, b = self.alpha[capability], self.beta[capability]

        # Entropy of Beta distribution (normalized)
        entropy = (
            scipy.special.betaln(a, b)
            - (a - 1) * scipy.special.psi(a)
            - (b - 1) * scipy.special.psi(b)
            + (a + b - 2) * scipy.special.psi(a + b)
        )

        max_entropy = scipy.special.betaln(1, 1)
        return entropy / max_entropy if max_entropy > 0 else 1.0

    def should_explore(self, capability: str, threshold: float = 0.4) -> bool:
        """Recommend exploration if uncertainty is high."""
        return self.get_uncertainty(capability) > threshold
```

#### 3.4 Emergent Category Discovery

```python
class EmergentCategoryDiscovery:
    """
    Discover capability categories from behavior, not prescription.

    Aligns with emergence principle: BYRD defines its own vocabulary.
    """

    async def discover_categories(self, min_cluster_size: int = 5) -> Dict[str, DiscoveredCategory]:
        """Discover categories by clustering behavioral patterns."""

        # Get recent capability attempts
        attempts = await self.memory._execute_query("""
            MATCH (e:Experience)
            WHERE e.type IN ['capability_attempt', 'action_outcome', 'agi_cycle']
            RETURN e.content as content, e.capability as capability,
                   e.success as success, e.metadata as metadata
            ORDER BY e.timestamp DESC
            LIMIT 500
        """)

        if len(attempts) < min_cluster_size:
            return {}

        # Cluster by semantic similarity
        clusters = await self._cluster_by_embedding(attempts)

        # Name clusters (only LLM call - for naming, not structure)
        categories = {}
        for cluster_id, members in clusters.items():
            if len(members) >= min_cluster_size:
                name, description = await self._name_cluster(members)

                successes = sum(1 for m in members if m.get("success", False))
                success_rate = successes / len(members)

                categories[name] = DiscoveredCategory(
                    name=name,
                    description=description,
                    pattern_count=len(members),
                    success_rate=success_rate,
                    examples=[m["content"][:100] for m in members[:5]],
                    discovered_at=datetime.now()
                )

        return categories

    async def _cluster_by_embedding(self, attempts: List[Dict]) -> Dict[str, List[Dict]]:
        """Cluster using sentence embeddings + k-means."""
        encoder = SentenceTransformer('all-MiniLM-L6-v2')

        embeddings = encoder.encode([a["content"] for a in attempts])

        # Determine optimal k using silhouette score
        best_k, best_score = 3, -1
        for k in range(3, min(10, len(attempts) // 5)):
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(embeddings)
            score = silhouette_score(embeddings, labels)
            if score > best_score:
                best_k, best_score = k, score

        # Final clustering
        kmeans = KMeans(n_clusters=best_k, random_state=42)
        labels = kmeans.fit_predict(embeddings)

        clusters = defaultdict(list)
        for i, label in enumerate(labels):
            clusters[str(label)].append(attempts[i])

        return dict(clusters)
```

### 4. Verification Layer

```python
class CapabilityEvaluator:
    """
    Held-out test suites for ground-truth capability measurement.

    Critical for training signal - without ground truth, learning is impossible.
    """

    # Test suites per capability
    TEST_SUITES = {
        "reasoning": [
            {
                "input": "If A implies B and B implies C, does A imply C?",
                "expected_contains": "yes"
            },
            {
                "input": "What is wrong with: All cats are animals. Fluffy is an animal. Therefore Fluffy is a cat.",
                "expected_contains": "invalid"
            },
        ],
        "code_generation": [
            {
                "input": "Write a function to check if a number is prime",
                "validator": "contains_def_and_returns_bool"
            },
        ],
        "research": [
            {
                "input": "What is the capital of France?",
                "expected_contains": "Paris"
            },
        ],
        "introspection": [
            {
                "input": "Describe your current capabilities",
                "validator": "returns_structured_list"
            },
        ],
    }

    async def evaluate_capability(self, capability: str) -> EvaluationResult:
        """Run test suite for capability."""
        if capability not in self.TEST_SUITES:
            return EvaluationResult(
                capability=capability,
                accuracy=0.5,
                confidence=0.0,
                tests_run=0
            )

        tests = self.TEST_SUITES[capability]
        passed = 0

        for test in tests:
            result = await self._run_test(capability, test)
            if result.passed:
                passed += 1

        return EvaluationResult(
            capability=capability,
            accuracy=passed / len(tests) if tests else 0,
            confidence=min(1.0, len(tests) / 10),
            tests_run=len(tests)
        )


class InformationTheory:
    """Information-theoretic utilities for principled learning."""

    @staticmethod
    def entropy(probabilities: List[float]) -> float:
        """Shannon entropy: H(X) = -Σ p(x) log₂ p(x)"""
        return -sum(p * math.log2(p) for p in probabilities if p > 0)

    @staticmethod
    def information_gain(before_entropy: float, after_entropy: float) -> float:
        """Information gained from observation: IG = H(before) - H(after)"""
        return before_entropy - after_entropy

    @staticmethod
    def kl_divergence(p: List[float], q: List[float]) -> float:
        """KL divergence: how different is q from p?"""
        return sum(pi * math.log2(pi / qi) for pi, qi in zip(p, q) if pi > 0 and qi > 0)
```

---

## Integration

### How Components Connect

```
User Query / Desire
        │
        ▼
┌───────────────────────┐
│    Learned Retriever  │ ◄── Trains on (query, helpful_items)
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│    Memory Reasoner    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      World Model      │ ◄── Updates on (action, outcome)
│    (predict outcome)  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Intuition Network   │ ◄── Trains on (situation, success)
│   (fast guidance)     │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│       Execute         │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Capability Evaluator  │ ──► Ground truth for training
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│    Self-Compiler      │
│  (extract patterns)   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│     Code Learner      │ ──► learned_strategies/*.py
│   (stable → code)     │
└───────────────────────┘
```

### Training Schedule

| Mode | Activity | Frequency |
|------|----------|-----------|
| AWAKE | Collect training examples | Continuous |
| AWAKE | World model predictions | Per action |
| DREAMING | Intuition network training | Every 50 examples |
| DREAMING | Learned retriever training | Every 100 examples |
| DREAMING | World model consolidation | Per cycle |
| DREAMING | Pattern codification | Per stable pattern |
| EVOLVING | Goal fitness with intuition | Per generation |
| COMPILING | Execute codified patterns | As matched |

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

| Component | Effort | Dependencies |
|-----------|--------|--------------|
| AGIRunner skeleton | 2 days | None |
| WorldModel | 2 days | None |
| BayesianCapabilityTracker | 1 day | scipy |
| CapabilityEvaluator | 2 days | None |
| Integration tests | 2 days | Above |

**Milestone**: AGI cycle runs end-to-end (even if learning is minimal)

### Phase 2: Graph & Memory (Week 3)

| Component | Effort | Dependencies |
|-----------|--------|--------------|
| Neo4j GDS setup | 1 day | Docker config |
| GraphAlgorithms class | 2 days | GDS |
| HierarchicalMemory | 2 days | None |
| EmergentCategoryDiscovery | 1 day | sentence-transformers |

**Milestone**: Real PageRank, communities, abstraction levels

### Phase 3: Learning Components (Week 4-5)

| Component | Effort | Dependencies |
|-----------|--------|--------------|
| IntuitionNetwork | 2 days | PyTorch, sentence-transformers |
| LearnedRetriever | 2 days | PyTorch, sentence-transformers |
| CodeLearner | 3 days | AST, importlib |
| Integration with AGIRunner | 2 days | Above |

**Milestone**: Learning components training during DREAMING

### Phase 4: Full Integration (Week 6)

| Component | Effort | Dependencies |
|-----------|--------|--------------|
| Wire all components into BYRD | 2 days | All above |
| End-to-end testing | 2 days | All above |
| Documentation | 1 day | All above |

**Milestone**: Full AGI cycle with learning demonstrated

---

## Success Criteria

### Minimum Viable AGI Seed

The system achieves "minimum viable" when:

- [ ] AGI Runner executes complete improvement cycles
- [ ] World Model prediction accuracy > 50%
- [ ] At least one pattern codified and executing
- [ ] Capability improvement measured by evaluator
- [ ] Bayesian tracker shows narrowing uncertainty

### Full Learning System

The system demonstrates genuine learning when:

- [ ] Abstraction hierarchy reaches L3 (axioms)
- [ ] Cross-domain transfer observed
- [ ] Novel problems solved (not in seed goals)
- [ ] Intuition network improves decision quality
- [ ] Learned retriever outperforms baseline
- [ ] Multiple codified patterns in use
- [ ] Capability curve shows acceleration

---

## Metrics Dashboard

| Metric | Source | Healthy Range |
|--------|--------|---------------|
| Improvement rate | AGIRunner | > 0 |
| World model accuracy | WorldModel | > 60% |
| Intuition agreement | IntuitionNetwork | > 70% |
| Retrieval helpfulness | LearnedRetriever | > 50% |
| Patterns codified | CodeLearner | Growing |
| Max abstraction level | HierarchicalMemory | L2+ |
| Category count | EmergentCategoryDiscovery | 5+ |
| Capability uncertainty | BayesianTracker | Decreasing |
| Evaluation accuracy | CapabilityEvaluator | > 70% |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| AGI cycles too slow | Batch operations, async execution |
| World model learns wrong rules | Confidence thresholds, validation |
| Intuition overfits | Hold-out evaluation, regularization |
| Code generation fails | Multiple attempts, fallback to patterns |
| Retriever degrades | A/B test against embedding baseline |
| Codified patterns buggy | AST validation, sandbox execution |
| Graph algorithms slow | Projection caching, query optimization |
| Training disrupts operation | Train only during DREAMING mode |

---

## File Structure

```
byrd/
├── agi_runner.py              # The execution engine (NEW)
├── world_model.py             # Causal learning (NEW)
├── intuition_network.py       # Trainable taste (NEW)
├── learned_retriever.py       # Trainable relevance (NEW)
├── code_learner.py            # Pattern codification (NEW)
├── graph_algorithms.py        # Neo4j GDS integration (NEW)
├── bayesian_tracker.py        # Bayesian capabilities (NEW)
├── emergent_categories.py     # Category discovery (NEW)
├── capability_evaluator.py    # Test suites (NEW)
├── information_theory.py      # Math utilities (NEW)
│
├── memory.py                  # EXTEND: hierarchical abstraction
├── memory_reasoner.py         # EXTEND: use learned retriever
├── accelerators.py            # EXTEND: use code learner
├── omega.py                   # EXTEND: orchestrate training
├── goal_evolver.py            # EXTEND: use intuition
├── dreaming_machine.py        # EXTEND: use world model
│
├── learned_strategies/        # Code-as-memory (NEW)
│   ├── desire_routing/
│   ├── pattern_matching/
│   └── decision_making/
│
└── tests/
    ├── test_agi_runner.py
    ├── test_world_model.py
    ├── test_intuition.py
    └── test_integration.py
```

---

## Conclusion

This unified plan merges the execution engine from AGI_SEED_V2 with the learning substrate from ARCHITECTURE_V3_LEARNING. The result is a complete system where:

1. **The AGIRunner drives improvement cycles** - No more islands, everything connects
2. **Learning components enable genuine growth** - Despite frozen LLM weights
3. **Verification provides ground truth** - Training has signal to learn from
4. **Memory becomes hierarchical** - Knowledge compresses into abstractions
5. **Categories emerge from behavior** - No prescribed vocabulary
6. **Stable patterns become code** - Knowledge externalizes permanently

The elegant insight: **Intelligence emerges from the interaction of execution and learning, not from either alone.**

---

*Document version: 1.0*
*Created: December 28, 2024*
*Status: Unified AGI architecture plan*
*Supersedes: AGI_SEED_V2_PLAN.md, ARCHITECTURE_V3_LEARNING.md*
