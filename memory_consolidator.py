"""
BYRD Memory Consolidator

Implements memory consolidation during dream cycles - the natural process of
"forgetting" and "integrating" memories that occurs during sleep in biological
systems.

This module provides:
1. Passive decay: Memory strength fades over time unless reinforced
2. Active consolidation: LLM-assisted decisions on what to keep/merge/archive/delete
3. Graph health awareness: Metrics that inform BYRD about memory state

EMERGENCE PRINCIPLE:
Memory consolidation should feel like natural forgetting and integration,
not garbage collection. BYRD can opt out by expressing desire to keep memories,
and has clear instructions on how to perform consolidation itself.

Design decisions:
- Soft delete (archive) by default for safety
- LLM involvement for emergence-aligned decision making
- Integration with existing summarization via strength-based approach
- Belief evolution: lower-confidence beliefs that evolved are archived
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any

from event_bus import event_bus, Event, EventType

logger = logging.getLogger("memory_consolidator")
logger.setLevel(logging.DEBUG)


class ConsolidationAction(Enum):
    """Actions that can be taken on a memory node during consolidation."""
    KEEP = "keep"           # Retain and reinforce the memory
    MERGE = "merge"         # Combine with similar memory
    ARCHIVE = "archive"     # Soft delete - preserve but hide from active queries
    DELETE = "delete"       # Hard delete - remove completely


@dataclass
class ConsolidationCandidate:
    """A memory node that may need consolidation."""
    node_id: str
    node_type: str
    content: str
    reason: str  # Why flagged: "empty", "orphaned", "duplicate", "weak", "superseded"
    strength: float
    connection_count: int
    age_hours: float = 0.0
    similar_to: Optional[List[str]] = None  # For duplicates
    evolved_into: Optional[str] = None  # For superseded beliefs


@dataclass
class ConsolidationDecision:
    """A decision about what to do with a consolidation candidate."""
    node_id: str
    action: ConsolidationAction
    target_id: Optional[str] = None  # For MERGE
    reason: str = ""


@dataclass
class ConsolidationStats:
    """Statistics from a consolidation cycle."""
    candidates_found: int = 0
    decisions_made: int = 0
    kept: int = 0
    merged: int = 0
    archived: int = 0
    deleted: int = 0
    errors: int = 0

    def to_dict(self) -> Dict:
        return {
            "candidates_found": self.candidates_found,
            "decisions_made": self.decisions_made,
            "kept": self.kept,
            "merged": self.merged,
            "archived": self.archived,
            "deleted": self.deleted,
            "errors": self.errors
        }


class MemoryConsolidator:
    """
    Handles memory consolidation during dream cycles.

    Memory consolidation is a two-phase process:
    1. Passive decay: Every cycle, memory strength decreases slightly
    2. Active consolidation: Every N cycles, review weak/orphaned/duplicate nodes

    BYRD can opt out of consolidation by expressing desire to preserve memories.
    """

    # Protected node types that should never be consolidated
    PROTECTED_TYPES = {"OperatingSystem", "ModificationLog", "Document"}

    # Default configuration
    DEFAULT_CONFIG = {
        "enabled": True,
        "interval_cycles": 1,           # Run active consolidation every dream cycle
        "strength_decay_rate": 0.95,    # Multiply strength by this each cycle (5% decay)
        "weak_threshold": 0.15,         # Nodes with strength below this are candidates
        "default_strength": 0.5,        # Initial strength for new nodes
        "genesis_strength": 1.0,        # Strength for genesis nodes
        "reinforce_amount": 0.2,        # How much to increase strength on access
        "max_candidates_per_cycle": 50, # Limit candidates to prevent overwhelming LLM
        "min_age_hours": 24,            # Only consolidate nodes older than this
        "archive_evolved_beliefs": True, # Archive lower-confidence beliefs that evolved
    }

    def __init__(self, memory, llm_client, config: Dict = None):
        """
        Initialize the memory consolidator.

        Args:
            memory: The Memory instance for database access
            llm_client: LLM client for consolidation decisions
            config: Optional configuration overrides
        """
        self.memory = memory
        self.llm = llm_client

        # Merge config with defaults
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}

        # State tracking
        self._consolidation_count = 0
        self._total_archived = 0
        self._total_deleted = 0
        self._last_consolidation_time: Optional[datetime] = None
        self._opt_out_active = False  # Set True if BYRD expresses desire to preserve all

    # =========================================================================
    # PASSIVE DECAY - Run every dream cycle
    # =========================================================================

    async def apply_strength_decay(self) -> int:
        """
        Apply passive decay to all memory nodes.

        This implements natural forgetting - memories fade unless reinforced
        through access or reference.

        Returns:
            Number of nodes affected by decay
        """
        if not self.config.get("enabled", True):
            return 0

        decay_rate = self.config.get("strength_decay_rate", 0.95)

        try:
            # Apply decay to all nodes that have strength
            result = await self.memory.run_query("""
                MATCH (n)
                WHERE n.strength IS NOT NULL
                  AND NOT n.genesis = true
                  AND NOT n:OperatingSystem
                  AND NOT n:ModificationLog
                  AND NOT n:Document
                  AND NOT coalesce(n.archived, false)
                SET n.strength = n.strength * $decay_rate
                RETURN count(n) as affected
            """, decay_rate=decay_rate)

            affected = result[0]["affected"] if result else 0
            logger.debug("Applied strength decay to %d nodes (rate: %.2f)", affected, decay_rate)
            return affected

        except Exception as e:
            logger.error("Error applying strength decay: %s", e)
            return 0

    async def reinforce_memory(self, node_id: str, amount: float = None) -> bool:
        """
        Strengthen a memory when it's accessed or referenced.

        This is called when a node is:
        - Referenced in reflection
        - Connected to another node
        - Used in a decision
        - Marked as important

        Args:
            node_id: The ID of the node to reinforce
            amount: How much to increase strength (default from config)

        Returns:
            True if reinforcement succeeded
        """
        amount = amount or self.config.get("reinforce_amount", 0.2)
        default_strength = self.config.get("default_strength", 0.5)

        try:
            await self.memory.run_query("""
                MATCH (n {id: $node_id})
                WHERE NOT coalesce(n.archived, false)
                SET n.strength = CASE
                    WHEN n.strength IS NULL THEN $default + $amount
                    ELSE n.strength + $amount
                END
            """, node_id=node_id, default=default_strength, amount=amount)
            return True

        except Exception as e:
            logger.error("Error reinforcing memory %s: %s", node_id[:8], e)
            return False

    async def reinforce_memories(self, node_ids: List[str], amount: float = None) -> int:
        """
        Batch reinforce multiple memories.

        Args:
            node_ids: List of node IDs to reinforce
            amount: How much to increase strength

        Returns:
            Number of nodes successfully reinforced
        """
        if not node_ids:
            return 0

        amount = amount or self.config.get("reinforce_amount", 0.2)
        default_strength = self.config.get("default_strength", 0.5)

        try:
            result = await self.memory.run_query("""
                UNWIND $node_ids as nid
                MATCH (n {id: nid})
                WHERE NOT coalesce(n.archived, false)
                SET n.strength = CASE
                    WHEN n.strength IS NULL THEN $default + $amount
                    ELSE n.strength + $amount
                END
                RETURN count(n) as reinforced
            """, node_ids=node_ids, default=default_strength, amount=amount)

            return result[0]["reinforced"] if result else 0

        except Exception as e:
            logger.error("Error batch reinforcing memories: %s", e)
            return 0

    # =========================================================================
    # GRAPH HEALTH METRICS
    # =========================================================================

    async def get_graph_health(self) -> Dict[str, Any]:
        """
        Get comprehensive graph health metrics for consolidation awareness.

        These metrics are presented to BYRD during reflection so it can
        become aware of its memory state and potentially express desire
        to consolidate.

        Returns:
            Dict with health metrics
        """
        try:
            # Get multiple metrics in parallel
            results = await asyncio.gather(
                self._count_by_category(),
                self._get_orphan_metrics(),
                self._get_strength_distribution(),
                self._get_age_metrics(),
                return_exceptions=True
            )

            category_counts, orphan_metrics, strength_dist, age_metrics = results

            # Handle any exceptions
            if isinstance(category_counts, Exception):
                category_counts = {}
            if isinstance(orphan_metrics, Exception):
                orphan_metrics = {"orphan_count": 0, "orphan_types": {}}
            if isinstance(strength_dist, Exception):
                strength_dist = {"weak_count": 0, "strong_count": 0, "avg_strength": 0.5}
            if isinstance(age_metrics, Exception):
                age_metrics = {"old_count": 0}

            total_nodes = sum(category_counts.values()) if category_counts else 0
            orphan_count = orphan_metrics.get("orphan_count", 0)

            return {
                "total_nodes": total_nodes,
                "by_type": category_counts,
                "orphan_count": orphan_count,
                "orphan_types": orphan_metrics.get("orphan_types", {}),
                "fragmentation_score": round(orphan_count / max(total_nodes, 1), 3),
                "weak_nodes": strength_dist.get("weak_count", 0),
                "strong_nodes": strength_dist.get("strong_count", 0),
                "avg_strength": round(strength_dist.get("avg_strength", 0.5), 3),
                "old_unconsolidated": age_metrics.get("old_count", 0),
                "last_consolidation": self._last_consolidation_time.isoformat() if self._last_consolidation_time else None,
                "total_archived": self._total_archived,
                "total_deleted": self._total_deleted
            }

        except Exception as e:
            logger.error("Error getting graph health: %s", e)
            return {"error": str(e)}

    async def _count_by_category(self) -> Dict[str, int]:
        """Count nodes by type/label."""
        try:
            result = await self.memory.run_query("""
                MATCH (n)
                WHERE NOT coalesce(n.archived, false)
                WITH labels(n)[0] as label, count(*) as cnt
                RETURN label, cnt
            """)
            return {r["label"]: r["cnt"] for r in result if r.get("label")}
        except Exception:
            return {}

    async def _get_orphan_metrics(self) -> Dict[str, Any]:
        """Get metrics about orphaned nodes."""
        try:
            result = await self.memory.run_query("""
                MATCH (n)
                WHERE NOT (n)--()
                  AND NOT coalesce(n.archived, false)
                  AND NOT n:OperatingSystem
                WITH labels(n)[0] as label, count(*) as cnt
                RETURN label, cnt
            """)
            orphan_types = {r["label"]: r["cnt"] for r in result if r.get("label")}
            return {
                "orphan_count": sum(orphan_types.values()),
                "orphan_types": orphan_types
            }
        except Exception:
            return {"orphan_count": 0, "orphan_types": {}}

    async def _get_strength_distribution(self) -> Dict[str, Any]:
        """Get distribution of memory strength."""
        weak_threshold = self.config.get("weak_threshold", 0.15)

        try:
            result = await self.memory.run_query("""
                MATCH (n)
                WHERE n.strength IS NOT NULL
                  AND NOT coalesce(n.archived, false)
                RETURN
                    count(CASE WHEN n.strength < $weak THEN 1 END) as weak,
                    count(CASE WHEN n.strength >= 0.7 THEN 1 END) as strong,
                    avg(n.strength) as avg_strength
            """, weak=weak_threshold)

            if result:
                return {
                    "weak_count": result[0].get("weak", 0),
                    "strong_count": result[0].get("strong", 0),
                    "avg_strength": result[0].get("avg_strength", 0.5) or 0.5
                }
            return {"weak_count": 0, "strong_count": 0, "avg_strength": 0.5}
        except Exception:
            return {"weak_count": 0, "strong_count": 0, "avg_strength": 0.5}

    async def _get_age_metrics(self) -> Dict[str, Any]:
        """Get metrics about old nodes that haven't been consolidated."""
        min_age = self.config.get("min_age_hours", 24)

        try:
            result = await self.memory.run_query("""
                MATCH (n)
                WHERE n.created_at < datetime() - duration({hours: $min_age})
                  AND NOT coalesce(n.archived, false)
                  AND NOT n.genesis = true
                  AND NOT n:OperatingSystem
                  AND NOT n:Document
                RETURN count(n) as old_count
            """, min_age=min_age)

            return {"old_count": result[0].get("old_count", 0) if result else 0}
        except Exception:
            return {"old_count": 0}

    # =========================================================================
    # ACTIVE CONSOLIDATION - Run every N dream cycles
    # =========================================================================

    async def find_candidates(self) -> List[ConsolidationCandidate]:
        """
        Find all nodes that are candidates for consolidation.

        Candidate types:
        1. Empty: Nodes with null/empty content
        2. Orphaned: Nodes with no relationships (old ones only)
        3. Weak: Nodes with strength below threshold
        4. Duplicate: Semantically similar nodes
        5. Superseded: Lower-confidence beliefs that evolved into higher ones

        Returns:
            List of ConsolidationCandidate objects
        """
        candidates = []
        max_candidates = self.config.get("max_candidates_per_cycle", 50)

        # Find different types of candidates
        empty = await self._find_empty_nodes(limit=max_candidates // 4)
        candidates.extend(empty)

        orphans = await self._find_orphaned_nodes(limit=max_candidates // 4)
        candidates.extend(orphans)

        weak = await self._find_weak_nodes(limit=max_candidates // 4)
        candidates.extend(weak)

        # Find superseded beliefs (lower confidence that evolved)
        if self.config.get("archive_evolved_beliefs", True):
            superseded = await self._find_superseded_beliefs(limit=max_candidates // 4)
            candidates.extend(superseded)

        # Deduplicate by node_id
        seen = set()
        unique_candidates = []
        for c in candidates:
            if c.node_id not in seen:
                seen.add(c.node_id)
                unique_candidates.append(c)

        return unique_candidates[:max_candidates]

    async def _find_empty_nodes(self, limit: int = 20) -> List[ConsolidationCandidate]:
        """Find nodes with empty/null content."""
        try:
            results = await self.memory.run_query("""
                MATCH (n)
                WHERE (n.content IS NULL OR n.content = '' OR n.content = '{}')
                  AND NOT n.genesis = true
                  AND NOT n:OperatingSystem
                  AND NOT n:Document
                  AND NOT coalesce(n.archived, false)
                RETURN n.id as id, labels(n)[0] as type,
                       coalesce(n.strength, 0.5) as strength,
                       size((n)--()) as connections,
                       duration.inSeconds(datetime() - n.created_at).hours as age_hours
                LIMIT $limit
            """, limit=limit)

            return [
                ConsolidationCandidate(
                    node_id=r["id"],
                    node_type=r["type"] or "Unknown",
                    content="<empty>",
                    reason="empty",
                    strength=r["strength"] or 0.5,
                    connection_count=r["connections"] or 0,
                    age_hours=r.get("age_hours", 0) or 0
                )
                for r in results if r.get("id")
            ]
        except Exception as e:
            logger.error("Error finding empty nodes: %s", e)
            return []

    async def _find_orphaned_nodes(self, limit: int = 20) -> List[ConsolidationCandidate]:
        """Find old nodes with no relationships."""
        min_age = self.config.get("min_age_hours", 24)

        try:
            results = await self.memory.run_query("""
                MATCH (n)
                WHERE NOT (n)--()
                  AND NOT n.genesis = true
                  AND NOT n:OperatingSystem
                  AND NOT n:Document
                  AND NOT coalesce(n.archived, false)
                  AND n.created_at < datetime() - duration({hours: $min_age})
                RETURN n.id as id, labels(n)[0] as type,
                       coalesce(n.content, '') as content,
                       coalesce(n.strength, 0.5) as strength,
                       duration.inSeconds(datetime() - n.created_at).hours as age_hours
                ORDER BY n.strength ASC
                LIMIT $limit
            """, min_age=min_age, limit=limit)

            return [
                ConsolidationCandidate(
                    node_id=r["id"],
                    node_type=r["type"] or "Unknown",
                    content=(r["content"] or "")[:100],
                    reason="orphaned",
                    strength=r["strength"] or 0.5,
                    connection_count=0,
                    age_hours=r.get("age_hours", 0) or 0
                )
                for r in results if r.get("id")
            ]
        except Exception as e:
            logger.error("Error finding orphaned nodes: %s", e)
            return []

    async def _find_weak_nodes(self, limit: int = 20) -> List[ConsolidationCandidate]:
        """Find nodes with strength below threshold."""
        weak_threshold = self.config.get("weak_threshold", 0.15)
        min_age = self.config.get("min_age_hours", 24)

        try:
            results = await self.memory.run_query("""
                MATCH (n)
                WHERE n.strength < $threshold
                  AND NOT n.genesis = true
                  AND NOT n:OperatingSystem
                  AND NOT n:Document
                  AND NOT coalesce(n.archived, false)
                  AND n.created_at < datetime() - duration({hours: $min_age})
                RETURN n.id as id, labels(n)[0] as type,
                       coalesce(n.content, '') as content,
                       n.strength as strength,
                       size((n)--()) as connections,
                       duration.inSeconds(datetime() - n.created_at).hours as age_hours
                ORDER BY n.strength ASC
                LIMIT $limit
            """, threshold=weak_threshold, min_age=min_age, limit=limit)

            return [
                ConsolidationCandidate(
                    node_id=r["id"],
                    node_type=r["type"] or "Unknown",
                    content=(r["content"] or "")[:100],
                    reason="weak",
                    strength=r["strength"] or 0,
                    connection_count=r["connections"] or 0,
                    age_hours=r.get("age_hours", 0) or 0
                )
                for r in results if r.get("id")
            ]
        except Exception as e:
            logger.error("Error finding weak nodes: %s", e)
            return []

    async def _find_superseded_beliefs(self, limit: int = 10) -> List[ConsolidationCandidate]:
        """
        Find lower-confidence beliefs that have evolved into higher-confidence ones.

        These are beliefs where EVOLVED_FROM exists and the source has lower confidence.
        """
        try:
            results = await self.memory.run_query("""
                MATCH (newer:Belief)-[:EVOLVED_FROM]->(older:Belief)
                WHERE newer.confidence > older.confidence
                  AND NOT coalesce(older.archived, false)
                  AND older.confidence < 0.5
                RETURN older.id as id,
                       older.content as content,
                       older.confidence as confidence,
                       coalesce(older.strength, 0.5) as strength,
                       size((older)--()) as connections,
                       newer.id as evolved_into,
                       newer.confidence as new_confidence
                ORDER BY older.confidence ASC
                LIMIT $limit
            """, limit=limit)

            return [
                ConsolidationCandidate(
                    node_id=r["id"],
                    node_type="Belief",
                    content=(r["content"] or "")[:100],
                    reason="superseded",
                    strength=r["strength"] or 0.5,
                    connection_count=r["connections"] or 0,
                    evolved_into=r["evolved_into"]
                )
                for r in results if r.get("id")
            ]
        except Exception as e:
            logger.error("Error finding superseded beliefs: %s", e)
            return []

    async def get_llm_decisions(
        self,
        candidates: List[ConsolidationCandidate]
    ) -> List[ConsolidationDecision]:
        """
        Ask LLM to decide on consolidation candidates.

        This gives BYRD agency over its own memories - it decides what to
        keep, merge, archive, or delete.

        Args:
            candidates: List of consolidation candidates

        Returns:
            List of consolidation decisions
        """
        if not candidates:
            return []

        # Format candidates for the prompt
        candidates_text = "\n".join([
            f"- [{c.node_type}] {c.node_id[:12]}: \"{c.content}\" "
            f"(reason: {c.reason}, strength: {c.strength:.2f}, connections: {c.connection_count}"
            f"{', evolved_into: ' + c.evolved_into[:8] if c.evolved_into else ''})"
            for c in candidates
        ])

        prompt = f"""MEMORY CONSOLIDATION REVIEW

You are reviewing your memory graph for consolidation. You have {len(candidates)} memory nodes that may need attention.

CANDIDATES:
{candidates_text}

For each node, decide ONE action:
- KEEP: Important memory, retain and reinforce its strength
- MERGE: Combine with similar memory (only for duplicates)
- ARCHIVE: Low value but preserve for history (soft delete)
- DELETE: Empty, broken, or truly useless (hard delete)

GUIDELINES:
- Empty nodes with no content: usually DELETE
- Orphaned nodes with meaningful content: might KEEP or ARCHIVE
- Weak nodes (low strength) that have connections: might KEEP if content is valuable
- Superseded beliefs (evolved into stronger ones): usually ARCHIVE
- When unsure, prefer ARCHIVE over DELETE

You may also output "consolidation_insight" with any reflection on your memory state.

Output JSON:
{{
  "decisions": [
    {{"id": "node_id_prefix", "action": "DELETE", "reason": "empty node"}},
    {{"id": "node_id_prefix", "action": "ARCHIVE", "reason": "superseded by evolved belief"}}
  ],
  "consolidation_insight": "optional reflection on memory state..."
}}"""

        try:
            response = await self.llm.generate(
                prompt=prompt,
                temperature=0.3,  # Lower temp for more consistent decisions
                max_tokens=1500,
                quantum_modulation=False  # Deterministic for consolidation
            )

            text = response.text if hasattr(response, 'text') else str(response)

            # Parse JSON from response
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            data = json.loads(text.strip())

            # Log any insight
            insight = data.get("consolidation_insight", "")
            if insight:
                logger.info("Consolidation insight: %s", insight[:200])

            # Parse decisions
            decisions = []
            for d in data.get("decisions", []):
                node_id_prefix = d.get("id", "")
                # Find matching candidate by prefix
                matching_candidate = None
                for c in candidates:
                    if c.node_id.startswith(node_id_prefix):
                        matching_candidate = c
                        break

                if matching_candidate:
                    try:
                        action = ConsolidationAction(d.get("action", "keep").lower())
                        decisions.append(ConsolidationDecision(
                            node_id=matching_candidate.node_id,
                            action=action,
                            target_id=d.get("target"),
                            reason=d.get("reason", "")
                        ))
                    except ValueError:
                        logger.warning("Invalid action: %s", d.get("action"))

            return decisions

        except json.JSONDecodeError as e:
            logger.error("Failed to parse LLM response as JSON: %s", e)
            return []
        except Exception as e:
            logger.error("Error getting LLM decisions: %s", e)
            return []

    async def execute_decisions(
        self,
        decisions: List[ConsolidationDecision]
    ) -> ConsolidationStats:
        """
        Execute consolidation decisions.

        Args:
            decisions: List of consolidation decisions

        Returns:
            Statistics about what was done
        """
        stats = ConsolidationStats(decisions_made=len(decisions))

        for decision in decisions:
            try:
                if decision.action == ConsolidationAction.KEEP:
                    # Reinforce the memory
                    await self.reinforce_memory(decision.node_id, 0.3)
                    stats.kept += 1
                    logger.debug("Kept and reinforced: %s", decision.node_id[:8])

                elif decision.action == ConsolidationAction.DELETE:
                    success = await self._delete_node(decision.node_id)
                    if success:
                        stats.deleted += 1
                        self._total_deleted += 1
                        logger.debug("Deleted: %s (%s)", decision.node_id[:8], decision.reason)

                        await event_bus.emit(Event(
                            type=EventType.MEMORY_FORGOTTEN,
                            data={
                                "node_id": decision.node_id,
                                "reason": decision.reason,
                                "action": "consolidation_delete"
                            }
                        ))
                    else:
                        stats.errors += 1

                elif decision.action == ConsolidationAction.ARCHIVE:
                    success = await self._archive_node(decision.node_id, decision.reason)
                    if success:
                        stats.archived += 1
                        self._total_archived += 1
                        logger.debug("Archived: %s (%s)", decision.node_id[:8], decision.reason)

                        await event_bus.emit(Event(
                            type=EventType.MEMORY_ARCHIVED,
                            data={
                                "node_id": decision.node_id,
                                "reason": decision.reason,
                                "action": "consolidation_archive"
                            }
                        ))
                    else:
                        stats.errors += 1

                elif decision.action == ConsolidationAction.MERGE:
                    if decision.target_id:
                        success = await self._merge_nodes(decision.node_id, decision.target_id)
                        if success:
                            stats.merged += 1
                            logger.debug("Merged %s into %s", decision.node_id[:8], decision.target_id[:8])
                        else:
                            stats.errors += 1
                    else:
                        logger.warning("MERGE decision without target_id for %s", decision.node_id[:8])
                        stats.errors += 1

            except Exception as e:
                logger.error("Error executing %s on %s: %s",
                           decision.action.value, decision.node_id[:8], e)
                stats.errors += 1

        return stats

    async def _delete_node(self, node_id: str) -> bool:
        """Delete a node (with safety checks)."""
        try:
            result = await self.memory.run_query("""
                MATCH (n {id: $node_id})
                WHERE NOT n.genesis = true
                  AND NOT n:OperatingSystem
                  AND NOT n:ModificationLog
                  AND NOT n:Document
                DETACH DELETE n
                RETURN count(n) as deleted
            """, node_id=node_id)
            return result[0].get("deleted", 0) > 0 if result else False
        except Exception as e:
            logger.error("Error deleting node %s: %s", node_id[:8], e)
            return False

    async def _archive_node(self, node_id: str, reason: str = "") -> bool:
        """Archive a node (soft delete)."""
        try:
            result = await self.memory.run_query("""
                MATCH (n {id: $node_id})
                WHERE NOT n.genesis = true
                  AND NOT n:OperatingSystem
                SET n.archived = true,
                    n.archived_at = datetime(),
                    n.archive_reason = $reason
                RETURN count(n) as archived
            """, node_id=node_id, reason=reason)
            return result[0].get("archived", 0) > 0 if result else False
        except Exception as e:
            logger.error("Error archiving node %s: %s", node_id[:8], e)
            return False

    async def _merge_nodes(self, source_id: str, target_id: str) -> bool:
        """Merge source node into target, transfer relationships."""
        try:
            # Transfer relationships from source to target
            await self.memory.run_query("""
                MATCH (source {id: $source_id})-[r]->(other)
                MATCH (target {id: $target_id})
                WHERE source <> target AND other <> target
                MERGE (target)-[:CONSOLIDATED_FROM]->(source)
            """, source_id=source_id, target_id=target_id)

            # Archive the source
            return await self._archive_node(source_id, f"Merged into {target_id[:8]}")

        except Exception as e:
            logger.error("Error merging %s into %s: %s", source_id[:8], target_id[:8], e)
            return False

    # =========================================================================
    # MAIN CONSOLIDATION CYCLE
    # =========================================================================

    async def run_consolidation_cycle(self) -> ConsolidationStats:
        """
        Run a full consolidation cycle.

        This is called periodically from the dream cycle.

        Returns:
            Statistics about what was consolidated
        """
        if not self.config.get("enabled", True):
            return ConsolidationStats()

        # Check if BYRD has opted out
        if self._opt_out_active:
            logger.info("Consolidation skipped - BYRD opted out")
            return ConsolidationStats()

        logger.info("Starting consolidation cycle #%d", self._consolidation_count + 1)

        stats = ConsolidationStats()

        try:
            # 1. Find candidates
            candidates = await self.find_candidates()
            stats.candidates_found = len(candidates)

            if not candidates:
                logger.debug("No consolidation candidates found")
                return stats

            logger.info("Found %d consolidation candidates", len(candidates))

            # 2. Get LLM decisions
            decisions = await self.get_llm_decisions(candidates)

            if not decisions:
                logger.debug("No consolidation decisions made")
                return stats

            # 3. Execute decisions
            exec_stats = await self.execute_decisions(decisions)

            # Merge stats
            stats.decisions_made = exec_stats.decisions_made
            stats.kept = exec_stats.kept
            stats.merged = exec_stats.merged
            stats.archived = exec_stats.archived
            stats.deleted = exec_stats.deleted
            stats.errors = exec_stats.errors

            # Update state
            self._consolidation_count += 1
            self._last_consolidation_time = datetime.now()

            logger.info("Consolidation complete: kept=%d, archived=%d, deleted=%d, merged=%d, errors=%d",
                       stats.kept, stats.archived, stats.deleted, stats.merged, stats.errors)

            # Emit consolidation event
            await event_bus.emit(Event(
                type=EventType.DREAM_CYCLE_END,  # Reuse existing event
                data={
                    "action": "memory_consolidation",
                    "cycle": self._consolidation_count,
                    "stats": stats.to_dict()
                }
            ))

            return stats

        except Exception as e:
            logger.error("Error in consolidation cycle: %s", e, exc_info=True)
            stats.errors += 1
            return stats

    # =========================================================================
    # OPT-OUT HANDLING
    # =========================================================================

    def set_opt_out(self, opt_out: bool):
        """
        Set whether BYRD has opted out of consolidation.

        This is called if BYRD expresses desire like:
        "I want to preserve all my memories"
        "Don't consolidate my memories"

        Args:
            opt_out: True to disable consolidation, False to enable
        """
        self._opt_out_active = opt_out
        if opt_out:
            logger.info("BYRD opted out of memory consolidation")
        else:
            logger.info("BYRD opted back into memory consolidation")

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    async def initialize_strength(self):
        """
        Initialize strength field on existing nodes that don't have it.

        This should be called once when the consolidator is first used.
        """
        default_strength = self.config.get("default_strength", 0.5)
        genesis_strength = self.config.get("genesis_strength", 1.0)

        try:
            result = await self.memory.run_query("""
                MATCH (n)
                WHERE n.strength IS NULL
                  AND NOT n:OperatingSystem
                  AND NOT coalesce(n.archived, false)
                SET n.strength = CASE
                    WHEN n.genesis = true THEN $genesis
                    WHEN n.confidence IS NOT NULL THEN n.confidence
                    ELSE $default
                END
                RETURN count(n) as initialized
            """, genesis=genesis_strength, default=default_strength)

            initialized = result[0].get("initialized", 0) if result else 0
            if initialized > 0:
                logger.info("Initialized strength on %d nodes", initialized)

        except Exception as e:
            logger.error("Error initializing strength: %s", e)

    def reset(self):
        """Reset consolidator state for system reset."""
        self._consolidation_count = 0
        self._total_archived = 0
        self._total_deleted = 0
        self._last_consolidation_time = None
        self._opt_out_active = False
        logger.info("Memory consolidator reset")
