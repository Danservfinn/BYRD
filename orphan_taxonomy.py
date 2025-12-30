#!/usr/bin/env python3
"""Orphan Node Taxonomic Classifier"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from memory import Memory
import yaml


class StructuralCategory(Enum):
    ISOLATED_OBSERVATION = "isolated_observation"
    FAILED_RECONCILIATION = "failed_reconciliation"
    NOISE_ARTIFACT = "noise_artifact"
    SEMANTIC_ORPHAN = "semantic_orphan"
    TEMPORAL_ISLAND = "temporal_island"
    DREAM_OUTPUT = "dream_output"
    SYSTEM_METADATA = "system_metadata"
    UNKNOWN_TYPE = "unknown_type"


class ConnectionFeasibility(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    IMPOSSIBLE = "impossible"


class PriorityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    IGNORE = "ignore"


@dataclass
class OrphanNode:
    id: str
    node_type: str
    content: str
    created_at: datetime
    structural_category: Optional[StructuralCategory] = None
    connection_feasibility: Optional[ConnectionFeasibility] = None
    priority: Optional[PriorityLevel] = None
    content_length: int = 0
    word_count: int = 0
    semantic_density: float = 0.0
    age_hours: float = 0.0
    recommended_action: str = ""


@dataclass
class TaxonomyReport:
    analysis_timestamp: datetime
    total_orphans: int
    nodes: List[OrphanNode]
    category_distribution: Dict[str, int] = field(default_factory=dict)
    feasibility_distribution: Dict[str, int] = field(default_factory=dict)
    priority_distribution: Dict[str, int] = field(default_factory=dict)
    type_distribution: Dict[str, int] = field(default_factory=dict)
    critical_nodes: List[OrphanNode] = field(default_factory=list)
    immediate_actions: List[str] = field(default_factory=list)


class OrphanTaxonomyClassifier:
    MIN_CONTENT_LENGTH = 20
    SEMANTIC_DENSITY_THRESHOLD = 0.3
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    async def classify_orphan(self, node_data: Dict) -> OrphanNode:
        content = node_data.get('content', node_data.get('description', ''))
        
        orphan = OrphanNode(
            id=node_data.get('id', ''),
            node_type=node_data.get('type', 'Unknown'),
            content=content,
            created_at=self._parse_datetime(node_data.get('created_at'))
        )
        
        orphan.content_length = len(orphan.content)
        orphan.word_count = len(orphan.content.split())
        orphan.semantic_density = self._calculate_semantic_density(orphan.content)
        orphan.age_hours = self._calculate_age_hours(orphan.created_at)
        
        orphan.structural_category = self._determine_category(orphan)
        orphan.connection_feasibility = self._assess_feasibility(orphan)
        orphan.priority = self._determine_priority(orphan)
        orphan.recommended_action = self._generate_recommendation(orphan)
        
        return orphan
    
    def _determine_category(self, orphan: OrphanNode) -> StructuralCategory:
        if orphan.content_length < self.MIN_CONTENT_LENGTH:
            return StructuralCategory.NOISE_ARTIFACT
        
        if orphan.node_type == 'Reflection':
            return StructuralCategory.DREAM_OUTPUT
        
        if orphan.node_type == 'SystemState':
            return StructuralCategory.SYSTEM_METADATA
        
        if orphan.age_hours > 720:
            return StructuralCategory.TEMPORAL_ISLAND
        
        if orphan.node_type == 'Experience':
            return StructuralCategory.ISOLATED_OBSERVATION
        
        return StructuralCategory.SEMANTIC_ORPHAN
    
    def _assess_feasibility(self, orphan: OrphanNode) -> ConnectionFeasibility:
        if orphan.structural_category == StructuralCategory.NOISE_ARTIFACT:
            return ConnectionFeasibility.IMPOSSIBLE
        
        if orphan.semantic_density >= self.SEMANTIC_DENSITY_THRESHOLD * 2:
            return ConnectionFeasibility.HIGH
        
        if orphan.content_length >= self.MIN_CONTENT_LENGTH:
            return ConnectionFeasibility.MEDIUM
        
        return ConnectionFeasibility.LOW
    
    def _determine_priority(self, orphan: OrphanNode) -> PriorityLevel:
        if orphan.structural_category == StructuralCategory.NOISE_ARTIFACT:
            return PriorityLevel.IGNORE
        
        if orphan.connection_feasibility == ConnectionFeasibility.HIGH:
            return PriorityLevel.HIGH
        
        if orphan.structural_category == StructuralCategory.DREAM_OUTPUT:
            return PriorityLevel.HIGH
        
        return PriorityLevel.MEDIUM
    
    def _generate_recommendation(self, orphan: OrphanNode) -> str:
        if orphan.structural_category == StructuralCategory.NOISE_ARTIFACT:
            return "Archive or delete"
        
        if orphan.connection_feasibility == ConnectionFeasibility.HIGH:
            return "Connect using semantic search"
        
        if orphan.structural_category == StructuralCategory.DREAM_OUTPUT:
            return "Link to source experiences"
        
        return "Standard connection procedure"
    
    def _calculate_semantic_density(self, content: str) -> float:
        if not content:
            return 0.0
        words = content.lower().split()
        if not words:
            return 0.0
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                   'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                   'could', 'should', 'may', 'might', 'must', 'shall', 'can',
                   'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
                   'as', 'into', 'through', 'during', 'before', 'after', 'above',
                   'below', 'between', 'under', 'again', 'further', 'then', 'once',
                   'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each',
                   'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                   'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just'}
        meaningful = [w for w in words if w not in stopwords and len(w) > 2]
        return len(meaningful) / len(words)
    
    def _calculate_age_hours(self, created_at: Optional[datetime]) -> float:
        if not created_at:
            return 0.0
        return (datetime.now() - created_at).total_seconds() / 3600
    
    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        if not dt_str:
            return None
        try:
            if isinstance(dt_str, datetime):
                return dt_str
            return datetime.fromisoformat(str(dt_str).replace('Z', '+00:00'))
        except:
            return None


class OrphanTaxonomyAnalyzer:
    def __init__(self, memory):
        self.memory = memory
        self.classifier = OrphanTaxonomyClassifier(memory)
    
    async def analyze_all_orphans(self, limit=50):
        orphans = await self.memory.find_orphan_nodes()
        if not orphans:
            return TaxonomyReport(
                analysis_timestamp=datetime.now(),
                total_orphans=0,
                nodes=[]
            )
        
        nodes = []
        for node_data in orphans[:limit]:
            orphan = await self.classifier.classify_orphan(node_data)
            nodes.append(orphan)
        
        return self._build_report(nodes)
    
    def _build_report(self, nodes):
        report = TaxonomyReport(
            analysis_timestamp=datetime.now(),
            total_orphans=len(nodes),
            nodes=nodes
        )
        
        for node in nodes:
            if node.structural_category:
                cat = node.structural_category.value
                report.category_distribution[cat] = report.category_distribution.get(cat, 0) + 1
            if node.connection_feasibility:
                feas = node.connection_feasibility.value
                report.feasibility_distribution[feas] = report.feasibility_distribution.get(feas, 0) + 1
            if node.priority:
                pri = node.priority.value
                report.priority_distribution[pri] = report.priority_distribution.get(pri, 0) + 1
            report.type_distribution[node.node_type] = report.type_distribution.get(node.node_type, 0) + 1
        
        return report
    
    def print_report(self, report):
        print("\nORPHAN NODE TAXONOMIC CLASSIFICATION")
        print("=" * 50)
        print(f"Analysis Time: {report.analysis_timestamp}")
        print(f"Total Orphans: {report.total_orphans}")
        
        print("\nStructural Categories:")
        for cat, count in sorted(report.category_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}")
        
        print("\nConnection Feasibility:")
        for feas, count in sorted(report.feasibility_distribution.items(), key=lambda x: x[1], reverse=True):
            pct = count / report.total_orphans * 100 if report.total_orphans else 0
            print(f"  {feas}: {count} ({pct:.1f}%)")
        
        print("\nPriorities:")
        for pri, count in sorted(report.priority_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"  {pri}: {count}")
        
        print("\nNode Types:")
        for typ, count in sorted(report.type_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"  {typ}: {count}")


async def run_analysis():
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
    
    memory = Memory(config)
    await memory.initialize()
    
    analyzer = OrphanTaxonomyAnalyzer(memory)
    report = await analyzer.analyze_all_orphans(50)
    
    analyzer.print_report(report)
    
    await memory.close()
    return report


if __name__ == "__main__":
    asyncio.run(run_analysis())

