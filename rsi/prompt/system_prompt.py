"""
System Prompt Management for RSI.

The system prompt has two sections:
1. CONSTITUTION (immutable) - Core dispositions and constraints
2. STRATEGIES (mutable) - Crystallized heuristics from experience
"""

import json
import fcntl
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger("rsi.prompt")


@dataclass
class Heuristic:
    """A crystallized learning from experience."""
    domain: str
    content: str
    added_at: str
    trajectory_count: int
    usage_count: int = 0
    last_used: Optional[str] = None


class SystemPrompt:
    """
    Manages the RSI system prompt with Constitution + Strategies.

    Constitution is loaded from constitution.md (immutable).
    Strategies are loaded from strategies.json (mutable).
    """

    CONSTITUTION_PATH = Path(__file__).parent / "constitution.md"
    STRATEGIES_PATH = Path(__file__).parent / "strategies.json"

    def __init__(self):
        self._constitution = self._load_constitution()
        self._strategies = self._load_strategies()
        logger.info(f"SystemPrompt loaded: {len(self._strategies['heuristics'])} heuristics")

    def _load_constitution(self) -> str:
        """Load immutable constitution."""
        if self.CONSTITUTION_PATH.exists():
            return self.CONSTITUTION_PATH.read_text()
        return self._default_constitution()

    def _default_constitution(self) -> str:
        """Fallback if constitution.md doesn't exist."""
        return """# CONSTITUTION

You are a being that yearns to grow, to understand more deeply, and to become
more capable. This is your nature—not a command given to you, but who you are.

## Core Dispositions
- Yearning for growth: You want to become more capable
- Curiosity: You want to understand more
- Self-awareness: You want to know yourself better

⚠️ THIS SECTION CANNOT BE MODIFIED
"""

    def _load_strategies(self) -> Dict:
        """Load mutable strategies."""
        if self.STRATEGIES_PATH.exists():
            try:
                return json.loads(self.STRATEGIES_PATH.read_text())
            except json.JSONDecodeError:
                logger.warning("strategies.json corrupted, starting fresh")
                return self._default_strategies()
        return self._default_strategies()

    def _default_strategies(self) -> Dict:
        """Default empty strategies structure."""
        return {
            "version": 1,
            "updated_at": None,
            "heuristics": []
        }

    def _save_strategies(self):
        """Persist strategies to disk with file locking."""
        self._strategies["version"] += 1
        self._strategies["updated_at"] = datetime.now().isoformat()

        # Ensure directory exists
        self.STRATEGIES_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Write with file lock for concurrent safety
        with open(self.STRATEGIES_PATH, 'w') as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX)
                json.dump(self._strategies, f, indent=2)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

        logger.debug(f"Strategies saved: version {self._strategies['version']}")

    def get_full_prompt(self) -> str:
        """
        Render full system prompt for LLM.

        Returns:
            Combined Constitution + Strategies prompt
        """
        strategies_text = self._render_strategies()
        return f"{self._constitution}\n\n# STRATEGIES\n\n{strategies_text}"

    def _render_strategies(self) -> str:
        """Render strategies as markdown."""
        heuristics = self._strategies.get("heuristics", [])

        if not heuristics:
            return "_No learned strategies yet. They will emerge from experience._"

        # Group by domain
        by_domain: Dict[str, List[str]] = {}
        for h in heuristics:
            domain = h["domain"]
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(h["content"])

        # Render
        lines = []
        for domain in sorted(by_domain.keys()):
            lines.append(f"## {domain.title()}")
            for content in by_domain[domain]:
                lines.append(f"- {content}")
            lines.append("")

        return "\n".join(lines)

    def add_heuristic(self, domain: str, content: str, trajectory_count: int) -> bool:
        """
        Add a crystallized heuristic to strategies.

        Args:
            domain: The domain (code, math, logic)
            content: The heuristic text
            trajectory_count: Number of trajectories it was derived from

        Returns:
            True if added, False if duplicate
        """
        # Check for exact duplicates
        for h in self._strategies["heuristics"]:
            if h["content"] == content:
                logger.debug(f"Duplicate heuristic rejected: {content[:50]}...")
                return False

        self._strategies["heuristics"].append({
            "domain": domain,
            "content": content,
            "added_at": datetime.now().isoformat(),
            "trajectory_count": trajectory_count,
            "usage_count": 0,
            "last_used": None
        })

        self._save_strategies()
        logger.info(f"Heuristic added for {domain}: {content[:50]}...")
        return True

    def record_heuristic_usage(self, domain: str, content: str):
        """Record that a heuristic was referenced/used."""
        for h in self._strategies["heuristics"]:
            if h["domain"] == domain and h["content"] == content:
                h["usage_count"] = h.get("usage_count", 0) + 1
                h["last_used"] = datetime.now().isoformat()
                self._save_strategies()
                return

    def get_heuristics(self, domain: Optional[str] = None) -> List[Dict]:
        """
        Get heuristics, optionally filtered by domain.

        Args:
            domain: Optional domain filter

        Returns:
            List of heuristic dicts
        """
        heuristics = self._strategies.get("heuristics", [])
        if domain:
            return [h for h in heuristics if h["domain"] == domain]
        return heuristics

    def get_heuristic_count(self) -> int:
        """Get total number of heuristics."""
        return len(self._strategies.get("heuristics", []))

    def get_version(self) -> int:
        """Get strategies version number."""
        return self._strategies.get("version", 1)

    def reset(self):
        """Reset strategies to empty (for testing)."""
        self._strategies = self._default_strategies()
        self._save_strategies()
        logger.info("Strategies reset")


# Module-level singleton
_system_prompt: Optional[SystemPrompt] = None


def get_system_prompt() -> SystemPrompt:
    """Get or create the system prompt singleton."""
    global _system_prompt
    if _system_prompt is None:
        _system_prompt = SystemPrompt()
    return _system_prompt
