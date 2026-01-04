"""
Crystallizer - Extracts heuristics from successful learning trajectories.

When enough successful trajectories accumulate in a domain (default: 20+),
the Crystallizer extracts a generalizable principle and adds it to the
Strategies section of the system prompt.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime
import logging

logger = logging.getLogger("rsi.crystallization")


@dataclass
class Heuristic:
    """A crystallized learning heuristic."""
    id: str
    domain: str
    content: str
    supporting_trajectories: int
    created_at: str
    usage_count: int = 0


class Crystallizer:
    """
    Extracts heuristics from successful trajectories.

    Process:
    1. Check if domain has enough trajectories (threshold)
    2. Sample trajectories for diversity
    3. Use LLM to extract generalizable principle
    4. Validate heuristic is actionable
    5. Check for duplicates
    6. Add to system prompt strategies
    """

    TRAJECTORY_THRESHOLD = 20  # Minimum trajectories for crystallization
    BOOTSTRAP_THRESHOLD = 10  # Lower threshold during bootstrap

    def __init__(
        self,
        memory,
        llm_client,
        system_prompt,
        experience_library=None
    ):
        """
        Initialize crystallizer.

        Args:
            memory: Memory instance
            llm_client: LLM client for extraction
            system_prompt: SystemPrompt to add heuristics to
            experience_library: Optional ExperienceLibrary for trajectories
        """
        self.memory = memory
        self.llm = llm_client
        self.system_prompt = system_prompt
        self.experience_library = experience_library

        # Track crystallized domains
        self._crystallized_domains: Dict[str, int] = {}

        # Stats
        self._crystallization_attempts = 0
        self._successful_crystallizations = 0

    def get_threshold(self, domain: str) -> int:
        """Get crystallization threshold for domain."""
        if domain in self._crystallized_domains:
            return self.TRAJECTORY_THRESHOLD  # Full threshold after first
        return self.BOOTSTRAP_THRESHOLD  # Lower during bootstrap

    async def maybe_crystallize(self, domain: str) -> Optional[Heuristic]:
        """
        Check if crystallization should occur and do it if ready.

        Args:
            domain: The domain to check

        Returns:
            Heuristic if crystallized, None otherwise
        """
        self._crystallization_attempts += 1

        # Get trajectories
        if self.experience_library:
            trajectories = await self.experience_library.get_successful_trajectories(
                domain, limit=100
            )
        else:
            trajectories = await self.memory.get_successful_trajectories(
                domain, limit=100
            )

        threshold = self.get_threshold(domain)

        if len(trajectories) < threshold:
            logger.debug(
                f"Not enough trajectories for {domain}: "
                f"{len(trajectories)}/{threshold}"
            )
            return None

        logger.info(f"Attempting crystallization for {domain} ({len(trajectories)} trajectories)")

        # Get stratified sample
        if self.experience_library:
            sample = await self.experience_library.get_stratified_sample(domain, 10)
        else:
            sample = self._get_stratified_sample(trajectories, 10)

        # Extract principle
        heuristic_content = await self._extract_principle(sample, domain)

        if not heuristic_content:
            logger.warning(f"Failed to extract principle for {domain}")
            return None

        # Validate actionability
        if not await self._is_actionable(heuristic_content):
            logger.info(f"Heuristic not actionable: {heuristic_content[:50]}...")
            return None

        # Check for duplicates
        existing = self.system_prompt.get_heuristics(domain)
        existing_contents = [h["content"] for h in existing]

        if await self._is_duplicate(heuristic_content, existing_contents):
            logger.info(f"Duplicate heuristic detected: {heuristic_content[:50]}...")
            return None

        # Add to system prompt
        added = self.system_prompt.add_heuristic(
            domain=domain,
            content=heuristic_content,
            trajectory_count=len(trajectories)
        )

        if not added:
            return None

        # Track crystallization
        self._crystallized_domains[domain] = self._crystallized_domains.get(domain, 0) + 1
        self._successful_crystallizations += 1

        # Create heuristic object
        heuristic = Heuristic(
            id=f"heur_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            domain=domain,
            content=heuristic_content,
            supporting_trajectories=len(trajectories),
            created_at=datetime.now().isoformat()
        )

        # Store in memory for tracking
        try:
            await self.memory.store_heuristic(
                id=heuristic.id,
                domain=domain,
                content=heuristic_content,
                trajectory_count=len(trajectories)
            )
        except Exception as e:
            logger.warning(f"Failed to persist heuristic to memory: {e}")

        logger.info(f"Crystallized: {heuristic_content[:80]}...")
        return heuristic

    def _get_stratified_sample(
        self,
        trajectories: List[Dict],
        sample_size: int
    ) -> List[Dict]:
        """Get stratified sample from trajectories."""
        n = len(trajectories)
        if n <= sample_size:
            return trajectories

        # Sort by date (oldest first)
        sorted_trajs = sorted(trajectories, key=lambda t: t.get("created_at", ""))

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

    async def _extract_principle(
        self,
        trajectories: List[Dict],
        domain: str
    ) -> Optional[str]:
        """Extract generalizable principle from trajectories."""
        if not trajectories:
            return None

        # Format trajectories for LLM
        trajectory_summaries = []
        for t in trajectories:
            problem = t.get("problem", "")[:150]
            approach = t.get("approach", "")[:150]
            trajectory_summaries.append(f"- Problem: {problem}... Approach: {approach}...")

        summaries_text = "\n".join(trajectory_summaries)

        prompt = f"""Analyze these successful {domain} problem-solving trajectories:

