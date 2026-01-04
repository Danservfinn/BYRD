#!/usr/bin/env python3
"""Simple test to diagnose the orphan nodes script issue."""
import os
import sys

# Test 1: Check if Python is working
print("Python is working...", file=sys.stderr)

# Test 2: Load environment
env_file = '.env'
if os.path.exists(env_file):
    print("Loading .env file...", file=sys.stderr)
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    print(".env loaded", file=sys.stderr)

# Test 3: Check neo4j import
try:
    from neo4j import GraphDatabase
    print("neo4j package imported successfully", file=sys.stderr)
except ImportError as e:
    print(f"ERROR: neo4j not installed: {e}", file=sys.stderr)
    sys.exit(1)

# Test 4: Try connection
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

print(f"Attempting connection to {uri}", file=sys.stderr)

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    print("Connection successful!", file=sys.stderr)
    driver.close()
except Exception as e:
    print(f"Connection failed: {type(e).__name__}: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

print("All tests passed!", file=sys.stderr)
