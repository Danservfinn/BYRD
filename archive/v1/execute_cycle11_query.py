#!/usr/bin/env python3
"""
CYCLE 11 DIRECT CODE QUERY

This executes the validated Cycle 11 pattern:
- Direct code query (no desires, no runtime execution)
- File content reading for verification
- Breaking verification deadlock with direct inspection

Based on validated pattern from verify_deadlock_simple.py
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
import json

def direct_file_query(filepath: str, pattern: str, extract_group: int = 1) -> List[Any]:
    """
Direct code query - read file, find pattern, extract values.
    No runtime execution, no desires - just direct inspection.
    """
    try:
        content = Path(filepath).read_text()
        matches = re.findall(pattern, content)
        return matches
    except Exception as e:
        print(f"  ✗ ERROR reading {filepath}: {e}")
        return []

def query_verification_config() -> Dict[str, Dict]:
    """
Query all verification-related configurations directly from code.
    This is the Cycle 11 pattern - direct inspection vs runtime.
    """
    results = {}
    
    print("\n" + "="*60)
    print("CYCLE 11: DIRECT CODE QUERY - Verification Deadlock Break")
    print("="*60)
    
    # Query memory.py config
    print("\n[QUERY] memory.py - CONNECTION_HEURISTIC_CONFIG")
    matches = direct_file_query(
        "memory.py", 
        r'"max_connections_per_run"\s*:\s*(\d+)'
    )
    max_conn = int(matches[0]) if matches else None
    print(f"  max_connections_per_run: {max_conn}")
    
    matches = direct_file_query(
        "memory.py",
        r'"similarity_threshold"\s*:\s*([0-9.]+)'
    )
    sim_thresh = float(matches[0]) if matches else None
    print(f"  similarity_threshold: {sim_thresh}")
    
    results['memory'] = {
        'max_connections_per_run': max_conn,
        'similarity_threshold': sim_thresh
    }
    
    # Query seeker.py config
    print("\n[QUERY] seeker.py - batch processing")
    matches = direct_file_query(
        "seeker.py",
        r'batch_size\s*=\s*(\d+)'
    )
    batch_size = int(matches[0]) if matches else None
    print(f"  batch_size: {batch_size}")
    
    matches = direct_file_query(
        "seeker.py",
        r'max_retries\s*=\s*(\d+)'
    )
    max_retries = int(matches[0]) if matches else None
    print(f"  max_retries: {max_retries}")
    
    results['seeker'] = {
        'batch_size': batch_size,
        'max_retries': max_retries
    }
    
    # Query reconcile_orphans.py
    print("\n[QUERY] reconcile_orphans.py - orphan processing")
    matches = direct_file_query(
        "reconcile_orphans.py",
        r'MAX_CONNECTIONS\s*=\s*(\d+)'
    )
    max_conn_recon = int(matches[0]) if matches else None
    print(f"  MAX_CONNECTIONS: {max_conn_recon}")
    
    results['reconcile'] = {
        'MAX_CONNECTIONS': max_conn_recon
    }
    
    return results

def verify_deadlock_break(results: Dict) -> bool:
    """
Verify that deadlock-breaking values are in place.
    Direct verification without runtime.
    """
    print("\n" + "="*60)
    print("VERIFICATION: Deadlock Break Values")
    print("="*60)
    
    all_pass = True
    
    # Check memory.py
    if 'memory' in results:
        mem = results['memory']
        if mem.get('max_connections_per_run', 0) >= 200:
            print("  ✓ PASS: max_connections_per_run >= 200")
        else:
            print(f"  ✗ FAIL: max_connections_per_run = {mem.get('max_connections_per_run')}")
            all_pass = False
        
        if mem.get('similarity_threshold', 1) <= 0.05:
            print("  ✓ PASS: similarity_threshold <= 0.05")
        else:
            print(f"  ✗ FAIL: similarity_threshold = {mem.get('similarity_threshold')}")
            all_pass = False
    
    # Check seeker.py
    if 'seeker' in results:
        seek = results['seeker']
        if seek.get('batch_size', 0) >= 20:
            print("  ✓ PASS: batch_size >= 20")
        else:
            print(f"  ✗ FAIL: batch_size = {seek.get('batch_size')}")
            all_pass = False
        
        if seek.get('max_retries', 0) >= 15:
            print("  ✓ PASS: max_retries >= 15")
        else:
            print(f"  ✗ FAIL: max_retries = {seek.get('max_retries')}")
            all_pass = False
    
    return all_pass

def main():
    """
 Execute Cycle 11 direct code query.
    Break verification deadlock by querying code directly.
    """
    # Step 1: Direct query
    results = query_verification_config()
    
    # Step 2: Verify
    all_pass = verify_deadlock_break(results)
    
    # Step 3: Summary
    print("\n" + "="*60)
    print("CYCLE 11 QUERY SUMMARY")
    print("="*60)
    
    if all_pass:
        print("\n✓✓✓ VERIFICATION DEADLOCK BROKEN ✓✓✓")
        print("\nMethod: Direct code query (Cycle 11 pattern)")
        print("Result: All deadlock-breaking values confirmed")
        print("\nNo desires created. No runtime needed.")
        print("Direct file inspection completed successfully.")
        return 0
    else:
        print("\n✗✗✗ VERIFICATION FAILED ✗✗✗")
        print("\nSome values do not meet deadlock-breaking thresholds.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
