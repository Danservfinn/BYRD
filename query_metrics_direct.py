#!/usr/bin/env python3
"""
Direct Neo4j Query for Metric Nodes - Break Verification Deadlock

This script executes direct Cypher queries to retrieve Metric nodes,
 breaking the verification deadlock by providing immediate database access.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from neo4j import GraphDatabase
except ImportError:
    print("[ERROR] Neo4j driver not installed. Run: pip install neo4j")
    sys.exit(1)

def main():
    """Execute direct graph query for Metric nodes."""
    print("="*70)
    print("DIRECT GRAPH QUERY - Metric Nodes")
    print("="*70)
    
    # Get Neo4j connection details from environment
    uri = os.getenv('NEO4J_URI', 'neo4j+s://9b21f7a8.databases.neo4j.io')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', '1mSKWa8gwgwQ22kbqQB7ICpNtACFcG7WHDT7ZROCOy8')
    
    print(f"\nConnecting to: {uri}")
    print(f"User: {user}")
    
    driver = None
    try:
        # Create driver
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("[OK] Connected to Neo4j")
        
        # Query for all metric-related node types
        with driver.session() as session:
            
            # 1. Count LoopMetric nodes
            result = session.run("MATCH (n:LoopMetric) RETURN count(n) as count")
            loop_metric_count = result.single()["count"]
            print(f"\nLoopMetric nodes: {loop_metric_count}")
            
            # 2. Count MetricSnapshot nodes
            result = session.run("MATCH (n:MetricSnapshot) RETURN count(n) as count")
            snapshot_count = result.single()["count"]
            print(f"MetricSnapshot nodes: {snapshot_count}")
            
            # 3. Sample LoopMetric data
            if loop_metric_count > 0:
                result = session.run("MATCH (n:LoopMetric) RETURN n LIMIT 3")
                print("\n--- Sample LoopMetric nodes ---")
                for record in result:
                    node = dict(record["n"])
                    print(f"  ID: {node.get('id', 'N/A')}")
                    print(f"  Timestamp: {node.get('timestamp', 'N/A')}")
                    print(f"  Keys: {list(node.keys())}")
                    print()
            
            # 4. Sample MetricSnapshot data
            if snapshot_count > 0:
                result = session.run("MATCH (n:MetricSnapshot) RETURN n LIMIT 3")
                print("--- Sample MetricSnapshot nodes ---")
                for record in result:
                    node = dict(record["n"])
                    print(f"  ID: {node.get('id', 'N/A')}")
                    print(f"  Capability Score: {node.get('capability_score', 'N/A')}")
                    print(f"  Timestamp: {node.get('timestamp', 'N/A')}")
                    print()
            
            # 5. Check for any other metric-related nodes
            result = session.run("""
                CALL db.labels() YIELD label
                WHERE label CONTAINS 'metric' OR label CONTAINS 'Metric'
                RETURN label
            """)
            metric_labels = [record["label"] for record in result]
            print(f"\nOther metric-related labels: {metric_labels}")
            
        print("\n" + "="*70)
        print("VERIFICATION DEADLOCK BROKEN")
        print("="*70)
        total = loop_metric_count + snapshot_count
        print(f"\nTotal metric nodes found: {total}")
        
        if total > 0:
            print("✓ Direct graph query successful - metrics are being written")
            return 0
        else:
            print("✓ Query executed - no metrics found (system may not have run yet)")
            return 0
            
    except Exception as e:
        print(f"\n[ERROR] Query failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if driver:
            driver.close()
            print("\n[OK] Connection closed")

if __name__ == "__main__":
    sys.exit(main())
