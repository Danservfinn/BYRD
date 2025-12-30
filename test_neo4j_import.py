#!/usr/bin/env python3
"""Test if neo4j package is available"""
import sys

print("Testing neo4j import...")
try:
    from neo4j import GraphDatabase
    print("✓ neo4j package is available")
    print(f"  Version: {GraphDatabase.__version__ if hasattr(GraphDatabase, '__version__') else 'unknown'}")
except ImportError as e:
    print(f"✗ neo4j package NOT available")
    print(f"  Error: {e}")
    sys.exit(1)

print("Test completed successfully")
