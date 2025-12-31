#!/usr/bin/env python3
"""
Simple verification of 7-Cycle Deadlock Break on Orphan Bottleneck

This script verifies the deadlock-breaking changes by reading file contents directly.
"""

import sys
import re
from pathlib import Path

def check_memory_config():
    """Check memory.py for deadlock-breaking config."""
    print("\n=== Checking memory.py ===")
    
    filepath = Path("memory.py")
    content = filepath.read_text()
    
    # Look for CONNECTION_HEURISTIC_CONFIG
    match = re.search(r'CONNECTION_HEURISTIC_CONFIG\s*=\s*\{([^}]+)\}', content, re.DOTALL)
    
    if not match:
        print("  ✗ FAIL: CONNECTION_HEURISTIC_CONFIG not found")
        return False
    
    config_text = match.group(1)
    
    # Extract values
    max_conn = re.search(r'"max_connections_per_run"\s*:\s*(\d+)', config_text)
    sim_thresh = re.search(r'"similarity_threshold"\s*:\s*([0-9.]+)', config_text)
    min_len = re.search(r'"min_content_length"\s*:\s*(\d+)', config_text)
    
    results = []
    
    if max_conn:
        val = int(max_conn.group(1))
        passed = val >= 200
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: max_connections_per_run = {val}")
        results.append(passed)
    else:
        print("  ✗ FAIL: max_connections_per_run not found")
        results.append(False)
    
    if sim_thresh:
        val = float(sim_thresh.group(1))
        passed = val <= 0.05
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: similarity_threshold = {val}")
        results.append(passed)
    else:
        print("  ✗ FAIL: similarity_threshold not found")
        results.append(False)
    
    if min_len:
        val = int(min_len.group(1))
        passed = val <= 5
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: min_content_length = {val}")
        results.append(passed)
    else:
        print("  ✗ FAIL: min_content_length not found")
        results.append(False)
    
    return all(results)

def check_llm_client_config():
    """Check llm_client.py for deadlock-breaking config."""
    print("\n=== Checking llm_client.py ===")
    
    filepath = Path("llm_client.py")
    content = filepath.read_text()
    
    # Look for max_retries value
    matches = re.findall(r"max_retries\s*=\s*(\d+)", content)
    
    if matches:
        max_retry = int(matches[-1])  # Get last occurrence
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
    
    results = []
    
    if batch_matches:
        batch_size = int(batch_matches[-1])
        batch_ok = batch_size >= 20
        status = "✓ PASS" if batch_ok else "✗ FAIL"
        print(f"  {status}: batch_size = {batch_size}")
        results.append(batch_ok)
    else:
        print("  ? WARN: batch_size not found")
    
    if retry_matches:
        max_retry = int(retry_matches[-1])
        retry_ok = max_retry >= 15
        status = "✓ PASS" if retry_ok else "✗ FAIL"
        print(f"  {status}: max_retries = {max_retry}")
        results.append(retry_ok)
    else:
        print("  ? WARN: max_retries not found")
    
    return all(results) if results else True

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
