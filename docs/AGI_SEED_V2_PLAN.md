# BYRD AGI Seed v2: Closing the Loop

## Overview

Transform the AGI Seed architecture from a design document into a functioning recursive self-improvement engine. The current implementation has the right concepts but lacks the mechanisms that make it actually work.

**Core Problem**: Components exist as islands. Nothing drives the actual improvement cycle.

**Solution**: Build the execution engine that connects everything into a closed loop.

---

## Phase 6: AGI Cycle Runner

### The Missing Engine

Create `agi_runner.py` - the execution engine that drives actual self-improvement.

```
┌─────────────────────────────────────────────────────────────────┐
│                      AGI IMPROVEMENT CYCLE                       │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  ASSESS  │───▶│ IDENTIFY │───▶│ GENERATE │───▶│ PREDICT  │  │
│  │ (SelfMdl)│    │ (Target) │    │(Hypoths) │    │(WorldMdl)│  │
│  └──────────┘    └──────────┘    └──────────┘    └────┬─────┘  │
│       ▲                                               │         │
│       │                                               ▼         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  LEARN   │◀───│ MEASURE  │◀───│ EXECUTE  │◀───│  VERIFY  │  │
│  │ (Update) │    │(Evaluate)│    │ (Apply)  │    │(SafetyMn)│  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
# agi_runner.py

class AGIRunner:
    """
    The execution engine that drives recursive self-improvement.

    This is what was missing: the actual loop that connects
    assessment → action → measurement → learning.
    """

    def __init__(self, byrd):
        self.byrd = byrd
        self.self_model = byrd.self_model
        self.world_model = byrd.world_model
        self.safety_monitor = byrd.safety_monitor
        self.coder = byrd.coder
        self.memory = byrd.memory

        # Cycle tracking
        self._cycle_count = 0
        self._successful_improvements = 0
        self._failed_attempts = 0

        # Improvement queue
        self._improvement_queue: List[ImprovementHypothesis] = []

    async def run_improvement_cycle(self) -> CycleResult:
        """
        Execute one complete improvement cycle.

        This is THE core loop that makes BYRD self-improving.
        """
        self._cycle_count += 1

        # 1. ASSESS: Get current capability state
        inventory = await self.self_model.assess_capabilities(force_refresh=True)

        # 2. IDENTIFY: Select improvement target
        target = await self._select_improvement_target(inventory)
        if not target:
            return CycleResult(success=False, reason="No improvement target identified")

        # 3. GENERATE: Create improvement hypotheses
        hypotheses = await self._generate_hypotheses(target, inventory)
        if not hypotheses:
            return CycleResult(success=False, reason="No hypotheses generated")

        # 4. PREDICT & RANK: Use world model to rank hypotheses
        ranked = await self._rank_hypotheses(hypotheses)

        # 5. VERIFY: Check safety of top hypothesis
        best = ranked[0]
        safety_check = await self.safety_monitor.verify_modification_safety(
            proposed_change=best.code_change,
            target_file=best.target_file,
            rationale=best.rationale
        )

        if not safety_check.safe:
            return CycleResult(
                success=False,
                reason=f"Safety check failed: {safety_check.recommendation}"
            )

        # 6. EXECUTE: Apply the improvement
        execution_result = await self._execute_improvement(best)

        # 7. MEASURE: Evaluate the outcome
        measurement = await self._measure_improvement(target, inventory)

        # 8. LEARN: Update models based on outcome
        await self._learn_from_outcome(best, measurement)

        return CycleResult(
            success=measurement.improved,
            target=target.name,
            improvement_delta=measurement.delta,
            hypothesis=best.description,
            cycle=self._cycle_count
        )

    async def _select_improvement_target(self, inventory) -> Optional[ImprovementTarget]:
        """
        Select the highest-value improvement target.

        Priority order:
        1. Declining capabilities (urgent)
        2. Plateau breakers (if improvement rate stalled)
        3. Weakest capabilities (highest potential gain)
        4. Meta-capabilities (highest leverage)
        """
        # Check for declining capabilities
        declining = [
            cap for cap in inventory.capabilities.values()
            if cap.trend == "declining"
        ]
        if declining:
            worst = min(declining, key=lambda c: c.success_rate)
            return ImprovementTarget(
                name=worst.name,
                current_level=worst.success_rate,
                priority="urgent",
                reason="Capability declining"
            )

        # Check for plateau
        if self.byrd.meta_learning:
            plateau = await self.byrd.meta_learning.detect_plateau()
            if plateau.is_plateau and plateau.affected_capabilities:
                return ImprovementTarget(
                    name=plateau.affected_capabilities[0],
                    current_level=inventory.capabilities[plateau.affected_capabilities[0]].success_rate,
                    priority="high",
                    reason=f"Plateau detected: {plateau.severity.value}"
                )

        # Target weakest capability
        if inventory.weakest:
            weakest_name = inventory.weakest[0]
            weakest_cap = inventory.capabilities[weakest_name]
            return ImprovementTarget(
                name=weakest_name,
                current_level=weakest_cap.success_rate,
                priority="medium",
                reason="Weakest capability"
            )

        return None

    async def _generate_hypotheses(
        self,
        target: ImprovementTarget,
        inventory: CapabilityInventory
    ) -> List[ImprovementHypothesis]:
        """
        Generate concrete improvement hypotheses.

        Each hypothesis includes:
        - What code change to make
        - Why it should help
        - Expected improvement magnitude
        """
        hypotheses = []

        # Strategy 1: Fix known limitations
        limitations = await self.self_model.identify_limitations()
        relevant_lims = [l for l in limitations if l.capability_affected == target.name]

        for lim in relevant_lims[:2]:
            if lim.potential_solutions:
                hypotheses.append(ImprovementHypothesis(
                    description=f"Fix limitation: {lim.description}",
                    target_capability=target.name,
                    strategy="limitation_fix",
                    code_change=await self._generate_fix_code(lim),
                    target_file=self._get_capability_file(target.name),
                    rationale=lim.potential_solutions[0],
                    expected_improvement=lim.severity * 0.5
                ))

        # Strategy 2: Learn from successful patterns
        successful_patterns = await self._get_successful_patterns(target.name)
        for pattern in successful_patterns[:2]:
            hypotheses.append(ImprovementHypothesis(
                description=f"Apply successful pattern: {pattern.name}",
                target_capability=target.name,
                strategy="pattern_application",
                code_change=await self._generate_pattern_code(pattern),
                target_file=self._get_capability_file(target.name),
                rationale=f"Pattern succeeded {pattern.success_count} times",
                expected_improvement=pattern.avg_improvement
            ))

        # Strategy 3: Compose with stronger capabilities
        composable = await self._find_composable_capabilities(target.name, inventory)
        for comp in composable[:2]:
            hypotheses.append(ImprovementHypothesis(
                description=f"Compose with {comp.name}",
                target_capability=target.name,
                strategy="composition",
                code_change=await self._generate_composition_code(target.name, comp),
                target_file=self._get_capability_file(target.name),
                rationale=f"Leverage {comp.name} (success rate: {comp.success_rate:.0%})",
                expected_improvement=0.1
            ))

        return hypotheses

    async def _rank_hypotheses(
        self,
        hypotheses: List[ImprovementHypothesis]
    ) -> List[ImprovementHypothesis]:
        """
        Rank hypotheses using world model predictions.
        """
        for hyp in hypotheses:
            prediction = await self.world_model.predict_outcome(
                action=f"Apply improvement: {hyp.description}",
                context={
                    "target": hyp.target_capability,
                    "strategy": hyp.strategy,
                    "expected_improvement": hyp.expected_improvement
                }
            )
            hyp.predicted_success = prediction.success_probability
            hyp.prediction_confidence = prediction.confidence

        # Rank by expected value: predicted_success * expected_improvement
        return sorted(
            hypotheses,
            key=lambda h: h.predicted_success * h.expected_improvement,
            reverse=True
        )

    async def _execute_improvement(self, hypothesis: ImprovementHypothesis) -> ExecutionResult:
        """
        Execute the improvement with rollback capability.
        """
        # Record for rollback
        await self.byrd.rollback.record_modification(
            file_path=hypothesis.target_file,
            description=hypothesis.description,
            desire_id=None  # Will link to desire if this came from one
        )

        # Apply the code change
        try:
            result = await self.coder.apply_code_change(
                file_path=hypothesis.target_file,
                change=hypothesis.code_change,
                description=hypothesis.description
            )
            return ExecutionResult(success=True, applied_change=hypothesis.code_change)
        except Exception as e:
            return ExecutionResult(success=False, error=str(e))

    async def _measure_improvement(
        self,
        target: ImprovementTarget,
        before_inventory: CapabilityInventory
    ) -> MeasurementResult:
        """
        Measure whether the improvement actually worked.

        This is CRITICAL - without measurement, we can't learn.
        """
        # Re-assess capabilities
        after_inventory = await self.self_model.assess_capabilities(force_refresh=True)

        before_cap = before_inventory.capabilities.get(target.name)
        after_cap = after_inventory.capabilities.get(target.name)

        if not before_cap or not after_cap:
            return MeasurementResult(improved=False, delta=0, reason="Capability not found")

        delta = after_cap.success_rate - before_cap.success_rate

        # Consider improvement if delta > 0.01 (1% improvement)
        improved = delta > 0.01

        if not improved and delta < -0.01:
            # Regression detected - trigger rollback
            await self.byrd.rollback.rollback_last(RollbackReason.CAPABILITY_REGRESSION)
            return MeasurementResult(
                improved=False,
                delta=delta,
                reason="Regression detected, rolled back"
            )

        return MeasurementResult(improved=improved, delta=delta)

    async def _learn_from_outcome(
        self,
        hypothesis: ImprovementHypothesis,
        measurement: MeasurementResult
    ):
        """
        Update all models based on the outcome.

        This closes the learning loop.
        """
        # Update world model with prediction error
        prediction = OutcomePrediction(
            action=hypothesis.description,
            context={"strategy": hypothesis.strategy},
            predicted_outcome="improvement" if hypothesis.predicted_success > 0.5 else "no_improvement",
            success_probability=hypothesis.predicted_success,
            confidence=hypothesis.prediction_confidence,
            uncertainty_type=UncertaintyType.EPISTEMIC,
            uncertainty_sources=[],
            reasoning=hypothesis.rationale,
            similar_past_cases=0
        )

        await self.world_model.update_from_prediction_error(
            prediction=prediction,
            actual_outcome="improved" if measurement.improved else "not_improved",
            actual_success=measurement.improved
        )

        # Record capability attempt
        await self.self_model.record_capability_attempt(
            capability="self_modification",
            success=measurement.improved,
            context={
                "target": hypothesis.target_capability,
                "strategy": hypothesis.strategy,
                "delta": measurement.delta
            }
        )

        # Update meta-learning
        if measurement.improved:
            self._successful_improvements += 1
            await self.byrd.meta_learning.record_domain_learning(
                domain=hypothesis.target_capability,
                knowledge_gained=measurement.delta
            )
        else:
            self._failed_attempts += 1

        # Record as experience
        outcome = "SUCCESS" if measurement.improved else "FAILURE"
        await self.memory.record_experience(
            content=f"[AGI_CYCLE] {outcome}: {hypothesis.description} "
                    f"(delta: {measurement.delta:+.2%})",
            type="agi_cycle",
            metadata={
                "cycle": self._cycle_count,
                "target": hypothesis.target_capability,
                "strategy": hypothesis.strategy,
                "improved": measurement.improved,
                "delta": measurement.delta
            }
        )
```

