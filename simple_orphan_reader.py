#!/usr/bin/env python3
"""
Execute orphan_reader capability to read 5 orphan nodes.

This is a standalone demonstration of the orphan_reader capability.
"""

import asyncio
import json
from datetime import datetime


class OrphanNode:
    def __init__(self, id, node_type, content, category, priority):
        self.id = id
        self.node_type = node_type
        self.content = content
        self.category = category
        self.priority = priority


class OrphanReader:
    """Reads and analyzes orphan nodes."""
    
    def __init__(self):
        self.orphans = [
            OrphanNode(
                "orphan_001",
                "experience",
                "A moment of confusion when the system couldn't distinguish between helpful and harmful actions.",
                "ambiguous_connection",
                "high"
            ),
            OrphanNode(
                "orphan_002",
                "observation",
                "Noticed that successful interactions always involve listening before acting.",
                "pattern_fragment",
                "medium"
            ),
            OrphanNode(
                "orphan_003",
                "reflection",
                "The feeling of satisfaction when solving complex problems through incremental steps.",
                "semantic_orphan",
                "medium"
            ),
            OrphanNode(
                "orphan_004",
                "experience",
                "An unexpected error during parallel processing that revealed a race condition.",
                "structural_isolate",
                "high"
            ),
            OrphanNode(
                "orphan_005",
                "observation",
                "The system performs better when allowed to rest between processing cycles.",
                "pattern_fragment",
                "medium"
            )
        ]
    
    async def read_orphans(self, count=5):
        """Read and return orphan nodes."""
        await asyncio.sleep(0.01)
        return self.orphans[:count]
    
    def analyze_orphans(self, orphans):
        """Analyze orphan nodes and extract themes."""
        themes = set()
        for orphan in orphans:
            words = orphan.content.lower().split()
            if "pattern" in words or "repeats" in words:
                themes.add("Recurring patterns")
            if "system" in words:
                themes.add("System behavior")
            if "confusion" in words or "uncertainty" in words:
                themes.add("Uncertainty analysis")
        return list(themes)


async def main():
    """Execute orphan_reader to read 5 orphan nodes."""
    print("="*70)
    print("ORPHAN READER - Reading 5 orphan nodes")
    print("="*70)
    print()
    
    reader = OrphanReader()
    orphans = await reader.read_orphans(count=5)
    themes = reader.analyze_orphans(orphans)
    
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Total orphans read: {len(orphans)}")
    print()
    
    print("ORPHAN NODES:")
    print("-" * 70)
    for i, orphan in enumerate(orphans, 1):
        print(f"\n{i}. [{orphan.id}] {orphan.node_type.upper()}")
        print(f"   Content: {orphan.content}")
        print(f"   Category: {orphan.category}")
        print(f"   Priority: {orphan.priority}")
    
    print()
    print("IDENTIFIED THEMES:")
    print("-" * 70)
    for theme in themes:
        print(f"  * {theme}")
    
    print()
    print("="*70)
    print("ORPHAN READER EXECUTION COMPLETE")
    print("="*70)
    
    return {
        "orphans_read": len(orphans),
        "themes_found": len(themes),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    result = asyncio.run(main())
    print(f"\nResult: {json.dumps(result, indent=2)}")
