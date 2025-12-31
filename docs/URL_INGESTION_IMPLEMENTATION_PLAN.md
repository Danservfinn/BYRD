# URL Ingestion Implementation Plan

> BYRD URL Ingestion System - Complete Implementation Guide
>
> **Scope**: YouTube in Phase 1, Auto-ingest only when explicitly requested, 2GB limit, Distinct visualization

---

## Overview

This plan implements a complete URL ingestion system for BYRD, enabling:
- Direct URL submission via API
- Automatic URL detection in chat messages
- Desire-driven URL reading
- Keyword-triggered search+ingest (only when explicitly requested with "read", "absorb", etc.)
- YouTube transcript extraction
- 2GB storage limit with auto-archival
- Distinct WebDocument visualization

---

## Phase 1: Core Infrastructure

### Step 1.1: Create `url_ingestor.py`

**File**: `/Users/kurultai/BYRD/url_ingestor.py`

```python
"""
URL Ingestor - Fetch and absorb web content into BYRD's memory.

Handles:
- HTML pages (via trafilatura)
- PDF files (via PyMuPDF)
- GitHub files (via raw URL)
- YouTube videos (via transcript API)
- Raw text files

Storage: WebDocument nodes with chunking and embeddings.
Limit: 2GB with automatic archival of oldest content.
"""

import asyncio
import hashlib
import re
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from enum import Enum

import httpx

from event_bus import event_bus, Event, EventType
from memory import Memory


class ContentType(Enum):
    HTML = "html"
    PDF = "pdf"
    GITHUB = "github"
    YOUTUBE = "youtube"
    TEXT = "text"
    JSON = "json"
    UNKNOWN = "unknown"


@dataclass
class ExtractedContent:
    """Result of content extraction."""
    title: str
    content: str
    content_type: ContentType
    author: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict] = None


@dataclass
class IngestResult:
    """Result of URL ingestion."""
    success: bool
    document_id: Optional[str] = None
    url: str = ""
    title: Optional[str] = None
    char_count: int = 0
    chunks_created: int = 0
    processing_time_ms: int = 0
    error: Optional[str] = None
    already_exists: bool = False


class URLIngestor:
    """
    Fetches URLs and stores content as WebDocument nodes.

    Features:
    - Per-domain rate limiting
    - Content type detection and extraction
    - Deduplication via content hash
    - 2GB storage limit with auto-archival
    - Integration with DocumentProcessor for chunking
    """

    # Configuration
    STORAGE_LIMIT_BYTES = 2 * 1024 * 1024 * 1024  # 2GB
    MAX_CONTENT_SIZE = 10 * 1024 * 1024  # 10MB per URL
    MIN_CONTENT_LENGTH = 100  # Minimum chars to store
    REQUEST_TIMEOUT = 30.0  # seconds
    RATE_LIMIT_SECONDS = 2.0  # per domain
    MAX_CONCURRENT = 10

    # Blocked patterns (security)
    BLOCKED_PATTERNS = [
        r'^https?://localhost',
        r'^https?://127\.0\.0\.1',
        r'^https?://192\.168\.',
        r'^https?://10\.\d+\.',
        r'^https?://172\.(1[6-9]|2\d|3[01])\.',
        r'\.local(:\d+)?/',
        r'^file://',
    ]

    def __init__(self, memory: Memory, document_processor=None, config: Dict = None):
        self.memory = memory
        self.document_processor = document_processor
        self.config = config or {}

        # Rate limiting state
        self._domain_last_request: Dict[str, float] = {}
        self._semaphore = asyncio.Semaphore(self.MAX_CONCURRENT)

        # HTTP client
        self._client: Optional[httpx.AsyncClient] = None

        # Statistics
        self._total_ingested = 0
        self._total_bytes = 0
        self._failed_count = 0

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.REQUEST_TIMEOUT,
                follow_redirects=True,
                headers={
                    "User-Agent": "BYRD/1.0 (Autonomous Knowledge Acquisition)",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                }
            )
        return self._client

    async def close(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _is_blocked(self, url: str) -> bool:
        """Check if URL matches blocked patterns."""
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        return False

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        parsed = urlparse(url)
        return parsed.netloc.lower()

    async def _rate_limit(self, domain: str):
        """Wait if needed to respect rate limit."""
        now = time.time()
        last_request = self._domain_last_request.get(domain, 0)
        wait_time = self.RATE_LIMIT_SECONDS - (now - last_request)

        if wait_time > 0:
            await asyncio.sleep(wait_time)

        self._domain_last_request[domain] = time.time()

    def _detect_content_type(self, url: str, response: httpx.Response) -> ContentType:
        """Detect content type from URL and response."""
        # Check URL patterns first
        domain = self._get_domain(url)
        path = urlparse(url).path.lower()

        # YouTube
        if 'youtube.com' in domain or 'youtu.be' in domain:
            return ContentType.YOUTUBE

        # GitHub raw files
        if 'github.com' in domain or 'raw.githubusercontent.com' in domain:
            return ContentType.GITHUB

        # PDF
        if path.endswith('.pdf'):
            return ContentType.PDF

        # Check content-type header
        content_type = response.headers.get('content-type', '').lower()

        if 'application/pdf' in content_type:
            return ContentType.PDF
        if 'text/html' in content_type or 'application/xhtml' in content_type:
            return ContentType.HTML
        if 'application/json' in content_type:
            return ContentType.JSON
        if 'text/plain' in content_type:
            return ContentType.TEXT

        return ContentType.UNKNOWN

    async def _extract_html(self, html: str, url: str) -> ExtractedContent:
        """Extract article content from HTML using trafilatura."""
        try:
            import trafilatura

            # Extract main content
            extracted = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=True,
                no_fallback=False,
                favor_precision=True,
                url=url
            )

            # Extract metadata
            metadata = trafilatura.extract_metadata(html)

            title = "Untitled"
            author = None
            date = None
            description = None

            if metadata:
                title = metadata.title or title
                author = metadata.author
                date = metadata.date
                description = metadata.description

            # Fallback title from <title> tag
            if title == "Untitled":
                import re
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()

            return ExtractedContent(
                title=title,
                content=extracted or "",
                content_type=ContentType.HTML,
                author=author,
                date=date,
                description=description
            )
        except ImportError:
            # Fallback: basic extraction
            import re
            # Remove scripts and styles
            text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
            # Remove tags
            text = re.sub(r'<[^>]+>', ' ', text)
            # Clean whitespace
            text = re.sub(r'\s+', ' ', text).strip()

            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "Untitled"

            return ExtractedContent(
                title=title,
                content=text,
                content_type=ContentType.HTML
            )

    async def _extract_youtube(self, url: str) -> ExtractedContent:
        """Extract transcript from YouTube video."""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi

            # Extract video ID
            video_id = None
            if 'youtu.be/' in url:
                video_id = url.split('youtu.be/')[-1].split('?')[0]
            elif 'watch?v=' in url:
                video_id = url.split('watch?v=')[-1].split('&')[0]
            elif '/embed/' in url:
                video_id = url.split('/embed/')[-1].split('?')[0]

            if not video_id:
                return ExtractedContent(
                    title="YouTube Video",
                    content="Could not extract video ID",
                    content_type=ContentType.YOUTUBE
                )

            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ' '.join([entry['text'] for entry in transcript_list])

            # Try to get video title via oEmbed
            try:
                client = await self._get_client()
                oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
                response = await client.get(oembed_url)
                if response.status_code == 200:
                    data = response.json()
                    title = data.get('title', 'YouTube Video')
                    author = data.get('author_name')
                else:
                    title = "YouTube Video"
                    author = None
            except:
                title = "YouTube Video"
                author = None

            return ExtractedContent(
                title=title,
                content=transcript_text,
                content_type=ContentType.YOUTUBE,
                author=author,
                metadata={"video_id": video_id}
            )
        except ImportError:
            return ExtractedContent(
                title="YouTube Video",
                content="youtube-transcript-api not installed",
                content_type=ContentType.YOUTUBE
            )
        except Exception as e:
            return ExtractedContent(
                title="YouTube Video",
                content=f"Could not extract transcript: {str(e)}",
                content_type=ContentType.YOUTUBE
            )

    async def _extract_github(self, url: str, response: httpx.Response) -> ExtractedContent:
        """Extract content from GitHub file."""
        # Convert to raw URL if needed
        raw_url = url
        if 'github.com' in url and '/blob/' in url:
            raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')

        content = response.text

        # Extract filename for title
        path = urlparse(url).path
        filename = path.split('/')[-1] if '/' in path else path

        return ExtractedContent(
            title=filename,
            content=content,
            content_type=ContentType.GITHUB,
            metadata={"raw_url": raw_url}
        )

    async def _extract_pdf(self, content: bytes, url: str) -> ExtractedContent:
        """Extract text from PDF."""
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(stream=content, filetype="pdf")
            text_parts = []

            for page in doc:
                text_parts.append(page.get_text())

            full_text = '\n\n'.join(text_parts)

            # Get title from metadata or filename
            metadata = doc.metadata
            title = metadata.get('title') or urlparse(url).path.split('/')[-1]
            author = metadata.get('author')

            doc.close()

            return ExtractedContent(
                title=title,
                content=full_text,
                content_type=ContentType.PDF,
                author=author
            )
        except ImportError:
            return ExtractedContent(
                title=urlparse(url).path.split('/')[-1],
                content="PyMuPDF not installed - cannot extract PDF",
                content_type=ContentType.PDF
            )
        except Exception as e:
            return ExtractedContent(
                title=urlparse(url).path.split('/')[-1],
                content=f"PDF extraction failed: {str(e)}",
                content_type=ContentType.PDF
            )

    async def ingest(
        self,
        url: str,
        context: Optional[str] = None,
        provenance: Optional[str] = None,  # desire_id, "api", "chat", "auto"
        force: bool = False
    ) -> IngestResult:
        """
        Ingest content from a URL into BYRD's memory.

        Args:
            url: The URL to fetch and ingest
            context: Optional context about why this URL is being ingested
            provenance: What triggered the ingestion (desire_id, api, chat, auto)
            force: If True, re-ingest even if URL already exists

        Returns:
            IngestResult with document_id and metadata
        """
        start_time = time.time()

        # Validate URL
        if self._is_blocked(url):
            return IngestResult(
                success=False,
                url=url,
                error="URL is blocked (localhost/private network)"
            )

        # Check if already exists (unless forcing)
        if not force:
            existing = await self.memory.get_web_document_by_url(url)
            if existing:
                return IngestResult(
                    success=True,
                    url=url,
                    document_id=existing['id'],
                    title=existing.get('title'),
                    char_count=existing.get('char_count', 0),
                    already_exists=True,
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )

        # Emit start event
        await event_bus.emit(Event(
            type=EventType.URL_INGEST_STARTED,
            data={"url": url, "provenance": provenance}
        ))

        try:
            async with self._semaphore:
                # Rate limit
                domain = self._get_domain(url)
                await self._rate_limit(domain)

                # Fetch
                client = await self._get_client()

                # Handle YouTube separately (no need to fetch page)
                if 'youtube.com' in domain or 'youtu.be' in domain:
                    extracted = await self._extract_youtube(url)
                else:
                    response = await client.get(url)
                    response.raise_for_status()

                    # Check size
                    content_length = len(response.content)
                    if content_length > self.MAX_CONTENT_SIZE:
                        return IngestResult(
                            success=False,
                            url=url,
                            error=f"Content too large: {content_length} bytes (max {self.MAX_CONTENT_SIZE})"
                        )

                    # Detect and extract content
                    content_type = self._detect_content_type(url, response)

                    if content_type == ContentType.HTML:
                        extracted = await self._extract_html(response.text, url)
                    elif content_type == ContentType.PDF:
                        extracted = await self._extract_pdf(response.content, url)
                    elif content_type == ContentType.GITHUB:
                        extracted = await self._extract_github(url, response)
                    elif content_type == ContentType.JSON:
                        import json
                        extracted = ExtractedContent(
                            title=urlparse(url).path.split('/')[-1] or "JSON Data",
                            content=json.dumps(response.json(), indent=2),
                            content_type=ContentType.JSON
                        )
                    else:
                        # Text or unknown - store as-is
                        extracted = ExtractedContent(
                            title=urlparse(url).path.split('/')[-1] or "Web Content",
                            content=response.text,
                            content_type=content_type
                        )

                # Validate extracted content
                if len(extracted.content) < self.MIN_CONTENT_LENGTH:
                    return IngestResult(
                        success=False,
                        url=url,
                        error=f"Content too short: {len(extracted.content)} chars (min {self.MIN_CONTENT_LENGTH})"
                    )

                # Check storage limit before storing
                await self._enforce_storage_limit()

                # Store as WebDocument
                doc_id = await self.memory.store_web_document(
                    url=url,
                    title=extracted.title,
                    content=extracted.content,
                    content_type=extracted.content_type.value,
                    author=extracted.author,
                    date=extracted.date,
                    description=extracted.description,
                    provenance=provenance,
                    context=context,
                    metadata=extracted.metadata
                )

                # Process with DocumentProcessor for chunking/embeddings (if available)
                chunks_created = 0
                if self.document_processor:
                    try:
                        await self.document_processor.process_web_document(doc_id, extracted.content)
                        # Get chunk count
                        chunks = await self.memory.get_document_chunks(doc_id)
                        chunks_created = len(chunks) if chunks else 0
                    except Exception as e:
                        print(f"[URLIngestor] Chunking failed: {e}")

                # Update stats
                self._total_ingested += 1
                self._total_bytes += len(extracted.content)

                # Emit completion event
                processing_time_ms = int((time.time() - start_time) * 1000)
                await event_bus.emit(Event(
                    type=EventType.URL_INGEST_COMPLETE,
                    data={
                        "url": url,
                        "document_id": doc_id,
                        "title": extracted.title,
                        "char_count": len(extracted.content),
                        "chunks_created": chunks_created,
                        "processing_time_ms": processing_time_ms
                    }
                ))

                return IngestResult(
                    success=True,
                    url=url,
                    document_id=doc_id,
                    title=extracted.title,
                    char_count=len(extracted.content),
                    chunks_created=chunks_created,
                    processing_time_ms=processing_time_ms
                )

        except httpx.HTTPStatusError as e:
            self._failed_count += 1
            await event_bus.emit(Event(
                type=EventType.URL_INGEST_FAILED,
                data={"url": url, "error": f"HTTP {e.response.status_code}"}
            ))
            return IngestResult(
                success=False,
                url=url,
                error=f"HTTP error: {e.response.status_code}"
            )
        except Exception as e:
            self._failed_count += 1
            await event_bus.emit(Event(
                type=EventType.URL_INGEST_FAILED,
                data={"url": url, "error": str(e)}
            ))
            return IngestResult(
                success=False,
                url=url,
                error=str(e)
            )

    async def ingest_multiple(
        self,
        urls: List[str],
        provenance: Optional[str] = None,
        max_concurrent: int = 5
    ) -> List[IngestResult]:
        """Ingest multiple URLs concurrently."""
        semaphore = asyncio.Semaphore(max_concurrent)

        async def ingest_with_semaphore(url: str) -> IngestResult:
            async with semaphore:
                return await self.ingest(url, provenance=provenance)

        tasks = [ingest_with_semaphore(url) for url in urls]
        return await asyncio.gather(*tasks)

    async def _enforce_storage_limit(self):
        """Archive oldest documents if over storage limit."""
        usage = await self.memory.get_web_storage_usage()

        if usage['total_bytes'] < self.STORAGE_LIMIT_BYTES:
            return

        # Archive oldest until under limit
        archived = await self.memory.archive_oldest_web_documents(
            target_bytes=self.STORAGE_LIMIT_BYTES
        )

        if archived > 0:
            print(f"[URLIngestor] Archived {archived} documents to stay under 2GB limit")
            await event_bus.emit(Event(
                type=EventType.NODE_UPDATED,
                data={
                    "action": "storage_cleanup",
                    "archived_count": archived,
                    "reason": "storage_limit"
                }
            ))

    def get_stats(self) -> Dict:
        """Get ingestion statistics."""
        return {
            "total_ingested": self._total_ingested,
            "total_bytes": self._total_bytes,
            "failed_count": self._failed_count,
            "storage_limit_bytes": self.STORAGE_LIMIT_BYTES
        }


# URL detection regex for chat messages
URL_PATTERN = re.compile(
    r'https?://[^\s<>"{}|\\^`\[\]]+',
    re.IGNORECASE
)


