"""
BYRD v2: Recursive Self-Learning

Entry point for the Q-DE-RSI implementation.
See docs/plans/2026-01-03-rsi-implementation-plan.md for architecture.

RSI Cycle:
  Reflect → Verify → Collapse → Route → Practice → Record → Crystallize → Measure
"""

import argparse
import asyncio
import yaml
import logging
from pathlib import Path
from typing import Optional, Dict

from core.memory import Memory
from core.llm_client import create_llm_client
from rsi import RSIEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("byrd")


class BYRD:
    """
    BYRD v2 - Recursive Self-Learning Agent.

    Architecture:
    - core/: Essential infrastructure (memory, llm, events)
    - constitutional/: Protected identity files
    - rsi/: Recursive self-improvement engine

    The RSI engine runs the core learning cycle:
    1. REFLECT: Generate improvement desires from constitution
    2. VERIFY: Check emergence (provenance + specificity)
    3. COLLAPSE: Quantum selection among competing desires
    4. ROUTE: Classify domain and check oracle constraint
    5. PRACTICE: TDD for code/math, consistency for logic
    6. RECORD: Store trajectory in experience library
    7. CRYSTALLIZE: Extract heuristics if threshold met
    8. MEASURE: Track metrics for hypothesis validation
    """

    def __init__(self, config: dict):
        """
        Initialize BYRD with configuration.

        Args:
            config: Configuration dict (typically from config.yaml)
        """
        self.config = config
        self.memory = Memory(config.get("memory", {}))
        self.llm = create_llm_client(config)
        self.rsi: Optional[RSIEngine] = None
        self.quantum = None  # Will be initialized if quantum is enabled
        self.event_bus = None  # Will be initialized for visualization
        self._running = False
        self._continuous = False

    @property
    def llm_client(self):
        """Backward compatibility property for server.py."""
        return self.llm

    @property
    def quantum_provider(self):
        """Backward compatibility property for server.py."""
        return self.quantum

    async def start(self):
        """Initialize and start BYRD."""
        logger.info("BYRD v2 starting...")

        # Connect to Neo4j
        await self.memory.connect()
        logger.info("Memory connected")

        # Initialize quantum provider if enabled
        if self.config.get("quantum", {}).get("enabled", False):
            try:
                from quantum_randomness import get_quantum_provider
                self.quantum = get_quantum_provider()
                logger.info("Quantum provider initialized")
            except ImportError:
                logger.warning("Quantum module not available, using classical randomness")

        # Initialize event bus for visualization
        try:
            from event_bus import event_bus
            self.event_bus = event_bus
            logger.info("Event bus connected")
        except ImportError:
            logger.debug("Event bus not available")

        # Initialize RSI Engine with all components
        rsi_config = self.config.get("rsi", {})
        self.rsi = RSIEngine(
            memory=self.memory,
            llm_client=self.llm,
            quantum_provider=self.quantum,
            event_bus=self.event_bus,
            config=rsi_config
        )
        logger.info("RSI Engine initialized")

        self._running = True
        logger.info("BYRD v2 ready")

    async def stop(self):
        """Stop BYRD gracefully."""
        logger.info("BYRD v2 stopping...")
        self._running = False
        self._continuous = False
        await self.memory.close()
        logger.info("BYRD v2 stopped")

    async def run_cycle(self) -> Dict:
        """
        Run one RSI cycle.

        Returns:
            CycleResult dict with cycle details
        """
        if self.rsi is None:
            logger.error("RSI Engine not initialized")
            return {"error": "RSI Engine not initialized"}

        result = await self.rsi.run_cycle()
        return result.to_dict()

    async def run_continuous(self, interval_seconds: int = 120, max_cycles: int = 0):
        """
        Run RSI cycles continuously.

        Args:
            interval_seconds: Seconds between cycles
            max_cycles: Maximum cycles to run (0 = unlimited)
        """
        self._continuous = True
        cycle_count = 0

        logger.info(f"Starting continuous RSI cycles (interval={interval_seconds}s, max={max_cycles or 'unlimited'})")

        while self._continuous and self._running:
            try:
                result = await self.run_cycle()
                cycle_count += 1

                phase = result.get("phase_reached", "unknown")
                success = result.get("practice_succeeded", False)
                heuristic = result.get("heuristic_crystallized")

                status = "✓" if success else "○"
                heur_status = f" [H: {heuristic[:30]}...]" if heuristic else ""

                logger.info(f"Cycle {cycle_count} {status} phase={phase}{heur_status}")

                if max_cycles > 0 and cycle_count >= max_cycles:
                    logger.info(f"Reached max cycles ({max_cycles})")
                    break

                # Wait for next cycle
                await asyncio.sleep(interval_seconds)

            except asyncio.CancelledError:
                logger.info("Continuous mode cancelled")
                break
            except Exception as e:
                logger.error(f"Cycle error: {e}")
                await asyncio.sleep(interval_seconds)

        self._continuous = False
        logger.info(f"Continuous mode ended after {cycle_count} cycles")

    def stop_continuous(self):
        """Stop continuous mode."""
        self._continuous = False

    async def get_status(self) -> Dict:
        """
        Get BYRD system status.

        Returns:
            Status dict with metrics and state
        """
        status = {
            "running": self._running,
            "continuous": self._continuous,
            "memory_connected": self.memory.driver is not None,
            "quantum_enabled": self.quantum is not None,
            "rsi_initialized": self.rsi is not None
        }

        if self.rsi:
            status["rsi_metrics"] = await self.rsi.get_metrics()

        return status

    async def get_system_prompt(self) -> str:
        """
        Get the current RSI system prompt.

        Returns:
            Full system prompt (constitution + strategies)
        """
        if self.rsi:
            return self.rsi.get_system_prompt()
        return ""

    async def get_heuristics(self, domain: Optional[str] = None):
        """
        Get current crystallized heuristics.

        Args:
            domain: Optional domain filter

        Returns:
            List of heuristic dicts
        """
        if self.rsi:
            return self.rsi.get_heuristics(domain)
        return []

    def is_running(self) -> bool:
        """Check if BYRD is running."""
        return self._running

    def reset(self):
        """Reset RSI state."""
        if self.rsi:
            self.rsi.reset()
        logger.info("BYRD RSI state reset")


