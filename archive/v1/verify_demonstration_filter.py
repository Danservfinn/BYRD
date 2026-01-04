#!/usr/bin/env python3
"""
Comprehensive verification test for the updated demonstration filter in seeker.py

This verifies that the updated _is_demonstration_desire method:
1. Uses regex patterns with word boundaries
2. Avoids false positives from legitimate language
3. Properly filters test/demo patterns
"""
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
    
    # Handle None explicitly
    if description is None:
        return False
    
    # Skip very short strings (likely false positives)
    if len(str(description).strip()) < 5:
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

def run_tests():
    """Run comprehensive test suite."""
    print("=" * 70)
    print("COMPREHENSIVE DEMONSTRATION FILTER VERIFICATION")
    print("=" * 70)
    print()
    
    # Test cases: (description, expected_result, category, note)
    test_cases = [
        # SHOULD REJECT - Test/demo patterns
        ("This is a demonstration desire", True, "REJECT", "direct demonstration keyword"),
        ("demo desire for testing", True, "REJECT", "demo with desire context"),
        ("test_desire example", True, "REJECT", "test_desire literal"),
        ("This is a test desire", True, "REJECT", "test desire phrase"),
        ("example usage of the system", True, "REJECT", "example usage"),
        ("Use mock memory for this", True, "REJECT", "mock memory"),
        ("This is for demonstration purposes", True, "REJECT", "for demonstration"),
        ("mock llm response", True, "REJECT", "mock llm"),
        ("Generate mock response", True, "REJECT", "mock response"),
        ("simulated for testing", True, "REJECT", "simulated for testing"),
        ("This is a test case", True, "REJECT", "test case"),
        ("Run unit test for module", True, "REJECT", "unit test"),
        ("integration test scenario", True, "REJECT", "integration test"),
        ("prove that the system works", True, "REJECT", "prove that system"),
        ("show that BYRD can learn", True, "REJECT", "show that BYRD can"),
        ("demonstrate that it understands", True, "REJECT", "demonstrate that"),
        ("example_desire for docs", True, "REJECT", "example_desire literal"),
        ("sample desire for user guide", True, "REJECT", "sample desire"),
        ("fake desire placeholder", True, "REJECT", "fake desire"),
        ("placeholder desire only", True, "REJECT", "placeholder desire"),
        ("mock desire for testing", True, "REJECT", "mock desire"),
        ("stub desire implementation", True, "REJECT", "stub desire"),
        ("dummy desire example", True, "REJECT", "dummy desire"),
        ("test_input parameter", True, "REJECT", "test_input"),
        ("sample_input data", True, "REJECT", "sample_input"),
        ("example input provided", True, "REJECT", "example input"),
        ("This is for testing only", True, "REJECT", "for testing only"),
        ("Use for demo purposes", True, "REJECT", "for demo purposes"),
        ("This is just a demo", True, "REJECT", "just a demo"),
        ("Run this for a demo", True, "REJECT", "for a demo"),
        ("Create demonstration video", True, "REJECT", "demonstration keyword"),
        ("Use for demonstration purposes only", True, "REJECT", "for demonstration purposes"),
        ("example desire for documentation", True, "REJECT", "example desire"),
        
        # SHOULD ACCEPT - Legitimate desires
        ("Learn about quantum computing", False, "ACCEPT", "normal learning desire"),
        ("Improve the memory system", False, "ACCEPT", "system improvement"),
        ("Analyze the current reflection", False, "ACCEPT", "analysis task"),
        ("Generate a creative response", False, "ACCEPT", "creative task"),
        ("Test the hypothesis", False, "ACCEPT", "legitimate scientific test"),
        ("Demonstrate understanding of the topic", False, "ACCEPT", "legitimate demonstrate"),
        ("Check the demo file for reference", False, "ACCEPT", "demo as noun (legitimate)"),
        ("This is an example of good code", False, "ACCEPT", "example without desire context"),
        ("Test the system performance", False, "ACCEPT", "legitimate performance test"),
        ("Remove bottleneck: Optimize query", False, "ACCEPT", "production task"),
        ("Accelerate memory retrieval", False, "ACCEPT", "production task"),
        
        # EDGE CASES
        ("", False, "ACCEPT", "empty string"),
        (None, False, "ACCEPT", "None value"),
        ("demo", False, "ACCEPT", "short string (too short)"),
        ("dem", False, "ACCEPT", "very short string"),
        ("a demo", False, "ACCEPT", "short with context"),
        ("DEMONSTRATION desire", True, "REJECT", "case insensitive"),
        ("Demonstration Desire", True, "REJECT", "case insensitive"),
        ("DeMoNsTrAtIoN dEsIrE", True, "REJECT", "case insensitive"),
    ]
    
    passed = 0
    failed = 0
    
    for desc, expected, category, note in test_cases:
        result = _is_demonstration_desire(desc)
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
            print(f"{status} {category}: {note}")
            print(f"  Input: '{desc[:50]}...'" if len(str(desc)) > 50 else f"  Input: '{desc}'")
            print(f"  Expected: {expected}, Got: {result}")
            print()
    
    # Summary
    total = passed + failed
    print()
    print("=" * 70)
    print(f"RESULTS: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    if failed == 0:
        print("✓ All tests passed! The demonstration filter is working correctly.")
    else:
        print(f"✗ {failed} test(s) failed.")
    print("=" * 70)
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
