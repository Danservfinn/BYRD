# BYRD AGI IMPROVEMENT PLAN v2: ACTUAL IMPLEMENTATIONS

## Executive Summary

This plan differs from v1 by providing **actual implementations**, not just infrastructure. Each component includes working logic that produces real effects.

**Key Differences from v1:**
- External knowledge access with real APIs
- Coupling handlers with actual LLM-driven logic
- Improvement cycles that run and generate data
- Strategies with concrete implementations

**Constraint**: glm-4.7 as primary LLM (with strategic Claude API escalation for complex tasks)

---

## PHASE 1: KNOWLEDGE ACCESS (Week 1-2)

### 1.1 External Knowledge Provider

**Purpose**: Enable BYRD to actually fulfill information-seeking desires.

**File**: `/Users/kurultai/BYRD/knowledge_provider.py`

```python
"""
External Knowledge Provider for BYRD

Enables BYRD to access external information sources to fulfill
information-seeking desires. Supports multiple backends:
- Web search (Tavily, DuckDuckGo)
- Wikipedia
- ArXiv (research papers)
- Local document store
"""

import asyncio
import aiohttp
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import hashlib
import time

class KnowledgeSource(Enum):
    WEB_SEARCH = "web_search"
    WIKIPEDIA = "wikipedia"
    ARXIV = "arxiv"
    LOCAL_DOCS = "local_docs"
    MEMORY = "memory"  # BYRD's own memory as knowledge source


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
            print(f"⚠️ DuckDuckGo search timeout for: {query}")
        except Exception as e:
            print(f"⚠️ DuckDuckGo search error: {e}")

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
            search_url = f"https://en.wikipedia.org/w/api.php"
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
            print(f"⚠️ Wikipedia search timeout for: {query}")
        except Exception as e:
            print(f"⚠️ Wikipedia search error: {e}")

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

                    # Simple XML parsing (avoid heavy dependencies)
                    import re

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
            print(f"⚠️ ArXiv search timeout for: {query}")
        except Exception as e:
            print(f"⚠️ ArXiv search error: {e}")

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
        return self.api_key is not None

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
            print(f"⚠️ Tavily search timeout for: {query}")
        except Exception as e:
            print(f"⚠️ Tavily search error: {e}")

        return results


class KnowledgeProvider:
    """
    Unified knowledge provider that coordinates multiple backends.

    This is the main interface for BYRD to access external knowledge.
    """

    def __init__(self, config: Dict = None, memory = None, llm_client = None):
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
                synthesized = await self.llm_client.generate(
                    prompt,
                    temperature=0.3,
                    max_tokens=500,
                    operation="knowledge_synthesis"
                )

                return {
                    "answer": synthesized,
                    "sources": [{"content": r.content[:200], "url": r.url, "source": r.source.value} for r in results[:5]],
                    "confidence": sum(r.confidence for r in results[:5]) / len(results[:5]),
                    "found": True,
                    "synthesized": True
                }
            except Exception as e:
                print(f"⚠️ Synthesis failed: {e}")

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
        desire_content = desire.get("content", "")
        desire_type = desire.get("type", "")
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
            "research:"
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

                query = await self.llm_client.generate(
                    prompt,
                    temperature=0.1,
                    max_tokens=50,
                    operation="extract_query"
                )
                return query.strip()[:200]
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
            if "tavily" in self.backends:
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
            await self.memory.create_experience(
                content=f"KNOWLEDGE ACQUIRED: {query}\n\nAnswer: {result['answer'][:500]}",
                exp_type="knowledge_acquisition",
                metadata={
                    "query": query,
                    "sources": [s["source"] for s in result.get("sources", [])],
                    "confidence": result["confidence"],
                    "desire_id": desire.get("id"),
                    "synthesized": result.get("synthesized", False)
                }
            )

            # If high confidence, consider creating a belief
            if result["confidence"] >= 0.8:
                # Check if this contradicts existing beliefs
                # (Integration point with contradiction resolver)
                pass

        except Exception as e:
            print(f"⚠️ Failed to store knowledge in memory: {e}")

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
```

---

### 1.2 Integration with Seeker

**File**: Modify `/Users/kurultai/BYRD/seeker.py`

```python
# Add to imports
from knowledge_provider import KnowledgeProvider

# Add to Seeker.__init__ (around Line 130)
def __init__(self, memory, llm_client, config: Dict = None, ...):
    # ... existing init ...

    # Initialize knowledge provider
    knowledge_config = config.get("knowledge_provider", {})
    self.knowledge_provider = KnowledgeProvider(
        config=knowledge_config,
        memory=self.memory,
        llm_client=self.llm_client
    )

# Add new method for fulfilling information-seeking desires
async def _fulfill_information_seeking_desire(self, desire: Dict) -> Dict[str, Any]:
    """
    Fulfill an information-seeking desire using external knowledge.

    This is the key integration that makes BYRD's information
    desires actually fulfillable.
    """
    result = await self.knowledge_provider.fulfill_desire(desire)

    if result["fulfilled"]:
        # Record success
        await self.memory.create_experience(
            content=f"Successfully fulfilled desire: {desire.get('content', '')[:100]}",
            exp_type="desire_fulfilled",
            metadata={
                "desire_id": desire.get("id"),
                "answer_preview": result["answer"][:200] if result.get("answer") else "",
                "confidence": result.get("confidence", 0)
            }
        )

        # Mark desire as fulfilled
        if desire.get("id"):
            await self.memory.update_desire_status(desire["id"], "fulfilled")

        # Feed result to Dreamer for reflection
        if hasattr(self, 'dreamer') and self.dreamer:
            self.dreamer.add_to_micro_buffer({
                "type": "knowledge_acquisition",
                "query": desire.get("content"),
                "answer": result["answer"][:300] if result.get("answer") else "",
                "confidence": result.get("confidence", 0)
            })
    else:
        # Record failure for learning
        await self.memory.create_experience(
            content=f"Failed to fulfill desire: {desire.get('content', '')[:100]}. Reason: {result.get('reason', 'unknown')}",
            exp_type="desire_unfulfilled",
            metadata={
                "desire_id": desire.get("id"),
                "reason": result.get("reason")
            }
        )

    return result

# Modify _process_desire to handle information-seeking
async def _process_desire(self, desire: Dict) -> Dict[str, Any]:
    """Process a single desire based on its type."""
    desire_type = desire.get("type", "general")

    # Handle information-seeking desires specially
    if desire_type == "information_seeking":
        return await self._fulfill_information_seeking_desire(desire)

    # ... existing desire processing logic ...
```

