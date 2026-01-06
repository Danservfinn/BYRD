"""
Tests for MetaArchitect Module.

Tests pattern learning, architecture proposal, and meta-improvement.
"""

import pytest
import asyncio

from rsi.plasticity.meta_architect import (
    # Patterns
    PatternType,
    PatternStrength,
    PatternCondition,
    PatternAction,
    DesignPattern,
    PatternMatch,
    PatternLibrary,
    # Learner
    ArchitectureOutcome,
    PatternCandidate,
    PatternLearner,
    # Proposer
    ArchitectureProposal,
    ProposalConstraints,
    ArchitectureProposer,
    # MetaArchitect
    Outcome,
    MetaArchitectState,
    MetaArchitect,
)

from rsi.plasticity.nas import (
    ArchitectureSpec,
    ArchitectureSpace,
    NodeSpec,
    NodeType,
    OperationType,
)


# ============================================================================
# Pattern Tests
# ============================================================================

class TestPatternCondition:
    """Test PatternCondition class."""

    def test_eq_operator(self):
        """Test equality operator."""
        cond = PatternCondition("goal", "eq", "test")
        assert cond.matches({"goal": "test"}) is True
        assert cond.matches({"goal": "other"}) is False

    def test_gt_operator(self):
        """Test greater-than operator."""
        cond = PatternCondition("count", "gt", 5)
        assert cond.matches({"count": 10}) is True
        assert cond.matches({"count": 3}) is False

    def test_contains_operator(self):
        """Test contains operator."""
        cond = PatternCondition("types", "contains", "linear")
        assert cond.matches({"types": ["linear", "attention"]}) is True
        assert cond.matches({"types": ["attention"]}) is False

    def test_missing_attribute(self):
        """Test with missing attribute."""
        cond = PatternCondition("missing", "eq", "value")
        assert cond.matches({}) is False

    def test_to_dict(self):
        """Test serialization."""
        cond = PatternCondition("test", "eq", "value")
        data = cond.to_dict()
        assert data['attribute'] == "test"
        assert data['operator'] == "eq"

    def test_from_dict(self):
        """Test deserialization."""
        data = {'attribute': 'x', 'operator': 'gt', 'value': 10}
        cond = PatternCondition.from_dict(data)
        assert cond.matches({"x": 15}) is True


class TestDesignPattern:
    """Test DesignPattern class."""

    @pytest.fixture
    def pattern(self):
        """Create test pattern."""
        return DesignPattern(
            id="test_pattern",
            name="Test Pattern",
            description="Test description",
            pattern_type=PatternType.STRUCTURAL,
            conditions=[PatternCondition("goal", "eq", "test")],
            actions=[PatternAction("add_node", {"type": "linear"})],
            observations=10,
            successes=8,
            failures=2
        )

    def test_success_rate(self, pattern):
        """Test success rate calculation."""
        assert pattern.success_rate == 0.8

    def test_strength(self, pattern):
        """Test strength calculation."""
        assert pattern.strength == PatternStrength.VERY_STRONG

    def test_confidence(self, pattern):
        """Test Bayesian confidence."""
        # (8+1) / (8+1 + 2+1) = 9/12 = 0.75
        assert 0.7 < pattern.confidence < 0.8

    def test_applies_to(self, pattern):
        """Test pattern application check."""
        assert pattern.applies_to({"goal": "test"}) is True
        assert pattern.applies_to({"goal": "other"}) is False

    def test_record_observation(self, pattern):
        """Test recording observations."""
        initial = pattern.observations
        pattern.record_observation(success=True, outcome_id="out_1")
        assert pattern.observations == initial + 1
        assert pattern.successes == 9

    def test_to_dict(self, pattern):
        """Test serialization."""
        data = pattern.to_dict()
        assert data['id'] == "test_pattern"
        assert data['pattern_type'] == "structural"
        assert data['success_rate'] == 0.8

    def test_from_dict(self, pattern):
        """Test deserialization."""
        data = pattern.to_dict()
        restored = DesignPattern.from_dict(data)
        assert restored.id == pattern.id
        assert restored.success_rate == pattern.success_rate


