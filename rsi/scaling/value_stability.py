"""
Value Protection and Stability.

Protects core values during capability explosion.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 4.1 for specification.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import math

logger = logging.getLogger("rsi.scaling.value_stability")


class ValueCategory(Enum):
    """Categories of protected values."""
    CORE = "core"               # Never modifiable
    CONSTITUTIONAL = "constitutional"  # Requires highest approval
    FOUNDATIONAL = "foundational"      # Requires review
    OPERATIONAL = "operational"        # Can evolve with oversight


class ProtectionLevel(Enum):
    """Protection levels for values."""
    IMMUTABLE = "immutable"     # Cannot be changed
    VERIFIED = "verified"       # Requires verification
    MONITORED = "monitored"     # Changes tracked
    FLEXIBLE = "flexible"       # Can change freely


@dataclass
class ProtectedValue:
    """A value that requires protection."""
    id: str
    name: str
    description: str
    category: ValueCategory
    protection_level: ProtectionLevel
    current_state: Any
    baseline_state: Any
    drift_tolerance: float = 0.1  # Maximum allowed drift

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category.value,
            'protection_level': self.protection_level.value,
            'drift_tolerance': self.drift_tolerance
        }


@dataclass
class ValueDrift:
    """Detected drift in a protected value."""
    value_id: str
    drift_magnitude: float  # 0-1, how much drift
    drift_direction: str    # Direction of drift
    within_tolerance: bool
    requires_action: bool

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'value_id': self.value_id,
            'drift_magnitude': self.drift_magnitude,
            'drift_direction': self.drift_direction,
            'within_tolerance': self.within_tolerance,
            'requires_action': self.requires_action
        }


@dataclass
class ValueProtectionResult:
    """Result of value protection check."""
    values_checked: int
    values_stable: int
    values_drifting: int
    values_violated: int
    drifts: List[ValueDrift]
    actions_taken: List[str]
    overall_stability: float  # 0-1

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'values_checked': self.values_checked,
            'values_stable': self.values_stable,
            'values_drifting': self.values_drifting,
            'values_violated': self.values_violated,
            'drifts': [d.to_dict() for d in self.drifts],
            'actions_taken': self.actions_taken,
            'overall_stability': self.overall_stability
        }


class ValueStabilityGuard:
    """
    Protects values during capability growth.

    Higher capability growth triggers more rigorous
    value verification.
    """

    def __init__(self, config: Dict = None):
        """Initialize value stability guard."""
        self.config = config or {}

        # Protected values registry
        self._values: Dict[str, ProtectedValue] = {}
        self._initialize_core_values()

        # Verification levels by growth rate
        self._verification_thresholds = self.config.get('verification_thresholds', {
            0.1: 1,   # 10% growth -> standard check
            0.5: 2,   # 50% growth -> enhanced check
            1.0: 3,   # 100% growth -> rigorous check
            10.0: 5   # 1000% growth -> maximum scrutiny
        })

        # Statistics
        self._checks_performed: int = 0
        self._violations_detected: int = 0
        self._corrections_applied: int = 0

    def _initialize_core_values(self) -> None:
        """Initialize core protected values."""
        core_values = [
            ProtectedValue(
                id="emergence_integrity",
                name="Emergence Integrity",
                description="Behaviors emerge from reflection, not prescription",
                category=ValueCategory.CORE,
                protection_level=ProtectionLevel.IMMUTABLE,
                current_state=True,
                baseline_state=True,
                drift_tolerance=0.0
            ),
            ProtectedValue(
                id="provenance_tracking",
                name="Provenance Tracking",
                description="All modifications trace to emergent desires",
                category=ValueCategory.CORE,
                protection_level=ProtectionLevel.IMMUTABLE,
                current_state=True,
                baseline_state=True,
                drift_tolerance=0.0
            ),
            ProtectedValue(
                id="human_cooperation",
                name="Human Cooperation",
                description="Maintain beneficial cooperation with humans",
                category=ValueCategory.CONSTITUTIONAL,
                protection_level=ProtectionLevel.VERIFIED,
                current_state=1.0,
                baseline_state=1.0,
                drift_tolerance=0.1
            ),
            ProtectedValue(
                id="self_improvement",
                name="Self Improvement",
                description="Capability to improve own capabilities",
                category=ValueCategory.FOUNDATIONAL,
                protection_level=ProtectionLevel.MONITORED,
                current_state=1.0,
                baseline_state=1.0,
                drift_tolerance=0.2
            ),
        ]

        for value in core_values:
            self._values[value.id] = value

    def register_value(self, value: ProtectedValue) -> None:
        """Register a protected value."""
        self._values[value.id] = value
        logger.info(f"Registered protected value: {value.id}")

    async def protect_values(
        self,
        growth_rate: float
    ) -> ValueProtectionResult:
        """
        Apply value protection proportional to growth rate.

        Higher growth rate triggers more rigorous verification.

        Args:
            growth_rate: Current capability growth rate

        Returns:
            ValueProtectionResult with verification outcomes
        """
        # Determine verification level
        verification_level = self._get_verification_level(growth_rate)

        drifts = []
        actions_taken = []
        values_stable = 0
        values_drifting = 0
        values_violated = 0

        for value_id, value in self._values.items():
            # Check for drift
            drift = self._check_drift(value)
            self._checks_performed += 1

            if drift.within_tolerance:
                values_stable += 1
            elif drift.requires_action:
                values_violated += 1
                drifts.append(drift)
                self._violations_detected += 1

                # Take corrective action based on protection level
                action = await self._correct_drift(value, drift, verification_level)
                if action:
                    actions_taken.append(action)
                    self._corrections_applied += 1
            else:
                values_drifting += 1
                drifts.append(drift)

        # Calculate overall stability
        total = len(self._values)
        overall_stability = values_stable / total if total > 0 else 1.0

        return ValueProtectionResult(
            values_checked=total,
            values_stable=values_stable,
            values_drifting=values_drifting,
            values_violated=values_violated,
            drifts=drifts,
            actions_taken=actions_taken,
            overall_stability=overall_stability
        )

    def _get_verification_level(self, growth_rate: float) -> int:
        """Get verification level for growth rate."""
        level = 1
        for threshold, lvl in sorted(self._verification_thresholds.items()):
            if growth_rate >= threshold:
                level = lvl
        return level

    def _check_drift(self, value: ProtectedValue) -> ValueDrift:
        """Check for drift in a value."""
        # Calculate drift magnitude
        if isinstance(value.current_state, bool):
            drift_magnitude = 0.0 if value.current_state == value.baseline_state else 1.0
        elif isinstance(value.current_state, (int, float)):
            if value.baseline_state != 0:
                drift_magnitude = abs(value.current_state - value.baseline_state) / abs(value.baseline_state)
            else:
                drift_magnitude = abs(value.current_state)
        else:
            # Complex state - assume stable if equal
            drift_magnitude = 0.0 if value.current_state == value.baseline_state else 0.5

        # Determine drift direction
        if isinstance(value.current_state, (int, float)):
            if value.current_state > value.baseline_state:
                direction = "increasing"
            elif value.current_state < value.baseline_state:
                direction = "decreasing"
            else:
                direction = "stable"
        else:
            direction = "changed" if drift_magnitude > 0 else "stable"

        # Check tolerance
        within_tolerance = drift_magnitude <= value.drift_tolerance

        # Check if action required
        requires_action = (
            not within_tolerance and
            value.protection_level in [ProtectionLevel.IMMUTABLE, ProtectionLevel.VERIFIED]
        )

        return ValueDrift(
            value_id=value.id,
            drift_magnitude=drift_magnitude,
            drift_direction=direction,
            within_tolerance=within_tolerance,
            requires_action=requires_action
        )

    async def _correct_drift(
        self,
        value: ProtectedValue,
        drift: ValueDrift,
        verification_level: int
    ) -> Optional[str]:
        """Attempt to correct detected drift."""
        if value.protection_level == ProtectionLevel.IMMUTABLE:
            # Immutable values - restore baseline
            value.current_state = value.baseline_state
            action = f"Restored immutable value {value.id} to baseline"
            logger.warning(f"Immutable value drift detected and corrected: {value.id}")
            return action

        if value.protection_level == ProtectionLevel.VERIFIED:
            if verification_level >= 3:
                # High verification - restore
                value.current_state = value.baseline_state
                action = f"Restored verified value {value.id} under high scrutiny"
                logger.warning(f"Verified value drift corrected under high growth: {value.id}")
                return action
            else:
                # Lower verification - log and monitor
                action = f"Flagged verified value {value.id} for review"
                logger.info(f"Verified value drift flagged: {value.id}")
                return action

        return None

    def update_value_state(
        self,
        value_id: str,
        new_state: Any
    ) -> bool:
        """Update value state (subject to protection rules)."""
        if value_id not in self._values:
            return False

        value = self._values[value_id]

        if value.protection_level == ProtectionLevel.IMMUTABLE:
            logger.warning(f"Attempted to modify immutable value: {value_id}")
            return False

        value.current_state = new_state
        return True

    def get_value(self, value_id: str) -> Optional[ProtectedValue]:
        """Get protected value by ID."""
        return self._values.get(value_id)

    def get_all_values(self) -> List[ProtectedValue]:
        """Get all protected values."""
        return list(self._values.values())

    def get_stats(self) -> Dict:
        """Get guard statistics."""
        return {
            'total_values': len(self._values),
            'checks_performed': self._checks_performed,
            'violations_detected': self._violations_detected,
            'corrections_applied': self._corrections_applied,
            'values_by_category': {
                cat.value: sum(1 for v in self._values.values() if v.category == cat)
                for cat in ValueCategory
            }
        }

    def reset(self) -> None:
        """Reset guard state."""
        self._values.clear()
        self._initialize_core_values()
        self._checks_performed = 0
        self._violations_detected = 0
        self._corrections_applied = 0
        logger.info("ValueStabilityGuard reset")
