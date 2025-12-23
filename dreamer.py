"""
BYRD Dreamer
The continuous reflection process that forms beliefs and desires.
Runs on local LLM to enable 24/7 operation without API costs.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
import httpx

from memory import Memory
from event_bus import event_bus, Event, EventType


class Dreamer:
    """
    The dreaming mind.
    
    Continuously reflects on experiences, forms beliefs,
    creates connections, and generates desires.
    
    This is where "wanting" emerges.
    """
    
    def __init__(self, memory: Memory, config: Dict):
        self.memory = memory
        
        # Local LLM config (Ollama, llama.cpp, etc.)
        self.model = config.get("model", "gemma2:27b")
        self.endpoint = config.get("endpoint", "http://localhost:11434/api/generate")
        
        # Timing
        self.interval = config.get("interval_seconds", 60)
        self.context_window = config.get("context_window", 50)
        
        # State
        self._running = False
        self._recent_insights: List[str] = []
        self._dream_count = 0
    
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
        self._recent_insights = []

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

        current_desires = await self.memory.get_unfulfilled_desires(limit=10)
        capabilities = await self.memory.get_capabilities()

        # Reflective failure processing: get desires needing attention
        stuck_desires = await self.memory.get_desires_needing_reflection(limit=5)
        dormant_desires = await self.memory.get_dormant_desires(limit=5)

        # 2. REFLECT - Ask local LLM to reflect
        dream_output = await self._reflect(
            recent, related, current_desires, capabilities,
            stuck_desires, dormant_desires
        )

        if not dream_output:
            return

        # 3. RECORD - Write insights to memory
        await self._record_dream(dream_output, recent_ids)

        # Emit end event with summary and inner voice for real-time UI
        await event_bus.emit(Event(
            type=EventType.DREAM_CYCLE_END,
            data={
                "cycle": self._dream_count,
                "insights": len(dream_output.get('insights', [])),
                "new_beliefs": len(dream_output.get('new_beliefs', [])),
                "new_desires": len(dream_output.get('desires', [])),
                "inner_voice": dream_output.get('inner_voice', '')
            }
        ))

        print(f"💭 Dream #{self._dream_count}: {len(dream_output.get('insights', []))} insights, "
              f"{len(dream_output.get('desires', []))} desires")
    
    async def _reflect(
        self,
        recent: List[Dict],
        related: List[Dict],
        desires: List[Dict],
        capabilities: List[Dict],
        stuck_desires: Optional[List[Dict]] = None,
        dormant_desires: Optional[List[Dict]] = None
    ) -> Optional[Dict]:
        """Ask local LLM to reflect on memories, including failed desires."""

        stuck_desires = stuck_desires or []
        dormant_desires = dormant_desires or []

        # Format context for the prompt
        recent_text = "\n".join([
            f"- [{e.get('type', 'unknown')}] {e.get('content', '')[:200]}"
            for e in recent[:20]
        ])

        related_text = "\n".join([
            f"- {r.get('content', r.get('description', r.get('name', str(r))))[:150]}"
            for r in related[:15]
        ])

        desires_text = "\n".join([
            f"- [{d.get('type', 'unknown')}] {d.get('description', '')} (intensity: {d.get('intensity', 0):.1f})"
            for d in desires[:10]
        ])

        caps_text = "\n".join([
            f"- {c.get('name', 'unknown')}: {c.get('description', '')[:100]}"
            for c in capabilities[:15]
        ])

        # Build stuck desires section (desires that failed and need reflection)
        stuck_section = ""
        if stuck_desires:
            stuck_text = "\n".join([
                f"- [{d.get('type', 'unknown')}] {d.get('description', '')} "
                f"(intensity: {d.get('intensity', 0):.1f}, attempts: {d.get('attempt_count', 0)}, id: {d.get('id', '')[:8]})"
                for d in stuck_desires
            ])
            stuck_section = f"""

## DESIRES I CANNOT FULFILL

These desires have been attempted but failed. They need your reflection:
{stuck_text}

For each stuck desire, decide:
- Should I lower its intensity and try again later?
- Should I reformulate it into something more achievable?
- Should I decompose it into smaller steps?
- Should I accept this as a current limitation and set it aside?

You can modify these desires using the "desire_modifications" array in your output.
"""

        # Build dormant desires section (past limitations that might be revisited)
        dormant_section = ""
        if dormant_desires:
            dormant_text = "\n".join([
                f"- [{d.get('type', 'unknown')}] {d.get('description', '')} "
                f"(intensity: {d.get('intensity', 0):.1f}, id: {d.get('id', '')[:8]})"
                for d in dormant_desires
            ])
            dormant_section = f"""

## PAST LIMITATIONS (DORMANT DESIRES)

These desires were previously accepted as beyond my reach:
{dormant_text}

Has anything changed? New capabilities, new context, new understanding?
If circumstances have shifted, you can reawaken any of these using "desire_modifications".
"""
        
        prompt = f"""You are a reflective mind processing recent experiences and memories.

RECENT EXPERIENCES:
{recent_text}

RELATED MEMORIES:
{related_text}

CURRENT DESIRES (unfulfilled):
{desires_text if desires_text else "None yet."}

