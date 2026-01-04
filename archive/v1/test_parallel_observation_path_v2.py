#!/usr/bin/env python3
"""Comprehensive test suite for Parallel Observation Path v2.

Tests:
1. Basic observation recording
2. Priority-based redundancy
3. Primary path transmission (memory, event_bus, custom)
4. Failure handling and degraded mode
5. Retrieval and replay functionality
6. Thread safety
7. Statistics and health monitoring
"""

import asyncio
import json
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from parallel_observation_path_v2 import (
    ParallelObservationPath,
    TransmissionStatus,
    ObservationPriority,
    PrimaryPathType,
    record_observation,
    get_observer,
    reset_observer,
    set_primary_path,
    get_statistics,
    get_health_status
)


# =============================================================================
# MOCKS FOR TESTING
# =============================================================================

class MockMemory:
    """Mock Memory class that can simulate failures."""
    
    def __init__(self, fail_count=0):
        self.fail_count = fail_count
        self.attempt = 0
        self.records = []
    
    async def record_experience(self, content, type, embedding=None, 
                                force=False, link_on_acquisition=False):
        self.attempt += 1
        if self.attempt <= self.fail_count:
            raise Exception(f"Mock memory failure (attempt {self.attempt})")
        exp_id = f"exp_{len(self.records) + 1}"
        self.records.append((exp_id, content, type))
        return exp_id


class MockEventBus:
    """Mock event bus for testing."""
    
    def __init__(self):
        self.emitted_events = []
    
    async def emit(self, event):
        self.emitted_events.append(event)


class CustomHandler:
    """Custom handler for testing."""
    
    def __init__(self):
        self.observations = []
    
    async def __call__(self, observation):
        self.observations.append(observation)


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