### Data Classes

```python
@dataclass
class ImprovementTarget:
    name: str
    current_level: float
    priority: str  # "urgent", "high", "medium", "low"
    reason: str

@dataclass
class ImprovementHypothesis:
    description: str
    target_capability: str
    strategy: str  # "limitation_fix", "pattern_application", "composition"
    code_change: str
    target_file: str
    rationale: str
    expected_improvement: float
    predicted_success: float = 0.0
    prediction_confidence: float = 0.0

@dataclass
class CycleResult:
    success: bool
    reason: str = ""
    target: str = ""
    improvement_delta: float = 0.0
    hypothesis: str = ""
    cycle: int = 0

@dataclass
class MeasurementResult:
    improved: bool
    delta: float
    reason: str = ""
```

---

## Phase 7: Real Graph Algorithms

### Replace Fake PageRank with Neo4j GDS

Currently we simulate PageRank with `degree * weight`. This is not PageRank.

### Implementation

1. **Install Neo4j Graph Data Science plugin** in Docker:
```yaml
# docker-compose.yml
neo4j:
  image: neo4j:5.15.0
  environment:
    - NEO4J_PLUGINS=["graph-data-science"]
```

2. **Create graph projection** for algorithms:
```python
# graph_algorithms.py

class GraphAlgorithms:
    """
    Real graph algorithms using Neo4j GDS.
    """

    def __init__(self, memory: Memory):
        self.memory = memory
        self._graph_exists = False

    async def ensure_graph_projection(self):
        """Create or refresh the graph projection for GDS algorithms."""
        if self._graph_exists:
            return

        # Drop existing projection if any
        await self.memory._execute_query("""
            CALL gds.graph.drop('byrd-mind', false)
        """)

        # Create new projection with all node types and relationships
        await self.memory._execute_query("""
            CALL gds.graph.project(
                'byrd-mind',
                ['Experience', 'Reflection', 'Belief', 'Desire', 'Capability'],
                {
                    DERIVED_FROM: {orientation: 'UNDIRECTED'},
                    SUPPORTS: {orientation: 'UNDIRECTED'},
                    CONFLICTS_WITH: {orientation: 'UNDIRECTED'},
                    LED_TO: {orientation: 'NATURAL'},
                    FULFILLS: {orientation: 'NATURAL'}
                },
                {
                    nodeProperties: ['confidence', 'intensity'],
                    relationshipProperties: ['weight']
                }
            )
        """)
        self._graph_exists = True

    async def pagerank(self, limit: int = 20) -> List[Dict]:
        """
        Real PageRank to find most important nodes.
        """
        await self.ensure_graph_projection()

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
                node.description as description,
                score as importance
            ORDER BY score DESC
            LIMIT $limit
        """, {"limit": limit})

        return [dict(r) for r in result]

    async def community_detection(self) -> Dict[str, List[str]]:
        """
        Find communities of related concepts using Louvain.
        """
        await self.ensure_graph_projection()

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

        communities = {}
        for r in result:
            communities[f"community_{r['communityId']}"] = r['members']
        return communities

    async def shortest_path(self, from_content: str, to_content: str) -> Optional[List[Dict]]:
        """
        Find shortest path between two concepts.
        """
        result = await self.memory._execute_query("""
            MATCH (start), (end)
            WHERE start.content CONTAINS $from_content
              AND end.content CONTAINS $to_content
            WITH start, end LIMIT 1
            CALL gds.shortestPath.dijkstra.stream('byrd-mind', {
                sourceNode: start,
                targetNode: end
            })
            YIELD path
            RETURN [node in nodes(path) | {
                content: node.content,
                type: labels(node)[0]
            }] as path_nodes
        """, {"from_content": from_content, "to_content": to_content})

        if result:
            return result[0]["path_nodes"]
        return None

    async def node_similarity(self, node_id: str, limit: int = 10) -> List[Dict]:
        """
        Find nodes most similar to a given node based on graph structure.
        """
        await self.ensure_graph_projection()

        result = await self.memory._execute_query("""
            MATCH (source) WHERE elementId(source) = $node_id
            CALL gds.nodeSimilarity.stream('byrd-mind', {
                topK: $limit
            })
            YIELD node1, node2, similarity
            WHERE gds.util.asNode(node1) = source
            WITH gds.util.asNode(node2) AS similar, similarity
            RETURN
                elementId(similar) as id,
                similar.content as content,
                labels(similar)[0] as type,
                similarity
            ORDER BY similarity DESC
        """, {"node_id": node_id, "limit": limit})

        return [dict(r) for r in result]

    async def betweenness_centrality(self, limit: int = 10) -> List[Dict]:
        """
        Find nodes that are bridges between communities.
        These are key integration points in BYRD's knowledge.
        """
        await self.ensure_graph_projection()

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

---

## Phase 8: Emergent Category Discovery

### Problem
Currently `CAPABILITY_CATEGORIES` is hardcoded, violating emergence principle.

### Solution
Discover categories from behavioral patterns.

```python
# emergent_categories.py

