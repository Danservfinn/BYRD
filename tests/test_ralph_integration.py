"""
Tests for Ralph integration modules.

Tests BYRDRalphAdapter, EmergenceDetector, and MetaAwareness.
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rsi.consciousness.stream import ConsciousnessStream
from rsi.consciousness.frame import ConsciousnessFrame
from rsi.orchestration.ralph_adapter import BYRDRalphAdapter, RalphIterationResult
from rsi.orchestration.emergence_detector import EmergenceDetector, EmergenceResult
from rsi.orchestration.meta_awareness import MetaAwareness, MetaContext
from rsi.engine import CyclePhase


@pytest.fixture
def consciousness():
    """Create in-memory consciousness stream for testing."""
    return ConsciousnessStream(use_memvid=False)


@pytest.fixture
def mock_rsi_engine():
    """Create a mock RSI engine."""
    engine = MagicMock()

    # Mock run_cycle to return a valid CycleResult-like object
    cycle_result = MagicMock()
    cycle_result.cycle_id = "test_cycle_1"
    cycle_result.phase_reached = CyclePhase.MEASURE
    cycle_result.desires_generated = 5
    cycle_result.desires_verified = 3
    cycle_result.selected_desire = {'description': 'test desire'}
    cycle_result.domain = 'code'
    cycle_result.practice_succeeded = True
    cycle_result.heuristic_crystallized = None
    cycle_result.to_dict = MagicMock(return_value={
        'cycle_id': 'test_cycle_1',
        'phase_reached': 'measure'
    })

    engine.run_cycle = AsyncMock(return_value=cycle_result)

    # Mock memory
    engine.memory = MagicMock()
    engine.memory.query_neo4j = AsyncMock(return_value=[])

    return engine


class TestEmergenceDetector:
    """Tests for EmergenceDetector."""

    @pytest.mark.asyncio
    async def test_too_early_detection(self, consciousness):
        """Test that emergence is not detected too early."""
        detector = EmergenceDetector(consciousness, config={'min_cycles': 50})

        # Write only 10 frames
        for i in range(10):
            frame = ConsciousnessFrame(
                frame_id=f"frame_{i}",
                cycle_id=f"cycle_{i}",
                sequence_number=i + 1,
                timestamp=datetime.now(),
                phase_reached="measure",
                selected_desire={'description': f'desire {i}'}
            )
            consciousness._frames.append(frame)
            consciousness._sequence_counter = i + 1

        # Check emergence
        result = await detector.check(consciousness._frames[-1])

        assert result.emerged == False
        assert "Too early" in result.reason

    @pytest.mark.asyncio
    async def test_crystallization_triggers_emergence(self, consciousness):
        """Test that heuristic crystallization triggers emergence."""
        detector = EmergenceDetector(consciousness, config={'min_cycles': 0})

        # Write enough frames
        for i in range(60):
            frame = ConsciousnessFrame(
                frame_id=f"frame_{i}",
                cycle_id=f"cycle_{i}",
                sequence_number=i + 1,
                timestamp=datetime.now(),
                phase_reached="measure",
                selected_desire={'description': f'unique desire {i} with different content'}
            )
            consciousness._frames.append(frame)
            consciousness._sequence_counter = i + 1

        # Create frame with crystallized heuristic
        final_frame = ConsciousnessFrame(
            frame_id="frame_60",
            cycle_id="cycle_60",
            sequence_number=61,
            timestamp=datetime.now(),
            phase_reached="crystallize",
            heuristic_crystallized="Important learned heuristic"
        )

        result = await detector.check(final_frame)

        assert result.emerged == True
        assert "heuristic_crystallized" in result.reason

    @pytest.mark.asyncio
    async def test_circular_patterns_block_emergence(self, consciousness):
        """Test that circular patterns prevent emergence."""
        detector = EmergenceDetector(consciousness, config={'min_cycles': 0})

        # Write frames with circular patterns (same 3 desires repeated)
        for i in range(60):
            frame = ConsciousnessFrame(
                frame_id=f"frame_{i}",
                cycle_id=f"cycle_{i}",
                sequence_number=i + 1,
                timestamp=datetime.now(),
                phase_reached="measure",
                selected_desire={'description': f'repeated desire {i % 3}'}
            )
            consciousness._frames.append(frame)
            consciousness._sequence_counter = i + 1

        result = await detector.check(consciousness._frames[-1])

        assert result.emerged == False
        assert "Circular patterns detected" in result.reason

    @pytest.mark.asyncio
    async def test_entropy_increase_signals(self, consciousness):
        """Test that increasing entropy contributes to emergence."""
        detector = EmergenceDetector(
            consciousness,
            config={'min_cycles': 0, 'entropy_threshold': 0.01}
        )

        # Write frames with increasing diversity
        for i in range(100):
            words = ' '.join([f'word{j}' for j in range(i // 2 + 1)])
            frame = ConsciousnessFrame(
                frame_id=f"frame_{i}",
                cycle_id=f"cycle_{i}",
                sequence_number=i + 1,
                timestamp=datetime.now(),
                phase_reached="measure",
                entropy_score=(i / 100.0),  # Increasing entropy
                selected_desire={'description': words}
            )
            consciousness._frames.append(frame)
            consciousness._sequence_counter = i + 1

        result = await detector.check(consciousness._frames[-1])

        assert 'entropy_delta' in result.metrics
        # Should have positive entropy delta
        assert result.metrics['entropy_delta'] >= 0


class TestMetaAwareness:
    """Tests for MetaAwareness."""

    @pytest.mark.asyncio
    async def test_generate_context(self, consciousness):
        """Test meta-context generation."""
        meta = MetaAwareness(consciousness, enabled=True)

        context = await meta.generate_context(iteration=5)

        assert context.iteration == 5
        assert context.total_frames == 0  # Empty consciousness
        assert context.entropy_trend in ['increasing', 'decreasing', 'stable']

    @pytest.mark.asyncio
    async def test_context_prompt_section(self, consciousness):
        """Test that context generates valid prompt section."""
        meta = MetaAwareness(consciousness, enabled=True)

        context = await meta.generate_context(iteration=10)
        prompt_section = context.to_prompt_section()

        assert "META-LOOP CONTEXT" in prompt_section
        assert "iteration 10" in prompt_section
        assert "recursive self-improvement loop" in prompt_section

    @pytest.mark.asyncio
    async def test_context_to_dict(self, consciousness):
        """Test context serialization."""
        meta = MetaAwareness(consciousness, enabled=True)

        context = await meta.generate_context(iteration=5)
        d = context.to_dict()

        assert d['iteration'] == 5
        assert 'entropy_trend' in d
        assert 'time_in_loop_seconds' in d


class TestBYRDRalphAdapter:
    """Tests for BYRDRalphAdapter."""

    @pytest.mark.asyncio
    async def test_execute_iteration(self, mock_rsi_engine, consciousness):
        """Test executing one Ralph iteration."""
        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={'meta_awareness': False}
        )

        result = await adapter.execute()

        assert result.iteration_number == 1
        assert result.completed == False  # No emergence yet
        assert result.cycle_result is not None
        mock_rsi_engine.run_cycle.assert_called_once()

    @pytest.mark.asyncio
    async def test_multiple_iterations(self, mock_rsi_engine, consciousness):
        """Test multiple iterations increment counter."""
        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={'meta_awareness': False}
        )

        result1 = await adapter.execute()
        result2 = await adapter.execute()
        result3 = await adapter.execute()

        assert result1.iteration_number == 1
        assert result2.iteration_number == 2
        assert result3.iteration_number == 3

    @pytest.mark.asyncio
    async def test_consciousness_frame_written(self, mock_rsi_engine, consciousness):
        """Test that consciousness frame is written after each iteration."""
        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={'meta_awareness': False}
        )

        await adapter.execute()

        assert consciousness.get_stats()['total_frames'] == 1

    @pytest.mark.asyncio
    async def test_checkpoint_on_crystallization(self, mock_rsi_engine, consciousness):
        """Test checkpoint flag when heuristic crystallized."""
        # Mock a crystallization
        mock_rsi_engine.run_cycle.return_value.heuristic_crystallized = "Test heuristic"

        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={'checkpoint_interval': 100}  # High interval
        )

        result = await adapter.execute()

        assert result.should_checkpoint == True

    @pytest.mark.asyncio
    async def test_checkpoint_on_interval(self, mock_rsi_engine, consciousness):
        """Test checkpoint flag on interval."""
        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={'checkpoint_interval': 5}
        )

        # First 4 iterations - no checkpoint
        for i in range(4):
            result = await adapter.execute()
            assert result.should_checkpoint == False

        # 5th iteration - checkpoint
        result = await adapter.execute()
        assert result.should_checkpoint == True

    @pytest.mark.asyncio
    async def test_meta_awareness_context_generated(self, mock_rsi_engine, consciousness):
        """Test that meta-awareness context is generated when enabled."""
        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={'meta_awareness': True}
        )

        # The adapter should generate meta-context
        result = await adapter.execute()

        # Meta context should have been created (we can check the meta object state)
        assert adapter.meta._loop_start_time is not None

    @pytest.mark.asyncio
    async def test_resource_usage_tracking(self, mock_rsi_engine, consciousness):
        """Test resource usage is tracked."""
        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={}
        )

        result = await adapter.execute()

        assert 'iteration' in result.resource_usage
        assert 'iteration_time_seconds' in result.resource_usage
        assert 'total_time_seconds' in result.resource_usage

    @pytest.mark.asyncio
    async def test_get_stats(self, mock_rsi_engine, consciousness):
        """Test statistics retrieval."""
        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={}
        )

        await adapter.execute()
        await adapter.execute()

        stats = adapter.get_stats()

        assert stats['iterations_completed'] == 2
        assert stats['total_time_seconds'] > 0
        assert 'consciousness_stats' in stats

    @pytest.mark.asyncio
    async def test_reset(self, mock_rsi_engine, consciousness):
        """Test adapter reset."""
        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={}
        )

        await adapter.execute()
        await adapter.execute()

        assert adapter.get_stats()['iterations_completed'] == 2

        adapter.reset()

        assert adapter.get_stats()['iterations_completed'] == 0
        assert consciousness.get_stats()['total_frames'] == 0

    @pytest.mark.asyncio
    async def test_check_completion(self, mock_rsi_engine, consciousness):
        """Test completion check."""
        adapter = BYRDRalphAdapter(
            rsi_engine=mock_rsi_engine,
            consciousness=consciousness,
            config={}
        )

        result = await adapter.execute()

        # Should delegate to result.completed
        assert adapter.check_completion(result) == result.completed


class TestRalphIterationResult:
    """Tests for RalphIterationResult dataclass."""

    def test_to_dict(self):
        """Test result serialization."""
        cycle_result = MagicMock()
        cycle_result.to_dict = MagicMock(return_value={'cycle_id': 'test'})

        emergence_result = EmergenceResult(
            emerged=False,
            reason="test reason",
            confidence=0.5,
            metrics={'test': 1}
        )

        result = RalphIterationResult(
            cycle_result=cycle_result,
            emergence_result=emergence_result,
            iteration_number=5,
            resource_usage={'tokens': 100},
            completed=False,
            should_checkpoint=True
        )

        d = result.to_dict()

        assert d['iteration_number'] == 5
        assert d['completed'] == False
        assert d['should_checkpoint'] == True
        assert d['emergence_result']['confidence'] == 0.5
