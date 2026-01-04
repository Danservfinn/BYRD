#!/usr/bin/env python3
"""
Fix 33 Orphan Nodes - Create Relationships

This script finds orphan nodes and creates relationships between them
to reduce graph fragmentation.

Strategies used:
1. Connect orphans of the same type in chains
2. Connect remaining orphans to a central hub
3. Verify results and report statistics

Usage:
    python fix_33_orphans.py [--dry-run]
"""

import asyncio
import os
import sys
import argparse
from datetime import datetime
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from memory import Memory


class OrphanFixer:
    """Fix orphan nodes by creating relationships."""
    
    def __init__(self, memory: Memory, dry_run: bool = False):
        self.memory = memory
        self.dry_run = dry_run
        self.stats = {
            "orphans_found": 0,
            "connections_created": 0,
            "nodes_connected": 0,
            "orphans_remaining": 0,
            "errors": []
        }
    
    async def find_all_orphans(self) -> list:
        """Find ALL orphan nodes without limit."""
        async with self.memory.driver.session() as session:
            result = await session.run("""
                MATCH (n)
                WHERE NOT (n)--()
                RETURN n.id as id, labels(n)[0] as type,
                       n.created_at as created_at,
                       coalesce(n.content, '') as content,
                       coalesce(n.description, '') as description
                ORDER BY n.created_at DESC
            """)
            return await result.data()
    
    async def create_relationship(
        self, 
        source_id: str, 
        target_id: str, 
        rel_type: str, 
        properties: dict = None
    ) -> bool:
        """Create a relationship between two nodes."""
        if self.dry_run:
            print(f"    [DRY RUN] Would create: {source_id[:20]}... -> {target_id[:20]}... ({rel_type})")
            return True
        
        try:
            async with self.memory.driver.session() as session:
                await session.run("""
                    MATCH (a {id: $source_id})
                    MATCH (b {id: $target_id})
                    CREATE (a)-[r:RELATED_TO]->(b)
                    SET r += $props
                    RETURN r
                """, source_id=source_id, target_id=target_id, props=properties or {})
            return True
        except Exception as e:
            self.stats["errors"].append(f"Relationship creation failed: {e}")
            return False
    
    async def connect_orphans_by_type(self, orphans: list) -> int:
        """Connect orphans of the same type together in chains."""
        connections = 0
        
        # Group by type
        by_type = {}
        for orphan in orphans:
            t = orphan['type']
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(orphan)
        
        # Connect within each type group
        for node_type, group in by_type.items():
            if len(group) < 2:
                continue
            
            print(f"    Connecting {len(group)} {node_type} orphans...")
            
            # Create a chain: orphan1 -> orphan2 -> orphan3 -> ...
            for i in range(len(group) - 1):
                source = group[i]
                target = group[i + 1]
                
                success = await self.create_relationship(
                    source['id'],
                    target['id'],
                    "SAME_TYPE",
                    {
                        "reason": "orphan_reconciliation",
                        "connected_at": datetime.now().isoformat(),
                        "strategy": "type_chain"
                    }
                )
                
                if success:
                    connections += 1
        
        return connections
    
    async def connect_remaining_orphans(self, orphans: list) -> int:
        """Connect any remaining orphans to the first orphan as a hub."""
        if len(orphans) < 2:
            return 0
        
        connections = 0
        hub = orphans[0]
        print(f"    Using {hub['type']} node as hub for remaining orphans...")
        
        for orphan in orphans[1:]:
            # Check if this orphan still has no connections
            async with self.memory.driver.session() as session:
                result = await session.run("""
                    MATCH (n {id: $id})
                    WHERE NOT (n)--()
                    RETURN count(n) as count
                """, id=orphan['id'])
                record = await result.single()
                still_orphan = record["count"] > 0 if record else False
            
            if still_orphan:
                success = await self.create_relationship(
                    orphan['id'],
                    hub['id'],
                    "ORPHAN_HUB_LINK",
                    {
                        "reason": "orphan_reconciliation",
                        "connected_at": datetime.now().isoformat(),
                        "strategy": "hub_connection"
                    }
                )
                
                if success:
                    connections += 1
        
        return connections
    
    async def fix(self) -> dict:
        """Main method to fix all orphan nodes."""
        print("=" * 60)
        print("ORPHAN NODE FIXER")
        print("=" * 60)
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"Started at: {datetime.now().isoformat()}")
        print()
        
        # Step 1: Find all orphan nodes
        print("[1] Finding all orphan nodes...")
        orphans = await self.find_all_orphans()
        self.stats["orphans_found"] = len(orphans)
        print(f"    Found {len(orphans)} orphan nodes")
        
        if not orphans:
            print("\n✓ No orphan nodes found!")
            return self.stats
        
        # Show orphan types
        type_counts = Counter(o['type'] for o in orphans)
        print("    Orphan types:")
        for t, count in sorted(type_counts.items()):
            print(f"      {t}: {count}")
        print()
        
        # Step 2: Connect orphans by type
        print("[2] Connecting orphans by type...")
        type_connections = await self.connect_orphans_by_type(orphans)
        self.stats["connections_created"] += type_connections
        print(f"    Created {type_connections} connections")
        print()
        
        # Step 3: Connect any remaining orphans
        print("[3] Connecting remaining orphans...")
        if not self.dry_run:
            remaining_connections = await self.connect_remaining_orphans(orphans)
            self.stats["connections_created"] += remaining_connections
            print(f"    Created {remaining_connections} connections")
        print()
        
        # Step 4: Verify results
        if not self.dry_run:
            print("[4] Verifying results...")
            remaining = await self.find_all_orphans()
            self.stats["orphans_remaining"] = len(remaining)
            print(f"    Orphans remaining: {len(remaining)}")
            
            reduction = len(orphans) - len(remaining)
            percentage = (reduction / len(orphans)) * 100 if orphans else 0
            
            print(f"    Total connections created: {self.stats['connections_created']}")
            print(f"    Reduction: {reduction}/{len(orphans)} ({percentage:.1f}%)")
            
            if len(remaining) == 0:
                print("\n✓ SUCCESS: All orphan nodes have been connected!")
            else:
                print(f"\n⚠ {len(remaining)} orphans still remain")
        else:
            print("[4] Dry run - no verification performed")
        
        # Print errors if any
        if self.stats["errors"]:
            print(f"\nErrors encountered: {len(self.stats['errors'])}")
            for error in self.stats["errors"][:5]:
                print(f"  - {error}")
        
        print()
        print(f"Completed at: {datetime.now().isoformat()}")
        print("=" * 60)
        
        return self.stats


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fix orphan nodes in BYRD's memory graph"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    # Connect to memory
    memory = Memory()
    await memory.connect()
    
    try:
        fixer = OrphanFixer(memory, dry_run=args.dry_run)
        stats = await fixer.fix()
    finally:
        await memory.close()


if __name__ == "__main__":
    asyncio.run(main())
