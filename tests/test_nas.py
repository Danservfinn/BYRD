"""
Tests for Neural Architecture Search Module.

Tests architecture space, evaluator, and search algorithm.
"""

import pytest
import asyncio

from rsi.plasticity.nas import (
    # Space
    NodeType,
    ConnectionType,
    OperationType,
    NodeSpec,
    ConnectionSpec,
    ArchitectureSpec,
    SpaceConstraints,
    SearchBudget,
    ArchitectureSpace,
    # Evaluator
    TestCase,
    TestSuite,
    EvaluationMetric,
    ArchitectureScore,
    ArchitectureEvaluator,
    # Search
    SearchStrategy,
    DiscoveredArchitecture,
    SearchResult,
    NeuralArchitectureSearch,
)


# ============================================================================
# Architecture Space Tests
# ============================================================================

class TestNodeTypes:
    """Test node type definitions."""

    def test_node_type_enum(self):
        """Test NodeType enum values."""
        assert NodeType.INPUT.value == "input"
        assert NodeType.OUTPUT.value == "output"
        assert NodeType.PROCESSING.value == "processing"
        assert NodeType.ATTENTION.value == "attention"

    def test_connection_type_enum(self):
        """Test ConnectionType enum values."""
        assert ConnectionType.SEQUENTIAL.value == "sequential"
        assert ConnectionType.SKIP.value == "skip"
        assert ConnectionType.RESIDUAL.value == "residual"

    def test_operation_type_enum(self):
        """Test OperationType enum values."""
        assert OperationType.LINEAR.value == "linear"
        assert OperationType.ATTENTION.value == "attention"
        assert OperationType.EMBEDDING.value == "embedding"


class TestNodeSpec:
    """Test NodeSpec dataclass."""

    def test_create_node_spec(self):
        """Test creating a node spec."""
        node = NodeSpec(
            id="test_node",
            node_type=NodeType.PROCESSING,
            operation=OperationType.LINEAR,
            input_dim=256,
            output_dim=512
        )
        assert node.id == "test_node"
        assert node.input_dim == 256
        assert node.output_dim == 512

    def test_node_to_dict(self):
        """Test node serialization."""
        node = NodeSpec(
            id="test",
            node_type=NodeType.ATTENTION,
            operation=OperationType.ATTENTION,
            input_dim=128,
            output_dim=128
        )
        data = node.to_dict()
        assert data['id'] == "test"
        assert data['node_type'] == "attention"
        assert data['operation'] == "attention"


class TestArchitectureSpec:
    """Test ArchitectureSpec dataclass."""

    @pytest.fixture
    def simple_architecture(self):
        """Create a simple architecture."""
        nodes = [
            NodeSpec("input", NodeType.INPUT, OperationType.IDENTITY, 256, 256),
            NodeSpec("hidden", NodeType.PROCESSING, OperationType.LINEAR, 256, 512),
            NodeSpec("output", NodeType.OUTPUT, OperationType.IDENTITY, 512, 512)
        ]
        connections = [
            ConnectionSpec("c1", "input", "hidden", ConnectionType.SEQUENTIAL),
            ConnectionSpec("c2", "hidden", "output", ConnectionType.SEQUENTIAL)
        ]
        return ArchitectureSpec(
            id="test_arch",
            name="Test Architecture",
            nodes=nodes,
            connections=connections,
            input_nodes=["input"],
            output_nodes=["output"]
        )

    def test_architecture_properties(self, simple_architecture):
        """Test architecture properties."""
        assert simple_architecture.node_count == 3
        assert simple_architecture.connection_count == 2

    def test_get_node(self, simple_architecture):
        """Test getting node by ID."""
        node = simple_architecture.get_node("hidden")
        assert node is not None
        assert node.operation == OperationType.LINEAR

        missing = simple_architecture.get_node("nonexistent")
        assert missing is None

    def test_architecture_to_dict(self, simple_architecture):
        """Test architecture serialization."""
        data = simple_architecture.to_dict()
        assert data['id'] == "test_arch"
        assert len(data['nodes']) == 3
        assert len(data['connections']) == 2


