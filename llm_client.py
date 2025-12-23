"""
BYRD LLM Client - Unified interface for LLM providers.
Supports Ollama (local) and OpenRouter (cloud).

The "one mind" principle: Dreamer and Seeker share the same LLM client,
ensuring all reflection and synthesis flows through a single model.
"""

import os
import json
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


class LLMClient(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> LLMResponse:
        """Generate a response from the LLM."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return provider/model identifier for logging."""
        pass

    @staticmethod
    def parse_json_response(text: str) -> Optional[Dict]:
        """
        Parse JSON from LLM response, handling markdown code blocks.

        Handles:
        - ```json ... ```
        - ``` ... ```
        - Raw JSON
        """
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
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
        **kwargs
    ) -> LLMResponse:
        """Generate using Ollama API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
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
                provider="ollama"
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
        **kwargs
    ) -> LLMResponse:
        """Generate using OpenRouter API."""
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
                provider="openrouter"
            )


class LLMError(Exception):
    """LLM client error."""
    pass


def create_llm_client(config: Dict) -> LLMClient:
    """
    Factory function to create the appropriate LLM client.

    Args:
        config: Dict with:
            - provider: "ollama" or "openrouter"
            - model: Model name (provider-specific)
            - endpoint: (ollama only) API endpoint
            - api_key: (openrouter only) API key
            - timeout: Request timeout in seconds
            - site_url: (openrouter only) HTTP-Referer header
            - app_name: (openrouter only) X-Title header

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

    else:
        raise LLMError(f"Unknown LLM provider: {provider}. Use 'ollama' or 'openrouter'.")
