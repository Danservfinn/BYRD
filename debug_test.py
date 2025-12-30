#!/usr/bin/env python3
"""Simple debug test to understand the test failure."""

import asyncio
import sys
import traceback

print("Starting debug test...")
print(f"Python version: {sys.version}")

try:
    # Try importing the test module
    print("\nAttempting to import test_graph_connectivity...")
    import test_graph_connectivity
    print("✓ Import successful")
    
    # Try running the main function
    print("\nAttempting to run main...")
    asyncio.run(test_graph_connectivity.main())
    print("✓ Main completed successfully")
    
except Exception as e:
    print(f"\n✗ Error occurred: {type(e).__name__}: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)

print("\n✓ Debug test completed successfully")
