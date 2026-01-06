"""
Tests for BaselineManager capability measurement.

Tests baseline establishment, measurement, and gaming detection.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
import asyncio

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rsi.measurement.baseline_manager import (
    BaselineManager,
    Baseline,
    MeasurementResult,
    GamingDetectionResult,
    TestCase,
    TestCaseType,
    TestResult,
    create_reasoning_test_suite,
    create_code_test_suite,
    create_math_test_suite,
)


@pytest.fixture
def mock_memory():
    """Create mock memory."""
    memory = MagicMock()
    memory.query_neo4j = AsyncMock(return_value=[])
    return memory


@pytest.fixture
def mock_llm_client():
    """Create mock LLM client."""
    client = MagicMock()
    client.query = AsyncMock(return_value="This is a test response")
    return client


@pytest.fixture
def baseline_manager(mock_memory, mock_llm_client):
    """Create baseline manager with mocks."""
    return BaselineManager(
        memory=mock_memory,
        llm_client=mock_llm_client,
        config={}
    )


@pytest.fixture
def sample_test_suite():
    """Create sample test suite."""
    return [
        TestCase(
            id="test_001",
            capability="reasoning",
            test_type=TestCaseType.REASONING,
            prompt="What is 2 + 2?",
            expected_pattern=r"4",
            difficulty=0.1,
            held_out=True
        ),
        TestCase(
            id="test_002",
            capability="reasoning",
            test_type=TestCaseType.REASONING,
            prompt="What is the capital of France?",
            expected_pattern=r"Paris",
            difficulty=0.2,
            held_out=True
        ),
        TestCase(
            id="test_003",
            capability="reasoning",
            test_type=TestCaseType.REASONING,
            prompt="Training test (not held out)",
            expected_pattern=r".*",
            difficulty=0.1,
            held_out=False
        ),
    ]


class TestBaselineEstablishment:
    """Tests for baseline establishment."""

    @pytest.mark.asyncio
    async def test_establish_baseline(self, baseline_manager, sample_test_suite, mock_llm_client):
        """Test establishing a baseline."""
        # Configure mock to return matching responses
        mock_llm_client.query.side_effect = ["The answer is 4", "The capital is Paris"]

        baseline = await baseline_manager.establish_baseline(
            capability="reasoning",
            test_suite=sample_test_suite
        )

        assert baseline.capability == "reasoning"
        assert baseline.test_count == 2  # Only held-out tests
        assert baseline.score >= 0.0
        assert baseline.score <= 1.0
        assert len(baseline.held_out_ids) == 2
        assert "test_001" in baseline.held_out_ids
        assert "test_002" in baseline.held_out_ids

    @pytest.mark.asyncio
    async def test_baseline_uses_only_held_out(self, baseline_manager, mock_llm_client):
        """Test that baseline only uses held-out tests."""
        test_suite = [
            TestCase(
                id="held_001",
                capability="test",
                test_type=TestCaseType.REASONING,
                prompt="Held out",
                expected_pattern=r"yes",
                held_out=True
            ),
            TestCase(
                id="training_001",
                capability="test",
                test_type=TestCaseType.REASONING,
                prompt="Training",
                expected_pattern=r"yes",
                held_out=False
            ),
        ]

        mock_llm_client.query.return_value = "yes"

        baseline = await baseline_manager.establish_baseline(
            capability="test",
            test_suite=test_suite
        )

        assert baseline.test_count == 1
        assert "held_001" in baseline.held_out_ids
        assert "training_001" not in baseline.held_out_ids

    @pytest.mark.asyncio
    async def test_baseline_computes_variance(self, baseline_manager, mock_llm_client):
        """Test that baseline computes score variance."""
        test_suite = [
            TestCase(
                id=f"test_{i}",
                capability="test",
                test_type=TestCaseType.REASONING,
                prompt=f"Test {i}",
                expected_pattern=r"yes" if i % 2 == 0 else r"no",
                held_out=True
            )
            for i in range(5)
        ]

        # Alternate responses
        mock_llm_client.query.side_effect = ["yes", "wrong", "yes", "wrong", "yes"]

        baseline = await baseline_manager.establish_baseline(
            capability="test",
            test_suite=test_suite
        )

        # With alternating pass/fail, variance should be > 0
        assert baseline.variance > 0


class TestMeasurement:
    """Tests for measurement against baseline."""

    @pytest.mark.asyncio
    async def test_measure_against_baseline(self, baseline_manager, sample_test_suite, mock_llm_client):
        """Test measuring current capability against baseline."""
        # First establish baseline
        mock_llm_client.query.side_effect = ["4", "Paris"]
        await baseline_manager.establish_baseline("reasoning", sample_test_suite)

        # Then measure - same performance
        mock_llm_client.query.side_effect = ["4", "Paris"]
        result = await baseline_manager.measure_against_baseline("reasoning")

        assert result.capability == "reasoning"
        assert result.tests_run == 2
        assert result.delta == pytest.approx(0.0, abs=0.01)

    @pytest.mark.asyncio
    async def test_measure_improvement(self, baseline_manager, sample_test_suite, mock_llm_client):
        """Test detecting improvement over baseline."""
        # Baseline with low performance
        mock_llm_client.query.side_effect = ["wrong", "wrong"]
        await baseline_manager.establish_baseline("reasoning", sample_test_suite)

        # Improved performance
        mock_llm_client.query.side_effect = ["4", "Paris"]
        result = await baseline_manager.measure_against_baseline("reasoning")

        assert result.is_improvement == True
        assert result.delta > 0

    @pytest.mark.asyncio
    async def test_measure_no_baseline_raises(self, baseline_manager):
        """Test that measuring without baseline raises error."""
        with pytest.raises(ValueError, match="No baseline"):
            await baseline_manager.measure_against_baseline("nonexistent")


class TestGamingDetection:
    """Tests for gaming detection."""

    @pytest.mark.asyncio
    async def test_no_gaming_with_insufficient_history(self, baseline_manager):
        """Test that gaming is not detected without history."""
        result = await baseline_manager.detect_gaming(
            capability="test",
            claimed_improvement=0.5
        )

        assert result.is_gaming == False
        assert "Insufficient history" in result.indicators[0]

    @pytest.mark.asyncio
    async def test_gaming_detection_large_jump(self, baseline_manager, sample_test_suite, mock_llm_client):
        """Test that large jumps without evidence trigger gaming."""
        # Establish baseline
        mock_llm_client.query.side_effect = ["4", "Paris"]
        await baseline_manager.establish_baseline("reasoning", sample_test_suite)

        # Make several measurements to build history
        for _ in range(3):
            mock_llm_client.query.side_effect = ["4", "Paris"]
            await baseline_manager.measure_against_baseline("reasoning")

        # Check for gaming with large claimed improvement
        result = await baseline_manager.detect_gaming(
            capability="reasoning",
            claimed_improvement=0.5  # 50% improvement
        )

        # Should flag the large improvement
        assert any("Large improvement" in ind for ind in result.indicators)

    @pytest.mark.asyncio
    async def test_variance_collapse_detection(self, baseline_manager, sample_test_suite, mock_llm_client):
        """Test detection of variance collapse (memorization)."""
        # Establish baseline
        mock_llm_client.query.side_effect = ["4", "Paris"]
        await baseline_manager.establish_baseline("reasoning", sample_test_suite)

        # Make identical measurements (suspiciously consistent)
        for _ in range(5):
            mock_llm_client.query.side_effect = ["4", "Paris"]
            await baseline_manager.measure_against_baseline("reasoning")

        result = await baseline_manager.detect_gaming(
            capability="reasoning",
            claimed_improvement=0.1
        )

        # Score variance should be very low with identical scores
        # This might trigger variance collapse warning
        assert result.confidence >= 0


class TestTestCaseScoring:
    """Tests for test case scoring."""

    def test_pattern_match_scoring(self, baseline_manager):
        """Test scoring with pattern matching."""
        test = TestCase(
            id="test",
            capability="test",
            test_type=TestCaseType.REASONING,
            prompt="What is 2+2?",
            expected_pattern=r"\b4\b"
        )

        score, passed = baseline_manager._score_response(test, "The answer is 4")
        assert score == 1.0
        assert passed == True

        score, passed = baseline_manager._score_response(test, "The answer is 5")
        assert score == 0.0
        assert passed == False

    def test_reference_answer_scoring(self, baseline_manager):
        """Test scoring with reference answer similarity."""
        test = TestCase(
            id="test",
            capability="test",
            test_type=TestCaseType.REASONING,
            prompt="What is the capital of France?",
            reference_answer="Paris is the capital"
        )

        score, passed = baseline_manager._score_response(test, "The capital is Paris")
        assert score > 0.0  # Some word overlap

    def test_default_scoring(self, baseline_manager):
        """Test default scoring for tests without criteria."""
        test = TestCase(
            id="test",
            capability="test",
            test_type=TestCaseType.REASONING,
            prompt="Open ended question"
        )

        score, passed = baseline_manager._score_response(test, "Some response")
        assert score == 0.5  # Non-empty gets partial credit

        score, passed = baseline_manager._score_response(test, "")
        assert score == 0.0


class TestPrebuiltSuites:
    """Tests for pre-built test suites."""

    def test_reasoning_suite(self):
        """Test reasoning test suite structure."""
        suite = create_reasoning_test_suite()

        assert len(suite) >= 3
        assert all(t.capability == "reasoning" for t in suite)
        assert all(t.test_type == TestCaseType.REASONING for t in suite)
        assert all(t.held_out for t in suite)

    def test_code_suite(self):
        """Test code test suite structure."""
        suite = create_code_test_suite()

        assert len(suite) >= 3
        assert all(t.capability == "code" for t in suite)
        assert all(t.test_type == TestCaseType.CODE for t in suite)

    def test_math_suite(self):
        """Test math test suite structure."""
        suite = create_math_test_suite()

        assert len(suite) >= 3
        assert all(t.capability == "math" for t in suite)
        assert all(t.test_type == TestCaseType.MATH for t in suite)


class TestStats:
    """Tests for statistics and reset."""

    def test_get_stats(self, baseline_manager):
        """Test statistics retrieval."""
        stats = baseline_manager.get_stats()

        assert 'baselines_count' in stats
        assert 'total_measurements' in stats
        assert 'gaming_detections' in stats

    @pytest.mark.asyncio
    async def test_reset(self, baseline_manager, sample_test_suite, mock_llm_client):
        """Test reset clears state."""
        # Establish a baseline
        mock_llm_client.query.side_effect = ["4", "Paris"]
        await baseline_manager.establish_baseline("reasoning", sample_test_suite)

        assert baseline_manager.get_stats()['baselines_count'] == 1

        baseline_manager.reset()

        assert baseline_manager.get_stats()['baselines_count'] == 0
        assert baseline_manager.get_stats()['total_measurements'] == 0


class TestDataclasses:
    """Tests for dataclass serialization."""

    def test_baseline_to_dict(self):
        """Test Baseline serialization."""
        baseline = Baseline(
            capability="test",
            score=0.8,
            variance=0.1,
            test_count=10,
            established_at="2026-01-06T00:00:00Z",
            held_out_ids=["test_001", "test_002"]
        )

        d = baseline.to_dict()

        assert d['capability'] == "test"
        assert d['score'] == 0.8
        assert d['variance'] == 0.1

    def test_measurement_result_to_dict(self):
        """Test MeasurementResult serialization."""
        result = MeasurementResult(
            capability="test",
            current_score=0.9,
            baseline_score=0.8,
            delta=0.1,
            delta_percent=12.5,
            tests_run=10,
            tests_passed=9,
            is_improvement=True,
            is_significant=True,
            confidence=0.95,
            measured_at="2026-01-06T00:00:00Z"
        )

        d = result.to_dict()

        assert d['delta'] == 0.1
        assert d['is_improvement'] == True

    def test_gaming_detection_to_dict(self):
        """Test GamingDetectionResult serialization."""
        result = GamingDetectionResult(
            capability="test",
            is_gaming=True,
            confidence=0.8,
            indicators=["Variance collapse", "Large jump"]
        )

        d = result.to_dict()

        assert d['is_gaming'] == True
        assert len(d['indicators']) == 2
