#!/usr/bin/env python3
"""Simple test to check Neo4j connection."""

import os
import sys

# Load .env
def load_env():
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

print("Environment loaded:")
print(f"  URI: {uri}")
print(f"  User: {user}")
print(f"  Password: {'*' * len(password) if password else 'None'}")
print()

try:
    from neo4j import GraphDatabase
    print("neo4j package imported successfully")
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    print("Driver created")
    
    driver.verify_connectivity()
    print("Connectivity verified!")
    
    driver.close()
    print("Connection closed")
    
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
