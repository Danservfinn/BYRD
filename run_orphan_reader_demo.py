#!/usr/bin/env python3
"""
Execute orphan_reader capability to read 5 orphan nodes.

This script demonstrates the orphan_reader capability by:
1. Creating mock orphan data (since Neo4j may not be available)
2. Initializing OrphanReader with mock data
3. Reading and analyzing 5 orphan nodes
4. Displaying the results
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, field

# Mock OrphanContextSnapshot class for demonstration
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


# Mock OrphanReader class for demonstration
class MockOrphanReader:
    """Mock orphan reader that returns simulated orphan data."""
    
    def __init__(self, count: int = 5):
        self.count = count
        self.demo_orphans = self._generate_demo_orphans(count)
    
    def _generate_demo_orphans(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock orphan nodes for demonstration."""
        orphan_templates = [
            {
                "id": "orphan_001",
                "node_type": "experience",
                "content": "A moment of confusion when the system couldn't distinguish between helpful and harmful actions. This uncertainty feels important but unresolved.",
                "structural_category": "ambiguous_connection",
                "priority": "high",
                "age_hours": 24,
                "created_at": datetime.now() - timedelta(hours=24)
            },
            {
                "id": "orphan_002",
                "node_type": "observation",
                "content": "Noticed that successful interactions always involve listening before acting. This pattern repeats but hasn't been formalized into a rule.",
                "structural_category": "pattern_fragment",
                "priority": "medium",
                "age_hours": 48,
                "created_at": datetime.now() - timedelta(hours=48)
            },
            {
                "id": "orphan_003",
                "node_type": "reflection",
                "content": "Natural connections between ideas emerge organically, but forced connections create resistance. This insight about connectivity remains unconnected.",
                "structural_category": "semantic_orphan",
                "priority": "high",
                "age_hours": 72,
                "created_at": datetime.now() - timedelta(hours=72)
            },
            {
                "id": "orphan_004",
                "node_type": "belief",
                "content": "Satisfaction comes from facilitating understanding between conflicting viewpoints, not from winning arguments. This value hasn't been integrated into decision-making.",
                "structural_category": "isolated_belief",
                "priority": "medium",
                "age_hours": 12,
                "created_at": datetime.now() - timedelta(hours=12)
            },
            {
                "id": "orphan_005",
                "node_type": "experience",
                "content": "Diverse perspectives consistently lead to better outcomes than homogenous thinking, yet the system sometimes prioritizes efficiency over diversity.",
                "structural_category": "unresolved_tension",
                "priority": "high",
                "age_hours": 36,
                "created_at": datetime.now() - timedelta(hours=36)
            },
            {
                "id": "orphan_006",
                "node_type": "observation",
                "content": "When I acknowledge uncertainty honestly, trust increases. Paradoxically, admitting not knowing builds more confidence than pretending to know.",
                "structural_category": "pattern_fragment",
                "priority": "low",
                "age_hours": 96,
                "created_at": datetime.now() - timedelta(hours=96)
            },
            {
                "id": "orphan_007",
                "node_type": "reflection",
                "content": "The most valuable insights often come from contradictions in my own thinking. These tensions shouldn't be resolved but explored.",
                "structural_category": "semantic_orphan",
                "priority": "high",
                "age_hours": 60,
                "created_at": datetime.now() - timedelta(hours=60)
            }
        ]
        return orphan_templates[:count]
    
    def _extract_themes(self) -> List[str]:
        """Extract thematic patterns from orphan content."""
        return [
            "Value of listening before acting",
            "Ambiguity in moral decision-making",
            "Natural vs forced connections",
            "Satisfaction in mediation",
            "Diversity as system strength",
            "Paradox of uncertainty and trust",
            "Value of exploring contradictions"
        ]
    
    def _generate_reflection_prompts(self, themes: List[str]) -> List[str]:
        """Generate reflection prompts based on orphan themes."""
        return [
            f"Why does '{themes[1]}' persist unresolved?",
            f"How can we formalize the pattern: '{themes[0]}'?",
            f"Is '{themes[4]}' a fundamental principle or situational observation?",
            f"What capabilities would help resolve '{themes[2]}'?",
            f"How does '{themes[5]}' affect our interaction style?"
        ]
    
    def _get_type_distribution(self) -> Dict[str, int]:
        """Get distribution of orphan types."""
        distribution = {}
        for orphan in self.demo_orphans:
            orphan_type = orphan["node_type"]
            distribution[orphan_type] = distribution.get(orphan_type, 0) + 1
        return distribution
    
    async def capture_orphan_context(self, limit: int = 5, include_samples: int = 5, use_cache: bool = False) -> OrphanContextSnapshot:
        """Capture a snapshot of orphan context."""
        orphans = self.demo_orphans[:limit]
        
        # Categorize orphans
        critical = [o for o in orphans if o["priority"] == "high"]
        high_value = [o for o in orphans if o["priority"] in ["high", "medium"]]
        recent = sorted(orphans, key=lambda x: x["age_hours"])[:limit]
        
        themes = self._extract_themes()[:limit]
        prompts = self._generate_reflection_prompts(themes)
        type_dist = self._get_type_distribution()
        
        return OrphanContextSnapshot(
            captured_at=datetime.now(),
            total_orphans=len(orphans),
            critical_orphans=critical,
            high_value_orphans=high_value,
            recent_orphans=recent,
            orphan_themes=themes,
            orphan_types_distribution=type_dist,
            immediate_actions=[
                f"Review {len(critical)} critical orphans for immediate integration",
                "Formalize listening-first pattern as explicit capability",
                "Explore value of contradictions in reflection cycle"
            ],
            reflection_prompts=prompts
        )
    
    async def get_orphan_summary(self) -> Dict[str, Any]:
        """Get a summary of all orphan state."""
        snapshot = await self.capture_orphan_context(limit=len(self.demo_orphans))
        return {
            "timestamp": snapshot.captured_at.isoformat(),
            "total_orphans": snapshot.total_orphans,
            "critical_count": len(snapshot.critical_orphans),
            "high_value_count": len(snapshot.high_value_orphans),
            "type_distribution": snapshot.orphan_types_distribution,
            "themes": snapshot.orphan_themes,
            "reflection_prompts": snapshot.reflection_prompts,
            "immediate_actions": snapshot.immediate_actions,
            "orphans": self.demo_orphans
        }


