#!/usr/bin/env python3
"""
Cypher Query Executor - Retrieve All Orphan Nodes

This script executes a Cypher query to retrieve the full content (all properties)
of all orphan nodes in a Neo4j graph database.

An orphan node is defined as a node that has no relationships (incoming or outgoing)
with any other nodes in the graph.

Usage:
    python retrieve_orphan_nodes.py

Requirements:
    - neo4j Python driver (install with: pip install neo4j)
    - Neo4j database connection configured in .env file

Environment Variables:
    NEO4J_URI: Neo4j connection URI (e.g., bolt://localhost:7687)
    NEO4J_USER: Neo4j username
    NEO4J_PASSWORD: Neo4j password
"""

import os
import sys
from typing import List, Dict, Any

# Load environment variables from .env file
def load_environment():
    """Load environment variables from .env file."""
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


def retrieve_orphan_nodes() -> List[Dict[str, Any]]:
    """
    Execute Cypher query to retrieve all orphan nodes with their full properties.
    
    The Cypher query:
        MATCH (n)
        WHERE NOT (n)-[]-()
        RETURN properties(n) AS node_properties
    
    Query breakdown:
        - MATCH (n): Find all nodes in the graph
        - WHERE NOT (n)-[]-(): Filter for nodes with no relationships (orphan nodes)
        - RETURN properties(n) AS node_properties: Return all properties of each orphan node
    
    Returns:
        List of dictionaries, where each dictionary contains all properties
        of one orphan node. Returns None if connection/query fails.
    
    Example output:
        [
            {'id': 1, 'name': 'Orphan1', 'type': 'Node'},
            {'id': 2, 'name': 'Orphan2', 'created_at': '2024-01-01'}
        ]
    """
    # Load environment variables
    load_environment()
    
    # Neo4j connection parameters
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    # Cypher query to retrieve all orphan nodes with all their properties
    cypher_query = """
        MATCH (n)
        WHERE NOT (n)-[]-()
        RETURN properties(n) AS node_properties
    """
    
    print("=" * 70)
    print("CYPHER QUERY - Retrieve All Orphan Nodes")
    print("=" * 70)
    print(cypher_query.strip())
    print("=" * 70)
    print(f"\nNeo4j URI: {uri}")
    print(f"User: {user}")
    print()
    
    # Import neo4j driver
    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("ERROR: neo4j Python package is not installed.")
        print("To install: pip install neo4j")
        return None
    
    driver = None
    try:
        # Establish connection to Neo4j
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("✓ Successfully connected to Neo4j")
        print()
        
        # Execute the Cypher query
        with driver.session() as session:
            result = session.run(cypher_query)
            
            # Collect all orphan node properties
            orphan_nodes = []
            for record in result:
                node_properties = record["node_properties"]
                orphan_nodes.append(node_properties)
            
            # Display results
            print(f"✓ Query executed successfully")
            print(f"✓ Found {len(orphan_nodes)} orphan nodes")
            print("=" * 70)
            
            # Print each orphan node with all its properties
            for idx, properties in enumerate(orphan_nodes, 1):
                print(f"\n[Orphan Node #{idx}]")
                if properties:
                    for key, value in sorted(properties.items()):
                        print(f"  {key}: {value}")
                else:
                    print("  (No properties)")
            
            print("\n" + "=" * 70)
            print(f"Total orphan nodes retrieved: {len(orphan_nodes)}")
            print("=" * 70)
            
            return orphan_nodes
            
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # Always close the connection
        if driver:
            driver.close()
            print("\n✓ Connection closed")


def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("RETRIEVING ALL ORPHAN NODES FROM NEO4J")
    print("=" * 70 + "\n")
    
    orphan_nodes = retrieve_orphan_nodes()
    
    if orphan_nodes is not None:
        print("\n✓ Script completed successfully")
        return 0
    else:
        print("\n✗ Script failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
