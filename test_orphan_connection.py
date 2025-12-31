#!/usr/bin/env python3
"""Test orphan node connection."""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from memory import Memory


async def main():
    load_dotenv()
    
    print("Testing memory connection...")
    
    memory = Memory()
    
    try:
        await memory.connect()
        print("✓ Connected to memory")
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        sys.exit(1)
    
    try:
        orphans = await memory.find_orphan_nodes()
        print(f"✓ Found {len(orphans)} orphan nodes")
        
        for i, orphan in enumerate(orphans[:5]):
            print(f"  [{i}] ID: {orphan.get('id', 'N/A')[:16]}... Type: {orphan.get('type', 'N/A')}")
    except Exception as e:
        print(f"✗ Failed to find orphans: {e}")
        import traceback
        traceback.print_exc()
        await memory.close()
        sys.exit(1)
    
    await memory.close()
    print("✓ Done")


if __name__ == "__main__":
    asyncio.run(main())
