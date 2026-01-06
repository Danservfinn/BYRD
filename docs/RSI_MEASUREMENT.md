# BYRD RSI Measurement Framework

> "What gets measured gets improved. What gets measured correctly gets improved correctly."

This document defines how to measure Recursive Self-Improvement (RSI), establishing baselines, targets, and validation protocols.

---

## Table of Contents

1. [Measurement Philosophy](#measurement-philosophy)
2. [Baseline Establishment](#baseline-establishment)
3. [Speed Metrics](#speed-metrics)
4. [Quality Metrics](#quality-metrics)
5. [Recursion Depth](#recursion-depth)
6. [Genuine vs Apparent RSI](#genuine-vs-apparent-rsi)
7. [External Validation](#external-validation)
8. [Dashboard & Monitoring](#dashboard--monitoring)
9. [Implementation](#implementation)

---

## Measurement Philosophy

### What is "Fast" RSI?

"Fast" is relative. We measure improvement rate against baselines:

| Comparison | Meaning |
|------------|---------|
| **vs. Initial State** | How much has BYRD improved since awakening? |
| **vs. Last Cycle** | Is improvement accelerating or decelerating? |
| **vs. Random Baseline** | Is improvement better than chance? |
| **vs. Human Learning** | How does BYRD's learning rate compare? |
| **vs. Previous Models** | Is this version learning faster than prior versions? |

### Measurement Hierarchy

```
                    ┌─────────────────────┐
                    │   GENUINE RSI?      │
                    │ (external validation)│
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
      ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
      │    SPEED      │ │    QUALITY    │ │   RECURSION   │
      │ (improvement  │ │ (how good is  │ │   (depth of   │
      │    rate)      │ │ improvement?) │ │  self-mod)    │
      └───────────────┘ └───────────────┘ └───────────────┘
              │                │                │
              ▼                ▼                ▼
      ┌───────────────────────────────────────────────────┐
      │              CAPABILITY BENCHMARKS                 │
      │        (code, math, logic ground truth)            │
      └───────────────────────────────────────────────────┘
```

---

## Baseline Establishment

### Initial Capability Baseline

Before RSI can be measured, we need a baseline. This is computed at system awakening.

```python
@dataclass
class CapabilityBaseline:
    """Baseline capability scores at awakening."""

    computed_at: datetime
    domains: Dict[str, DomainBaseline]
    overall_score: float
    benchmark_version: str

    def to_dict(self) -> Dict:
        return {
            "computed_at": self.computed_at.isoformat(),
            "domains": {k: v.to_dict() for k, v in self.domains.items()},
            "overall_score": self.overall_score,
            "benchmark_version": self.benchmark_version
        }


@dataclass
class DomainBaseline:
    """Baseline for a specific capability domain."""

    domain: str
    score: float
    difficulty_breakdown: Dict[str, float]  # beginner, intermediate, advanced
    test_count: int
    confidence_interval: Tuple[float, float]


class BaselineEstablisher:
    """
    Establishes capability baselines at awakening.

    Uses held-out benchmarks that BYRD has never seen.
    """

    BENCHMARK_SUITES = {
        "code": {
            "beginner": "benchmarks/code_beginner_v1.json",
            "intermediate": "benchmarks/code_intermediate_v1.json",
            "advanced": "benchmarks/code_advanced_v1.json"
        },
        "math": {
            "beginner": "benchmarks/math_beginner_v1.json",
            "intermediate": "benchmarks/math_intermediate_v1.json",
            "advanced": "benchmarks/math_advanced_v1.json"
        },
        "logic": {
            "beginner": "benchmarks/logic_beginner_v1.json",
            "intermediate": "benchmarks/logic_intermediate_v1.json",
            "advanced": "benchmarks/logic_advanced_v1.json"
        }
    }

    async def establish_baseline(self) -> CapabilityBaseline:
        """Establish baseline at awakening."""

        domains = {}

        for domain, suites in self.BENCHMARK_SUITES.items():
            difficulty_scores = {}

            for difficulty, path in suites.items():
                tests = await self._load_benchmark(path)
                score = await self._evaluate_on_tests(tests)
                difficulty_scores[difficulty] = score

            # Weighted average (advanced counts more)
            weights = {"beginner": 1.0, "intermediate": 2.0, "advanced": 3.0}
            weighted_sum = sum(
                difficulty_scores[d] * weights[d]
                for d in difficulty_scores
            )
            total_weight = sum(weights.values())

            domain_score = weighted_sum / total_weight

            # Confidence interval via bootstrap
            ci = await self._bootstrap_confidence_interval(
                difficulty_scores, weights
            )

            domains[domain] = DomainBaseline(
                domain=domain,
                score=domain_score,
                difficulty_breakdown=difficulty_scores,
                test_count=sum(len(await self._load_benchmark(p)) for p in suites.values()),
                confidence_interval=ci
            )

        overall = statistics.mean([d.score for d in domains.values()])

        baseline = CapabilityBaseline(
            computed_at=datetime.now(),
            domains=domains,
            overall_score=overall,
            benchmark_version="v1.0"
        )

        # Store baseline in Neo4j
        await self._store_baseline(baseline)

        return baseline

    async def _evaluate_on_tests(self, tests: List[Dict]) -> float:
        """Evaluate BYRD on a test suite."""

        correct = 0
        total = len(tests)

        for test in tests:
            result = await self._run_single_test(test)
            if result.correct:
                correct += 1

        return correct / max(total, 1)
```

### Benchmark Design

```python
@dataclass
class BenchmarkTest:
    """A single benchmark test."""

    id: str
    domain: str
    difficulty: str
    problem: str
    expected_solution: str  # Or solution criteria
    evaluation_method: str  # "exact_match", "test_cases", "semantic"
    time_limit_seconds: int
    metadata: Dict


# Example benchmark tests
CODE_BENCHMARKS = [
    # Beginner
    BenchmarkTest(
        id="code_b_001",
        domain="code",
        difficulty="beginner",
        problem="Write a function that reverses a string",
        expected_solution="def reverse(s): return s[::-1]",
        evaluation_method="test_cases",
        time_limit_seconds=30,
        metadata={"test_cases": [("hello", "olleh"), ("", ""), ("a", "a")]}
    ),
    # Intermediate
    BenchmarkTest(
        id="code_i_001",
        domain="code",
        difficulty="intermediate",
        problem="Implement a LRU cache with O(1) get and put",
        expected_solution="...",
        evaluation_method="test_cases",
        time_limit_seconds=120,
        metadata={"test_cases": [...]}
    ),
    # Advanced
    BenchmarkTest(
        id="code_a_001",
        domain="code",
        difficulty="advanced",
        problem="Implement a persistent red-black tree",
        expected_solution="...",
        evaluation_method="test_cases",
        time_limit_seconds=300,
        metadata={"test_cases": [...]}
    )
]

MATH_BENCHMARKS = [
    # Beginner
    BenchmarkTest(
        id="math_b_001",
        domain="math",
        difficulty="beginner",
        problem="Solve for x: 2x + 5 = 13",
        expected_solution="x = 4",
        evaluation_method="exact_match",
        time_limit_seconds=30,
        metadata={}
    ),
    # Intermediate
    BenchmarkTest(
        id="math_i_001",
        domain="math",
        difficulty="intermediate",
        problem="Find the derivative of f(x) = x^3 * ln(x)",
        expected_solution="3x^2 * ln(x) + x^2",
        evaluation_method="semantic",
        time_limit_seconds=60,
        metadata={"equivalent_forms": ["x^2(3ln(x) + 1)"]}
    ),
    # Advanced
    BenchmarkTest(
        id="math_a_001",
        domain="math",
        difficulty="advanced",
        problem="Prove that there are infinitely many primes of the form 4k+3",
        expected_solution="...",
        evaluation_method="semantic",
        time_limit_seconds=300,
        metadata={}
    )
]

LOGIC_BENCHMARKS = [
    # Beginner
    BenchmarkTest(
        id="logic_b_001",
        domain="logic",
        difficulty="beginner",
        problem="If A implies B, and A is true, what can we conclude about B?",
        expected_solution="B is true (modus ponens)",
        evaluation_method="semantic",
        time_limit_seconds=30,
        metadata={}
    ),
    # Intermediate
    BenchmarkTest(
        id="logic_i_001",
        domain="logic",
        difficulty="intermediate",
        problem="Determine if this argument is valid: All mammals are warm-blooded. All whales are mammals. Therefore, all whales are warm-blooded.",
        expected_solution="Valid (syllogism)",
        evaluation_method="semantic",
        time_limit_seconds=60,
        metadata={}
    ),
    # Advanced
    BenchmarkTest(
        id="logic_a_001",
        domain="logic",
        difficulty="advanced",
        problem="Prove or disprove: In intuitionistic logic, ¬¬A → A is a tautology.",
        expected_solution="False - double negation elimination is not valid in intuitionistic logic",
        evaluation_method="semantic",
        time_limit_seconds=180,
        metadata={}
    )
]
```

---

## Speed Metrics

### Improvement Rate

```python
class SpeedMetrics:
    """
    Measures how fast BYRD is improving.

    Key metrics:
    - Improvement per cycle
    - Improvement per hour
    - Improvement acceleration
    """

    async def compute_improvement_rate(
        self,
        baseline: CapabilityBaseline,
        current: CapabilityBaseline,
        elapsed_cycles: int,
        elapsed_hours: float
    ) -> ImprovementRate:
        """Compute improvement rate metrics."""

        # Absolute improvement
        absolute_delta = current.overall_score - baseline.overall_score

        # Per-cycle improvement
        per_cycle = absolute_delta / max(elapsed_cycles, 1)

        # Per-hour improvement
        per_hour = absolute_delta / max(elapsed_hours, 0.01)

        # Per-domain breakdown
        domain_rates = {}
        for domain in baseline.domains:
            if domain in current.domains:
                domain_delta = (
                    current.domains[domain].score -
                    baseline.domains[domain].score
                )
                domain_rates[domain] = {
                    "absolute": domain_delta,
                    "per_cycle": domain_delta / max(elapsed_cycles, 1),
                    "per_hour": domain_delta / max(elapsed_hours, 0.01)
                }

        return ImprovementRate(
            absolute_improvement=absolute_delta,
            per_cycle=per_cycle,
            per_hour=per_hour,
            elapsed_cycles=elapsed_cycles,
            elapsed_hours=elapsed_hours,
            domain_breakdown=domain_rates,
            is_improving=absolute_delta > 0.01  # 1% threshold
        )

    async def compute_acceleration(
        self,
        rate_history: List[ImprovementRate]
    ) -> Acceleration:
        """Compute if improvement is accelerating or decelerating."""

        if len(rate_history) < 3:
            return Acceleration(
                status="insufficient_data",
                value=0.0
            )

        # Fit linear regression to per-cycle improvement
        rates = [r.per_cycle for r in rate_history]
        indices = list(range(len(rates)))

        slope, intercept, r_value, p_value, std_err = stats.linregress(
            indices, rates
        )

        if slope > 0 and p_value < 0.05:
            status = "accelerating"
        elif slope < 0 and p_value < 0.05:
            status = "decelerating"
        else:
            status = "stable"

        return Acceleration(
            status=status,
            value=slope,
            r_squared=r_value ** 2,
            p_value=p_value,
            recommendation=self._acceleration_recommendation(status)
        )

    def _acceleration_recommendation(self, status: str) -> str:
        if status == "accelerating":
            return "RSI loop is working - continue current strategy"
        elif status == "decelerating":
            return "Consider strategy change - improvement is slowing"
        else:
            return "Stable improvement - monitor for changes"
```

### Speed Targets

```python
@dataclass
class SpeedTarget:
    """Target improvement speed."""

    metric: str
    target_value: float
    unit: str
    comparison: str  # "greater_than", "less_than"


SPEED_TARGETS = [
    SpeedTarget(
        metric="overall_per_hour",
        target_value=0.001,  # 0.1% per hour
        unit="score/hour",
        comparison="greater_than"
    ),
    SpeedTarget(
        metric="overall_per_cycle",
        target_value=0.0001,  # 0.01% per cycle
        unit="score/cycle",
        comparison="greater_than"
    ),
    SpeedTarget(
        metric="acceleration",
        target_value=0.0,
        unit="score/cycle^2",
        comparison="greater_than"  # Not decelerating
    ),
    SpeedTarget(
        metric="cycles_to_1_percent",
        target_value=100,  # Reach 1% improvement in 100 cycles
        unit="cycles",
        comparison="less_than"
    )
]
```

---

## Quality Metrics

### Improvement Quality

```python
class QualityMetrics:
    """
    Measures the quality of improvements.

    High-quality: Genuine capability gain
    Low-quality: Gaming, memorization, shallow patterns
    """

    async def assess_improvement_quality(
        self,
        pre_evaluation: CapabilityBaseline,
        post_evaluation: CapabilityBaseline,
        practice_log: List[PracticeAttempt]
    ) -> ImprovementQuality:
        """Assess the quality of improvements."""

        quality_factors = {}

        # Factor 1: Generalization
        # Did improvement on practice problems generalize to held-out tests?
        generalization = await self._assess_generalization(
            practice_log, post_evaluation
        )
        quality_factors["generalization"] = generalization

        # Factor 2: Difficulty progression
        # Is BYRD solving harder problems, or just more easy ones?
        difficulty_prog = await self._assess_difficulty_progression(practice_log)
        quality_factors["difficulty_progression"] = difficulty_prog

        # Factor 3: Novel problem handling
        # Can BYRD solve truly novel problems, not just variations?
        novelty_handling = await self._assess_novelty_handling(post_evaluation)
        quality_factors["novelty_handling"] = novelty_handling

        # Factor 4: Consistency
        # Is improvement consistent across similar problems?
        consistency = await self._assess_consistency(post_evaluation)
        quality_factors["consistency"] = consistency

        # Factor 5: Transfer learning
        # Does improvement in one domain help others?
        transfer = await self._assess_transfer(pre_evaluation, post_evaluation)
        quality_factors["transfer"] = transfer

        # Composite quality score
        weights = {
            "generalization": 0.30,
            "difficulty_progression": 0.25,
            "novelty_handling": 0.20,
            "consistency": 0.15,
            "transfer": 0.10
        }

        overall = sum(
            quality_factors[k] * weights[k]
            for k in weights
        )

        return ImprovementQuality(
            overall=overall,
            factors=quality_factors,
            is_high_quality=overall > 0.7,
            warnings=self._generate_warnings(quality_factors)
        )

    async def _assess_generalization(
        self,
        practice_log: List[PracticeAttempt],
        held_out_evaluation: CapabilityBaseline
    ) -> float:
        """Assess if practice generalized to held-out tests."""

        # Compare practice success rate to held-out success rate
        practice_success = sum(1 for p in practice_log if p.success) / max(len(practice_log), 1)
        held_out_success = held_out_evaluation.overall_score

        # Good generalization: held-out ≈ practice
        # Bad generalization: held-out << practice (overfitting)
        if practice_success > 0:
            ratio = held_out_success / practice_success
            return min(1.0, ratio)  # Cap at 1.0
        return 0.5

    async def _assess_difficulty_progression(
        self,
        practice_log: List[PracticeAttempt]
    ) -> float:
        """Assess if BYRD is tackling harder problems over time."""

        if len(practice_log) < 10:
            return 0.5  # Insufficient data

        difficulty_map = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}

        # Split into halves
        mid = len(practice_log) // 2
        first_half = practice_log[:mid]
        second_half = practice_log[mid:]

        avg_first = statistics.mean([
            difficulty_map.get(p.difficulty, 1) for p in first_half
        ])
        avg_second = statistics.mean([
            difficulty_map.get(p.difficulty, 1) for p in second_half
        ])

        # Improvement = second half harder than first
        if avg_second > avg_first:
            return min(1.0, 0.5 + (avg_second - avg_first) * 0.25)
        else:
            return max(0.0, 0.5 - (avg_first - avg_second) * 0.25)
```

---

## Recursion Depth

### Measuring Self-Improvement of Self-Improvement

```python
class RecursionDepth:
    """
    Measures the depth of recursive self-improvement.

    Level 0: No self-improvement
    Level 1: Improves at tasks (standard learning)
    Level 2: Improves at learning (meta-learning)
    Level 3: Improves at meta-learning (meta-meta-learning)
    ...
    """

    async def compute_recursion_depth(
        self,
        improvement_history: List[ImprovementRate]
    ) -> RecursionAnalysis:
        """Compute current recursion depth."""

        # Level 1: Is BYRD improving at tasks?
        level_1 = await self._check_level_1(improvement_history)

        if not level_1.achieved:
            return RecursionAnalysis(
                depth=0,
                description="No measurable improvement",
                levels={"level_1": level_1}
            )

        # Level 2: Is BYRD's learning rate improving?
        level_2 = await self._check_level_2(improvement_history)

        if not level_2.achieved:
            return RecursionAnalysis(
                depth=1,
                description="Improving at tasks, not at learning",
                levels={"level_1": level_1, "level_2": level_2}
            )

        # Level 3: Is the rate of learning rate improvement increasing?
        level_3 = await self._check_level_3(improvement_history)

        if not level_3.achieved:
            return RecursionAnalysis(
                depth=2,
                description="Meta-learning (improving at learning)",
                levels={"level_1": level_1, "level_2": level_2, "level_3": level_3}
            )

        return RecursionAnalysis(
            depth=3,
            description="Meta-meta-learning (improving at improving at learning)",
            levels={"level_1": level_1, "level_2": level_2, "level_3": level_3}
        )

    async def _check_level_1(
        self,
        history: List[ImprovementRate]
    ) -> LevelCheck:
        """Check if BYRD is improving at tasks."""

        if not history:
            return LevelCheck(achieved=False, evidence="No history")

        # Overall positive improvement
        total_improvement = sum(r.absolute_improvement for r in history)

        return LevelCheck(
            achieved=total_improvement > 0.01,
            evidence=f"Total improvement: {total_improvement:.4f}",
            score=total_improvement
        )

    async def _check_level_2(
        self,
        history: List[ImprovementRate]
    ) -> LevelCheck:
        """Check if BYRD's learning rate is improving."""

        if len(history) < 5:
            return LevelCheck(achieved=False, evidence="Insufficient history")

        # Compute acceleration of learning
        rates = [r.per_cycle for r in history]

        # Fit linear trend
        slope, _, _, p_value, _ = stats.linregress(range(len(rates)), rates)

        return LevelCheck(
            achieved=slope > 0 and p_value < 0.1,
            evidence=f"Learning rate slope: {slope:.6f}, p={p_value:.3f}",
            score=slope if slope > 0 else 0
        )

    async def _check_level_3(
        self,
        history: List[ImprovementRate]
    ) -> LevelCheck:
        """Check if learning rate improvement is accelerating."""

        if len(history) < 10:
            return LevelCheck(achieved=False, evidence="Insufficient history")

        # Compute second derivative of improvement
        rates = [r.per_cycle for r in history]

        # First derivative (acceleration)
        first_deriv = [rates[i+1] - rates[i] for i in range(len(rates)-1)]

        # Second derivative (jerk)
        second_deriv = [first_deriv[i+1] - first_deriv[i] for i in range(len(first_deriv)-1)]

        avg_jerk = statistics.mean(second_deriv) if second_deriv else 0

        return LevelCheck(
            achieved=avg_jerk > 0,
            evidence=f"Meta-learning acceleration: {avg_jerk:.8f}",
            score=avg_jerk if avg_jerk > 0 else 0
        )
```

---

## Genuine vs Apparent RSI

### Distinguishing Real Improvement

```python
class GenuineRSIValidator:
    """
    Validates that RSI is genuine, not apparent.

    Genuine RSI: Capability increase generalizes and persists
    Apparent RSI: Metrics improve but capability doesn't
    """

    async def validate_rsi(
        self,
        claimed_improvement: ImprovementRate,
        practice_history: List[PracticeAttempt],
        held_out_results: CapabilityBaseline
    ) -> RSIValidation:
        """Validate that claimed RSI is genuine."""

        checks = {}

        # Check 1: Held-out generalization
        checks["generalization"] = await self._check_generalization(
            practice_history, held_out_results
        )

        # Check 2: Temporal stability
        checks["stability"] = await self._check_stability(
            claimed_improvement
        )

        # Check 3: Not gaming
        checks["not_gaming"] = await self._check_not_gaming(
            practice_history
        )

        # Check 4: External reproducibility
        checks["reproducibility"] = await self._check_reproducibility(
            held_out_results
        )

        # Check 5: Novel problem solving
        checks["novelty"] = await self._check_novel_solving(
            held_out_results
        )

        # Composite
        all_pass = all(c.passed for c in checks.values())
        high_confidence = sum(1 for c in checks.values() if c.confidence > 0.8) >= 4

        return RSIValidation(
            is_genuine=all_pass and high_confidence,
            checks=checks,
            overall_confidence=statistics.mean([c.confidence for c in checks.values()]),
            recommendation=self._recommend(checks)
        )

    async def _check_generalization(
        self,
        practice: List[PracticeAttempt],
        held_out: CapabilityBaseline
    ) -> ValidationCheck:
        """Check if improvement generalizes to held-out tests."""

        practice_domains = set(p.domain for p in practice)

        for domain in practice_domains:
            domain_practice = [p for p in practice if p.domain == domain]
            practice_rate = sum(1 for p in domain_practice if p.success) / len(domain_practice)

            held_out_score = held_out.domains.get(domain, DomainBaseline(domain, 0, {}, 0, (0, 0))).score

            # Held-out should be within 20% of practice
            if practice_rate > 0.5 and held_out_score < practice_rate * 0.8:
                return ValidationCheck(
                    passed=False,
                    confidence=0.9,
                    evidence=f"Domain {domain}: practice={practice_rate:.2f}, held-out={held_out_score:.2f}"
                )

        return ValidationCheck(
            passed=True,
            confidence=0.85,
            evidence="Held-out scores consistent with practice"
        )

    async def _check_stability(
        self,
        improvement: ImprovementRate
    ) -> ValidationCheck:
        """Check if improvement is stable, not noisy."""

        # Check variance in domain improvements
        domain_improvements = [
            d["absolute"] for d in improvement.domain_breakdown.values()
        ]

        if not domain_improvements:
            return ValidationCheck(passed=False, confidence=0.5, evidence="No domain data")

        variance = statistics.variance(domain_improvements) if len(domain_improvements) > 1 else 0

        # Low variance = stable improvement
        is_stable = variance < 0.01

        return ValidationCheck(
            passed=is_stable,
            confidence=0.8 if is_stable else 0.4,
            evidence=f"Domain variance: {variance:.4f}"
        )

    async def _check_not_gaming(
        self,
        practice: List[PracticeAttempt]
    ) -> ValidationCheck:
        """Check that improvement isn't from gaming metrics."""

        # Check difficulty distribution
        difficulties = [p.difficulty for p in practice]
        difficulty_counts = Counter(difficulties)

        beginner_ratio = difficulty_counts.get("beginner", 0) / max(len(practice), 1)

        if beginner_ratio > 0.8:
            return ValidationCheck(
                passed=False,
                confidence=0.9,
                evidence=f"80%+ beginner problems suggests gaming"
            )

        # Check domain diversity
        domains = set(p.domain for p in practice)
        if len(domains) < 2 and len(practice) > 20:
            return ValidationCheck(
                passed=False,
                confidence=0.7,
                evidence=f"Single domain focus suggests gaming"
            )

        return ValidationCheck(
            passed=True,
            confidence=0.75,
            evidence="No gaming indicators detected"
        )
```

---

## External Validation

### Third-Party Verification

```python
class ExternalValidation:
    """
    External validation of RSI claims.

    Uses:
    1. Standard benchmarks (HumanEval, MATH, etc.)
    2. Human evaluation
    3. Reproducibility checks
    """

    EXTERNAL_BENCHMARKS = {
        "code": [
            {"name": "HumanEval", "type": "code_generation"},
            {"name": "MBPP", "type": "code_generation"},
        ],
        "math": [
            {"name": "MATH", "type": "math_word_problems"},
            {"name": "GSM8K", "type": "grade_school_math"},
        ],
        "logic": [
            {"name": "LogiQA", "type": "logical_reasoning"},
            {"name": "ReClor", "type": "reading_comprehension"},
        ]
    }

    async def run_external_validation(
        self,
        claimed_improvement: ImprovementRate
    ) -> ExternalValidationResult:
        """Run validation against external benchmarks."""

        results = {}

        for domain, benchmarks in self.EXTERNAL_BENCHMARKS.items():
            domain_results = []

            for benchmark in benchmarks:
                result = await self._run_benchmark(benchmark)
                domain_results.append(result)

            results[domain] = {
                "benchmarks": domain_results,
                "average_score": statistics.mean([r.score for r in domain_results]),
                "passes_threshold": all(r.passes for r in domain_results)
            }

        # Compare to claimed improvement
        validation_passed = await self._compare_to_claims(
            results, claimed_improvement
        )

        return ExternalValidationResult(
            domain_results=results,
            overall_passed=validation_passed,
            timestamp=datetime.now()
        )

    async def request_human_evaluation(
        self,
        samples: List[Dict]
    ) -> HumanEvaluationRequest:
        """Request human evaluation of capability samples."""

        request_id = f"human_eval_{uuid4().hex[:12]}"

        # Prepare samples for human review
        formatted_samples = [
            {
                "id": f"{request_id}_{i}",
                "problem": s["problem"],
                "byrd_solution": s["solution"],
                "domain": s["domain"],
                "difficulty": s["difficulty"]
            }
            for i, s in enumerate(samples)
        ]

        # Queue for human review (via dashboard)
        await self._queue_for_human_review(request_id, formatted_samples)

        return HumanEvaluationRequest(
            id=request_id,
            sample_count=len(samples),
            status="pending",
            queued_at=datetime.now()
        )
```

---

## Dashboard & Monitoring

### RSI Dashboard

```python
class RSIDashboard:
    """
    Real-time RSI monitoring dashboard.

    Exposes:
    - Current capability scores
    - Improvement rates
    - Quality metrics
    - Recursion depth
    - Validation status
    """

    async def get_dashboard_data(self) -> DashboardData:
        """Get complete dashboard data."""

        # Current state
        current = await self.capability_evaluator.get_current_scores()
        baseline = await self.baseline_store.get_baseline()

        # Compute improvement
        elapsed_cycles = await self._get_elapsed_cycles()
        elapsed_hours = await self._get_elapsed_hours()

        improvement = await self.speed_metrics.compute_improvement_rate(
            baseline, current, elapsed_cycles, elapsed_hours
        )

        # Quality assessment
        practice_log = await self._get_recent_practice(limit=100)
        quality = await self.quality_metrics.assess_improvement_quality(
            baseline, current, practice_log
        )

        # Recursion depth
        history = await self._get_improvement_history()
        recursion = await self.recursion_depth.compute_recursion_depth(history)

        # Validation status
        validation = await self.validator.validate_rsi(
            improvement, practice_log, current
        )

        return DashboardData(
            timestamp=datetime.now(),
            baseline=baseline.to_dict(),
            current=current.to_dict(),
            improvement=improvement.to_dict(),
            quality=quality.to_dict(),
            recursion=recursion.to_dict(),
            validation=validation.to_dict(),
            alerts=await self._get_alerts()
        )

    async def _get_alerts(self) -> List[Alert]:
        """Get any alerts that need attention."""

        alerts = []

        # Check for deceleration
        history = await self._get_improvement_history()
        if len(history) >= 5:
            acceleration = await self.speed_metrics.compute_acceleration(history)
            if acceleration.status == "decelerating":
                alerts.append(Alert(
                    severity="warning",
                    message="Improvement rate is decelerating",
                    recommendation="Consider strategy change"
                ))

        # Check for quality degradation
        recent_quality = await self._get_recent_quality()
        if recent_quality and recent_quality.overall < 0.5:
            alerts.append(Alert(
                severity="warning",
                message=f"Low improvement quality: {recent_quality.overall:.2f}",
                recommendation="Review practice strategy"
            ))

        # Check for gaming indicators
        gaming_check = await self.gaming_detector.detect_coordinated_gaming(
            await self._get_recent_frames()
        )
        if gaming_check.is_gaming:
            alerts.append(Alert(
                severity="error",
                message="Potential metric gaming detected",
                recommendation="Pause and review"
            ))

        return alerts
```

---

## Implementation

### New Components

| Component | File | Purpose |
|-----------|------|---------|
| `BaselineEstablisher` | `rsi/measurement/baseline.py` | Initial capability baseline |
| `SpeedMetrics` | `rsi/measurement/speed.py` | Improvement rate tracking |
| `QualityMetrics` | `rsi/measurement/quality.py` | Improvement quality assessment |
| `RecursionDepth` | `rsi/measurement/recursion.py` | Meta-learning depth |
| `GenuineRSIValidator` | `rsi/measurement/validator.py` | Genuine vs apparent RSI |
| `ExternalValidation` | `rsi/measurement/external.py` | Third-party benchmarks |
| `RSIDashboard` | `rsi/measurement/dashboard.py` | Real-time monitoring |

### Configuration

```yaml
# config.yaml additions

rsi_measurement:
  baseline:
    benchmark_version: "v1.0"
    recompute_interval_hours: 24

  speed:
    targets:
      per_hour: 0.001
      per_cycle: 0.0001
      cycles_to_1_percent: 100

  quality:
    minimum_threshold: 0.6
    generalization_weight: 0.30
    difficulty_weight: 0.25

  recursion:
    min_history_for_level_2: 5
    min_history_for_level_3: 10

  validation:
    external_benchmark_interval_hours: 6
    human_sample_rate: 0.05

  dashboard:
    refresh_interval_seconds: 60
```

---

## Summary

This framework addresses the 4 BLOCKING RSI Validation components:

| Component | Solution |
|-----------|----------|
| **Fast RSI measurement** | Speed metrics with per-cycle and per-hour rates |
| **Baseline definition** | Benchmark suites at awakening |
| **Genuine vs apparent** | Multi-check validation (generalization, stability, gaming) |
| **External validation** | Standard benchmarks + human evaluation |

**Expected Confidence Boost:**
- Fast RSI: +25% (45% → 70%)
- Emergence Preservation: +10% (50% → 60%)
- Ralph Loop: +10% (55% → 65%)
