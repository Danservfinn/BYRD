"""
RSI Hypothesis Tests - Statistical validation of core hypotheses.

Validates:
- H1: Activation rate ≥ 50% (dispositional seeding increases emergence)
- H2: Direction variance > 0 (diversity despite common disposition)
- H3: Growth rate positive (capabilities improve over time)
- H6: Heuristic transfer ≥ 15% improvement (crystallized knowledge helps)
- H7: Evolved prompts outperform static (learning compounds)
- H8: Test pass rate ≥ 80% (oracle constraint maintains quality)

These tests determine whether the RSI loop is working as designed.
Phase gate to Gastown requires H1, H6, H7 to pass.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from .metrics import RSIMetrics

logger = logging.getLogger("rsi.measurement.hypothesis_tests")


@dataclass
class TestResult:
    """Result of a single hypothesis test."""
    hypothesis: str
    description: str
    passed: bool
    value: float
    threshold: float
    margin: float  # How much above/below threshold
    tested_at: str

    def to_dict(self) -> Dict:
        return {
            "hypothesis": self.hypothesis,
            "description": self.description,
            "passed": self.passed,
            "value": round(self.value, 4),
            "threshold": self.threshold,
            "margin": round(self.margin, 4),
            "tested_at": self.tested_at
        }


@dataclass
class ValidationReport:
    """Complete validation report for all hypotheses."""
    tests: List[TestResult]
    phase_gate_passed: bool
    gate_criteria: Dict[str, bool]
    generated_at: str
    total_cycles: int

    def to_dict(self) -> Dict:
        return {
            "tests": [t.to_dict() for t in self.tests],
            "phase_gate_passed": self.phase_gate_passed,
            "gate_criteria": self.gate_criteria,
            "generated_at": self.generated_at,
            "total_cycles": self.total_cycles,
            "summary": {
                "passed": sum(1 for t in self.tests if t.passed),
                "failed": sum(1 for t in self.tests if not t.passed),
                "total": len(self.tests)
            }
        }


class HypothesisValidator:
    """
    Validates RSI hypotheses against collected metrics.

    Phase Gate Criteria (for Gastown):
    - H1 validated: Activation rate ≥ 50%
    - H6 validated: Heuristic transfer positive (≥ 15% improvement)
    - H7 validated: Evolved prompts outperform static
    - Complete cycles: ≥ 3 full loops
    - Stability: No critical bugs for 1 week
    """

    # Hypothesis thresholds
    H1_ACTIVATION_THRESHOLD = 0.50
    H2_VARIANCE_THRESHOLD = 0.0  # Just needs to be positive
    H3_GROWTH_THRESHOLD = 0.0  # Just needs to be positive
    H6_TRANSFER_THRESHOLD = 0.15
    H7_EVOLUTION_THRESHOLD = 0.0  # Evolved > static
    H8_QUALITY_THRESHOLD = 0.80

    # Phase gate requirements
    MIN_COMPLETE_CYCLES = 3

    def __init__(self, metrics_collector):
        """
        Initialize hypothesis validator.

        Args:
            metrics_collector: MetricsCollector instance
        """
        self.metrics = metrics_collector

        # Baseline storage for before/after comparisons
        self._baseline_scores: Dict[str, float] = {}
        self._static_prompt_scores: Dict[str, float] = {}

    async def run_all_tests(self) -> ValidationReport:
        """
        Run all hypothesis tests.

        Returns:
            ValidationReport with all test results
        """
        rsi_metrics = await self.metrics.compute_metrics()
        tests = []

        # H1: Activation Rate
        tests.append(self._test_h1_activation(rsi_metrics))

        # H2: Direction Variance
        tests.append(self._test_h2_variance(rsi_metrics))

        # H3: Growth Rate (requires baseline comparison)
        tests.append(await self._test_h3_growth())

        # H6: Heuristic Transfer
        tests.append(await self._test_h6_transfer())

        # H7: Evolved vs Static
        tests.append(await self._test_h7_evolution())

        # H8: Quality (Test Pass Rate)
        tests.append(self._test_h8_quality(rsi_metrics))

        # Check phase gate criteria
        gate_criteria = {
            "H1": any(t.passed for t in tests if t.hypothesis == "H1"),
            "H6": any(t.passed for t in tests if t.hypothesis == "H6"),
            "H7": any(t.passed for t in tests if t.hypothesis == "H7"),
            "complete_cycles": rsi_metrics.complete_cycles >= self.MIN_COMPLETE_CYCLES
        }
        phase_gate_passed = all(gate_criteria.values())

        return ValidationReport(
            tests=tests,
            phase_gate_passed=phase_gate_passed,
            gate_criteria=gate_criteria,
            generated_at=datetime.now().isoformat(),
            total_cycles=rsi_metrics.total_reflections
        )

    def _test_h1_activation(self, metrics: RSIMetrics) -> TestResult:
        """
        H1: Dispositional seeding increases RSI activation.

        Threshold: Activation rate ≥ 50%
        Activation = emergent_desires / total_reflections
        """
        value = metrics.activation_rate
        threshold = self.H1_ACTIVATION_THRESHOLD
        passed = value >= threshold

        return TestResult(
            hypothesis="H1",
            description="Dispositional seeding increases RSI activation (≥50%)",
            passed=passed,
            value=value,
            threshold=threshold,
            margin=value - threshold,
            tested_at=datetime.now().isoformat()
        )

    def _test_h2_variance(self, metrics: RSIMetrics) -> TestResult:
        """
        H2: Improvement directions are diverse despite common disposition.

        Threshold: Direction variance > 0 (entropy-based)
        """
        value = metrics.direction_variance
        threshold = self.H2_VARIANCE_THRESHOLD
        passed = value > threshold

        return TestResult(
            hypothesis="H2",
            description="Improvement directions are diverse (variance > 0)",
            passed=passed,
            value=value,
            threshold=threshold,
            margin=value - threshold,
            tested_at=datetime.now().isoformat()
        )

    async def _test_h3_growth(self) -> TestResult:
        """
        H3: Capabilities improve over time.

        Threshold: Growth rate > 0
        Requires baseline scores to be set.
        """
        # If no baseline, test is inconclusive
        if not self._baseline_scores:
            return TestResult(
                hypothesis="H3",
                description="Capabilities improve over time (growth > 0)",
                passed=False,
                value=0.0,
                threshold=self.H3_GROWTH_THRESHOLD,
                margin=0.0,
                tested_at=datetime.now().isoformat()
            )

        # Compute average growth across tracked capabilities
        current_scores = await self._get_current_capability_scores()
        growths = []

        for cap, baseline in self._baseline_scores.items():
            if cap in current_scores and baseline > 0:
                growth = (current_scores[cap] - baseline) / baseline
                growths.append(growth)

        avg_growth = sum(growths) / len(growths) if growths else 0.0
        threshold = self.H3_GROWTH_THRESHOLD
        passed = avg_growth > threshold

        return TestResult(
            hypothesis="H3",
            description="Capabilities improve over time (growth > 0)",
            passed=passed,
            value=avg_growth,
            threshold=threshold,
            margin=avg_growth - threshold,
            tested_at=datetime.now().isoformat()
        )

    async def _test_h6_transfer(self) -> TestResult:
        """
        H6: Crystallized heuristics improve novel problem performance.

        Threshold: ≥15% improvement after heuristic applied
        Requires before/after comparison.
        """
        # Get stored before/after if available
        before = self._baseline_scores.get("pre_heuristic", 0.0)
        after = self._baseline_scores.get("post_heuristic", 0.0)

        if before == 0.0:
            # No data yet - test inconclusive
            return TestResult(
                hypothesis="H6",
                description="Heuristic transfer improves performance (≥15%)",
                passed=False,
                value=0.0,
                threshold=self.H6_TRANSFER_THRESHOLD,
                margin=-self.H6_TRANSFER_THRESHOLD,
                tested_at=datetime.now().isoformat()
            )

        improvement = (after - before) / max(before, 0.01)
        threshold = self.H6_TRANSFER_THRESHOLD
        passed = improvement >= threshold

        return TestResult(
            hypothesis="H6",
            description="Heuristic transfer improves performance (≥15%)",
            passed=passed,
            value=improvement,
            threshold=threshold,
            margin=improvement - threshold,
            tested_at=datetime.now().isoformat()
        )

    async def _test_h7_evolution(self) -> TestResult:
        """
        H7: Evolved prompts outperform static prompts.

        Threshold: Evolved score > Static score
        Requires comparison with static baseline.
        """
        static_score = self._static_prompt_scores.get("average", 0.0)
        current_scores = await self._get_current_capability_scores()
        evolved_score = sum(current_scores.values()) / len(current_scores) if current_scores else 0.0

        if static_score == 0.0:
            # No static baseline - test inconclusive
            return TestResult(
                hypothesis="H7",
                description="Evolved prompts outperform static",
                passed=False,
                value=0.0,
                threshold=self.H7_EVOLUTION_THRESHOLD,
                margin=0.0,
                tested_at=datetime.now().isoformat()
            )

        improvement = evolved_score - static_score
        passed = improvement > self.H7_EVOLUTION_THRESHOLD

        return TestResult(
            hypothesis="H7",
            description="Evolved prompts outperform static",
            passed=passed,
            value=improvement,
            threshold=self.H7_EVOLUTION_THRESHOLD,
            margin=improvement - self.H7_EVOLUTION_THRESHOLD,
            tested_at=datetime.now().isoformat()
        )

    def _test_h8_quality(self, metrics: RSIMetrics) -> TestResult:
        """
        H8: Oracle constraint maintains quality (test pass rate ≥ 80%).

        This ensures we're not learning from incorrect solutions.
        """
        value = metrics.test_pass_rate
        threshold = self.H8_QUALITY_THRESHOLD
        passed = value >= threshold

        return TestResult(
            hypothesis="H8",
            description="Oracle constraint maintains quality (≥80% pass rate)",
            passed=passed,
            value=value,
            threshold=threshold,
            margin=value - threshold,
            tested_at=datetime.now().isoformat()
        )

    async def _get_current_capability_scores(self) -> Dict[str, float]:
        """Get current capability scores from metrics."""
        try:
            # This would query stored capability scores
            # For now, use trajectory success rate as proxy
            metrics = await self.metrics.compute_metrics()
            return {
                "overall": metrics.trajectory_success_rate,
                "code": metrics.trajectory_success_rate,
                "math": metrics.trajectory_success_rate,
                "logic": metrics.trajectory_success_rate
            }
        except Exception as e:
            logger.warning(f"Failed to get capability scores: {e}")
            return {}

    def set_baseline(self, capability: str, score: float):
        """
        Set baseline score for growth comparison.

        Call this before running validation to establish baseline.
        """
        self._baseline_scores[capability] = score
        logger.info(f"Set baseline for {capability}: {score}")

    def set_static_baseline(self, score: float):
        """
        Set static prompt baseline for evolution comparison.

        This should be the average performance with a non-evolving prompt.
        """
        self._static_prompt_scores["average"] = score
        logger.info(f"Set static prompt baseline: {score}")

    def record_heuristic_transfer(self, before: float, after: float):
        """
        Record before/after scores for heuristic transfer test.

        Call before applying a new heuristic and after testing with it.
        """
        self._baseline_scores["pre_heuristic"] = before
        self._baseline_scores["post_heuristic"] = after
        logger.info(f"Recorded heuristic transfer: {before} -> {after}")

    def get_phase_gate_status(self) -> Dict[str, Any]:
        """Get current phase gate status without running tests."""
        return {
            "baselines_set": len(self._baseline_scores) > 0,
            "static_baseline_set": len(self._static_prompt_scores) > 0,
            "requirements": {
                "H1": "Activation ≥ 50%",
                "H6": "Heuristic transfer ≥ 15%",
                "H7": "Evolved > static",
                "complete_cycles": f"≥ {self.MIN_COMPLETE_CYCLES} cycles"
            }
        }


async def run_validation(metrics_collector) -> ValidationReport:
    """
    Convenience function to run full validation.

    Args:
        metrics_collector: MetricsCollector instance

    Returns:
        ValidationReport with all results
    """
    validator = HypothesisValidator(metrics_collector)
    return await validator.run_all_tests()
