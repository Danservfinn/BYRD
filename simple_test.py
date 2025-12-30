#!/usr/bin/env python3
"""Simple test to check basic functionality."""

import asyncio
import sys

print("Python version:", sys.version)
print("Starting simple test...")

async def main():
    print("Inside main()")
    print("Test passed!")

if __name__ == "__main__":
    asyncio.run(main())
