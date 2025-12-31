"""
Test target file for self-modification demonstration.
This is a safe file for BYRD to modify.
"""

def existing_function():
    """An existing test function."""
    return "original"

class TestClass:
    """A test class."""
    version = 1

# [SELF-MODIFIED] This file was modified by BYRD
