#!/usr/bin/env python3
"""Debug genesis to see actual errors"""

import sys
import traceback

print("=== Debugging genesis_reflect_constraint.py ===\n")

# Test 1: Can we import it?
try:
    print("[1] Attempting import...")
    import genesis_reflect_constraint
    print("    ✓ Import successful\n")
except Exception as e:
    print(f"    ✗ Import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 2: Does the function exist?
if hasattr(genesis_reflect_constraint, 'genesis_create_zai_constraint'):
    print("[2] ✓ genesis_create_zai_constraint function exists\n")
else:
    print("[2] ✗ Function not found\n")
    sys.exit(1)

# Test 3: Run the function with full output
print("[3] Running genesis function...\n")
import asyncio
try:
    result = asyncio.run(genesis_reflect_constraint.genesis_create_zai_constraint())
    print(f"\n[3] Function returned: {result}\n")
    if result:
        print("=== SUCCESS ===")
        sys.exit(0)
    else:
        print("=== FAILED: Returned None ===")
        sys.exit(1)
except Exception as e:
    print(f"\n[3] ✗ Exception during execution: {type(e).__name__}: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
