"""
Tests for RalphLoop orchestration.

Tests the main loop, resource limits, checkpointing, and termination conditions.
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rsi.consciousness.stream import ConsciousnessStream
from rsi.consciousness.frame import ConsciousnessFrame
from rsi.orchestration.ralph_loop import (
    RalphLoop,
    LoopResult,
    LoopTerminationReason,
    run_ralph_loop
)
from rsi.orchestration.ralph_adapter import RalphIterationResult
from rsi.orchestration.emergence_detector import EmergenceResult
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


class TestRalphLoopBasics:
    """Basic RalphLoop tests."""

    def test_initialization(self, mock_rsi_engine, consciousness):
        """Test loop initialization."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            config={'checkpoint_interval': 10}
        )

        assert loop.rsi == mock_rsi_engine
        assert loop.consciousness == consciousness
        assert loop._checkpoint_interval == 10
        assert loop._running == False
        assert loop._iteration_count == 0

    def test_cannot_run_twice(self, mock_rsi_engine, consciousness):
        """Test that running twice raises error."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness
        )

        loop._running = True

        with pytest.raises(RuntimeError, match="already running"):
            asyncio.get_event_loop().run_until_complete(
                loop.run(max_iterations=1)
            )


class TestRalphLoopTermination:
    """Tests for loop termination conditions."""

    @pytest.mark.asyncio
    async def test_stops_on_max_iterations(self, mock_rsi_engine, consciousness):
        """Test loop stops when max iterations reached."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            config={'checkpoint_enabled': False}
        )

        result = await loop.run(
            max_iterations=5,
            max_cost_usd=1000.0,
            max_time_seconds=3600
        )

        assert result.terminated == True
        assert result.reason == LoopTerminationReason.MAX_ITERATIONS
        assert result.iterations_completed == 5

    @pytest.mark.asyncio
    async def test_stops_on_max_time(self, mock_rsi_engine, consciousness):
        """Test loop stops when max time reached."""
        # Make iterate slow by adding delay
        async def slow_execute(*args, **kwargs):
            await asyncio.sleep(0.1)
            cycle_result = MagicMock()
            cycle_result.phase_reached = CyclePhase.MEASURE
            cycle_result.heuristic_crystallized = None
            return RalphIterationResult(
                cycle_result=cycle_result,
                emergence_result=EmergenceResult(
                    emerged=False,
                    reason="not yet",
                    confidence=0.1,
                    metrics={}
                ),
                iteration_number=1,
                resource_usage={'tokens_this_iteration': 0},
                completed=False,
                should_checkpoint=False
            )

        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            config={'checkpoint_enabled': False}
        )

        # Patch the adapter's execute method
        loop.adapter.execute = slow_execute

        result = await loop.run(
            max_iterations=1000,
            max_cost_usd=1000.0,
            max_time_seconds=0.3  # 300ms limit
        )

        assert result.terminated == True
        assert result.reason == LoopTerminationReason.MAX_TIME
        # Should have run ~3 iterations in 300ms with 100ms each
        assert result.iterations_completed >= 2
        assert result.iterations_completed <= 5

    @pytest.mark.asyncio
    async def test_stops_on_emergence(self, mock_rsi_engine, consciousness):
        """Test loop stops when emergence detected."""
        call_count = [0]

        async def emergence_execute(*args, **kwargs):
            call_count[0] += 1
            cycle_result = MagicMock()
            cycle_result.phase_reached = CyclePhase.MEASURE
            cycle_result.heuristic_crystallized = None

            # Emerge on 3rd iteration
            emerged = call_count[0] >= 3

            return RalphIterationResult(
                cycle_result=cycle_result,
                emergence_result=EmergenceResult(
                    emerged=emerged,
                    reason="Genuine emergence detected" if emerged else "not yet",
                    confidence=0.95 if emerged else 0.1,
                    metrics={}
                ),
                iteration_number=call_count[0],
                resource_usage={'tokens_this_iteration': 100},
                completed=emerged,
                should_checkpoint=False
            )

        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            config={'checkpoint_enabled': False}
        )

        loop.adapter.execute = emergence_execute

        result = await loop.run(
            max_iterations=100,
            max_cost_usd=1000.0,
            max_time_seconds=3600
        )

        assert result.terminated == True
        assert result.reason == LoopTerminationReason.EMERGENCE_DETECTED
        assert result.iterations_completed == 3
        assert result.final_emergence is not None
        assert result.final_emergence.emerged == True

    @pytest.mark.asyncio
    async def test_stops_on_manual_stop(self, mock_rsi_engine, consciousness):
        """Test loop stops when stop() is called."""
        call_count = [0]

        async def slow_execute(*args, **kwargs):
            call_count[0] += 1
            await asyncio.sleep(0.05)
            cycle_result = MagicMock()
            cycle_result.phase_reached = CyclePhase.MEASURE
            cycle_result.heuristic_crystallized = None
            return RalphIterationResult(
                cycle_result=cycle_result,
                emergence_result=EmergenceResult(
                    emerged=False, reason="not yet", confidence=0.1, metrics={}
                ),
                iteration_number=call_count[0],
                resource_usage={'tokens_this_iteration': 0},
                completed=False,
                should_checkpoint=False
            )

        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            config={'checkpoint_enabled': False}
        )

        loop.adapter.execute = slow_execute

        async def stop_after_delay():
            await asyncio.sleep(0.1)
            loop.stop()

        # Run both concurrently
        stop_task = asyncio.create_task(stop_after_delay())
        result = await loop.run(max_iterations=100)

        await stop_task

        assert result.terminated == True
        assert result.reason == LoopTerminationReason.MANUAL_STOP

    @pytest.mark.asyncio
    async def test_handles_error(self, mock_rsi_engine, consciousness):
        """Test loop handles errors gracefully."""
        async def error_execute(*args, **kwargs):
            raise ValueError("Test error")

        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            config={'checkpoint_enabled': False}
        )

        loop.adapter.execute = error_execute

        result = await loop.run(max_iterations=10)

        assert result.terminated == True
        assert result.reason == LoopTerminationReason.ERROR
        assert "Test error" in result.error_message


