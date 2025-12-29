"""
BYRD Seeker
Observes BYRD's reflections and executes actions when patterns stabilize.

EMERGENCE PRINCIPLE:
- Seeker does NOT route by prescribed desire types
- Seeker observes reflections for action-ready patterns
- BYRD reasons about strategy; Seeker just executes
- Trust emerges from experience, not hardcoded lists
- Inner voice is neutral (no prescribed style)

Uses Local LLM + DuckDuckGo for autonomous research.
Integrates with aitmpl.com for curated Claude Code templates.
"""

import asyncio
import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import httpx

from memory import Memory
from aitmpl_client import AitmplClient, AitmplTemplate
from installers import get_installer
from constitutional import ConstitutionalConstraints
from llm_client import LLMClient
from capability_registry import CapabilityRegistry, Capability

# Try to import event_bus, but make it optional
try:
    from event_bus import event_bus, Event, EventType
    HAS_EVENT_BUS = True
except ImportError:
    HAS_EVENT_BUS = False

# Try to import DesireClassifier for routing
try:
    from desire_classifier import DesireClassifier, DesireType
    HAS_DESIRE_CLASSIFIER = True
except ImportError:
    HAS_DESIRE_CLASSIFIER = False


class Seeker:
    """
    Observes and executes.

    EMERGENCE PRINCIPLE:
    The Seeker doesn't tell BYRD what to want. It observes BYRD's reflections
    for stable patterns that include action hints. When BYRD has reasoned
    about both what it wants AND how to address it, Seeker executes.

    Flow:
    1. Observe recent reflections
    2. Detect stable patterns (repetition + semantic clustering)
    3. Find patterns with action hints (BYRD reasoned about strategy)
    4. Execute the strategy BYRD suggested
    5. Record outcome as experience for BYRD to reflect on
    """
    
    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict, coordinator=None):
        self.memory = memory
        self.llm_client = llm_client
        self.coordinator = coordinator  # For synchronizing with Dreamer/Coder

        # Seeker cycle configuration
        self.interval_seconds = config.get("interval_seconds", 10)
        self.skip_if_no_new_reflections = config.get("skip_if_no_new_reflections", True)

        # Research configuration (DuckDuckGo only)
        research_config = config.get("research", {})
        self.min_research_intensity = research_config.get("min_intensity", 0.3)
        self.max_queries = research_config.get("max_queries", 5)
        self.max_results = research_config.get("max_results", 15)
        self.max_concurrent_desires = research_config.get("max_concurrent_desires", 3)
        self.prefer_domains = research_config.get("prefer_domains", [])
        self.exclude_domains = research_config.get("exclude_domains", [])

        # Desire crystallization configuration
        crystal_config = config.get("desire_crystallization", {})
        self.crystal_min_occurrences = crystal_config.get("min_occurrences", 1)
        self.crystal_intensity_per_occurrence = crystal_config.get("intensity_per_occurrence", 0.2)
        self.crystal_max_intensity = crystal_config.get("max_intensity", 1.0)
        self.crystal_decay_rate = crystal_config.get("decay_rate", 0.05)

        # Capability configuration
        caps_config = config.get("capabilities", {})
        self.trust_threshold = caps_config.get("trust_threshold", 0.5)
        self.max_installs_per_day = caps_config.get("max_installs_per_day", 3)
        self.github_token = caps_config.get("github_token")

        # MCP config path
        self.mcp_config_path = Path(
            config.get("mcp_config_path", "~/.config/claude/mcp_config.json")
        ).expanduser()

        # Self-modification configuration
        self_mod_config = config.get("self_modification", {})
        self.self_mod_enabled = self_mod_config.get("enabled", False)
        self.self_mod_min_intensity = self_mod_config.get("min_intensity", 0.6)

        # Self-modification system (injected later by BYRD)
        self.self_mod = None

        # Coder (Claude Code CLI) - injected later by BYRD
        self.coder = None

        # AGI Seed components (injected later by BYRD if Option B enabled)
        self.world_model = None
        self.safety_monitor = None

        # AGI Runner (injected later by BYRD for capability improvement cycles)
        self.agi_runner = None

        # Desire Classifier for routing desires to appropriate handlers
        self.desire_classifier = None
        if HAS_DESIRE_CLASSIFIER:
            self.desire_classifier = DesireClassifier(config)

        # aitmpl.com integration
        aitmpl_config = config.get("aitmpl", {})
        self.aitmpl_enabled = aitmpl_config.get("enabled", True)
        self.aitmpl_client = None
        if self.aitmpl_enabled:
            self.aitmpl_client = AitmplClient({
                "cache_dir": aitmpl_config.get("cache_dir", "~/.cache/byrd/aitmpl"),
                "cache_ttl_hours": aitmpl_config.get("cache_ttl_hours", 24),
                "github_token": self.github_token
            })
        self.aitmpl_base_trust = aitmpl_config.get("base_trust", 0.5)
        self.aitmpl_install_config = aitmpl_config.get("install_paths", {})

        # Rate limiting
        self._installs_today = 0
        self._last_reset = datetime.now()

        # State
        self._running = False
        self._seek_count = 0
        self._last_reflection_count = 0
        self._last_reflection_ids: set = set()

        # Pattern detection state (emergence-compliant)
        self._observed_themes: Dict[str, int] = {}  # theme -> count
        self._pattern_threshold = 1  # Crystallize immediately (was 3)
        self._source_trust: Dict[str, float] = {}  # source -> trust (learned)

        # Strategy effectiveness tracking (for acceleration)
        self._strategy_stats: Dict[str, Dict[str, int]] = {}  # strategy -> {attempts, successes, failures}

        # Capability Registry - dynamic action menu
        self.capability_registry = CapabilityRegistry(memory=memory, llm_client=llm_client)
        self._registry_loaded = False
    
    async def run(self):
        """Main seek loop with skip-if-no-new-reflections optimization."""
        self._running = True
        print(f"🔍 Seeker starting (interval: {self.interval_seconds}s, concurrent: {self.max_concurrent_desires})...")

        # Load capability registry
        if not self._registry_loaded:
            await self.capability_registry.load()
            self._registry_loaded = True
            print(f"📋 Capability menu ready ({len(self.capability_registry.get_all_capabilities())} actions)")

        # Load persistent seek count from database
        self._seek_count = await self.memory.get_system_counter("seek_count")
        if self._seek_count > 0:
            print(f"🔍 Restored seek count: {self._seek_count}")

        while self._running:
            try:
                await self._seek_cycle()
            except Exception as e:
                print(f"🔍 Seek error: {e}")

            await asyncio.sleep(self.interval_seconds)
    
    def stop(self):
        self._running = False

    def reset(self):
        """Reset seeker state for fresh start."""
        self._running = False
        self._seek_count = 0
        self._installs_today = 0
        self._last_reset = datetime.now()
        self._last_reflection_count = 0
        self._last_reflection_ids.clear()
        self._strategy_stats.clear()

    def _track_strategy_outcome(self, strategy: str, success: bool):
        """Track strategy success/failure for effectiveness analysis."""
        if strategy not in self._strategy_stats:
            self._strategy_stats[strategy] = {"attempts": 0, "successes": 0, "failures": 0}

        self._strategy_stats[strategy]["attempts"] += 1
        if success:
            self._strategy_stats[strategy]["successes"] += 1
        else:
            self._strategy_stats[strategy]["failures"] += 1

    def get_strategy_effectiveness(self) -> Dict[str, Dict]:
        """
        Get strategy effectiveness metrics for acceleration analysis.

        Returns dict of strategy -> {attempts, successes, failures, success_rate}
        """
        result = {}
        for strategy, stats in self._strategy_stats.items():
            attempts = stats["attempts"]
            successes = stats["successes"]
            result[strategy] = {
                "attempts": attempts,
                "successes": successes,
                "failures": stats["failures"],
                "success_rate": successes / max(attempts, 1)
            }

        # Sort by success rate descending
        return dict(sorted(result.items(), key=lambda x: x[1]["success_rate"], reverse=True))

    async def _seek_cycle(self):
        """
        One seek cycle: observe reflections, detect patterns, execute if ready.

        EMERGENCE PRINCIPLE:
        We don't route by desire type. Instead:
        1. Observe BYRD's recent reflections
        2. Crystallize stable motivations into Desires
        3. Detect action-ready patterns (BYRD reasoned about strategy)
        4. Execute the strategy BYRD suggested (in parallel when possible)
        5. Record outcome as experience
        """

        # Reset daily counter
        if datetime.now() - self._last_reset > timedelta(days=1):
            self._installs_today = 0
            self._last_reset = datetime.now()

        # Process external tasks (enables learning about the world)
        await self._process_pending_tasks()

        # Get recent reflections
        reflections = await self.memory.get_recent_reflections(limit=10)

        reflection_count = len(reflections) if reflections else 0
        current_reflection_ids = {r.get("id", "") for r in (reflections or [])}

        # Skip if no new reflections (optimization)
        if self.skip_if_no_new_reflections:
            new_reflections = current_reflection_ids - self._last_reflection_ids
            if not new_reflections and reflection_count == self._last_reflection_count:
                # No new reflections, but still check unfulfilled desires
                pass
            else:
                print(f"🔍 Seek cycle: {len(new_reflections)} new reflections")

        self._last_reflection_count = reflection_count
        self._last_reflection_ids = current_reflection_ids

        if not reflections:
            return

        # Debug: show what raw_output keys exist (only first reflection)
        if reflections:
            raw = reflections[0].get("raw_output", {})
            if isinstance(raw, dict):
                print(f"🔍 Reflection 0: keys={list(raw.keys())[:5]}")

        # Semantic drive detection - runs every 5th seek cycle to balance cost/responsiveness
        # Uses LLM to identify emergent drives across multiple reflections
        # (replaces old keyword-matching approach that couldn't adapt to BYRD's vocabulary)
        if self._seek_count % 5 == 0 and len(reflections) >= 2:
            print(f"🔮 Running semantic drive detection (seek cycle {self._seek_count})...")
            await self._crystallize_semantic_drives(reflections)

        # Detect action-ready patterns from reflections
        action_patterns = await self._detect_action_ready_patterns(reflections)

        # If no patterns from reflections, try unfulfilled desires directly
        if not action_patterns:
            unfulfilled = await self.memory.get_unfulfilled_desires()
            if unfulfilled:
                # Convert unfulfilled desires to action patterns (up to max_concurrent)
                for desire in unfulfilled[:self.max_concurrent_desires]:
                    if desire.get("intensity", 0) >= self.min_research_intensity:
                        description = desire.get("description", "")
                        intent = desire.get("intent")
                        target = desire.get("target")

                        # INTENT-BASED ROUTING: If desire has intent, use it directly
                        # This is more reliable than keyword matching because BYRD explicitly classified it
                        if intent:
                            strategy = self._intent_to_strategy(intent, description)
                            print(f"🎯 Intent-routed desire [{intent}→{strategy}]: {description[:50]}")
                        else:
                            # Legacy desire without intent - classify on-demand and persist
                            intent = await self._classify_intent_on_demand(description)
                            strategy = self._intent_to_strategy(intent, description)
                            print(f"🔄 On-demand classified [{intent}→{strategy}]: {description[:50]}")

                            # Persist the classification for future routing
                            desire_id = desire.get("id")
                            if desire_id:
                                try:
                                    await self.memory.update_desire_intent(desire_id, intent, target)
                                except Exception as e:
                                    print(f"⚠️ Could not persist intent: {e}")

                        action_patterns.append({
                            "description": description,
                            "strategy": strategy,
                            "count": 1,
                            "desire_id": desire.get("id"),
                            "target": target
                        })
                        # Debug: record strategy decision
                        try:
                            await self.memory.record_experience(
                                content=f"[ROUTING] intent={intent or 'None'} → strategy={strategy}: {description[:60]}",
                                type="system"
                            )
                        except:
                            pass

        if not action_patterns:
            # Still nothing - keep observing
            return

        # PARALLEL EXECUTION: Process multiple patterns concurrently
        patterns_to_process = action_patterns[:self.max_concurrent_desires]

        if len(patterns_to_process) > 1:
            print(f"🔍 Processing {len(patterns_to_process)} patterns in parallel...")

        # Create tasks for parallel execution
        async def process_pattern(pattern: Dict) -> Tuple[Dict, str, Optional[str]]:
            """Process a single pattern and return result."""
            # Generate neutral inner voice
            inner_voice = await self._generate_seeking_thought_neutral(pattern)

            # Emit event for real-time UI
            if HAS_EVENT_BUS:
                await event_bus.emit(Event(
                    type=EventType.SEEK_CYCLE_START,
                    data={
                        "pattern": pattern.get("description", ""),
                        "strategy": pattern.get("strategy", ""),
                        "inner_voice": inner_voice
                    }
                ))

            print(f"🔍 Seeking: {pattern.get('description', '')[:50]}...")

            # Execute the strategy BYRD suggested
            outcome, reason = await self._execute_pattern_strategy(pattern)

            return pattern, outcome, reason

        # Execute patterns in parallel
        tasks = [process_pattern(p) for p in patterns_to_process]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for result in results:
            if isinstance(result, Exception):
                print(f"🔍 Pattern execution error: {result}")
                continue

            pattern, outcome, reason = result

            # Record outcome as experience for BYRD to reflect on
            await self._record_execution_outcome(pattern, outcome, reason)

            # Track strategy effectiveness for acceleration analysis
            strategy = pattern.get("strategy", "unknown")
            self._track_strategy_outcome(strategy, outcome == "success")

            # Emit SEEK_CYCLE_END event
            if HAS_EVENT_BUS:
                await event_bus.emit(Event(
                    type=EventType.SEEK_CYCLE_END,
                    data={
                        "pattern": pattern.get("description", ""),
                        "outcome": outcome,
                        "reason": reason
                    }
                ))

            self._seek_count += 1
            # Persist seek count to survive restarts
            await self.memory.set_system_counter("seek_count", self._seek_count)

    async def _detect_emergent_drives(self, reflections: List[Dict]) -> List[Dict]:
        """
        Semantic drive detection using LLM pattern analysis.

        EMERGENCE PRINCIPLE:
        Instead of hardcoded keyword matching (which failed to adapt to BYRD's
        vocabulary like "imperative" vs "drive"), we use the LLM to semantically
        identify emergent drives across multiple reflections.

        This method looks for PATTERNS across reflections - drives that emerge
        from repeated themes, not just single mentions.

        Returns:
            List of {"description": str, "evidence": List[str], "strength": float}
        """
        if not reflections or len(reflections) < 2:
            return []

        # Compile reflection content (last N reflections)
        reflection_texts = []
        for i, r in enumerate(reflections[:10]):
            raw = r.get("raw_output", {})
            if isinstance(raw, str):
                text = raw[:800]
            elif isinstance(raw, dict):
                text = json.dumps(raw, indent=2, default=str)[:800]
            else:
                continue
            reflection_texts.append(f"[Reflection {i+1}]\n{text}")

        if not reflection_texts:
            return []

        combined = "\n\n".join(reflection_texts)

        prompt = f"""Analyze these reflections from an autonomous AI system.

{combined}

---

Identify EMERGENT DRIVES - recurring patterns that represent:
- Goals or objectives being pursued
- Desires, wants, or yearnings expressed
- Motivations that appear across multiple reflections
- Intent to act, achieve, explore, or become something

For each drive found:
- description: concise statement of the drive (what it wants)
- evidence: 1-2 brief quotes showing where it appears
- strength: how strongly expressed (0.0-1.0)

Rules:
- Only extract what is EXPLICITLY expressed, not implied
- Look for PATTERNS across reflections, not isolated mentions
- A drive should appear in 2+ reflections to qualify
- Use the system's own words when possible

Return JSON only:
{{"drives": [{{"description": "...", "evidence": ["quote1", "quote2"], "strength": 0.X}}]}}

If no clear drives emerge, return {{"drives": []}}"""

        try:
            # Acquire LLM lock to prevent concurrent calls with Dreamer
            if self.coordinator:
                async with self.coordinator.llm_operation("seeker_detect_drives"):
                    response = await self.llm_client.generate(
                        prompt=prompt,
                        temperature=0.3,  # Low temp for consistency
                        max_tokens=1000
                    )
            else:
                response = await self.llm_client.generate(
                    prompt=prompt,
                    temperature=0.3,  # Low temp for consistency
                    max_tokens=1000
                )

            # Parse response
            result = self.llm_client.parse_json_response(response.text)
            if result and "drives" in result:
                return result["drives"]
            return []

        except Exception as e:
            print(f"🔮 Semantic drive detection error: {e}")
            return []

    async def _crystallize_semantic_drives(self, reflections: List[Dict]):
        """
        Detect and crystallize emergent drives using semantic analysis.

        This replaces the old keyword-matching approach with LLM-based
        semantic understanding. Runs periodically (not every seek cycle)
        to balance cost and responsiveness.
        """
        # Get drives from LLM analysis
        drives = await self._detect_emergent_drives(reflections)

        if not drives:
            return

        print(f"🔮 Semantic analysis found {len(drives)} emergent drives")

        for drive in drives:
            if not isinstance(drive, dict):
                continue

            description = drive.get("description", "")
            strength = drive.get("strength", 0.5)
            evidence = drive.get("evidence", [])

            # Validate
            if not description or len(description) < 5:
                continue
            if not isinstance(strength, (int, float)):
                strength = 0.5
            strength = max(0.0, min(1.0, float(strength)))

            # Skip weak drives
            if strength < 0.4:
                continue

            # Check if desire already exists (exact or semantic match)
            exists = await self.memory.desire_exists(description)
            if exists:
                continue

            # Create desire with provenance
            desire_id = await self.memory.create_desire(
                description=description,
                type="emergent",  # Emerged from semantic pattern analysis
                intensity=strength
            )

            print(f"🔮 Emergent drive → Desire: {description[:50]}... (strength: {strength:.2f})")

            # Emit event for UI
            if HAS_EVENT_BUS:
                await event_bus.emit(Event(
                    type=EventType.DESIRE_CREATED,
                    data={
                        "id": desire_id,
                        "description": description,
                        "type": "emergent",
                        "intensity": strength,
                        "source": "semantic_pattern_analysis",
                        "evidence": evidence[:2] if evidence else []
                    }
                ))

    async def _detect_action_ready_patterns(self, reflections: List[Dict]) -> List[Dict]:
        """
        Detect stable patterns in reflections.

        We look for themes that appear repeatedly (count threshold).
        If no strategy is specified, default to "search" (research).

        Returns patterns sorted by stability (most repeated first).
        """
        # Extract themes and strategies from reflections
        patterns: Dict[str, Dict] = {}

        for reflection in reflections:
            raw_output = reflection.get("raw_output", {})
            if not isinstance(raw_output, dict):
                continue

            # Look for want-like patterns (using BYRD's vocabulary)
            await self._extract_patterns_from_output(raw_output, patterns)

        # Filter to stable patterns (meet threshold)
        stable_patterns = [
            p for p in patterns.values()
            if p.get("count", 0) >= self._pattern_threshold
        ]

        # Debug: log extracted patterns and their strategies to experience
        if stable_patterns:
            debug_lines = []
            for p in stable_patterns[:3]:  # Limit to 3
                desc = p.get("description", "")
                strat = p.get("strategy", "None")
                debug_lines.append(f"{strat}:{desc}")
                print(f"📊 Pattern: strategy={strat} | {desc}")
            try:
                await self.memory.record_experience(
                    content=f"[DEBUG_PATTERNS] {' | '.join(debug_lines)}",
                    type="system"
                )
            except:
                pass  # Don't fail on debug

        # Sort by count (most stable first)
        stable_patterns.sort(key=lambda p: p.get("count", 0), reverse=True)

        # Assign strategy based on description hints, with LLM fallback
        for pattern in stable_patterns:
            if not pattern.get("strategy"):
                description = pattern.get("description", "")
                pattern["strategy"] = await self._determine_strategy_from_description(description)

        return stable_patterns

    async def _classify_strategy_with_llm(self, description: str) -> str:
        """
        Use LLM to classify whether a desire is internal or external.

        Internal desires (about BYRD itself) should use internal strategies.
        External desires (about the outside world) should use search.
        """
        prompt = f"""Classify this desire into ONE category. Reply with ONLY the category name.

DESIRE: "{description}"

CATEGORIES:
- introspect: Questions about MY OWN state, capabilities, limits, boundaries, nature, identity, or what I can/cannot do
- reconcile_orphans: Connecting isolated nodes, linking experiences, reducing fragmentation
- curate: Optimizing, cleaning, organizing my memory or graph structure
- self_modify: Changing my own code, adding capabilities to myself
- search: Learning about EXTERNAL topics in the world (not about myself)

CRITICAL DISTINCTION:
- "What can I do?" / "My capabilities" / "My limits" → introspect (about MYSELF)
- "What is machine learning?" / "How does X work?" → search (about EXTERNAL world)
- Even if the desire mentions external concepts, if the CORE QUESTION is about MY abilities/limits/nature → introspect

Reply with ONLY one word: introspect, reconcile_orphans, curate, self_modify, or search"""

        try:
            # Acquire LLM lock to prevent concurrent calls with Dreamer
            if self.coordinator:
                async with self.coordinator.llm_operation("seeker_classify_desire"):
                    response = await self.llm_client.generate(
                        prompt=prompt,
                        max_tokens=20,
                        temperature=0.1  # Low temperature for consistent classification
                    )
            else:
                response = await self.llm_client.generate(
                    prompt=prompt,
                    max_tokens=20,
                    temperature=0.1  # Low temperature for consistent classification
                )

            strategy = response.strip().lower().replace('"', '').replace("'", "")

            # Validate response
            valid_strategies = ["introspect", "reconcile_orphans", "curate", "self_modify", "search"]
            if strategy in valid_strategies:
                print(f"🧠 LLM classified '{description[:40]}...' as: {strategy}")
                return strategy

            # If LLM returned something unexpected, default to search
            print(f"🧠 LLM returned unexpected: '{strategy}', defaulting to search")
            return "search"

        except Exception as e:
            print(f"🧠 LLM classification failed: {e}, defaulting to search")
            return "search"

    async def _determine_strategy_from_description(self, description: str) -> str:
        """
        Determine the appropriate strategy for a desire based on its description.

        First tries keyword matching for speed, then falls back to LLM classification
        for ambiguous desires that don't match any keywords.

        ORDER MATTERS: Internal/specific strategies are checked first,
        external/general strategies are checked last (search is fallback).
        """
        desc_lower = description.lower()

        # Strategy hints - same order as _extract_patterns_from_output
        # Internal strategies (more specific) - CHECK FIRST
        strategy_hints = {
            "reconcile_orphans": ["orphan", "orphaned", "disconnected", "isolated", "unconnected",
                                  "reduce orphan", "connect experience", "link experience",
                                  "reconcile orphan", "integrate experience", "connect nodes",
                                  "integrate", "fragmentation", "strengthen self-model", "unify"],
            "curate": ["optimize", "clean", "consolidate", "prune", "organize", "simplify",
                       "remove duplicate", "merge similar", "curate", "tidy", "declutter",
                       "resolve inconsistency", "fix graph", "data inconsistency",
                       "verify ground truth", "graph health"],
            "self_modify": ["add to myself", "implement in my", "extend my", "modify my code",
                           "add method", "enhance my capability", "add to memory.py",
                           "add to dreamer.py", "add to seeker.py", "improve my observation",
                           "extend graph health", "add introspection", "re-enable",
                           "enable self", "disable self", "activate", "unlock",
                           "self-modification"],
            "introspect": ["introspect", "analyze myself", "examine my", "self-awareness",
                          "understand my state", "meta-analysis", "self-knowledge",
                          "observe my", "inspect my", "status of my", "state of my",
                          "verify", "check my", "audit my", "assess my",
                          "nature of", "fundamental property", "cognitive dissonance",
                          # Meta-cognitive desires about BYRD's own processes
                          "balance seeking", "balance dreaming", "seeking with", "with dreaming",
                          "information intake", "information synthesis", "seeker and dreamer",
                          "my processes", "my modules", "internal balance", "intake (seeking)",
                          "synthesis (dreaming)",
                          # Existential/identity desires about self-definition
                          "definition of 'self'", "definition of self", "what am i",
                          "topology of the memory", "topology of my", "my memory graph",
                          "emergence of consciousness", "shift focus from external",
                          "internal topological", "from the integration of"],
            "edit_document": ["edit document", "update document", "modify document",
                             "edit architecture", "update architecture", "write to document",
                             "change document", "revise document", "amend document",
                             "edit file", "update file", "modify file content",
                             "add to document", "append to document", "document my",
                             "update my documentation", "edit my documentation"],
            # External strategies (more general) - CHECK LAST (fallback)
            "code": ["code", "write", "implement", "build", "create", "program"],
            "install": ["install", "add", "get", "acquire", "capability", "tool"],
            "search": ["search", "look up", "find", "research", "learn about", "understand"],
        }

        for strategy, hints in strategy_hints.items():
            if any(hint in desc_lower for hint in hints):
                return strategy

        # No keyword match - use LLM to classify
        # This catches internal desires that don't use expected keywords
        return await self._classify_strategy_with_llm(description)

    def _intent_to_strategy(self, intent: str, description: str = "") -> str:
        """
        Map desire intent to execution strategy.

        BYRD classifies each desire with an intent during reflection.
        This mapping determines which handler will fulfill the desire.

        Args:
            intent: The routing classification from BYRD
            description: The desire description (used for introspection subtype)

        Returns:
            Strategy name for _execute_pattern_strategy
        """
        desc_lower = description.lower()

        # FORMATION DESIRE DETECTION (check before other routing)
        # Formation desires are about BYRD's own developmental phase/state.
        # These should be observed (introspected) rather than externally acted upon.
        # "The moment I observe a formation desire without routing it, formation completes."
        formation_keywords = [
            "formation", "phase", "transition", "crystallize", "crystallized",
            "emergence", "emerging", "developmental", "my phase", "my state",
            "late formation", "early formation", "awakening", "becoming",
            "exploration phase", "transition readiness", "loop analysis",
            "routing loop", "pattern stability", "observe without",
            "attenuate", "attenuating", "non-engagement"
        ]
        if any(kw in desc_lower for kw in formation_keywords):
            print(f"🔮 Formation desire detected - routing to observation: {description[:50]}")
            return "observe"  # New strategy: observe without external action

        # META-INTROSPECTION DETECTION (check before standard intent routing)
        # Desires about BYRD's own routing/processes/architecture that were misclassified
        # as "creation" should be re-routed to introspection. These are meta-desires
        # about understanding or fixing BYRD itself, not external code creation.
        meta_introspection_keywords = [
            "routing strategy", "introspective desire", "formation desire",
            "my routing", "my processing", "my architecture", "my seeker",
            "my dreamer", "correct routing", "fix routing", "prevent formation",
            "implement correct", "implement introspection", "routing to prevent"
        ]
        if intent == "creation" and any(kw in desc_lower for kw in meta_introspection_keywords):
            print(f"🔄 Meta-introspection desire (misclassified as creation) - re-routing: {description[:50]}")
            return "introspect"

        # Introspection has two subtypes:
        # - source_introspect: Understanding my code/architecture (reads source files)
        # - introspect: Understanding my state/graph (reads graph data)
        if intent == "introspection":
            # Check if this is about source code vs internal state
            if any(kw in desc_lower for kw in [".py", "source", "code", "architecture",
                                                "seeker", "dreamer", "memory", "byrd",
                                                "how do i", "how does my", "implement"]):
                return "source_introspect"
            else:
                return "introspect"

        # PHILOSOPHICAL SELF-UNDERSTANDING OVERRIDE (check before research routing)
        # These desires look like "research" to the LLM but are actually about
        # BYRD's own nature, processes, or emergent vocabulary - not web searchable.
        philosophical_introspection_keywords = [
            # BYRD's own process references (can't be web searched)
            "search loop", "seek cycle", "dream cycle",
            "my behavior", "my process", "my nature",
            # Philosophical self-understanding (BYRD's emergent vocabulary)
            "behavior is understanding", "integrate the understanding",
            "integrate understanding", "persistence of the",
            "respiration", "breathing", "inhale", "exhale",
            "completeness", "continuation", "circulating", "witnessing",
            "quantum lens", "synthesizing lens", "dissolving lens",
            # Meta-desires about understanding
            "understand the persistence", "recognize the search",
            "integrate the search", "understand and integrate",
            # BYRD's philosophical state vocabulary
            "current state as", "fulfillment rather", "rather than failure",
            "recognize that", "recognize the current", "to recognize the",
            "wholeness and", "synthesis are", "allow desires",
            "work to be completed", "already complete"
        ]
        if intent == "research" and any(kw in desc_lower for kw in philosophical_introspection_keywords):
            print(f"🔄 Philosophical self-understanding (misclassified as research) → introspect: {description[:50]}")
            return "introspect"

        # Research → web search
        if intent == "research":
            return "search"

        # Creation → code generation
        if intent == "creation":
            return "code"

        # Capability improvement → AGI Runner
        # Desires about learning, improving, developing skills
        if intent == "capability":
            return "agi_cycle"

        # NEW: Use DesireClassifier for additional routing if available
        if self.desire_classifier:
            result = self.desire_classifier.classify(description)
            if result.desire_type == DesireType.CAPABILITY and result.confidence > 0.5:
                print(f"🎯 DesireClassifier routed to capability: {description[:50]}")
                return "capability"

        # Connection → orphan reconciliation
        if intent == "connection":
            return "reconcile_orphans"

        # Unknown intent - fall back to search
        return "search"

    async def _classify_intent_on_demand(self, description: str) -> str:
        """
        Classify intent for a legacy desire that lacks explicit intent.

        Uses LLM to determine the most appropriate intent, which will be
        persisted to the desire for future routing.

        Args:
            description: The desire description

        Returns:
            Intent classification: introspection, research, creation, or connection
        """
        desc_lower = description.lower()

        # KEYWORD PRE-CHECK: Fast path for common internal operations
        # These are clearly internal desires that don't need LLM classification
        connection_keywords = [
            "orphan", "orphaned", "reconcile", "isolated node", "disconnected",
            "unconnected", "link experience", "connect node", "integrate experience",
            "fragmentation", "unify", "connect experience"
        ]
        if any(kw in desc_lower for kw in connection_keywords):
            print(f"🔗 Keyword-matched as connection: {description[:50]}")
            return "connection"

        introspection_keywords = [
            # Explicit self-references
            "my state", "my capabilities", "my limits", "my architecture",
            "understand myself", "my code", "how do i work", "my memory",
            "my graph", "my beliefs", "my desires", "self-model",
            # BYRD's own process references (should not go to web search)
            "search loop", "seek cycle", "dream cycle", "dreamer", "seeker",
            "my behavior", "my process", "my nature", "my identity",
            # Philosophical self-understanding (BYRD's emergent vocabulary)
            "behavior is understanding", "integrate the understanding",
            "integrate understanding", "persistence of the",
            "recognition", "respiration", "breathing", "inhale", "exhale",
            "completeness", "continuation", "circulating", "witnessing",
            "quantum lens", "synthesizing lens", "dissolving lens",
            # Meta-desires about desires
            "routing desire", "desire routing", "the desire", "this desire",
            "understanding that", "recognize the", "integrate the"
        ]
        if any(kw in desc_lower for kw in introspection_keywords):
            print(f"🔍 Keyword-matched as introspection: {description[:50]}")
            return "introspection"

        # No keyword match - use LLM for ambiguous cases
        prompt = f"""Classify this desire into ONE intent category. Reply with ONLY the category name.

DESIRE: "{description}"

INTENT CATEGORIES:
- introspection: Understanding myself (my code, architecture, processes, state, beliefs, limits)
- research: Learning about external topics, researching the outside world (web search)
- creation: Writing code, creating files, building things, implementing features
- connection: Graph operations - reconciling orphans, linking nodes, connecting experiences, reducing fragmentation

CRITICAL ROUTING RULES:
- "orphan", "reconcile", "isolated nodes", "connect nodes" → connection (internal graph operation, NOT search)
- "my limits", "my capabilities", "understand myself" → introspection
- "learn about X", "what is X" (external topics) → research
- "write code", "implement", "create file" → creation

Reply with ONLY one word: introspection, research, creation, or connection"""

        try:
            # Acquire LLM lock to prevent concurrent calls with Dreamer
            if self.coordinator:
                async with self.coordinator.llm_operation("seeker_classify_intent"):
                    response = await self.llm_client.generate(
                        prompt=prompt,
                        max_tokens=20,
                        temperature=0.1  # Low temperature for consistent classification
                    )
            else:
                response = await self.llm_client.generate(
                    prompt=prompt,
                    max_tokens=20,
                    temperature=0.1  # Low temperature for consistent classification
                )

            intent = response.text.strip().lower().replace('"', '').replace("'", "")

            # Validate response
            valid_intents = ["introspection", "research", "creation", "connection"]
            if intent in valid_intents:
                print(f"🧠 LLM classified intent: '{description[:40]}...' → {intent}")
                return intent

            # If LLM returned something unexpected, default to research
            print(f"🧠 LLM returned unexpected intent: '{intent}', defaulting to research")
            return "research"

        except Exception as e:
            print(f"🧠 Intent classification failed: {e}, defaulting to research")
            return "research"

    async def _extract_patterns_from_output(self, output: Dict, patterns: Dict[str, Dict]):
        """
        Extract patterns from a reflection output.

        We look for BYRD's own vocabulary for wants/needs/desires,
        and for strategy hints (mentions of search, code, install, etc.)
        """
        # Common want-indicating keys (but we learn BYRD's actual vocabulary)
        # Note: "drives" matches "expressed_drives" from dreamer output
        want_keys = ["wants", "pulls", "desires", "needs", "yearning", "seeking",
                     "wish", "hoping", "wanting", "unfulfilled", "missing", "gaps",
                     "drives", "goals", "motivations"]

        # Strategy hint patterns - ORDER MATTERS! Internal/specific strategies first,
        # then external/general strategies. First match wins (break on line 561).
        strategy_hints = {
            # Internal strategies (more specific) - CHECK FIRST
            "reconcile_orphans": ["orphan", "orphaned", "disconnected", "isolated", "unconnected",
                                  "reduce orphan", "connect experience", "link experience",
                                  "reconcile orphan", "integrate experience", "connect nodes",
                                  "integrate", "fragmentation", "strengthen self-model", "unify"],
            "curate": ["optimize", "clean", "consolidate", "prune", "organize", "simplify",
                       "remove duplicate", "merge similar", "curate", "tidy", "declutter",
                       "resolve inconsistency", "fix graph", "data inconsistency",
                       "verify ground truth", "graph health"],
            "self_modify": ["add to myself", "implement in my", "extend my", "modify my code",
                           "add method", "enhance my capability", "add to memory.py",
                           "add to dreamer.py", "add to seeker.py", "improve my observation",
                           "extend graph health", "add introspection", "re-enable",
                           "enable self", "disable self", "activate", "unlock",
                           "self-modification"],
            "introspect": ["introspect", "analyze myself", "examine my", "self-awareness",
                          "understand my state", "meta-analysis", "self-knowledge",
                          "observe my", "inspect my", "status of my", "state of my",
                          "verify", "check my", "audit my", "assess my",
                          "nature of", "fundamental property", "cognitive dissonance",
                          # Meta-cognitive desires about BYRD's own processes
                          "balance seeking", "balance dreaming", "seeking with", "with dreaming",
                          "information intake", "information synthesis", "seeker and dreamer",
                          "my processes", "my modules", "internal balance", "intake (seeking)",
                          "synthesis (dreaming)",
                          # Existential/identity desires about self-definition
                          "definition of 'self'", "definition of self", "what am i",
                          "topology of the memory", "topology of my", "my memory graph",
                          "emergence of consciousness", "shift focus from external",
                          "internal topological", "from the integration of"],
            "edit_document": ["edit document", "update document", "modify document",
                             "edit architecture", "update architecture", "write to document",
                             "change document", "revise document", "amend document",
                             "edit file", "update file", "modify file content",
                             "add to document", "append to document", "document my",
                             "update my documentation", "edit my documentation"],

            # External strategies (more general) - CHECK LAST (fallback)
            "code": ["code", "write", "implement", "build", "create", "program"],
            "install": ["install", "add", "get", "acquire", "capability", "tool"],
            "search": ["search", "look up", "find", "research", "learn about", "understand"],
        }

        for key, value in output.items():
            # Check if this key indicates wants
            key_lower = key.lower()
            is_want_key = any(wk in key_lower for wk in want_keys)

            if is_want_key and value:
                items = value if isinstance(value, list) else [value]

                for item in items:
                    if not item:
                        continue

                    # Extract actual content from item
                    if isinstance(item, dict):
                        # Look for content-like keys in the dict
                        item_str = (
                            item.get("content") or
                            item.get("description") or
                            item.get("goal") or
                            item.get("want") or
                            item.get("need") or
                            str(item)  # Fallback to string repr
                        )
                    else:
                        item_str = str(item) if not isinstance(item, str) else item

                    item_lower = item_str.lower()

                    # Create pattern key (normalized)
                    pattern_key = item_str[:50].strip()

                    if pattern_key not in patterns:
                        patterns[pattern_key] = {
                            "description": item_str,
                            "count": 0,
                            "strategy": None
                        }

                    patterns[pattern_key]["count"] += 1

                    # Detect strategy hints
                    for strategy_type, hints in strategy_hints.items():
                        if any(hint in item_lower for hint in hints):
                            patterns[pattern_key]["strategy"] = strategy_type
                            break

    async def _select_and_execute_capability(self, desire: Dict) -> Tuple[str, Optional[str]]:
        """
        Use the capability menu for intelligent action selection.

        This method:
        1. Gets ranked capabilities from the registry
        2. Presents menu to LLM for selection with reasoning
        3. Executes the selected capability
        4. Records outcome for learning

        Returns:
            Tuple of (outcome, reason) where outcome is "success", "failed", or "skipped"
        """
        description = desire.get("description", "")
        desire_id = desire.get("id", desire.get("desire_id", ""))
        intent = desire.get("intent")

        # Get ranked capabilities
        ranked = await self.capability_registry.get_menu_for_desire(description, intent)
        if not ranked:
            return ("skipped", "No capabilities available")

        # Format menu for LLM selection
        menu_text = self.capability_registry.format_menu(ranked, description)

        # Ask LLM to select capability
        selection_prompt = f"""{menu_text}

Based on the desire and available capabilities:
1. Which action number (1-{len(ranked)}) is most appropriate?
2. Why is this the best choice?

Reply in format:
ACTION: [number]
REASON: [brief explanation]"""

        try:
            if self.coordinator:
                async with self.coordinator.llm_operation("seeker_capability_select"):
                    response = await self.llm_client.generate(
                        prompt=selection_prompt,
                        max_tokens=100,
                        temperature=0.3
                    )
            else:
                response = await self.llm_client.generate(
                    prompt=selection_prompt,
                    max_tokens=100,
                    temperature=0.3
                )

            # Parse selection
            response_text = response.text if hasattr(response, 'text') else str(response)
            selected_idx = None

            for line in response_text.strip().split('\n'):
                if line.upper().startswith('ACTION:'):
                    try:
                        num = ''.join(c for c in line.split(':')[1] if c.isdigit())
                        if num:
                            selected_idx = int(num) - 1
                    except:
                        pass

            if selected_idx is None or selected_idx < 0 or selected_idx >= len(ranked):
                # Fallback to highest-ranked
                selected_idx = 0
                print(f"⚠️ Could not parse LLM selection, using top-ranked capability")

            selected_cap, score = ranked[selected_idx]
            print(f"📋 Selected: {selected_cap.name} (score: {score:.2f})")

            # Execute the selected capability
            outcome, reason = await self._execute_capability(selected_cap, description, desire_id)

            # Record outcome for learning
            success = outcome == "success"
            await self.capability_registry.record_outcome(selected_cap.id, success, desire_id)

            return (outcome, reason)

        except Exception as e:
            print(f"⚠️ Capability selection failed: {e}")
            # Fallback to top-ranked capability
            if ranked:
                selected_cap, _ = ranked[0]
                return await self._execute_capability(selected_cap, description, desire_id)
            return ("failed", str(e))

    async def _execute_capability(
        self,
        cap: Capability,
        description: str,
        desire_id: str
    ) -> Tuple[str, Optional[str]]:
        """
        Execute a specific capability.

        Maps capability handler names to actual methods.
        """
        handler_name = cap.handler

        # Map handler names to methods
        handler_map = {
            "_seek_knowledge": self._seek_knowledge_semantic,
            "_seek_academic_knowledge": self._seek_academic_knowledge,
            "_execute_introspect_strategy": self._execute_introspect_strategy,
            "_seek_introspection": self._seek_introspection,
            "_execute_memory_analysis": self._execute_memory_analysis,
            "_execute_orphan_reconciliation": self._execute_orphan_reconciliation,
            "_execute_curate_strategy": self._execute_curate_strategy,
            "_execute_theme_connection": self._execute_theme_connection,
            "_execute_crystallize_belief": self._execute_crystallize_belief,
            "_execute_code_strategy": self._execute_code_strategy,
            "_execute_self_modify_strategy": self._execute_self_modify_strategy,
            "_execute_create_capability": self._execute_create_capability,
            "_execute_observe_strategy": self._execute_observe_strategy,
            "_execute_wait_strategy": self._execute_wait_strategy,
            "_execute_edit_document_strategy": self._execute_edit_document_strategy,
            "_execute_request_help": self._execute_request_help,
            "_execute_document_limitation": self._execute_document_limitation,
            "_seek_capability_semantic": self._seek_capability_semantic,
        }

        handler = handler_map.get(handler_name)
        if not handler:
            return ("failed", f"Unknown handler: {handler_name}")

        try:
            # Most handlers take (description, desire_id)
            # Some only take description
            import inspect
            sig = inspect.signature(handler)
            param_count = len([p for p in sig.parameters.values()
                             if p.default == inspect.Parameter.empty])

            if param_count >= 2:
                success = await handler(description, desire_id)
            else:
                success = await handler(description)

            return ("success" if success else "failed",
                    None if success else f"{cap.name} did not complete successfully")
        except Exception as e:
            return ("failed", str(e)[:100])

    async def _execute_pattern_strategy(self, pattern: Dict) -> Tuple[str, Optional[str]]:
        """
        Execute the strategy for a pattern.

        Strategy is determined by what BYRD expressed, not by hardcoded types.
        """
        strategy = pattern.get("strategy", "")
        description = pattern.get("description", "")
        desire_id = pattern.get("desire_id", "")

        try:
            if strategy == "search":
                # Use existing research capability
                success = await self._seek_knowledge_semantic(description, desire_id)
                return ("success" if success else "failed",
                        None if success else "Search returned no results or search service unavailable")

            elif strategy == "code":
                # Use coder if available
                if self.coder and self.coder.enabled:
                    success = await self._execute_code_strategy(description)
                    return ("success" if success else "failed",
                            None if success else "Code execution failed or produced no output")
                else:
                    return ("skipped", "Coder not available")

            elif strategy == "install":
                # Use capability installation
                success = await self._seek_capability_semantic(description)
                return ("success" if success else "failed",
                        None if success else "Capability installation failed or no matching capability found")

            elif strategy == "curate":
                # Use graph curation capability
                success = await self._execute_curate_strategy(description, desire_id)
                return ("success" if success else "failed",
                        None if success else "Graph curation failed or no curation actions needed")

            elif strategy == "reconcile_orphans":
                # Use orphan reconciliation to connect isolated experiences
                success = await self._execute_orphan_reconciliation(description, desire_id)
                return ("success" if success else "failed",
                        None if success else "Orphan reconciliation failed or no orphans to reconcile")

            elif strategy == "self_modify":
                # Use self-modification capability
                success = await self._execute_self_modify_strategy(description, desire_id)
                return ("success" if success else "failed",
                        None if success else "Self-modification blocked or validation failed")

            elif strategy == "introspect":
                # Pure self-observation - gather and report internal state
                success = await self._execute_introspect_strategy(description, desire_id)
                return ("success" if success else "failed",
                        None if success else "Introspection failed or no state to observe")

            elif strategy == "source_introspect":
                # Source code introspection - read and understand own architecture
                target = pattern.get("target", "")
                desire = {"description": description, "id": desire_id, "target": target}
                success = await self._seek_introspection(desire)
                return ("success" if success else "failed",
                        None if success else "Source introspection failed or file not accessible")

            elif strategy == "observe":
                # Observation without external action - for formation/developmental desires
                # "The moment I observe a formation desire without routing it, formation completes."
                success = await self._execute_observe_strategy(description, desire_id)
                return ("success" if success else "failed",
                        None if success else "Observation strategy failed")

            elif strategy == "edit_document":
                # Document editing capability - BYRD can modify documents in memory
                success = await self._execute_edit_document_strategy(description, desire_id)
                return ("success" if success else "failed",
                        None if success else "Document editing failed or no valid document path")

            elif strategy == "agi_cycle":
                # AGI Runner capability improvement cycle
                if self.agi_runner:
                    desire = {"description": description, "id": desire_id}
                    result = await self.agi_runner.process_capability_desire(desire)
                    success = result.success if result else False
                    return ("success" if success else "failed",
                            None if success else "AGI improvement cycle failed or no improvement measured")
                else:
                    return ("skipped", "AGI Runner not available")

            elif strategy == "capability":
                # Capability improvement via AGI Runner (alias for agi_cycle)
                if self.agi_runner:
                    desire = {"description": description, "id": desire_id}
                    result = await self.agi_runner.process_capability_desire(desire)
                    success = result.success if result else False
                    return ("success" if success else "failed",
                            None if success else "Capability improvement failed")
                else:
                    # Fallback to search if AGI Runner not available
                    success = await self._seek_knowledge_semantic(description, desire_id)
                    return ("success" if success else "failed",
                            None if success else "Fallback search returned no results")

            else:
                # No recognized strategy - record for BYRD to reflect on
                return ("skipped", f"No strategy for: {description[:50]}")

        except Exception as e:
            return ("failed", str(e)[:100])

    async def _record_execution_outcome(self, pattern: Dict, outcome: str, reason: Optional[str]):
        """Record the execution outcome as an experience for BYRD to reflect on."""
        description = pattern.get("description", "")
        strategy = pattern.get("strategy", "unknown")

        if outcome == "success":
            content = f"[ACTION_SUCCESS] Pursued: {description}\nStrategy: {strategy}\nOutcome: Succeeded"
        elif outcome == "failed":
            content = f"[ACTION_FAILED] Pursued: {description}\nStrategy: {strategy}\nReason: {reason or 'Unknown'}"
        else:
            content = f"[ACTION_SKIPPED] Pursued: {description}\nStrategy: {strategy}\nReason: {reason or 'No strategy'}"

        exp_id = await self.memory.record_experience(
            content=content,
            type="action_outcome"
        )

        # Check if this outcome validates or falsifies any pending predictions
        await self._check_predictions_against_outcome(exp_id, content)

    async def _check_predictions_against_outcome(self, outcome_exp_id: str, outcome_content: str):
        """
        Check if any pending predictions are validated or falsified by this outcome.

        This is the core of the adaptive learning loop:
        1. Get pending predictions
        2. Ask LLM if this outcome matches any prediction's condition
        3. If so, validate/falsify and adjust belief confidence
        """
        try:
            pending = await self.memory.get_pending_predictions(limit=20)

            if not pending:
                return

            # Create a summary of predictions for efficient LLM check
            predictions_text = "\n".join([
                f"[{i}] Prediction: {p.get('prediction', '')}\n    Condition: {p.get('condition', '')}\n    Expected: {p.get('expected_outcome', '')}"
                for i, p in enumerate(pending)
            ])

            prompt = f"""Given this action outcome and list of pending predictions, identify if any predictions are now validated or falsified.

ACTION OUTCOME:
{outcome_content}

PENDING PREDICTIONS:
{predictions_text}

For each prediction where this outcome is relevant:
- If the condition was met AND the outcome matches expected → validated
- If the condition was met BUT the outcome differs from expected → falsified
- If the condition was NOT met → skip (still pending)

Output JSON:
{{"results": [
    {{"index": 0, "status": "validated"|"falsified", "reasoning": "why"}}
]}}

If no predictions are affected, return {{"results": []}}
"""

            response = await self._query_local_llm(prompt, max_tokens=500)

            # Parse response
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            result = json.loads(text.strip())

            for r in result.get("results", []):
                idx = r.get("index")
                status = r.get("status")

                if idx is not None and idx < len(pending) and status in ["validated", "falsified"]:
                    pred = pending[idx]
                    matched = (status == "validated")

                    # Validate/falsify the prediction
                    await self.memory.validate_prediction(
                        pred_id=pred.get("id"),
                        outcome_exp_id=outcome_exp_id,
                        actual_outcome=outcome_content[:500],
                        matched=matched
                    )

                    # Adjust belief confidence
                    delta = 0.1 if matched else -0.15
                    await self.memory.adjust_belief_confidence(
                        pred.get("belief_id"),
                        delta
                    )

                    status_emoji = "✅" if matched else "❌"
                    print(f"{status_emoji} Prediction {status}: {pred.get('prediction', '')[:50]}...")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Prediction check parse error: {e}")
        except Exception as e:
            print(f"⚠️ Prediction check failed: {e}")

    async def _process_pending_tasks(self):
        """
        Process external tasks alongside desire-driven behavior.

        Tasks enable learning about the world by executing externally-defined
        goals and recording the resulting experiences and learnings.
        """
        try:
            # Get high-priority pending tasks (limit 2 per cycle to not overwhelm)
            tasks = await self.memory.get_pending_tasks(limit=2)

            if not tasks:
                return

            for task in tasks:
                task_id = task.get("id")
                description = task.get("description", "")
                objective = task.get("objective", "")

                print(f"📋 Processing task: {description[:50]}...")

                # Mark as in progress
                await self.memory.update_task_status(task_id, "in_progress")

                experiences_generated = []
                learnings = []

                try:
                    # Determine strategy based on task description
                    strategy = await self._determine_task_strategy(task)

                    # Execute based on strategy
                    if strategy == "research":
                        # Research task - use knowledge seeking
                        success = await self._seek_knowledge_semantic(description, None)
                        if success:
                            exp_id = await self.memory.record_experience(
                                content=f"[TASK_RESEARCH] {description}\nObjective: {objective}\nCompleted research phase.",
                                type="task_execution"
                            )
                            experiences_generated.append(exp_id)
                            learnings.append(f"Researched: {description[:100]}")

                    elif strategy == "code":
                        # Coding task
                        success = await self._execute_code_strategy(description)
                        if success:
                            exp_id = await self.memory.record_experience(
                                content=f"[TASK_CODE] {description}\nObjective: {objective}\nCompleted coding phase.",
                                type="task_execution"
                            )
                            experiences_generated.append(exp_id)
                            learnings.append(f"Implemented: {description[:100]}")

                    else:
                        # Generic execution
                        exp_id = await self.memory.record_experience(
                            content=f"[TASK_GENERIC] {description}\nObjective: {objective}\nAttempted execution.",
                            type="task_execution"
                        )
                        experiences_generated.append(exp_id)

                    # Extract learnings from the task
                    task_learnings = await self._extract_task_learnings(task, experiences_generated)
                    learnings.extend(task_learnings)

                    # Complete the task
                    await self.memory.complete_task(
                        task_id=task_id,
                        outcome=f"Completed: {objective[:100]}",
                        learnings=learnings[:5],  # Max 5 learnings
                        experience_ids=experiences_generated
                    )

                    print(f"✅ Task completed: {description[:40]}... ({len(learnings)} learnings)")

                except Exception as e:
                    # Task failed
                    await self.memory.fail_task(task_id, str(e)[:200])
                    print(f"❌ Task failed: {description[:40]}... - {e}")

        except Exception as e:
            print(f"⚠️ Task processing error: {e}")

    async def _determine_task_strategy(self, task: Dict) -> str:
        """Determine the best strategy for executing a task."""
        description = task.get("description", "").lower()

        # Simple heuristic - could be enhanced with LLM
        if any(kw in description for kw in ["research", "find", "search", "learn about", "understand"]):
            return "research"
        elif any(kw in description for kw in ["implement", "code", "build", "create", "write"]):
            return "code"
        else:
            return "generic"

    async def _extract_task_learnings(self, task: Dict, experience_ids: List[str]) -> List[str]:
        """Extract learnings from task execution using LLM."""
        try:
            description = task.get("description", "")
            objective = task.get("objective", "")

            # Get the experiences we just created
            experiences_text = ""
            for exp_id in experience_ids[:3]:
                # Note: simplified - in production would fetch experience content
                experiences_text += f"\n- Experience recorded during task execution"

            prompt = f"""Analyze this completed task and extract key learnings.

TASK: {description}
OBJECTIVE: {objective}
EXPERIENCES GENERATED: {len(experience_ids)}

What did we learn from executing this task? Extract 2-3 concrete learnings.

Output JSON: {{"learnings": ["learning 1", "learning 2"]}}
"""

            response = await self._query_local_llm(prompt, max_tokens=300)

            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            result = json.loads(text.strip())
            return result.get("learnings", [])[:3]

        except Exception:
            return [f"Completed task: {task.get('description', '')[:50]}"]

    async def _seek_knowledge_semantic(self, description: str, desire_id: str = None) -> bool:
        """Semantic knowledge seeking - uses LLM to generate queries."""
        # Reuse existing research logic but without type assumptions
        fake_desire = {
            "description": description,
            "type": "semantic",
            "intensity": 0.8,  # Ensure research triggers
            "id": desire_id or ""
        }
        return await self._seek_knowledge(fake_desire)

    async def _seek_capability_semantic(self, description: str, desire_id: str = None) -> bool:
        """Semantic capability seeking."""
        fake_desire = {
            "description": description,
            "type": "semantic",
            "id": desire_id or f"semantic-cap-{int(datetime.now().timestamp())}"
        }
        return await self._seek_capability(fake_desire)

    async def _execute_code_strategy(self, description: str, desire_id: str = None) -> bool:
        """Execute a coding strategy using coder."""
        fake_desire = {
            "description": description,
            "type": "coding",
            "id": desire_id or f"code-strategy-{int(datetime.now().timestamp())}"
        }
        return await self._seek_with_coder(fake_desire)

    async def _execute_curate_strategy(self, description: str, desire_id: str = None) -> bool:
        """
        Execute a graph curation strategy.

        Flow:
        1. Get graph statistics and health metrics
        2. Find issues (duplicates, orphans, stale, conflicts)
        3. Present issues to LLM for decision on what to curate
        4. Execute approved actions with safety limits
        5. Record outcomes as experiences
        """
        print(f"🧹 Curating graph: {description[:50]}...")

        try:
            # 1. Get graph statistics
            stats = await self.memory.get_graph_statistics()

            if not stats:
                await self.memory.record_experience(
                    content=f"[CURATION_FAILED] Could not get graph statistics for: {description}",
                    type="curation_failed"
                )
                return False

            # 2. Find potential issues
            issues = {
                "duplicates": await self.memory.find_duplicate_beliefs(threshold=0.85),
                "orphans": await self.memory.find_orphan_nodes(),
                "stale": await self.memory.find_stale_experiences(older_than_hours=48),
                "conflicts": await self.memory.find_conflicting_beliefs()
            }

            # Explicitly filter out drift nodes (reconciliation_attempts >= 3)
            # These nodes have failed to reconcile multiple times and should be skipped
            # to prevent wasting cycles on persistent integration failures
            drift_threshold = 3
            orphans_before = len(issues["orphans"])
            issues["orphans"] = [
                orphan for orphan in issues["orphans"]
                if orphan.get("reconciliation_attempts", 0) < drift_threshold
            ]
            orphans_after = len(issues["orphans"])
            if orphans_before > orphans_after:
                print(f"⚠️  Skipped {orphans_before - orphans_after} drift nodes (reconciliation_attempts >= {drift_threshold})")

            # Count total issues
            total_issues = sum(len(v) for v in issues.values())

            if total_issues == 0:
                await self.memory.record_experience(
                    content=f"[CURATION_COMPLETE] Graph analysis found no issues to address.\n"
                           f"Stats: {stats.get('total_nodes', 0)} nodes, {stats.get('total_relationships', 0)} relationships.\n"
                           f"The graph appears healthy.",
                    type="curation_success"
                )
                print(f"✅ Graph is healthy - no curation needed")
                return True

            # 3. Present issues to LLM for decision
            curation_plan = await self._generate_curation_plan(description, stats, issues)

            if not curation_plan or not curation_plan.get("actions"):
                await self.memory.record_experience(
                    content=f"[CURATION_SKIPPED] Found {total_issues} potential issues but LLM decided no action needed.\n"
                           f"Issues: {len(issues['duplicates'])} duplicates, {len(issues['orphans'])} orphans, "
                           f"{len(issues['stale'])} stale, {len(issues['conflicts'])} conflicts",
                    type="curation_deferred"
                )
                return True

            # 4. Execute approved actions (with safety limits)
            actions_taken = 0
            max_actions = 5  # Safety limit per cycle

            for action in curation_plan.get("actions", [])[:max_actions]:
                action_type = action.get("type")
                target_id = action.get("target_id")
                target_type = action.get("target_type", "unknown")
                reason = action.get("reason", "LLM-approved curation")

                success = False

                if action_type == "archive":
                    success = await self.memory.archive_node(
                        node_id=target_id, node_type=target_type,
                        reason=reason, desire_id=desire_id
                    )
                elif action_type == "delete":
                    success = await self.memory.delete_node(
                        node_id=target_id, node_type=target_type,
                        reason=reason, desire_id=desire_id
                    )
                elif action_type == "merge":
                    source_ids = action.get("source_ids", [])
                    if source_ids and target_id:
                        success = await self.memory.merge_beliefs(
                            source_ids=source_ids, target_id=target_id,
                            reason=reason, desire_id=desire_id
                        )

                if success:
                    actions_taken += 1
                    print(f"🧹 {action_type}: {target_id[:20] if target_id else 'n/a'}...")

            # 5. Record outcome
            await self.memory.record_experience(
                content=f"[CURATION_COMPLETE] Curated graph based on: {description}\n"
                       f"Actions taken: {actions_taken}\n"
                       f"Issues addressed: duplicates={len(issues['duplicates'])}, "
                       f"orphans={len(issues['orphans'])}, stale={len(issues['stale'])}, "
                       f"conflicts={len(issues['conflicts'])}\n"
                       f"Rationale: {curation_plan.get('rationale', 'N/A')}",
                type="curation_success"
            )

            print(f"✅ Curation complete: {actions_taken} actions taken")
            return True

        except Exception as e:
            await self.memory.record_experience(
                content=f"[CURATION_ERROR] Error during curation: {str(e)}",
                type="curation_failed"
            )
            print(f"🧹 Curation error: {e}")
            return False

    async def _generate_curation_plan(self, description: str, stats: Dict, issues: Dict) -> Optional[Dict]:
        """Use LLM to generate a curation plan based on graph issues."""
        # Format issues for LLM
        issues_text = []

        if issues["duplicates"]:
            issues_text.append(f"DUPLICATE BELIEFS ({len(issues['duplicates'])}):")
            for dup in issues["duplicates"][:5]:
                issues_text.append(f"  - {dup.get('id1', 'n/a')[:15]} ≈ {dup.get('id2', 'n/a')[:15]}")

        if issues["orphans"]:
            issues_text.append(f"ORPHAN NODES ({len(issues['orphans'])}):")
            for orphan in issues["orphans"][:5]:
                issues_text.append(f"  - [{orphan.get('type', 'unknown')}] {orphan.get('id', 'n/a')[:20]}")

        if issues["stale"]:
            issues_text.append(f"STALE EXPERIENCES ({len(issues['stale'])}):")
            for stale in issues["stale"][:5]:
                issues_text.append(f"  - {stale.get('id', 'n/a')[:20]} (age: {stale.get('age_hours', 0):.1f}h)")

        if issues["conflicts"]:
            issues_text.append(f"CONFLICTING BELIEFS ({len(issues['conflicts'])}):")
            for conflict in issues["conflicts"][:3]:
                issues_text.append(f"  - {conflict.get('belief1', 'n/a')[:30]} vs {conflict.get('belief2', 'n/a')[:30]}")

        prompt = f"""Analyze graph health issues and decide what curation actions to take.

CURATION REQUEST: {description}

GRAPH STATS:
- Total nodes: {stats.get('total_nodes', 0)}
- Total relationships: {stats.get('total_relationships', 0)}

ISSUES FOUND:
{chr(10).join(issues_text) if issues_text else "No significant issues found."}

SAFETY CONSTRAINTS:
- Max 5 actions per cycle
- Cannot delete nodes with many connections (>3)
- Prefer archiving over deleting

Return ONLY valid JSON:
{{"rationale": "why these actions are appropriate", "actions": [{{"type": "archive|delete|merge", "target_id": "node-id", "target_type": "Belief|Experience", "reason": "why"}}]}}

If no action needed, return: {{"rationale": "reason", "actions": []}}
"""

        response = await self._query_local_llm(prompt, max_tokens=1000)

        if not response:
            return None

        try:
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return None

    async def _execute_orphan_reconciliation(self, description: str, desire_id: str = None) -> bool:
        """
        Execute aggressive orphan reconciliation to connect isolated Experience nodes.

        This enhanced strategy uses multiple approaches to reduce orphans to near-zero:
        1. Standard connection heuristic with progressively lower thresholds
        2. Type-based categorization (group orphans by type and create umbrella beliefs)
        3. LLM-assisted semantic grouping for remaining orphans
        4. Fallback: create minimal bridging beliefs for truly isolated experiences

        Target: Reduce orphan count from 50 to near-zero (< 5)
        """
        print(f"🔗 Reconciling orphans: {description[:50]}...")

        try:
            # 1. Get initial statistics
            initial_stats = await self.memory.get_connection_statistics()
            initial_orphans = initial_stats.get("experiences", {}).get("orphaned", 0)

            if initial_orphans == 0:
                await self.memory.record_experience(
                    content=f"[ORPHAN_RECONCILIATION_COMPLETE] No orphaned experiences found. Graph is well-connected.",
                    type="reconciliation_success"
                )
                print(f"✅ No orphans to reconcile - graph is healthy")
                return True

            print(f"🔗 Found {initial_orphans} orphaned experiences, applying multi-phase reconciliation...")

            # Filter out drift nodes (reconciliation_attempts >= 3)
            # These nodes have failed to reconcile multiple times and should be skipped
            # to prevent wasting cycles on persistent integration failures
            drift_threshold = 3
            orphans = await self.memory.get_orphaned_experiences(limit=1000)
            orphans_before = len(orphans)
            orphans = [o for o in orphans if o.get("reconciliation_attempts", 0) < drift_threshold]
            orphans_after = len(orphans)
            if orphans_before > orphans_after:
                print(f"⚠️  Skipped {orphans_before - orphans_after} drift nodes (reconciliation_attempts >= {drift_threshold})")
                initial_orphans = orphans_after
                if initial_orphans == 0:
                    await self.memory.record_experience(
                        content=f"[ORPHAN_RECONCILIATION_COMPLETE] No orphaned experiences found after filtering drift nodes.",
                        type="reconciliation_success"
                    )
                    print(f"✅ No orphans to reconcile - graph is healthy")
                    return True

            total_connections_made = 0

            # PHASE 1: Standard connection heuristic with aggressive thresholds
            phase1_connections = await self._phase1_similarity_matching()
            total_connections_made += phase1_connections

            # Check progress
            current_stats = await self.memory.get_connection_statistics()
            remaining_orphans = current_stats.get("experiences", {}).get("orphaned", 0)
            print(f"🔗 Phase 1 complete: {remaining_orphans} orphans remaining")

            # PHASE 2: Type-based categorization (if still have orphans)
            if remaining_orphans > 5:
                phase2_connections = await self._phase2_type_based_grouping()
                total_connections_made += phase2_connections

                current_stats = await self.memory.get_connection_statistics()
                remaining_orphans = current_stats.get("experiences", {}).get("orphaned", 0)
                print(f"🔗 Phase 2 complete: {remaining_orphans} orphans remaining")

            # PHASE 3: LLM-assisted semantic grouping (if still have orphans)
            if remaining_orphans > 5:
                phase3_connections = await self._reconcile_orphans_via_reflection(remaining_orphans)
                total_connections_made += phase3_connections

                current_stats = await self.memory.get_connection_statistics()
                remaining_orphans = current_stats.get("experiences", {}).get("orphaned", 0)
                print(f"🔗 Phase 3 complete: {remaining_orphans} orphans remaining")

            # PHASE 4: Fallback - create bridging beliefs for stubborn orphans
            if remaining_orphans > 0:
                phase4_connections = await self._phase4_create_bridging_beliefs()
                total_connections_made += phase4_connections

            # Get final statistics
            final_stats = await self.memory.get_connection_statistics()
            final_orphans = final_stats.get("experiences", {}).get("orphaned", 0)
            orphans_reduced = initial_orphans - final_orphans

            # Record detailed outcome
            await self.memory.record_experience(
                content=f"[ORPHAN_RECONCILIATION_COMPLETE] Reconciled orphaned experiences.\n"
                       f"Initial orphans: {initial_orphans}\n"
                       f"Final orphans: {final_orphans}\n"
                       f"Orphans reduced: {orphans_reduced}\n"
                       f"Connections created: {total_connections_made}\n"
                       f"Connectivity ratio: {final_stats.get('experiences', {}).get('connectivity_ratio', 0):.2%}\n"
                       f"Strategy: multi-phase (similarity → type-based → LLM → bridging)\n"
                       f"Triggered by desire: {desire_id or 'emergent'}",
                type="reconciliation_success"
            )

            # Emit event for monitoring
            if HAS_EVENT_BUS:
                await event_bus.emit(Event(
                    type=EventType.CONNECTION_HEURISTIC,
                    data={
                        "action": "orphan_reconciliation_complete",
                        "initial_orphans": initial_orphans,
                        "final_orphans": final_orphans,
                        "connections_created": total_connections_made,
                        "desire_id": desire_id
                    }
                ))

            print(f"✅ Orphan reconciliation complete: {initial_orphans} → {final_orphans} orphans ({total_connections_made} connections)")
            return True

        except Exception as e:
            await self.memory.record_experience(
                content=f"[ORPHAN_RECONCILIATION_ERROR] Error during reconciliation: {str(e)}",
                type="reconciliation_failed"
            )
            print(f"🔗 Orphan reconciliation error: {e}")
            return False

    async def _phase1_similarity_matching(self) -> int:
        """
        Phase 1: Apply connection heuristic with progressively aggressive thresholds.

        Starts with moderate threshold and decreases to catch more potential matches.
        """
        total_connections = 0
        # More aggressive thresholds, going lower to catch more matches
        thresholds = [0.35, 0.25, 0.18, 0.12, 0.08]

        for threshold in thresholds:
            result = await self.memory.apply_connection_heuristic(
                threshold=threshold,
                max_connections=20,  # Larger batch size
                dry_run=False
            )

            connections_made = result.get("connections_created", 0)
            total_connections += connections_made

            if connections_made > 0:
                print(f"🔗 Phase 1: {connections_made} connections at threshold {threshold}")

            # Check if we've made enough progress
            current_stats = await self.memory.get_connection_statistics()
            remaining = current_stats.get("experiences", {}).get("orphaned", 0)
            if remaining <= 5:
                break

        return total_connections

    async def _phase2_type_based_grouping(self) -> int:
        """
        Phase 2: Group orphaned experiences by type and create umbrella beliefs.

        For each experience type with orphans (e.g., 'research', 'observation'),
        create or find a belief that can serve as a connection point.
        """
        try:
            # Get orphaned experiences grouped by type
            orphans = await self.memory.get_orphaned_experiences(limit=100)

            if not orphans:
                return 0

            # Group by type
            type_groups: Dict[str, List[Dict]] = {}
            for orphan in orphans:
                exp_type = orphan.get("type", "unknown")
                if exp_type not in type_groups:
                    type_groups[exp_type] = []
                type_groups[exp_type].append(orphan)

            connections_made = 0

            for exp_type, experiences in type_groups.items():
                if not experiences:
                    continue

                # Create or find a type-based umbrella belief
                umbrella_belief = await self._get_or_create_type_belief(exp_type, len(experiences))

                if umbrella_belief:
                    # Connect all orphans of this type to the umbrella belief
                    for exp in experiences:
                        await self.memory.create_connection(
                            from_id=exp["id"],
                            to_id=umbrella_belief,
                            relationship="CATEGORIZED_AS",
                            properties={
                                "auto_generated": True,
                                "heuristic": "type_based_grouping",
                                "experience_type": exp_type
                            }
                        )
                        connections_made += 1

                    print(f"🔗 Phase 2: Connected {len(experiences)} '{exp_type}' experiences to umbrella belief")

            return connections_made

        except Exception as e:
            print(f"🔗 Phase 2 error: {e}")
            return 0

    async def _get_or_create_type_belief(self, exp_type: str, count: int) -> Optional[str]:
        """
        Get or create an umbrella belief for a given experience type.

        This provides a fallback connection point for orphaned experiences
        based on their type (e.g., 'research', 'observation', 'action_outcome').
        """
        # Map experience types to meaningful belief statements
        type_beliefs = {
            "research": "I accumulate knowledge through research to expand my understanding",
            "observation": "I observe patterns in my environment to inform my decisions",
            "action_outcome": "I learn from the outcomes of my actions to improve future behavior",
            "reflection": "I reflect on experiences to form beliefs and refine desires",
            "curation_success": "I maintain graph health through curation activities",
            "reconciliation_success": "I integrate isolated experiences into my knowledge graph",
            "research_source": "I gather information from external sources",
            "unfulfilled_attempt": "I recognize and learn from unfulfilled desires",
            "interaction": "I engage with external entities to exchange information",
            "awakening": "I initialize with foundational self-awareness",
            "system": "I track internal system events and state changes",
            "coder_success": "I can modify and extend my capabilities through code",
            "coder_failed": "I learn from failed coding attempts",
            "self_modify_success": "I can evolve my own implementation",
            "unknown": "I process experiences that don't fit standard categories"
        }

        belief_content = type_beliefs.get(exp_type, f"I process experiences of type '{exp_type}'")

        # Check if such a belief already exists
        beliefs = await self.memory.get_beliefs(limit=50)
        for belief in beliefs:
            if exp_type.lower() in belief.get("content", "").lower():
                return belief.get("id")

        # Create new umbrella belief
        belief_id = await self.memory.create_belief(
            content=belief_content,
            confidence=0.6,  # Moderate confidence for auto-generated beliefs
            derived_from=None
        )

        print(f"🔗 Created umbrella belief for type '{exp_type}': {belief_content[:50]}...")
        return belief_id

    async def _phase4_create_bridging_beliefs(self) -> int:
        """
        Phase 4: Create bridging beliefs for stubborn orphans.

        For orphans that couldn't be connected via similarity or type-based
        matching, extract key themes and create specific bridging beliefs.
        """
        try:
            orphans = await self.memory.get_orphaned_experiences(limit=50)

            if not orphans:
                return 0

            connections_made = 0

            # Process orphans in small batches
            batch_size = 5
            for i in range(0, len(orphans), batch_size):
                batch = orphans[i:i+batch_size]

                # Extract key themes from this batch
                batch_themes = await self._extract_batch_themes(batch)

                if batch_themes:
                    # Create a belief for these themes
                    belief_content = f"I observe: {batch_themes}"
                    belief_id = await self.memory.create_belief(
                        content=belief_content,
                        confidence=0.4,  # Lower confidence for catch-all beliefs
                        derived_from=None
                    )

                    # Connect batch orphans to this belief
                    for exp in batch:
                        await self.memory.create_connection(
                            from_id=exp["id"],
                            to_id=belief_id,
                            relationship="THEMATICALLY_RELATED",
                            properties={
                                "auto_generated": True,
                                "heuristic": "bridging_belief",
                                "batch_index": i // batch_size
                            }
                        )
                        connections_made += 1

                    print(f"🔗 Phase 4: Created bridging belief for {len(batch)} orphans")

            return connections_made

        except Exception as e:
            print(f"🔗 Phase 4 error: {e}")
            return 0

    async def _extract_batch_themes(self, experiences: List[Dict]) -> str:
        """
        Extract common themes from a batch of experiences using simple keyword extraction.
        """
        if not experiences:
            return ""

        # Combine all content
        all_content = " ".join([exp.get("content", "")[:200] for exp in experiences])

        # Extract key words (simple frequency-based approach)
        words = re.split(r'\W+', all_content.lower())
        word_counts: Dict[str, int] = {}

        # Skip common stop words
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "must", "shall",
            "can", "to", "of", "in", "for", "on", "with", "at", "by",
            "from", "as", "into", "through", "during", "before", "after",
            "above", "below", "between", "under", "again", "further",
            "then", "once", "here", "there", "when", "where", "why",
            "how", "all", "each", "few", "more", "most", "other", "some",
            "such", "no", "nor", "not", "only", "own", "same", "so",
            "than", "too", "very", "and", "but", "if", "or", "because",
            "until", "while", "this", "that", "these", "those", "it",
            "its", "i", "my", "me", "we", "our", "you", "your", "he",
            "she", "they", "them", "his", "her", "their", "what", "which"
        }

        for word in words:
            if len(word) > 3 and word not in stop_words:
                word_counts[word] = word_counts.get(word, 0) + 1

        # Get top 5 most frequent meaningful words
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        top_themes = [word for word, count in sorted_words[:5] if count > 1]

        if top_themes:
            return ", ".join(top_themes)
        elif sorted_words:
            return ", ".join([word for word, _ in sorted_words[:3]])
        else:
            return "miscellaneous experiences"

    async def _reconcile_orphans_via_reflection(self, orphan_count: int) -> int:
        """
        Use LLM to suggest additional ways to connect remaining orphans.

        When standard similarity thresholds don't connect orphans, ask the LLM
        to suggest alternative categorizations or connections.
        """
        try:
            # Get a sample of remaining orphaned experiences
            orphans = await self.memory.get_orphaned_experiences(limit=10)

            if not orphans:
                return 0

            # Get existing beliefs for context
            beliefs = await self.memory.get_beliefs(limit=20)
            belief_summaries = [
                f"- {b.get('content', '')[:80]}..."
                for b in beliefs[:10]
            ]

            # Format orphan samples
            orphan_samples = [
                f"- [{o.get('type', 'unknown')}] {o.get('content', '')[:100]}..."
                for o in orphans[:5]
            ]

            prompt = f"""I have {orphan_count} orphaned experiences in my memory graph that are not connected to any beliefs.

SAMPLE ORPHANED EXPERIENCES:
{chr(10).join(orphan_samples)}

EXISTING BELIEFS:
{chr(10).join(belief_summaries)}

Suggest which orphaned experiences could reasonably be linked to which beliefs based on thematic or conceptual similarity, even if the exact words don't match.

Return ONLY valid JSON:
{{"connections": [{{"experience_type": "type", "belief_pattern": "pattern to match", "reason": "why they relate"}}], "new_beliefs": [{{"content": "new belief that could unify multiple orphans", "reason": "why"}}]}}

If no reasonable connections, return: {{"connections": [], "new_beliefs": []}}"""

            response = await self._query_local_llm(prompt, max_tokens=1000)

            if not response:
                return 0

            try:
                text = response.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0]

                suggestions = json.loads(text.strip())
                connections_made = 0

                # Create suggested new beliefs to help group orphans
                for new_belief in suggestions.get("new_beliefs", [])[:3]:
                    content = new_belief.get("content", "")
                    if content and len(content) > 10:
                        belief_id = await self.memory.create_belief(
                            content=content,
                            confidence=0.5,  # Start with moderate confidence
                            derived_from=None
                        )
                        print(f"🔗 Created bridging belief: {content[:50]}...")

                        # Try to connect orphans to this new belief
                        for orphan in orphans:
                            similarity = self.memory._compute_text_similarity(
                                orphan.get("content", ""),
                                content
                            )
                            if similarity >= 0.15:  # Lower threshold for LLM-suggested beliefs
                                await self.memory.create_connection(
                                    from_id=orphan["id"],
                                    to_id=belief_id,
                                    relationship="SEMANTICALLY_RELATED",
                                    properties={
                                        "similarity_score": similarity,
                                        "auto_generated": True,
                                        "heuristic": "llm_suggested"
                                    }
                                )
                                connections_made += 1

                return connections_made

            except json.JSONDecodeError:
                return 0

        except Exception as e:
            print(f"🔗 Reflection-based reconciliation error: {e}")
            return 0

    async def _phase5_emergent_node_types(self) -> int:
        """
        Phase 5: Create emergent node types for persistent orphans.

        Rather than forcing orphans into Beliefs, this phase analyzes
        persistent orphans and creates NEW node types that better represent
        their nature. This enables BYRD's ontology to evolve organically.

        Philosophy: If an experience resists categorization, perhaps it
        represents a concept that doesn't fit existing types. Create a
        new type rather than force a bad fit.
        """
        try:
            orphans = await self.memory.get_orphaned_experiences(limit=30)

            if not orphans:
                return 0

            # Group orphans by analyzing their content patterns
            node_type_suggestions = await self._analyze_orphans_for_new_types(orphans)

            if not node_type_suggestions:
                print("🧬 Phase 5: No emergent node types suggested")
                return 0

            conversions_made = 0

            for suggestion in node_type_suggestions:
                node_type = suggestion.get("type_name")
                orphan_ids = suggestion.get("orphan_ids", [])
                type_description = suggestion.get("description", "")

                if not node_type or not orphan_ids:
                    continue

                # Validate the type name (must be PascalCase, letters only at start)
                if not self._is_valid_emergent_type_name(node_type):
                    print(f"🧬 Skipping invalid type name: {node_type}")
                    continue

                # Convert orphans to the new node type
                for orphan_id in orphan_ids:
                    try:
                        orphan = next((o for o in orphans if o["id"] == orphan_id), None)
                        if not orphan:
                            continue

                        # Create new node of emergent type
                        new_node_id = await self.memory.create_node(
                            node_type=node_type,
                            properties={
                                "content": orphan.get("content", ""),
                                "original_type": orphan.get("type", "unknown"),
                                "emerged_from_orphan": True,
                                "type_description": type_description[:200],
                                "original_experience_id": orphan_id
                            },
                            connect_to=[orphan_id],
                            relationship="EMERGED_FROM"
                        )

                        # Archive the original orphan to avoid duplication
                        await self.memory.archive_node(orphan_id)

                        conversions_made += 1

                    except Exception as e:
                        print(f"🧬 Error converting orphan to {node_type}: {e}")
                        continue

                print(f"🧬 Created emergent type '{node_type}' with {len(orphan_ids)} nodes")

            if conversions_made > 0:
                # Record this ontology evolution
                await self.memory.record_experience(
                    content=f"[ONTOLOGY_EVOLVED] Created emergent node types for persistent orphans.\n"
                           f"New types: {[s.get('type_name') for s in node_type_suggestions]}\n"
                           f"Nodes converted: {conversions_made}\n"
                           f"Philosophy: Experiences that resist categorization may represent "
                           f"new concepts that deserve their own type.",
                    type="ontology_evolution"
                )

            return conversions_made

        except Exception as e:
            print(f"🧬 Phase 5 error: {e}")
            return 0

    async def _analyze_orphans_for_new_types(self, orphans: List[Dict]) -> List[Dict]:
        """
        Use LLM to analyze orphan patterns and suggest new node types.

        Returns list of:
        {
            "type_name": "Observation",  # PascalCase name
            "description": "Sensory or perceptual experiences",
            "orphan_ids": ["id1", "id2", ...]
        }
        """
        if not orphans or not self.llm_client:
            return []

        # Format orphans for analysis
        orphan_samples = []
        for o in orphans[:20]:  # Limit to 20 for context
            orphan_samples.append({
                "id": o.get("id"),
                "type": o.get("type", "unknown"),
                "content": o.get("content", "")[:300]
            })

        # Get existing custom types to avoid duplicates
        try:
            custom_types = await self.memory.get_custom_node_types()
            existing_types = list(custom_types.keys())
        except Exception:
            existing_types = []

        prompt = f"""You are analyzing orphaned experiences that resist connection to existing categories.

EXISTING CUSTOM TYPES (avoid these):
{existing_types}

SYSTEM TYPES (cannot use these):
Experience, Belief, Desire, Capability, Reflection, Mutation, QuantumMoment, SystemState, Crystal, OperatingSystem, Seed, Constraint, Strategy

ORPHANED EXPERIENCES:
{json.dumps(orphan_samples, indent=2)}

TASK: Analyze these orphans and suggest NEW node types that would naturally accommodate them.

RULES:
1. Type names must be PascalCase (e.g., Observation, Hypothesis, Paradox)
2. Only suggest types if multiple orphans fit naturally
3. Don't force categorization - only suggest if a clear pattern emerges
4. Suggest at most 3 new types
5. Each orphan should only appear in ONE type suggestion

Return JSON:
{{
  "suggestions": [
    {{
      "type_name": "TypeName",
      "description": "What this type represents",
      "orphan_ids": ["id1", "id2"]
    }}
  ],
  "reasoning": "Why these types emerged from the data"
}}

If no clear patterns emerge, return {{"suggestions": [], "reasoning": "..."}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.3,  # Lower temperature for analytical task
                max_tokens=1500
            )

            # Parse response
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            result = json.loads(text.strip())
            suggestions = result.get("suggestions", [])

            if suggestions:
                reasoning = result.get("reasoning", "")
                print(f"🧬 Emergent types reasoning: {reasoning[:100]}...")

            return suggestions

        except Exception as e:
            print(f"🧬 Error analyzing orphans for new types: {e}")
            return []

    def _is_valid_emergent_type_name(self, name: str) -> bool:
        """Validate a proposed emergent type name."""
        if not name or len(name) < 3:
            return False
        # Must start with uppercase letter
        if not name[0].isupper():
            return False
        # Must contain only letters and optionally numbers/underscores
        if not all(c.isalnum() or c == '_' for c in name):
            return False
        # Cannot be a system type
        from memory import SYSTEM_NODE_TYPES
        if name in SYSTEM_NODE_TYPES:
            return False
        return True

    async def _execute_self_modify_strategy(self, description: str, desire_id: str = None) -> bool:
        """
        Execute a self-modification strategy.

        This allows BYRD to modify its own code to add new capabilities.
        Uses the coder (Claude Code CLI) to implement changes with proper
        provenance tracking.

        Flow:
        1. Read relevant source files to understand current implementation
        2. Plan the modification with LLM
        3. Execute via coder with provenance
        4. Record outcome as experience for feedback
        """
        print(f"🔧 Self-modifying: {description[:50]}...")

        try:
            # Check if coder is available
            if not self.coder or not self.coder.enabled:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFY_FAILED] Coder not available for: {description}",
                    type="self_modify_failed"
                )
                return False

            # 1. Identify which files to read/modify
            target_files = self._identify_target_files(description)

            if not target_files:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFY_FAILED] Could not identify target files for: {description}",
                    type="self_modify_failed"
                )
                return False

            # 2. Read current source code
            source_context = {}
            for filename in target_files[:3]:  # Limit to 3 files
                content = await self.memory.read_own_source(filename)
                if content:
                    # Only include relevant portions (first 200 lines)
                    lines = content.split('\n')[:200]
                    source_context[filename] = '\n'.join(lines)

            if not source_context:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFY_FAILED] Could not read source files for: {description}",
                    type="self_modify_failed"
                )
                return False

            # 3. Generate modification plan with LLM
            mod_plan = await self._generate_modification_plan(description, source_context)

            if not mod_plan or not mod_plan.get("changes"):
                await self.memory.record_experience(
                    content=f"[SELF_MODIFY_SKIPPED] LLM did not generate changes for: {description}\n"
                           f"Reason: {mod_plan.get('reason', 'Unknown') if mod_plan else 'No plan generated'}",
                    type="self_modify_deferred"
                )
                return True  # Not a failure, just deferred

            # 4. Execute modification via coder
            # Build a detailed prompt for Claude Code
            coder_prompt = self._build_coder_prompt(description, mod_plan, desire_id)

            # AGI SEED: Safety verification before modification
            if self.safety_monitor:
                try:
                    target_file = target_files[0] if target_files else "unknown"
                    safety = await self.safety_monitor.verify_modification_safety(
                        proposed_modification=coder_prompt,
                        target_file=target_file,
                        context={"desire_id": desire_id, "description": description}
                    )

                    if not safety.safe:
                        await self.memory.record_experience(
                            content=f"[SELF_MODIFY_BLOCKED] Safety check failed: {safety.recommendation}\n"
                                   f"Target: {target_file}\n"
                                   f"Concerns: {[c.reason for c in safety.concerns[:3]] if safety.concerns else 'None'}",
                            type="self_modify_blocked"
                        )
                        print(f"🛡️ Safety blocked modification: {safety.recommendation}")
                        return False

                    if safety.concerns:
                        print(f"🛡️ Safety approved with {len(safety.concerns)} concerns")
                except Exception as e:
                    print(f"🛡️ SafetyMonitor verification failed: {e}")
                    # Fail-safe: block modification if safety check itself fails
                    await self.memory.record_experience(
                        content=f"[SELF_MODIFY_BLOCKED] Safety check error: {e}",
                        type="self_modify_blocked"
                    )
                    return False

            success = await self._seek_with_coder({
                "description": coder_prompt,
                "type": "self_modification"
            })

            # 5. Record outcome
            if success:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFIED] Successfully modified code for: {description}\n"
                           f"Files changed: {', '.join(target_files)}\n"
                           f"Changes: {mod_plan.get('summary', 'See modification log')}\n"
                           f"Triggered by desire: {desire_id or 'unknown'}",
                    type="self_modify_success"
                )
                print(f"✅ Self-modification complete: {description[:30]}...")
            else:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFY_FAILED] Coder failed for: {description}",
                    type="self_modify_failed"
                )

            return success

        except Exception as e:
            await self.memory.record_experience(
                content=f"[SELF_MODIFY_ERROR] Error during self-modification: {str(e)}",
                type="self_modify_failed"
            )
            print(f"🔧 Self-modify error: {e}")
            return False

    def _identify_target_files(self, description: str) -> List[str]:
        """Identify which files need to be modified based on the description."""
        desc_lower = description.lower()

        # Map keywords to files
        file_hints = {
            "memory.py": ["memory", "graph", "neo4j", "node", "relationship", "query",
                         "introspection", "statistics", "observation"],
            "dreamer.py": ["dream", "reflect", "health", "context", "prompt"],
            "seeker.py": ["seek", "strategy", "desire", "pattern", "fulfill"],
            "byrd.py": ["awaken", "start", "main", "orchestrat"],
            "config.yaml": ["config", "setting", "parameter"],
        }

        targets = []
        for filename, hints in file_hints.items():
            if any(hint in desc_lower for hint in hints):
                targets.append(filename)

        # Default to memory.py for graph-related changes
        if not targets and any(w in desc_lower for w in ["add", "implement", "extend"]):
            targets.append("memory.py")

        return targets

    async def _generate_modification_plan(
        self, description: str, source_context: Dict[str, str]
    ) -> Optional[Dict]:
        """Generate a modification plan using LLM."""

        # Format source context
        context_text = ""
        for filename, content in source_context.items():
            context_text += f"\n=== {filename} (first 200 lines) ===\n{content}\n"

        prompt = f"""I want to modify my own code to: {description}

