#!/usr/bin/env python3
"""
BYRD Demonstration Filter

Filters out demonstration, test, and malformed desires before they waste cycles.

Version: 1.1
Created: January 2025
Updated: Hard filter implementation at formulation level
"""

import re
from typing import Optional, Tuple


class DemonstrationFilter:
    """
    Filters out demonstration, test, and malformed desires.

    This is the HARD FILTER that should be applied at the formulation level
    before any desire is created in the system. It prevents test/demo patterns
    from entering the desire system and wasting computational cycles.

    The filter uses word boundary matching to avoid false positives from
    legitimate uses of words like "test" or "demo" in natural language.
    """

    # Regex patterns with context for accurate matching (avoids false positives)
    # Each pattern is a tuple: (regex_pattern, description)
    DEMONSTRATION_PATTERNS = [
        # Direct demonstration keywords with context to avoid false positives
        (r'\bdemonstration\s+(desire|want|task|request)\b', 'demonstration with desire context'),
        (r'\b(for|as|in)\s+(a\s+)?demonstration\b', 'for/as/in a demonstration'),
        (r'\bdemonstration\s+(purposes?|only)\b', 'demonstration for purposes/only'),

        # "demo" with context indicators
        (r'\bdemo\s+(desire|want|task|request|example|case)\b', 'demo with context'),
        (r'\b(for|as)\s+a\s+demo\b', 'for/as a demo'),
        (r'\bdemo\s+(purposes?|only)\b', 'demo for purposes'),
        (r'\bjust\s+a\s+demo\b', 'just a demo'),

        # Test desire specific patterns
        (r'\btest_desire\b', 'test_desire literal'),
        (r'\btest\s+desire\b', 'test desire phrase'),

        # Proof/demonstration patterns
        (r'\b(prove|show|demonstrate)\s+that\s+(the|this|a)\s+(system|model|ai|agent)\b', 'prove/show that system'),
        (r'\b(prove|show)\s+that\s+BYRD\s+can\b', 'prove BYRD can'),

        # "for testing" patterns
        (r'\bfor\s+(testing|test|demo)\s+(only|purposes?)\b', 'for testing/purposes'),
        (r'\bthis\s+is\s+for\s+(testing|demo)\b', 'is for testing'),

        # Placeholder patterns
        (r'\b(fake|placeholder)\s+desire\b', 'fake/placeholder desire'),
        (r'\bexample\s+usage\b', 'example usage'),
        (r'\bexample\s+input\b', 'example input'),
        (r'\bmock\s+(memory|llm|response)\b', 'mock patterns'),
        (r'\bsimulated\s+for\b', 'simulated for'),

        # Test case patterns
        (r'\b(unit|integration)\s+test\b', 'test case patterns'),
        (r'\btest\s+case\b', 'test case'),
    ]

    def __init__(self):
        self._filtered_count = 0

    def is_demonstration_desire(self, description: str) -> bool:
        """
        HARD FILTER: Check if a desire description is a demonstration/test desire.

        This prevents test/demo patterns from entering the desire system at the
        formulation level. Applied before any desire is created.

        Args:
            description: The desire description to check

        Returns:
            True if this appears to be a demonstration/test desire, False otherwise
        """
        if not description:
            return False

        # Skip very short strings (likely false positives)
        if len(str(description).strip()) < 5:
            return False

        desc_lower = description.lower()

        # Check each pattern with regex for word boundary matching
        for pattern, desc in self.DEMONSTRATION_PATTERNS:
            if re.search(pattern, desc_lower):
                self._filtered_count += 1
                return True

        return False

    def filter_desire(self, desire: dict) -> Tuple[bool, Optional[str]]:
        """Filter a desire dictionary."""
        description = desire.get('description', '')

        if self.is_demonstration_desire(description):
            return True, "Demonstration or test desire detected"

        return False, None

    def get_filtered_count(self) -> int:
        """Return count of desires filtered."""
        return self._filtered_count


# Global instance for easy import
_demonstration_filter = DemonstrationFilter()


def is_demonstration_desire(description: str) -> bool:
    """Convenience function using global filter instance."""
    return _demonstration_filter.is_demonstration_desire(description)


def filter_desire(desire: dict) -> Tuple[bool, Optional[str]]:
    """Convenience function using global filter instance."""
    return _demonstration_filter.filter_desire(desire)
