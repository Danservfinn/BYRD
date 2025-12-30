#!/usr/bin/env python3
"""Query Neo4j for orphan nodes and dump to orphans_dump.json."""

import os
import sys
import json
from datetime import datetime

def main():
    """Execute orphan node query and dump to JSON."""
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    query = "MATCH (n) WHERE NOT (n)-[]-() RETURN n"
    
    output_file = "orphans_dump.json"
    
    print("=" * 60)
    print("NEO4J ORPHAN NODE DUMPER")
    print("=" * 60)
    print(f"URI: {uri}")
    print(f"Time: {datetime.now()}")
    print()
    
    orphans = []
    
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("[+] Connected to Neo4j")
        print()
        
        with driver.session() as session:
            result = session.run(query)
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
                print(f"  ID: {node.element_id}")
                print(f"  Labels: {list(node.labels)}")
        
        driver.close()
        print("[+] Query complete")
        
    except ImportError:
        print("[!] neo4j package not installed")
        orphans = []
    except Exception as e:
        print(f"[!] Connection error: {e}")
        orphans = []
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "orphan_count": len(orphans),
        "orphans": orphans
    }
    
    from pathlib import Path
    json_str = json.dumps(report, indent=2)
    Path(output_file).write_text(json_str)
    
    print(f"[+] Orphan data written to {output_file}")
    print(f"[+] Total orphans: {len(orphans)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
