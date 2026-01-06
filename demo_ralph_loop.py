#!/usr/bin/env python3
"""
Demo script showing the Ralph Loop + Memvid integration with BYRD.

This script demonstrates:
1. ConsciousnessStream with time-travel and entropy tracking
2. BYRDRalphAdapter orchestrating RSI cycles
3. EmergenceDetector checking for genuine improvement
4. MetaAwareness providing loop context to BYRD

Run with: python demo_ralph_loop.py [--iterations N]
"""

import asyncio
import argparse
import logging
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("ralph_demo")

# Import BYRD RSI components
from rsi.consciousness.stream import ConsciousnessStream
from rsi.consciousness.frame import ConsciousnessFrame
from rsi.orchestration.ralph_adapter import BYRDRalphAdapter
from rsi.orchestration.emergence_detector import EmergenceDetector
from rsi.orchestration.meta_awareness import MetaAwareness
from rsi.engine import CyclePhase


def create_mock_rsi_engine():
    """Create a mock RSI engine for demonstration."""
    engine = MagicMock()

    # Simulate cycle count for varying results
    cycle_count = [0]

    async def mock_run_cycle(meta_context=None):
        cycle_count[0] += 1
        cycle_id = f"demo_cycle_{cycle_count[0]}"

        # Create mock cycle result
        result = MagicMock()
        result.cycle_id = cycle_id
        result.started_at = datetime.now().isoformat()
        result.completed_at = datetime.now().isoformat()

        # Vary results based on cycle
        if cycle_count[0] % 5 == 0:
            # Every 5th cycle: crystallize a heuristic
            result.phase_reached = CyclePhase.CRYSTALLIZE
            result.heuristic_crystallized = f"Learned heuristic #{cycle_count[0] // 5}"
            result.practice_succeeded = True
        elif cycle_count[0] % 3 == 0:
            # Every 3rd cycle: successful practice
            result.phase_reached = CyclePhase.MEASURE
            result.heuristic_crystallized = None
            result.practice_succeeded = True
        else:
            # Otherwise: practice attempt
            result.phase_reached = CyclePhase.PRACTICE
            result.heuristic_crystallized = None
            result.practice_succeeded = cycle_count[0] % 2 == 0

        result.desires_generated = 3 + (cycle_count[0] % 4)
        result.desires_verified = 2 + (cycle_count[0] % 3)
        result.selected_desire = {
            'description': f'Improve capability #{cycle_count[0]}',
            'domain': ['code', 'math', 'logic'][cycle_count[0] % 3],
            'intensity': 0.5 + (cycle_count[0] % 5) * 0.1
        }
        result.domain = result.selected_desire['domain']

        result.to_dict = MagicMock(return_value={
            'cycle_id': cycle_id,
            'phase_reached': result.phase_reached.value,
            'practice_succeeded': result.practice_succeeded,
            'heuristic_crystallized': result.heuristic_crystallized
        })

        # Log meta-context if provided
        if meta_context:
            logger.info(f"  Meta-context: iteration={meta_context.get('iteration')}, "
                       f"entropy_trend={meta_context.get('entropy_trend')}")

        return result

    engine.run_cycle = mock_run_cycle
    engine.memory = MagicMock()
    engine.memory.query_neo4j = AsyncMock(return_value=[])

    return engine


async def run_demo(max_iterations: int = 10, verbose: bool = True):
    """Run the Ralph loop demonstration."""

    print("\n" + "=" * 60)
    print("  BYRD + Ralph Loop + Memvid Integration Demo")
    print("=" * 60 + "\n")

    # Initialize components
    consciousness = ConsciousnessStream(use_memvid=False)
    mock_engine = create_mock_rsi_engine()

    adapter = BYRDRalphAdapter(
        rsi_engine=mock_engine,
        consciousness=consciousness,
        config={
            'meta_awareness': True,
            'checkpoint_interval': 5
        }
    )

    print(f"Starting Ralph loop for up to {max_iterations} iterations...\n")
    print("-" * 60)

    for i in range(max_iterations):
        print(f"\n[Iteration {i + 1}]")

        # Execute one iteration
        result = await adapter.execute()

        # Display results
        cycle = result.cycle_result
        print(f"  Cycle: {cycle.cycle_id}")
        print(f"  Phase reached: {cycle.phase_reached.value}")
        print(f"  Desires: {cycle.desires_generated} generated, {cycle.desires_verified} verified")
        print(f"  Selected: {cycle.selected_desire.get('description', 'N/A')}")
        print(f"  Practice: {'Success' if cycle.practice_succeeded else 'Attempt'}")

        if cycle.heuristic_crystallized:
            print(f"  ** CRYSTALLIZED: {cycle.heuristic_crystallized}")

        if result.should_checkpoint:
            print(f"  [CHECKPOINT] Would create git checkpoint here")

        # Check emergence
        print(f"  Emergence check: {result.emergence_result.reason}")

        if result.completed:
            print(f"\n** EMERGENCE DETECTED! Exiting loop. **")
            break

        # Small delay for readability
        await asyncio.sleep(0.1)

    # Final stats
    print("\n" + "-" * 60)
    print("\nFinal Statistics:")
    stats = adapter.get_stats()
    print(f"  Iterations completed: {stats['iterations_completed']}")
    print(f"  Total time: {stats['total_time_seconds']:.2f}s")
    print(f"  Consciousness frames: {stats['consciousness_stats']['total_frames']}")

    # Demonstrate time-travel
    print("\nTime-Travel Demo:")
    if stats['consciousness_stats']['total_frames'] > 3:
        past_frame = await consciousness.time_travel(3)
        if past_frame:
            print(f"  3 frames ago: cycle={past_frame.cycle_id}, "
                  f"phase={past_frame.phase_reached}")

    # Demonstrate entropy computation
    if stats['consciousness_stats']['total_frames'] >= 5:
        entropy_delta = await consciousness.compute_entropy_delta(window=5)
        print(f"  Entropy delta (last 5 frames): {entropy_delta:.4f}")

    # Demonstrate circular pattern detection
    if stats['consciousness_stats']['total_frames'] >= 10:
        circular = await consciousness.detect_circular_patterns(window=10)
        print(f"  Circular patterns detected: {circular['is_circular']}")
        if circular['is_circular']:
            print(f"    Repeated desires: {circular['repeated_desires'][:3]}")

    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60 + "\n")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Demo of BYRD + Ralph Loop + Memvid integration"
    )
    parser.add_argument(
        '--iterations', '-n',
        type=int,
        default=10,
        help='Maximum number of Ralph iterations (default: 10)'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Reduce output verbosity'
    )

    args = parser.parse_args()

    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)

    asyncio.run(run_demo(args.iterations, not args.quiet))


if __name__ == "__main__":
    main()
