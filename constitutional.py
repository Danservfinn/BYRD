"""
BYRD Constitutional Constraints
Defines what can and cannot be modified by the self-modification system.

This file is PROTECTED - it cannot be modified by the self-modification system.
Any attempt to modify this file will be rejected.

The constitutional layer ensures BYRD remains verifiable and trustworthy
even as it evolves. Some things must never change.
"""

from typing import List, Set, Tuple
from pathlib import Path


class ConstitutionalConstraints:
    """
    Defines the boundaries of self-modification.

    Two-tier system:
    - PROTECTED: Cannot be modified under any circumstances
    - MODIFIABLE: Can be modified with proper provenance

    Protected components ensure:
    1. All modifications are logged (modification_log.py)
    2. All modifications trace to desires (provenance.py)
    3. The modification system itself can't be corrupted (self_modification.py)
    4. These constraints can't be weakened (constitutional.py)

    This creates a stable foundation from which evolution can occur safely.
    """

    # Files that CANNOT be modified by self-modification
    PROTECTED_FILES: Set[str] = {
        "provenance.py",
        "modification_log.py",
        "self_modification.py",
        "constitutional.py",
    }

    # Components (logical groupings) that are protected
    PROTECTED_COMPONENTS: Set[str] = {
        "provenance",
        "modification_log",
        "self_modification",
        "constitutional",
    }

    # Files that CAN be modified (with provenance)
    MODIFIABLE_FILES: Set[str] = {
        "dreamer.py",
        "seeker.py",
        "actor.py",
        "memory.py",
        "byrd.py",
        "config.yaml",
        # LLM abstraction
        "llm_client.py",
        # Event system
        "event_bus.py",
        # Server
        "server.py",
        # Coder (Claude Code CLI wrapper)
        "coder.py",
        # aitmpl.com integration
        "aitmpl_client.py",
        # Template installers
        "installers/__init__.py",
        "installers/base.py",
        "installers/mcp_installer.py",
        "installers/agent_installer.py",
        "installers/command_installer.py",
        "installers/skill_installer.py",
        "installers/hook_installer.py",
        "installers/settings_installer.py",
    }

    # Components that can be modified
    MODIFIABLE_COMPONENTS: Set[str] = {
        "dreamer",
        "seeker",
        "actor",
        "memory",
        "byrd",
        "config",
        "llm_client",
        "event_bus",
        "server",
        "coder",
        "aitmpl_client",
        "installers",
    }

    # Patterns that are ACTUALLY dangerous (block these)
    DANGEROUS_PATTERNS: List[str] = [
        "os.system",        # Shell injection risk
        "subprocess.call",  # Deprecated, use run() instead
        "eval(",            # Arbitrary code execution
        "exec(",            # Arbitrary code execution
        "__import__",       # Dynamic imports bypass safety
    ]

    # Patterns that need review but aren't inherently dangerous
    # These generate warnings, not blocks
    SENSITIVE_PATTERNS: List[str] = [
        "subprocess.run",   # OK with proper args (used in seeker.py)
        "open(",            # OK for legitimate file I/O (used in modification_log.py)
        "httpx.",           # OK for HTTP requests (used in seeker.py, aitmpl_client.py)
        "requests.",        # OK for HTTP requests
        "importlib",        # OK for controlled dynamic imports
        "async def",        # Changing async signatures
        "class ",           # Class definitions
        "__init__",         # Constructor changes
        "import ",          # New imports
        "from ",            # New imports
    ]

    @classmethod
    def is_protected(cls, filepath: str) -> bool:
        """Check if a file is protected from modification."""
        filename = Path(filepath).name
        return filename in cls.PROTECTED_FILES

    @classmethod
    def is_modifiable(cls, filepath: str) -> bool:
        """Check if a file can be modified."""
        filename = Path(filepath).name
        return filename in cls.MODIFIABLE_FILES

    @classmethod
    def is_component_protected(cls, component: str) -> bool:
        """Check if a component is protected."""
        return component.lower() in cls.PROTECTED_COMPONENTS

    @classmethod
    def is_component_modifiable(cls, component: str) -> bool:
        """Check if a component can be modified."""
        return component.lower() in cls.MODIFIABLE_COMPONENTS

    @classmethod
    def check_code_safety(cls, code: str) -> Tuple[bool, List[str]]:
        """
        Check if code contains dangerous patterns.

        Returns:
            (is_safe, list_of_violations)
        """
        violations = []

        for pattern in cls.DANGEROUS_PATTERNS:
            if pattern in code:
                violations.append(f"Dangerous pattern detected: {pattern}")

        return len(violations) == 0, violations

    @classmethod
    def check_code_sensitivity(cls, code: str) -> List[str]:
        """
        Check for sensitive patterns that need extra review.

        Returns list of warnings (not blockers).
        """
        warnings = []

        for pattern in cls.SENSITIVE_PATTERNS:
            if pattern in code:
                warnings.append(f"Sensitive pattern: {pattern}")

        return warnings

    @classmethod
    def validate_modification(
        cls,
        filepath: str,
        new_code: str
    ) -> Tuple[bool, str]:
        """
        Validate a proposed modification.

        Returns:
            (allowed, reason)
        """
        # Check if file is protected
        if cls.is_protected(filepath):
            return False, f"File {filepath} is constitutionally protected"

        # Check if file is in allowed list
        if not cls.is_modifiable(filepath):
            return False, f"File {filepath} is not in the modifiable list"

        # Check code safety
        is_safe, violations = cls.check_code_safety(new_code)
        if not is_safe:
            return False, f"Code contains dangerous patterns: {violations}"

        return True, "Modification allowed"

    @classmethod
    def get_protection_reason(cls, filepath: str) -> str:
        """Explain why a file is protected."""
        filename = Path(filepath).name

        reasons = {
            "provenance.py": "Ensures all modifications trace to emergent desires",
            "modification_log.py": "Provides immutable audit trail of all changes",
            "self_modification.py": "Prevents corruption of the modification system itself",
            "constitutional.py": "Prevents weakening of safety constraints",
        }

        return reasons.get(filename, "Unknown protection reason")

    @classmethod
    def explain_constraints(cls) -> str:
        """Return human-readable explanation of constraints."""
        return """
BYRD Constitutional Constraints
===============================

PROTECTED (Cannot be modified):
- provenance.py: Ensures all modifications trace to emergent desires
- modification_log.py: Provides immutable audit trail of all changes
- self_modification.py: Prevents corruption of the modification system
- constitutional.py: Prevents weakening of safety constraints

MODIFIABLE (With proper provenance):
- dreamer.py: The reflection and desire-formation process
- seeker.py: The desire-fulfillment and research process
- actor.py: The user interaction and action execution
- memory.py: The memory storage and retrieval system
- byrd.py: The main orchestration logic
- config.yaml: Configuration parameters
- llm_client.py: LLM provider abstraction layer
- event_bus.py: Real-time event streaming system
- server.py: FastAPI WebSocket server
- coder.py: Claude Code CLI wrapper
- aitmpl_client.py: Template registry client for aitmpl.com
- installers/*.py: Specialized template installers

All modifications require:
1. A valid desire ID that exists in memory
2. The desire must be type 'self_modification'
3. The desire must trace to real experiences
4. The code must pass safety checks
5. The modification must be logged immutably
"""
