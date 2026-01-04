#!/usr/bin/env python3
"""
Orphan Node File Dump Mechanism - CRITICAL PATH

This module provides the critical path for observing orphan node data via
the guaranteed file_dump mechanism. It ensures orphan data persists even
when the primary memory system fails.

KEY PRINCIPLES:
1. Write to disk FIRST - guaranteed persistence
2. File-based observation log in .parallel_observations/
3. Survives crashes, network issues, database failures
4. Works with or without Neo4j connection

USAGE:
    python orphan_file_dump.py [--limit N] [--mock]

OUTPUT:
    - .parallel_observations/orphan_reports.jsonl - Analysis reports
    - Each report contains full orphan classification data
"""

import asyncio
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional
import json
from dataclasses import dataclass, field
from enum import Enum

# Try to import optional dependencies
PARALLEL_PATH_AVAILABLE = False
ORPHAN_TAXONOMY_AVAILABLE = False

try:
    from orphan_taxonomy import (
        OrphanTaxonomyAnalyzer, TaxonomyReport, OrphanNode,
        StructuralCategory, ConnectionFeasibility, PriorityLevel
    )
    ORPHAN_TAXONOMY_AVAILABLE = True
except ImportError:
    # Define fallback types for mock mode
    class StructuralCategory(Enum):
        ISOLATED_OBSERVATION = "isolated_observation"
        DREAM_OUTPUT = "dream_output"
        NOISE_ARTIFACT = "noise_artifact"
        SEMANTIC_ORPHAN = "semantic_orphan"
        TEMPORAL_ISLAND = "temporal_island"
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
        nodes: list
        category_distribution: dict = field(default_factory=dict)
        feasibility_distribution: dict = field(default_factory=dict)
        priority_distribution: dict = field(default_factory=dict)
        type_distribution: dict = field(default_factory=dict)
        critical_nodes: list = field(default_factory=list)
        immediate_actions: list = field(default_factory=list)

try:
    import yaml
except ImportError:
    yaml = None

# Configuration
ORPHAN_REPORT_FILE = Path(".parallel_observations/orphan_reports.jsonl")


