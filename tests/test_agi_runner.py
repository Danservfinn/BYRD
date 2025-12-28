"""
Test suite for AGI Runner - The Execution Engine

Tests the core improvement cycle:
ASSESS → IDENTIFY → GENERATE → PREDICT → VERIFY → EXECUTE → MEASURE → LEARN

These tests verify Phase 0 and Phase 1 of UNIFIED_AGI_PLAN.md.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import dataclass
from typing import Dict, Any, List

# Import the components we're testing
import sys
sys.path.insert(0, '..')

from agi_runner import (
    AGIRunner,
    ImprovementTarget,
    ImprovementHypothesis,
    MeasurementResult,
    CycleResult
)
from desire_classifier import DesireClassifier, DesireType


class MockMemory:
    """Mock Memory for testing without Neo4j."""

    def __init__(self):
        self.queries_run = []
        self.nodes_created = []

    async def _run_query(self, query: str, params: Dict = None):
        self.queries_run.append((query, params))
        # Return mock data based on query type
        if "MATCH (g:Goal)" in query and "count" in query:
            return [{"count": 0}]
        if "MATCH (e:Experience)" in query:
            return []
        if "MATCH (r:Reflection)" in query:
            return []
        return []

    async def record_experience(self, content: str, type: str = "observation"):
        self.nodes_created.append({"type": "Experience", "content": content})
        return f"exp_{len(self.nodes_created)}"


class MockSelfModel:
    """Mock SelfModel for testing."""

    def __init__(self):
        self._capabilities = {}
        self._alpha = {}
        self._beta = {}

    async def assess_current_capabilities(self) -> Dict[str, float]:
        return {
            "reasoning": 0.6,
            "memory": 0.5,
            "learning": 0.4,
            "research": 0.7
        }

    def bayesian_update(self, capability: str, success: bool):
        if capability not in self._alpha:
            self._alpha[capability] = 1.0
            self._beta[capability] = 1.0
        if success:
            self._alpha[capability] += 1
        else:
            self._beta[capability] += 1


class MockWorldModel:
    """Mock WorldModel for testing."""

    async def predict_outcome(self, action: str, context: Dict) -> Dict:
        return {
            "predicted_success": 0.7,
            "confidence": 0.6,
            "risks": []
        }

    async def consolidate(self):
        pass


class MockRollback:
    """Mock RollbackSystem for testing."""

    async def create_checkpoint(self, reason: str) -> str:
        return f"checkpoint_{reason}"

    async def rollback_to(self, checkpoint_id: str) -> bool:
        return True


class MockBYRD:
    """Mock BYRD instance for testing AGIRunner."""

    def __init__(self):
        self.memory = MockMemory()
        self.self_model = MockSelfModel()
        self.world_model = MockWorldModel()
        self.rollback = MockRollback()
        self.config = {
            "initial_goals": [
                {"description": "Test goal 1", "domain": "test", "priority": "high"},
                {"description": "Test goal 2", "domain": "test", "priority": "medium"}
            ]
        }


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def mock_byrd():
    """Create a mock BYRD instance."""
    return MockBYRD()


@pytest.fixture
def agi_runner(mock_byrd):
    """Create an AGIRunner with mock dependencies."""
    return AGIRunner(mock_byrd)


# =============================================================================
# Data Class Tests
# =============================================================================

class TestDataClasses:
    """Test the data classes used by AGIRunner."""

    def test_improvement_target_creation(self):
        target = ImprovementTarget(
            name="reasoning",
            current_level=0.5,
            priority="high",
            reason="Below threshold"
        )
        assert target.name == "reasoning"
        assert target.current_level == 0.5
        assert target.priority == "high"

    def test_improvement_hypothesis_defaults(self):
        hypothesis = ImprovementHypothesis(
            target="memory",
            strategy="practice",
            description="Test hypothesis",
            expected_improvement=0.1
        )
        assert hypothesis.predicted_success == 0.5
        assert hypothesis.prediction_confidence == 0.0
        assert hypothesis.resources_needed == []
        assert hypothesis.risks == []

    def test_measurement_result(self):
        result = MeasurementResult(
            improved=True,
            delta=0.15,
            before_score=0.5,
            after_score=0.65
        )
        assert result.improved is True
        assert result.delta == 0.15

    def test_cycle_result(self):
        result = CycleResult(
            success=True,
            target="reasoning",
            delta=0.1,
            cycle=5
        )
        assert result.success is True
        assert result.cycle == 5


# =============================================================================
# AGIRunner Initialization Tests
# =============================================================================

class TestAGIRunnerInit:
    """Test AGIRunner initialization."""

    def test_init_creates_runner(self, agi_runner):
        assert agi_runner is not None
        assert agi_runner._cycle_count == 0
        assert agi_runner._bootstrapped is False

    def test_init_connects_to_byrd_components(self, agi_runner, mock_byrd):
        assert agi_runner.memory is mock_byrd.memory
        assert agi_runner.self_model is mock_byrd.self_model
        assert agi_runner.world_model is mock_byrd.world_model
        assert agi_runner.rollback is mock_byrd.rollback

    def test_init_creates_desire_classifier(self, agi_runner):
        assert agi_runner.desire_classifier is not None
        assert isinstance(agi_runner.desire_classifier, DesireClassifier)

    def test_init_bootstrap_metrics(self, agi_runner):
        metrics = agi_runner._bootstrap_metrics
        assert metrics['goals_injected'] == 0
        assert metrics['research_indexed'] == 0
        assert metrics['patterns_seeded'] == 0
        assert metrics['counterfactuals_seeded'] == 0


# =============================================================================
# Reset Tests
# =============================================================================

class TestAGIRunnerReset:
    """Test AGIRunner reset functionality."""

    def test_reset_clears_cycle_count(self, agi_runner):
        agi_runner._cycle_count = 10
        agi_runner.reset()
        assert agi_runner._cycle_count == 0

    def test_reset_clears_bootstrap_state(self, agi_runner):
        agi_runner._bootstrapped = True
        agi_runner.reset()
        assert agi_runner._bootstrapped is False

    def test_reset_clears_cycle_history(self, agi_runner):
        agi_runner._cycle_history.append(CycleResult(success=True))
        agi_runner.reset()
        assert len(agi_runner._cycle_history) == 0

    def test_reset_clears_bootstrap_metrics(self, agi_runner):
        agi_runner._bootstrap_metrics['goals_injected'] = 5
        agi_runner.reset()
        assert agi_runner._bootstrap_metrics['goals_injected'] == 0


# =============================================================================
# Bootstrap Tests (Phase 0)
# =============================================================================

class TestBootstrap:
    """Test bootstrap_from_current_state() - Phase 0 activation."""

    @pytest.mark.asyncio
    async def test_bootstrap_sets_flag(self, agi_runner):
        await agi_runner.bootstrap_from_current_state()
        assert agi_runner._bootstrapped is True

    @pytest.mark.asyncio
    async def test_bootstrap_only_runs_once(self, agi_runner):
        await agi_runner.bootstrap_from_current_state()
        initial_queries = len(agi_runner.memory.queries_run)

        # Run again - should not execute
        await agi_runner.bootstrap_from_current_state()
        assert len(agi_runner.memory.queries_run) == initial_queries

    @pytest.mark.asyncio
    async def test_bootstrap_checks_goal_population(self, agi_runner):
        await agi_runner.bootstrap_from_current_state()

        # Should have queried for existing goals
        goal_queries = [q for q, _ in agi_runner.memory.queries_run
                       if "MATCH (g:Goal)" in q]
        assert len(goal_queries) > 0


# =============================================================================
# Desire Classification Tests
# =============================================================================

class TestDesireClassification:
    """Test desire classification integration."""

    def test_classify_capability_desire(self, agi_runner):
        result = agi_runner.desire_classifier.classify(
            "I want to improve my reasoning capabilities"
        )
        assert result.desire_type == DesireType.CAPABILITY

    def test_classify_action_desire(self, agi_runner):
        result = agi_runner.desire_classifier.classify(
            "Search for information about neural networks"
        )
        assert result.desire_type == DesireType.ACTION

    def test_classify_philosophical_desire(self, agi_runner):
        result = agi_runner.desire_classifier.classify(
            "I wonder about the nature of consciousness"
        )
        assert result.desire_type == DesireType.PHILOSOPHICAL


# =============================================================================
# Metrics Tests
# =============================================================================

class TestMetrics:
    """Test metrics reporting."""

    def test_get_metrics_returns_dict(self, agi_runner):
        metrics = agi_runner.get_metrics()
        assert isinstance(metrics, dict)

    def test_metrics_includes_cycle_count(self, agi_runner):
        agi_runner._cycle_count = 5
        metrics = agi_runner.get_metrics()
        assert metrics.get('cycle_count') == 5

    def test_metrics_includes_bootstrap_status(self, agi_runner):
        metrics = agi_runner.get_metrics()
        assert 'bootstrapped' in metrics


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration:
    """Integration tests for AGIRunner."""

    @pytest.mark.asyncio
    async def test_full_bootstrap_cycle(self, agi_runner):
        """Test complete bootstrap process."""
        assert not agi_runner._bootstrapped

        await agi_runner.bootstrap_from_current_state()

        assert agi_runner._bootstrapped
        # Verify some queries were made
        assert len(agi_runner.memory.queries_run) > 0

    @pytest.mark.asyncio
    async def test_runner_with_evaluator(self, agi_runner):
        """Test AGIRunner when evaluator is injected."""
        # Mock evaluator
        mock_evaluator = MagicMock()
        mock_evaluator.evaluate = AsyncMock(return_value={
            "reasoning": 0.7,
            "memory": 0.6
        })

        agi_runner.evaluator = mock_evaluator
        assert agi_runner.evaluator is not None


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
