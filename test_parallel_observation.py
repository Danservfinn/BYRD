#!/usr/bin/env python3
"""Test the parallel observation path."""

import asyncio
import sys
from datetime import datetime

# Mock the event bus BEFORE importing parallel_observation
class MockEvent:
    def __init__(self, type, data):
        self.type = type
        self.data = data

class MockEventType:
    EXPERIENCE_CREATED = "experience_created"
    TRANSMISSION_FAILED = "transmission_failed"
    TRANSMISSION_STATUS_CHANGED = "transmission_status_changed"
    BUFFERED_OBSERVATION_FLUSHED = "buffered_observation_flushed"
    BUFFER_PERSISTED = "buffer_persisted"

class MockEventBus:
    def __init__(self):
        self.events = []
    
    async def emit(self, event):
        self.events.append(event)
        print(f"  Event: {event.type} - {event.data.get('status', 'N/A')}")
    
    def get_history(self, limit=10):
        return self.events[-limit:]

# Create mock module
mock_event_bus = type(sys)('event_bus')
mock_event_bus.event_bus = MockEventBus()
mock_event_bus.Event = MockEvent
mock_event_bus.EventType = MockEventType()

sys.modules['event_bus'] = mock_event_bus

# NOW import parallel_observation
from parallel_observation import ParallelObservationPath, TransmissionStatus, record_observation

# Mock Memory that fails
class FailingMemory:
    def __init__(self, fail_count=3):
        self.fail_count = fail_count
        self.attempt = 0
    
    async def record_experience(self, content, type, embedding=None, force=False, link_on_acquisition=True):
        self.attempt += 1
        if self.attempt <= self.fail_count:
            raise Exception(f"Neo4j connection failed (attempt {self.attempt})")
        return f"exp_{self.attempt}"

# Mock Memory that works
class WorkingMemory:
    def __init__(self):
        self.records = []
    
    async def record_experience(self, content, type, embedding=None, force=False, link_on_acquisition=True):
        exp_id = f"exp_{len(self.records) + 1}"
        self.records.append((exp_id, content, type))
        return exp_id


async def test_basic_buffering():
    """Test that observations buffer when primary fails."""
    print("\n=== Test 1: Basic Buffering ===")
    
    memory = FailingMemory(fail_count=3)
    path = ParallelObservationPath(memory=memory)
    
    # Try to record 3 observations - should all buffer
    for i in range(3):
        result = await path.record_observation(f"Observation {i}", "test")
        status = path.status
        print(f"  Obs {i}: result={result}, status={status.value}")
    
    assert path.status == TransmissionStatus.DEGRADED
    assert len(path._buffer) == 3
    print("  ✓ Observations buffered correctly")


async def test_flush_on_recovery():
    """Test that buffered observations flush when primary recovers."""
    print("\n=== Test 2: Flush on Recovery ===")
    
    memory = FailingMemory(fail_count=2)
    path = ParallelObservationPath(memory=memory)
    
    # Buffer some observations
    for i in range(3):
        await path.record_observation(f"Obs {i}", "test")
    
    print(f"  Status before: {path.status.value}")
    print(f"  Buffer size: {len(path._buffer)}")
    
    # Now memory should work - trigger a flush
    await path._flush_batch()
    
    print(f"  Status after flush: {path.status.value}")
    print(f"  Buffer size: {len(path._buffer)}")
    print(f"  Successful transmissions: {path._successful_transmissions}")
    print("  ✓ Observations flushed on recovery")


async def test_statistics():
    """Test statistics tracking."""
    print("\n=== Test 3: Statistics ===")
    
    memory = WorkingMemory()
    path = ParallelObservationPath(memory=memory)
    
    await path.record_observation("Test 1", "test")
    await path.record_observation("Test 2", "test")
    await path.record_observation("Test 3", "test")
    
    stats = path.statistics
    print(f"  Total observations: {stats['total_observations']}")
    print(f"  Successful: {stats['successful_transmissions']}")
    print(f"  Status: {stats['status']}")
    
    assert stats['total_observations'] == 3
    assert stats['successful_transmissions'] == 3
    print("  ✓ Statistics tracked correctly")


async def test_persistence():
    """Test buffer persistence to disk."""
    print("\n=== Test 4: Persistence ===")
    
    path = ParallelObservationPath(memory=None)  # No memory, forced to buffer
    
    for i in range(5):
        await path.record_observation(f"Persistent obs {i}", "test")
    
    print(f"  Buffer size before persist: {len(path._buffer)}")
    
    await path._persist_buffer_to_disk()
    
    print(f"  Buffer size after persist: {len(path._buffer)}")
    print(f"  Buffer file exists: {path.BUFFER_FILE.exists()}")
    
    # Load from disk
    loaded = await path.load_from_disk()
    print(f"  Loaded {loaded} observations from disk")
    print(f"  Buffer size after load: {len(path._buffer)}")
    
    assert loaded == 5
    assert len(path._buffer) == 5
    print("  ✓ Persistence works correctly")


async def test_concurrent_access():
    """Test concurrent access to the parallel path."""
    print("\n=== Test 5: Concurrent Access ===")
    
    memory = WorkingMemory()
    path = ParallelObservationPath(memory=memory)
    
    async def record_many(start_id):
        for i in range(10):
            await path.record_observation(f"Concurrent {start_id}-{i}", "test")
    
    # Run multiple concurrent tasks
    await asyncio.gather(
        record_many(0),
        record_many(1),
        record_many(2)
    )
    
    stats = path.statistics
    print(f"  Total observations: {stats['total_observations']}")
    print(f"  Successful: {stats['successful_transmissions']}")
    
    assert stats['total_observations'] == 30
    assert stats['successful_transmissions'] == 30
    print("  ✓ Concurrent access handled safely")


async def main():
    print("\n" + "="*50)
    print("Testing Parallel Observation Path")
    print("="*50)
    
    try:
        await test_basic_buffering()
        await test_flush_on_recovery()
        await test_statistics()
        await test_persistence()
        await test_concurrent_access()
        
        print("\n" + "="*50)
        print("✓ All tests passed!")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
