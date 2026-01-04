#!/usr/bin/env python3
"""Simple test of AGI Improvement Cycle"""

import asyncio

async def test_single_cycle():
    """Test running a single cycle"""
    print("Creating cycle...")
    import agi_improvement_cycle
    cycle = agi_improvement_cycle.create_default_cycle()
    print(f"Cycle created. Instrumentation: {agi_improvement_cycle.HAS_INSTRUMENTATION}")
    
    print("Running cycle...")
    state = await cycle.run_cycle()
    
    print(f"Cycle completed!")
    print(f"ID: {state.cycle_id}")
    print(f"Delta: {state.delta_measurements}")
    
    return state

if __name__ == "__main__":
    try:
        result = asyncio.run(test_single_cycle())
        print("\nSUCCESS: Test passed!")
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
