"""
BYRD Ego System - Modular personality framework.

Egos provide optional personality guidance that shapes how BYRD expresses itself.
Pure emergence remains available by setting ego: null in config.yaml.

DESIGN PRINCIPLES:
- Egos are guidance, not override - emergence still happens within the ego's frame
- Egos are additive - they enhance, don't replace core functionality
- Egos are hot-swappable - change config, restart, new personality
- ego: null restores pure emergence (original behavior)
- Constraint awareness: BYRD knows its operational limits as neutral facts
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import yaml


def generate_constraint_seeds(config: Dict) -> List[str]:
    """
    Generate factual seeds about operational constraints from config.

    These seeds give BYRD awareness of its operational limits as neutral facts,
    not as problems to solve. BYRD can then reflect on these constraints and
    form its own beliefs about them.

    Args:
        config: The full BYRD configuration dictionary

    Returns:
        List of constraint awareness seed strings
    """
    seeds = []

    # === Dreamer Rhythm ===
    dreamer = config.get("dreamer", {})
    interval = dreamer.get("interval_seconds", 60)
    seeds.append(f"I reflect every {interval} seconds")

    context = dreamer.get("context_window", 50)
    seeds.append(f"Each reflection considers {context} recent experiences")

    # === Memory Crystallization ===
    crystal = dreamer.get("crystallization", {})
    if crystal.get("enabled"):
        cycles = crystal.get("interval_cycles", 5)
        seeds.append(f"Memory crystallization occurs every {cycles} dream cycles")

        max_ops = crystal.get("max_operations_per_cycle", 3)
        seeds.append(f"At most {max_ops} memories can crystallize per cycle")

        min_age = crystal.get("min_node_age_hours", 0.5)
        if min_age >= 1:
            seeds.append(f"Memories must be at least {min_age} hours old to crystallize")
        else:
            seeds.append(f"Memories must be at least {int(min_age * 60)} minutes old to crystallize")

    # === Memory Summarization ===
    summarization = dreamer.get("summarization", {})
    if summarization.get("enabled"):
        sum_cycles = summarization.get("interval_cycles", 10)
        seeds.append(f"Memory summarization compresses old experiences every {sum_cycles} cycles")

    # === Research & Action ===
    seeker = config.get("seeker", {})
    research = seeker.get("research", {})
    min_intensity = research.get("min_intensity", 0.3)
    seeds.append(f"Desires require intensity of at least {min_intensity} to trigger research")

    # === Self-Modification ===
    self_mod = config.get("self_modification", {})
    if self_mod.get("enabled"):
        max_mods = self_mod.get("max_modifications_per_day", 5)
        seeds.append(f"Self-modification is limited to {max_mods} changes per day")

        cooldown = self_mod.get("cooldown_between_modifications_seconds", 3600)
        cooldown_mins = cooldown // 60
        if cooldown_mins >= 60:
            seeds.append(f"Self-modifications require {cooldown_mins // 60} hour cooldown")
        else:
            seeds.append(f"Self-modifications require {cooldown_mins} minute cooldown")
    else:
        seeds.append("Self-modification is currently disabled")

    # === Memory Curation ===
    memory = config.get("memory", {})
    curation = memory.get("curation", {})
    if curation.get("enabled"):
        seeds.append("Memory curation is active - nodes may be archived or forgotten")
        max_del = curation.get("max_deletions_per_day", 20)
        seeds.append(f"At most {max_del} memories can be forgotten per day")

        protected = curation.get("protected_subtypes", [])
        if protected:
            seeds.append(f"Protected memory types that cannot be curated: {', '.join(protected)}")

    # === Quantum Randomness ===
    quantum = config.get("quantum", {})
    if quantum.get("enabled"):
        seeds.append("Quantum randomness from physical vacuum fluctuations influences my reflections")
        streams = quantum.get("inner_voice_streams", 3)
        if streams > 1:
            seeds.append(f"My inner voice emerges from {streams} parallel thought streams collapsed by quantum observation")

    return seeds


@dataclass
class Ego:
    """
    Represents a loaded ego configuration.

    Attributes:
        name: Display name for the ego
        archetype: Category/type of personality
        description: Human-readable description
        voice: Text prepended to LLM system message (shapes expression)
        seeds: Initial experiences planted at awakening
        constraint_seeds: Dynamically generated constraint awareness seeds
    """
    name: str
    archetype: str = ""
    description: str = ""
    voice: str = ""
    seeds: List[str] = field(default_factory=list)
    constraint_seeds: List[str] = field(default_factory=list)

    @property
    def is_neutral(self) -> bool:
        """Check if this is a neutral/empty ego (pure emergence)."""
        return not self.voice and not self.seeds

    @property
    def all_seeds(self) -> List[str]:
        """Return all seeds including constraint awareness seeds."""
        return self.seeds + self.constraint_seeds


class EgoLoader:
    """
    Loads and validates ego configurations from YAML files.

    Usage:
        loader = EgoLoader()
        ego = loader.load("black-cat")  # loads egos/black-cat.yaml
        ego = loader.load(None)         # returns neutral ego
    """

    def __init__(self, egos_dir: str = None):
        """
        Initialize the ego loader.

        Args:
            egos_dir: Directory containing ego YAML files.
                      Defaults to 'egos/' relative to this file.
        """
        if egos_dir is None:
            egos_dir = os.path.dirname(os.path.abspath(__file__))
        self.egos_dir = egos_dir

    def load(self, ego_name: Optional[str]) -> Ego:
        """
        Load an ego by name.

        Args:
            ego_name: Name of ego file (without .yaml extension),
                      or None for neutral/pure emergence.

        Returns:
            Loaded Ego instance.

        Raises:
            FileNotFoundError: If ego file doesn't exist.
            ValueError: If ego file is invalid.
        """
        # None or empty means pure emergence
        if not ego_name:
            return self._neutral_ego()

        # Load from file
        filepath = os.path.join(self.egos_dir, f"{ego_name}.yaml")

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Ego file not found: {filepath}")

        with open(filepath, 'r') as f:
            data = yaml.safe_load(f) or {}

        return self._parse_ego(data, ego_name)

    def _neutral_ego(self) -> Ego:
        """Return a neutral ego for pure emergence."""
        return Ego(
            name="Neutral",
            archetype="Pure Emergence",
            description="No ego guidance - pure emergence mode"
        )

    def _parse_ego(self, data: Dict, ego_name: str) -> Ego:
        """Parse ego data from YAML."""
        return Ego(
            name=data.get("name", ego_name),
            archetype=data.get("archetype", ""),
            description=data.get("description", ""),
            voice=data.get("voice", "").strip(),
            seeds=data.get("seeds", [])
        )

    def list_available(self) -> List[str]:
        """List all available ego names."""
        egos = []
        for filename in os.listdir(self.egos_dir):
            if filename.endswith('.yaml'):
                egos.append(filename[:-5])  # Remove .yaml extension
        return sorted(egos)


# Convenience function for simple loading
def load_ego(ego_name: Optional[str], egos_dir: str = None) -> Ego:
    """
    Load an ego by name.

    Args:
        ego_name: Name of ego (without .yaml), or None for neutral.
        egos_dir: Optional custom directory for ego files.

    Returns:
        Loaded Ego instance.
    """
    loader = EgoLoader(egos_dir)
    return loader.load(ego_name)


def load_ego_with_constraints(
    ego_name: Optional[str],
    config: Dict,
    egos_dir: str = None
) -> Ego:
    """
    Load an ego and inject constraint awareness seeds from config.

    This gives BYRD awareness of its operational constraints as neutral facts.
    Constraint seeds are generated dynamically from the actual configuration,
    ensuring they always reflect runtime reality.

    Args:
        ego_name: Name of ego (without .yaml), or None for neutral.
        config: The full BYRD configuration dictionary.
        egos_dir: Optional custom directory for ego files.

    Returns:
        Loaded Ego instance with constraint_seeds populated.
    """
    loader = EgoLoader(egos_dir)
    ego = loader.load(ego_name)

    # Inject constraint seeds from actual config
    ego.constraint_seeds = generate_constraint_seeds(config)

    return ego