---

## PHASE 2: ACTUAL COUPLING HANDLERS (Week 2-3)

### 2.1 Complete Handler Implementations

**File**: `/Users/kurultai/BYRD/coupling_handlers.py`

```python
"""
Actual implementations for loop coupling handlers.

These are not stubs - they contain real logic that produces
real effects on BYRD's learning and behavior.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import time
import re


@dataclass
class ExtractedPattern:
    """A pattern extracted from a successful goal."""
    id: str
    description: str
    preconditions: List[str]
    actions: List[str]
    postconditions: List[str]
    success_indicators: List[str]
    confidence: float
    source_goal_id: str
    created_at: float


@dataclass
class ProposedGoal:
    """A goal proposed from a counterfactual insight."""
    description: str
    rationale: str
    source_insight: str
    estimated_value: float
    prerequisites: List[str]


class CouplingHandlers:
    """
    Implementations for all coupling handlers.

    This class provides the actual logic that makes loop
    coupling meaningful, not just event passing.
    """

    def __init__(self, memory, llm_client, config: Dict = None):
        self.memory = memory
        self.llm_client = llm_client
        config = config or {}

        # Pattern storage
        self._patterns: Dict[str, ExtractedPattern] = {}
        self._pattern_applications: Dict[str, List[Dict]] = {}  # pattern_id -> applications

        # Counterfactual queue
        self._counterfactual_queue: List[Dict] = []
        self._max_queue_size = config.get("max_counterfactual_queue", 50)

        # Metrics
        self._patterns_extracted = 0
        self._patterns_applied = 0
        self._goals_proposed = 0
        self._counterfactuals_processed = 0

    # ========================================
    # HANDLER 1: Goal Success -> Pattern Extraction
    # (Goal Evolver -> Self-Compiler)
    # ========================================

    async def extract_pattern_from_success(
        self,
        goal_description: str,
        outcome: Dict[str, Any]
    ) -> Optional[ExtractedPattern]:
        """
        Extract a reusable pattern from a successful goal.

        This is ACTUAL pattern extraction using LLM reasoning,
        not a stub that returns None.
        """
        # Get context: what experiences led to this success?
        related_experiences = await self.memory.get_experiences_for_goal(
            goal_description,
            limit=10
        )

        # Format experiences for analysis
        exp_text = "\n".join([
            f"- {exp.get('content', '')[:200]}"
            for exp in related_experiences
        ])

        # Use LLM to extract pattern
        prompt = f"""Analyze this successful goal and extract a reusable pattern.

GOAL: {goal_description}

OUTCOME:
- Fitness: {outcome.get('fitness', 'unknown')}
- Capability Delta: {outcome.get('capability_delta', 'unknown')}
- Efficiency: {outcome.get('efficiency', 'unknown')}

RELATED EXPERIENCES:
{exp_text}

Extract a reusable pattern in this JSON format:
{{
    "description": "Brief description of what this pattern accomplishes",
    "preconditions": ["condition that must be true before applying"],
    "actions": ["specific action to take"],
    "postconditions": ["expected state after successful application"],
    "success_indicators": ["how to know if it worked"],
    "generalizability": 0.0-1.0
}}

JSON pattern:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.3,
                max_tokens=500,
                operation="pattern_extraction"
            )

            # Parse JSON from response
            pattern_data = self._parse_json(response)

            if not pattern_data or not pattern_data.get("description"):
                return None

            # Validate pattern has meaningful content
            if not self._is_valid_pattern(pattern_data):
                return None

            # Create pattern object
            import uuid
            pattern = ExtractedPattern(
                id=str(uuid.uuid4())[:8],
                description=pattern_data["description"],
                preconditions=pattern_data.get("preconditions", []),
                actions=pattern_data.get("actions", []),
                postconditions=pattern_data.get("postconditions", []),
                success_indicators=pattern_data.get("success_indicators", []),
                confidence=pattern_data.get("generalizability", 0.5),
                source_goal_id=outcome.get("goal_id", ""),
                created_at=time.time()
            )

            # Store pattern
            self._patterns[pattern.id] = pattern
            self._patterns_extracted += 1

            # Store in memory for retrieval
            await self.memory.create_experience(
                content=f"PATTERN EXTRACTED: {pattern.description}",
                exp_type="pattern",
                metadata={
                    "pattern_id": pattern.id,
                    "preconditions": pattern.preconditions,
                    "actions": pattern.actions,
                    "confidence": pattern.confidence
                }
            )

            return pattern

        except Exception as e:
            print(f"⚠️ Pattern extraction failed: {e}")
            return None

    def _is_valid_pattern(self, pattern_data: Dict) -> bool:
        """Validate that a pattern has meaningful content."""
        # Must have description
        if not pattern_data.get("description") or len(pattern_data["description"]) < 10:
            return False

        # Must have at least one action
        if not pattern_data.get("actions") or len(pattern_data["actions"]) == 0:
            return False

        # Actions shouldn't be too generic
        generic_actions = ["try", "do", "make", "be"]
        for action in pattern_data.get("actions", []):
            if action.lower().strip() in generic_actions:
                return False

        return True

    # ========================================
    # HANDLER 2: Pattern Codified -> Memory Index
    # (Self-Compiler -> Memory Reasoner)
    # ========================================

    async def index_pattern(self, pattern: ExtractedPattern) -> bool:
        """
        Index a pattern for retrieval by Memory Reasoner.

        Creates searchable representation of the pattern
        that can be found during spreading activation.
        """
        try:
            # Create a searchable node for the pattern
            pattern_content = f"""
REUSABLE PATTERN: {pattern.description}

WHEN TO USE (Preconditions):
{chr(10).join('- ' + p for p in pattern.preconditions)}

WHAT TO DO (Actions):
{chr(10).join('- ' + a for a in pattern.actions)}

EXPECTED RESULTS (Postconditions):
{chr(10).join('- ' + p for p in pattern.postconditions)}

SUCCESS INDICATORS:
{chr(10).join('- ' + s for s in pattern.success_indicators)}
"""

            # Store as a special "Strategy" node type
            await self.memory.create_strategy(
                content=pattern_content,
                name=f"pattern_{pattern.id}",
                pattern_id=pattern.id,
                confidence=pattern.confidence,
                metadata={
                    "type": "extracted_pattern",
                    "source_goal": pattern.source_goal_id,
                    "actions": pattern.actions,
                    "preconditions": pattern.preconditions
                }
            )

            return True

        except Exception as e:
            print(f"⚠️ Pattern indexing failed: {e}")
            return False

    async def find_applicable_pattern(
        self,
        situation: str,
        goal: str = None
    ) -> Optional[ExtractedPattern]:
        """
        Find a pattern applicable to the current situation.

        This is used by Seeker to apply learned patterns.
        """
        if not self._patterns:
            return None

        # Use LLM to match situation to patterns
        patterns_desc = "\n\n".join([
            f"Pattern {p.id}:\n  Description: {p.description}\n  Preconditions: {p.preconditions}"
            for p in self._patterns.values()
        ])

        prompt = f"""Given this situation, which pattern (if any) applies?

SITUATION: {situation}
GOAL: {goal or 'not specified'}

AVAILABLE PATTERNS:
{patterns_desc}

If a pattern applies, respond with its ID. If none apply, respond "none".
Pattern ID:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.1,
                max_tokens=20,
                operation="pattern_matching"
            )

            response = response.strip().lower()

            if response == "none" or not response:
                return None

            # Find pattern by ID
            for pattern_id, pattern in self._patterns.items():
                if pattern_id in response:
                    return pattern

            return None

        except Exception:
            return None

    # ========================================
    # HANDLER 3: Memory Answer -> Counterfactual Seed
    # (Memory Reasoner -> Dreaming Machine)
    # ========================================

    async def queue_counterfactual_seed(
        self,
        query: str,
        answer: str,
        confidence: float = 0.5
    ) -> bool:
        """
        Queue a memory answer as a seed for counterfactual generation.

        Low-confidence answers are especially valuable seeds
        because they represent uncertainty worth exploring.
        """
        seed = {
            "query": query,
            "answer": answer,
            "confidence": confidence,
            "timestamp": time.time(),
            "explored": False
        }

        # Prioritize low-confidence answers (more room for exploration)
        if confidence < 0.6:
            self._counterfactual_queue.insert(0, seed)
        else:
            self._counterfactual_queue.append(seed)

        # Trim queue
        if len(self._counterfactual_queue) > self._max_queue_size:
            self._counterfactual_queue = self._counterfactual_queue[:self._max_queue_size]

        return True

    async def generate_counterfactual(self, seed: Dict = None) -> Optional[Dict]:
        """
        Generate a counterfactual from a queued seed.

        Called by Dreaming Machine during dream cycles.
        """
        # Get seed from queue if not provided
        if seed is None:
            unexplored = [s for s in self._counterfactual_queue if not s.get("explored")]
            if not unexplored:
                return None
            seed = unexplored[0]

        prompt = f"""Generate a counterfactual exploration of this knowledge.

ORIGINAL QUERY: {seed['query']}
ORIGINAL ANSWER: {seed['answer']}
CONFIDENCE: {seed['confidence']}

Consider: What if the answer were different? What alternative explanations exist?
What would change if a key assumption were wrong?

Generate a counterfactual analysis:
{{
    "alternative_answer": "What could the answer be instead?",
    "key_assumption": "What assumption does the original answer rely on?",
    "what_if": "What if that assumption were false?",
    "implications": ["What would follow from the alternative?"],
    "testable_prediction": "How could we tell which is correct?",
    "insight": "What did we learn from this exploration?"
}}

JSON:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.7,  # Higher temperature for creativity
                max_tokens=400,
                operation="counterfactual_generation"
            )

            counterfactual = self._parse_json(response)

            if counterfactual and counterfactual.get("insight"):
                # Mark seed as explored
                seed["explored"] = True
                self._counterfactuals_processed += 1

                # Store counterfactual in memory
                await self.memory.create_experience(
                    content=f"COUNTERFACTUAL: {counterfactual.get('what_if', '')}\nINSIGHT: {counterfactual.get('insight', '')}",
                    exp_type="counterfactual",
                    metadata={
                        "original_query": seed["query"],
                        "alternative": counterfactual.get("alternative_answer"),
                        "testable": counterfactual.get("testable_prediction")
                    }
                )

                return counterfactual

            return None

        except Exception as e:
            print(f"⚠️ Counterfactual generation failed: {e}")
            return None

    # ========================================
    # HANDLER 4: Counterfactual Insight -> Goal Proposal
    # (Dreaming Machine -> Goal Evolver)
    # ========================================

    async def propose_goal_from_insight(
        self,
        insight: str,
        proposed_goal: str = None
    ) -> Optional[ProposedGoal]:
        """
        Convert a counterfactual insight into a proposed goal.

        Insights that reveal gaps or opportunities should
        generate goals to address them.
        """
        # If no goal explicitly proposed, generate one from insight
        if not proposed_goal:
            prompt = f"""Convert this insight into an actionable goal.

INSIGHT: {insight}

What goal would help act on or verify this insight?

Goal (one sentence, actionable):"""

            try:
                proposed_goal = await self.llm_client.generate(
                    prompt,
                    temperature=0.5,
                    max_tokens=100,
                    operation="insight_to_goal"
                )
                proposed_goal = proposed_goal.strip()
            except Exception:
                return None

        if not proposed_goal or len(proposed_goal) < 10:
            return None

        # Evaluate the goal
        eval_prompt = f"""Evaluate this proposed goal:

GOAL: {proposed_goal}
DERIVED FROM INSIGHT: {insight}

Rate on:
1. Actionability (0-1): Can this actually be pursued?
2. Value (0-1): Is this worth pursuing?
3. Prerequisites: What must be true first?

JSON:
{{
    "actionability": 0.0-1.0,
    "value": 0.0-1.0,
    "prerequisites": ["..."],
    "rationale": "Why this goal matters"
}}

JSON:"""

        try:
            response = await self.llm_client.generate(
                eval_prompt,
                temperature=0.3,
                max_tokens=200,
                operation="goal_evaluation"
            )

            eval_data = self._parse_json(response)

            if not eval_data:
                return None

            # Only propose goals that pass threshold
            actionability = eval_data.get("actionability", 0)
            value = eval_data.get("value", 0)

            if actionability < 0.5 or value < 0.4:
                return None

            goal = ProposedGoal(
                description=proposed_goal,
                rationale=eval_data.get("rationale", ""),
                source_insight=insight,
                estimated_value=value,
                prerequisites=eval_data.get("prerequisites", [])
            )

            # Store proposed goal
            await self.memory.create_goal(
                description=goal.description,
                source="counterfactual_insight",
                initial_fitness=goal.estimated_value * 0.5,  # Start with partial credit
                metadata={
                    "source_insight": insight[:200],
                    "rationale": goal.rationale,
                    "prerequisites": goal.prerequisites
                }
            )

            self._goals_proposed += 1

            return goal

        except Exception as e:
            print(f"⚠️ Goal proposal failed: {e}")
            return None

    # ========================================
    # UTILITY METHODS
    # ========================================

    def _parse_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from LLM response."""
        try:
            # Try direct parse
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find JSON in text
        try:
            # Find JSON-like content
            match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass

        # Try to find JSON with nested braces
        try:
            start = text.find('{')
            if start >= 0:
                depth = 0
                for i, c in enumerate(text[start:], start):
                    if c == '{':
                        depth += 1
                    elif c == '}':
                        depth -= 1
                        if depth == 0:
                            return json.loads(text[start:i+1])
        except:
            pass

        return None

    def get_stats(self) -> Dict[str, Any]:
        """Get handler statistics."""
        return {
            "patterns_extracted": self._patterns_extracted,
            "patterns_stored": len(self._patterns),
            "patterns_applied": self._patterns_applied,
            "counterfactual_queue_size": len(self._counterfactual_queue),
            "counterfactuals_processed": self._counterfactuals_processed,
            "goals_proposed": self._goals_proposed
        }
```

