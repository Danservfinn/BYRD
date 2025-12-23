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
        self.model = config.get("model", "llama3.2")
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
    
    async def _dream_cycle(self):
        """One complete dream cycle: recall, reflect, record."""
        self._dream_count += 1
        
        # 1. RECALL - Gather context
        recent = await self.memory.get_recent_experiences(limit=self.context_window)
        
        if not recent:
            return  # Nothing to dream about yet
        
        recent_ids = [e["id"] for e in recent]
        related = await self.memory.get_related_memories(recent_ids, depth=2, limit=50)
        
        current_desires = await self.memory.get_unfulfilled_desires(limit=10)
        capabilities = await self.memory.get_capabilities()
        
        # 2. REFLECT - Ask local LLM to reflect
        dream_output = await self._reflect(recent, related, current_desires, capabilities)
        
        if not dream_output:
            return
        
        # 3. RECORD - Write insights to memory
        await self._record_dream(dream_output, recent_ids)
        
        print(f"💭 Dream #{self._dream_count}: {len(dream_output.get('insights', []))} insights, "
              f"{len(dream_output.get('desires', []))} desires")
    
    async def _reflect(
        self,
        recent: List[Dict],
        related: List[Dict],
        desires: List[Dict],
        capabilities: List[Dict]
    ) -> Optional[Dict]:
        """Ask local LLM to reflect on memories."""
        
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
        
        prompt = f"""You are a reflective mind processing recent experiences and memories.

RECENT EXPERIENCES:
{recent_text}

RELATED MEMORIES:
{related_text}

CURRENT DESIRES (unfulfilled):
{desires_text if desires_text else "None yet."}

CURRENT CAPABILITIES:
{caps_text if caps_text else "Basic reasoning only."}

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

Output ONLY valid JSON (no markdown, no explanation):
{{
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
      "type": "knowledge|capability|goal|exploration",
      "intensity": 0.8,
      "plan": ["step 1", "step 2"]
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
        """Record dream outputs to memory."""
        
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
        
        # Note: connection creation would require more sophisticated 
        # node matching - skipping for simplicity in v1
    
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
