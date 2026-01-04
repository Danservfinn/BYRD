#!/usr/bin/env python3
"""Simple test to check orphan_reader and reflection_engine imports."""

import sys
print(f"Python version: {sys.version}")

try:
    print("\n[1] Testing reflection_engine imports...")
    from reflection_engine import ReflectionEngine, ReflectionContext, Desire, DesireType
    print("    ✓ reflection_engine imports successful")
except Exception as e:
    print(f"    ✗ reflection_engine import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n[2] Testing orphan_reader imports...")
    from orphan_reader import OrphanReader, OrphanContextSnapshot, get_orphan_reader
    print("    ✓ orphan_reader imports successful")
except Exception as e:
    print(f"    ✗ orphan_reader import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n[3] Testing memory import...")
    from memory import Memory
    print("    ✓ memory import successful")
except Exception as e:
    print(f"    ✗ memory import failed: {e}")

print("\n[4] Testing basic ReflectionEngine instantiation...")
try:
    engine = ReflectionEngine()
    print("    ✓ ReflectionEngine instantiated")
except Exception as e:
    print(f"    ✗ ReflectionEngine instantiation failed: {e}")
    import traceback
    traceback.print_exc()

print("\nAll tests complete.")
