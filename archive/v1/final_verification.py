#!/usr/bin/env python3
"""Final verification of the demonstration filter."""
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
        # Direct demonstration keywords
        (r'\bdemonstration\b', 'direct demonstration'),
        
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

# Test key scenarios
tests = [
    ("This is a demonstration desire", True),
    ("demo desire for testing", True),
    ("test_desire example", True),
    ("mock llm response", True),
    ("unit test for module", True),
    ("for testing purposes", True),
    ("example usage of system", True),
    ("fake desire placeholder", True),
    ("just a demo", True),
    ("for a demo", True),
    ("", False),
    (None, False),
    ("demo", False),
    ("Test the hypothesis", False),
    ("Demonstrate understanding", False),
    ("Learn about quantum computing", False),
    ("Improve memory system", False),
    ("Remove bottleneck: Optimize", False),
]

print("Final Verification of Demonstration Filter")
print("=" * 60)

all_pass = True
for desc, expected in tests:
    result = _is_demonstration_desire(desc)
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        all_pass = False
    print(f"{status}: '{str(desc)[:40]}...' -> {result} (expected {expected})")

print("=" * 60)
if all_pass:
    print("\u2713 All tests PASSED! Filter is complete.")
else:
    print("\u2717 Some tests FAILED.")