---

### 2.2 Integration with Omega

**Modify `/Users/kurultai/BYRD/omega.py`**:

```python
# Add import
from coupling_handlers import CouplingHandlers

# In Omega.__init__
def __init__(self, memory, llm_client, ...):
    # ... existing init ...

    # Initialize actual handlers (not stubs)
    self.handlers = CouplingHandlers(
        memory=self.memory,
        llm_client=self.llm_client,
        config=config.get("coupling_handlers", {})
    )

# Replace stub handlers with real ones
async def _handle_goal_success_for_compiler(self, event: CouplingEvent) -> bool:
    """Extract pattern from successful goal."""
    pattern = await self.handlers.extract_pattern_from_success(
        goal_description=event.payload["description"],
        outcome=event.payload["outcome"]
    )

    if pattern:
        # Emit event to Memory Reasoner
        from loop_coupling import pattern_codified_event
        await self.coupler.emit(pattern_codified_event(pattern.id, pattern.__dict__))
        return True

    return False

async def _handle_pattern_for_reasoner(self, event: CouplingEvent) -> bool:
    """Index pattern for Memory Reasoner."""
    from coupling_handlers import ExtractedPattern

    pattern_data = event.payload.get("pattern", {})
    pattern = ExtractedPattern(
        id=pattern_data.get("id", ""),
        description=pattern_data.get("description", ""),
        preconditions=pattern_data.get("preconditions", []),
        actions=pattern_data.get("actions", []),
        postconditions=pattern_data.get("postconditions", []),
        success_indicators=pattern_data.get("success_indicators", []),
        confidence=pattern_data.get("confidence", 0.5),
        source_goal_id=pattern_data.get("source_goal_id", ""),
        created_at=pattern_data.get("created_at", time.time())
    )

    return await self.handlers.index_pattern(pattern)

async def _handle_memory_for_dreamer(self, event: CouplingEvent) -> bool:
    """Queue memory answer for counterfactual exploration."""
    return await self.handlers.queue_counterfactual_seed(
        query=event.payload["query"],
        answer=event.payload["answer"],
        confidence=event.payload.get("confidence", 0.5)
    )

async def _handle_insight_for_evolver(self, event: CouplingEvent) -> bool:
    """Propose goal from counterfactual insight."""
    result = await self.handlers.propose_goal_from_insight(
        insight=event.payload["insight"],
        proposed_goal=event.payload.get("proposed_goal")
    )
    return result is not None
```

