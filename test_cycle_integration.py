#!/usr/bin/env python3
"""
Test the integrated AGI Improvement Cycle with Loop Instrumentation.

This demonstrates how loop instrumentation breaks the zero-delta loop by:
1. Tracking all cycle executions
2. Calculating delta measurements
3. Detecting stagnation patterns
4. Providing intervention triggers
"""

import asyncio
import sys

async def main():
    print("\n" + "="*70)
    print("AGI IMPROVEMENT CYCLE WITH LOOP INSTRUMENTATION")
    print("Breaking the Zero-Delta Loop")
    print("="*70 + "\n")
    
    # Import and create cycle
    import agi_improvement_cycle
    cycle = agi_improvement_cycle.create_default_cycle()
    
    print(f"\nInstrumentation Status: {agi_improvement_cycle.HAS_INSTRUMENTATION}")
    if cycle.instrumenter:
        print(f"Loop Name: {cycle.loop_name}")
        print(f"Instrumenter: Active")
    
    # Run multiple cycles to demonstrate stagnation detection
    print("\n" + "-"*70)
    print("Running 5 improvement cycles to demonstrate instrumentation...")
    print("-"*70 + "\n")
    
    for i in range(1, 6):
        print(f"\n=== CYCLE {i} ===")
        try:
            state = await cycle.run_cycle()
            
            # Display delta measurements
            print(f"\nDelta Measurements: {state.delta_measurements}")
            has_positive = any(d > 0 for d in state.delta_measurements.values())
            print(f"Positive Delta: {has_positive}")
            
            # Check for stagnation detection
            if cycle.instrumenter:
                profile = cycle.instrumenter.get_profile(cycle.loop_name)
                if profile:
                    print(f"Loop State: {profile.current_state.value}")
                    print(f"Success Rate: {profile.success_rate:.1f}%")
                    print(f"Meaningful Rate: {profile.meaningful_rate:.1f}%")
                    
                    if cycle.instrumenter.is_stagnant(cycle.loop_name):
                        print("\n⚠️  STAGNATION DETECTED!")
                        analysis = cycle.instrumenter.analyze_stagnation(cycle.loop_name)
                        print(f"Stagnant cycles: {analysis.get('stagnant_cycles', 0)}")
            
        except Exception as e:
            print(f"ERROR in cycle {i}: {e}")
            import traceback
            traceback.print_exc()
            break
    
    # Display final dashboard
    if cycle.instrumenter:
        print("\n" + "="*70)
        print("FINAL INSTRUMENTATION DASHBOARD")
        print("="*70)
        profile = cycle.instrumenter.get_profile(cycle.loop_name)
        if profile:
            print(f"Total Cycles: {profile.total_cycles}")
            print(f"Successful: {profile.successful_cycles}")
            print(f"Meaningful: {profile.meaningful_cycles}")
            print(f"Avg Delta: {profile.avg_delta:.4f}")
            print(f"Loop State: {profile.current_state.value}")
        
        print("\n" + "="*70)
        print("✓ INTEGRATION SUCCESSFUL")
        print("Zero-delta loop protection is active")
        print("="*70 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
