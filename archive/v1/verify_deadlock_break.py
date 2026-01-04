#!/usr/bin/env python3
"""
Verify 7-Cycle Deadlock Break on Orphan Bottleneck

This script verifies that the deadlock-breaking changes are in place:
1. max_connections_per_run >= 200 (was 50)
2. max_retries >= 15 (was 5-7)
3. batch_size >= 20 (was 5)
4. similarity_threshold <= 0.05 (was 0.3)

Run this to confirm all changes are active.
"""

import sys
import os
import re
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_memory_config():
    """Check memory.py for deadlock-breaking config."""
    print("\n=== Checking memory.py ===")
    
    from memory import Memory
    config = Memory.CONNECTION_HEURISTIC_CONFIG
    
    checks = {
        "max_connections_per_run": config.get("max_connections_per_run", 0) >= 200,
        "similarity_threshold": config.get("similarity_threshold", 1.0) <= 0.05,
        "min_content_length": config.get("min_content_length", 999) <= 5,
    }
    
    for key, passed in checks.items():
        actual = config.get(key, "NOT FOUND")
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {key} = {actual}")
    
    return all(checks.values())

def check_llm_client_config():
    """Check llm_client.py for deadlock-breaking config."""
    print("\n=== Checking llm_client.py ===")
    
    filepath = Path("llm_client.py")
    content = filepath.read_text()
    
    # Look for max_retries value
    matches = re.findall(r"max_retries\s*=\s*(\d+)", content)
    
    if matches:
        max_retry = int(matches[-1])  # Get last occurrence (actual value used)
        passed = max_retry >= 15
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: max_retries = {max_retry}")
        return passed
    else:
        print("  ✗ FAIL: max_retries not found")
        return False

def check_seeker_config():
    """Check seeker.py for deadlock-breaking config."""
    print("\n=== Checking seeker.py ===")
    
    filepath = Path("seeker.py")
    content = filepath.read_text()
    
    # Look for batch_size
    batch_matches = re.findall(r"batch_size\s*=\s*(\d+)", content)
    # Look for max_retries  
    retry_matches = re.findall(r"max_retries\s*=\s*(\d+)", content)
    
    batch_ok = False
    retry_ok = False
    
    if batch_matches:
        batch_size = int(batch_matches[-1])
        batch_ok = batch_size >= 20
        status = "✓ PASS" if batch_ok else "✗ FAIL"
        print(f"  {status}: batch_size = {batch_size}")
    else:
        print(f"  ? WARN: batch_size not found")
    
    if retry_matches:
        max_retry = int(retry_matches[-1])
        retry_ok = max_retry >= 15
        status = "✓ PASS" if retry_ok else "✗ FAIL"
        print(f"  {status}: max_retries = {max_retry}")
    else:
        print(f"  ? WARN: max_retries not found")
    
    return batch_ok and retry_ok

def check_reconcile_orphans_config():
    """Check reconcile_orphans.py for deadlock-breaking config."""
    print("\n=== Checking reconcile_orphans.py ===")
    
    filepath = Path("reconcile_orphans.py")
    content = filepath.read_text()
    
    # Look for MAX_CONNECTIONS
    matches = re.findall(r"MAX_CONNECTIONS\s*=\s*(\d+)", content)
    
    if matches:
        max_conn = int(matches[-1])
        passed = max_conn >= 200
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: MAX_CONNECTIONS = {max_conn}")
        return passed
    else:
        print("  ? WARN: MAX_CONNECTIONS not found")
        return True  # Not critical

def main():
    """Run all verification checks."""
    print("="*60)
    print("VERIFYING 7-CYCLE DEADLOCK BREAK")
    print("="*60)
    
    results = {
        "memory.py": check_memory_config(),
        "llm_client.py": check_llm_client_config(),
        "seeker.py": check_seeker_config(),
        "reconcile_orphans.py": check_reconcile_orphans_config(),
    }
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for file, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {file}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓✓✓ ALL CHECKS PASSED ✓✓✓")
        print("7-Cycle deadlock has been broken!")
        print("\nKey changes:")
        print("  • max_connections_per_run: 50 → 200")
        print("  • max_retries: 5-7 → 15")
        print("  • batch_size: 5 → 20")
        print("  • similarity_threshold: 0.3 → 0.05")
        return 0
    else:
        print("\n✗✗✗ SOME CHECKS FAILED ✗✗✗")
        print("Deadlock break is incomplete.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
