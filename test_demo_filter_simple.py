#!/usr/bin/env python3
"""
Simple standalone test for the demonstration filter.
Runs without pytest dependencies.
"""

def is_demonstration_desire(description: str) -> bool:
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
        
    desc_lower = description.lower()
    
    # Comprehensive list of demonstration/test keywords
    demo_keywords = [
        "demonstration", "demo", "test_desire", "test desire",
        "example usage", "mock memory", "for demonstration",
        "mock llm", "mock response", "simulated for",
        "test case", "unit test", "integration test",
        "prove that", "show that", "demonstrate that",
        "example_desire", "sample desire", "fake desire",
        "placeholder desire", "mock desire", "stub desire",
        "dummy desire", "test_input", "sample_input",
        "example input", "for testing", "for demo"
    ]
    
    return any(kw in desc_lower for kw in demo_keywords)


def test_filter():
    """Run comprehensive tests on the demonstration filter."""
    passed = 0
    failed = 0
    
    test_cases = [
        # Should reject (True)
        ("This is a demonstration desire", True, "demonstration keyword"),
        ("demo desire for testing", True, "demo keyword"),
        ("test_desire example", True, "test_desire"),
        ("This is a test desire", True, "test desire"),
        ("example usage of the system", True, "example usage"),
        ("Use mock memory for this", True, "mock memory"),
        ("This is for demonstration purposes", True, "for demonstration"),
        ("mock llm response", True, "mock llm"),
        ("Generate mock response", True, "mock response"),
        ("simulated for testing", True, "simulated for"),
        ("This is a test case", True, "test case"),
        ("Run unit test for module", True, "unit test"),
        ("integration test scenario", True, "integration test"),
        ("prove that the system works", True, "prove that"),
        ("show that BYRD can learn", True, "show that"),
        ("demonstrate that it understands", True, "demonstrate that"),
        ("example_desire for docs", True, "example_desire"),
        ("sample desire to show", True, "sample desire"),
        ("fake desire placeholder", True, "fake desire"),
        ("placeholder desire only", True, "placeholder desire"),
        ("mock desire for testing", True, "mock desire"),
        ("stub desire implementation", True, "stub desire"),
        ("dummy desire example", True, "dummy desire"),
        ("test_input parameter", True, "test_input"),
        ("sample_input data", True, "sample_input"),
        ("example input provided", True, "example input"),
        ("This is for testing only", True, "for testing"),
        ("Use for demo purposes", True, "for demo"),
        ("DEMONSTRATION desire", True, "case insensitive uppercase"),
        ("Demonstration Desire", True, "case insensitive title"),
        ("This is just a demo", True, "substring detection"),
        ("Create demonstration video", True, "substring detection"),
        ("Use for demonstration purposes only", True, "substring detection"),
        
        # Should accept (False)
        ("Learn about quantum computing", False, "normal desire"),
        ("Improve the memory system", False, "normal desire"),
        ("Analyze the current reflection", False, "normal desire"),
        ("Generate a creative response", False, "normal desire"),
        ("", False, "empty string"),
        (None, False, "None value"),
        # Note: demonstration and Demonstrate DO match due to substring matching
        # This is expected behavior - the filter is conservative
    ]
    
    print("Running Demonstration Filter Tests")
    print("=" * 60)
    
    for description, expected, name in test_cases:
        result = is_demonstration_desire(description)
        if result == expected:
            passed += 1
            print(f"✓ PASS: {name}")
        else:
            failed += 1
            print(f"✗ FAIL: {name}")
            print(f"  Description: {description}")
            print(f"  Expected: {expected}, Got: {result}")
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(test_filter())
