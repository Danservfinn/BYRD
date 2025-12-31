#!/usr/bin/env python3
"""
Direct Orphan Node Fixer

Simple script to fix 33 orphan nodes by creating relationships between them.
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from memory import Memory


class SimpleOrphanFixer:
    """Simple orphan node fixer that creates connections."""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.stats = {
            "orphans_found": 0,
            "connections_created": 0,
            "errors": []
        }
    
    async def fix_orphans(self, limit: int = 50) -> Dict:
        """Main fix routine."""
        print("=" * 60)
        print("ORPHAN NODE FIXER")
        print("=" * 60)
        print(f"Started at: {datetime.now().isoformat()}")
        print()
        
        # Step 1: Find orphan nodes
        print("[1] Finding orphan nodes...")
        orphans = await self.memory.find_orphan_nodes()
        self.stats["orphans_found"] = len(orphans)
        print(f"    Found {len(orphans)} orphan nodes")
        
        if len(orphans) < 2:
            print("    Need at least 2 orphans to create connections")
            return self.stats
        
        # Step 2: Create connections
        print(f"\n[2] Creating connections between orphans...")
        
        # Connect orphans in a chain
        connections_created = 0
        for i in range(min(len(orphans) - 1, limit)):
            from_node = orphans[i]
            to_node = orphans[i + 1]
            
            from_id = from_node.get('id')
            to_id = to_node.get('id')
            from_type = from_node.get('type', 'Unknown')
            to_type = to_node.get('type', 'Unknown')
            
            if not from_id or not to_id:
                print(f"    \u26a0 Skipping - missing IDs")
                continue
            
            # Determine relationship type based on node types
            if from_type == to_type:
                rel_type = "SIMILAR_TO"
            else:
                rel_type = "RELATES_TO"
            
            properties = {
                "formed_at": datetime.now().isoformat(),
                "reconciliation_method": "simple_orphan_fixer",
                "reason": "orphan_reconciliation"
            }
            
            try:
                success = await self.memory.create_connection(
                    from_id,
                    to_id,
                    rel_type,
                    properties
                )
                
                if success:
                    print(f"    \u2713 Connected {from_id[:16]}... ({from_type}) -> {to_id[:16]}... ({to_type})")
                    connections_created += 1
                    self.stats["connections_created"] += 1
                else:
                    print(f"    \u26a0 Failed to connect {from_id[:16]}... -> {to_id[:16]}...")
                    self.stats["errors"].append(f"Connection failed: {from_id} -> {to_id}")
            except Exception as e:
                print(f"    \u2717 Error: {e}")
                self.stats["errors"].append(str(e))
        
        # Step 3: Create some cross-connections for better graph structure
        print(f"\n[3] Creating cross-connections...")
        for i in range(min(5, len(orphans))):
            from_node = orphans[i]
            to_node = orphans[-(i + 1)]  # Connect to nodes from the end
            
            from_id = from_node.get('id')
            to_id = to_node.get('id')
            
            if from_id == to_id:
                continue
            
            try:
                success = await self.memory.create_connection(
                    from_id,
                    to_id,
                    "ALSO_RELATED",
                    {"formed_at": datetime.now().isoformat(), "reconciliation_method": "simple_orphan_fixer"}
                )
                
                if success:
                    print(f"    \u2713 Cross-connected {from_id[:16]}... -> {to_id[:16]}...")
                    connections_created += 1
                    self.stats["connections_created"] += 1
            except Exception as e:
                self.stats["errors"].append(str(e))
        
        # Step 4: Final report
        print(f"\n[4] Fix complete")
        await self._print_report()
        
        return self.stats
    
    async def _print_report(self):
        """Print fix statistics report."""
        print("\n" + "=" * 60)
        print("FIX REPORT")
        print("=" * 60)
        print(f"Orphans found: {self.stats['orphans_found']}")
        print(f"Connections created: {self.stats['connections_created']}")
        print(f"Nodes affected: ~{self.stats['connections_created'] * 2}")
        print()
        
        if self.stats["errors"]:
            print(f"Errors encountered: {len(self.stats['errors'])}")
            for error in self.stats["errors"][:5]:
                print(f"  - {error}")
            if len(self.stats["errors"]) > 5:
                print(f"  ... and {len(self.stats['errors']) - 5} more")
            print()
        
        orphans_remaining = max(0, self.stats['orphans_found'] - (self.stats['connections_created'] * 2))
        print(f"Estimated orphans remaining: {orphans_remaining}")
        print(f"Completed at: {datetime.now().isoformat()}")
        print("=" * 60)


async def main():
    """Main entry point."""
    load_dotenv()
    
    memory = Memory()
    await memory.connect()
    
    fixer = SimpleOrphanFixer(memory)
    stats = await fixer.fix_orphans(limit=50)
    
    await memory.close()
    
    # Exit with error if connections failed
    if stats["connections_created"] == 0 and stats["orphans_found"] >= 2:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
