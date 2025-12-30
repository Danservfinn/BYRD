#!/usr/bin/env python3
"""
Real AGI Improvement Cycle Execution

This script executes the actual AGI improvement cycle using the real AGIRunner.
This breaks the analysis-action cycle by taking real execution.

Usage:
    python run_real_improvement_cycle.py
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from byrd import BYRD
from agi_runner import AGIRunner


def print_header():
    """Print execution header."""
    print("\n" + "=" * 70)
    print(" REAL AGI IMPROVEMENT CYCLE EXECUTION")
    print(" Breaking analysis-action loop - executing real implementation")
    print("=" * 70 + "\n")


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")


async def main():
    """Execute the real improvement cycle."""
    print_header()
    start_time = datetime.now()
    
    try:
        # Initialize BYRD system
        print_section("[STEP 1] Initializing BYRD System")
        print("  Loading configuration and components...")
        byrd = BYRD()
        await byrd.initialize()
        print("  ✓ BYRD initialized")
        
        # Get AGI Runner (already initialized in byrd.py)
        print_section("[STEP 2] Accessing AGI Runner")
        runner = byrd.agi_runner
        print("  ✓ AGI Runner obtained")
        print(f"  Current cycle count: {runner._cycle_count}")
        print(f"  Bootstrapped: {runner._bootstrapped}")
        
        # Bootstrap to activate Option B loops
        if not runner._bootstrapped:
            print_section("[STEP 3] Bootstrapping Option B Loops")
            print("  Activating dormant loops (Goal Evolver, Memory Reasoner, Self-Compiler, Dreaming Machine)...")
            await runner.bootstrap_from_current_state()
            print("  ✓ Option B loops activated")
        else:
            print_section("[STEP 3] Already Bootstrapped")
            print("  ✓ Option B loops already active")
        
        # Display bootstrap metrics
        print(f"\n  Bootstrap Metrics:")
        for key, value in runner._bootstrap_metrics.items():
            print(f"    - {key}: {value}")
        
        # Execute improvement cycle
        print_section("[STEP 4] Executing Improvement Cycle")
        print("  Running full assessment → hypothesis → prediction → execution → measurement")
        
        cycle_result = await runner.run_improvement_cycle()
        
        # Display results
        print_section("[STEP 5] Cycle Results")
        print(f"  Success:           {cycle_result.success}")
        print(f"  Target:            {cycle_result.target}")
        print(f"  Delta:             {cycle_result.delta:+.3f}")
        print(f"  Cycle Number:      {cycle_result.cycle}")
        print(f"  Strategy:          {cycle_result.strategy}")
        print(f"  Hypotheses Tried:  {cycle_result.hypotheses_tried}")
        print(f"  Measurement:       {cycle_result.measurement_method}")
        if cycle_result.reason:
            print(f"  Reason:            {cycle_result.reason}")
        
        # Display cycle history
        print(f"\n  Total Cycles Run: {len(runner._cycle_history)}")
        if runner._cycle_history:
            total_delta = sum(c.delta for c in runner._cycle_history)
            success_rate = sum(1 for c in runner._cycle_history if c.success) / len(runner._cycle_history)
            print(f"  Total Delta:       {total_delta:+.3f}")
            print(f"  Success Rate:      {success_rate:.1%}")
        
        # Display strategy stats
        if runner._strategy_stats:
            print(f"\n  Strategy Effectiveness:")
            for strategy, stats in runner._strategy_stats.items():
                if stats.get('attempts', 0) > 0:
                    success_rate = stats.get('successes', 0) / stats['attempts']
                    avg_delta = stats.get('total_delta', 0) / stats['attempts']
                    print(f"    {strategy}: {success_rate:.0%} success, avg {avg_delta:+.3f} ({stats['attempts']} attempts)")
        
        # Summary
        duration = (datetime.now() - start_time).total_seconds()
        print_section("EXECUTION COMPLETE")
        print(f"  Total Duration: {duration:.2f}s")
        print(f"  Status: {'✓ SUCCESS' if cycle_result.success else '✗ FAILED'}")
        print("  " + "=" * 66)
        
        return 0 if cycle_result.success else 1
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
