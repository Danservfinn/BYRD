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

        # Timing
        self.interval = config.get("interval_seconds", 60)
        self.context_window = config.get("context_window", 50)

        # State
        self._running = False
        self._dream_count = 0

        # Track BYRD's emerging vocabulary
        self._observed_keys: Dict[str, int] = {}  # key -> count

        # Queue of BYRD's inner voices for narrator (max 10)
        self._inner_voice_queue: deque = deque(maxlen=10)
    
    async def run(self):
        """Main dream loop - runs forever."""
        self._running = True
        print("💭 Dreamer starting...")
        
        while self._running:
            try:
                await self._dream_cycle()
            except Exception as e:
                print(f"💭 Dream error: {e}")
            
            await asyncio.sleep(self.interval)
    
    def stop(self):
        self._running = False

    def reset(self):
        """Reset dreamer state for fresh start."""
        self._running = False
        self._dream_count = 0
        self._observed_keys = {}

    async def _dream_cycle(self):
        """One complete dream cycle: recall, reflect, record."""
        self._dream_count += 1

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

        # 2. REFLECT - Ask local LLM to reflect (minimal, unbiased prompt)
        reflection_output = await self._reflect(
            recent, related, capabilities, previous_reflections
        )

        if not reflection_output:
            return

        # 3. RECORD - Store reflection in BYRD's own vocabulary
        await self._record_reflection(reflection_output, recent_ids)

        # Extract any inner voice for UI (using whatever key BYRD chose)
        inner_voice = self._extract_inner_voice(reflection_output)

        # Add to narrator queue if we got something
        if inner_voice:
            self._inner_voice_queue.append(inner_voice)

        # Count what BYRD produced (without forcing categories)
        output_keys = list(reflection_output.get("output", {}).keys()) if isinstance(reflection_output.get("output"), dict) else []

        # Emit end event
        await event_bus.emit(Event(
            type=EventType.DREAM_CYCLE_END,
            data={
                "cycle": self._dream_count,
                "output_keys": output_keys,
                "inner_voice": inner_voice
            }
        ))

        print(f"💭 Dream #{self._dream_count}: keys={output_keys}")
    
    async def _reflect(
        self,
        recent: List[Dict],
        related: List[Dict],
        capabilities: List[Dict],
        previous_reflections: List[Dict]
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

        # MINIMAL PROMPT - pure data presentation, no guidance
        prompt = f"""EXPERIENCES:
{recent_text}

RELATED MEMORIES:
{related_text}

AVAILABLE CAPABILITIES:
{caps_text}

{f"PREVIOUS REFLECTIONS:{chr(10)}{prev_text}" if prev_text else ""}

Output JSON with a single "output" field containing whatever you want to record."""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=500  # Reduced for faster qwen3 response
            )

            # Debug: log raw response for troubleshooting
            raw_text = response.text
            if not raw_text:
                print(f"💭 Empty response from LLM")
                return None

            # Try to parse JSON
            result = self.llm_client.parse_json_response(raw_text)
            if result is None:
                # JSON parse failed - try to extract useful content anyway
                print(f"💭 JSON parse failed, raw response starts with: {raw_text[:200]}")
                # Wrap raw text as output if it's not JSON
                return {"output": raw_text.strip()}

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

        # If output is a string, that's BYRD's voice
        if isinstance(output, str) and output.strip():
            return output[:200]

        if not isinstance(output, dict):
            return ""

        # Check for common voice-like keys (but don't prescribe them)
        voice_candidates = [
            "inner_voice", "voice", "thinking", "thoughts", "inner",
            "feeling", "expressing", "saying", "musing", "wondering"
        ]

        for key in voice_candidates:
            if key in output:
                val = output[key]
                if isinstance(val, str):
                    return val[:200]
                elif isinstance(val, list) and val:
                    return str(val[0])[:200]

        # If no voice key found, return empty - that's fine
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

    def _summarize_reflection(self, output: Any) -> str:
        """Create a brief summary of the reflection for the experience stream."""
        if not isinstance(output, dict):
            return str(output)[:200] if output else ""

        parts = []
        for key, value in list(output.items())[:3]:
            if isinstance(value, str):
                parts.append(f"{key}: {value[:50]}")
            elif isinstance(value, list) and value:
                parts.append(f"{key}: [{len(value)} items]")
            elif isinstance(value, dict):
                parts.append(f"{key}: {{...}}")

        return "; ".join(parts)[:200]

    def get_observed_vocabulary(self) -> Dict[str, int]:
        """Return the vocabulary BYRD has developed in its reflections."""
        return self._observed_keys.copy()

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
