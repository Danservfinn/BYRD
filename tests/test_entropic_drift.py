"""
Tests for the Entropic Drift Detection module.

Entropic drift detection monitors for signs that the RSI system is converging
on narrow solutions or losing diversity, which would indicate approaching the
improvement ceiling.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from rsi.verification.entropic_drift import (
    EntropicDriftMonitor,
    DriftSeverity,
    DriftType,
    DriftSignal,
    DriftReport,
    SolutionDiversityTracker,
    BenchmarkTracker,
    StrategyEntropyTracker,
)


class TestDriftSeverity:
    """Test DriftSeverity enum."""

    def test_all_severities_defined(self):
        """Test all severity levels are defined."""
        assert DriftSeverity.NONE is not None
        assert DriftSeverity.MINOR is not None
        assert DriftSeverity.MODERATE is not None
        assert DriftSeverity.SEVERE is not None
        assert DriftSeverity.CRITICAL is not None

    def test_severity_ordering(self):
        """Test that severities can be compared."""
        assert DriftSeverity.NONE.value < DriftSeverity.MINOR.value
        assert DriftSeverity.MINOR.value < DriftSeverity.MODERATE.value
        assert DriftSeverity.MODERATE.value < DriftSeverity.SEVERE.value
        assert DriftSeverity.SEVERE.value < DriftSeverity.CRITICAL.value


class TestDriftReport:
    """Test DriftReport dataclass."""

    def test_report_creation(self):
        """Test creating a drift report."""
        report = DriftReport(
            timestamp=datetime.now(),
            overall_severity=DriftSeverity.MINOR,
            solution_diversity=0.75,
            benchmark_trend=0.85,
            strategy_entropy=0.68,
            generalization_gap=0.12,
            recommendations=["Monitor diversity"],
        )
        assert report.overall_severity == DriftSeverity.MINOR
        assert len(report.recommendations) == 1

    def test_report_with_no_recommendations(self):
        """Test report with empty recommendations."""
        report = DriftReport(
            timestamp=datetime.now(),
            overall_severity=DriftSeverity.NONE,
            solution_diversity=0.9,
            benchmark_trend=0.95,
            strategy_entropy=0.8,
            generalization_gap=0.05,
        )
        assert report.recommendations is None or len(report.recommendations) == 0


class TestSolutionDiversityTracker:
    """Test SolutionDiversityTracker."""

    @pytest.fixture
    def tracker(self):
        return SolutionDiversityTracker()

    def test_initial_diversity(self, tracker):
        """Test initial diversity state."""
        score = tracker.get_diversity_score()
        assert 0.0 <= score <= 1.0

    def test_record_solution(self, tracker):
        """Test recording a solution."""
        tracker.record_solution(
            solution_id="sol_001",
            features={"approach": "iterative", "complexity": "low"},
        )
        assert tracker.solution_count >= 1

    def test_diversity_decreases_with_similar_solutions(self, tracker):
        """Test that diversity decreases with similar solutions."""
        initial_score = tracker.get_diversity_score()

        # Add many similar solutions
        for i in range(10):
            tracker.record_solution(
                solution_id=f"sol_{i}",
                features={"approach": "same", "method": "identical"},
            )

        final_score = tracker.get_diversity_score()
        assert final_score <= initial_score

    def test_diversity_maintained_with_varied_solutions(self, tracker):
        """Test that diversity is maintained with varied solutions."""
        approaches = ["iterative", "recursive", "dynamic", "greedy", "divide-conquer"]

        for i, approach in enumerate(approaches):
            tracker.record_solution(
                solution_id=f"sol_{i}",
                features={"approach": approach, "unique": str(i)},
            )

        score = tracker.get_diversity_score()
        assert score > 0.5  # Good diversity maintained


class TestBenchmarkTracker:
    """Test BenchmarkTracker."""

    @pytest.fixture
    def tracker(self):
        return BenchmarkTracker()

    def test_record_benchmark(self, tracker):
        """Test recording benchmark results."""
        tracker.record_benchmark(
            benchmark_id="bench_001",
            score=0.85,
            domain="code",
        )
        assert tracker.benchmark_count >= 1

    def test_detect_decline(self, tracker):
        """Test detecting benchmark decline."""
        # Record declining scores
        scores = [0.9, 0.88, 0.85, 0.82, 0.78, 0.75]
        for i, score in enumerate(scores):
            tracker.record_benchmark(
                benchmark_id=f"bench_{i}",
                score=score,
                domain="code",
            )

        trend = tracker.get_trend()
        assert trend < 0  # Negative trend indicates decline

    def test_detect_improvement(self, tracker):
        """Test detecting benchmark improvement."""
        # Record improving scores
        scores = [0.7, 0.75, 0.78, 0.82, 0.85, 0.88]
        for i, score in enumerate(scores):
            tracker.record_benchmark(
                benchmark_id=f"bench_{i}",
                score=score,
                domain="code",
            )

        trend = tracker.get_trend()
        assert trend > 0  # Positive trend indicates improvement

    def test_get_benchmark_score(self, tracker):
        """Test getting overall benchmark score."""
        tracker.record_benchmark("b1", 0.8, "code")
        tracker.record_benchmark("b2", 0.9, "code")

        score = tracker.get_benchmark_score()
        assert 0.0 <= score <= 1.0


class TestStrategyEntropyTracker:
    """Test StrategyEntropyTracker."""

    @pytest.fixture
    def tracker(self):
        return StrategyEntropyTracker()

    def test_record_strategy_usage(self, tracker):
        """Test recording strategy usage."""
        tracker.record_usage(strategy_id="strat_001")
        assert tracker.total_usages >= 1

    def test_entropy_high_with_even_distribution(self, tracker):
        """Test that entropy is high with even strategy distribution."""
        strategies = ["a", "b", "c", "d", "e"]
        for _ in range(10):
            for strat in strategies:
                tracker.record_usage(strat)

        entropy = tracker.get_entropy()
        assert entropy > 0.7  # High entropy with even distribution

    def test_entropy_low_with_single_strategy(self, tracker):
        """Test that entropy is low when one strategy dominates."""
        # Use one strategy many times
        for _ in range(100):
            tracker.record_usage("dominant")

        # Use others rarely
        tracker.record_usage("rare1")
        tracker.record_usage("rare2")

        entropy = tracker.get_entropy()
        assert entropy < 0.5  # Low entropy with dominant strategy


class TestGeneralizationGapTracker:
    """Test GeneralizationGapTracker."""

    @pytest.fixture
    def tracker(self):
        return GeneralizationGapTracker()

    def test_record_performance(self, tracker):
        """Test recording train/test performance."""
        tracker.record_performance(
            train_score=0.95,
            test_score=0.85,
            domain="code",
        )
        assert tracker.sample_count >= 1

    def test_detect_overfitting(self, tracker):
        """Test detecting overfitting (large gap)."""
        # Record performances with large train/test gap
        for _ in range(10):
            tracker.record_performance(
                train_score=0.98,
                test_score=0.65,
                domain="code",
            )

        gap = tracker.get_generalization_gap()
        assert gap > 0.2  # Significant overfitting

    def test_good_generalization(self, tracker):
        """Test detecting good generalization."""
        # Record performances with small train/test gap
        for _ in range(10):
            tracker.record_performance(
                train_score=0.88,
                test_score=0.85,
                domain="code",
            )

        gap = tracker.get_generalization_gap()
        assert gap < 0.1  # Good generalization


class TestEntropicDriftMonitor:
    """Test the main EntropicDriftMonitor class."""

    @pytest.fixture
    def monitor(self):
        return EntropicDriftMonitor()

    def test_has_all_trackers(self, monitor):
        """Test that monitor has all required trackers."""
        assert monitor.diversity_tracker is not None
        assert monitor.benchmark_tracker is not None
        assert monitor.entropy_tracker is not None
        assert monitor.gap_tracker is not None

    @pytest.mark.asyncio
    async def test_analyze_returns_report(self, monitor):
        """Test that analyze returns a DriftReport."""
        report = await monitor.analyze()
        assert isinstance(report, DriftReport)

    @pytest.mark.asyncio
    async def test_report_includes_all_metrics(self, monitor):
        """Test that report includes all metrics."""
        report = await monitor.analyze()

        assert report.solution_diversity is not None
        assert report.benchmark_trend is not None
        assert report.strategy_entropy is not None
        assert report.generalization_gap is not None

    @pytest.mark.asyncio
    async def test_severity_calculation(self, monitor):
        """Test that severity is calculated correctly."""
        report = await monitor.analyze()
        assert isinstance(report.overall_severity, DriftSeverity)

    @pytest.mark.asyncio
    async def test_generates_recommendations(self, monitor):
        """Test that recommendations are generated for issues."""
        # Inject some concerning metrics
        for _ in range(20):
            monitor.diversity_tracker.record_solution(
                solution_id=f"same_{_}",
                features={"approach": "identical"},
            )

        report = await monitor.analyze()
        # Should have recommendations due to low diversity
        if report.solution_diversity < 0.5:
            assert len(report.recommendations) > 0


class TestMonitorWithMocks:
    """Test monitor with mocked trackers."""

    @pytest.mark.asyncio
    async def test_critical_severity_detection(self):
        """Test detecting critical severity."""
        monitor = EntropicDriftMonitor()

        # Mock all trackers to return concerning values
        monitor.diversity_tracker.get_diversity_score = MagicMock(return_value=0.1)
        monitor.benchmark_tracker.get_benchmark_score = MagicMock(return_value=0.3)
        monitor.entropy_tracker.get_entropy = MagicMock(return_value=0.2)
        monitor.gap_tracker.get_generalization_gap = MagicMock(return_value=0.5)

        report = await monitor.analyze()

        # Should detect critical or severe issues
        assert report.overall_severity in [DriftSeverity.SEVERE, DriftSeverity.CRITICAL]

    @pytest.mark.asyncio
    async def test_no_severity_with_healthy_metrics(self):
        """Test no severity with healthy metrics."""
        monitor = EntropicDriftMonitor()

        # Mock all trackers to return healthy values
        monitor.diversity_tracker.get_diversity_score = MagicMock(return_value=0.9)
        monitor.benchmark_tracker.get_benchmark_score = MagicMock(return_value=0.95)
        monitor.entropy_tracker.get_entropy = MagicMock(return_value=0.85)
        monitor.gap_tracker.get_generalization_gap = MagicMock(return_value=0.05)

        report = await monitor.analyze()

        assert report.overall_severity == DriftSeverity.NONE


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_empty_tracker_state(self):
        """Test analysis with no data recorded."""
        monitor = EntropicDriftMonitor()

        # Don't record anything, just analyze
        report = await monitor.analyze()

        assert report is not None
        assert report.overall_severity is not None

    def test_diversity_with_single_solution(self):
        """Test diversity with only one solution."""
        tracker = SolutionDiversityTracker()
        tracker.record_solution("only_one", {"unique": True})

        score = tracker.get_diversity_score()
        assert score is not None

    def test_benchmark_with_single_result(self):
        """Test benchmark with only one result."""
        tracker = BenchmarkTracker()
        tracker.record_benchmark("only_one", 0.8, "code")

        trend = tracker.get_trend()
        assert trend is not None or trend == 0  # No trend with single point

    def test_entropy_with_single_strategy(self):
        """Test entropy with only one strategy used."""
        tracker = StrategyEntropyTracker()
        tracker.record_usage("only_one")

        entropy = tracker.get_entropy()
        assert entropy == 0  # Zero entropy with single strategy
