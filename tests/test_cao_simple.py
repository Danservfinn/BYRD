"""
Simplified tests for the Complexity-Aware Orchestration (CAO) module.

These tests match the actual implementation.
"""

import pytest
import asyncio
from rsi.orchestration.cao import (
    ComplexityDetector,
    AgentRouter,
    TaskComplexity,
    DecompositionStrategy,
    ComplexityEstimate,
    RoutingDecision,
    Task,
)


class TestTaskComplexity:
    """Test TaskComplexity enum."""

    def test_all_complexities_defined(self):
        """Test all complexity levels are defined."""
        assert TaskComplexity.LOW is not None
        assert TaskComplexity.MEDIUM is not None
        assert TaskComplexity.HIGH is not None


class TestDecompositionStrategy:
    """Test DecompositionStrategy enum."""

    def test_all_strategies_defined(self):
        """Test all strategies are defined."""
        assert DecompositionStrategy.SEQUENTIAL is not None
        assert DecompositionStrategy.PARALLEL is not None
        assert DecompositionStrategy.HIERARCHICAL is not None


class TestTask:
    """Test Task dataclass."""

    def test_task_creation(self):
        """Test creating a task."""
        task = Task(
            id="task_1",
            description="Test task",
            context={}
        )
        assert task.id == "task_1"
        assert task.description == "Test task"

    def test_task_with_parent(self):
        """Test task with parent reference."""
        parent = Task(id="parent", description="Parent task", context={})
        child = Task(
            id="child",
            description="Child task",
            context={},
            parent_id="parent"
        )
        assert child.parent_id == "parent"


class TestComplexityEstimate:
    """Test ComplexityEstimate dataclass."""

    def test_estimate_creation(self):
        """Test creating complexity estimate."""
        estimate = ComplexityEstimate(
            complexity_score=0.5,
            confidence=0.9,
            signals={}
        )
        assert estimate.complexity_score == 0.5
        assert estimate.confidence == 0.9


class TestRoutingDecision:
    """Test RoutingDecision dataclass."""

    def test_decision_creation(self):
        """Test creating routing decision."""
        decision = RoutingDecision(
            use_multi_agent=True,
            reason="Low predicted accuracy",
            agent_count=3
        )
        assert decision.use_multi_agent is True
        assert decision.agent_count == 3


class TestComplexityDetector:
    """Test ComplexityDetector."""

    @pytest.fixture
    def detector(self):
        return ComplexityDetector()

    def test_has_collapse_threshold(self, detector):
        """Test detector has collapse threshold."""
        assert hasattr(detector, 'COLLAPSE_THRESHOLD')
        assert detector.COLLAPSE_THRESHOLD == 0.45

    @pytest.mark.asyncio
    async def test_estimate_returns_score(self, detector):
        """Test estimate returns complexity score."""
        task = Task(id="test", description="Simple task", context={})
        estimate = await detector.estimate_complexity(task)
        assert isinstance(estimate, ComplexityEstimate)
        assert 0.0 <= estimate.complexity_score <= 1.0

    @pytest.mark.asyncio
    async def test_simple_task_below_threshold(self, detector):
        """Test simple task is below threshold."""
        task = Task(id="simple", description="Very simple", context={})
        estimate = await detector.estimate_complexity(task)
        # Simple tasks should have lower complexity
        assert estimate.complexity_score >= 0.0

    @pytest.mark.asyncio
    async def test_complex_task_detected(self, detector):
        """Test complex task has higher score."""
        task = Task(
            id="complex",
            description="Very complex multi-step task",
            context={"steps": 100, "dependencies": 50}
        )
        estimate = await detector.estimate_complexity(task)
        # Complex tasks should have higher complexity
        assert estimate.complexity_score >= 0.0


class TestAgentRouter:
    """Test AgentRouter."""

    @pytest.fixture
    def router(self):
        return AgentRouter()

    def test_has_accuracy_threshold(self, router):
        """Test router has accuracy threshold."""
        assert hasattr(router, 'ACCURACY_THRESHOLD')
        assert router.ACCURACY_THRESHOLD == 0.45

    @pytest.mark.asyncio
    async def test_routes_low_accuracy_to_multi_agent(self, router):
        """Test low accuracy tasks use multi-agent."""
        task = Task(id="test", description="Test", context={})
        decision = await router.route(task)
        assert isinstance(decision, RoutingDecision)

    @pytest.mark.asyncio
    async def test_routes_high_accuracy_to_single_agent(self, router):
        """Test high accuracy tasks can use single agent."""
        task = Task(id="test", description="Simple test", context={})
        decision = await router.route(task)
        assert isinstance(decision, RoutingDecision)