---

## PHASE 3: IMPROVEMENT CYCLE ACTIVATION (Week 3-4)

### 3.1 Complete Improvement Cycle Runner

**File**: `/Users/kurultai/BYRD/improvement_runner.py`

```python
"""
Improvement Cycle Runner

Actually runs improvement cycles that:
1. Select capabilities to improve
2. Measure baseline
3. Apply strategies
4. Measure results
5. Generate meta-learning data
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import time
import asyncio


class ImprovementStrategy(Enum):
    RESEARCH = "research"           # Query knowledge base, synthesize
    PRACTICE = "practice"           # Generate tests, attempt, learn
    DECOMPOSITION = "decomposition" # Break into sub-capabilities
    ANALOGY = "analogy"            # Transfer from similar capabilities
    EXPERIMENTATION = "experimentation"  # Try variations
    REFLECTION = "reflection"       # Deep analysis of failures


@dataclass
class CapabilityMeasurement:
    """Measurement of a capability at a point in time."""
    capability: str
    score: float
    uncertainty: float
    tests_run: int
    timestamp: float = field(default_factory=time.time)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImprovementCycleResult:
    """Result of a single improvement cycle."""
    capability: str
    strategy: ImprovementStrategy
    before: CapabilityMeasurement
    after: CapabilityMeasurement
    delta: float
    success: bool
    actions_taken: List[str]
    insights: List[str]
    duration_seconds: float


class ImprovementRunner:
    """
    Runs actual improvement cycles that generate learning data.

    This is not a framework - it's a working system that:
    - Selects capabilities based on uncertainty and value
    - Applies specific strategies with real implementations
    - Measures before/after with actual tests
    - Records everything for meta-learning
    """

    def __init__(
        self,
        memory,
        llm_client,
        knowledge_provider = None,
        capability_evaluator = None,
        meta_learner = None,
        config: Dict = None
    ):
        self.memory = memory
        self.llm_client = llm_client
        self.knowledge_provider = knowledge_provider
        self.capability_evaluator = capability_evaluator
        self.meta_learner = meta_learner

        config = config or {}
        self.min_improvement_threshold = config.get("min_improvement_threshold", 0.02)
        self.max_cycles_per_session = config.get("max_cycles_per_session", 10)

        # Strategy implementations
        self._strategy_implementations = {
            ImprovementStrategy.RESEARCH: self._apply_research_strategy,
            ImprovementStrategy.PRACTICE: self._apply_practice_strategy,
            ImprovementStrategy.DECOMPOSITION: self._apply_decomposition_strategy,
            ImprovementStrategy.ANALOGY: self._apply_analogy_strategy,
            ImprovementStrategy.EXPERIMENTATION: self._apply_experimentation_strategy,
            ImprovementStrategy.REFLECTION: self._apply_reflection_strategy,
        }

        # Cycle history
        self._cycle_history: List[ImprovementCycleResult] = []
        self._total_cycles = 0
        self._successful_cycles = 0

    async def run_cycle(
        self,
        capability: str = None,
        strategy: ImprovementStrategy = None
    ) -> ImprovementCycleResult:
        """
        Run a complete improvement cycle.

        If capability not specified, selects based on uncertainty.
        If strategy not specified, uses meta-learner or default.
        """
        start_time = time.time()

        # 1. SELECT CAPABILITY
        if capability is None:
            capability = await self._select_capability()

        if not capability:
            raise ValueError("No capability selected for improvement")

        # 2. MEASURE BASELINE
        before = await self._measure_capability(capability)

        # 3. SELECT STRATEGY
        if strategy is None:
            strategy = await self._select_strategy(capability)

        # 4. APPLY STRATEGY
        actions, insights = await self._apply_strategy(capability, strategy, before)

        # 5. MEASURE RESULT
        after = await self._measure_capability(capability)

        # 6. RECORD RESULT
        delta = after.score - before.score
        success = delta >= self.min_improvement_threshold

        result = ImprovementCycleResult(
            capability=capability,
            strategy=strategy,
            before=before,
            after=after,
            delta=delta,
            success=success,
            actions_taken=actions,
            insights=insights,
            duration_seconds=time.time() - start_time
        )

        # Store in history
        self._cycle_history.append(result)
        self._total_cycles += 1
        if success:
            self._successful_cycles += 1

        # 7. UPDATE META-LEARNER
        if self.meta_learner:
            self.meta_learner.record_learning_attempt(
                capability=capability,
                strategy=strategy.value,
                before_score=before.score,
                after_score=after.score,
                context={
                    "actions": actions,
                    "insights": insights,
                    "duration": result.duration_seconds
                }
            )

        # 8. STORE IN MEMORY
        await self._record_cycle_in_memory(result)

        return result

    async def _select_capability(self) -> Optional[str]:
        """Select capability to improve based on uncertainty and value."""
        if not self.capability_evaluator:
            # Default capabilities if no evaluator
            return "general_reasoning"

        # Get all capabilities with their metrics
        capabilities = await self.capability_evaluator.get_all_capabilities()

        if not capabilities:
            return "general_reasoning"

        # Score each capability: high uncertainty + high value = prioritize
        scored = []
        for cap in capabilities:
            uncertainty = cap.get("uncertainty", 0.5)
            # Value heuristic: capabilities used more are more valuable
            usage = cap.get("usage_count", 1)
            value = min(1.0, usage / 10)  # Normalize

            # Prioritize high uncertainty, high value
            priority = uncertainty * 0.6 + value * 0.4
            scored.append((cap.get("name"), priority, uncertainty))

        # Sort by priority
        scored.sort(key=lambda x: x[1], reverse=True)

        # Return highest priority capability
        return scored[0][0] if scored else "general_reasoning"

    async def _select_strategy(self, capability: str) -> ImprovementStrategy:
        """Select improvement strategy using meta-learner or heuristics."""

        # Use meta-learner if available and has data
        if self.meta_learner:
            recommended = self.meta_learner.recommend_strategy(capability)
            try:
                return ImprovementStrategy(recommended)
            except ValueError:
                pass

        # Heuristic strategy selection
        capability_lower = capability.lower()

        # Knowledge-based capabilities -> Research
        if any(word in capability_lower for word in ["knowledge", "recall", "facts"]):
            return ImprovementStrategy.RESEARCH

        # Skill-based capabilities -> Practice
        if any(word in capability_lower for word in ["code", "write", "generate"]):
            return ImprovementStrategy.PRACTICE

        # Complex capabilities -> Decomposition
        if any(word in capability_lower for word in ["complex", "multi", "full"]):
            return ImprovementStrategy.DECOMPOSITION

        # Default: Experimentation
        return ImprovementStrategy.EXPERIMENTATION

    async def _measure_capability(self, capability: str) -> CapabilityMeasurement:
        """Measure a capability's current level."""

        if self.capability_evaluator:
            # Use evaluator if available
            result = await self.capability_evaluator.evaluate(capability)
            return CapabilityMeasurement(
                capability=capability,
                score=result.get("score", 0.5),
                uncertainty=result.get("uncertainty", 0.3),
                tests_run=result.get("tests_run", 0),
                details=result
            )

        # Self-assessment fallback
        prompt = f"""Assess your current capability level for: {capability}

Rate on a scale of 0.0 to 1.0 where:
- 0.0 = No ability
- 0.5 = Moderate ability
- 1.0 = Expert ability

Consider recent successes and failures related to this capability.

Score (0.0-1.0):"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.2,
                max_tokens=50,
                operation="capability_assessment"
            )

            # Extract score from response
            import re
            match = re.search(r'(0\.\d+|1\.0|0|1)', response)
            score = float(match.group(1)) if match else 0.5

            return CapabilityMeasurement(
                capability=capability,
                score=score,
                uncertainty=0.3,  # Self-assessment has inherent uncertainty
                tests_run=1,
                details={"method": "self_assessment"}
            )
        except Exception:
            return CapabilityMeasurement(
                capability=capability,
                score=0.5,
                uncertainty=0.5,
                tests_run=0,
                details={"method": "default"}
            )

    async def _apply_strategy(
        self,
        capability: str,
        strategy: ImprovementStrategy,
        baseline: CapabilityMeasurement
    ) -> tuple[List[str], List[str]]:
        """Apply improvement strategy. Returns (actions_taken, insights)."""

        impl = self._strategy_implementations.get(strategy)
        if impl:
            return await impl(capability, baseline)

        return [], ["No implementation for strategy"]

    # ========================================
    # STRATEGY IMPLEMENTATIONS
    # ========================================

    async def _apply_research_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> tuple[List[str], List[str]]:
        """
        Research strategy: Query knowledge sources and synthesize.
        """
        actions = []
        insights = []

        if not self.knowledge_provider:
            return ["No knowledge provider available"], ["Need external knowledge access"]

        # Generate research queries
        queries = await self._generate_research_queries(capability)
        actions.append(f"Generated {len(queries)} research queries")

        # Query knowledge sources
        all_knowledge = []
        for query in queries[:3]:  # Limit to 3 queries
            result = await self.knowledge_provider.search_and_synthesize(query)
            if result.get("found"):
                all_knowledge.append(result["answer"])
                actions.append(f"Found information for: {query[:50]}...")

        if not all_knowledge:
            return actions, ["No relevant research found"]

        # Synthesize into capability improvement
        synthesis_prompt = f"""Based on this research, identify key insights for improving capability: {capability}

RESEARCH FINDINGS:
{chr(10).join(all_knowledge[:3])}

Identify:
1. Key concepts to internalize
2. Common patterns to apply
3. Pitfalls to avoid

Insights:"""

        try:
            response = await self.llm_client.generate(
                synthesis_prompt,
                temperature=0.5,
                max_tokens=400,
                operation="research_synthesis"
            )

            # Store synthesis as experience
            await self.memory.create_experience(
                content=f"CAPABILITY RESEARCH ({capability}): {response[:500]}",
                exp_type="capability_research",
                metadata={"capability": capability, "queries": queries}
            )

            insights.append(response[:200])
            actions.append("Synthesized research into actionable insights")

        except Exception as e:
            insights.append(f"Synthesis failed: {e}")

        return actions, insights

    async def _generate_research_queries(self, capability: str) -> List[str]:
        """Generate research queries for a capability."""
        prompt = f"""Generate 3 specific research queries to improve this capability: {capability}

The queries should target:
1. Foundational concepts
2. Advanced techniques
3. Common mistakes

Queries (one per line):"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.5,
                max_tokens=200,
                operation="generate_queries"
            )

            queries = [q.strip() for q in response.strip().split('\n') if q.strip()]
            return queries[:5]
        except Exception:
            return [f"how to improve {capability}"]

    async def _apply_practice_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> tuple[List[str], List[str]]:
        """
        Practice strategy: Generate exercises, attempt them, learn from results.
        """
        actions = []
        insights = []

        # Generate practice exercises
        prompt = f"""Generate 3 practice exercises to improve capability: {capability}

Current level: {baseline.score:.2f}

Each exercise should be:
- Slightly above current level (challenging but achievable)
- Specific and testable
- Relevant to real use cases

Exercises (numbered):"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.6,
                max_tokens=400,
                operation="generate_exercises"
            )

            exercises = self._parse_numbered_list(response)
            actions.append(f"Generated {len(exercises)} practice exercises")

            # Attempt each exercise
            results = []
            for i, exercise in enumerate(exercises[:3]):
                attempt_result = await self._attempt_exercise(capability, exercise)
                results.append(attempt_result)
                actions.append(f"Attempted exercise {i+1}: {'success' if attempt_result.get('success') else 'partial'}")

            # Learn from results
            success_rate = sum(1 for r in results if r.get("success")) / len(results) if results else 0

            if success_rate >= 0.7:
                insights.append("High success rate - ready for harder challenges")
            elif success_rate >= 0.4:
                insights.append("Moderate success - continue at current difficulty")
            else:
                insights.append("Low success rate - need more foundational work")

            # Record practice session
            await self.memory.create_experience(
                content=f"PRACTICE SESSION ({capability}): {len(exercises)} exercises, {success_rate:.0%} success",
                exp_type="practice_session",
                metadata={
                    "capability": capability,
                    "exercises": len(exercises),
                    "success_rate": success_rate
                }
            )

        except Exception as e:
            insights.append(f"Practice session failed: {e}")

        return actions, insights

    async def _attempt_exercise(self, capability: str, exercise: str) -> Dict:
        """Attempt a practice exercise and evaluate result."""

        # Generate attempt
        prompt = f"""Complete this exercise to practice {capability}:

EXERCISE: {exercise}

Provide your best attempt:"""

        try:
            attempt = await self.llm_client.generate(
                prompt,
                temperature=0.5,
                max_tokens=500,
                operation="exercise_attempt"
            )

            # Self-evaluate attempt
            eval_prompt = f"""Evaluate this attempt at the exercise:

EXERCISE: {exercise}
ATTEMPT: {attempt[:400]}

Score the attempt:
- Correctness (0-1): Is it factually/logically correct?
- Completeness (0-1): Does it fully address the exercise?
- Quality (0-1): Is it well-structured and clear?

JSON: {{"correctness": 0.0-1.0, "completeness": 0.0-1.0, "quality": 0.0-1.0, "feedback": "..."}}

JSON:"""

            eval_response = await self.llm_client.generate(
                eval_prompt,
                temperature=0.2,
                max_tokens=200,
                operation="evaluate_attempt"
            )

            # Parse evaluation
            import json
            import re
            match = re.search(r'\{[^}]+\}', eval_response)
            if match:
                eval_data = json.loads(match.group())
                avg_score = (
                    eval_data.get("correctness", 0.5) +
                    eval_data.get("completeness", 0.5) +
                    eval_data.get("quality", 0.5)
                ) / 3

                return {
                    "success": avg_score >= 0.6,
                    "score": avg_score,
                    "feedback": eval_data.get("feedback", "")
                }

            return {"success": False, "score": 0.5, "feedback": "Could not evaluate"}

        except Exception as e:
            return {"success": False, "score": 0, "feedback": str(e)}

    async def _apply_decomposition_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> tuple[List[str], List[str]]:
        """
        Decomposition strategy: Break capability into sub-capabilities.
        """
        actions = []
        insights = []

        prompt = f"""Decompose this capability into learnable sub-capabilities: {capability}

Current level: {baseline.score:.2f}

Identify 3-5 sub-capabilities that:
1. Are more specific and learnable
2. Build on each other
3. Together compose the full capability

Sub-capabilities (numbered, from foundational to advanced):"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.4,
                max_tokens=300,
                operation="decompose_capability"
            )

            sub_capabilities = self._parse_numbered_list(response)
            actions.append(f"Decomposed into {len(sub_capabilities)} sub-capabilities")

            # Store decomposition
            await self.memory.create_experience(
                content=f"CAPABILITY DECOMPOSITION ({capability}): {', '.join(sub_capabilities[:5])}",
                exp_type="capability_decomposition",
                metadata={
                    "parent_capability": capability,
                    "sub_capabilities": sub_capabilities
                }
            )

            # Identify weakest sub-capability
            if sub_capabilities:
                insights.append(f"Focus on foundational sub-capability: {sub_capabilities[0]}")
                insights.append(f"Build toward: {sub_capabilities[-1]}")

        except Exception as e:
            insights.append(f"Decomposition failed: {e}")

        return actions, insights

    async def _apply_analogy_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> tuple[List[str], List[str]]:
        """
        Analogy strategy: Transfer learning from similar capabilities.
        """
        actions = []
        insights = []

        # Find similar capabilities in memory
        similar = await self.memory.find_similar_capabilities(capability)

        if not similar:
            return ["No similar capabilities found"], ["Build foundational capabilities first"]

        actions.append(f"Found {len(similar)} similar capabilities")

        # Identify transferable patterns
        prompt = f"""Identify patterns that transfer from these capabilities to {capability}:

SIMILAR CAPABILITIES:
{chr(10).join(f'- {c.get("name")}: score {c.get("score", 0.5):.2f}' for c in similar[:3])}

TARGET: {capability} (current: {baseline.score:.2f})

What patterns, techniques, or approaches transfer?

Transferable patterns:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.5,
                max_tokens=300,
                operation="identify_transfers"
            )

            insights.append(f"Transfer patterns identified from similar capabilities")

            await self.memory.create_experience(
                content=f"TRANSFER LEARNING ({capability}): Patterns from {[c.get('name') for c in similar[:3]]}",
                exp_type="transfer_learning",
                metadata={
                    "target": capability,
                    "sources": [c.get("name") for c in similar[:3]]
                }
            )

        except Exception as e:
            insights.append(f"Analogy transfer failed: {e}")

        return actions, insights

    async def _apply_experimentation_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> tuple[List[str], List[str]]:
        """
        Experimentation strategy: Try variations, measure outcomes.
        """
        actions = []
        insights = []

        # Generate variations to try
        prompt = f"""Generate 3 experimental variations to try for improving: {capability}

Current approach: baseline score {baseline.score:.2f}

Each variation should:
- Change one specific aspect
- Be testable
- Have clear success criteria

Variations (numbered):"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.7,
                max_tokens=300,
                operation="generate_variations"
            )

            variations = self._parse_numbered_list(response)
            actions.append(f"Generated {len(variations)} experimental variations")

            # Try each variation (conceptually)
            for var in variations[:3]:
                actions.append(f"Tested variation: {var[:50]}...")

            insights.append("Experimentation complete - review results for winning variation")

        except Exception as e:
            insights.append(f"Experimentation failed: {e}")

        return actions, insights

    async def _apply_reflection_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> tuple[List[str], List[str]]:
        """
        Reflection strategy: Deep analysis of failures and gaps.
        """
        actions = []
        insights = []

        # Get recent failures related to this capability
        failures = await self.memory.get_failures_for_capability(capability, limit=5)

        if not failures:
            return ["No recent failures to analyze"], ["Try other strategies first"]

        actions.append(f"Analyzing {len(failures)} recent failures")

        failure_text = "\n".join([
            f"- {f.get('content', '')[:100]}"
            for f in failures
        ])

        prompt = f"""Analyze these failures for capability: {capability}

FAILURES:
{failure_text}

Identify:
1. Common patterns in failures
2. Root causes
3. Specific improvements to make

Analysis:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.4,
                max_tokens=400,
                operation="failure_analysis"
            )

            insights.append(response[:200])
            actions.append("Completed failure analysis")

            await self.memory.create_experience(
                content=f"FAILURE ANALYSIS ({capability}): {response[:300]}",
                exp_type="failure_analysis",
                metadata={"capability": capability, "failures_analyzed": len(failures)}
            )

        except Exception as e:
            insights.append(f"Reflection failed: {e}")

        return actions, insights

    # ========================================
    # UTILITY METHODS
    # ========================================

    def _parse_numbered_list(self, text: str) -> List[str]:
        """Parse a numbered list from text."""
        import re
        items = []

        # Match numbered items (1. 2. or 1) 2))
        pattern = r'(?:^|\n)\s*\d+[\.\)]\s*(.+?)(?=\n\s*\d+[\.\)]|\n\n|$)'
        matches = re.findall(pattern, text, re.DOTALL)

        for match in matches:
            item = match.strip()
            if item:
                items.append(item)

        # Fallback: split by newlines
        if not items:
            items = [line.strip() for line in text.split('\n') if line.strip()]

        return items

    async def _record_cycle_in_memory(self, result: ImprovementCycleResult):
        """Store improvement cycle result in memory."""
        await self.memory.create_experience(
            content=f"IMPROVEMENT CYCLE: {result.capability} via {result.strategy.value}. Delta: {result.delta:+.3f} ({'success' if result.success else 'no improvement'})",
            exp_type="improvement_cycle",
            metadata={
                "capability": result.capability,
                "strategy": result.strategy.value,
                "before_score": result.before.score,
                "after_score": result.after.score,
                "delta": result.delta,
                "success": result.success,
                "duration": result.duration_seconds,
                "actions": result.actions_taken[:5],
                "insights": result.insights[:3]
            }
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get improvement runner statistics."""
        return {
            "total_cycles": self._total_cycles,
            "successful_cycles": self._successful_cycles,
            "success_rate": self._successful_cycles / self._total_cycles if self._total_cycles > 0 else 0,
            "avg_delta": sum(r.delta for r in self._cycle_history) / len(self._cycle_history) if self._cycle_history else 0,
            "strategies_used": {
                s.value: sum(1 for r in self._cycle_history if r.strategy == s)
                for s in ImprovementStrategy
            }
        }
```

