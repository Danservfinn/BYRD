"""
Tests for Cognitive Plasticity Engine.

Tests plasticity levels, proposal generation, execution, and level advancement.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rsi.plasticity import (
    # Levels
    PlasticityLevel,
    LevelProgress,
    LevelRequirements,
    LEVEL_REQUIREMENTS,
    can_advance_level,
    get_level_requirements,
    is_operation_allowed,
    # Proposals
    ModificationType,
    RollbackPlan,
    PlasticityProposal,
    ModificationResult,
    ProposalGenerator,
    # Executor
    Checkpoint,
    ModificationExecutor,
    # Engine
    EngineState,
    CognitivePlasticityEngine,
    # Module types
    ModuleRegistry,
    ModuleStatus,
    create_reasoning_module,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_memory():
    """Create mock memory."""
    memory = MagicMock()
    memory.query_neo4j = AsyncMock(return_value=[])
    return memory


@pytest.fixture
def mock_registry():
    """Create mock module registry."""
    registry = MagicMock()
    registry.list_modules = AsyncMock(return_value=[create_reasoning_module()])
    registry.get_module = AsyncMock(return_value=create_reasoning_module())
    registry.update_module = AsyncMock(return_value=create_reasoning_module())
    registry.register_module = AsyncMock(return_value="new_mod_id")
    return registry


@pytest.fixture
def mock_governance():
    """Create mock safety governance."""
    governance = MagicMock()
    governance.evaluate_and_approve = AsyncMock(return_value=(
        MagicMock(can_proceed=True, blocking_issues=[]),
        MagicMock(approved=True, reason="Approved")
    ))
    return governance


@pytest.fixture
def engine(mock_registry, mock_governance, mock_memory):
    """Create plasticity engine with mocks."""
    return CognitivePlasticityEngine(
        module_registry=mock_registry,
        safety_governance=mock_governance,
        memory=mock_memory,
        config={}
    )


@pytest.fixture
def executor(mock_registry, mock_memory):
    """Create modification executor with mocks."""
    return ModificationExecutor(
        module_registry=mock_registry,
        memory=mock_memory,
        config={}
    )


@pytest.fixture
def proposal_generator():
    """Create proposal generator."""
    return ProposalGenerator(config={})


@pytest.fixture
def sample_proposal():
    """Create a sample proposal."""
    return PlasticityProposal(
        id="prop_test_001",
        goal="Tune reasoning parameters",
        level=PlasticityLevel.WEIGHT_ADJUSTMENT,
        modification_type=ModificationType.WEIGHT_ADJUST,
        operation="modify_weight",
        parameters={"adjustment": 0.1},
        target_modules=["mod_reasoning_v1"],
        context={},
        rollback_plan=RollbackPlan(
            steps=["Restore previous values"],
            estimated_time_seconds=5.0
        )
    )


# ============================================================================
# Plasticity Level Tests
# ============================================================================

class TestPlasticityLevels:
    """Tests for plasticity level definitions."""

    def test_level_ordering(self):
        """Test that levels are ordered correctly."""
        assert PlasticityLevel.WEIGHT_ADJUSTMENT < PlasticityLevel.MODULE_CONFIGURATION
        assert PlasticityLevel.MODULE_CONFIGURATION < PlasticityLevel.MODULE_COMPOSITION
        assert PlasticityLevel.MODULE_COMPOSITION < PlasticityLevel.MODULE_DISCOVERY
        assert PlasticityLevel.MODULE_DISCOVERY < PlasticityLevel.META_ARCHITECTURE

    def test_level_values(self):
        """Test level numeric values."""
        assert PlasticityLevel.WEIGHT_ADJUSTMENT.value == 0
        assert PlasticityLevel.META_ARCHITECTURE.value == 4

    def test_get_level_requirements(self):
        """Test getting level requirements."""
        reqs = get_level_requirements(PlasticityLevel.MODULE_CONFIGURATION)
        assert reqs.min_successful_mods == 10
        assert reqs.min_success_rate == 0.8

    def test_is_operation_allowed_at_level(self):
        """Test operation permission checking."""
        # Weight adjustment operations at level 0
        assert is_operation_allowed(
            PlasticityLevel.WEIGHT_ADJUSTMENT,
            "modify_weight"
        ) == True

        # Module composition operation not at level 0
        assert is_operation_allowed(
            PlasticityLevel.WEIGHT_ADJUSTMENT,
            "compose_sequential"
        ) == False

        # Module composition operation at level 2
        assert is_operation_allowed(
            PlasticityLevel.MODULE_COMPOSITION,
            "compose_sequential"
        ) == True

    def test_operations_cumulative(self):
        """Test that higher levels include lower level operations."""
        # Level 2 should allow level 0 operations
        assert is_operation_allowed(
            PlasticityLevel.MODULE_COMPOSITION,
            "modify_weight"
        ) == True


class TestLevelProgress:
    """Tests for level progress tracking."""

    def test_record_attempt(self):
        """Test recording modification attempts."""
        progress = LevelProgress(level=PlasticityLevel.WEIGHT_ADJUSTMENT)

        progress.record_attempt(success=True)
        assert progress.successful_modifications == 1
        assert progress.total_attempts == 1

        progress.record_attempt(success=False)
        assert progress.failed_modifications == 1
        assert progress.total_attempts == 2

    def test_success_rate(self):
        """Test success rate calculation."""
        progress = LevelProgress(level=PlasticityLevel.WEIGHT_ADJUSTMENT)

        assert progress.success_rate == 0.0

        progress.record_attempt(success=True)
        progress.record_attempt(success=True)
        progress.record_attempt(success=False)

        assert progress.success_rate == pytest.approx(0.666, rel=0.01)

    def test_to_dict(self):
        """Test serialization."""
        progress = LevelProgress(level=PlasticityLevel.WEIGHT_ADJUSTMENT)
        progress.record_attempt(success=True)

        d = progress.to_dict()

        assert d['level'] == 0
        assert d['level_name'] == 'WEIGHT_ADJUSTMENT'
        assert d['successful_modifications'] == 1


class TestLevelAdvancement:
    """Tests for level advancement checks."""

    def test_cannot_advance_insufficient_mods(self):
        """Test advancement blocked with insufficient modifications."""
        progress = LevelProgress(level=PlasticityLevel.WEIGHT_ADJUSTMENT)
        progress.record_attempt(success=True)  # Only 1

        can, reason = can_advance_level(
            PlasticityLevel.WEIGHT_ADJUSTMENT,
            progress
        )

        assert can == False
        assert "modifications" in reason

    def test_cannot_advance_low_success_rate(self):
        """Test advancement blocked with low success rate."""
        progress = LevelProgress(level=PlasticityLevel.WEIGHT_ADJUSTMENT)

        # Add enough attempts but with low success rate
        for _ in range(10):
            progress.record_attempt(success=True)
        for _ in range(10):
            progress.record_attempt(success=False)  # 50% rate

        can, reason = can_advance_level(
            PlasticityLevel.WEIGHT_ADJUSTMENT,
            progress
        )

        assert can == False
        assert "success rate" in reason

    def test_can_advance_with_requirements(self):
        """Test advancement allowed when requirements met."""
        progress = LevelProgress(level=PlasticityLevel.WEIGHT_ADJUSTMENT)

        # Meet requirements for Level 1 (10 successful, 80% rate)
        for _ in range(12):
            progress.record_attempt(success=True)
        for _ in range(2):
            progress.record_attempt(success=False)

        can, reason = can_advance_level(
            PlasticityLevel.WEIGHT_ADJUSTMENT,
            progress
        )

        assert can == True

    def test_cannot_advance_at_max_level(self):
        """Test cannot advance beyond max level."""
        progress = LevelProgress(level=PlasticityLevel.META_ARCHITECTURE)
        progress.successful_modifications = 1000
        progress.total_attempts = 1000

        can, reason = can_advance_level(
            PlasticityLevel.META_ARCHITECTURE,
            progress
        )

        assert can == False
        assert "maximum level" in reason


# ============================================================================
# Proposal Generator Tests
# ============================================================================

class TestProposalGenerator:
    """Tests for proposal generation."""

    def test_generate_weight_adjustment(self, proposal_generator):
        """Test generating weight adjustment proposal."""
        proposal = proposal_generator.generate_proposal(
            goal="Tune the temperature parameter",
            current_level=PlasticityLevel.WEIGHT_ADJUSTMENT,
            context={},
            available_modules=["mod_1"]
        )

        assert proposal is not None
        assert proposal.modification_type == ModificationType.WEIGHT_ADJUST
        assert proposal.operation == "modify_weight"

    def test_generate_config_update(self, proposal_generator):
        """Test generating config update proposal."""
        proposal = proposal_generator.generate_proposal(
            goal="Update configuration settings",
            current_level=PlasticityLevel.WEIGHT_ADJUSTMENT,
            context={},
            available_modules=["mod_1"]
        )

        assert proposal is not None
        assert proposal.modification_type == ModificationType.CONFIG_UPDATE

    def test_generate_module_composition(self, proposal_generator):
        """Test generating composition proposal."""
        proposal = proposal_generator.generate_proposal(
            goal="Combine reasoning and memory modules",
            current_level=PlasticityLevel.MODULE_COMPOSITION,
            context={'target_modules': ['mod_1', 'mod_2']},
            available_modules=["mod_1", "mod_2"]
        )

        assert proposal is not None
        assert proposal.modification_type == ModificationType.MODULE_COMPOSE

    def test_operation_not_allowed_at_level(self, proposal_generator):
        """Test that disallowed operations return None."""
        proposal = proposal_generator.generate_proposal(
            goal="Combine modules together",  # Level 2 operation
            current_level=PlasticityLevel.WEIGHT_ADJUSTMENT,  # Level 0
            context={},
            available_modules=["mod_1"]
        )

        assert proposal is None

    def test_rollback_plan_generated(self, proposal_generator):
        """Test that proposals include rollback plans."""
        proposal = proposal_generator.generate_proposal(
            goal="Adjust weights",
            current_level=PlasticityLevel.WEIGHT_ADJUSTMENT,
            context={},
            available_modules=["mod_1"]
        )

        assert proposal.rollback_plan is not None
        assert len(proposal.rollback_plan.steps) > 0


# ============================================================================
# Executor Tests
# ============================================================================

class TestModificationExecutor:
    """Tests for modification execution."""

    @pytest.mark.asyncio
    async def test_execute_weight_adjustment(self, executor, sample_proposal):
        """Test executing a weight adjustment."""
        result = await executor.execute(sample_proposal)

        assert result.success == True
        assert len(result.changes_made) > 0

    @pytest.mark.asyncio
    async def test_checkpoint_created(self, executor, sample_proposal):
        """Test that checkpoint is created before execution."""
        await executor.execute(sample_proposal)

        # Should have at least one checkpoint
        assert executor.get_stats()['checkpoints_count'] >= 1

    @pytest.mark.asyncio
    async def test_dry_run(self, executor, sample_proposal):
        """Test dry run execution."""
        result = await executor.execute(sample_proposal, dry_run=True)

        assert result.success == True
        # Dry run simulates changes without executing
        assert "Would modify" in result.changes_made[0]

    @pytest.mark.asyncio
    async def test_rollback_on_failure(self, executor, sample_proposal):
        """Test rollback is triggered on failure."""
        # Make the handler fail
        async def failing_handler(proposal):
            raise RuntimeError("Intentional failure")

        executor.register_handler(
            ModificationType.WEIGHT_ADJUST,
            failing_handler
        )

        result = await executor.execute(sample_proposal)

        assert result.success == False
        assert result.rollback_triggered == True

    def test_get_stats(self, executor):
        """Test executor statistics."""
        stats = executor.get_stats()

        assert 'executions_count' in stats
        assert 'successful_executions' in stats
        assert 'rollbacks_triggered' in stats

    @pytest.mark.asyncio
    async def test_reset(self, executor, sample_proposal):
        """Test executor reset."""
        await executor.execute(sample_proposal)
        assert executor.get_stats()['executions_count'] == 1

        executor.reset()

        assert executor.get_stats()['executions_count'] == 0


# ============================================================================
# Plasticity Engine Tests
# ============================================================================

class TestCognitivePlasticityEngine:
    """Tests for the main plasticity engine."""

    def test_initial_level(self, engine):
        """Test engine starts at Level 0."""
        assert engine.current_level == PlasticityLevel.WEIGHT_ADJUSTMENT

    @pytest.mark.asyncio
    async def test_propose_modification(self, engine):
        """Test generating a modification proposal."""
        proposal = await engine.propose_modification(
            goal="Tune reasoning parameters",
            context={}
        )

        assert proposal is not None
        assert proposal.level == PlasticityLevel.WEIGHT_ADJUSTMENT

    @pytest.mark.asyncio
    async def test_execute_modification(self, engine, sample_proposal):
        """Test executing a modification."""
        result = await engine.execute_modification(sample_proposal)

        assert result.success == True

    @pytest.mark.asyncio
    async def test_propose_and_execute(self, engine):
        """Test propose and execute in one step."""
        proposal, result = await engine.propose_and_execute(
            goal="Adjust temperature",
            context={}
        )

        assert proposal is not None
        assert result is not None

    @pytest.mark.asyncio
    async def test_level_progress_tracked(self, engine):
        """Test that level progress is tracked."""
        proposal = await engine.propose_modification("Tune weights")
        await engine.execute_modification(proposal)

        progress = engine.level_progress[PlasticityLevel.WEIGHT_ADJUSTMENT]
        assert progress.total_attempts >= 1

    @pytest.mark.asyncio
    async def test_advance_level(self, engine):
        """Test level advancement."""
        # Simulate many successful modifications
        engine._level_progress[PlasticityLevel.WEIGHT_ADJUSTMENT].successful_modifications = 15
        engine._level_progress[PlasticityLevel.WEIGHT_ADJUSTMENT].total_attempts = 16

        success, reason = await engine.advance_level()

        assert success == True
        assert engine.current_level == PlasticityLevel.MODULE_CONFIGURATION

    @pytest.mark.asyncio
    async def test_cannot_advance_without_progress(self, engine):
        """Test cannot advance without sufficient progress."""
        success, reason = await engine.advance_level()

        assert success == False
        assert "modifications" in reason or "rate" in reason

    @pytest.mark.asyncio
    async def test_check_level_progress(self, engine):
        """Test level progress checking."""
        progress = await engine.check_level_progress()

        assert 'current_level' in progress
        assert 'can_advance' in progress
        assert 'requirements' in progress

    def test_get_level_info(self, engine):
        """Test getting level information."""
        info = engine.get_level_info()

        assert info['level'] == 0
        assert 'allowed_operations' in info

    def test_get_all_levels_info(self, engine):
        """Test getting all levels information."""
        all_info = engine.get_all_levels_info()

        assert len(all_info) == 5

    @pytest.mark.asyncio
    async def test_pending_proposals_tracked(self, engine):
        """Test pending proposals are tracked."""
        proposal = await engine.propose_modification("Test goal")

        pending = engine.get_pending_proposals()
        assert len(pending) >= 1

    def test_get_state(self, engine):
        """Test getting engine state."""
        state = engine.get_state()

        assert isinstance(state, EngineState)
        assert state.current_level == PlasticityLevel.WEIGHT_ADJUSTMENT

    def test_get_stats(self, engine):
        """Test engine statistics."""
        stats = engine.get_stats()

        assert 'current_level' in stats
        assert 'total_modifications' in stats
        assert 'levels_unlocked' in stats

    @pytest.mark.asyncio
    async def test_reset(self, engine):
        """Test engine reset."""
        proposal = await engine.propose_modification("Test")
        await engine.execute_modification(proposal)

        engine.reset()

        assert engine.current_level == PlasticityLevel.WEIGHT_ADJUSTMENT
        assert engine.get_stats()['total_modifications'] == 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestPlasticityIntegration:
    """Integration tests for plasticity system."""

    @pytest.mark.asyncio
    async def test_full_modification_cycle(self, engine):
        """Test complete modification cycle."""
        # Propose
        proposal = await engine.propose_modification(
            goal="Tune reasoning weights",
            context={'desire_id': 'des_001'}
        )
        assert proposal is not None
        assert proposal.provenance_id == 'des_001'

        # Execute
        result = await engine.execute_modification(proposal)
        assert result.success == True

        # Progress updated
        progress = engine.level_progress[PlasticityLevel.WEIGHT_ADJUSTMENT]
        assert progress.successful_modifications >= 1

    @pytest.mark.asyncio
    async def test_rejection_for_unsafe_operation(self, engine, mock_governance):
        """Test that unsafe operations are rejected."""
        # Make governance reject
        mock_governance.evaluate_and_approve = AsyncMock(return_value=(
            MagicMock(can_proceed=False, blocking_issues=["Unsafe"]),
            None
        ))

        proposal = await engine.propose_modification("Tune weights")
        result = await engine.execute_modification(proposal)

        assert result.success == False
        assert "Blocked" in result.error


class TestProposalSerialization:
    """Tests for proposal serialization."""

    def test_proposal_to_dict(self, sample_proposal):
        """Test PlasticityProposal serialization."""
        d = sample_proposal.to_dict()

        assert d['id'] == "prop_test_001"
        assert d['level'] == 0
        assert d['modification_type'] == "weight_adjust"
        assert d['rollback_plan'] is not None

    def test_result_to_dict(self):
        """Test ModificationResult serialization."""
        result = ModificationResult(
            success=True,
            proposal_id="prop_001",
            changes_made=["Changed A", "Changed B"]
        )

        d = result.to_dict()

        assert d['success'] == True
        assert len(d['changes_made']) == 2
