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
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse
from enum import Enum

import httpx

from event_bus import event_bus, Event, EventType


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

    def __init__(self, memory, document_processor=None, config: Dict = None):
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
            elif '/shorts/' in url:
                video_id = url.split('/shorts/')[-1].split('?')[0]

            if not video_id:
                return ExtractedContent(
                    title="YouTube Video",
                    content="Could not extract video ID",
                    content_type=ContentType.YOUTUBE
                )

            # Get transcript (run in thread pool since it's sync)
            loop = asyncio.get_event_loop()
            transcript_list = await loop.run_in_executor(
                None,
                lambda: YouTubeTranscriptApi.get_transcript(video_id)
            )
            transcript_text = ' '.join([entry['text'] for entry in transcript_list])

            # Try to get video title via oEmbed
            title = "YouTube Video"
            author = None
            try:
                client = await self._get_client()
                oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
                response = await client.get(oembed_url)
                if response.status_code == 200:
                    data = response.json()
                    title = data.get('title', 'YouTube Video')
                    author = data.get('author_name')
            except:
                pass

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
                content="youtube-transcript-api not installed. Install with: pip install youtube-transcript-api",
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
        content = response.text

        # Extract filename for title
        path = urlparse(url).path
        filename = path.split('/')[-1] if '/' in path else path

        # If it's a blob URL, note the raw URL
        raw_url = url
        if 'github.com' in url and '/blob/' in url:
            raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')

        return ExtractedContent(
            title=filename,
            content=content,
            content_type=ContentType.GITHUB,
            metadata={"raw_url": raw_url, "original_url": url}
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
                content="PyMuPDF not installed - cannot extract PDF. Install with: pip install pymupdf",
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

        # Normalize URL
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        print(f"[URLIngestor] Ingesting: {url}")

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
                print(f"[URLIngestor] Already exists: {existing.get('title', url)}")
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

                # Handle YouTube separately (no need to fetch page for transcript)
                if 'youtube.com' in domain or 'youtu.be' in domain:
                    extracted = await self._extract_youtube(url)
                else:
                    # Fetch the URL
                    client = await self._get_client()
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
                        try:
                            formatted = json.dumps(response.json(), indent=2)
                        except:
                            formatted = response.text
                        extracted = ExtractedContent(
                            title=urlparse(url).path.split('/')[-1] or "JSON Data",
                            content=formatted,
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
                        "content_type": extracted.content_type.value,
                        "processing_time_ms": processing_time_ms
                    }
                ))

                print(f"[URLIngestor] Ingested: {extracted.title} ({len(extracted.content)} chars)")

                return IngestResult(
                    success=True,
                    url=url,
                    document_id=doc_id,
                    title=extracted.title,
                    char_count=len(extracted.content),
                    chunks_created=0,  # TODO: integrate with DocumentProcessor
                    processing_time_ms=processing_time_ms
                )

        except httpx.HTTPStatusError as e:
            self._failed_count += 1
            error_msg = f"HTTP {e.response.status_code}"
            await event_bus.emit(Event(
                type=EventType.URL_INGEST_FAILED,
                data={"url": url, "error": error_msg}
            ))
            print(f"[URLIngestor] Failed: {error_msg}")
            return IngestResult(
                success=False,
                url=url,
                error=error_msg
            )
        except httpx.RequestError as e:
            self._failed_count += 1
            error_msg = f"Request failed: {str(e)}"
            await event_bus.emit(Event(
                type=EventType.URL_INGEST_FAILED,
                data={"url": url, "error": error_msg}
            ))
            print(f"[URLIngestor] Failed: {error_msg}")
            return IngestResult(
                success=False,
                url=url,
                error=error_msg
            )
        except Exception as e:
            self._failed_count += 1
            error_msg = str(e)
            await event_bus.emit(Event(
                type=EventType.URL_INGEST_FAILED,
                data={"url": url, "error": error_msg}
            ))
            print(f"[URLIngestor] Failed: {error_msg}")
            return IngestResult(
                success=False,
                url=url,
                error=error_msg
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
        try:
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
        except Exception as e:
            print(f"[URLIngestor] Storage limit check failed: {e}")

    def get_stats(self) -> Dict:
        """Get ingestion statistics."""
        return {
            "total_ingested": self._total_ingested,
            "total_bytes": self._total_bytes,
            "failed_count": self._failed_count,
            "storage_limit_bytes": self.STORAGE_LIMIT_BYTES
        }

    def reset(self):
        """Reset statistics (for system reset)."""
        self._total_ingested = 0
        self._total_bytes = 0
        self._failed_count = 0
        self._domain_last_request.clear()


# URL detection regex for chat messages
URL_PATTERN = re.compile(
    r'https?://[^\s<>"\'{}|\\^`\[\]]+',
    re.IGNORECASE
)


def extract_urls(text: str) -> List[str]:
    """Extract all URLs from text."""
    urls = URL_PATTERN.findall(text)
    # Clean trailing punctuation
    cleaned = []
    for url in urls:
        # Remove trailing punctuation that's not part of URL
        while url and url[-1] in '.,;:!?)':
            url = url[:-1]
        if url:
            cleaned.append(url)
    return cleaned
