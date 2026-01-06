#!/usr/bin/env python3
"""
Run BYRD's RSI cycle with Ralph orchestration.

This script wraps BYRD's 8-phase RSI cycle in Ralph's Read → Execute → Check → Repeat
loop, providing:
- Resource limits (iterations, cost, time)
- Git checkpointing before self-modifications
- Emergence detection for loop termination
- Optional meta-awareness (BYRD knowing about the loop)

Usage:
    python run_with_ralph.py [options]

Options:
    --max-iterations N    Maximum number of RSI cycles (default: 1000)
    --max-cost USD        Maximum cost in USD (default: 50.0)
    --max-runtime SEC     Maximum runtime in seconds (default: 14400)
    --checkpoint-interval N  Git checkpoint frequency (default: 5)
    --meta-awareness LEVEL  Meta-awareness level: none|minimal|moderate|full (default: moderate)
    --consciousness-path PATH  Path to consciousness.mv2 file (default: consciousness.mv2)
    --no-memvid           Disable Memvid, use in-memory storage
    --dry-run             Don't actually run, just validate configuration
"""

import asyncio
import argparse
import logging
import time
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rsi import (
    RSIEngine,
    ConsciousnessStream,
    BYRDRalphAdapter,
    RalphIterationResult
)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("byrd.ralph")


class RalphRunner:
    """
    Orchestrates BYRD's RSI cycle within Ralph's loop pattern.

    This is a simplified Ralph implementation specifically for BYRD.
    For full Ralph features, consider using ralph-orchestrator package.
    """

    def __init__(
        self,
        adapter: BYRDRalphAdapter,
        max_iterations: int = 1000,
        max_cost_usd: float = 50.0,
        max_runtime_seconds: float = 14400,
        checkpoint_interval: int = 5
    ):
        self.adapter = adapter
        self.max_iterations = max_iterations
        self.max_cost_usd = max_cost_usd
        self.max_runtime_seconds = max_runtime_seconds
        self.checkpoint_interval = checkpoint_interval

        self._start_time: Optional[float] = None
        self._iteration = 0

    async def run(self) -> Dict:
        """
        Run the Ralph loop until emergence or resource exhaustion.

        Returns:
            Dict with run statistics and final state
        """
        self._start_time = time.time()
        self._iteration = 0

        logger.info("=" * 60)
        logger.info("BYRD Ralph Loop Starting")
        logger.info(f"Max iterations: {self.max_iterations}")
        logger.info(f"Max cost: ${self.max_cost_usd}")
        logger.info(f"Max runtime: {self.max_runtime_seconds}s")
        logger.info("=" * 60)

        termination_reason = "unknown"
        last_result: Optional[RalphIterationResult] = None

        try:
            while self._iteration < self.max_iterations:
                self._iteration += 1

                # Check runtime limit
                elapsed = time.time() - self._start_time
                if elapsed > self.max_runtime_seconds:
                    termination_reason = "runtime_exceeded"
                    logger.warning(f"Runtime limit exceeded: {elapsed:.1f}s > {self.max_runtime_seconds}s")
                    break

                # Execute one iteration
                logger.info(f"\n[Iteration {self._iteration}/{self.max_iterations}]")
                result = await self.adapter.execute()
                last_result = result

                # Log progress
                phase = result.cycle_result.phase_reached
                phase_name = phase.value if hasattr(phase, 'value') else str(phase)
                logger.info(
                    f"  Phase: {phase_name} | "
                    f"Emerged: {result.emergence_result.emerged} | "
                    f"Confidence: {result.emergence_result.confidence:.2%}"
                )

                if result.cycle_result.heuristic_crystallized:
                    logger.info(f"  ✨ Heuristic crystallized: {result.cycle_result.heuristic_crystallized[:80]}...")

                # Git checkpoint if needed
                if result.should_checkpoint:
                    await self._git_checkpoint(result)

                # Check emergence
                if result.completed:
                    termination_reason = "emergence_detected"
                    logger.info(f"\n🎉 Emergence detected!")
                    logger.info(f"   Reason: {result.emergence_result.reason}")
                    break

                # Check cost limit
                if result.resource_usage.get('total_cost_usd', 0) > self.max_cost_usd:
                    termination_reason = "cost_exceeded"
                    logger.warning(f"Cost limit exceeded: ${result.resource_usage['total_cost_usd']:.2f}")
                    break

            else:
                termination_reason = "max_iterations"
                logger.info(f"\nReached maximum iterations ({self.max_iterations})")

        except KeyboardInterrupt:
            termination_reason = "user_interrupted"
            logger.info("\n\nUser interrupted (Ctrl+C)")
        except Exception as e:
            termination_reason = f"error: {str(e)}"
            logger.error(f"\n\nError during execution: {e}", exc_info=True)

        # Final report
        elapsed = time.time() - self._start_time
        stats = self.adapter.get_stats()

        logger.info("\n" + "=" * 60)
        logger.info("BYRD Ralph Loop Complete")
        logger.info("=" * 60)
        logger.info(f"Termination reason: {termination_reason}")
        logger.info(f"Iterations completed: {self._iteration}")
        logger.info(f"Total time: {elapsed:.1f}s")
        logger.info(f"Consciousness frames: {stats['consciousness_stats']['total_frames']}")

        if last_result and last_result.emergence_result.emerged:
            logger.info(f"Emergence confidence: {last_result.emergence_result.confidence:.2%}")
            logger.info(f"Emergence reason: {last_result.emergence_result.reason}")

        return {
            'termination_reason': termination_reason,
            'iterations_completed': self._iteration,
            'elapsed_seconds': elapsed,
            'emerged': last_result.emergence_result.emerged if last_result else False,
            'emergence_confidence': last_result.emergence_result.confidence if last_result else 0.0,
            'stats': stats
        }

    async def _git_checkpoint(self, result: RalphIterationResult):
        """Create a git checkpoint."""
        try:
            # Stage all changes
            subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)

            # Create commit
            phase = result.cycle_result.phase_reached
            phase_name = phase.value if hasattr(phase, 'value') else str(phase)

            message = (
                f"[BYRD Ralph checkpoint] Iteration {result.iteration_number}\n\n"
                f"Phase: {phase_name}\n"
                f"Emerged: {result.emergence_result.emerged}\n"
                f"Confidence: {result.emergence_result.confidence:.2f}\n"
            )

            if result.cycle_result.heuristic_crystallized:
                message += f"Heuristic: {result.cycle_result.heuristic_crystallized[:100]}\n"

            subprocess.run(
                ['git', 'commit', '-m', message],
                check=True,
                capture_output=True
            )
            logger.info(f"  📌 Git checkpoint created")

        except subprocess.CalledProcessError as e:
            # No changes to commit is fine
            if b"nothing to commit" not in e.stderr:
                logger.warning(f"  Git checkpoint failed: {e.stderr.decode()[:100]}")


