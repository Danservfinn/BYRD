#!/usr/bin/env python3
"""Debug script to check genesis_reflect_constraint.py"""

# First, let's check if the file has syntax errors
import ast
import sys

try:
    with open("genesis_reflect_constraint.py", "r") as f:
        content = f.read()
    
    print("File content length:", len(content))
    print("\n--- First 500 chars ---")
    print(content[:500])
    print("\n--- Checking syntax... ---")
    ast.parse(content)
    print("✓ Syntax is valid")
    
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
    print(f"   Line {e.lineno}: {e.text}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print("\n--- Checking for main function ---")
if "async def genesis_create_zai_constraint" in content:
    print("✓ genesis_create_zai_constraint function found")
if 'if __name__ == "__main__"' in content:
    print("✓ __main__ guard found")

print("\nAll checks passed!")
