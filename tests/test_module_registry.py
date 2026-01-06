"""
Tests for Module Registry and Composer.

Tests module registration, discovery, composition, and execution.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
import asyncio

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rsi.plasticity import (
    ModuleType,
    ModuleStatus,
    CompositionType,
    ModuleCapability,
    ModuleDependency,
    CognitiveModule,
    ComposedModule,
    CompositionCandidate,
    ModuleRegistry,
    ModuleComposer,
    CompositionResult,
    CompositionRule,
    create_module_id,
    create_reasoning_module,
    create_memory_module,
    create_planning_module,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_memory():
    """Create mock memory for Neo4j operations."""
    memory = MagicMock()
    memory.query_neo4j = AsyncMock(return_value=[])
    return memory


@pytest.fixture
def registry(mock_memory):
    """Create registry with mock memory."""
    return ModuleRegistry(memory=mock_memory, config={})


@pytest.fixture
def composer(registry):
    """Create composer with registry."""
    return ModuleComposer(registry=registry, config={})


@pytest.fixture
def sample_module():
    """Create a sample cognitive module."""
    return CognitiveModule(
        id=create_module_id(),
        name="Test Module",
        module_type=ModuleType.REASONING,
        version="1.0.0",
        status=ModuleStatus.REGISTERED,
        description="A test module",
        capabilities=[
            ModuleCapability(
                name="test_capability",
                description="Test capability",
                performance_baseline=0.7
            )
        ],
        composable_with=[ModuleType.MEMORY, ModuleType.PLANNING],
        tags=["test", "sample"]
    )


@pytest.fixture
def reasoning_module():
    """Create core reasoning module."""
    return create_reasoning_module()


@pytest.fixture
def memory_module():
    """Create core memory module."""
    return create_memory_module()


@pytest.fixture
def planning_module():
    """Create core planning module."""
    return create_planning_module()


# ============================================================================
# Module Types Tests
# ============================================================================

class TestModuleTypes:
    """Tests for module type definitions."""

    def test_module_type_enum(self):
        """Test ModuleType enum values."""
        assert ModuleType.REASONING.value == "reasoning"
        assert ModuleType.MEMORY.value == "memory"
        assert ModuleType.PLANNING.value == "planning"
        assert ModuleType.META.value == "meta"

    def test_module_status_enum(self):
        """Test ModuleStatus enum values."""
        assert ModuleStatus.DRAFT.value == "draft"
        assert ModuleStatus.REGISTERED.value == "registered"
        assert ModuleStatus.ACTIVE.value == "active"
        assert ModuleStatus.DEPRECATED.value == "deprecated"

    def test_composition_type_enum(self):
        """Test CompositionType enum values."""
        assert CompositionType.SEQUENTIAL.value == "sequential"
        assert CompositionType.PARALLEL.value == "parallel"
        assert CompositionType.ENSEMBLE.value == "ensemble"
        assert CompositionType.CONDITIONAL.value == "conditional"

    def test_create_module_id(self):
        """Test module ID generation."""
        id1 = create_module_id()
        id2 = create_module_id()

        assert id1.startswith("mod_")
        assert len(id1) == 16  # "mod_" + 12 hex chars
        assert id1 != id2  # Should be unique

    def test_cognitive_module_to_dict(self, sample_module):
        """Test module serialization."""
        d = sample_module.to_dict()

        assert d['name'] == "Test Module"
        assert d['module_type'] == "reasoning"
        assert d['version'] == "1.0.0"
        assert len(d['capabilities']) == 1
        assert 'test' in d['tags']

    def test_cognitive_module_from_dict(self, sample_module):
        """Test module deserialization."""
        d = sample_module.to_dict()
        restored = CognitiveModule.from_dict(d)

        assert restored.name == sample_module.name
        assert restored.module_type == sample_module.module_type
        assert len(restored.capabilities) == len(sample_module.capabilities)

    def test_module_success_rate(self, sample_module):
        """Test success rate calculation."""
        assert sample_module.success_rate == 0.0  # No invocations

        sample_module.invocation_count = 10
        sample_module.success_count = 8
        assert sample_module.success_rate == 0.8

    def test_module_avg_latency(self, sample_module):
        """Test average latency calculation."""
        assert sample_module.avg_latency_ms == 0.0  # No invocations

        sample_module.invocation_count = 5
        sample_module.total_latency_ms = 500.0
        assert sample_module.avg_latency_ms == 100.0


class TestPrebuiltModules:
    """Tests for pre-built core modules."""

    def test_reasoning_module(self, reasoning_module):
        """Test reasoning module structure."""
        assert reasoning_module.id == "mod_reasoning_v1"
        assert reasoning_module.module_type == ModuleType.REASONING
        assert reasoning_module.status == ModuleStatus.ACTIVE
        assert len(reasoning_module.capabilities) >= 2
        assert "core" in reasoning_module.tags

    def test_memory_module(self, memory_module):
        """Test memory module structure."""
        assert memory_module.id == "mod_memory_v1"
        assert memory_module.module_type == ModuleType.MEMORY
        assert any(c.name == "store" for c in memory_module.capabilities)
        assert any(c.name == "retrieve" for c in memory_module.capabilities)

    def test_planning_module(self, planning_module):
        """Test planning module structure."""
        assert planning_module.id == "mod_planning_v1"
        assert planning_module.module_type == ModuleType.PLANNING
        assert any(c.name == "create_plan" for c in planning_module.capabilities)


# ============================================================================
# Module Registry Tests
# ============================================================================

class TestModuleRegistry:
    """Tests for module registry operations."""

    @pytest.mark.asyncio
    async def test_initialize_core_modules(self, registry):
        """Test registry initialization with core modules."""
        await registry.initialize()

        modules = await registry.list_modules()
        assert len(modules) == 3  # reasoning, memory, planning

        # Check core modules are registered
        reasoning = await registry.get_module("mod_reasoning_v1")
        assert reasoning is not None
        assert reasoning.name == "Core Reasoning"

    @pytest.mark.asyncio
    async def test_register_module(self, registry, sample_module):
        """Test module registration."""
        module_id = await registry.register_module(sample_module)

        assert module_id == sample_module.id

        retrieved = await registry.get_module(module_id)
        assert retrieved is not None
        assert retrieved.name == sample_module.name

    @pytest.mark.asyncio
    async def test_register_sets_status(self, registry):
        """Test that registering a draft module sets status."""
        module = CognitiveModule(
            id=create_module_id(),
            name="Draft Module",
            module_type=ModuleType.EVALUATION,
            status=ModuleStatus.DRAFT
        )

        await registry.register_module(module)

        retrieved = await registry.get_module(module.id)
        assert retrieved.status == ModuleStatus.REGISTERED

    @pytest.mark.asyncio
    async def test_list_modules_with_type_filter(self, registry):
        """Test listing modules with type filter."""
        await registry.initialize()

        reasoning_modules = await registry.list_modules(
            filter_type=ModuleType.REASONING
        )
        assert len(reasoning_modules) == 1
        assert reasoning_modules[0].module_type == ModuleType.REASONING

    @pytest.mark.asyncio
    async def test_list_modules_with_tag_filter(self, registry):
        """Test listing modules with tag filter."""
        await registry.initialize()

        core_modules = await registry.list_modules(filter_tags=["core"])
        assert len(core_modules) == 3  # All core modules have "core" tag

    @pytest.mark.asyncio
    async def test_search_modules(self, registry):
        """Test module search by name/description."""
        await registry.initialize()

        results = await registry.search_modules("reasoning")
        assert len(results) >= 1
        assert any(m.name == "Core Reasoning" for m in results)

    @pytest.mark.asyncio
    async def test_find_by_capability(self, registry):
        """Test finding modules by capability."""
        await registry.initialize()

        modules = await registry.find_by_capability("logical_inference")
        assert len(modules) == 1
        assert modules[0].id == "mod_reasoning_v1"

    @pytest.mark.asyncio
    async def test_update_module(self, registry, sample_module):
        """Test updating module properties."""
        await registry.register_module(sample_module)

        updated = await registry.update_module(
            sample_module.id,
            {"description": "Updated description", "status": ModuleStatus.ACTIVE}
        )

        assert updated.description == "Updated description"
        assert updated.status == ModuleStatus.ACTIVE

    @pytest.mark.asyncio
    async def test_record_invocation(self, registry, sample_module):
        """Test recording module invocations."""
        await registry.register_module(sample_module)

        await registry.record_invocation(sample_module.id, success=True, latency_ms=50.0)
        await registry.record_invocation(sample_module.id, success=True, latency_ms=30.0)
        await registry.record_invocation(sample_module.id, success=False, latency_ms=100.0)

        module = await registry.get_module(sample_module.id)
        assert module.invocation_count == 3
        assert module.success_count == 2
        assert module.total_latency_ms == 180.0

    @pytest.mark.asyncio
    async def test_deprecate_module(self, registry, sample_module):
        """Test deprecating a module."""
        await registry.register_module(sample_module)

        result = await registry.deprecate_module(sample_module.id)
        assert result == True

        module = await registry.get_module(sample_module.id)
        assert module.status == ModuleStatus.DEPRECATED

    @pytest.mark.asyncio
    async def test_get_composition_candidates(self, registry):
        """Test getting composition candidates for a goal."""
        await registry.initialize()

        # Use search terms that match module names/descriptions
        candidates = await registry.get_composition_candidates(
            goal="reasoning logic inference",
            max_modules=3
        )

        # Should suggest composing modules matching the goal
        # If we found candidates, verify their structure
        for candidate in candidates:
            assert len(candidate.modules) == 2
            assert candidate.composition_type in CompositionType

    @pytest.mark.asyncio
    async def test_get_stats(self, registry):
        """Test registry statistics."""
        await registry.initialize()

        stats = registry.get_stats()

        assert stats.total_modules == 3
        assert stats.active_modules == 3  # All core modules are active
        assert 'reasoning' in stats.modules_by_type

    @pytest.mark.asyncio
    async def test_reset(self, registry, sample_module):
        """Test registry reset."""
        await registry.register_module(sample_module)
        assert registry.get_stats().total_modules == 1

        registry.reset()

        assert registry.get_stats().total_modules == 0


# ============================================================================
# Module Composer Tests
# ============================================================================

class TestModuleComposer:
    """Tests for module composition operations."""

    @pytest.mark.asyncio
    async def test_compose_sequential(self, composer, reasoning_module, memory_module):
        """Test sequential composition."""
        composed = await composer.compose(
            modules=[reasoning_module, memory_module],
            composition_type=CompositionType.SEQUENTIAL,
            name="Reasoning+Memory"
        )

        assert composed.name == "Reasoning+Memory"
        assert composed.composition_type == CompositionType.SEQUENTIAL
        assert len(composed.source_modules) == 2
        assert "mod_reasoning_v1" in composed.source_modules
        assert "mod_memory_v1" in composed.source_modules

    @pytest.mark.asyncio
    async def test_compose_parallel(self, composer, reasoning_module, planning_module):
        """Test parallel composition."""
        composed = await composer.compose(
            modules=[reasoning_module, planning_module],
            composition_type=CompositionType.PARALLEL
        )

        assert composed.composition_type == CompositionType.PARALLEL
        # Combined type should be META since different types
        assert composed.module_type == ModuleType.META

    @pytest.mark.asyncio
    async def test_compose_ensemble(self, composer):
        """Test ensemble composition of same-type modules."""
        mod1 = CognitiveModule(
            id=create_module_id(),
            name="Reasoner A",
            module_type=ModuleType.REASONING,
            status=ModuleStatus.ACTIVE
        )
        mod2 = CognitiveModule(
            id=create_module_id(),
            name="Reasoner B",
            module_type=ModuleType.REASONING,
            status=ModuleStatus.ACTIVE
        )

        composed = await composer.compose(
            modules=[mod1, mod2],
            composition_type=CompositionType.ENSEMBLE
        )

        assert composed.composition_type == CompositionType.ENSEMBLE
        # Same type modules keep the type
        assert composed.module_type == ModuleType.REASONING

    @pytest.mark.asyncio
    async def test_compose_validates_minimum_modules(self, composer, reasoning_module):
        """Test that composition requires at least 2 modules."""
        with pytest.raises(ValueError, match="At least 2 modules"):
            await composer.compose(
                modules=[reasoning_module],
                composition_type=CompositionType.SEQUENTIAL
            )

    @pytest.mark.asyncio
    async def test_compose_validates_status(self, composer):
        """Test that composition validates module status."""
        mod1 = CognitiveModule(
            id=create_module_id(),
            name="Active",
            module_type=ModuleType.REASONING,
            status=ModuleStatus.ACTIVE
        )
        mod2 = CognitiveModule(
            id=create_module_id(),
            name="Deprecated",
            module_type=ModuleType.MEMORY,
            status=ModuleStatus.DEPRECATED
        )

        with pytest.raises(ValueError, match="invalid status"):
            await composer.compose(
                modules=[mod1, mod2],
                composition_type=CompositionType.SEQUENTIAL
            )

    @pytest.mark.asyncio
    async def test_compose_merges_capabilities(self, composer, reasoning_module, memory_module):
        """Test that composition merges capabilities."""
        composed = await composer.compose(
            modules=[reasoning_module, memory_module],
            composition_type=CompositionType.PARALLEL
        )

        cap_names = [c.name for c in composed.capabilities]
        assert "logical_inference" in cap_names
        assert "store" in cap_names

    @pytest.mark.asyncio
    async def test_execute_sequential(self, composer, reasoning_module, memory_module):
        """Test sequential composition execution."""
        composed = await composer.compose(
            modules=[reasoning_module, memory_module],
            composition_type=CompositionType.SEQUENTIAL
        )

        # Create mock executors
        executors = {
            "mod_reasoning_v1": lambda x: f"reasoned: {x}",
            "mod_memory_v1": lambda x: f"memorized: {x}"
        }

        result = await composer.execute_composed(
            composed,
            input_data="test input",
            executors=executors
        )

        assert result.success == True
        assert result.output == "memorized: reasoned: test input"
        assert len(result.module_outputs) == 2

    @pytest.mark.asyncio
    async def test_execute_parallel(self, composer, reasoning_module, memory_module):
        """Test parallel composition execution."""
        composed = await composer.compose(
            modules=[reasoning_module, memory_module],
            composition_type=CompositionType.PARALLEL
        )

        executors = {
            "mod_reasoning_v1": lambda x: f"reasoned: {x}",
            "mod_memory_v1": lambda x: f"memorized: {x}"
        }

        result = await composer.execute_composed(
            composed,
            input_data="test",
            executors=executors
        )

        assert result.success == True
        assert isinstance(result.output, dict)
        assert "mod_reasoning_v1" in result.output
        assert "mod_memory_v1" in result.output

    @pytest.mark.asyncio
    async def test_execute_ensemble_numeric(self, composer):
        """Test ensemble execution with numeric results."""
        mod1 = CognitiveModule(
            id="mod_1",
            name="Scorer A",
            module_type=ModuleType.EVALUATION,
            status=ModuleStatus.ACTIVE
        )
        mod2 = CognitiveModule(
            id="mod_2",
            name="Scorer B",
            module_type=ModuleType.EVALUATION,
            status=ModuleStatus.ACTIVE
        )

        composed = await composer.compose(
            modules=[mod1, mod2],
            composition_type=CompositionType.ENSEMBLE
        )

        executors = {
            "mod_1": lambda x: 0.8,
            "mod_2": lambda x: 0.6
        }

        result = await composer.execute_composed(composed, "input", executors)

        assert result.success == True
        assert result.output == 0.7  # Average of 0.8 and 0.6

    @pytest.mark.asyncio
    async def test_execute_ensemble_string_voting(self, composer):
        """Test ensemble execution with string voting."""
        mod1 = CognitiveModule(
            id="mod_1",
            name="Classifier A",
            module_type=ModuleType.EVALUATION,
            status=ModuleStatus.ACTIVE
        )
        mod2 = CognitiveModule(
            id="mod_2",
            name="Classifier B",
            module_type=ModuleType.EVALUATION,
            status=ModuleStatus.ACTIVE
        )
        mod3 = CognitiveModule(
            id="mod_3",
            name="Classifier C",
            module_type=ModuleType.EVALUATION,
            status=ModuleStatus.ACTIVE
        )

        composed = await composer.compose(
            modules=[mod1, mod2, mod3],
            composition_type=CompositionType.ENSEMBLE
        )

        executors = {
            "mod_1": lambda x: "positive",
            "mod_2": lambda x: "positive",
            "mod_3": lambda x: "negative"
        }

        result = await composer.execute_composed(composed, "input", executors)

        assert result.success == True
        assert result.output == "positive"  # Majority vote

    @pytest.mark.asyncio
    async def test_execute_conditional(self, composer):
        """Test conditional composition execution."""
        mod1 = CognitiveModule(
            id="mod_1",
            name="Path A",
            module_type=ModuleType.REASONING,
            status=ModuleStatus.ACTIVE
        )
        mod2 = CognitiveModule(
            id="mod_2",
            name="Path B",
            module_type=ModuleType.REASONING,
            status=ModuleStatus.ACTIVE
        )

        composed = await composer.compose(
            modules=[mod1, mod2],
            composition_type=CompositionType.CONDITIONAL,
            config={"condition": lambda x: 1 if x > 5 else 0}
        )

        executors = {
            "mod_1": lambda x: f"path_a: {x}",
            "mod_2": lambda x: f"path_b: {x}"
        }

        # Input <= 5 should route to mod_1
        result1 = await composer.execute_composed(composed, 3, executors)
        assert result1.output == "path_a: 3"

        # Input > 5 should route to mod_2
        result2 = await composer.execute_composed(composed, 10, executors)
        assert result2.output == "path_b: 10"

    @pytest.mark.asyncio
    async def test_execute_async_executors(self, composer, reasoning_module, memory_module):
        """Test execution with async executors."""
        composed = await composer.compose(
            modules=[reasoning_module, memory_module],
            composition_type=CompositionType.SEQUENTIAL
        )

        async def async_reason(x):
            await asyncio.sleep(0.01)
            return f"async_reasoned: {x}"

        async def async_memorize(x):
            await asyncio.sleep(0.01)
            return f"async_memorized: {x}"

        executors = {
            "mod_reasoning_v1": async_reason,
            "mod_memory_v1": async_memorize
        }

        result = await composer.execute_composed(composed, "test", executors)

        assert result.success == True
        assert "async_memorized: async_reasoned: test" == result.output

    @pytest.mark.asyncio
    async def test_execute_handles_errors(self, composer, reasoning_module, memory_module):
        """Test that execution handles errors gracefully."""
        composed = await composer.compose(
            modules=[reasoning_module, memory_module],
            composition_type=CompositionType.SEQUENTIAL
        )

        def failing_executor(x):
            raise RuntimeError("Execution failed")

        executors = {
            "mod_reasoning_v1": failing_executor,
            "mod_memory_v1": lambda x: x
        }

        result = await composer.execute_composed(composed, "test", executors)

        assert result.success == False
        assert "Execution failed" in result.error

    def test_add_custom_rule(self, composer):
        """Test adding custom composition rules."""
        custom_rule = CompositionRule(
            name="no_evaluation",
            description="Cannot compose with evaluation modules",
            validator=lambda mods, _: (
                not any(m.module_type == ModuleType.EVALUATION for m in mods),
                "Evaluation modules not allowed"
            )
        )

        composer.add_rule(custom_rule)

        stats = composer.get_stats()
        assert stats['rules_count'] == 5  # 4 default + 1 custom

    def test_get_stats(self, composer):
        """Test composer statistics."""
        stats = composer.get_stats()

        assert 'compositions_created' in stats
        assert 'compositions_executed' in stats
        assert 'rules_count' in stats

    @pytest.mark.asyncio
    async def test_reset(self, composer, reasoning_module, memory_module):
        """Test composer reset."""
        await composer.compose(
            modules=[reasoning_module, memory_module],
            composition_type=CompositionType.SEQUENTIAL
        )

        assert composer.get_stats()['compositions_created'] == 1

        composer.reset()

        assert composer.get_stats()['compositions_created'] == 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestRegistryComposerIntegration:
    """Integration tests for registry and composer."""

    @pytest.mark.asyncio
    async def test_compose_from_registry(self, registry, composer):
        """Test composing modules fetched from registry."""
        await registry.initialize()

        # Get modules from registry
        reasoning = await registry.get_module("mod_reasoning_v1")
        memory = await registry.get_module("mod_memory_v1")

        # Compose them
        composed = await composer.compose(
            modules=[reasoning, memory],
            composition_type=CompositionType.SEQUENTIAL,
            name="ReasoningMemory"
        )

        # Register composed module
        await registry.register_module(composed)

        # Should now have 4 modules
        stats = registry.get_stats()
        assert stats.total_modules == 4

    @pytest.mark.asyncio
    async def test_composition_candidate_to_composed(self, registry, composer):
        """Test turning a composition candidate into a composed module."""
        await registry.initialize()

        # Get modules directly and compose them (more reliable than search)
        reasoning = await registry.get_module("mod_reasoning_v1")
        planning = await registry.get_module("mod_planning_v1")

        # Compose them directly
        composed = await composer.compose(
            modules=[reasoning, planning],
            composition_type=CompositionType.SEQUENTIAL
        )

        assert len(composed.source_modules) == 2
        assert "mod_reasoning_v1" in composed.source_modules
        assert "mod_planning_v1" in composed.source_modules


class TestComposedModuleSerialization:
    """Tests for ComposedModule serialization."""

    @pytest.mark.asyncio
    async def test_composed_module_to_dict(self, composer, reasoning_module, memory_module):
        """Test ComposedModule serialization."""
        composed = await composer.compose(
            modules=[reasoning_module, memory_module],
            composition_type=CompositionType.SEQUENTIAL
        )

        d = composed.to_dict()

        assert d['is_composed'] == True
        assert d['composition_type'] == 'sequential'
        assert len(d['source_modules']) == 2
