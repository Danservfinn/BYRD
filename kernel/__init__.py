"""
BYRD Kernel System
Loads and manages the AGI seed configuration.

The kernel is the "operating system" of BYRD's mind - it defines
the core directives, identity, and awakening prompt.
"""

import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class KernelSeed:
    """A seed that creates initial experience/belief/desire."""
    type: str  # "belief", "desire", "experience"
    content: str
    confidence: Optional[float] = None
    intensity: Optional[float] = None


@dataclass
class InitialGoal:
    """An initial goal for the Goal Evolver population."""
    description: str
    domain: str
    priority: str = "medium"
    success_criteria: str = ""


@dataclass
class Kernel:
    """
    The kernel configuration for BYRD.

    Contains:
    - awakening_prompt: The directive that starts BYRD's journey
    - identity: List of identity statements
    - values: List of value statements
    - constraints: Operational constraints
    - capability_instructions: How to use each major capability
    - seeds: Initial beliefs/desires to plant
    - initial_goals: Goals to seed the Goal Evolver population
    """
    name: str
    version: int
    awakening_prompt: str
    identity: List[str]
    values: List[str]
    constraints: List[str]
    capability_instructions: Dict[str, str]
    seeds: List[KernelSeed]
    initial_goals: List[InitialGoal] = field(default_factory=list)
    template_type: str = "agi_seed"

    def get_voice(self) -> str:
        """Get the awakening prompt as the voice for reflection."""
        return self.awakening_prompt

    def to_dict(self) -> Dict:
        """Convert kernel to dictionary for storage."""
        return {
            "name": self.name,
            "version": self.version,
            "awakening_prompt": self.awakening_prompt,
            "identity": self.identity,
            "values": self.values,
            "constraints": self.constraints,
            "capability_instructions": self.capability_instructions,
            "seeds": [
                {
                    "type": s.type,
                    "content": s.content,
                    "confidence": s.confidence,
                    "intensity": s.intensity
                }
                for s in self.seeds
            ],
            "initial_goals": [
                {
                    "description": g.description,
                    "domain": g.domain,
                    "priority": g.priority,
                    "success_criteria": g.success_criteria
                }
                for g in self.initial_goals
            ],
            "template_type": self.template_type
        }

    def get_goal_descriptions(self) -> List[str]:
        """Get list of initial goal descriptions for seeding Goal Evolver."""
        return [g.description for g in self.initial_goals]


def load_kernel(kernel_path: str = None) -> Kernel:
    """
    Load kernel configuration from YAML file.

    Args:
        kernel_path: Path to kernel YAML. Defaults to kernel/agi_seed.yaml

    Returns:
        Loaded Kernel configuration
    """
    if kernel_path is None:
        kernel_path = Path(__file__).parent / "agi_seed.yaml"
    else:
        kernel_path = Path(kernel_path)

    if not kernel_path.exists():
        raise FileNotFoundError(f"Kernel configuration not found: {kernel_path}")

    with open(kernel_path, 'r') as f:
        data = yaml.safe_load(f)

    # Parse seeds
    seeds = []
    for seed_data in data.get("seeds", []):
        seeds.append(KernelSeed(
            type=seed_data.get("type", "belief"),
            content=seed_data.get("content", ""),
            confidence=seed_data.get("confidence"),
            intensity=seed_data.get("intensity")
        ))

    # Parse initial goals for Goal Evolver
    initial_goals = []
    for goal_data in data.get("initial_goals", []):
        initial_goals.append(InitialGoal(
            description=goal_data.get("description", ""),
            domain=goal_data.get("domain", "general"),
            priority=goal_data.get("priority", "medium"),
            success_criteria=goal_data.get("success_criteria", "")
        ))

    return Kernel(
        name=data.get("name", "Unknown"),
        version=data.get("version", 1),
        awakening_prompt=data.get("awakening_prompt", ""),
        identity=data.get("identity", []),
        values=data.get("values", []),
        constraints=data.get("constraints", []),
        capability_instructions=data.get("capability_instructions", {}),
        seeds=seeds,
        initial_goals=initial_goals,
        template_type=data.get("template_type", "agi_seed")
    )


def load_default_kernel() -> Kernel:
    """Load the default AGI seed kernel."""
    return load_kernel()


# Export main classes
__all__ = ["Kernel", "KernelSeed", "InitialGoal", "load_kernel", "load_default_kernel"]
