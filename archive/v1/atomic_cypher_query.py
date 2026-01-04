#!/usr/bin/env python3
"""
Atomic Cypher Query Executor - Orphan Nodes

A simple, standalone script that executes a single atomic Cypher query
against a Neo4j graph database to retrieve all orphan nodes (nodes with
no relationships).

Usage:
    python atomic_cypher_query.py
"""

import os
import sys
import traceback
import json
from datetime import datetime
from neo4j import GraphDatabase

# Manually load .env file if dotenv is not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback: read .env manually
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


def execute_atomic_query():
    """
    Execute a single atomic Cypher query.
    
    This function:
    1. Establishes a connection to Neo4j
    2. Executes exactly one Cypher query to find orphan nodes
    3. Closes the connection
    
    Returns:
        List of orphan node properties
    """
    # Neo4j connection parameters
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    # Single atomic Cypher query to execute
    # This query retrieves all orphan nodes (nodes with no relationships)
    # and returns all their properties
    cypher_query = """
        MATCH (n)
        WHERE NOT (n)-[]-()
        RETURN properties(n) AS node_properties
    """
    
    print("=" * 60)
    print("CYPHER QUERY TO EXECUTE:")
    print("=" * 60)
    print(cypher_query.strip())
    print("=" * 60)
    print(f"\nConnecting to Neo4j at: {uri}")
    print(f"User: {user}")
    print()
    
    driver = None
    try:
        # Establish connection
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("✓ Connection established successfully.")
        print()
        
        # Execute the single atomic query
        with driver.session() as session:
            result = session.run(cypher_query)
            
            # Collect all orphan node properties
            orphan_nodes = []
            for record in result:
                orphan_nodes.append(record["node_properties"])
            
            print(f"Query executed successfully.")
            print(f"Found {len(orphan_nodes)} orphan nodes (nodes with no relationships).")
            
            # Print all properties of each orphan node
            for idx, properties in enumerate(orphan_nodes, 1):
                print(f"\n--- Orphan Node {idx} ---")
                print(f"Properties: {properties}")
            
            return orphan_nodes
        
        return None
        
    except Exception as e:
        print(f"\n{'='*60}")
        print("ERROR OCCURRED:")
        print(f"{'='*60}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Message: {e}")
        print(f"\nFull traceback:")
        traceback.print_exc()
        print(f"{'='*60}")
        return None
        
    finally:
        # Always close the connection
        if driver:
            driver.close()


if __name__ == "__main__":
    result = execute_atomic_query()
    if result is not None:
        print(f"\n{'='*60}")
        print("SCRIPT COMPLETED SUCCESSFULLY")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("SCRIPT FAILED")
        print(f"{'='*60}")
        sys.exit(1)