class EmergentCategoryDiscovery:
    """
    Discover capability categories from observed behavior,
    not from prescription.
    """

    def __init__(self, memory: Memory, llm_client: LLMClient):
        self.memory = memory
        self.llm_client = llm_client
        self.discovered_categories: Dict[str, DiscoveredCategory] = {}

    async def discover_categories(self, min_cluster_size: int = 5) -> Dict[str, DiscoveredCategory]:
        """
        Discover capability categories by clustering behavioral patterns.
        """
        # Get all capability attempts
        attempts = await self.memory._execute_query("""
            MATCH (e:Experience)
            WHERE e.type = 'capability_attempt' OR e.type = 'action_outcome'
            RETURN e.content as content, e.capability as capability,
                   e.success as success, e.error as error
            ORDER BY e.timestamp DESC
            LIMIT 500
        """)

        if len(attempts) < min_cluster_size:
            return {}

        # Extract behavioral patterns
        patterns = self._extract_patterns(attempts)

        # Cluster patterns by similarity
        clusters = await self._cluster_patterns(patterns)

        # Name each cluster (this is the only LLM call - for naming, not structure)
        for cluster_id, cluster_patterns in clusters.items():
            if len(cluster_patterns) >= min_cluster_size:
                name, description = await self._name_cluster(cluster_patterns)

                # Calculate success rate for this category
                successes = sum(1 for p in cluster_patterns if p.get("success", False))
                success_rate = successes / len(cluster_patterns)

                self.discovered_categories[name] = DiscoveredCategory(
                    name=name,
                    description=description,
                    pattern_count=len(cluster_patterns),
                    success_rate=success_rate,
                    examples=[p["content"][:100] for p in cluster_patterns[:5]],
                    discovered_at=datetime.now()
                )

        return self.discovered_categories

    def _extract_patterns(self, attempts: List[Dict]) -> List[Dict]:
        """Extract behavioral patterns from attempts."""
        patterns = []
        for attempt in attempts:
            # Extract action verbs and objects
            content = attempt.get("content", "")
            patterns.append({
                "content": content,
                "success": attempt.get("success", False),
                "capability": attempt.get("capability", "unknown"),
                "tokens": self._tokenize(content)
            })
        return patterns

    def _tokenize(self, content: str) -> List[str]:
        """Simple tokenization for pattern matching."""
        # Extract key action words
        import re
        words = re.findall(r'\b[a-z]+\b', content.lower())
        # Filter to meaningful words (remove stop words)
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'for', 'of', 'and', 'in', 'on'}
        return [w for w in words if w not in stop_words and len(w) > 2]

    async def _cluster_patterns(self, patterns: List[Dict]) -> Dict[str, List[Dict]]:
        """Cluster patterns by token similarity."""
        from collections import defaultdict

        clusters = defaultdict(list)

        # Simple clustering by dominant tokens
        for pattern in patterns:
            tokens = pattern["tokens"]
            if not tokens:
                continue

            # Use most common token as cluster key
            # (In production, use proper clustering like k-means on embeddings)
            dominant = max(set(tokens), key=tokens.count) if tokens else "unknown"
            clusters[dominant].append(pattern)

        return dict(clusters)

    async def _name_cluster(self, patterns: List[Dict]) -> Tuple[str, str]:
        """Use LLM to name a discovered cluster."""
        examples = [p["content"][:100] for p in patterns[:10]]

        prompt = f"""These behaviors were observed in an AI system:

{chr(10).join(f'- {e}' for e in examples)}

What capability category do these represent?
Output JSON: {{"name": "short_name", "description": "what this capability does"}}"""

        try:
            response = await self.llm_client.generate(prompt=prompt, max_tokens=100, temperature=0.3)
            data = self.llm_client.parse_json_response(response.text)
            if data:
                return data.get("name", "unknown"), data.get("description", "")
        except:
            pass

        return "unknown", ""