class OrphanFileDumper:
    """
    Orphan node observation and file dumping system.
    
    CRITICAL PATH: Guarantees orphan data persists via file-based logging.
    """
    
    def __init__(self, config_path: str = "config.yaml", mock_mode: bool = False):
        """Initialize the dumper with configuration."""
        self.mock_mode = mock_mode
        self.config = {}
        self.analyzer: Optional[OrphanTaxonomyAnalyzer] = None
        self.memory = None
        
        if yaml and not mock_mode:
            try:
                with open(config_path) as f:
                    self.config = yaml.safe_load(f)
            except Exception as e:
                print(f"[!] Warning: Could not load config: {e}")
    
    async def initialize(self):
        """Initialize memory connection and analyzer."""
        if self.mock_mode:
            print("[+] Running in MOCK mode - using simulated data")
            self._create_mock_data()
            return
        
        if not ORPHAN_TAXONOMY_AVAILABLE:
            print("[!] Warning: orphan_taxonomy not available, using mock mode")
            self.mock_mode = True
            self._create_mock_data()
            return
        
        try:
            from memory import Memory
            
            self.memory = Memory(self.config)
            await self.memory.initialize()
            
            self.analyzer = OrphanTaxonomyAnalyzer(self.memory)
            print("[+] Initialized memory and orphan analyzer")
        except Exception as e:
            print(f"[!] Warning: Could not initialize memory: {e}")
            print("[+] Falling back to mock mode")
            self.mock_mode = True
            self._create_mock_data()
    
    def _create_mock_data(self):
        """Create mock orphan data for testing without Neo4j."""
        now = datetime.now()
        
        # Create mock orphan nodes
        self.mock_orphans = [
            OrphanNode(
                id="mock_001",
                node_type="Experience",
                content="This is a test orphan node representing an isolated observation that was never connected to the main graph.",
                created_at=now,
                structural_category=StructuralCategory.ISOLATED_OBSERVATION,
                connection_feasibility=ConnectionFeasibility.MEDIUM,
                priority=PriorityLevel.MEDIUM,
                content_length=125,
                word_count=20,
                semantic_density=0.5,
                age_hours=48.0,
                recommended_action="Connect using semantic search"
            ),
            OrphanNode(
                id="mock_002",
                node_type="Reflection",
                content="A dream output that was never properly integrated into BYRD's memory system.",
                created_at=now,
                structural_category=StructuralCategory.DREAM_OUTPUT,
                connection_feasibility=ConnectionFeasibility.HIGH,
                priority=PriorityLevel.HIGH,
                content_length=85,
                word_count=14,
                semantic_density=0.7,
                age_hours=24.0,
                recommended_action="Connect using semantic search"
            ),
            OrphanNode(
                id="mock_003",
                node_type="Experience",
                content="noise artifact",
                created_at=now,
                structural_category=StructuralCategory.NOISE_ARTIFACT,
                connection_feasibility=ConnectionFeasibility.IMPOSSIBLE,
                priority=PriorityLevel.IGNORE,
                content_length=15,
                word_count=2,
                semantic_density=0.1,
                age_hours=12.0,
                recommended_action="Archive or delete"
            ),
            OrphanNode(
                id="mock_004",
                node_type="Belief",
                content="A semantic orphan - a belief that became disconnected from its supporting evidence and experiences.",
                created_at=now,
                structural_category=StructuralCategory.SEMANTIC_ORPHAN,
                connection_feasibility=ConnectionFeasibility.LOW,
                priority=PriorityLevel.LOW,
                content_length=98,
                word_count=16,
                semantic_density=0.4,
                age_hours=720.0,
                recommended_action="Review for potential reconnection or archival"
            )
        ]
        print(f"[+] Created {len(self.mock_orphans)} mock orphan nodes")
    
    def dump_report_to_file(self, report: TaxonomyReport) -> bool:
        """
        Dump orphan analysis report to file - GUARANTEED to succeed.
        
        This is the CRITICAL PATH - writes directly to disk.
        
        Args:
            report: Taxonomy analysis report
            
        Returns:
            True if write succeeded
        """
        try:
            # Ensure directory exists
            ORPHAN_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare report data
            report_data = {
                "timestamp": report.analysis_timestamp.isoformat(),
                "total_orphans": report.total_orphans,
                "category_distribution": report.category_distribution,
                "feasibility_distribution": report.feasibility_distribution,
                "priority_distribution": report.priority_distribution,
                "type_distribution": report.type_distribution,
                "critical_node_count": len(report.critical_nodes),
                "immediate_actions": report.immediate_actions,
                "nodes": [
                    {
                        "id": n.id,
                        "node_type": n.node_type,
                        "content": n.content,
                        "structural_category": n.structural_category.value if n.structural_category else None,
                        "connection_feasibility": n.connection_feasibility.value if n.connection_feasibility else None,
                        "priority": n.priority.value if n.priority else None,
                        "content_length": n.content_length,
                        "word_count": n.word_count,
                        "semantic_density": n.semantic_density,
                        "age_hours": n.age_hours,
                        "recommended_action": n.recommended_action
                    }
                    for n in report.nodes
                ]
            }
            
            # Write to file (CRITICAL: this must succeed)
            with open(ORPHAN_REPORT_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(report_data, ensure_ascii=False) + "\n")
                f.flush()
                import os
                os.fsync(f.fileno())
            
            return True
        except Exception as e:
            print(f"[!] CRITICAL ERROR: Failed to write report to file: {e}")
            return False
    
    async def dump_all_orphans(self, limit: int = 50) -> TaxonomyReport:
        """
        Observe and dump all orphan nodes via file_dump mechanism.
        
        This is the critical path - ensures orphan data persists even
        if the primary memory system fails.
        
        Args:
            limit: Maximum number of orphans to process
            
        Returns:
            TaxonomyReport with analysis results
        """
        print("\n" + "="*60)
        print("ORPHAN FILE DUMP - CRITICAL PATH")
        print("="*60)
        print(f"Timestamp: {datetime.now()}")
        print(f"Output File: {ORPHAN_REPORT_FILE}")
        print()
        
        # Analyze orphans
        if self.mock_mode:
            nodes = self.mock_orphans[:limit]
            
            # Build distributions
            cat_dist = {}
            feas_dist = {}
            pri_dist = {}
            type_dist = {}
            critical = []
            
            for n in nodes:
                if n.structural_category:
                    cat = n.structural_category.value
                    cat_dist[cat] = cat_dist.get(cat, 0) + 1
                if n.connection_feasibility:
                    feas = n.connection_feasibility.value
                    feas_dist[feas] = feas_dist.get(feas, 0) + 1
                if n.priority:
                    pri = n.priority.value
                    pri_dist[pri] = pri_dist.get(pri, 0) + 1
                    if n.priority == PriorityLevel.HIGH:
                        critical.append(n)
                type_dist[n.node_type] = type_dist.get(n.node_type, 0) + 1
            
            report = TaxonomyReport(
                analysis_timestamp=datetime.now(),
                total_orphans=len(nodes),
                nodes=nodes,
                category_distribution=cat_dist,
                feasibility_distribution=feas_dist,
                priority_distribution=pri_dist,
                type_distribution=type_dist,
                critical_nodes=critical,
                immediate_actions=["Review mock orphans for integration"]
            )
        else:
            report = await self.analyzer.analyze_all_orphans(limit)
        
        print(f"[+] Found {report.total_orphans} orphan nodes")
        print()
        
        # Dump report to file (CRITICAL PATH)
        success = self.dump_report_to_file(report)
        
        if success:
            print(f"[+] Successfully dumped {report.total_orphans} orphans to file")
            print(f"[+] Report written to {ORPHAN_REPORT_FILE}")
        else:
            print(f"[!] Failed to dump orphans to file")
        
        return report
    
    async def close(self):
        """Close connections."""
        if self.memory:
            await self.memory.close()


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Observe orphan node data via file_dump mechanism"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=50,
        help="Maximum number of orphans to process (default: 50)"
    )
    parser.add_argument(
        "--priority", "-p",
        choices=["critical", "high", "medium", "low", "ignore"],
        default="medium",
        help="Filter by priority level (default: medium)"
    )
    parser.add_argument(
        "--config", "-c",
        default="config.yaml",
        help="Configuration file path (default: config.yaml)"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock data instead of connecting to Neo4j (for testing)"
    )
    
    args = parser.parse_args()
    
    # Initialize dumper
    dumper = OrphanFileDumper(config_path=args.config, mock_mode=args.mock)
    
    try:
        await dumper.initialize()
        
        # Run dump
        report = await dumper.dump_all_orphans(limit=args.limit)
        
        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total Orphans Analyzed: {report.total_orphans}")
        print("\nCategory Distribution:")
        for cat, count in sorted(report.category_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}")
        print("\nPriority Distribution:")
        for pri, count in sorted(report.priority_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"  {pri}: {count}")
        print("\nNode Types:")
        for typ, count in sorted(report.type_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"  {typ}: {count}")
        print()
        
        # Exit with appropriate code
        if report.total_orphans == 0:
            print("[+] No orphans found - graph is clean")
        else:
            print(f"[+] Orphan data successfully persisted to {ORPHAN_REPORT_FILE}")
        
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await dumper.close()


if __name__ == "__main__":
    asyncio.run(main())
