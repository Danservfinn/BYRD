"""
Bootstrap Manager - Handles cold start for crystallization.

Problem: Crystallization requires 20+ trajectories. New domain = 0 trajectories.
Solution: Seed domains with curated trajectories and use lower initial threshold.
"""

from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger("rsi.crystallization.bootstrap")


class BootstrapManager:
    """
    Manages the cold start problem for crystallization.

    Features:
    - Seed trajectories for new domains
    - Lower threshold during bootstrap phase
    - Track maturity per domain
    - Phase out bootstrap trajectories after first crystallization
    """

    BOOTSTRAP_THRESHOLD = 10  # Lower threshold during bootstrap
    MATURE_THRESHOLD = 20  # Full threshold after first crystallization

    # Curated seed trajectories for common domains
    SEED_TRAJECTORIES = {
        "code": [
            {
                "problem": "Debug a function that returns incorrect values for edge cases",
                "approach": "Add assertions and test with empty/null inputs first",
                "success": True
            },
            {
                "problem": "Optimize a slow loop that processes large lists",
                "approach": "Replace list operations with set/dict for O(1) lookups",
                "success": True
            },
            {
                "problem": "Fix async function that hangs intermittently",
                "approach": "Add timeouts and trace await points with logging",
                "success": True
            },
            {
                "problem": "Refactor duplicated code across multiple functions",
                "approach": "Extract common pattern into helper function with clear interface",
                "success": True
            },
            {
                "problem": "Handle API errors gracefully in production code",
                "approach": "Implement retry with exponential backoff and fallback values",
                "success": True
            }
        ],
        "math": [
            {
                "problem": "Solve system of linear equations numerically",
                "approach": "Convert to matrix form, use numpy.linalg.solve with condition checking",
                "success": True
            },
            {
                "problem": "Find roots of polynomial equation",
                "approach": "Use numerical methods (Newton-Raphson) with multiple starting points",
                "success": True
            },
            {
                "problem": "Optimize function with constraints",
                "approach": "Apply Lagrange multipliers or use scipy.optimize with bounds",
                "success": True
            }
        ],
        "logic": [
            {
                "problem": "Validate logical argument with multiple premises",
                "approach": "List all premises, identify logical form, check for valid inference patterns",
                "success": True
            },
            {
                "problem": "Identify fallacy in reasoning chain",
                "approach": "Break down argument step by step, verify each inference independently",
                "success": True
            },
            {
                "problem": "Construct proof by contradiction",
                "approach": "Assume negation, derive consequences systematically until contradiction found",
                "success": True
            }
        ]
    }

    def __init__(self, memory, experience_library=None):
        """
        Initialize bootstrap manager.

        Args:
            memory: Memory instance
            experience_library: Optional ExperienceLibrary
        """
        self.memory = memory
        self.experience_library = experience_library

        # Track which domains have been seeded and matured
        self._seeded_domains: Dict[str, bool] = {}
        self._matured_domains: Dict[str, bool] = {}

    async def ensure_bootstrap(self, domain: str):
        """
        Ensure domain has bootstrap trajectories.

        Args:
            domain: Domain to bootstrap
        """
        if domain in self._seeded_domains:
            return

        if domain not in self.SEED_TRAJECTORIES:
            logger.debug(f"No seed trajectories for domain: {domain}")
            self._seeded_domains[domain] = True
            return

        # Check if domain already has trajectories
        existing = await self._get_trajectory_count(domain)
        if existing >= self.BOOTSTRAP_THRESHOLD:
            logger.debug(f"Domain {domain} already has {existing} trajectories")
            self._seeded_domains[domain] = True
            return

        # Seed the domain
        await self.seed_domain(domain)

    async def seed_domain(self, domain: str):
        """
        Seed a domain with curated trajectories.

        Args:
            domain: Domain to seed
        """
        trajectories = self.SEED_TRAJECTORIES.get(domain, [])
        if not trajectories:
            logger.warning(f"No seed trajectories for domain: {domain}")
            return

        logger.info(f"Seeding {domain} with {len(trajectories)} bootstrap trajectories")

        for i, t in enumerate(trajectories):
            try:
                if self.experience_library:
                    await self.experience_library.store_trajectory(
                        desire={"id": f"bootstrap_{domain}_{i}", "description": "bootstrap"},
                        domain=domain,
                        problem=t["problem"],
                        solution="(bootstrap seed)",
                        approach=t["approach"],
                        success=t["success"],
                        metadata={"bootstrap": True}
                    )
                else:
                    await self.memory.store_trajectory(
                        id=f"bootstrap_{domain}_{i}_{datetime.now().strftime('%Y%m%d')}",
                        desire_id=f"bootstrap_{domain}",
                        domain=domain,
                        problem=t["problem"],
                        solution="(bootstrap seed)",
                        approach=t["approach"],
                        success=t["success"]
                    )
            except Exception as e:
                logger.warning(f"Failed to store bootstrap trajectory: {e}")

        self._seeded_domains[domain] = True

    async def _get_trajectory_count(self, domain: str) -> int:
        """Get count of trajectories for domain."""
        try:
            if self.experience_library:
                return await self.experience_library.get_trajectory_count(domain)
            trajectories = await self.memory.get_successful_trajectories(domain, limit=100)
            return len(trajectories)
        except Exception:
            return 0

    def get_threshold(self, domain: str) -> int:
        """
        Get crystallization threshold for domain.

        Returns lower threshold during bootstrap, full threshold after
        first crystallization.

        Args:
            domain: Domain to check

        Returns:
            Threshold count
        """
        if self._matured_domains.get(domain):
            return self.MATURE_THRESHOLD
        return self.BOOTSTRAP_THRESHOLD

    def is_mature(self, domain: str) -> bool:
        """Check if domain has matured past bootstrap phase."""
        return self._matured_domains.get(domain, False)

    async def on_crystallization(self, domain: str):
        """
        Called when crystallization succeeds for a domain.

        Marks domain as mature and phases out bootstrap trajectories.

        Args:
            domain: Domain that crystallized
        """
        if self._matured_domains.get(domain):
            return  # Already mature

        logger.info(f"Domain {domain} matured after first crystallization")
        self._matured_domains[domain] = True

        # Optionally mark bootstrap trajectories as inactive
        await self._mark_bootstrap_inactive(domain)

    async def _mark_bootstrap_inactive(self, domain: str):
        """Mark bootstrap trajectories as inactive for the domain."""
        try:
            # This would be a memory operation to mark bootstrap trajectories
            # as not to be used in future crystallizations
            await self.memory.mark_bootstrap_trajectories_inactive(domain)
        except Exception as e:
            logger.debug(f"Could not mark bootstrap inactive (may not be implemented): {e}")

    def get_status(self) -> Dict:
        """Get bootstrap status for all domains."""
        return {
            "seeded": dict(self._seeded_domains),
            "matured": dict(self._matured_domains),
            "available_seeds": list(self.SEED_TRAJECTORIES.keys())
        }

    def add_seed_trajectory(
        self,
        domain: str,
        problem: str,
        approach: str,
        success: bool = True
    ):
        """
        Add a custom seed trajectory for a domain.

        This allows extending the bootstrap set at runtime.

        Args:
            domain: Target domain
            problem: Problem description
            approach: Approach taken
            success: Whether it succeeded
        """
        if domain not in self.SEED_TRAJECTORIES:
            self.SEED_TRAJECTORIES[domain] = []

        self.SEED_TRAJECTORIES[domain].append({
            "problem": problem,
            "approach": approach,
            "success": success
        })

        logger.info(f"Added custom seed trajectory for {domain}")

    def reset(self):
        """Reset bootstrap state."""
        self._seeded_domains.clear()
        self._matured_domains.clear()