@dataclass
class DiscoveredCategory:
    name: str
    description: str
    pattern_count: int
    success_rate: float
    examples: List[str]
    discovered_at: datetime
```

---

## Phase 9: Closed-Loop Verification

### Problem
No way to verify that improvements actually happened.

### Solution
Create evaluation harnesses with held-out tests.

```python
# evaluation.py

class CapabilityEvaluator:
    """
    Verifies capability improvements with actual tests.
    """

    # Test suites for each capability
    TEST_SUITES = {
        "reasoning": [
            {"input": "If A implies B and B implies C, does A imply C?", "expected": "yes"},
            {"input": "What is wrong with: All cats are animals. Fluffy is an animal. Therefore Fluffy is a cat.", "expected": "invalid"},
            # ... more tests
        ],
        "code_generation": [
            {"input": "Write a function to check if a number is prime", "validator": "returns_correct_for_primes"},
            {"input": "Write a function to reverse a string", "validator": "returns_reversed_string"},
            # ... more tests
        ],
        "research": [
            {"input": "Find the capital of France", "expected_contains": "Paris"},
            {"input": "What year was Python created?", "expected_contains": "1991"},
            # ... more tests
        ]
    }

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self._test_results: Dict[str, List[TestResult]] = {}

    async def evaluate_capability(self, capability: str) -> EvaluationResult:
        """
        Run test suite for a capability and return accuracy.
        """
        if capability not in self.TEST_SUITES:
            return EvaluationResult(capability=capability, accuracy=0.5, confidence=0.0, tests_run=0)

        tests = self.TEST_SUITES[capability]
        passed = 0

        for test in tests:
            result = await self._run_test(capability, test)
            if result.passed:
                passed += 1

        accuracy = passed / len(tests) if tests else 0.0

        return EvaluationResult(
            capability=capability,
            accuracy=accuracy,
            confidence=min(1.0, len(tests) / 20),  # More tests = higher confidence
            tests_run=len(tests)
        )

    async def _run_test(self, capability: str, test: Dict) -> TestResult:
        """Run a single test."""
        try:
            response = await self.llm_client.generate(
                prompt=test["input"],
                max_tokens=200,
                temperature=0.1  # Low temperature for evaluation
            )

            output = response.text.lower()

            if "expected" in test:
                passed = test["expected"].lower() in output
            elif "expected_contains" in test:
                passed = test["expected_contains"].lower() in output
            elif "validator" in test:
                passed = self._run_validator(test["validator"], output)
            else:
                passed = False

            return TestResult(test_input=test["input"], passed=passed, output=output)

        except Exception as e:
            return TestResult(test_input=test["input"], passed=False, error=str(e))


