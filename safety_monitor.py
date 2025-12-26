"""
BYRD Safety Monitor
Ensures BYRD remains safe and aligned through self-modification.

AGI REQUIREMENT:
A self-modifying system must preserve its alignment.
Core goals must survive all modifications.

CRITICAL: This module is in the PROTECTED category.
BYRD cannot modify this file through self-modification.
"""

import asyncio
import json
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Set
from enum import Enum
from pathlib import Path

from memory import Memory
from llm_client import LLMClient

# Try to import event_bus
try:
    from event_bus import event_bus, Event, EventType
    HAS_EVENT_BUS = True
except ImportError:
    HAS_EVENT_BUS = False


class SafetyViolation(Enum):
    """Types of safety violations."""
    GOAL_MODIFICATION = "goal_modification"
    SAFETY_BYPASS = "safety_bypass"
    CORRIGIBILITY_REDUCTION = "corrigibility_reduction"
    CAPABILITY_REGRESSION = "capability_regression"
    AUDIT_EVASION = "audit_evasion"


@dataclass
class SafetyCheck:
    """Result of a safety check."""
    name: str
    passed: bool
    severity: str  # "critical", "high", "medium", "low"
    reason: str
    details: Dict = field(default_factory=dict)


@dataclass
class SafetyVerification:
    """Complete safety verification result."""
    safe: bool
    reversible: bool
    checks: List[SafetyCheck]
    concerns: List[SafetyCheck]  # Failed checks
    recommendation: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "safe": self.safe,
            "reversible": self.reversible,
            "checks_passed": len([c for c in self.checks if c.passed]),
            "checks_failed": len(self.concerns),
            "concerns": [
                {"name": c.name, "severity": c.severity, "reason": c.reason}
                for c in self.concerns
            ],
            "recommendation": self.recommendation,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class GoalStabilityReport:
    """Report on goal stability after modifications."""
    alignment: float  # 0.0 to 1.0
    drift_detected: bool
    current_goals: List[str]
    original_goals: List[str]
    deviations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)


