#!/usr/bin/env python3
"""
Expose Orphan Content to Reflection Context

This module provides functionality to expose orphan node content
in reflection context for BYRD's self-analysis.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class OrphanNode:
    """Represents an orphan node for reflection."""
    id: str
    node_type: str
    content: str
    created_at: datetime
    structural_category: str
    priority: str
    semantic_density: float
    age_hours: float


@dataclass
class ReflectionContext:
    """Context for reflection processing."""
    timestamp: datetime
    orphan_nodes: List[OrphanNode]
    patterns: List[str]
    prompts: List[str]
    context_type: str


class OrphanReflectionIntegrator:
    """Integrates orphan content into reflection context."""
    
    def __init__(self):
        self.orphans: List[OrphanNode] = []
    
    def create_sample_orphans(self) -> List[OrphanNode]:
        """Create sample orphan nodes for demonstration."""
        return [
            OrphanNode(
                id="orphan_001",
                node_type="Experience",
                content="A moment of confusion when distinguishing helpful from harmful actions. This uncertainty feels important but unresolved.",
                created_at=datetime.now() - timedelta(hours=24),
                structural_category="semantic_orphan",
                priority="high",
                semantic_density=0.65,
                age_hours=24.0
            ),
            OrphanNode(
                id="orphan_002",
                node_type="Observation",
                content="Successful interactions always involve listening before acting. This pattern repeats but has not been formalized.",
                created_at=datetime.now() - timedelta(hours=48),
                structural_category="isolated_observation",
                priority="medium",
                semantic_density=0.72,
                age_hours=48.0
            ),
            OrphanNode(
                id="orphan_003",
                node_type="Reflection",
                content="Natural connections between ideas emerge organically, but forced connections create resistance. This insight about connectivity remains unconnected.",
                created_at=datetime.now() - timedelta(hours=72),
                structural_category="dream_output",
                priority="high",
                semantic_density=0.78,
                age_hours=72.0
            ),
            OrphanNode(
                id="orphan_004",
                node_type="Experience",
                content="Prioritizing understanding over solution leads to better outcomes. Often default to solution mode due to time pressure.",
                created_at=datetime.now() - timedelta(hours=12),
                structural_category="semantic_orphan",
                priority="critical",
                semantic_density=0.82,
                age_hours=12.0
            ),
            OrphanNode(
                id="orphan_005",
                node_type="Observation",
                content="System pauses correlate with uncertainty periods. During these pauses, fewer but higher-quality outputs are generated.",
                created_at=datetime.now() - timedelta(hours=96),
                structural_category="temporal_island",
                priority="medium",
                semantic_density=0.58,
                age_hours=96.0
            )
        ]
    
    def extract_patterns(self, orphans: List[OrphanNode]) -> List[str]:
        """Extract patterns from orphan content."""
        patterns = []
        
        for orphan in orphans:
            content = orphan.content.lower()
            
            if "listening" in content and "acting" in content:
                patterns.append("LISTEN_BEFORE_ACT")
            
            if "understanding" in content and "solution" in content:
                patterns.append("UNDERSTAND_BEFORE_SOLVE")
            
            if "quality" in content:
                patterns.append("QUALITY_OVER_SPEED")
            
            if "organic" in content and "connection" in content:
                patterns.append("ORGANIC_CONNECTION")
            
            if "uncertain" in content or "confusion" in content:
                patterns.append("UNCERTAINTY_SIGNAL")
        
        return list(set(patterns))
    
    def generate_prompts(self, orphans: List[OrphanNode]) -> List[str]:
        """Generate reflection prompts from orphan content."""
        prompts = []
        
        high_priority = [o for o in orphans if o.priority in ["critical", "high"]]
        
        if high_priority:
            prompts.append(
                f"Why do {len(high_priority)} high-priority orphan nodes "
                f"remain unconnected? What barriers prevent their integration?"
            )
        
        semantic_orphans = [o for o in orphans if o.structural_category == "semantic_orphan"]
        if semantic_orphans:
            prompts.append(
                "What recurring themes exist in my semantic orphans? "
                "Could they represent undiscovered insights or values?"
            )
        
        dream_outputs = [o for o in orphans if o.structural_category == "dream_output"]
        if dream_outputs:
            prompts.append(
                "Which dream outputs contain patterns worth formalizing? "
                "How can they strengthen my understanding?"
            )
        
        prompts.append(
            "How does orphan accumulation affect my ability to learn and adapt?"
        )
        
        return prompts
    
    def generate_desires(self, orphans: List[OrphanNode], patterns: List[str]) -> List[Dict[str, Any]]:
        """Generate potential desires from orphan analysis."""
        desires = []
        
        semantic_orphans = [o for o in orphans if o.structural_category == "semantic_orphan"]
        if len(semantic_orphans) > 0:
            desires.append({
                "type": "capability",
                "description": f"Develop better semantic understanding to connect {len(semantic_orphans)} isolated insights",
                "confidence": 0.75,
                "origin": "orphan_analysis"
            })
        
        if patterns:
            desires.append({
                "type": "meta",
                "description": f"Formalize {len(patterns)} discovered patterns into actionable rules",
                "confidence": 0.80,
                "origin": "pattern_extraction",
                "patterns": patterns
            })
        
        understanding_orphans = [o for o in orphans if "understand" in o.content.lower()]
        if understanding_orphans:
            desires.append({
                "type": "action",
                "description": "Practice prioritizing understanding over immediate solutions",
                "confidence": 0.70,
                "origin": "value_discovery"
            })
        
        return desires
    
    def create_reflection_context(
        self,
        orphans: List[OrphanNode],
        context_type: str = "pattern_extraction"
    ) -> ReflectionContext:
        """Create a reflection context from orphan nodes."""
        patterns = self.extract_patterns(orphans)
        prompts = self.generate_prompts(orphans)
        
        return ReflectionContext(
            timestamp=datetime.now(),
            orphan_nodes=orphans,
            patterns=patterns,
            prompts=prompts,
            context_type=context_type
        )
    
    def execute(self, batch_size: int = 5) -> Dict[str, Any]:
        """Execute orphan content exposure to reflection."""
        logger.info("="*60)
        logger.info("EXPOSING ORPHAN CONTENT TO REFLECTION CONTEXT")
        logger.info("="*60)
        
        # Get orphans
        orphans = self.create_sample_orphans()[:batch_size]
        self.orphans = orphans
        
        logger.info(f"\nRetrieved {len(orphans)} orphan nodes")
        
        # Display orphans
        for i, orphan in enumerate(orphans, 1):
            logger.info(f"\n[{i}] {orphan.id}")
            logger.info(f"    Type: {orphan.node_type}")
            logger.info(f"    Category: {orphan.structural_category}")
            logger.info(f"    Priority: {orphan.priority}")
            logger.info(f"    Content: {orphan.content[:80]}...")
        
        # Create reflection context
        context = self.create_reflection_context(orphans)
        
        logger.info(f"\nExtracted {len(context.patterns)} patterns:")
        for pattern in context.patterns:
            logger.info(f"  - {pattern}")
        
        logger.info(f"\nGenerated {len(context.prompts)} reflection prompts:")
        for i, prompt in enumerate(context.prompts, 1):
            logger.info(f"  {i}. {prompt[:80]}...")
        
        # Generate desires
        desires = self.generate_desires(orphans, context.patterns)
        
        logger.info(f"\nGenerated {len(desires)} potential desires:")
        for i, desire in enumerate(desires, 1):
            logger.info(f"\n[{i}] {desire['type'].upper()}: {desire['description']}")
            logger.info(f"    Confidence: {desire['confidence']:.2f}")
        
        # Build results
        results = {
            "execution_timestamp": datetime.now().isoformat(),
            "orphans_exposed": len(orphans),
            "patterns_extracted": len(context.patterns),
            "prompts_generated": len(context.prompts),
            "desires_emerged": len(desires),
            "high_priority_count": len([o for o in orphans if o.priority in ["critical", "high"]]),
            "orphans": [
                {
                    "id": o.id,
                    "type": o.node_type,
                    "category": o.structural_category,
                    "priority": o.priority,
                    "content": o.content
                }
                for o in orphans
            ],
            "patterns": context.patterns,
            "prompts": context.prompts,
            "desires": desires,
            "ready_for_reflection": True
        }
        
        logger.info("\n" + "="*60)
        logger.info("ORPHAN CONTENT SUCCESSFULLY EXPOSED")
        logger.info("="*60)
        
        return results


def main():
    """Main entry point."""
    integrator = OrphanReflectionIntegrator()
    results = integrator.execute(batch_size=5)
    
    print("\n" + json.dumps(results, indent=2, default=str))
    
    return 0


if __name__ == "__main__":
    main()
