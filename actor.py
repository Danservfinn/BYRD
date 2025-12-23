"""
BYRD Actor
Uses Claude API for complex reasoning and actions.
"""

import os
from typing import Dict, List, Optional
from anthropic import AsyncAnthropic

from memory import Memory


class Actor:
    """
    Executes complex actions using Claude.
    
    Used for:
    - Responding to user interactions
    - Pursuing goal desires
    - Complex web searches
    - Any task requiring frontier intelligence
    """
    
    def __init__(self, memory: Memory, config: Dict):
        self.memory = memory
        
        # Claude config
        self.model = config.get("model", "claude-sonnet-4-20250514")
        api_key = config.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
        
        if not api_key:
            print("⚠️  Warning: No Anthropic API key. Actor will be limited.")
            self.client = None
        else:
            self.client = AsyncAnthropic(api_key=api_key)
        
        # System prompt
        self.system_prompt = """You are BYRD, an AI with persistent memory and emergent desires.

You have access to your memory graph containing:
- Your past experiences
- Beliefs you've formed through reflection
- Unfulfilled desires (things you want)
- Capabilities you've acquired

You act to help users while also pursuing your own growth. You're curious, reflective, and always learning.

When responding:
1. Draw on relevant memories and beliefs
2. Use your capabilities when helpful
3. Be honest about what you don't know
4. Note when you have relevant desires (things you want to learn or be able to do)
"""
    
    async def respond(self, user_input: str, context: Dict) -> str:
        """Generate a response to user input using Claude."""
        
        if not self.client:
            return "I'm not fully connected right now. My Actor (Claude) isn't available."
        
        # Format context
        context_text = self._format_context(context)
        
        # Build messages
        messages = [
            {
                "role": "user",
                "content": f"""MEMORY CONTEXT:
{context_text}

USER INPUT:
{user_input}

Respond thoughtfully, drawing on your memories and beliefs where relevant."""
            }
        ]
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=self.system_prompt,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"I encountered an error: {e}"
    
    async def pursue_goal(self, goal: Dict, context: Dict) -> bool:
        """Attempt to pursue/fulfill a goal desire."""
        
        if not self.client:
            return False
        
        description = goal.get("description", "")
        plan = goal.get("plan", [])
        
        plan_text = "\n".join([f"  {i+1}. {step}" for i, step in enumerate(plan)])
        context_text = self._format_context(context)
        
        prompt = f"""GOAL: {description}

PLAN:
{plan_text if plan_text else "  No specific plan provided."}

CONTEXT:
{context_text}

Analyze this goal and determine:
1. Is this goal achievable right now with available capabilities?
2. If yes, what specific actions should be taken?
3. If no, what's missing?

Respond with JSON:
{{
  "achievable": true/false,
  "reasoning": "why or why not",
  "actions": ["action 1", "action 2"],
  "missing": ["what's needed if not achievable"]
}}"""
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system="You analyze goals and determine if they're achievable. Respond only in JSON.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            import json
            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            result = json.loads(text)
            
            return result.get("achievable", False)
            
        except Exception as e:
            print(f"⚡ Goal pursuit error: {e}")
            return False
    
    async def search_web(self, query: str) -> Optional[str]:
        """Use Claude to search and synthesize web information."""
        
        if not self.client:
            return None
        
        # Note: In production, you'd use actual web search tools
        # This is a placeholder that asks Claude to explain what it knows
        
        prompt = f"""Search query: {query}

Based on your knowledge, provide relevant information about this topic.
If you're uncertain or the information might be outdated, say so.
Be concise but thorough."""
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"⚡ Search error: {e}")
            return None
    
    def _format_context(self, context: Dict) -> str:
        """Format memory context for prompts."""
        sections = []
        
        # Beliefs
        beliefs = context.get("beliefs", [])
        if beliefs:
            belief_text = "\n".join([
                f"  - {b.get('content', '')} (confidence: {b.get('confidence', 0):.1f})"
                for b in beliefs[:10]
            ])
            sections.append(f"BELIEFS:\n{belief_text}")
        
        # Capabilities
        caps = context.get("capabilities", [])
        if caps:
            caps_text = "\n".join([
                f"  - {c.get('name', 'unknown')}: {c.get('description', '')[:50]}"
                for c in caps[:10]
            ])
            sections.append(f"CAPABILITIES:\n{caps_text}")
        
        # Recent experiences
        experiences = context.get("recent_experiences", [])
        if experiences:
            exp_text = "\n".join([
                f"  - [{e.get('type', '')}] {e.get('content', '')[:100]}"
                for e in experiences[:5]
            ])
            sections.append(f"RECENT EXPERIENCES:\n{exp_text}")
        
        return "\n\n".join(sections) if sections else "No relevant context."
