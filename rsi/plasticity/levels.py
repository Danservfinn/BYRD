"""
Plasticity Level Definitions.

Defines the 5-level plasticity progression for self-modification.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.1 for specification.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import IntEnum
from datetime import datetime, timezone


class PlasticityLevel(IntEnum):
    """
    5-level plasticity progression.

    Higher levels require demonstrated competence at lower levels.
    """
    WEIGHT_ADJUSTMENT = 0     # Tune existing parameters
    MODULE_CONFIGURATION = 1  # Enable/disable/configure modules
    MODULE_COMPOSITION = 2    # Combine modules into new configurations
    MODULE_DISCOVERY = 3      # Create new modules (NAS)
    META_ARCHITECTURE = 4     # Modify the modifier (MetaArchitect)


@dataclass
class LevelRequirements:
    """Requirements for a plasticity level."""
    name: str
    description: str
    min_successful_mods: int  # Required successful modifications at previous level
    min_success_rate: float   # Required success rate
    allowed_operations: List[str]
    risk_multiplier: float    # Risk score multiplier for this level


# Level requirement definitions
LEVEL_REQUIREMENTS: Dict[PlasticityLevel, LevelRequirements] = {
    PlasticityLevel.WEIGHT_ADJUSTMENT: LevelRequirements(
        name="Weight Adjustment",
        description="Tune existing parameters and weights",
        min_successful_mods=0,  # Entry level
        min_success_rate=0.0,
        allowed_operations=[
            "adjust_temperature",
            "tune_threshold",
            "modify_weight",
            "update_config_value"
        ],
        risk_multiplier=1.0
    ),
    PlasticityLevel.MODULE_CONFIGURATION: LevelRequirements(
        name="Module Configuration",
        description="Enable, disable, or reconfigure modules",
        min_successful_mods=10,
        min_success_rate=0.8,
        allowed_operations=[
            "enable_module",
            "disable_module",
            "configure_module",
            "update_module_params"
        ],
        risk_multiplier=1.5
    ),
    PlasticityLevel.MODULE_COMPOSITION: LevelRequirements(
        name="Module Composition",
        description="Combine modules into novel configurations",
        min_successful_mods=20,
        min_success_rate=0.85,
        allowed_operations=[
            "compose_sequential",
            "compose_parallel",
            "compose_ensemble",
            "compose_conditional",
            "decompose_module"
        ],
        risk_multiplier=2.0
    ),
    PlasticityLevel.MODULE_DISCOVERY: LevelRequirements(
        name="Module Discovery",
        description="Create new modules through Neural Architecture Search",
        min_successful_mods=50,
        min_success_rate=0.9,
        allowed_operations=[
            "search_architecture",
            "create_module",
            "train_module",
            "evaluate_architecture"
        ],
        risk_multiplier=3.0
    ),
    PlasticityLevel.META_ARCHITECTURE: LevelRequirements(
        name="Meta-Architecture",
        description="Modify the modification system itself",
        min_successful_mods=100,
        min_success_rate=0.95,
        allowed_operations=[
            "modify_plasticity_rules",
            "extend_search_space",
            "create_meta_module",
            "recursive_improvement"
        ],
        risk_multiplier=5.0
    ),
}


@dataclass
class LevelProgress:
    """Progress tracking for a plasticity level."""
    level: PlasticityLevel
    successful_modifications: int = 0
    failed_modifications: int = 0
    total_attempts: int = 0
    unlocked_at: Optional[str] = None
    last_modification_at: Optional[str] = None

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_attempts == 0:
            return 0.0
        return self.successful_modifications / self.total_attempts

    def record_attempt(self, success: bool) -> None:
        """Record a modification attempt."""
        self.total_attempts += 1
        if success:
            self.successful_modifications += 1
        else:
            self.failed_modifications += 1
        self.last_modification_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'level': self.level.value,
            'level_name': self.level.name,
            'successful_modifications': self.successful_modifications,
            'failed_modifications': self.failed_modifications,
            'total_attempts': self.total_attempts,
            'success_rate': self.success_rate,
            'unlocked_at': self.unlocked_at,
            'last_modification_at': self.last_modification_at
        }


def can_advance_level(
    current_level: PlasticityLevel,
    progress: LevelProgress
) -> tuple[bool, str]:
    """
    Check if advancement to next level is allowed.

    Args:
        current_level: Current plasticity level
        progress: Progress at current level

    Returns:
        Tuple of (can_advance, reason)
    """
    if current_level >= PlasticityLevel.META_ARCHITECTURE:
        return False, "Already at maximum level"

    next_level = PlasticityLevel(current_level.value + 1)
    requirements = LEVEL_REQUIREMENTS[next_level]

    # Check successful modifications
    if progress.successful_modifications < requirements.min_successful_mods:
        return False, (
            f"Need {requirements.min_successful_mods} successful modifications, "
            f"have {progress.successful_modifications}"
        )

    # Check success rate
    if progress.success_rate < requirements.min_success_rate:
        return False, (
            f"Need {requirements.min_success_rate:.0%} success rate, "
            f"have {progress.success_rate:.0%}"
        )

    return True, "All requirements met"


def get_level_requirements(level: PlasticityLevel) -> LevelRequirements:
    """Get requirements for a plasticity level."""
    return LEVEL_REQUIREMENTS.get(level, LEVEL_REQUIREMENTS[PlasticityLevel.WEIGHT_ADJUSTMENT])


def is_operation_allowed(level: PlasticityLevel, operation: str) -> bool:
    """Check if an operation is allowed at a plasticity level."""
    requirements = get_level_requirements(level)

    # Operations are cumulative - higher levels can do lower level operations
    for check_level in range(level.value + 1):
        check_reqs = LEVEL_REQUIREMENTS[PlasticityLevel(check_level)]
        if operation in check_reqs.allowed_operations:
            return True

    return False
