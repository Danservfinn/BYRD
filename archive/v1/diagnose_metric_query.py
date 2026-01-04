#!/usr/bin/env python3
"""Minimal diagnostic script for Metric query deadlock break."""

import os
import sys

print("="*60)
print("DIAGNOSTIC - Metric Query Deadlock Break")
print("="*60)

# Test 1: Python version
print(f"\n[1] Python version: {sys.version}")

# Test 2: Check neo4j import
print("\n[2] Checking neo4j driver...")
try:
    import neo4j
    print(f"    OK - neo4j version {neo4j.__version__}")
except ImportError as e:
    print(f"    FAIL - {e}")
    print("    Install: pip install neo4j")
    sys.exit(1)

# Test 3: Environment variables
print("\n[3] Checking environment variables...")
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')

print(f"    NEO4J_URI: {'SET' if uri else 'NOT SET'}")
print(f"    NEO4J_USER: {'SET' if user else 'NOT SET'}")
print(f"    NEO4J_PASSWORD: {'SET' if password else 'NOT SET'}")

# Load from .env if needed
if not all([uri, user, password]):
    print("\n    Loading from .env file...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        uri = os.getenv('NEO4J_URI')
        user = os.getenv('NEO4J_USER')
        password = os.getenv('NEO4J_PASSWORD')
        print("    Loaded via dotenv")
    except ImportError:
        # Manual .env parsing
        if os.path.exists('.env'):
            with open('.env') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            uri = os.getenv('NEO4J_URI')
            user = os.getenv('NEO4J_USER')
            password = os.getenv('NEO4J_PASSWORD')
            print("    Loaded manually")

# Fallback values
if not uri:
    uri = 'neo4j+s://9b21f7a8.databases.neo4j.io'
if not user:
    user = 'neo4j'
if not password:
    password = '1mSKWa8gwgwQ22kbqQB7ICpNtACFcG7WHDT7ZROCOy8'

print(f"\n    Using URI: {uri[:30]}...")
print(f"    Using User: {user}")

# Test 4: Connection
print("\n[4] Testing Neo4j connection...")
from neo4j import GraphDatabase

driver = None
try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    print("    OK - Connected successfully")
except Exception as e:
    print(f"    FAIL - {type(e).__name__}: {e}")
    sys.exit(1)

# Test 5: Query
print("\n[5] Executing metric query...")
try:
    with driver.session() as session:
        result = session.run("MATCH (n:LoopMetric) RETURN count(n) as count")
        count = result.single()["count"]
        print(f"    LoopMetric nodes: {count}")
except Exception as e:
    print(f"    FAIL - {type(e).__name__}: {e}")

# Cleanup
if driver:
    driver.close()
    print("\n[6] Connection closed")

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)