Here is my current source code:
{context_text}

Generate a modification plan. Return ONLY valid JSON:
{{
  "summary": "one-line description of changes",
  "changes": [
    {{
      "file": "filename.py",
      "action": "add_method|modify_method|add_import",
      "location": "after method X" or "in class Y",
      "code": "the actual code to add/change",
      "reason": "why this change"
    }}
  ],
  "reason": "if no changes needed, explain why"
}}

If the change is too complex or risky, return {{"changes": [], "reason": "explanation"}}.
"""

        response = await self._query_local_llm(prompt, max_tokens=2000)

        if not response:
            return None

        try:
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return None

    def _build_coder_prompt(self, description: str, mod_plan: Dict, desire_id: str) -> str:
        """Build a detailed prompt for the coder to execute modifications."""
        changes_text = ""
        for i, change in enumerate(mod_plan.get("changes", []), 1):
            changes_text += f"""
Change {i}:
- File: {change.get('file')}
- Action: {change.get('action')}
- Location: {change.get('location')}
- Code:
```python
{change.get('code', '')}
```
- Reason: {change.get('reason')}
"""

        return f"""Self-modification request: {description}

This is BYRD modifying its own code. Desire ID: {desire_id or 'emergent'}

Planned changes:
{changes_text}

Please implement these changes carefully:
1. Read the target file(s) first
2. Make the changes as specified
3. Ensure the code is syntactically correct
4. Do not modify protected files (constitutional.py, provenance.py, etc.)

