#!/usr/bin/env python3
"""Observe Orphan Node Data from File Dump.

This script reads and analyzes orphan node data from the
.parallel_observations/orphan_reports.jsonl file.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

def read_orphan_reports(filepath: str = ".parallel_observations/orphan_reports.jsonl") -> List[Dict[str, Any]]:
    """Read all orphan reports from JSONL file."""
    reports = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    reports.append(json.loads(line))
    return reports

def display_orphan_summary(reports: List[Dict[str, Any]]):
    """Display summary of orphan reports."""
    print("=" * 70)
    print("ORPHAN NODE DATA OBSERVATION")
    print("=" * 70)
    print(f"Total reports: {len(reports)}")
    print(f"Report file: .parallel_observations/orphan_reports.jsonl")
    print()
    
    if not reports:
        print("No orphan reports found.")
        return
    
    for idx, report in enumerate(reports, 1):
        print(f"--- Report #{idx} ---")
        print(f"Timestamp: {report.get('timestamp', 'N/A')}")
        
        # Handle both old and new report formats
        if 'total_orphans' in report:
            print(f"Total orphans: {report['total_orphans']}")
        elif 'orphans' in report:
            print(f"Total orphans: {len(report['orphans'])}")
        
        # Display category distribution if available
        if 'category_distribution' in report:
            print("Category distribution:")
            for cat, count in report['category_distribution'].items():
                print(f"  {cat}: {count}")
        
        # Display feasibility distribution if available
        if 'feasibility_distribution' in report:
            print("Connection feasibility:")
            for feas, count in report['feasibility_distribution'].items():
                print(f"  {feas}: {count}")
        
        # Display priority distribution if available
        if 'priority_distribution' in report:
            print("Priority distribution:")
            for prio, count in report['priority_distribution'].items():
                print(f"  {prio}: {count}")
        
        # Display type distribution if available
        if 'type_distribution' in report:
            print("Node type distribution:")
            for ntype, count in report['type_distribution'].items():
                print(f"  {ntype}: {count}")
        
        # Display immediate actions if available
        if 'immediate_actions' in report:
            print("Immediate actions:")
            for action in report['immediate_actions']:
                print(f"  - {action}")
        
        # Display individual orphan nodes
        nodes = report.get('nodes', report.get('orphans', []))
        if nodes:
            print(f"\nIndividual orphan nodes ({len(nodes)}):")
            for node in nodes:
                node_id = node.get('id', node.get('element_id', 'unknown'))
                node_type = node.get('node_type', node.get('labels', ['unknown'])[0])
                content = node.get('content', 'N/A')
                category = node.get('structural_category', 'N/A')
                priority = node.get('priority', 'N/A')
                action = node.get('recommended_action', 'N/A')
                
                print(f"  [{node_id}] {node_type}")
                if content != 'N/A':
                    content_preview = content[:80] + '...' if len(content) > 80 else content
                    print(f"    Content: {content_preview}")
                if category != 'N/A':
                    print(f"    Category: {category}")
                if priority != 'N/A':
                    print(f"    Priority: {priority}")
                if action != 'N/A':
                    print(f"    Action: {action}")
                print()
        
        print()

def main():
    """Main observation function."""
    reports = read_orphan_reports()
    display_orphan_summary(reports)
    
    # Write observation summary to file
    obs_dir = ".parallel_observations"
    os.makedirs(obs_dir, exist_ok=True)
    
    observation_summary = {
        "timestamp": datetime.now().isoformat(),
        "observation_type": "orphan_dump_observation",
        "total_reports_read": len(reports),
        "total_orphans_found": sum(
            r.get('total_orphans', len(r.get('orphans', []))) for r in reports
        )
    }
    
    with open(os.path.join(obs_dir, "orphan_observation_summary.json"), 'w') as f:
        json.dump(observation_summary, f, indent=2)
    
    print("[+] Observation summary written to .parallel_observations/orphan_observation_summary.json")
    
    return 0

if __name__ == "__main__":
    exit(main())
