#!/usr/bin/env python3
"""Minimal test that will show actual errors"""

import sys
import traceback

print("[1] Starting test...", flush=True)

try:
    print("[2] Importing genesis_reflect_constraint...", flush=True)
    import genesis_reflect_constraint
    print("[3] Import successful", flush=True)
    
    print("[4] Getting function...", flush=True)
    func = genesis_reflect_constraint.genesis_create_zai_constraint
    print(f"[5] Function: {func}", flush=True)
    
    print("[6] Calling async function...", flush=True)
    import asyncio
    
    async def run_with_output():
        print("[7] Inside async wrapper", flush=True)
        result = await func()
        print(f"[8] Function returned: {result}", flush=True)
        return result
    
    result = asyncio.run(run_with_output())
    print(f"[9] Final result: {result}", flush=True)
    
    if result:
        print("[10] SUCCESS", flush=True)
        sys.exit(0)
    else:
        print("[10] FAILURE - None returned", flush=True)
        sys.exit(1)
        
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)
