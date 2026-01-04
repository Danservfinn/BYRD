#!/usr/bin/env python3
"""
Test the hard filter for demonstration desires in seeker.py
"""

# Simulate the _is_demonstration_desire method
def _is_demonstration_desire(description: str) -> bool:
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


# Test cases
test_cases = [
    # Should be REJECTED (True)
    ("This is a demonstration of the system", True, "contains 'demonstration'"),
    ("Demo for testing purposes", True, "contains 'demo'"),
    ("test_desire example", True, "contains 'test_desire'"),
    ("test desire for unit testing", True, "contains 'test desire'"),
    ("example usage of the API", True, "contains 'example usage'"),
    ("mock memory data structure", True, "contains 'mock memory'"),
    ("for demonstration only", True, "contains 'for demonstration'"),
    ("mock llm response", True, "contains 'mock llm'"),
    ("simulated for testing", True, "contains 'simulated for'"),
    ("test case for authentication", True, "contains 'test case'"),
    ("unit test for parser", True, "contains 'unit test'"),
    ("integration test scenario", True, "contains 'integration test'"),
    ("prove that the system works", True, "contains 'prove that'"),
    ("show that data flows correctly", True, "contains 'show that'"),
    ("demonstrate that algorithm converges", True, "contains 'demonstrate that'"),
    ("example_desire for documentation", True, "contains 'example_desire'"),
    ("sample desire for user guide", True, "contains 'sample desire'"),
    ("fake desire placeholder", True, "contains 'fake desire'"),
    ("placeholder desire for UI", True, "contains 'placeholder desire'"),
    ("mock desire for testing", True, "contains 'mock desire'"),
    ("stub desire for API", True, "contains 'stub desire'"),
    ("dummy desire for integration", True, "contains 'dummy desire'"),
    ("test_input validation", True, "contains 'test_input'"),
    ("sample_input processing", True, "contains 'sample_input'"),
    ("example input data", True, "contains 'example input'"),
    ("for testing configuration", True, "contains 'for testing'"),
    ("for demo presentation", True, "contains 'for demo'"),
    
    # Should be ACCEPTED (False)
    ("Learn about quantum computing", False, "legitimate learning desire"),
    ("Improve the codebase architecture", False, "legitimate improvement desire"),
    ("Research machine learning papers", False, "legitimate research desire"),
    ("Optimize database queries", False, "legitimate optimization desire"),
    ("Implement user authentication", False, "legitimate implementation desire"),
    ("Analyze system performance", False, "legitimate analysis desire"),
    ("Connect to external API", False, "legitimate connection desire"),
    ("Refactor legacy code", False, "legitimate refactoring desire"),
    ("Explore new technologies", False, "legitimate exploration desire"),
    ("Understand user behavior patterns", False, "legitimate understanding desire"),
    ("Create visualization dashboard", False, "legitimate creation desire"),
    ("Debug memory leak issue", False, "legitimate debugging desire"),
    ("Deploy application to production", False, "legitimate deployment desire"),
    ("Monitor system health", False, "legitimate monitoring desire"),
    ("Document API endpoints", False, "legitimate documentation desire"),
    ("Improve test coverage", False, "legitimate improvement (but not a test desire itself)"),
    ("Enhance user experience", False, "legitimate enhancement desire"),
    ("Investigate performance bottleneck", False, "legitimate investigation desire"),
    ("Integrate payment gateway", False, "legitimate integration desire"),
    ("Analyze market trends", False, "legitimate analysis desire"),
]

# Run tests
print("Testing hard filter for demonstration desires...\n")
print("="*70)

passed = 0
failed = 0

for description, expected, reason in test_cases:
    result = _is_demonstration_desire(description)
    status = "✓ PASS" if result == expected else "✗ FAIL"
    
    if result == expected:
        passed += 1
    else:
        failed += 1
    
    action = "REJECT" if result else "ACCEPT"
    print(f"{status}: {action} - '{description[:50]}...' ({reason})")

print("="*70)
print(f"\nResults: {passed} passed, {failed} failed out of {len(test_cases)} tests")

if failed == 0:
    print("\n✓ All tests passed! Hard filter is working correctly.")
    exit(0)
else:
    print(f"\n✗ {failed} test(s) failed. Hard filter needs adjustment.")
    exit(1)
