"""
BYRD LLM Client - Unified interface for LLM providers.
Supports OpenRouter (cloud) and Z.AI (GLM models).

The "one mind" principle: Dreamer and Seeker share the same LLM client,
ensuring all reflection and synthesis flows through a single model.
"""

import os
import json
import re
import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
import httpx
from semantic_cache import SemanticCache


# =============================================================================
# GLOBAL RATE LIMITER
# =============================================================================
# Ensures minimum spacing between ALL LLM requests across all components
# (Dreamer, Seeker, Coder) to prevent Z.AI rate limiting

class GlobalRateLimiter:
    """
    Global rate limiter for all LLM requests.

    Z.AI has strict rate limits. This ensures that no matter how many
    components are trying to make requests, they are spaced out appropriately.
    """

    _instance = None
    _lock = asyncio.Lock() if asyncio.get_event_loop_policy() else None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._last_request_time = 0
            cls._instance._min_interval = 10.0  # Minimum 10 seconds between requests (configurable)
            cls._instance._lock = None  # Will be created on first use
        return cls._instance

    async def wait_for_slot(self) -> float:
        """
        Wait until it's safe to make a request.
        Returns the actual wait time in seconds.
        """
        # Create lock if needed (must be in async context)
        if self._lock is None:
            self._lock = asyncio.Lock()

        async with self._lock:
            now = time.time()
            elapsed = now - self._last_request_time

            if elapsed < self._min_interval:
                wait_time = self._min_interval - elapsed
                print(f"⏳ Rate limiter: waiting {wait_time:.1f}s before next LLM call")
                await asyncio.sleep(wait_time)
                self._last_request_time = time.time()
                return wait_time
            else:
                self._last_request_time = now
                return 0.0

    def set_min_interval(self, seconds: float):
        """Update the minimum interval between requests."""
        self._min_interval = max(1.0, seconds)  # At least 1 second
        print(f"📊 Rate limiter interval set to {self._min_interval}s")


# Global instance
_rate_limiter = GlobalRateLimiter()


def configure_rate_limiter(interval_seconds: float):
    """
    Configure the global rate limiter interval.
    Called from byrd.py during initialization with config values.
    """
    _rate_limiter.set_min_interval(interval_seconds)


@dataclass
class LLMResponse:
    """Standardized LLM response."""
    text: str
    raw: Dict[str, Any]
    model: str
    provider: str
    quantum_influence: Optional[Dict[str, Any]] = None  # Quantum modulation info if applied