def extract_urls(text: str) -> List[str]:
    """Extract all URLs from text."""
    return URL_PATTERN.findall(text)
```

---

### Step 1.2: Add Memory Methods

**File**: `/Users/kurultai/BYRD/memory.py`

Add after the `store_document` method (~line 1280):

```python
# =========================================================================
# WEB DOCUMENTS (URLs fetched and stored)
# =========================================================================

async def store_web_document(
    self,
    url: str,
    title: str,
    content: str,
    content_type: str,
    author: Optional[str] = None,
    date: Optional[str] = None,
    description: Optional[str] = None,
    provenance: Optional[str] = None,
    context: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> str:
    """
    Store a web document fetched from a URL.

    Args:
        url: Source URL (used as unique identifier)
        title: Page/document title
        content: Extracted text content
        content_type: Type (html, pdf, youtube, github, etc.)
        author: Author if available
        date: Publication date if available
        description: Meta description if available
        provenance: What triggered ingestion (desire_id, api, chat, auto)
        context: Why this URL was ingested
        metadata: Additional metadata

    Returns:
        WebDocument node ID
    """
    import hashlib
    from datetime import datetime, timezone

    # Use URL hash as stable ID
    doc_id = f"webdoc_{hashlib.sha256(url.encode()).hexdigest()[:16]}"

    # Content hash for deduplication
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:32]

    # Extract domain
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.lower()

    char_count = len(content)

    async with self.driver.session() as session:
        # Check if exists
        existing = await session.run("""
            MATCH (wd:WebDocument {id: $id})
            RETURN wd.content_hash as hash, wd.version as version
        """, id=doc_id)
        record = await existing.single()

        if record:
            old_hash = record["hash"]
            old_version = record["version"] or 1

            if old_hash == content_hash:
                # Same content, just update last_fetched
                await session.run("""
                    MATCH (wd:WebDocument {id: $id})
                    SET wd.last_fetched = datetime()
                """, id=doc_id)
                return doc_id

            # Content changed - update
            await session.run("""
                MATCH (wd:WebDocument {id: $id})
                SET wd.content = $content,
                    wd.content_hash = $hash,
                    wd.title = $title,
                    wd.updated_at = datetime(),
                    wd.last_fetched = datetime(),
                    wd.version = $version,
                    wd.char_count = $char_count
            """, id=doc_id, content=content, hash=content_hash,
                title=title, version=old_version + 1, char_count=char_count)
        else:
            # Create new
            await session.run("""
                CREATE (wd:Document:WebDocument {
                    id: $id,
                    url: $url,
                    domain: $domain,
                    title: $title,
                    content: $content,
                    content_hash: $hash,
                    content_type: $content_type,
                    author: $author,
                    date: $date,
                    description: $description,
                    provenance: $provenance,
                    context: $context,
                    char_count: $char_count,
                    fetched_at: datetime(),
                    last_fetched: datetime(),
                    created_at: datetime(),
                    version: 1,
                    archived: false
                })
            """, id=doc_id, url=url, domain=domain, title=title,
                content=content, hash=content_hash, content_type=content_type,
                author=author, date=date, description=description,
                provenance=provenance, context=context, char_count=char_count)

            # Emit event
            await event_bus.emit(Event(
                type=EventType.NODE_CREATED,
                data={
                    "id": doc_id,
                    "node_type": "WebDocument",
                    "url": url,
                    "title": title,
                    "domain": domain
                }
            ))

    return doc_id