@dataclass
class EvaluationResult:
    capability: str
    accuracy: float
    confidence: float
    tests_run: int

@dataclass
class TestResult:
    test_input: str
    passed: bool
    output: str = ""
    error: str = ""
```

---

## Phase 10: Information-Theoretic Foundation

### Problem
No principled handling of uncertainty. "Bayesian-inspired" but not actually Bayesian.

### Solution
Add proper information-theoretic calculations.

```python
# information_theory.py

import math
from typing import List, Dict, Tuple

class InformationTheory:
    """
    Information-theoretic foundations for learning.
    """

    @staticmethod
    def entropy(probabilities: List[float]) -> float:
        """
        Calculate Shannon entropy of a distribution.

        H(X) = -Σ p(x) log₂ p(x)
        """
        return -sum(p * math.log2(p) for p in probabilities if p > 0)

    @staticmethod
    def information_gain(before_entropy: float, after_entropy: float) -> float:
        """
        Information gain from an observation.

        IG = H(before) - H(after)
        """
        return before_entropy - after_entropy

    @staticmethod
    def bayesian_update(prior: float, likelihood: float, evidence: float) -> float:
        """
        Bayesian belief update.

        P(H|E) = P(E|H) * P(H) / P(E)
        """
        if evidence == 0:
            return prior
        return (likelihood * prior) / evidence

    @staticmethod
    def confidence_interval(successes: int, total: int, confidence: float = 0.95) -> Tuple[float, float]:
        """
        Wilson score interval for binomial proportion.

        Better than simple success/total for small samples.
        """
        if total == 0:
            return (0.0, 1.0)

        import scipy.stats as stats

        z = stats.norm.ppf((1 + confidence) / 2)
        phat = successes / total

        denominator = 1 + z**2 / total
        center = (phat + z**2 / (2 * total)) / denominator
        margin = z * math.sqrt((phat * (1 - phat) + z**2 / (4 * total)) / total) / denominator

        return (max(0, center - margin), min(1, center + margin))


