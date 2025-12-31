#!/usr/bin/env python3
"""
Direct Atomic Graph Query for Metric Nodes

A simple, standalone script that executes atomic Cypher queries
against a Neo4j graph database to retrieve Metric nodes:
- LoopMetric nodes
- MetricSnapshot nodes

This breaks the verification deadlock by providing direct database inspection.

Usage:
    python direct_metric_query.py
"""

import os
import sys
import json
from datetime import datetime

# Try to import Neo4j driver
NEO4J_AVAILABLE = False
DRIVER_ERROR = None

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError as e:
    DRIVER_ERROR = str(e)
    print(f"[ERROR] Neo4j driver not available: {DRIVER_ERROR}")
    print("[INFO] Install with: pip install neo4j")
    sys.exit(1)

# Load environment variables
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

def query_metric_counts(driver):
    """Query counts of all metric node types."""
    query = """
        MATCH (lm:LoopMetric)
        RETURN count(lm) as loop_metric_count
    """
    
    with driver.session() as session:
        result = session.run(query)
        loop_count = result.single()["loop_metric_count"]
    
    query = """
        MATCH (ms:MetricSnapshot)
        RETURN count(ms) as metric_snapshot_count
    """
    
    with driver.session() as session:
        result = session.run(query)
        snapshot_count = result.single()["metric_snapshot_count"]
    
    return {
        "LoopMetric": loop_count,
        "MetricSnapshot": snapshot_count
    }

def query_loop_metrics(driver, limit=10):
    """Query LoopMetric nodes."""
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
            props = record["props"]
            records.append(props)
    
    return records

def query_metric_snapshots(driver, limit=10):
    """Query MetricSnapshot nodes."""
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
            props = record["props"]
            records.append(props)
    
    return records

def main():
    """Main execution."""
    print("#"*70)
    print("# DIRECT ATOMIC GRAPH QUERY - Metric Nodes")
    print("#"*70)
    print(f"\nExecution time: {datetime.now().isoformat()}")
    
    # Get connection parameters
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    print(f"\n[STEP 1] Connecting to Neo4j...")
    print(f"  URI: {uri}")
    print(f"  User: {user}")
    
    driver = None
    try:
        # Create driver
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("  ✓ Connected successfully")
        
        # Query counts
        print(f"\n[STEP 2] Querying metric node counts...")
        counts = query_metric_counts(driver)
        print(f"  LoopMetric: {counts['LoopMetric']} nodes")
        print(f"  MetricSnapshot: {counts['MetricSnapshot']} nodes")
        
        total = counts['LoopMetric'] + counts['MetricSnapshot']
        
        if total == 0:
            print("\n[WARNING] No metric nodes found in database")
            print("This indicates metrics may not be written yet.")
            return 0
        
        # Query LoopMetric nodes
        print(f"\n[STEP 3] Querying LoopMetric nodes...")
        loop_metrics = query_loop_metrics(driver, limit=10)
        print(f"  Retrieved {len(loop_metrics)} LoopMetric nodes")
        
        if loop_metrics:
            print("\n" + "="*70)
            print("LOOP METRIC NODES (first 10)")
            print("="*70)
            for i, metric in enumerate(loop_metrics, 1):
                print(f"\n[{i}] LoopMetric:")
                for key, value in metric.items():
                    if isinstance(value, str) and len(value) > 100:
                        value = value[:100] + "..."
                    print(f"    {key}: {value}")
        
        # Query MetricSnapshot nodes
        print(f"\n[STEP 4] Querying MetricSnapshot nodes...")
        snapshots = query_metric_snapshots(driver, limit=10)
        print(f"  Retrieved {len(snapshots)} MetricSnapshot nodes")
        
        if snapshots:
            print("\n" + "="*70)
            print("METRIC SNAPSHOT NODES (first 10)")
            print("="*70)
            for i, snapshot in enumerate(snapshots, 1):
                print(f"\n[{i}] MetricSnapshot:")
                for key, value in snapshot.items():
                    if isinstance(value, str) and len(value) > 100:
                        value = value[:100] + "..."
                    print(f"    {key}: {value}")
        
        # Verification summary
        print("\n" + "="*70)
        print("✓✓✓ VERIFICATION DEADLOCK BROKEN ✓✓✓")
        print("="*70)
        print(f"\nSuccessfully queried {total:,} total metric nodes:")
        print(f"  • LoopMetric: {counts['LoopMetric']:,} nodes")
        print(f"  • MetricSnapshot: {counts['MetricSnapshot']:,} nodes")
        print("\nDirect graph query confirms metrics are being written to database.")
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Query failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        if driver:
            driver.close()
            print("\n[OK] Neo4j connection closed")

if __name__ == "__main__":
    sys.exit(main())
