"""
External Knowledge Provider for BYRD

Enables BYRD to access external information sources to fulfill
information-seeking desires. Supports multiple backends:
- Web search (Tavily, DuckDuckGo)
- Wikipedia
- ArXiv (research papers)

Based on IMPLEMENTATION_PLAN_v2.md Phase 1.
"""

import asyncio
import aiohttp
import json
import os
import re
import hashlib
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod


class KnowledgeSource(Enum):
    WEB_SEARCH = "web_search"
    WIKIPEDIA = "wikipedia"
    ARXIV = "arxiv"
    MEMORY = "memory"


@dataclass
class KnowledgeResult:
    """Result from a knowledge query."""
    source: KnowledgeSource
    query: str
    content: str
    url: Optional[str] = None
    confidence: float = 0.5
    timestamp: float = 0.0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
        if self.metadata is None:
            self.metadata = {}


class KnowledgeBackend(ABC):
    """Abstract base class for knowledge backends."""

    @abstractmethod
    async def search(self, query: str, max_results: int = 5) -> List[KnowledgeResult]:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass


class DuckDuckGoBackend(KnowledgeBackend):
    """
    Free web search via DuckDuckGo Instant Answer API.
    No API key required.
    """

    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    def is_available(self) -> bool:
        return True  # Always available, no API key needed

    async def search(self, query: str, max_results: int = 5) -> List[KnowledgeResult]:
        results = []

        try:
            session = await self._get_session()
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }

            async with session.get(self.base_url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()

                    # Abstract (main answer)
                    if data.get("Abstract"):
                        results.append(KnowledgeResult(
                            source=KnowledgeSource.WEB_SEARCH,
                            query=query,
                            content=data["Abstract"],
                            url=data.get("AbstractURL"),
                            confidence=0.8,
                            metadata={"type": "abstract", "source": data.get("AbstractSource")}
                        ))

                    # Related topics
                    for topic in data.get("RelatedTopics", [])[:max_results]:
                        if isinstance(topic, dict) and topic.get("Text"):
                            results.append(KnowledgeResult(
                                source=KnowledgeSource.WEB_SEARCH,
                                query=query,
                                content=topic["Text"],
                                url=topic.get("FirstURL"),
                                confidence=0.6,
                                metadata={"type": "related_topic"}
                            ))

                    # Infobox
                    if data.get("Infobox", {}).get("content"):
                        infobox_text = "\n".join([
                            f"{item.get('label', '')}: {item.get('value', '')}"
                            for item in data["Infobox"]["content"]
                            if item.get("value")
                        ])
                        if infobox_text:
                            results.append(KnowledgeResult(
                                source=KnowledgeSource.WEB_SEARCH,
                                query=query,
                                content=infobox_text,
                                confidence=0.7,
                                metadata={"type": "infobox"}
                            ))

        except asyncio.TimeoutError:
            print(f"   DuckDuckGo search timeout for: {query}")
        except Exception as e:
            print(f"   DuckDuckGo search error: {e}")

        return results[:max_results]


class WikipediaBackend(KnowledgeBackend):
    """
    Wikipedia API backend.
    No API key required.
    """

    def __init__(self):
        self.base_url = "https://en.wikipedia.org/api/rest_v1"
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    def is_available(self) -> bool:
        return True

    async def search(self, query: str, max_results: int = 3) -> List[KnowledgeResult]:
        results = []

        try:
            session = await self._get_session()

            # Search for pages
            search_url = "https://en.wikipedia.org/w/api.php"
            search_params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": max_results
            }

            async with session.get(search_url, params=search_params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    search_results = data.get("query", {}).get("search", [])

                    for result in search_results[:max_results]:
                        title = result.get("title", "")

                        # Get summary for each result
                        summary_url = f"{self.base_url}/page/summary/{title.replace(' ', '_')}"

                        try:
                            async with session.get(summary_url, timeout=5) as summary_response:
                                if summary_response.status == 200:
                                    summary_data = await summary_response.json()

                                    results.append(KnowledgeResult(
                                        source=KnowledgeSource.WIKIPEDIA,
                                        query=query,
                                        content=summary_data.get("extract", ""),
                                        url=summary_data.get("content_urls", {}).get("desktop", {}).get("page"),
                                        confidence=0.85,
                                        metadata={
                                            "title": title,
                                            "description": summary_data.get("description", "")
                                        }
                                    ))
                        except Exception:
                            continue

        except asyncio.TimeoutError:
            print(f"   Wikipedia search timeout for: {query}")
        except Exception as e:
            print(f"   Wikipedia search error: {e}")

        return results


class ArxivBackend(KnowledgeBackend):
    """
    ArXiv API for research papers.
    No API key required.
    """

    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    def is_available(self) -> bool:
        return True

    async def search(self, query: str, max_results: int = 3) -> List[KnowledgeResult]:
        results = []

        try:
            session = await self._get_session()
            params = {
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": max_results,
                "sortBy": "relevance"
            }

            async with session.get(self.base_url, params=params, timeout=15) as response:
                if response.status == 200:
                    # ArXiv returns Atom XML
                    text = await response.text()

                    entries = re.findall(r'<entry>(.*?)</entry>', text, re.DOTALL)

                    for entry in entries[:max_results]:
                        title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                        summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                        link_match = re.search(r'<id>(.*?)</id>', entry)

                        if title_match and summary_match:
                            title = title_match.group(1).strip().replace('\n', ' ')
                            summary = summary_match.group(1).strip().replace('\n', ' ')
                            url = link_match.group(1) if link_match else None

                            results.append(KnowledgeResult(
                                source=KnowledgeSource.ARXIV,
                                query=query,
                                content=f"**{title}**\n\n{summary}",
                                url=url,
                                confidence=0.9,
                                metadata={"type": "research_paper", "title": title}
                            ))

        except asyncio.TimeoutError:
            print(f"   ArXiv search timeout for: {query}")
        except Exception as e:
            print(f"   ArXiv search error: {e}")

        return results


class TavilyBackend(KnowledgeBackend):
    """
    Tavily Search API - AI-optimized web search.
    Requires API key (free tier available).
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/search"
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    def is_available(self) -> bool:
        return self.api_key is not None and len(self.api_key) > 0

    async def search(self, query: str, max_results: int = 5) -> List[KnowledgeResult]:
        if not self.is_available():
            return []

        results = []

        try:
            session = await self._get_session()
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": max_results,
                "include_answer": True
            }

            async with session.post(self.base_url, json=payload, timeout=15) as response:
                if response.status == 200:
                    data = await response.json()

                    # Direct answer
                    if data.get("answer"):
                        results.append(KnowledgeResult(
                            source=KnowledgeSource.WEB_SEARCH,
                            query=query,
                            content=data["answer"],
                            confidence=0.9,
                            metadata={"type": "direct_answer", "provider": "tavily"}
                        ))

                    # Search results
                    for result in data.get("results", [])[:max_results]:
                        results.append(KnowledgeResult(
                            source=KnowledgeSource.WEB_SEARCH,
                            query=query,
                            content=result.get("content", ""),
                            url=result.get("url"),
                            confidence=result.get("score", 0.5),
                            metadata={"title": result.get("title"), "provider": "tavily"}
                        ))

        except asyncio.TimeoutError:
            print(f"   Tavily search timeout for: {query}")
        except Exception as e:
            print(f"   Tavily search error: {e}")

        return results


class KnowledgeProvider:
    """
    Unified knowledge provider that coordinates multiple backends.

    This is the main interface for BYRD to access external knowledge.
    """

    def __init__(self, config: Dict = None, memory=None, llm_client=None):
        config = config or {}
        self.memory = memory
        self.llm_client = llm_client

        # Initialize backends
        self.backends: Dict[str, KnowledgeBackend] = {}

        # Always available (no API key)
        self.backends["duckduckgo"] = DuckDuckGoBackend()
        self.backends["wikipedia"] = WikipediaBackend()
        self.backends["arxiv"] = ArxivBackend()

        # Optional (requires API key)
        tavily_key = config.get("tavily_api_key") or os.environ.get("TAVILY_API_KEY")
        if tavily_key:
            self.backends["tavily"] = TavilyBackend(tavily_key)

        # Result cache
        self._cache: Dict[str, List[KnowledgeResult]] = {}
        self._cache_ttl = config.get("cache_ttl", 3600)  # 1 hour
        self._cache_timestamps: Dict[str, float] = {}

        # Metrics
        self._queries = 0
        self._cache_hits = 0
        self._successful_queries = 0

    def _cache_key(self, query: str, sources: List[str]) -> str:
        """Generate cache key for a query."""
        normalized = query.strip().lower()
        sources_str = ",".join(sorted(sources))
        return hashlib.md5(f"{normalized}:{sources_str}".encode()).hexdigest()

    def _is_cache_valid(self, key: str) -> bool:
        """Check if cache entry is still valid."""
        if key not in self._cache_timestamps:
            return False
        return (time.time() - self._cache_timestamps[key]) < self._cache_ttl

    async def search(
        self,
        query: str,
        sources: List[str] = None,
        max_results: int = 5
    ) -> List[KnowledgeResult]:
        """
        Search for knowledge across multiple sources.

        Args:
            query: The search query
            sources: List of source names to use (default: all available)
            max_results: Maximum results per source

        Returns:
            List of KnowledgeResult objects
        """
        self._queries += 1

        # Default to all available sources
        if sources is None:
            sources = [name for name, backend in self.backends.items() if backend.is_available()]

        # Check cache
        cache_key = self._cache_key(query, sources)
        if cache_key in self._cache and self._is_cache_valid(cache_key):
            self._cache_hits += 1
            return self._cache[cache_key]

        # Query all sources in parallel
        tasks = []
        for source_name in sources:
            if source_name in self.backends and self.backends[source_name].is_available():
                tasks.append(self.backends[source_name].search(query, max_results))

        if not tasks:
            return []

        # Gather results
        all_results = []
        results_lists = await asyncio.gather(*tasks, return_exceptions=True)

        for results in results_lists:
            if isinstance(results, list):
                all_results.extend(results)

        # Sort by confidence
        all_results.sort(key=lambda r: r.confidence, reverse=True)

        # Cache results
        self._cache[cache_key] = all_results
        self._cache_timestamps[cache_key] = time.time()

        if all_results:
            self._successful_queries += 1

        return all_results

    async def search_and_synthesize(
        self,
        query: str,
        sources: List[str] = None,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Search for knowledge and synthesize into a coherent answer.

        Returns dict with 'answer', 'sources', 'confidence'.
        """
        results = await self.search(query, sources, max_results)

        if not results:
            return {
                "answer": None,
                "sources": [],
                "confidence": 0.0,
                "found": False
            }

        # If we have an LLM, synthesize the results
        if self.llm_client and len(results) > 1:
            # Combine results for synthesis
            context = "\n\n".join([
                f"[Source: {r.source.value}]\n{r.content[:500]}"
                for r in results[:5]
            ])

            prompt = f"""Synthesize the following information into a clear, accurate answer.

Query: {query}

Information gathered:
{context}

Provide a synthesized answer that:
1. Combines key facts from multiple sources
2. Notes any contradictions or uncertainties
3. Is concise but complete

Synthesized answer:"""

            try:
                response = await self.llm_client.generate(
                    prompt,
                    temperature=0.3,
                    max_tokens=500,
                    operation="knowledge_synthesis"
                )

                # Handle LLMResponse object
                text = response.text if hasattr(response, 'text') else str(response)

                return {
                    "answer": text,
                    "sources": [{"content": r.content[:200], "url": r.url, "source": r.source.value} for r in results[:5]],
                    "confidence": sum(r.confidence for r in results[:5]) / len(results[:5]),
                    "found": True,
                    "synthesized": True
                }
            except Exception as e:
                print(f"   Synthesis failed: {e}")

        # Fallback: return best result
        best = results[0]
        return {
            "answer": best.content,
            "sources": [{"content": best.content[:200], "url": best.url, "source": best.source.value}],
            "confidence": best.confidence,
            "found": True,
            "synthesized": False
        }

    async def fulfill_desire(self, desire: Dict) -> Dict[str, Any]:
        """
        Fulfill an information-seeking desire.

        This is the main integration point with BYRD's Seeker.
        """
        desire_content = desire.get("content", "") or desire.get("description", "")
        metadata = desire.get("metadata", {})

        # Extract the actual query from the desire
        query = await self._extract_query(desire_content, metadata)

        if not query:
            return {
                "fulfilled": False,
                "reason": "Could not extract searchable query from desire"
            }

        # Determine best sources based on desire type
        sources = self._select_sources(desire_content, metadata)

        # Search and synthesize
        result = await self.search_and_synthesize(query, sources)

        if result["found"]:
            # Store the knowledge in BYRD's memory
            if self.memory:
                await self._store_in_memory(query, result, desire)

            return {
                "fulfilled": True,
                "answer": result["answer"],
                "confidence": result["confidence"],
                "sources": result["sources"]
            }
        else:
            return {
                "fulfilled": False,
                "reason": "No relevant information found",
                "query": query
            }

    async def _extract_query(self, desire_content: str, metadata: Dict) -> Optional[str]:
        """Extract a searchable query from desire content."""

        # If metadata contains explicit topic, use that
        if metadata.get("topic"):
            return metadata["topic"]

        # Common patterns in information-seeking desires
        patterns = [
            "seek evidence to strengthen or refute belief:",
            "seek information about:",
            "understand why predictions fail for:",
            "test and improve capability:",
            "find way to unblock goal:",
            "investigate:",
            "learn about:",
            "research:",
            "understand:",
            "want to know about:",
        ]

        content_lower = desire_content.lower()
        for pattern in patterns:
            if pattern in content_lower:
                # Extract everything after the pattern
                idx = content_lower.index(pattern) + len(pattern)
                query = desire_content[idx:].strip()
                return query[:200]  # Limit query length

        # Fallback: use LLM to extract query
        if self.llm_client:
            try:
                prompt = f"""Extract a concise search query from this desire:
"{desire_content}"

Return ONLY the search query, nothing else:"""

                response = await self.llm_client.generate(
                    prompt,
                    temperature=0.1,
                    max_tokens=50,
                    operation="extract_query"
                )
                text = response.text if hasattr(response, 'text') else str(response)
                return text.strip()[:200]
            except Exception:
                pass

        # Last resort: use the desire content directly
        return desire_content[:200]

    def _select_sources(self, desire_content: str, metadata: Dict) -> List[str]:
        """Select appropriate knowledge sources based on desire."""
        content_lower = desire_content.lower()

        # Research/academic topics -> ArXiv + Wikipedia
        if any(word in content_lower for word in ["research", "paper", "study", "scientific", "theory"]):
            return ["arxiv", "wikipedia"]

        # Technical topics -> Wikipedia + Web
        if any(word in content_lower for word in ["algorithm", "programming", "technical", "code"]):
            return ["wikipedia", "duckduckgo"]

        # General knowledge -> Wikipedia first
        if any(word in content_lower for word in ["what is", "who is", "history", "definition"]):
            return ["wikipedia", "duckduckgo"]

        # Current events -> Web search
        if any(word in content_lower for word in ["latest", "recent", "news", "current"]):
            sources = ["duckduckgo"]
            if "tavily" in self.backends and self.backends["tavily"].is_available():
                sources.insert(0, "tavily")
            return sources

        # Default: all available
        return list(self.backends.keys())

    async def _store_in_memory(self, query: str, result: Dict, desire: Dict):
        """Store acquired knowledge in BYRD's memory."""
        if not self.memory:
            return

        try:
            # Create experience for the knowledge acquisition
            await self.memory.record_experience(
                content=f"[KNOWLEDGE_ACQUIRED] Query: {query}\n\nAnswer: {str(result.get('answer', ''))[:500]}",
                type="knowledge_acquisition"
            )

        except Exception as e:
            print(f"   Failed to store knowledge in memory: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge provider statistics."""
        return {
            "total_queries": self._queries,
            "cache_hits": self._cache_hits,
            "successful_queries": self._successful_queries,
            "success_rate": self._successful_queries / self._queries if self._queries > 0 else 0,
            "cache_hit_rate": self._cache_hits / self._queries if self._queries > 0 else 0,
            "available_backends": [name for name, b in self.backends.items() if b.is_available()]
        }

    async def close(self):
        """Close all backend sessions."""
        for backend in self.backends.values():
            if hasattr(backend, '_session') and backend._session:
                await backend._session.close()

    def reset(self):
        """Reset provider state."""
        self._queries = 0
        self._cache_hits = 0
        self._successful_queries = 0
        self._cache.clear()
        self._cache_timestamps.clear()
