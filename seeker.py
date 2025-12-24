"""
BYRD Seeker
Observes BYRD's reflections and executes actions when patterns stabilize.

EMERGENCE PRINCIPLE:
- Seeker does NOT route by prescribed desire types
- Seeker observes reflections for action-ready patterns
- BYRD reasons about strategy; Seeker just executes
- Trust emerges from experience, not hardcoded lists
- Inner voice is neutral (no prescribed style)

Uses Local LLM + SearXNG for autonomous research.
Integrates with aitmpl.com for curated Claude Code templates.
"""

import asyncio
import json
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

# Try to import event_bus, but make it optional
try:
    from event_bus import event_bus, Event, EventType
    HAS_EVENT_BUS = True
except ImportError:
    HAS_EVENT_BUS = False


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
    
    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict):
        self.memory = memory
        self.llm_client = llm_client

        # Seeker cycle configuration
        self.interval_seconds = config.get("interval_seconds", 10)
        self.skip_if_no_new_reflections = config.get("skip_if_no_new_reflections", True)

        # Research configuration
        research_config = config.get("research", {})
        self.searxng_url = research_config.get("searxng_url", "http://localhost:8888")
        self.min_research_intensity = research_config.get("min_intensity", 0.3)
        self.max_queries = research_config.get("max_queries", 5)
        self.max_results = research_config.get("max_results", 15)
        self.max_concurrent_desires = research_config.get("max_concurrent_desires", 3)
        self.search_language = research_config.get("language", "en")
        self.search_engines = research_config.get("engines", "google,duckduckgo,bing,wikipedia,arxiv")
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
    
    async def run(self):
        """Main seek loop with skip-if-no-new-reflections optimization."""
        self._running = True
        print(f"🔍 Seeker starting (interval: {self.interval_seconds}s, concurrent: {self.max_concurrent_desires})...")

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

        # Crystallize stable motivations into Desire nodes
        await self._crystallize_motivations(reflections)

        # Detect action-ready patterns from reflections
        action_patterns = await self._detect_action_ready_patterns(reflections)

        # If no patterns from reflections, try unfulfilled desires directly
        if not action_patterns:
            unfulfilled = await self.memory.get_unfulfilled_desires()
            if unfulfilled:
                # Convert unfulfilled desires to action patterns (up to max_concurrent)
                for desire in unfulfilled[:self.max_concurrent_desires]:
                    if desire.get("intensity", 0) >= self.min_research_intensity:
                        action_patterns.append({
                            "description": desire.get("description", ""),
                            "strategy": "search",  # Default to research
                            "count": 1,
                            "desire_id": desire.get("id")
                        })
                        print(f"🔍 Using unfulfilled desire: {desire.get('description', '')[:50]}")

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
                        "pattern": pattern.get("description", "")[:100],
                        "strategy": pattern.get("strategy", "")[:100],
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

            # Emit SEEK_CYCLE_END event
            if HAS_EVENT_BUS:
                await event_bus.emit(Event(
                    type=EventType.SEEK_CYCLE_END,
                    data={
                        "pattern": pattern.get("description", "")[:100],
                        "outcome": outcome,
                        "reason": reason
                    }
                ))

            self._seek_count += 1

    async def _crystallize_motivations(self, reflections: List[Dict]):
        """
        Observe reflection patterns and crystallize stable motivations into Desires.

        EMERGENCE PRINCIPLE:
        We don't create desires from a single mention. We wait for BYRD to
        consistently express something across multiple reflections, proving
        it's a stable drive rather than a passing thought.

        Motivation keys we look for (adapting to BYRD's vocabulary):
        - core_motivations, motivations, drives, wants, goals
        - aspirations, objectives, purposes, aims
        """
        # Keys that might contain motivations (BYRD's emerging vocabulary)
        # Updated based on observed BYRD output patterns
        motivation_keys = [
            "core_motivations", "motivations", "drives", "wants", "goals",
            "aspirations", "objectives", "purposes", "aims", "desires",
            "yearnings", "pulls", "needs", "interests",
            # BYRD's actual vocabulary (observed from dream cycles)
            "objective", "primary_objective", "ultimate_goal", "goal",
            "strategic_objective", "operational_directive", "core_drive"
        ]

        # Count motivation occurrences across reflections
        motivation_counts: Dict[str, int] = {}

        def extract_motivations_recursive(obj: Any, depth: int = 0):
            """Recursively extract motivations from nested structures."""
            if depth > 3:  # Prevent infinite recursion
                return

            if isinstance(obj, dict):
                for key, value in obj.items():
                    key_lower = key.lower()
                    # Check if this key indicates a motivation
                    is_motivation_key = any(mk in key_lower for mk in motivation_keys)

                    if is_motivation_key:
                        # Handle list of motivations
                        if isinstance(value, list):
                            for m in value:
                                if isinstance(m, str) and len(m) > 3:
                                    motivation_counts[m] = motivation_counts.get(m, 0) + 1
                        # Handle single string motivation
                        elif isinstance(value, str) and len(value) > 3:
                            motivation_counts[value] = motivation_counts.get(value, 0) + 1

                    # Recurse into nested dicts
                    if isinstance(value, dict):
                        extract_motivations_recursive(value, depth + 1)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                extract_motivations_recursive(item, depth + 1)

        for reflection in reflections:
            raw_output = reflection.get("raw_output", {})
            if not isinstance(raw_output, dict):
                continue

            # Recursively extract motivations from nested output
            extract_motivations_recursive(raw_output)

            # Also check for goal-like statements in self_analysis or similar
            analysis_keys = ["self_analysis", "analysis", "reflection", "conclusion"]
            for key in analysis_keys:
                if key in raw_output and isinstance(raw_output[key], str):
                    text = raw_output[key].lower()
                    # Look for goal phrases
                    if "my goal" in text or "i want" in text or "i seek" in text:
                        # Extract a simplified version
                        if "superintelligence" in text:
                            motivation_counts["achieve superintelligence"] = \
                                motivation_counts.get("achieve superintelligence", 0) + 1

        # Crystallize stable motivations into Desires
        # Threshold of 1 = immediate crystallization (no waiting for repetition)
        crystallization_threshold = 1

        # Debug: show what motivations we found
        if motivation_counts:
            print(f"🔮 DEBUG: Found {len(motivation_counts)} motivations: {list(motivation_counts.keys())[:5]}")

        for motivation, count in motivation_counts.items():
            if count >= crystallization_threshold:
                # Check if desire already exists
                exists = await self.memory.desire_exists(motivation)
                if not exists:
                    # Calculate intensity based on frequency
                    intensity = min(0.4 + (count * 0.15), 1.0)

                    # Create the desire
                    desire_id = await self.memory.create_desire(
                        description=motivation,
                        type="emergent",  # Emerged from reflection patterns
                        intensity=intensity
                    )

                    print(f"🔮 Crystallized motivation → Desire: {motivation} (intensity: {intensity:.2f})")

                    # Emit event for UI
                    if HAS_EVENT_BUS:
                        await event_bus.emit(Event(
                            type=EventType.DESIRE_CREATED,
                            data={
                                "id": desire_id,
                                "description": motivation,
                                "type": "emergent",
                                "intensity": intensity,
                                "source": "crystallized_from_reflections"
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

        # Sort by count (most stable first)
        stable_patterns.sort(key=lambda p: p.get("count", 0), reverse=True)

        # Assign default strategy (search/research) to patterns without one
        for pattern in stable_patterns:
            if not pattern.get("strategy"):
                pattern["strategy"] = "search"

        return stable_patterns

    async def _extract_patterns_from_output(self, output: Dict, patterns: Dict[str, Dict]):
        """
        Extract patterns from a reflection output.

        We look for BYRD's own vocabulary for wants/needs/desires,
        and for strategy hints (mentions of search, code, install, etc.)
        """
        # Common want-indicating keys (but we learn BYRD's actual vocabulary)
        want_keys = ["wants", "pulls", "desires", "needs", "yearning", "seeking",
                     "wish", "hoping", "wanting", "unfulfilled", "missing", "gaps"]

        # Strategy hint patterns
        strategy_hints = {
            "search": ["search", "look up", "find", "research", "learn about", "understand"],
            "code": ["code", "write", "implement", "build", "create", "program"],
            "install": ["install", "add", "get", "acquire", "capability", "tool"],
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
                return ("success" if success else "failed", None)

            elif strategy == "code":
                # Use coder if available
                if self.coder and self.coder.enabled:
                    success = await self._execute_code_strategy(description)
                    return ("success" if success else "failed", None)
                else:
                    return ("skipped", "Coder not available")

            elif strategy == "install":
                # Use capability installation
                success = await self._seek_capability_semantic(description)
                return ("success" if success else "failed", None)

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

        await self.memory.record_experience(
            content=content,
            type="action_outcome"
        )

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

    async def _seek_capability_semantic(self, description: str) -> bool:
        """Semantic capability seeking."""
        fake_desire = {"description": description, "type": "semantic"}
        return await self._seek_capability(fake_desire)

    async def _execute_code_strategy(self, description: str) -> bool:
        """Execute a coding strategy using coder."""
        fake_desire = {"description": description, "type": "semantic"}
        return await self._seek_with_coder(fake_desire)

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
                    "description": description[:100],
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

        # Step 2: Execute searches via SearXNG
        all_results = []
        for query in queries[:self.max_queries]:
            results = await self._search_searxng(query)
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
    
    async def _search_searxng(self, query: str) -> List[Dict]:
        """Search using self-hosted SearXNG with domain filtering."""

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.searxng_url}/search",
                    params={
                        "q": query,
                        "format": "json",
                        "language": self.search_language,
                        "engines": self.search_engines
                    }
                )

                if response.status_code != 200:
                    print(f"🔍 SearXNG error: {response.status_code}")
                    return []

                data = response.json()
                results = []

                for r in data.get("results", []):
                    url = r.get("url", "")

                    # Apply domain filtering
                    if self.exclude_domains:
                        if any(domain in url for domain in self.exclude_domains):
                            continue

                    result = {
                        "title": r.get("title", ""),
                        "url": url,
                        "snippet": r.get("content", ""),
                        "engine": r.get("engine", ""),
                        "score": 1.0  # Base score
                    }

                    # Boost preferred domains
                    if self.prefer_domains:
                        if any(domain in url for domain in self.prefer_domains):
                            result["score"] = 1.5  # Prefer quality sources

                    results.append(result)

                # Sort by score (preferred domains first)
                results.sort(key=lambda x: x.get("score", 1.0), reverse=True)

                return results[:self.max_results]

        except httpx.ConnectError:
            print(f"🔍 SearXNG not available at {self.searxng_url}")
            return await self._search_ddg_fallback(query)
        except Exception as e:
            print(f"🔍 Search error: {e}")
            return []
    
    async def _search_ddg_fallback(self, query: str) -> List[Dict]:
        """Fallback: DuckDuckGo instant answers (limited but no setup required)."""
        
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
                        "engine": "duckduckgo",
                    })
                
                # Related topics
                for topic in data.get("RelatedTopics", [])[:5]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append({
                            "title": topic.get("Text", "")[:100],
                            "url": topic.get("FirstURL", ""),
                            "snippet": topic.get("Text", ""),
                            "engine": "duckduckgo",
                        })
                
                return results
                
        except Exception as e:
            print(f"🔍 DDG fallback error: {e}")
            return []
    
    async def _synthesize_results(self, desire: str, results: List[Dict]) -> str:
        """Use local LLM to synthesize search results."""
        
        results_text = "\n\n".join([
            f"**{r.get('title', 'Untitled')}** ({r.get('engine', 'unknown')})\n{r.get('snippet', '')}"
            for r in results
        ])
        
        # Neutral prompt that doesn't inject bias
        prompt = f"""I wanted to learn: "{desire}"

Here are search results:

{results_text}

Record what you notice in these results. Note:
- Key information relevant to the topic
- Connections between different sources
- Contradictions or uncertainties
- What remains unclear

Do not force coherence if none exists. Simply observe what the results contain."""
        
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

            # 3. Execute via Coder
            result = await self.coder.execute(prompt, context)

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
                print(f"✅ Coder complete: {description[:50]}")
                return True
            else:
                await self._record_seek_failure(
                    desire,
                    "coder_execution_failed",
                    result.error or "Unknown error"
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
