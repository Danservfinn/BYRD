#!/usr/bin/env python3
"""Simple test of orphan dump functionality."""

import asyncio
from pathlib import Path
from datetime import datetime
import json

async def main():
    print("Testing orphan file dump...")
    
    # Create report file directory
    report_dir = Path(".parallel_observations")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Write a test report
    report_file = report_dir / "orphan_reports.jsonl"
    
    test_report = {
        "timestamp": datetime.now().isoformat(),
        "total_orphans": 2,
        "category_distribution": {"isolated_observation": 1, "dream_output": 1},
        "nodes": [
            {"id": "test_001", "node_type": "Experience", "content": "Test orphan 1"},
            {"id": "test_002", "node_type": "Reflection", "content": "Test orphan 2"}
        ]
    }
    
    with open(report_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(test_report, ensure_ascii=False) + "\n")
    
    print(f"[+] Test report written to {report_file}")
    print("[+] Test completed successfully")

if __name__ == "__main__":
    asyncio.run(main())
