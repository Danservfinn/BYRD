#!/usr/bin/env python3
"""Run genesis with maximum debug output"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Enable all output
print("=== STARTING GENESIS DEBUG RUN ===")
print(f"Working directory: {os.getcwd()}")
print(f"config.yaml exists: {os.path.exists('config.yaml')}")

# Import and run
try:
    print("\n--- Importing module... ---")
    import genesis_reflect_constraint
    print("Module imported successfully")
    
    print("\n--- Getting function... ---")
    func = genesis_reflect_constraint.genesis_create_zai_constraint
    print(f"Function: {func}")
    
    print("\n--- Running genesis function... ---")
    import asyncio
    result = asyncio.run(func())
    
    print(f"\n=== RESULT: {result} ===")
    
    if result:
        print("SUCCESS: Genesis action completed")
        sys.exit(0)
    else:
        print("FAILURE: Genesis action returned None")
        sys.exit(1)
        
except Exception as e:
    print(f"\n=== EXCEPTION: {type(e).__name__} ===")
    print(f"Message: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
