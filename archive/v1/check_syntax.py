#!/usr/bin/env python
"""Quick syntax check for memory.py"""
import ast
import sys

try:
    with open('memory.py', 'r') as f:
        code = f.read()
    ast.parse(code)
    print("✓ memory.py syntax is valid")
    sys.exit(0)
except SyntaxError as e:
    print(f"✗ Syntax error in memory.py: {e}")
    sys.exit(1)
