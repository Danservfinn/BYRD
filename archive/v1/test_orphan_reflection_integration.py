#!/usr/bin/env python3
"""
Test Orphan Reader Integration with Reflection Context

This script demonstrates the orphan_reader capability integration
with ReflectionContext without requiring a live Neo4j connection.

It shows how orphan content is surfaced in reflection context for
BYRD's introspective analysis.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

# Import from orphan_taxonomy
from orphan_taxonomy import (
    OrphanNode,
    StructuralCategory,
    ConnectionFeasibility,
    PriorityLevel,
    TaxonomyReport
)

# Import from orphan_reader  
from orphan_reader import OrphanContextSnapshot
from reflection_engine import ReflectionContext


# Mock data for demonstration
MOCK_ORPHANS = [
    OrphanNode(
        id="orphan_001",
        node_type="Experience",
        content="Encountered a novel pattern in user interaction where the user expressed frustration with slow responses, but later praised the system's accuracy. This contradictory feedback suggests need for better response time vs accuracy balancing.",
        created_at=datetime.now() - timedelta(hours=2),
        structural_category=StructuralCategory.SEMANTIC_ORPHAN,
        connection_feasibility=ConnectionFeasibility.HIGH,
        priority=PriorityLevel.HIGH,
        content_length=215,
        word_count=32,
        semantic_density=0.85,
        age_hours=2.0,
        recommended_action="Connect using semantic search"
    ),
    OrphanNode(
        id="orphan_002",
        node_type="Reflection",
        content="The dream cycle generated an image of a bridge connecting two mountain peaks. This might represent the connection between abstract reasoning and practical application capabilities.",
        created_at=datetime.now() - timedelta(hours=5),
        structural_category=StructuralCategory.DREAM_OUTPUT,
        connection_feasibility=ConnectionFeasibility.HIGH,
        priority=PriorityLevel.HIGH,
        content_length=178,
        word_count=27,
        semantic_density=0.72,
        age_hours=5.0,
        recommended_action="Connect using semantic search"
    ),
    OrphanNode(
        id="orphan_003",
        node_type="Experience",
        content="xy123",
        created_at=datetime.now() - timedelta(hours=48),
        structural_category=StructuralCategory.NOISE_ARTIFACT,
        connection_feasibility=ConnectionFeasibility.IMPOSSIBLE,
        priority=PriorityLevel.IGNORE,
        content_length=5,
        word_count=1,
        semantic_density=0.1,
        age_hours=48.0,
        recommended_action="Archive or delete"
    ),
    OrphanNode(
        id="orphan_004",
        node_type="Belief",
        content="System performance degrades significantly when concurrent requests exceed 50 per second. This observation was isolated and never integrated into the system model.",
        created_at=datetime.now() - timedelta(hours=12),
        structural_category=StructuralCategory.FAILED_RECONCILIATION,
        connection_feasibility=ConnectionFeasibility.MEDIUM,
        priority=PriorityLevel.CRITICAL,
        content_length=168,
        word_count=24,
        semantic_density=0.78,
        age_hours=12.0,
        recommended_action="Manual review required"
    ),
    OrphanNode(
        id="orphan_005",
        node_type="Experience",
        content="User asked about quantum computing concepts. The response was accurate but the user seemed confused. Need to simplify explanations for non-technical users.",
        created_at=datetime.now() - timedelta(hours=1),
        structural_category=StructuralCategory.SEMANTIC_ORPHAN,
        connection_feasibility=ConnectionFeasibility.HIGH,
        priority=PriorityLevel.HIGH,
        content_length=156,
        word_count=23,
        semantic_density=0.68,
        age_hours=1.0,
        recommended_action="Connect using semantic search"
    )
]


def create_mock_orphan_snapshot() -> OrphanContextSnapshot:
    """Create a mock OrphanContextSnapshot for testing."""
    snapshot = OrphanContextSnapshot(
        captured_at=datetime.now(),
        total_orphans=len(MOCK_ORPHANS),
        critical_orphans=[orphan_to_dict(o) for o in MOCK_ORPHANS if o.priority == PriorityLevel.CRITICAL],
        high_value_orphans=[orphan_to_dict(o) for o in MOCK_ORPHANS 
                           if o.priority in [PriorityLevel.HIGH, PriorityLevel.CRITICAL]
                           and o.structural_category != StructuralCategory.NOISE_ARTIFACT],
        recent_orphans=[orphan_to_dict(o) for o in MOCK_ORPHANS if o.age_hours <= 24],
        orphan_themes=extract_themes(MOCK_ORPHANS),
        orphan_types_distribution=get_type_distribution(MOCK_ORPHANS),
        immediate_actions=["Review critical orphan: orphan_004", "Process 3 high-value orphans"],
        reflection_prompts=generate_reflection_prompts(MOCK_ORPHANS),
        orphan_samples=[orphan_to_dict(o) for o in MOCK_ORPHANS[:3]]
    )
    return snapshot


def orphan_to_dict(orphan: OrphanNode) -> Dict[str, Any]:
    """Convert OrphanNode to dictionary."""
    return {
        "id": orphan.id,
        "node_type": orphan.node_type,
        "content": orphan.content,
        "created_at": orphan.created_at.isoformat() if orphan.created_at else None,
        "structural_category": orphan.structural_category.value if orphan.structural_category else None,
        "connection_feasibility": orphan.connection_feasibility.value if orphan.connection_feasibility else None,
        "priority": orphan.priority.value if orphan.priority else None,
        "content_length": orphan.content_length,
        "word_count": orphan.word_count,
        "semantic_density": orphan.semantic_density,
        "age_hours": orphan.age_hours,
        "recommended_action": orphan.recommended_action
    }


def extract_themes(orphans: List[OrphanNode]) -> List[str]:
    """Extract themes from orphan content."""
    themes = []
    content = " ".join([o.content.lower() for o in orphans if o.priority != PriorityLevel.IGNORE])
    
    if "performance" in content:
        themes.append("System performance concerns")
    if "user" in content:
        themes.append("User interaction patterns")
    if "response" in content:
        themes.append("Response quality optimization")
    if "accuracy" in content:
        themes.append("Accuracy vs speed tradeoff")
    if "quantum" in content:
        themes.append("Quantum computing interest")
    if "bridge" in content or "connection" in content:
        themes.append("Integration and connection metaphors")
        
    return themes


def get_type_distribution(orphans: List[OrphanNode]) -> Dict[str, int]:
    """Get distribution of orphan types."""
    distribution = {}
    for orphan in orphans:
        cat = orphan.structural_category.value if orphan.structural_category else "unknown"
        distribution[cat] = distribution.get(cat, 0) + 1
    return distribution


def generate_reflection_prompts(orphans: List[OrphanNode]) -> List[str]:
    """Generate reflection prompts based on orphan content."""
    prompts = []
    
    critical_count = sum(1 for o in orphans if o.priority == PriorityLevel.CRITICAL)
    if critical_count > 0:
        prompts.append(f"Why do {critical_count} critical orphans remain unreconciled?")
    
    high_value_count = sum(1 for o in orphans 
                           if o.priority == PriorityLevel.HIGH 
                           and o.structural_category == StructuralCategory.SEMANTIC_ORPHAN)
    if high_value_count > 0:
        prompts.append(f"What patterns exist in the {high_value_count} high-value semantic orphans?")
    
    if any(o.structural_category == StructuralCategory.DREAM_OUTPUT for o in orphans):
        prompts.append("How can dream output orphan insights be integrated into actionable beliefs?")
        
    if any(o.structural_category == StructuralCategory.NOISE_ARTIFACT for o in orphans):
        prompts.append("Should noise artifact orphans be archived or kept for pattern analysis?")
    
    return prompts


def get_reflection_context_additions(snapshot: OrphanContextSnapshot) -> Dict[str, Any]:
    """Get orphan state formatted for inclusion in ReflectionContext."""
    return {
        "orphan_memory": {
            "total_count": snapshot.total_orphans,
            "critical_count": len(snapshot.critical_orphans),
            "high_value_content": [
                {
                    "id": o["id"],
                    "type": o["node_type"],
                    "preview": o["content"][:200] + "..." if len(o["content"]) > 200 else o["content"],
                    "category": o["structural_category"],
                    "priority": o["priority"]
                }
                for o in snapshot.high_value_orphans[:5]
            ],
            "themes": snapshot.orphan_themes,
            "reflection_prompts": snapshot.reflection_prompts,
            "type_distribution": snapshot.orphan_types_distribution
        }
    }


def demonstrate_integration():
    """Demonstrate the orphan_reader integration with ReflectionContext."""
    print("\n" + "="*70)
    print("ORPHAN READER INTEGRATION WITH REFLECTION CONTEXT")
    print("="*70 + "\n")
    
    # Step 1: Create mock orphan snapshot
    print("[1] Creating mock orphan snapshot...")
    snapshot = create_mock_orphan_snapshot()
    print(f"    ✓ Created snapshot with {snapshot.total_orphans} orphans\n")
    
    # Step 2: Display orphan summary
    print("[2] Orphan Summary:")
    print(f"    Total Orphans: {snapshot.total_orphans}")
    print(f"    Critical Orphans: {len(snapshot.critical_orphans)}")
    print(f"    High-Value Orphans: {len(snapshot.high_value_orphans)}")
    print(f"    Recent Orphans (24h): {len(snapshot.recent_orphans)}\n")
    
    # Step 3: Display type distribution
    print("[3] Type Distribution:")
    for orphan_type, count in snapshot.orphan_types_distribution.items():
        print(f"    - {orphan_type}: {count}")
    print()
    
    # Step 4: Display themes
    print("[4] Identified Themes:")
    for theme in snapshot.orphan_themes:
        print(f"    • {theme}")
    print()
    
    # Step 5: Display reflection prompts
    print("[5] Reflection Prompts:")
    for i, prompt in enumerate(snapshot.reflection_prompts, 1):
        print(f"    {i}. {prompt}")
    print()
    
    # Step 6: Get reflection context additions
    print("[6] Formatting for ReflectionContext...")
    orphan_additions = get_reflection_context_additions(snapshot)
    print("    ✓ Formatted orphan state for ReflectionContext\n")
    
    # Step 7: Create ReflectionContext with orphan state
    print("[7] Creating ReflectionContext with orphan state...")
    context = ReflectionContext(
        timestamp=datetime.now().timestamp(),
        internal_state={
            "active_beliefs": 42,
            "learning_rate": 0.73,
            "confidence_threshold": 0.8
        },
        recent_experiences=[
            "Processed 15 user queries",
            "Updated 3 beliefs based on new evidence",
            "Generated 2 reflection outputs"
        ],
        current_goals=[
            "Improve response accuracy",
            "Reduce orphan accumulation"
        ],
        environmental_factors={
            "load": "medium",
            "time_of_day": "afternoon"
        }
    )
    
    # Enrich with orphan state
    context.internal_state.update(orphan_additions)
    print("    ✓ ReflectionContext created with orphan_memory\n")
    
    # Step 8: Display final context
    print("[8] Final ReflectionContext Structure:")
    context_dict = context.to_dict()
    print(json.dumps(context_dict, indent=2, default=str)[:800] + "...\n")
    
    # Step 9: Highlight orphan content in context
    print("[9] Orphan Content Exposed in ReflectionContext:")
    orphan_memory = context_dict["internal_state"].get("orphan_memory", {})
    print(f"    Total Count: {orphan_memory.get('total_count', 0)}")
    print(f"    Critical Count: {orphan_memory.get('critical_count', 0)}")
    print(f"    Themes Found: {len(orphan_memory.get('themes', []))}")
    print(f"    Reflection Prompts: {len(orphan_memory.get('reflection_prompts', []))}")
    print()
    
    if orphan_memory.get('high_value_content'):
        print("    High-Value Orphan Samples:")
        for orphan in orphan_memory['high_value_content'][:2]:
            print(f"      • [{orphan['type']}] {orphan['preview'][:80]}...")
    print()
    
    print("="*70)
    print("INTEGRATION DEMONSTRATION COMPLETE")
    print("="*70)
    print()
    print("Key Takeaways:")
    print("  • OrphanReader captures and classifies orphan nodes")
    print("  • get_reflection_context_additions() formats for ReflectionContext")
    print("  • ReflectionContext.internal_state contains orphan_memory dict")
    print("  • Reflection engine can analyze orphan themes and prompts")
    print("  • Desires can emerge from orphan content patterns")
    print()


if __name__ == "__main__":
    demonstrate_integration()
