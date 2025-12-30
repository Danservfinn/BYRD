import hashlib
import time
from typing import Optional, Dict, Tuple, Any
from dataclasses import dataclass
import numpy as np

@dataclass
class CacheEntry:
    query_hash: str
    query_text: str
    query_embedding: Optional[np.ndarray]
    response: str
    timestamp: float
    hit_count: int = 0

class SemanticCache:
    """
    Caches LLM responses with semantic similarity matching.

    Two-tier lookup:
    1. Exact hash match (fast)
    2. Semantic similarity match (if embedder available)
    """

    def __init__(
        self,
        max_entries: int = 1000,
        ttl_seconds: float = 3600,  # 1 hour default
        similarity_threshold: float = 0.92,
        embedder = None  # Optional sentence-transformers embedder
    ):
        self.max_entries = max_entries
        self.ttl_seconds = ttl_seconds
        self.similarity_threshold = similarity_threshold
        self.embedder = embedder

        self._hash_cache: Dict[str, CacheEntry] = {}
        self._semantic_index: Dict[str, CacheEntry] = {}  # For similarity lookup

        # Metrics
        self._hits = 0
        self._misses = 0
        self._semantic_hits = 0

    def _hash_query(self, query: str) -> str:
        """Create deterministic hash of query."""
        normalized = query.strip().lower()
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]

    def _is_expired(self, entry: CacheEntry) -> bool:
        return (time.time() - entry.timestamp) > self.ttl_seconds

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    async def get(self, query: str) -> Optional[str]:
        """
        Look up cached response.
        Returns None if not found or expired.
        """
        query_hash = self._hash_query(query)

        # Tier 1: Exact hash match
        if query_hash in self._hash_cache:
            entry = self._hash_cache[query_hash]
            if not self._is_expired(entry):
                entry.hit_count += 1
                self._hits += 1
                return entry.response

        # Tier 2: Semantic similarity (if embedder available)
        if self.embedder and len(self._semantic_index) > 0:
            try:
                query_embedding = self.embedder.encode(query)

                best_match = None
                best_similarity = 0.0

                for entry in self._semantic_index.values():
                    if entry.query_embedding is not None and not self._is_expired(entry):
                        similarity = self._cosine_similarity(
                            query_embedding,
                            entry.query_embedding
                        )
                        if similarity > best_similarity:
                            best_similarity = similarity
                            best_match = entry

                if best_match and best_similarity >= self.similarity_threshold:
                    best_match.hit_count += 1
                    self._semantic_hits += 1
                    self._hits += 1
                    return best_match.response
            except Exception:
                pass  # Fallback to cache miss

        self._misses += 1
        return None

    async def put(self, query: str, response: str):
        """Store response in cache."""
        query_hash = self._hash_query(query)

        # Compute embedding if available
        query_embedding = None
        if self.embedder:
            try:
                query_embedding = self.embedder.encode(query)
            except Exception:
                pass

        entry = CacheEntry(
            query_hash=query_hash,
            query_text=query,
            query_embedding=query_embedding,
            response=response,
            timestamp=time.time()
        )

        # Enforce max entries (LRU eviction)
        if len(self._hash_cache) >= self.max_entries:
            self._evict_oldest()

        self._hash_cache[query_hash] = entry
        if query_embedding is not None:
            self._semantic_index[query_hash] = entry

    def _evict_oldest(self):
        """Remove oldest entry based on timestamp."""
        oldest_hash = None
        oldest_time = float('inf')

        for hash_key, entry in self._hash_cache.items():
            if entry.timestamp < oldest_time:
                oldest_time = entry.timestamp
                oldest_hash = hash_key

        if oldest_hash:
            del self._hash_cache[oldest_hash]
            if oldest_hash in self._semantic_index:
                del self._semantic_index[oldest_hash]

    def clear(self):
        """Clear all cache entries."""
        self._hash_cache.clear()
        self._semantic_index.clear()
        self._hits = 0
        self._misses = 0
        self._semantic_hits = 0

    def get_stats(self) -> Dict[str, Any]:
        """Return cache statistics."""
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0.0
        return {
            "entries": len(self._hash_cache),
            "hits": self._hits,
            "misses": self._misses,
            "semantic_hits": self._semantic_hits,
            "hit_rate": hit_rate,
            "max_entries": self.max_entries
        }
