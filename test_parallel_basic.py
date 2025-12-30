#!/usr/bin/env python3
"""Basic test of parallel transmission path."""

import asyncio
import json
from pathlib import Path
from parallel_transmission_path import (
    ParallelTransmissionPath,
    TransmissionStatus,
    ObservationPriority
)


class MockMemory:
    def __init__(self, fail_count=0):
        self.fail_count = fail_count
        self.attempt = 0
        self.records = []
    
    async def record_experience(self, content, type, embedding=None, force=False, link_on_acquisition=False):
        self.attempt += 1
        if self.attempt <= self.fail_count:
            raise Exception(f"Neo4j connection failed (attempt {self.attempt})")
        exp_id = f"exp_{len(self.records) + 1}"
        self.records.append((exp_id, content, type))
        return exp_id


async def test_basic():
    print("Test 1: Basic recording")
    path = ParallelTransmissionPath()
    result = await path.record_observation("Test 1", "test", "test")
    assert result.success
    assert result.parallel_succeeded
    print("  PASSED")


async def test_with_memory():
    print("Test 2: With working memory")
    memory = MockMemory(fail_count=0)
    path = ParallelTransmissionPath()
    path.set_memory(memory)
    result = await path.record_observation("Test 2", "test", "test")
    assert result.success
    assert result.primary_succeeded
    assert result.parallel_succeeded
    print("  PASSED")


async def test_degraded():
    print("Test 3: Degraded mode")
    memory = MockMemory(fail_count=5)
    path = ParallelTransmissionPath()
    path.set_memory(memory)
    result = await path.record_observation("Test 3", "test", "test")
    assert result.success
    assert not result.primary_succeeded
    assert result.parallel_succeeded
    assert path.status == TransmissionStatus.DEGRADED
    print("  PASSED")


async def test_critical():
    print("Test 4: Critical priority")
    path = ParallelTransmissionPath()
    result = await path.record_observation(
        "Critical test",
        "test",
        "test",
        priority=ObservationPriority.CRITICAL
    )
    assert result.success
    assert path.critical_log.exists()
    with open(path.critical_log, "r") as f:
        data = json.load(f)
    assert data["priority"] == "critical"
    print("  PASSED")


async def main():
    print("\n" + "="*40)
    print("Testing Parallel Transmission Path")
    print("="*40 + "\n")
    
    try:
        await test_basic()
        await test_with_memory()
        await test_degraded()
        await test_critical()
        
        print("\n" + "="*40)
        print("All tests PASSED!")
        print("="*40 + "\n")
    except Exception as e:
        print(f"\nFAILED: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
