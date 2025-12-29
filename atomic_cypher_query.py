#!/usr/bin/env python3
"""
Atomic Cypher Query Executor

A simple, standalone script that executes a single atomic Cypher query
against a Neo4j graph database without any surrounding strategy or complexity.

Usage:
    python atomic_cypher_query.py
"""

import os
from neo4j import GraphDatabase


def execute_atomic_query():
    """
    Execute a single atomic Cypher query.
    
    This function:
    1. Establishes a connection to Neo4j
    2. Executes exactly one Cypher query
    3. Closes the connection
    
    Returns:
        The query result summary
    """
    # Neo4j connection parameters
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    # Single atomic Cypher query to execute
    # This query counts all nodes in the database
    cypher_query = """
        MATCH (n)
        RETURN count(n) AS total_nodes
    """
    
    driver = None
    try:
        # Establish connection
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        # Execute the single atomic query
        with driver.session() as session:
            result = session.run(cypher_query)
            record = result.single()
            
            if record:
                total_nodes = record["total_nodes"]
                print(f"Query executed successfully.")
                print(f"Total nodes in database: {total_nodes}")
                return total_nodes
            
        return None
        
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
        
    finally:
        # Always close the connection
        if driver:
            driver.close()


if __name__ == "__main__":
    execute_atomic_query()