{summaries_text}

Extract ONE generalizable principle or heuristic that explains why these solutions succeeded.

The principle should be:
- Specific and actionable (tells you WHAT TO DO)
- Applicable to new problems in this domain
- Concise (one clear sentence)

Good example: "When debugging async code, add logging before and after each await to trace execution flow"
Bad example: "Think carefully about async code"

Return ONLY the principle, nothing else."""

        try:
            response = await self.llm.query(prompt, temperature=0.5, max_tokens=200)
            return response.strip().strip('"').strip()
        except Exception as e:
            logger.error(f"Principle extraction failed: {e}")
            return None

    async def _is_actionable(self, heuristic: str) -> bool:
        """Check if heuristic is specific and actionable."""
        # First: keyword check (fast)
        action_verbs = [
            "check", "verify", "add", "remove", "split", "merge",
            "validate", "test", "define", "decompose", "cast",
            "use", "apply", "include", "avoid", "ensure", "log",
            "trace", "before", "after", "first", "always", "never"
        ]
        has_action = any(verb in heuristic.lower() for verb in action_verbs)

        # Reject vague phrases
        vague_phrases = [
            "try harder", "be careful", "think more", "use best practices",
            "consider carefully", "be thorough", "pay attention"
        ]
        is_vague = any(phrase in heuristic.lower() for phrase in vague_phrases)

        if is_vague:
            return False

        if has_action and len(heuristic.split()) >= 5:
            return True

        # Ambiguous: use LLM for final check
        try:
            prompt = f"""Is this heuristic specific and actionable?

Heuristic: "{heuristic}"

A heuristic is actionable if it tells you WHAT TO DO, not just what to think about.

Good: "When debugging async code, add logging before and after each await"
Bad: "Think carefully about async code"

Reply YES or NO only."""

            response = await self.llm.query(prompt, max_tokens=5)
            return "YES" in response.upper()
        except Exception:
            return has_action

    async def _is_duplicate(self, new: str, existing: List[str]) -> bool:
        """Check if heuristic is semantically similar to existing ones."""
        if not existing:
            return False

        # Simple string similarity check first
        new_words = set(new.lower().split())
        for h in existing:
            h_words = set(h.lower().split())
            overlap = len(new_words & h_words) / max(len(new_words | h_words), 1)
            if overlap > 0.7:
                return True

        # LLM check for semantic similarity
        try:
            existing_text = "\n".join(f'- "{h}"' for h in existing[:5])
            prompt = f"""Is this new heuristic essentially the same as any existing one?

New: "{new}"

Existing:
{existing_text}

Reply YES or NO only."""

            response = await self.llm.query(prompt, max_tokens=5)
            return "YES" in response.upper()
        except Exception:
            return False

    def get_stats(self) -> Dict:
        """Get crystallization statistics."""
        return {
            "attempts": self._crystallization_attempts,
            "successful": self._successful_crystallizations,
            "success_rate": self._successful_crystallizations / max(self._crystallization_attempts, 1),
            "domains_crystallized": dict(self._crystallized_domains)
        }

    def reset(self):
        """Reset crystallizer state."""
        self._crystallized_domains.clear()
        self._crystallization_attempts = 0
        self._successful_crystallizations = 0
