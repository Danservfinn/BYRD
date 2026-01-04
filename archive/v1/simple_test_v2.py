#!/usr/bin/env python3
"""Simple test to debug parallel_observation_path_v2"""

import asyncio
import sys
import traceback

print("Testing imports...")

try:
    from parallel_observation_path_v2 import (
        ParallelObservationPath,
        TransmissionStatus,
        ObservationPriority,
        PrimaryPathType
    )
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\nTesting basic creation...")

async def test_basic():
    try:
        path = ParallelObservationPath()
        print("✓ Created ParallelObservationPath")
        
        result = await path.record_observation(
            content="Test observation",
            source="test",
            observation_type="test"
        )
        print(f"✓ Recorded observation: {result.observation_id}")
        print(f"  Success: {result.success}")
        print(f"  Parallel succeeded: {result.parallel_succeeded}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_basic())
    sys.exit(0 if success else 1)
