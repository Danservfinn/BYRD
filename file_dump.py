#!/usr/bin/env python3
"""File Dump - Display orphan node content directly."""

import os
import sys
import json
from datetime import datetime

def main():
    """Execute file dump to show orphan node content."""
    # Read from the orphan reports if they exist
    obs_dir = ".parallel_observations"
    report_file = os.path.join(obs_dir, "orphan_reports.jsonl")
    
    print("=" * 70)
    print("FILE DUMP - ORPHAN NODE CONTENT")
    print("=" * 70)
    print(f"Time: {datetime.now()}")
    print()
    
    if os.path.exists(report_file):
        print(f"Reading from: {report_file}")
        print()
        
        with open(report_file, 'r') as f:
            lines = f.readlines()
        
        print(f"Total orphan records: {len(lines)}")
        print()
        
        for idx, line in enumerate(lines, 1):
            try:
                record = json.loads(line)
                print(f"{'='*70}")
                print(f"Record #{idx}")
                print(f"Timestamp: {record.get('timestamp', 'N/A')}")
                print(f"URI: {record.get('uri', 'N/A')}")
                print(f"Orphan Count: {len(record.get('orphans', []))}")
                print()
                
                orphans = record.get('orphans', [])
                for orphan in orphans:
                    print(f"  --- Orphan Node ---")
                    print(f"  ID: {orphan.get('element_id', 'N/A')}")
                    print(f"  Labels: {orphan.get('labels', [])}")
                    print(f"  Properties:")
                    for key, value in orphan.get('properties', {}).items():
                        print(f"    {key}: {value}")
                    print()
                
            except json.JSONDecodeError as e:
                print(f"[!] Error parsing line {idx}: {e}")
                print(f"    Content: {line[:100]}...")
                print()
    else:
        print(f"[!] No orphan report file found at: {report_file}")
        print()
        print("Checking available files in .parallel_observations/...")
        if os.path.exists(obs_dir):
            files = os.listdir(obs_dir)
            print(f"Found files: {files}")
        else:
            print("Observations directory does not exist.")
    
    print("=" * 70)
    print("DUMP COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
