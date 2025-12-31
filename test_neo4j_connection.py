#!/usr/bin/env python3
"""Simple test of Neo4j connection."""

import os
import sys

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Test imports
try:
    from neo4j import GraphDatabase
    print("[OK] Neo4j driver imported")
except ImportError as e:
    print(f"[ERROR] Cannot import neo4j: {e}")
    sys.exit(1)

# Get connection params
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

print(f"URI: {uri}")
print(f"User: {user}")
print(f"Password: {'*' * len(password)}")

# Test connection
try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    print("[OK] Connection verified")
    
    # Test a simple query
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        print(f"[OK] Test query successful: {result.single()['test']}")
    
    driver.close()
    print("[OK] Connection closed")
    print("\n✓ Neo4j connection works!")
    
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
