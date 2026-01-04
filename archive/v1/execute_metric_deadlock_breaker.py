#!/usr/bin/env python3
"""
Metric Node Verification Deadlock Breaker

A simple, standalone script that executes a direct Cypher query against
a Neo4j graph database to retrieve all Metric nodes, breaking any
verification deadlock.

This script specifically targets:
- LoopMetric nodes
- MetricSnapshot nodes
- Any nodes with labels containing 'metric'

Usage:
    python execute_metric_deadlock_breaker.py
"""

import os
import sys
import json
from datetime import datetime

# Try to import neo4j driver
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

# Try to load .env with dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def load_env():
    """
    Load environment variables from .env file or system environment.
    
    Returns:
        tuple: (uri, user, password)
    """
    # Read .env file manually if dotenv wasn't available
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'password')
    
    return uri, user, password


def execute_metric_query():
    """
    Execute direct Cypher query to find all Metric nodes.
    
    This is the atomic operation that breaks the verification deadlock
    by directly querying the graph database for Metric nodes.
    
    Returns:
        dict: Results containing counts, samples, and status
    """
    if not NEO4J_AVAILABLE:
        return {
            "status": "error",
            "error": "Neo4j driver not installed. Install with: pip install neo4j",
            "loop_metric_count": 0,
            "metric_snapshot_count": 0,
            "total_count": 0,
            "samples": [],
            "labels": []
        }
    
    uri, user, password = load_env()
    
    results = {
        "status": "pending",
        "loop_metric_count": 0,
        "metric_snapshot_count": 0,
        "total_count": 0,
        "samples": [],
        "labels": [],
        "timestamp": datetime.now().isoformat()
    }
    
    driver = None
    
    print("=" * 70)
    print("METRIC NODE VERIFICATION DEADLOCK BREAKER")
    print("=" * 70)
    print(f"\nConnecting to Neo4j at: {uri}")
    print(f"User: {user}")
    print()
    
    try:
        # Establish connection
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("[OK] Connection established")
        
        with driver.session() as session:
            # STEP 1: Count LoopMetric nodes
            print("\n[STEP 1] Querying LoopMetric nodes...")
            result = session.run("""
                MATCH (n:LoopMetric)
                RETURN count(n) as count
            """)
            loop_count = result.single()["count"]
            results["loop_metric_count"] = loop_count
            print(f"[RESULT] LoopMetric nodes: {loop_count:,}")
            
            # STEP 2: Count MetricSnapshot nodes
            print("\n[STEP 2] Querying MetricSnapshot nodes...")
            result = session.run("""
                MATCH (n:MetricSnapshot)
                RETURN count(n) as count
            """)
            snapshot_count = result.single()["count"]
            results["metric_snapshot_count"] = snapshot_count
            print(f"[RESULT] MetricSnapshot nodes: {snapshot_count:,}")
            
            total = loop_count + snapshot_count
            results["total_count"] = total
            
            # STEP 3: Sample nodes if any exist
            if total > 0:
                print("\n[STEP 3] Sampling metric nodes...")
                
                # Sample LoopMetric
                if loop_count > 0:
                    result = session.run("""
                        MATCH (n:LoopMetric)
                        RETURN properties(n) as props
                        LIMIT 2
                    """)
                    for record in result:
                        props = record["props"]
                        sample = {
                            "type": "LoopMetric",
                            "id": props.get("id", "N/A")[:50],
                            "timestamp": props.get("timestamp", "N/A"),
                            "metric_count": len(props)
                        }
                        results["samples"].append(sample)
                        print(f"  [Sample] LoopMetric: {sample['id']}...")
                
                # Sample MetricSnapshot
                if snapshot_count > 0:
                    result = session.run("""
                        MATCH (n:MetricSnapshot)
                        RETURN properties(n) as props
                        LIMIT 2
                    """)
                    for record in result:
                        props = record["props"]
                        sample = {
                            "type": "MetricSnapshot",
                            "id": props.get("id", "N/A")[:50],
                            "capability_score": props.get("capability_score", "N/A"),
                            "timestamp": props.get("timestamp", "N/A")
                        }
                        results["samples"].append(sample)
                        print(f"  [Sample] MetricSnapshot: {sample['id']}...")
            
            # STEP 4: Find all metric-related labels
            print("\n[STEP 4] Finding all metric-related labels...")
            result = session.run("""
                CALL db.labels() YIELD label
                WHERE toLower(label) CONTAINS 'metric'
                RETURN label
            """)
            labels = [r["label"] for r in result]
            results["labels"] = labels
            if labels:
                print(f"[RESULT] Found {len(labels)} metric-related labels: {', '.join(labels)}")
            else:
                print("[RESULT] No metric-related labels found")
            
            # Success
            results["status"] = "success"
            print("\n[SUCCESS] Metric node query completed successfully")
            
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"\n[ERROR] {error_msg}")
        results["status"] = "error"
        results["error"] = error_msg
        
    finally:
        if driver:
            driver.close()
            print("\n[OK] Connection closed")
    
    return results


def print_summary(results):
    """
    Print a formatted summary of the query results.
    
    Args:
        results: Dictionary containing query results
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if results["status"] == "error":
        print(f"\n❌ QUERY FAILED")
        print(f"Error: {results.get('error', 'Unknown error')}")
        print("\nPossible causes:")
        print("  - Neo4j database not running")
        print("  - Incorrect credentials in .env file")
        print("  - Network connectivity issue")
        print("  - Neo4j driver not installed")
        return 1
    
    print(f"\n✓ DEADLOCK BROKEN - Metric nodes verified")
    print(f"\nTotal Metric nodes found: {results['total_count']:,}")
    print(f"  - LoopMetric: {results['loop_metric_count']:,}")
    print(f"  - MetricSnapshot: {results['metric_snapshot_count']:,}")
    
    if results["samples"]:
        print(f"\nSampled {len(results['samples'])} nodes:")
        for i, sample in enumerate(results["samples"], 1):
            print(f"  {i}. {sample['type']}: {sample['id']}")
    
    if results["labels"]:
        print(f"\nMetric-related labels: {', '.join(results['labels'])}")
    
    print(f"\nTimestamp: {results['timestamp']}")
    print("\n" + "=" * 70)
    print("✓ VERIFICATION DEADLOCK SUCCESSFULLY BROKEN")
    print("=" * 70)
    
    return 0


def main():
    """
    Main entry point for the script.
    """
    results = execute_metric_query()
    exit_code = print_summary(results)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
