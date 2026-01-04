#!/usr/bin/env python3
"""Query Neo4j for orphan nodes and export to orphans_dump.json."""

import os
import sys
import json
from datetime import datetime

# Neo4j connection settings
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Cypher query for orphan nodes
ORPHAN_QUERY = "MATCH (n) WHERE NOT (n)-[]-() RETURN n"

# Output file
OUTPUT_FILE = "orphans_dump.json"


def main():
    """Execute the orphan node query and dump to JSON."""
    print("=" * 60)
    print("Neo4j Orphan Nodes Query")
    print("=" * 60)
    print(f"Time: {datetime.now()}")
    print(f"URI: {URI}")
    print()
    
    orphans = []
    
    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("[!] neo4j package not installed")
        sys.exit(1)
    
    try:
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        driver.verify_connectivity()
        print("[+] Connected to Neo4j")
        print()
        
        with driver.session() as session:
            result = session.run(ORPHAN_QUERY)
            records = list(result)
            
            print(f"[+] Found {len(records)} orphan node(s)")
            print()
            
            for idx, record in enumerate(records, 1):
                node = record["n"]
                orphan = {
                    "index": idx,
                    "element_id": str(node.element_id),
                    "labels": list(node.labels),
                    "properties": dict(node._properties)
                }
                orphans.append(orphan)
                print(f"--- Orphan #{idx} ---")
                print(f"ID: {node.element_id}")
                print(f"Labels: {list(node.labels)}")
        
        driver.close()
        print("[+] Query complete")
        
    except Exception as e:
        print(f"[!] Connection error: {e}")
        sys.exit(1)
    
    # Build output structure
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "query": ORPHAN_QUERY,
        "orphan_count": len(orphans),
        "orphans": orphans
    }
    
    # Convert to JSON string
    json_output = json.dumps(output_data, indent=2)
    
    # Write to file
    Path(OUTPUT_FILE).write_text(json_output)
    
    print(f"[+] Orphan data written to {OUTPUT_FILE}")
    print(f"[+] Total orphans: {len(orphans)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