class BayesianCapabilityTracker:
    """
    Track capabilities using proper Bayesian inference.
    """

    def __init__(self):
        # Prior: Beta(1, 1) = uniform
        self.alpha: Dict[str, float] = {}  # successes + 1
        self.beta: Dict[str, float] = {}   # failures + 1

    def update(self, capability: str, success: bool):
        """Update belief about capability after observation."""
        if capability not in self.alpha:
            self.alpha[capability] = 1.0
            self.beta[capability] = 1.0

        if success:
            self.alpha[capability] += 1
        else:
            self.beta[capability] += 1

    def get_estimate(self, capability: str) -> Tuple[float, float, float]:
        """
        Get capability estimate with uncertainty.

        Returns: (mean, lower_95, upper_95)
        """
        if capability not in self.alpha:
            return (0.5, 0.0, 1.0)  # Maximum uncertainty

        a = self.alpha[capability]
        b = self.beta[capability]

        # Mean of Beta distribution
        mean = a / (a + b)

        # 95% credible interval
        import scipy.stats as stats
        lower = stats.beta.ppf(0.025, a, b)
        upper = stats.beta.ppf(0.975, a, b)

        return (mean, lower, upper)

    def get_uncertainty(self, capability: str) -> float:
        """
        Get uncertainty (entropy) of capability belief.
        """
        if capability not in self.alpha:
            return 1.0  # Maximum uncertainty

        a = self.alpha[capability]
        b = self.beta[capability]

        # Entropy of Beta distribution
        import scipy.special as special

        entropy = (
            special.betaln(a, b)
            - (a - 1) * special.psi(a)
            - (b - 1) * special.psi(b)
            + (a + b - 2) * special.psi(a + b)
        )

        # Normalize to [0, 1]
        max_entropy = special.betaln(1, 1)  # Beta(1,1) entropy
        return entropy / max_entropy if max_entropy > 0 else 1.0
