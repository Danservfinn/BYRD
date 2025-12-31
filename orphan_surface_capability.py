#!/usr/bin/env python3
"""
Orphan Surface Capability

Breaks the desires-without-execution loop by actually surfacing orphan content.

This capability:
1. Queries Neo4j for orphan nodes (disconnected content)
2. Classifies them using orphan_taxonomy
3. Surfaces high-value orphans in an actionable format
4. Provides a bridge between the bypass loop and actual execution

PHILOSOPHY:
- Desires without execution create orphaned potential
- This potential must be surfaced to become actionable
- Not all orphans are noise - many are deferred actions
- Breaking the loop requires making the invisible visible
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict

try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None
    print("[!] neo4j package not installed - will work in demo mode")

# Define fallback classes if orphan_taxonomy is not available
if OrphanTaxonomyClassifier is None:
    from enum import Enum
    
    class StructuralCategory(Enum):
        ISOLATED_OBSERVATION = "isolated_observation"
        SEMANTIC_ORPHAN = "semantic_orphan"
        NOISE_ARTIFACT = "noise_artifact"
        
    class ConnectionFeasibility(Enum):
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        
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
class SurfacedOrphan:
    """An orphan that has been surfaced for action."""
    orphan: OrphanNode
    surface_time: datetime
    surface_method: str  # "console", "report", "queue", "direct"
    action_taken: str
    action_result: str
    
    def to_dict(self) -> Dict:
        return {
            "orphan": asdict(self.orphan),
            "surface_time": self.surface_time.isoformat(),
            "surface_method": self.surface_method,
            "action_taken": self.action_taken,
            "action_result": self.action_result
        }


class OrphanSurfaceCapability:
    """
    Capability that surfaces orphan content to break the desires-without-execution loop.
    
    This is the bridge between:
    - Local graph connector (creates pending actions as nodes)
    - Actual execution (needs actionable content)
    
    By surfacing orphans, we:
    1. Make invisible potential visible
    2. Provide actionable content to systems that can execute
    3. Break the infinite loop of desire → pending action → orphan
    """
    
    # High-priority node types to surface immediately
    CRITICAL_TYPES = ["PendingAction", "Desire", "Reflection", "Experience"]
    
    # Minimum content length to surface (filter noise)
    MIN_SURFACE_LENGTH = 20
    
    def __init__(
        self,
        neo4j_uri: Optional[str] = None,
        neo4j_user: Optional[str] = None,
        neo4j_password: Optional[str] = None
    ):
        self.uri = neo4j_uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = neo4j_user or os.getenv("NEO4J_USER", "neo4j")
        self.password = neo4j_password or os.getenv("NEO4J_PASSWORD", "password")
        
        self.classifier = OrphanTaxonomyClassifier() if OrphanTaxonomyClassifier else None
        self.driver = None
        self._connected = False
        
        # Surface history
        self.surfaced_count = 0
        self.surfaced_history: List[SurfacedOrphan] = []
        
    async def connect(self) -> bool:
        """Connect to Neo4j."""
        if not GraphDatabase:
            return False
            
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            self.driver.verify_connectivity()
            self._connected = True
            return True
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            return False
    
    async def query_orphans(self) -> List[Dict]:
        """Query Neo4j for orphan nodes."""
        if not self._connected:
            return []
            
        query = "MATCH (n) WHERE NOT (n)-[]-() RETURN n"
        
        orphans = []
        try:
            with self.driver.session() as session:
                result = session.run(query)
                for record in result:
                    node = record["n"]
                    orphans.append({
                        "element_id": str(node.element_id),
                        "labels": list(node.labels),
                        "properties": dict(node._properties)
                    })
        except Exception as e:
            print(f"[!] Query failed: {e}")
            
        return orphans
    
    async def classify_orphan(self, orphan_data: Dict) -> Optional[OrphanNode]:
        """Classify an orphan using taxonomy."""
        if not self.classifier:
            # Basic classification without taxonomy
            props = orphan_data.get("properties", {})
            return OrphanNode(
                id=orphan_data["element_id"],
                node_type=orphan_data["labels"][0] if orphan_data["labels"] else "Unknown",
                content=props.get("content", props.get("description", "")),
                created_at=datetime.fromisoformat(props.get("created_at", datetime.now().isoformat()))
            )
        
        # Use full taxonomy classifier
        return await self.classifier.classify_orphan(orphan_data["properties"])
    
    def should_surface(self, orphan: OrphanNode) -> Tuple[bool, str]:
        """Determine if an orphan should be surfaced."""
        # Filter by content length
        if orphan.content_length < self.MIN_SURFACE_LENGTH:
            return False, "Too short (noise)"
        
        # Filter by critical types
        if orphan.node_type in self.CRITICAL_TYPES:
            return True, f"Critical type: {orphan.node_type}"
        
        # Filter by priority if classified
        if orphan.priority in [PriorityLevel.CRITICAL, PriorityLevel.HIGH]:
            return True, f"High priority: {orphan.priority.value}"
        
        # Filter by connection feasibility
        if orphan.connection_feasibility == ConnectionFeasibility.HIGH:
            return True, "High connection feasibility"
        
        # Filter by structural category
        if orphan.structural_category in [
            StructuralCategory.ISOLATED_OBSERVATION,
            StructuralCategory.SEMANTIC_ORPHAN
        ]:
            return True, f"Actionable category: {orphan.structural_category.value}"
        
        return False, "Low priority or not actionable"
    
    def surface_to_console(self, orphan: OrphanNode, reason: str) -> SurfacedOrphan:
        """Surface an orphan to console output."""
        print("\n" + "=" * 70)
        print("SURFACED ORPHAN - ACTIONABLE CONTENT")
        print("=" * 70)
        print(f"ID: {orphan.id}")
        print(f"Type: {orphan.node_type}")
        print(f"Priority: {orphan.priority.value if orphan.priority else 'N/A'}")
        print(f"Category: {orphan.structural_category.value if orphan.structural_category else 'N/A'}")
        print(f"Reason surfaced: {reason}")
        print(f"Content: {orphan.content}")
        print(f"Recommended: {orphan.recommended_action}")
        print("=" * 70)
        
        surfaced = SurfacedOrphan(
            orphan=orphan,
            surface_time=datetime.now(),
            surface_method="console",
            action_taken="displayed",
            action_result="content made visible"
        )
        
        self.surfaced_history.append(surfaced)
        self.surfaced_count += 1
        
        return surfaced
    
    def surface_to_report(self, orphans: List[OrphanNode], output_file: str = "surfaced_orphans.json"):
        """Surface orphans to a JSON report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_orphans_analyzed": len(orphans),
            "orphans_surfaced": len([o for o in orphans if self.should_surface(o)[0]]),
            "surfaced_orphans": [
                asdict(o) for o in orphans if self.should_surface(o)[0]
            ]
        }
        
        Path(output_file).write_text(json.dumps(report, indent=2, default=str))
        print(f"[+] Report written to {output_file}")
        
    async def surface_high_priority_orphans(
        self,
        max_orphans: int = 10,
        methods: List[str] = None
    ) -> Dict:
        """
        Main entry point: Query, classify, and surface high-priority orphans.
        
        This breaks the loop by:
        1. Finding orphans created by the bypass mechanism
        2. Classifying them to understand their potential
        3. Surfacing them in actionable format
        
        Args:
            max_orphans: Maximum number of orphans to surface
            methods: List of surface methods (default: ["console", "report"])
        
        Returns:
            Summary of what was surfaced
        """
        methods = methods or ["console", "report"]
        
        print("\n" + "=" * 70)
        print("ORPHAN SURFACE CAPABILITY - BREAKING THE LOOP")
        print("=" * 70)
        print(f"Time: {datetime.now()}")
        print()
        
        # Connect if not already
        if not self._connected:
            if not await self.connect():
                print("[!] Cannot connect to Neo4j")
                return {"success": False, "error": "connection_failed"}
        
        # Query orphans
        print("[1] Querying orphan nodes...")
        orphan_data = await self.query_orphans()
        print(f"    Found {len(orphan_data)} orphan node(s)")
        
        if not orphan_data:
            print("[+] No orphans found - system clean")
            return {"success": True, "orphans_found": 0, "orphans_surfaced": 0}
        
        # Classify orphans
        print("[2] Classifying orphans...")
        classified = []
        for data in orphan_data:
            orphan = await self.classify_orphan(data)
            if orphan:
                classified.append(orphan)
        print(f"    Classified {len(classified)} orphans")
        
        # Filter and surface high-priority
        print("[3] Surfacing high-priority orphans...")
        surfaced = []
        for orphan in classified[:max_orphans]:
            should, reason = self.should_surface(orphan)
            if should:
                if "console" in methods:
                    surfaced.append(self.surface_to_console(orphan, reason))
                if "report" in methods:
                    surfaced.append(orphan)
        
        # Generate report
        if "report" in methods:
            self.surface_to_report(classified)
        
        # Summary
        print("\n" + "=" * 70)
        print("SURFACE SUMMARY")
        print("=" * 70)
        print(f"Total orphans analyzed: {len(classified)}")
        print(f"Orphans surfaced: {len(surfaced)}")
        print(f"Loop breakage: {'ACTIVE' if surfaced else 'NONE NEEDED'}")
        print("=" * 70)
        
        return {
            "success": True,
            "orphans_found": len(classified),
            "orphans_surfaced": len(surfaced),
            "surfaced_details": [s.to_dict() for s in surfaced if isinstance(s, SurfacedOrphan)],
            "loop_broken": len(surfaced) > 0
        }
    
    async def close(self):
        """Close Neo4j connection."""
        if self.driver:
            self.driver.close()
            self._connected = False


async def main():
    """CLI entry point."""
    capability = OrphanSurfaceCapability()
    
    try:
        result = await capability.surface_high_priority_orphans()
        
        # Exit code based on whether we broke the loop
        if result.get("loop_broken"):
            print("\n[+] Successfully surfaced orphan content")
            print("[+] Desires-without-execution loop broken")
            return 0
        else:
            print("\n[+] No actionable orphans found")
            return 0
            
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        return 1
    except Exception as e:
        import traceback
        print(f"\n[!] Error: {e}")
        traceback.print_exc()
        return 1
    finally:
        await capability.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
