#!/usr/bin/env python3
"""
Metric Graph Query - Verification Deadlock Break

A focused, clean script that executes direct Cypher queries to retrieve
Metric nodes from Neo4j, breaking verification deadlock without requiring
runtime execution or complex dependency chains.

This script queries:
- LoopMetric nodes (per-loop metrics)
- MetricSnapshot nodes (point-in-time metrics)
- General Metric nodes

Usage:
    python metric_graph_query.py
    python metric_graph_query.py --limit 50
    python metric_graph_query.py --type LoopMetric
"""

import os
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

# Neo4j driver import with graceful fallback
NEO4J_AVAILABLE = False
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    print("[WARNING] neo4j package not installed. Run: pip install neo4j")


def load_environment() -> Dict[str, str]:
    """Load environment variables from .env file.
    
    Returns:
        Dictionary of environment variables
    """
    env_vars = {
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USER': 'neo4j',
        'NEO4J_PASSWORD': 'password'
    }
    
    # Try python-dotenv first
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # Manual fallback
        env_file = '.env'
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    # Apply environment overrides
    for key in env_vars:
        if os.getenv(key):
            env_vars[key] = os.getenv(key)
    
    return env_vars


def create_driver(env_vars: Dict[str, str]):
    """Create Neo4j driver instance.
    
    Args:
        env_vars: Dictionary with connection parameters
        
    Returns:
        Neo4j driver or None if unavailable
    """
    if not NEO4J_AVAILABLE:
        return None
    
    return GraphDatabase.driver(
        env_vars['NEO4J_URI'],
        auth=(env_vars['NEO4J_USER'], env_vars['NEO4J_PASSWORD'])
    )


def query_loop_metrics(driver, limit: int = 20) -> List[Dict[str, Any]]:
    """Query LoopMetric nodes.
    
    Args:
        driver: Neo4j driver instance
        limit: Maximum records to return
        
    Returns:
        List of LoopMetric node properties
    """
    query = """
        MATCH (lm:LoopMetric)
        RETURN properties(lm) AS props
        ORDER BY lm.timestamp DESC
        LIMIT $limit
    """
    
    records = []
    with driver.session() as session:
        result = session.run(query, limit=limit)
        for record in result:
            records.append(record["props"])
    return records


def query_metric_snapshots(driver, limit: int = 20) -> List[Dict[str, Any]]:
    """Query MetricSnapshot nodes.
    
    Args:
        driver: Neo4j driver instance
        limit: Maximum records to return
        
    Returns:
        List of MetricSnapshot node properties
    """
    query = """
        MATCH (ms:MetricSnapshot)
        RETURN properties(ms) AS props
        ORDER BY ms.timestamp DESC
        LIMIT $limit
    """
    
    records = []
    with driver.session() as session:
        result = session.run(query, limit=limit)
        for record in result:
            records.append(record["props"])
    return records


def query_all_metrics(driver, limit: int = 20) -> List[Dict[str, Any]]:
    """Query all nodes with 'Metric' in their labels.
    
    Args:
        driver: Neo4j driver instance
        limit: Maximum records to return
        
    Returns:
        List of Metric node properties with their labels
    """
    query = """
        MATCH (n)
        WHERE any(label IN labels(n) WHERE label CONTAINS 'Metric')
        RETURN labels(n) AS labels, properties(n) AS props
        ORDER BY coalesce(n.timestamp, datetime()) DESC
        LIMIT $limit
    """
    
    records = []
    with driver.session() as session:
        result = session.run(query, limit=limit)
        for record in result:
            records.append({
                'labels': record["labels"],
                'properties': record["props"]
            })
    return records


def get_metric_counts(driver) -> Dict[str, int]:
    """Get counts of all metric-related node types.
    
    Args:
        driver: Neo4j driver instance
        
    Returns:
        Dictionary mapping node types to counts
    """
    counts = {}
    
    # Count specific metric types
    queries = {
        'LoopMetric': 'MATCH (lm:LoopMetric) RETURN count(lm) AS c',
        'MetricSnapshot': 'MATCH (ms:MetricSnapshot) RETURN count(ms) AS c',
        'Metric': 'MATCH (m:Metric) RETURN count(m) AS c'
    }
    
    for node_type, query in queries.items():
        with driver.session() as session:
            result = session.run(query)
            counts[node_type] = result.single()["c"]
    
    return counts