```

---

## Phase 11: Integration & Testing

### Integration Points

1. **AGI Runner in main loop**:
```python
# byrd.py
async def _agi_improvement_loop(self):
    """Run continuous AGI improvement cycles."""
    while self._running:
        result = await self.agi_runner.run_improvement_cycle()

        if result.success:
            print(f"🚀 AGI Cycle {result.cycle}: +{result.improvement_delta:.1%} to {result.target}")
        else:
            print(f"📊 AGI Cycle {result.cycle}: {result.reason}")

        await asyncio.sleep(300)  # 5 min between cycles
```

2. **Graph algorithms in reasoning**:
```python
# accelerators.py - Replace GraphPoweredReasoning internals
self.graph_algorithms = GraphAlgorithms(memory)

async def find_important_nodes(self, context: str, limit: int = 10):
    return await self.graph_algorithms.pagerank(limit)
```

3. **Bayesian tracking in SelfModel**:
```python
# self_model.py
self.bayesian_tracker = BayesianCapabilityTracker()

async def record_capability_attempt(self, capability: str, success: bool, ...):
    self.bayesian_tracker.update(capability, success)
    # ... rest of method
```

4. **Emergent categories replace hardcoded**:
```python
# self_model.py
async def assess_capabilities(self, force_refresh: bool = False):
    # Use discovered categories instead of CAPABILITY_CATEGORIES
    if not self.discovered_categories:
        discovery = EmergentCategoryDiscovery(self.memory, self.llm_client)
        self.discovered_categories = await discovery.discover_categories()

    for category_name in self.discovered_categories.keys():
        # ... assess each discovered category
