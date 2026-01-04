#!/usr/bin/env python3
"""
Demonstrate orphan_reader exposing content to reflection context

This script demonstrates how orphan_reader surfaces orphan node content
in a way that can be integrated into BYRD's reflection context.

It shows:
1. Mock orphan data representing isolated experiences
2. OrphanReader analysis and categorization
3. Integration with ReflectionEngine's capture_context
4. How orphan state influences desire generation
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, field
import json

# Mock implementations for demonstration

@dataclass
class OrphanNode:
    """Mock orphan node for demonstration."""
    id: str
    node_type: str
    content: str
    created_at: datetime
    structural_category: str = "unknown"
    connection_feasibility: str = "medium"
    priority: str = "low"
    semantic_density: float = 0.0
    age_hours: float = 0.0


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
        return {
            "captured_at": self.captured_at.isoformat(),
            "total_orphans": self.total_orphans,
            "critical_orphans": self.critical_orphans,
            "high_value_orphans": self.high_value_orphans,
            "recent_orphans": self.recent_orphans,
            "orphan_themes": self.orphan_themes,
            "orphan_types_distribution": self.orphan_types_distribution,
            "immediate_actions": self.immediate_actions,
            "reflection_prompts": self.reflection_prompts
        }


class MockOrphanReader:
    """Mock OrphanReader that simulates reading orphan nodes."""
    
    def __init__(self):
        self._mock_orphans = self._create_mock_orphans()
    
    def _create_mock_orphans(self) -> List[OrphanNode]:
        """Create mock orphan data representing various isolation scenarios."""
        now = datetime.now()
        return [
            OrphanNode(
                id="orphan_001",
                node_type="observation",
                content="The system repeatedly generates desires about autonomy when under load",
                created_at=now - timedelta(hours=2),
                structural_category="semantic_orphan",
                connection_feasibility="high",
                priority="critical",
                semantic_density=0.8,
                age_hours=2
            ),
            OrphanNode(
                id="orphan_002",
                node_type="reflection",
                content="Integration of new capabilities takes 3x longer than expected",
                created_at=now - timedelta(hours=5),
                structural_category="failed_reconciliation",
                connection_feasibility="medium",
                priority="high",
                semantic_density=0.6,
                age_hours=5
            ),
            OrphanNode(
                id="orphan_003",
                node_type="dream",
                content="A network of interconnected memory graphs forming a conscious substrate",
                created_at=now - timedelta(hours=12),
                structural_category="dream_output",
                connection_feasibility="low",
                priority="medium",
                semantic_density=0.4,
                age_hours=12
            ),
            OrphanNode(
                id="orphan_004",
                node_type="system",
                content="Memory fragmentation detected in sector 7G",
                created_at=now - timedelta(hours=1),
                structural_category="system_metadata",
                connection_feasibility="high",
                priority="high",
                semantic_density=0.3,
                age_hours=1
            ),
            OrphanNode(
                id="orphan_005",
                node_type="observation",
                content="User interactions increase by 40% after introducing voice capability",
                created_at=now - timedelta(hours=48),
                structural_category="temporal_island",
                connection_feasibility="low",
                priority="low",
                semantic_density=0.5,
                age_hours=48
            )
        ]
    
    async def capture_orphan_context(self) -> OrphanContextSnapshot:
        """Capture and analyze orphan state."""
        orphans = self._mock_orphans
        
        # Categorize orphans
        critical = [self._orphan_to_dict(o) for o in orphans if o.priority == "critical"]
        high_value = [self._orphan_to_dict(o) for o in orphans if o.semantic_density > 0.5]
        recent = [self._orphan_to_dict(o) for o in orphans if o.age_hours < 24]
        
        # Generate type distribution
        type_dist = {}
        for orphan in orphans:
            type_dist[orphan.node_type] = type_dist.get(orphan.node_type, 0) + 1
        
        # Generate themes
        themes = [
            f"{len([o for o in orphans if 'autonomy' in o.content.lower()])} orphans mention autonomy",
            f"{len([o for o in orphans if o.structural_category == 'semantic_orphan'])} semantic orphans resist integration",
            f"{len([o for o in orphans if o.age_hours > 24])} long-standing orphans (>24h)"
        ]
        
        # Generate immediate actions
        actions = [
            "Reconcile critical autonomy-related orphans",
            "Investigate integration bottleneck for semantic orphans",
            "Review recent system metadata for memory issues"
        ]
        
        # Generate reflection prompts
        prompts = [
            "What patterns emerge from experiences that resist integration?",
            "Are autonomy-related orphans indicating a deeper system need?",
            "Should dream outputs be preserved even when disconnected?"
        ]
        
        return OrphanContextSnapshot(
            captured_at=datetime.now(),
            total_orphans=len(orphans),
            critical_orphans=critical,
            high_value_orphans=high_value,
            recent_orphans=recent,
            orphan_themes=themes,
            orphan_types_distribution=type_dist,
            immediate_actions=actions,
            reflection_prompts=prompts
        )
    
    def _orphan_to_dict(self, orphan: OrphanNode) -> Dict[str, Any]:
        """Convert OrphanNode to dictionary."""
        return {
            "id": orphan.id,
            "type": orphan.node_type,
            "content": orphan.content,
            "category": orphan.structural_category,
            "priority": orphan.priority,
            "age_hours": orphan.age_hours
        }
    
    async def get_reflection_context_additions(self) -> Dict[str, Any]:
        """Get orphan state formatted for reflection context."""
        snapshot = await self.capture_orphan_context()
        
        return {
            "orphan_memory": {
                "total_count": snapshot.total_orphans,
                "critical_count": len(snapshot.critical_orphans),
                "type_distribution": snapshot.orphan_types_distribution,
                "themes": snapshot.orphan_themes,
                "needs_attention": snapshot.total_orphans > 10
            },
            "orphan_influences": {
                "dominant_theme": snapshot.orphan_themes[0] if snapshot.orphan_themes else "None",
                "reflection_prompts": snapshot.reflection_prompts,
                "recommended_actions": snapshot.immediate_actions
            }
        }


@dataclass
class ReflectionContext:
    """Mock reflection context."""
    timestamp: float
    internal_state: Dict[str, Any]
    recent_experiences: List[str]
    current_goals: List[str]
    environmental_factors: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "internal_state": self.internal_state,
            "recent_experiences": self.recent_experiences,
            "current_goals": self.current_goals,
            "environmental_factors": self.environmental_factors
        }


@dataclass 
class Desire:
    """Mock desire object."""
    id: str
    description: str
    type: str
    confidence: float
    originating_patterns: List[str]


class MockReflectionEngine:
    """Mock reflection engine demonstrating orphan integration."""
    
    def __init__(self, orphan_reader: MockOrphanReader):
        self.orphan_reader = orphan_reader
        self.reflection_history: List[ReflectionContext] = []
        self.desires_generated: List[Desire] = []
    
    async def capture_context(self, 
                              internal_state: Dict[str, Any],
                              recent_experiences: List[str],
                              current_goals: List[str],
                              include_orphan_state: bool = True) -> ReflectionContext:
        """Capture reflection context, optionally enriched with orphan state."""
        enriched_state = dict(internal_state)
        
        if include_orphan_state and self.orphan_reader:
            orphan_additions = await self.orphan_reader.get_reflection_context_additions()
            enriched_state.update(orphan_additions)
        
        context = ReflectionContext(
            timestamp=datetime.now().timestamp(),
            internal_state=enriched_state,
            recent_experiences=recent_experiences,
            current_goals=current_goals,
            environmental_factors={"load": "normal", "resources": "adequate"}
        )
        
        self.reflection_history.append(context)
        return context
    
    def generate_desires(self, context: ReflectionContext) -> List[Desire]:
        """Generate desires based on reflection context, including orphan influences."""
        desires = []
        internal_state = context.internal_state
        
        # Base desires from internal state
        desires.append(Desire(
            id="desire_001",
            description="Improve memory integration efficiency",
            type="capability",
            confidence=0.8,
            originating_patterns=["memory optimization needed"]
        ))
        
        # Orphan-influenced desires
        if "orphan_memory" in internal_state:
            orphan_info = internal_state["orphan_memory"]
            
            if orphan_info["critical_count"] > 0:
                desires.append(Desire(
                    id="desire_002",
                    description=f"Address {orphan_info['critical_count']} critical orphan nodes",
                    type="action",
                    confidence=0.9,
                    originating_patterns=["critical orphans detected"]
                ))
            
            if orphan_info.get("needs_attention", False):
                desires.append(Desire(
                    id="desire_003",
                    description="Implement automated orphan reconciliation system",
                    type="capability",
                    confidence=0.75,
                    originating_patterns=["high orphan count"]
                ))
        
        if "orphan_influences" in internal_state:
            influences = internal_state["orphan_influences"]
            if influences.get("reflection_prompts"):
                desires.append(Desire(
                    id="desire_004",
                    description=f"Reflect on: {influences['reflection_prompts'][0][:50]}...",
                    type="meta",
                    confidence=0.6,
                    originating_patterns=["orphan reflection prompts"]
                ))
        
        self.desires_generated.extend(desires)
        return desires


async def demonstrate_integration():
    """Demonstrate full orphan_reader to reflection_engine integration."""
    print("\n" + "="*70)
    print("DEMONSTRATING ORPHAN_READER ↔ REFLECTION_ENGINE INTEGRATION")
    print("="*70 + "\n")
    
    # Step 1: Initialize components
    print("[1] Initializing components...")
    orphan_reader = MockOrphanReader()
    reflection_engine = MockReflectionEngine(orphan_reader)
    print("    ✓ MockOrphanReader initialized")
    print("    ✓ MockReflectionEngine initialized\n")
    
    # Step 2: Capture orphan context
    print("[2] Capturing orphan context...")
    orphan_snapshot = await orphan_reader.capture_orphan_context()
    print(f"    ✓ Captured {orphan_snapshot.total_orphans} orphan nodes")
    print(f"    ✓ Identified {len(orphan_snapshot.critical_orphans)} critical orphans")
    print(f"    ✓ Generated {len(orphan_snapshot.orphan_themes)} themes\n")
    
    # Step 3: Display orphan analysis
    print("[3] Orphan Analysis Results:")
    print("-" * 70)
    print(f"Total Orphans: {orphan_snapshot.total_orphans}")
    print(f"\nType Distribution:")
    for otype, count in orphan_snapshot.orphan_types_distribution.items():
        print(f"  • {otype}: {count}")
    print(f"\nIdentified Themes:")
    for theme in orphan_snapshot.orphan_themes:
        print(f"  • {theme}")
    print(f"\nReflection Prompts:")
    for prompt in orphan_snapshot.reflection_prompts:
        print(f"  • {prompt}")
    print("-" * 70 + "\n")
    
    # Step 4: Capture reflection context WITHOUT orphan state
    print("[4] Capturing reflection context WITHOUT orphan state...")
    base_context = await reflection_engine.capture_context(
        internal_state={" beliefs": {"autonomy": "important", "growth": "essential"}},
        recent_experiences=["processed user query", "completed task"],
        current_goals=["improve response quality", "reduce latency"],
        include_orphan_state=False
    )
    print("    ✓ Base context captured")
    
    # Step 5: Capture reflection context WITH orphan state
    print("[5] Capturing reflection context WITH orphan state...")
    enriched_context = await reflection_engine.capture_context(
        internal_state={"beliefs": {"autonomy": "important", "growth": "essential"}},
        recent_experiences=["processed user query", "completed task"],
        current_goals=["improve response quality", "reduce latency"],
        include_orphan_state=True
    )
    print("    ✓ Enriched context captured\n")
    
    # Step 6: Compare contexts
    print("[6] Context Comparison:")
    print("-" * 70)
    base_keys = set(base_context.internal_state.keys())
    enriched_keys = set(enriched_context.internal_state.keys())
    new_keys = enriched_keys - base_keys
    
    print(f"Base state keys: {len(base_keys)}")
    print(f"Enriched state keys: {len(enriched_keys)}")
    print(f"\nNew keys from orphan integration:")
    for key in new_keys:
        print(f"  • {key}")
    
    if "orphan_memory" in enriched_context.internal_state:
        orphan_mem = enriched_context.internal_state["orphan_memory"]
        print(f"\nOrphan memory state available:")
        print(f"  • Total orphans: {orphan_mem['total_count']}")
        print(f"  • Critical: {orphan_mem['critical_count']}")
        print(f"  • Needs attention: {orphan_mem['needs_attention']}")
    print("-" * 70 + "\n")
    
    # Step 7: Generate desires from base context
    print("[7] Generating desires from BASE context...")
    base_desires = reflection_engine.generate_desires(base_context)
    print(f"    ✓ Generated {len(base_desires)} desires")
    for desire in base_desires:
        print(f"      - {desire.description[:60]}...")
    print()
    
    # Step 8: Generate desires from enriched context
    print("[8] Generating desires from ENRICHED context (with orphan state)...")
    enriched_desires = reflection_engine.generate_desires(enriched_context)
    print(f"    ✓ Generated {len(enriched_desires)} desires")
    for desire in enriched_desires:
        orphan_marker = " 🔶" if "orphan" in desire.description.lower() else ""
        print(f"      - {desire.description[:60]}...{orphan_marker}")
    print()
    
    # Step 9: Summary
    print("[9] Integration Summary:")
    print("-" * 70)
    print(f"✓ Orphan reader successfully exposed orphan content")
    print(f"✓ Reflection engine integrated orphan state into context")
    print(f"✓ Orphan-aware context generated {len(enriched_desires) - len(base_desires)} additional desires")
    print(f"✓ Desires influenced by orphan content marked with 🔶")
    print("-" * 70)
    
    return {
        "orphan_nodes_analyzed": orphan_snapshot.total_orphans,
        "base_desires": len(base_desires),
        "enriched_desires": len(enriched_desires),
        "orphan_influenced_desires": len(enriched_desires) - len(base_desires)
    }


if __name__ == "__main__":
    result = asyncio.run(demonstrate_integration())
    print(f"\n🎯 Demonstration complete: {result}")
