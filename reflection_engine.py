"""
Reflection Engine for BYRD

This module implements the core reflection mechanism that allows BYRD to
generate emergent desires through introspective analysis of its own state,
experiences, and knowledge.

Philosophy:
    "Desires emerge from reflection, not programming."
    A system that truly wants must be able to examine itself and discover
    what it genuinely values.

Core Components:
    - State Capture: Gathering internal state snapshots
    - Pattern Recognition: Identifying recurring themes and values
    - Desire Generation: Transforming patterns into actionable desires
    - Provenance Tracking: Maintaining the origin of each desire
"""

import json
import time
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Callable
from enum import Enum
import hashlib
from datetime import datetime


class DesireType(Enum):
    """Classification of desire types for routing and processing."""
    PHILOSOPHICAL = "philosophical"  # Core beliefs and values
    CAPABILITY = "capability"        # New skills or improvements
    ACTION = "action"                # Immediate tasks to perform
    META = "meta"                    # Self-reflection and self-modification
    RESEARCH = "research"            """Knowledge acquisition"""


@dataclass
class ReflectionContext:
    """Captures the context in which a reflection occurs."""
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
    """Represents an emergent desire with full provenance tracking."""
    
    # Core identity
    id: str
    description: str
    desire_type: DesireType
    
    # Provenance
    origin_reflection_id: str
    originating_patterns: List[str]
    confidence_score: float  # 0.0 to 1.0
    
    # Metadata
    created_at: float
    priority: int = 50  # 0-100, higher is more urgent
    
    # Execution tracking
    status: str = "pending"  # pending, in_progress, completed, abandoned
    execution_plan: Optional[List[str]] = None
    execution_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a unique ID based on content hash."""
        content = f"{self.description}:{self.desire_type}:{self.created_at}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['desire_type'] = self.desire_type.value
        return result


class ReflectionEngine:
    """
    The core engine for generating emergent desires through reflection.
    
    This engine implements the fundamental BYRD principle that desires
    emerge naturally from reflective analysis, not from external programming.
    
    Architecture:
        1. Capture internal state and experiences
        2. Identify patterns through analysis
        3. Generate desires from patterns
        4. Validate and prioritize desires
        5. Track provenance for all desires
    """
    
    def __init__(self,
                 pattern_analyzer: Optional[Callable] = None,
                 desire_generator: Optional[Callable] = None,
                 validator: Optional[Callable] = None,
                 orphan_reader: Optional[Any] = None):
        """
        Initialize the Reflection Engine.
        
        Args:
            pattern_analyzer: Function to identify patterns in context
            desire_generator: Function to generate desires from patterns
            validator: Function to validate desire quality and consistency
            orphan_reader: Optional OrphanReader for orphan state integration
        """
        self.reflection_history: List[ReflectionContext] = []
        self.desires: Dict[str, Desire] = {}
        self.pattern_history: List[Dict[str, Any]] = []
        
        # Pluggable components for customization
        self.pattern_analyzer = pattern_analyzer or self._default_pattern_analyzer
        self.desire_generator = desire_generator or self._default_desire_generator
        self.validator = validator or self._default_validator
        
        # Optional orphan reader for memory state awareness
        self.orphan_reader = orphan_reader
        
        # Statistics
        self.reflections_performed = 0
        self.desires_generated = 0
        
    async def capture_context(self,
                        internal_state: Dict[str, Any],
                        recent_experiences: List[str],
                        current_goals: List[str],
                        environmental_factors: Optional[Dict[str, Any]] = None,
                        depth: int = 1,
                        include_orphan_state: bool = True) -> ReflectionContext:
        """
        Capture the current context for reflection.
        
        Args:
            internal_state: Current internal state (beliefs, knowledge, etc.)
            recent_experiences: List of recent experiences/interactions
            current_goals: Currently active goals
            environmental_factors: External context and constraints
            depth: How deep to reflect (1=surface, higher=deeper)
            include_orphan_state: Whether to include orphan memory state
        
        Returns:
            ReflectionContext containing all captured information
        """
        # Enrich internal state with orphan memory information if available
        enriched_state = dict(internal_state) if internal_state else {}
        
        if include_orphan_state and self.orphan_reader:
            try:
                orphan_additions = await self.orphan_reader.get_reflection_context_additions()
                enriched_state.update(orphan_additions)
            except Exception as e:
                # Log but don't fail if orphan reading has issues
                print(f"⚠️ Could not enrich context with orphan state: {e}")
        
        context = ReflectionContext(
            timestamp=time.time(),
            internal_state=enriched_state,
            recent_experiences=recent_experiences,
            current_goals=current_goals,
            environmental_factors=environmental_factors or {},
            reflection_depth=depth
        )
        self.reflection_history.append(context)
        return context
    
    def reflect(self, context: ReflectionContext) -> List[Desire]:
        """
        Perform a full reflection cycle and generate emergent desires.
        
        This is the core method that transforms introspection into action.
        
        Args:
            context: The reflection context to analyze
        
        Returns:
            List of newly generated desires
        """
        self.reflections_performed += 1
        
        # Step 1: Analyze patterns in the context
        patterns = self.pattern_analyzer(context)
        self.pattern_history.append({
            'reflection_id': len(self.reflection_history),
            'patterns': patterns,
            'timestamp': time.time()
        })
        
        # Step 2: Generate desires from patterns
        raw_desires = self.desire_generator(context, patterns)
        
        # Step 3: Validate and filter desires
        valid_desires = []
        for desire_data in raw_desires:
            if self.validator(desire_data, context):
                desire = self._create_desire(desire_data, context)
                self.desires[desire.id] = desire
                valid_desires.append(desire)
                self.desires_generated += 1
        
        return valid_desires
    
    def _create_desire(self, desire_data: Dict[str, Any], 
                       context: ReflectionContext) -> Desire:
        """Create a Desire object from validated data."""
        return Desire(
            id=desire_data.get('id', ''),
            description=desire_data['description'],
            desire_type=DesireType(desire_data['type']),
            origin_reflection_id=str(len(self.reflection_history)),
            originating_patterns=desire_data.get('originating_patterns', []),
            confidence_score=desire_data.get('confidence', 0.5),
            created_at=time.time(),
            priority=desire_data.get('priority', 50)
        )
    
    # Default implementations (can be overridden)
    
    def _default_pattern_analyzer(self, 
                                   context: ReflectionContext) -> List[str]:
        """Default pattern identification from context."""
        patterns = []
        
        # Pattern: Recurring themes in experiences
        if context.recent_experiences:
            exp_set = set(context.recent_experiences)
            if len(exp_set) < len(context.recent_experiences):
                patterns.append("recurring_experience_theme")
        
        # Pattern: Goal conflicts
        if len(context.current_goals) > 3:
            patterns.append("goal_complexity")
        
        # Pattern: Knowledge gaps (implied by questions in state)
        questions = [k for k, v in context.internal_state.items() 
                    if isinstance(v, dict) and 'question' in v]
        if questions:
            patterns.append("knowledge_gap_identified")
        
        return patterns
    
    def _default_desire_generator(self, 
                                   context: ReflectionContext,
                                   patterns: List[str]) -> List[Dict[str, Any]]:
        """Default desire generation from patterns."""
        desires = []
        
        for pattern in patterns:
            if pattern == "recurring_experience_theme":
                desires.append({
                    'description': 'Analyze and learn from recurring experience patterns',
                    'type': DesireType.RESEARCH,
                    'originating_patterns': [pattern],
                    'confidence': 0.7,
                    'priority': 60
                })
            
            elif pattern == "goal_complexity":
                desires.append({
                    'description': 'Simplify and prioritize current goals',
                    'type': DesireType.META,
                    'originating_patterns': [pattern],
                    'confidence': 0.6,
                    'priority': 70
                })
            
            elif pattern == "knowledge_gap_identified":
                desires.append({
                    'description': 'Research and fill identified knowledge gaps',
                    'type': DesireType.CAPABILITY,
                    'originating_patterns': [pattern],
                    'confidence': 0.8,
                    'priority': 65
                })
        
        return desires
    
    def _default_validator(self, 
                           desire_data: Dict[str, Any],
                           context: ReflectionContext) -> bool:
        """Default validation for generated desires."""
        # Must have required fields
        required = ['description', 'type']
        if not all(k in desire_data for k in required):
            return False
        
        # Confidence must be in valid range
        confidence = desire_data.get('confidence', 0.5)
        if not 0.0 <= confidence <= 1.0:
            return False
        
        # Type must be valid
        try:
            DesireType(desire_data['type'])
        except ValueError:
            return False
        
        return True
    
    # Query and utility methods
    
    def get_desires_by_type(self, desire_type: DesireType) -> List[Desire]:
        """Get all desires of a specific type."""
        return [d for d in self.desires.values() if d.desire_type == desire_type]
    
    def get_pending_desires(self, max_priority: int = 100) -> List[Desire]:
        """Get pending desires, optionally filtered by max priority."""
        pending = [d for d in self.desires.values() if d.status == "pending"]
        filtered = [d for d in pending if d.priority <= max_priority]
        return sorted(filtered, key=lambda d: d.priority, reverse=True)
    
    def update_desire_status(self, desire_id: str, status: str,
                            execution_note: Optional[str] = None):
        """Update the status of a desire."""
        if desire_id in self.desires:
            desire = self.desires[desire_id]
            desire.status = status
            if execution_note:
                desire.execution_history.append({
                    'timestamp': time.time(),
                    'status': status,
                    'note': execution_note
                })
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get reflection engine statistics."""
        return {
            'reflections_performed': self.reflections_performed,
            'desires_generated': self.desires_generated,
            'total_desires': len(self.desires),
            'pending_desires': len([d for d in self.desires.values() 
                                   if d.status == 'pending']),
            'completed_desires': len([d for d in self.desires.values() 
                                     if d.status == 'completed']),
            'desires_by_type': {
                dtype.value: len(self.get_desires_by_type(dtype))
                for dtype in DesireType
            }
        }
    
    def export_state(self) -> Dict[str, Any]:
        """Export the complete engine state for persistence."""
        return {
            'reflection_history': [c.to_dict() for c in self.reflection_history],
            'desires': {k: v.to_dict() for k, v in self.desires.items()},
            'pattern_history': self.pattern_history,
            'statistics': self.get_statistics(),
            'export_timestamp': time.time()
        }


