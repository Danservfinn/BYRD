#!/usr/bin/env python3
"""
RSI Validation Runner

Runs RSI cycles and validates hypotheses to check phase gate criteria.

Usage:
    # Run validation with 10 cycles
    python validate_rsi.py --cycles 10

    # Run until phase gate passes (or max cycles)
    python validate_rsi.py --until-gate --max-cycles 100

    # Just check current status
    python validate_rsi.py --status
"""

import argparse
import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

from core.config import load_config, get_memory_config, get_rsi_config, get_llm_config
from core.memory import Memory
from core.llm_client import create_llm_client
from rsi import RSIEngine
from rsi.measurement import (
    MetricsCollector, HypothesisValidator, run_validation, ValidationReport
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("validate_rsi")


class RSIValidator:
    """
    Runs RSI validation cycles and checks phase gate criteria.

    Phase Gate Requirements:
    - H1: Activation rate ≥ 50%
    - H6: Heuristic transfer ≥ 15% improvement
    - H7: Evolved prompts outperform static
    - Complete cycles: ≥ 3
    """

    def __init__(self, config: dict):
        """Initialize validator with configuration."""
        self.config = config
        # Extract section configs
        memory_config = config.get("memory", config)
        llm_config = config.get("local_llm", config)
        self.memory = Memory(memory_config)
        self.llm = create_llm_client(llm_config)
        self.rsi: Optional[RSIEngine] = None
        self.validator: Optional[HypothesisValidator] = None

        # Validation state
        self._cycles_run = 0
        self._cycle_results = []
        self._validation_history = []

    async def initialize(self):
        """Initialize components."""
        logger.info("Initializing RSI Validator...")

        # Connect to Neo4j
        await self.memory.connect()
        logger.info("Memory connected")

        # Initialize quantum if enabled
        quantum = None
        if self.config.get("quantum", {}).get("enabled", False):
            try:
                from core.quantum_randomness import get_quantum_provider
                quantum = get_quantum_provider()
                logger.info("Quantum provider initialized")
            except ImportError:
                logger.warning("Quantum not available")

        # Initialize RSI Engine
        rsi_config = self.config.get("rsi", {})
        self.rsi = RSIEngine(
            memory=self.memory,
            llm_client=self.llm,
            quantum_provider=quantum,
            event_bus=None,
            config=rsi_config
        )
        logger.info("RSI Engine initialized")

        # Initialize hypothesis validator
        self.validator = HypothesisValidator(self.rsi.metrics)
        logger.info("Hypothesis validator initialized")

    async def run_cycles(self, num_cycles: int) -> Dict:
        """
        Run specified number of RSI cycles.

        Args:
            num_cycles: Number of cycles to run

        Returns:
            Summary of results
        """
        logger.info(f"Running {num_cycles} RSI cycles...")

        for i in range(num_cycles):
            try:
                result = await self.rsi.run_cycle()
                self._cycles_run += 1
                self._cycle_results.append(result.to_dict())

                # Log progress
                phase = result.phase_reached.value
                success = "✓" if result.practice_succeeded else "○"
                heuristic = "🔷" if result.heuristic_crystallized else ""

                logger.info(
                    f"Cycle {self._cycles_run}: {success} phase={phase} "
                    f"desires={result.desires_verified}/{result.desires_generated} {heuristic}"
                )

            except Exception as e:
                logger.error(f"Cycle {i+1} failed: {e}")

        return await self.get_summary()

    async def run_until_gate(self, max_cycles: int = 100, check_interval: int = 5) -> Dict:
        """
        Run cycles until phase gate passes or max reached.

        Args:
            max_cycles: Maximum cycles to run
            check_interval: Check gate every N cycles

        Returns:
            Summary with gate status
        """
        logger.info(f"Running until phase gate passes (max {max_cycles} cycles)...")

        while self._cycles_run < max_cycles:
            # Run a batch of cycles
            batch_size = min(check_interval, max_cycles - self._cycles_run)
            await self.run_cycles(batch_size)

            # Check phase gate
            report = await self.validator.run_all_tests()
            self._validation_history.append(report)

            if report.phase_gate_passed:
                logger.info("🎉 Phase gate PASSED!")
                return await self.get_summary()

            # Log gate status
            logger.info(
                f"Gate status after {self._cycles_run} cycles: "
                f"H1={report.gate_criteria.get('H1', False)} "
                f"H6={report.gate_criteria.get('H6', False)} "
                f"H7={report.gate_criteria.get('H7', False)} "
                f"cycles={report.gate_criteria.get('complete_cycles', False)}"
            )

        logger.warning(f"Max cycles ({max_cycles}) reached without passing gate")
        return await self.get_summary()

    async def get_summary(self) -> Dict:
        """Get current validation summary."""
        metrics = await self.rsi.get_metrics()
        report = await self.validator.run_all_tests()

        return {
            "cycles_run": self._cycles_run,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "validation": report.to_dict(),
            "phase_gate": {
                "passed": report.phase_gate_passed,
                "criteria": report.gate_criteria
            },
            "recent_cycles": self._cycle_results[-10:] if self._cycle_results else []
        }

    async def get_status(self) -> Dict:
        """Get current status without running cycles."""
        if not self.rsi:
            return {"error": "Not initialized"}

        metrics = await self.rsi.get_metrics()
        gate_status = self.validator.get_phase_gate_status()

        return {
            "initialized": True,
            "cycles_run": self._cycles_run,
            "metrics": metrics,
            "gate_status": gate_status
        }

    async def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up...")
        await self.memory.close()


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="RSI Validation Runner")
    parser.add_argument(
        "--cycles", type=int, default=10,
        help="Number of cycles to run"
    )
    parser.add_argument(
        "--until-gate", action="store_true",
        help="Run until phase gate passes"
    )
    parser.add_argument(
        "--max-cycles", type=int, default=100,
        help="Maximum cycles when running until gate"
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Just show current status"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--output", type=str,
        help="Output file for results (JSON)"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load configuration with env var expansion
    try:
        config = load_config()
    except FileNotFoundError:
        logger.error("config.yaml not found")
        return

    # Create validator
    validator = RSIValidator(config)

    try:
        await validator.initialize()

        if args.status:
            result = await validator.get_status()
        elif args.until_gate:
            result = await validator.run_until_gate(max_cycles=args.max_cycles)
        else:
            result = await validator.run_cycles(args.cycles)

        # Print summary
        print("\n" + "="*60)
        print("RSI VALIDATION SUMMARY")
        print("="*60)

        if "validation" in result:
            v = result["validation"]
            print(f"\nCycles Run: {result['cycles_run']}")
            print(f"Phase Gate: {'✓ PASSED' if result['phase_gate']['passed'] else '✗ NOT PASSED'}")

            print("\nHypothesis Tests:")
            for test in v.get("tests", []):
                status = "✓" if test["passed"] else "✗"
                print(f"  {status} {test['hypothesis']}: {test['value']:.3f} "
                      f"(threshold: {test['threshold']}, margin: {test['margin']:.3f})")

            print("\nGate Criteria:")
            for key, passed in result["phase_gate"]["criteria"].items():
                status = "✓" if passed else "✗"
                print(f"  {status} {key}")

        elif "gate_status" in result:
            print(f"\nCycles Run: {result['cycles_run']}")
            print("\nGate Requirements:")
            for key, req in result["gate_status"]["requirements"].items():
                print(f"  • {key}: {req}")

        # Save to file if requested
        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\nResults saved to: {args.output}")

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        await validator.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
