#!/usr/bin/env python3
"""
Cypher Query for Orphan Nodes

This script contains the Cypher query to retrieve all properties of orphan nodes
(nodes with no relationships).

The Query:
    MATCH (n)
    WHERE NOT (n)-[]-()
    RETURN properties(n) AS node_properties

Explanation:
    - MATCH (n): Find all nodes in the database
    - WHERE NOT (n)-[]-(): Filter to only nodes with NO relationships (incoming or outgoing)
    - RETURN properties(n): Return ALL properties of each orphan node

Usage:
    This query can be executed in:
    1. Neo4j Browser (at http://localhost:7474)
    2. Via Neo4j Python driver (see execute_query() function below)
    3. Via cypher-shell command line tool

Note: To execute this query, you need a running Neo4j database instance.
"""

# The Cypher Query
CYPHER_QUERY = """
MATCH (n)
WHERE NOT (n)-[]-()
RETURN properties(n) AS node_properties
"""

def print_query_info():
    """Print information about the Cypher query."""
    print("="*70)
    print("CYPHER QUERY TO RETRIEVE ALL PROPERTIES OF ORPHAN NODES")
    print("="*70)
    print()
    print("Query:")
    print("-"*70)
    print(CYPHER_QUERY.strip())
    print("-"*70)
    print()
    print("Explanation:")
    print("  • MATCH (n)                - Find all nodes in the database")
    print("  • WHERE NOT (n)-[]-()     - Keep only nodes with NO relationships")
    print("  • RETURN properties(n)    - Return ALL properties of each node")
    print()
    print("Expected Output:")
    print("  • Returns a list of property dictionaries, one per orphan node")
    print("  • Each dictionary contains ALL properties of that node")
    print("  • If there are 50 orphan nodes, you'll get 50 property sets")
    print()
    print("="*70)
    print()

def execute_query_with_driver(uri="bolt://localhost:7687", user="neo4j", password="password"):
    """
    Execute the query using Neo4j Python driver.
    
    Requires: pip install neo4j
    Requires: A running Neo4j database instance
    
    Args:
        uri: Neo4j connection URI
        user: Neo4j username
        password: Neo4j password
    
    Returns:
        List of orphan node properties (dictionaries)
    """
    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("ERROR: neo4j Python driver not installed.")
        print("Install with: pip install neo4j")
        return None
    
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        
        with driver.session() as session:
            result = session.run(CYPHER_QUERY.strip())
            
            orphan_nodes = [record["node_properties"] for record in result]
            
            print(f"\n{'='*70}")
            print(f"QUERY EXECUTION RESULTS")
            print(f"{'='*70}")
            print(f"Total orphan nodes found: {len(orphan_nodes)}")
            print(f"{'='*70}\n")
            
            for idx, properties in enumerate(orphan_nodes, 1):
                print(f"--- Orphan Node {idx} ---")
                for key, value in properties.items():
                    print(f"  {key}: {value}")
                print()
            
            return orphan_nodes
            
    except Exception as e:
        print(f"ERROR: Could not connect to Neo4j database")
        print(f"Details: {e}")
        print("\nPlease ensure:")
        print("  1. Neo4j is running (accessible at the URI)")
        print("  2. Username and password are correct")
        print("  3. Network connectivity is available")
        return None
        
    finally:
        if driver:
            driver.close()


if __name__ == "__main__":
    print_query_info()
    
    print("To execute this query against a real Neo4j database:")
    print("1. Ensure Neo4j is running")
    print("2. Set your connection details in .env or pass as arguments")
    print("3. Run: python orphan_nodes_cypher_query.py --execute")
    print()
    
    import sys
    if "--execute" in sys.argv:
        # Try to load from .env if available
        import os
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        
        execute_query_with_driver(uri, user, password)
