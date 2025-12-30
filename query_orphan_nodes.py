#!/usr/bin/env python3
"""
Query Neo4j for all orphan nodes and dump their full content to JSON.

Orphan nodes are nodes that have no relationships (no incoming or outgoing edges).
This script connects to Neo4j, executes a Cypher query to find all such nodes,
and writes their complete data (element_id, labels, and properties) to orphans_dump.json.

Usage:
    python query_orphan_nodes.py

Environment Variables:
    NEO4J_URI: Connection URI (default: bolt://localhost:7687)
    NEO4J_USER: Username (default: neo4j)
    NEO4J_PASSWORD: Password (default: password)
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


def get_connection_params() -> tuple[str, str, str]:
    """Get Neo4j connection parameters from environment variables."""
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    return uri, user, password


def query_orphan_nodes(uri: str, user: str, password: str) -> List[Dict[str, Any]]:
    """
    Query Neo4j for all orphan nodes.
    
    Args:
        uri: Neo4j connection URI
        user: Neo4j username
        password: Neo4j password
        
    Returns:
        List of orphan node dictionaries containing element_id, labels, and properties
    """
    # Cypher query to find nodes with no relationships
    query = "MATCH (n) WHERE NOT (n)-[]-() RETURN n"
    
    orphans: List[Dict[str, Any]] = []
    
    try:
        from neo4j import GraphDatabase
        
        print(f"\n{'='*60}")
        print("Neo4j Orphan Node Query")
        print(f"{'='*60}")
        print(f"URI: {uri}")
        print(f"Time: {datetime.now().isoformat()}")
        print()
        
        # Connect to Neo4j
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("[+] Successfully connected to Neo4j")
        print()
        
        # Execute query
        with driver.session() as session:
            result = session.run(query)
            records = list(result)
            
            print(f"[+] Found {len(records)} orphan node(s)")
            print()
            
            # Process each orphan node
            for idx, record in enumerate(records, 1):
                node = record["n"]
                
                orphan = {
                    "index": idx,
                    "element_id": str(node.element_id),
                    "labels": list(node.labels),
                    "properties": dict(node._properties)
                }
                orphans.append(orphan)
                
                # Print summary
                print(f"--- Orphan #{idx} ---")
                print(f"  ID: {node.element_id}")
                print(f"  Labels: {', '.join(node.labels) if node.labels else '(none)'}")
                if node._properties:
                    print(f"  Properties: {len(node._properties)} key(s)")
                print()
        
        driver.close()
        print("[+] Query complete")
        
    except ImportError:
        print("[!] Error: neo4j Python package not installed")
        print("[!] Install with: pip install neo4j")
    except Exception as e:
        print(f"[!] Error: {type(e).__name__}: {e}")
    
    return orphans


def write_orphans_dump(orphans: List[Dict[str, Any]], output_file: str = "orphans_dump.json") -> None:
    """
    Write orphan nodes to a JSON file.
    
    Args:
        orphans: List of orphan node dictionaries
        output_file: Path to output JSON file
    """
    # Create report structure
    report = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "query": "MATCH (n) WHERE NOT (n)-[]-() RETURN n",
            "description": "Orphan nodes (nodes with no relationships)"
        },
        "summary": {
            "total_orphans": len(orphans),
            "orphans_by_label": _count_orphans_by_label(orphans)
        },
        "orphans": orphans
    }
    
    # Write to file
    output_path = Path(output_file)
    json_str = json.dumps(report, indent=2, ensure_ascii=False)
    output_path.write_text(json_str, encoding='utf-8')
    
    print(f"\n[+] Orphan data written to: {output_path.absolute()}")
    print(f"[+] Total orphans: {len(orphans)}")


def _count_orphans_by_label(orphans: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count orphans grouped by their labels."""
    label_counts: Dict[str, int] = {}
    
    for orphan in orphans:
        labels = orphan.get("labels", [])
        if not labels:
            label_key = "(no labels)"
        else:
            label_key = ", ".join(sorted(labels))
        
        label_counts[label_key] = label_counts.get(label_key, 0) + 1
    
    return label_counts


def main() -> int:
    """Main entry point for the orphan node query script."""
    # Get connection parameters
    uri, user, password = get_connection_params()
    
    # Query for orphan nodes
    orphans = query_orphan_nodes(uri, user, password)
    
    # Write results to JSON file
    write_orphans_dump(orphans, "orphans_dump.json")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