async def main():
    """Main entry point for BYRD v2."""
    parser = argparse.ArgumentParser(description="BYRD v2 - Recursive Self-Learning")
    parser.add_argument(
        "--mode", choices=["single", "continuous", "status"],
        default="single",
        help="Run mode: single cycle, continuous, or status check"
    )
    parser.add_argument(
        "--interval", type=int, default=120,
        help="Interval between cycles in continuous mode (seconds)"
    )
    parser.add_argument(
        "--max-cycles", type=int, default=0,
        help="Maximum cycles in continuous mode (0 = unlimited)"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose logging"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load configuration
    config_path = Path(__file__).parent / "config.yaml"

    if not config_path.exists():
        logger.error("config.yaml not found")
        return

    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Create and start BYRD
    byrd = BYRD(config)

    try:
        await byrd.start()

        if args.mode == "status":
            status = await byrd.get_status()
            print("\n=== BYRD v2 Status ===")
            for key, value in status.items():
                if key == "rsi_metrics":
                    print(f"\nRSI Metrics:")
                    for mk, mv in value.items():
                        print(f"  {mk}: {mv}")
                else:
                    print(f"{key}: {value}")

        elif args.mode == "continuous":
            await byrd.run_continuous(
                interval_seconds=args.interval,
                max_cycles=args.max_cycles
            )

        else:  # single
            result = await byrd.run_cycle()
            print("\n=== RSI Cycle Result ===")
            for key, value in result.items():
                if value is not None:
                    print(f"{key}: {value}")

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        await byrd.stop()


if __name__ == "__main__":
    asyncio.run(main())