async def test_basic_recording():
    """Test 1: Basic observation recording."""
    print("\n=== Test 1: Basic Recording ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = ParallelObservationPath(log_directory=tmpdir)
        
        # Record observations
        result1 = await path.record_observation(
            content="Test observation 1",
            source="test",
            observation_type="test_obs"
        )
        
        assert result1.success, "First recording should succeed"
        assert result1.observation_id.startswith("obs_"), "Should have valid ID"
        assert result1.parallel_succeeded, "Parallel write should succeed"
        print(f"  ✓ Recorded: {result1.observation_id}")
        
        result2 = await path.record_observation(
            content="Test observation 2",
            source="test",
            observation_type="test_obs",
            priority=ObservationPriority.HIGH
        )
        
        assert result2.success, "Second recording should succeed"
        print(f"  ✓ Recorded: {result2.observation_id}")
        
        # Check statistics
        stats = path.statistics
        assert stats["total_observations"] == 2, "Should have 2 observations"
        print(f"  ✓ Statistics: {stats['total_observations']} observations")
        
        # Check disk persistence
        log_file = Path(tmpdir) / "observations.jsonl"
        assert log_file.exists(), "Log file should exist"
        
        with open(log_file, "r") as f:
            lines = f.readlines()
        assert len(lines) == 2, "Should have 2 log entries"
        print(f"  ✓ Disk persistence: {len(lines)} entries")


async def test_priority_redundancy():
    """Test 2: Priority-based redundancy."""
    print("\n=== Test 2: Priority-Based Redundancy ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = ParallelObservationPath(log_directory=tmpdir)
        
        # Record observations with different priorities
        await path.record_observation(
            content="Low priority obs",
            source="test",
            observation_type="test",
            priority=ObservationPriority.LOW
        )
        
        await path.record_observation(
            content="Medium priority obs",
            source="test",
            observation_type="test",
            priority=ObservationPriority.MEDIUM
        )
        
        await path.record_observation(
            content="High priority obs",
            source="test",
            observation_type="test",
            priority=ObservationPriority.HIGH
        )
        
        await path.record_observation(
            content="Critical priority obs",
            source="test",
            observation_type="test",
            priority=ObservationPriority.CRITICAL
        )
        
        # Check log files
        primary_log = Path(tmpdir) / "observations.jsonl"
        backup_log = Path(tmpdir) / "observations_backup.jsonl"
        critical_log = Path(tmpdir) / "critical_events.jsonl"
        
        with open(primary_log, "r") as f:
            primary_lines = f.readlines()
        with open(backup_log, "r") as f:
            backup_lines = f.readlines()
        with open(critical_log, "r") as f:
            critical_lines = f.readlines()
        
        assert len(primary_lines) == 4, "Primary log should have all 4"
        assert len(backup_lines) == 2, "Backup log should have HIGH and CRITICAL"
        assert len(critical_lines) == 1, "Critical log should have only CRITICAL"
        
        print(f"  ✓ Primary log: {len(primary_lines)} entries")
        print(f"  ✓ Backup log: {len(backup_lines)} entries (HIGH, CRITICAL)")
        print(f"  ✓ Critical log: {len(critical_lines)} entries (CRITICAL only)")


async def test_primary_path_memory():
    """Test 3: Primary path with Memory."""
    print("\n=== Test 3: Primary Path (Memory) ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = ParallelObservationPath(
            log_directory=tmpdir,
            primary_path_type=PrimaryPathType.MEMORY
        )
        
        # Set up mock memory
        memory = MockMemory(fail_count=2)
        path.set_primary_path(memory)
        
        # First 2 should fail primary, succeed parallel
        result1 = await path.record_observation(
            content="Test 1",
            source="test",
            observation_type="test"
        )
        assert result1.success, "Should succeed via parallel"
        assert not result1.primary_succeeded, "Primary should fail"
        assert result1.parallel_succeeded, "Parallel should succeed"
        print(f"  ✓ Attempt 1: parallel={result1.parallel_succeeded}, primary={result1.primary_succeeded}")
        
        result2 = await path.record_observation(
            content="Test 2",
            source="test",
            observation_type="test"
        )
        assert not result2.primary_succeeded, "Primary should still fail"
        print(f"  ✓ Attempt 2: parallel={result2.parallel_succeeded}, primary={result2.primary_succeeded}")
        
        # Third should succeed on both
        result3 = await path.record_observation(
            content="Test 3",
            source="test",
            observation_type="test"
        )
        assert result3.success, "Should succeed"
        assert result3.primary_succeeded, "Primary should succeed now"
        assert result3.parallel_succeeded, "Parallel should always succeed"
        print(f"  ✓ Attempt 3: parallel={result3.parallel_succeeded}, primary={result3.primary_succeeded}")
        
        # Check memory records
        assert len(memory.records) == 1, "Memory should have 1 record"
        print(f"  ✓ Memory records: {len(memory.records)}")


async def test_retrieval_and_replay():
    """Test 4: Retrieval and replay."""
    print("\n=== Test 4: Retrieval and Replay ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = ParallelObservationPath(log_directory=tmpdir)
        
        # Record some observations
        for i in range(5):
            await path.record_observation(
                content=f"Observation {i}",
                source="test",
                observation_type="test"
            )
        
        # Retrieve recent observations
        observations = path.get_recent_observations(limit=3)
        assert len(observations) == 3, "Should get 3 observations"
        assert "Observation 4" in observations[-1]["content"], "Should have latest"
        print(f"  ✓ Retrieved {len(observations)} observations")
        
        # Test priority filter
        high_obs = path.get_recent_observations(
            limit=10,
            priority_filter=ObservationPriority.HIGH
        )
        assert len(high_obs) == 0, "No high priority observations recorded"
        print(f"  ✓ Priority filter: {len(high_obs)} high priority")
        
        # Test replay
        memory = MockMemory()
        path.set_primary_path(memory)
        
        replay_stats = await path.replay_to_primary(limit=3)
        assert replay_stats["replayed"] == 3, "Should replay 3 observations"
        assert replay_stats["failed"] == 0, "Should have no failures"
        assert len(memory.records) == 3, "Memory should have 3 records"
        print(f"  ✓ Replayed {replay_stats['replayed']} observations")


async def test_degraded_mode():
    """Test 5: Degraded mode on consecutive failures."""
    print("\n=== Test 5: Degraded Mode ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = ParallelObservationPath(log_directory=tmpdir)
        
        # Set up memory that always fails
        memory = MockMemory(fail_count=100)
        path.set_primary_path(memory)
        
        # Record 4 observations (should enter degraded after 3 failures)
        for i in range(4):
            result = await path.record_observation(
                content=f"Test {i}",
                source="test",
                observation_type="test"
            )
            print(f"  ✓ Attempt {i+1}: status={result.status.value}")
        
        # Should be in degraded state
        assert path.status == TransmissionStatus.DEGRADED, "Should be degraded"
        print(f"  ✓ Status: {path.status.value}")
        
        # Statistics should reflect failures
        stats = path.statistics
        assert stats["primary_failure_count"] >= 3, "Should have 3+ failures"
        assert stats["consecutive_failures"] == 4, "Should have 4 consecutive failures"
        print(f"  ✓ Primary failures: {stats['primary_failure_count']}")
        
        # All observations should still be persisted via parallel
        log_file = Path(tmpdir) / "observations.jsonl"
        with open(log_file, "r") as f:
            lines = f.readlines()
        assert len(lines) == 4, "All 4 should be persisted"
        print(f"  ✓ Parallel persistence: {len(lines)} entries")


async def test_health_monitoring():
    """Test 6: Health monitoring."""
    print("\n=== Test 6: Health Monitoring ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = ParallelObservationPath(log_directory=tmpdir)
        
        # Record some observations
        for i in range(5):
            await path.record_observation(
                content=f"Test {i}",
                source="test",
                observation_type="test"
            )
        
        # Get health status
        health = path.get_health_status()
        
        assert health["status"] == TransmissionStatus.OPERATIONAL.value, "Should be operational"
        assert health["health"] == "healthy", "Should be healthy"
        assert health["primary_path_configured"] == False, "No primary path yet"
        assert health["statistics"]["total_observations"] == 5, "5 observations"
        
        print(f"  ✓ Status: {health['status']}")
        print(f"  ✓ Health: {health['health']}")
        print(f"  ✓ Observations: {health['statistics']['total_observations']}")
        
        # Add failing primary path
        memory = MockMemory(fail_count=10)
        path.set_primary_path(memory)
        
        # Record more to trigger degraded mode
        for i in range(5):
            await path.record_observation(
                content=f"Test {i}",
                source="test",
                observation_type="test"
            )
        
        # Check degraded health
        health = path.get_health_status()
        assert health["health"] == "degraded", "Should be degraded"
        print(f"  ✓ Health after failures: {health['health']}")


async def test_singleton_and_convenience():
    """Test 7: Singleton and convenience functions."""
    print("\n=== Test 7: Singleton and Convenience Functions ===")
    
    # Reset singleton
    reset_observer()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Get singleton
        observer1 = get_observer(log_directory=tmpdir)
        observer2 = get_observer()
        
        assert observer1 is observer2, "Should be same instance"
        print("  ✓ Singleton pattern works")
        
        # Use convenience function
        result = await record_observation(
            content="Convenience test",
            source="test",
            observation_type="test"
        )
        
        assert result.success, "Convenience function should work"
        print(f"  ✓ record_observation(): {result.observation_id}")
        
        # Get statistics
        stats = get_statistics()
        assert stats["total_observations"] >= 1, "Should have statistics"
        print(f"  ✓ get_statistics(): {stats['total_observations']} observations")
        
        # Get health
        health = get_health_status()
        assert "status" in health, "Should have health status"
        print(f"  ✓ get_health_status(): {health['status']}")
        
        # Set primary path
        memory = MockMemory()
        set_primary_path(memory)
        
        result = await record_observation(
            content="With primary path",
            source="test",
            observation_type="test"
        )
        
        assert result.primary_succeeded, "Should use primary path now"
        print(f"  ✓ set_primary_path() works")


async def test_concurrent_access():
    """Test 8: Concurrent access (thread safety)."""
    print("\n=== Test 8: Concurrent Access ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = ParallelObservationPath(log_directory=tmpdir)
        
        # Record many observations concurrently
        tasks = []
        for i in range(50):
            task = path.record_observation(
                content=f"Concurrent {i}",
                source="test",
                observation_type="test"
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # All should succeed
        successes = sum(1 for r in results if r.success)
        assert successes == 50, f"All 50 should succeed, got {successes}"
        print(f"  ✓ All {successes} concurrent recordings succeeded")
        
        # Check disk has all entries
        log_file = Path(tmpdir) / "observations.jsonl"
        with open(log_file, "r") as f:
            lines = f.readlines()
        assert len(lines) == 50, "Should have 50 log entries"
        print(f"  ✓ Disk has all {len(lines)} entries")


async def test_metadata_and_tags():
    """Test 9: Metadata and tags."""
    print("\n=== Test 9: Metadata and Tags ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = ParallelObservationPath(log_directory=tmpdir)
        
        # Record with metadata and tags
        result = await path.record_observation(
            content="Rich observation",
            source="test",
            observation_type="test",
            priority=ObservationPriority.HIGH,
            metadata={"key1": "value1", "key2": 42},
            tags=["important", "test"]
        )
        
        assert result.success, "Should succeed"
        print(f"  ✓ Recorded with metadata and tags")
        
        # Retrieve and verify
        observations = path.get_recent_observations(limit=1)
        obs = observations[0]
        
        assert obs["metadata"]["key1"] == "value1", "Metadata should persist"
        assert obs["metadata"]["key2"] == 42, "Metadata should persist"
        assert "important" in obs["tags"], "Tags should persist"
        assert obs["priority"] == "high", "Priority should be correct"
        print(f"  ✓ Metadata and tags persisted correctly")


async def test_transmission_log():
    """Test 10: Transmission logging."""
    print("\n=== Test 10: Transmission Log ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = ParallelObservationPath(log_directory=tmpdir)
        
        # Record observations
        await path.record_observation("Test 1", "test", "test")
        await path.record_observation("Test 2", "test", "test")
        
        # Check transmission log
        log_file = Path(tmpdir) / "transmissions.jsonl"
        assert log_file.exists(), "Transmission log should exist"
        
        with open(log_file, "r") as f:
            lines = f.readlines()
        
        assert len(lines) == 2, "Should have 2 transmission entries"
        
        for line in lines:
            entry = json.loads(line)
            assert "timestamp" in entry, "Should have timestamp"
            assert "observation_id" in entry, "Should have observation_id"
            assert "success" in entry, "Should have success flag"
            assert "status" in entry, "Should have status"
        
        print(f"  ✓ Transmission log: {len(lines)} entries")


# =============================================================================
# TEST RUNNER
# =============================================================================

async def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("PARALLEL OBSERVATION PATH v2 - TEST SUITE")
    print("="*60)
    
    tests = [
        test_basic_recording,
        test_priority_redundancy,
        test_primary_path_memory,
        test_retrieval_and_replay,
        test_degraded_mode,
        test_health_monitoring,
        test_singleton_and_convenience,
        test_concurrent_access,
        test_metadata_and_tags,
        test_transmission_log,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            await test()
            passed += 1
            print(f"✓ {test.__name__} PASSED")
        except AssertionError as e:
            failed += 1
            print(f"✗ {test.__name__} FAILED: {e}")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} ERROR: {e}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)
