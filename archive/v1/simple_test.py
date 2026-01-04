#!/usr/bin/env python
"""Very simple test that just checks if code runs."""
print("Starting...")

# Test the filter pattern directly
import re

demo_patterns = [
    (r'\bdemonstration\b', 'direct demonstration'),
    (r'\bdemo\s+(desire|want|task|request|example|case)\b', 'demo with context'),
    (r'\b(for|as)\s+a\s+demo\b', 'for/as a demo'),
    (r'\bdemo\s+(purposes?|only)\b', 'demo for purposes'),
    (r'\bjust\s+a\s+demo\b', 'just a demo'),
    (r'\btest_desire\b', 'test_desire literal'),
    (r'\btest\s+desire\b', 'test desire phrase'),
]

def check_demo(description):
    if not description:
        return False
    if len(description.strip()) < 5:
        return False
    desc_lower = description.lower()
    for pattern, desc in demo_patterns:
        if re.search(pattern, desc_lower):
            return True
    return False

# Test cases
tests = [
    "test_desire",
    "demo desire",
    "improve memory",
    "",
    "hi",
]

for t in tests:
    result = check_demo(t)
    print(f"'{t}' -> {result}")

print("\nDirect test complete")