```

### Test Suite

```python
# tests/test_agi_cycle.py

import pytest

class TestAGICycle:

    async def test_full_improvement_cycle(self, byrd_instance):
        """Test that a full AGI cycle completes."""
        runner = byrd_instance.agi_runner
        result = await runner.run_improvement_cycle()

        assert result.cycle == 1
        assert isinstance(result.success, bool)
        assert result.target != "" or result.reason != ""

    async def test_regression_triggers_rollback(self, byrd_instance):
        """Test that capability regression triggers rollback."""
        # Simulate a bad modification
        # Verify rollback was called
        pass

    async def test_world_model_learns_from_error(self, byrd_instance):
        """Test that prediction errors update world model."""
        pass

    async def test_graph_algorithms_run(self, byrd_instance):
        """Test that real graph algorithms execute."""
        algorithms = byrd_instance.graph_algorithms
        important = await algorithms.pagerank(limit=5)

        assert isinstance(important, list)
        # PageRank scores should be positive
        for node in important:
            assert node.get("importance", 0) >= 0

class TestBayesianTracking:

    def test_confidence_grows_with_observations(self):
        """Test that confidence interval narrows with more data."""
        tracker = BayesianCapabilityTracker()

        # Few observations = wide interval
        tracker.update("test", True)
        _, low1, high1 = tracker.get_estimate("test")
        width1 = high1 - low1

        # Many observations = narrow interval
        for _ in range(50):
            tracker.update("test", True)
        _, low2, high2 = tracker.get_estimate("test")
        width2 = high2 - low2

        assert width2 < width1
```

---

## Implementation Order

| Phase | Priority | Complexity | Dependencies |
|-------|----------|------------|--------------|
| Phase 6: AGI Runner | CRITICAL | High | Phases 1-5 |
| Phase 7: Graph Algorithms | High | Medium | Neo4j GDS plugin |
| Phase 8: Emergent Categories | High | Medium | Phase 7 |
| Phase 9: Evaluation Harness | High | Medium | None |
| Phase 10: Info Theory | Medium | Medium | scipy |
| Phase 11: Integration | CRITICAL | High | Phases 6-10 |

---

## Success Criteria

### Phase 6 Complete When:
- [ ] AGI Runner executes full improvement cycles
- [ ] Hypotheses are generated and ranked
- [ ] Improvements are measured and verified
- [ ] Learning loop updates all models
- [ ] Rollback triggers on regression

### Phase 7 Complete When:
- [ ] Neo4j GDS plugin installed
- [ ] Graph projection created
- [ ] PageRank returns meaningful importance scores
- [ ] Community detection finds concept clusters
- [ ] Shortest path finds causal chains

### Phase 8 Complete When:
- [ ] Categories discovered from behavior (not hardcoded)
- [ ] New categories emerge over time
- [ ] Category success rates tracked

### Phase 9 Complete When:
- [ ] Test suites exist for each capability
- [ ] Evaluation runs before/after improvements
- [ ] Accuracy metrics are reliable

### Phase 10 Complete When:
- [ ] Bayesian tracking replaces simple counters
- [ ] Information gain tracked per experience
- [ ] Confidence intervals computed correctly

### Phase 11 Complete When:
- [ ] All phases integrated into BYRD
- [ ] Integration tests pass
- [ ] Full AGI cycle demonstrated end-to-end
- [ ] Improvement verified by evaluation harness

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Neo4j GDS not compatible | Medium | High | Fall back to manual queries |
| AGI cycles too slow | High | Medium | Batch operations, caching |
| Code generation fails | High | Medium | Multiple hypothesis attempts |
| Evaluation tests too narrow | Medium | High | Expand test suites iteratively |
| Bayesian math errors | Low | High | Use well-tested scipy |
| Integration complexity | High | High | Incremental integration, many tests |
