#!/usr/bin/env python3
"""
Orphan Nodes Query - Full Content Retrieval

This script executes a Cypher query against Neo4j to retrieve ALL orphan nodes
(nodes with no relationships) and displays their complete content including
all properties and labels.

REQUIREMENTS:
    pip install neo4j python-dotenv

USAGE:
    python run_orphan_query.py

The script will:
1. Load Neo4j connection details from .env file
2. Execute: MATCH (n) WHERE NOT (n)-[]-() RETURN n
3. Display full content of every orphan node found
"""

import os
import sys
import json
from datetime import datetime

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual fallback
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Cypher query to find ALL orphan nodes and return complete node objects
CYPHER_QUERY = """
MATCH (n)
WHERE NOT (n)-[]-()
RETURN n AS orphan_node
ORDER BY elementId(n)
"""

def main():
    """Main execution function."""
    # Connection parameters from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    print("=" * 80)
    print("ORPHAN NODES - FULL CONTENT RETRIEVAL")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nNeo4j URI: {uri}")
    print(f"User: {user}")
    print()
    
    print("Cypher Query:")
    print("-" * 80)
    print(CYPHER_QUERY.strip())
    print("-" * 80)
    print()
    
    # Import Neo4j driver
    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("ERROR: neo4j package not installed!")
        print("\nPlease install required packages:")
        print("    pip install neo4j python-dotenv")
        sys.exit(1)
    
    driver = None
    orphan_nodes = []
    
    try:
        # Connect to Neo4j
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("✓ Connected to Neo4j database")
        print()
        
        # Execute query
        with driver.session() as session:
            result = session.run(CYPHER_QUERY)
            
            # Collect all orphan nodes with full content
            for record in result:
                node = record["orphan_node"]
                
                # Extract complete node information
                node_data = {
                    "element_id": node.element_id,
                    "labels": list(node.labels),
                    "properties": dict(node._properties)  # ALL properties
                }
                orphan_nodes.append(node_data)
        
        print(f"✓ Query executed successfully")
        print(f"✓ Found {len(orphan_nodes)} orphan node(s)")
        print()
        
        # Display FULL CONTENT
        print("=" * 80)
        print("FULL CONTENT OF ALL ORPHAN NODES")
        print("=" * 80)
        print()
        
        if not orphan_nodes:
            print("No orphan nodes found.")
            print("All nodes in the database have at least one relationship.")
        else:
            for idx, node_data in enumerate(orphan_nodes, 1):
                print(f"{'=' * 80}")
                print(f"ORPHAN NODE #{idx} - FULL CONTENT")
                print(f"{'=' * 80}")
                print(f"Element ID: {node_data['element_id']}")
                print(f"Labels: {', '.join(node_data['labels']) or '(none)'}")
                print()
                print("ALL PROPERTIES:")
                print("-" * 80)
                
                props = node_data['properties']
                if props:
                    print(json.dumps(props, indent=2, default=str, ensure_ascii=False))
                else:
                    print("(No properties)")
                
                print("-" * 80)
                print()
        
        print("=" * 80)
        print(f"SUMMARY: Retrieved {len(orphan_nodes)} orphan node(s) with full content")
        print("=" * 80)
        
        return orphan_nodes
        
    except Exception as e:
        print()
        print("=" * 80)
        print("ERROR")
        print("=" * 80)
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 80)
        sys.exit(1)
        
    finally:
        if driver:
            driver.close()
            print("\n✓ Connection closed")


if __name__ == "__main__":
    main()