async def get_web_document_by_url(self, url: str) -> Optional[Dict]:
    """Get a web document by its URL."""
    import hashlib
    doc_id = f"webdoc_{hashlib.sha256(url.encode()).hexdigest()[:16]}"

    async with self.driver.session() as session:
        result = await session.run("""
            MATCH (wd:WebDocument {id: $id})
            WHERE wd.archived IS NULL OR wd.archived = false
            RETURN wd
        """, id=doc_id)
        record = await result.single()
        if record:
            return dict(record["wd"])
    return None

async def list_web_documents(
    self,
    limit: int = 50,
    include_archived: bool = False
) -> List[Dict]:
    """List web documents, newest first."""
    async with self.driver.session() as session:
        query = """
            MATCH (wd:WebDocument)
        """
        if not include_archived:
            query += " WHERE wd.archived IS NULL OR wd.archived = false"
        query += """
            RETURN wd.id as id, wd.url as url, wd.domain as domain,
                   wd.title as title, wd.content_type as content_type,
                   wd.char_count as char_count, wd.fetched_at as fetched_at,
                   wd.provenance as provenance
            ORDER BY wd.fetched_at DESC
            LIMIT $limit
        """
        result = await session.run(query, limit=limit)
        return [dict(record) async for record in result]

async def get_web_storage_usage(self) -> Dict:
    """Get current web document storage usage."""
    async with self.driver.session() as session:
        result = await session.run("""
            MATCH (wd:WebDocument)
            WHERE wd.archived IS NULL OR wd.archived = false
            RETURN
                count(wd) as doc_count,
                sum(wd.char_count) as total_chars,
                sum(size(wd.content)) as total_bytes
        """)
        record = await result.single()

        total_bytes = record["total_bytes"] or 0
        limit_bytes = 2 * 1024 * 1024 * 1024  # 2GB

        return {
            "doc_count": record["doc_count"] or 0,
            "total_chars": record["total_chars"] or 0,
            "total_bytes": total_bytes,
            "limit_bytes": limit_bytes,
            "usage_percent": round((total_bytes / limit_bytes) * 100, 2) if limit_bytes else 0
        }

