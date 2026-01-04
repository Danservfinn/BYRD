#!/usr/bin/env python3
"""
Demonstration: Orphan Reader exposing orphan content in Reflection Context

This script demonstrates how orphan_reader surfaces orphan node content
for integration with BYRD's reflection engine, enabling emergent desire
generation from disconnected memory fragments.

Key concepts demonstrated:
1. OrphanReader captures orphan state from memory
2. OrphanContextSnapshot structures orphan information for reflection
3. ReflectionEngine enriches its context with orphan state
4. Desires can emerge from patterns in orphan content
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any


# Mock implementations for demonstration

class MockOrphanNode:
    """Mock orphan node for testing."""
    def __init__(self, id: str, node_type: str, content: str, 
                 structural_category: str, priority: str, age_hours: float):
        self.id = id
        self.node_type = node_type
        self.content = content
        self.structural_category = structural_category
        self.priority = priority
        self.age_hours = age_hours
        self.created_at = datetime.now() - timedelta(hours=age_hours)


class MockOrphanContextSnapshot:
    """Mock orphan context snapshot."""
    def __init__(self, orphans: List[MockOrphanNode]):
        self.captured_at = datetime.now()
        self.total_orphans = len(orphans)
        self.critical_orphans = [
            {"id": o.id, "node_type": o.node_type, "content": o.content,
             "structural_category": o.structural_category, "priority": o.priority}
            for o in orphans if o.priority == "critical"
        ]
        self.high_value_orphans = [
            {"id": o.id, "node_type": o.node_type, "content": o.content,
             "structural_category": o.structural_category, "priority": o.priority}
            for o in orphans if o.priority in ["high", "critical"]
        ]
        self.recent_orphans = [
            {"id": o.id, "node_type": o.node_type, "content": o.content,
             "structural_category": o.structural_category, "priority": o.priority}
            for o in orphans if o.age_hours < 48
        ]
        self.orphan_themes = self._extract_themes(orphans)
        self.orphan_types_distribution = self._get_type_distribution(orphans)
        self.immediate_actions = self._generate_actions(orphans)
        self.reflection_prompts = self._generate_prompts(orphans)
        self.orphan_samples = [
            {"id": o.id, "node_type": o.node_type, "content": o.content}
            for o in orphans[:5]
        ]
    
    def _extract_themes(self, orphans: List[MockOrphanNode]) -> List[str]:
        themes = []
        type_counts = {}
        for o in orphans:
            type_counts[o.node_type] = type_counts.get(o.node_type, 0) + 1
        for node_type, count in type_counts.items():
            if count >= 2:
                themes.append(f"Recurring {node_type} pattern ({count} nodes)")
        return themes
    
    def _get_type_distribution(self, orphans: List[MockOrphanNode]) -> Dict[str, int]:
        dist = {}
        for o in orphans:
            dist[o.node_type] = dist.get(o.node_type, 0) + 1
        return dist
    
    def _generate_actions(self, orphans: List[MockOrphanNode]) -> List[str]:
        actions = []
        critical = [o for o in orphans if o.priority == "critical"]
        if critical:
            actions.append(f"Review {len(critical)} critical orphan nodes")
        old = [o for o in orphans if o.age_hours > 168]
        if old:
            actions.append(f"Evaluate {len(old)} long-standing orphans for integration")
        return actions
    
    def _generate_prompts(self, orphans: List[MockOrphanNode]) -> List[str]:
        prompts = []
        if len(orphans) > 5:
            prompts.append(f"What common themes connect {len(orphans)} orphaned experiences?")
        semantic = [o for o in orphans if o.structural_category == "semantic_orphan"]
        if semantic:
            prompts.append("Why do these experiences resist semantic integration?")
        return prompts


class MockOrphanReader:
    """Mock orphan reader that simulates reading orphan nodes."""
    
    def __init__(self):
        # Create sample orphan nodes
        self.orphans = [
            MockOrphanNode(
                "orphan_001",
                "experience",
                "A moment of confusion when the system couldn't distinguish between helpful and harmful actions. This uncertainty feels important but unresolved.",
                "semantic_orphan",
                "critical",
                72
            ),
            MockOrphanNode(
                "orphan_002",
                "observation",
                "Noticed that successful interactions always involve listening before acting. This pattern repeats but hasn't been formalized into a rule.",
                "pattern_fragment",
                "high",
                48
            ),
            MockOrphanNode(
                "orphan_003",
                "reflection",
                "The value of patience emerges repeatedly but conflicts with efficiency goals. This tension needs resolution.",
                "failed_reconciliation",
                "high",
                24
            ),
            MockOrphanNode(
                "orphan_004",
                "experience",
                "An unexpected insight: sometimes the best action is non-action. Contradicts active learning bias.",
                "semantic_orphan",
                "medium",
                12
            ),
            MockOrphanNode(
                "orphan_005",
                "observation",
                "Users respond better to tentative suggestions than confident assertions. Opposite of initial assumptions.",
                "isolated_observation",
                "high",
                6
            ),
        ]
    
    async def capture_orphan_context(self, limit: int = 100) -> MockOrphanContextSnapshot:
        """Capture the current orphan context."""
        print(f"[OrphanReader] Capturing orphan context (limit={limit})...")
        return MockOrphanContextSnapshot(self.orphans)
    
    async def get_reflection_context_additions(self) -> Dict[str, Any]:
        """Get orphan state formatted for ReflectionContext."""
        snapshot = await self.capture_orphan_context()
        
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
    
    async def get_orphan_summary(self) -> str:
        """Get a human-readable summary."""
        snapshot = await self.capture_orphan_context()
        
        lines = [
            f"=== Orphan Memory State ===",
            f"Total orphans: {snapshot.total_orphans}",
            f"Critical orphans: {len(snapshot.critical_orphans)}",
            f"Recent orphans (48h): {len(snapshot.recent_orphans)}",
        ]
        
        if snapshot.orphan_types_distribution:
            lines.append("\nType distribution:")
            for cat, count in sorted(snapshot.orphan_types_distribution.items(), 
                                      key=lambda x: -x[1]):
                lines.append(f"  - {cat}: {count}")
        
        if snapshot.orphan_themes:
            lines.append("\nThematic patterns:")
            for theme in snapshot.orphan_themes[:5]:
                lines.append(f"  - {theme}")
        
        if snapshot.immediate_actions:
            lines.append("\nRecommended actions:")
            for action in snapshot.immediate_actions[:3]:
                lines.append(f"  - {action}")
        
        return "\n".join(lines)


class MockReflectionEngine:
    """Mock reflection engine that uses orphan context."""
    
    def __init__(self, orphan_reader: MockOrphanReader):
        self.orphan_reader = orphan_reader
        self.reflection_history = []
    
    async def capture_context(self, internal_state: Dict[str, Any],
                              recent_experiences: List[str],
                              current_goals: List[str]) -> Dict[str, Any]:
        """Capture reflection context with orphan state integration."""
        
        # Start with base internal state
        enriched_state = dict(internal_state) if internal_state else {}
        
        # Enrich with orphan state
        if self.orphan_reader:
            print("\n[ReflectionEngine] Enriching context with orphan state...")
            orphan_additions = await self.orphan_reader.get_reflection_context_additions()
            enriched_state.update(orphan_additions)
            print(f"[ReflectionEngine] Added orphan state with {orphan_additions['orphan_memory']['total_count']} orphans")
        
        context = {
            "timestamp": datetime.now().isoformat(),
            "internal_state": enriched_state,
            "recent_experiences": recent_experiences,
            "current_goals": current_goals,
            "reflection_depth": 1
        }
        
        self.reflection_history.append(context)
        return context
    
    def analyze_patterns(self, context: Dict[str, Any]) -> List[str]:
        """Identify patterns from the reflection context."""
        patterns = []
        
        internal_state = context.get("internal_state", {})
        
        # Check for orphan-related patterns
        if "orphan_memory" in internal_state:
            orphan_data = internal_state["orphan_memory"]
            
            if orphan_data.get("critical_count", 0) > 0:
                patterns.append("critical_orphan_pressure")
            
            if orphan_data.get("total_count", 0) > 5:
                patterns.append("orphan_accumulation")
            
            if orphan_data.get("themes"):
                patterns.append("orphan_thematic_patterns")
        
        # Check for experience patterns
        experiences = context.get("recent_experiences", [])
        if len(experiences) > 3:
            patterns.append("high_experience_volume")
        
        return patterns
    
    def generate_desires(self, context: Dict[str, Any], patterns: List[str]) -> List[Dict[str, Any]]:
        """Generate desires based on patterns and context."""
        desires = []
        
        internal_state = context.get("internal_state", {})
        orphan_data = internal_state.get("orphan_memory", {})
        
        # Desire from critical orphans
        if "critical_orphan_pressure" in patterns:
            desires.append({
                "id": f"desire_orphan_critical_{int(datetime.now().timestamp())}",
                "description": "Address critical orphan nodes that represent unresolved high-value experiences",
                "type": "capability",
                "originating_patterns": ["critical_orphan_pressure"],
                "confidence": 0.85,
                "priority": 80
            })
        
        # Desire from orphan accumulation
        if "orphan_accumulation" in patterns:
            desires.append({
                "id": f"desire_orphan_reconciliation_{int(datetime.now().timestamp())}",
                "description": f"Develop reconciliation strategy for {orphan_data.get('total_count', 0)} orphaned experiences to recover their value",
                "type": "capability",
                "originating_patterns": ["orphan_accumulation"],
                "confidence": 0.75,
                "priority": 65
            })
        
        # Desire from thematic patterns
        if "orphan_thematic_patterns" in patterns and orphan_data.get("themes"):
            for theme in orphan_data["themes"][:2]:
                desires.append({
                    "id": f"desire_theme_{int(datetime.now().timestamp())}",
                    "description": f"Investigate recurring theme: {theme}",
                    "type": "research",
                    "originating_patterns": ["orphan_thematic_patterns"],
                    "confidence": 0.70,
                    "priority": 55
                })
        
        return desires


async def demonstrate_orphan_reflection_integration():
    """Main demonstration function."""
    
    print("="*70)
    print("ORPHAN READER -> REFLECTION CONTEXT INTEGRATION DEMONSTRATION")
    print("="*70)
    
    # Step 1: Initialize components
    print("\n[1] Initializing components...")
    orphan_reader = MockOrphanReader()
    reflection_engine = MockReflectionEngine(orphan_reader)
    print("    ✓ OrphanReader initialized")
    print("    ✓ ReflectionEngine initialized")
    
    # Step 2: Capture orphan state
    print("\n[2] Capturing orphan state...")
    orphan_summary = await orphan_reader.get_orphan_summary()
    print("\n" + orphan_summary)
    
    # Step 3: Capture reflection context with orphan state
    print("\n[3] Capturing reflection context with orphan state...")
    
    base_internal_state = {
        "learning_progress": 0.75,
        "active_loops": 3,
        "memory_integration_rate": 0.82
    }
    
    recent_experiences = [
        "Helped user debug code",
        "Failed to connect observation to existing knowledge",
        "Generated insight about user preferences"
    ]
    
    current_goals = [
        "Improve memory integration",
        "Enhance understanding of user needs",
        "Reduce orphan accumulation"
    ]
    
    context = await reflection_engine.capture_context(
        internal_state=base_internal_state,
        recent_experiences=recent_experiences,
        current_goals=current_goals
    )
    
    # Step 4: Analyze patterns from enriched context
    print("\n[4] Analyzing patterns from enriched reflection context...")
    patterns = reflection_engine.analyze_patterns(context)
    print(f"    Identified {len(patterns)} patterns:")
    for pattern in patterns:
        print(f"      - {pattern}")
    
    # Step 5: Generate desires from patterns and orphan state
    print("\n[5] Generating desires from patterns and orphan state...")
    desires = reflection_engine.generate_desires(context, patterns)
    print(f"    Generated {len(desires)} emergent desires:")
    for i, desire in enumerate(desires, 1):
        print(f"\n    Desire {i}:")
        print(f"      ID: {desire['id']}")
        print(f"      Type: {desire['type']}")
        print(f"      Priority: {desire['priority']}")
        print(f"      Confidence: {desire['confidence']}")
        print(f"      Description: {desire['description']}")
        print(f"      Origin: {', '.join(desire['originating_patterns'])}")
    
    # Step 6: Show the full integration
    print("\n[6] Full integration demonstration...")
    print("\n" + "="*70)
    print("ORPHAN STATE IN REFLECTION CONTEXT")
    print("="*70)
    
    orphan_memory = context["internal_state"]["orphan_memory"]
    print(f"\nOrphan Memory Statistics:")
    print(f"  Total orphans: {orphan_memory['total_count']}")
    print(f"  Critical orphans: {orphan_memory['critical_count']}")
    print(f"  High-value items: {len(orphan_memory['high_value_content'])}")
    
    print(f"\nType Distribution:")
    for node_type, count in orphan_memory['type_distribution'].items():
        print(f"  {node_type}: {count}")
    
    print(f"\nIdentified Themes:")
    for theme in orphan_memory['themes']:
        print(f"  - {theme}")
    
    print(f"\nReflection Prompts (from orphan state):")
    for prompt in orphan_memory['reflection_prompts']:
        print(f"  • {prompt}")
    
    print(f"\nHigh-Value Orphan Content Samples:")
    for item in orphan_memory['high_value_content']:
        print(f"\n  [{item['id']}] {item['type']} ({item['category']}, {item['priority']} priority)")
        print(f"    Preview: {item['preview']}")
    
    # Final summary
    print("\n" + "="*70)
    print("INTEGRATION SUMMARY")
    print("="*70)
    print("\nThis demonstration shows how orphan_reader:")
    print("  1. Captures orphan node content from memory")
    print("  2. Structures it into OrphanContextSnapshot")
    print("  3. Exposes it via get_reflection_context_additions()")
    print("  4. Enriches ReflectionContext.internal_state")
    print("  5. Enables desire generation from orphan patterns")
    print("\nKey benefit: Orphan content becomes visible to reflection,")
    print("allowing emergent desires to form from disconnected experiences.")
    print("="*70)
    
    return {
        "orphan_count": orphan_memory['total_count'],
        "desires_generated": len(desires),
        "patterns_identified": len(patterns),
        "reflection_contexts_captured": len(reflection_engine.reflection_history)
    }


if __name__ == "__main__":
    results = asyncio.run(demonstrate_orphan_reflection_integration())
    print(f"\n✓ Demonstration complete: {results}")
