#!/usr/bin/env python3
"""
Orphan Nodes Query - Retrieve and display all orphan nodes from Neo4j

This script executes a Cypher query to find all nodes with no relationships
(orphan nodes) and displays their full content.
"""

import os
import sys

# Print startup message
print("=" * 70)
print("ORPHAN NODES QUERY")
print("=" * 70)

# Load environment
from dotenv import load_dotenv
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

print(f"\nConfiguration:")
print(f"  URI: {NEO4J_URI}")
print(f"  User: {NEO4J_USER}")
print(f"  Password: {'***' if NEO4J_PASSWORD else 'NOT SET'}")

# The Cypher query to find orphan nodes
CYPHER_QUERY = """
MATCH (n)
WHERE NOT (n)-[]-()
RETURN n AS orphan_node
"""

print(f"\nCypher Query:")
print(f"{CYPHER_QUERY.strip()}")
print()

try:
    from neo4j import GraphDatabase
    print("[*] Neo4j driver imported successfully")
except ImportError as e:
    print(f"[!] ERROR: Failed to import neo4j: {e}")
    print("[!] Please install: pip install neo4j python-dotenv")
    sys.exit(1)

# Connect and execute
print("[*] Connecting to Neo4j...")
driver = None

try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    driver.verify_connectivity()
    print("[+] Connected successfully!")
    
    with driver.session() as session:
        print("[*] Executing query...")
        result = session.run(CYPHER_QUERY)
        
        # Collect results
        records = list(result)
        count = len(records)
        
        print(f"[+] Query completed. Found {count} orphan node(s).")
        print("\n" + "=" * 70)
        print("RESULTS - Full Content of Orphan Nodes")
        print("=" * 70)
        
        if count == 0:
            print("\nNo orphan nodes found in the database.")
        else:
            for idx, record in enumerate(records, 1):
                node = record["orphan_node"]
                print(f"\n--- ORPHAN NODE {idx} ---")
                print(f"Labels: {list(node.labels)}")
                print(f"Element ID: {node.element_id}")
                print(f"Properties:")
                for key, value in node._properties.items():
                    print(f"  {key}: {value}")
        
        print("\n" + "=" * 70)
        print("Query completed successfully!")
        print("=" * 70)
        
except Exception as e:
    print(f"\n[!] ERROR: {type(e).__name__}")
    print(f"[!] Message: {e}")
    import traceback
    print("\n[!] Full traceback:")
    traceback.print_exc()
    sys.exit(1)
    
finally:
    if driver:
        driver.close()
        print("\n[*] Connection closed.")