class TestArchitectureSpace:
    """Test ArchitectureSpace class."""

    @pytest.fixture
    def space(self):
        """Create architecture space."""
        return ArchitectureSpace()

    def test_sample_random(self, space):
        """Test random architecture sampling."""
        arch = space.sample_random("Test")
        assert arch is not None
        assert arch.node_count >= 2
        assert len(arch.input_nodes) > 0
        assert len(arch.output_nodes) > 0

    def test_mutate(self, space):
        """Test architecture mutation."""
        original = space.sample_random()
        mutated = space.mutate(original, mutation_rate=0.5)

        assert mutated.id != original.id
        assert 'parent' in mutated.metadata

    def test_crossover(self, space):
        """Test architecture crossover."""
        parent1 = space.sample_random("Parent1")
        parent2 = space.sample_random("Parent2")
        offspring = space.crossover(parent1, parent2)

        assert offspring.id not in [parent1.id, parent2.id]
        assert 'parent1' in offspring.metadata
        assert 'parent2' in offspring.metadata

    def test_validate(self, space):
        """Test architecture validation."""
        arch = space.sample_random()
        valid, issues = space.validate(arch)
        assert valid is True
        assert issues == []

    def test_get_stats(self, space):
        """Test space statistics."""
        space.sample_random()
        space.sample_random()

        stats = space.get_stats()
        assert stats['samples_generated'] == 2

    def test_reset(self, space):
        """Test space reset."""
        space.sample_random()
        space.reset()
        assert space._samples_generated == 0


# ============================================================================
# Evaluator Tests
# ============================================================================

class TestTestSuite:
    """Test TestSuite class."""

    def test_create_test_suite(self):
        """Test creating a test suite."""
        cases = [
            TestCase("t1", "Test 1", {"x": 1}, {"y": 2}),
            TestCase("t2", "Test 2", {"x": 2}, {"y": 4})
        ]
        suite = TestSuite("suite1", "Test Suite", cases)

        assert suite.size == 2
        assert suite.name == "Test Suite"


class TestEvaluationMetric:
    """Test EvaluationMetric class."""

    def test_create_metric(self):
        """Test creating a metric."""
        metric = EvaluationMetric("accuracy", 0.95, weight=2.0)
        assert metric.value == 0.95
        assert metric.weight == 2.0
        assert metric.higher_is_better is True

    def test_metric_to_dict(self):
        """Test metric serialization."""
        metric = EvaluationMetric("loss", 0.1, higher_is_better=False)
        data = metric.to_dict()
        assert data['name'] == "loss"
        assert data['higher_is_better'] is False


class TestArchitectureEvaluator:
    """Test ArchitectureEvaluator class."""

    @pytest.fixture
    def evaluator(self):
        """Create evaluator."""
        return ArchitectureEvaluator()

    @pytest.fixture
    def space(self):
        """Create space."""
        return ArchitectureSpace()

    def test_register_test_suite(self, evaluator):
        """Test registering a test suite."""
        suite = evaluator.create_default_test_suite()
        assert suite.id in evaluator._test_suites

    @pytest.mark.asyncio
    async def test_evaluate(self, evaluator, space):
        """Test architecture evaluation."""
        arch = space.sample_random()
        suite = evaluator.create_default_test_suite()

        score = await evaluator.evaluate(arch, suite)

        assert score.architecture_id == arch.id
        assert 0.0 <= score.overall_score <= 1.0
        assert score.evaluation_time_ms > 0
        assert len(score.metrics) > 0

    @pytest.mark.asyncio
    async def test_evaluate_without_suite(self, evaluator, space):
        """Test evaluation without explicit suite."""
        arch = space.sample_random()
        evaluator.create_default_test_suite()

        score = await evaluator.evaluate(arch)
        assert score is not None

    def test_register_custom_metric(self, evaluator):
        """Test registering custom metric."""
        def custom_metric(arch):
            return 0.5

        evaluator.register_metric("custom", custom_metric)
        assert "custom" in evaluator._metric_functions

    @pytest.mark.asyncio
    async def test_get_best_architectures(self, evaluator, space):
        """Test getting best architectures."""
        suite = evaluator.create_default_test_suite()

        for i in range(5):
            arch = space.sample_random()
            await evaluator.evaluate(arch, suite)

        best = evaluator.get_best_architectures(top_n=3)
        assert len(best) <= 3

    def test_get_stats(self, evaluator):
        """Test evaluator stats."""
        stats = evaluator.get_stats()
        assert 'total_evaluations' in stats
        assert 'metrics_available' in stats

    def test_reset(self, evaluator):
        """Test evaluator reset."""
        evaluator.create_default_test_suite()
        evaluator.reset()
        assert evaluator._total_evaluations == 0


# ============================================================================
# Search Tests
# ============================================================================

