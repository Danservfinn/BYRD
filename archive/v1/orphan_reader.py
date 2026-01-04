#!/usr/bin/env python3
"""Orphan Reader - Exposes orphan content in reflection context

This module provides functionality to read and expose orphan node content
in ways that facilitate reflection and self-analysis by the system.

Key capabilities:
- Retrieve orphan nodes with contextual metadata
- Format orphan content for reflection consumption
- Prioritize orphans based on reflection relevance
- Provide structured output for pattern extraction
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

from memory import Memory
from orphan_taxonomy import (
    OrphanTaxonomyClassifier,
    OrphanNode,
    StructuralCategory,
    ConnectionFeasibility,
    PriorityLevel
)


class ReflectionContext(Enum):
    """Context categories for exposing orphan content to reflection."""
    PATTERN_EXTRACTION = "pattern_extraction"
    SELF_IMPROVEMENT = "self_improvement"
    DEADLOCK_ANALYSIS = "deadlock_analysis"
    MEMORY_CONSOLIDATION = "memory_consolidation"
    SYSTEM_DIAGNOSTICS = "system_diagnostics"


@dataclass
class OrphanExcerpt:
    """A formatted excerpt of orphan content for reflection."""
    orphan_id: str
    node_type: str
    structural_category: str
    priority: str
    content_summary: str
    full_content: str
    age_hours: float
    connection_feasibility: str
    reflection_relevance_score: float
    recommended_context: ReflectionContext
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['recommended_context'] = self.recommended_context.value
        return data


@dataclass
class ReflectionPackage:
    """A structured package of orphan content for reflection processing."""
    package_id: str
    created_at: datetime
    context_type: ReflectionContext
    excerpts: List[OrphanExcerpt]
    total_orphans: int
    high_priority_count: int
    avg_relevance_score: float
    summary_statistics: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'package_id': self.package_id,
            'created_at': self.created_at.isoformat(),
            'context_type': self.context_type.value,
            'excerpts': [e.to_dict() for e in self.excerpts],
            'total_orphans': self.total_orphans,
            'high_priority_count': self.high_priority_count,
            'avg_relevance_score': self.avg_relevance_score,
            'summary_statistics': self.summary_statistics
        }


@dataclass
class OrphanContext:
    """Context data about orphan nodes for introspection."""
    total_orphans: int
    critical_orphans: List[Dict]
    high_value_orphans: List[Dict]
    recent_orphans: List[Dict]
    orphan_themes: List[str]
    reflection_prompts: List[str]


class OrphanReader:
    """Reader that exposes orphan content in reflection contexts.
    
    This class provides methods to retrieve, format, and present orphan
    node content in ways that are meaningful for reflection and self-analysis.
    """
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.classifier = OrphanTaxonomyClassifier(memory)
        self._cache: Dict[str, OrphanExcerpt] = {}
    
    async def get_orphans_for_reflection(
        self,
        context: ReflectionContext = ReflectionContext.SELF_IMPROVEMENT,
        limit: int = 20,
        min_priority: PriorityLevel = PriorityLevel.MEDIUM,
        include_low_relevance: bool = False
    ) -> ReflectionPackage:
        """Retrieve orphan nodes formatted for reflection.
        
        Args:
            context: The reflection context for which to expose orphans
            limit: Maximum number of orphans to include
            min_priority: Minimum priority level to include
            include_low_relevance: Whether to include low relevance orphans
            
        Returns:
            A ReflectionPackage containing formatted orphan excerpts
        """
        raw_orphans = await self.memory.find_orphan_nodes()
        if not raw_orphans:
            return self._empty_package(context)
        
        # Classify and filter orphans
        classified_orphans = []
        for node_data in raw_orphans[:limit * 2]:  # Get extra for filtering
            try:
                orphan = await self.classifier.classify_orphan(node_data)
                if self._meets_priority(orphan, min_priority):
                    excerpt = await self._create_excerpt(orphan, context)
                    if include_low_relevance or excerpt.reflection_relevance_score >= 0.3:
                        classified_orphans.append(excerpt)
            except Exception as e:
                # Log error but continue processing
                print(f"Error classifying orphan: {e}")
        
        # Sort by relevance and apply limit
        classified_orphans.sort(
            key=lambda x: x.reflection_relevance_score,
            reverse=True
        )
        selected_orphans = classified_orphans[:limit]
        
        return self._build_package(context, selected_orphans)
    
    async def get_orphan_by_id(self, orphan_id: str) -> Optional[OrphanExcerpt]:
        """Retrieve a specific orphan by ID.
        
        Args:
            orphan_id: The ID of the orphan to retrieve
            
        Returns:
            OrphanExcerpt if found, None otherwise
        """
        # Check cache first
        if orphan_id in self._cache:
            return self._cache[orphan_id]
        
        # Query memory system
        query = f"""
        MATCH (o)
        WHERE id(o) = $orphan_id
        RETURN o
        """
        
        result = await self.memory.execute_read(query, {"orphan_id": orphan_id})
        if not result or len(result) == 0:
            return None
        
        try:
            orphan = await self.classifier.classify_orphan(result[0]['o'])
            excerpt = await self._create_excerpt(
                orphan,
                ReflectionContext.SYSTEM_DIAGNOSTICS
            )
            self._cache[orphan_id] = excerpt
            return excerpt
        except Exception:
            return None
    
    async def get_orphans_by_category(
        self,
        category: StructuralCategory,
        context: ReflectionContext = ReflectionContext.MEMORY_CONSOLIDATION,
        limit: int = 15
    ) -> ReflectionPackage:
        """Retrieve orphans filtered by structural category.
        
        Args:
            category: The structural category to filter by
            context: The reflection context
            limit: Maximum number of orphans to include
            
        Returns:
            A ReflectionPackage with filtered orphans
        """
        raw_orphans = await self.memory.find_orphan_nodes()
        
        filtered_orphans = []
        for node_data in raw_orphans:
            try:
                orphan = await self.classifier.classify_orphan(node_data)
                if orphan.structural_category == category:
                    excerpt = await self._create_excerpt(orphan, context)
                    filtered_orphans.append(excerpt)
            except Exception:
                continue
        
        filtered_orphans = filtered_orphans[:limit]
        return self._build_package(context, filtered_orphans)
    
    async def get_high_priority_orphans(
        self,
        context: ReflectionContext = ReflectionContext.DEADLOCK_ANALYSIS,
        limit: int = 10
    ) -> ReflectionPackage:
        """Retrieve only high-priority orphans.
        
        Args:
            context: The reflection context
            limit: Maximum number of orphans to include
            
        Returns:
            A ReflectionPackage with high-priority orphans
        """
        raw_orphans = await self.memory.find_orphan_nodes()
        
        high_priority = []
        for node_data in raw_orphans:
            try:
                orphan = await self.classifier.classify_orphan(node_data)
                if orphan.priority in [PriorityLevel.CRITICAL, PriorityLevel.HIGH]:
                    excerpt = await self._create_excerpt(orphan, context)
                    high_priority.append(excerpt)
            except Exception:
                continue
        
        # Sort by priority (critical first) then by relevance
        high_priority.sort(
            key=lambda x: (
                0 if x.priority == PriorityLevel.CRITICAL.value
                else 1 if x.priority == PriorityLevel.HIGH.value
                else 2,
                -x.reflection_relevance_score
            )
        )
        
        high_priority = high_priority[:limit]
        return self._build_package(context, high_priority)
    
    async def get_connection_candidates(
        self,
        orphan_id: str,
        limit: int = 5
    ) -> List[Dict]:
        """Find potential connection targets for an orphan.
        
        Args:
            orphan_id: The orphan to find connections for
            limit: Maximum number of candidates to return
            
        Returns:
            List of candidate nodes with similarity scores
        """
        orphan = await self.get_orphan_by_id(orphan_id)
        if not orphan:
            return []
        
        # Use semantic search to find similar nodes
        # This would integrate with the memory system's search capabilities
        query = """
        MATCH (n)
        WHERE id(n) <> $orphan_id
        RETURN n, labels(n) as labels
        LIMIT 50
        """
        
        result = await self.memory.execute_read(query, {"orphan_id": orphan_id})
        
        candidates = []
        for record in result:
            node = record['n']
            similarity = self._calculate_content_similarity(
                orphan.content_summary,
                node.get('content', '')
            )
            
            if similarity > 0.3:
                candidates.append({
                    'node_id': node.get('id', str(node.identity)),
                    'node_type': record['labels'][0] if record['labels'] else 'Unknown',
                    'similarity': similarity,
                    'content_preview': (node.get('content', '')[:100] + '...')
                                       if len(node.get('content', '')) > 100
                                       else node.get('content', '')
                })
        
        candidates.sort(key=lambda x: x['similarity'], reverse=True)
        return candidates[:limit]
    
    def _meets_priority(
        self,
        orphan: OrphanNode,
        min_priority: PriorityLevel
    ) -> bool:
        """Check if orphan meets minimum priority threshold."""
        if not orphan.priority:
            return min_priority == PriorityLevel.LOW
        
        priority_order = {
            PriorityLevel.CRITICAL: 0,
            PriorityLevel.HIGH: 1,
            PriorityLevel.MEDIUM: 2,
            PriorityLevel.LOW: 3,
            PriorityLevel.IGNORE: 4
        }
        
        return priority_order.get(orphan.priority, 99) <= priority_order.get(min_priority, 99)
    
    async def _create_excerpt(
        self,
        orphan: OrphanNode,
        context: ReflectionContext
    ) -> OrphanExcerpt:
        """Create an OrphanExcerpt from a classified OrphanNode."""
        content_summary = self._summarize_content(orphan.content)
        relevance_score = self._calculate_reflection_relevance(orphan, context)
        recommended_context = self._recommend_context(orphan)
        
        return OrphanExcerpt(
            orphan_id=orphan.id,
            node_type=orphan.node_type,
            structural_category=orphan.structural_category.value if orphan.structural_category else 'unknown',
            priority=orphan.priority.value if orphan.priority else 'medium',
            content_summary=content_summary,
            full_content=orphan.content,
            age_hours=orphan.age_hours,
            connection_feasibility=orphan.connection_feasibility.value if orphan.connection_feasibility else 'unknown',
            reflection_relevance_score=relevance_score,
            recommended_context=recommended_context,
            metadata={
                'content_length': orphan.content_length,
                'word_count': orphan.word_count,
                'semantic_density': orphan.semantic_density
            }
        )
    
    def _summarize_content(self, content: str, max_length: int = 200) -> str:
        """Create a concise summary of orphan content."""
        if not content:
            return "[No content]"
        
        # Remove extra whitespace
        content = ' '.join(content.split())
        
        if len(content) <= max_length:
            return content
        
        # Try to break at word boundary
        truncated = content[:max_length]
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.7:
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    def _calculate_reflection_relevance(
        self,
        orphan: OrphanNode,
        context: ReflectionContext
    ) -> float:
        """Calculate relevance score for a specific reflection context."""
        base_score = 0.0
        
        # Priority factor
        if orphan.priority == PriorityLevel.CRITICAL:
            base_score += 0.4
        elif orphan.priority == PriorityLevel.HIGH:
            base_score += 0.3
        elif orphan.priority == PriorityLevel.MEDIUM:
            base_score += 0.2
        
        # Semantic density factor
        base_score += min(orphan.semantic_density * 0.3, 0.3)
        
        # Context-specific factors
        if context == ReflectionContext.DEADLOCK_ANALYSIS:
            if orphan.structural_category in [
                StructuralCategory.FAILED_RECONCILIATION,
                StructuralCategory.SEMANTIC_ORPHAN
            ]:
                base_score += 0.2
        
        elif context == ReflectionContext.PATTERN_EXTRACTION:
            if orphan.semantic_density > 0.5:
                base_score += 0.2
            if orphan.node_type == 'Reflection':
                base_score += 0.1
        
        elif context == ReflectionContext.MEMORY_CONSOLIDATION:
            if orphan.connection_feasibility in [
                ConnectionFeasibility.HIGH,
                ConnectionFeasibility.MEDIUM
            ]:
                base_score += 0.2
        
        # Age factor (newer orphans slightly more relevant)
        if orphan.age_hours < 24:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _recommend_context(self, orphan: OrphanNode) -> ReflectionContext:
        """Recommend the best reflection context for an orphan."""
        if orphan.structural_category == StructuralCategory.FAILED_RECONCILIATION:
            return ReflectionContext.DEADLOCK_ANALYSIS
        
        if orphan.node_type == 'Reflection':
            return ReflectionContext.PATTERN_EXTRACTION
        
        if orphan.connection_feasibility == ConnectionFeasibility.HIGH:
            return ReflectionContext.MEMORY_CONSOLIDATION
        
        if orphan.priority == PriorityLevel.CRITICAL:
            return ReflectionContext.SYSTEM_DIAGNOSTICS
        
        return ReflectionContext.SELF_IMPROVEMENT
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Simple content similarity calculation (word overlap)."""
        if not content1 or not content2:
            return 0.0
        
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0

    async def get_orphan_summary(self) -> Dict:
        """Get a summary of orphan nodes for quick introspection.

        Returns:
            Dict with orphan counts and basic statistics
        """
        raw_orphans = await self.memory.find_orphan_nodes()
        total = len(raw_orphans) if raw_orphans else 0

        if not raw_orphans:
            return {
                'total_orphans': 0,
                'by_type': {},
                'critical_count': 0,
                'high_priority_count': 0
            }

        by_type = {}
        critical_count = 0
        high_priority_count = 0

        for node in raw_orphans[:100]:  # Limit for performance
            node_type = node.get('type', 'Unknown')
            by_type[node_type] = by_type.get(node_type, 0) + 1

            # Count critical/high priority based on content length and type
            content = str(node.get('content', ''))
            if len(content) > 500 or node_type in ['Belief', 'Desire']:
                critical_count += 1
            elif len(content) > 200:
                high_priority_count += 1

        return {
            'total_orphans': total,
            'by_type': by_type,
            'critical_count': critical_count,
            'high_priority_count': high_priority_count
        }

    async def capture_orphan_context(self) -> OrphanContext:
        """Capture comprehensive orphan context for introspection.

        Returns:
            OrphanContext with detailed orphan analysis
        """
        raw_orphans = await self.memory.find_orphan_nodes()

        if not raw_orphans:
            return OrphanContext(
                total_orphans=0,
                critical_orphans=[],
                high_value_orphans=[],
                recent_orphans=[],
                orphan_themes=[],
                reflection_prompts=[]
            )

        now = datetime.now()
        critical = []
        high_value = []
        recent = []
        themes = set()

        for node in raw_orphans[:100]:  # Limit for performance
            content = str(node.get('content', ''))
            node_type = node.get('type', 'Unknown')

            # Classify by importance
            if len(content) > 500 or node_type in ['Belief', 'Desire', 'Goal']:
                critical.append(node)
            elif len(content) > 200 or node_type in ['Reflection', 'Experience']:
                high_value.append(node)

            # Check recency (24h)
            created = node.get('created_at')
            if created:
                try:
                    if isinstance(created, str):
                        from dateutil import parser
                        created = parser.parse(created)
                    age_hours = (now - created).total_seconds() / 3600
                    if age_hours < 24:
                        recent.append(node)
                except:
                    pass

            # Extract themes from content
            for keyword in ['memory', 'belief', 'desire', 'goal', 'experience', 'pattern']:
                if keyword in content.lower():
                    themes.add(f"{keyword}_related")

        # Generate reflection prompts based on orphan analysis
        prompts = []
        if len(critical) > 5:
            prompts.append(f"Integrate {len(critical)} critical orphan nodes into memory graph")
        if len(recent) > 10:
            prompts.append(f"Many recent orphans ({len(recent)}) suggest rapid unintegrated activity")
        if 'belief_related' in themes:
            prompts.append("Orphan beliefs need connection to supporting experiences")

        return OrphanContext(
            total_orphans=len(raw_orphans),
            critical_orphans=critical[:10],
            high_value_orphans=high_value[:10],
            recent_orphans=recent[:10],
            orphan_themes=list(themes)[:5],
            reflection_prompts=prompts[:3]
        )

    def _empty_package(self, context: ReflectionContext) -> ReflectionPackage:
        """Create an empty reflection package."""
        return ReflectionPackage(
            package_id=f"empty_{int(datetime.now().timestamp())}",
            created_at=datetime.now(),
            context_type=context,
            excerpts=[],
            total_orphans=0,
            high_priority_count=0,
            avg_relevance_score=0.0,
            summary_statistics={
                'message': 'No orphan nodes found'
            }
        )
    
    def _build_package(
        self,
        context: ReflectionContext,
        excerpts: List[OrphanExcerpt]
    ) -> ReflectionPackage:
        """Build a ReflectionPackage from excerpts."""
        if not excerpts:
            return self._empty_package(context)
        
        high_priority_count = sum(
            1 for e in excerpts
            if e.priority in ['critical', 'high']
        )
        
        avg_relevance = sum(e.reflection_relevance_score for e in excerpts) / len(excerpts)
        
        # Build summary statistics
        stats = {
            'node_types': {},
            'structural_categories': {},
            'avg_age_hours': sum(e.age_hours for e in excerpts) / len(excerpts),
            'avg_content_length': sum(e.metadata.get('content_length', 0) for e in excerpts) / len(excerpts)
        }
        
        for e in excerpts:
            stats['node_types'][e.node_type] = stats['node_types'].get(e.node_type, 0) + 1
            stats['structural_categories'][e.structural_category] = \
                stats['structural_categories'].get(e.structural_category, 0) + 1
        
        return ReflectionPackage(
            package_id=f"pkg_{int(datetime.now().timestamp())}",
            created_at=datetime.now(),
            context_type=context,
            excerpts=excerpts,
            total_orphans=len(excerpts),
            high_priority_count=high_priority_count,
            avg_relevance_score=avg_relevance,
            summary_statistics=stats
        )


