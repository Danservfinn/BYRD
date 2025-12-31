#!/usr/bin/env python3
"""
BYRD Demonstration Filter

Filters out demonstration, test, and malformed desires before they waste cycles.

Version: 1.0
Created: January 2025
"""

import re
from typing import Optional, Tuple


class DemonstrationFilter:
    """
    Filters out demonstration, test, and malformed desires.
    """

    # Patterns from test_filter_simple.py
    DEMONSTRATION_PATTERNS = [
        'demonstration',
        'test_desire',
        'test desire',
        'example usage',
        'mock memory',
        'for demonstration',
        'mock llm',
        'mock response',
        'simulated for',
        'test case',
        'unit test',
        'integration test',
        'prove that',
        'show that',
        'demonstrate that',
        'example_desire',
        'sample desire',
        'fake desire',
        'placeholder desire',
        'mock desire',
        'stub desire',
        'dummy desire',
        'test_input',
        'sample_input',
        'example input',
        'for testing',
        'for demo',
    ]

    def __init__(self):
        self._filtered_count = 0

    def is_demonstration_desire(self, description: str) -> bool:
        """Check if a desire is a demonstration/test desire."""
        if not description:
            return True
        if description is None:
            return True
        if len(str(description).strip()) < 5:
            return True
        
        desc_lower = description.lower()
        
        for pattern in self.DEMONSTRATION_PATTERNS:
            if pattern in desc_lower:
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
        return self._filtered_count


# Singleton instance
_demonstration_filter = DemonstrationFilter()


def is_demonstration_desire(description: str) -> bool:
    return _demonstration_filter.is_demonstration_desire(description)


def filter_desire(desire: dict) -> Tuple[bool, Optional[str]]:
    return _demonstration_filter.filter_desire(desire)
