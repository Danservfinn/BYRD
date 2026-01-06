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

    async def reflect_for_rsi(
        self,
        meta_context: Optional[Dict] = None
    ) -> List[DesireWithProvenance]:
        """
        Run reflection and extract RSI-relevant desires.

        Args:
            meta_context: Optional meta-context from Ralph orchestration.
                If provided, includes information about the broader loop
                (iteration count, entropy trends, time in loop) for meta-awareness.

        Returns:
            List of desires with provenance attached
        """
        self._reflection_count += 1
        logger.info(f"RSI Reflection #{self._reflection_count} starting")

        # Build reflection prompt with RSI context
        rsi_context = self.system_prompt.get_full_prompt()
        context = await self._gather_context()

        prompt = self._build_reflection_prompt(rsi_context, context, meta_context)

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

    def _build_reflection_prompt(
        self,
        rsi_context: str,
        context: Dict,
        meta_context: Optional[Dict] = None
    ) -> str:
        """Build the full reflection prompt.

        Args:
            rsi_context: RSI system prompt (Constitution + Strategies)
            context: Recent experiences and trajectories
            meta_context: Optional orchestration loop awareness context
        """
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

        # Build optional meta-awareness section
        meta_section = ""
        if meta_context:
            meta_section = self._build_meta_section(meta_context)

        return f"""{rsi_context}
{meta_section}
---

# RECENT CONTEXT

## Experiences
{experiences_text or "_No recent experiences._"}

## Learning Attempts
{trajectories_text or "_No recent learning attempts._"}

---

# REFLECTION

Based on your Constitution and the context above, reflect on what verifiable capabilities you want to improve.

Focus on domains where improvement can be tested:
- **code**: Programming, debugging, algorithm implementation, Python, async, testing
- **math**: Calculations, equations, proofs, numerical analysis, algebra
- **logic**: Multi-step reasoning, deduction, inference, argument analysis

Express improvement desires that emerged from this reflection.
Each desire should be specific enough to generate practice problems.

Return ONLY valid JSON (no markdown, no explanation):
{{"observations":["pattern1","pattern2"],"desires":[{{"description":"I want to improve my Python debugging for async code","intensity":0.7,"domain":"code"}},{{"description":"I want to improve multi-step logical reasoning","intensity":0.6,"domain":"logic"}}]}}
"""

    def _build_meta_section(self, meta_context: Dict) -> str:
        """
        Build meta-awareness section for reflection prompt.

        This section injects awareness of the orchestration loop,
        allowing BYRD to reflect on its own improvement process.

        Args:
            meta_context: Dict containing loop awareness info:
                - iteration: Current Ralph iteration number
                - entropy_trend: 'increasing', 'decreasing', or 'stable'
                - time_in_loop_seconds: How long the loop has been running
                - total_frames: Number of consciousness frames recorded
                - recent_emergence_signals: List of recent emergence indicators

        Returns:
            Formatted meta-awareness section string
        """
        iteration = meta_context.get('iteration', 0)
        entropy_trend = meta_context.get('entropy_trend', 'unknown')
        time_in_loop = meta_context.get('time_in_loop_seconds', 0)
        total_frames = meta_context.get('total_frames', 0)
        emergence_signals = meta_context.get('recent_emergence_signals', [])

        # Format time nicely
        if time_in_loop >= 3600:
            time_str = f"{time_in_loop / 3600:.1f} hours"
        elif time_in_loop >= 60:
            time_str = f"{time_in_loop / 60:.1f} minutes"
        else:
            time_str = f"{time_in_loop:.0f} seconds"

        # Format emergence signals
        signals_text = ""
        if emergence_signals:
            signals_text = "\n".join([f"  - {s}" for s in emergence_signals[:5]])
        else:
            signals_text = "  _No emergence signals yet._"

        return f"""
---

# META-LOOP CONTEXT

You are currently in iteration {iteration} of a recursive self-improvement loop.
This context is provided for meta-awareness - your improvement of your own improvement process.

- **Loop Duration**: {time_str}
- **Consciousness Frames Recorded**: {total_frames}
- **Entropy Trend**: {entropy_trend}

**Recent Emergence Signals**:
{signals_text}

Consider: Are your improvement desires leading to genuine capability growth?
What patterns do you observe in your own learning trajectory?
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
            data = json.loads(text.strip())
            # Unwrap if nested in "output" field (common LLM pattern)
            if "output" in data and isinstance(data["output"], dict):
                data = data["output"]
            return data
        except json.JSONDecodeError:
            logger.warning("Failed to parse reflection JSON, extracting manually")
            return self._extract_manually(response)

    def _extract_manually(self, response: str) -> Dict:
        """Fallback extraction when JSON parsing fails."""
        import re
        desires = []
        lines = response.split("\n")

        # Keywords that indicate improvement desires
        desire_keywords = [
            "want to", "wish to", "need to improve", "should improve",
            "desire to", "seek to", "aim to", "hope to", "yearn to",
            "improve my", "enhance my", "develop my", "strengthen my",
            "better at", "learning", "practice", "master"
        ]

        for line in lines:
            line_lower = line.lower()
            # Skip empty lines and headers
            if not line.strip() or line.startswith("#"):
                continue

            # Check for desire indicators
            if any(kw in line_lower for kw in desire_keywords):
                domain = self._infer_domain(line_lower)
                desires.append({
                    "description": line.strip("- *").strip(),
                    "intensity": 0.6,
                    "domain": domain
                })

        # If still no desires found, create synthetic ones with strong domain keywords
        if not desires:
            # Always generate at least one CODE desire for practice
            desires.append({
                "description": "I want to improve my Python debugging and algorithm implementation skills through code practice",
                "intensity": 0.6,
                "domain": "code"
            })
            # Check for specific domain mentions in response
            resp_lower = response.lower()
            if any(kw in resp_lower for kw in ["math", "equation", "calculation", "numerical", "algebra"]):
                desires.append({
                    "description": "I want to improve my math equation solving and numerical calculation abilities",
                    "intensity": 0.5,
                    "domain": "math"
                })
            if any(kw in resp_lower for kw in ["logic", "reasoning", "deduction", "inference"]):
                desires.append({
                    "description": "I want to improve my logical reasoning and multi-step deduction capabilities",
                    "intensity": 0.5,
                    "domain": "logic"
                })

        return {
            "observations": [],
            "desires": desires
        }

    def _infer_domain(self, text: str) -> str:
        """Infer domain from text keywords."""
        # Code domain keywords
        code_keywords = ["code", "python", "programming", "debug", "function", "async",
                        "api", "test", "implement", "script", "syntax", "algorithm"]
        # Math domain keywords
        math_keywords = ["math", "calculate", "equation", "proof", "theorem",
                        "algebra", "geometry", "integral", "numerical", "matrix"]
        # Logic domain keywords
        logic_keywords = ["logic", "reasoning", "deduce", "infer", "argument",
                         "prove", "conclude", "premise", "consistent", "valid"]

        code_count = sum(1 for kw in code_keywords if kw in text)
        math_count = sum(1 for kw in math_keywords if kw in text)
        logic_count = sum(1 for kw in logic_keywords if kw in text)

        if code_count > math_count and code_count > logic_count:
            return "code"
        elif math_count > code_count and math_count > logic_count:
            return "math"
        elif logic_count > 0:
            return "logic"
        return "other"

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
