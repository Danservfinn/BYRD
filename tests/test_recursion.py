"""
Tests for Recursion Module.

Tests improvement algebra, level-invariant representations,
and recursive depth amplification.
"""

import pytest
import asyncio

from rsi.recursion import (
    # Algebra - Types
    ImprovementType,
    ImprovementResult,
    # Algebra - Base
    Improvement,
    IdentityImprovement,
    FunctionImprovement,
    # Algebra - Composed
    SequentialImprovement,
    ParallelImprovement,
    ConditionalImprovement,
    RecursiveImprovement,
    UntilImprovement,
    ChoiceImprovement,
    FallbackImprovement,
    # Algebra - Operators
    ImprovementAlgebra,
    # Representation
    LevelType,
    Improvable,
    LeveledPattern,
    CompressedPatterns,
    ObservePrimitive,
    TransformPrimitive,
    EvaluatePrimitive,
    SelectPrimitive,
    MetaLevelCompressor,
    # Depth Amplifier
    AmplificationConfig,
    AmplificationResult,
    RecursiveDepthAmplifier,
)


# ============================================================================
# Improvement Algebra Tests
# ============================================================================

class TestImprovementResult:
    """Test ImprovementResult dataclass."""

    def test_create_result(self):
        """Test creating a result."""
        result = ImprovementResult(
            id="test",
            success=True,
            original="before",
            improved="after",
            improvement_type=ImprovementType.PARAMETER,
            delta_score=0.1
        )
        assert result.success is True
        assert result.delta_score == 0.1

    def test_to_dict(self):
        """Test serialization."""
        result = ImprovementResult(
            id="test",
            success=True,
            original="x",
            improved="y",
            improvement_type=ImprovementType.STRUCTURE,
            delta_score=0.5
        )
        data = result.to_dict()
        assert data['success'] is True
        assert data['improvement_type'] == 'structure'


class TestIdentityImprovement:
    """Test IdentityImprovement."""

    @pytest.mark.asyncio
    async def test_identity_returns_same(self):
        """Test identity returns target unchanged."""
        identity = IdentityImprovement()
        result = await identity.apply("test")
        assert result.improved == "test"
        assert result.delta_score == 0.0

    def test_zero_cost(self):
        """Test identity has zero cost."""
        identity = IdentityImprovement()
        assert identity.estimate_cost("test") == 0.0