async def create_rsi_engine(config: Dict) -> RSIEngine:
    """
    Create and initialize RSI engine with all dependencies.

    Args:
        config: Configuration dictionary

    Returns:
        Initialized RSIEngine
    """
    # Import dependencies
    from core.memory import Memory
    from core.llm_client import create_llm_client
    from core.event_bus import event_bus

    # Try to get quantum provider
    quantum = None
    try:
        from quantum_randomness import get_quantum_provider
        quantum = get_quantum_provider()
    except ImportError:
        logger.warning("Quantum provider not available, using classical randomness")

    # Initialize memory
    memory = Memory(config.get('memory', {}))
    await memory.connect()

    # Initialize LLM client
    llm_client = create_llm_client(config.get('llm', {}))

    # Create RSI engine
    rsi_engine = RSIEngine(
        memory=memory,
        llm_client=llm_client,
        quantum_provider=quantum,
        event_bus=event_bus,
        config=config.get('rsi', {})
    )

    return rsi_engine


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run BYRD's RSI cycle with Ralph orchestration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--max-iterations', type=int, default=1000,
        help='Maximum number of RSI cycles (default: 1000)'
    )
    parser.add_argument(
        '--max-cost', type=float, default=50.0,
        help='Maximum cost in USD (default: 50.0)'
    )
    parser.add_argument(
        '--max-runtime', type=float, default=14400,
        help='Maximum runtime in seconds (default: 14400 = 4 hours)'
    )
    parser.add_argument(
        '--checkpoint-interval', type=int, default=5,
        help='Git checkpoint frequency (default: 5)'
    )
    parser.add_argument(
        '--meta-awareness', type=str, default='moderate',
        choices=['none', 'minimal', 'moderate', 'full'],
        help='Meta-awareness level (default: moderate)'
    )
    parser.add_argument(
        '--consciousness-path', type=str, default='consciousness.mv2',
        help='Path to consciousness.mv2 file (default: consciousness.mv2)'
    )
    parser.add_argument(
        '--no-memvid', action='store_true',
        help='Disable Memvid, use in-memory storage'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Don't actually run, just validate configuration"
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load config
    config = {}
    config_path = Path(__file__).parent / 'config.yaml'
    if config_path.exists():
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}

    logger.info("Initializing BYRD with Ralph orchestration...")

    # Validate configuration
    if args.dry_run:
        logger.info("Dry run - validating configuration only")
        logger.info(f"  Max iterations: {args.max_iterations}")
        logger.info(f"  Max cost: ${args.max_cost}")
        logger.info(f"  Max runtime: {args.max_runtime}s")
        logger.info(f"  Checkpoint interval: {args.checkpoint_interval}")
        logger.info(f"  Meta-awareness: {args.meta_awareness}")
        logger.info(f"  Consciousness path: {args.consciousness_path}")
        logger.info(f"  Use Memvid: {not args.no_memvid}")
        logger.info("Configuration valid!")
        return

    try:
        # Create RSI engine
        rsi_engine = await create_rsi_engine(config)

        # Create consciousness stream
        consciousness = ConsciousnessStream(
            path=args.consciousness_path,
            use_memvid=not args.no_memvid
        )

        # Create Ralph adapter
        adapter_config = {
            'checkpoint_interval': args.checkpoint_interval,
            'meta_awareness': args.meta_awareness != 'none',
            'emergence': {
                'entropy_threshold': 0.1,
                'min_cycles': 50,
                'crystallization_weight': 0.5
            }
        }

        adapter = BYRDRalphAdapter(
            rsi_engine=rsi_engine,
            consciousness=consciousness,
            config=adapter_config
        )

        # Create and run Ralph loop
        runner = RalphRunner(
            adapter=adapter,
            max_iterations=args.max_iterations,
            max_cost_usd=args.max_cost,
            max_runtime_seconds=args.max_runtime,
            checkpoint_interval=args.checkpoint_interval
        )

        result = await runner.run()

        # Return appropriate exit code
        if result['emerged']:
            logger.info("\n✅ BYRD achieved emergence!")
            sys.exit(0)
        elif result['termination_reason'] == 'user_interrupted':
            sys.exit(130)  # Standard for Ctrl+C
        elif result['termination_reason'].startswith('error'):
            sys.exit(1)
        else:
            logger.info(f"\n⚠️  Loop terminated: {result['termination_reason']}")
            sys.exit(0)

    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.error("Make sure all BYRD dependencies are installed")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to initialize: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
