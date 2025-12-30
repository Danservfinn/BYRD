#!/usr/bin/env python3
"""Query Neo4j for all orphan nodes and dump full content to orphans_dump.json.

An orphan node is defined as a node with no incoming or outgoing relationships.
This script connects to Neo4j, finds all such nodes, and exports their complete
information (element ID, labels, and all properties) to a JSON file.

Usage:
    python dump_orphan_nodes.py
    
Environment Variables:
    NEO4J_URI: Neo4j connection URI (default: bolt://localhost:7687)
    NEO4J_USER: Neo4j username (default: neo4j)
    NEO4J_PASSWORD: Neo4j password (default: password)
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


def get_neo4j_config() -> Dict[str, str]:
    """Retrieve Neo4j connection configuration from environment variables.
    
    Returns:
        Dictionary containing uri, user, and password for Neo4j connection.
    """
    return {
        "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        "user": os.getenv("NEO4J_USER", "neo4j"),
        "password": os.getenv("NEO4J_PASSWORD", "password")
    }


def serialize_neo4j_value(value: Any) -> Any:
    """Convert Neo4j data types to JSON-serializable Python types.
    
    Args:
        value: A value from Neo4j (may be special types like neo4j.time.Date)
        
    Returns:
        JSON-serializable representation of the value.
    """
    if value is None:
        return None
    
    # Handle Neo4j temporal types
    if hasattr(value, 'iso_format'):
        return value.iso_format()
    if hasattr(value, 'to_native'):
        return value.to_native()
    
    # Handle Neo4j spatial types (Point)
    if hasattr(value, 'srid') and hasattr(value, 'x') and hasattr(value, 'y'):
        return {
            "srid": value.srid,
            "x": value.x,
            "y": value.y,
            "z": getattr(value, 'z', None)
        }
    
    # Handle lists/dicts recursively
    if isinstance(value, list):
        return [serialize_neo4j_item(v) for v in value]
    if isinstance(value, dict):
        return {k: serialize_neo4j_item(v) for k, v in value.items()}
    
    return value


def serialize_neo4j_item(item: Any) -> Any:
    """Serialize a single Neo4j item, handling various data types."""
    try:
        return serialize_neo4j_value(item)
    except Exception:
        return str(item)


def fetch_orphan_nodes(config: Dict[str, str]) -> List[Dict[str, Any]]:
    """Query Neo4j for all orphan nodes.
    
    An orphan node is a node with no relationships (neither incoming nor outgoing).
    
    Args:
        config: Dictionary with Neo4j connection parameters.
        
    Returns:
        List of dictionaries containing orphan node information.
        
    Raises:
        ImportError: If neo4j package is not installed.
        Exception: For connection or query errors.
    """
    try:
        from neo4j import GraphDatabase
    except ImportError as e:
        raise ImportError(
            "neo4j Python driver not installed. Install with: pip install neo4j"
        ) from e
    
    # Cypher query to find nodes with no relationships
    query = "MATCH (n) WHERE NOT (n)-[]-() RETURN n"
    
    orphans = []
    
    with GraphDatabase.driver(
        config["uri"], 
        auth=(config["user"], config["password"])
    ) as driver:
        driver.verify_connectivity()
        
        with driver.session() as session:
            result = session.run(query)
            records = list(result)
            
            for idx, record in enumerate(records, 1):
                node = record["n"]
                
                # Serialize all properties for JSON compatibility
                properties = {}
                for key, value in node._properties.items():
                    properties[key] = serialize_neo4j_item(value)
                
                orphan = {
                    "index": idx,
                    "element_id": str(node.element_id),
                    "labels": list(node.labels),
                    "properties": properties
                }
                orphans.append(orphan)
    
    return orphans


def create_report(orphans: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a structured report with orphan node data.
    
    Args:
        orphans: List of orphan node dictionaries.
        
    Returns:
        Dictionary containing the complete report.
    """
    return {
        "query_info": {
            "description": "Orphan nodes (nodes with no relationships)",
            "cypher_query": "MATCH (n) WHERE NOT (n)-[]-() RETURN n"
        },
        "timestamp": datetime.now().isoformat(),
        "orphan_count": len(orphans),
        "orphans": orphans
    }


def write_json_report(report: Dict[str, Any], output_path: str) -> None:
    """Write the orphan node report to a JSON file.
    
    Args:
        report: The report dictionary to write.
        output_path: Path to the output JSON file.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    json_str = json.dumps(report, indent=2, ensure_ascii=False)
    output_file.write_text(json_str, encoding="utf-8")


def main() -> int:
    """Main execution function.
    
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    print("=" * 70)
    print("Neo4j Orphan Node Dump Utility")
    print("=" * 70)
    
    # Get configuration
    config = get_neo4j_config()
    print(f"URI: {config['uri']}")
    print(f"User: {config['user']}")
    print(f"Time: {datetime.now()}")
    print()
    
    output_file = "orphans_dump.json"
    
    try:
        # Fetch orphan nodes
        print("[*] Querying Neo4j for orphan nodes...")
        orphans = fetch_orphan_nodes(config)
        
        print(f"[+] Found {len(orphans)} orphan node(s)")
        print()
        
        # Display summary of orphans
        for orphan in orphans:
            print(f"  - ID: {orphan['element_id']}")
            print(f"    Labels: {', '.join(orphan['labels']) if orphan['labels'] else 'none'}")
            if orphan['properties']:
                prop_keys = list(orphan['properties'].keys())
                print(f"    Properties: {len(prop_keys)} ({', '.join(prop_keys[:5])}{'...' if len(prop_keys) > 5 else ''})")
        
        # Create and write report
        report = create_report(orphans)
        write_json_report(report, output_file)
        
        print()
        print(f"[+] Orphan data written to: {output_file}")
        print(f"[+] Total orphans: {len(orphans)}")
        print()
        print("=" * 70)
        return 0
        
    except ImportError as e:
        print(f"[!] Error: {e}")
        print("[!] Install the Neo4j Python driver: pip install neo4j")
        return 1
    except Exception as e:
        print(f"[!] Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
