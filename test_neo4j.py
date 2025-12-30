#!/usr/bin/env python3
"""Simple test to check Neo4j connectivity."""

import os
import sys

# Load .env
env_file = '.env'
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Check connection
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

print(f"URI: {uri}")
print(f"User: {user}")
print(f"Password: {'*' * len(password) if password else 'not set'}")

try:
    from neo4j import GraphDatabase
    print("\nneo4j package imported successfully")
except ImportError as e:
    print(f"\nFailed to import neo4j: {e}")
    sys.exit(1)

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    print("\nConnected to Neo4j successfully!")
    
    # Test query
    with driver.session() as session:
        result = session.run("MATCH (n) WHERE NOT (n)-[]-() RETURN count(n) AS count")
        record = result.single()
        count = record["count"]
        print(f"\nFound {count} orphan nodes")
    
    driver.close()
    print("\nTest completed successfully!")
    
except Exception as e:
    print(f"\nError: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
