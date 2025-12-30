#!/usr/bin/env python3
"""Check if neo4j package can be imported."""
import sys
print("Testing neo4j import...")
try:
    import neo4j
    print(f"neo4j imported successfully, version: {neo4j.__version__}")
    from neo4j import GraphDatabase
    print("GraphDatabase imported successfully")
except ImportError as e:
    print(f"ImportError: {e}")
    print("The neo4j package may not be installed in this environment")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
