"""
Integration module for Cognitive Tiering.

Provides drop-in replacement LLM client that uses cognitive tiering
under the hood. This allows the RSI Engine and other components to
benefit from tier-aware routing without changing their code.

Usage:
    # Create tier-aware client
    from rsi.cognition.integration import create_tiered_llm_client

    tiered_client = create_tiered_llm_client()

    # Use like regular LLM client
    response = await tiered_client.generate(prompt="...")

See PROMPT.md "Layer 2: Cognitive Tiering" for specification.
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass
import logging

from .tiers import CognitiveTier, get_tier_config
from .router import CognitiveRouter, RoutingContext
from .escalation import EscalationPolicy
from .unified import UnifiedCognition, ThinkRequest

logger = logging.getLogger("rsi.cognition.integration")


@dataclass
class TieredLLMResponse:
    """Response from tiered LLM client (compatible with LLMResponse)."""
    text: str
    raw: Dict[str, Any]
    model: str
    provider: str
    tier_used: CognitiveTier
    quality_score: Optional[float] = None
    quantum_influence: Optional[Dict[str, Any]] = None


class TieredLLMClient:
    """
    LLM client that uses cognitive tiering for intelligent routing.

    This is a drop-in replacement for the core LLMClient.
    It wraps the cognitive tiering system to provide automatic
    tier selection and escalation.

    Features:
    - Automatic tier selection based on task type
    - Quality-based escalation to premium tiers
    - Cost tracking and budget management
    - Fallback to GLM 4.7 when premium unavailable

    Usage:
        client = TieredLLMClient(base_client)
        response = await client.generate(prompt="Analyze this code")
    """

    def __init__(
        self,
        base_client=None,
        cognition: Optional[UnifiedCognition] = None,
        default_tier: CognitiveTier = CognitiveTier.GLM_4_7,
        config: Dict = None
    ):
        """
        Initialize tiered LLM client.

        Args:
            base_client: Optional base LLM client (for direct calls)
            cognition: Optional UnifiedCognition instance
            default_tier: Default tier to use (default: GLM_4_7)
            config: Configuration options
        """
        self.config = config or {}
        self._base_client = base_client
        self._default_tier = default_tier

        # Create or use provided cognition
        if cognition:
            self._cognition = cognition
        else:
            self._cognition = UnifiedCognition(
                llm_client=base_client,
                config=self.config.get('cognition', {})
            )

        # Statistics
        self._call_count = 0
        self._escalation_count = 0

    def set_base_client(self, client):
        """Set the base LLM client."""
        self._base_client = client
        self._cognition.set_llm_client(client)

    @property
    def model_name(self) -> str:
        """Return model name (for compatibility)."""
        config = get_tier_config(self._default_tier)
        return f"{config.provider}/{config.model}"

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        quantum_modulation: bool = False,
        quantum_context: str = "unknown",
        task_type: str = "think",
        is_critical: bool = False,
        is_safety_critical: bool = False,
        **kwargs
    ) -> TieredLLMResponse:
        """
        Generate using cognitive tiering.

        This is the main entry point that provides compatibility
        with the standard LLMClient interface while using tiering.

        Args:
            prompt: The prompt to process
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            quantum_modulation: Enable quantum temperature modulation
            quantum_context: Context for quantum tracking
            task_type: Type of task (think, reason, create, evaluate)
            is_critical: Whether this is a critical decision
            is_safety_critical: Whether this is safety-critical
            **kwargs: Additional arguments

        Returns:
            TieredLLMResponse with text and metadata
        """
        self._call_count += 1

        # Use the cognition system
        request = ThinkRequest(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            metadata={
                'quantum_modulation': quantum_modulation,
                'quantum_context': quantum_context,
                'is_critical': is_critical,
                'is_safety_critical': is_safety_critical,
                **kwargs
            }
        )

        result = await self._cognition.think(request)

        # Track escalations
        if result.tier_used != self._default_tier:
            self._escalation_count += 1

        return TieredLLMResponse(
            text=result.content,
            raw=result.metadata,
            model=get_tier_config(result.tier_used).model,
            provider=get_tier_config(result.tier_used).provider,
            tier_used=result.tier_used,
            quality_score=result.quality_score,
            quantum_influence=kwargs.get('quantum_influence')
        )

    async def query(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Simple query interface (compatibility with LLMClient.query).

        Returns just the text response.
        """
        response = await self.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
        return response.text

    def reset(self):
        """Reset client state."""
        self._call_count = 0
        self._escalation_count = 0
        if self._base_client and hasattr(self._base_client, 'reset'):
            self._base_client.reset()

    def get_stats(self) -> Dict[str, Any]:
        """Get tiered client statistics."""
        return {
            'call_count': self._call_count,
            'escalation_count': self._escalation_count,
            'escalation_rate': self._escalation_count / max(self._call_count, 1),
            'default_tier': self._default_tier.name,
            'cognition_stats': self._cognition.get_stats()
        }

    @staticmethod
    def parse_json_response(text: str) -> Optional[Dict]:
        """
        Parse JSON from LLM response (compatibility method).

        Delegates to the base client's implementation if available.
        """
        import json
        import re

        if not text:
            return None

        text = text.strip()

        # Handle markdown code blocks
        json_block_match = re.search(r'```json\s*([\s\S]*?)```', text)
        if json_block_match:
            try:
                return json.loads(json_block_match.group(1).strip())
            except json.JSONDecodeError:
                pass

        code_block_match = re.search(r'```\s*([\s\S]*?)```', text)
        if code_block_match:
            try:
                return json.loads(code_block_match.group(1).strip())
            except json.JSONDecodeError:
                pass

        # Try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Find JSON by braces
        first_brace = text.find('{')
        if first_brace != -1:
            # Balance braces
            depth = 0
            in_string = False
            escape_next = False
            for i, char in enumerate(text[first_brace:]):
                if escape_next:
                    escape_next = False
                    continue
                if char == '\\' and in_string:
                    escape_next = True
                    continue
                if char == '"' and not escape_next:
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(text[first_brace:first_brace + i + 1])
                        except json.JSONDecodeError:
                            pass
                        break

        return None


def create_tiered_llm_client(
    base_client=None,
    config: Dict = None
) -> TieredLLMClient:
    """
    Factory function to create a tiered LLM client.

    Args:
        base_client: Optional base LLM client
        config: Configuration options

    Returns:
        Configured TieredLLMClient
    """
    return TieredLLMClient(
        base_client=base_client,
        config=config or {}
    )


def wrap_llm_client(client) -> TieredLLMClient:
    """
    Wrap an existing LLM client with cognitive tiering.

    This is the easiest way to add tiering to existing code:

        # Before
        response = await llm_client.generate(prompt)

        # After
        tiered_client = wrap_llm_client(llm_client)
        response = await tiered_client.generate(prompt)

    Args:
        client: Existing LLM client to wrap

    Returns:
        TieredLLMClient wrapping the original client
    """
    return TieredLLMClient(base_client=client)