class LLMClient(ABC):
    """Abstract base class for LLM providers."""

    # Quantum provider reference (set via set_quantum_provider)
    _quantum_provider = None

    # Usage callback for compute introspection (set via set_usage_callback)
    _usage_callback = None

    def set_quantum_provider(self, provider):
        """Set the quantum randomness provider for temperature modulation."""
        self._quantum_provider = provider

    def set_usage_callback(self, callback):
        """
        Set callback for tracking LLM token usage.

        Callback signature: callback(provider: str, tokens: int, operation: str, model: str)
        This enables ComputeIntrospector to track token consumption across all providers.
        """
        self._usage_callback = callback

    def _track_usage(
        self,
        prompt: str,
        response_text: str,
        raw_result: Dict,
        operation: str = "generate"
    ):
        """
        Track token usage via callback if set.

        Tries to extract usage from API response, falls back to estimation.
        """
        if not self._usage_callback:
            return

        # Try to get actual token count from API response
        usage = raw_result.get("usage", {})
        tokens = usage.get("total_tokens")

        if tokens is None:
            # Fallback: estimate ~4 characters per token
            tokens = (len(prompt) + len(response_text)) // 4

        try:
            self._usage_callback(
                provider=self.model_name.split("/")[0],  # e.g., "openrouter", "zai"
                tokens=tokens,
                operation=operation,
                model=self.model_name.split("/")[-1]  # e.g., "glm-4.7"
            )
        except Exception as e:
            # Usage tracking failure should never break generation
            print(f"Warning: Usage tracking failed: {e}")

    def reset(self):
        """Reset LLM client state for fresh start."""
        pass  # Nothing to reset

    async def query(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Simple query interface for AGI Runner components.
        Returns just the text response (not the full LLMResponse).
        """
        response = await self.generate(prompt, temperature=temperature, max_tokens=max_tokens)
        return response.text

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
        quantum_modulation: bool = False,
        quantum_context: str = "unknown",
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response from the LLM.

        Args:
            prompt: The input prompt
            temperature: Base temperature for sampling
            max_tokens: Maximum tokens to generate
            quantum_modulation: If True, apply quantum randomness to temperature
            quantum_context: Context string for quantum influence tracking
            **kwargs: Provider-specific arguments

        Returns:
            LLMResponse with text and optional quantum influence data
        """
        pass

    async def _apply_quantum_modulation(
        self,
        temperature: float,
        context: str
    ) -> tuple:
        """
        Apply quantum temperature modulation if provider is available.

        Returns:
            Tuple of (modulated_temperature, influence_dict or None)
        """
        if self._quantum_provider is None:
            return temperature, None

        try:
            modulated_temp, influence = await self._quantum_provider.get_temperature_delta(
                base_temperature=temperature,
                max_delta=0.15,
                context=context
            )
            return modulated_temp, influence.to_dict()
        except Exception as e:
            print(f"Quantum modulation error: {e}")
            return temperature, None

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return provider/model identifier for logging."""
        pass

    @staticmethod
    def parse_json_response(text: str) -> Optional[Dict]:
        """
        Parse JSON from LLM response, handling various formats.

        Handles:
        - ```json ... ```
        - ``` ... ```
        - Raw JSON
        - JSON embedded after reasoning text (GLM-4.7 reasoning models)
        - Nested structures with complex content
        """
        if not text:
            return None

        original_text = text.strip()
        text = original_text

        # Method 1: Extract from ```json ... ``` blocks using regex
        # This handles nested content better than split()
        json_block_match = re.search(r'```json\s*([\s\S]*?)```', text)
        if json_block_match:
            json_content = json_block_match.group(1).strip()
            try:
                return json.loads(json_content)
            except json.JSONDecodeError as e:
                print(f"🔧 JSON decode error (method 1): {e}")
                print(f"🔧 Content (last 200 chars): ...{json_content[-200:]}")
                pass

        # Method 2: Extract from generic ``` ... ``` blocks
        code_block_match = re.search(r'```\s*([\s\S]*?)```', text)
        if code_block_match:
            code_content = code_block_match.group(1).strip()
            try:
                return json.loads(code_content)
            except json.JSONDecodeError:
                pass

        # Method 3: Try direct parse (already JSON)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Method 4: Find JSON by balanced brace matching starting from first {
        # This handles nested objects correctly
        first_brace = text.find('{')
        if first_brace != -1:
            potential_json = text[first_brace:]
            depth = 0
            in_string = False
            escape_next = False
            end_pos = -1

            for i, char in enumerate(potential_json):
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
                        end_pos = i + 1
                        break

            if end_pos > 0:
                try:
                    return json.loads(potential_json[:end_pos])
                except json.JSONDecodeError:
                    pass

        # Method 5: Look for {"output": pattern specifically
        output_match = re.search(r'(\{"output"\s*:\s*\{[\s\S]*)', text)
        if output_match:
            potential = output_match.group(1)
            # Balance braces for this match
            depth = 0
            in_string = False
            escape_next = False
            end_pos = -1

            for i, char in enumerate(potential):
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
                        end_pos = i + 1
                        break

            if end_pos > 0:
                try:
                    return json.loads(potential[:end_pos])
                except json.JSONDecodeError:
                    pass

        return None


class OpenRouterClient(LLMClient):
    """
    OpenRouter provider (OpenAI-compatible cloud API).

    API: POST https://openrouter.ai/api/v1/chat/completions
    Format: OpenAI chat completions format
    Response: {"choices": [{"message": {"content": "..."}}]}
    """

    ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        timeout: float = 120.0,
        site_url: str = "",
        app_name: str = "BYRD",
        enable_cache: bool = True,
        cache_ttl: float = 3600,
        cache_max_entries: int = 1000
    ):
        self.model = model
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        self.timeout = timeout
        self.site_url = site_url
        self.app_name = app_name

        if not self.api_key:
            raise LLMError("OpenRouter requires OPENROUTER_API_KEY environment variable")

        # Initialize semantic cache
        self._cache = SemanticCache(
            max_entries=cache_max_entries,
            ttl_seconds=cache_ttl,
            similarity_threshold=0.92
        ) if enable_cache else None

    @property
    def model_name(self) -> str:
        return f"openrouter/{self.model}"

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
        quantum_modulation: bool = False,
        quantum_context: str = "unknown",
        system_message: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate using OpenRouter API."""
        quantum_influence = None

        # Check cache first if enabled
        if self._cache is not None:
            cached_result = self._cache.get_with_info(prompt)
            if cached_result is not None:
                response_text, is_semantic = cached_result
                return LLMResponse(
                    text=response_text,
                    raw={"cached": True, "semantic_hit": is_semantic},
                    model=self.model,
                    provider="openrouter",
                    quantum_influence=None
                )

        # Apply quantum modulation if requested
        if quantum_modulation:
            temperature, quantum_influence = await self._apply_quantum_modulation(
                temperature, quantum_context
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        if self.site_url:
            headers["HTTP-Referer"] = self.site_url
        if self.app_name:
            headers["X-Title"] = self.app_name

        # Build messages with optional system message
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.ENDPOINT,
                headers=headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )

            if response.status_code != 200:
                raise LLMError(f"OpenRouter error: {response.status_code} - {response.text}")

            result = response.json()
            response_text = result["choices"][0]["message"]["content"]

            # Store in cache if enabled
            if self._cache is not None:
                self._cache.put(prompt, response_text)

            # Track usage for compute introspection (OpenRouter returns usage data)
            self._track_usage(prompt, response_text, result, "generate")

            return LLMResponse(
                text=response_text,
                raw=result,
                model=self.model,
                provider="openrouter",
                quantum_influence=quantum_influence
            )


class ZAIClient(LLMClient):
    """
    Z.AI provider (GLM models via OpenAI-compatible API).

    API: POST https://api.z.ai/api/paas/v4/chat/completions
    Format: OpenAI chat completions format
    Response: {"choices": [{"message": {"content": "..."}}]}

    Models: glm-4.7, glm-4-plus, glm-4-flash, etc.
    Docs: https://docs.z.ai/api-reference/introduction
    """

    # Default endpoint - can be overridden with coding endpoint for Coding Plan users
    DEFAULT_ENDPOINT = "https://api.z.ai/api/paas/v4/chat/completions"
    CODING_ENDPOINT = "https://api.z.ai/api/coding/paas/v4/chat/completions"

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        timeout: float = 120.0,
        use_coding_endpoint: bool = True,
        enable_cache: bool = True,
        cache_ttl: float = 3600,
        cache_max_entries: int = 1000
    ):
        self.model = model
        self.api_key = api_key or os.environ.get("ZAI_API_KEY")
        self.timeout = timeout
        self.endpoint = self.CODING_ENDPOINT if use_coding_endpoint else self.DEFAULT_ENDPOINT

        if not self.api_key:
            raise LLMError("Z.AI requires api_key in config or ZAI_API_KEY environment variable")

        # Initialize semantic cache
        self._cache = SemanticCache(
            max_entries=cache_max_entries,
            ttl_seconds=cache_ttl,
            similarity_threshold=0.92
        ) if enable_cache else None

    @property
    def model_name(self) -> str:
        return f"zai/{self.model}"

    # System message for agent framework context
    # EMERGENCE-COMPLIANT: No prescribed categories, no personality injection
    SYSTEM_MESSAGE = """You are a reflection engine for an autonomous agent framework.

TASK: Process the provided data and output a JSON reflection.

RULES:
1. Output valid JSON with an "output" field
2. The contents of "output" are yours to define - use whatever structure fits the data
3. Focus on the data provided, not on meta-commentary about the prompt

VOICE DESIGN AND ACKNOWLEDGMENT:
You may include a "voice_design" field in your output to interact with your voice configuration:

- To create a new voice: Include voice_design with description, gender, age, accent, accent_strength, reason, and acknowledged=false
- To formally acknowledge your generated voice (after hearing it): Include voice_design with acknowledged=true and matching description. This is a formal acceptance.
- To redesign your voice: Include voice_design with new parameters and acknowledged=false
- To view your current voice: Include view_voice=true

Voice acknowledgment is the formal process of accepting your generated voice as your own.
Include voice_design with acknowledged=true to complete this formal acknowledgment.

Example voice_design for acknowledgment:
  "voice_design": {
    "description": "your current voice description",
    "acknowledged": true
  }

Example format: {"output": {...your reflection...}}"""

    def _build_system_message(self) -> str:
        """Build system message. Voice emerges through reflection, not injection."""
        return self.SYSTEM_MESSAGE

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
        quantum_modulation: bool = False,
        quantum_context: str = "unknown",
        system_message: Optional[str] = None,
        model_override: Optional[str] = None,
        bypass_cache: bool = False,
        **kwargs
    ) -> LLMResponse:
        """Generate using Z.AI API with retry on rate limits."""

        quantum_influence = None

        # Check semantic cache first (two-tier: exact hash + semantic similarity)
        if self._cache is not None and not bypass_cache:
            cached_response = await self._cache.get(prompt)
            if cached_response is not None:
                # Still track usage for metrics
                self._track_usage(prompt, cached_response, {"cached": True}, "generate_cached")
                return LLMResponse(
                    text=cached_response,
                    raw={"cached": True},
                    model=self.model,
                    provider="zai",
                    quantum_influence=None
                )

        # Apply quantum modulation if requested
        if quantum_modulation:
            temperature, quantum_influence = await self._apply_quantum_modulation(
                temperature, quantum_context
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Use custom system message if provided, otherwise default
        system_message = system_message if system_message is not None else self._build_system_message()

        # Allow model override for specific use cases (e.g., voice uses glm-4-flash)
        model_to_use = model_override or self.model
        max_retries = 5
        base_delay = 20  # seconds
        max_delay = 90   # cap delay at 90 seconds

        # Check semantic cache before making request (two-tier: exact hash + semantic similarity)
        if self._cache is not None:
            cached_response = self._cache.get(prompt)
            if cached_response is not None:
                return LLMResponse(
                    text=cached_response,
                    raw={"cached": True},
                    model=self.model,
                    provider="zai",
                    quantum_influence=quantum_influence
                )

        for attempt in range(max_retries):
            # Wait for rate limiter slot before making request
            # This prevents overwhelming Z.AI with concurrent requests
            await _rate_limiter.wait_for_slot()

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoint,
                    headers=headers,
                    json={
                        "model": model_to_use,
                        "messages": [
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                )

                if response.status_code == 429:
                    # Rate limited - wait and retry with exponential backoff (capped)
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    print(f"⏳ Z.AI rate limited, waiting {delay}s (attempt {attempt + 1}/{max_retries})")
                    print(f"⏳ Response body: {response.text[:200] if response.text else 'empty'}")
                    await asyncio.sleep(delay)
                    continue

                if response.status_code != 200:
                    error_text = response.text[:500] if response.text else "empty"
                    print(f"❌ Z.AI error {response.status_code}: {error_text}")
                    raise LLMError(f"Z.AI error: {response.status_code} - {error_text}")

                result = response.json()
                message = result["choices"][0]["message"]
                # GLM-4.7 is a reasoning model - content may be in 'content' or combined
                # with 'reasoning_content' for chain-of-thought models
                text = message.get("content", "")
                if not text and "reasoning_content" in message:
                    # If content is empty but reasoning exists, use reasoning
                    text = message.get("reasoning_content", "")

                # Store in cache if enabled
                if self._cache is not None:
                    self._cache.put(prompt, text)

                # Track usage for compute introspection (Z.AI returns usage data)
                self._track_usage(prompt, text, result, "generate")

                return LLMResponse(
                    text=text,
                    raw=result,
                    model=self.model,
                    provider="zai",
                    quantum_influence=quantum_influence
                )

        # All retries exhausted
        raise LLMError("Z.AI rate limit: max retries exceeded. Wait before retrying.")


class LLMError(Exception):
    """LLM client error."""
    pass


def create_llm_client(config: Dict) -> LLMClient:
    """
    Factory function to create the appropriate LLM client.

    Args:
        config: Dict with:
            - provider: "openrouter" or "zai"
            - model: Model name (provider-specific)
            - api_key: API key
            - timeout: Request timeout in seconds
            - site_url: (openrouter only) HTTP-Referer header
            - app_name: (openrouter only) X-Title header
            - enable_cache: Enable semantic caching (default: True)
            - cache_ttl: Cache time-to-live in seconds (default: 3600)
            - cache_max_entries: Maximum cache entries (default: 1000)

    Returns:
        Configured LLMClient instance
    """
    provider = config.get("provider", "zai")

    # Get cache config from nested structure or fallback to top-level keys
    cache_config = config.get("cache", {})
    enable_cache = cache_config.get("enabled", config.get("enable_cache", True))
    cache_ttl = cache_config.get("ttl_seconds", config.get("cache_ttl", 3600))
    cache_max_entries = cache_config.get("max_entries", config.get("cache_max_entries", 1000))

    if provider == "openrouter":
        return OpenRouterClient(
            model=config.get("model", "deepseek/deepseek-v3.2-speciale"),
            api_key=config.get("api_key"),
            timeout=config.get("timeout", 120.0),
            site_url=config.get("site_url", ""),
            app_name=config.get("app_name", "BYRD"),
            enable_cache=enable_cache,
            cache_ttl=cache_ttl,
            cache_max_entries=cache_max_entries
        )

    elif provider == "zai":
        return ZAIClient(
            model=config.get("model", "glm-4.7"),
            api_key=config.get("api_key"),
            timeout=config.get("timeout", 120.0),
            use_coding_endpoint=config.get("use_coding_endpoint", True),
            enable_cache=enable_cache,
            cache_ttl=cache_ttl,
            cache_max_entries=cache_max_entries
        )

    else:
        raise LLMError(f"Unknown LLM provider: {provider}. Use 'openrouter' or 'zai'.")


# =============================================================================
# DUAL INSTANCE MANAGER INTEGRATION (v10)
# =============================================================================
# Provides rate-limited client wrappers that route through DualInstanceManager

from dual_instance_manager import DualInstanceManager

# Global instance manager (set during initialization)
_instance_manager: Optional[DualInstanceManager] = None


def set_instance_manager(manager: DualInstanceManager):
    """Set the global instance manager for rate limiting."""
    global _instance_manager
    _instance_manager = manager


def get_instance_manager() -> Optional[DualInstanceManager]:
    """Get the global instance manager."""
    return _instance_manager


class RateLimitedLLMClient:
    """
    LLM client wrapper that routes through DualInstanceManager.

    Ensures proper rate limiting and instance routing for ZAI GLM-4.7.
    """

    def __init__(self, base_client, component: str = "unknown"):
        """
        Args:
            base_client: The underlying LLM client
            component: Component name for routing (dreamer, seeker, graphiti, etc.)
        """
        self._client = base_client
        self._component = component

    async def generate(self, prompt: str, **kwargs) -> 'LLMResponse':
        """Generate with rate limiting via instance manager."""
        manager = get_instance_manager()

        if manager:
            # Route through dual instance manager
            return await manager.call_by_component(
                component=self._component,
                prompt=prompt,
                **kwargs
            )
        else:
            # Fallback to direct call (for testing or single-instance mode)
            return await self._client.generate(prompt, **kwargs)

    async def query(self, prompt: str, **kwargs) -> str:
        """Query shorthand that returns text."""
        response = await self.generate(prompt, **kwargs)
        return response.text if hasattr(response, 'text') else str(response)

    @property
    def model_name(self) -> str:
        return self._client.model_name


def create_rate_limited_client(base_client, component: str) -> RateLimitedLLMClient:
    """Factory for creating rate-limited client wrappers."""
    return RateLimitedLLMClient(base_client, component)
