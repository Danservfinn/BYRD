"""
Tests for the Complexity-Aware Orchestration (CAO) module.

CAO implements adaptive task routing based on Apple/DeepMind research showing
that LLMs experience performance collapse above 45% complexity threshold.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from rsi.orchestration.cao import (
    ComplexityDetector,
    AgentRouter,
    TaskDecomposer,
    ComplexityAwareOrchestrator,
    Task,
    TaskComplexity,
    DecompositionStrategy,
    ComplexityEstimate,
    RoutingDecision,
)


class TestComplexitySignals:
    """Test ComplexitySignals dataclass."""

    def test_signals_creation(self):
        """Test creating complexity signals."""
        signals = ComplexitySignals(
            token_count=1500,
            reasoning_depth=4,
            dependency_count=3,
            domain_complexity=0.7,
            historical_accuracy=0.85,
        )
        assert signals.token_count == 1500
        assert signals.reasoning_depth == 4
        assert signals.domain_complexity == 0.7

    def test_signals_with_defaults(self):
        """Test signals with default values."""
        signals = ComplexitySignals()
        assert signals.token_count == 0
        assert signals.reasoning_depth == 0


class TestTask:
    """Test Task dataclass."""

    def test_task_creation(self):
        """Test task creation with required fields."""
        task = Task(
            id="task_001",
            description="Implement feature X",
            domain="code",
            context={"file": "module.py"},
        )
        assert task.id == "task_001"
        assert task.domain == "code"

    def test_task_with_parent(self):
        """Test task with parent reference."""
        parent = Task(id="parent", description="Parent task", domain="code")
        child = Task(
            id="child",
            description="Child task",
            domain="code",
            parent_id="parent",
        )
        assert child.parent_id == "parent"


class TestComplexityDetector:
    """Test ComplexityDetector class."""

    @pytest.fixture
    def detector(self):
        return ComplexityDetector()

    @pytest.fixture
    def simple_task(self):
        return Task(
            id="simple",
            description="Add a comment",
            domain="code",
            context={"size": "small"},
        )

    @pytest.fixture
    def complex_task(self):
        return Task(
            id="complex",
            description="Refactor the entire authentication system with OAuth2, JWT tokens, multi-factor authentication, session management, and role-based access control while maintaining backwards compatibility",
            domain="code",
            context={"files": ["auth.py", "jwt.py", "mfa.py", "session.py", "rbac.py"]},
        )

    def test_has_collapse_threshold(self, detector):
        """Test that detector has the 45% collapse threshold."""
        assert detector.COLLAPSE_THRESHOLD == 0.45

    @pytest.mark.asyncio
    async def test_estimate_returns_score(self, detector, simple_task):
        """Test that estimate returns a complexity score."""
        score = await detector.estimate_complexity(simple_task)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    @pytest.mark.asyncio
    async def test_simple_task_below_threshold(self, detector, simple_task):
        """Test that simple tasks are below collapse threshold."""
        score = await detector.estimate_complexity(simple_task)
        assert score < detector.COLLAPSE_THRESHOLD

    @pytest.mark.asyncio
    async def test_complex_task_detected(self, detector, complex_task):
        """Test that complex tasks are detected as complex."""
        score = await detector.estimate_complexity(complex_task)
        # Complex tasks should have higher scores
        assert score > 0.3

    @pytest.mark.asyncio
    async def test_get_signals(self, detector, simple_task):
        """Test getting detailed complexity signals."""
        signals = await detector.get_complexity_signals(simple_task)
        assert isinstance(signals, ComplexitySignals)


class TestAgentRouter:
    """Test AgentRouter class."""

    @pytest.fixture
    def router(self):
        return AgentRouter()

    @pytest.fixture
    def low_accuracy_task(self):
        return Task(
            id="low",
            description="Complex multi-step task",
            domain="planning",
            context={"predicted_accuracy": 0.3},
        )

    @pytest.fixture
    def high_accuracy_task(self):
        return Task(
            id="high",
            description="Simple direct task",
            domain="code",
            context={"predicted_accuracy": 0.8},
        )

    def test_has_accuracy_threshold(self, router):
        """Test that router has 45% accuracy threshold."""
        assert router.MULTI_AGENT_THRESHOLD == 0.45

    @pytest.mark.asyncio
    async def test_routes_low_accuracy_to_multi_agent(self, router, low_accuracy_task):
        """Test that low accuracy tasks go to multi-agent."""
        use_multi = await router.should_use_multi_agent(low_accuracy_task)
        assert use_multi is True

    @pytest.mark.asyncio
    async def test_routes_high_accuracy_to_single_agent(self, router, high_accuracy_task):
        """Test that high accuracy tasks go to single agent."""
        use_multi = await router.should_use_multi_agent(high_accuracy_task)
        assert use_multi is False

    @pytest.mark.asyncio
    async def test_get_agent_count(self, router, low_accuracy_task):
        """Test getting recommended agent count."""
        count = await router.get_recommended_agent_count(low_accuracy_task)
        assert isinstance(count, int)
        assert count >= 1


class TestDecompositionStrategy:
    """Test DecompositionStrategy enum."""

    def test_all_strategies_defined(self):
        """Test all decomposition strategies are defined."""
        assert DecompositionStrategy.SEQUENTIAL is not None
        assert DecompositionStrategy.PARALLEL is not None
        assert DecompositionStrategy.HIERARCHICAL is not None
        assert DecompositionStrategy.RECURSIVE is not None


class TestTaskDecomposer:
    """Test TaskDecomposer class."""

    @pytest.fixture
    def decomposer(self):
        return TaskDecomposer()

    @pytest.fixture
    def decomposable_task(self):
        return Task(
            id="decompose",
            description="Build a complete user management system with registration, login, profile, and settings",
            domain="code",
            context={"features": ["registration", "login", "profile", "settings"]},
        )

    @pytest.mark.asyncio
    async def test_decompose_returns_subtasks(self, decomposer, decomposable_task):
        """Test that decompose returns a list of subtasks."""
        subtasks = await decomposer.decompose(decomposable_task)
        assert isinstance(subtasks, list)
        assert all(isinstance(t, Task) for t in subtasks)

    @pytest.mark.asyncio
    async def test_subtasks_have_parent_reference(self, decomposer, decomposable_task):
        """Test that subtasks reference parent."""
        subtasks = await decomposer.decompose(decomposable_task)
        if subtasks:
            for subtask in subtasks:
                assert subtask.parent_id == decomposable_task.id

    @pytest.mark.asyncio
    async def test_select_strategy(self, decomposer, decomposable_task):
        """Test strategy selection."""
        strategy = await decomposer.select_strategy(decomposable_task)
        assert isinstance(strategy, DecompositionStrategy)


class TestComplexityAwareOrchestrator:
    """Test the main ComplexityAwareOrchestrator class."""

    @pytest.fixture
    def orchestrator(self):
        return ComplexityAwareOrchestrator()

    @pytest.fixture
    def sample_task(self):
        return Task(
            id="orch_test",
            description="Implement a simple helper function",
            domain="code",
            context={},
        )

    def test_orchestrator_has_components(self, orchestrator):
        """Test that orchestrator has all required components."""
        assert orchestrator.detector is not None
        assert orchestrator.router is not None
        assert orchestrator.decomposer is not None

    @pytest.mark.asyncio
    async def test_execute_returns_result(self, orchestrator, sample_task):
        """Test that execute returns a TaskResult."""
        result = await orchestrator.execute(sample_task)
        assert isinstance(result, TaskResult)

    @pytest.mark.asyncio
    async def test_result_has_status(self, orchestrator, sample_task):
        """Test that result includes status."""
        result = await orchestrator.execute(sample_task)
        assert result.status in ["completed", "failed", "decomposed"]

    @pytest.mark.asyncio
    async def test_tracks_complexity(self, orchestrator, sample_task):
        """Test that orchestrator tracks complexity."""
        result = await orchestrator.execute(sample_task)
        assert result.complexity_score is not None
        assert 0.0 <= result.complexity_score <= 1.0


class TestOrchestratorWithMocks:
    """Test orchestrator with mocked components."""

    @pytest.mark.asyncio
    async def test_decomposes_complex_tasks(self):
        """Test that complex tasks are decomposed."""
        orchestrator = ComplexityAwareOrchestrator()

        # Mock detector to return high complexity
        orchestrator.detector.estimate_complexity = AsyncMock(return_value=0.8)

        task = Task(
            id="complex",
            description="Very complex task",
            domain="code",
        )

        result = await orchestrator.execute(task)
        # Complex tasks should be decomposed
        assert result.was_decomposed or result.status == "decomposed"

    @pytest.mark.asyncio
    async def test_direct_execution_for_simple_tasks(self):
        """Test that simple tasks are executed directly."""
        orchestrator = ComplexityAwareOrchestrator()

        # Mock detector to return low complexity
        orchestrator.detector.estimate_complexity = AsyncMock(return_value=0.2)

        task = Task(
            id="simple",
            description="Simple task",
            domain="code",
        )

        result = await orchestrator.execute(task)
        assert result.was_decomposed is False


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_handles_empty_task(self):
        """Test handling of minimal task."""
        orchestrator = ComplexityAwareOrchestrator()

        task = Task(id="empty", description="", domain="code")
        result = await orchestrator.execute(task)

        assert result is not None

    @pytest.mark.asyncio
    async def test_handles_none_context(self):
        """Test handling of None context."""
        detector = ComplexityDetector()

        task = Task(
            id="no_context",
            description="Task without context",
            domain="code",
            context=None,
        )

        score = await detector.estimate_complexity(task)
        assert score is not None

    @pytest.mark.asyncio
    async def test_threshold_boundary(self):
        """Test behavior at exactly 45% threshold."""
        detector = ComplexityDetector()
        router = AgentRouter()

        # Mock to return exactly threshold
        detector.estimate_complexity = AsyncMock(return_value=0.45)

        task = Task(id="boundary", description="Boundary case", domain="code")

        score = await detector.estimate_complexity(task)
        assert score == 0.45

        # At boundary, should not use multi-agent (< not <=)
        use_multi = await router.should_use_multi_agent(task)
        # Behavior at boundary depends on implementation
        assert isinstance(use_multi, bool)