class TestRalphLoopIterate:
    """Tests for iterate() method."""

    @pytest.mark.asyncio
    async def test_iterate_increments_counter(self, mock_rsi_engine, consciousness):
        """Test iterate increments iteration counter."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness
        )
        loop._start_time = 0.0

        await loop.iterate()
        assert loop._iteration_count == 1

        await loop.iterate()
        assert loop._iteration_count == 2

    @pytest.mark.asyncio
    async def test_iterate_tracks_history(self, mock_rsi_engine, consciousness):
        """Test iterate stores history."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness
        )
        loop._start_time = 0.0

        await loop.iterate()
        await loop.iterate()
        await loop.iterate()

        assert len(loop._iteration_history) == 3
        assert loop._iteration_history[0]['iteration'] == 1
        assert loop._iteration_history[2]['iteration'] == 3

    @pytest.mark.asyncio
    async def test_iterate_passes_context(self, mock_rsi_engine, consciousness):
        """Test iterate passes loop context to adapter."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness
        )
        loop._start_time = 100.0
        loop._total_cost = 5.0

        captured_context = []

        original_execute = loop.adapter.execute

        async def capture_execute(context=None):
            captured_context.append(context)
            return await original_execute(context)

        loop.adapter.execute = capture_execute

        await loop.iterate()

        assert len(captured_context) == 1
        assert captured_context[0]['loop_iteration'] == 1
        assert captured_context[0]['cost_so_far'] == 5.0


class TestRalphLoopCheckpoint:
    """Tests for checkpoint functionality."""

    @pytest.mark.asyncio
    async def test_checkpoint_creates_git_commit(self, mock_rsi_engine, consciousness):
        """Test checkpoint creates git commit and tag."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            config={'checkpoint_enabled': True}
        )
        loop._start_time = 0.0
        loop._iteration_count = 10
        loop._last_emergence = EmergenceResult(
            emerged=False, reason="test", confidence=0.5, metrics={}
        )

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stderr='')

            await loop.checkpoint()

            # Should have called git add, commit, and tag
            assert mock_run.call_count == 3
            calls = mock_run.call_args_list

            # Check git add
            assert 'git' in calls[0][0][0]
            assert 'add' in calls[0][0][0]

            # Check git commit
            assert 'git' in calls[1][0][0]
            assert 'commit' in calls[1][0][0]

            # Check git tag
            assert 'git' in calls[2][0][0]
            assert 'tag' in calls[2][0][0]

        assert loop._checkpoints_created == 1

    @pytest.mark.asyncio
    async def test_checkpoint_disabled(self, mock_rsi_engine, consciousness):
        """Test checkpoint does nothing when disabled."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            config={'checkpoint_enabled': False}
        )
        loop._iteration_count = 10

        with patch('subprocess.run') as mock_run:
            await loop.checkpoint()

            # Should not have called git
            mock_run.assert_not_called()

        assert loop._checkpoints_created == 0


class TestRalphLoopStats:
    """Tests for statistics and reset."""

    @pytest.mark.asyncio
    async def test_get_stats(self, mock_rsi_engine, consciousness):
        """Test statistics retrieval."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            config={'checkpoint_enabled': False}
        )

        await loop.run(max_iterations=3)

        stats = loop.get_stats()

        assert stats['running'] == False
        assert stats['iterations_completed'] == 3
        assert stats['elapsed_seconds'] > 0
        assert 'adapter_stats' in stats

    def test_reset(self, mock_rsi_engine, consciousness):
        """Test reset clears state."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness
        )

        # Simulate some work
        loop._iteration_count = 10
        loop._total_cost = 5.0
        loop._checkpoints_created = 3
        loop._iteration_history = [{'test': True}]
        loop._last_emergence = EmergenceResult(
            emerged=True, reason="test", confidence=1.0, metrics={}
        )

        loop.reset()

        assert loop._iteration_count == 0
        assert loop._total_cost == 0.0
        assert loop._checkpoints_created == 0
        assert loop._iteration_history == []
        assert loop._last_emergence is None

    def test_cannot_reset_while_running(self, mock_rsi_engine, consciousness):
        """Test cannot reset while running."""
        loop = RalphLoop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness
        )

        loop._running = True

        with pytest.raises(RuntimeError, match="Cannot reset"):
            loop.reset()


class TestRalphLoopResult:
    """Tests for LoopResult."""

    def test_loop_result_to_dict(self):
        """Test LoopResult serialization."""
        result = LoopResult(
            terminated=True,
            reason=LoopTerminationReason.EMERGENCE_DETECTED,
            iterations_completed=50,
            final_emergence=EmergenceResult(
                emerged=True,
                reason="Genuine emergence",
                confidence=0.95,
                metrics={'entropy': 0.8}
            ),
            total_time_seconds=3600.0,
            total_cost_usd=10.5,
            total_tokens=100000,
            checkpoints_created=10,
            iteration_history=[{'iteration': 50}],
            error_message=None
        )

        d = result.to_dict()

        assert d['terminated'] == True
        assert d['reason'] == 'emergence_detected'
        assert d['iterations_completed'] == 50
        assert d['final_emergence']['emerged'] == True
        assert d['final_emergence']['confidence'] == 0.95
        assert d['total_cost_usd'] == 10.5
        assert d['checkpoints_created'] == 10

    def test_loop_result_with_error(self):
        """Test LoopResult with error."""
        result = LoopResult(
            terminated=True,
            reason=LoopTerminationReason.ERROR,
            iterations_completed=5,
            final_emergence=None,
            total_time_seconds=10.0,
            total_cost_usd=0.5,
            total_tokens=5000,
            checkpoints_created=1,
            error_message="Something went wrong"
        )

        d = result.to_dict()

        assert d['reason'] == 'error'
        assert d['error_message'] == "Something went wrong"
        assert d['final_emergence'] is None


class TestRunRalphLoopConvenience:
    """Tests for convenience function."""

    @pytest.mark.asyncio
    async def test_run_ralph_loop_function(self, mock_rsi_engine, consciousness):
        """Test the convenience function works."""
        result = await run_ralph_loop(
            rsi_engine=mock_rsi_engine,
            consciousness_stream=consciousness,
            max_iterations=5,
            max_cost_usd=100.0,
            max_time_seconds=3600,
            config={'checkpoint_enabled': False}
        )

        assert result.terminated == True
        assert result.iterations_completed == 5
