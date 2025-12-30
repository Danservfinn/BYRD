#!/usr/bin/env python3
"""Test the parallel transmission path."""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
import json

# Import the new module
from parallel_transmission_path import (
    ParallelTransmissionPath,
    TransmissionStatus,
    ObservationPriority,
    record_observation,
    get_transmission_path,
    set_global_memory,
    get_statistics
)


class MockMemory:
    """Mock memory that can fail."""
    def __init__(self, fail_count=0):
        self.fail_count = fail_count
        self.attempt = 0
        self.records = []
    
    async def record_experience(self, content, type, embedding=None, force=False, link_on_acquisition=True):
        self.attempt += 1
        if self.attempt <= self.fail_count:
            raise Exception(f"Neo4j connection failed (attempt {self.attempt})")
        exp_id = f"exp_{len(self.records) + 1}"
        self.records.append((exp_id, content, type))
        return exp_id


async def test_basic_recording():
    """Test basic observation recording."""
    print("\n=== Test 1: Basic Recording ===")
    
    path = ParallelTransmissionPath()
    
    # Record observations
    result1 = await path.record_observation(
        content="Test observation 1",
        source="test",
        observation_type="test_obs"
    )
    
    assert result1.success, "First recording should succeed"
    assert result1.observation_id.startswith("obs_"), "Should have valid ID"
    print(f"  ✓ Recorded: {result1.observation_id}")
    
    result2 = await path.record_observation(
        content="Test observation 2",
        source="test",
        observation_type="test_obs",
        priority=ObservationPriority.HIGH
    )
    
    assert result2.success, "Second recording should succeed"
    print(f"  ✓ Recorded: {result2.observation_id}")
    
    stats = path.statistics
    assert stats["total_observations"] == 2, "Should have 2 observations"
    assert stats["parallel_success_count"] == 2, "Should have 2 parallel successes"
    print(f"  ✓ Statistics: {stats['total_observations']} observations")
    
    # Check file exists
    assert path.observations_log.exists(), "Log file should exist"
    print("  ✓ Log file created")


async def test_with_memory_success():
    """Test recording with working memory."""
    print("\n=== Test 2: With Working Memory ===")
    
    memory = MockMemory(fail_count=0)
    path = ParallelTransmissionPath()
    path.set_memory(memory)
    
    result = await path.record_observation(
        content="Memory test observation",
        source="dreamer",
        observation_type="reflection"
    )
    
    assert result.success, "Should succeed"
    assert result.primary_succeeded, "Primary should succeed"
    assert result.parallel_succeeded, "Parallel should succeed"
    print(f"  ✓ Both paths succeeded: {result.observation_id}")
    
    stats = path.statistics
    assert stats["primary_success_count"] == 1, "Should have 1 primary success"
    assert stats["success_rate"] == 1.0, "Should have 100% success rate"
    print(f"  ✓ Success rate: {stats['success_rate'] * 100}%")


async def test_with_memory_failure():
    """Test graceful degradation when memory fails."""
    print("\n=== Test 3: Graceful Degradation ===")
    
    memory = MockMemory(fail_count=3)
    path = ParallelTransmissionPath()
    path.set_memory(memory)
    
    # Try to record while memory fails
    result = await path.record_observation(
        content="Degraded mode observation",
        source="seeker",
        observation_type="research"
    )
    
    # Should still succeed via parallel path
    assert result.success, "Should succeed via parallel path"
    assert not result.primary_succeeded, "Primary should fail"
    assert result.parallel_succeeded, "Parallel should succeed"
    print(f"  ✓ Degraded mode: {result.observation_id}")
    print(f"  ✓ Parallel path succeeded despite primary failure")
    
    # Status should be degraded after 3 failures
    assert path.status == TransmissionStatus.DEGRADED, "Should be degraded"
    print(f"  ✓ Status: {path.status.value}")


async def test_critical_priority():
    """Test critical observations go to separate log."""
    print("\n=== Test 4: Critical Priority ===")
    
    path = ParallelTransmissionPath()
    
    result = await path.record_observation(
        content="CRITICAL: System failure",
        source="system",
        observation_type="error",
        priority=ObservationPriority.CRITICAL
    )
    
    assert result.success, "Should succeed"
    assert path.critical_log.exists(), "Critical log should exist"
    print(f"  ✓ Critical observation logged to separate file")
    
    # Verify content
    with open(path.critical_log, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1, "Should have one critical entry"
    entry = json.loads(lines[0])
    assert entry["priority"] == "critical", "Should be critical priority"
    print(f"  ✓ Critical entry verified")


async def test_global_instance():
    """Test global instance functions."""
    print("\n=== Test 5: Global Instance ===")
    
    # Use convenience functions
    result1 = await record_observation(
        content="Global test 1",
        source="test",
        observation_type="global"
    )
    assert result1.success, "Global function should work"
    print(f"  ✓ Global record_observation works")
    
    # Set global memory
    memory = MockMemory(fail_count=0)
    set_global_memory(memory)
    
    # Now should use primary path too
    result2 = await record_observation(
        content="Global test 2",
        source="test",
        observation_type="global"
    )
    assert result2.primary_succeeded, "Should use primary path after setting memory"
    print(f"  ✓ Global memory injection works")
    
    stats = get_statistics()
    assert stats["total_observations"] > 0, "Should have statistics"
    print(f"  ✓ Global statistics: {stats['total_observations']} observations")


async def test_persistence():
    """Test that observations persist to disk."""
    print("\n=== Test 6: Disk Persistence ===")
    
    path = ParallelTransmissionPath()
    
    # Record multiple observations
    for i in range(5):
        await path.record_observation(
            content=f"Persistent observation {i}",
            source="test",
            observation_type="persistence"
        )
    
    # Verify file has entries
    with open(path.observations_log, "r") as f:
        lines = f.readlines()
    
    assert len(lines) == 5, "Should have 5 persisted observations"
    print(f"  ✓ All 5 observations persisted to disk")
    
    # Verify they're valid JSON
    for line in lines:
        entry = json.loads(line)
        assert "id" in entry, "Should have ID"
        assert "content" in entry, "Should have content"
        assert "timestamp" in entry, "Should have timestamp"
    print(f"  ✓ All entries are valid JSON")


async def main():
    print("\n" + "="*50)
    print("Testing Parallel Transmission Path")
    print("="*50)
    
    try:
        await test_basic_recording()
        await test_with_memory_success()
        await test_with_memory_failure()
        await test_critical_priority()
        await test_global_instance()
        await test_persistence()
        
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