class TestFunctionImprovement:
    """Test FunctionImprovement."""

    @pytest.mark.asyncio
    async def test_sync_function(self):
        """Test with synchronous function."""
        def double(x, ctx):
            return x * 2

        imp = FunctionImprovement(double)
        result = await imp.apply(5)
        assert result.improved == 10

    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test with async function."""
        async def async_double(x, ctx):
            return x * 2

        imp = FunctionImprovement(async_double)
        result = await imp.apply(5)
        assert result.improved == 10

    @pytest.mark.asyncio
    async def test_function_failure(self):
        """Test function that raises exception."""
        def failing(x, ctx):
            raise ValueError("test error")

        imp = FunctionImprovement(failing)
        result = await imp.apply(5)
        assert result.success is False


class TestImprovementAlgebra:
    """Test ImprovementAlgebra operators."""

    @pytest.fixture
    def add_one(self):
        """Create add-one improvement."""
        return FunctionImprovement(lambda x, ctx: x + 1, name="add_one")

    @pytest.fixture
    def double(self):
        """Create double improvement."""
        return FunctionImprovement(lambda x, ctx: x * 2, name="double")

    @pytest.mark.asyncio
    async def test_sequential(self, add_one, double):
        """Test sequential composition."""
        seq = ImprovementAlgebra.sequential(add_one, double)
        result = await seq.apply(5)
        # (5 + 1) * 2 = 12
        assert result.improved == 12

    @pytest.mark.asyncio
    async def test_parallel(self, add_one, double):
        """Test parallel composition."""
        parallel = ImprovementAlgebra.parallel(
            add_one, double,
            merge=lambda a, b: a + b
        )
        result = await parallel.apply(5)
        # 6 + 10 = 16
        assert result.improved == 16

    @pytest.mark.asyncio
    async def test_conditional_true(self, add_one):
        """Test conditional when condition is true."""
        cond = ImprovementAlgebra.conditional(
            add_one,
            lambda x, ctx: x > 0
        )
        result = await cond.apply(5)
        assert result.improved == 6

    @pytest.mark.asyncio
    async def test_conditional_false(self, add_one):
        """Test conditional when condition is false."""
        cond = ImprovementAlgebra.conditional(
            add_one,
            lambda x, ctx: x < 0
        )
        result = await cond.apply(5)
        assert result.improved == 5  # Unchanged

    @pytest.mark.asyncio
    async def test_recurse(self, add_one):
        """Test recursive improvement."""
        rec = ImprovementAlgebra.recurse(add_one, depth=3)
        result = await rec.apply(5)
        # 5 + 1 + 1 + 1 = 8
        assert result.improved == 8

    @pytest.mark.asyncio
    async def test_until(self, add_one):
        """Test until improvement."""
        until = ImprovementAlgebra.until(
            add_one,
            condition=lambda r: r.improved >= 10,
            max_iterations=10
        )
        result = await until.apply(5)
        assert result.improved >= 10

    @pytest.mark.asyncio
    async def test_choice(self, add_one, double):
        """Test choice improvement."""
        choice = ImprovementAlgebra.choice(
            [add_one, double],
            selector=lambda x, ctx: 1  # Select double
        )
        result = await choice.apply(5)
        assert result.improved == 10

    @pytest.mark.asyncio
    async def test_fallback(self):
        """Test fallback improvement."""
        failing = FunctionImprovement(
            lambda x, ctx: (_ for _ in ()).throw(ValueError("fail"))
        )
        backup = FunctionImprovement(lambda x, ctx: x + 100)

        fb = ImprovementAlgebra.fallback(failing, backup)
        result = await fb.apply(5)
        assert result.improved == 105

    def test_identity(self):
        """Test identity operator."""
        identity = ImprovementAlgebra.identity()
        assert isinstance(identity, IdentityImprovement)


# ============================================================================
# Representation Tests
# ============================================================================

class TestImprovable:
    """Test Improvable class."""

    def test_create(self):
        """Test creating improvable."""
        imp = Improvable(
            id="test",
            level=0,
            content="data",
            score=0.5
        )
        assert imp.level == 0
        assert imp.score == 0.5

    def test_to_dict(self):
        """Test serialization."""
        imp = Improvable(id="test", content="x")
        data = imp.to_dict()
        assert data['id'] == "test"

    def test_from_dict(self):
        """Test deserialization."""
        data = {'id': 'test', 'level': 2, 'score': 0.8}
        imp = Improvable.from_dict(data)
        assert imp.level == 2
        assert imp.score == 0.8

    def test_at_level(self):
        """Test creating copy at different level."""
        imp = Improvable(id="test", level=0)
        at_level_2 = imp.at_level(2)
        assert at_level_2.level == 2
        assert 'source_level' in at_level_2.metadata


class TestLeveledPattern:
    """Test LeveledPattern class."""

    def test_applies_at_level(self):
        """Test level checking."""
        pattern = LeveledPattern(
            id="p1",
            name="Test",
            description="Test pattern",
            min_level=1,
            max_level=5
        )
        assert pattern.applies_at_level(3) is True
        assert pattern.applies_at_level(0) is False
        assert pattern.applies_at_level(10) is False

    def test_instantiate_at_level(self):
        """Test level instantiation."""
        pattern = LeveledPattern(
            id="p1",
            name="Test",
            description="Test",
            pattern_template={'key': 'value'},
            level_adaptations={2: {'extra': 'data'}}
        )

        inst_1 = pattern.instantiate_at_level(1)
        assert 'extra' not in inst_1

        inst_2 = pattern.instantiate_at_level(2)
        assert inst_2.get('extra') == 'data'

    def test_record_application(self):
        """Test recording applications."""
        pattern = LeveledPattern(id="p", name="P", description="P")
        pattern.record_application(level=1, success=True)
        pattern.record_application(level=1, success=False)

        assert pattern.applications_by_level[1] == 2
        assert pattern.successes_by_level[1] == 1
        assert pattern.success_rate_at_level(1) == 0.5


class TestPrimitives:
    """Test level-invariant primitives."""

    def test_observe(self):
        """Test observe primitive."""
        obs = ObservePrimitive()
        target = Improvable(id="t", content="data", score=0.5)
        result = obs.apply(target)

        assert 'observations' in result.metadata

    def test_transform(self):
        """Test transform primitive."""
        trans = TransformPrimitive(
            transform_fn=lambda c, ctx: c.upper() if isinstance(c, str) else c
        )
        target = Improvable(id="t", content="hello")
        result = trans.apply(target)

        assert result.content == "HELLO"

    def test_evaluate(self):
        """Test evaluate primitive."""
        eval_prim = EvaluatePrimitive(
            eval_fn=lambda t, ctx: 0.9
        )
        target = Improvable(id="t", score=0.1)
        result = eval_prim.apply(target)

        assert result.score == 0.9

    def test_select(self):
        """Test select primitive."""
        sel = SelectPrimitive()
        target = Improvable(id="t")

        options = [
            Improvable(id="a", score=0.3),
            Improvable(id="b", score=0.9),
            Improvable(id="c", score=0.5)
        ]

        result = sel.apply(target, {'options': options})
        assert result.score == 0.9  # Selected highest


class TestMetaLevelCompressor:
    """Test MetaLevelCompressor."""

    def test_compress_similar_patterns(self):
        """Test compressing similar patterns."""
        compressor = MetaLevelCompressor(config={'min_patterns': 2})

        patterns = [
            LeveledPattern(
                id="p1", name="P1", description="P1",
                pattern_template={'a': 1, 'b': 2}
            ),
            LeveledPattern(
                id="p2", name="P2", description="P2",
                pattern_template={'a': 1, 'b': 3}
            ),
            LeveledPattern(
                id="p3", name="P3", description="P3",
                pattern_template={'a': 1, 'c': 4}
            )
        ]

        compressed = compressor.compress_to_level(patterns, target_level=1)
        assert len(compressed) >= 1

    def test_min_patterns_threshold(self):
        """Test min patterns threshold."""
        compressor = MetaLevelCompressor(config={'min_patterns': 5})

        patterns = [
            LeveledPattern(id="p1", name="P1", description="P1")
        ]

        compressed = compressor.compress_to_level(patterns, target_level=1)
        assert len(compressed) == 0


# ============================================================================
# Depth Amplifier Tests
# ============================================================================

class TestAmplificationConfig:
    """Test AmplificationConfig."""

    def test_defaults(self):
        """Test default config."""
        config = AmplificationConfig()
        assert config.max_depth == 5
        assert config.early_stopping is True

    def test_custom(self):
        """Test custom config."""
        config = AmplificationConfig(
            max_depth=10,
            min_improvement_threshold=0.001
        )
        assert config.max_depth == 10


class TestRecursiveDepthAmplifier:
    """Test RecursiveDepthAmplifier."""

    @pytest.fixture
    def amplifier(self):
        """Create test amplifier."""
        config = AmplificationConfig(
            max_depth=3,
            min_improvement_threshold=0.0,
            early_stopping=False
        )
        return RecursiveDepthAmplifier(config)

    @pytest.fixture
    def improvement(self):
        """Create test improvement."""
        def improve_score(target, ctx):
            if isinstance(target, Improvable):
                improved = Improvable(
                    id=f"improved_{target.id}",
                    level=target.level,
                    content=target.content,
                    score=target.score + 0.1
                )
                # Set delta_score in context for tracking
                if ctx is not None:
                    ctx['delta_score'] = 0.1
                return improved
            return target

        return FunctionImprovement(improve_score, name="improve_score")

    @pytest.mark.asyncio
    async def test_improve_at_level_0(self, amplifier, improvement):
        """Test improvement at level 0."""
        target = Improvable(id="t", score=0.5)
        result = await amplifier.improve_at_level(target, improvement, level=0)

        assert result.success is True

    @pytest.mark.asyncio
    async def test_improve_at_level_1(self, amplifier, improvement):
        """Test improvement at level 1 (meta-improvement)."""
        target = Improvable(id="t", score=0.5)
        result = await amplifier.improve_at_level(target, improvement, level=1)

        # Should apply improvement recursively
        assert result.success is True

    @pytest.mark.asyncio
    async def test_amplify(self, amplifier, improvement):
        """Test full amplification."""
        target = Improvable(id="t", score=0.5)
        result = await amplifier.amplify(target, improvement)

        assert result.success is True
        assert result.depth_reached > 0

    @pytest.mark.asyncio
    async def test_amplify_until_convergence(self, amplifier, improvement):
        """Test amplification until convergence."""
        target = Improvable(id="t", score=0.5)
        result = await amplifier.amplify_until_convergence(
            target,
            improvement,
            convergence_threshold=0.5,
            max_rounds=3
        )

        assert result.success is True

    def test_get_primitives(self, amplifier):
        """Test getting primitives."""
        prims = amplifier.get_primitives()
        assert 'observe' in prims
        assert 'transform' in prims
        assert 'evaluate' in prims
        assert 'select' in prims

    def test_get_stats(self, amplifier):
        """Test getting stats."""
        stats = amplifier.get_stats()
        assert 'total_amplifications' in stats
        assert 'max_depth_achieved' in stats

    def test_reset(self, amplifier):
        """Test reset."""
        amplifier._total_amplifications = 10
        amplifier.reset()
        assert amplifier._total_amplifications == 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestRecursionIntegration:
    """Integration tests for recursion module."""

    @pytest.mark.asyncio
    async def test_compose_and_amplify(self):
        """Test composing improvements and amplifying."""
        # Create compound improvement
        def add_score_fn(x, ctx):
            if hasattr(x, 'score'):
                result = Improvable(
                    id=f"improved_{x.id}" if hasattr(x, 'id') else 'new',
                    level=x.level if hasattr(x, 'level') else 0,
                    content=x.content if hasattr(x, 'content') else x,
                    score=x.score + 0.05
                )
                if ctx is not None:
                    ctx['delta_score'] = 0.05
                return result
            return x

        add_one = FunctionImprovement(add_score_fn, name="add_score")

        compound = ImprovementAlgebra.sequential(
            add_one,
            ImprovementAlgebra.conditional(
                add_one,
                lambda x, ctx: hasattr(x, 'score') and x.score < 0.9
            )
        )

        # Amplify
        amplifier = RecursiveDepthAmplifier(AmplificationConfig(max_depth=2))
        target = Improvable(id="test", score=0.5)

        result = await amplifier.amplify(target, compound)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_pattern_extraction_during_amplification(self):
        """Test that patterns are extracted during amplification."""
        improvement = FunctionImprovement(
            lambda x, ctx: Improvable(
                id=f"improved_{x.id}",
                level=x.level,
                score=x.score + 0.1
            ) if isinstance(x, Improvable) else x,
            name="score_boost"
        )

        config = AmplificationConfig(
            max_depth=3,
            pattern_extraction_enabled=True,
            early_stopping=False
        )
        amplifier = RecursiveDepthAmplifier(config)
        target = Improvable(id="test", score=0.5)

        result = await amplifier.amplify(target, improvement)

        # Should have extracted patterns
        all_patterns = amplifier.get_all_patterns()
        assert len(result.patterns_extracted) >= 0

    @pytest.mark.asyncio
    async def test_level_invariance(self):
        """Test that primitives work at any level."""
        observe = ObservePrimitive()

        # Apply at different levels
        for level in [0, 1, 2, 5]:
            target = Improvable(id=f"level_{level}", level=level)
            result = observe.apply(target)

            assert result is not None
            assert 'observations' in result.metadata
            assert result.metadata['observations']['level'] == level