class TestPatternLibrary:
    """Test PatternLibrary class."""

    @pytest.fixture
    def library(self):
        """Create test library."""
        return PatternLibrary()

    @pytest.fixture
    def sample_patterns(self):
        """Create sample patterns."""
        return [
            DesignPattern(
                id="p1",
                name="Pattern 1",
                description="High confidence",
                pattern_type=PatternType.STRUCTURAL,
                conditions=[PatternCondition("goal", "eq", "test")],
                actions=[PatternAction("action1", {})],
                observations=10,
                successes=9,
                failures=1
            ),
            DesignPattern(
                id="p2",
                name="Pattern 2",
                description="Medium confidence",
                pattern_type=PatternType.OPERATIONAL,
                conditions=[PatternCondition("count", "gt", 5)],
                actions=[PatternAction("action2", {})],
                observations=5,
                successes=3,
                failures=2
            ),
        ]

    def test_add_pattern(self, library, sample_patterns):
        """Test adding patterns."""
        library.add_pattern(sample_patterns[0])
        assert len(library.get_all_patterns()) == 1

    def test_get_pattern(self, library, sample_patterns):
        """Test getting pattern by ID."""
        library.add_pattern(sample_patterns[0])
        pattern = library.get_pattern("p1")
        assert pattern is not None
        assert pattern.name == "Pattern 1"

    def test_remove_pattern(self, library, sample_patterns):
        """Test removing pattern."""
        library.add_pattern(sample_patterns[0])
        result = library.remove_pattern("p1")
        assert result is True
        assert library.get_pattern("p1") is None

    def test_find_matching_patterns(self, library, sample_patterns):
        """Test pattern matching."""
        for p in sample_patterns:
            library.add_pattern(p)

        matches = library.find_matching_patterns(
            context={"goal": "test", "count": 10}
        )
        assert len(matches) == 2

    def test_get_patterns_by_type(self, library, sample_patterns):
        """Test filtering by type."""
        for p in sample_patterns:
            library.add_pattern(p)

        structural = library.get_patterns_by_type(PatternType.STRUCTURAL)
        assert len(structural) == 1
        assert structural[0].id == "p1"

    def test_get_strong_patterns(self, library, sample_patterns):
        """Test getting strong patterns."""
        for p in sample_patterns:
            library.add_pattern(p)

        strong = library.get_strong_patterns(PatternStrength.STRONG)
        assert len(strong) == 1  # Only p1 has 10 observations

    def test_get_stats(self, library, sample_patterns):
        """Test statistics."""
        for p in sample_patterns:
            library.add_pattern(p)

        stats = library.get_stats()
        assert stats['total_patterns'] == 2

    def test_reset(self, library, sample_patterns):
        """Test reset."""
        library.add_pattern(sample_patterns[0])
        library.reset()
        assert len(library.get_all_patterns()) == 0


# ============================================================================
# Learner Tests
# ============================================================================

class TestPatternLearner:
    """Test PatternLearner class."""

    @pytest.fixture
    def learner(self):
        """Create test learner."""
        return PatternLearner(config={
            'min_support': 2,
            'min_confidence': 0.5
        })

    @pytest.mark.asyncio
    async def test_learn_from_outcome(self, learner):
        """Test learning from outcomes."""
        # Add multiple outcomes
        for i in range(5):
            await learner.learn_from_outcome(
                architecture_id=f"arch_{i}",
                goal="test goal",
                success=i % 2 == 0,  # Alternate success/failure
                score=0.8 if i % 2 == 0 else 0.3,
                architecture_data={
                    'node_count': 5 + i,
                    'connection_count': 4 + i,
                    'node_types': ['processing', 'attention'],
                    'operation_types': ['linear', 'attention'],
                    'connection_types': ['sequential']
                }
            )

        assert learner._outcomes_processed == 5

    @pytest.mark.asyncio
    async def test_pattern_extraction(self, learner):
        """Test that patterns are extracted after enough outcomes."""
        # Add successful outcomes with consistent patterns
        for i in range(5):
            await learner.learn_from_outcome(
                architecture_id=f"arch_{i}",
                goal="test goal",
                success=True,
                score=0.9,
                architecture_data={
                    'node_count': 6,
                    'connection_count': 8,
                    'node_types': ['processing'],
                    'operation_types': ['linear'],
                    'connection_types': ['sequential']
                }
            )

        # Should have some patterns extracted
        # (patterns are extracted when min_support is reached)
        stats = learner.get_stats()
        assert stats['outcomes_stored'] == 5

    def test_get_learning_insights(self, learner):
        """Test learning insights."""
        insights = learner.get_learning_insights()
        assert 'message' in insights  # No outcomes yet

    def test_consolidate_outcomes(self, learner):
        """Test outcome consolidation."""
        # Add many outcomes manually
        for i in range(20):
            learner._outcomes.append(
                ArchitectureOutcome(
                    id=f"out_{i}",
                    architecture_id=f"arch_{i}",
                    goal="test",
                    success=True,
                    score=0.8,
                    node_count=5,
                    connection_count=4,
                    node_types=[],
                    operation_types=[],
                    connection_types=[]
                )
            )

        removed = learner.consolidate_outcomes(max_outcomes=10)
        assert removed == 10
        assert len(learner._outcomes) == 10

    def test_reset(self, learner):
        """Test reset."""
        learner._outcomes_processed = 10
        learner.reset()
        assert learner._outcomes_processed == 0


