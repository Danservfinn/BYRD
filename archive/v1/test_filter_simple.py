#!/usr/bin/env python3
"""Simple test to debug the filter."""
import re

def test_filter(description: str) -> bool:
    """Test if description is a demonstration desire."""
    if not description:
        return False
    if description is None:
        return False
    if len(str(description).strip()) < 5:
        return False
    
    desc_lower = description.lower()
    
    # Simple patterns first
    if 'demonstration' in desc_lower:
        return True
    if 'test_desire' in desc_lower:
        return True
    if 'test desire' in desc_lower:
        return True
    if 'example usage' in desc_lower:
        return True
    if 'mock memory' in desc_lower:
        return True
    if 'for demonstration' in desc_lower:
        return True
    if 'mock llm' in desc_lower:
        return True
    if 'mock response' in desc_lower:
        return True
    if 'simulated for' in desc_lower:
        return True
    if 'test case' in desc_lower:
        return True
    if 'unit test' in desc_lower:
        return True
    if 'integration test' in desc_lower:
        return True
    if 'prove that' in desc_lower:
        return True
    if 'show that' in desc_lower:
        return True
    if 'demonstrate that' in desc_lower:
        return True
    if 'example_desire' in desc_lower:
        return True
    if 'sample desire' in desc_lower:
        return True
    if 'fake desire' in desc_lower:
        return True
    if 'placeholder desire' in desc_lower:
        return True
    if 'mock desire' in desc_lower:
        return True
    if 'stub desire' in desc_lower:
        return True
    if 'dummy desire' in desc_lower:
        return True
    if 'test_input' in desc_lower:
        return True
    if 'sample_input' in desc_lower:
        return True
    if 'example input' in desc_lower:
        return True
    if 'for testing' in desc_lower:
        return True
    if 'for demo' in desc_lower:
        return True
    
    return False

# Test
test_desc = "This is a demonstration desire"
result = test_filter(test_desc)
print(f"Test: '{test_desc}' -> {result}")
print("Expected: True")
print(f"Result: {'PASS' if result == True else 'FAIL'}")