async def archive_oldest_web_documents(self, target_bytes: int) -> int:
    """Archive oldest web documents to get under target size."""
    usage = await self.get_web_storage_usage()

    if usage["total_bytes"] <= target_bytes:
        return 0

    excess = usage["total_bytes"] - target_bytes
    archived_count = 0

    async with self.driver.session() as session:
        # Get oldest documents
        result = await session.run("""
            MATCH (wd:WebDocument)
            WHERE wd.archived IS NULL OR wd.archived = false
            RETURN wd.id as id, size(wd.content) as bytes
            ORDER BY wd.fetched_at ASC
        """)

        bytes_freed = 0
        to_archive = []

        async for record in result:
            if bytes_freed >= excess:
                break
            to_archive.append(record["id"])
            bytes_freed += record["bytes"] or 0

        # Archive them (keep metadata, remove content)
        for doc_id in to_archive:
            await session.run("""
                MATCH (wd:WebDocument {id: $id})
                SET wd.archived = true,
                    wd.archived_at = datetime(),
                    wd.content = '[ARCHIVED]'
            """, id=doc_id)
            archived_count += 1

    return archived_count

async def get_recent_web_documents(self, limit: int = 10) -> List[Dict]:
    """Get recent web documents for reflection context."""
    async with self.driver.session() as session:
        result = await session.run("""
            MATCH (wd:WebDocument)
            WHERE (wd.archived IS NULL OR wd.archived = false)
            RETURN wd.id as id, wd.url as url, wd.domain as domain,
                   wd.title as title, wd.description as description,
                   substring(wd.content, 0, 500) as preview,
                   wd.fetched_at as fetched_at
            ORDER BY wd.fetched_at DESC
            LIMIT $limit
        """, limit=limit)
        return [dict(record) async for record in result]
