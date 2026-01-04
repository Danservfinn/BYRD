"""
BYRD v2: Recursive Self-Learning

Entry point for the Q-DE-RSI implementation.
See docs/plans/2026-01-03-rsi-implementation-plan.md for architecture.

Phase 0: Clean slate - minimal entry point
Phase 1: Core RSI components will be implemented here
"""

import asyncio
import yaml
from pathlib import Path

from core.memory import Memory
from core.llm_client import create_llm_client


class BYRD:
    """
    BYRD v2 - Recursive Self-Learning Agent.

    Architecture:
    - core/: Essential infrastructure (memory, llm, events)
    - constitutional/: Protected identity files
    - rsi/: Recursive self-improvement engine (Phase 1)
    """

    def __init__(self, config: dict):
        self.config = config
        self.memory = Memory(config)
        self.llm = create_llm_client(config)
        self.rsi = None  # Initialized after memory connects
        self._running = False

    async def start(self):
        """Initialize and start BYRD."""
        print("BYRD v2 starting...")

        # Connect to Neo4j
        await self.memory.connect()
        print("  Memory connected")

        # RSI Engine will be initialized here in Phase 1
        # from rsi import RSIEngine
        # self.rsi = RSIEngine(self.memory, self.llm, self.config)

        print("BYRD v2 initialized. Ready for Phase 1 RSI implementation.")
        self._running = True

    async def stop(self):
        """Stop BYRD gracefully."""
        print("BYRD v2 stopping...")
        self._running = False
        await self.memory.close()
        print("BYRD v2 stopped.")

    async def run_cycle(self):
        """
        Run one RSI cycle.

        Phase 0: Stub - just confirms system is running
        Phase 1: Will delegate to RSIEngine
        """
        if self.rsi is None:
            print("RSI Engine not yet implemented. See Phase 1 plan.")
            return {"status": "stub", "message": "Phase 1 not implemented"}

        return await self.rsi.run_cycle()

    def is_running(self) -> bool:
        """Check if BYRD is running."""
        return self._running


async def main():
    """Main entry point for BYRD v2."""
    # Load configuration
    config_path = Path(__file__).parent / "config.yaml"

    if not config_path.exists():
        print("Error: config.yaml not found")
        return

    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Create and start BYRD
    byrd = BYRD(config)

    try:
        await byrd.start()

        # Run a test cycle
        result = await byrd.run_cycle()
        print(f"Test cycle result: {result}")

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        await byrd.stop()


if __name__ == "__main__":
    asyncio.run(main())
