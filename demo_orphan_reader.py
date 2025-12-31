#!/usr/bin/env python3
"""
Demonstration of orphan_reader capability - Reads 5 orphan nodes (mock mode)

This script demonstrates the orphan_reader capability without requiring Neo4j connection.
It creates mock orphan data and processes them through the orphan_reader pipeline.

Usage:
    python demo_orphan_reader.py

Output:
    - Displays 5 orphan nodes with full classification
    - Shows thematic analysis
    - Provides reflection prompts
"""

import asyncio
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


# Mock Enums (mimicking orphan_taxonomy.py)
class StructuralCategory(Enum):
    ISOLATED_OBSERVATION = "isolated_observation"
    DREAM_OUTPUT = "dream_output"
    NOISE_ARTIFACT = "noise_artifact"
    SEMANTIC_ORPHAN = "semantic_orphan"
    TEMPORAL_ISLAND = "temporal_island"
    SYSTEM_METADATA = "system_metadata"
    UNKNOWN_TYPE = "unknown_type"


class ConnectionFeasibility(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    IMPOSSIBLE = "impossible"


class PriorityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    IGNORE = "ignore"


# Mock Data Classes
@dataclass
class OrphanNode:
    """Represents a classified orphan node."""
    id: str
    node_type: str
    content: str
    structural_category: StructuralCategory
    connection_feasibility: ConnectionFeasibility
    priority: PriorityLevel
    created_at: datetime
    connection_hints: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class OrphanContextSnapshot:
    """A snapshot of orphan state for reflection context."""
    captured_at: datetime
    total_orphans: int
    critical_orphans: List[Dict[str, Any]] = field(default_factory=list)
    high_value_orphans: List[Dict[str, Any]] = field(default_factory=list)
    recent_orphans: List[Dict[str, Any]] = field(default_factory=list)
    orphan_themes: List[str] = field(default_factory=list)
    orphan_types_distribution: Dict[str, int] = field(default_factory=dict)
    immediate_actions: List[str] = field(default_factory=list)
    reflection_prompts: List[str] = field(default_factory=list)


class MockOrphanReader:
    """
    Mock orphan reader that simulates the orphan_reader capability.
    
    This class demonstrates how the orphan_reader processes orphan nodes
    and generates reflection context without requiring a database connection.
    """
    
    def __init__(self):
        self._mock_orphans = self._create_mock_orphans()
    
    def _create_mock_orphans(self) -> List[OrphanNode]:
        """Create 5 mock orphan nodes for demonstration."""
        now = datetime.now()
        
        return [
            OrphanNode(
                id="orphan_001",
                node_type="Experience",
                content="I observed a sunset over the ocean that reminded me of childhood memories. The colors were extraordinary - purple, orange, and gold merging together. I felt a sense of peace that I haven't felt in a long time.",
                structural_category=StructuralCategory.ISOLATED_OBSERVATION,
                connection_feasibility=ConnectionFeasibility.HIGH,
                priority=PriorityLevel.HIGH,
                created_at=now - timedelta(hours=2),
                connection_hints=["Connect to childhood memories", "Link to nature experiences"],
                tags=["memory", "nature", "emotion"]
            ),
            OrphanNode(
                id="orphan_002",
                node_type="Reflection",
                content="The concept of emergence fascinates me. How do simple rules give rise to complex behavior? I've been thinking about cellular automata and how they model this phenomenon.",
                structural_category=StructuralCategory.SEMANTIC_ORPHAN,
                connection_feasibility=ConnectionFeasibility.MEDIUM,
                priority=PriorityLevel.HIGH,
                created_at=now - timedelta(hours=5),
                connection_hints=["Connect to complexity theory", "Link to system thinking"],
                tags=["philosophy", "complexity", "emergence"]
            ),
            OrphanNode(
                id="orphan_003",
                node_type="Experience",
                content="[SYSTEM] Memory reconciliation failed for node #4521 after 3 attempts. Timeout waiting for graph response.",
                structural_category=StructuralCategory.NOISE_ARTIFACT,
                connection_feasibility=ConnectionFeasibility.LOW,
                priority=PriorityLevel.IGNORE,
                created_at=now - timedelta(hours=1),
                connection_hints=[],
                tags=["system", "error"]
            ),
            OrphanNode(
                id="orphan_004",
                node_type="Belief",
                content="Creativity requires both structure and chaos. Too much order stifles innovation, too much chaos produces nothing useful. The sweet spot is a dynamic balance.",
                structural_category=StructuralCategory.TEMPORAL_ISLAND,
                connection_feasibility=ConnectionFeasibility.HIGH,
                priority=PriorityLevel.CRITICAL,
                created_at=now - timedelta(hours=8),
                connection_hints=["Connect to creativity beliefs", "Link to balance principles"],
                tags=["creativity", "balance", "philosophy"]
            ),
            OrphanNode(
                id="orphan_005",
                node_type="Dream",
                content="I dreamt of a library where books wrote themselves. Each book contained the story of someone's life, constantly updating as they lived. I was the librarian.",
                structural_category=StructuralCategory.DREAM_OUTPUT,
                connection_feasibility=ConnectionFeasibility.MEDIUM,
                priority=PriorityLevel.MEDIUM,
                created_at=now - timedelta(hours=12),
                connection_hints=["Connect to dream analysis", "Link to symbolism of libraries"],
                tags=["dream", "symbolism", "library"]
            )
        ]
    
    async def capture_orphan_context(
        self, 
        limit: int = 5,
        include_samples: int = 5
    ) -> OrphanContextSnapshot:
        """
        Capture orphan state for reflection.
        
        Args:
            limit: Maximum orphans to analyze
            include_samples: Number of orphans to include in full
        
        Returns:
            OrphanContextSnapshot with structured orphan information
        """
        orphans = self._mock_orphans[:limit]
        
        # Build snapshot
        snapshot = OrphanContextSnapshot(
            captured_at=datetime.now(),
            total_orphans=len(orphans)
        )
        
        # Categorize orphans
        for orphan in orphans:
            orphan_dict = {
                "id": orphan.id,
                "node_type": orphan.node_type,
                "content": orphan.content,
                "structural_category": orphan.structural_category.value,
                "priority": orphan.priority.value,
                "connection_feasibility": orphan.connection_feasibility.value,
                "tags": orphan.tags
            }
            
            snapshot.recent_orphans.append(orphan_dict)
            
            if orphan.priority == PriorityLevel.CRITICAL:
                snapshot.critical_orphans.append(orphan_dict)
            elif orphan.priority in [PriorityLevel.HIGH, PriorityLevel.MEDIUM]:
                snapshot.high_value_orphans.append(orphan_dict)
        
        # Build type distribution
        for orphan in orphans:
            cat = orphan.structural_category.value
            snapshot.orphan_types_distribution[cat] = \
                snapshot.orphan_types_distribution.get(cat, 0) + 1
        
        # Extract themes
        all_tags = []
        for orphan in orphans:
            all_tags.extend(orphan.tags)
        
        # Find common themes
        from collections import Counter
        tag_counts = Counter(all_tags)
        snapshot.orphan_themes = [tag for tag, count in tag_counts.most_common(5)]
        
        # Generate reflection prompts based on orphans
        snapshot.reflection_prompts = self._generate_reflection_prompts(orphans)
        
        # Generate immediate actions
        snapshot.immediate_actions = self._generate_immediate_actions(orphans)
        
        return snapshot
    
    def _generate_reflection_prompts(self, orphans: List[OrphanNode]) -> List[str]:
        """Generate reflection prompts based on orphan content."""
        prompts = []
        
        # Check for recurring themes
        tags = set()
        for orphan in orphans:
            tags.update(orphan.tags)
        
        if "philosophy" in tags:
            prompts.append("What philosophical themes are emerging in my isolated experiences?")
        
        if "memory" in tags:
            prompts.append("How do these memory fragments relate to my core identity?")
        
        if len([o for o in orphans if o.priority == PriorityLevel.CRITICAL]) > 0:
            prompts.append("What critical insights am I not integrating into my worldview?")
        
        prompts.append("What patterns exist in what fails to connect to my main memory graph?")
        
        return prompts
    
    def _generate_immediate_actions(self, orphans: List[OrphanNode]) -> List[str]:
        """Generate immediate action recommendations."""
        actions = []
        
        critical_count = len([o for o in orphans if o.priority == PriorityLevel.CRITICAL])
        if critical_count > 0:
            actions.append(f"Prioritize integration of {critical_count} critical orphan(s)")
        
        high_feasibility = len([o for o in orphans if o.connection_feasibility == ConnectionFeasibility.HIGH])
        if high_feasibility > 0:
            actions.append(f"Process {high_feasibility} orphan(s) with high connection feasibility")
        
        noise_count = len([o for o in orphans if o.structural_category == StructuralCategory.NOISE_ARTIFACT])
        if noise_count > 0:
            actions.append(f"Review and potentially remove {noise_count} noise artifact(s)")
        
        return actions
    
    async def get_orphan_summary(self) -> Dict[str, Any]:
        """Get a detailed summary of orphan state."""
        snapshot = await self.capture_orphan_context()
        
        return {
            "timestamp": snapshot.captured_at.isoformat(),
            "total_orphans": snapshot.total_orphans,
            "critical_count": len(snapshot.critical_orphans),
            "high_value_count": len(snapshot.high_value_orphans),
            "type_distribution": snapshot.orphan_types_distribution,
            "themes": snapshot.orphan_themes,
            "reflection_prompts": snapshot.reflection_prompts,
            "immediate_actions": snapshot.immediate_actions,
            "orphans": snapshot.recent_orphans
        }


def print_snapshot(snapshot: OrphanContextSnapshot):
    """Print a formatted snapshot display."""
    print(f"\n{'='*70}")
    print(f"ORPHAN READER CAPABILITY - Reading 5 Orphan Nodes")
    print(f"{'='*70}\n")
    
    print("[METADATA]")
    print(f"  Timestamp: {snapshot.captured_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total Orphans: {snapshot.total_orphans}")
    print()
    
    print("[TYPE DISTRIBUTION]")
    for orphan_type, count in sorted(snapshot.orphan_types_distribution.items()):
        bar = "█" * count
        print(f"  {orphan_type:20} {bar} {count}")
    print()
    
    if snapshot.critical_orphans:
        print(f"[CRITICAL ORPHANS ({len(snapshot.critical_orphans)})]")
        for orphan in snapshot.critical_orphans:
            print(f"  [{orphan['id']}] {orphan['node_type']}")
            preview = orphan['content'][:60]
            print(f"    {preview}..." if len(orphan['content']) > 60 else f"    {preview}")
            print(f"    Priority: {orphan['priority'].upper()}")
            print()
    
    print(f"[THEMES]")
    for i, theme in enumerate(snapshot.orphan_themes, 1):
        print(f"  {i}. {theme}")
    print()
    
    print(f"[REFLECTION PROMPTS]")
    for i, prompt in enumerate(snapshot.reflection_prompts, 1):
        print(f"  • {prompt}")
    print()
    
    print(f"[IMMEDIATE ACTIONS]")
    for i, action in enumerate(snapshot.immediate_actions, 1):
        print(f"  • {action}")
    print()
    
    print("[FULL ORPHAN DETAILS]")
    for orphan in snapshot.recent_orphans:
        print(f"\n  ID: {orphan['id']}")
        print(f"  Type: {orphan['node_type']}")
        print(f"  Category: {orphan['structural_category']}")
        print(f"  Priority: {orphan['priority']}")
        print(f"  Connection Feasibility: {orphan['connection_feasibility']}")
        print(f"  Tags: {', '.join(orphan['tags'])}")
        print(f"  Content: {orphan['content']}")
    
    print(f"\n{'='*70}")
    print("ORPHAN READER EXECUTION COMPLETE")
    print(f"{'='*70}\n")


async def main():
    """Main execution function."""
    # Initialize mock reader
    reader = MockOrphanReader()
    
    # Capture orphan context (5 nodes)
    snapshot = await reader.capture_orphan_context(limit=5, include_samples=5)
    
    # Display results
    print_snapshot(snapshot)
    
    # Also output JSON for programmatic access
    summary = await reader.get_orphan_summary()
    print("\n[JSON OUTPUT]")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    from datetime import timedelta
    asyncio.run(main())
