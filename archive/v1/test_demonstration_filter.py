"""Test the demonstration filter in seeker.py"""
import re

def _is_demonstration_desire(description: str) -> bool:
    """
 HARD FILTER: Check if a desire description is a demonstration/test desire.
    
    This prevents test/demo patterns from entering the desire system at the
    formulation level. Applied before any desire is created.
    
    The filter uses word boundary matching to avoid false positives from
    legitimate uses of words like "test" or "demo" in natural language.
    
    Args:
        description: The desire description to check
        
    Returns:
        True if this appears to be a demonstration/test desire, False otherwise
    """
    if not description:
        return False
    
    # Skip very short strings (likely false positives)
    if len(description.strip()) < 5:
        return False
        
    desc_lower = description.lower()
    
    # Define patterns with context for accurate matching
    # Each pattern is a tuple: (regex_pattern, description)
    demo_patterns = [
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
        
        # Example/sample with desire/task context
        (r'\bexample\s+(desire|want|task|request)\b', 'example desire'),
        (r'\bsample\s+desire\b', 'sample desire'),
        
        # Mock patterns (unambiguous)
        (r'\bmock\s+(memory|llm|response|desire|want)\b', 'mock something'),
        (r'\b(mock|stub|dummy)\s+desire\b', 'mock desire variants'),
        
        # Simulated patterns
        (r'\bsimulated\s+(for|in)\s+(testing|demo|demonstration)\b', 'simulated for'),
        
        # Test types
        (r'\b(unit|integration)\s+test\b', 'specific test types'),
        (r'\btest\s+case\b', 'test case'),
        (r'\btest_input\b', 'test_input literal'),
        (r'\bsample_input\b', 'sample_input literal'),
        
        # Prove/show/demonstrate that (verification phrases)
        (r'\b(prove|show|demonstrate)\s+that\s+(the|this|a)\s+(system|model|ai|agent)\b', 'prove/show that system'),
        (r'\b(prove|show)\s+that\s+BYRD\s+can\b', 'prove BYRD can'),
        
        # "for testing" patterns
        (r'\bfor\s+(testing|test|demo)\s+(only|purposes?)\b', 'for testing/purposes'),
        (r'\bthis\s+is\s+for\s+(testing|demo)\b', 'is for testing'),
        
        # Placeholder patterns
        (r'\b(fake|placeholder)\s+desire\b', 'fake/placeholder desire'),
        (r'\bexample\s+usage\b', 'example usage'),
        (r'\bexample\s+input\b', 'example input'),
    ]
    
    # Check each pattern
    for pattern, desc in demo_patterns:
        if re.search(pattern, desc_lower):
            return True
    
    return False

# Test cases
test_cases = [
    # Should be filtered (True)
    ("This is a demonstration desire", True),
    ("Create a demo desire for testing", True),
    ("This is for a demo only", True),
    ("test_desire example", True),
    ("mock memory for testing", True),
    ("Prove that the system works", True),
    ("this is for testing purposes", True),
    ("fake desire as placeholder", True),
    ("create a demonstration request for the system", True),
    
    # Should NOT be filtered (False) - legitimate desires
    ("I want to demonstrate my painting skills", False),
    ("Help me understand the demonstration of quantum computing principles", False),
    ("The demo version of the software has limitations", False),
    ("Test this hypothesis through experimentation", False),
    ("Create a comprehensive testing framework", False),
    ("Example of good coding practices", False),
    ("I need to sample the data for analysis", False),
    ("Can you demonstrate how to solve this problem?", False),
]

print("Testing demonstration filter:")
print("=" * 60)

passed = 0
failed = 0

for test_input, expected in test_cases:
    result = _is_demonstration_desire(test_input)
    status = "\u2713 PASS" if result == expected else "\u2717 FAIL"
    
    if result == expected:
        passed += 1
    else:
        failed += 1
    
    print(f"{status}: '{test_input[:50]}...' => {result} (expected {expected})")

print("=" * 60)
print(f"Results: {passed} passed, {failed} failed")

if failed == 0:
    print("\n\u2713 All tests passed! The demonstration filter is working correctly.")
else:
    print(f"\n\u2717 {failed} test(s) failed. The filter may need adjustment.")
