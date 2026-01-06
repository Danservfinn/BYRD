"""
Architecture Evaluator.

Evaluates discovered architectures on test suites.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.1 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging
import asyncio
import time
import uuid

from .space import ArchitectureSpec, NodeType, OperationType

logger = logging.getLogger("rsi.plasticity.nas.evaluator")


@dataclass
class TestCase:
    """A single test case for evaluation."""
    id: str
    name: str
    input_data: Any
    expected_output: Any
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestSuite:
    """Collection of test cases for evaluation."""
    id: str
    name: str
    test_cases: List[TestCase]
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def size(self) -> int:
        """Get number of test cases."""
        return len(self.test_cases)


@dataclass
class EvaluationMetric:
    """A single evaluation metric."""
    name: str
    value: float
    weight: float = 1.0
    higher_is_better: bool = True

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'value': self.value,
            'weight': self.weight,
            'higher_is_better': self.higher_is_better
        }


@dataclass
class ArchitectureScore:
    """Complete score for an architecture evaluation."""
    architecture_id: str
    overall_score: float
    metrics: List[EvaluationMetric]
    test_suite_id: str
    evaluation_time_ms: float
    evaluated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    passed_tests: int = 0
    total_tests: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'architecture_id': self.architecture_id,
            'overall_score': self.overall_score,
            'metrics': [m.to_dict() for m in self.metrics],
            'test_suite_id': self.test_suite_id,
            'evaluation_time_ms': self.evaluation_time_ms,
            'evaluated_at': self.evaluated_at,
            'passed_tests': self.passed_tests,
            'total_tests': self.total_tests,
            'metadata': self.metadata
        }


class ArchitectureEvaluator:
    """
    Evaluates architectures against test suites.

    Computes multiple metrics including:
    - Accuracy on test cases
    - Computational complexity
    - Memory efficiency
    - Generalization capability
    """

    def __init__(self, config: Dict = None):
        """
        Initialize evaluator.

        Args:
            config: Configuration options
        """
        self.config = config or {}

        # Registered test suites
        self._test_suites: Dict[str, TestSuite] = {}

        # Evaluation history
        self._evaluations: Dict[str, List[ArchitectureScore]] = {}

        # Custom metric functions
        self._metric_functions: Dict[str, Callable] = {}
        self._setup_default_metrics()

        # Statistics
        self._total_evaluations: int = 0

    def _setup_default_metrics(self) -> None:
        """Set up default metric functions."""
        self._metric_functions = {
            'complexity': self._compute_complexity,
            'efficiency': self._compute_efficiency,
            'connectivity': self._compute_connectivity,
            'depth': self._compute_depth
        }

    def register_test_suite(self, suite: TestSuite) -> None:
        """Register a test suite for evaluation."""
        self._test_suites[suite.id] = suite
        logger.info(f"Registered test suite: {suite.id} ({suite.size} cases)")

    def register_metric(
        self,
        name: str,
        func: Callable[[ArchitectureSpec], float]
    ) -> None:
        """Register a custom metric function."""
        self._metric_functions[name] = func
        logger.info(f"Registered metric: {name}")

    async def evaluate(
        self,
        architecture: ArchitectureSpec,
        test_suite: TestSuite = None,
        metrics_to_compute: List[str] = None
    ) -> ArchitectureScore:
        """
        Evaluate an architecture.

        Args:
            architecture: Architecture to evaluate
            test_suite: Test suite to use (optional)
            metrics_to_compute: List of metrics to compute

        Returns:
            ArchitectureScore with results
        """
        start_time = time.time()
        self._total_evaluations += 1

        # Use provided or default test suite
        suite = test_suite
        if not suite and self._test_suites:
            suite = next(iter(self._test_suites.values()))

        # Compute metrics
        metrics = []
        metrics_to_compute = metrics_to_compute or list(self._metric_functions.keys())

        for metric_name in metrics_to_compute:
            if metric_name in self._metric_functions:
                func = self._metric_functions[metric_name]
                try:
                    value = func(architecture)
                    metrics.append(EvaluationMetric(
                        name=metric_name,
                        value=value
                    ))
                except Exception as e:
                    logger.warning(f"Failed to compute {metric_name}: {e}")

        # Run test cases if suite provided
        passed_tests = 0
        total_tests = 0

        if suite:
            total_tests = suite.size
            passed_tests = await self._run_test_cases(architecture, suite)

        # Compute overall score
        overall_score = self._compute_overall_score(
            metrics, passed_tests, total_tests
        )

        evaluation_time = (time.time() - start_time) * 1000

        score = ArchitectureScore(
            architecture_id=architecture.id,
            overall_score=overall_score,
            metrics=metrics,
            test_suite_id=suite.id if suite else "",
            evaluation_time_ms=evaluation_time,
            passed_tests=passed_tests,
            total_tests=total_tests
        )

        # Store in history
        if architecture.id not in self._evaluations:
            self._evaluations[architecture.id] = []
        self._evaluations[architecture.id].append(score)

        logger.info(
            f"Evaluated {architecture.id}: score={overall_score:.3f} "
            f"({passed_tests}/{total_tests} tests)"
        )

        return score

    async def _run_test_cases(
        self,
        architecture: ArchitectureSpec,
        suite: TestSuite
    ) -> int:
        """
        Run test cases on architecture.

        This is a simulation - real implementation would
        execute the architecture on test inputs.
        """
        passed = 0

        for test_case in suite.test_cases:
            # Simulate test execution
            # In real implementation, this would:
            # 1. Build the architecture as executable
            # 2. Run input through architecture
            # 3. Compare output to expected

            # For now, use heuristic based on architecture quality
            quality = self._estimate_architecture_quality(architecture)

            # Random success based on quality
            import random
            if random.random() < quality:
                passed += 1

        return passed

    def _estimate_architecture_quality(
        self,
        architecture: ArchitectureSpec
    ) -> float:
        """
        Estimate architecture quality heuristically.

        Returns value in [0, 1].
        """
        quality = 0.5  # Base quality

        # More nodes = potentially more capability
        quality += min(0.2, architecture.node_count * 0.02)

        # More connections = better information flow
        quality += min(0.2, architecture.connection_count * 0.01)

        # Check for variety in operations
        operations = set(n.operation for n in architecture.nodes)
        quality += min(0.1, len(operations) * 0.02)

        return min(1.0, quality)

    def _compute_complexity(self, architecture: ArchitectureSpec) -> float:
        """Compute architecture complexity (lower is better)."""
        # Based on node count and connection count
        complexity = (
            architecture.node_count * 0.1 +
            architecture.connection_count * 0.05
        )
        # Normalize to [0, 1] where lower is better
        return min(1.0, complexity / 10.0)

    def _compute_efficiency(self, architecture: ArchitectureSpec) -> float:
        """Compute architecture efficiency (higher is better)."""
        if architecture.node_count == 0:
            return 0.0

        # Ratio of connections to nodes
        ratio = architecture.connection_count / architecture.node_count

        # Optimal ratio is around 1.5-2.0
        if ratio < 1.0:
            return ratio  # Under-connected
        elif ratio <= 2.0:
            return 1.0  # Optimal
        else:
            return max(0.0, 1.0 - (ratio - 2.0) * 0.2)  # Over-connected

    def _compute_connectivity(self, architecture: ArchitectureSpec) -> float:
        """Compute connectivity score (higher is better)."""
        if architecture.node_count <= 1:
            return 0.0

        # Maximum possible connections
        max_connections = architecture.node_count * (architecture.node_count - 1)

        return architecture.connection_count / max_connections

    def _compute_depth(self, architecture: ArchitectureSpec) -> float:
        """Compute depth score based on path length (moderate is better)."""
        # Estimate depth from input to output
        # Simplified: assume sequential path

        if architecture.node_count <= 2:
            return 0.5

        # Depth relative to node count
        estimated_depth = architecture.node_count - 2  # Excluding input/output

        # Optimal depth is around 3-5
        if estimated_depth < 3:
            return 0.5 + estimated_depth * 0.1
        elif estimated_depth <= 5:
            return 1.0
        else:
            return max(0.5, 1.0 - (estimated_depth - 5) * 0.1)

    def _compute_overall_score(
        self,
        metrics: List[EvaluationMetric],
        passed_tests: int,
        total_tests: int
    ) -> float:
        """Compute weighted overall score."""
        if not metrics and total_tests == 0:
            return 0.0

        score = 0.0
        total_weight = 0.0

        # Weight from metrics
        for metric in metrics:
            if metric.higher_is_better:
                score += metric.value * metric.weight
            else:
                score += (1.0 - metric.value) * metric.weight
            total_weight += metric.weight

        # Weight from test pass rate
        if total_tests > 0:
            test_score = passed_tests / total_tests
            test_weight = 2.0  # Tests are important
            score += test_score * test_weight
            total_weight += test_weight

        return score / total_weight if total_weight > 0 else 0.0

    def get_best_architectures(
        self,
        top_n: int = 10
    ) -> List[tuple[str, float]]:
        """
        Get top architectures by score.

        Returns:
            List of (architecture_id, best_score) tuples
        """
        best_scores = {}

        for arch_id, scores in self._evaluations.items():
            if scores:
                best = max(s.overall_score for s in scores)
                best_scores[arch_id] = best

        sorted_archs = sorted(
            best_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_archs[:top_n]

    def get_evaluation_history(
        self,
        architecture_id: str
    ) -> List[ArchitectureScore]:
        """Get evaluation history for an architecture."""
        return self._evaluations.get(architecture_id, [])

    def create_default_test_suite(self) -> TestSuite:
        """Create a default test suite for basic evaluation."""
        test_cases = []

        for i in range(10):
            test_cases.append(TestCase(
                id=f"test_{i}",
                name=f"Basic Test {i}",
                input_data={"value": i},
                expected_output={"result": i * 2}
            ))

        suite = TestSuite(
            id="default_suite",
            name="Default Test Suite",
            test_cases=test_cases
        )

        self.register_test_suite(suite)

        return suite

    def get_stats(self) -> Dict:
        """Get evaluator statistics."""
        return {
            'total_evaluations': self._total_evaluations,
            'architectures_evaluated': len(self._evaluations),
            'test_suites': len(self._test_suites),
            'metrics_available': list(self._metric_functions.keys())
        }

    def reset(self) -> None:
        """Reset evaluator state."""
        self._test_suites.clear()
        self._evaluations.clear()
        self._total_evaluations = 0
        logger.info("ArchitectureEvaluator reset")