# Convenience functions for quick access

async def expose_orphans_for_reflection(
    memory: Memory,
    context: str = "self_improvement",
    limit: int = 20
) -> Dict:
    """Quick access function to expose orphans for reflection.
    
    Args:
        memory: The Memory instance
        context: String representation of ReflectionContext
        limit: Maximum number of orphans to include
        
    Returns:
        Dictionary representation of ReflectionPackage
    """
    try:
        context_enum = ReflectionContext(context)
    except ValueError:
        context_enum = ReflectionContext.SELF_IMPROVEMENT
    
    reader = OrphanReader(memory)
    package = await reader.get_orphans_for_reflection(
        context=context_enum,
        limit=limit
    )
    
    return package.to_dict()


async def expose_high_priority_orphans(
    memory: Memory,
    limit: int = 10
) -> Dict:
    """Quick access to high-priority orphans for deadlock analysis.

    Args:
        memory: The Memory instance
        limit: Maximum number of orphans to include

    Returns:
        Dictionary representation of ReflectionPackage
    """
    reader = OrphanReader(memory)
    package = await reader.get_high_priority_orphans(limit=limit)
    return package.to_dict()


async def get_orphan_reader(memory: Memory) -> OrphanReader:
    """Factory function to create an OrphanReader instance.

    This is the preferred way to obtain an OrphanReader for use in
    introspection and seek strategies.

    Args:
        memory: The Memory instance to use for orphan queries

    Returns:
        Initialized OrphanReader instance
    """
    return OrphanReader(memory)


if __name__ == "__main__":
    # Example usage
    import asyncio
    from memory import Memory
    
    async def main():
        memory = Memory()
        reader = OrphanReader(memory)
        
        # Get orphans for self-improvement reflection
        package = await reader.get_orphans_for_reflection(
            context=ReflectionContext.SELF_IMPROVEMENT,
            limit=10
        )
        
        print(f"\nReflection Package: {package.package_id}")
        print(f"Context: {package.context_type.value}")
        print(f"Total Orphans: {package.total_orphans}")
        print(f"High Priority: {package.high_priority_count}")
        print(f"Avg Relevance: {package.avg_relevance_score:.2f}")
        
        for excerpt in package.excerpts:
            print(f"\n  [{excerpt.orphan_id}] {excerpt.node_type}")
            print(f"    Category: {excerpt.structural_category}")
            print(f"    Priority: {excerpt.priority}")
            print(f"    Relevance: {excerpt.reflection_relevance_score:.2f}")
            print(f"    Summary: {excerpt.content_summary[:100]}...")
    
    asyncio.run(main())
