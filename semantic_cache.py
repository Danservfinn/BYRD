"""
Semantic Cache for LLM Client

Reduces redundant LLM calls through semantic similarity matching.
Two-tier lookup: exact hash match + semantic similarity.
"""

import hashlib
import time
from typing import Optional, Dict, Tuple, Any, List
from dataclasses import dataclass, field
import numpy as np


@dataclass
class CacheEntry:
    """Represents a single cache entry."""
    query_hash: str
    query_text: str
    query_embedding: Optional[np.ndarray]
    response: str
    timestamp: float
    hit_count: int = 0
    
    def is_expired(self, ttl_seconds: float) -> bool:
        """Check if entry has expired."""
        return time.time() - self.timestamp > ttl_seconds


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
        self._evictions = 0
        self._total_queries = 0

    def _hash_query(self, query: str) -> str:
        """Generate SHA256 hash of query."""
        return hashlib.sha256(query.encode()).hexdigest()

    def _compute_similarity(self, embed1: np.ndarray, embed2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings."""
        dot_product = np.dot(embed1, embed2)
        norm1 = np.linalg.norm(embed1)
        norm2 = np.linalg.norm(embed2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

    def _evict_expired(self) -> int:
        """Remove expired entries, return count evicted."""
        expired_keys = [
            key for key, entry in self._hash_cache.items()
            if entry.is_expired(self.ttl_seconds)
        ]
        
        for key in expired_keys:
            entry = self._hash_cache.pop(key)
            self._semantic_index.pop(key, None)
            self._evictions += 1
        
        return len(expired_keys)

    def _evict_lru(self) -> None:
        """Evict least recently used entry (lowest hit_count, oldest timestamp)."""
        if not self._hash_cache:
            return
        
        lru_key = min(
            self._hash_cache.keys(),
            key=lambda k: (self._hash_cache[k].hit_count, self._hash_cache[k].timestamp)
        )
        
        entry = self._hash_cache.pop(lru_key)
        self._semantic_index.pop(lru_key, None)
        self._evictions += 1

    def get(self, query: str) -> Optional[str]:
        """
        Retrieve cached response for query.
        
        Returns None if not found or expired.
        """
        self._total_queries += 1
        
        # Tier 1: Exact hash match
        query_hash = self._hash_query(query)
        
        if query_hash in self._hash_cache:
            entry = self._hash_cache[query_hash]
            
            if entry.is_expired(self.ttl_seconds):
                self._hash_cache.pop(query_hash)
                self._semantic_index.pop(query_hash, None)
                self._evictions += 1
                self._misses += 1
                return None
            
            entry.hit_count += 1
            self._hits += 1
            return entry.response
        
        # Tier 2: Semantic similarity match (if embedder available)
        if self.embedder is not None and self._semantic_index:
            try:
                query_embedding = self.embedder.encode(query)
                
                for hash_key, entry in self._semantic_index.items():
                    if entry.is_expired(self.ttl_seconds):
                        continue
                    
                    if entry.query_embedding is not None:
                        similarity = self._compute_similarity(
                            query_embedding, 
                            entry.query_embedding
                        )
                        
                        if similarity >= self.similarity_threshold:
                            entry.hit_count += 1
                            self._semantic_hits += 1
                            return entry.response
            except Exception:
                # Fail gracefully if embedding fails
                pass
        
        self._misses += 1
        return None

    def get(self, query: str) -> Optional[str]:
        """
        Retrieve cached response for query.
        
        Returns None if not found or expired.
        """
        self._total_queries += 1
        
        # Tier 1: Exact hash match
        query_hash = self._hash_query(query)
        
        if query_hash in self._hash_cache:
            entry = self._hash_cache[query_hash]
            
            if entry.is_expired(self.ttl_seconds):
                self._hash_cache.pop(query_hash)
                self._semantic_index.pop(query_hash, None)
                self._evictions += 1
                self._misses += 1
                return None
            
            entry.hit_count += 1
            self._hits += 1
            return entry.response
        
        # Tier 2: Semantic similarity match (if embedder available)
        if self.embedder is not None and self._semantic_index:
            try:
                query_embedding = self.embedder.encode(query)
                
                for hash_key, entry in self._semantic_index.items():
                    if entry.is_expired(self.ttl_seconds):
                        continue
                    
                    if entry.query_embedding is not None:
                        similarity = self._compute_similarity(
                            query_embedding, 
                            entry.query_embedding
                        )
                        
                        if similarity >= self.similarity_threshold:
                            entry.hit_count += 1
                            self._semantic_hits += 1
                            return entry.response
            except Exception:
                # Fail gracefully if embedding fails
                pass
        
        self._misses += 1
        return None

    def get_with_info(self, query: str) -> Optional[tuple]:
        """
        Retrieve cached response for query with metadata.
        
        Returns (response_text, is_semantic_hit) tuple or None if not found/expired.
        """
        self._total_queries += 1
        
        # Tier 1: Exact hash match
        query_hash = self._hash_query(query)
        
        if query_hash in self._hash_cache:
            entry = self._hash_cache[query_hash]
            
            if entry.is_expired(self.ttl_seconds):
                self._hash_cache.pop(query_hash)
                self._semantic_index.pop(query_hash, None)
                self._evictions += 1
                self._misses += 1
                return None
            
            entry.hit_count += 1
            self._hits += 1
            return (entry.response, False)  # False = not a semantic hit (exact match)
        
        # Tier 2: Semantic similarity match (if embedder available)
        if self.embedder is not None and self._semantic_index:
            try:
                query_embedding = self.embedder.encode(query)
                
                for hash_key, entry in self._semantic_index.items():
                    if entry.is_expired(self.ttl_seconds):
                        continue
                    
                    if entry.query_embedding is not None:
                        similarity = self._compute_similarity(
                            query_embedding, 
                            entry.query_embedding
                        )
                        
                        if similarity >= self.similarity_threshold:
                            entry.hit_count += 1
                            self._semantic_hits += 1
                            return (entry.response, True)  # True = semantic hit
            except Exception:
                # Fail gracefully if embedding fails
                pass
        
        self._misses += 1
        return None

    def set(self, query: str, response: str) -> None:
        """
        Store query-response pair in cache.
        """
        query_hash = self._hash_query(query)
        
        # Compute embedding if embedder available
        query_embedding = None
        if self.embedder is not None:
            try:
                query_embedding = self.embedder.encode(query)
            except Exception:
                pass
        
        entry = CacheEntry(
            query_hash=query_hash,
            query_text=query,
            query_embedding=query_embedding,
            response=response,
            timestamp=time.time(),
            hit_count=0
        )
        
        # Evict expired first
        self._evict_expired()
        
        # Evict LRU if at capacity
        if len(self._hash_cache) >= self.max_entries:
            self._evict_lru()
        
        self._hash_cache[query_hash] = entry
        self._semantic_index[query_hash] = entry

    def put(self, query: str, response: str) -> None:
        """
        Alias for set() for compatibility with existing code.
        """
        self.set(query, response)

    def clear(self) -> None:
        """Clear all cache entries."""
        self._hash_cache.clear()
        self._semantic_index.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_hits = self._hits + self._semantic_hits
        hit_rate = (total_hits / self._total_queries * 100) if self._total_queries > 0 else 0.0
        
        return {
            "total_queries": self._total_queries,
            "exact_hits": self._hits,
            "semantic_hits": self._semantic_hits,
            "total_hits": total_hits,
            "misses": self._misses,
            "hit_rate_percent": round(hit_rate, 2),
            "entries": len(self._hash_cache),
            "max_entries": self.max_entries,
            "evictions": self._evictions,
            "ttl_seconds": self.ttl_seconds,
            "similarity_threshold": self.similarity_threshold
        }

    def __len__(self) -> int:
        return len(self._hash_cache)

    def __repr__(self) -> str:
        stats = self.get_stats()
        return (
            f"SemanticCache(entries={stats['entries']}/{stats['max_entries']}, "
            f"hit_rate={stats['hit_rate_percent']}%, "
            f"queries={stats['total_queries']})"
        )