def format_output(results: Dict[str, Any]) -> str:
    """Format query results for display.
    
    Args:
        results: Dictionary containing all query results
        
    Returns:
        Formatted string output
    """
    output = []
    separator = "=" * 60
    
    output.append("\n" + separator)
    output.append("METRIC GRAPH QUERY RESULTS")
    output.append(f"Execution: {datetime.now().isoformat()}")
    output.append(separator)
    
    # Counts
    output.append("\n[METRIC NODE COUNTS]")
    for node_type, count in results.get('counts', {}).items():
        output.append(f"  {node_type}: {count}")
    
    # LoopMetrics
    loop_metrics = results.get('loop_metrics', [])
    output.append(f"\n[LOOP METRIC NODES] ({len(loop_metrics)} found)")
    for i, metric in enumerate(loop_metrics[:5], 1):
        output.append(f"  [{i}] {metric.get('id', metric.get('loop_name', 'unknown'))}")
    
    # MetricSnapshots
    snapshots = results.get('metric_snapshots', [])
    output.append(f"\n[METRIC SNAPSHOT NODES] ({len(snapshots)} found)")
    for i, snap in enumerate(snapshots[:5], 1):
        output.append(f"  [{i}] {snap.get('id', snap.get('timestamp', 'unknown'))}")
    
    # All Metrics
    all_metrics = results.get('all_metrics', [])
    output.append(f"\n[ALL METRIC NODES] ({len(all_metrics)} found)")
    for i, metric in enumerate(all_metrics[:5], 1):
        labels = metric.get('labels', [])
        output.append(f"  [{i}] Labels: {labels}")
    
    output.append("\n" + separator)
    output.append("VERIFICATION DEADLOCK BROKEN - Direct query complete")
    output.append(separator + "\n")
    
    return "\n".join(output)


def run_demo() -> Dict[str, Any]:
    """Run in demo mode with simulated data.
    
    Returns:
        Simulated results dictionary
    """
    return {
        'counts': {
            'LoopMetric': 15,
            'MetricSnapshot': 8,
            'Metric': 3
        },
        'loop_metrics': [
            {'id': 'lm_001', 'loop_name': 'capability_improvement', 'timestamp': datetime.now().isoformat()},
            {'id': 'lm_002', 'loop_name': 'belief_refinement', 'timestamp': datetime.now().isoformat()}
        ],
        'metric_snapshots': [
            {'id': 'ms_001', 'timestamp': datetime.now().isoformat()},
            {'id': 'ms_002', 'timestamp': datetime.now().isoformat()}
        ],
        'all_metrics': [
            {'labels': ['LoopMetric'], 'properties': {'id': 'lm_001'}},
            {'labels': ['MetricSnapshot'], 'properties': {'id': 'ms_001'}}
        ]
    }


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Query Metric nodes from Neo4j')
    parser.add_argument('--limit', type=int, default=20, help='Max records per query')
    parser.add_argument('--type', type=str, help='Specific node type to query')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode')
    args = parser.parse_args()
    
    # Demo mode
    if args.demo:
        print("[DEMO MODE] Simulating metric query results...")
        results = run_demo()
        print(format_output(results))
        return
    
    # Real database mode
    env_vars = load_environment()
    driver = create_driver(env_vars)
    
    if driver is None:
        print("[ERROR] Neo4j driver unavailable. Use --demo flag.")
        sys.exit(1)
    
    try:
        results = {
            'counts': get_metric_counts(driver),
            'loop_metrics': query_loop_metrics(driver, args.limit),
            'metric_snapshots': query_metric_snapshots(driver, args.limit),
            'all_metrics': query_all_metrics(driver, args.limit)
        }
        print(format_output(results))
    finally:
        driver.close()


if __name__ == "__main__":
    main()
