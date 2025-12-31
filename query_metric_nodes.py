#!/usr/bin/env python3
"""
Direct Graph Query for Metric Nodes - Verification Deadlock Break

This script executes direct Cypher queries to retrieve Metric nodes from Neo4j:
- LoopMetric nodes (per-loop metrics)
- MetricSnapshot nodes (point-in-time metrics)

This breaks the verification deadlock by providing direct database inspection
without requiring runtime execution or complex dependency chains.

Usage:
    python query_metric_nodes.py
"""

import os
import sys
import json
from datetime import datetime
from neo4j import GraphDatabase
from typing import Dict, List, Any, Optional

# Load environment variables
def load_env():
    """Load environment variables from .env file."""
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

def query_loop_metrics(driver: GraphDatabase.driver, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Query LoopMetric nodes to verify per-loop metrics are being recorded.
    
    Args:
        driver: Neo4j driver instance
        limit: Maximum number of records to return
        
    Returns:
        List of LoopMetric node data
    """
    query = """
        MATCH (lm:LoopMetric)
        RETURN lm
        ORDER BY lm.timestamp DESC
        LIMIT $limit
    """
    
    with driver.session() as session:
        result = session.run(query, limit=limit)
        records = [dict(r["lm"]) for r in result]
    
    return records

def query_metric_snapshots(driver: GraphDatabase.driver, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Query MetricSnapshot nodes to verify point-in-time metrics are being recorded.
    
    Args:
        driver: Neo4j driver instance
        limit: Maximum number of records to return
        
    Returns:
        List of MetricSnapshot node data
    """
    query = """
        MATCH (ms:MetricSnapshot)
        RETURN ms
        ORDER BY ms.timestamp DESC
        LIMIT $limit
    """
    
    with driver.session() as session:
        result = session.run(query, limit=limit)
        records = [dict(r["ms"]) for r in result]
    
    return records

def get_metric_counts(driver: GraphDatabase.driver) -> Dict[str, int]:
    """
    Get total counts of all metric node types.
    
    Args:
        driver: Neo4j driver instance
        
    Returns:
        Dictionary with node type counts
    """
    counts = {}
    
    # Count LoopMetric nodes
    with driver.session() as session:
        result = session.run("MATCH (lm:LoopMetric) RETURN count(lm) as count")
        counts['LoopMetric'] = result.single()["count"]
    
    # Count MetricSnapshot nodes
    with driver.session() as session:
        result = session.run("MATCH (ms:MetricSnapshot) RETURN count(ms) as count")
        counts['MetricSnapshot'] = result.single()["count"]
    
    return counts

def display_loop_metrics(metrics: List[Dict[str, Any]]) -> None:
    """
    Display LoopMetric records in a readable format.
    
    Args:
        metrics: List of LoopMetric dictionaries
    """
    print("\n" + "="*70)
    print("LOOP METRIC NODES")
    print("="*70)
    
    if not metrics:
        print("  ✗ No LoopMetric nodes found")
        return
    
    for i, metric in enumerate(metrics, 1):
        print(f"\n[{i}] {metric.get('id', 'unknown')}")
        print(f"    Loop: {metric.get('loop_name', 'unknown')}")
        print(f"    Cycle: {metric.get('cycle_number', 'unknown')}")
        print(f"    Mode: {metric.get('mode', 'unknown')}")
        print(f"    Timestamp: {metric.get('timestamp', 'unknown')}")
        
        # Parse and display metrics JSON
        metrics_json = metric.get('metrics', '{}')
        try:
            metrics_data = json.loads(metrics_json) if isinstance(metrics_json, str) else metrics_json
            print(f"    Metrics Keys: {list(metrics_data.keys())}")
        except Exception as e:
            print(f"    Metrics: {str(metrics_json)[:100]}...")

def display_metric_snapshots(snapshots: List[Dict[str, Any]]) -> None:
    """
    Display MetricSnapshot records in a readable format.
    
    Args:
        snapshots: List of MetricSnapshot dictionaries
    """
    print("\n" + "="*70)
    print("METRIC SNAPSHOT NODES")
    print("="*70)
    
    if not snapshots:
        print("  ✗ No MetricSnapshot nodes found")
        return
    
    for i, snapshot in enumerate(snapshots, 1):
        print(f"\n[{i}] {snapshot.get('id', 'unknown')}")
        print(f"    Capability Score: {snapshot.get('capability_score', 'unknown')}")
        print(f"    LLM Efficiency: {snapshot.get('llm_efficiency', 'unknown')}")
        print(f"    Growth Rate: {snapshot.get('growth_rate', 'unknown')}")
        print(f"    Coupling Correlation: {snapshot.get('coupling_correlation', 'unknown')}")
        print(f"    Timestamp: {snapshot.get('timestamp', 'unknown')}")
        
        # Parse and display loop health
        loop_health = snapshot.get('loop_health', '{}')
        try:
            health_data = json.loads(loop_health) if isinstance(loop_health, str) else loop_health
            print(f"    Loop Health: {health_data}")
        except Exception as e:
            print(f"    Loop Health: {str(loop_health)[:100]}...")

def display_counts(counts: Dict[str, int]) -> None:
    """
    Display metric node counts.
    
    Args:
        counts: Dictionary with node type counts
    """
    print("\n" + "="*70)
    print("METRIC NODE COUNTS")
    print("="*70)
    
    for node_type, count in counts.items():
        status = "✓" if count > 0 else "✗"
        print(f"  {status} {node_type}: {count}")

def main():
    """
    Main execution function.
    
    This breaks the verification deadlock by:
    1. Directly connecting to Neo4j
    2. Executing atomic queries for Metric nodes
    3. Displaying results for immediate verification
    4. No runtime dependencies, no complex chains
    """
    print("\n" + "#"*70)
    print("# DIRECT GRAPH QUERY - Metric Nodes Verification")
    print("#"*70)
    print("\nBreaking verification deadlock with direct database inspection...")
    
    # Load environment
    load_env()
    
    # Neo4j connection parameters
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    print(f"\nConnecting to Neo4j: {uri}")
    
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("✓ Connection established")
        
        # Query metric node counts
        print("\n[QUERY] Fetching metric node counts...")
        counts = get_metric_counts(driver)
        display_counts(counts)
        
        # Query LoopMetric nodes
        print("\n[QUERY] Fetching LoopMetric nodes...")
        loop_metrics = query_loop_metrics(driver, limit=10)
        display_loop_metrics(loop_metrics)
        
        # Query MetricSnapshot nodes
        print("\n[QUERY] Fetching MetricSnapshot nodes...")
        metric_snapshots = query_metric_snapshots(driver, limit=10)
        display_metric_snapshots(metric_snapshots)
        
        # Verification summary
        print("\n" + "="*70)
        print("VERIFICATION SUMMARY")
        print("="*70)
        
        total_metrics = counts.get('LoopMetric', 0) + counts.get('MetricSnapshot', 0)
        
        if total_metrics > 0:
            print(f"✓✓✓ VERIFICATION DEADLOCK BROKEN ✓✓✓")
            print(f"\nFound {total_metrics} metric nodes in database:")
            print(f"  - LoopMetric: {counts.get('LoopMetric', 0)} nodes")
            print(f"  - MetricSnapshot: {counts.get('MetricSnapshot', 0)} nodes")
            print("\nDirect graph query confirms metrics are being written.")
            return 0
        else:
            print("✗ VERIFICATION FAILED")
            print("\nNo metric nodes found in database.")
            print("This indicates metrics may not be written yet or connection issue.")
            return 1
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        traceback.print_exc()
        return 1
    
    finally:
        if driver:
            driver.close()
            print("\n✓ Connection closed")

if __name__ == "__main__":
    import traceback
    sys.exit(main())
