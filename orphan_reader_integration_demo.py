#!/usr/bin/env python3
"""
Orphan Reader Integration Demonstration

This script demonstrates how orphan_reader exposes orphan content
in reflection context for BYRD's introspective analysis.

NOTE: This is a conceptual demonstration. The actual implementation
exists in orphan_reader.py and is integrated in reflection_engine.py.
"""

import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional


# =============================================================================
# DEMONSTRATION: How OrphanReader Exposes Content to ReflectionContext
# =============================================================================

class OrphanContextSnapshot:
    """Snapshot of orphan state (from orphan_reader.py)"""
    
    def __init__(self, 
                 captured_at: datetime,
                 total_orphans: int,
                 critical_orphans: List[Dict] = None,
                 high_value_orphans: List[Dict] = None,
                 recent_orphans: List[Dict] = None,
                 orphan_themes: List[str] = None,
                 orphan_types_distribution: Dict[str, int] = None,
                 immediate_actions: List[str] = None,
                 reflection_prompts: List[str] = None,
                 orphan_samples: List[Dict] = None):
        
        self.captured_at = captured_at
        self.total_orphans = total_orphans
        self.critical_orphans = critical_orphans or []
        self.high_value_orphans = high_value_orphans or []
        self.recent_orphans = recent_orphans or []
        self.orphan_themes = orphan_themes or []
        self.orphan_types_distribution = orphan_types_distribution or {}
        self.immediate_actions = immediate_actions or []
        self.reflection_prompts = reflection_prompts or []
        self.orphan_samples = orphan_samples or []


