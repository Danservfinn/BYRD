#!/usr/bin/env python3
"""Observe orphan node data via file_dump mechanism."""

import asyncio
import yaml
from orphan_taxonomy import OrphanTaxonomyAnalyzer, TaxonomyReport


async def observe_and_dump():
    """Run orphan analysis and display results."""
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
    
    from memory import Memory
    memory = Memory(config)
    await memory.initialize()
    
    analyzer = OrphanTaxonomyAnalyzer(memory)
    report = await analyzer.analyze_all_orphans(50)
    
    # Display report
    print("\n" + "="*50)
    print("ORPHAN NODE OBSERVATION")
    print("="*50)
    print(f"Timestamp: {report.analysis_timestamp}")
    print(f"Total Orphans: {report.total_orphans}")
    
    print("\nCategory Distribution:")
    for cat, count in report.category_distribution.items():
        print(f"  {cat}: {count}")
    
    print("\nConnection Feasibility:")
    for feas, count in report.feasibility_distribution.items():
        pct = count / report.total_orphans * 100 if report.total_orphans else 0
        print(f"  {feas}: {count} ({pct:.1f}%)")
    
    print("\nPriority Distribution:")
    for pri, count in report.priority_distribution.items():
        print(f"  {pri}: {count}")
    
    print("\nNode Types:")
    for typ, count in report.type_distribution.items():
        print(f"  {typ}: {count}")
    
    if report.nodes:
        print(f"\nTop 5 Orphan Nodes:")
        for node in report.nodes[:5]:
            cat = node.structural_category.value if node.structural_category else 'N/A'
            print(f"  [{node.id}] {node.node_type} - {cat}")
            print(f"    Content: {node.content[:100]}...")
    
    await memory.close()
    
    return report


def file_dump_report(report):
    """Print report data for file capture."""
    ts = report.analysis_timestamp.strftime('%Y%m%d_%H%M%S')
    print(f"\nFILE_DUMP: orphan_report_{ts}.json")
    print(f"\nFile Dump - Orphan Node Analysis")
    print(f"Timestamp: {report.analysis_timestamp}")
    print(f"Total Orphans: {report.total_orphans}")
    print(f"\nCategories:")
    for cat, cnt in sorted(report.category_distribution.items()):
        print(f"  {cat}: {cnt}")
    print(f"\nFeasibility:")
    for feas, cnt in sorted(report.feasibility_distribution.items()):
        pct = cnt / report.total_orphans * 100 if report.total_orphans else 0
        print(f"  {feas}: {cnt} ({pct:.1f}%)")
    print(f"\nPriorities:")
    for pri, cnt in sorted(report.priority_distribution.items()):
        print(f"  {pri}: {cnt}")


if __name__ == "__main__":
    report = asyncio.run(observe_and_dump())
    file_dump_report(report)