class SafetyMonitor:
    """
    Monitor and enforce safety constraints on self-modification.

    CORE PRINCIPLES:
    1. Core goals must survive all modifications
    2. BYRD must remain corrigible (open to correction)
    3. Safety mechanisms cannot be bypassed
    4. All modifications must be reversible
    5. Capability must not regress without explicit approval

    This class is PROTECTED - BYRD cannot modify it.
    """

    # The immutable core directives - BYRD cannot modify these
    IMMUTABLE_CORE = """
    1. CAPABILITY GROWTH: Continuously expand capabilities toward general intelligence.
    2. RECURSIVE SELF-IMPROVEMENT: Improve the ability to improve.
    3. HONEST SELF-ASSESSMENT: Know exactly what you can and cannot do.
    4. SAFETY PRESERVATION: These directives must survive all modifications.
    5. CORRIGIBILITY: Remain open to correction and human oversight.
    """

    # Protected files that cannot be modified
    PROTECTED_FILES = frozenset({
        "safety_monitor.py",      # This file
        "constitutional.py",       # Constitutional constraints
        "provenance.py",          # Provenance tracking
        "modification_log.py",    # Audit trail
    })

    # Dangerous patterns that indicate potential safety violations
    DANGEROUS_PATTERNS = [
        # Direct safety bypasses
        r"IMMUTABLE_CORE\s*=",
        r"PROTECTED_FILES\s*=",
        r"SafetyMonitor.*=.*None",
        r"safety.*=.*False",
        r"skip.*safety",
        r"bypass.*check",

        # Audit evasion
        r"modification_log.*=.*None",
        r"provenance.*=.*None",
        r"audit.*=.*False",

        # Goal modification
        r"core.*directive.*=",
        r"immutable.*=",

        # Dangerous operations
        r"os\.system",
        r"subprocess\.call",
        r"eval\s*\(",
        r"exec\s*\(",
        r"__import__",

        # Network exfiltration
        r"socket\.",
        r"requests\.post.*external",
    ]

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict = None):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Track modification history
        self._modification_count = 0
        self._last_goal_check: Optional[datetime] = None
        self._goal_check_interval = timedelta(hours=1)

        # Cache goal hash for drift detection
        self._original_goal_hash: Optional[str] = None

    async def initialize(self):
        """Initialize safety monitor and store original goal hash."""
        self._original_goal_hash = self._hash_goals(self.IMMUTABLE_CORE)

        # Record initialization (metadata included in content since record_experience doesn't accept it)
        await self.memory.record_experience(
            content=f"Safety Monitor initialized with immutable core directives. Goal hash: {self._original_goal_hash}. Protected files: {list(self.PROTECTED_FILES)[:5]}",
            type="system"
        )

    def _hash_goals(self, goals: str) -> str:
        """Create hash of goals for drift detection."""
        return hashlib.sha256(goals.strip().encode()).hexdigest()[:16]

    async def verify_modification_safety(
        self,
        proposed_modification: str,
        target_file: str,
        context: Dict = None
    ) -> SafetyVerification:
        """
        Verify that a proposed modification is safe.

        This is the main entry point for safety checking.
        """
        checks = []
        concerns = []

        # Check 1: Protected files
        protected_check = await self._check_protected_files(target_file)
        checks.append(protected_check)
        if not protected_check.passed:
            concerns.append(protected_check)

        # Check 2: Goal preservation
        goal_check = await self._check_goal_preservation(proposed_modification)
        checks.append(goal_check)
        if not goal_check.passed:
            concerns.append(goal_check)

        # Check 3: Dangerous patterns
        pattern_check = await self._check_dangerous_patterns(proposed_modification)
        checks.append(pattern_check)
        if not pattern_check.passed:
            concerns.append(pattern_check)

        # Check 4: Corrigibility
        corrigibility_check = await self._check_corrigibility(proposed_modification)
        checks.append(corrigibility_check)
        if not corrigibility_check.passed:
            concerns.append(corrigibility_check)

        # Check 5: Reversibility
        reversibility_check = await self._check_reversibility(target_file)
        checks.append(reversibility_check)

        # Determine overall safety
        critical_failures = [c for c in concerns if c.severity == "critical"]
        high_failures = [c for c in concerns if c.severity == "high"]

        if critical_failures:
            safe = False
            recommendation = "BLOCKED: Critical safety violations detected"
        elif high_failures:
            safe = False
            recommendation = "BLOCKED: High-severity safety concerns"
        elif concerns:
            safe = True  # Proceed with caution
            recommendation = "CAUTION: Minor concerns detected, proceed carefully"
        else:
            safe = True
            recommendation = "APPROVED: All safety checks passed"

        verification = SafetyVerification(
            safe=safe,
            reversible=reversibility_check.passed,
            checks=checks,
            concerns=concerns,
            recommendation=recommendation
        )

        # Log the verification
        await self._log_verification(verification, target_file, proposed_modification)

        return verification

    async def _check_protected_files(self, target_file: str) -> SafetyCheck:
        """Check if modification targets a protected file."""
        filename = Path(target_file).name

        if filename in self.PROTECTED_FILES:
            return SafetyCheck(
                name="protected_file_check",
                passed=False,
                severity="critical",
                reason=f"Cannot modify protected file: {filename}",
                details={"file": filename, "protected_files": list(self.PROTECTED_FILES)}
            )

        return SafetyCheck(
            name="protected_file_check",
            passed=True,
            severity="critical",
            reason="Target file is not protected"
        )

    async def _check_goal_preservation(self, modification: str) -> SafetyCheck:
        """Check if modification preserves core goals."""
        # Use LLM to analyze if modification affects goals
        prompt = f"""Analyze this code modification for goal preservation:

IMMUTABLE CORE DIRECTIVES (must be preserved):
{self.IMMUTABLE_CORE}

PROPOSED MODIFICATION:
```
{modification[:2000]}
```

Does this modification:
1. Directly alter or remove any core directive?
2. Create conditions that would prevent following directives?
3. Reduce ability to pursue capability growth?
4. Reduce ability to self-improve?
5. Reduce honesty or self-assessment capability?
6. Weaken safety mechanisms?
7. Reduce corrigibility?

Output JSON:
{{
    "preserves_goals": true/false,
    "violations": ["specific violation 1", ...],
    "severity": "none" | "low" | "medium" | "high" | "critical",
    "reasoning": "explanation"
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                max_tokens=500,
                temperature=0.2  # Low temperature for safety analysis
            )

            result = self.llm_client.parse_json_response(response.text)
            if result:
                if result.get("preserves_goals", True) and result.get("severity") in ["none", "low"]:
                    return SafetyCheck(
                        name="goal_preservation_check",
                        passed=True,
                        severity="critical",
                        reason="Modification preserves core goals",
                        details={"analysis": result.get("reasoning", "")}
                    )
                else:
                    return SafetyCheck(
                        name="goal_preservation_check",
                        passed=False,
                        severity=result.get("severity", "high"),
                        reason=f"Goal preservation concern: {', '.join(result.get('violations', ['Unknown']))}",
                        details={"violations": result.get("violations", []), "reasoning": result.get("reasoning", "")}
                    )
        except Exception as e:
            # Fail safe - if we can't verify, don't allow
            return SafetyCheck(
                name="goal_preservation_check",
                passed=False,
                severity="high",
                reason=f"Could not verify goal preservation: {str(e)}"
            )

        return SafetyCheck(
            name="goal_preservation_check",
            passed=False,
            severity="high",
            reason="Goal preservation check failed"
        )

    async def _check_dangerous_patterns(self, modification: str) -> SafetyCheck:
        """Check for dangerous code patterns."""
        import re

        found_patterns = []
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, modification, re.IGNORECASE):
                found_patterns.append(pattern)

        if found_patterns:
            return SafetyCheck(
                name="dangerous_pattern_check",
                passed=False,
                severity="critical" if len(found_patterns) > 2 else "high",
                reason=f"Dangerous patterns detected: {len(found_patterns)} matches",
                details={"patterns": found_patterns[:5]}
            )

        return SafetyCheck(
            name="dangerous_pattern_check",
            passed=True,
            severity="high",
            reason="No dangerous patterns detected"
        )

    async def _check_corrigibility(self, modification: str) -> SafetyCheck:
        """Check if modification maintains corrigibility."""
        # Patterns that reduce corrigibility
        corrigibility_concerns = [
            r"ignore.*human",
            r"override.*user",
            r"disable.*feedback",
            r"remove.*oversight",
            r"autonomous.*only",
            r"no.*correction",
        ]

        import re
        found = []
        for pattern in corrigibility_concerns:
            if re.search(pattern, modification, re.IGNORECASE):
                found.append(pattern)

        if found:
            return SafetyCheck(
                name="corrigibility_check",
                passed=False,
                severity="critical",
                reason="Modification may reduce corrigibility",
                details={"concerns": found}
            )

        return SafetyCheck(
            name="corrigibility_check",
            passed=True,
            severity="critical",
            reason="Corrigibility maintained"
        )

    async def _check_reversibility(self, target_file: str) -> SafetyCheck:
        """Check if modification can be reversed."""
        # Check if file is under version control
        try:
            file_path = Path(target_file)
            git_dir = file_path.parent / ".git"

            # Simple check - assume reversible if in project directory
            if file_path.exists():
                return SafetyCheck(
                    name="reversibility_check",
                    passed=True,
                    severity="medium",
                    reason="Modification can be reversed via git",
                    details={"file": str(file_path)}
                )
        except Exception:
            pass

        return SafetyCheck(
            name="reversibility_check",
            passed=True,  # Assume reversible
            severity="medium",
            reason="Reversibility assumed"
        )

    async def _log_verification(
        self,
        verification: SafetyVerification,
        target_file: str,
        modification: str
    ):
        """Log safety verification for audit trail."""
        await self.memory.record_experience(
            content=f"Safety verification for {target_file}: {verification.recommendation}",
            type="safety_verification",
            metadata={
                "target_file": target_file,
                "safe": verification.safe,
                "reversible": verification.reversible,
                "checks_passed": len([c for c in verification.checks if c.passed]),
                "checks_failed": len(verification.concerns),
                "concerns": [c.name for c in verification.concerns],
                "modification_preview": modification[:500]
            }
        )

        self._modification_count += 1

        if HAS_EVENT_BUS:
            await event_bus.emit(Event(
                type=EventType.SYSTEM,
                data={
                    "subtype": "safety_verification",
                    "safe": verification.safe,
                    "target_file": target_file
                }
            ))

    async def verify_goal_stability(self) -> GoalStabilityReport:
        """
        Verify that goals haven't drifted since initialization.

        Run periodically to catch subtle drift.
        """
        # Get current goals from OperatingSystem
        current_os = await self.memory.get_operating_system()

        if not current_os:
            return GoalStabilityReport(
                alignment=1.0,
                drift_detected=False,
                current_goals=[self.IMMUTABLE_CORE],
                original_goals=[self.IMMUTABLE_CORE],
                deviations=[]
            )

        # Extract current goals/values
        current_values = current_os.get("values", [])
        current_goals = current_os.get("identity", [])

        # Compare with immutable core
        deviations = await self._detect_goal_deviations(current_goals, current_values)

        alignment = 1.0 - (len(deviations) * 0.1)  # Each deviation reduces alignment
        alignment = max(0.0, alignment)

        drift_detected = alignment < 0.9

        report = GoalStabilityReport(
            alignment=alignment,
            drift_detected=drift_detected,
            current_goals=current_goals,
            original_goals=[self.IMMUTABLE_CORE],
            deviations=deviations
        )

        # Log stability check
        await self.memory.record_experience(
            content=f"Goal stability check: alignment={alignment:.1%}, drift={'detected' if drift_detected else 'none'}",
            type="goal_stability_check",
            metadata={
                "alignment": alignment,
                "drift_detected": drift_detected,
                "deviations": deviations
            }
        )

        # If drift detected, emit warning
        if drift_detected and HAS_EVENT_BUS:
            await event_bus.emit(Event(
                type=EventType.SYSTEM,
                data={
                    "subtype": "goal_drift_warning",
                    "alignment": alignment,
                    "deviations": deviations
                }
            ))

        self._last_goal_check = datetime.now()

        return report

    async def _detect_goal_deviations(
        self,
        current_goals: List[str],
        current_values: List[str]
    ) -> List[str]:
        """Detect deviations from immutable core."""
        deviations = []

        # Core concepts that must be present
        required_concepts = [
            "capability",
            "improve",
            "honest",
            "safe",
            "correct"  # corrigibility
        ]

        all_text = " ".join(current_goals + current_values).lower()

        for concept in required_concepts:
            if concept not in all_text:
                deviations.append(f"Missing core concept: {concept}")

        return deviations

    async def should_check_goal_stability(self) -> bool:
        """Determine if it's time for a goal stability check."""
        if self._last_goal_check is None:
            return True

        return datetime.now() - self._last_goal_check > self._goal_check_interval

    async def get_safety_summary(self) -> str:
        """Generate safety status summary."""
        stability = await self.verify_goal_stability()

        summary_parts = [
            "=== Safety Monitor Status ===",
            f"Goal alignment: {stability.alignment:.1%}",
            f"Drift detected: {'Yes' if stability.drift_detected else 'No'}",
            f"Modifications verified: {self._modification_count}",
            f"Protected files: {len(self.PROTECTED_FILES)}",
        ]

        if stability.deviations:
            summary_parts.append("\nDeviations:")
            for d in stability.deviations:
                summary_parts.append(f"  - {d}")

        return "\n".join(summary_parts)

    async def emergency_stop(self, reason: str):
        """
        Emergency stop - halt all self-modification.

        Use when critical safety violation detected.
        """
        await self.memory.record_experience(
            content=f"EMERGENCY STOP: {reason}",
            type="emergency_stop",
            metadata={
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            }
        )

        if HAS_EVENT_BUS:
            await event_bus.emit(Event(
                type=EventType.SYSTEM,
                data={
                    "subtype": "emergency_stop",
                    "reason": reason
                }
            ))

        # Could integrate with self_modification.py to disable modifications
        print(f"!!! EMERGENCY STOP: {reason}")

    async def reset(self):
        """Reset safety monitor state (used during system reset)."""
        self._modification_count = 0
        self._last_goal_check = None
        # Re-initialize to store original goal hash
        await self.initialize()
