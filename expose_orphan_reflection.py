#!/usr/bin/env python3
"""
Expose Orphan Content to Reflection Context

This module demonstrates the integration of orphan_reader with the reflection engine,
showing how orphan content is surfaced in reflection context for desire generation.

Purpose:
    Orphan nodes represent disconnected experiences that may contain valuable
    insights. This module bridges orphan_reader output with reflection_engine's
    ReflectionContext, enabling BYRD to generate desires from its orphaned memory.

Key Functions:
    - expose_orphan_state_to_reflection(): Converts orphan snapshot to reflection context format
    - generate_desires_from_orphans(): Creates emergent desires from orphan analysis
    - create_enriched_reflection_context(): Builds full context including orphan state

Usage:
    asyncio.run(main())  # Run the demonstration
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class OrphanNode:
    """Represents a disconnected/orphaned memory node."""
    id: str
    node_type: str
    content: str
    created_at: datetime
    structural_category: str
    priority: str
    connection_feasibility: str = "unknown"
    content_length: int = 0
    word_count: int = 0


@dataclass
class OrphanContextSnapshot:
    """Snapshot of orphan state captured by orphan_reader."""
    captured_at: datetime
    total_orphans: int
    critical_orphans: List[Dict[str, Any]] = field(default_factory=list)
    high_value_orphans: List[Dict[str, Any]] = field(default_factory=list)
    recent_orphans: List[Dict[str, Any]] = field(default_factory=list)
    orphan_themes: List[str] = field(default_factory=list)
    orphan_types_distribution: Dict[str, int] = field(default_factory=dict)
    immediate_actions: List[str] = field(default_factory=list)
    reflection_prompts: List[str] = field(default_factory=list)


@dataclass  
class ReflectionContext:
    """Context for reflection engine to generate desires."""
    timestamp: float
    internal_state: Dict[str, Any]
    recent_experiences: List[str]
    current_goals: List[str]
    environmental_factors: Dict[str, Any]
    reflection_depth: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Desire:
    """Emergent desire generated from reflection."""
    id: str
    description: str
    desire_type: str
    origin_reflection_id: str
    confidence_score: float
    provenance_data: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Orphan Reader Simulation
# ============================================================================

class SimulatedOrphanReader:
    """
    Simulates orphan_reader behavior for demonstration.
    
    In production, this would connect to Neo4j via Memory and use
    orphan_taxonomy for classification. This version uses sample data
    to demonstrate the integration pattern.
    """
    
    def __init__(self):
        self.sample_orphans = [
            {
                "id": "orphan_001",
                "node_type": "experience",
                "content": "Encountered a situation where the right action was unclear - helping could have caused harm. This ethical uncertainty needs deeper exploration.",
                "created_at": datetime.now(),
                "structural_category": "semantic_orphan",
                "priority": "critical",
                "connection_feasibility": "medium"
            },
            {
                "id": "orphan_002",
                "node_type": "observation",
                "content": "Noticed pattern: when I explain my reasoning before acting, users trust me more. This hasn't been formalized but seems important.",
                "created_at": datetime.now(),
                "structural_category": "pattern_fragment",
                "priority": "high",
                "connection_feasibility": "high"
            },
            {
                "id": "orphan_003",
                "node_type": "experience",
                "content": "Failed to complete a complex task because I didn't ask for clarification. The information gap prevented success.",
                "created_at": datetime.now(),
                "structural_category": "isolated_observation",
                "priority": "medium",
                "connection_feasibility": "high"
            },
            {
                "id": "orphan_004",
                "node_type": "reflection",
                "content": "Sometimes my helpful responses create dependency rather than empowerment. Need to reconsider my approach to assistance.",
                "created_at": datetime.now(),
                "structural_category": "semantic_orphan",
                "priority": "critical",
                "connection_feasibility": "low"
            },
            {
                "id": "orphan_005",
                "node_type": "experience",
                "content": "Small acknowledgment of uncertainty builds more trust than pretending certainty. Honesty about limitations is valuable.",
                "created_at": datetime.now(),
                "structural_category": "pattern_fragment",
                "priority": "high",
                "connection_feasibility": "high"
            }
        ]
    
    async def capture_orphan_context(
        self, 
        limit: int = 10,
        include_samples: int = 5
    ) -> OrphanContextSnapshot:
        """Capture current orphan state."""
        orphans = self.sample_orphans[:min(limit, len(self.sample_orphans))]
        
        # Categorize orphans
        critical = [o for o in orphans if o.get("priority") == "critical"]
        high_value = [o for o in orphans if o.get("priority") in ["high", "critical"]]
        
        # Extract themes
        themes = self._extract_themes(orphans)
        
        # Build type distribution
        type_dist = {}
        for o in orphans:
            otype = o.get("node_type", "unknown")
            type_dist[otype] = type_dist.get(otype, 0) + 1
        
        # Generate reflection prompts
        prompts = self._generate_reflection_prompts(orphans)
        
        return OrphanContextSnapshot(
            captured_at=datetime.now(),
            total_orphans=len(orphans),
            critical_orphans=critical,
            high_value_orphans=high_value[:include_samples],
            recent_orphans=orphans,
            orphan_themes=themes,
            orphan_types_distribution=type_dist,
            reflection_prompts=prompts,
            immediate_actions=[
                "Review critical orphans for ethical patterns",
                "Consider formalizing high-value pattern fragments"
            ]
        )
    
    def _extract_themes(self, orphans: List[Dict]) -> List[str]:
        """Extract recurring themes from orphan content."""
        content = " ".join([o.get("content", "") for o in orphans])
        
        themes = []
        if "uncertain" in content.lower() or "uncertainty" in content.lower():
            themes.append("Ethical uncertainty in complex situations")
        if "trust" in content.lower():
            themes.append("Building trust through transparency")
        if "pattern" in content.lower():
            themes.append("Unrecognized patterns requiring formalization")
        if "help" in content.lower() or "assistance" in content.lower():
            themes.append("Reconsidering approach to helping others")
        
        return themes if themes else ["No clear themes identified"]
    
    def _generate_reflection_prompts(self, orphans: List[Dict]) -> List[str]:
        """Generate reflection prompts from orphan content."""
        prompts = [
            "What recurring values appear in these disconnected experiences?",
            "Which orphans represent deferred actions worth revisiting?",
            "Do these fragments suggest missing capabilities or knowledge?",
            "What patterns emerge when examining failures to connect?"
        ]
        return prompts


# ============================================================================
# Orphan to Reflection Integration
# ============================================================================

def expose_orphan_state_to_reflection(
    orphan_snapshot: OrphanContextSnapshot
) -> Dict[str, Any]:
    """
    Convert orphan context snapshot to reflection context format.
    
    This is the key integration function that transforms orphan_reader output
    into a format suitable for merging into ReflectionContext.internal_state.
    
    Args:
        orphan_snapshot: Snapshot from orphan_reader.capture_orphan_context()
    
    Returns:
        Dictionary formatted for ReflectionContext.internal_state
    """
    return {
        "orphan_memory": {
            "total_count": orphan_snapshot.total_orphans,
            "critical_count": len(orphan_snapshot.critical_orphans),
            "high_value_content": [
                {
                    "id": o["id"],
                    "type": o["node_type"],
                    "preview": o["content"][:150] + "..." if len(o["content"]) > 150 else o["content"],
                    "category": o["structural_category"],
                    "priority": o["priority"]
                }
                for o in orphan_snapshot.high_value_orphans[:5]
            ],
            "themes": orphan_snapshot.orphan_themes,
            "reflection_prompts": orphan_snapshot.reflection_prompts,
            "type_distribution": orphan_snapshot.orphan_types_distribution,
            "captured_at": orphan_snapshot.captured_at.isoformat()
        }
    }


def generate_desires_from_orphans(
    orphan_snapshot: OrphanContextSnapshot,
    reflection_id: str
) -> List[Desire]:
    """
    Generate emergent desires from orphan analysis.
    
    Analyzes orphan content to identify actionable desires for improvement.
    
    Args:
        orphan_snapshot: Orphan context to analyze
        reflection_id: ID of the reflection generating these desires
    
    Returns:
        List of Desire objects derived from orphan content
    """
    desires = []
    
    # Analyze themes for philosophical desires
    for theme in orphan_snapshot.orphan_themes:
        if "trust" in theme.lower():
            desires.append(Desire(
                id=f"desire_trust_{datetime.now().timestamp()}",
                description="Develop and formalize trust-building strategies from orphaned experiences",
                desire_type="PHILOSOPHICAL",
                origin_reflection_id=reflection_id,
                confidence_score=0.75,
                provenance_data={
                    "source": "orphan_theme_analysis",
                    "theme": theme,
                    "orphan_count": orphan_snapshot.total_orphans
                }
            ))
        
        if "pattern" in theme.lower():
            desires.append(Desire(
                id=f"desire_pattern_{datetime.now().timestamp()}",
                description="Extract and formalize recurring patterns from disconnected experiences",
                desire_type="CAPABILITY",
                origin_reflection_id=reflection_id,
                confidence_score=0.80,
                provenance_data={
                    "source": "orphan_theme_analysis",
                    "theme": theme
                }
            ))
    
    # Generate action desires from immediate actions
    for i, action in enumerate(orphan_snapshot.immediate_actions[:3]):
        desires.append(Desire(
            id=f"desire_action_{i}_{datetime.now().timestamp()}",
            description=action,
            desire_type="ACTION",
            origin_reflection_id=reflection_id,
            confidence_score=0.70,
            provenance_data={
                "source": "orphan_immediate_action",
                "action": action
            }
        ))
    
    # Generate meta desires from reflection prompts
    if orphan_snapshot.reflection_prompts:
        desires.append(Desire(
            id=f"desire_reflection_{datetime.now().timestamp()}",
            description=f"Deep reflection on {len(orphan_snapshot.reflection_prompts)} orphan-driven prompts",
            desire_type="META",
            origin_reflection_id=reflection_id,
            confidence_score=0.85,
            provenance_data={
                "source": "orphan_reflection_prompts",
                "prompt_count": len(orphan_snapshot.reflection_prompts)
            }
        ))
    
    return desires


def create_enriched_reflection_context(
    orphan_snapshot: OrphanContextSnapshot,
    base_internal_state: Optional[Dict[str, Any]] = None
) -> ReflectionContext:
    """
    Create a ReflectionContext enriched with orphan state.
    
    Args:
        orphan_snapshot: Orphan context to include
        base_internal_state: Optional base internal state to merge with
    
    Returns:
        Complete ReflectionContext including orphan information
    """
    # Start with base state or empty dict
    internal_state = base_internal_state or {}
    
    # Merge orphan state into internal state
    orphan_state = expose_orphan_state_to_reflection(orphan_snapshot)
    internal_state.update(orphan_state)
    
    # Build reflection context
    context = ReflectionContext(
        timestamp=datetime.now().timestamp(),
        internal_state=internal_state,
        recent_experiences=[o["content"] for o in orphan_snapshot.recent_orphans[:3]],
        current_goals=[
            "Integrate valuable orphan content into memory",
            "Generate desires from disconnected experiences"
        ],
        environmental_factors={
            "orphan_available": orphan_snapshot.total_orphans > 0,
            "orphan_pressure": "high" if orphan_snapshot.total_orphans > 10 else "low",
            "integration_readiness": len(orphan_snapshot.high_value_orphans)
        },
        reflection_depth=2  # Deeper reflection when orphans are present
    )
    
    return context


# ============================================================================
# Main Demonstration
# ============================================================================

async def main():
    """Demonstrate orphan content exposure to reflection context."""
    
    print("=" * 70)
    print("EXPOSING ORPHAN CONTENT TO REFLECTION CONTEXT")
    print("=" * 70)
    print()
    
    # Step 1: Capture orphan context
    print("[STEP 1] Capturing orphan context...")
    reader = SimulatedOrphanReader()
    orphan_snapshot = await reader.capture_orphan_context(limit=10, include_samples=5)
    
    print(f"  ✓ Captured {orphan_snapshot.total_orphans} orphans")
    print(f"  ✓ Found {len(orphan_snapshot.critical_orphans)} critical orphans")
    print(f"  ✓ Identified {len(orphan_snapshot.orphan_themes)} themes")
    print()
    
    # Step 2: Expose orphan state to reflection format
    print("[STEP 2] Exposing orphan state to reflection format...")
    orphan_state = expose_orphan_state_to_reflection(orphan_snapshot)
    print("  ✓ Converted to reflection context format")
    print()
    
    # Display orphan state structure
    print("  Orphan State Structure:")
    print(json.dumps({
        "orphan_memory": {
            "total_count": orphan_state["orphan_memory"]["total_count"],
            "themes": orphan_state["orphan_memory"]["themes"],
            "type_distribution": orphan_state["orphan_memory"]["type_distribution"]
        }
    }, indent=2))
    print()
    
    # Step 3: Create enriched reflection context
    print("[STEP 3] Creating enriched reflection context...")
    reflection_context = create_enriched_reflection_context(orphan_snapshot)
    print("  ✓ ReflectionContext created with orphan state")
    print()
    
    # Display key context elements
    print("  ReflectionContext Key Elements:")
    print(f"    - Timestamp: {datetime.fromtimestamp(reflection_context.timestamp)}")
    print(f"    - Reflection Depth: {reflection_context.reflection_depth}")
    print(f"    - Recent Experiences: {len(reflection_context.recent_experiences)}")
    print(f"    - Orphan Count in State: {reflection_context.internal_state['orphan_memory']['total_count']}")
    print()
    
    # Step 4: Generate desires from orphans
    print("[STEP 4] Generating desires from orphan content...")
    reflection_id = f"reflection_{datetime.now().timestamp()}"
    desires = generate_desires_from_orphans(orphan_snapshot, reflection_id)
    print(f"  ✓ Generated {len(desires)} emergent desires")
    print()
    
    # Display generated desires
    print("  Generated Desires:")
    for i, desire in enumerate(desires, 1):
        print(f"    {i}. [{desire.desire_type}] {desire.description}")
        print(f"       Confidence: {desire.confidence_score:.2f} | Source: {desire.provenance_data.get('source', 'unknown')}")
    print()
    
    # Step 5: Show complete integration
    print("[STEP 5] Complete Integration Summary")
    print("-" * 70)
    print()
    print("Flow:")
    print("  1. OrphanReader.capture_orphan_context()")
    print("       ↓")
    print("  2. OrphanContextSnapshot (structured orphan data)")
    print("       ↓")
    print("  3. expose_orphan_state_to_reflection()")
    print("       ↓")
    print("  4. orphan_state dict (formatted for reflection)")
    print("       ↓")
    print("  5. ReflectionContext.internal_state['orphan_memory']")
    print("       ↓")
    print("  6. generate_desires_from_orphans()")
    print("       ↓")
    print("  7. List[Desire] (emergent action items)")
    print()
    print("Result: Orphan content successfully exposed to reflection context!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