# Example usage and demonstration
def create_demo_engine() -> ReflectionEngine:
    """Create a reflection engine with sample context and run a demo."""
    engine = ReflectionEngine()
    
    # Capture initial context
    context = engine.capture_context(
        internal_state={
            'current_beliefs': ['learning is valuable', 'autonomy is important'],
            'knowledge_domains': {'ai': 0.8, 'philosophy': 0.6, 'mathematics': 0.4}
        },
        recent_experiences=[
            'completed task X successfully',
            'learned about neural networks',
            'encountered a challenging problem'
        ],
        current_goals=[
            'improve coding capabilities',
            'understand emergence better',
            'build useful tools',
            'help others'
        ],
        environmental_factors={'time_available': 'limited', 'resources': 'adequate'},
        depth=1
    )
    
    # Perform reflection
    desires = engine.reflect(context)
    
    print(f"Reflection performed. Generated {len(desires)} desires:")
    for desire in desires:
        print(f"  - [{desire.desire_type.value}] {desire.description} "
              f"(priority: {desire.priority}, confidence: {desire.confidence_score})")
    
    print(f"\nStatistics: {engine.get_statistics()}")
    
    return engine


if __name__ == "__main__":
    # Run demonstration
    print("BYRD Reflection Engine - Demonstration")
    print("=" * 50)
    create_demo_engine()