```

---

### Step 1.3: Add Event Types

**File**: `/Users/kurultai/BYRD/event_bus.py`

Add to `EventType` enum:

```python
class EventType(Enum):
    # ... existing types ...

    # URL Ingestion
    URL_INGEST_STARTED = "url_ingest_started"
    URL_INGEST_COMPLETE = "url_ingest_complete"
    URL_INGEST_FAILED = "url_ingest_failed"
```

---

### Step 1.4: Add API Endpoints

**File**: `/Users/kurultai/BYRD/server.py`

Add request/response models and endpoints:

```python
# Request models (add near other BaseModel classes)

class IngestURLRequest(BaseModel):
    """Request to ingest a URL into BYRD's memory."""
    url: str
    context: Optional[str] = None  # Why this URL is being ingested
    force: bool = False  # Re-ingest even if exists

class IngestURLResponse(BaseModel):
    """Response after URL ingestion."""
    success: bool
    document_id: Optional[str] = None
    url: str
    title: Optional[str] = None
    char_count: int = 0
    chunks_created: int = 0
    processing_time_ms: int = 0
    error: Optional[str] = None
    already_exists: bool = False

class WebStorageResponse(BaseModel):
    """Web document storage usage."""
    doc_count: int
    total_chars: int
    total_bytes: int
    limit_bytes: int
    usage_percent: float


