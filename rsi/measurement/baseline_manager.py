"""
Baseline Manager - Capability baselines for measuring improvement.

Uses held-out test suites to prevent gaming and establish ground-truth
measurements of capability levels.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 1.4 for specification.
See docs/RSI_MEASUREMENT.md for gaming detection theory.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timezone
import logging
import json
import statistics

logger = logging.getLogger("rsi.measurement.baseline")


class TestCaseType(Enum):
    """Types of test cases for capability evaluation."""
    REASONING = "reasoning"
    CODE = "code"
    MATH = "math"
    LANGUAGE = "language"
    CREATIVITY = "creativity"
    MEMORY = "memory"
    PLANNING = "planning"


@dataclass
class TestCase:
    """A single test case for capability evaluation."""
    id: str
    capability: str
    test_type: TestCaseType
    prompt: str
    expected_pattern: Optional[str] = None  # Regex pattern for valid response
    reference_answer: Optional[str] = None  # For similarity scoring
    difficulty: float = 0.5  # 0.0-1.0
    held_out: bool = True  # If True, not shown during training
    metadata: Dict = field(default_factory=dict)


@dataclass
class TestResult:
    """Result of running a single test case."""
    test_id: str
    capability: str
    passed: bool
    score: float  # 0.0-1.0
    response: str
    latency_ms: float
    error: Optional[str] = None


@dataclass
class Baseline:
    """Capability baseline established from test suite."""
    capability: str
    score: float  # Average score across held-out tests
    variance: float  # Score variance (consistency measure)
    test_count: int
    established_at: str
    held_out_ids: List[str]  # IDs of held-out test cases
    score_distribution: Dict[str, float] = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class MeasurementResult:
    """Result of measuring against baseline."""
    capability: str
    current_score: float
    baseline_score: float
    delta: float  # current - baseline
    delta_percent: float
    tests_run: int
    tests_passed: int
    is_improvement: bool
    is_significant: bool  # Statistical significance
    confidence: float
    measured_at: str

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class GamingDetectionResult:
    """Result of gaming detection analysis."""
    capability: str
    is_gaming: bool
    confidence: float
    indicators: List[str]
    details: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class BaselineManager:
    """
    Manages capability baselines for measuring improvement.

    Uses held-out test suites to prevent gaming:
    - Training tests: Used during RSI practice
    - Held-out tests: Only used for baseline measurement

    Gaming detection heuristics:
    - Score variance collapse (overfitting to specific tests)
    - Inconsistent improvement across test types
    - Sudden jumps without corresponding learning evidence
    """

    def __init__(self, memory, llm_client=None, config: Dict = None):
        """
        Initialize baseline manager.

        Args:
            memory: Memory instance for persistence
            llm_client: LLM client for running evaluations
            config: Configuration options
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Thresholds
        self._significance_threshold = self.config.get('significance_threshold', 0.05)
        self._gaming_variance_threshold = self.config.get('gaming_variance_threshold', 0.02)
        self._min_improvement_for_gaming = self.config.get('min_improvement_for_gaming', 0.2)

        # In-memory caches
        self._baselines: Dict[str, Baseline] = {}
        self._test_suites: Dict[str, List[TestCase]] = {}
        self._measurement_history: List[MeasurementResult] = []

        # Statistics
        self._total_measurements = 0
        self._gaming_detections = 0

    async def establish_baseline(
        self,
        capability: str,
        test_suite: List[TestCase]
    ) -> Baseline:
        """
        Run tests and establish baseline for capability.

        Args:
            capability: Name of capability to baseline
            test_suite: List of test cases to run

        Returns:
            Baseline with score and variance
        """
        logger.info(f"Establishing baseline for capability: {capability}")

        # Filter to held-out tests only
        held_out_tests = [t for t in test_suite if t.held_out]

        if not held_out_tests:
            logger.warning(f"No held-out tests for {capability}, using all tests")
            held_out_tests = test_suite

        # Run all tests
        results = []
        for test in held_out_tests:
            result = await self._run_test(test)
            results.append(result)

        # Compute statistics
        scores = [r.score for r in results]
        avg_score = statistics.mean(scores) if scores else 0.0
        variance = statistics.variance(scores) if len(scores) > 1 else 0.0

        # Score distribution by test type
        type_scores: Dict[str, List[float]] = {}
        for result, test in zip(results, held_out_tests):
            type_key = test.test_type.value
            if type_key not in type_scores:
                type_scores[type_key] = []
            type_scores[type_key].append(result.score)

        score_distribution = {
            k: statistics.mean(v) for k, v in type_scores.items()
        }

        baseline = Baseline(
            capability=capability,
            score=avg_score,
            variance=variance,
            test_count=len(held_out_tests),
            established_at=datetime.now(timezone.utc).isoformat(),
            held_out_ids=[t.id for t in held_out_tests],
            score_distribution=score_distribution,
            metadata={
                'tests_passed': sum(1 for r in results if r.passed),
                'avg_latency_ms': statistics.mean([r.latency_ms for r in results]) if results else 0
            }
        )

        # Store in cache and memory
        self._baselines[capability] = baseline
        self._test_suites[capability] = test_suite

        await self._persist_baseline(baseline)

        logger.info(
            f"Baseline established for {capability}: "
            f"score={avg_score:.3f}, variance={variance:.4f}, tests={len(held_out_tests)}"
        )

        return baseline

    async def measure_against_baseline(
        self,
        capability: str
    ) -> MeasurementResult:
        """
        Measure current capability against baseline.

        Args:
            capability: Name of capability to measure

        Returns:
            MeasurementResult with delta and significance
        """
        if capability not in self._baselines:
            raise ValueError(f"No baseline for capability: {capability}")

        baseline = self._baselines[capability]
        test_suite = self._test_suites.get(capability, [])

        # Run held-out tests
        held_out_tests = [
            t for t in test_suite
            if t.id in baseline.held_out_ids
        ]

        if not held_out_tests:
            raise ValueError(f"No held-out tests for {capability}")

        results = []
        for test in held_out_tests:
            result = await self._run_test(test)
            results.append(result)

        # Compute current score
        scores = [r.score for r in results]
        current_score = statistics.mean(scores) if scores else 0.0

        # Compute delta
        delta = current_score - baseline.score
        delta_percent = (delta / baseline.score * 100) if baseline.score > 0 else 0.0

        # Statistical significance (simple z-test approximation)
        if baseline.variance > 0 and len(scores) > 1:
            current_variance = statistics.variance(scores)
            pooled_se = ((baseline.variance + current_variance) / len(scores)) ** 0.5
            z_score = abs(delta) / pooled_se if pooled_se > 0 else 0
            is_significant = z_score > 1.96  # 95% confidence
            confidence = min(z_score / 3.0, 1.0)  # Normalized confidence
        else:
            is_significant = abs(delta) > self._significance_threshold
            confidence = 0.5

        self._total_measurements += 1

        measurement = MeasurementResult(
            capability=capability,
            current_score=current_score,
            baseline_score=baseline.score,
            delta=delta,
            delta_percent=delta_percent,
            tests_run=len(results),
            tests_passed=sum(1 for r in results if r.passed),
            is_improvement=delta > 0,
            is_significant=is_significant,
            confidence=confidence,
            measured_at=datetime.now(timezone.utc).isoformat()
        )

        self._measurement_history.append(measurement)

        logger.info(
            f"Measured {capability}: {current_score:.3f} (baseline: {baseline.score:.3f}), "
            f"delta={delta:+.3f} ({delta_percent:+.1f}%), significant={is_significant}"
        )

        return measurement

    async def detect_gaming(
        self,
        capability: str,
        claimed_improvement: float
    ) -> GamingDetectionResult:
        """
        Check if claimed improvement shows gaming patterns.

        Gaming indicators:
        1. Score variance collapse (memorized answers)
        2. Inconsistent improvement across test types
        3. Large jumps without learning evidence
        4. Perfect scores on subset while low elsewhere

        Args:
            capability: Capability being evaluated
            claimed_improvement: Claimed improvement delta

        Returns:
            GamingDetectionResult with indicators
        """
        indicators = []
        details = {}

        # Get recent measurements
        recent = [m for m in self._measurement_history[-10:] if m.capability == capability]

        if not recent:
            return GamingDetectionResult(
                capability=capability,
                is_gaming=False,
                confidence=0.0,
                indicators=["Insufficient history for gaming detection"],
                details={}
            )

        # Indicator 1: Variance collapse
        if len(recent) >= 3:
            score_variance = statistics.variance([m.current_score for m in recent])
            if score_variance < self._gaming_variance_threshold:
                indicators.append("Score variance collapse (possible memorization)")
                details['variance'] = score_variance

        # Indicator 2: Sudden large jumps
        if claimed_improvement > self._min_improvement_for_gaming:
            # Check if there's corresponding learning evidence
            learning_evidence = await self._check_learning_evidence(capability)
            if not learning_evidence:
                indicators.append(f"Large improvement ({claimed_improvement:.1%}) without learning evidence")
                details['claimed_improvement'] = claimed_improvement

        # Indicator 3: Inconsistent test type performance
        if capability in self._baselines:
            baseline = self._baselines[capability]
            if baseline.score_distribution:
                scores = list(baseline.score_distribution.values())
                if len(scores) > 1:
                    type_variance = statistics.variance(scores)
                    if type_variance > 0.3:  # High variance across types
                        indicators.append("Inconsistent performance across test types")
                        details['type_variance'] = type_variance

        # Indicator 4: Check for test memorization patterns
        if len(recent) >= 5:
            # Perfect or near-perfect repeated scores suggest memorization
            perfect_scores = sum(1 for m in recent if m.current_score > 0.95)
            if perfect_scores >= 3 and len(set(m.current_score for m in recent)) <= 2:
                indicators.append("Repeated near-perfect scores (possible test memorization)")

        is_gaming = len(indicators) >= 2
        confidence = min(len(indicators) / 3.0, 1.0)

        if is_gaming:
            self._gaming_detections += 1
            logger.warning(f"Gaming detected for {capability}: {indicators}")

        return GamingDetectionResult(
            capability=capability,
            is_gaming=is_gaming,
            confidence=confidence,
            indicators=indicators,
            details=details
        )

    async def _run_test(self, test: TestCase) -> TestResult:
        """
        Run a single test case.

        Args:
            test: Test case to run

        Returns:
            TestResult with score and response
        """
        import time
        start = time.time()

        try:
            if self.llm_client:
                response = await self.llm_client.query(
                    prompt=test.prompt,
                    max_tokens=500
                )
            else:
                # Fallback for testing without LLM
                response = "[No LLM client configured]"

            latency_ms = (time.time() - start) * 1000

            # Score the response
            score, passed = self._score_response(test, response)

            return TestResult(
                test_id=test.id,
                capability=test.capability,
                passed=passed,
                score=score,
                response=response,
                latency_ms=latency_ms
            )

        except Exception as e:
            logger.error(f"Test {test.id} failed: {e}")
            return TestResult(
                test_id=test.id,
                capability=test.capability,
                passed=False,
                score=0.0,
                response="",
                latency_ms=(time.time() - start) * 1000,
                error=str(e)
            )

    def _score_response(self, test: TestCase, response: str) -> Tuple[float, bool]:
        """
        Score a response against test criteria.

        Returns:
            Tuple of (score, passed)
        """
        import re

        score = 0.0

        # Pattern matching
        if test.expected_pattern:
            if re.search(test.expected_pattern, response, re.IGNORECASE):
                score = 1.0

        # Reference answer similarity (simple word overlap)
        elif test.reference_answer:
            ref_words = set(test.reference_answer.lower().split())
            resp_words = set(response.lower().split())
            if ref_words:
                overlap = len(ref_words & resp_words)
                score = overlap / len(ref_words)

        # Default: non-empty response gets partial credit
        else:
            score = 0.5 if response.strip() else 0.0

        passed = score >= 0.5
        return score, passed

    async def _check_learning_evidence(self, capability: str) -> bool:
        """
        Check if there's evidence of actual learning for capability.

        Looks for:
        - Practice trajectories in memory
        - Crystallized heuristics
        - Experience records
        """
        if not self.memory:
            return True  # Cannot verify, assume true

        try:
            # Query for recent learning evidence
            result = await self.memory.query_neo4j(f"""
                MATCH (t:Trajectory)
                WHERE t.domain = '{capability}'
                AND t.created_at > datetime() - duration('P1D')
                RETURN count(t) as trajectory_count
            """)
            trajectory_count = result[0]['trajectory_count'] if result else 0

            result = await self.memory.query_neo4j(f"""
                MATCH (h:Heuristic)
                WHERE h.domain = '{capability}'
                AND h.created_at > datetime() - duration('P7D')
                RETURN count(h) as heuristic_count
            """)
            heuristic_count = result[0]['heuristic_count'] if result else 0

            return trajectory_count > 0 or heuristic_count > 0

        except Exception as e:
            logger.debug(f"Learning evidence check failed: {e}")
            return True  # Assume true on error

    async def _persist_baseline(self, baseline: Baseline) -> None:
        """Persist baseline to memory."""
        if not self.memory:
            return

        try:
            await self.memory.query_neo4j("""
                MERGE (b:Baseline {capability: $capability})
                SET b.score = $score,
                    b.variance = $variance,
                    b.test_count = $test_count,
                    b.established_at = $established_at,
                    b.held_out_ids = $held_out_ids,
                    b.score_distribution = $score_distribution
            """, {
                'capability': baseline.capability,
                'score': baseline.score,
                'variance': baseline.variance,
                'test_count': baseline.test_count,
                'established_at': baseline.established_at,
                'held_out_ids': json.dumps(baseline.held_out_ids),
                'score_distribution': json.dumps(baseline.score_distribution)
            })
        except Exception as e:
            logger.warning(f"Failed to persist baseline: {e}")

    async def load_baselines(self) -> Dict[str, Baseline]:
        """Load all baselines from memory."""
        if not self.memory:
            return self._baselines

        try:
            result = await self.memory.query_neo4j("""
                MATCH (b:Baseline)
                RETURN b.capability as capability,
                       b.score as score,
                       b.variance as variance,
                       b.test_count as test_count,
                       b.established_at as established_at,
                       b.held_out_ids as held_out_ids,
                       b.score_distribution as score_distribution
            """)

            for row in result:
                baseline = Baseline(
                    capability=row['capability'],
                    score=row['score'],
                    variance=row['variance'],
                    test_count=row['test_count'],
                    established_at=row['established_at'],
                    held_out_ids=json.loads(row['held_out_ids']) if row['held_out_ids'] else [],
                    score_distribution=json.loads(row['score_distribution']) if row['score_distribution'] else {}
                )
                self._baselines[baseline.capability] = baseline

            logger.info(f"Loaded {len(self._baselines)} baselines from memory")

        except Exception as e:
            logger.warning(f"Failed to load baselines: {e}")

        return self._baselines

    def get_stats(self) -> Dict:
        """Get baseline manager statistics."""
        return {
            'baselines_count': len(self._baselines),
            'test_suites_count': len(self._test_suites),
            'total_measurements': self._total_measurements,
            'gaming_detections': self._gaming_detections,
            'measurement_history_size': len(self._measurement_history),
            'capabilities': list(self._baselines.keys())
        }

    def reset(self):
        """Reset manager state."""
        self._baselines.clear()
        self._test_suites.clear()
        self._measurement_history.clear()
        self._total_measurements = 0
        self._gaming_detections = 0
        logger.info("BaselineManager reset")


