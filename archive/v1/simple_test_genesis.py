#!/usr/bin/env python3
"""Simple direct test to see what's wrong"""

import asyncio
import sys

print("Starting simple test...")

try:
    from genesis_reflect_constraint import genesis_create_zai_constraint
    print("✓ Import successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Calling genesis function...")
result = asyncio.run(genesis_create_zai_constraint())
print(f"Result: {result}")
print("Done!")
