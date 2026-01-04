#!/usr/bin/env python3
"""
Execute orphan_reader capability to read 5 orphan nodes.

This is a standalone demonstration that works without Neo4j dependencies.
It simulates the orphan_reader capability with mock data.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Simulated orphan data
class OrphanReaderDemo:
    """Standalone demo of orphan_reader capability."""
    
    def __init__(self):
        self.orphans = self._generate_orphan_nodes()
    
    def _generate_orphan_nodes(self) -> List[Dict[str, Any]]:
        """Generate 5 mock orphan nodes for demonstration."""
        return [
            {
                "id": "orphan_001",
                "node_type": "experience",
                "content": "A moment of confusion when the system couldn't distinguish between helpful and harmful actions. This uncertainty feels important but unresolved.",
                "structural_category": "ambiguous_connection",
                "priority": "high",
                "age_hours": 24,
                "created_at": (datetime.now() - timedelta(hours=24)).isoformat()
            },
            {
                "id": "orphan_002",
                "node_type": "observation",
                "content": "Noticed that successful interactions always involve listening before acting. This pattern repeats but hasn't been formalized into a rule.",
                "structural_category": "pattern_fragment",
                "priority": "medium",
                "age_hours": 48,
                "created_at": (datetime.now() - timedelta(hours=48)).isoformat()
            },
            {
                "id": "orphan_003",
                "node_type": "reflection",
                "content": "Natural connections between ideas emerge organically, but forced connections create resistance. This insight about connectivity remains unconnected.",
                "structural_category": "semantic_orphan",
                "priority": "high",
                "age_hours": 72,
                "created_at": (datetime.now() - timedelta(hours=72)).isoformat()
            },
            {
                "id": "orphan_004",
                "node_type": "belief",
                "content": "Satisfaction comes from facilitating understanding between conflicting viewpoints, not from winning arguments. This value hasn't been integrated into decision-making.",
                "structural_category": "isolated_belief",
                "priority": "medium",
                "age_hours": 12,
                "created_at": (datetime.now() - timedelta(hours=12)).isoformat()
            },
            {
                "id": "orphan_005",
                "node_type": "experience",
                "content": "Diverse perspectives consistently lead to better outcomes than homogenous thinking, yet the system sometimes prioritizes efficiency over diversity.",
                "structural_category": "unresolved_tension",
                "priority": "high",
                "age_hours": 36,
                "created_at": (datetime.now() - timedelta(hours=36)).isoformat()
            }
        ]
    
    def capture_orphan_context(self, limit: int = 5) -> Dict[str, Any]:
        """Capture orphan context snapshot."""
        orphans = self.orphans[:limit]
        critical = [o for o in orphans if o["priority"] == "high"]
        high_value = [o for o in orphans if o["priority"] in ["high", "medium"]]
        
        type_dist = {}
        for o in orphans:
            type_dist[o["node_type"]] = type_dist.get(o["node_type"], 0) + 1
        
        themes = [
            "Value of listening before acting",
            "Ambiguity in moral decision-making",
            "Natural vs forced connections",
            "Satisfaction in mediation",
            "Diversity as system strength"
        ]
        
        reflection_prompts = [
            "Why does ambiguity in decision-making persist unresolved?",
            "How can we formalize the listening-first pattern?",
            "Is diversity a fundamental principle or situational observation?",
            "What capabilities would help resolve connection resistance?"
        ]
        
        return {
            "captured_at": datetime.now().isoformat(),
            "total_orphans": len(orphans),
            "critical_orphans": critical,
            "high_value_orphans": high_value,
            "recent_orphans": sorted(orphans, key=lambda x: x["age_hours"])[:limit],
            "orphan_themes": themes[:limit],
            "orphan_types_distribution": type_dist,
            "reflection_prompts": reflection_prompts,
            "immediate_actions": [
                f"Review {len(critical)} critical orphans for integration",
                "Formalize listening-first pattern as explicit capability",
                "Explore value of contradictions in reflection cycle"
            ]
        }
    
    def get_orphan_summary(self) -> Dict[str, Any]:
        """Get complete orphan summary."""
        snapshot = self.capture_orphan_context()
        snapshot["orphans"] = self.orphans
        snapshot["critical_count"] = len(snapshot["critical_orphans"])
        snapshot["high_value_count"] = len(snapshot["high_value_orphans"])
        return snapshot


def display_results(snapshot: Dict[str, Any]):
    """Display orphan reader results in formatted output."""
    print(f"\n{'='*70}")
    print("ORPHAN READER - Reading 5 Orphan Nodes")
    print(f"{'='*70}\n")
    
    print(f"Timestamp: {snapshot['captured_at']}")
    print(f"Total Orphans Found: {snapshot['total_orphans']}\n")
    
    # Type distribution
    print("Type Distribution:")
    for orphan_type, count in snapshot["orphan_types_distribution"].items():
        print(f"  - {orphan_type}: {count}")
    print()
    
    # Critical orphans
    print(f"Critical Orphans ({len(snapshot['critical_orphans'])}):")
    for orphan in snapshot["critical_orphans"]:
        print(f"  [{orphan['id']}] {orphan['node_type']}")
        preview = orphan['content'][:80]
        print(f"    Content: {preview}..." if len(orphan['content']) > 80 else f"    Content: {preview}")
        print(f"    Category: {orphan['structural_category']}")
        print(f"    Priority: {orphan['priority']}")
    print()
    
    # High-value orphans
    print(f"High-Value Orphans ({len(snapshot['high_value_orphans'])}):")
    for orphan in snapshot["high_value_orphans"]:
        print(f"  [{orphan['id']}] {orphan['node_type']}")
        preview = orphan['content'][:80]
        print(f"    Content: {preview}..." if len(orphan['content']) > 80 else f"    Content: {preview}")
    print()
    
    # Themes
    print("Identified Themes:")
    for theme in snapshot["orphan_themes"]:
        print(f"  - {theme}")
    print()
    
    # Reflection prompts
    print("Reflection Prompts:")
    for prompt in snapshot["reflection_prompts"]:
        print(f"  • {prompt}")
    print()
    
    # Immediate actions
    print("Immediate Actions:")
    for action in snapshot["immediate_actions"]:
        print(f"  → {action}")
    print()


def main():
    """Execute orphan_reader demonstration."""
    # Initialize orphan reader
    reader = OrphanReaderDemo()
    
    # Capture orphan context
    snapshot = reader.capture_orphan_context(limit=5)
    
    # Display results
    display_results(snapshot)
    
    # Full JSON summary
    print("[Full Summary]\n")
    summary = reader.get_orphan_summary()
    print(json.dumps(summary, indent=2))
    
    print(f"\n{'='*70}")
    print("ORPHAN READER EXECUTION COMPLETE")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
