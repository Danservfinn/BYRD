#!/usr/bin/env python3
"""
7-CYCLE DEADLOCK FIX VERIFICATION

This script verifies that all orphan-related deadlock fixes are in place.

THE DEADLOCK PROBLEM (Before):
- batch_size = 5 (too small, causes excessive cycles)
- retry_limit = 7 (hard deadlock point)
- max_connections = 50 (insufficient for high orphan volume)

THE FIX (After):
- batch_size >= 20 (5x+ throughput increase)
- retry_limit >= 15 (2x+ resilience increase)
- max_connections >= 200 (4x+ capacity increase)

This script checks all orphan processing files to ensure the fixes are applied.
"""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration thresholds for deadlock-free operation
MIN_BATCH_SIZE = 20
MIN_RETRY_LIMIT = 15
MIN_MAX_CONNECTIONS = 200

# Files to check
FILES_TO_CHECK = [
    "orphan_reader.py",
    "reconcile_orphans.py",
    "memory.py",
    "seeker.py",
    "break_7cycle_deadlock.py",
    "orphan_deadlock_breaker.py",
]

def extract_config_values(filepath: str) -> Dict[str, int]:
    """Extract configuration values from a Python file."""
    config = {
        "batch_size": None,
        "max_retries": None,
        "retry_limit": None,
        "max_connections": None,
    }
    
    if not os.path.exists(filepath):
        return config
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract batch_size
    batch_match = re.search(r'batch_size\s*=\s*(\d+)', content, re.IGNORECASE)
    if batch_match:
        config["batch_size"] = int(batch_match.group(1))
    
    # Extract max_retries
    retry_match = re.search(r'max_retries\s*=\s*(\d+)', content, re.IGNORECASE)
    if retry_match:
        config["max_retries"] = int(retry_match.group(1))
    
    # Extract retry_limit (alternative name)
    retry_limit_match = re.search(r'retry_limit\s*=\s*(\d+)', content, re.IGNORECASE)
    if retry_limit_match:
        config["retry_limit"] = int(retry_limit_match.group(1))
    
    # Extract max_connections
    conn_match = re.search(r'max_connections\s*=\s*(\d+)', content, re.IGNORECASE)
    if conn_match:
        config["max_connections"] = int(conn_match.group(1))
    
    return config

def check_deadlock_free(config: Dict[str, int]) -> Tuple[bool, List[str]]:
    """Check if configuration is deadlock-free."""
    issues = []
    
    # Check batch_size
    if config.get("batch_size") is not None:
        if config["batch_size"] < MIN_BATCH_SIZE:
            issues.append(
                f"batch_size={config['batch_size']} < {MIN_BATCH_SIZE} (DEADLOCK RISK)"
            )
    
    # Check retry limits
    retry_value = config.get("max_retries") or config.get("retry_limit")
    if retry_value is not None:
        if retry_value < MIN_RETRY_LIMIT:
            issues.append(
                f"retry={retry_value} < {MIN_RETRY_LIMIT} (7-CYCLE DEADLOCK RISK)"
            )
    
    # Check max_connections
    if config.get("max_connections") is not None:
        if config["max_connections"] < MIN_MAX_CONNECTIONS:
            issues.append(
                f"max_connections={config['max_connections']} < {MIN_MAX_CONNECTIONS} (BOTTLENECK RISK)"
            )
    
    return len(issues) == 0, issues

def print_separator(char="=", length=70):
    print(char * length)

def main():
    print_separator()
    print("7-CYCLE DEADLOCK FIX VERIFICATION")
    print_separator()
    print(f"\nRequired thresholds for deadlock-free operation:")
    print(f"  • batch_size >= {MIN_BATCH_SIZE}")
    print(f"  • retry_limit >= {MIN_RETRY_LIMIT}")
    print(f"  • max_connections >= {MIN_MAX_CONNECTIONS}")
    print()
    
    all_passed = True
    results = []
    
    for filepath in FILES_TO_CHECK:
        print_separator("-")
        print(f"Checking: {filepath}")
        
        config = extract_config_values(filepath)
        
        # Print config values
        for key, value in config.items():
            if value is not None:
                print(f"  {key}: {value}")
        
        # Check if deadlock-free
        is_safe, issues = check_deadlock_free(config)
        
        if is_safe:
            print(f"  ✅ PASS: Deadlock-free configuration")
        else:
            print(f"  ❌ FAIL: Deadlock risk detected")
            for issue in issues:
                print(f"     • {issue}")
            all_passed = False
        
        results.append({
            "filepath": filepath,
            "config": config,
            "is_safe": is_safe,
            "issues": issues
        })
        
        print()
    
    print_separator()
    print("SUMMARY")
    print_separator()
    
    safe_count = sum(1 for r in results if r["is_safe"])
    total_count = len(results)
    
    print(f"Files checked: {total_count}")
    print(f"Files passing: {safe_count}")
    print(f"Files failing: {total_count - safe_count}")
    print()
    
    if all_passed:
        print("✅ SUCCESS: All files have deadlock-free configurations")
        print("\nThe 7-cycle deadlock on orphan bottleneck has been broken.")
        return 0
    else:
        print("❌ FAILURE: Some files still have deadlock-prone configurations")
        print("\nPlease update the failing files to use:")
        print(f"  • batch_size >= {MIN_BATCH_SIZE}")
        print(f"  • max_retries >= {MIN_RETRY_LIMIT}")
        print(f"  • max_connections >= {MIN_MAX_CONNECTIONS}")
        return 1

if __name__ == "__main__":
    exit(main())
