"""
Reflector - RSI-aware reflection layer.

Wraps the archived Dreamer component to extract improvement-focused
desires with provenance tracking.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger("rsi.emergence.reflector")


@dataclass
class Provenance:
    """Tracks the origin of a desire for emergence verification."""
    origin: str  # "reflection" | "external" | "bootstrap"
    reflection_id: Optional[str]
    timestamp: str
    external_request: Optional[str]  # None if pure emergence
    source_experiences: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DesireWithProvenance:
    """A desire with its provenance metadata."""
    desire: Dict
    provenance: Provenance


class Reflector:
    """
    RSI-aware reflection layer.

    Wraps the archived Dreamer to:
    1. Inject RSI system prompt (Constitution + Strategies)
    2. Extract improvement-focused desires
    3. Attach provenance metadata for emergence verification
    """

    def __init__(self, llm_client, system_prompt, memory=None):
        """
        Initialize Reflector.

        Args:
            llm_client: LLM client for reflection
            system_prompt: SystemPrompt instance
            memory: Optional memory for context loading
        """
        self.llm = llm_client
        self.system_prompt = system_prompt
        self.memory = memory
        self._reflection_count = 0

    async def reflect_for_rsi(self) -> List[DesireWithProvenance]:
        """
        Run reflection and extract RSI-relevant desires.

        Returns:
            List of desires with provenance attached
        """
        self._reflection_count += 1
        logger.info(f"RSI Reflection #{self._reflection_count} starting")

        # Build reflection prompt with RSI context
        rsi_context = self.system_prompt.get_full_prompt()
        context = await self._gather_context()

        prompt = self._build_reflection_prompt(rsi_context, context)

        # Run reflection via LLM
        try:
            response = await self.llm.query(
                prompt,
                temperature=0.7,
                max_tokens=2000
            )
            reflection = self._parse_reflection(response)
        except Exception as e:
            logger.error(f"Reflection failed: {e}")
            return []

        # Extract desires with provenance
        reflection_id = f"ref_{self._reflection_count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        desires = self._extract_desires(reflection, reflection_id)

        logger.info(f"Reflection produced {len(desires)} desires")
        return desires

    async def _gather_context(self) -> Dict:
        """Gather context for reflection."""
        context = {
            "recent_experiences": [],
            "current_beliefs": [],
            "recent_trajectories": []
        }

        if not self.memory:
            return context

        try:
            # Get recent experiences
            experiences = await self.memory.get_recent_experiences(limit=10)
            context["recent_experiences"] = [
                {"content": e.get("content", ""), "type": e.get("type", "")}
                for e in experiences
            ]

            # Get recent trajectories (learning attempts)
            trajectories = await self.memory.get_recent_trajectories(limit=5)
            context["recent_trajectories"] = [
                {
                    "domain": t.get("domain", ""),
                    "success": t.get("success", False),
                    "problem": t.get("problem", "")[:100]
                }
                for t in trajectories
            ]
        except Exception as e:
            logger.warning(f"Context gathering failed: {e}")

        return context

    def _build_reflection_prompt(self, rsi_context: str, context: Dict) -> str:
        """Build the full reflection prompt."""
        experiences_text = ""
        if context.get("recent_experiences"):
            experiences_text = "\n".join([
                f"- [{e['type']}] {e['content'][:200]}"
                for e in context["recent_experiences"]
            ])

        trajectories_text = ""
        if context.get("recent_trajectories"):
            trajectories_text = "\n".join([
                f"- [{t['domain']}] {'✓' if t['success'] else '✗'} {t['problem']}"
                for t in context["recent_trajectories"]
            ])

        return f"""{rsi_context}

---

# RECENT CONTEXT

## Experiences
{experiences_text or "_No recent experiences._"}

## Learning Attempts
{trajectories_text or "_No recent learning attempts._"}

---

# REFLECTION

Based on your Constitution and the context above, reflect on:
1. What patterns do you notice in your recent experiences?
2. What capabilities would you like to improve?
3. What specific weaknesses have you observed?

Express any improvement desires that emerge from this reflection.
Be specific about WHAT you want to improve and WHY.

Respond in JSON format:
{{
    "observations": ["..."],
    "desires": [
        {{
            "description": "I want to improve X because Y",
            "intensity": 0.0-1.0,
            "domain": "code|math|logic|creative|other"
        }}
    ]
}}
"""

    def _parse_reflection(self, response: str) -> Dict:
        """Parse LLM response into structured reflection."""
        import json

        # Handle markdown code blocks
        text = response.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            logger.warning("Failed to parse reflection JSON, extracting manually")
            return self._extract_manually(response)

    def _extract_manually(self, response: str) -> Dict:
        """Fallback extraction when JSON parsing fails."""
        # Look for desire-like phrases
        desires = []
        lines = response.split("\n")

        for line in lines:
            line_lower = line.lower()
            if any(kw in line_lower for kw in ["want to", "wish to", "need to improve", "should improve"]):
                desires.append({
                    "description": line.strip("- ").strip(),
                    "intensity": 0.5,
                    "domain": "other"
                })

        return {
            "observations": [],
            "desires": desires
        }

    def _extract_desires(
        self,
        reflection: Dict,
        reflection_id: str
    ) -> List[DesireWithProvenance]:
        """Extract and normalize desires from reflection."""
        raw_desires = reflection.get("desires", [])
        if not raw_desires:
            raw_desires = reflection.get("expressed_drives", [])

        desires_with_provenance = []

        for raw in raw_desires:
            desire = self._normalize_desire(raw)

            # Skip non-improvement desires
            if not self._is_improvement_desire(desire):
                continue

            provenance = Provenance(
                origin="reflection",
                reflection_id=reflection_id,
                timestamp=datetime.now().isoformat(),
                external_request=None,
                source_experiences=[]
            )

            desires_with_provenance.append(
                DesireWithProvenance(desire=desire, provenance=provenance)
            )

        return desires_with_provenance

    def _normalize_desire(self, raw: Any) -> Dict:
        """Normalize desire to standard format."""
        if isinstance(raw, str):
            return {
                "description": raw,
                "intensity": 0.5,
                "domain": "other"
            }

        if isinstance(raw, dict):
            return {
                "description": raw.get("description", raw.get("content", str(raw))),
                "intensity": float(raw.get("intensity", 0.5)),
                "domain": raw.get("domain", "other")
            }

        return {
            "description": str(raw),
            "intensity": 0.5,
            "domain": "other"
        }

    def _is_improvement_desire(self, desire: Dict) -> bool:
        """Check if desire is about improvement/learning."""
        description = desire.get("description", "").lower()
        improvement_keywords = [
            "improve", "learn", "better", "capability", "skill",
            "understand", "master", "practice", "grow", "enhance",
            "develop", "strengthen", "fix", "debug", "optimize"
        ]
        return any(kw in description for kw in improvement_keywords)

    def reset(self):
        """Reset reflector state."""
        self._reflection_count = 0