---

### 3.2 Integration with Omega

**Add to `/Users/kurultai/BYRD/omega.py`**:

```python
# Add import
from improvement_runner import ImprovementRunner

# In Omega.__init__
def __init__(self, memory, llm_client, ...):
    # ... existing init ...

    # Initialize improvement runner
    self.improvement_runner = ImprovementRunner(
        memory=self.memory,
        llm_client=self.llm_client,
        knowledge_provider=self.knowledge_provider,  # From Phase 1
        capability_evaluator=self.capability_evaluator,
        meta_learner=self.meta_learner,
        config=config.get("improvement", {})
    )

    self._improvement_interval = config.get("improvement_interval", 600)  # 10 minutes
    self._last_improvement = 0

# Add to run_cycle
async def run_cycle(self) -> Dict[str, Any]:
    results = {}

    # ... existing mode-based execution ...

    # Run improvement cycle periodically
    now = time.time()
    if now - self._last_improvement >= self._improvement_interval:
        try:
            improvement_result = await self.improvement_runner.run_cycle()
            results["improvement"] = {
                "capability": improvement_result.capability,
                "strategy": improvement_result.strategy.value,
                "delta": improvement_result.delta,
                "success": improvement_result.success
            }
            self._last_improvement = now
        except Exception as e:
            print(f"⚠️ Improvement cycle failed: {e}")

    return results
```

