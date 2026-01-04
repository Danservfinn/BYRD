"""
Experience Library - Stores and retrieves learning trajectories.

Trajectories are the raw material for crystallization.
When enough successful trajectories accumulate in a domain,
principles can be extracted.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger("rsi.learning.library")


@dataclass
class Trajectory:
    """A complete learning trajectory from desire to outcome."""
    id: str
    desire_id: str
    domain: str
    problem: str
    approach: str
    solution: str
    success: bool
    partial_score: float  # 0.0-1.0 based on tests passed
    created_at: str
    metadata: Optional[Dict] = None


class ExperienceLibrary:
    """
    Stores and retrieves learning trajectories.

    Provides methods for:
    - Storing new trajectories
    - Querying successful trajectories by domain
    - Stratified sampling for crystallization
    """

    def __init__(self, memory):
        """
        Initialize library with memory backend.

        Args:
            memory: Memory instance for Neo4j storage
        """
        self.memory = memory
        self._trajectory_count = 0

    async def store_trajectory(
        self,
        desire: Dict,
        domain: str,
        problem: str,
        solution: str,
        approach: str,
        success: bool,
        partial_score: float = None,
        metadata: Dict = None
    ) -> str:
        """
        Store a learning trajectory.

        Args:
            desire: The originating desire
            domain: Practice domain (code, math, logic)
            problem: The problem that was attempted
            solution: The solution that was generated
            approach: Summary of the approach taken
            success: Whether the attempt succeeded
            partial_score: Optional partial score (0.0-1.0)
            metadata: Optional additional metadata

        Returns:
            Trajectory ID
        """
        self._trajectory_count += 1
        trajectory_id = f"traj_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self._trajectory_count}"

        # Calculate partial score if not provided
        if partial_score is None:
            partial_score = 1.0 if success else 0.0

        trajectory = Trajectory(
            id=trajectory_id,
            desire_id=desire.get("id", "unknown"),
            domain=domain,
            problem=problem[:1000],  # Truncate for storage
            approach=approach[:500],
            solution=solution[:2000],
            success=success,
            partial_score=partial_score,
            created_at=datetime.now().isoformat(),
            metadata=metadata
        )

        # Store in Neo4j
        try:
            await self.memory.store_trajectory(
                id=trajectory.id,
                desire_id=trajectory.desire_id,
                domain=trajectory.domain,
                problem=trajectory.problem,
                solution=trajectory.solution,
                approach=trajectory.approach,
                success=trajectory.success,
                partial_score=trajectory.partial_score
            )
            logger.debug(f"Stored trajectory {trajectory_id}")
        except Exception as e:
            logger.error(f"Failed to store trajectory: {e}")
            # Fallback: record as experience
            await self.memory.record_experience(
                content=f"[TRAJECTORY] {domain} | {'SUCCESS' if success else 'FAIL'} | {approach[:100]}",
                type="trajectory"
            )

        return trajectory_id

    async def get_successful_trajectories(
        self,
        domain: str,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get successful trajectories for a domain.

        Args:
            domain: The domain to query
            limit: Maximum trajectories to return

        Returns:
            List of trajectory dicts, ordered by recency
        """
        try:
            return await self.memory.get_successful_trajectories(
                domain=domain,
                limit=limit
            )
        except Exception as e:
            logger.warning(f"Failed to get trajectories: {e}")
            return []

    async def get_stratified_sample(
        self,
        domain: str,
        sample_size: int = 10
    ) -> List[Dict]:
        """
        Get a stratified sample of trajectories for crystallization.

        Samples from:
        - Oldest trajectories (4)
        - Middle trajectories (3)
        - Newest trajectories (3)

        This ensures temporal diversity in extracted principles.

        Args:
            domain: The domain to sample from
            sample_size: Target sample size

        Returns:
            Stratified sample of trajectories
        """
        all_trajectories = await self.get_successful_trajectories(domain, limit=100)

        if not all_trajectories:
            return []

        n = len(all_trajectories)

        if n <= sample_size:
            return all_trajectories

        # Sort by date (oldest first)
        sorted_trajs = sorted(all_trajectories, key=lambda t: t.get("created_at", ""))

        # Stratified sampling
        sample = []

        # Oldest 40%
        oldest_count = int(sample_size * 0.4)
        sample.extend(sorted_trajs[:oldest_count])

        # Middle 30%
        middle_count = int(sample_size * 0.3)
        mid_start = n // 2 - middle_count // 2
        sample.extend(sorted_trajs[mid_start:mid_start + middle_count])

        # Newest 30%
        newest_count = sample_size - len(sample)
        sample.extend(sorted_trajs[-newest_count:])

        return sample

    async def get_trajectory_count(self, domain: str = None) -> int:
        """
        Get count of trajectories.

        Args:
            domain: Optional domain filter

        Returns:
            Number of trajectories
        """
        try:
            if domain:
                trajectories = await self.get_successful_trajectories(domain, limit=1000)
                return len(trajectories)
            return self._trajectory_count
        except Exception:
            return self._trajectory_count

    async def get_domain_stats(self) -> Dict[str, Dict]:
        """
        Get statistics per domain.

        Returns:
            Dict mapping domain -> stats
        """
        stats = {}

        for domain in ["code", "math", "logic"]:
            try:
                all_trajs = await self.memory.get_trajectories_by_domain(domain, limit=1000)
                success_trajs = [t for t in all_trajs if t.get("success", False)]

                stats[domain] = {
                    "total": len(all_trajs),
                    "successful": len(success_trajs),
                    "success_rate": len(success_trajs) / max(len(all_trajs), 1)
                }
            except Exception:
                stats[domain] = {"total": 0, "successful": 0, "success_rate": 0.0}

        return stats

    async def mark_trajectory_used(self, trajectory_id: str):
        """
        Mark a trajectory as used in crystallization.

        Args:
            trajectory_id: ID of the trajectory
        """
        try:
            await self.memory.update_trajectory(
                trajectory_id,
                used_in_crystallization=True,
                used_at=datetime.now().isoformat()
            )
        except Exception as e:
            logger.warning(f"Failed to mark trajectory as used: {e}")

    def reset(self):
        """Reset library state."""
        self._trajectory_count = 0
