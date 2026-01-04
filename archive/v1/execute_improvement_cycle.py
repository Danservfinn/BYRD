#!/usr/bin/env python3
"""
Execute the AGI Improvement Cycle - Breaking Analysis-Action Loop

This script directly executes the solution instead of continuing diagnostics.
It runs one complete improvement cycle through the AGI Runner.
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from byrd import BYRD
from agi_runner import AGIRunner, CycleResult


def print_header():
    """Print execution header."""
    print("\n" + "=" * 60)
    print("EXECUTING AGI IMPROVEMENT CYCLE")
    print("Breaking analysis-action loop - taking real action")
    print("=" * 60 + "\n")


def print_result(result: CycleResult):
    """Print cycle result summary."""
    print("\n" + "-" * 60)
    print("CYCLE COMPLETE")
    print("-" * 60)
    print(f"Success: {result.success}")
    print(f"Target: {result.target}")
    print(f"Delta: {result.delta:+.2%}")
    print(f"Strategy: {result.strategy}")
    print(f"Duration: {result.duration_seconds:.1f}s")
    print(f"Cycle #: {result.cycle}")
    if result.reason:
        print(f"Reason: {result.reason}")
    print("-" * 60 + "\n")


async def main():
    """Execute the improvement cycle."""
    print_header()
    
    start_time = datetime.now()
    
    # Initialize BYRD system first
    print("[INIT] Initializing BYRD system...")
    byrd = BYRD()
    
    # Initialize AGI Runner with BYRD instance
    print("[INIT] Initializing AGI Runner...")
    runner = AGIRunner(byrd)
    
    # Bootstrap from current state
    print("[INIT] Bootstrapping from current state...")
    await runner.bootstrap_from_current_state()
    
    # Execute improvement cycle
    print("[ACTION] Executing improvement cycle...")
    result = await runner.run_improvement_cycle()
    
    # Display results
    print_result(result)
    
    # Print cycle history
    if runner._cycle_history:
        print(f"Total cycles completed: {len(runner._cycle_history)}")
        
        # Calculate aggregate metrics
        successful = sum(1 for r in runner._cycle_history if r.success)
        avg_delta = sum(r.delta for r in runner._cycle_history) / len(runner._cycle_history)
        
        print(f"Success rate: {successful}/{len(runner._cycle_history)} ({successful/len(runner._cycle_history):.1%})")
        print(f"Average delta: {avg_delta:+.2%}")
    
    total_duration = (datetime.now() - start_time).total_seconds()
    print(f"\nTotal execution time: {total_duration:.1f}s")
    print("\n" + "=" * 60)
    print("ACTION COMPLETE - Solution Executed")
    print("=" * 60 + "\n")
    
    return result.success


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Execution stopped by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERROR] Execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