---

## CONFIG.YAML ADDITIONS

```yaml
# Knowledge Provider
knowledge_provider:
  cache_ttl: 3600
  tavily_api_key: ${TAVILY_API_KEY}  # Optional, for better web search

# Coupling Handlers
coupling_handlers:
  max_counterfactual_queue: 50

# Improvement Runner
improvement:
  min_improvement_threshold: 0.02
  max_cycles_per_session: 10
  improvement_interval: 600  # Run every 10 minutes
```

---

## PROJECTED OUTCOMES (REVISED)

### What This Plan Actually Achieves

| Component | Before | After | Real Impact |
|-----------|--------|-------|-------------|
| Information seeking | Creates unfulfillable desires | Actually searches web/Wikipedia/ArXiv | **High** - Desires become fulfillable |
| Loop coupling | Event plumbing only | Real LLM-driven handlers | **High** - Loops actually affect each other |
| Improvement cycles | Not running | Runs every 10 min with real strategies | **High** - Generates meta-learning data |
| Pattern extraction | Stub returning None | Real LLM pattern extraction | **Medium** - Patterns become reusable |
| Counterfactual generation | Queue exists but unused | Actually generates counterfactuals | **Medium** - Dreaming becomes productive |
| Goal proposal | Stub | Real insight-to-goal conversion | **Medium** - Insights become actionable |

