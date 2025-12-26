"""
BYRD LLM Client - Unified interface for LLM providers.
Supports Ollama (local), OpenRouter (cloud), and Z.AI (GLM models).

The "one mind" principle: Dreamer and Seeker share the same LLM client,
ensuring all reflection and synthesis flows through a single model.
"""

import os
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
import httpx


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

    def set_quantum_provider(self, provider):
        """Set the quantum randomness provider for temperature modulation."""
        self._quantum_provider = provider

    def set_ego_voice(self, voice: str):
        """DEPRECATED: Voice injection removed for pure emergence."""
        pass  # No-op - voice emerges through reflection

    def get_ego_voice(self) -> str:
        """DEPRECATED: Voice injection removed for pure emergence."""
        return ""  # No prescribed voice

    def reset(self):
        """Reset LLM client state for fresh start."""
        pass  # Nothing to reset

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


class OllamaClient(LLMClient):
    """
    Ollama provider (local LLM).

    API: POST /api/generate
    Format: {"model": "...", "prompt": "...", "stream": false, "options": {...}}
    Response: {"response": "..."}
    """

    def __init__(self, model: str, endpoint: str, timeout: float = 120.0):
        self.model = model
        self.endpoint = endpoint
        self.timeout = timeout

    @property
    def model_name(self) -> str:
        return f"ollama/{self.model}"

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
        quantum_modulation: bool = False,
        quantum_context: str = "unknown",
        **kwargs
    ) -> LLMResponse:
        """Generate using Ollama API."""
        quantum_influence = None

        # Apply quantum modulation if requested
        if quantum_modulation:
            temperature, quantum_influence = await self._apply_quantum_modulation(
                temperature, quantum_context
            )

        timeout_config = httpx.Timeout(self.timeout, connect=60.0)
        async with httpx.AsyncClient(timeout=timeout_config) as client:
            response = await client.post(
                self.endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }
            )
            if response.status_code != 200:
                raise LLMError(f"Ollama error: {response.status_code}")

            result = response.json()
            return LLMResponse(
                text=result.get("response", ""),
                raw=result,
                model=self.model,
                provider="ollama",
                quantum_influence=quantum_influence
            )


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
        app_name: str = "BYRD"
    ):
        self.model = model
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        self.timeout = timeout
        self.site_url = site_url
        self.app_name = app_name

        if not self.api_key:
            raise LLMError("OpenRouter requires OPENROUTER_API_KEY environment variable")

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
        **kwargs
    ) -> LLMResponse:
        """Generate using OpenRouter API."""
        quantum_influence = None

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

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.ENDPOINT,
                headers=headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )

            if response.status_code != 200:
                raise LLMError(f"OpenRouter error: {response.status_code} - {response.text}")

            result = response.json()
            return LLMResponse(
                text=result["choices"][0]["message"]["content"],
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
        use_coding_endpoint: bool = True
    ):
        self.model = model
        self.api_key = api_key or os.environ.get("ZAI_API_KEY")
        self.timeout = timeout
        self.endpoint = self.CODING_ENDPOINT if use_coding_endpoint else self.DEFAULT_ENDPOINT

        if not self.api_key:
            raise LLMError("Z.AI requires api_key in config or ZAI_API_KEY environment variable")

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
        **kwargs
    ) -> LLMResponse:
        """Generate using Z.AI API with retry on rate limits."""
        import asyncio

        quantum_influence = None

        # Apply quantum modulation if requested
        if quantum_modulation:
            temperature, quantum_influence = await self._apply_quantum_modulation(
                temperature, quantum_context
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        system_message = self._build_system_message()
        max_retries = 5
        base_delay = 20  # seconds
        max_delay = 90   # cap delay at 90 seconds

        for attempt in range(max_retries):
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoint,
                    headers=headers,
                    json={
                        "model": self.model,
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


def create_llm_client(config: Dict, ego_voice: str = "") -> LLMClient:
    """
    Factory function to create the appropriate LLM client.

    Args:
        config: Dict with:
            - provider: "ollama", "openrouter", or "zai"
            - model: Model name (provider-specific)
            - endpoint: (ollama only) API endpoint
            - api_key: (openrouter/zai) API key
            - timeout: Request timeout in seconds
            - site_url: (openrouter only) HTTP-Referer header
            - app_name: (openrouter only) X-Title header
        ego_voice: DEPRECATED - voice emerges through reflection

    Returns:
        Configured LLMClient instance
    """
    provider = config.get("provider", "ollama")

    if provider == "ollama":
        return OllamaClient(
            model=config.get("model", "gemma2:27b"),
            endpoint=config.get("endpoint", "http://localhost:11434/api/generate"),
            timeout=config.get("timeout", 120.0)
        )

    elif provider == "openrouter":
        return OpenRouterClient(
            model=config.get("model", "deepseek/deepseek-v3.2-speciale"),
            api_key=config.get("api_key"),
            timeout=config.get("timeout", 120.0),
            site_url=config.get("site_url", ""),
            app_name=config.get("app_name", "BYRD")
        )

    elif provider == "zai":
        return ZAIClient(
            model=config.get("model", "glm-4.7"),
            api_key=config.get("api_key"),
            timeout=config.get("timeout", 120.0),
            use_coding_endpoint=config.get("use_coding_endpoint", True)
        )

    else:
        raise LLMError(f"Unknown LLM provider: {provider}. Use 'ollama', 'openrouter', or 'zai'.")
