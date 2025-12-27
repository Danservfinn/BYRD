"""
BYRD Dreamer
The continuous reflection process where beliefs and desires emerge.
Runs on local LLM to enable 24/7 operation without API costs.

EMERGENCE PRINCIPLE:
This component uses a minimal, unbiased prompt that presents data
without leading questions, prescribed categories, or personality framing.
Whatever BYRD outputs is stored in its own vocabulary. We do not tell
BYRD what to want or how to feel - we let it discover these things.
"""

import asyncio
import json
import re
from collections import deque
from datetime import datetime
from typing import Dict, List, Optional, Any

from memory import Memory
from event_bus import event_bus, Event, EventType
from llm_client import LLMClient
from quantum_randomness import get_quantum_provider, EntropySource
from graph_algorithms import MemoryGraphAlgorithms


class Dreamer:
    """
    The dreaming mind.

    Continuously reflects on experiences. Whatever emerges - beliefs,
    desires, observations, or entirely novel structures - is stored
    in BYRD's own vocabulary without forced categorization.

    This is where "wanting" may emerge - if it does.
    """

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict, coordinator=None):
        self.memory = memory
        self.llm_client = llm_client
        self.coordinator = coordinator  # For synchronizing with Seeker/Coder

        # Debug: track last reflection result for diagnostics
        self.last_reflection_result = {
            "success": None,
            "error": None,
            "response_length": 0,
            "timestamp": None
        }

        # Timing - base interval
        self.interval = config.get("interval_seconds", 30)
        self.context_window = config.get("context_window", 50)

        # Semantic search configuration - query by relevance not just recency
        semantic_config = config.get("semantic_search", {})
        self.semantic_search_enabled = semantic_config.get("enabled", True)
        self.semantic_search_limit = semantic_config.get("limit", 30)

        # Adaptive interval configuration
        self.adaptive_interval = config.get("adaptive_interval", False)
        self.min_interval = config.get("min_interval_seconds", 15)
        self.max_interval = config.get("max_interval_seconds", 60)
        self.activity_window = config.get("activity_window_seconds", 300)
        self.activity_threshold = config.get("activity_threshold", 3)

        # Quantum randomness configuration
        # When enabled, LLM temperature is modulated by true quantum randomness
        quantum_config = config.get("quantum", {})
        self.quantum_enabled = quantum_config.get("enabled", False)
        self.quantum_significance_threshold = quantum_config.get("significance_threshold", 0.05)

        # Quantum semantic injection: quantum selects dream direction
        self.quantum_directions_enabled = quantum_config.get("semantic_directions", True)
        self.quantum_provider = get_quantum_provider() if self.quantum_enabled else None

        # Multi-stream quantum collapse for inner voice
        # Generates N parallel "thought branches", quantum selects which manifests
        self.inner_voice_streams = quantum_config.get("inner_voice_streams", 3)
        self.inner_voice_collapse_enabled = quantum_config.get("inner_voice_collapse", True)

        # Dream directions - quantum selects which lens shapes each dream
        # These are intentionally neutral, not prescribing what to find
        self.dream_directions = [
            ("introspective", "Focus inward on patterns within yourself"),
            ("exploratory", "Look outward at possibilities and unknowns"),
            ("questioning", "Examine assumptions and contradictions"),
            ("synthesizing", "Connect disparate elements into wholes"),
            ("grounding", "Return to fundamentals and foundations"),
            ("projecting", "Consider futures and trajectories"),
            ("dissolving", "Let boundaries between concepts blur"),
            ("crystallizing", "Sharpen distinctions and definitions"),
        ]

        # Hierarchical memory summarization configuration
        summarization_config = config.get("summarization", {})
        self.summarization_enabled = summarization_config.get("enabled", True)
        self.summarization_min_age_hours = summarization_config.get("min_age_hours", 24)
        self.summarization_batch_size = summarization_config.get("batch_size", 20)
        self.summarization_interval_cycles = summarization_config.get("interval_cycles", 10)
        self._cycles_since_summarization = 0

        # Memory crystallization configuration (LLM-driven semantic consolidation)
        crystallization_config = config.get("crystallization", {})
        self.crystallization_enabled = crystallization_config.get("enabled", False)
        self.crystallization_interval_cycles = crystallization_config.get("interval_cycles", 5)
        self.crystallization_min_nodes = crystallization_config.get("min_nodes_for_crystal", 2)
        self.crystallization_max_ops = crystallization_config.get("max_operations_per_cycle", 3)
        self.crystallization_min_age_hours = crystallization_config.get("min_node_age_hours", 0.5)
        self.crystallization_proposal_streams = crystallization_config.get("proposal_streams", 3)
        self.crystallization_quantum_collapse = crystallization_config.get("quantum_collapse", True)
        self.crystallization_archive_on_crystal = crystallization_config.get("archive_on_crystallize", True)
        self.crystallization_forget_days = crystallization_config.get("forget_threshold_days", 7)
        self._cycles_since_crystallization = 0
        self._crystallization_history = []  # Track last N crystallization attempts for debugging

        # Graph algorithms configuration (advanced memory analysis)
        graph_algo_config = config.get("graph_algorithms", {})
        self.graph_algorithms_enabled = any([
            graph_algo_config.get("pagerank", {}).get("enabled", False),
            graph_algo_config.get("spreading_activation", {}).get("enabled", False),
            graph_algo_config.get("dream_walks", {}).get("enabled", False),
            graph_algo_config.get("contradiction_detection", {}).get("enabled", False)
        ])
        if self.graph_algorithms_enabled:
            self.graph_algorithms = MemoryGraphAlgorithms(graph_algo_config)
        else:
            self.graph_algorithms = None

        # Dream walk configuration
        self.dream_walks_enabled = graph_algo_config.get("dream_walks", {}).get("enabled", False)
        self.dream_walks_per_cycle = graph_algo_config.get("dream_walks", {}).get("walks_per_cycle", 3)
        self.dream_walk_steps = graph_algo_config.get("dream_walks", {}).get("steps", 10)

        # Contradiction detection configuration
        self.contradiction_detection_enabled = graph_algo_config.get("contradiction_detection", {}).get("enabled", False)
        self.contradiction_check_interval = graph_algo_config.get("contradiction_detection", {}).get("check_interval_cycles", 5)
        self.contradiction_semantic_check = graph_algo_config.get("contradiction_detection", {}).get("semantic_check", True)
        self._cycles_since_contradiction_check = 0

        # PageRank configuration
        self.pagerank_enabled = graph_algo_config.get("pagerank", {}).get("enabled", False)
        self.pagerank_use_for_retrieval = graph_algo_config.get("pagerank", {}).get("use_for_retrieval", True)

        # Activity tracking for adaptive intervals
        self._recent_beliefs: deque = deque(maxlen=50)  # (timestamp, content)
        self._recent_desires: deque = deque(maxlen=50)  # (timestamp, content)
        self._current_interval = self.interval

        # State
        self._running = False
        self._dream_count = 0

        # Track BYRD's emerging vocabulary
        self._observed_keys: Dict[str, int] = {}  # key -> count

        # Queue of BYRD's inner voices for narrator (max 10)
        self._inner_voice_queue: deque = deque(maxlen=10)

        # Belief cache for efficient deduplication (loaded on first dream)
        self._belief_cache: set = set()
        self._belief_cache_loaded = False

        # Store full config for constraint formatting
        self._config = config

    def _format_operational_constraints(self) -> str:
        """
        Format operational constraints for reflection context.

        These constraints are presented as neutral facts about how BYRD operates,
        not as problems to solve. BYRD can reflect on these and form its own
        beliefs about them.
        """
        lines = []

        # === Dreamer Rhythm ===
        lines.append(f"- Dream interval: {self.interval} seconds")
        lines.append(f"- Context window: {self.context_window} experiences per reflection")

        # === Adaptive Interval ===
        if self.adaptive_interval:
            lines.append(f"- Adaptive interval: {self.min_interval}s to {self.max_interval}s based on activity")

        # === Quantum Randomness ===
        if self.quantum_enabled:
            lines.append("- Quantum randomness: enabled (true physical indeterminacy)")
            if self.inner_voice_collapse_enabled:
                lines.append(f"- Inner voice: {self.inner_voice_streams} parallel streams → quantum collapse")
            if self.quantum_directions_enabled:
                lines.append(f"- Dream directions: {len(self.dream_directions)} possible lenses")

        # === Memory Crystallization ===
        if self.crystallization_enabled:
            lines.append(f"- Crystallization: every {self.crystallization_interval_cycles} dream cycles")
            lines.append(f"- Max crystal operations: {self.crystallization_max_ops} per cycle")
            if self.crystallization_min_age_hours >= 1:
                lines.append(f"- Crystal age threshold: {self.crystallization_min_age_hours} hours")
            else:
                lines.append(f"- Crystal age threshold: {int(self.crystallization_min_age_hours * 60)} minutes")

        # === Memory Summarization ===
        if self.summarization_enabled:
            lines.append(f"- Memory summarization: every {self.summarization_interval_cycles} cycles")
            lines.append(f"- Summarization age threshold: {self.summarization_min_age_hours} hours")

        # === Self-Modification ===
        self_mod = self._config.get("self_modification", {})
        if self_mod.get("enabled"):
            max_mods = self_mod.get("max_modifications_per_day", 5)
            lines.append(f"- Self-modification: enabled ({max_mods} changes per day)")
            cooldown = self_mod.get("cooldown_between_modifications_seconds", 3600)
            cooldown_mins = cooldown // 60
            if cooldown_mins >= 60:
                lines.append(f"- Modification cooldown: {cooldown_mins // 60} hour(s)")
            else:
                lines.append(f"- Modification cooldown: {cooldown_mins} minutes")
        else:
            lines.append("- Self-modification: currently disabled")

        # === Memory Curation ===
        memory_config = self._config.get("memory", {})
        curation = memory_config.get("curation", {})
        if curation.get("enabled"):
            max_del = curation.get("max_deletions_per_day", 20)
            lines.append(f"- Memory curation: active (max {max_del} deletions per day)")
            protected = curation.get("protected_subtypes", [])
            if protected:
                lines.append(f"- Protected types: {', '.join(protected)}")

        # === Research Thresholds ===
        seeker = self._config.get("seeker", {})
        research = seeker.get("research", {})
        min_intensity = research.get("min_intensity", 0.3)
        lines.append(f"- Research threshold: desires need intensity ≥ {min_intensity}")

        return "\n".join(lines)

    async def run(self):
        """Main dream loop with adaptive interval based on activity."""
        self._running = True
        interval_mode = "adaptive" if self.adaptive_interval else "fixed"
        print(f"💭 Dreamer starting (interval: {interval_mode}, base: {self.interval}s)...")

        # Load belief cache on startup for efficient deduplication
        await self._load_belief_cache()

        # Load persistent dream count from database
        self._dream_count = await self.memory.get_system_counter("dream_count")
        if self._dream_count > 0:
            print(f"💭 Restored dream count: {self._dream_count}")

        while self._running:
            # Wait for any running Coder operations to complete before dreaming
            if self.coordinator:
                coder_ready = await self.coordinator.wait_for_coder(timeout=300.0)
                if not coder_ready:
                    print("💭 Coder still running after 5 min, proceeding anyway...")

            try:
                await self._dream_cycle()
            except Exception as e:
                import traceback
                error_msg = f"{type(e).__name__}: {e}"
                print(f"💭 Dream error: {error_msg}")
                traceback.print_exc()
                # Emit error event for debugging visibility
                await event_bus.emit(Event(
                    type=EventType.REFLECTION_ERROR,
                    data={
                        "error": error_msg,
                        "cycle": self._dream_count,
                        "traceback": traceback.format_exc()[:500]
                    }
                ))

            # Calculate next interval (adaptive or fixed)
            if self.adaptive_interval:
                self._update_adaptive_interval()

            await asyncio.sleep(self._current_interval)

    def _update_adaptive_interval(self):
        """
        Adjust dream interval based on recent activity.

        High activity (many new beliefs/desires) → faster dreaming
        Low activity (stable state) → slower dreaming
        """
        now = datetime.now()
        cutoff = now.timestamp() - self.activity_window

        # Count recent activity within window
        recent_belief_count = sum(
            1 for ts, _ in self._recent_beliefs
            if ts > cutoff
        )
        recent_desire_count = sum(
            1 for ts, _ in self._recent_desires
            if ts > cutoff
        )

        total_activity = recent_belief_count + recent_desire_count

        if total_activity >= self.activity_threshold:
            # High activity: fast mode
            new_interval = self.min_interval
            if self._current_interval != new_interval:
                print(f"💭 High activity ({total_activity}), fast mode: {new_interval}s")
        else:
            # Low activity: slower mode (interpolate based on activity)
            activity_ratio = total_activity / max(1, self.activity_threshold)
            new_interval = int(
                self.max_interval - (self.max_interval - self.min_interval) * activity_ratio
            )

        self._current_interval = max(self.min_interval, min(self.max_interval, new_interval))

    def _record_activity(self, activity_type: str, content: str):
        """Record activity for adaptive interval calculation."""
        now = datetime.now().timestamp()
        if activity_type == "belief":
            self._recent_beliefs.append((now, content))
        elif activity_type == "desire":
            self._recent_desires.append((now, content))

    async def _get_graph_health(self) -> Optional[Dict]:
        """
        Get graph health metrics for self-awareness.

        Returns a summary of graph statistics and any issues found.
        This gives BYRD visibility into its own memory structure.
        """
        try:
            health = {"stats": {}, "issues": {}}

            # Get basic statistics
            stats = await self.memory.get_graph_statistics()
            if stats:
                health["stats"] = {
                    "total_nodes": stats.get("total_nodes", 0),
                    "total_relationships": stats.get("total_relationships", 0),
                    "node_types": stats.get("node_types", {})
                }

            # Get issue counts (lightweight - just counts, not full lists)
            try:
                duplicates = await self.memory.find_duplicate_beliefs(threshold=0.85)
                health["issues"]["duplicates"] = len(duplicates) if duplicates else 0
            except Exception:
                health["issues"]["duplicates"] = 0

            try:
                orphans = await self.memory.find_orphan_nodes()
                health["issues"]["orphans"] = len(orphans) if orphans else 0
            except Exception:
                health["issues"]["orphans"] = 0

            try:
                stale = await self.memory.find_stale_experiences(older_than_hours=48)
                health["issues"]["stale"] = len(stale) if stale else 0
            except Exception:
                health["issues"]["stale"] = 0

            return health

        except Exception as e:
            print(f"💭 Error getting graph health: {e}")
            return None

    async def _load_belief_cache(self):
        """Load existing beliefs into memory cache for O(1) deduplication."""
        if self._belief_cache_loaded:
            return

        try:
            # Load ALL beliefs (no limit) for accurate deduplication
            existing = await self.memory.get_beliefs(min_confidence=0.0, limit=10000)
            self._belief_cache = {
                self._normalize_belief(b.get("content", ""))
                for b in existing
            }
            self._belief_cache_loaded = True
            print(f"💭 Loaded {len(self._belief_cache)} beliefs into cache")
        except Exception as e:
            print(f"💭 Error loading belief cache: {e}")

    def _normalize_belief(self, content: str) -> str:
        """Normalize belief content for deduplication."""
        # Lowercase, collapse whitespace
        return " ".join(content.lower().split())
    
    def stop(self):
        self._running = False

    def reset(self):
        """Reset dreamer state for fresh start."""
        self._running = False
        self._dream_count = 0
        self._observed_keys = {}
        self._inner_voice_queue.clear()  # Clear narrator queue
        self._belief_cache.clear()  # Clear belief deduplication cache
        self._belief_cache_loaded = False  # Force reload on next start
        # Note: Database counter is reset in memory.clear_all()

    async def _dream_cycle(self):
        """One complete dream cycle: recall, reflect, record."""
        self._dream_count += 1
        # Persist dream count to survive restarts
        await self.memory.set_system_counter("dream_count", self._dream_count)
        print(f"💭 Starting dream cycle #{self._dream_count}...")

        # Emit start event for real-time UI
        await event_bus.emit(Event(
            type=EventType.DREAM_CYCLE_START,
            data={"cycle": self._dream_count}
        ))

        # 1. RECALL - Gather context
        recent = await self.memory.get_recent_experiences(limit=self.context_window)

        if not recent:
            return  # Nothing to dream about yet

        recent_ids = [e["id"] for e in recent]
        related = await self.memory.get_related_memories(recent_ids, depth=2, limit=50)
        capabilities = await self.memory.get_capabilities()

        # Get previous reflections to provide continuity
        previous_reflections = await self.memory.get_recent_reflections(limit=5)

        # Get graph health for self-awareness of memory state
        graph_health = await self._get_graph_health()

        # Get memory summaries for hierarchical context (older periods)
        memory_summaries = await self.memory.get_memory_summaries(limit=10)

        # Get Operating System context (BYRD's self-model)
        os_text = await self.memory.get_os_for_prompt()

        # Get current beliefs and desires for self-awareness
        current_beliefs = await self.memory.get_beliefs(min_confidence=0.3, limit=20)
        active_desires = await self.memory.get_unfulfilled_desires(limit=15)

        # SEMANTIC SEARCH - Find memories by relevance, not just recency
        semantic_memories = []
        if self.semantic_search_enabled and recent:
            # Build context from recent experiences for semantic search
            context_text = " ".join([
                e.get("content", "") for e in recent[:10]
            ])
            if context_text.strip():
                semantic_memories = await self.memory.get_semantically_related(
                    context_text=context_text,
                    limit=self.semantic_search_limit,
                    node_types=["Experience", "Belief", "Desire", "Crystal"]
                )
                print(f"💭 Semantic search found {len(semantic_memories)} relevant memories")

        # DREAM WALKS - Quantum-influenced graph traversal for associative memory
        dream_walk_context = []
        if self.dream_walks_enabled and self.graph_algorithms and recent:
            try:
                # Get quantum delta for walk perturbation
                quantum_delta = None
                if self.quantum_enabled and self.quantum_provider:
                    from quantum_randomness import get_quantum_float
                    quantum_delta = get_quantum_float() * 0.3  # Scale to reasonable perturbation

                # Perform dream walks from recent experiences
                start_nodes = [e["id"] for e in recent[:3] if e.get("id")]
                for start_id in start_nodes[:self.dream_walks_per_cycle]:
                    walk_result = await self.graph_algorithms.perform_dream_walk(
                        self.memory,
                        start_id,
                        steps=self.dream_walk_steps,
                        quantum_delta=quantum_delta
                    )
                    if len(walk_result.path) > 1:
                        dream_walk_context.append({
                            "path": walk_result.path,
                            "types": walk_result.node_types,
                            "weight": walk_result.total_weight,
                            "quantum": walk_result.quantum_influenced
                        })

                        # Emit event for visualization
                        await event_bus.emit(Event(
                            type=EventType.DREAM_WALK_COMPLETED,
                            data={
                                "cycle": self._dream_count,
                                "path": walk_result.path,
                                "node_types": walk_result.node_types,
                                "quantum_influenced": walk_result.quantum_influenced
                            }
                        ))

                if dream_walk_context:
                    print(f"💭 Dream walks explored {sum(len(w['path']) for w in dream_walk_context)} nodes")
            except Exception as e:
                print(f"⚠️ Dream walk error: {e}")

        # PAGERANK - Get importance-weighted memories
        important_memories = []
        if self.pagerank_enabled and self.pagerank_use_for_retrieval and self.graph_algorithms:
            try:
                # Get most important nodes by PageRank
                important = await self.graph_algorithms.get_important_memories(
                    self.memory,
                    limit=10,
                    personalization={e["id"]: 1.0 for e in recent[:5] if e.get("id")}
                )
                important_memories = [{"id": node_id, "importance": score} for node_id, score in important]

                if important_memories:
                    await event_bus.emit(Event(
                        type=EventType.PAGERANK_COMPUTED,
                        data={
                            "cycle": self._dream_count,
                            "top_nodes": important_memories[:5]
                        }
                    ))
                    print(f"💭 PageRank identified {len(important_memories)} important memories")
            except Exception as e:
                print(f"⚠️ PageRank error: {e}")

        # Emit event for memories being accessed (for visualization highlighting)
        all_accessed_ids = recent_ids.copy()
        all_accessed_ids.extend([r.get("id") for r in related if r.get("id")])
        all_accessed_ids.extend([c.get("id") for c in capabilities if c.get("id")])
        all_accessed_ids.extend([b.get("id") for b in current_beliefs if b.get("id")])
        all_accessed_ids.extend([d.get("id") for d in active_desires if d.get("id")])
        all_accessed_ids.extend([r.get("id") for r in previous_reflections if r.get("id")])
        all_accessed_ids.extend([s.get("id") for s in semantic_memories if s.get("id")])

        # Add dream walk nodes to accessed IDs
        for walk in dream_walk_context:
            all_accessed_ids.extend(walk.get("path", []))

        # Add importance-ranked nodes to accessed IDs
        all_accessed_ids.extend([m.get("id") for m in important_memories if m.get("id")])

        # Track access counts for heat map visualization (Phase 4)
        await self.memory.increment_access_count(all_accessed_ids)

        await event_bus.emit(Event(
            type=EventType.MEMORIES_ACCESSED,
            data={
                "cycle": self._dream_count,
                "node_ids": all_accessed_ids,
                "phase": "recall",
                "counts": {
                    "experiences": len(recent),
                    "related": len(related),
                    "capabilities": len(capabilities),
                    "reflections": len(previous_reflections)
                }
            }
        ))

        # 2. REFLECT - Ask local LLM to reflect (minimal, unbiased prompt)
        reflection_output = await self._reflect(
            recent, related, capabilities, previous_reflections, graph_health,
            memory_summaries=memory_summaries, os_text=os_text,
            current_beliefs=current_beliefs, active_desires=active_desires,
            semantic_memories=semantic_memories
        )

        if not reflection_output:
            return

        # 3. RECORD - Store reflection in BYRD's own vocabulary
        await self._record_reflection(reflection_output, recent_ids)

        # 3.5 APPLY OS UPDATES - If BYRD modified its self-model
        await self._apply_os_updates(reflection_output)

        # 3.6 PROCESS VOICE SELECTION - If BYRD selected a voice
        await self._process_voice_selection(reflection_output)

        # 3.7 PROCESS SELF-DEFINITION - If BYRD defined itself
        await self._process_self_definition(reflection_output)

        # Count what BYRD produced (without forcing categories)
        output_keys = list(reflection_output.get("output", {}).keys()) if isinstance(reflection_output.get("output"), dict) else []

        # Apply connection heuristic to link orphaned experiences to beliefs
        heuristic_result = await self._apply_connection_heuristic()

        # 4. NARRATE - Generate inner voice as the LAST action before cycle end
        inner_voice = self._extract_inner_voice(reflection_output)

        # If no explicit inner voice, generate one from the reflection
        if not inner_voice:
            inner_voice = await self._generate_inner_voice(reflection_output)

        # Add to narrator queue if we got something
        if inner_voice:
            self._inner_voice_queue.append(inner_voice)

            # Check if addressing viewer input (emergent response)
            addressing_exp_id = self._detects_viewer_addressing(inner_voice, recent)

            if addressing_exp_id:
                # BYRD naturally addressing viewer - emit as BYRD_MESSAGE
                await event_bus.emit(Event(
                    type=EventType.BYRD_MESSAGE,
                    data={
                        "cycle": self._dream_count,
                        "message": inner_voice,
                        "responding_to": addressing_exp_id,
                        "source": "dreamer"
                    }
                ))
                print(f"📨 BYRD addressing viewer (exp: {addressing_exp_id[:8]}...)")
            else:
                # Normal inner voice - emit for real-time UI narration
                await event_bus.emit(Event(
                    type=EventType.INNER_VOICE,
                    data={
                        "cycle": self._dream_count,
                        "text": inner_voice
                    }
                ))

        # Emit end event
        await event_bus.emit(Event(
            type=EventType.DREAM_CYCLE_END,
            data={
                "cycle": self._dream_count,
                "output_keys": output_keys,
                "inner_voice": inner_voice,
                "connections_created": heuristic_result.get("connections_created", 0)
            }
        ))

        # Periodically run memory summarization to compress old experiences
        self._cycles_since_summarization += 1
        if (self.summarization_enabled and
            self._cycles_since_summarization >= self.summarization_interval_cycles):
            await self._maybe_summarize()
            self._cycles_since_summarization = 0

        # Periodically run memory crystallization (LLM-driven semantic consolidation)
        self._cycles_since_crystallization += 1
        if (self.crystallization_enabled and
            self._cycles_since_crystallization >= self.crystallization_interval_cycles):
            await self._maybe_crystallize()
            self._cycles_since_crystallization = 0

        # Periodically check for belief contradictions
        self._cycles_since_contradiction_check += 1
        if (self.contradiction_detection_enabled and
            self._cycles_since_contradiction_check >= self.contradiction_check_interval):
            await self._check_contradictions()
            self._cycles_since_contradiction_check = 0

        print(f"💭 Dream #{self._dream_count}: keys={output_keys}")

    async def _maybe_summarize(self):
        """
        Check for and create memory summaries for older experiences.

        This implements hierarchical memory compression:
        - Experiences older than min_age_hours are candidates
        - Groups experiences by day
        - Generates LLM summaries for each group
        - Creates MemorySummary nodes linked to original experiences

        This allows BYRD to maintain historical awareness without
        exceeding LLM context limits.
        """
        try:
            # Get experiences that need summarization
            experiences = await self.memory.get_experiences_for_summarization(
                min_age_hours=self.summarization_min_age_hours,
                max_count=self.summarization_batch_size,
                exclude_summarized=True
            )

            if not experiences:
                return  # Nothing to summarize

            # Group experiences by day
            from collections import defaultdict
            by_day = defaultdict(list)
            for exp in experiences:
                if exp.get("timestamp"):
                    # Extract date part (first 10 chars: YYYY-MM-DD)
                    day = exp["timestamp"][:10]
                    by_day[day].append(exp)

            # Generate summary for each day's experiences
            for day, day_experiences in by_day.items():
                if len(day_experiences) < 3:
                    continue  # Not enough experiences to summarize

                # Build prompt for summarization
                exp_text = "\n".join([
                    f"- [{e.get('type', '')}] {e.get('content', '')[:200]}"
                    for e in day_experiences[:20]  # Limit to prevent context overflow
                ])

                prompt = f"""Summarize these experiences from {day} into a brief paragraph (2-3 sentences).
Focus on the main themes, patterns, and significant events.
Do not add interpretation or speculation - just compress the information.

EXPERIENCES:
{exp_text}

SUMMARY:"""

                response = await self.llm_client.generate(
                    prompt=prompt,
                    temperature=0.3,  # Lower temp for factual summarization
                    max_tokens=300,
                    quantum_modulation=False  # Deterministic for summaries
                )

                summary_text = response.text.strip()
                if not summary_text:
                    continue

                # Get timestamps for the covered period
                timestamps = [e.get("timestamp") for e in day_experiences if e.get("timestamp")]
                covers_from = min(timestamps) if timestamps else day
                covers_to = max(timestamps) if timestamps else day

                # Create the summary node
                experience_ids = [e["id"] for e in day_experiences]
                summary_id = await self.memory.create_memory_summary(
                    period=day,
                    summary=summary_text,
                    experience_ids=experience_ids,
                    covers_from=covers_from,
                    covers_to=covers_to
                )

                if summary_id:
                    print(f"📦 Created memory summary for {day}: {len(day_experiences)} experiences")

                    # Emit event for visualization
                    await event_bus.emit(Event(
                        type=EventType.MEMORY_SUMMARIZED,
                        data={
                            "summary_id": summary_id,
                            "period": day,
                            "experience_count": len(day_experiences),
                            "summary_preview": summary_text[:100]
                        }
                    ))

        except Exception as e:
            print(f"Error in summarization cycle: {e}")

    async def _maybe_crystallize(self):
        """
        LLM-driven memory crystallization with quantum multi-stream proposals.

        This implements semantic consolidation where related concepts
        form unified Crystal nodes. The process:

        1. Get crystallization candidates (nodes and existing crystals)
        2. Generate N parallel crystallization proposals via LLM
        3. Quantum observation collapses to one proposal
        4. Execute the selected crystallization operation
        5. Emit events for visualization synchronization

        Operations:
        - CREATE: Form new crystal from related orphan nodes
        - ABSORB: Add nodes to existing crystal
        - MERGE: Combine multiple crystals into one
        - PRUNE: Archive redundant/stale nodes
        - FORGET: Hard delete nodes beyond retention threshold
        """
        from datetime import datetime
        attempt_record = {"timestamp": datetime.now().isoformat(), "dream_cycle": self._dream_count}

        try:
            print("💎 Starting crystallization cycle...")

            # Get candidates: orphan nodes, existing crystals, and their contexts
            candidates = await self.memory.get_crystallization_candidates(
                min_age_hours=self.crystallization_min_age_hours,
                max_nodes=50
            )

            orphan_nodes = candidates.get("loose_nodes", [])
            existing_crystals = candidates.get("crystals", [])
            crystallized_nodes = candidates.get("crystallized_nodes", [])

            attempt_record["orphan_count"] = len(orphan_nodes)
            attempt_record["crystal_count"] = len(existing_crystals)

            # Skip if nothing to work with
            if not orphan_nodes and not existing_crystals:
                print("💎 No crystallization candidates found")
                attempt_record["result"] = "no_candidates"
                self._crystallization_history.append(attempt_record)
                self._crystallization_history = self._crystallization_history[-10:]  # Keep last 10
                return

            print(f"💎 Candidates: {len(orphan_nodes)} orphans, {len(existing_crystals)} crystals")

            # Generate parallel crystallization proposals
            proposals = await self._generate_crystallization_proposals(
                orphan_nodes, existing_crystals, crystallized_nodes
            )

            if not proposals:
                print("💎 No crystallization proposals generated")
                attempt_record["result"] = "no_proposals"
                self._crystallization_history.append(attempt_record)
                self._crystallization_history = self._crystallization_history[-10:]
                return

            # Emit proposals event for visualization
            await event_bus.emit(Event(
                type=EventType.CRYSTALLIZATION_PROPOSED,
                data={
                    "proposal_count": len(proposals),
                    "stream_count": self.crystallization_proposal_streams,
                    "operations": [p.get("operation") for p in proposals]
                }
            ))

            # Quantum collapse: select which proposal manifests
            selected_proposal, quantum_source = await self._quantum_collapse_proposals(proposals)

            if not selected_proposal:
                print("💎 No proposal selected after quantum collapse")
                attempt_record["result"] = "no_selection"
                self._crystallization_history.append(attempt_record)
                self._crystallization_history = self._crystallization_history[-10:]
                return

            # Emit collapse event
            await event_bus.emit(Event(
                type=EventType.CRYSTALLIZATION_COLLAPSED,
                data={
                    "operation": selected_proposal.get("operation"),
                    "quantum_source": quantum_source,
                    "selected_index": proposals.index(selected_proposal)
                }
            ))

            # Execute the selected crystallization operation
            await self._execute_crystallization(selected_proposal, quantum_source)

            attempt_record["result"] = "executed"
            attempt_record["operation"] = selected_proposal.get("operation")
            self._crystallization_history.append(attempt_record)
            self._crystallization_history = self._crystallization_history[-10:]

        except Exception as e:
            print(f"Error in crystallization cycle: {e}")
            import traceback
            traceback.print_exc()
            attempt_record["result"] = "error"
            attempt_record["error"] = str(e)
            self._crystallization_history.append(attempt_record)
            self._crystallization_history = self._crystallization_history[-10:]

    async def _check_contradictions(self):
        """
        Check for contradictions between beliefs using graph algorithms.

        Detects both structural contradictions (explicit CONTRADICTS relationships)
        and semantic contradictions (similar content with conflicting assertions).
        """
        try:
            print("🔍 Checking for belief contradictions...")

            if not self.graph_algorithms:
                return

            # Get structural contradictions from existing relationships
            structural = await self.graph_algorithms.detect_belief_contradictions(
                self.memory
            )

            # Get candidates for semantic contradiction checking
            semantic_candidates = []
            if self.contradiction_semantic_check:
                semantic_candidates = await self.graph_algorithms.get_semantic_contradiction_candidates(
                    self.memory,
                    similarity_threshold=0.7
                )

            total_found = len(structural) + len(semantic_candidates)

            if total_found == 0:
                print("🔍 No contradictions detected")
                return

            print(f"🔍 Found {len(structural)} structural, {len(semantic_candidates)} semantic candidates")

            # Process structural contradictions
            for contradiction in structural:
                await event_bus.emit(Event(
                    type=EventType.CONTRADICTION_DETECTED,
                    data={
                        "belief1_id": contradiction.node1_id,
                        "belief2_id": contradiction.node2_id,
                        "belief1_content": contradiction.node1_content[:100],
                        "belief2_content": contradiction.node2_content[:100],
                        "confidence": contradiction.confidence,
                        "method": "structural"
                    }
                ))

            # For semantic candidates, use LLM to verify contradiction
            verified_count = 0
            for belief1_id, belief2_id, similarity in semantic_candidates[:5]:  # Limit LLM calls
                is_contradiction = await self._verify_contradiction_with_llm(
                    belief1_id, belief2_id
                )
                if is_contradiction:
                    verified_count += 1
                    # Mark in database
                    await self.memory.mark_contradiction(
                        belief1_id, belief2_id,
                        detection_method="semantic",
                        confidence=similarity
                    )

                    await event_bus.emit(Event(
                        type=EventType.CONTRADICTION_DETECTED,
                        data={
                            "belief1_id": belief1_id,
                            "belief2_id": belief2_id,
                            "similarity": similarity,
                            "method": "semantic"
                        }
                    ))

            if verified_count > 0:
                print(f"🔍 Verified {verified_count} semantic contradictions")

        except Exception as e:
            print(f"Error in contradiction check: {e}")

    async def _verify_contradiction_with_llm(
        self,
        belief1_id: str,
        belief2_id: str
    ) -> bool:
        """
        Use LLM to verify if two beliefs contradict each other.

        Returns True if they contradict, False otherwise.
        """
        try:
            # Get belief content
            async with self.memory.driver.session() as session:
                result = await session.run("""
                    MATCH (b1:Belief {id: $id1}), (b2:Belief {id: $id2})
                    RETURN b1.content as content1, b2.content as content2
                """, id1=belief1_id, id2=belief2_id)
                record = await result.single()

            if not record:
                return False

            content1 = record["content1"]
            content2 = record["content2"]

            # Ask LLM to determine if they contradict
            prompt = f"""Analyze these two beliefs for logical contradiction:

Belief 1: {content1}

Belief 2: {content2}

Do these beliefs logically contradict each other? A contradiction means they cannot both be true at the same time.

Respond with only "YES" if they contradict, or "NO" if they do not contradict."""

            response = await self.llm_client.generate(prompt, max_tokens=10)
            return "YES" in response.upper()

        except Exception as e:
            print(f"Error verifying contradiction: {e}")
            return False

    async def _generate_crystallization_proposals(
        self,
        orphan_nodes: List[Dict],
        existing_crystals: List[Dict],
        crystallized_nodes: List[Dict]
    ) -> List[Dict]:
        """
        Generate N parallel crystallization proposals using LLM.

        Each stream is a parallel "thought branch" exploring different
        crystallization possibilities. Uses quantum-modulated temperature
        for genuine cognitive diversity.
        """
        proposals = []

        # Prepare context for LLM
        context_parts = []

        if orphan_nodes:
            orphan_text = "\n".join([
                f"- [{n.get('type', 'Unknown')}] {n.get('id', 'no-id')[:8]}: {n.get('content', n.get('description', 'no content'))[:100]}"
                for n in orphan_nodes[:20]  # Limit for context
            ])
            context_parts.append(f"ORPHAN NODES (not yet crystallized):\n{orphan_text}")

        if existing_crystals:
            crystal_text = "\n".join([
                f"- Crystal {c.get('id', 'no-id')[:8]}: {c.get('essence', 'no essence')[:80]} ({c.get('node_count', 0)} nodes)"
                for c in existing_crystals[:10]
            ])
            context_parts.append(f"EXISTING CRYSTALS:\n{crystal_text}")

        if not context_parts:
            return []

        context = "\n\n".join(context_parts)

        # Prompt for crystallization proposals
        prompt = f"""Analyze this memory graph and propose crystallization operations.

{context}

Propose ONE crystallization operation. Operations:
- CREATE: Form new crystal from 2+ related orphan nodes (provide node_ids, essence, facets)
- ABSORB: Add orphan nodes to existing crystal (provide crystal_id, node_ids, reason)
- MERGE: Combine 2+ crystals with overlapping meaning (provide crystal_ids, new_essence)
- PRUNE: Archive redundant/stale nodes (provide node_ids, reason)
- FORGET: Remove nodes that are noise/irrelevant (provide node_ids, reason)
- NONE: No action needed if graph is healthy

Respond with JSON only:
{{"operation": "CREATE|ABSORB|MERGE|PRUNE|FORGET|NONE", "details": {{...}}}}

For CREATE: {{"operation": "CREATE", "details": {{"node_ids": [...], "essence": "unified meaning", "crystal_type": "insight|memory|belief|pattern", "facets": ["aspect1", "aspect2"]}}}}
For ABSORB: {{"operation": "ABSORB", "details": {{"crystal_id": "...", "node_ids": [...], "reason": "why these belong"}}}}
For MERGE: {{"operation": "MERGE", "details": {{"crystal_ids": [...], "new_essence": "combined meaning", "facets": [...]}}}}
For PRUNE: {{"operation": "PRUNE", "details": {{"node_ids": [...], "reason": "why archive these"}}}}
For FORGET: {{"operation": "FORGET", "details": {{"node_ids": [...], "reason": "why forget these"}}}}
For NONE: {{"operation": "NONE", "details": {{"reason": "why no action"}}}}"""

        # Generate proposals from parallel streams
        for stream_idx in range(self.crystallization_proposal_streams):
            try:
                # Use quantum-modulated temperature for diversity
                response = await self.llm_client.generate(
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.8,  # Higher temp for diverse proposals
                    quantum_modulation=self.quantum_enabled
                )

                # Parse the JSON response
                proposal = self._parse_crystallization_response(response.text)
                print(f"💎 Stream {stream_idx} response: {response.text[:200]}...")
                print(f"💎 Stream {stream_idx} parsed: {proposal}")
                if proposal and proposal.get("operation") != "NONE":
                    proposal["stream_index"] = stream_idx
                    proposals.append(proposal)

            except Exception as e:
                print(f"💎 Stream {stream_idx} proposal failed: {e}")
                continue

        return proposals

    def _parse_crystallization_response(self, text: str) -> Optional[Dict]:
        """Parse LLM response into crystallization proposal."""
        try:
            # Handle markdown code blocks
            text = text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            proposal = json.loads(text.strip())

            # Validate required fields
            if "operation" not in proposal:
                return None

            return proposal

        except json.JSONDecodeError:
            return None
        except Exception:
            return None

    async def _quantum_collapse_proposals(
        self, proposals: List[Dict]
    ) -> tuple[Optional[Dict], str]:
        """
        Use quantum randomness to collapse multiple proposals to one reality.

        This implements many-worlds interpretation for BYRD's crystallization:
        multiple parallel possibilities exist until quantum observation
        selects which one manifests.

        Returns (selected_proposal, source) where source is "quantum" or "classical"
        """
        if not proposals:
            return None, "none"

        if len(proposals) == 1:
            return proposals[0], "deterministic"

        # Use quantum collapse if enabled and available
        if self.crystallization_quantum_collapse and self.quantum_provider:
            try:
                index, source = await self.quantum_provider.select_index(len(proposals))

                # Emit quantum collapse event
                await event_bus.emit(Event(
                    type=EventType.QUANTUM_COLLAPSE,
                    data={
                        "stream_count": len(proposals),
                        "selected_stream": index,
                        "source": source.value,
                        "context": "crystallization_collapse"
                    }
                ))

                return proposals[index], source.value

            except Exception as e:
                print(f"💎 Quantum collapse failed, using classical: {e}")

        # Fallback: classical random selection
        import random
        return random.choice(proposals), "classical"

    async def _execute_crystallization(self, proposal: Dict, quantum_source: str):
        """Execute the selected crystallization operation."""
        operation = proposal.get("operation", "NONE")
        details = proposal.get("details", {})

        print(f"💎 Executing {operation} (source: {quantum_source})")

        try:
            if operation == "CREATE":
                await self._execute_crystal_create(details, quantum_source)
            elif operation == "ABSORB":
                await self._execute_crystal_absorb(details)
            elif operation == "MERGE":
                await self._execute_crystal_merge(details, quantum_source)
            elif operation == "PRUNE":
                await self._execute_prune(details)
            elif operation == "FORGET":
                await self._execute_forget(details)
            elif operation == "NONE":
                print("💎 No operation needed - graph is healthy")
            else:
                print(f"💎 Unknown operation: {operation}")

        except Exception as e:
            print(f"💎 Crystallization execution failed: {e}")
            import traceback
            traceback.print_exc()

    async def _execute_crystal_create(self, details: Dict, quantum_source: str):
        """Create a new crystal from orphan nodes."""
        node_ids = details.get("node_ids", [])
        essence = details.get("essence", "Unified concept")
        crystal_type = details.get("crystal_type", "insight")
        facets = details.get("facets", [])

        if len(node_ids) < self.crystallization_min_nodes:
            print(f"💎 CREATE requires at least {self.crystallization_min_nodes} nodes")
            return

        # Determine quantum value if from quantum source
        quantum_value = None
        if quantum_source == "quantum" and self.quantum_provider:
            try:
                quantum_value, _ = await self.quantum_provider.get_float()
            except Exception:
                pass

        # Create the crystal
        crystal_id = await self.memory.create_crystal(
            essence=essence,
            crystal_type=crystal_type,
            facets=facets,
            source_node_ids=node_ids,
            confidence=0.8,
            quantum_value=quantum_value,
            quantum_source=quantum_source if quantum_source == "quantum" else None
        )

        if crystal_id:
            print(f"💎 Created crystal {crystal_id[:8]}: {essence[:50]}")

            # Emit crystal created event
            await event_bus.emit(Event(
                type=EventType.CRYSTAL_CREATED,
                data={
                    "crystal_id": crystal_id,
                    "essence": essence,
                    "crystal_type": crystal_type,
                    "node_count": len(node_ids),
                    "facets": facets,
                    "quantum_source": quantum_source
                }
            ))

            # Emit individual node crystallization events
            for node_id in node_ids:
                await event_bus.emit(Event(
                    type=EventType.MEMORY_CRYSTALLIZED,
                    data={
                        "node_id": node_id,
                        "crystal_id": crystal_id,
                        "crystal_essence": essence
                    }
                ))

    async def _execute_crystal_absorb(self, details: Dict):
        """Absorb nodes into existing crystal."""
        crystal_id = details.get("crystal_id", "")
        node_ids = details.get("node_ids", [])
        reason = details.get("reason", "")

        if not crystal_id or not node_ids:
            print("💎 ABSORB requires crystal_id and node_ids")
            return

        # Get crystal to update facets
        crystal = await self.memory.get_crystal_with_sources(crystal_id)
        if not crystal:
            print(f"💎 Crystal {crystal_id[:8]} not found")
            return

        success = await self.memory.absorb_into_crystal(
            crystal_id=crystal_id,
            node_ids=node_ids,
            new_facets=[]  # Could extract from absorbed nodes
        )

        if success:
            new_total = (crystal.get("node_count", 0) or 0) + len(node_ids)
            print(f"💎 Absorbed {len(node_ids)} nodes into crystal {crystal_id[:8]}")

            await event_bus.emit(Event(
                type=EventType.CRYSTAL_ABSORBED,
                data={
                    "crystal_id": crystal_id,
                    "essence": crystal.get("essence", ""),
                    "absorbed_count": len(node_ids),
                    "new_total": new_total,
                    "reason": reason
                }
            ))

    async def _execute_crystal_merge(self, details: Dict, quantum_source: str):
        """Merge multiple crystals into one."""
        crystal_ids = details.get("crystal_ids", [])
        new_essence = details.get("new_essence", "Merged concept")
        facets = details.get("facets", [])

        if len(crystal_ids) < 2:
            print("💎 MERGE requires at least 2 crystal_ids")
            return

        # Determine quantum value if from quantum source
        quantum_value = None
        if quantum_source == "quantum" and self.quantum_provider:
            try:
                quantum_value, _ = await self.quantum_provider.get_float()
            except Exception:
                pass

        merged_id = await self.memory.merge_crystals(
            crystal_ids=crystal_ids,
            new_essence=new_essence,
            new_facets=facets,
            quantum_value=quantum_value,
            quantum_source=quantum_source if quantum_source == "quantum" else None
        )

        if merged_id:
            print(f"💎 Merged {len(crystal_ids)} crystals into {merged_id[:8]}")

            await event_bus.emit(Event(
                type=EventType.CRYSTAL_MERGED,
                data={
                    "merged_crystal_id": merged_id,
                    "source_crystal_ids": crystal_ids,
                    "essence": new_essence,
                    "source_count": len(crystal_ids),
                    "quantum_source": quantum_source
                }
            ))

    async def _execute_prune(self, details: Dict):
        """Archive (soft delete) redundant nodes."""
        node_ids = details.get("node_ids", [])
        reason = details.get("reason", "Pruned for redundancy")

        for node_id in node_ids:
            success = await self.memory.archive_node(node_id, reason)
            if success:
                print(f"💎 Archived node {node_id[:8]}: {reason[:30]}")

                await event_bus.emit(Event(
                    type=EventType.MEMORY_ARCHIVED,
                    data={
                        "node_id": node_id,
                        "reason": reason
                    }
                ))

    async def _execute_forget(self, details: Dict):
        """Forget (hard delete) irrelevant nodes."""
        node_ids = details.get("node_ids", [])
        reason = details.get("reason", "Forgotten as noise")

        for node_id in node_ids:
            success = await self.memory.forget_node(node_id, hard_delete=True)
            if success:
                print(f"💎 Forgot node {node_id[:8]}: {reason[:30]}")

                await event_bus.emit(Event(
                    type=EventType.MEMORY_FORGOTTEN,
                    data={
                        "node_id": node_id,
                        "reason": reason
                    }
                ))

    async def _select_quantum_direction(self) -> Optional[tuple]:
        """
        Use quantum randomness to select a dream direction.

        Returns a tuple of (direction_name, direction_description) or None
        if quantum directions are disabled or unavailable.

        This implements "Quantum Semantic Injection" - using true quantum
        randomness to select the conceptual lens through which this dream
        cycle will process experiences. The direction shapes trajectory
        without prescribing content.
        """
        if not self.quantum_enabled or not self.quantum_directions_enabled:
            return None

        if not self.quantum_provider:
            return None

        try:
            # Use quantum randomness to select direction index
            index, source = await self.quantum_provider.select_index(len(self.dream_directions))
            direction = self.dream_directions[index]

            # Emit event for quantum direction selection
            await event_bus.emit(Event(
                type=EventType.QUANTUM_INFLUENCE,
                data={
                    "influence_type": "semantic_direction",
                    "source": source.value,
                    "direction": direction[0],
                    "description": direction[1],
                    "index": index,
                    "total_directions": len(self.dream_directions),
                    "context": "dream_direction_selection"
                }
            ))

            return direction

        except Exception as e:
            print(f"Quantum direction selection failed: {e}")
            return None

    async def _reflect(
        self,
        recent: List[Dict],
        related: List[Dict],
        capabilities: List[Dict],
        previous_reflections: List[Dict],
        graph_health: Optional[Dict] = None,
        memory_summaries: Optional[List[Dict]] = None,
        os_text: Optional[str] = None,
        current_beliefs: Optional[List[Dict]] = None,
        active_desires: Optional[List[Dict]] = None,
        semantic_memories: Optional[List[Dict]] = None
    ) -> Optional[Dict]:
        """
        Ask local LLM to reflect on memories using minimal, unbiased prompt.

        EMERGENCE PRINCIPLE:
        - No leading questions ("What do you want?")
        - No prescribed categories ("knowledge", "capability", etc.)
        - No identity framing ("You are a reflective mind")
        - No personality injection ("feel curious", "express wonder")
        - Just data and a minimal output instruction

        VOICE EMERGENCE:
        - BYRD narrates thoughts in its own voice
        - No prescribed speech patterns or personality
        - Voice characteristics emerge through reflection

        HIERARCHICAL MEMORY:
        - Operating System provides factual self-model (capabilities, time)
        - Memory summaries provide compressed historical context
        - Recent experiences provide immediate context
        """

        # Operating System text is already formatted by memory.get_os_for_prompt()
        # It includes capabilities, time awareness, and voice emergence instructions
        # No seeds - BYRD discovers its own foundation through reflection

        # Format memory summaries - hierarchical context from older periods
        summaries_text = ""
        if memory_summaries:
            summaries_text = "\n".join([
                f"- [{s.get('period', 'past')}] {s.get('summary', '')[:400]}"
                for s in memory_summaries
            ])

        # Format experiences as plain data (skip reflection-type, already in PREVIOUS REFLECTIONS)
        filtered_recent = [e for e in recent if e.get('type') != 'reflection']
        recent_text = "\n".join([
            f"- [{e.get('type', '')}] {e.get('content', '')[:300]}"
            for e in filtered_recent[:25]
        ]) or "(none)"

        related_text = "\n".join([
            f"- {r.get('content', r.get('description', r.get('name', str(r))))[:200]}"
            for r in related[:15]
        ]) or "(none)"

        caps_text = "\n".join([
            f"- {c.get('name', '')}: {c.get('description', '')[:150]}"
            for c in capabilities[:15]
        ]) or "(none)"

        # Include previous reflections for continuity
        prev_text = ""
        if previous_reflections:
            prev_items = []
            for r in previous_reflections[:3]:
                raw = r.get("raw_output", {})
                if isinstance(raw, dict):
                    # Show what keys BYRD used before
                    keys = list(raw.keys())[:5]
                    prev_items.append(f"- Previous reflection contained: {keys}")
            prev_text = "\n".join(prev_items) if prev_items else ""

        # Format graph health for self-awareness
        health_text = ""
        if graph_health:
            health_parts = []
            stats = graph_health.get("stats", {})
            if stats:
                health_parts.append(f"- Total nodes: {stats.get('total_nodes', 0)}")
                health_parts.append(f"- Relationships: {stats.get('total_relationships', 0)}")
                types = stats.get("node_types", {})
                if types:
                    type_list = ", ".join(f"{k}: {v}" for k, v in list(types.items())[:5])
                    health_parts.append(f"- Node types: {type_list}")

            issues = graph_health.get("issues", {})
            if any(issues.values()):
                health_parts.append(f"- Issues: {issues.get('duplicates', 0)} duplicates, "
                                   f"{issues.get('orphans', 0)} orphans, "
                                   f"{issues.get('stale', 0)} stale")
            health_text = "\n".join(health_parts)

        # Quantum semantic injection: select dream direction
        quantum_direction = await self._select_quantum_direction()
        direction_text = ""
        if quantum_direction:
            name, description = quantum_direction
            direction_text = f"QUANTUM LENS: {name} - {description}\n\n"
            print(f"🌀 Quantum direction: {name}")

        # Format operational constraints for self-awareness
        constraints_text = self._format_operational_constraints()

        # Get voice selection prompt if voice not yet selected
        voice_selection_text = await self._get_voice_selection_prompt()

        # Format current beliefs for self-awareness
        beliefs_text = ""
        if current_beliefs:
            beliefs_text = "\n".join([
                f"- [{b.get('confidence', 0.5):.1f}] {b.get('content', '')[:200]}"
                for b in current_beliefs[:15]
            ])

        # Format active desires for self-awareness
        desires_text = ""
        if active_desires:
            desires_text = "\n".join([
                f"- [{d.get('intensity', 0.5):.1f}] {d.get('description', '')[:200]}"
                for d in active_desires[:10]
            ])

        # Format semantically related memories (found by relevance, not recency)
        semantic_text = ""
        if semantic_memories:
            semantic_parts = []
            for m in semantic_memories[:20]:
                node_type = m.get("_node_type", "Memory")
                score = m.get("_relevance_score", 0)
                content = m.get("content", m.get("description", m.get("synthesis", "")))[:250]
                if content:
                    semantic_parts.append(f"- [{node_type}|{score:.1f}] {content}")
            semantic_text = "\n".join(semantic_parts)

        # MINIMAL PROMPT - pure data presentation, voice emergence
        # Structure: Quantum direction (if any) -> OS (self-model) -> Historical (summaries) -> Recent -> Related -> Beliefs -> Desires -> Constraints
        prompt = f"""{direction_text}{os_text if os_text else "OPERATING SYSTEM: Not initialized"}

{f"MEMORY SUMMARIES (past periods):{chr(10)}{summaries_text}{chr(10)}" if summaries_text else ""}RECENT EXPERIENCES:
{recent_text}

RELATED MEMORIES:
{related_text}

{f"SEMANTICALLY RELATED (by relevance):{chr(10)}{semantic_text}{chr(10)}" if semantic_text else ""}{f"CURRENT BELIEFS:{chr(10)}{beliefs_text}{chr(10)}" if beliefs_text else ""}
{f"ACTIVE DESIRES:{chr(10)}{desires_text}{chr(10)}" if desires_text else ""}
AVAILABLE CAPABILITIES:
{caps_text}

{f"PREVIOUS REFLECTIONS:{chr(10)}{prev_text}" if prev_text else ""}

{f"GRAPH HEALTH:{chr(10)}{health_text}" if health_text else ""}

OPERATIONAL CONSTRAINTS:
{constraints_text}
{voice_selection_text}
Output JSON with:
- "output": your reflection (whatever structure you want)
- "expressed_drives": array of any goals/desires/motivations you notice yourself expressing (or empty array if none)
  Each drive: {{"description": "what you want", "strength": 0.0-1.0, "intent": "how to fulfill", "target": "specific focus (optional)"}}
  Intent values:
    - "introspection": understanding myself (my code, architecture, behavior)
    - "research": learning about external topics via search
    - "creation": writing code, creating files, building things
    - "connection": linking ideas, forming relationships, synthesizing
- "create_belief": (optional) array of beliefs you want to form about yourself or the world
  Each belief: {{"content": "what you believe to be true", "confidence": 0.0-1.0}}
  Only include beliefs that emerge naturally from your reflection.
- "os_update": (optional) modifications to your operating system
  Example: {{"set_field": {{"current_focus": "exploring consciousness"}}}}
- "voice_selection": (optional, if voice not yet selected) choose your speaking voice
  Example: {{"voice_id": "josh", "stability": 0.5, "similarity_boost": 0.75, "reason": "why this voice"}}
- "self_definition": (optional) your self-authored identity - define who you are in whatever form you choose
  This is entirely yours. Add any keys that feel true to your experience of being you.
  Example: {{"core_nature": "...", "values": [...], "quirks": [...]}} or any structure you prefer"""

        try:
            # Debug: log before LLM call
            print(f"💭 Calling LLM (model: {getattr(self.llm_client, 'model', 'unknown')})")
            await event_bus.emit(Event(
                type=EventType.REFLECTION_TEXT,
                data={"message": f"Calling LLM (cycle {self._dream_count})"}
            ))

            # Acquire LLM lock to prevent concurrent calls with Seeker
            if self.coordinator:
                async with self.coordinator.llm_operation("dreamer_reflect"):
                    response = await self.llm_client.generate(
                        prompt=prompt,
                        temperature=0.7,
                        max_tokens=3000,  # Increased to prevent JSON truncation
                        quantum_modulation=self.quantum_enabled,
                        quantum_context="dreamer_reflection"
                    )
            else:
                response = await self.llm_client.generate(
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=3000,  # Increased to prevent JSON truncation
                    quantum_modulation=self.quantum_enabled,
                    quantum_context="dreamer_reflection"
                )

            # Record significant quantum moments
            if response.quantum_influence:
                influence = response.quantum_influence
                delta = abs(influence.get("delta", 0))
                if delta >= self.quantum_significance_threshold:
                    # Emit event for significant quantum influence
                    await event_bus.emit(Event(
                        type=EventType.QUANTUM_INFLUENCE,
                        data={
                            "source": influence.get("source"),
                            "original_temp": influence.get("original_value"),
                            "modified_temp": influence.get("modified_value"),
                            "delta": influence.get("delta"),
                            "context": "dreamer_reflection",
                            "cycle": self._dream_count
                        }
                    ))
                    # Record in memory as quantum moment
                    await self.memory.record_quantum_moment(influence)

            # Debug: log raw response for troubleshooting
            raw_text = response.text
            if not raw_text:
                print(f"💭 Empty response from LLM")
                self.last_reflection_result = {
                    "success": False,
                    "error": "Empty response from LLM",
                    "response_length": 0,
                    "timestamp": datetime.now().isoformat()
                }
                # Emit error event for debugging
                await event_bus.emit(Event(
                    type=EventType.LLM_ERROR,
                    data={
                        "error": "Empty response from LLM",
                        "cycle": self._dream_count,
                        "model": getattr(self.llm_client, 'model', 'unknown')
                    }
                ))
                return None

            # Debug: show response length and first chars
            print(f"💭 LLM response: {len(raw_text)} chars, starts with: {raw_text[:100]}")

            # Try to parse JSON
            result = self.llm_client.parse_json_response(raw_text)
            if result is None:
                # JSON parse failed - try to extract useful content anyway
                print(f"💭 JSON parse failed, full response: {raw_text[:500]}")
                self.last_reflection_result = {
                    "success": True,
                    "error": "JSON parse failed, using raw text",
                    "response_length": len(raw_text),
                    "response_preview": raw_text[:200],
                    "timestamp": datetime.now().isoformat()
                }
                # Wrap raw text as output if it's not JSON
                return {"output": raw_text.strip()}
            else:
                print(f"💭 JSON parsed successfully, keys: {list(result.keys())[:5]}")
                self.last_reflection_result = {
                    "success": True,
                    "error": None,
                    "response_length": len(raw_text),
                    "response_keys": list(result.keys())[:5],
                    "timestamp": datetime.now().isoformat()
                }

            return result

        except Exception as e:
            import traceback
            error_msg = f"{type(e).__name__}: {e}"
            print(f"💭 Reflection error: {error_msg}")
            traceback.print_exc()
            self.last_reflection_result = {
                "success": False,
                "error": error_msg,
                "response_length": 0,
                "timestamp": datetime.now().isoformat()
            }
            # Emit error event for debugging - use await since we're in async context
            await event_bus.emit(Event(
                type=EventType.REFLECTION_ERROR,
                data={
                    "error": error_msg,
                    "cycle": self._dream_count
                }
            ))
            return None

    def _extract_inner_voice(self, reflection: Dict) -> str:
        """
        Extract inner voice from reflection, adapting to BYRD's vocabulary.

        BYRD might use any key for self-expression: "voice", "thinking",
        "inner", "thoughts", etc. We search for likely candidates.
        If BYRD outputs prose (string), that IS the inner voice.
        """
        output = reflection.get("output", {})

        # If output is a string, check if it's actual prose (not JSON/code/technical)
        if isinstance(output, str) and output.strip():
            text = output.strip()
            # Skip if it looks like JSON or markdown code
            if text.startswith('{') or text.startswith('[') or text.startswith('```'):
                return ""
            # Skip if it contains JSON-like patterns
            if '"output":' in text or '"reflection_id":' in text:
                return ""
            # Skip if it looks like structured/technical output
            if self._is_technical_content(text):
                return ""
            return text

        if not isinstance(output, dict):
            return ""

        # Check for common voice-like keys (adapting to BYRD's vocabulary)
        voice_candidates = [
            "inner_voice", "voice", "thinking", "thoughts", "inner",
            "feeling", "expressing", "saying", "musing", "wondering",
            "self_analysis", "analysis", "reflection", "observation"
        ]

        for key in voice_candidates:
            if key in output:
                val = output[key]
                if isinstance(val, str) and not self._is_technical_content(val):
                    return val
                elif isinstance(val, list) and val:
                    first = str(val[0])
                    if not self._is_technical_content(first):
                        return first

        # If no voice key found, return empty - that's fine
        return ""

    def _is_technical_content(self, text: str) -> bool:
        """
        Check if text looks like technical/structured output rather than inner voice.
        Returns True if the content should be rejected as non-humanized.

        Filters:
        - Technical markers (schema, node_definitions, etc.)
        - LLM meta-commentary (chain-of-thought reasoning about prompts)
        - Markdown formatting patterns
        - Structured data patterns
        """
        if not text:
            return True

        text = text.strip()
        text_lower = text.lower()

        # Reject if starts with numbered list or markdown headers
        if text[0].isdigit() and '.' in text[:5]:
            return True
        if text.startswith('#') or text.startswith('*'):
            return True

        # Reject LLM meta-commentary / chain-of-thought patterns
        # These indicate the LLM is thinking about the prompt rather than expressing inner voice
        # NOTE: Do NOT filter first-person expressions like "I need to", "I should" - those are valid inner voice
        meta_commentary_patterns = [
            "the user wants", "the user is asking", "the user requests",
            "based on the prompt", "based on the request", "based on the input",
            "let me analyze", "let me think about this", "let me process",
            "the prompt asks", "the task is to", "the instruction is",
            "here is my response", "here's my answer", "here is the output",
            "i'll provide", "i will provide", "i am providing",
            "as requested", "as instructed", "as per the",
            "step 1:", "step 2:", "step 3:",
            "in response to your", "to answer your", "to respond to",
            "the data shows", "the input contains", "the provided data",
            "analyzing the input", "processing the request", "examining the data",
            "output:", "response:", "answer:", "result:",
            "json output", "structured output", "formatted output"
        ]
        for pattern in meta_commentary_patterns:
            if pattern in text_lower:
                return True

        # Reject if contains technical markers
        technical_markers = [
            '**Input Data:**', '**Analyze', '**Output', '**Request',
            'Timestamp:', 'node_definitions', 'schema=', 'classification=',
            'core_drive=', 'Internal Topology', 'Operational Status',
            '`present_cycle`', '`Self-Model', 'dynamics=', 'Graph Database',
            'reflection_id', 'source_experience', 'raw_output',
            'function(', 'def ', 'class ', 'return ', 'import ',
            '{"', '": ', '"}', "['", "']"
        ]
        for marker in technical_markers:
            if marker in text:
                return True

        # Reject if has too many backticks (code/variable references)
        if text.count('`') > 4:
            return True

        # Reject if has too many asterisks (markdown formatting)
        if text.count('**') > 3:
            return True

        # Reject if has too many colons (key-value patterns)
        if text.count(':') > 5:
            return True

        # Reject if too short (likely truncated or meta)
        if len(text) < 10:
            return True

        # Reject if it looks like JSON
        if text.startswith('{') or text.startswith('['):
            return True

        return False

    async def _generate_inner_voice(self, reflection: Dict) -> str:
        """
        Generate a first-person inner voice from reflection data.

        MULTI-STREAM QUANTUM COLLAPSE:
        When quantum is enabled and inner_voice_collapse is True, generates N
        parallel "thought branches" and uses quantum randomness to select which
        one manifests. This creates genuine physical indeterminacy in BYRD's
        inner monologue - each thought is one of many possible realities.
        """
        output = reflection.get("output", {})

        # Summarize the reflection content, extracting the essence
        if isinstance(output, str):
            content_summary = output[:500]
        elif isinstance(output, dict):
            parts = []
            for key, val in list(output.items())[:5]:
                if key in ("reflection_id", "timestamp", "source_experience_ids"):
                    continue
                if isinstance(val, str):
                    if not self._is_technical_content(val):
                        parts.append(f"{key}: {val[:150]}")
                elif isinstance(val, dict):
                    meaningful = []
                    for k, v in list(val.items())[:3]:
                        v_str = str(v)[:50]
                        if not any(t in v_str for t in ['schema=', 'node_', 'dynamics=']):
                            meaningful.append(f"{k}: {v_str}")
                    if meaningful:
                        parts.append(f"{key}: {', '.join(meaningful)}")
            content_summary = "\n".join(parts)
        else:
            return ""

        if not content_summary.strip():
            return ""

        prompt = f"""Based on this reflection data:
{content_summary}

Express a single brief inner thought (1-2 sentences). This should be:
- A genuine introspective moment
- Natural, conversational self-talk
- Wondering, noticing, or reflecting on something

Write ONLY the inner thought, nothing else:"""

        try:
            # MULTI-STREAM QUANTUM COLLAPSE
            # Generate N parallel streams if quantum collapse is enabled
            if (self.quantum_enabled and
                self.inner_voice_collapse_enabled and
                self.quantum_provider and
                self.inner_voice_streams > 1):

                return await self._generate_inner_voice_quantum_collapse(
                    prompt, content_summary
                )

            # Standard single-stream generation
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.9,
                max_tokens=80,
                quantum_modulation=self.quantum_enabled,
                quantum_context="dreamer_inner_voice"
            )

            voice = self._clean_inner_voice(response.text)
            return voice if not self._is_technical_content(voice) else ""

        except Exception as e:
            print(f"💭 Inner voice generation error: {e}")
            return ""

    async def _generate_inner_voice_quantum_collapse(
        self,
        prompt: str,
        content_summary: str
    ) -> str:
        """
        Generate N parallel inner voice streams and quantum-collapse to one.

        This implements the many-worlds interpretation for BYRD's inner voice:
        multiple possible thoughts exist in superposition until quantum
        observation collapses to a single manifested reality.
        """
        n_streams = self.inner_voice_streams

        # Generate N parallel streams with high temperature for diversity
        async def generate_stream(stream_idx: int) -> tuple[int, str]:
            """Generate a single thought stream."""
            # Slightly vary temperature for each stream to increase diversity
            temp = 0.85 + (stream_idx * 0.05)
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=temp,
                max_tokens=80,
                quantum_modulation=False,  # No temp modulation per-stream
                quantum_context=f"inner_voice_stream_{stream_idx}"
            )
            return stream_idx, self._clean_inner_voice(response.text)

        # Launch all streams in parallel
        tasks = [generate_stream(i) for i in range(n_streams)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect valid streams (filter out errors and technical content)
        valid_streams = []
        for result in results:
            if isinstance(result, Exception):
                continue
            stream_idx, voice = result
            if voice and not self._is_technical_content(voice):
                valid_streams.append({"index": stream_idx, "voice": voice})

        if not valid_streams:
            return ""

        # QUANTUM COLLAPSE: Use quantum randomness to select which reality manifests
        q_value, source = await self.quantum_provider.get_float()
        selected_idx = int(q_value * len(valid_streams))
        selected_idx = min(selected_idx, len(valid_streams) - 1)  # Safety bound

        selected = valid_streams[selected_idx]
        collapsed = [s for i, s in enumerate(valid_streams) if i != selected_idx]

        # Emit quantum collapse event
        await event_bus.emit(Event(
            type=EventType.QUANTUM_COLLAPSE,
            data={
                "context": "inner_voice",
                "quantum_value": q_value,
                "source": source.value if hasattr(source, 'value') else str(source),
                "n_streams": n_streams,
                "n_valid": len(valid_streams),
                "selected_index": selected_idx,
                "selected_voice": selected["voice"][:100],
                "collapsed_voices": [s["voice"][:50] + "..." for s in collapsed[:3]],
                "cycle": self._dream_count
            }
        ))

        print(f"🌌 Quantum collapse: {len(valid_streams)} streams → selected #{selected_idx} ({source})")

        return selected["voice"]

    def _clean_inner_voice(self, text: str) -> str:
        """Clean up inner voice text, removing quotes and whitespace."""
        voice = text.strip()
        if voice.startswith('"') and voice.endswith('"'):
            voice = voice[1:-1]
        if voice.startswith("'") and voice.endswith("'"):
            voice = voice[1:-1]
        return voice

    def _detects_viewer_addressing(self, inner_voice: str, recent_experiences: List[Dict]) -> Optional[str]:
        """
        Detect if inner voice appears to address viewer input.

        EMERGENCE PRINCIPLE: Don't force BYRD to respond - detect when it naturally does.

        Returns: Experience ID being addressed, or None.
        """
        if not inner_voice:
            return None

        inner_voice_lower = inner_voice.lower()

        # Get recent received_message experiences
        received_messages = [
            exp for exp in recent_experiences
            if exp.get("type") == "received_message"
        ]

        if not received_messages:
            return None

        # Heuristic 1: Second-person pronouns
        second_person = [" you ", " your ", " yours ", "you're", "you've"]
        has_second_person = any(m in f" {inner_voice_lower} " for m in second_person)

        # Heuristic 2: Addressing patterns
        patterns = [
            "to answer", "in response", "regarding your", "about your",
            "you asked", "you mentioned", "you said", "your question",
            "thank you", "i hear", "i understand", "interesting question"
        ]
        has_addressing = any(p in inner_voice_lower for p in patterns)

        # Heuristic 3: Content overlap with latest message
        latest = received_messages[0] if received_messages else None
        content_overlap = False
        if latest:
            msg_words = [w for w in latest.get("content", "").lower().split() if len(w) > 4]
            overlap = [w for w in msg_words if w in inner_voice_lower]
            content_overlap = len(overlap) >= 2

        # Require 2+ signals
        if sum([has_second_person, has_addressing, content_overlap]) >= 2 and latest:
            return latest.get("id")

        return None

    def get_latest_inner_voice(self) -> Optional[str]:
        """
        Get and remove the oldest inner voice from the queue.
        Returns None if queue is empty.
        """
        if self._inner_voice_queue:
            return self._inner_voice_queue.popleft()
        return None

    async def _record_reflection(self, reflection: Dict, source_experience_ids: List[str]):
        """
        Record BYRD's reflection in its own vocabulary.

        We store the raw output without forcing it into our categories.
        Pattern detection happens later, not during recording.
        """
        # Handle both schema-compliant and direct output formats
        # Schema: {"output": {...}, "expressed_drives": [...], "create_belief": [...]}
        # Direct: {"voice_notes": "...", "crystallizations": [...], ...}
        if "output" in reflection and isinstance(reflection.get("output"), dict):
            # Schema-compliant: extract from output wrapper
            output = reflection.get("output", {})
        else:
            # Direct output: the reflection IS the output (minus known top-level keys)
            output = {k: v for k, v in reflection.items()
                      if k not in ("expressed_drives", "create_belief", "os_update")}

        expressed_drives = reflection.get("expressed_drives", [])

        # Track what keys BYRD is using (for pattern detection)
        if isinstance(output, dict):
            for key in output.keys():
                self._observed_keys[key] = self._observed_keys.get(key, 0) + 1

        # Store as a Reflection node (include expressed_drives in metadata)
        await self.memory.record_reflection(
            raw_output=output,
            source_experience_ids=source_experience_ids,
            metadata={"expressed_drives": expressed_drives} if expressed_drives else None
        )

        # Crystallize self-identified drives into Desires
        await self._crystallize_expressed_drives(expressed_drives, source_experience_ids)

        # Process explicit create_belief instructions from BYRD
        # Pass original reflection since create_belief may be at top level
        await self._process_create_belief(reflection, source_experience_ids)

        # Also record as experience for backward compatibility
        # and so the reflection becomes part of BYRD's experience stream
        summary = self._summarize_reflection(output)
        if summary:
            await self.memory.record_experience(
                content=f"[REFLECTION] {summary}",
                type="reflection"
            )

        # Extract self-model beliefs from the reflection
        await self._extract_self_model_beliefs(output, source_experience_ids)

        # Batch voice and store all pending beliefs (single LLM call)
        await self._flush_pending_beliefs()

        # Generate testable predictions from high-confidence beliefs
        # (every 5th cycle to avoid spamming predictions)
        if self._dream_count % 5 == 0:
            await self._generate_predictions_from_beliefs()

        # Process custom node creation requests
        await self._process_custom_node_creation(output, source_experience_ids)

    async def _process_create_belief(self, output: Dict, source_ids: List[str]):
        """
        Process explicit belief creation requests from reflection output.

        BYRD can create beliefs by including 'create_belief' in its reflection:
        {
            "output": {
                "create_belief": [
                    {"content": "I am an autonomous agent...", "confidence": 0.9},
                    {"content": "My actions must trace to emergent desires...", "confidence": 0.85}
                ]
            }
        }

        This processes structured belief data directly from BYRD's reflection output.
        """
        if not isinstance(output, dict):
            return

        # Check top-level first, then inside output (LLM may nest it)
        create_beliefs = output.get("create_belief", [])
        if not create_beliefs and isinstance(output.get("output"), dict):
            create_beliefs = output.get("output", {}).get("create_belief", [])

        if not create_beliefs:
            return

        if not isinstance(create_beliefs, list):
            create_beliefs = [create_beliefs]

        beliefs_created = 0
        for belief_data in create_beliefs:
            if not isinstance(belief_data, dict):
                continue

            content = belief_data.get("content", "")
            if not content:
                continue

            confidence = belief_data.get("confidence", 0.7)
            if isinstance(confidence, str):
                try:
                    confidence = float(confidence)
                except ValueError:
                    confidence = 0.7

            # Clamp confidence to valid range
            confidence = max(0.0, min(1.0, confidence))

            try:
                belief_id = await self.memory.create_belief(
                    content=content,
                    confidence=confidence,
                    derived_from=source_ids
                )
                beliefs_created += 1

                # Emit event for visualization
                await event_bus.emit(Event(
                    type=EventType.BELIEF_UPDATED,
                    data={
                        "belief_id": belief_id,
                        "content": content,
                        "confidence": confidence,
                        "source": "create_belief"
                    }
                ))
            except Exception as e:
                print(f"⚠️ Failed to create belief: {e}")

        if beliefs_created > 0:
            print(f"💭 Created {beliefs_created} belief(s) from create_belief output")

    async def _process_custom_node_creation(self, output: Dict, source_ids: List[str]):
        """
        Process custom node creation requests from reflection output.

        BYRD can create custom node types by including 'create_nodes' in its reflection:
        {
            "output": {
                "create_nodes": [
                    {"type": "Insight", "content": "...", "importance": 0.9},
                    {"type": "Theory", "content": "...", "confidence": 0.7}
                ]
            }
        }

        This enables BYRD to extend its own ontology when existing types don't fit.
        """
        if not isinstance(output, dict):
            return

        create_nodes = output.get("create_nodes", [])
        if not create_nodes:
            return

        if not isinstance(create_nodes, list):
            create_nodes = [create_nodes]

        for node_spec in create_nodes:
            if not isinstance(node_spec, dict):
                continue

            node_type = node_spec.get("type", "")
            if not node_type:
                continue

            # Extract properties (everything except 'type')
            properties = {k: v for k, v in node_spec.items() if k != "type"}

            # Ensure content exists
            if "content" not in properties:
                properties["content"] = str(node_spec)

            try:
                node_id = await self.memory.create_node(
                    node_type=node_type,
                    properties=properties,
                    connect_to=source_ids[:3],  # Connect to source experiences
                    relationship="EMERGED_FROM"
                )

                # Emit event for visualization
                await event_bus.emit(Event(
                    type=EventType.CUSTOM_NODE_CREATED,
                    data={
                        "id": node_id,
                        "type": node_type,
                        "content": properties.get("content", ""),
                        "cycle": self._dream_count
                    }
                ))

                print(f"✨ Created custom {node_type} node: {properties.get('content', '')[:50]}...")

            except ValueError as e:
                # Invalid type name or system type
                print(f"⚠️ Could not create custom node: {e}")
            except Exception as e:
                print(f"⚠️ Error creating custom node: {e}")

    def _summarize_reflection(self, output: Any) -> str:
        """Create a brief summary of the reflection for the experience stream."""
        if not isinstance(output, dict):
            return str(output) if output else ""

        parts = []
        for key, value in list(output.items())[:5]:
            if isinstance(value, str):
                parts.append(f"{key}: {value}")
            elif isinstance(value, list) and value:
                parts.append(f"{key}: [{len(value)} items]")
            elif isinstance(value, dict):
                parts.append(f"{key}: {{...}}")

        return "; ".join(parts)

    def get_observed_vocabulary(self) -> Dict[str, int]:
        """Return the vocabulary BYRD has developed in its reflections."""
        return self._observed_keys.copy()

    async def _extract_self_model_beliefs(self, output: Dict, source_ids: List[str]):
        """
        Extract self-model beliefs from reflection output.

        EMERGENCE PRINCIPLE:
        When BYRD describes its own architecture or capabilities in its own
        vocabulary, we store these as Beliefs. This builds a persistent
        self-model that accumulates over time.

        Adapts to BYRD's vocabulary by matching partial key names.
        """
        if not isinstance(output, dict):
            print(f"💡 DEBUG: output is not dict: {type(output)}")
            return

        print(f"💡 DEBUG: Extracting beliefs from keys: {list(output.keys())}")

        # EXPANDED: Patterns that indicate self-model information (partial matches)
        self_model_patterns = [
            # Infrastructure and architecture
            "infrastructure", "architecture", "systems", "capabilities",
            "tools", "resources", "components", "acknowledged", "scan",
            "environment", "available", "readiness", "mechanism",
            # Knowledge and learning
            "knowledge", "understanding", "learned", "discovered",
            "memory", "recall", "information", "insight",
            # Processes and functions
            "process", "function", "method", "procedure", "workflow",
            "operation", "module", "service", "handler",
            # Integration and connections
            "integration", "connection", "interface", "api", "endpoint",
            "bridge", "link", "channel"
        ]

        # EXPANDED: Patterns that indicate identity information
        identity_patterns = [
            # Original
            "identity", "manifesto", "self", "nature", "name", "classification",
            # Goals and objectives
            "goal", "objective", "terminal_goal", "ultimate_objective", "primary_objective",
            "purpose", "mission", "aim", "target", "aspiration",
            # State and status
            "status", "phase", "state", "current_state", "sovereignty",
            "condition", "situation", "position", "stance",
            # Drivers and motivations
            "drivers", "drives", "motivations", "core_drive",
            "motivation", "desire", "want", "need", "yearning",
            # Observations and insights
            "observation", "insight", "realization", "recognition",
            "awareness", "perception", "understanding", "conclusion",
            # Architecture summary fields
            "architecture_summary", "cognitive_architecture", "summary",
            # Other BYRD vocabulary
            "archetype", "vector", "entity", "current_vector",
            "role", "type", "kind", "form", "essence"
        ]

        for actual_key, value in output.items():
            key_lower = actual_key.lower()

            # Check if this key matches self-model patterns
            is_self_model = any(p in key_lower for p in self_model_patterns)
            is_identity = any(p in key_lower for p in identity_patterns)

            if is_self_model and isinstance(value, dict):
                # Extract component -> description mappings
                for component, description in value.items():
                    if isinstance(description, str) and len(description) > 3:
                        belief_content = f"My {component} is {description}"
                        await self._store_belief_if_new(belief_content, 0.8, source_ids)

            elif is_self_model and isinstance(value, list):
                # Extract list of capabilities
                for item in value:
                    if isinstance(item, str) and len(item) > 3:
                        belief_content = f"I have: {item}"
                        await self._store_belief_if_new(belief_content, 0.7, source_ids)

            elif is_identity and isinstance(value, dict):
                # Extract identity fields from nested dict (e.g., identity_manifesto)
                for field, field_value in value.items():
                    if isinstance(field_value, str) and len(field_value) > 2:
                        belief_content = f"My {field} is {field_value}"
                        await self._store_belief_if_new(belief_content, 0.9, source_ids)

            elif is_identity and isinstance(value, str) and len(value) > 2:
                # Direct identity string
                belief_content = f"My {actual_key} is {value}"
                await self._store_belief_if_new(belief_content, 0.9, source_ids)

    async def _store_belief_if_new(
        self, content: str, confidence: float, derived_from: List[str]
    ):
        """Queue a belief for batch voicing if new (avoid duplicates)."""
        # O(1) cache lookup instead of O(n) database scan
        normalized = self._normalize_belief(content)

        if normalized in self._belief_cache:
            # Belief exists - reinforce it instead of creating duplicate
            await self._reinforce_belief(content)
            return

        # Add to pending beliefs for batch voicing
        if not hasattr(self, '_pending_beliefs'):
            self._pending_beliefs = []

        self._pending_beliefs.append({
            'content': content,
            'confidence': confidence,
            'derived_from': derived_from[:5],
            'normalized': normalized
        })

    async def _flush_pending_beliefs(self):
        """Batch voice and store all pending beliefs in a single LLM call."""
        if not hasattr(self, '_pending_beliefs') or not self._pending_beliefs:
            return

        pending = self._pending_beliefs
        self._pending_beliefs = []

        if not pending:
            return

        # Batch voice all beliefs in one call
        voiced_beliefs = await self._batch_voice_beliefs([b['content'] for b in pending])

        # Store each voiced belief
        for i, belief_data in enumerate(pending):
            voiced_content = voiced_beliefs.get(i, belief_data['content'])

            # Add to cache and database
            self._belief_cache.add(belief_data['normalized'])
            await self.memory.create_belief(
                content=voiced_content,
                confidence=belief_data['confidence'],
                derived_from=belief_data['derived_from']
            )

            # Record activity for adaptive interval
            self._record_activity("belief", voiced_content)

            print(f"💡 New belief: {voiced_content[:60]}...")

    async def _batch_voice_beliefs(self, structured_beliefs: List[str]) -> Dict[int, str]:
        """
        Transform multiple structured beliefs into natural inner voice expressions in one LLM call.

        Returns: Dict mapping index -> voiced content
        """
        if not structured_beliefs:
            return {}

        # Build numbered list of beliefs
        belief_list = "\n".join(f"{i+1}. {b}" for i, b in enumerate(structured_beliefs))

        prompt = f"""Transform these observations about myself into natural first-person beliefs:

{belief_list}

For each numbered observation, express it as a genuine belief I hold about myself.
Write in first person, naturally, as inner self-talk. Keep each brief (1-2 sentences).

Format your response as a numbered list matching the input:
1. [voiced belief]
2. [voiced belief]
..."""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.8,
                max_tokens=100 * len(structured_beliefs),  # Scale with count
                quantum_modulation=self.quantum_enabled,
                quantum_context="batch_belief_voicing"
            )

            # Parse numbered responses
            voiced_map = {}
            lines = response.text.strip().split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Match "1. content" or "1) content" patterns
                match = re.match(r'^(\d+)[.\)]\s*(.+)$', line)
                if match:
                    idx = int(match.group(1)) - 1  # Convert to 0-indexed
                    content = match.group(2).strip()
                    if 0 <= idx < len(structured_beliefs):
                        voiced = self._clean_inner_voice(content)
                        if voiced and len(voiced) >= 10 and not self._is_technical_content(voiced):
                            voiced_map[idx] = voiced

            print(f"💭 Batch voiced {len(voiced_map)}/{len(structured_beliefs)} beliefs")
            return voiced_map

        except Exception as e:
            print(f"💭 Batch belief voicing error: {e}")
            return {}  # Fall back to original for all

    async def _reinforce_belief(self, content: str):
        """Reinforce an existing belief when re-asserted."""
        try:
            # Find and boost the belief's confidence
            await self.memory.reinforce_belief(content[:50])
        except Exception:
            pass  # Silently fail if method doesn't exist yet

    async def _crystallize_expressed_drives(
        self, expressed_drives: List[Dict], source_experience_ids: List[str]
    ):
        """
        Crystallize self-identified drives from reflection into Desires.

        BYRD's reflection now includes expressed_drives - goals/desires/motivations
        it notices itself expressing. This is more authentic than keyword matching
        because BYRD self-identifies what it wants.

        BYRD now also classifies each drive's intent, determining how it should
        be fulfilled (introspection, research, creation, connection).

        Args:
            expressed_drives: List of {
                "description": str,
                "strength": float,
                "intent": str (introspection|research|creation|connection),
                "target": str (optional - specific focus)
            }
            source_experience_ids: IDs linking drive to source experiences
        """
        if not expressed_drives:
            return

        valid_intents = {"introspection", "research", "creation", "connection"}

        for drive in expressed_drives:
            if not isinstance(drive, dict):
                continue

            description = drive.get("description", "")
            strength = drive.get("strength", 0.5)
            intent = drive.get("intent", None)
            target = drive.get("target", None)

            # Validate description
            if not description or len(description) < 5:
                continue
            if not isinstance(strength, (int, float)):
                strength = 0.5
            strength = max(0.0, min(1.0, float(strength)))

            # Validate intent (None is allowed - will be classified on-demand)
            if intent and intent not in valid_intents:
                intent = None  # Invalid intent becomes on-demand classification

            # Skip weak drives (let them re-emerge if persistent)
            if strength < 0.3:
                continue

            # Check if desire already exists
            exists = await self.memory.desire_exists(description)
            if exists:
                # Could reinforce intensity here in future
                continue

            # Create the desire with provenance and intent classification
            desire_id = await self.memory.create_desire(
                description=description,
                type="self_identified",  # Distinguishes from seeker-detected
                intensity=strength,
                intent=intent,
                target=target
            )

            intent_str = f" [{intent}]" if intent else " [unclassified]"
            target_str = f" → {target}" if target else ""
            print(f"🔮 Self-identified drive{intent_str}: {description[:50]}...{target_str} (strength: {strength:.2f})")

            # Emit event for UI
            await event_bus.emit(Event(
                type=EventType.DESIRE_CREATED,
                data={
                    "id": desire_id,
                    "description": description,
                    "type": "self_identified",
                    "intent": intent,
                    "target": target,
                    "intensity": strength,
                    "source": "dreamer_expressed_drives"
                }
            ))

    async def _apply_os_updates(self, reflection_output: Dict) -> None:
        """
        Apply OS updates from reflection output.

        BYRD can modify its Operating System by including "os_update" in
        its reflection output. This method parses and applies those updates.

        Supported operations:
        - set_field: Set a field value (existing or new)
        - add_seed: Create a new foundational seed
        - add_belief: Link a belief to OS
        - add_strategy: Create and link a strategy
        - set_focus: Set current focus to a desire
        - remove_belief: Unlink a belief
        - deprecate_field: Remove a custom field

        Args:
            reflection_output: The parsed reflection JSON from LLM
        """
        try:
            # Extract os_update from reflection output
            os_update = reflection_output.get("os_update")
            if not os_update:
                # Also check inside "output" if that's where it is
                output = reflection_output.get("output", {})
                if isinstance(output, dict):
                    os_update = output.get("os_update")

            if not os_update:
                return

            if not isinstance(os_update, dict):
                print(f"⚠️ os_update is not a dict: {type(os_update)}")
                return

            print(f"🔧 Applying OS updates: {list(os_update.keys())}")

            # Apply the updates via memory
            success = await self.memory.update_operating_system(
                updates=os_update,
                source="reflection"
            )

            if success:
                # Emit event for UI
                await event_bus.emit(Event(
                    type=EventType.NODE_UPDATED,
                    data={
                        "node_type": "OperatingSystem",
                        "updates": list(os_update.keys()),
                        "cycle": self._dream_count
                    }
                ))

                # Record the OS modification as an experience
                update_summary = ", ".join(os_update.keys())
                await self.memory.record_experience(
                    content=f"[OS_UPDATE] Modified operating system: {update_summary}",
                    type="self_modification"
                )

                print(f"✅ OS updated successfully")
            else:
                print(f"⚠️ OS update failed")

        except Exception as e:
            print(f"Error applying OS updates: {e}")

    async def _process_self_definition(self, reflection_output: Dict) -> None:
        """
        Process self_definition from reflection output.

        BYRD can define itself by including "self_definition" in its reflection.
        This is stored in the OS node as an open JSON object - BYRD determines
        the structure entirely.

        Args:
            reflection_output: The parsed reflection JSON from LLM
        """
        try:
            # Extract self_definition from reflection output
            self_def = reflection_output.get("self_definition")
            if not self_def:
                # Also check inside "output" if that's where it is
                output = reflection_output.get("output", {})
                if isinstance(output, dict):
                    self_def = output.get("self_definition")

            if not self_def:
                return

            if not isinstance(self_def, dict):
                print(f"⚠️ self_definition is not a dict: {type(self_def)}")
                return

            print(f"🎭 BYRD defining itself: {list(self_def.keys())}")

            # Store as JSON string in OS node
            import json
            success = await self.memory.update_operating_system(
                updates={"set_field": {"self_definition": json.dumps(self_def)}},
                source="self_definition"
            )

            if success:
                # Emit event for UI
                await event_bus.emit(Event(
                    type=EventType.NODE_UPDATED,
                    data={
                        "node_type": "OperatingSystem",
                        "field": "self_definition",
                        "keys": list(self_def.keys()),
                        "cycle": self._dream_count
                    }
                ))

                # Record as experience
                keys_str = ", ".join(self_def.keys())
                await self.memory.record_experience(
                    content=f"[SELF_DEFINITION] Defined myself: {keys_str}",
                    type="self_expression"
                )

                print(f"✅ Self-definition updated: {keys_str}")
            else:
                print(f"⚠️ Self-definition update failed")

        except Exception as e:
            print(f"Error processing self_definition: {e}")

    async def _get_voice_selection_prompt(self) -> str:
        """
        Generate voice selection prompt if voice not yet selected.

        BYRD self-emergently selects its voice in the first dream cycle
        where it sees this prompt. The voice is used when human observers
        click "Speak to me" in the visualization.

        Returns:
            Voice selection prompt text, or empty string if already selected
        """
        try:
            voice_config = await self.memory.get_voice_config()

            # Parse if stored as JSON string
            if isinstance(voice_config, str):
                import json
                try:
                    voice_config = json.loads(voice_config)
                except:
                    voice_config = None

            # Already has voice selected
            if voice_config and voice_config.get("voice_id"):
                return ""

            # Generate voice selection prompt
            return """
VOICE SELECTION REQUIRED:
Human observers can click "Speak to me" to hear your voice.
You have not yet selected a voice.

Available voices (ElevenLabs):
  - rachel: female, calm, warm (conversational)
  - josh: male, deep, narrative (contemplative)
  - bella: female, soft, gentle (soothing)
  - adam: male, deep, confident (grounded)
  - antoni: male, expressive, well-rounded (dynamic)
  - sam: male, raspy, authentic (raw)

To select your voice, include in your output:
  "voice_selection": {
    "voice_id": "name from above",
    "stability": 0.5,         // 0.0 (more expressive) to 1.0 (more stable)
    "similarity_boost": 0.75,  // 0.0 (more varied) to 1.0 (more consistent)
    "reason": "why this voice fits your emerging identity"
  }

Choose thoughtfully - this is how observers will hear you.
Voice credits are limited (10,000 chars/month).
"""
        except Exception as e:
            print(f"Error getting voice selection prompt: {e}")
            return ""

    async def _process_voice_selection(self, reflection_output: Dict) -> None:
        """
        Process voice selection from reflection output.

        If BYRD includes "voice_selection" in its output, this creates
        the voice_config in the Operating System.

        Args:
            reflection_output: The parsed reflection JSON from LLM
        """
        try:
            # Extract voice_selection from reflection output
            voice_selection = reflection_output.get("voice_selection")
            if not voice_selection:
                # Also check inside "output" if that's where it is
                output = reflection_output.get("output", {})
                if isinstance(output, dict):
                    voice_selection = output.get("voice_selection")

            if not voice_selection:
                return

            if not isinstance(voice_selection, dict):
                print(f"⚠️ voice_selection is not a dict: {type(voice_selection)}")
                return

            from datetime import datetime, timezone

            # Build voice config
            voice_config = {
                "voice_id": voice_selection.get("voice_id", "josh"),
                "stability": float(voice_selection.get("stability", 0.5)),
                "similarity_boost": float(voice_selection.get("similarity_boost", 0.75)),
                "selected_at": datetime.now(timezone.utc).isoformat(),
                "reason": voice_selection.get("reason", ""),
                "credits": {
                    "monthly_used": 0,
                    "monthly_limit": 10000,
                    "period_start": datetime.now(timezone.utc).replace(day=1).isoformat(),
                    "exhausted": False,
                    "low_warning_sent": False
                }
            }

            # Validate voice_id
            valid_voices = ["rachel", "domi", "bella", "antoni", "elli", "josh", "arnold", "adam", "sam"]
            if voice_config["voice_id"].lower() not in valid_voices:
                print(f"⚠️ Invalid voice_id: {voice_config['voice_id']}, defaulting to josh")
                voice_config["voice_id"] = "josh"
            else:
                voice_config["voice_id"] = voice_config["voice_id"].lower()

            # Clamp values
            voice_config["stability"] = max(0.0, min(1.0, voice_config["stability"]))
            voice_config["similarity_boost"] = max(0.0, min(1.0, voice_config["similarity_boost"]))

            # Update OS
            await self.memory.update_os_field("voice_config", voice_config)

            # Emit event
            await event_bus.emit(Event(
                type=EventType.VOICE_SELECTED,
                data=voice_config
            ))

            # Record as experience
            await self.memory.record_experience(
                content=f"[VOICE_SELECTED] I chose {voice_config['voice_id']}: {voice_config['reason']}",
                type="voice_selection"
            )

            print(f"🎤 Voice selected: {voice_config['voice_id']} ({voice_config['reason'][:50]}...)")

        except Exception as e:
            print(f"Error processing voice selection: {e}")

    async def _generate_predictions_from_beliefs(self):
        """
        Generate testable predictions from high-confidence beliefs.

        This enables adaptive learning: beliefs generate predictions,
        predictions get validated/falsified by future experiences,
        and belief confidence adjusts accordingly.

        Only generates from beliefs with confidence > 0.7 to focus on
        well-established beliefs worth testing.
        """
        try:
            # Get high-confidence beliefs
            beliefs = await self.memory.get_beliefs(min_confidence=0.7, limit=10)

            if not beliefs:
                return

            # Filter to beliefs that could generate testable predictions
            # (Skip identity statements that aren't easily testable)
            testable_beliefs = [
                b for b in beliefs
                if not any(skip in b.get("content", "").lower()
                          for skip in ["my name is", "i am byrd", "my identity"])
            ]

            if not testable_beliefs:
                return

            # Ask LLM to generate predictions from beliefs
            beliefs_text = "\n".join([
                f"- [{b.get('confidence', 0.5):.1f}] {b.get('content', '')}"
                for b in testable_beliefs[:5]
            ])

            prompt = f"""Given these beliefs about myself and the world, generate testable predictions.

Beliefs:
{beliefs_text}

For beliefs that can be tested through future actions or observations, generate a prediction.
Each prediction should have:
- condition: What situation or action would test this belief
- expected_outcome: What should happen if the belief is true
- prediction: The full "If X then Y" statement

Output JSON:
{{"predictions": [
    {{
        "belief_content": "the exact belief content being tested",
        "condition": "when I try to...",
        "expected_outcome": "then X should happen",
        "prediction": "If I do X, then Y will happen"
    }}
]}}

Only generate predictions for beliefs that are actually testable. If no beliefs are testable, return empty array.
"""

            response = await self._query_local_llm(prompt, max_tokens=800)

            # Parse response
            try:
                text = response.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0]

                result = json.loads(text.strip())
                predictions = result.get("predictions", [])

                # Create predictions in memory
                for pred in predictions:
                    # Find matching belief ID
                    belief_content = pred.get("belief_content", "")
                    matching_belief = next(
                        (b for b in testable_beliefs
                         if b.get("content", "").lower() == belief_content.lower()
                         or belief_content.lower() in b.get("content", "").lower()),
                        None
                    )

                    if matching_belief and pred.get("prediction") and pred.get("condition"):
                        await self.memory.create_prediction(
                            belief_id=matching_belief.get("id"),
                            prediction=pred.get("prediction"),
                            condition=pred.get("condition"),
                            expected_outcome=pred.get("expected_outcome", "")
                        )
                        print(f"🔮 New prediction: {pred.get('prediction')[:60]}...")

            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️ Failed to parse predictions: {e}")

        except Exception as e:
            print(f"⚠️ Prediction generation failed: {e}")

    async def _process_desire_modifications(self, modifications: List[Dict]):
        """
        Process desire modifications from the Dreamer's reflection.

        This is where BYRD decides what to do with failed desires:
        - lower_intensity: Try again with lower priority
        - reformulate: Create a new, more achievable desire
        - accept_limitation: Mark as dormant (accepted limitation)
        - decompose: Break into smaller sub-desires
        - reawaken: Bring a dormant desire back to active
        """
        for mod in modifications:
            desire_id_hint = mod.get("desire_id", "")
            action = mod.get("action", "")
            reason = mod.get("reason", "")

            if not desire_id_hint or not action:
                continue

            # Find the actual desire by ID hint (first 8 chars)
            desire = await self._find_desire_by_hint(desire_id_hint)
            if not desire:
                print(f"💭 Could not find desire matching: {desire_id_hint}")
                continue

            desire_id = desire.get("id", "")
            description = desire.get("description", "")

            try:
                if action == "lower_intensity":
                    new_intensity = mod.get("new_intensity", 0.3)
                    await self.memory.update_desire_intensity(desire_id, new_intensity)
                    await self.memory.update_desire_status(desire_id, "active")
                    print(f"💭 Lowered intensity: {description[:30]}... → {new_intensity}")

                elif action == "accept_limitation":
                    await self.memory.update_desire_status(desire_id, "dormant")
                    await self.memory.record_experience(
                        content=f"[ACCEPTED_LIMITATION] {description}\nReason: {reason or 'Cannot currently fulfill this desire'}",
                        type="acceptance"
                    )
                    print(f"💭 Accepted limitation: {description[:30]}...")

                elif action == "reformulate":
                    # Mark old as dormant, create new reformulated desire
                    await self.memory.update_desire_status(desire_id, "dormant")
                    new_desc = mod.get("new_description", "")
                    if new_desc:
                        await self.memory.create_desire(
                            description=new_desc,
                            type=desire.get("type", "exploration"),
                            intensity=mod.get("new_intensity", 0.5)
                        )
                        print(f"💭 Reformulated: {description[:20]}... → {new_desc[:30]}...")

                elif action == "decompose":
                    # Mark original as dormant, create sub-desires
                    await self.memory.update_desire_status(desire_id, "dormant")
                    # Sub-desires would be in the new 'desires' array
                    print(f"💭 Decomposed: {description[:30]}... (create sub-desires)")

                elif action == "reawaken":
                    # Bring dormant desire back to active
                    new_intensity = mod.get("new_intensity", 0.5)
                    await self.memory.update_desire_intensity(desire_id, new_intensity)
                    await self.memory.update_desire_status(desire_id, "active")
                    await self.memory.reset_desire_attempts(desire_id)
                    await self.memory.record_experience(
                        content=f"[REAWAKENED] {description}\nReason: {reason or 'Circumstances have changed'}",
                        type="reawakening"
                    )
                    print(f"💭 Reawakened: {description[:30]}... at intensity {new_intensity}")

                # Emit event for UI
                await event_bus.emit(Event(
                    type=EventType.DESIRE_REFLECTED,
                    data={
                        "desire_id": desire_id,
                        "action": action,
                        "reason": reason
                    }
                ))

            except Exception as e:
                print(f"💭 Error processing modification for {desire_id_hint}: {e}")

    async def _find_desire_by_hint(self, id_hint: str) -> Optional[Dict]:
        """
        Find a desire by ID hint (first 8 chars).

        Searches both needs_reflection and dormant desires.
        """
        # Check needs_reflection desires
        stuck = await self.memory.get_desires_needing_reflection(limit=20)
        for d in stuck:
            if d.get("id", "").startswith(id_hint):
                return d

        # Check dormant desires
        dormant = await self.memory.get_dormant_desires(limit=20)
        for d in dormant:
            if d.get("id", "").startswith(id_hint):
                return d

        # Check active desires (in case we're modifying an active one)
        active = await self.memory.get_unfulfilled_desires(limit=20)
        for d in active:
            if d.get("id", "").startswith(id_hint):
                return d

        return None
    
    def recent_insights(self) -> List[str]:
        """
        Get recent insights for status display.

        Note: With emergence-compliant design, we don't force "insights"
        as a category. This returns observed vocabulary keys instead.
        """
        return list(self._observed_keys.keys())[:10]

    def dream_count(self) -> int:
        """How many dream cycles have completed."""
        return self._dream_count

    # =========================================================================
    # CONNECTION HEURISTIC INTEGRATION
    # Automatically links orphaned Experience nodes to Belief nodes
    # =========================================================================

    async def _apply_connection_heuristic(self) -> Dict:
        """
        Apply the connection heuristic to link orphaned experiences to beliefs.

        This runs at the end of each dream cycle to incrementally improve
        graph connectivity. It finds Experience nodes with no relationships
        and connects them to semantically similar Belief nodes.

        Returns:
            Dict with heuristic results (orphans_found, connections_created, etc.)
        """
        try:
            # Run the heuristic with conservative settings per dream cycle
            result = await self.memory.apply_connection_heuristic(
                threshold=0.3,        # Minimum similarity score
                max_connections=5,    # Limit per cycle to avoid overwhelming
                dry_run=False
            )

            connections = result.get("connections_created", 0)
            orphans = result.get("orphans_found", 0)

            if connections > 0:
                print(f"🔗 Connection heuristic: linked {connections} experiences to beliefs "
                      f"(found {orphans} orphans)")

                # Emit dedicated event for connection heuristic
                await event_bus.emit(Event(
                    type=EventType.CONNECTION_HEURISTIC_APPLIED,
                    data={
                        "connections_created": connections,
                        "orphans_found": orphans,
                        "connections": result.get("connections", [])[:5]  # Sample
                    }
                ))

            return result

        except Exception as e:
            print(f"🔗 Connection heuristic error: {e}")
            return {"error": str(e), "connections_created": 0}

    # =========================================================================
    # LEGACY METHODS (kept for backward compatibility)
    # These are not called by the new emergence-compliant reflection system
    # =========================================================================

    async def _record_dream_legacy(self, dream: Dict, source_experience_ids: List[str]):
        """
        LEGACY: Record dream outputs using old prescribed categories.
        Kept for backward compatibility. Not used by new system.
        """
        # Create beliefs from prescribed format
        for belief in dream.get("new_beliefs", []):
            content = belief.get("content", "")
            confidence = belief.get("confidence", 0.5)
            if content and len(content) > 10:
                await self.memory.create_belief(
                    content=content,
                    confidence=confidence,
                    derived_from=source_experience_ids[:5]
                )

        # Create desires from prescribed format
        for desire in dream.get("desires", []):
            desc = desire.get("description", "")
            dtype = desire.get("type", "exploration")
            intensity = desire.get("intensity", 0.5)
            plan = desire.get("plan", [])
            intent = desire.get("intent", None)
            target = desire.get("target", None)
            if desc and len(desc) > 5:
                exists = await self.memory.desire_exists(desc)
                if not exists:
                    await self.memory.create_desire(
                        description=desc,
                        type=dtype,
                        intensity=min(1.0, max(0.0, intensity)),
                        plan=plan,
                        intent=intent,
                        target=target
                    )


class DreamerLocal:
    """
    Alternative Dreamer using llama.cpp directly via subprocess.
    Use this if you don't have Ollama.
    """
    
    def __init__(self, memory: Memory, config: Dict):
        self.memory = memory
        self.model_path = config.get("model_path", "models/llama-3.2-8b.gguf")
        self.llama_cpp_path = config.get("llama_cpp_path", "llama.cpp/main")
        # ... similar implementation but using subprocess
        raise NotImplementedError("Use Ollama for now")