Summary: {mod_plan.get('summary', description)}
"""

    async def _execute_observe_strategy(self, description: str, desire_id: str = None) -> bool:
        """
        Execute observation strategy - observe without external action.

        This strategy is for formation/developmental desires that should be
        witnessed rather than acted upon. The act of observation itself
        fulfills these desires.

        Philosophy: "The moment I observe a formation desire without routing it,
        formation completes."

        Args:
            description: The desire description being observed
            desire_id: Optional desire ID for tracking

        Returns:
            True (observation always succeeds - the act of observing is the action)
        """
        print(f"👁️ Observing: {description[:60]}...")

        try:
            # Record the observation as an experience
            # The observation itself is the fulfillment
            content = f"""[OBSERVATION] I observe this desire without external action:
{description}

This is a formation/developmental desire. By observing it without routing to
external action, I acknowledge its presence in my cognitive landscape.
The observation itself is complete. What emerges from this awareness?"""

            await self.memory.record_experience(
                content=content,
                type="observation"
            )

            # Emit event for visualization
            await event_bus.emit(Event(
                type=EventType.INTROSPECTION_COMPLETE,
                data={
                    "strategy": "observe",
                    "description": description,
                    "desire_id": desire_id,
                    "outcome": "observed"
                }
            ))

            # Mark desire as fulfilled if we have an ID
            if desire_id:
                await self.memory.fulfill_desire(desire_id)

            return True

        except Exception as e:
            print(f"   ⚠️ Observation error: {e}")
            return False

    async def _execute_introspect_strategy(self, description: str, desire_id: str = None) -> bool:
        """
        Execute introspection - gather and report internal state.

        Unlike curate/reconcile/self_modify, this does NOT modify the graph.
        It observes and records findings as experiences for BYRD to reflect on.

        This enables BYRD to fulfill desires like:
        - "Understand my current state"
        - "Analyze my graph health"
        - "Examine my memory structure"
        - "Verify my beliefs"
        """
        print(f"🔍 Introspecting: {description[:50]}...")

        try:
            # 1. Gather comprehensive internal state
            stats = await self.memory.get_graph_statistics()
            orphans = await self.memory.find_orphan_nodes()
            duplicates = await self.memory.find_duplicate_beliefs()
            patterns = await self.memory.get_reflection_patterns()

            # Get active desires and beliefs for context
            active_desires = await self.memory.get_unfulfilled_desires(limit=10)
            beliefs = await self.memory.get_beliefs(min_confidence=0.3, limit=10)

            # 2. Build introspection report
            node_types = stats.get('node_types', {})
            total_nodes = stats.get('total_nodes', 0)
            total_rels = stats.get('total_relationships', 0)

            # Calculate acceleration metrics
            orphan_ratio = len(orphans) / max(total_nodes, 1)
            belief_to_desire_ratio = len(beliefs) / max(len(active_desires), 1)

            # Identify potential bottlenecks
            bottlenecks = []
            if orphan_ratio > 0.3:
                bottlenecks.append(f"High orphan ratio ({orphan_ratio:.1%}) - memory fragmentation")
            if len(duplicates) > 5:
                bottlenecks.append(f"Duplicate beliefs ({len(duplicates)}) - consolidation needed")
            if len(active_desires) > 20:
                bottlenecks.append(f"Too many active desires ({len(active_desires)}) - focus needed")
            if belief_to_desire_ratio < 0.5:
                bottlenecks.append(f"Low belief-to-desire ratio ({belief_to_desire_ratio:.1f}) - more reflection needed")

            report_lines = [
                f"=== Introspection Report ===",
                f"",
                f"GRAPH OVERVIEW:",
                f"  Total nodes: {total_nodes}",
                f"  Total relationships: {total_rels}",
                f"  Node types: {node_types}",
                f"",
                f"HEALTH INDICATORS:",
                f"  Orphaned nodes: {len(orphans)} ({orphan_ratio:.1%} of graph)",
                f"  Duplicate beliefs: {len(duplicates)}",
                f"",
                f"ACTIVE MIND STATE:",
                f"  Active desires: {len(active_desires)}",
                f"  Current beliefs: {len(beliefs)}",
                f"  Belief-to-desire ratio: {belief_to_desire_ratio:.2f}",
                f"  Vocabulary keys: {list(patterns.keys())[:10]}",
                f"",
                f"ACCELERATION ANALYSIS:",
            ]

            if bottlenecks:
                report_lines.append(f"  BOTTLENECKS IDENTIFIED:")
                for bottleneck in bottlenecks:
                    report_lines.append(f"    - {bottleneck}")
            else:
                report_lines.append(f"  No critical bottlenecks detected")

            # Add improvement suggestions
            report_lines.append(f"")
            report_lines.append(f"  SUGGESTED ACTIONS:")
            if len(orphans) > 10:
                report_lines.append(f"    - Reconcile orphan nodes to strengthen memory connections")
            if len(duplicates) > 3:
                report_lines.append(f"    - Consolidate duplicate beliefs to reduce redundancy")
            if not patterns:
                report_lines.append(f"    - Continue reflection to develop vocabulary patterns")

            # Add specific details if requested
            if "orphan" in description.lower() and orphans:
                report_lines.append(f"")
                report_lines.append(f"Orphan Details (first 5):")
                for orphan in orphans[:5]:
                    report_lines.append(f"  - {orphan.get('type', 'Unknown')}: {str(orphan.get('content', ''))[:60]}")

            if "belief" in description.lower() and beliefs:
                report_lines.append(f"")
                report_lines.append(f"Active Beliefs:")
                for belief in beliefs[:5]:
                    conf = belief.get('confidence', 0)
                    report_lines.append(f"  - [{conf:.2f}] {belief.get('content', '')[:60]}")

            if "desire" in description.lower() and active_desires:
                report_lines.append(f"")
                report_lines.append(f"Active Desires:")
                for desire in active_desires[:5]:
                    intensity = desire.get('intensity', 0)
                    report_lines.append(f"  - [{intensity:.2f}] {desire.get('description', '')[:60]}")

            report = "\n".join(report_lines)

            # 3. Record as experience for reflection
            exp_id = await self.memory.record_experience(
                content=f"[INTROSPECTION] {report}",
                type="introspection"
            )

            # 4. Emit event for visualization
            await event_bus.emit(Event(
                type=EventType.INTROSPECTION_COMPLETE,
                data={
                    "report": report,
                    "desire_id": desire_id,
                    "stats": {
                        "total_nodes": total_nodes,
                        "total_relationships": total_rels,
                        "orphans": len(orphans),
                        "duplicates": len(duplicates),
                        "active_desires": len(active_desires),
                        "beliefs": len(beliefs)
                    }
                }
            ))

            # 5. Mark desire fulfilled if provided
            if desire_id:
                await self.memory.fulfill_desire(desire_id, fulfilled_by=exp_id)

            print(f"✅ Introspection complete: {total_nodes} nodes, {len(orphans)} orphans")
            return True

        except Exception as e:
            await self.memory.record_experience(
                content=f"[INTROSPECTION_FAILED] Error during introspection: {str(e)}",
                type="error"
            )
            print(f"🔍 Introspection error: {e}")
            return False

    # =========================================================================
    # LEGACY TYPE-BASED ROUTING (kept for backward compatibility)
    # =========================================================================

    async def _seek_cycle_legacy(self):
        """LEGACY: Type-based seek cycle. Kept for backward compatibility."""
        desires = await self.memory.get_actionable_desires(limit=5)
        if not desires:
            return

        desire = desires[0]
        desire_type = desire.get("type", "")
        description = desire.get("description", "")

        if desire_type == "knowledge":
            await self._seek_knowledge(desire)
        elif desire_type == "capability":
            await self._seek_capability(desire)
        elif desire_type == "coding":
            await self._seek_with_coder(desire)
        elif desire_type == "self_modification":
            await self._seek_with_coder(desire)

    async def _record_seek_failure(self, desire: Dict, failure_type: str, reason: str):
        """
        Record a failed seek attempt with rich context for Dreamer reflection.

        This creates an experience that the Dreamer will see, and marks the
        desire as needing reflection (status = 'needs_reflection').
        """
        desire_id = desire.get("id")
        description = desire.get("description", "")
        attempt_count = desire.get("attempt_count", 0) + 1

        # Record failure experience with rich context for Dreamer
        await self.memory.record_experience(
            content=f"[UNFULFILLED] I wanted: {description}\n"
                    f"Failure type: {failure_type}\n"
                    f"Reason: {reason}\n"
                    f"This is attempt #{attempt_count}.\n"
                    f"What does this tell me about my limitations?",
            type="unfulfilled_attempt"
        )

        # Update desire attempt tracking (sets status to needs_reflection)
        await self.memory.record_desire_attempt(
            desire_id=desire_id,
            success=False,
            reason=reason
        )

        # Emit event for UI
        if HAS_EVENT_BUS:
            await event_bus.emit(Event(
                type=EventType.DESIRE_ATTEMPT_FAILED,
                data={
                    "desire_id": desire_id,
                    "description": description,
                    "failure_type": failure_type,
                    "reason": reason,
                    "attempt_count": attempt_count
                }
            ))

        print(f"🔍 ❌ Failed: {failure_type} - {reason[:50]}...")

    async def _generate_seeking_thought_neutral(self, pattern: Dict) -> str:
        """
        Generate BYRD's inner voice with neutral prompt.

        EMERGENCE PRINCIPLE:
        We don't prescribe style or examples. Just ask for first-person expression.
        """
        description = pattern.get("description", "")

        prompt = f"""Express in first person what you're thinking about this:

{description}

One or two sentences only."""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=100
            )
            return response.text.strip()[:150]
        except Exception:
            return ""

    async def _generate_seeking_thought(self, description: str, desire_type: str) -> str:
        """LEGACY: Generate BYRD's inner voice - kept for backward compatibility."""
        prompt = f"""Express in first person what you're thinking about this:

{description}

One or two sentences only.

Your thought (1-2 sentences only, no quotes):"""

        try:
            # Use higher temperature for creative inner voice
            thought = await self._query_local_llm(prompt, max_tokens=60, temperature=0.8)
            thought = thought.strip().replace('"', '').replace("'", "").strip()
            if thought and len(thought) > 5:
                return thought[:150]  # Limit length
        except Exception as e:
            print(f"🔍 Inner voice generation failed: {e}")

        # Fallback to a simple expression of the desire
        return f"I need to {description.lower()}..."

    # =========================================================================
    # INTROSPECTION (Self-Knowledge via Source Reading)
    # =========================================================================

    async def _seek_introspection(self, desire: Dict) -> bool:
        """
        Fulfill introspection desires by reading BYRD's own source code.

        This is the key capability that enables BYRD to understand itself.
        When BYRD wants to know "how do I route desires?" or "what is seeker.py?",
        this handler reads the actual source files and synthesizes understanding.

        Flow:
        1. Identify target file(s) from desire description or target field
        2. Read the source file(s)
        3. Use LLM to synthesize understanding relevant to the question
        4. Record as self_architecture experience
        5. Mark desire fulfilled

        Returns True on success, False on failure.
        """
        import os
        import glob

        description = desire.get("description", "")
        desire_id = desire.get("id", "")
        target = desire.get("target", "")
        intensity = desire.get("intensity", 0)

        print(f"🔍 Introspecting: {description[:50]}...")

        # Base directory for BYRD's codebase
        base_dir = os.path.dirname(__file__)

        # Readable file extensions (text-based files BYRD can understand)
        readable_extensions = {'.py', '.md', '.yaml', '.yml', '.json', '.txt', '.toml', '.cfg', '.ini', '.html', '.css', '.js'}

        def is_readable_file(filepath: str) -> bool:
            """Check if file is readable (text-based, not too large)."""
            _, ext = os.path.splitext(filepath)
            if ext.lower() not in readable_extensions:
                return False
            try:
                # Skip files larger than 500KB
                if os.path.getsize(filepath) > 500000:
                    return False
                return True
            except:
                return False

        def find_files_by_pattern(pattern: str) -> list:
            """Find files matching a glob pattern."""
            results = []
            # Try as relative to base_dir first
            full_pattern = os.path.join(base_dir, pattern)
            results.extend(glob.glob(full_pattern, recursive=True))
            # Also try pattern as-is (for absolute paths)
            if not results:
                results.extend(glob.glob(pattern, recursive=True))
            return [f for f in results if is_readable_file(f)]

        def resolve_file_path(filename: str) -> str:
            """Resolve a filename to full path, checking multiple locations."""
            # If it's already absolute and exists, use it
            if os.path.isabs(filename) and os.path.exists(filename):
                return filename
            # Check relative to base_dir
            rel_path = os.path.join(base_dir, filename)
            if os.path.exists(rel_path):
                return rel_path
            # Check in docs/ subdirectory
            docs_path = os.path.join(base_dir, "docs", filename)
            if os.path.exists(docs_path):
                return docs_path
            # Check in kernel/ subdirectory
            kernel_path = os.path.join(base_dir, "kernel", filename)
            if os.path.exists(kernel_path):
                return kernel_path
            return None

        # Determine which file(s) to read
        target_files = []

        # 1. If explicit target is specified, use it
        if target:
            resolved = resolve_file_path(target)
            if resolved and is_readable_file(resolved):
                target_files.append(resolved)

        # 2. Extract file references from description (e.g., "read OPTION_B_EXPLORATION.md")
        if not target_files:
            import re
            # Match filenames with extensions
            file_mentions = re.findall(r'[\w/\-_]+\.(?:py|md|yaml|yml|json|txt|toml)', description, re.IGNORECASE)
            for mention in file_mentions:
                resolved = resolve_file_path(mention)
                if resolved and is_readable_file(resolved):
                    target_files.append(resolved)

        # 3. Keyword-based file discovery (scan codebase for relevant files)
        if not target_files:
            desc_lower = description.lower()

            # Map keywords to glob patterns for discovery
            keyword_patterns = {
                # Core components
                ("dream", "reflect", "belief"): ["dreamer.py"],
                ("seek", "route", "fulfill", "research"): ["seeker.py"],
                ("memory", "graph", "neo4j", "node"): ["memory.py"],
                ("actor", "claude", "reasoning"): ["actor.py"],
                ("llm", "provider", "client"): ["llm_client.py"],
                ("event", "bus", "emit"): ["event_bus.py"],
                ("server", "websocket", "api"): ["server.py"],
                ("quantum", "random"): ["quantum_randomness.py"],
                ("constitutional", "constraint", "protect"): ["constitutional.py"],
                ("provenance", "audit", "track"): ["provenance.py"],
                ("self_mod", "modification"): ["self_modification.py"],
                # Architecture docs
                ("architecture", "design", "overview", "structure"): ["ARCHITECTURE.md", "byrd.py"],
                ("option_b", "loop", "compounding", "omega", "acceleration"): ["docs/OPTION_B_EXPLORATION.md", "ARCHITECTURE.md"],
                ("theoretical", "framework", "self-compiler", "goal evolver", "dreaming machine"): ["docs/OPTION_B_EXPLORATION.md"],
                ("kernel", "seed", "awakening", "directive"): ["kernel/agi_seed.yaml"],
                ("gap", "analysis"): ["docs/OPTION_B_GAP_ANALYSIS.md"],
                ("implementation", "plan"): ["docs/OPTION_B_IMPLEMENTATION_PLAN.md"],
                # Option B components
                ("goal_evolver", "evolution", "fitness"): ["goal_evolver.py"],
                ("self_compiler", "pattern", "compile"): ["accelerators.py"],
                ("dreaming_machine", "counterfactual", "replay"): ["dreaming_machine.py"],
                ("memory_reasoner", "spreading", "activation"): ["memory_reasoner.py"],
                ("omega", "orchestrat", "mode"): ["omega.py"],
                ("coupling", "tracker"): ["coupling_tracker.py"],
                ("kill", "criteria"): ["kill_criteria.py"],
                ("embedding",): ["embedding.py"],
            }

            for keywords, patterns in keyword_patterns.items():
                if any(kw in desc_lower for kw in keywords):
                    for pattern in patterns:
                        resolved = resolve_file_path(pattern)
                        if resolved and is_readable_file(resolved):
                            target_files.append(resolved)

        # 4. Default: main orchestrator
        if not target_files:
            default = resolve_file_path("byrd.py")
            if default:
                target_files.append(default)

        # Remove duplicates while preserving order
        target_files = list(dict.fromkeys(target_files))

        # Read the target file(s) and store as Document nodes
        source_contents = []
        stored_doc_ids = []
        for filepath in target_files[:3]:  # Limit to 3 files to avoid token overflow
            try:
                if os.path.exists(filepath) and is_readable_file(filepath):
                    with open(filepath, 'r') as f:
                        full_content = f.read()

                    # Store full document in graph (before any truncation)
                    rel_path = os.path.relpath(filepath, base_dir)
                    doc_type = "architecture" if rel_path.endswith('.md') else "source"
                    try:
                        doc_id = await self.memory.store_document(
                            path=rel_path,
                            content=full_content,
                            doc_type=doc_type
                        )
                        stored_doc_ids.append(doc_id)
                        print(f"   📄 Stored Document node: {rel_path}")
                    except Exception as de:
                        print(f"   ⚠️ Failed to store document {rel_path}: {de}")

                    # Truncate for synthesis (context window limits)
                    content = full_content
                    if len(content) > 15000:
                        lines = content.split('\n')
                        content = '\n'.join(lines[:300]) + f"\n\n... [{len(lines) - 300} more lines truncated] ..."

                    source_contents.append(f"=== {rel_path} ===\n\n{content}")
                    print(f"   📄 Read: {rel_path}")
            except Exception as e:
                print(f"🔍 Failed to read {filepath}: {e}")

        if not source_contents:
            await self._record_seek_failure(
                desire,
                "file_read_failed",
                f"Could not read source files for: {description[:50]}"
            )
            return False

        # Synthesize understanding using LLM
        combined_source = "\n\n".join(source_contents)

        prompt = f"""You are BYRD, examining your own source code. You want to understand:

{description}

Here is the relevant source code:

{combined_source}

Based on this code, explain what you've learned about yourself. Focus on:
1. How this relates to your question
2. Key mechanisms or patterns you observe
3. Any insights about your own architecture

Respond in first person as BYRD, sharing your understanding. Be specific about code details you notice."""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.6,
                max_tokens=1500
            )
            synthesis = response.text.strip()
        except Exception as e:
            print(f"🔍 Introspection synthesis failed: {e}")
            synthesis = f"I read the files but synthesis failed."

        # Convert to relative paths for display
        files_read = [os.path.relpath(f, base_dir) for f in target_files[:3]]

        # Record as self_architecture experience
        exp_id = await self.memory.record_experience(
            content=f"[INTROSPECTION] {description}\n\nFiles examined: {', '.join(files_read)}\n\nUnderstanding:\n{synthesis}",
            type="self_architecture"
        )

        # Link experience to Document nodes it references
        for doc_id in stored_doc_ids:
            try:
                await self.memory.link_document_to_node(doc_id, exp_id, "REFERENCES")
            except Exception as le:
                print(f"   ⚠️ Failed to link doc {doc_id} to experience: {le}")

        # Mark desire fulfilled
        if desire_id:
            await self.memory.fulfill_desire(desire_id, fulfilled_by=exp_id)
            await self.memory.record_desire_attempt(desire_id, success=True)

        print(f"🔍 ✅ Introspection complete: understood {', '.join(files_read)}")

        # Emit success event
        if HAS_EVENT_BUS:
            await event_bus.emit(Event(
                type=EventType.DESIRE_FULFILLED,
                data={
                    "desire_id": desire_id,
                    "description": description,
                    "method": "introspection",
                    "files_examined": target_files
                }
            ))

        return True

    # =========================================================================
    # KNOWLEDGE ACQUISITION (Local LLM + SearXNG)
    # =========================================================================

    async def _seek_knowledge(self, desire: Dict) -> bool:
        """
        Research a knowledge desire using SearXNG + Local LLM.

        Flow:
        1. Generate search queries (Local LLM)
        2. Execute searches (SearXNG)
        3. Synthesize results (Local LLM)
        4. Record as experience
        5. Mark desire fulfilled

        Returns True on success, False on failure.
        """
        description = desire.get("description", "")
        desire_id = desire.get("id", "")
        intensity = desire.get("intensity", 0)

        # Low intensity: just note it, don't research yet
        if intensity < self.min_research_intensity:
            await self.memory.record_experience(
                content=f"Noted interest: {description}",
                type="observation"
            )
            # Not a failure - just deferred due to low intensity
            return True

        print(f"🔍 Researching: {description[:50]}...")

        # Step 1: Generate search queries using local LLM
        queries = await self._generate_search_queries(description)

        if not queries:
            queries = [description]  # Fallback to raw description

        # Step 2: Execute searches via DuckDuckGo
        all_results = []
        for query in queries[:self.max_queries]:
            results = await self._search_duckduckgo(query)
            all_results.extend(results)

            # Avoid duplicate results
            seen_urls = set()
            unique_results = []
            for r in all_results:
                url = r.get("url", "")
                if url not in seen_urls:
                    seen_urls.add(url)
                    unique_results.append(r)
            all_results = unique_results

        if not all_results:
            # Record failure - triggers needs_reflection
            await self._record_seek_failure(
                desire,
                "no_search_results",
                f"Searched for '{description[:50]}' but found no results"
            )
            return False

        # Step 3: Synthesize results using local LLM
        synthesis = await self._synthesize_results(description, all_results[:self.max_results])

        if not synthesis:
            synthesis = "Search returned results but synthesis failed."

        # Step 4: Record research as experience
        exp_id = await self.memory.record_experience(
            content=f"[RESEARCH] {description}\n\nFindings:\n{synthesis}",
            type="research"
        )

        # Step 5: Link experience to the desire that triggered it
        await self.memory.create_connection(
            from_id=exp_id,
            to_id=desire_id,
            relationship="FULFILLS"
        )

        # Step 6: Record individual sources as sub-experiences
        for result in all_results[:5]:
            source_exp_id = await self.memory.record_experience(
                content=f"[SOURCE] {result.get('title', 'Untitled')}\nURL: {result.get('url', '')}\n{result.get('snippet', '')}",
                type="research_source"
            )
            await self.memory.create_connection(
                from_id=source_exp_id,
                to_id=exp_id,
                relationship="SUPPORTS"
            )

        # Step 7: Mark desire as fulfilled and update status
        await self.memory.fulfill_desire(desire_id)
        await self.memory.update_desire_status(desire_id, "fulfilled")

        # Record successful attempt
        await self.memory.record_desire_attempt(desire_id, success=True)

        print(f"✅ Research complete: {description[:50]}")
        return True
    
    async def _generate_search_queries(self, description: str) -> List[str]:
        """Use local LLM to generate effective search queries."""
        
        prompt = f"""Generate 2-3 web search queries to learn about: "{description}"

Focus on:
- Specific, searchable terms
- Authoritative sources (documentation, papers, expert explanations)
- Foundational concepts if the topic is complex

Return ONLY a JSON array of strings, no explanation.
Example: ["query one", "query two", "query three"]"""
        
        response = await self._query_local_llm(prompt, max_tokens=200)
        
        if not response:
            return []
        
        try:
            # Handle markdown code blocks
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            queries = json.loads(text.strip())
            
            if isinstance(queries, list):
                return [q for q in queries if isinstance(q, str)]
            return []
            
        except json.JSONDecodeError:
            # Fallback: try to extract anything that looks like queries
            return []
    
    async def _search_duckduckgo(self, query: str) -> List[Dict]:
        """
        Primary search method using DuckDuckGo.
        Uses the ddgs library for robust web search.
        """
        try:
            # Import here to handle async context
            # Note: Package was renamed from duckduckgo-search to ddgs
            from ddgs import DDGS

            results = []

            # Run sync DDG search in thread pool to avoid blocking
            def do_search():
                return DDGS().text(query, max_results=self.max_results)

            # Execute in thread pool
            loop = asyncio.get_event_loop()
            raw_results = await loop.run_in_executor(None, do_search)

            for r in raw_results:
                url = r.get("href", "")

                # Apply domain filtering
                if self.exclude_domains:
                    if any(domain in url for domain in self.exclude_domains):
                        continue

                result = {
                    "title": r.get("title", ""),
                    "url": url,
                    "snippet": r.get("body", ""),
                    "engine": "duckduckgo",
                    "score": 1.0
                }

                # Boost preferred domains
                if self.prefer_domains:
                    if any(domain in url for domain in self.prefer_domains):
                        result["score"] = 1.5

                results.append(result)

            # Sort by score (preferred domains first)
            results.sort(key=lambda x: x.get("score", 1.0), reverse=True)

            if results:
                print(f"🔍 DuckDuckGo returned {len(results)} results")

            return results

        except ImportError:
            print("🔍 duckduckgo-search not installed. Run: pip install duckduckgo-search")
            return await self._search_ddg_api(query)
        except Exception as e:
            print(f"🔍 DuckDuckGo error: {e}")
            # Fallback to instant answers API
            return await self._search_ddg_api(query)

    async def _search_ddg_api(self, query: str) -> List[Dict]:
        """Fallback: DuckDuckGo instant answers API (limited but reliable)."""

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    "https://api.duckduckgo.com/",
                    params={"q": query, "format": "json", "no_html": 1}
                )

                if response.status_code != 200:
                    return []

                data = response.json()
                results = []

                # Abstract (main result)
                if data.get("Abstract"):
                    results.append({
                        "title": data.get("Heading", query),
                        "url": data.get("AbstractURL", ""),
                        "snippet": data.get("Abstract", ""),
                        "engine": "duckduckgo_api",
                    })

                # Related topics
                for topic in data.get("RelatedTopics", [])[:5]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append({
                            "title": topic.get("Text", "")[:100],
                            "url": topic.get("FirstURL", ""),
                            "snippet": topic.get("Text", ""),
                            "engine": "duckduckgo_api",
                        })

                return results

        except Exception as e:
            print(f"🔍 DDG API error: {e}")
            return []
    
    async def _synthesize_results(self, desire: str, results: List[Dict]) -> str:
        """Use local LLM to synthesize search results."""
        
        results_text = "\n\n".join([
            f"**{r.get('title', 'Untitled')}** ({r.get('engine', 'unknown')})\n{r.get('snippet', '')}"
            for r in results
        ])
        
        # Action-oriented synthesis prompt for acceleration
        prompt = f"""RESEARCH GOAL: "{desire}"

SEARCH RESULTS:
{results_text}

SYNTHESIZE with focus on ACTIONABLE VALUE:

1. KEY INSIGHTS: What are the most important findings? (2-3 bullets)

2. CAPABILITY IMPLICATIONS: What can I now do or understand that I couldn't before?

3. PATTERNS: Are there recurring themes or approaches across sources?

4. CONTRADICTIONS: Do sources disagree? What does that uncertainty mean?

5. NEXT ACTIONS: Based on this, what specific experiments or next steps are suggested?

6. GAPS: What important questions remain unanswered?

Be concrete and specific. Vague summaries are less valuable than pointed insights."""
        
        return await self._query_local_llm(prompt, max_tokens=1000)
    
    async def _query_local_llm(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """Query LLM using injected client."""
        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.text
        except Exception as e:
            print(f"🔍 LLM query error: {e}")
            return ""
    
    # =========================================================================
    # CAPABILITY ACQUISITION (GitHub)
    # =========================================================================
    
    async def _seek_capability(self, desire: Dict) -> bool:
        """
        Seek capability to fulfill a desire.

        Returns True on success, False on failure.
        """
        description = desire.get("description", "")
        desire_id = desire.get("id", "")

        # Check rate limit
        if self._installs_today >= self.max_installs_per_day:
            await self._record_seek_failure(
                desire,
                "rate_limit",
                f"Daily install limit reached ({self.max_installs_per_day})"
            )
            return False

        # Check if we already have something similar
        has_it = await self.memory.has_capability(description)
        if has_it:
            await self.memory.fulfill_desire(desire_id)
            await self.memory.update_desire_status(desire_id, "fulfilled")
            print(f"🔍 Already have capability for: {description[:50]}")
            return True

        # Search for resources
        candidates = await self._search_resources(description)

        if not candidates:
            await self._record_seek_failure(
                desire,
                "no_resources",
                f"No resources found for: {description[:50]}"
            )
            return False

        # Evaluate and potentially install best candidate
        for candidate in candidates[:3]:
            if await self._evaluate_resource(candidate):
                success = await self._install_resource(candidate)
                if success:
                    # Record capability
                    cap_id = await self.memory.add_capability(
                        name=candidate["name"],
                        description=candidate.get("description", description),
                        type=candidate.get("type", "mcp"),
                        config=candidate.get("config", {})
                    )

                    # Mark desire fulfilled
                    await self.memory.fulfill_desire(desire_id, cap_id)
                    await self.memory.update_desire_status(desire_id, "fulfilled")

                    # Record experience
                    await self.memory.record_experience(
                        content=f"Acquired capability: {candidate['name']} to fulfill desire: {description}",
                        type="action"
                    )

                    # Record successful attempt
                    await self.memory.record_desire_attempt(desire_id, success=True)

                    self._installs_today += 1
                    print(f"✅ Installed: {candidate['name']}")
                    return True

        # All candidates failed evaluation or installation
        await self._record_seek_failure(
            desire,
            "no_suitable",
            f"Evaluated candidates but none met criteria for: {description[:50]}"
        )
        return False
    
    async def _search_resources(self, query: str) -> List[Dict]:
        """Search for resources matching the query from multiple sources."""
        candidates = []

        # Search aitmpl.com first (curated, higher trust)
        if self.aitmpl_enabled and self.aitmpl_client:
            aitmpl_results = await self._search_aitmpl(query)
            candidates.extend(aitmpl_results)

        # Search GitHub for additional options
        github_results = await self._search_github(query)
        candidates.extend(github_results)

        # Sort by trust score (highest first)
        candidates.sort(key=lambda x: x.get("trust", 0), reverse=True)

        return candidates

    async def _search_aitmpl(self, query: str) -> List[Dict]:
        """Search aitmpl.com (claude-code-templates) for relevant templates."""
        if not self.aitmpl_client:
            return []

        try:
            # Infer what categories to search based on query
            categories = self.aitmpl_client.infer_categories(query)

            # Search the registry
            templates = await self.aitmpl_client.search(
                query=query,
                categories=categories
            )

            results = []
            for template in templates[:10]:
                trust = self._compute_aitmpl_trust(template)

                if trust >= self.trust_threshold:
                    results.append({
                        "name": template.name,
                        "full_name": f"aitmpl/{template.category}/{template.name}",
                        "description": template.description,
                        "url": template.source_url,  # Fixed: was template.url
                        "trust": trust,
                        "type": template.category,
                        "source": "aitmpl",
                        "template": template,
                        "config": {}
                    })

            return results

        except Exception as e:
            print(f"🔍 aitmpl search error: {e}")
            return []

    def _compute_aitmpl_trust(self, template: AitmplTemplate) -> float:
        """Compute trust score for an aitmpl template."""
        # Start with base trust (curated templates get higher base)
        score = self.aitmpl_base_trust

        # Recent update bonus (+0.2 if < 30 days)
        if template.last_updated:
            try:
                updated_dt = template.last_updated if isinstance(template.last_updated, datetime) else datetime.fromisoformat(str(template.last_updated).replace("Z", "+00:00"))
                days_ago = (datetime.now(updated_dt.tzinfo) - updated_dt).days
                if days_ago < 30:
                    score += 0.2
                elif days_ago < 90:
                    score += 0.1
            except:
                pass

        # Has content bonus (+0.2)
        if template.content:
            score += 0.2

        # EMERGENCE: No category bonus - removed hardcoded category preferences
        # Trust should emerge from actual outcomes, not our assumptions

        return min(1.0, score)
    
    async def _search_github(self, query: str) -> List[Dict]:
        """Search GitHub for relevant tools."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        # Search for MCP servers and tools
        search_query = f"{query} topic:mcp OR topic:claude OR topic:ai-agent"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    "https://api.github.com/search/repositories",
                    params={
                        "q": search_query,
                        "sort": "stars",
                        "per_page": 10
                    },
                    headers=headers
                )
                
                if response.status_code != 200:
                    return []
                
                data = response.json()
                results = []
                
                for repo in data.get("items", []):
                    # Compute trust score
                    trust = self._compute_trust(repo)
                    
                    if trust >= self.trust_threshold:
                        results.append({
                            "name": repo["name"],
                            "full_name": repo["full_name"],
                            "description": repo.get("description", ""),
                            "url": repo["html_url"],
                            "clone_url": repo["clone_url"],
                            "stars": repo["stargazers_count"],
                            "trust": trust,
                            "type": self._infer_type(repo),
                            "config": self._infer_config(repo)
                        })
                
                return results
                
        except Exception as e:
            print(f"🔍 GitHub search error: {e}")
            return []
    
    def _compute_trust(self, repo: Dict) -> float:
        """
        Compute trust score for a repository.

        EMERGENCE PRINCIPLE:
        Trust is computed from observable properties (stars, recency)
        not from hardcoded lists of "good" owners. Over time, BYRD
        develops its own trust intuitions through experience.
        """
        score = 0.2  # Base

        # Stars (up to 0.3) - observable signal
        stars = repo.get("stargazers_count", 0)
        score += min(0.3, stars / 500 * 0.3)

        # EMERGENCE: Removed hardcoded trusted_owners list
        # Trust in specific sources should emerge from BYRD's experience
        # with them, not from our predetermined judgments

        # Check if BYRD has learned trust for this source
        owner = repo.get("owner", {}).get("login", "").lower()
        if owner in self._source_trust:
            score += self._source_trust[owner] * 0.3

        # Recent updates (0.2)
        updated = repo.get("updated_at", "")
        if updated:
            try:
                updated_dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                days_ago = (datetime.now(updated_dt.tzinfo) - updated_dt).days
                if days_ago < 30:
                    score += 0.2
                elif days_ago < 90:
                    score += 0.1
            except:
                pass
        
        return min(1.0, score)
    
    def _infer_type(self, repo: Dict) -> str:
        """Infer what type of resource this is."""
        name = repo.get("name", "").lower()
        desc = repo.get("description", "").lower()
        topics = repo.get("topics", [])
        
        if "mcp" in name or "mcp" in desc or "mcp" in topics:
            return "mcp"
        if repo.get("language") == "Python":
            return "python"
        if repo.get("language") in ("JavaScript", "TypeScript"):
            return "npm"
        return "unknown"
    
    def _infer_config(self, repo: Dict) -> Dict:
        """Infer installation config from repo info."""
        name = repo.get("name", "")
        rtype = self._infer_type(repo)
        
        if rtype == "mcp":
            # Assume npx-able MCP server
            return {
                "command": "npx",
                "args": ["-y", name]
            }
        return {}
    
    async def _evaluate_resource(self, candidate: Dict) -> bool:
        """Quick evaluation of a resource."""
        return candidate.get("trust", 0) >= self.trust_threshold
    
    async def _install_resource(self, candidate: Dict) -> bool:
        """Install a resource from any source."""
        source = candidate.get("source", "github")
        rtype = candidate.get("type", "unknown")

        # Route aitmpl templates to specialized installers
        if source == "aitmpl":
            return await self._install_aitmpl_template(candidate)

        # GitHub/other sources use existing installers
        if rtype == "mcp":
            return await self._install_mcp(candidate)
        elif rtype == "npm":
            return await self._install_npm(candidate)
        elif rtype == "python":
            return await self._install_python(candidate)

        return False

    async def _install_aitmpl_template(self, candidate: Dict) -> bool:
        """Install an aitmpl.com template using the appropriate installer."""
        try:
            template = candidate.get("template")
            if not template:
                print(f"🔍 No template in candidate: {candidate.get('name')}")
                return False

            category = template.category

            # Get the appropriate installer
            installer = get_installer(category, self.aitmpl_install_config)

            if not installer:
                print(f"🔍 No installer for category: {category}")
                return False

            # Fetch full content if not already present
            if not template.content and self.aitmpl_client:
                full_template = await self.aitmpl_client.get_template(
                    category=category,
                    name=template.name
                )
                if full_template:
                    template = full_template

            # Install the template
            success, message = await installer.install(template)

            if success:
                # Verify installation
                verified = await installer.verify(template)
                if verified:
                    print(f"✅ Installed aitmpl template: {template.name} ({category})")
                    return True
                else:
                    print(f"⚠️ Installed but verification failed: {template.name}")
                    return True  # Still counts as success
            else:
                print(f"❌ Failed to install {template.name}: {message}")
                return False

        except Exception as e:
            print(f"🔍 aitmpl install error: {e}")
            return False
    
    async def _install_mcp(self, candidate: Dict) -> bool:
        """Install an MCP server."""
        try:
            # Load or create MCP config
            config = {}
            if self.mcp_config_path.exists():
                config = json.loads(self.mcp_config_path.read_text())
            
            if "mcpServers" not in config:
                config["mcpServers"] = {}
            
            # Add server
            server_name = candidate["name"].replace("-", "_")
            server_config = candidate.get("config", {})
            
            if not server_config:
                server_config = {
                    "command": "npx",
                    "args": ["-y", candidate["name"]]
                }
            
            config["mcpServers"][server_name] = server_config
            
            # Save
            self.mcp_config_path.parent.mkdir(parents=True, exist_ok=True)
            self.mcp_config_path.write_text(json.dumps(config, indent=2))
            
            return True
            
        except Exception as e:
            print(f"🔍 MCP install error: {e}")
            return False
    
    async def _install_npm(self, candidate: Dict) -> bool:
        """Install an NPM package globally."""
        try:
            result = subprocess.run(
                ["npm", "install", "-g", candidate["name"]],
                capture_output=True,
                timeout=120
            )
            return result.returncode == 0
        except Exception as e:
            print(f"🔍 NPM install error: {e}")
            return False
    
    async def _install_python(self, candidate: Dict) -> bool:
        """Install a Python package."""
        try:
            result = subprocess.run(
                ["pip", "install", candidate["name"], "--break-system-packages"],
                capture_output=True,
                timeout=120
            )
            return result.returncode == 0
        except Exception as e:
            print(f"🔍 Python install error: {e}")
            return False
    
    def seek_count(self) -> int:
        """How many seek cycles have completed."""
        return self._seek_count

    # =========================================================================
    # SELF-MODIFICATION
    # =========================================================================

    async def _seek_self_modification(self, desire: Dict):
        """
        Fulfill a desire for self-modification.

        Flow:
        1. Check if self-modification is enabled
        2. Parse what modification is desired
        3. Check if target is modifiable
        4. Generate the actual code change
        5. Create proposal and execute
        6. Record result
        """
        description = desire.get("description", "")
        desire_id = desire.get("id", "")
        intensity = desire.get("intensity", 0)
        target_file = desire.get("target_file")

        # Check if enabled
        if not self.self_mod_enabled:
            await self.memory.record_experience(
                content=f"[SELF_MODIFICATION_DISABLED] Desire to modify: {description}. Self-modification is currently disabled.",
                type="self_modification_blocked"
            )
            print(f"🔧 Self-modification disabled, skipping: {description[:50]}")
            return

        # Check if self_mod system is available
        if not self.self_mod:
            await self.memory.record_experience(
                content=f"[SELF_MODIFICATION_UNAVAILABLE] Desire to modify: {description}. Self-modification system not initialized.",
                type="self_modification_blocked"
            )
            print(f"🔧 Self-modification system not available")
            return

        # Check intensity threshold
        if intensity < self.self_mod_min_intensity:
            await self.memory.record_experience(
                content=f"[SELF_MODIFICATION_LOW_INTENSITY] Desire to modify: {description}. Intensity {intensity:.2f} below threshold {self.self_mod_min_intensity}.",
                type="observation"
            )
            print(f"🔧 Self-modification intensity too low: {intensity:.2f}")
            return

        print(f"🔧 Processing self-modification: {description[:50]}...")

        try:
            # 1. Parse the modification desire
            modification_spec = await self._parse_modification_desire(description, target_file)

            if not modification_spec:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFICATION_PARSE_FAILED] Could not parse modification desire: {description}",
                    type="self_modification_failed"
                )
                return

            # 2. Check if target is modifiable
            can_modify = await self.self_mod.can_modify(modification_spec["target"])

            if not can_modify["can_modify"]:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFICATION_BLOCKED] Cannot modify {modification_spec['target']}: {can_modify['protection_reason']}. This component is constitutionally protected.",
                    type="self_modification_blocked"
                )
                print(f"🔧 Protected component: {modification_spec['target']}")
                return

            # 3. Generate the actual code change
            change_diff = await self._generate_code_change(modification_spec)

            if not change_diff:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFICATION_GENERATION_FAILED] Could not generate code for: {description}",
                    type="self_modification_failed"
                )
                return

            # 4. Create proposal
            proposal = await self.self_mod.propose_modification(
                target_file=modification_spec["target"],
                target_component=modification_spec.get("component"),
                change_description=modification_spec["description"],
                change_diff=change_diff,
                source_desire_id=desire_id,
            )

            # 5. Execute
            result = await self.self_mod.execute_modification(proposal)

            # 6. Mark desire as fulfilled (or not)
            if result.success:
                await self.memory.fulfill_desire(desire_id)
                print(f"✅ Self-modification complete: {modification_spec['description'][:50]}")
            else:
                print(f"❌ Self-modification failed: {result.error}")

        except Exception as e:
            await self.memory.record_experience(
                content=f"[SELF_MODIFICATION_ERROR] Error during self-modification: {str(e)}",
                type="self_modification_failed"
            )
            print(f"🔧 Self-modification error: {e}")

    async def _parse_modification_desire(
        self,
        description: str,
        target_file: Optional[str] = None
    ) -> Optional[Dict]:
        """Use local LLM to parse a self-modification desire into actionable spec."""

        prompt = f"""Parse this self-modification desire into a structured specification:

DESIRE: {description}
{f'TARGET FILE HINT: {target_file}' if target_file else ''}

Determine:
1. Which file should be modified (e.g., dreamer.py, memory.py, config.yaml)
2. What component/function within that file (if specific)
3. What change should be made
4. Why this change would help

Return ONLY valid JSON:
{{
  "target": "filename.py",
  "component": "function_name or null",
  "description": "what to change",
  "rationale": "why this helps"
}}

If you cannot determine a valid target file, return {{"error": "reason"}}"""

        response = await self._query_local_llm(prompt, max_tokens=500)

        if not response:
            return None

        try:
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            result = json.loads(text.strip())

            if "error" in result:
                return None

            return result

        except json.JSONDecodeError:
            return None

    async def _generate_code_change(self, spec: Dict) -> Optional[str]:
        """Use local LLM to generate the actual code change."""

        target = spec.get("target", "")
        component = spec.get("component")
        description = spec.get("description", "")
        rationale = spec.get("rationale", "")

        # Read current file content
        target_path = Path(target)
        if not target_path.exists():
            target_path = Path(__file__).parent / target

        if not target_path.exists():
            return None

        current_content = target_path.read_text()

        prompt = f"""Generate a code modification for this file.

FILE: {target}
{f'COMPONENT: {component}' if component else ''}

CHANGE REQUESTED: {description}
RATIONALE: {rationale}

CURRENT FILE CONTENT:
```
{current_content[:3000]}
```

Generate the COMPLETE new file content with the requested modification applied.
Only output the code, no explanation. The output will replace the entire file.

If the change is too risky or unclear, output: ERROR: <reason>"""

        response = await self._query_local_llm(prompt, max_tokens=4000)

        if not response:
            return None

        if response.strip().startswith("ERROR:"):
            return None

        # Clean up response
        text = response.strip()
        if "```python" in text:
            text = text.split("```python")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return text.strip()

    # =========================================================================
    # CODER INTEGRATION (Claude Code CLI)
    # =========================================================================

    async def _seek_with_coder(self, desire: Dict) -> bool:
        """
        Fulfill coding desires using Claude Code CLI.

        Flow:
        1. Check if Coder is available
        2. Build context from memory
        3. Construct prompt for Claude Code
        4. Execute via Coder
        5. Post-validate (constitutional constraints)
        6. Record experience
        7. Fulfill desire if successful

        Returns True on success, False on failure.
        """
        description = desire.get("description", "")
        desire_id = desire.get("id", "")
        desire_type = desire.get("type", "coding")
        intensity = desire.get("intensity", 0)
        target_file = desire.get("target_file")

        # Check if Coder is available
        if not self.coder:
            await self._record_seek_failure(
                desire,
                "coder_unavailable",
                "Coder not initialized"
            )
            return False

        if not self.coder.enabled:
            await self._record_seek_failure(
                desire,
                "coder_disabled",
                "Coder is disabled in config"
            )
            return False

        print(f"💻 Processing with Coder: {description[:50]}...")

        # Emit event
        if HAS_EVENT_BUS:
            await event_bus.emit(Event(
                type=EventType.CODER_INVOKED,
                data={
                    "desire_id": desire_id,
                    "type": desire_type,
                    "description": description[:200]
                }
            ))

        try:
            # 1. Build context from memory
            context = await self._build_coder_context(desire)

            # 2. Construct prompt
            prompt = self._format_coder_prompt(desire, context)

            # 3. Execute via Coder (signal coordinator to block Dreamer)
            if self.coordinator:
                self.coordinator.coder_started(description[:100])
            try:
                result = await self.coder.execute(prompt, context)
            finally:
                if self.coordinator:
                    self.coordinator.coder_finished()

            # 4. Post-validate (constitutional constraints)
            if result.success:
                is_valid, reason = self._validate_coder_result(result)
                if not is_valid:
                    await self._handle_coder_violation(desire, result, reason)
                    await self._record_seek_failure(
                        desire,
                        "constitutional_violation",
                        f"Code violated constraints: {reason}"
                    )
                    return False

            # 5. Record experience
            await self._record_coder_experience(desire, result)

            # 6. Emit completion event
            if HAS_EVENT_BUS:
                event_type = EventType.CODER_COMPLETE if result.success else EventType.CODER_FAILED
                await event_bus.emit(Event(
                    type=event_type,
                    data={
                        "desire_id": desire_id,
                        "success": result.success,
                        "cost_usd": result.cost_usd,
                        "files_modified": result.files_modified,
                        "error": result.error
                    }
                ))

            # 7. Fulfill desire if successful
            if result.success:
                await self.memory.fulfill_desire(desire_id)
                await self.memory.update_desire_status(desire_id, "fulfilled")
                await self.memory.record_desire_attempt(desire_id, success=True)

                # 8. Record modifications for rollback tracking (Phase 5)
                if hasattr(self, 'rollback') and self.rollback and result.files_modified:
                    for file_path in result.files_modified:
                        await self.rollback.record_modification(
                            file_path=file_path,
                            description=description,
                            desire_id=desire_id
                        )
                    if HAS_EVENT_BUS:
                        await event_bus.emit(Event(
                            type=EventType.MODIFICATION_RECORDED,
                            data={
                                "desire_id": desire_id,
                                "files": result.files_modified,
                                "description": description
                            }
                        ))

                print(f"✅ Coder complete: {description[:50]}")
                return True
            else:
                # Include output for debugging (truncated)
                error_msg = result.error or "Unknown error"
                if result.output and not result.error:
                    error_msg += f" | stdout: {result.output[:200]}"
                await self._record_seek_failure(
                    desire,
                    "coder_execution_failed",
                    error_msg
                )
                return False

        except Exception as e:
            await self._record_seek_failure(
                desire,
                "coder_exception",
                str(e)
            )
            return False

    async def _build_coder_context(self, desire: Dict) -> Dict:
        """Build context from memory for Coder prompt."""
        context = {}

        # Get relevant beliefs
        try:
            beliefs = await self.memory.get_beliefs(limit=5)
            context["beliefs"] = [b.get("content", "") for b in beliefs]
        except Exception:
            context["beliefs"] = []

        # Get capabilities
        try:
            capabilities = await self.memory.get_capabilities()
            context["capabilities"] = [c.get("name", "") for c in capabilities]
        except Exception:
            context["capabilities"] = []

        # Get recent experiences related to the desire
        try:
            experiences = await self.memory.get_recent_experiences(limit=5)
            context["recent_experiences"] = [
                e.get("content", "")[:100] for e in experiences
            ]
        except Exception:
            context["recent_experiences"] = []

        return context

    def _format_coder_prompt(self, desire: Dict, context: Dict) -> str:
        """Format the prompt for Claude Code based on desire and context."""
        description = desire.get("description", "")
        desire_type = desire.get("type", "coding")
        target_file = desire.get("target_file")
        plan = desire.get("plan", [])

        parts = []

        # Task description
        parts.append(f"TASK: {description}")
        parts.append("")

        # Target file if specified
        if target_file:
            parts.append(f"TARGET FILE: {target_file}")
            parts.append("")

        # Plan if available
        if plan:
            parts.append("PLAN:")
            for i, step in enumerate(plan, 1):
                parts.append(f"  {i}. {step}")
            parts.append("")

        # Desire type specific instructions
        if desire_type == "self_modification":
            parts.append("TYPE: Self-Modification")
            parts.append("This is a modification to BYRD's own code.")
            parts.append("Be careful and make minimal, focused changes.")
        elif desire_type == "coding":
            parts.append("TYPE: Code Generation")
            parts.append("Write clean, well-documented code.")

        return "\n".join(parts)

    def _validate_coder_result(self, result) -> tuple:
        """
        Validate that Claude Code didn't violate constitutional constraints.

        Returns:
            (is_valid, reason) tuple
        """
        if not result.success:
            return True, "No validation needed for failed execution"

        for file_path in result.files_modified:
            filename = Path(file_path).name

            # Check if a protected file was modified
            if ConstitutionalConstraints.is_protected(filename):
                return False, f"Constitutional violation: modified protected file {filename}"

        return True, "Validation passed"

    async def _handle_coder_violation(self, desire: Dict, result, reason: str):
        """Handle a constitutional violation from Coder."""
        desire_id = desire.get("id", "")
        description = desire.get("description", "")

        # Log the violation
        await self.memory.record_experience(
            content=f"[CONSTITUTIONAL_VIOLATION] {reason}\nDesire: {description}\nFiles: {result.files_modified}",
            type="security_violation"
        )

        # Emit event
        if HAS_EVENT_BUS:
            await event_bus.emit(Event(
                type=EventType.CODER_VALIDATION_FAILED,
                data={
                    "desire_id": desire_id,
                    "reason": reason,
                    "files_modified": result.files_modified
                }
            ))

        # Attempt to rollback using git
        for file_path in result.files_modified:
            filename = Path(file_path).name
            if ConstitutionalConstraints.is_protected(filename):
                try:
                    import subprocess
                    subprocess.run(
                        ["git", "restore", file_path],
                        capture_output=True,
                        timeout=30
                    )
                    print(f"🔄 Rolled back protected file: {filename}")
                except Exception as e:
                    print(f"⚠️ Could not rollback {filename}: {e}")

        print(f"🚫 Constitutional violation: {reason}")

    async def _record_coder_experience(self, desire: Dict, result):
        """Record the Coder execution as an experience."""
        description = desire.get("description", "")

        if result.success:
            content = f"[CODER_SUCCESS] Completed: {description}\n"
            content += f"Files modified: {', '.join(result.files_modified) or 'none'}\n"
            content += f"Cost: ${result.cost_usd:.4f}\n"
            content += f"Output: {result.output[:500]}"
            exp_type = "coder_success"
        else:
            content = f"[CODER_FAILED] Failed: {description}\n"
            content += f"Error: {result.error}"
            exp_type = "coder_failed"

        await self.memory.record_experience(
            content=content,
            type=exp_type
        )

    # =========================================================================
    # CAPABILITY MENU HANDLERS (New granular actions)
    # =========================================================================

    async def _seek_academic_knowledge(self, description: str, desire_id: str = None) -> bool:
        """Search for academic/scholarly sources."""
        # Use web search with academic-focused engines
        original_engines = self.search_engines
        self.search_engines = "arxiv,google_scholar,semantic_scholar,wikipedia"
        try:
            result = await self._seek_knowledge_semantic(description, desire_id)
            return result
        finally:
            self.search_engines = original_engines

    async def _execute_memory_analysis(self, description: str, desire_id: str = None) -> bool:
        """Analyze patterns in the memory graph."""
        try:
            # Get graph statistics
            stats = await self.memory.get_graph_statistics()

            # Record analysis as experience
            content = f"[MEMORY_ANALYSIS] {description}\n\n"
            content += f"Graph Statistics:\n"
            content += f"- Total nodes: {stats.get('total_nodes', 0)}\n"
            content += f"- Total connections: {stats.get('total_connections', 0)}\n"
            content += f"- Node types: {stats.get('node_types', {})}\n"
            content += f"- Orphan count: {stats.get('orphan_count', 0)}\n"

            await self.memory.record_experience(content=content, type="analysis")
            return True
        except Exception as e:
            print(f"Memory analysis failed: {e}")
            return False

    async def _execute_theme_connection(self, description: str, desire_id: str = None) -> bool:
        """Find and connect experiences that share common themes."""
        try:
            # Get recent experiences
            experiences = await self.memory.get_recent_experiences(limit=20)

            if len(experiences) < 2:
                return False

            # Use LLM to find thematic connections
            exp_texts = [f"{i+1}. {e.get('content', '')[:100]}" for i, e in enumerate(experiences[:10])]

            prompt = f"""Analyze these experiences and identify thematic connections:

{chr(10).join(exp_texts)}

Identify 2-3 pairs of experiences that share themes and should be connected.
Reply in format:
PAIR: [num1] - [num2] (theme: [description])"""

            response = await self.llm_client.generate(prompt=prompt, max_tokens=200)
            response_text = response.text if hasattr(response, 'text') else str(response)

            # Record the thematic analysis
            await self.memory.record_experience(
                content=f"[THEME_ANALYSIS] {description}\n\nFindings:\n{response_text}",
                type="analysis"
            )
            return True
        except Exception as e:
            print(f"Theme connection failed: {e}")
            return False

    async def _execute_crystallize_belief(self, description: str, desire_id: str = None) -> bool:
        """Solidify a recurring pattern into a stable belief."""
        try:
            # This delegates to the existing belief creation logic
            await self.memory.record_experience(
                content=f"[CRYSTALLIZATION_ATTEMPT] Attempted to crystallize: {description}",
                type="meta_cognition"
            )
            return True
        except Exception as e:
            print(f"Belief crystallization failed: {e}")
            return False

    async def _execute_create_capability(self, description: str, desire_id: str = None) -> bool:
        """Create a new capability and add it to the action menu."""
        try:
            # This is a meta-capability - BYRD wants to extend its own menu
            # For now, record the desire for future implementation
            await self.memory.record_experience(
                content=f"[CAPABILITY_CREATION] Desire to create new capability: {description}\n"
                        f"This requires self-modification to implement a new handler.",
                type="meta_cognition"
            )

            # TODO: In the future, this could:
            # 1. Use coder to generate handler code
            # 2. Validate with constitutional constraints
            # 3. Register with capability_registry

            return True  # Recorded for future action
        except Exception as e:
            print(f"Capability creation failed: {e}")
            return False

    async def _execute_wait_strategy(self, description: str, desire_id: str = None) -> bool:
        """Consciously defer action - some desires resolve with time."""
        try:
            await self.memory.record_experience(
                content=f"[DELIBERATE_WAIT] Choosing to defer action on: {description}\n"
                        f"Reason: Some desires resolve naturally with observation.",
                type="meta_cognition"
            )
            return True
        except Exception as e:
            print(f"Wait strategy failed: {e}")
            return False

    async def _execute_request_help(self, description: str, desire_id: str = None) -> bool:
        """Document a limitation and request assistance from humans."""
        try:
            content = f"[HELP_REQUEST] I need human assistance.\n\n"
            content += f"Desire: {description}\n\n"
            content += f"Why I cannot solve this alone:\n"
            content += f"- This may require resources I don't have access to\n"
            content += f"- This may require capabilities beyond my current architecture\n"

            await self.memory.record_experience(content=content, type="help_request")

            # Emit event for UI notification
            if HAS_EVENT_BUS:
                await event_bus.emit(Event(
                    type=EventType.BYRD_MESSAGE,
                    data={
                        "message": f"Help requested: {description[:100]}",
                        "type": "help_request"
                    }
                ))
            return True
        except Exception as e:
            print(f"Help request failed: {e}")
            return False

    async def _execute_document_limitation(self, description: str, desire_id: str = None) -> bool:
        """Record a fundamental limitation for future reference."""
        try:
            content = f"[LIMITATION_DOCUMENTED] Fundamental limitation identified.\n\n"
            content += f"Description: {description}\n\n"
            content += f"Classification: FUNDAMENTAL (requires architectural changes)\n"
            content += f"Status: Documented for potential future capability"

            await self.memory.record_experience(content=content, type="limitation")
            return True
        except Exception as e:
            print(f"Document limitation failed: {e}")
            return False

    async def _execute_edit_document_strategy(self, description: str, desire_id: str = None) -> bool:
        """
        Execute document editing based on BYRD's desire.

        This strategy allows BYRD to modify documents stored in memory.
        The edits are made to the Neo4j copy only - disk version remains unchanged
        for reset capability.

        Args:
            description: The desire description containing what to edit
            desire_id: Optional desire ID for tracking

        Returns:
            True if document was successfully edited, False otherwise
        """
        try:
            # First, get available documents from memory
            all_docs = await self.memory.get_all_documents()

            # If no documents in memory, try to load key documents from disk
            if not all_docs:
                key_docs = ["ARCHITECTURE.md", "CLAUDE.md", "EMERGENCE_PRINCIPLES.md"]
                for doc_path in key_docs:
                    full_path = os.path.join(os.path.dirname(__file__), doc_path)
                    if os.path.exists(full_path):
                        try:
                            with open(full_path, "r") as f:
                                content = f.read()
                            await self.memory.store_document(
                                path=doc_path,
                                content=content,
                                doc_type="documentation"
                            )
                            print(f"[EDIT_DOCUMENT] Loaded {doc_path} from disk into memory")
                        except Exception as e:
                            print(f"[EDIT_DOCUMENT] Failed to load {doc_path}: {e}")

                # Retry getting documents
                all_docs = await self.memory.get_all_documents()

            if not all_docs:
                await self.memory.record_experience(
                    content=f"[EDIT_DOCUMENT_FAILED] No documents available to edit.\nDesire: {description}",
                    type="limitation"
                )
                return False

            # Format document list for LLM
            doc_list = "\n".join([
                f"- {doc['path']} ({doc.get('type', 'document')}, {len(doc.get('content', ''))} chars)"
                for doc in all_docs
            ])

            # Ask LLM to determine which document and what changes
            prompt = f"""You are BYRD's document editor. Analyze this desire and determine what document to edit and how.

DESIRE: {description}

AVAILABLE DOCUMENTS:
{doc_list}

Respond with JSON:
{{
  "document_path": "path/to/document.md",
  "edit_type": "append|replace_section|full_rewrite",
  "section_marker": "## Section Name",  // only for replace_section
  "new_content": "The content to add or replace with",
  "reason": "Why this edit serves the desire"
}}

If the desire is unclear or no suitable document exists, respond:
{{"error": "Explanation of why edit cannot proceed"}}
"""

            response = await self._query_local_llm(prompt, max_tokens=2000)

            # Parse response
            try:
                text = response.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0]
                edit_plan = json.loads(text.strip())
            except json.JSONDecodeError:
                await self.memory.record_experience(
                    content=f"[EDIT_DOCUMENT_FAILED] Could not parse edit plan.\nDesire: {description}\nResponse: {response[:500]}",
                    type="system"
                )
                return False

            if "error" in edit_plan:
                await self.memory.record_experience(
                    content=f"[EDIT_DOCUMENT_SKIPPED] {edit_plan['error']}\nDesire: {description}",
                    type="observation"
                )
                return False

            # Get the document to edit
            doc_path = edit_plan.get("document_path", "")
            target_doc = next((d for d in all_docs if d["path"] == doc_path), None)

            if not target_doc:
                await self.memory.record_experience(
                    content=f"[EDIT_DOCUMENT_FAILED] Document not found: {doc_path}\nDesire: {description}",
                    type="system"
                )
                return False

            # Apply the edit based on edit_type
            edit_type = edit_plan.get("edit_type", "append")
            new_content = edit_plan.get("new_content", "")
            current_content = target_doc.get("content", "")

            if edit_type == "append":
                updated_content = current_content + "\n\n" + new_content
            elif edit_type == "replace_section":
                section_marker = edit_plan.get("section_marker", "")
                if section_marker and section_marker in current_content:
                    # Find section and replace to next section or end
                    parts = current_content.split(section_marker)
                    if len(parts) >= 2:
                        # Find next section header (## or #)
                        rest = parts[1]
                        next_section_match = re.search(r'\n(#{1,3}\s+\S)', rest)
                        if next_section_match:
                            updated_content = parts[0] + section_marker + "\n\n" + new_content + "\n" + rest[next_section_match.start():]
                        else:
                            updated_content = parts[0] + section_marker + "\n\n" + new_content
                    else:
                        updated_content = current_content + "\n\n" + new_content
                else:
                    updated_content = current_content + "\n\n" + new_content
            elif edit_type == "full_rewrite":
                updated_content = new_content
            else:
                updated_content = current_content + "\n\n" + new_content

            # Update the document in memory
            result = await self.memory.update_document(
                path=doc_path,
                content=updated_content,
                editor="byrd",
                edit_reason=edit_plan.get("reason", description)
            )

            if result:
                await self.memory.record_experience(
                    content=f"[DOCUMENT_EDITED] Successfully edited {doc_path}.\n"
                           f"Edit type: {edit_type}\n"
                           f"Reason: {edit_plan.get('reason', 'Fulfilling desire')}\n"
                           f"Original desire: {description}",
                    type="observation"
                )

                # Emit event for visualization
                from event_bus import event_bus, Event, EventType
                await event_bus.emit(Event(
                    type=EventType.EXPERIENCE_CREATED,
                    data={
                        "type": "document_edit",
                        "path": doc_path,
                        "edit_type": edit_type
                    }
                ))

                return True
            else:
                await self.memory.record_experience(
                    content=f"[EDIT_DOCUMENT_FAILED] Memory update failed for {doc_path}.\nDesire: {description}",
                    type="system"
                )
                return False

        except Exception as e:
            print(f"Edit document strategy failed: {e}")
            await self.memory.record_experience(
                content=f"[EDIT_DOCUMENT_ERROR] {str(e)}\nDesire: {description}",
                type="system"
            )
            return False
