#!/usr/bin/env python3
"""Debug script to test Neo4j connectivity."""

import os
import sys
import traceback

print("[1] Loading environment variables...")
env_file = '.env'
if os.path.exists(env_file):
    print(f"[2] Found .env file")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    print("[3] Environment variables loaded")
else:
    print("[2] No .env file found")

print("\n[4] Checking NEO4J_URI...")
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")
print(f"     URI: {uri}")
print(f"     User: {user}")
print(f"     Password set: {bool(password)}")

print("\n[5] Attempting to import neo4j...")
try:
    from neo4j import GraphDatabase
    print("[6] SUCCESS: neo4j imported")
except ImportError as e:
    print(f"[6] FAILED: {e}")
    print("\nThe neo4j Python package is not installed.")
    print("To install it, run: pip install neo4j")
    sys.exit(1)

print("\n[7] Attempting to connect to Neo4j...")
try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    print("[8] SUCCESS: Connected to Neo4j!")
    driver.close()
except Exception as e:
    print(f"[8] FAILED: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n[9] All checks passed!")
print("[10] Proceeding with orphan node query...")