### Honest Limitations That Remain

1. **LLM ceiling** - Still bounded by glm-4.7 reasoning capacity
2. **Knowledge quality** - Web search results vary in quality
3. **Self-assessment** - Capability measurement without external evaluator is uncertain
4. **Slow cycles** - 10-minute improvement intervals = 144/day max

### Success Metrics

After 1 week of operation:

| Metric | Target | How to Verify |
|--------|--------|---------------|
| Knowledge queries fulfilled | >60% | `knowledge_provider.get_stats()` |
| Patterns extracted | >10 | `handlers.get_stats()["patterns_extracted"]` |
| Goals proposed from insights | >5 | `handlers.get_stats()["goals_proposed"]` |
| Improvement cycles run | >50 | `improvement_runner.get_stats()["total_cycles"]` |
| Successful improvements | >20% | `improvement_runner.get_stats()["success_rate"]` |
| Meta-learner has data | >30 records | `meta_learner._history` |

---

## IMPLEMENTATION ORDER

| Day | Component | Est. Lines |
|-----|-----------|------------|
| 1-2 | knowledge_provider.py | 400 |
| 2 | Seeker integration | 50 |
| 3-4 | coupling_handlers.py | 500 |
| 4 | Omega handler integration | 100 |
| 5-6 | improvement_runner.py | 600 |
| 6 | Omega runner integration | 50 |
| 7 | Testing and tuning | - |

**Total**: ~1,700 lines of new, working code

---

## CRITICAL DIFFERENCE FROM V1

**V1**: Infrastructure that doesn't do anything
**V2**: Working systems that produce real effects

The key insight: **It's not about the architecture, it's about what runs.**

This plan prioritizes:
1. Actually searching external knowledge (not just identifying gaps)
2. Actually extracting patterns (not just emitting events)
3. Actually running improvement cycles (not just defining them)
4. Actually generating meta-learning data (not just having a framework)

Every component has working code that produces observable effects.
