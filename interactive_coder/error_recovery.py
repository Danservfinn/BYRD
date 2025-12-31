"""
error_recovery.py - Automatic Error Recovery

Classifies errors and generates recovery strategies for:
- Timeout errors
- Rate limit errors
- Syntax errors
- Import errors
- File not found errors
- Constitutional violations
- CLI unavailability
"""

import logging
import re
from dataclasses import dataclass
from typing import Dict, Optional, Any, List

logger = logging.getLogger(__name__)


class ErrorType:
    """Error type constants."""
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    SYNTAX_ERROR = "syntax_error"
    IMPORT_ERROR = "import_error"
    FILE_NOT_FOUND = "file_not_found"
    CONSTITUTIONAL = "constitutional"
    CLI_UNAVAILABLE = "cli_unavailable"
    PERMISSION_DENIED = "permission_denied"
    NETWORK_ERROR = "network_error"
    UNKNOWN = "unknown"


# Error classification patterns
ERROR_PATTERNS = {
    ErrorType.TIMEOUT: [
        r"timed? ?out",
        r"timeout",
        r"execution.*exceeded",
    ],
    ErrorType.RATE_LIMIT: [
        r"429",
        r"rate ?limit",
        r"too many requests",
        r"quota exceeded",
    ],
    ErrorType.SYNTAX_ERROR: [
        r"syntaxerror",
        r"syntax error",
        r"invalid syntax",
        r"unexpected token",
    ],
    ErrorType.IMPORT_ERROR: [
        r"importerror",
        r"modulenotfounderror",
        r"no module named",
        r"cannot import",
    ],
    ErrorType.FILE_NOT_FOUND: [
        r"filenotfounderror",
        r"no such file",
        r"file not found",
        r"path.*not exist",
    ],
    ErrorType.CONSTITUTIONAL: [
        r"constitutional.*violation",
        r"protected file",
        r"cannot modify",
        r"dangerous pattern",
    ],
    ErrorType.CLI_UNAVAILABLE: [
        r"no coding cli",
        r"cli.*not found",
        r"command not found",
    ],
    ErrorType.PERMISSION_DENIED: [
        r"permission denied",
        r"access denied",
        r"not permitted",
    ],
    ErrorType.NETWORK_ERROR: [
        r"connection.*refused",
        r"network.*unreachable",
        r"connection.*error",
        r"socket.*error",
    ],
}


@dataclass
class RecoveryResult:
    """Result of a recovery attempt."""
    recovered: bool
    strategy_used: str
    new_prompt: Optional[str]
    wait_seconds: float = 0
    should_retry: bool = True
    error_type: str = ErrorType.UNKNOWN
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "recovered": self.recovered,
            "strategy_used": self.strategy_used,
            "new_prompt": self.new_prompt[:200] if self.new_prompt else None,
            "wait_seconds": self.wait_seconds,
            "should_retry": self.should_retry,
            "error_type": self.error_type,
            "message": self.message,
        }