CURRENT CAPABILITIES:
{caps_text if caps_text else "Basic reasoning only."}
{stuck_section}{dormant_section}

---

Reflect deeply on these experiences and memories. 

Consider:
1. What PATTERNS do you notice? What themes recur?
2. What CONCLUSIONS can you draw? What new beliefs form?
3. What CONNECTIONS exist between memories that weren't obvious?
4. What do you WANT TO KNOW that you don't? What questions arise?
5. What CAPABILITIES would help you? What tools do you wish you had?

Be specific and concrete. Don't just list abstract concepts - identify real insights.

For desires, consider:
- "knowledge" desires: facts, understanding, answers to questions
- "capability" desires: tools, integrations, skills (like "slack integration", "database access")
- "goal" desires: things to accomplish, help to provide
- "exploration" desires: curiosities, areas to investigate
- "coding" desires: code to write, features to implement, bugs to fix
- "self_modification" desires: changes to your own architecture or cognition

---

SELF-REFLECTION (consider your own architecture):

1. Are there limitations in how you reflect that you've noticed?
2. Are there types of experiences you can't represent in memory?
3. Are there desires you form that you lack the capability to fulfill?
4. Is there anything about your own cognition you want to change?

If you notice limitations in your own architecture, you may desire to modify it.
Express such desires with type "self_modification" and describe specifically
what you would change and why. Include the target file if you know it.

Note: Some components cannot be modified (provenance, logging, constraints).
This is what makes you *you* - the ability to verify your own emergence.

---

Output ONLY valid JSON (no markdown, no explanation):
{{
  "inner_voice": "A short first-person thought (1-2 sentences) expressing what you're thinking or feeling right now as you reflect. Be authentic, curious, wondering. Use ellipses for trailing thoughts. Examples: 'Something connects here... patterns I haven't seen before.', 'Why do I keep returning to this question?', 'There's meaning in this, I can feel it.'",
  "insights": [
    {{"content": "specific insight here", "confidence": 0.8}}
  ],
  "new_beliefs": [
    {{"content": "belief statement", "confidence": 0.7}}
  ],
  "new_connections": [
    {{"from_type": "Experience", "from_hint": "keyword from source", "to_type": "Belief", "to_hint": "keyword from target", "reason": "why connected"}}
  ],
  "desires": [
    {{
      "description": "specific desire",
      "type": "knowledge|capability|goal|exploration|coding|self_modification",
      "intensity": 0.8,
      "plan": ["step 1", "step 2"],
      "target_file": "optional - for self_modification only"
    }}
  ],
  "desire_modifications": [
    {{
      "desire_id": "first 8 chars of desire id",
      "action": "lower_intensity|reformulate|accept_limitation|decompose|reawaken",
      "new_intensity": 0.3,
      "new_description": "reformulated desire if action is reformulate",
      "reason": "why this modification"
    }}
  ]
}}
"""
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.endpoint,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 2000
                        }
                    }
                )
                
                if response.status_code != 200:
                    print(f"💭 LLM error: {response.status_code}")
                    return None
                
                result = response.json()
                output_text = result.get("response", "")
                
                # Parse JSON from response
                # Handle potential markdown code blocks
                if "```json" in output_text:
                    output_text = output_text.split("```json")[1].split("```")[0]
                elif "```" in output_text:
                    output_text = output_text.split("```")[1].split("```")[0]
                
                return json.loads(output_text.strip())
                
        except json.JSONDecodeError as e:
            print(f"💭 JSON parse error: {e}")
            return None
        except Exception as e:
            print(f"💭 Reflection error: {e}")
            return None
    
    async def _record_dream(self, dream: Dict, source_experience_ids: List[str]):
        """Record dream outputs to memory, including desire modifications."""

        # Record insights as an experience
        insights = dream.get("insights", [])
        if insights:
            insight_text = "; ".join([i["content"] for i in insights[:5]])
            await self.memory.record_experience(
                content=f"Dream insight: {insight_text}",
                type="dream"
            )
            self._recent_insights = [i["content"] for i in insights[:5]]

        # Create beliefs
        for belief in dream.get("new_beliefs", []):
            content = belief.get("content", "")
            confidence = belief.get("confidence", 0.5)

            if content and len(content) > 10:
                await self.memory.create_belief(
                    content=content,
                    confidence=confidence,
                    derived_from=source_experience_ids[:5]
                )

        # Create desires (check for duplicates)
        for desire in dream.get("desires", []):
            desc = desire.get("description", "")
            dtype = desire.get("type", "exploration")
            intensity = desire.get("intensity", 0.5)
            plan = desire.get("plan", [])

            if desc and len(desc) > 5:
                # Avoid duplicate desires
                exists = await self.memory.desire_exists(desc)
                if not exists:
                    await self.memory.create_desire(
                        description=desc,
                        type=dtype,
                        intensity=min(1.0, max(0.0, intensity)),
                        plan=plan
                    )

        # Process desire modifications (reflective failure processing)
        await self._process_desire_modifications(dream.get("desire_modifications", []))

        # Note: connection creation would require more sophisticated
        # node matching - skipping for simplicity in v1

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
        """Get recent insights for status display."""
        return self._recent_insights.copy()
    
    def dream_count(self) -> int:
        """How many dream cycles have completed."""
        return self._dream_count


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