class TestSearchStrategy:
    """Test SearchStrategy enum."""

    def test_search_strategies(self):
        """Test strategy values."""
        assert SearchStrategy.RANDOM.value == "random"
        assert SearchStrategy.EVOLUTIONARY.value == "evolutionary"
        assert SearchStrategy.TOURNAMENT.value == "tournament"


class TestNeuralArchitectureSearch:
    """Test NeuralArchitectureSearch class."""

    @pytest.fixture
    def nas(self):
        """Create NAS instance."""
        return NeuralArchitectureSearch(config={
            'population_size': 10,
            'mutation_rate': 0.2
        })

    @pytest.mark.asyncio
    async def test_search_basic(self, nas):
        """Test basic search."""
        budget = SearchBudget(
            max_evaluations=20,
            max_time_seconds=30.0
        )

        result = await nas.search(
            goal="Find efficient architecture",
            budget=budget
        )

        assert result is not None
        assert result.best_architecture is not None
        assert result.total_evaluations > 0
        assert len(result.all_discovered) > 0

    @pytest.mark.asyncio
    async def test_search_with_target(self, nas):
        """Test search with target score."""
        budget = SearchBudget(
            max_evaluations=50,
            target_score=0.3  # Low target for quick test
        )

        result = await nas.search(
            goal="Reach target",
            budget=budget
        )

        assert result is not None
        # May or may not reach target
        if result.target_reached:
            assert result.best_architecture.score.overall_score >= 0.3

    @pytest.mark.asyncio
    async def test_evaluate_architecture(self, nas):
        """Test direct architecture evaluation."""
        arch = nas.space.sample_random()
        score = await nas.evaluate_architecture(arch)

        assert score is not None
        assert score.architecture_id == arch.id

    def test_get_best(self, nas):
        """Test getting best before search."""
        assert nas.get_best() is None

    @pytest.mark.asyncio
    async def test_get_best_after_search(self, nas):
        """Test getting best after search."""
        await nas.search(
            goal="Test",
            budget=SearchBudget(max_evaluations=10)
        )
        best = nas.get_best()
        assert best is not None

    def test_get_population(self, nas):
        """Test getting population."""
        pop = nas.get_population()
        assert pop == []  # Empty before search

    def test_get_stats(self, nas):
        """Test getting NAS stats."""
        stats = nas.get_stats()
        assert 'total_searches' in stats
        assert 'strategy' in stats
        assert 'space_stats' in stats
        assert 'evaluator_stats' in stats

    def test_reset(self, nas):
        """Test NAS reset."""
        nas._generation = 5
        nas.reset()
        assert nas._generation == 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestNASIntegration:
    """Integration tests for NAS components."""

    @pytest.mark.asyncio
    async def test_full_search_workflow(self):
        """Test complete search workflow."""
        # Create components
        space = ArchitectureSpace(SpaceConstraints(
            min_nodes=3,
            max_nodes=8
        ))
        evaluator = ArchitectureEvaluator()
        nas = NeuralArchitectureSearch(space, evaluator, {
            'population_size': 5
        })

        # Create test suite
        suite = evaluator.create_default_test_suite()

        # Run search
        result = await nas.search(
            goal="Find optimal architecture",
            budget=SearchBudget(max_evaluations=15)
        )

        # Verify results
        assert result.best_architecture is not None
        assert result.total_evaluations >= 5
        assert result.final_generation >= 0

        # Check architecture is valid
        valid, _ = space.validate(result.best_architecture.architecture)
        assert valid is True

    @pytest.mark.asyncio
    async def test_multiple_searches(self):
        """Test running multiple searches."""
        nas = NeuralArchitectureSearch(config={'population_size': 5})

        results = []
        for i in range(3):
            result = await nas.search(
                goal=f"Search {i}",
                budget=SearchBudget(max_evaluations=10)
            )
            results.append(result)

        # Each search should complete
        assert len(results) == 3
        assert nas._total_searches == 3

    @pytest.mark.asyncio
    async def test_discovered_architecture_lineage(self):
        """Test that discovered architectures have lineage."""
        nas = NeuralArchitectureSearch(config={'population_size': 5})

        result = await nas.search(
            goal="Test lineage",
            budget=SearchBudget(max_evaluations=20)
        )

        # Later generations should have parent IDs
        later_gen = [d for d in result.all_discovered if d.generation > 0]
        if later_gen:
            # At least some should have parents
            with_parents = [d for d in later_gen if d.parent_ids]
            assert len(with_parents) > 0
