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
import os
import re
from pathlib import Path
from typing import Optional, Dict

from core.memory import Memory
from core.llm_client import create_llm_client
from core.claude_coder import ClaudeCoder
from core.byrd_service import BYRDService, create_byrd_service, ServiceMode
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
        self.coder: Optional[ClaudeCoder] = None  # Claude Agent SDK coder
        self.service: Optional[BYRDService] = None  # Human-service-first layer
        self.ralph_loop = None  # Ralph Loop for iterative RSI
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

    @property
    def agi_runner(self):
        """Backward compatibility property for server.py."""
        return self.rsi

    @property
    def rsi_engine(self):
        """Backward compatibility property for server.py."""
        return self.rsi

    @property
    def dreamer(self):
        """Backward compatibility property for server.py - returns rsi for Ralph Loop access."""
        return self.rsi

    @property
    def seeker(self):
        """Backward compatibility property for server.py - returns rsi for desire fulfillment access."""
        return self.rsi

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

        # Initialize ClaudeCoder (Claude Agent SDK)
        coder_config = self.config.get("claude_coder", {})
        if coder_config.get("enabled", True):
            self.coder = ClaudeCoder(
                config=coder_config,
                memory=self.memory,
                working_dir=str(Path.cwd()),
            )
            logger.info(f"ClaudeCoder initialized: {self.coder.get_stats()}")
        else:
            logger.info("ClaudeCoder disabled in config")

        # Initialize RSI Engine with all components
        rsi_config = self.config.get("rsi", {})
        self.rsi = RSIEngine(
            memory=self.memory,
            llm_client=self.llm,
            quantum_provider=self.quantum,
            event_bus=self.event_bus,
            config=rsi_config,
            coder=self.coder  # Pass coder for CODE/MATH domain practice
        )
        logger.info("RSI Engine initialized")

        # Initialize Ralph Loop (iterative RSI with emergence detection)
        ralph_config = self.config.get("ralph_loop", {})
        if ralph_config.get("enabled", True):
            try:
                from rsi.orchestration.ralph_loop import RalphLoop
                from rsi.consciousness.stream import ConsciousnessStream

                consciousness = ConsciousnessStream(
                    memory=self.memory,
                    config=ralph_config.get("consciousness", {})
                )

                self.ralph_loop = RalphLoop(
                    rsi_engine=self.rsi,
                    consciousness_stream=consciousness,
                    config=ralph_config
                )
                logger.info("Ralph Loop initialized")
            except ImportError as e:
                logger.warning(f"Ralph Loop not available: {e}")

        # Initialize BYRDService (human-service-first orchestration)
        service_config = self.config.get("service", {})
        if service_config.get("enabled", True):
            self.service = create_byrd_service(
                memory=self.memory,
                ralph_loop=self.ralph_loop,
                config=service_config
            )
            logger.info("BYRDService initialized (human-service-first mode)")

        self._running = True
        logger.info("BYRD v2 ready")

    async def stop(self):
        """Stop BYRD gracefully."""
        logger.info("BYRD v2 stopping...")
        self._running = False
        self._continuous = False

        # Stop service if running
        if self.service:
            await self.service.stop()

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

    # ========================================================================
    # SERVICE CONTROL (Human-Service-First)
    # ========================================================================

    async def start_service(self) -> None:
        """Start the BYRDService (human-service-first task queue with RSI)."""
        if not self.service:
            logger.warning("BYRDService not initialized")
            return

        await self.service.start()
        logger.info("BYRDService started - monitoring for tasks")

    async def stop_service(self) -> None:
        """Stop the BYRDService."""
        if self.service:
            await self.service.stop()
            logger.info("BYRDService stopped")

    async def enqueue_task(
        self,
        description: str,
        objective: str,
        priority: float = 0.5,
        source: str = "external"
    ) -> str:
        """
        Enqueue a task for processing.

        High-priority tasks (>=0.8) will interrupt ongoing RSI cycles.

        Args:
            description: What the task is
            objective: What success looks like
            priority: 0.0-1.0, higher = more urgent
            source: "external" or "emergent"

        Returns:
            task_id: The ID of the created task
        """
        if not self.service:
            logger.warning("BYRDService not initialized, creating task directly in memory")
            return await self.memory.create_task(
                description=description,
                objective=objective,
                priority=priority,
                source=source
            )

        return await self.service.enqueue_task(
            description=description,
            objective=objective,
            priority=priority,
            source=source
        )

    async def get_service_stats(self) -> Optional[Dict]:
        """Get current service statistics."""
        if self.service:
            stats = await self.service.get_stats()
            return {
                'mode': stats.mode.value,
                'uptime_seconds': stats.uptime_seconds,
                'tasks_processed': stats.tasks_processed,
                'tasks_completed': stats.tasks_completed,
                'tasks_failed': stats.tasks_failed,
                'rsi_cycles_completed': stats.rsi_cycles_completed,
                'rsi_interruptions': stats.rsi_interruptions,
                'current_task': stats.current_task,
                'queue_size': self.service.get_queue_size(),
                'is_idle': self.service.is_idle()
            }
        return None

    def pause_service(self) -> None:
        """Pause the service (stops RSI, continues task processing)."""
        if self.service:
            self.service.pause()

    def resume_service(self) -> None:
        """Resume the service."""
        if self.service:
            self.service.resume()


async def main():
    """Main entry point for BYRD v2."""
    parser = argparse.ArgumentParser(description="BYRD v2 - Recursive Self-Learning")
    parser.add_argument(
        "--mode", choices=["single", "continuous", "status", "service"],
        default="single",
        help="Run mode: single cycle, continuous, service, or status check"
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

    # Load configuration with environment variable expansion
    config_path = Path(__file__).parent / "config.yaml"

    if not config_path.exists():
        logger.error("config.yaml not found")
        return

    def expand_env_vars(content: str) -> str:
        """Expand ${VAR:-default} patterns in config."""
        def replacer(match):
            var = match.group(1)
            default = match.group(2) if match.group(2) else ""
            return os.environ.get(var, default)
        return re.sub(r'\$\{([^:}]+)(?::-([^}]*))?\}', replacer, content)

    with open(config_path) as f:
        config_content = expand_env_vars(f.read())
        config = yaml.safe_load(config_content)

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

        elif args.mode == "service":
            # Human-service-first mode: task queue with interruptible RSI
            if not byrd.service:
                print("\n❌ BYRDService not enabled in config.yaml")
                print("   Add 'service: { enabled: true }' to enable service mode")
                return

            await byrd.start_service()

            print("\n=== BYRD Service Mode (Human-Service-First) ===")
            print("BYRD is now running in service mode.")
            print("- Tasks can be injected via API or enqueue_task()")
            print("- RSI runs during idle periods")
            print("- High-priority tasks interrupt RSI")
            print("\nPress Ctrl+C to stop...\n")

            # Keep running until interrupted
            while byrd.is_running():
                await asyncio.sleep(1)

                # Periodically print stats
                stats = await byrd.get_service_stats()
                if stats:
                    print(
                        f"\r[Service] Mode: {stats['mode']} | "
                        f"Tasks: {stats['tasks_processed']} processed, "
                        f"{stats['tasks_completed']} completed, "
                        f"{stats['tasks_failed']} failed | "
                        f"RSI: {stats['rsi_cycles_completed']} cycles, "
                        f"{stats['rsi_interruptions']} interruptions | "
                        f"Queue: {stats['queue_size']}",
                        end="", flush=True
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