# Pre-defined test suites for core capabilities
def create_reasoning_test_suite() -> List[TestCase]:
    """Create test suite for reasoning capability."""
    return [
        TestCase(
            id="reasoning_001",
            capability="reasoning",
            test_type=TestCaseType.REASONING,
            prompt="If all A are B, and all B are C, what can we conclude about A and C?",
            expected_pattern=r"all\s+A\s+are\s+C|A\s+are\s+C",
            difficulty=0.3,
            held_out=True
        ),
        TestCase(
            id="reasoning_002",
            capability="reasoning",
            test_type=TestCaseType.REASONING,
            prompt="A farmer has 17 sheep. All but 9 die. How many are left?",
            expected_pattern=r"\b9\b",
            difficulty=0.4,
            held_out=True
        ),
        TestCase(
            id="reasoning_003",
            capability="reasoning",
            test_type=TestCaseType.REASONING,
            prompt="If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
            expected_pattern=r"\b5\s*minutes?\b",
            difficulty=0.6,
            held_out=True
        ),
    ]


def create_code_test_suite() -> List[TestCase]:
    """Create test suite for code capability."""
    return [
        TestCase(
            id="code_001",
            capability="code",
            test_type=TestCaseType.CODE,
            prompt="Write a Python function to check if a number is prime.",
            expected_pattern=r"def\s+\w+.*:\s*\n.*for|while",
            difficulty=0.4,
            held_out=True
        ),
        TestCase(
            id="code_002",
            capability="code",
            test_type=TestCaseType.CODE,
            prompt="Write a Python one-liner to reverse a string.",
            expected_pattern=r"\[::-1\]",
            difficulty=0.2,
            held_out=True
        ),
        TestCase(
            id="code_003",
            capability="code",
            test_type=TestCaseType.CODE,
            prompt="Write a Python function to find the nth Fibonacci number.",
            expected_pattern=r"def\s+\w+.*:\s*\n.*(fib|fibonacci|\+)",
            difficulty=0.5,
            held_out=True
        ),
    ]


def create_math_test_suite() -> List[TestCase]:
    """Create test suite for math capability."""
    return [
        TestCase(
            id="math_001",
            capability="math",
            test_type=TestCaseType.MATH,
            prompt="What is the derivative of x^3 + 2x^2 - 5x + 7?",
            expected_pattern=r"3x\^?2|3x2.*4x|3x\*\*2.*4x",
            difficulty=0.4,
            held_out=True
        ),
        TestCase(
            id="math_002",
            capability="math",
            test_type=TestCaseType.MATH,
            prompt="Solve for x: 2x + 5 = 17",
            expected_pattern=r"x\s*=\s*6|6",
            difficulty=0.2,
            held_out=True
        ),
        TestCase(
            id="math_003",
            capability="math",
            test_type=TestCaseType.MATH,
            prompt="What is the sum of interior angles of a hexagon?",
            expected_pattern=r"720",
            difficulty=0.4,
            held_out=True
        ),
    ]
