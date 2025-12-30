#!/usr/bin/env python3
"""
Orphan Node Reconciliation System

Reconciles orphan nodes in BYRD's memory graph by:
1. Finding all orphan nodes
2. Classifying them by structural category and connection feasibility
3. Establishing proper connections based on semantic analysis
4. Reducing graph fragmentation

Usage:
    python reconcile_orphans.py [--dry-run] [--limit N]
"""

import asyncio
import os
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory import Memory
from orphan_taxonomy import (
    OrphanTaxonomyClassifier,
    OrphanTaxonomyAnalyzer,
    OrphanNode,
    StructuralCategory,
    ConnectionFeasibility,
    PriorityLevel
)


class OrphanReconciler:
    """
    Main orchestrator for orphan node reconciliation.
    
    Implements a multi-strategy approach:
    1. Direct semantic matching for HIGH feasibility nodes
    2. Temporal linking for RELATED nodes of similar age
    3. Type-based clustering for similar node categories
    4. Hub connection for CRITICAL priority nodes
    """

    # Semantic similarity threshold for matching
    SEMANTIC_THRESHOLD = 0.3
    
    # Maximum connections to create in one run
    MAX_CONNECTIONS = 50

    def __init__(self, memory: Memory, dry_run: bool = False):
        self.memory = memory
        self.dry_run = dry_run
        self.classifier = OrphanTaxonomyClassifier(memory)
        self.stats = {
            "orphans_found": 0,
            "connections_created": 0,
            "nodes_connected": 0,
            "by_category": {},
            "errors": []
        }

    async def reconcile_all(self, limit: int = 100) -> Dict:
        """
        Main reconciliation routine.
        
        Args:
            limit: Maximum number of orphans to process
            
        Returns:
            Dictionary with reconciliation statistics
        """
        print("\n" + "="*60)
        print("ORPHAN NODE RECONCILIATION")
        print("="*60)
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"Started at: {datetime.now().isoformat()}")
        print()

        # Step 1: Find all orphan nodes
        orphans_raw = await self.memory.find_orphan_nodes()
        self.stats["orphans_found"] = len(orphans_raw)
        print(f"[1] Found {len(orphans_raw)} orphan nodes")
        
        if not orphans_raw:
            print("\n✓ No orphan nodes to reconcile.")
            return self.stats

        # Step 2: Classify all orphans
        print(f"[2] Classifying orphan nodes...")
        classified_orphans = []
        for node_data in orphans_raw[:limit]:
            orphan = await self.classifier.classify_orphan(node_data)
            classified_orphans.append(orphan)
            
            # Track by category
            cat = orphan.structural_category.value if orphan.structural_category else "unknown"
            self.stats["by_category"][cat] = self.stats["by_category"].get(cat, 0) + 1
        
        print(f"    Classified {len(classified_orphans)} nodes")
        
        # Step 3: Group by priority and apply strategies
        print(f"[3] Applying reconciliation strategies...")
        
        # Sort by priority (CRITICAL first, then HIGH, etc.)
        priority_order = {
            PriorityLevel.CRITICAL: 0,
            PriorityLevel.HIGH: 1,
            PriorityLevel.MEDIUM: 2,
            PriorityLevel.LOW: 3,
            PriorityLevel.IGNORE: 999
        }
        classified_orphans.sort(
            key=lambda o: priority_order.get(o.priority, 999)
        )
        
        # Apply strategies in priority order
        connections_made = 0
        for orphan in classified_orphans:
            if connections_made >= self.MAX_CONNECTIONS:
                print(f"    Reached max connections limit ({self.MAX_CONNECTIONS})")
                break
            
            if orphan.priority == PriorityLevel.IGNORE:
                continue
            
            # Verify still orphan (might have been connected already)
            still_orphan = await self._verify_still_orphan(orphan.id)
            if not still_orphan:
                continue
            
            # Apply appropriate strategy based on category and feasibility
            strategy_result = await self._apply_strategy(orphan, classified_orphans)
            
            if strategy_result:
                connections_made += strategy_result
                self.stats["connections_created"] += strategy_result
                self.stats["nodes_connected"] += strategy_result * 2  # Each connection involves 2 nodes

        # Step 4: Final report
        print(f"\n[4] Reconciliation complete")
        await self._print_report()
        
        return self.stats

    async def _verify_still_orphan(self, node_id: str) -> bool:
        """Check if a node is still orphaned."""
        try:
            async with self.memory.driver.session() as session:
                result = await session.run("""
                    MATCH (n {id: $id})
                    WHERE NOT (n)--()
                    RETURN count(n) as count
                """, id=node_id)
                record = await result.single()
                return record["count"] > 0
        except Exception as e:
            self.stats["errors"].append(f"Error verifying orphan status: {e}")
            return False

    async def _apply_strategy(
        self, 
        orphan: OrphanNode, 
        all_orphans: List[OrphanNode]
    ) -> int:
        """
        Apply the appropriate reconciliation strategy for an orphan.
        
        Returns:
            Number of connections created (0 or 1)
        """
        strategy = self._determine_strategy(orphan)
        
        if strategy == "semantic_match":
            return await self._strategy_semantic_match(orphan, all_orphans)
        elif strategy == "type_cluster":
            return await self._strategy_type_cluster(orphan, all_orphans)
        elif strategy == "temporal_link":
            return await self._strategy_temporal_link(orphan, all_orphans)
        elif strategy == "hub_connection":
            return await self._strategy_hub_connection(orphan)
        else:
            return 0

    def _determine_strategy(self, orphan: OrphanNode) -> str:
        """Determine the best strategy for connecting this orphan."""
        # CRITICAL nodes get hub connection
        if orphan.priority == PriorityLevel.CRITICAL:
            return "hub_connection"
        
        # HIGH feasibility gets semantic matching
        if orphan.connection_feasibility == ConnectionFeasibility.HIGH:
            return "semantic_match"
        
        # MEDIUM feasibility gets type-based clustering
        if orphan.connection_feasibility == ConnectionFeasibility.MEDIUM:
            return "type_cluster"
        
        # LOW feasibility gets temporal linking (best-effort)
        if orphan.connection_feasibility == ConnectionFeasibility.LOW:
            return "temporal_link"
        
        return "none"

    async def _strategy_semantic_match(
        self, 
        orphan: OrphanNode, 
        all_orphans: List[OrphanNode]
    ) -> int:
        """
        Strategy: Find semantically similar orphan and connect.
        
        Uses content similarity based on shared meaningful words.
        """
        best_match = None
        best_score = 0
        
        orphan_words = set(orphan.content.lower().split())
        
        for candidate in all_orphans:
            if candidate.id == orphan.id:
                continue
            
            # Calculate simple word overlap similarity
            candidate_words = set(candidate.content.lower().split())
            intersection = orphan_words & candidate_words
            union = orphan_words | candidate_words
            
            if len(union) == 0:
                continue
            
            similarity = len(intersection) / len(union)
            
            if similarity > best_score and similarity >= self.SEMANTIC_THRESHOLD:
                best_score = similarity
                best_match = candidate
        
        if best_match:
            return await self._create_connection(
                orphan.id,
                best_match.id,
                "SEMANTICALLY_RELATED",
                {"similarity": best_score, "method": "word_overlap"}
            )
        
        # Fallback to type clustering
        return await self._strategy_type_cluster(orphan, all_orphans)

    async def _strategy_type_cluster(
        self, 
        orphan: OrphanNode, 
        all_orphans: List[OrphanNode]
    ) -> int:
        """
        Strategy: Connect to another orphan of the same type.
        
        Useful for grouping similar nodes together.
        """
        for candidate in all_orphans:
            if candidate.id == orphan.id:
                continue
            
            if candidate.node_type == orphan.node_type:
                return await self._create_connection(
                    orphan.id,
                    candidate.id,
                    "SAME_TYPE",
                    {"type": orphan.node_type}
                )
        
        return 0

    async def _strategy_temporal_link(
        self, 
        orphan: OrphanNode, 
        all_orphans: List[OrphanNode]
    ) -> int:
        """
        Strategy: Connect to orphan from similar time period.
        
        Useful for experiences from the same context/session.
        """
        # Find orphans within 24 hours
        time_window_hours = 24
        
        for candidate in all_orphans:
            if candidate.id == orphan.id:
                continue
            
            age_diff = abs(orphan.age_hours - candidate.age_hours)
            if age_diff <= time_window_hours:
                return await self._create_connection(
                    orphan.id,
                    candidate.id,
                    "TEMPORALLY_COLOCATED",
                    {"age_diff_hours": age_diff}
                )
        
        # Fallback: connect to any orphan
        for candidate in all_orphans:
            if candidate.id == orphan.id:
                continue
            return await self._create_connection(
                orphan.id,
                candidate.id,
                "BEST_EFFORT_LINK",
                {}
            )
        
        return 0

    async def _strategy_hub_connection(self, orphan: OrphanNode) -> int:
        """
        Strategy: Connect CRITICAL orphans to highly-connected hub nodes.
        
        Finds nodes with many connections and links the orphan to them.
        """
        try:
            async with self.memory.driver.session() as session:
                # Find a well-connected node of the same type
                result = await session.run("""
                    MATCH (n:{{type}})
                    WHERE (n)--()
                    WITH n, count {{ (n)--() }} as connections
                    ORDER BY connections DESC
                    LIMIT 1
                    RETURN n.id as hub_id, connections
                """, type=orphan.node_type)
                
                record = await result.single()
                if record:
                    hub_id = record["hub_id"]
                    connections = record["connections"]
                    
                    return await self._create_connection(
                        orphan.id,
                        hub_id,
                        "LINKED_TO_HUB",
                        {"hub_connections": connections}
                    )
        except Exception as e:
            self.stats["errors"].append(f"Hub connection failed: {e}")
        
        # Fallback to type clustering
        orphans_raw = await self.memory.find_orphan_nodes()
        all_orphans = [await self.classifier.classify_orphan(o) for o in orphans_raw]
        return await self._strategy_type_cluster(orphan, all_orphans)

    async def _create_connection(
        self,
        from_id: str,
        to_id: str,
        rel_type: str,
        properties: Dict
    ) -> int:
        """
        Create a relationship between two nodes.
        
        Returns:
            1 if successful, 0 otherwise
        """
        if self.dry_run:
            print(f"    [DRY RUN] Would connect {from_id[:16]}... -> {to_id[:16]}... ({rel_type})")
            return 1
        
        try:
            # Add timestamp to properties
            properties["created_at"] = datetime.now().isoformat()
            properties["reconciliation_method"] = "orphan_reconciler"
            
            success = await self.memory.create_relationship(
                from_id,
                to_id,
                rel_type,
                properties
            )
            
            if success:
                print(f"    ✓ Connected {from_id[:16]}... -> {to_id[:16]}... ({rel_type})")
                return 1
            else:
                self.stats["errors"].append(f"Failed to create relationship {from_id} -> {to_id}")
                return 0
                
        except Exception as e:
            self.stats["errors"].append(f"Connection error: {e}")
            return 0

    async def _print_report(self):
        """Print reconciliation statistics report."""
        print("\n" + "="*60)
        print("RECONCILIATION REPORT")
        print("="*60)
        print(f"Orphans found: {self.stats['orphans_found']}")
        print(f"Connections created: {self.stats['connections_created']}")
        print(f"Nodes connected: {self.stats['nodes_connected']}")
        print()
        
        if self.stats["by_category"]:
            print("Orphans by category:")
            for cat, count in sorted(self.stats["by_category"].items()):
                print(f"  {cat}: {count}")
            print()
        
        if self.stats["errors"]:
            print(f"Errors encountered: {len(self.stats['errors'])}")
            for error in self.stats["errors"][:5]:  # Show first 5
                print(f"  - {error}")
            if len(self.stats["errors"]) > 5:
                print(f"  ... and {len(self.stats['errors']) - 5} more")
        
        print()
        orphans_remaining = self.stats["orphans_found"] - self.stats["nodes_connected"]
        print(f"Orphans remaining: {orphans_remaining}")
        print(f"Reduction: {self.stats['nodes_connected']}/{self.stats['orphans_found']} "
              f"({self.stats['nodes_connected']/max(self.stats['orphans_found'],1)*100:.1f}%)")
        print(f"Completed at: {datetime.now().isoformat()}")
        print("="*60)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Reconcile orphan nodes in BYRD's memory graph"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum orphans to process (default: 100)"
    )
    
    args = parser.parse_args()
    
    # Initialize memory system
    from dotenv import load_dotenv
    load_dotenv()
    
    memory = Memory()
    await memory.connect()
    
    # Run reconciliation
    reconciler = OrphanReconciler(memory, dry_run=args.dry_run)
    stats = await reconciler.reconcile_all(limit=args.limit)
    
    await memory.close()
    
    # Exit with error if any issues
    if stats["errors"] and not args.dry_run:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