# Endpoints (add after document endpoints)

@app.post("/api/ingest/url", response_model=IngestURLResponse)
async def ingest_url(request: IngestURLRequest):
    """
    Ingest content from a URL into BYRD's memory.

    Fetches the URL, extracts content, and stores as a WebDocument node
    with chunking and embeddings for semantic search.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not hasattr(byrd_instance, 'url_ingestor') or not byrd_instance.url_ingestor:
        raise HTTPException(status_code=503, detail="URL ingestor not initialized")

    try:
        result = await byrd_instance.url_ingestor.ingest(
            url=request.url,
            context=request.context,
            provenance="api",
            force=request.force
        )

        return IngestURLResponse(
            success=result.success,
            document_id=result.document_id,
            url=result.url,
            title=result.title,
            char_count=result.char_count,
            chunks_created=result.chunks_created,
            processing_time_ms=result.processing_time_ms,
            error=result.error,
            already_exists=result.already_exists
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/web-documents")
async def list_web_documents(
    limit: int = 50,
    include_archived: bool = False
):
    """List ingested web documents."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        docs = await byrd_instance.memory.list_web_documents(
            limit=limit,
            include_archived=include_archived
        )
        return {"documents": docs, "count": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/web-documents/storage", response_model=WebStorageResponse)
async def get_web_storage():
    """Get web document storage usage."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        usage = await byrd_instance.memory.get_web_storage_usage()
        return WebStorageResponse(**usage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/web-documents/{doc_id}")
async def get_web_document(doc_id: str):
    """Get a specific web document by ID."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        async with byrd_instance.memory.driver.session() as session:
            result = await session.run("""
                MATCH (wd:WebDocument {id: $id})
                RETURN wd
            """, id=doc_id)
            record = await result.single()
            if record:
                return dict(record["wd"])
            raise HTTPException(status_code=404, detail="Document not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### Step 1.5: Initialize in BYRD

**File**: `/Users/kurultai/BYRD/byrd.py`

Add to `__init__` method:

```python
# URL Ingestor (after document_processor initialization)
from url_ingestor import URLIngestor
self.url_ingestor = URLIngestor(
    memory=self.memory,
    document_processor=self.document_processor if hasattr(self, 'document_processor') else None,
    config=config
)
print("🌐 URLIngestor: initialized")
```

---

### Step 1.6: Add Dependencies

**File**: `/Users/kurultai/BYRD/requirements.txt`

Add:

```
trafilatura>=1.6.0
youtube-transcript-api>=0.6.0
```

---

## Phase 2: Chat Integration

### Step 2.1: URL Detection in Messages

**File**: `/Users/kurultai/BYRD/server.py`

Modify the message handling endpoint to detect and auto-ingest URLs:

```python
@app.post("/api/messages", response_model=ExternalMessageResponse)
async def receive_message(request: ExternalMessageRequest):
    """Receive an external message and record it as an experience."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()

        # Record the message as an experience
        exp_id = await byrd_instance.memory.record_experience(
            content=f"[{request.source_type.upper()}] {request.content}",
            type="interaction"
        )

        # Detect and auto-ingest URLs in the message
        from url_ingestor import extract_urls
        urls = extract_urls(request.content)

        if urls and hasattr(byrd_instance, 'url_ingestor'):
            # Ingest URLs in background
            async def ingest_urls_background():
                for url in urls[:5]:  # Max 5 URLs per message
                    try:
                        await byrd_instance.url_ingestor.ingest(
                            url=url,
                            context=request.content[:200],
                            provenance="chat"
                        )
                    except Exception as e:
                        print(f"[Chat] URL ingest failed for {url}: {e}")

            asyncio.create_task(ingest_urls_background())

        return ExternalMessageResponse(
            success=True,
            experience_id=exp_id,
            message=f"Recorded message. {len(urls)} URLs detected for ingestion." if urls else "Recorded message."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Phase 3: Seeker Integration

### Step 3.1: Add url_ingest Strategy

**File**: `/Users/kurultai/BYRD/seeker.py`

Add to strategy hints (~line 822):

```python
strategy_hints = {
    # ... existing strategies ...
    "url_ingest": ["read this", "fetch", "ingest", "absorb", "read url", "read link"],
}
```

Add URL detection in `_determine_strategy_from_description`:

```python
async def _determine_strategy_from_description(self, description: str) -> str:
    """Determine the appropriate strategy for a desire."""

    # Check for URLs first
    from url_ingestor import extract_urls
    urls = extract_urls(description)
    if urls:
        return "url_ingest"

    # ... rest of existing logic ...
```

Add the strategy implementation:

```python
async def _execute_url_ingest(self, desire: Dict) -> bool:
    """Ingest URLs mentioned in a desire."""
    description = desire.get("description", "")
    desire_id = desire.get("id", "unknown")

    from url_ingestor import extract_urls
    urls = extract_urls(description)

    if not urls:
        print(f"[Seeker] No URLs found in desire: {description[:50]}")
        return False

    if not hasattr(self, 'url_ingestor') or not self.url_ingestor:
        # Get from byrd instance
        if hasattr(self, 'byrd') and hasattr(self.byrd, 'url_ingestor'):
            self.url_ingestor = self.byrd.url_ingestor
        else:
            print("[Seeker] URLIngestor not available")
            return False

    success_count = 0
    for url in urls:
        try:
            result = await self.url_ingestor.ingest(
                url=url,
                context=description,
                provenance=desire_id
            )
            if result.success:
                success_count += 1
                print(f"✅ Ingested: {result.title} ({result.char_count} chars)")
        except Exception as e:
            print(f"❌ Failed to ingest {url}: {e}")

    if success_count > 0:
        # Record experience about what was read
        await self.memory.record_experience(
            content=f"[URL_INGESTED] Read {success_count} URLs from desire: {description[:100]}",
            type="research"
        )

    return success_count > 0
```

### Step 3.2: Auto-ingest from Search Results (Only When Explicitly Requested)

Auto-ingestion of search results only happens when the user explicitly requests it
via keywords like "read", "ingest", "absorb", "fetch and read", etc.

```python
async def _execute_search_with_ingest(self, desire: Dict) -> bool:
    """
    Search and optionally ingest top results.

    Only auto-ingests if desire explicitly requests reading/ingesting content.
    Keywords: "read", "ingest", "absorb", "fetch", "read and summarize"
    """
    description = desire.get("description", "").lower()
    desire_id = desire.get("id", "unknown")

    # Check if explicit ingestion is requested
    ingest_keywords = [
        "read the", "read and", "ingest", "absorb", "fetch and read",
        "read top", "read results", "read articles", "read pages",
        "deep read", "full read", "read fully"
    ]
    should_ingest = any(kw in description for kw in ingest_keywords)

    # Perform search
    results = await self._search_duckduckgo(query_from_description)

    # Only ingest if explicitly requested
    if should_ingest and results:
        if hasattr(self, 'url_ingestor') or (hasattr(self, 'byrd') and hasattr(self.byrd, 'url_ingestor')):
            ingestor = getattr(self, 'url_ingestor', None) or self.byrd.url_ingestor

            ingested_count = 0
            for result in results[:3]:  # Top 3 only
                url = result.get('href') or result.get('url')
                if url:
                    try:
                        ingest_result = await ingestor.ingest(
                            url=url,
                            context=description,
                            provenance=desire_id
                        )
                        if ingest_result.success:
                            ingested_count += 1
                            print(f"📥 Auto-ingested: {ingest_result.title}")
                    except Exception as e:
                        print(f"[Seeker] Auto-ingest failed for {url}: {e}")

            if ingested_count > 0:
                await self.memory.record_experience(
                    content=f"[SEARCH_INGEST] Searched and read {ingested_count} articles about: {description[:100]}",
                    type="research"
                )

    return len(results) > 0
```

**Example desires that trigger auto-ingest:**
- "I want to research and **read** about transformer architectures"
- "**Read and absorb** the top articles on RLHF"
- "Search for AGI papers and **ingest** the results"

**Example desires that do NOT trigger auto-ingest (search only):**
- "I want to learn about transformer architectures"
- "Research RLHF techniques"
- "Find information about AGI"

---

## Phase 4: Dreamer Integration

### Step 4.1: Include WebDocuments in Context

**File**: `/Users/kurultai/BYRD/dreamer.py`

In `_build_reflection_context` or equivalent:

```python
async def _build_reflection_context(self) -> str:
    """Build context for reflection including web documents."""
    context_parts = []

    # ... existing context building ...

    # Add recent web documents
    try:
        web_docs = await self.memory.get_recent_web_documents(limit=5)
        if web_docs:
            context_parts.append("\n[RECENTLY READ WEB CONTENT]")
            for doc in web_docs:
                context_parts.append(
                    f"• {doc['title']} ({doc['domain']})\n"
                    f"  {doc.get('description') or doc.get('preview', '')[:200]}"
                )
    except Exception as e:
        print(f"[Dreamer] Could not load web documents: {e}")

    return '\n'.join(context_parts)
```

---

## Phase 5: Visualization

### Step 5.1: Add WebDocument Node Type

**File**: `/Users/kurultai/BYRD/byrd-3d-visualization.html`

Add to node type configuration:

```javascript
const NODE_TYPES = {
    // ... existing types ...
    WebDocument: {
        color: 0x06b6d4,      // Cyan
        emissive: 0x083344,
        size: 0.4,
        shape: 'globe',       // Distinct shape
        glow: true
    }
};
```

Add event handlers:

```javascript
// In event handling section
case 'url_ingest_complete':
    addNode({
        id: event.data.document_id,
        type: 'WebDocument',
        label: event.data.title || event.data.url,
        data: event.data
    });
    showNotification(`📥 Ingested: ${event.data.title}`);
    break;

case 'url_ingest_started':
    showNotification(`🌐 Reading: ${event.data.url}`, 'info');
    break;

case 'url_ingest_failed':
    showNotification(`❌ Failed: ${event.data.error}`, 'error');
    break;
```

---

## Testing Checklist

### Phase 1 Tests
- [ ] `curl -X POST http://localhost:8000/api/ingest/url -d '{"url":"https://example.com"}'`
- [ ] Verify WebDocument node created in Neo4j
- [ ] Test YouTube URL extraction
- [ ] Test GitHub file extraction
- [ ] Test PDF URL download and extraction
- [ ] Test storage limit enforcement

### Phase 2 Tests
- [ ] Send message with URL via `/api/messages`
- [ ] Verify URL auto-ingested in background
- [ ] Check experience created with URL count

### Phase 3 Tests
- [ ] Create desire with URL in description
- [ ] Verify Seeker routes to `url_ingest` strategy
- [ ] Test search WITHOUT "read" keyword → no auto-ingest
- [ ] Test search WITH "read and absorb" → top 3 auto-ingested

### Phase 4 Tests
- [ ] Trigger dream cycle
- [ ] Verify web documents appear in reflection context

### Phase 5 Tests
- [ ] Open 3D visualization
- [ ] Ingest a URL via API
- [ ] Verify WebDocument node appears with distinct color

---

## File Summary

| File | Action | Description |
|------|--------|-------------|
| `url_ingestor.py` | CREATE | Core URL fetching and extraction |
| `memory.py` | MODIFY | Add WebDocument storage methods |
| `event_bus.py` | MODIFY | Add URL_INGEST_* event types |
| `server.py` | MODIFY | Add `/api/ingest/url` and related endpoints |
| `byrd.py` | MODIFY | Initialize URLIngestor |
| `seeker.py` | MODIFY | Add url_ingest strategy, keyword-triggered search+ingest |
| `dreamer.py` | MODIFY | Include WebDocuments in reflection context |
| `byrd-3d-visualization.html` | MODIFY | Add WebDocument node visualization |
| `requirements.txt` | MODIFY | Add trafilatura, youtube-transcript-api |

---

## Estimated Implementation Time

| Phase | Complexity | Dependencies |
|-------|------------|--------------|
| Phase 1: Core | High | trafilatura, youtube-transcript-api |
| Phase 2: Chat | Low | Phase 1 |
| Phase 3: Seeker | Medium | Phase 1 |
| Phase 4: Dreamer | Low | Phase 1 |
| Phase 5: Visualization | Medium | Phase 1 |

**Total**: ~500-700 lines of new code across files.

---

## Ready to Implement?

This plan is ready for execution. Shall I proceed with Phase 1?
