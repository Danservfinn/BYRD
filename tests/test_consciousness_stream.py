"""
Tests for the ConsciousnessStream module.

Tests time-travel queries, entropy computation, and circular pattern detection.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, AsyncMock

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rsi.consciousness.stream import ConsciousnessStream
from rsi.consciousness.frame import ConsciousnessFrame
from rsi.engine import CycleResult, CyclePhase


@pytest.fixture
def consciousness():
    """Create in-memory consciousness stream for testing."""
    return ConsciousnessStream(use_memvid=False)


@pytest.fixture
def mock_cycle_result():
    """Create a mock CycleResult factory."""
    def _create(
        cycle_id: str = "test_1",
        phase: CyclePhase = CyclePhase.MEASURE,
        desires_generated: int = 5,
        desires_verified: int = 3,
        selected_desire: dict = None,
        practice_succeeded: bool = True,
        heuristic_crystallized: str = None
    ) -> MagicMock:
        result = MagicMock()
        result.cycle_id = cycle_id
        result.phase_reached = phase
        result.desires_generated = desires_generated
        result.desires_verified = desires_verified
        result.selected_desire = selected_desire or {'description': f'test desire {cycle_id}'}
        result.domain = 'code'
        result.practice_succeeded = practice_succeeded
        result.heuristic_crystallized = heuristic_crystallized
        return result
    return _create


class TestConsciousnessFrame:
    """Tests for ConsciousnessFrame dataclass."""

    def test_frame_creation(self):
        """Test creating a consciousness frame."""
        frame = ConsciousnessFrame(
            frame_id="test_frame_1",
            cycle_id="cycle_1",
            sequence_number=1,
            timestamp=datetime.now(),
            phase_reached="measure",
            desires_generated=5,
            desires_verified=3,
            selected_desire={'description': 'test desire'},
            practice_succeeded=True
        )

        assert frame.frame_id == "test_frame_1"
        assert frame.sequence_number == 1
        assert frame.content_hash != ""  # Hash should be computed

    def test_frame_hash_consistency(self):
        """Test that same content produces same hash."""
        now = datetime.now()
        frame1 = ConsciousnessFrame(
            frame_id="frame_1",
            cycle_id="cycle_1",
            sequence_number=1,
            timestamp=now,
            phase_reached="measure",
            selected_desire={'description': 'test'}
        )
        frame2 = ConsciousnessFrame(
            frame_id="frame_2",  # Different ID
            cycle_id="cycle_1",  # Same cycle
            sequence_number=2,   # Different sequence
            timestamp=now,
            phase_reached="measure",
            selected_desire={'description': 'test'}  # Same desire
        )

        # Content hash is based on cycle_id, phase, desire, heuristic
        assert frame1.content_hash == frame2.content_hash

    def test_frame_to_dict(self):
        """Test frame serialization."""
        frame = ConsciousnessFrame(
            frame_id="test_frame",
            cycle_id="cycle_1",
            sequence_number=1,
            timestamp=datetime.now(),
            phase_reached="measure"
        )

        d = frame.to_dict()
        assert d['frame_id'] == "test_frame"
        assert d['cycle_id'] == "cycle_1"
        assert 'content_hash' in d

    def test_frame_from_dict(self):
        """Test frame deserialization."""
        data = {
            'frame_id': 'test_frame',
            'cycle_id': 'cycle_1',
            'sequence_number': 1,
            'timestamp': datetime.now().isoformat(),
            'phase_reached': 'measure',
            'desires_generated': 5,
            'desires_verified': 3,
            'selected_desire': {'description': 'test'},
            'domain': 'code',
            'practice_succeeded': True,
            'heuristic_crystallized': None,
            'belief_delta': {},
            'capability_delta': {},
            'entropy_score': 0.5,
            'ralph_iteration': 1,
            'resource_usage': {},
            'parent_hash': None
        }

        frame = ConsciousnessFrame.from_dict(data)
        assert frame.frame_id == 'test_frame'
        assert frame.entropy_score == 0.5


class TestConsciousnessStream:
    """Tests for ConsciousnessStream."""

    @pytest.mark.asyncio
    async def test_write_frame(self, consciousness, mock_cycle_result):
        """Test writing a consciousness frame."""
        cycle = mock_cycle_result()
        frame = await consciousness.write_frame(cycle)

        assert frame.cycle_id == "test_1"
        assert frame.sequence_number == 1
        assert frame.content_hash != ""

    @pytest.mark.asyncio
    async def test_frame_chain_integrity(self, consciousness, mock_cycle_result):
        """Test that frames form a hash chain."""
        # Write multiple frames
        frame1 = await consciousness.write_frame(mock_cycle_result(cycle_id="cycle_1"))
        frame2 = await consciousness.write_frame(mock_cycle_result(cycle_id="cycle_2"))
        frame3 = await consciousness.write_frame(mock_cycle_result(cycle_id="cycle_3"))

        # Each frame should reference the previous
        assert frame1.parent_hash is None  # First frame has no parent
        assert frame2.parent_hash == frame1.content_hash
        assert frame3.parent_hash == frame2.content_hash

    @pytest.mark.asyncio
    async def test_time_travel(self, consciousness, mock_cycle_result):
        """Test time-travel queries."""
        # Write 10 frames
        for i in range(10):
            await consciousness.write_frame(mock_cycle_result(cycle_id=f"cycle_{i}"))

        # Time travel 5 frames back
        past = await consciousness.time_travel(5)

        assert past is not None
        assert past.cycle_id == "cycle_4"  # 10 - 5 - 1 = 4

    @pytest.mark.asyncio
    async def test_time_travel_out_of_bounds(self, consciousness, mock_cycle_result):
        """Test time-travel with invalid index."""
        await consciousness.write_frame(mock_cycle_result())

        # Try to go back further than history
        past = await consciousness.time_travel(100)
        assert past is None

    @pytest.mark.asyncio
    async def test_entropy_computation(self, consciousness, mock_cycle_result):
        """Test entropy score computation."""
        # Short description = low entropy
        result1 = mock_cycle_result(cycle_id="1")
        result1.selected_desire = {'description': 'test'}
        frame1 = await consciousness.write_frame(result1)
        assert frame1.entropy_score < 0.5

        # Long, diverse description = higher entropy
        result2 = mock_cycle_result(cycle_id="2")
        result2.selected_desire = {
            'description': 'I want to explore the nature of consciousness and understand how recursive self-improvement enables genuine emergence in artificial intelligence systems'
        }
        frame2 = await consciousness.write_frame(result2)
        assert frame2.entropy_score > frame1.entropy_score

    @pytest.mark.asyncio
    async def test_entropy_delta_computation(self, consciousness, mock_cycle_result):
        """Test entropy delta computation over window."""
        # Write frames with increasing entropy
        for i in range(20):
            result = mock_cycle_result(cycle_id=f"cycle_{i}")
            # Add more words as we go
            words = ' '.join([f'word{j}' for j in range(i + 1)])
            result.selected_desire = {'description': words}
            await consciousness.write_frame(result)

        # Entropy should be increasing
        delta = await consciousness.compute_entropy_delta(window=20)
        assert delta > 0  # Recent entropy > older entropy

    @pytest.mark.asyncio
    async def test_circular_pattern_detection(self, consciousness, mock_cycle_result):
        """Test detection of circular patterns."""
        # Write frames with repeated desires
        for i in range(30):
            result = mock_cycle_result(cycle_id=f"cycle_{i}")
            # Only 3 unique desires, cycling
            result.selected_desire = {'description': f'desire type {i % 3}'}
            await consciousness.write_frame(result)

        circular = await consciousness.detect_circular_patterns(window=30)

        assert circular['is_circular'] == True
        assert circular['pattern_count'] >= 3
        assert len(circular['repeated_desires']) >= 3

    @pytest.mark.asyncio
    async def test_no_circular_patterns(self, consciousness, mock_cycle_result):
        """Test that unique desires are not flagged as circular."""
        # Write frames with unique desires
        for i in range(20):
            result = mock_cycle_result(cycle_id=f"cycle_{i}")
            result.selected_desire = {'description': f'unique desire number {i} with extra text'}
            await consciousness.write_frame(result)

        circular = await consciousness.detect_circular_patterns(window=20)

        assert circular['is_circular'] == False
        assert circular['pattern_count'] == 0

    @pytest.mark.asyncio
    async def test_semantic_search(self, consciousness, mock_cycle_result):
        """Test semantic search over frames."""
        # Write frames with different topics
        topics = ['consciousness', 'emergence', 'recursion', 'improvement', 'learning']
        for i, topic in enumerate(topics):
            result = mock_cycle_result(cycle_id=f"cycle_{i}")
            result.selected_desire = {'description': f'I want to understand {topic}'}
            await consciousness.write_frame(result)

        # Search for consciousness
        results = await consciousness.search_semantic('consciousness', limit=5)

        assert len(results) >= 1
        assert any('consciousness' in r.selected_desire.get('description', '').lower()
                   for r in results)

    @pytest.mark.asyncio
    async def test_temporal_range_query(self, consciousness, mock_cycle_result):
        """Test getting frames within a time range."""
        now = datetime.now()

        # Write frames
        for i in range(5):
            await consciousness.write_frame(mock_cycle_result(cycle_id=f"cycle_{i}"))

        # Get all frames from last hour
        start = now - timedelta(hours=1)
        end = now + timedelta(hours=1)
        results = await consciousness.get_temporal_range(start, end)

        assert len(results) == 5

    def test_get_stats(self, consciousness):
        """Test statistics retrieval."""
        stats = consciousness.get_stats()

        assert stats['total_frames'] == 0
        assert stats['using_memvid'] == False
        assert stats['path'] == 'in-memory'

    @pytest.mark.asyncio
    async def test_reset(self, consciousness, mock_cycle_result):
        """Test consciousness stream reset."""
        # Write some frames
        for i in range(5):
            await consciousness.write_frame(mock_cycle_result(cycle_id=f"cycle_{i}"))

        assert consciousness.get_stats()['total_frames'] == 5

        # Reset
        consciousness.reset()

        assert consciousness.get_stats()['total_frames'] == 0
        assert len(consciousness._frames) == 0
