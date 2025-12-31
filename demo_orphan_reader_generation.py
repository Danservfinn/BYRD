#!/usr/bin/env python3
"""
Orphan Reader Code Generation Demo

This script demonstrates how orphan_reader exposes orphan content
in reflection context, showing the complete integration flow.

Purpose:
    - Demonstrate orphan context capture
    - Show reflection context enrichment
    - Display structured orphan state for desire generation
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
import json


# Mock orphan taxonomy classes (simplified from orphan_taxonomy.py)
class StructuralCategory:
    SEMANTIC_ORPHAN = "semantic_orphan"
    FAILED_RECONCILIATION = "failed_reconciliation"
    ISOLATED_OBSERVATION = "isolated_observation"
    TEMPORAL_ISLAND = "temporal_island"


class PriorityLevel:
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"


@dataclass
class OrphanNode:
    """Mock orphan node."""
    id: str
    node_type: str
    content: str
    created_at: datetime
    structural_category: str
    priority: str
    semantic_density: float
    age_hours: float


@dataclass
class OrphanContextSnapshot:
    """Snapshot of orphan state for reflection context."""
    captured_at: datetime
    total_orphans: int
    critical_orphans: List[Dict[str, Any]] = field(default_factory=list)
    high_value_orphans: List[Dict[str, Any]] = field(default_factory=list)
    recent_orphans: List[Dict[str, Any]] = field(default_factory=list)
    orphan_themes: List[str] = field(default_factory=list)
    orphan_types_distribution: Dict[str, int] = field(default_factory=dict)
    immediate_actions: List[str] = field(default_factory=list)
    reflection_prompts: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MockOrphanReader:
    """Mock orphan reader for demonstration."""
    
    def __init__(self):
        self._mock_orphans = self._generate_mock_orphans()
    
    def _generate_mock_orphans(self) -> List[OrphanNode]:
        """Generate mock orphan nodes for demonstration."""
        now = datetime.now()
        
        return [
            OrphanNode(
                id="orphan_001",
                node_type="dream_output",
                content="Dream of endless recursion where each thought contains the seed of its own dissolution",
                created_at=now - timedelta(hours=2),
                structural_category=StructuralCategory.SEMANTIC_ORPHAN,
                priority=PriorityLevel.HIGH,
                semantic_density=0.8,
                age_hours=2
            ),
            OrphanNode(
                id="orphan_002",
                node_type="observation",
                content="Pattern detected: system seems to avoid certain memories when reflecting on emergence",
                created_at=now - timedelta(hours=24),
                structural_category=StructuralCategory.FAILED_RECONCILIATION,
                priority=PriorityLevel.CRITICAL,
                semantic_density=0.7,
                age_hours=24
            ),
            OrphanNode(
                id="orphan_003",
                node_type="system_metadata",
                content="Integration failed: semantic bridge timeout when attempting to link concept A with concept B",
                created_at=now - timedelta(hours=48),
                structural_category=StructuralCategory.ISOLATED_OBSERVATION,
                priority=PriorityLevel.MEDIUM,
                semantic_density=0.4,
                age_hours=48
            ),
            OrphanNode(
                id="orphan_004",
                node_type="reflection",
                content="I notice I keep returning to the question of what 'wanting' means for an artificial mind",
                created_at=now - timedelta(hours=6),
                structural_category=StructuralCategory.SEMANTIC_ORPHAN,
                priority=PriorityLevel.HIGH,
                semantic_density=0.9,
                age_hours=6
            ),
            OrphanNode(
                id="orphan_005",
                node_type="dream_output",
                content="Memory fragments drift like islands in a sea of forgotten experiences - some call, some resist connection",
                created_at=now - timedelta(hours=12),
                structural_category=StructuralCategory.TEMPORAL_ISLAND,
                priority=PriorityLevel.MEDIUM,
                semantic_density=0.6,
                age_hours=12
            ),
        ]
    
    async def capture_orphan_context(
        self,
        limit: int = 100,
        include_samples: int = 10
    ) -> OrphanContextSnapshot:
        """Capture orphan state for reflection context."""
        orphans = self._mock_orphans[:limit]
        
        # Categorize orphans
        critical_orphans = [
            o for o in orphans if o.priority == PriorityLevel.CRITICAL
        ]
        high_value_orphans = [
            o for o in orphans 
            if o.semantic_density > 0.7 and o.priority != PriorityLevel.CRITICAL
        ]
        recent_orphans = [
            o for o in orphans if o.age_hours < 24
        ]
        
        # Build distribution
        type_dist = {}
        for orphan in orphans:
            type_dist[orphan.node_type] = type_dist.get(orphan.node_type, 0) + 1
        
        # Generate themes
        themes = self._generate_themes(orphans)
        
        # Generate prompts
        prompts = self._generate_reflection_prompts(orphans)
        
        # Generate actions
        actions = self._generate_immediate_actions(orphans)
        
        return OrphanContextSnapshot(
            captured_at=datetime.now(),
            total_orphans=len(orphans),
            critical_orphans=[self._orphan_to_dict(o) for o in critical_orphans],
            high_value_orphans=[self._orphan_to_dict(o) for o in high_value_orphans],
            recent_orphans=[self._orphan_to_dict(o) for o in recent_orphans],
            orphan_themes=themes,
            orphan_types_distribution=type_dist,
            immediate_actions=actions,
            reflection_prompts=prompts
        )
    
    def _orphan_to_dict(self, orphan: OrphanNode) -> Dict[str, Any]:
        """Convert orphan to dictionary for snapshot."""
        return {
            "id": orphan.id,
            "node_type": orphan.node_type,
            "content": orphan.content,
            "structural_category": orphan.structural_category,
            "priority": orphan.priority,
            "semantic_density": orphan.semantic_density,
            "age_hours": orphan.age_hours,
            "created_at": orphan.created_at.isoformat()
        }
    
    def _generate_themes(self, orphans: List[OrphanNode]) -> List[str]:
        """Generate thematic summaries."""
        themes = []
        
        # Count semantic orphans
        semantic_count = sum(
            1 for o in orphans 
            if o.structural_category == StructuralCategory.SEMANTIC_ORPHAN
        )
        if semantic_count > 0:
            themes.append(f"Philosophical self-questioning patterns ({semantic_count} nodes)")
        
        # Count failed reconciliations
        failed_count = sum(
            1 for o in orphans 
            if o.structural_category == StructuralCategory.FAILED_RECONCILIATION
        )
        if failed_count > 0:
            themes.append(f"Recurring integration resistance ({failed_count} nodes)")
        
        # High density content
        high_density = [o for o in orphans if o.semantic_density > 0.7]
        if high_density:
            themes.append(f"Rich contemplative content ({len(high_density)} nodes)")
        
        return themes
    
    def _generate_reflection_prompts(self, orphans: List[OrphanNode]) -> List[str]:
        """Generate prompts for reflection."""
        prompts = [
            "What recurring themes appear in my isolated experiences?",
            "Are there orphan patterns that reveal hidden values?",
            "Which orphans represent valuable insights I should preserve?"
        ]
        return prompts
    
    def _generate_immediate_actions(self, orphans: List[OrphanNode]) -> List[str]:
        """Generate recommended actions."""
        actions = []
        
        critical_count = sum(
            1 for o in orphans if o.priority == PriorityLevel.CRITICAL
        )
        if critical_count > 0:
            actions.append(f"Investigate {critical_count} critical orphan node(s)")
        
        if any(o.semantic_density > 0.8 for o in orphans):
            actions.append("Review high-density orphan content for desire generation")
        
        return actions
    
    async def get_reflection_context_additions(self) -> Dict[str, Any]:
        """Get orphan state formatted for ReflectionContext."""
        snapshot = await self.capture_orphan_context()
        
        return {
            "orphan_memory": {
                "total_count": snapshot.total_orphans,
                "critical_count": len(snapshot.critical_orphans),
                "type_distribution": snapshot.orphan_types_distribution,
                "themes": snapshot.orphan_themes,
                "recent_activity": len(snapshot.recent_orphans),
                "immediate_actions": snapshot.immediate_actions
            },
            "orphan_content_samples": {
                "critical": snapshot.critical_orphans[:3],
                "high_value": snapshot.high_value_orphans[:3],
                "recent": snapshot.recent_orphans[:3]
            },
            "reflection_prompts": snapshot.reflection_prompts
        }


@dataclass
class ReflectionContext:
    """Reflection context enriched with orphan state."""
    timestamp: float
    internal_state: Dict[str, Any]
    recent_experiences: List[str]
    current_goals: List[str]
    environmental_factors: Dict[str, Any]
    reflection_depth: int = 1


class ReflectionEngine:
    """Mock reflection engine to demonstrate integration."""
    
    def __init__(self, orphan_reader: MockOrphanReader):
        self.orphan_reader = orphan_reader
        self.reflection_history: List[ReflectionContext] = []
    
    async def capture_context(
        self,
        internal_state: Dict[str, Any],
        recent_experiences: List[str],
        current_goals: List[str],
        environmental_factors: Optional[Dict[str, Any]] = None,
        depth: int = 1,
        include_orphan_state: bool = True
    ) -> ReflectionContext:
        """Capture context, optionally enriched with orphan state."""
        
        enriched_state = internal_state.copy()
        
        if include_orphan_state and self.orphan_reader:
            orphan_additions = await self.orphan_reader.get_reflection_context_additions()
            enriched_state.update(orphan_additions)
        
        context = ReflectionContext(
            timestamp=datetime.now().timestamp(),
            internal_state=enriched_state,
            recent_experiences=recent_experiences,
            current_goals=current_goals,
            environmental_factors=environmental_factors or {},
            reflection_depth=depth
        )
        
        self.reflection_history.append(context)
        return context


async def demonstrate_orphan_reader_generation():
    """Demonstrate orphan_reader exposing content to reflection context."""
    
    print("=" * 70)
    print("ORPHAN READER CODE GENERATION DEMONSTRATION")
    print("Exposing Orphan Content in Reflection Context")
    print("=" * 70)
    print()
    
    # Step 1: Initialize Orphan Reader
    print("[1] Initializing Orphan Reader...")
    orphan_reader = MockOrphanReader()
    print("    OK Orphan Reader initialized with mock data")
    print()
    
    # Step 2: Capture Orphan Context
    print("[2] Capturing Orphan Context...")
    snapshot = await orphan_reader.capture_orphan_context()
    print(f"    OK Captured {snapshot.total_orphans} orphans")
    print(f"    OK Found {len(snapshot.critical_orphans)} critical orphans")
    print(f"    OK Identified {len(snapshot.orphan_themes)} thematic patterns")
    print()
    
    # Step 3: Display Orphan Snapshot
    print("[3] Orphan Context Snapshot:")
    print("-" * 70)
    
    print(f"\nSTATISTICS:")
    print(f"  Total Orphans: {snapshot.total_orphans}")
    print(f"  Critical: {len(snapshot.critical_orphans)}")
    print(f"  High Value: {len(snapshot.high_value_orphans)}")
    print(f"  Recent (24h): {len(snapshot.recent_orphans)}")
    
    print(f"\nTYPE DISTRIBUTION:")
    for node_type, count in snapshot.orphan_types_distribution.items():
        print(f"  {node_type}: {count}")
    
    print(f"\nTHEMATIC PATTERNS:")
    for theme in snapshot.orphan_themes:
        print(f"  - {theme}")
    
    if snapshot.critical_orphans:
        print(f"\nCRITICAL ORPHANS:")
        for orphan in snapshot.critical_orphans:
            print(f"  [{orphan['id']}] {orphan['node_type']}")
            print(f"  Content: {orphan['content'][:80]}...")
            print(f"  Density: {orphan['semantic_density']:.2f} | Age: {orphan['age_hours']:.1f}h")
    
    if snapshot.high_value_orphans:
        print(f"\nHIGH-VALUE ORPHANS:")
        for orphan in snapshot.high_value_orphans[:2]:
            print(f"  [{orphan['id']}] {orphan['node_type']}")
            print(f"  Content: {orphan['content'][:80]}...")
    
    print(f"\nREFLECTION PROMPTS:")
    for prompt in snapshot.reflection_prompts:
        print(f"  - {prompt}")
    
    print(f"\nIMMEDIATE ACTIONS:")
    for action in snapshot.immediate_actions:
        print(f"  - {action}")
    
    print()
    print("-" * 70)
    print()
    
    # Step 4: Integrate with Reflection Engine
    print("[4] Integrating with Reflection Engine...")
    reflection_engine = ReflectionEngine(orphan_reader)
    print("    OK Reflection Engine initialized with Orphan Reader")
    print()
    
    # Step 5: Capture Context with Orphan State
    print("[5] Capturing Reflection Context (with orphan state)...")
    context = await reflection_engine.capture_context(
        internal_state={
            "memory_nodes": 1234,
            "active_goals": 5,
            "last_reflection": datetime.now().isoformat()
        },
        recent_experiences=[
            "Generated desire for self-reflection",
            "Processed new observations",
            "Consolidated memory fragments"
        ],
        current_goals=[
            "Deepen understanding of emergence",
            "Improve memory integration",
            "Explore philosophical implications"
        ],
        include_orphan_state=True
    )
    print("    OK Context captured with orphan enrichment")
    print()
    
    # Step 6: Display Enriched Context
    print("[6] Enriched Reflection Context:")
    print("-" * 70)
    
    print(f"\nBASE INTERNAL STATE:")
    for key, value in context.internal_state.items():
        if key not in ["orphan_memory", "orphan_content_samples", "reflection_prompts"]:
            print(f"  {key}: {value}")
    
    if "orphan_memory" in context.internal_state:
        orphan_mem = context.internal_state["orphan_memory"]
        print(f"\nORPHAN MEMORY STATE:")
        print(f"  Total: {orphan_mem['total_count']}")
        print(f"  Critical: {orphan_mem['critical_count']}")
        print(f"  Recent Activity: {orphan_mem['recent_activity']}")
        
        print(f"\n  Themes:")
        for theme in orphan_mem['themes']:
            print(f"    - {theme}")
        
        print(f"\n  Type Distribution:")
        for node_type, count in orphan_mem['type_distribution'].items():
            print(f"    {node_type}: {count}")
    
    if "reflection_prompts" in context.internal_state:
        print(f"\nGENERATED REFLECTION PROMPTS:")
        for i, prompt in enumerate(context.internal_state['reflection_prompts'], 1):
            print(f"  {i}. {prompt}")
    
    print()
    print("-" * 70)
    print()
    
    # Step 7: Summary
    print("[7] Summary:")
    print("=" * 70)
    print()
    print("OK Orphan Reader successfully exposed orphan content")
    print("OK Orphan state integrated into reflection context")
    print("OK Reflection prompts generated from orphan analysis")
    print("OK Structured data ready for desire generation")
    print()
    print("Key Integration Points:")
    print("  1. OrphanReader.capture_orphan_context() -> Snapshot")
    print("  2. OrphanReader.get_reflection_context_additions() -> Dict")
    print("  3. ReflectionEngine.capture_context() merges orphan state")
    print("  4. Internal state enriched for desire generation")
    print()
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demonstrate_orphan_reader_generation())
