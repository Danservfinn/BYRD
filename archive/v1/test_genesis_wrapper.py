#!/usr/bin/env python3
"""Wrapper to test genesis_reflect_constraint and show errors"""

import sys
import traceback

# Import the main function
try:
    from genesis_reflect_constraint import genesis_create_zai_constraint
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

# Run it with proper error handling
import asyncio

try:
    result = asyncio.run(genesis_create_zai_constraint())
    if result:
        print(f"\n=== SUCCESS: Constraint ID = {result} ===")
        sys.exit(0)
    else:
        print(f"\n=== FAILURE: Function returned None ===")
        sys.exit(1)
except Exception as e:
    print(f"\n=== RUNTIME ERROR: {type(e).__name__}: {e} ===")
    traceback.print_exc()
    sys.exit(1)
