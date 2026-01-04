#!/usr/bin/env python3
"""Print orphan nodes directly to stdout - no file writing."""

import os
import sys
from datetime import datetime


def main():
    """Query and print orphan nodes to stdout."""
    # Neo4j connection settings from environment or defaults
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    # Cypher query to find orphan nodes (nodes with no relationships)
    query = "MATCH (n) WHERE NOT (n)-[]-() RETURN n"
    
    # Header
    print("=" * 60)
    print("ORPHAN NODE DUMP")
    print("=" * 60)
    print(f"URI: {uri}")
    print(f"Time: {datetime.now().isoformat()}")
    print()
    
    try:
        from neo4j import GraphDatabase
        
        # Connect to Neo4j
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("[+] Connected to Neo4j")
        print()
        
        # Execute query
        with driver.session() as session:
            result = session.run(query)
            records = list(result)
            
            # Report count
            print(f"[+] Found {len(records)} orphan node(s)")
            print()
            
            # Print each orphan node
            for idx, record in enumerate(records, 1):
                node = record["n"]
                print(f"--- Orphan #{idx} ---")
                print(f"ID: {node.element_id}")
                print(f"Labels: {', '.join(node.labels)}")
                if node._properties:
                    print("Properties:")
                    for key, value in sorted(node._properties.items()):
                        print(f"  {key}: {value}")
                print()
        
        driver.close()
        print("[+] Query complete")
        
    except ImportError:
        print("[!] Error: neo4j package not installed")
        print("    Install with: pip install neo4j")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Connection error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
