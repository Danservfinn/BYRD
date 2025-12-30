#!/usr/bin/env python3
"""Check if we can import graph_connectivity and understand its structure."""

import sys
import os

print("Python path:")
for p in sys.path[:5]:
    print(f"  {p}")
print()

print("Files in current directory:")
for f in os.listdir('.')[:10]:
    if f.endswith('.py'):
        print(f"  {f}")
print()

print("Checking for neo4j module...")
try:
    import neo4j
    print("  ✓ neo4j is available")
except ImportError:
    print("  ✗ neo4j not installed (expected in sandbox)")
print()

print("Checking graph_connectivity module structure...")
try:
    # Mock neo4j first
    from unittest.mock import Mock
    mock_neo4j = Mock()
    sys.modules['neo4j'] = mock_neo4j
    
    import graph_connectivity
    print("  ✓ graph_connectivity imported successfully")
    print()
    
    print("Available classes/functions:")
    for name in dir(graph_connectivity):
        obj = getattr(graph_connectivity, name)
        if not name.startswith('_') and callable(obj) or isinstance(obj, type):
            print(f"  • {name}")
    
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()
