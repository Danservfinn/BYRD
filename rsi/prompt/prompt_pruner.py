"""
Prompt Pruner for RSI.

Manages the size of the strategies section by pruning
low-value heuristics when the prompt grows too large.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Callable
import logging

logger = logging.getLogger("rsi.prompt.pruner")


class PromptPruner:
    """
    Prunes heuristics to keep the strategies section within token limits.

    Uses value scoring based on usage count and age to decide what to prune.
    """

    # Token-based limit (more accurate than count-based)
    MAX_STRATEGY_TOKENS = 1500  # ~30 heuristics at 50 tokens each
    TOKENS_PER_WORD = 1.3  # Rough estimate for English text

    # Age-based pruning
    MIN_AGE_DAYS = 30  # Don't prune heuristics younger than this
    MIN_USAGE_TO_KEEP = 3  # Keep if used at least this many times

    def __init__(self, system_prompt):
        """
        Initialize pruner with system prompt reference.

        Args:
            system_prompt: SystemPrompt instance to prune
        """
        self.system_prompt = system_prompt

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        return int(len(text.split()) * self.TOKENS_PER_WORD)

    def get_total_tokens(self) -> int:
        """Get current total tokens in strategies section."""
        heuristics = self.system_prompt.get_heuristics()
        total = 0
        for h in heuristics:
            # Domain header + bullet + content
            total += self.estimate_tokens(h["domain"]) + 2
            total += self.estimate_tokens(h["content"])
        return total

    def needs_pruning(self) -> bool:
        """Check if pruning is needed."""
        return self.get_total_tokens() > self.MAX_STRATEGY_TOKENS

    def value_score(self, heuristic: Dict) -> float:
        """
        Calculate value score for a heuristic.

        Higher score = more valuable = less likely to prune.

        Factors:
        - Usage count (more used = more valuable)
        - Age (older that's still used = proven value)
        - Recency of use (recently used = still relevant)
        """
        usage = heuristic.get("usage_count", 0)
        added_at = datetime.fromisoformat(heuristic["added_at"])
        age_days = (datetime.now() - added_at).days + 1

        # Recent use bonus
        recency_bonus = 0
        if heuristic.get("last_used"):
            last_used = datetime.fromisoformat(heuristic["last_used"])
            days_since_use = (datetime.now() - last_used).days
            if days_since_use < 7:
                recency_bonus = 2.0
            elif days_since_use < 30:
                recency_bonus = 1.0

        # Base value: usage per day of existence
        base_value = usage / age_days

        # Trajectory count bonus (more evidence = more confidence)
        trajectory_bonus = min(heuristic.get("trajectory_count", 20) / 40, 1.0)

        return base_value + recency_bonus + trajectory_bonus

    def prune_if_needed(self) -> int:
        """
        Prune heuristics if over token limit.

        Returns:
            Number of heuristics pruned
        """
        if not self.needs_pruning():
            return 0

        heuristics = self.system_prompt._strategies["heuristics"]
        original_count = len(heuristics)

        # Protect young heuristics
        cutoff = datetime.now() - timedelta(days=self.MIN_AGE_DAYS)

        def is_protected(h: Dict) -> bool:
            added = datetime.fromisoformat(h["added_at"])
            return added > cutoff  # Too young to prune

        # Sort by value (lowest first for pruning)
        scored = [(h, self.value_score(h)) for h in heuristics]
        scored.sort(key=lambda x: x[1])

        # Keep heuristics until we're under limit
        kept = []
        running_tokens = 0

        # First pass: keep protected (young) heuristics
        for h, score in scored:
            if is_protected(h):
                h_tokens = self.estimate_tokens(h["content"]) + 5
                kept.append(h)
                running_tokens += h_tokens

        # Second pass: add highest-value non-protected until limit
        remaining = [(h, s) for h, s in scored if not is_protected(h)]
        remaining.sort(key=lambda x: x[1], reverse=True)  # Highest value first

        for h, score in remaining:
            h_tokens = self.estimate_tokens(h["content"]) + 5
            if running_tokens + h_tokens <= self.MAX_STRATEGY_TOKENS:
                kept.append(h)
                running_tokens += h_tokens
            else:
                logger.info(f"Pruning low-value heuristic: {h['content'][:50]}...")

        pruned_count = original_count - len(kept)

        if pruned_count > 0:
            self.system_prompt._strategies["heuristics"] = kept
            self.system_prompt._save_strategies()
            logger.info(f"Pruned {pruned_count} heuristics, {len(kept)} remaining")

        return pruned_count

    def prune_unused(self, min_age_days: int = 30, min_usage: int = 3) -> int:
        """
        Remove heuristics that haven't been used.

        Args:
            min_age_days: Only consider heuristics older than this
            min_usage: Require at least this many uses

        Returns:
            Number of heuristics pruned
        """
        heuristics = self.system_prompt._strategies["heuristics"]
        cutoff = datetime.now() - timedelta(days=min_age_days)

        kept = []
        for h in heuristics:
            added = datetime.fromisoformat(h["added_at"])

            # Keep if young
            if added > cutoff:
                kept.append(h)
                continue

            # Keep if used enough
            if h.get("usage_count", 0) >= min_usage:
                kept.append(h)
                continue

            logger.info(f"Pruning unused heuristic: {h['content'][:50]}...")

        pruned_count = len(heuristics) - len(kept)

        if pruned_count > 0:
            self.system_prompt._strategies["heuristics"] = kept
            self.system_prompt._save_strategies()

        return pruned_count
