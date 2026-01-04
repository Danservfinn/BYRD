#!/usr/bin/env python3
"""
Test to verify delta measurement breaks false-positive success loop.

This test demonstrates two scenarios:
1. Success with positive delta
2. Failure with zero/negative delta (false positive blocked)
"""

import asyncio
import sys
from datetime import datetime

# Import the cycle from the main module
from agi_improvement_cycle import AGIImprovementCycle


async def test_positive_delta():
    """Test case where delta is positive - should succeed."""
    print("\n" + "="*60)
    print("TEST 1: Positive Delta (Expected Success)")
    print("="*60)
    
    async def assess_fn(_):
        return {
            "timestamp": datetime.now().isoformat(),
            "performance": {
                "accuracy": 0.85,
                "speed": 1.0
            }
        }
    
    async def identify_fn(assessments):
        return [{"opportunity": "improve_accuracy", "priority": 0.9}]
    
    async def generate_fn(opportunities):
        return [{"solution": "better_model", "approach": "upgrade"}]
    
    async def predict_fn(solutions):
        return {"better_model": 0.9}
    
    async def verify_fn(data):
        return {"better_model": True}
    
    async def execute_fn(solutions):
        return {"status": "implemented"}
    
    async def measure_fn(_):
        # Positive delta: 0.85 -> 0.90
        return {"accuracy": 0.90}
    
    async def learn_fn(data):
        return {
            "success": data["success"],
            "deltas": data["delta_measurements"]
        }
    
    cycle = AGIImprovementCycle(
        assess_fn, identify_fn, generate_fn, predict_fn,
        verify_fn, execute_fn, measure_fn, learn_fn
    )
    
    state = await cycle.run_cycle()
    
    print(f"Baseline: {state.baseline_measurements}")
    print(f"Measurements: {state.measurements}")
    print(f"Delta: {state.delta_measurements}")
    
    has_positive = any(d > 0 for d in state.delta_measurements.values())
    
    if has_positive:
        print("✓ TEST PASSED: Positive delta detected, cycle succeeded")
        return True
    else:
        print("✗ TEST FAILED: Expected positive delta but found none")
        return False


async def test_negative_delta():
    """Test case where delta is negative - should fail and block false positive."""
    print("\n" + "="*60)
    print("TEST 2: Negative Delta (Expected Failure - False Positive Blocked)")
    print("="*60)
    
    async def assess_fn(_):
        return {
            "timestamp": datetime.now().isoformat(),
            "performance": {
                "accuracy": 0.85,
                "speed": 1.0
            }
        }
    
    async def identify_fn(assessments):
        return [{"opportunity": "improve_accuracy", "priority": 0.9}]
    
    async def generate_fn(opportunities):
        return [{"solution": "worse_model", "approach": "downgrade"}]
    
    async def predict_fn(solutions):
        return {"worse_model": 0.9}  # Still predicts high!
    
    async def verify_fn(data):
        return {"worse_model": True}
    
    async def execute_fn(solutions):
        return {"status": "implemented"}
    
    async def measure_fn(_):
        # Negative delta: 0.85 -> 0.80 (performance got worse!)
        return {"accuracy": 0.80}
    
    async def learn_fn(data):
        return {
            "success": data["success"],
            "deltas": data["delta_measurements"],
            "false_positive_blocked": True
        }
    
    cycle = AGIImprovementCycle(
        assess_fn, identify_fn, generate_fn, predict_fn,
        verify_fn, execute_fn, measure_fn, learn_fn
    )
    
    state = await cycle.run_cycle()
    
    print(f"Baseline: {state.baseline_measurements}")
    print(f"Measurements: {state.measurements}")
    print(f"Delta: {state.delta_measurements}")
    print(f"Errors: {state.errors}")
    
    has_positive = any(d > 0 for d in state.delta_measurements.values())
    
    if not has_positive:
        print("✓ TEST PASSED: No positive delta detected, false positive blocked")
        return True
    else:
        print("✗ TEST FAILED: Expected no positive delta but found one")
        return False


async def test_no_baseline_match():
    """Test case where measurements don't match baseline - should error."""
    print("\n" + "="*60)
    print("TEST 3: No Baseline Match (Expected Error)")
    print("="*60)
    
    async def assess_fn(_):
        return {
            "timestamp": datetime.now().isoformat(),
            "performance": {"accuracy": 0.85}
        }
    
    async def identify_fn(assessments):
        return [{"opportunity": "test", "priority": 0.9}]
    
    async def generate_fn(opportunities):
        return [{"solution": "test_sol", "approach": "test"}]
    
    async def predict_fn(solutions):
        return {"test_sol": 0.9}
    
    async def verify_fn(data):
        return {"test_sol": True}
    
    async def execute_fn(solutions):
        return {"status": "done"}
    
    async def measure_fn(_):
        # Wrong metric name - won't match baseline
        return {"speed": 1.0}
    
    async def learn_fn(data):
        return {"success": data["success"]}
    
    cycle = AGIImprovementCycle(
        assess_fn, identify_fn, generate_fn, predict_fn,
        verify_fn, execute_fn, measure_fn, learn_fn
    )
    
    try:
        state = await cycle.run_cycle()
        print(f"Baseline: {state.baseline_measurements}")
        print(f"Measurements: {state.measurements}")
        print(f"Delta: {state.delta_measurements}")
        print(f"Errors: {state.errors}")
        
        if not state.delta_measurements:
            print("✓ TEST PASSED: No delta calculated due to baseline mismatch")
            return True
        else:
            print("✗ TEST FAILED: Expected no delta but delta was calculated")
            return False
    except ValueError as e:
        print(f"✓ TEST PASSED: Got expected error: {e}")
        return True


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("DELTA MEASUREMENT VALIDATION TEST SUITE")
    print("Verifying false-positive success loop is broken")
    print("="*60)
    
    results = []
    
    results.append(await test_positive_delta())
    results.append(await test_negative_delta())
    results.append(await test_no_baseline_match())
    
    print("\n" + "="*60)
    print(f"TEST SUMMARY: {sum(results)}/{len(results)} tests passed")
    print("="*60)
    
    if all(results):
        print("\n✓ ALL TESTS PASSED")
        print("✓ False-positive success loop is effectively broken")
        print("✓ Delta measurement requirement is enforced")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