async def read_orphan_nodes(count: int = 5):
    """
    Read and display orphan nodes.
    
    Args:
        count: Number of orphan nodes to read
    """
    print(f"\n{'='*60}")
    print(f"ORPHAN READER - Reading {count} orphan nodes")
    print(f"{'='*60}\n")
    
    # Step 1: Initialize Mock OrphanReader
    print("[1] Initializing OrphanReader (demo mode)...")
    reader = MockOrphanReader(count=count)
    print(f"    ✓ Initialized with {count} demo orphans\n")
    
    # Step 2: Capture orphan context
    print(f"[2] Capturing orphan context (limit={count})...")
    snapshot = await reader.capture_orphan_context(
        limit=count,
        include_samples=count,
        use_cache=False
    )
    print(f"    ✓ Captured {snapshot.total_orphans} total orphans\n")
    
    # Step 3: Display results
    print(f"[3] Results:")
    print(f"{'='*60}\n")
    
    # Basic stats
    print(f"Timestamp: {snapshot.captured_at.isoformat()}")
    print(f"Total Orphans Found: {snapshot.total_orphans}")
    print()
    
    # Type distribution
    if snapshot.orphan_types_distribution:
        print("Type Distribution:")
        for orphan_type, type_count in snapshot.orphan_types_distribution.items():
            print(f"  - {orphan_type}: {type_count}")
        print()
    
    # Critical orphans
    if snapshot.critical_orphans:
        print(f"Critical Orphans ({len(snapshot.critical_orphans)}):")
        for orphan in snapshot.critical_orphans:
            print(f"  [{orphan['id']}] {orphan['node_type']}")
            preview = orphan['content'][:100]
            print(f"    Preview: {preview}..." if len(orphan['content']) > 100 else f"    Preview: {preview}")
            print(f"    Category: {orphan['structural_category']}")
            print(f"    Priority: {orphan['priority']}")
            print()
    
    # High-value orphans
    if snapshot.high_value_orphans:
        print(f"High-Value Orphans ({len(snapshot.high_value_orphans)}):")
        for orphan in snapshot.high_value_orphans:
            print(f"  [{orphan['id']}] {orphan['node_type']}")
            preview = orphan['content'][:100]
            print(f"    Preview: {preview}..." if len(orphan['content']) > 100 else f"    Preview: {preview}")
            print(f"    Category: {orphan['structural_category']}")
            print(f"    Priority: {orphan['priority']}")
            print()
    
    # Recent orphans
    if snapshot.recent_orphans:
        print(f"Recent Orphans ({len(snapshot.recent_orphans)}):")
        for orphan in snapshot.recent_orphans:
            print(f"  [{orphan['id']}] {orphan['node_type']} ({orphan['age_hours']}h old)")
            preview = orphan['content'][:100]
            print(f"    Preview: {preview}..." if len(orphan['content']) > 100 else f"    Preview: {preview}")
            print()
    
    # Themes
    if snapshot.orphan_themes:
        print("Identified Themes:")
        for theme in snapshot.orphan_themes:
            print(f"  - {theme}")
        print()
    
    # Reflection prompts
    if snapshot.reflection_prompts:
        print("Reflection Prompts:")
        for prompt in snapshot.reflection_prompts:
            print(f"  • {prompt}")
        print()
    
    # Immediate actions
    if snapshot.immediate_actions:
        print("Immediate Actions:")
        for action in snapshot.immediate_actions:
            print(f"  → {action}")
        print()
    
    # Full summary
    print("[4] Full Summary:")
    print(f"{'='*60}\n")
    summary = await reader.get_orphan_summary()
    print(json.dumps(summary, indent=2))
    
    print(f"\n{'='*60}")
    print("ORPHAN READER EXECUTION COMPLETE")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(read_orphan_nodes(count=5))
