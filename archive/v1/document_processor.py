"""
Document Processor - File ingestion and processing for BYRD.

Handles file upload, text extraction, chunking, embedding generation,
and storage in Neo4j for future retrieval and reflection.
"""

import asyncio
import hashlib
import uuid
import re
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
import json

from event_bus import event_bus, Event, EventType


class ProcessingStage(Enum):
    """Stages of document processing."""
    VALIDATING = "validating"
    EXTRACTING = "extracting"
    ANALYZING = "analyzing"
    CHUNKING = "chunking"
    EMBEDDING = "embedding"
    STORING = "storing"
    ENRICHING = "enriching"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class QuickIngestResult:
    """Result of quick ingest phase."""
    document_id: str
    status: str  # "processing" | "duplicate" | "error"
    message: str
    estimated_time_seconds: int = 15
    existing_document: Optional[Dict] = None


@dataclass
class ProcessingProgress:
    """Current processing progress."""
    document_id: str
    status: str
    stage: ProcessingStage
    progress_percent: int
    stages_completed: List[str]
    current_stage: str
    stages_remaining: List[str]
    estimated_seconds_remaining: int


@dataclass
class ChunkInfo:
    """Information about a document chunk."""
    index: int
    heading: Optional[str]
    content: str
    char_start: int
    char_end: int
    overlap_prev: int = 0
    overlap_next: int = 0


@dataclass
class DocumentAnalysis:
    """LLM analysis of document content."""
    summary: str
    detected_type: str  # code | documentation | data | academic_paper | notes | conversation
    detected_language: Optional[str]  # For code files
    importance: float  # 0-1
    key_topics: List[str]


@dataclass
class SearchResult:
    """Unified search result shape."""
    type: str  # "chunk" | "document"
    document_id: str
    chunk_id: Optional[str]
    filename: str
    heading: Optional[str]
    content_preview: str
    score: float
    match_type: str  # "semantic" | "keyword" | "hybrid"


@dataclass
class DeleteResult:
    """Result of cascade delete."""
    document_id: str
    chunks_deleted: int
    beliefs_deleted: int
    entities_deleted: int
    experiences_deleted: int