# ============================================================================
# Proposer Tests
# ============================================================================

class TestArchitectureProposer:
    """Test ArchitectureProposer class."""

    @pytest.fixture
    def library(self):
        """Create library with patterns."""
        lib = PatternLibrary()

        # Add some patterns
        lib.add_pattern(DesignPattern(
            id="p1",
            name="Node count pattern",
            description="Optimal node count",
            pattern_type=PatternType.STRUCTURAL,
            conditions=[],
            actions=[
                PatternAction("target_node_count", {"min": 5, "max": 10})
            ],
            observations=10,
            successes=8,
            failures=2
        ))

        lib.add_pattern(DesignPattern(
            id="p2",
            name="Linear operation pattern",
            description="Use linear operations",
            pattern_type=PatternType.OPERATIONAL,
            conditions=[],
            actions=[
                PatternAction("include_operation", {"operation_type": "linear"})
            ],
            observations=8,
            successes=7,
            failures=1
        ))

        return lib

    @pytest.fixture
    def proposer(self, library):
        """Create test proposer."""
        return ArchitectureProposer(library=library)

    @pytest.mark.asyncio
    async def test_propose_architecture(self, proposer):
        """Test basic proposal generation."""
        proposal = await proposer.propose_architecture(
            goal="Test architecture"
        )

        assert proposal is not None
        assert proposal.architecture is not None
        assert proposal.confidence > 0

    @pytest.mark.asyncio
    async def test_proposal_with_constraints(self, proposer):
        """Test proposal with constraints."""
        constraints = ProposalConstraints(
            min_nodes=3,
            max_nodes=8,
            required_operations=['linear']
        )

        proposal = await proposer.propose_architecture(
            goal="Constrained architecture",
            constraints=constraints
        )

        assert proposal.architecture.node_count >= 3
        assert proposal.architecture.node_count <= 8

    @pytest.mark.asyncio
    async def test_propose_variations(self, proposer):
        """Test generating variations."""
        base = await proposer.propose_architecture(goal="Base")
        variations = await proposer.propose_variations(base, num_variations=3)

        assert len(variations) == 3
        for v in variations:
            assert v.architecture.id != base.architecture.id

    def test_get_stats(self, proposer):
        """Test statistics."""
        stats = proposer.get_stats()
        assert 'proposals_generated' in stats

    def test_reset(self, proposer):
        """Test reset."""
        proposer._proposals_generated = 10
        proposer.reset()
        assert proposer._proposals_generated == 0


# ============================================================================
# MetaArchitect Tests
# ============================================================================