class ReflectionContext:
    """Context for reflection (from reflection_engine.py)"""
    
    def __init__(self,
                 timestamp: float,
                 internal_state: Dict[str, Any],
                 recent_experiences: List[str],
                 current_goals: List[str],
                 environmental_factors: Dict[str, Any] = None,
                 reflection_depth: int = 1):
        
        self.timestamp = timestamp
        self.internal_state = internal_state
        self.recent_experiences = recent_experiences
        self.current_goals = current_goals
        self.environmental_factors = environmental_factors or {}
        self.reflection_depth = reflection_depth
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class OrphanReader:
    """OrphanReader exposes orphan content to reflection context.
    
    Key method: get_reflection_context_additions()
    This returns a dict formatted for merging into ReflectionContext.internal_state
    """
    
    def __init__(self, memory):
        self.memory = memory
        self._cache = None
    
    async def capture_orphan_context(self, limit: int = 100) -> OrphanContextSnapshot:
        """Capture current orphan state for reflection."""
        # In actual implementation, this:
        # 1. Queries memory for orphan nodes
        # 2. Classifies using OrphanTaxonomyClassifier
        # 3. Categorizes by priority, type, recency
        # 4. Extracts themes
        # 5. Generates reflection prompts
        pass
    
    async def get_reflection_context_additions(self) -> Dict[str, Any]:
        """THE KEY INTEGRATION POINT.
        
        Returns orphan state formatted for ReflectionContext.internal_state
        
        The structure returned is:
        {
            "orphan_memory": {
                "total_count": int,
                "critical_count": int,
                "high_value_content": List[Dict],
                "themes": List[str],
                "reflection_prompts": List[str],
                "type_distribution": Dict[str, int]
            }
        }
        """
        snapshot = await self.capture_orphan_context()
        
        return {
            "orphan_memory": {
                "total_count": snapshot.total_orphans,
                "critical_count": len(snapshot.critical_orphans),
                "high_value_content": [
                    {
                        "id": o["id"],
                        "type": o["node_type"],
                        "preview": self._truncate(o["content"], 200),
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
    
    def _truncate(self, text: str, max_len: int) -> str:
        if len(text) > max_len:
            return text[:max_len] + "..."
        return text


class ReflectionEngine:
    """ReflectionEngine uses OrphanReader to enrich reflection context.
    
    Key method: capture_context()
    This calls orphan_reader.get_reflection_context_additions() and merges
    the results into the ReflectionContext.internal_state
    """
    
    def __init__(self, orphan_reader: Optional[OrphanReader] = None):
        self.orphan_reader = orphan_reader
        self.reflection_history = []
    
    async def capture_context(self,
                             internal_state: Dict[str, Any],
                             recent_experiences: List[str],
                             current_goals: List[str],
                             environmental_factors: Optional[Dict[str, Any]] = None,
                             include_orphan_state: bool = True) -> ReflectionContext:
        """Capture context with orphan state integrated.
        
        THE KEY INTEGRATION:
        1. Takes base internal_state
        2. Calls orphan_reader.get_reflection_context_additions()
        3. Merges orphan_memory into internal_state
        4. Creates ReflectionContext with enriched state
        """
        # Enrich internal state with orphan memory information
        enriched_state = dict(internal_state) if internal_state else {}
        
        if include_orphan_state and self.orphan_reader:
            orphan_additions = await self.orphan_reader.get_reflection_context_additions()
            enriched_state.update(orphan_additions)
        
        # Create context with orphan state included
        context = ReflectionContext(
            timestamp=datetime.now().timestamp(),
            internal_state=enriched_state,  # Contains orphan_memory!
            recent_experiences=recent_experiences,
            current_goals=current_goals,
            environmental_factors=environmental_factors or {}
        )
        
        self.reflection_history.append(context)
        return context


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_integration():
    """Show how orphan content flows into reflection context."""
    
    print("\n" + "="*70)
    print("ORPHAN READER → REFLECTION CONTEXT INTEGRATION")
    print("="*70 + "\n")
    
    print("STEP 1: OrphanReader captures orphan state")
    print("-" * 70)
    print("OrphanReader.capture_orphan_context():")
    print("  • Queries memory for orphan nodes")
    print("  • Classifies using OrphanTaxonomyClassifier")
    print("  • Creates OrphanContextSnapshot with:")
    print("    - Categorized orphans (critical, high-value, recent)")
    print("    - Type distribution")
    print("    - Themes extracted from content")
    print("    - Reflection prompts for analysis")
    print("    - Immediate actions")
    print()
    
    print("STEP 2: OrphanReader formats for ReflectionContext")
    print("-" * 70)
    print("OrphanReader.get_reflection_context_additions():")
    print("  • Takes OrphanContextSnapshot")
    print("  • Formats into structure for ReflectionContext.internal_state")
    print("  • Returns dict with 'orphan_memory' key:")
    mock_additions = {
        "orphan_memory": {
            "total_count": 5,
            "critical_count": 1,
            "high_value_content": [
                {
                    "id": "orphan_001",
                    "type": "Experience",
                    "preview": "Encountered a novel pattern in user interaction...",
                    "category": "semantic_orphan",
                    "priority": "high"
                }
            ],
            "themes": ["System performance concerns", "User interaction patterns"],
            "reflection_prompts": [
                "Why do 1 critical orphans remain unreconciled?",
                "What patterns exist in the 3 high-value semantic orphans?"
            ],
            "type_distribution": {
                "semantic_orphan": 2,
                "dream_output": 1,
                "failed_reconciliation": 1,
                "noise_artifact": 1
            }
        }
    }
    print(json.dumps(mock_additions, indent=4))
    print()
    
    print("STEP 3: ReflectionEngine enriches context with orphan state")
    print("-" * 70)
    print("ReflectionEngine.capture_context():")
    print("  • Takes base internal_state from caller")
    print("  • Calls orphan_reader.get_reflection_context_additions()")
    print("  • Merges: internal_state.update(orphan_additions)")
    print("  • Creates ReflectionContext with enriched state")
    print()
    
    # Show before/after
    base_state = {
        "active_beliefs": 42,
        "learning_rate": 0.73,
        "confidence_threshold": 0.8
    }
    print("  Before internal_state:")
    print("  ", json.dumps(base_state, indent=2))
    print()
    
    enriched_state = dict(base_state)
    enriched_state.update(mock_additions)
    print("  After internal_state (with orphan_memory):")
    print("  ", json.dumps(enriched_state, indent=2))
    print()
    
    print("STEP 4: ReflectionContext contains orphan information")
    print("-" * 70)
    print("ReflectionContext structure:")
    context = {
        "timestamp": datetime.now().timestamp(),
        "internal_state": enriched_state,  # Contains orphan_memory!
        "recent_experiences": [
            "Processed 15 user queries",
            "Updated 3 beliefs"
        ],
        "current_goals": [
            "Improve response accuracy",
            "Reduce orphan accumulation"
        ],
        "environmental_factors": {
            "load": "medium"
        }
    }
    print(json.dumps(context, indent=2))
    print()
    
    print("STEP 5: Reflection analysis can use orphan content")
    print("-" * 70)
    print("Pattern analyzer can now:")
    print("  • Access context.internal_state['orphan_memory']")
    print("  • Analyze themes: ['System performance concerns', ...]")
    print("  • Consider prompts: ['Why do critical orphans remain...']")
    print("  • Review high_value_content for patterns")
    print("  • Generate desires based on orphan themes")
    print()
    
    print("Example desire emerging from orphan analysis:")
    example_desire = {
        "id": "desire_orphan_reduction",
        "description": "Implement automated reconciliation for high-value semantic orphans to reduce orphan accumulation and capture valuable isolated experiences",
        "desire_type": "capability",
        "origin": "orphan_memory.themes analysis",
        "confidence": 0.85
    }
    print(json.dumps(example_desire, indent=2))
    print()
    
    print("="*70)
    print("INTEGRATION COMPLETE")
    print("="*70)
    print()
    print("SUMMARY:")
    print("  1. OrphanReader captures and classifies orphan nodes")
    print("  2. get_reflection_context_additions() formats for ReflectionContext")
    print("  3. ReflectionEngine merges orphan state into internal_state")
    print("  4. ReflectionContext.internal_state contains 'orphan_memory' dict")
    print("  5. Pattern analysis and desire generation can access orphan content")
    print("  6. Desires can emerge from orphan content patterns")
    print()
    print("FILES INVOLVED:")
    print("  - orphan_reader.py: OrphanReader class")
    print("  - orphan_taxonomy.py: Classification and analysis")
    print("  - reflection_engine.py: ReflectionEngine with orphan integration")
    print()


if __name__ == "__main__":
    demonstrate_integration()
