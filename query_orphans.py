#!/usr/bin/env python3
"""Query Neo4j for orphan nodes and dump to orphans_dump.json."""

import os
import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    """Find orphan nodes and dump to JSON file."""
    # Get Neo4j connection settings from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    # Cypher query to find orphan nodes (nodes with no relationships)
    query = "MATCH (n) WHERE NOT (n)-[]-() RETURN n"
    
    # Output data structure
    output = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "neo4j_uri": uri,
            "query": query
        },
        "orphans": []
    }
    
    print("=" * 60)
    print("ORPHAN NODE DUMP")
    print("=" * 60)
    print(f"URI: {uri}")
    print(f"Time: {output['metadata']['timestamp']}")
    print()
    
    try:
        from neo4j import GraphDatabase
        
        # Connect to Neo4j
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("[+] Connected to Neo4j")
        print()
        
        with driver.session() as session:
            result = session.run(query)
            records = list(result)
            
            print(f"[+] Found {len(records)} orphan node(s)")
            print()
            
            if len(records) == 0:
                print("No orphan nodes found.")
            else:
                # Collect each orphan node
                for record in records:
                    node = record["n"]
                    props = dict(node._properties)
                    
                    orphan_data = {
                        "element_id": node.element_id,
                        "labels": list(node.labels),
                        "properties": props
                    }
                    output["orphans"].append(orphan_data)
                    print(f"[+] Processed node: {node.element_id}")
        
        # Write output to JSON file using pathlib
        output_path = Path("orphans_dump.json")
        output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"[+] Dumped {len(records)} orphan(s) to {output_path}")
        
        driver.close()
        print("=" * 60)
        print(f"[+] Total orphans: {len(records)}")
        print("=" * 60)
        
        return 0
        
    except ImportError:
        print("[!] ERROR: neo4j package not installed")
        print("    Install with: pip install neo4j")
        return 1
    except Exception as e:
        print(f"[!] ERROR: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
