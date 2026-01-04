#!/usr/bin/env python
"""Minimal test for Memory demonstration filter."""
import sys
import traceback

try:
    print("Importing memory module...")
    from memory import Memory
    print("✓ Import successful")
    
    print("Creating Memory instance...")
    memory = Memory({})
    print("✓ Memory instance created")
    
    # Check if method exists
    if hasattr(memory, '_is_demonstration_desire'):
        print("✓ _is_demonstration_desire method exists")
    else:
        print("✗ _is_demonstration_desire method NOT FOUND")
        sys.exit(1)
    
    # Test a few cases
    print("\nRunning filter tests:")
    
    tests = [
        ("test_desire", True, "should filter"),
        ("demo desire", True, "should filter"),
        ("improve memory", False, "should pass"),
    ]
    
    all_passed = True
    for desc, expected, note in tests:
        try:
            result = memory._is_demonstration_desire(desc)
            status = "✓" if result == expected else "✗"
            if result != expected:
                all_passed = False
            print(f"  {status} '{desc}' -> {result} ({note})")
        except Exception as e:
            print(f"  ✗ '{desc}' -> ERROR: {e}")
            all_passed = False
    
    if all_passed:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed")
        sys.exit(1)
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
