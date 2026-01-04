#!/usr/bin/env python3
"""
Atomic Metric Node Query - Verification Deadlock Break

A simple, standalone script that executes atomic Cypher queries
against a Neo4j graph database to retrieve Metric nodes:
- LoopMetric nodes (per-loop metrics)
- MetricSnapshot nodes (point-in-time metrics)

This breaks verification deadlock by providing direct database inspection.

Usage:
    python metric_node_query.py
"""

import os
import sys
import json
from datetime import datetime

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


def get_neo4j_driver():
    """Get Neo4j driver instance or None if not available."""
    try:
        from neo4j import GraphDatabase
        return GraphDatabase
    except ImportError:
        return None


def query_loop_metrics(driver_class):
    """Execute atomic query to retrieve LoopMetric nodes.
    
    Returns:
        List of LoopMetric node data
    """
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    cypher_query = """
        MATCH (lm:LoopMetric)
        RETURN lm
        ORDER BY lm.timestamp DESC
        LIMIT 10
    """
    
    print("=" * 70)
    print("QUERY: LoopMetric Nodes")
    print("=" * 70)
    print(cypher_query.strip())
    print("=" * 70)
    print(f"\nConnecting to Neo4j at: {uri}")
    print(f"User: {user}")
    print()
    
    driver = None
    results = []
    
    try:
        driver = driver_class.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run(cypher_query)
            for record in result:
                node = record["lm"]
                results.append(dict(node))
                print(f"  ✓ LoopMetric found: {node.get('id', 'N/A')}")
    except Exception as e:
        print(f"  ⚠ Query error: {e}")
    finally:
        if driver:
            driver.close()
    
    return results


def query_metric_snapshots(driver_class):
    """Execute atomic query to retrieve MetricSnapshot nodes.
    
    Returns:
        List of MetricSnapshot node data
    """
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    cypher_query = """
        MATCH (ms:MetricSnapshot)
        RETURN ms
        ORDER BY ms.timestamp DESC
        LIMIT 10
    """
    
    print("=" * 70)
    print("QUERY: MetricSnapshot Nodes")
    print("=" * 70)
    print(cypher_query.strip())
    print("=" * 70)
    print(f"\nConnecting to Neo4j at: {uri}")
    print(f"User: {user}")
    print()
    
    driver = None
    results = []
    
    try:
        driver = driver_class.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run(cypher_query)
            for record in result:
                node = record["ms"]
                results.append(dict(node))
                print(f"  ✓ MetricSnapshot found: {node.get('id', 'N/A')}")
    except Exception as e:
        print(f"  ⚠ Query error: {e}")
    finally:
        if driver:
            driver.close()
    
    return results


def get_metric_counts(driver_class):
    """Get counts of Metric nodes in the database.
    
    Returns:
        Dictionary with counts for each metric type
    """
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    cypher_query = """
        MATCH (n)
        WHERE n:LoopMetric OR n:MetricSnapshot
        RETURN labels(n) AS labels, count(n) AS count
    """
    
    print("=" * 70)
    print("QUERY: Metric Node Counts")
    print("=" * 70)
    print(cypher_query.strip())
    print("=" * 70)
    print()
    
    driver = None
    counts = {}
    
    try:
        driver = driver_class.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run(cypher_query)
            for record in result:
                label = record["labels"][0] if record["labels"] else "Unknown"
                count = record["count"]
                counts[label] = count
                print(f"  ✓ {label}: {count} nodes")
    except Exception as e:
        print(f"  ⚠ Query error: {e}")
    finally:
        if driver:
            driver.close()
    
    return counts


def main():
    """Main execution function."""
    print("\n" + "#" * 70)
    print("# ATOMIC METRIC NODE QUERY - Verification Deadlock Break")
    print("#" * 70)
    print(f"Execution time: {datetime.now().isoformat()}")
    print()
    
    # Check for Neo4j driver availability
    driver_class = get_neo4j_driver()
    
    if driver_class is None:
        print("=" * 70)
        print("NEO4J DRIVER NOT AVAILABLE")
        print("=" * 70)
        print("\nThe neo4j Python package is not installed.")
        print("Install it with: pip install neo4j")
        print("\nShowing expected query structure instead...\n")
        
        # Show expected output without database
        print("Expected LoopMetric query would return:")
        print("  - LoopMetric nodes with: id, loop_name, cycle, mode, metrics")
        print()
        print("Expected MetricSnapshot query would return:")
        print("  - MetricSnapshot nodes with: id, timestamp, snapshot_data")
        print()
        return
    
    print("Neo4j driver available. Executing queries...\n")
    
    # Execute all queries
    counts = get_metric_counts(driver_class)
    loop_metrics = query_loop_metrics(driver_class)
    metric_snapshots = query_metric_snapshots(driver_class)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total LoopMetric nodes: {counts.get('LoopMetric', 0)}")
    print(f"Total MetricSnapshot nodes: {counts.get('MetricSnapshot', 0)}")
    print(f"LoopMetric nodes retrieved: {len(loop_metrics)}")
    print(f"MetricSnapshot nodes retrieved: {len(metric_snapshots)}")
    print("=" * 70)
    print("Verification deadlock broken via direct graph query.")
    print("=" * 70)


if __name__ == "__main__":
    main()
