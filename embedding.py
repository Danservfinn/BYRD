"""
Embedding provider abstraction for BYRD.
Supports Ollama (local) and OpenAI (cloud) backends.

Part of Option B implementation - provides embeddings for:
- Pattern matching in Self-Compiler
- Semantic similarity in Memory Reasoner
- Query embedding for spreading activation
"""

import asyncio
import os
from typing import List, Optional, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging

import httpx
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class EmbeddingResult:
    """Result from an embedding operation."""
    embedding: List[float]
    model: str
    tokens: int
    dimensions: int


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    async def embed(self, text: str) -> EmbeddingResult:
        """Embed a single text string."""
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        """Embed multiple text strings."""
        pass

    @property
    @abstractmethod
    def dimensions(self) -> int:
        """Return the embedding dimensions."""
        pass


class OllamaEmbedding(EmbeddingProvider):
    """Ollama-based embedding provider (local, free)."""

    # Known embedding dimensions for common models
    MODEL_DIMENSIONS = {
        "nomic-embed-text": 768,
        "mxbai-embed-large": 1024,
        "all-minilm": 384,
        "snowflake-arctic-embed": 1024,
    }

    def __init__(
        self,
        model: str = "nomic-embed-text",
        endpoint: str = "http://localhost:11434"
    ):
        self.model = model
        self.endpoint = endpoint
        self._dimensions = self.MODEL_DIMENSIONS.get(model, 768)

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed(self, text: str) -> EmbeddingResult:
        """Embed a single text using Ollama."""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.endpoint}/api/embeddings",
                    json={"model": self.model, "prompt": text}
                )
                response.raise_for_status()
                data = response.json()

                embedding = data.get("embedding", [])

                return EmbeddingResult(
                    embedding=embedding,
                    model=self.model,
                    tokens=len(text.split()),  # Approximate
                    dimensions=len(embedding)
                )
        except httpx.HTTPError as e:
            logger.error(f"Ollama embedding failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected embedding error: {e}")
            raise

    async def embed_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        """Embed multiple texts (sequential for Ollama)."""
        results = []
        for text in texts:
            result = await self.embed(text)
            results.append(result)
        return results


class OpenAIEmbedding(EmbeddingProvider):
    """OpenAI-based embedding provider (cloud, paid)."""

    MODEL_DIMENSIONS = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536,
    }

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None
    ):
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self._dimensions = self.MODEL_DIMENSIONS.get(model, 1536)

        if not self.api_key:
            raise ValueError("OpenAI API key required")

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed(self, text: str) -> EmbeddingResult:
        """Embed a single text using OpenAI."""
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=self.api_key)

            response = await client.embeddings.create(
                model=self.model,
                input=text
            )

            embedding = response.data[0].embedding

            return EmbeddingResult(
                embedding=embedding,
                model=self.model,
                tokens=response.usage.total_tokens,
                dimensions=len(embedding)
            )
        except Exception as e:
            logger.error(f"OpenAI embedding failed: {e}")
            raise

    async def embed_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        """Embed multiple texts using OpenAI (batched)."""
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=self.api_key)

            response = await client.embeddings.create(
                model=self.model,
                input=texts
            )

            tokens_per_text = response.usage.total_tokens // len(texts)

            return [
                EmbeddingResult(
                    embedding=e.embedding,
                    model=self.model,
                    tokens=tokens_per_text,
                    dimensions=len(e.embedding)
                )
                for e in response.data
            ]
        except Exception as e:
            logger.error(f"OpenAI batch embedding failed: {e}")
            raise


class CachedEmbedding(EmbeddingProvider):
    """Wrapper that caches embeddings to reduce API calls."""

    def __init__(self, provider: EmbeddingProvider, max_cache_size: int = 10000):
        self.provider = provider
        self.cache: dict = {}
        self.max_cache_size = max_cache_size

    @property
    def dimensions(self) -> int:
        return self.provider.dimensions

    async def embed(self, text: str) -> EmbeddingResult:
        """Embed with caching."""
        cache_key = hash(text)

        if cache_key in self.cache:
            return self.cache[cache_key]

        result = await self.provider.embed(text)

        # Add to cache, evict oldest if needed
        if len(self.cache) >= self.max_cache_size:
            # Simple FIFO eviction
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        self.cache[cache_key] = result
        return result

    async def embed_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        """Embed batch with caching."""
        results = []
        uncached_texts = []
        uncached_indices = []

        # Check cache first
        for i, text in enumerate(texts):
            cache_key = hash(text)
            if cache_key in self.cache:
                results.append(self.cache[cache_key])
            else:
                results.append(None)
                uncached_texts.append(text)
                uncached_indices.append(i)

        # Embed uncached texts
        if uncached_texts:
            new_results = await self.provider.embed_batch(uncached_texts)
            for idx, result in zip(uncached_indices, new_results):
                results[idx] = result
                self.cache[hash(texts[idx])] = result

        return results


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    a_np = np.array(a)
    b_np = np.array(b)

    dot_product = np.dot(a_np, b_np)
    norm_a = np.linalg.norm(a_np)
    norm_b = np.linalg.norm(b_np)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def euclidean_distance(a: List[float], b: List[float]) -> float:
    """Compute Euclidean distance between two embeddings."""
    a_np = np.array(a)
    b_np = np.array(b)
    return float(np.linalg.norm(a_np - b_np))


def find_most_similar(
    query_embedding: List[float],
    embeddings: List[List[float]],
    top_k: int = 5
) -> List[tuple]:
    """
    Find the most similar embeddings to a query.
    Returns list of (index, similarity) tuples.
    """
    similarities = [
        (i, cosine_similarity(query_embedding, emb))
        for i, emb in enumerate(embeddings)
    ]

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]


def get_embedding_provider(config: dict) -> EmbeddingProvider:
    """
    Factory function to get embedding provider from config.

    Config example:
    {
        "provider": "ollama",  # or "openai"
        "model": "nomic-embed-text",
        "endpoint": "http://localhost:11434",
        "cache": True,
        "cache_size": 10000
    }
    """
    provider_type = config.get("provider", "ollama")

    if provider_type == "ollama":
        provider = OllamaEmbedding(
            model=config.get("model", "nomic-embed-text"),
            endpoint=config.get("endpoint", "http://localhost:11434")
        )
    elif provider_type == "openai":
        provider = OpenAIEmbedding(
            model=config.get("model", "text-embedding-3-small"),
            api_key=config.get("api_key")
        )
    else:
        raise ValueError(f"Unknown embedding provider: {provider_type}")

    # Optionally wrap with cache
    if config.get("cache", True):
        provider = CachedEmbedding(
            provider,
            max_cache_size=config.get("cache_size", 10000)
        )

    return provider


# Singleton for global access
_embedding_provider: Optional[EmbeddingProvider] = None


def get_global_embedder(config: Optional[dict] = None) -> EmbeddingProvider:
    """Get or create the global embedding provider."""
    global _embedding_provider

    if _embedding_provider is None:
        if config is None:
            # Default config
            config = {
                "provider": "ollama",
                "model": "nomic-embed-text",
                "cache": True
            }
        _embedding_provider = get_embedding_provider(config)

    return _embedding_provider


def set_global_embedder(provider: EmbeddingProvider) -> None:
    """Set the global embedding provider."""
    global _embedding_provider
    _embedding_provider = provider