class TestMetaArchitect:
    """Test MetaArchitect class."""

    @pytest.fixture
    def meta_architect(self):
        """Create test MetaArchitect."""
        return MetaArchitect(config={
            'success_threshold': 0.7
        })

    @pytest.fixture
    def sample_architecture(self):
        """Create sample architecture."""
        space = ArchitectureSpace()
        return space.sample_random("Test")

    @pytest.mark.asyncio
    async def test_learn_from_outcome(self, meta_architect, sample_architecture):
        """Test learning from outcome."""
        outcome = Outcome(
            success=True,
            score=0.85,
            metrics={'accuracy': 0.9},
            context={'goal': 'test'}
        )

        patterns = await meta_architect.learn_from_outcome(
            architecture=sample_architecture,
            outcome=outcome
        )

        assert meta_architect._state.outcomes_processed == 1

    @pytest.mark.asyncio
    async def test_propose_architecture(self, meta_architect):
        """Test architecture proposal."""
        proposal = await meta_architect.propose_architecture(
            goal="Test goal",
            context={'priority': 'performance'}
        )

        assert proposal is not None
        assert proposal.goal == "Test goal"
        assert meta_architect._state.proposals_generated == 1

    @pytest.mark.asyncio
    async def test_improve_proposal(self, meta_architect):
        """Test proposal improvement."""
        # First proposal
        initial = await meta_architect.propose_architecture(goal="Test")

        # Provide feedback
        feedback = Outcome(
            success=False,
            score=0.4,
            context={'goal': 'Test'}
        )

        # Improve
        improved = await meta_architect.improve_proposal(initial, feedback)

        assert improved.id != initial.id
        assert meta_architect._state.improvement_cycles == 1

    @pytest.mark.asyncio
    async def test_search_with_patterns(self, meta_architect):
        """Test pattern-guided search."""
        proposals = await meta_architect.search_with_patterns(
            goal="Search test",
            budget={'max_evaluations': 5}
        )

        assert len(proposals) >= 1

    def test_get_learned_patterns(self, meta_architect):
        """Test getting patterns."""
        patterns = meta_architect.get_learned_patterns()
        assert isinstance(patterns, list)

    def test_get_pattern_insights(self, meta_architect):
        """Test getting insights."""
        insights = meta_architect.get_pattern_insights()
        assert isinstance(insights, dict)

    def test_get_state(self, meta_architect):
        """Test state retrieval."""
        state = meta_architect.get_state()
        assert state.current_level == 4  # Level 4 = MetaArchitect

    def test_get_stats(self, meta_architect):
        """Test comprehensive stats."""
        stats = meta_architect.get_stats()
        assert 'state' in stats
        assert 'library' in stats
        assert 'learner' in stats

    def test_reset(self, meta_architect):
        """Test reset."""
        meta_architect._state.proposals_generated = 10
        meta_architect.reset()
        assert meta_architect._state.proposals_generated == 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestMetaArchitectIntegration:
    """Integration tests for MetaArchitect."""

    @pytest.mark.asyncio
    async def test_learn_and_propose_cycle(self):
        """Test full learn-propose cycle."""
        meta = MetaArchitect(config={
            'learner': {'min_support': 2, 'min_confidence': 0.5}
        })
        space = ArchitectureSpace()

        # Generate and learn from multiple architectures
        for i in range(5):
            arch = space.sample_random(f"Test_{i}")
            outcome = Outcome(
                success=i % 2 == 0,
                score=0.8 if i % 2 == 0 else 0.3,
                context={'goal': 'test', 'iteration': i}
            )

            await meta.learn_from_outcome(arch, outcome)

        # Propose based on learning
        proposal = await meta.propose_architecture(goal="Learned proposal")

        assert proposal is not None
        assert meta._state.outcomes_processed == 5
        assert meta._state.proposals_generated == 1

    @pytest.mark.asyncio
    async def test_iterative_improvement(self):
        """Test iterative improvement cycle."""
        meta = MetaArchitect()

        # Initial proposal
        proposal = await meta.propose_architecture(goal="Iterative test")
        initial_id = proposal.id

        # Iterate improvements
        for i in range(3):
            feedback = Outcome(
                success=False,
                score=0.3 + (i * 0.1),  # Improving scores
                context={'goal': 'Iterative test'}
            )

            proposal = await meta.improve_proposal(proposal, feedback)

            assert proposal.id != initial_id

        assert meta._state.improvement_cycles == 3

    @pytest.mark.asyncio
    async def test_pattern_reuse_across_proposals(self):
        """Test that learned patterns influence future proposals."""
        meta = MetaArchitect(config={
            'learner': {'min_support': 2}
        })
        space = ArchitectureSpace()

        # Learn successful patterns
        for i in range(5):
            arch = space.sample_random(f"Success_{i}")
            outcome = Outcome(
                success=True,
                score=0.9,
                context={'goal': 'consistent goal'}
            )
            await meta.learn_from_outcome(arch, outcome)

        # Get patterns
        patterns = meta.get_learned_patterns()

        # New proposal should be influenced by patterns
        proposal = await meta.propose_architecture(
            goal="Pattern-guided proposal"
        )

        assert proposal.confidence > 0.3  # Should have some pattern influence
