#!/usr/bin/env python
"""Quick test to verify Memory demonstration filter works."""
import sys
sys.path.insert(0, '.')

from memory import Memory

def test_filter():
    """Test the demonstration desire filter in Memory class."""
    # Create a minimal Memory instance (we don't need to connect to Neo4j)
    memory = Memory({})
    
    test_cases = [
        ("This is a demonstration desire", True),
        ("demo desire for testing", True),
        ("test_desire example", True),
        ("example desire usage", True),
        ("mock memory desire", True),
        ("I want to improve my memory", False),
        ("test if this works", False),
        ("demo a product feature", False),
        ("prove that I can learn", False),  # Should NOT trigger (missing context)
        ("prove that the system can work", True),  # Should trigger
        ("", False),  # Empty string
        ("hi", False),  # Too short
    ]
    
    passed = 0
    failed = 0
    
    for description, expected in test_cases:
        result = memory._is_demonstration_desire(description)
        status = "✓" if result == expected else "✗"
        if result == expected:
            passed += 1
        else:
            failed += 1
        print(f"{status} '{description}' -> {result} (expected {expected})")
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = test_filter()
    sys.exit(0 if success else 1)
