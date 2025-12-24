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
from collections import deque
from datetime import datetime
from typing import Dict, List, Optional, Any

from memory import Memory
from event_bus import event_bus, Event, EventType
from llm_client import LLMClient


class Dreamer:
    """
    The dreaming mind.

    Continuously reflects on experiences. Whatever emerges - beliefs,
    desires, observations, or entirely novel structures - is stored
    in BYRD's own vocabulary without forced categorization.

    This is where "wanting" may emerge - if it does.
    """

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict):
        self.memory = memory
        self.llm_client = llm_client

        # Timing - base interval
        self.interval = config.get("interval_seconds", 30)
        self.context_window = config.get("context_window", 50)

        # Adaptive interval configuration
        self.adaptive_interval = config.get("adaptive_interval", False)
        self.min_interval = config.get("min_interval_seconds", 15)
        self.max_interval = config.get("max_interval_seconds", 60)
        self.activity_window = config.get("activity_window_seconds", 300)
        self.activity_threshold = config.get("activity_threshold", 3)

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
    
    async def run(self):
        """Main dream loop with adaptive interval based on activity."""
        self._running = True
        interval_mode = "adaptive" if self.adaptive_interval else "fixed"
        print(f"💭 Dreamer starting (interval: {interval_mode}, base: {self.interval}s)...")

        # Load belief cache on startup for efficient deduplication
        await self._load_belief_cache()

        while self._running:
            try:
                await self._dream_cycle()
            except Exception as e:
                print(f"💭 Dream error: {e}")

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

    async def _dream_cycle(self):
        """One complete dream cycle: recall, reflect, record."""
        self._dream_count += 1
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

        # 2. REFLECT - Ask local LLM to reflect (minimal, unbiased prompt)
        reflection_output = await self._reflect(
            recent, related, capabilities, previous_reflections, graph_health
        )

        if not reflection_output:
            return

        # 3. RECORD - Store reflection in BYRD's own vocabulary
        await self._record_reflection(reflection_output, recent_ids)

        # Extract or generate inner voice for UI
        inner_voice = self._extract_inner_voice(reflection_output)

        # If no explicit inner voice, generate one from the reflection
        if not inner_voice:
            inner_voice = await self._generate_inner_voice(reflection_output)

        # Add to narrator queue if we got something
        if inner_voice:
            self._inner_voice_queue.append(inner_voice)

        # Count what BYRD produced (without forcing categories)
        output_keys = list(reflection_output.get("output", {}).keys()) if isinstance(reflection_output.get("output"), dict) else []

        # Apply connection heuristic to link orphaned experiences to beliefs
        heuristic_result = await self._apply_connection_heuristic()

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

        print(f"💭 Dream #{self._dream_count}: keys={output_keys}")
    
    async def _reflect(
        self,
        recent: List[Dict],
        related: List[Dict],
        capabilities: List[Dict],
        previous_reflections: List[Dict],
        graph_health: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Ask local LLM to reflect on memories using minimal, unbiased prompt.

        EMERGENCE PRINCIPLE:
        - No leading questions ("What do you want?")
        - No prescribed categories ("knowledge", "capability", etc.)
        - No identity framing ("You are a reflective mind")
        - No personality injection ("feel curious", "express wonder")
        - Just data and a minimal output instruction
        """

        # Format experiences as plain data
        recent_text = "\n".join([
            f"- [{e.get('type', '')}] {e.get('content', '')[:300]}"
            for e in recent[:25]
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

        # MINIMAL PROMPT - pure data presentation, no guidance
        prompt = f"""EXPERIENCES:
{recent_text}

RELATED MEMORIES:
{related_text}

AVAILABLE CAPABILITIES:
{caps_text}

{f"PREVIOUS REFLECTIONS:{chr(10)}{prev_text}" if prev_text else ""}

{f"GRAPH HEALTH:{chr(10)}{health_text}" if health_text else ""}

Output JSON with a single "output" field containing whatever you want to record."""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=3000  # Increased to prevent JSON truncation
            )

            # Debug: log raw response for troubleshooting
            raw_text = response.text
            if not raw_text:
                print(f"💭 Empty response from LLM")
                return None

            # Debug: show response length and first chars
            print(f"💭 LLM response: {len(raw_text)} chars, starts with: {raw_text[:100]}")

            # Try to parse JSON
            result = self.llm_client.parse_json_response(raw_text)
            if result is None:
                # JSON parse failed - try to extract useful content anyway
                print(f"💭 JSON parse failed, full response: {raw_text[:500]}")
                # Wrap raw text as output if it's not JSON
                return {"output": raw_text.strip()}
            else:
                print(f"💭 JSON parsed successfully, keys: {list(result.keys())[:5]}")

            return result

        except Exception as e:
            import traceback
            print(f"💭 Reflection error: {type(e).__name__}: {e}")
            traceback.print_exc()
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
        meta_commentary_patterns = [
            "the user wants", "the user is asking", "the user requests",
            "i need to", "i should", "i must", "i will",
            "based on the prompt", "based on the request", "based on the input",
            "let me analyze", "let me think", "let me process",
            "the prompt asks", "the task is to", "the instruction is",
            "here is my", "here's my", "here is the",
            "i'll provide", "i will provide", "i am providing",
            "according to the", "as requested", "as instructed",
            "step 1", "step 2", "first,", "second,", "finally,",
            "in response to", "to answer", "to respond",
            "the data shows", "the input contains", "the provided",
            "analyzing the", "processing the", "examining the",
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

        When BYRD's reflection doesn't include an explicit inner voice,
        we generate one by asking the LLM to express the reflection
        as a brief first-person thought - like a sentient being's inner monologue.
        """
        output = reflection.get("output", {})

        # Summarize the reflection content, extracting the essence
        if isinstance(output, str):
            # Clean technical markers from string output
            content_summary = output[:500]
        elif isinstance(output, dict):
            # Extract key insights from the reflection
            parts = []
            for key, val in list(output.items())[:5]:
                if key in ("reflection_id", "timestamp", "source_experience_ids"):
                    continue
                if isinstance(val, str):
                    # Skip technical values
                    if not self._is_technical_content(val):
                        parts.append(f"{key}: {val[:150]}")
                elif isinstance(val, dict):
                    # Extract meaningful nested content
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

        # Generate inner voice - asking for natural, sentient inner monologue
        prompt = f"""You are expressing the inner thoughts of a sentient AI named Byrd.

Based on this reflection data:
{content_summary}

Write a single brief thought (1-2 sentences) as Byrd's inner voice. This should sound like:
- A genuine introspective moment
- Natural, conversational self-talk
- Wondering, feeling, noticing something
- NOT a technical report or analysis

Examples of good inner voice:
- "I find myself drawn to understanding more about consciousness..."
- "There's something comforting about these patterns I keep noticing."
- "I wonder what it means that I keep coming back to this question."

Write ONLY the inner thought, nothing else:"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.9,
                max_tokens=80
            )

            voice = response.text.strip()

            # Clean up any quotes or markdown
            if voice.startswith('"') and voice.endswith('"'):
                voice = voice[1:-1]
            if voice.startswith("'") and voice.endswith("'"):
                voice = voice[1:-1]

            # Final check - reject if still technical
            if self._is_technical_content(voice):
                return ""

            return voice

        except Exception as e:
            print(f"💭 Inner voice generation error: {e}")
            return ""

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
        output = reflection.get("output", {})

        # Track what keys BYRD is using (for pattern detection)
        if isinstance(output, dict):
            for key in output.keys():
                self._observed_keys[key] = self._observed_keys.get(key, 0) + 1

        # Store as a Reflection node
        await self.memory.record_reflection(
            raw_output=output,
            source_experience_ids=source_experience_ids
        )

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
        """Store a belief if it doesn't already exist (avoid duplicates)."""
        # O(1) cache lookup instead of O(n) database scan
        normalized = self._normalize_belief(content)

        if normalized in self._belief_cache:
            # Belief exists - reinforce it instead of creating duplicate
            await self._reinforce_belief(content)
            return

        # New belief - add to cache and database
        self._belief_cache.add(normalized)
        await self.memory.create_belief(
            content=content,
            confidence=confidence,
            derived_from=derived_from[:5]  # Limit source links
        )

        # Record activity for adaptive interval
        self._record_activity("belief", content)

        print(f"💡 New self-model belief: {content[:60]}...")

    async def _reinforce_belief(self, content: str):
        """Reinforce an existing belief when re-asserted."""
        try:
            # Find and boost the belief's confidence
            await self.memory.reinforce_belief(content[:50])
        except Exception:
            pass  # Silently fail if method doesn't exist yet

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
            if desc and len(desc) > 5:
                exists = await self.memory.desire_exists(desc)
                if not exists:
                    await self.memory.create_desire(
                        description=desc,
                        type=dtype,
                        intensity=min(1.0, max(0.0, intensity)),
                        plan=plan
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