class ErrorRecovery:
    """
    Automatic error recovery for coding sessions.

    Classifies errors and generates recovery strategies with retry logic.
    """

    MAX_RECOVERY_ATTEMPTS = 3

    # Recovery strategies by error type
    RECOVERY_STRATEGIES = {
        ErrorType.TIMEOUT: {
            "strategy": "simplify_task",
            "wait": 0,
            "message": "Task took too long. Will try a simpler approach.",
        },
        ErrorType.RATE_LIMIT: {
            "strategy": "wait_and_retry",
            "wait": 60,
            "message": "Rate limited. Waiting before retry.",
        },
        ErrorType.SYNTAX_ERROR: {
            "strategy": "fix_syntax",
            "wait": 0,
            "message": "Syntax error detected. Will fix and retry.",
        },
        ErrorType.IMPORT_ERROR: {
            "strategy": "install_dependency",
            "wait": 0,
            "message": "Missing dependency. Will install and retry.",
        },
        ErrorType.FILE_NOT_FOUND: {
            "strategy": "verify_path",
            "wait": 0,
            "message": "File not found. Will verify path first.",
        },
        ErrorType.CONSTITUTIONAL: {
            "strategy": "explain_constraint",
            "wait": 0,
            "message": "Constitutional constraint violation. Cannot proceed.",
        },
        ErrorType.CLI_UNAVAILABLE: {
            "strategy": "fallback_subprocess",
            "wait": 0,
            "message": "CLI unavailable. Using subprocess fallback.",
        },
        ErrorType.PERMISSION_DENIED: {
            "strategy": "check_permissions",
            "wait": 0,
            "message": "Permission denied. Will check file permissions.",
        },
        ErrorType.NETWORK_ERROR: {
            "strategy": "retry_network",
            "wait": 5,
            "message": "Network error. Will retry after brief wait.",
        },
        ErrorType.UNKNOWN: {
            "strategy": "retry_generic",
            "wait": 0,
            "message": "Unknown error. Will attempt generic retry.",
        },
    }

    def __init__(self):
        """Initialize the error recovery system."""
        self._recovery_attempts: Dict[str, int] = {}
        self._recovery_history: List[Dict] = []

    def analyze_error(self, error: str, output: str = "") -> str:
        """
        Classify the error type.

        Args:
            error: Error message
            output: Full output (may contain additional error info)

        Returns:
            ErrorType constant
        """
        combined = f"{error} {output}".lower()

        for error_type, patterns in ERROR_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, combined, re.IGNORECASE):
                    return error_type

        return ErrorType.UNKNOWN

    def can_recover(self, error_type: str) -> bool:
        """
        Check if we should attempt recovery.

        Args:
            error_type: Type of error

        Returns:
            True if recovery should be attempted
        """
        # Constitutional violations cannot be recovered
        if error_type == ErrorType.CONSTITUTIONAL:
            return False

        # Check attempt count
        attempts = self._recovery_attempts.get(error_type, 0)
        return attempts < self.MAX_RECOVERY_ATTEMPTS

    async def recover(
        self,
        error_type: str,
        original_prompt: str,
        error: str,
        output: str = "",
    ) -> RecoveryResult:
        """
        Generate recovery strategy.

        Args:
            error_type: Type of error
            original_prompt: The original prompt that failed
            error: Error message
            output: Full output

        Returns:
            RecoveryResult with strategy and new prompt
        """
        # Track attempts
        self._recovery_attempts[error_type] = self._recovery_attempts.get(error_type, 0) + 1

        # Get strategy config
        strategy_config = self.RECOVERY_STRATEGIES.get(
            error_type,
            self.RECOVERY_STRATEGIES[ErrorType.UNKNOWN]
        )

        strategy = strategy_config["strategy"]
        wait = strategy_config["wait"]
        message = strategy_config["message"]

        # Generate recovery prompt based on strategy
        new_prompt = self._generate_recovery_prompt(
            strategy, original_prompt, error, output
        )

        # Check if we should retry
        should_retry = error_type != ErrorType.CONSTITUTIONAL

        result = RecoveryResult(
            recovered=should_retry,
            strategy_used=strategy,
            new_prompt=new_prompt,
            wait_seconds=wait,
            should_retry=should_retry,
            error_type=error_type,
            message=message,
        )

        # Log recovery attempt
        self._recovery_history.append(result.to_dict())
        logger.info(f"Recovery attempt: {strategy} for {error_type}")

        return result

    def _generate_recovery_prompt(
        self,
        strategy: str,
        original_prompt: str,
        error: str,
        output: str,
    ) -> str:
        """Generate a recovery prompt based on strategy."""

        if strategy == "simplify_task":
            return f"""The previous attempt timed out. Please try a simpler approach.

ORIGINAL TASK: {original_prompt[:500]}

Instructions:
1. Break the task into smaller steps
2. Complete the most essential part first
3. Avoid complex operations that might take too long"""

        elif strategy == "wait_and_retry":
            return original_prompt  # Just retry after waiting

        elif strategy == "fix_syntax":
            return f"""The previous attempt had a syntax error. Please fix it.

ORIGINAL TASK: {original_prompt[:500]}

ERROR: {error}

Instructions:
1. Review the error message carefully
2. Fix the syntax issue
3. Verify the fix before continuing"""

        elif strategy == "install_dependency":
            # Extract module name from error
            match = re.search(r"no module named ['\"]?(\w+)", error.lower())
            module = match.group(1) if match else "the missing module"

            return f"""A required dependency is missing. Please install it first.

ORIGINAL TASK: {original_prompt[:500]}

MISSING MODULE: {module}
ERROR: {error}

Instructions:
1. First install the missing dependency: pip install {module}
2. Then proceed with the original task"""

        elif strategy == "verify_path":
            return f"""A file was not found. Please verify the path first.

ORIGINAL TASK: {original_prompt[:500]}

ERROR: {error}

Instructions:
1. List files in the relevant directory to verify paths
2. Use the correct file path
3. Then proceed with the original task"""

        elif strategy == "explain_constraint":
            return f"""This task violates constitutional constraints and cannot be completed.

ORIGINAL TASK: {original_prompt[:500]}

CONSTRAINT VIOLATED: {error}

This task cannot proceed as it attempts to modify protected files."""

        elif strategy == "fallback_subprocess":
            return f"""The CLI is unavailable. Please use a simpler approach.

ORIGINAL TASK: {original_prompt[:500]}

Instructions:
1. Use basic shell commands if possible
2. Avoid CLI-specific features
3. Complete what can be done with subprocess"""

        elif strategy == "check_permissions":
            return f"""Permission was denied. Please check file permissions.

ORIGINAL TASK: {original_prompt[:500]}

ERROR: {error}

Instructions:
1. Check file/directory permissions
2. Use appropriate permissions or different location
3. Then proceed with the original task"""

        elif strategy == "retry_network":
            return original_prompt  # Retry after network recovers

        else:  # retry_generic
            return f"""The previous attempt failed. Please try again with more care.

ORIGINAL TASK: {original_prompt[:500]}

ERROR: {error}

Instructions:
1. Review what went wrong
2. Take a more careful approach
3. Complete the task"""

    def get_recovery_history(self) -> List[Dict]:
        """Get history of recovery attempts."""
        return self._recovery_history.copy()

    def get_attempt_count(self, error_type: str) -> int:
        """Get number of recovery attempts for an error type."""
        return self._recovery_attempts.get(error_type, 0)

    def reset(self):
        """Reset recovery state for new session."""
        self._recovery_attempts = {}
        self._recovery_history = []

    def get_stats(self) -> Dict[str, Any]:
        """Get recovery statistics."""
        return {
            "total_attempts": sum(self._recovery_attempts.values()),
            "attempts_by_type": self._recovery_attempts.copy(),
            "history_count": len(self._recovery_history),
        }