class DocumentProcessor:
    """
    Handles document ingestion, processing, and storage.

    Two-phase processing:
    1. Quick Ingest: Validate, hash, create pending document, return immediately
    2. Background Processing: Extract, analyze, chunk, embed, store, enrich
    """

    # Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    INLINE_THRESHOLD = 5000  # Files smaller than 5KB stored inline
    CHUNK_TARGET_SIZE = 1000  # Target characters per chunk
    CHUNK_OVERLAP = 50  # Character overlap between chunks
    EMBEDDING_BATCH_SIZE = 32  # Embeddings generated in batches

    SUPPORTED_TYPES = {
        'text/plain': 'text',
        'text/markdown': 'markdown',
        'application/pdf': 'pdf',
        'application/json': 'json',
        'text/x-python': 'python',
        'text/javascript': 'javascript',
        'text/typescript': 'typescript',
        'text/yaml': 'yaml',
        'application/x-yaml': 'yaml',
    }

    SUPPORTED_EXTENSIONS = {
        '.txt': 'text',
        '.md': 'markdown',
        '.pdf': 'pdf',
        '.json': 'json',
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.html': 'html',
        '.css': 'css',
        '.sql': 'sql',
        '.sh': 'shell',
        '.bash': 'shell',
        '.go': 'go',
        '.rs': 'rust',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.hpp': 'cpp',
    }

    STAGE_ORDER = [
        ProcessingStage.VALIDATING,
        ProcessingStage.EXTRACTING,
        ProcessingStage.ANALYZING,
        ProcessingStage.CHUNKING,
        ProcessingStage.EMBEDDING,
        ProcessingStage.STORING,
        ProcessingStage.ENRICHING,
        ProcessingStage.COMPLETE,
    ]

    def __init__(self, memory, llm_client, config: Dict = None):
        """
        Initialize document processor.

        Args:
            memory: Memory instance for Neo4j operations
            llm_client: LLM client for analysis
            config: Optional configuration overrides
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Apply config overrides
        if 'documents' in self.config:
            doc_config = self.config['documents']
            if 'max_file_size_mb' in doc_config:
                self.MAX_FILE_SIZE = doc_config['max_file_size_mb'] * 1024 * 1024
            if 'inline_threshold_bytes' in doc_config:
                self.INLINE_THRESHOLD = doc_config['inline_threshold_bytes']
            if 'chunk_target_size' in doc_config:
                self.CHUNK_TARGET_SIZE = doc_config['chunk_target_size']
            if 'chunk_overlap' in doc_config:
                self.CHUNK_OVERLAP = doc_config['chunk_overlap']
            if 'embedding_batch_size' in doc_config:
                self.EMBEDDING_BATCH_SIZE = doc_config['embedding_batch_size']

        # Processing state
        self._processing_tasks: Dict[str, asyncio.Task] = {}
        self._progress_state: Dict[str, ProcessingProgress] = {}

        # Embedding model (lazy loaded)
        self._embedding_model = None

        # Schema initialized flag
        self._schema_initialized = False

    async def ensure_schema(self) -> None:
        """
        Ensure Neo4j schema (constraints and indexes) for document nodes exists.

        Creates:
        - Uniqueness constraints for Document.id, Document.content_hash
        - Uniqueness constraints for DocumentChunk.id, DocumentCollection.id
        - Performance indexes for processing_status, reflected_on, uploaded_at
        - Vector index for chunk embeddings (384 dimensions, cosine similarity)
        """
        if self._schema_initialized:
            return

        if not self.memory or not hasattr(self.memory, 'driver'):
            print("[DocumentProcessor] Memory not available, skipping schema init")
            return

        schema_queries = [
            # Uniqueness constraints
            "CREATE CONSTRAINT doc_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT doc_hash IF NOT EXISTS FOR (d:Document) REQUIRE d.content_hash IS UNIQUE",
            "CREATE CONSTRAINT chunk_id IF NOT EXISTS FOR (c:DocumentChunk) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT coll_id IF NOT EXISTS FOR (dc:DocumentCollection) REQUIRE dc.id IS UNIQUE",

            # Performance indexes
            "CREATE INDEX doc_status IF NOT EXISTS FOR (d:Document) ON (d.processing_status)",
            "CREATE INDEX doc_reflected IF NOT EXISTS FOR (d:Document) ON (d.reflected_on)",
            "CREATE INDEX doc_uploaded IF NOT EXISTS FOR (d:Document) ON (d.uploaded_at)",
            "CREATE INDEX chunk_doc IF NOT EXISTS FOR (c:DocumentChunk) ON (c.document_id)",
        ]

        # Vector index requires separate handling (Neo4j 5.11+)
        vector_index_query = """
        CREATE VECTOR INDEX chunk_embeddings IF NOT EXISTS
        FOR (c:DocumentChunk)
        ON c.embedding
        OPTIONS {indexConfig: {
          `vector.dimensions`: 384,
          `vector.similarity_function`: 'cosine'
        }}
        """

        try:
            async with self.memory.driver.session() as session:
                # Create constraints and indexes
                for query in schema_queries:
                    try:
                        await session.run(query)
                    except Exception as e:
                        # Ignore "already exists" errors
                        if "already exists" not in str(e).lower():
                            print(f"[DocumentProcessor] Schema query failed: {e}")

                # Try to create vector index (may fail on older Neo4j versions)
                try:
                    await session.run(vector_index_query)
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        print(f"[DocumentProcessor] Vector index not created (requires Neo4j 5.11+): {e}")

            self._schema_initialized = True
            print("[DocumentProcessor] Schema initialization complete")
        except Exception as e:
            print(f"[DocumentProcessor] Schema initialization failed: {e}")

    def _get_embedding_model(self):
        """Lazy load the embedding model."""
        if self._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            except ImportError:
                print("[DocumentProcessor] sentence-transformers not available, embeddings disabled")
                return None
        return self._embedding_model

    def _compute_hash(self, content: bytes) -> str:
        """Compute SHA-256 hash of content."""
        return f"sha256:{hashlib.sha256(content).hexdigest()}"

    def _detect_file_type(self, filename: str, mime_type: str = None) -> str:
        """Detect file type from filename and mime type."""
        # Try extension first
        ext = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
        if ext in self.SUPPORTED_EXTENSIONS:
            return self.SUPPORTED_EXTENSIONS[ext]

        # Try mime type
        if mime_type and mime_type in self.SUPPORTED_TYPES:
            return self.SUPPORTED_TYPES[mime_type]

        # Default to text
        return 'text'

    def _validate_file(self, content: bytes, filename: str, mime_type: str = None) -> Tuple[bool, str]:
        """
        Validate file for processing.

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check size
        if len(content) > self.MAX_FILE_SIZE:
            return False, f"File exceeds maximum size of {self.MAX_FILE_SIZE // (1024*1024)}MB"

        # Check if empty
        if len(content) == 0:
            return False, "File is empty"

        # Check file type
        file_type = self._detect_file_type(filename, mime_type)
        if file_type == 'text' and not filename.endswith('.txt'):
            # Unknown extension, try to detect if it's text
            try:
                content.decode('utf-8')
            except UnicodeDecodeError:
                return False, "Unsupported file type (not valid UTF-8 text)"

        return True, ""

    async def _check_duplicate(self, content_hash: str) -> Optional[Dict]:
        """Check if document with same hash already exists."""
        query = """
        MATCH (d:Document {content_hash: $hash})
        RETURN d.id as id, d.filename as filename, d.uploaded_at as uploaded_at,
               d.processing_status as status, d.summary as summary
        """
        async with self.memory.driver.session() as session:
            result = await session.run(query, hash=content_hash)
            record = await result.single()
            if record:
                return dict(record)
        return None

    async def quick_ingest(
        self,
        content: bytes,
        filename: str,
        mime_type: str = None,
        user_tags: List[str] = None,
        user_purpose: str = None,
        user_notes: str = None,
        collection_id: str = None
    ) -> QuickIngestResult:
        """
        Phase 1: Quick ingest - validate, hash, create pending document.

        Returns immediately after creating the document node.
        Background processing is queued automatically.
        """
        # Ensure schema exists on first use
        await self.ensure_schema()

        # Validate
        is_valid, error_msg = self._validate_file(content, filename, mime_type)
        if not is_valid:
            return QuickIngestResult(
                document_id="",
                status="error",
                message=error_msg
            )

        # Compute hash
        content_hash = self._compute_hash(content)

        # Check for duplicate
        existing = await self._check_duplicate(content_hash)
        if existing:
            return QuickIngestResult(
                document_id=existing['id'],
                status="duplicate",
                message="Document already exists",
                existing_document=existing
            )

        # Create document ID
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        file_type = self._detect_file_type(filename, mime_type)

        # Determine storage mode
        storage_mode = "inline" if len(content) < self.INLINE_THRESHOLD else "chunked"

        # Decode content for text files
        try:
            text_content = content.decode('utf-8')
        except UnicodeDecodeError:
            # For binary files (PDF), we'll extract text later
            text_content = None

        # Create pending document node
        query = """
        CREATE (d:Document {
            id: $doc_id,
            filename: $filename,
            file_type: $file_type,
            mime_type: $mime_type,
            size_bytes: $size_bytes,
            content_hash: $content_hash,
            uploaded_at: datetime(),
            user_tags: $user_tags,
            user_purpose: $user_purpose,
            user_notes: $user_notes,
            storage_mode: $storage_mode,
            content: $content,
            processing_status: 'pending',
            processing_stage: 'validating',
            graphiti_processed: false,
            reflected_on: false,
            reflection_depth: 0
        })
        RETURN d.id as id
        """

        async with self.memory.driver.session() as session:
            await session.run(
                query,
                doc_id=doc_id,
                filename=filename,
                file_type=file_type,
                mime_type=mime_type or "",
                size_bytes=len(content),
                content_hash=content_hash,
                user_tags=user_tags or [],
                user_purpose=user_purpose or "",
                user_notes=user_notes or "",
                storage_mode=storage_mode,
                content=text_content if storage_mode == "inline" else None
            )

        # Add to collection if specified
        if collection_id:
            await self._add_to_collection(doc_id, collection_id)

        # Emit upload event
        await event_bus.emit(Event(
            type=EventType.DOCUMENT_UPLOADED,
            data={
                "document_id": doc_id,
                "filename": filename,
                "size_bytes": len(content)
            }
        ))

        # Queue background processing
        task = asyncio.create_task(
            self._process_in_background(doc_id, content, filename, file_type)
        )
        self._processing_tasks[doc_id] = task

        # Estimate processing time based on size
        estimated_seconds = max(5, len(content) // 50000)  # ~50KB/second

        return QuickIngestResult(
            document_id=doc_id,
            status="processing",
            message="Document queued for processing",
            estimated_time_seconds=estimated_seconds
        )

    async def _process_in_background(
        self,
        doc_id: str,
        content: bytes,
        filename: str,
        file_type: str
    ):
        """
        Phase 2: Background processing - extract, analyze, chunk, embed, store.
        """
        try:
            # Initialize progress tracking
            self._progress_state[doc_id] = ProcessingProgress(
                document_id=doc_id,
                status="processing",
                stage=ProcessingStage.VALIDATING,
                progress_percent=0,
                stages_completed=[],
                current_stage="validating",
                stages_remaining=[s.value for s in self.STAGE_ORDER[1:]],
                estimated_seconds_remaining=30
            )

            await self._update_stage(doc_id, ProcessingStage.EXTRACTING)

            # Extract text content
            text_content = await self._extract_text(content, file_type)
            if not text_content:
                raise ValueError("Failed to extract text content")

            await self._update_stage(doc_id, ProcessingStage.ANALYZING)

            # Analyze with LLM
            analysis = await self._analyze_document(text_content, filename, file_type)

            # Update document with analysis
            await self._update_document_analysis(doc_id, analysis)

            await self._update_stage(doc_id, ProcessingStage.CHUNKING)

            # Check if we need chunking
            if len(text_content) >= self.INLINE_THRESHOLD:
                # Create chunks
                chunks = self._create_chunks(text_content, file_type)

                await self._update_stage(doc_id, ProcessingStage.EMBEDDING)

                # Generate embeddings
                embeddings = await self._generate_embeddings([c.content for c in chunks])

                await self._update_stage(doc_id, ProcessingStage.STORING)

                # Store chunks with embeddings
                await self._store_chunks(doc_id, chunks, embeddings)

                # Update document chunk count
                await self._update_document_chunk_count(doc_id, len(chunks))
            else:
                await self._update_stage(doc_id, ProcessingStage.STORING)

            await self._update_stage(doc_id, ProcessingStage.ENRICHING)

            # Graphiti entity extraction (if available)
            await self._run_graphiti_extraction(doc_id, text_content)

            # Mark as complete
            await self._update_stage(doc_id, ProcessingStage.COMPLETE)
            await self._mark_processing_complete(doc_id)

            # Record experience
            await self.memory.record_experience(
                content=f"[DOCUMENT_INGESTED] {filename} processed successfully | "
                        f"type={analysis.detected_type} importance={analysis.importance:.2f}",
                type="document_ingestion"
            )

            # Emit completion event
            await event_bus.emit(Event(
                type=EventType.DOCUMENT_PROCESSED,
                data={
                    "document_id": doc_id,
                    "filename": filename,
                    "detected_type": analysis.detected_type,
                    "importance": analysis.importance
                }
            ))

        except Exception as e:
            await self._mark_processing_error(doc_id, str(e))
            await event_bus.emit(Event(
                type=EventType.DOCUMENT_ERROR,
                data={
                    "document_id": doc_id,
                    "error": str(e)
                }
            ))
        finally:
            # Clean up
            if doc_id in self._processing_tasks:
                del self._processing_tasks[doc_id]

    async def _extract_text(self, content: bytes, file_type: str) -> str:
        """Extract text from file content."""
        if file_type == 'pdf':
            return await self._extract_pdf_text(content)
        else:
            # Text-based files
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                return content.decode('latin-1')

    async def _extract_pdf_text(self, content: bytes) -> str:
        """Extract text from PDF."""
        try:
            from io import BytesIO
            import PyPDF2

            pdf_file = BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text_parts = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            return '\n\n'.join(text_parts)
        except ImportError:
            # PyPDF2 not available, return empty
            return ""
        except Exception as e:
            print(f"[DocumentProcessor] PDF extraction error: {e}")
            return ""

    async def _analyze_document(
        self,
        text_content: str,
        filename: str,
        file_type: str
    ) -> DocumentAnalysis:
        """Analyze document with LLM."""
        # Truncate for analysis if too long
        analysis_text = text_content[:8000] if len(text_content) > 8000 else text_content

        prompt = f"""Analyze this document and provide a JSON response.

Filename: {filename}
File type: {file_type}

Content:
{analysis_text}

Respond with JSON only:
{{
    "summary": "2-3 sentence summary of the document",
    "detected_type": "code|documentation|data|academic_paper|notes|conversation|config|other",
    "detected_language": "python|javascript|etc or null if not code",
    "importance": 0.0-1.0 (how important/valuable is this content),
    "key_topics": ["topic1", "topic2", "topic3"]
}}"""

        try:
            response = await self.llm_client.query(prompt, max_tokens=500)

            # Parse JSON response
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            data = json.loads(text.strip())

            return DocumentAnalysis(
                summary=data.get("summary", "No summary available"),
                detected_type=data.get("detected_type", "other"),
                detected_language=data.get("detected_language"),
                importance=float(data.get("importance", 0.5)),
                key_topics=data.get("key_topics", [])
            )
        except Exception as e:
            print(f"[DocumentProcessor] Analysis error: {e}")
            # Return default analysis
            return DocumentAnalysis(
                summary=f"Document: {filename}",
                detected_type="other",
                detected_language=file_type if file_type in ['python', 'javascript', 'typescript'] else None,
                importance=0.5,
                key_topics=[]
            )

    def _create_chunks(self, text: str, file_type: str) -> List[ChunkInfo]:
        """Create chunks based on file type."""
        if file_type == 'markdown':
            return self._chunk_by_headers(text)
        elif file_type in ['python', 'javascript', 'typescript', 'go', 'rust', 'java']:
            return self._chunk_by_code_blocks(text, file_type)
        else:
            return self._chunk_by_size(text)

    def _chunk_by_headers(self, text: str) -> List[ChunkInfo]:
        """Chunk markdown by headers."""
        chunks = []
        # Split by ## or ### headers
        pattern = r'(^#{1,3}\s+.+$)'
        parts = re.split(pattern, text, flags=re.MULTILINE)

        current_heading = None
        current_content = []
        char_pos = 0

        for part in parts:
            if re.match(r'^#{1,3}\s+', part):
                # Save previous chunk
                if current_content:
                    content = '\n'.join(current_content).strip()
                    if content:
                        chunks.append(ChunkInfo(
                            index=len(chunks),
                            heading=current_heading,
                            content=content,
                            char_start=char_pos - len(content),
                            char_end=char_pos
                        ))
                current_heading = part.strip().lstrip('#').strip()
                current_content = []
            else:
                current_content.append(part)
            char_pos += len(part)

        # Don't forget last chunk
        if current_content:
            content = '\n'.join(current_content).strip()
            if content:
                chunks.append(ChunkInfo(
                    index=len(chunks),
                    heading=current_heading,
                    content=content,
                    char_start=char_pos - len(content),
                    char_end=char_pos
                ))

        # If no headers found, fall back to size-based chunking
        if not chunks:
            return self._chunk_by_size(text)

        return chunks

    def _chunk_by_code_blocks(self, text: str, file_type: str) -> List[ChunkInfo]:
        """Chunk code by functions/classes."""
        chunks = []

        # Patterns for different languages
        if file_type == 'python':
            pattern = r'(^(?:async\s+)?(?:def|class)\s+\w+)'
        elif file_type in ['javascript', 'typescript']:
            pattern = r'(^(?:export\s+)?(?:async\s+)?(?:function|class|const|let|var)\s+\w+)'
        else:
            # Generic: split by empty lines
            pattern = r'\n\n+'

        parts = re.split(pattern, text, flags=re.MULTILINE)

        current_heading = None
        current_content = []
        char_pos = 0

        for i, part in enumerate(parts):
            if re.match(r'^(?:async\s+)?(?:def|class|function|export|const|let|var)\s+', part.strip()):
                # Save previous chunk
                if current_content:
                    content = '\n'.join(current_content).strip()
                    if content and len(content) > 50:  # Skip tiny chunks
                        chunks.append(ChunkInfo(
                            index=len(chunks),
                            heading=current_heading,
                            content=content,
                            char_start=char_pos - len(content),
                            char_end=char_pos
                        ))
                # Extract function/class name
                match = re.search(r'(?:def|class|function)\s+(\w+)', part)
                current_heading = match.group(1) if match else None
                current_content = [part]
            else:
                current_content.append(part)
            char_pos += len(part)

        # Don't forget last chunk
        if current_content:
            content = '\n'.join(current_content).strip()
            if content and len(content) > 50:
                chunks.append(ChunkInfo(
                    index=len(chunks),
                    heading=current_heading,
                    content=content,
                    char_start=char_pos - len(content),
                    char_end=char_pos
                ))

        # If no structure found, fall back to size-based chunking
        if not chunks:
            return self._chunk_by_size(text)

        return chunks

    def _chunk_by_size(self, text: str) -> List[ChunkInfo]:
        """Chunk by target size with overlap."""
        chunks = []

        # Split by paragraphs first
        paragraphs = re.split(r'\n\n+', text)

        current_chunk = []
        current_size = 0
        char_pos = 0

        for para in paragraphs:
            para_size = len(para)

            if current_size + para_size > self.CHUNK_TARGET_SIZE and current_chunk:
                # Save current chunk
                content = '\n\n'.join(current_chunk)
                chunks.append(ChunkInfo(
                    index=len(chunks),
                    heading=None,
                    content=content,
                    char_start=char_pos - len(content),
                    char_end=char_pos,
                    overlap_prev=self.CHUNK_OVERLAP if len(chunks) > 0 else 0,
                    overlap_next=self.CHUNK_OVERLAP
                ))

                # Start new chunk with overlap
                if current_chunk:
                    last_para = current_chunk[-1]
                    current_chunk = [last_para[-self.CHUNK_OVERLAP:]] if len(last_para) > self.CHUNK_OVERLAP else [last_para]
                    current_size = len(current_chunk[0])
                else:
                    current_chunk = []
                    current_size = 0

            current_chunk.append(para)
            current_size += para_size
            char_pos += para_size + 2  # +2 for paragraph break

        # Don't forget last chunk
        if current_chunk:
            content = '\n\n'.join(current_chunk)
            chunks.append(ChunkInfo(
                index=len(chunks),
                heading=None,
                content=content,
                char_start=char_pos - len(content),
                char_end=char_pos,
                overlap_prev=self.CHUNK_OVERLAP if len(chunks) > 0 else 0,
                overlap_next=0
            ))

        return chunks

    async def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings in batches."""
        model = self._get_embedding_model()
        if model is None:
            return [[] for _ in texts]

        embeddings = []

        # Process in batches
        for i in range(0, len(texts), self.EMBEDDING_BATCH_SIZE):
            batch = texts[i:i + self.EMBEDDING_BATCH_SIZE]
            # Run in thread pool to avoid blocking
            batch_embeddings = await asyncio.to_thread(
                model.encode,
                batch,
                convert_to_numpy=True
            )
            embeddings.extend(batch_embeddings.tolist())

        return embeddings

    async def _store_chunks(
        self,
        doc_id: str,
        chunks: List[ChunkInfo],
        embeddings: List[List[float]]
    ):
        """Store chunks with embeddings in Neo4j."""
        query = """
        MATCH (d:Document {id: $doc_id})
        CREATE (c:DocumentChunk {
            id: $chunk_id,
            document_id: $doc_id,
            chunk_index: $index,
            heading: $heading,
            content: $content,
            char_start: $char_start,
            char_end: $char_end,
            overlap_prev: $overlap_prev,
            overlap_next: $overlap_next,
            embedding: $embedding
        })
        CREATE (d)-[:HAS_CHUNK]->(c)
        """

        async with self.memory.driver.session() as session:
            for chunk, embedding in zip(chunks, embeddings):
                chunk_id = f"chunk_{uuid.uuid4().hex[:12]}"
                await session.run(
                    query,
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    index=chunk.index,
                    heading=chunk.heading,
                    content=chunk.content,
                    char_start=chunk.char_start,
                    char_end=chunk.char_end,
                    overlap_prev=chunk.overlap_prev,
                    overlap_next=chunk.overlap_next,
                    embedding=embedding
                )

    async def _update_document_analysis(self, doc_id: str, analysis: DocumentAnalysis):
        """Update document with analysis results."""
        query = """
        MATCH (d:Document {id: $doc_id})
        SET d.summary = $summary,
            d.detected_type = $detected_type,
            d.detected_language = $detected_language,
            d.importance = $importance,
            d.key_topics = $key_topics
        """
        async with self.memory.driver.session() as session:
            await session.run(
                query,
                doc_id=doc_id,
                summary=analysis.summary,
                detected_type=analysis.detected_type,
                detected_language=analysis.detected_language,
                importance=analysis.importance,
                key_topics=analysis.key_topics
            )

    async def _update_document_chunk_count(self, doc_id: str, count: int):
        """Update document chunk count."""
        query = """
        MATCH (d:Document {id: $doc_id})
        SET d.chunk_count = $count
        """
        async with self.memory.driver.session() as session:
            await session.run(query, doc_id=doc_id, count=count)

    async def _update_stage(self, doc_id: str, stage: ProcessingStage):
        """Update processing stage and emit event."""
        # Update document
        query = """
        MATCH (d:Document {id: $doc_id})
        SET d.processing_stage = $stage,
            d.processing_status = 'processing'
        """
        async with self.memory.driver.session() as session:
            await session.run(query, doc_id=doc_id, stage=stage.value)

        # Update progress state
        if doc_id in self._progress_state:
            progress = self._progress_state[doc_id]
            stage_idx = self.STAGE_ORDER.index(stage)
            progress.stage = stage
            progress.current_stage = stage.value
            progress.stages_completed = [s.value for s in self.STAGE_ORDER[:stage_idx]]
            progress.stages_remaining = [s.value for s in self.STAGE_ORDER[stage_idx + 1:]]
            progress.progress_percent = int((stage_idx / len(self.STAGE_ORDER)) * 100)

        # Emit event
        await event_bus.emit(Event(
            type=EventType.DOCUMENT_PROCESSING,
            data={
                "document_id": doc_id,
                "stage": stage.value,
                "progress_percent": self._progress_state.get(doc_id, {}).progress_percent if doc_id in self._progress_state else 0
            }
        ))

    async def _mark_processing_complete(self, doc_id: str):
        """Mark document processing as complete."""
        query = """
        MATCH (d:Document {id: $doc_id})
        SET d.processing_status = 'complete',
            d.processing_stage = 'complete',
            d.processing_completed_at = datetime()
        """
        async with self.memory.driver.session() as session:
            await session.run(query, doc_id=doc_id)

        if doc_id in self._progress_state:
            del self._progress_state[doc_id]

    async def _mark_processing_error(self, doc_id: str, error: str):
        """Mark document processing as failed."""
        query = """
        MATCH (d:Document {id: $doc_id})
        SET d.processing_status = 'error',
            d.processing_stage = 'error',
            d.processing_error = $error
        """
        async with self.memory.driver.session() as session:
            await session.run(query, doc_id=doc_id, error=error)

        if doc_id in self._progress_state:
            del self._progress_state[doc_id]

    async def _run_graphiti_extraction(self, doc_id: str, text_content: str):
        """Run Graphiti entity extraction if available."""
        try:
            # Check if Graphiti is available
            from graphiti_layer import get_graphiti_layer
            graphiti = get_graphiti_layer()
            if graphiti:
                await graphiti.extract_entities_from_text(
                    text_content[:10000],  # Limit for extraction
                    source_id=doc_id,
                    source_type="document"
                )

                # Mark as processed
                query = """
                MATCH (d:Document {id: $doc_id})
                SET d.graphiti_processed = true
                """
                async with self.memory.driver.session() as session:
                    await session.run(query, doc_id=doc_id)
        except ImportError:
            pass
        except Exception as e:
            print(f"[DocumentProcessor] Graphiti extraction error: {e}")

    async def _add_to_collection(self, doc_id: str, collection_id: str):
        """Add document to a collection."""
        query = """
        MATCH (d:Document {id: $doc_id})
        MATCH (c:DocumentCollection {id: $collection_id})
        CREATE (c)-[:CONTAINS]->(d)
        WITH c
        SET c.document_count = c.document_count + 1
        """
        async with self.memory.driver.session() as session:
            await session.run(query, doc_id=doc_id, collection_id=collection_id)

    # ==================== Public Query Methods ====================

    async def get_document(self, doc_id: str) -> Optional[Dict]:
        """Get document by ID."""
        query = """
        MATCH (d:Document {id: $doc_id})
        OPTIONAL MATCH (b:Belief)-[:DERIVED_FROM]->(:DocumentChunk)-[:HAS_CHUNK]-(d)
        RETURN d, count(DISTINCT b) as belief_count
        """
        async with self.memory.driver.session() as session:
            result = await session.run(query, doc_id=doc_id)
            record = await result.single()
            if record:
                doc = dict(record['d'])
                doc['belief_count'] = record['belief_count']
                return doc
        return None

    async def get_document_content(self, doc_id: str) -> Optional[Dict]:
        """Get document content (inline or chunks)."""
        doc = await self.get_document(doc_id)
        if not doc:
            return None

        if doc.get('storage_mode') == 'inline':
            return {
                "document_id": doc_id,
                "storage_mode": "inline",
                "content": doc.get('content', '')
            }
        else:
            # Get chunks
            query = """
            MATCH (d:Document {id: $doc_id})-[:HAS_CHUNK]->(c:DocumentChunk)
            RETURN c.chunk_index as index, c.heading as heading, c.content as content
            ORDER BY c.chunk_index
            """
            async with self.memory.driver.session() as session:
                result = await session.run(query, doc_id=doc_id)
                chunks = [dict(record) async for record in result]

            return {
                "document_id": doc_id,
                "storage_mode": "chunked",
                "chunks": chunks
            }

    async def get_processing_progress(self, doc_id: str) -> Optional[ProcessingProgress]:
        """Get current processing progress."""
        if doc_id in self._progress_state:
            return self._progress_state[doc_id]

        # Check if already complete
        doc = await self.get_document(doc_id)
        if doc:
            status = doc.get('processing_status', 'unknown')
            stage = doc.get('processing_stage', 'unknown')

            if status == 'complete':
                return ProcessingProgress(
                    document_id=doc_id,
                    status="complete",
                    stage=ProcessingStage.COMPLETE,
                    progress_percent=100,
                    stages_completed=[s.value for s in self.STAGE_ORDER],
                    current_stage="complete",
                    stages_remaining=[],
                    estimated_seconds_remaining=0
                )
            elif status == 'error':
                return ProcessingProgress(
                    document_id=doc_id,
                    status="error",
                    stage=ProcessingStage.ERROR,
                    progress_percent=0,
                    stages_completed=[],
                    current_stage="error",
                    stages_remaining=[],
                    estimated_seconds_remaining=0
                )

        return None

    async def list_documents(
        self,
        offset: int = 0,
        limit: int = 20,
        purpose: str = None,
        status: str = None,
        collection_id: str = None
    ) -> Dict:
        """List documents with pagination."""
        where_clauses = []
        params = {"offset": offset, "limit": limit}

        if purpose:
            where_clauses.append("d.user_purpose = $purpose")
            params["purpose"] = purpose

        if status:
            where_clauses.append("d.processing_status = $status")
            params["status"] = status

        if collection_id:
            where_clauses.append("EXISTS { MATCH (c:DocumentCollection {id: $collection_id})-[:CONTAINS]->(d) }")
            params["collection_id"] = collection_id

        where_clause = " AND ".join(where_clauses) if where_clauses else "true"

        # Get total count
        count_query = f"""
        MATCH (d:Document)
        WHERE {where_clause}
        RETURN count(d) as total
        """

        # Get documents
        list_query = f"""
        MATCH (d:Document)
        WHERE {where_clause}
        RETURN d
        ORDER BY d.uploaded_at DESC
        SKIP $offset
        LIMIT $limit
        """

        async with self.memory.driver.session() as session:
            count_result = await session.run(count_query, **params)
            count_record = await count_result.single()
            total = count_record['total'] if count_record else 0

            list_result = await session.run(list_query, **params)
            documents = [dict(record['d']) async for record in list_result]

        return {
            "documents": documents,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": offset + len(documents) < total
        }

    async def search_documents(
        self,
        query: str,
        mode: str = "hybrid",  # semantic | keyword | hybrid
        limit: int = 10,
        offset: int = 0
    ) -> Dict:
        """Search documents and chunks."""
        results = []

        # Keyword search
        if mode in ["keyword", "hybrid"]:
            keyword_query = """
            MATCH (d:Document)
            WHERE d.summary CONTAINS $query OR d.filename CONTAINS $query
            RETURN 'document' as type, d.id as document_id, null as chunk_id,
                   d.filename as filename, null as heading,
                   d.summary as content_preview, 0.7 as score, 'keyword' as match_type
            UNION
            MATCH (c:DocumentChunk)
            WHERE c.content CONTAINS $query OR c.heading CONTAINS $query
            MATCH (d:Document {id: c.document_id})
            RETURN 'chunk' as type, d.id as document_id, c.id as chunk_id,
                   d.filename as filename, c.heading as heading,
                   substring(c.content, 0, 200) as content_preview,
                   0.6 as score, 'keyword' as match_type
            """
            async with self.memory.driver.session() as session:
                result = await session.run(keyword_query, query=query)
                keyword_results = [dict(record) async for record in result]
                results.extend(keyword_results)

        # Semantic search
        if mode in ["semantic", "hybrid"]:
            model = self._get_embedding_model()
            if model:
                query_embedding = await asyncio.to_thread(
                    model.encode,
                    [query],
                    convert_to_numpy=True
                )
                query_embedding = query_embedding[0].tolist()

                # Vector search using Neo4j
                vector_query = """
                CALL db.index.vector.queryNodes('chunk_embeddings', $limit, $embedding)
                YIELD node, score
                MATCH (d:Document {id: node.document_id})
                RETURN 'chunk' as type, d.id as document_id, node.id as chunk_id,
                       d.filename as filename, node.heading as heading,
                       substring(node.content, 0, 200) as content_preview,
                       score, 'semantic' as match_type
                """
                try:
                    async with self.memory.driver.session() as session:
                        result = await session.run(
                            vector_query,
                            limit=limit,
                            embedding=query_embedding
                        )
                        semantic_results = [dict(record) async for record in result]
                        results.extend(semantic_results)
                except Exception as e:
                    # Vector index might not exist yet
                    print(f"[DocumentProcessor] Vector search error: {e}")

        # Deduplicate and sort by score
        seen = set()
        unique_results = []
        for r in sorted(results, key=lambda x: x['score'], reverse=True):
            key = (r['document_id'], r.get('chunk_id'))
            if key not in seen:
                seen.add(key)
                unique_results.append(SearchResult(
                    type=r['type'],
                    document_id=r['document_id'],
                    chunk_id=r.get('chunk_id'),
                    filename=r['filename'],
                    heading=r.get('heading'),
                    content_preview=r['content_preview'],
                    score=r['score'],
                    match_type=r['match_type']
                ))

        # Apply pagination
        total = len(unique_results)
        paginated = unique_results[offset:offset + limit]

        return {
            "results": [r.__dict__ for r in paginated],
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": offset + len(paginated) < total
        }

    async def delete_document_cascade(self, doc_id: str) -> DeleteResult:
        """Delete document and all related data."""
        async with self.memory.driver.session() as session:
            # Count what we're deleting
            count_query = """
            MATCH (d:Document {id: $doc_id})
            OPTIONAL MATCH (d)-[:HAS_CHUNK]->(c:DocumentChunk)
            OPTIONAL MATCH (b:Belief)-[:DERIVED_FROM]->(c)
            OPTIONAL MATCH (c)-[:MENTIONS]->(e:Entity)
            WHERE NOT EXISTS { MATCH (other:DocumentChunk)-[:MENTIONS]->(e) WHERE other.id <> c.id }
            OPTIONAL MATCH (exp:Experience)-[:ABOUT]->(d)
            RETURN count(DISTINCT c) as chunks,
                   count(DISTINCT b) as beliefs,
                   count(DISTINCT e) as entities,
                   count(DISTINCT exp) as experiences
            """
            count_result = await session.run(count_query, doc_id=doc_id)
            counts = await count_result.single()

            # Delete beliefs derived from chunks
            await session.run("""
                MATCH (d:Document {id: $doc_id})-[:HAS_CHUNK]->(c:DocumentChunk)
                MATCH (b:Belief)-[:DERIVED_FROM]->(c)
                DETACH DELETE b
            """, doc_id=doc_id)

            # Delete orphaned entities (mentioned only by this doc's chunks)
            await session.run("""
                MATCH (d:Document {id: $doc_id})-[:HAS_CHUNK]->(c:DocumentChunk)-[:MENTIONS]->(e:Entity)
                WHERE NOT EXISTS { MATCH (other:DocumentChunk)-[:MENTIONS]->(e) WHERE other.document_id <> $doc_id }
                DETACH DELETE e
            """, doc_id=doc_id)

            # Delete experiences about this document
            await session.run("""
                MATCH (exp:Experience)-[:ABOUT]->(d:Document {id: $doc_id})
                DETACH DELETE exp
            """, doc_id=doc_id)

            # Delete chunks
            await session.run("""
                MATCH (d:Document {id: $doc_id})-[:HAS_CHUNK]->(c:DocumentChunk)
                DETACH DELETE c
            """, doc_id=doc_id)

            # Delete document
            await session.run("""
                MATCH (d:Document {id: $doc_id})
                DETACH DELETE d
            """, doc_id=doc_id)

        return DeleteResult(
            document_id=doc_id,
            chunks_deleted=counts['chunks'] if counts else 0,
            beliefs_deleted=counts['beliefs'] if counts else 0,
            entities_deleted=counts['entities'] if counts else 0,
            experiences_deleted=counts['experiences'] if counts else 0
        )

    # ==================== Collection Methods ====================

    async def create_collection(
        self,
        name: str,
        notes: str = None
    ) -> str:
        """Create a new document collection."""
        collection_id = f"coll_{uuid.uuid4().hex[:12]}"

        query = """
        CREATE (c:DocumentCollection {
            id: $collection_id,
            name: $name,
            user_notes: $notes,
            uploaded_at: datetime(),
            document_count: 0
        })
        RETURN c.id as id
        """

        async with self.memory.driver.session() as session:
            await session.run(
                query,
                collection_id=collection_id,
                name=name,
                notes=notes or ""
            )

        return collection_id

    async def get_collection(self, collection_id: str) -> Optional[Dict]:
        """Get collection by ID."""
        query = """
        MATCH (c:DocumentCollection {id: $collection_id})
        OPTIONAL MATCH (c)-[:CONTAINS]->(d:Document)
        RETURN c, collect(d.id) as document_ids
        """
        async with self.memory.driver.session() as session:
            result = await session.run(query, collection_id=collection_id)
            record = await result.single()
            if record:
                coll = dict(record['c'])
                coll['document_ids'] = record['document_ids']
                return coll
        return None

    async def list_collections(self, offset: int = 0, limit: int = 20) -> Dict:
        """List all collections."""
        count_query = "MATCH (c:DocumentCollection) RETURN count(c) as total"
        list_query = """
        MATCH (c:DocumentCollection)
        RETURN c
        ORDER BY c.uploaded_at DESC
        SKIP $offset
        LIMIT $limit
        """

        async with self.memory.driver.session() as session:
            count_result = await session.run(count_query)
            count_record = await count_result.single()
            total = count_record['total'] if count_record else 0

            list_result = await session.run(list_query, offset=offset, limit=limit)
            collections = [dict(record['c']) async for record in list_result]

        return {
            "collections": collections,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": offset + len(collections) < total
        }

    async def delete_collection(self, collection_id: str, delete_documents: bool = False) -> Dict:
        """Delete a collection, optionally with its documents."""
        async with self.memory.driver.session() as session:
            if delete_documents:
                # Get document IDs first
                doc_query = """
                MATCH (c:DocumentCollection {id: $collection_id})-[:CONTAINS]->(d:Document)
                RETURN d.id as doc_id
                """
                result = await session.run(doc_query, collection_id=collection_id)
                doc_ids = [record['doc_id'] async for record in result]

                # Delete each document
                for doc_id in doc_ids:
                    await self.delete_document_cascade(doc_id)

                docs_deleted = len(doc_ids)
            else:
                docs_deleted = 0

            # Delete collection
            await session.run("""
                MATCH (c:DocumentCollection {id: $collection_id})
                DETACH DELETE c
            """, collection_id=collection_id)

        return {
            "collection_id": collection_id,
            "documents_deleted": docs_deleted
        }


# Singleton instance
_document_processor: Optional[DocumentProcessor] = None


def get_document_processor() -> Optional[DocumentProcessor]:
    """Get the document processor singleton."""
    return _document_processor


def initialize_document_processor(memory, llm_client, config: Dict = None) -> DocumentProcessor:
    """Initialize the document processor singleton."""
    global _document_processor
    _document_processor = DocumentProcessor(memory, llm_client, config)
    return _document_processor
