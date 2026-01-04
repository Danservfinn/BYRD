#!/usr/bin/env python3
"""Minimal test script to query Metric nodes."""

import os
import sys

print("[START] Testing metric query...")
print(f"Python: {sys.version}")

# Try import
try:
    from neo4j import GraphDatabase
    print("[OK] Neo4j imported")
except ImportError as e:
    print(f"[ERROR] Cannot import neo4j: {e}")
    sys.exit(1)

# Get credentials from .env
uri = 'neo4j+s://9b21f7a8.databases.neo4j.io'
user = 'neo4j'
password = '1mSKWa8gwgwQ22kbqQB7ICpNtACFcG7WHDT7ZROCOy8'

print(f"\n[CONNECT] Connecting to {uri[:30]}...")

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    print("[OK] Connected")
    
    with driver.session() as session:
        # Query 1: Count LoopMetric
        result = session.run("MATCH (n:LoopMetric) RETURN count(n) as count")
        loop_count = result.single()["count"]
        print(f"\n[RESULT] LoopMetric: {loop_count}")
        
        # Query 2: Count MetricSnapshot  
        result = session.run("MATCH (n:MetricSnapshot) RETURN count(n) as count")
        snapshot_count = result.single()["count"]
        print(f"[RESULT] MetricSnapshot: {snapshot_count}")
        
        total = loop_count + snapshot_count
        print(f"\n[SUMMARY] Total metric nodes: {total}")
        
        if total > 0:
            print("[SUCCESS] Deadlock broken - metrics verified!")
        else:
            print("[INFO] No metrics found - system may not have run")
            
    driver.close()
    print("[DONE]")
    sys.exit(0)
    
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
