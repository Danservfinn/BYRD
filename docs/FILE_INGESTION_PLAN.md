# BYRD File Ingestion System - Implementation Plan

## Overview

Enable BYRD to receive, parse, categorize, and store files in Neo4j for future retrieval and reflection. Documents become part of BYRD's knowledge substrate—not just stored, but understood.

### Design Principles

1. **Layered Processing**: Immediate indexing for retrieval, deeper reflection in dream cycles
2. **Hybrid Categorization**: BYRD analyzes content, user hints weighted as guidance
3. **Smart Storage**: Inline for small files, chunked for large ones
4. **Provenance Tracking**: Beliefs trace back to specific document chunks

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         FILE INGESTION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   User Upload                                                    │
│   (UI / API)                                                     │
│        │                                                         │
│        ▼                                                         │
│   ┌─────────────┐                                               │
│   │   PHASE 1   │  Quick Ingest (<2s)                           │
│   │  Validate   │  • Hash check (dedup)                         │
│   │  + Queue    │  • Create pending Document                    │
│   └─────────────┘  • Return immediately                         │
│        │                                                         │
│        ▼                                                         │
│   ┌─────────────┐                                               │
│   │   PHASE 2   │  Background Processing                        │
│   │  Process    │  • Extract text                               │
│   │  + Store    │  • Analyze (LLM summary, type detection)      │
│   └─────────────┘  • Chunk intelligently                        │
│        │           • Generate embeddings                         │
│        │           • Store in Neo4j                              │
│        ▼           • Extract entities (Graphiti)                 │
│   ┌─────────────┐                                               │
│   │   PHASE 3   │  Dream Cycle Integration                      │
│   │  Reflect    │  • Dreamer notices new documents              │
│   │  + Learn    │  • Forms beliefs from chunks                  │
│   └─────────────┘  • Creates document relationships             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Neo4j Schema

### Node Types

```cypher
// DocumentCollection - groups related files
CREATE (dc:DocumentCollection {
  id: "coll_<uuid>",
  name: "Project Codebase",
  uploaded_at: datetime(),
  document_count: 12,
  user_notes: "The main API codebase"
})

// Document - the file itself
CREATE (d:Document {
  id: "doc_<uuid>",
  filename: "paper.pdf",
  file_type: "pdf",
  mime_type: "application/pdf",
  size_bytes: 245000,
  content_hash: "sha256:abc123...",
  uploaded_at: datetime(),

  // User-provided metadata
  user_tags: ["research", "ai"],
  user_purpose: "knowledge",        // knowledge | context | memory
  user_notes: "Key paper on transformers",

  // BYRD-generated metadata
  summary: "This paper introduces...",
  detected_type: "academic_paper",  // code | documentation | data | academic_paper | notes | conversation
  detected_language: "python",      // For code files
  importance: 0.7,                  // 0-1, based on content analysis

  // Storage strategy
  storage_mode: "chunked",          // "inline" | "chunked"
  content: null,                    // Only populated if storage_mode = "inline"
  chunk_count: 12,                  // Only if chunked

  // Processing status
  processing_status: "complete",    // pending | processing | complete | error
  processing_stage: "complete",     // validating | extracting | analyzing | chunking | embedding | storing | enriching | complete | error
  processing_error: null,
  processing_started_at: datetime(),
  processing_completed_at: datetime(),

  // Integration status
  graphiti_processed: true,
  reflected_on: false,
  reflected_at: null,
  reflection_depth: 0               // How many dream cycles have considered this
})

// DocumentChunk - for large documents
CREATE (c:DocumentChunk {
  id: "chunk_<uuid>",
  document_id: "doc_<uuid>",
  chunk_index: 0,
  heading: "Introduction",          // Section heading if available
  content: "The transformer architecture...",
  char_start: 0,
  char_end: 1050,
  overlap_prev: 0,                  // Chars overlapping with previous chunk
  overlap_next: 50                  // Chars overlapping with next chunk
  // embedding stored via Neo4j Vector Index, not as property
})
```

### Relationships

```cypher
// Collection contains documents
(dc:DocumentCollection)-[:CONTAINS]->(d:Document)

// Document has chunks
(d:Document)-[:HAS_CHUNK]->(c:DocumentChunk)

// Chunks mention entities (from Graphiti)
(c:DocumentChunk)-[:MENTIONS {confidence: 0.9}]->(e:Entity)

// Beliefs derived from chunks (provenance)
(b:Belief)-[:DERIVED_FROM {relevance: 0.8, created_at: datetime()}]->(c:DocumentChunk)

// Experiences about documents
(exp:Experience)-[:ABOUT]->(d:Document)

// Document relationships (discovered by BYRD)
(d1:Document)-[:RELATES_TO {reason: "implements concepts from", confidence: 0.85}]->(d2:Document)
```

### Indexes and Constraints

```cypher
// Uniqueness constraints
CREATE CONSTRAINT doc_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT doc_hash IF NOT EXISTS FOR (d:Document) REQUIRE d.content_hash IS UNIQUE;
CREATE CONSTRAINT chunk_id IF NOT EXISTS FOR (c:DocumentChunk) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT coll_id IF NOT EXISTS FOR (dc:DocumentCollection) REQUIRE dc.id IS UNIQUE;

// Vector index for semantic search (Neo4j 5.11+)
CREATE VECTOR INDEX chunk_embeddings IF NOT EXISTS
FOR (c:DocumentChunk)
ON c.embedding
OPTIONS {indexConfig: {
  `vector.dimensions`: 384,
  `vector.similarity_function`: 'cosine'
}};

// Performance indexes
CREATE INDEX doc_status IF NOT EXISTS FOR (d:Document) ON (d.processing_status);
CREATE INDEX doc_reflected IF NOT EXISTS FOR (d:Document) ON (d.reflected_on);
CREATE INDEX doc_uploaded IF NOT EXISTS FOR (d:Document) ON (d.uploaded_at);
CREATE INDEX chunk_doc IF NOT EXISTS FOR (c:DocumentChunk) ON (c.document_id);
```

---

## Processing Pipeline

### Configuration

```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
INLINE_THRESHOLD = 5000           # Files smaller than 5KB stored inline
CHUNK_TARGET_SIZE = 1000          # Target characters per chunk
CHUNK_OVERLAP = 50                # Character overlap between chunks
EMBEDDING_BATCH_SIZE = 32         # Embeddings generated in batches
```

### Processing Stages

```python
class ProcessingStage(Enum):
    VALIDATING = "validating"     # Check file type, size, hash
    EXTRACTING = "extracting"     # Extract text from PDF, etc.
    ANALYZING = "analyzing"       # LLM summary, type detection
    CHUNKING = "chunking"         # Split into chunks
    EMBEDDING = "embedding"       # Generate embeddings
    STORING = "storing"           # Write to Neo4j
    ENRICHING = "enriching"       # Graphiti entity extraction
    COMPLETE = "complete"
    ERROR = "error"
```

### Chunking Strategies

| File Type | Strategy |
|-----------|----------|
| Markdown | Split by headers (##, ###) |
| Code | Split by functions/classes |
| PDF | Split by paragraphs/pages |
| Plain text | Split by paragraphs or fixed size |
| JSON | Split by top-level keys |

### Two-Phase Processing

**Phase 1: Quick Ingest (<2 seconds)**
1. Validate file type and size
2. Compute content hash
3. Check for duplicate (return existing if found)
4. Create Document node with `status: pending`
5. Queue background processing
6. Return immediately with document ID

**Phase 2: Background Processing**
1. Extract text content
2. Analyze with LLM (summary, type, importance)
3. Decide storage mode (inline vs chunked)
4. If chunked: create chunks with appropriate strategy
5. Generate embeddings in batches
6. Store embeddings in Neo4j vector index
7. Run Graphiti entity extraction
8. Update document status to complete
9. Emit completion event

---

## API Endpoints

### Upload Single File

```
POST /api/documents/upload
Content-Type: multipart/form-data

file: <binary>
tags: "research,ai"           (optional, comma-separated)
purpose: "knowledge"          (optional: knowledge|context|memory)
notes: "Important paper"      (optional)
collection_id: "coll_abc123"  (optional)

Response 202:
{
  "document_id": "doc_xyz789",
  "status": "processing",
  "message": "Document queued for processing",
  "estimated_time_seconds": 15
}

Response 200 (duplicate):
{
  "document_id": "doc_existing123",
  "status": "duplicate",
  "message": "Document already exists",
  "document": { ... existing document details ... }
}
```

### Upload Multiple Files

```
POST /api/documents/upload-multiple
Content-Type: multipart/form-data

files: <binary[]>
tags: "project"
purpose: "context"
collection_name: "My Project"  (creates collection if provided)

Response 202:
{
  "collection_id": "coll_abc123",
  "results": [
    {"filename": "file1.py", "document_id": "doc_1", "status": "processing"},
    {"filename": "file2.py", "document_id": "doc_2", "status": "processing"},
    {"filename": "file3.py", "document_id": "doc_existing", "status": "duplicate"}
  ],
  "total": 3,
  "processing": 2,
  "duplicates": 1
}
```

### Get Document

```
GET /api/documents/{doc_id}

Response 200:
{
  "id": "doc_xyz789",
  "filename": "paper.pdf",
  "file_type": "pdf",
  "size_bytes": 245000,
  "uploaded_at": "2024-01-15T10:30:00Z",
  "user_tags": ["research"],
  "user_purpose": "knowledge",
  "summary": "This paper introduces...",
  "detected_type": "academic_paper",
  "importance": 0.7,
  "processing_status": "complete",
  "chunk_count": 12,
  "reflected_on": true,
  "belief_count": 3
}
```

### Get Document Content

```
GET /api/documents/{doc_id}/content

Response 200:
{
  "document_id": "doc_xyz789",
  "storage_mode": "chunked",
  "chunks": [
    {"index": 0, "heading": "Introduction", "content": "..."},
    {"index": 1, "heading": "Methods", "content": "..."}
  ]
}

// Or for inline storage:
{
  "document_id": "doc_abc123",
  "storage_mode": "inline",
  "content": "Full file content here..."
}
```

### Get Processing Progress

```
GET /api/documents/{doc_id}/progress

Response 200:
{
  "document_id": "doc_xyz789",
  "status": "processing",
  "stage": "embedding",
  "progress_percent": 65,
  "stages_completed": ["validating", "extracting", "analyzing", "chunking"],
  "current_stage": "embedding",
  "stages_remaining": ["storing", "enriching"],
  "estimated_seconds_remaining": 8
}
```

### List Documents

```
GET /api/documents?offset=0&limit=20&purpose=knowledge&status=complete

Response 200:
{
  "documents": [...],
  "total": 47,
  "offset": 0,
  "limit": 20,
  "has_more": true
}
```

### Search Documents

```
GET /api/documents/search?q=transformer+architecture&mode=hybrid&limit=10

Response 200:
{
  "results": [
    {
      "type": "chunk",
      "document_id": "doc_xyz789",
      "chunk_id": "chunk_abc123",
      "filename": "paper.pdf",
      "heading": "Architecture",
      "content_preview": "The transformer architecture uses...",
      "score": 0.92,
      "match_type": "semantic"
    },
    {
      "type": "document",
      "document_id": "doc_def456",
      "chunk_id": null,
      "filename": "notes.md",
      "heading": null,
      "content_preview": "Notes on transformer models...",
      "score": 0.85,
      "match_type": "keyword"
    }
  ],
  "total": 23,
  "offset": 0,
  "limit": 10,
  "has_more": true
}
```

### Delete Document (Cascade)

```
DELETE /api/documents/{doc_id}

Response 200:
{
  "deleted": {
    "document": "doc_xyz789",
    "chunks": 12,
    "orphaned_beliefs": 2,
    "orphaned_entities": 5,
    "experiences": 1
  },
  "message": "Document and related data deleted"
}
```

### Collection Endpoints

```
POST /api/documents/collections
GET /api/documents/collections
GET /api/documents/collections/{coll_id}
DELETE /api/documents/collections/{coll_id}
```

---

## UI Integration

### Drag & Drop Zone

```html
<!-- Add to byrd-3d-visualization.html -->

<!-- Full-screen drop zone (appears on drag) -->
<div id="upload-dropzone" class="fixed inset-0 z-[200] hidden pointer-events-none">
  <div class="absolute inset-0 bg-purple-900/80 backdrop-blur-sm"></div>
  <div class="absolute inset-0 flex items-center justify-center">
    <div class="text-center">
      <div class="text-6xl mb-4">📄</div>
      <div class="text-2xl text-white font-bold">Drop files to feed BYRD</div>
      <div class="text-purple-200 mt-2">PDF, text, code, markdown, JSON</div>
    </div>
  </div>
</div>

<!-- Upload button in toolbar -->
<button id="btn-upload" class="px-3 py-1.5 bg-purple-600 hover:bg-purple-500
        rounded text-white text-sm flex items-center gap-2">
  <span>📄</span> Feed BYRD
</button>
```

### Upload Modal

```html
<div id="upload-modal" class="fixed inset-0 z-[150] hidden">
  <div class="absolute inset-0 bg-black/50" onclick="closeUploadModal()"></div>
  <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
              bg-slate-800 rounded-lg p-6 w-[500px] max-h-[80vh] overflow-auto">
    <h2 class="text-xl font-bold text-white mb-4">Feed BYRD</h2>

    <!-- File list -->
    <div id="upload-file-list" class="space-y-2 mb-4 max-h-[200px] overflow-auto">
      <!-- Populated by JS -->
    </div>

    <!-- Metadata inputs -->
    <div class="space-y-3">
      <div>
        <label class="text-sm text-slate-400">Tags (comma-separated)</label>
        <input type="text" id="upload-tags" placeholder="research, ai, architecture"
               class="w-full bg-slate-700 rounded px-3 py-2 text-white">
      </div>
      <div>
        <label class="text-sm text-slate-400">Purpose</label>
        <select id="upload-purpose" class="w-full bg-slate-700 rounded px-3 py-2 text-white">
          <option value="">Let BYRD decide</option>
          <option value="knowledge">Knowledge (learn from this)</option>
          <option value="context">Context (reference material)</option>
          <option value="memory">Memory (remember this event)</option>
        </select>
      </div>
      <div>
        <label class="text-sm text-slate-400">Notes for BYRD</label>
        <textarea id="upload-notes" rows="2" placeholder="What should BYRD know about these files?"
                  class="w-full bg-slate-700 rounded px-3 py-2 text-white"></textarea>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex justify-end gap-3 mt-6">
      <button onclick="closeUploadModal()"
              class="px-4 py-2 bg-slate-600 hover:bg-slate-500 rounded text-white">
        Cancel
      </button>
      <button onclick="executeUpload()" id="btn-execute-upload"
              class="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded text-white">
        Upload
      </button>
    </div>
  </div>
</div>
```

### Progress Toasts

```html
<div id="upload-progress-container" class="fixed bottom-4 right-4 z-[100] space-y-2">
  <!-- Progress toasts inserted here by JS -->
</div>
```

### JavaScript Integration

```javascript
const uploadState = {
  selectedFiles: [],
  uploading: false,
  activeUploads: new Map()
};

// Drag & drop handlers
document.addEventListener('dragenter', (e) => {
  e.preventDefault();
  document.getElementById('upload-dropzone').classList.remove('hidden');
});

document.getElementById('upload-dropzone').addEventListener('dragleave', (e) => {
  if (e.target === document.getElementById('upload-dropzone')) {
    document.getElementById('upload-dropzone').classList.add('hidden');
  }
});

document.getElementById('upload-dropzone').addEventListener('drop', (e) => {
  e.preventDefault();
  document.getElementById('upload-dropzone').classList.add('hidden');
  handleFiles(e.dataTransfer.files);
});

// File handling
function handleFiles(fileList) {
  uploadState.selectedFiles = Array.from(fileList).filter(validateFile);
  if (uploadState.selectedFiles.length > 0) {
    showUploadModal();
  }
}

function validateFile(file) {
  const maxSize = 10 * 1024 * 1024; // 10MB
  const allowedTypes = [
    'text/plain', 'text/markdown', 'application/pdf',
    'application/json', 'text/x-python', 'text/javascript'
  ];
  // Also allow by extension
  const allowedExts = ['.txt', '.md', '.pdf', '.json', '.py', '.js', '.ts', '.yaml', '.yml'];

  const ext = '.' + file.name.split('.').pop().toLowerCase();
  return file.size <= maxSize && (allowedTypes.includes(file.type) || allowedExts.includes(ext));
}

// Upload execution
async function executeUpload() {
  const formData = new FormData();
  uploadState.selectedFiles.forEach(f => formData.append('files', f));
  formData.append('tags', document.getElementById('upload-tags').value);
  formData.append('purpose', document.getElementById('upload-purpose').value);
  formData.append('notes', document.getElementById('upload-notes').value);

  closeUploadModal();

  const response = await fetch('/api/documents/upload-multiple', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  result.results.forEach(r => {
    if (r.status === 'processing') {
      showProgressToast(r.document_id, r.filename);
      subscribeToProgress(r.document_id);
    }
  });
}

// WebSocket progress updates
function subscribeToProgress(docId) {
  // Use existing WebSocket connection
  uploadState.activeUploads.set(docId, { progress: 0, stage: 'validating' });
}

// Handle progress events from WebSocket
function handleDocumentProgress(event) {
  const { document_id, stage, progress_percent } = event.data;
  updateProgressToast(document_id, stage, progress_percent);

  if (stage === 'complete') {
    setTimeout(() => removeProgressToast(document_id), 3000);
  }
}
```

---

## Dream Cycle Integration

### Dreamer Document Awareness

The Dreamer periodically checks for unreflected documents and includes them in reflection context.

```python
# In dreamer.py

async def _get_unreflected_documents(self, limit: int = 3) -> List[Dict]:
    """Get documents BYRD hasn't reflected on yet."""
    query = """
    MATCH (d:Document)
    WHERE d.reflected_on = false
      AND d.processing_status = 'complete'
    RETURN d.id as id, d.filename as filename, d.summary as summary,
           d.detected_type as type, d.user_purpose as purpose,
           d.importance as importance
    ORDER BY d.importance DESC, d.uploaded_at DESC
    LIMIT $limit
    """
    async with self.memory.driver.session() as session:
        result = await session.run(query, limit=limit)
        return [dict(record) async for record in result]
```

### Document-Aware Reflection

When unreflected documents exist, they're included in the reflection prompt:

```
## NEW DOCUMENTS TO CONSIDER

### paper.pdf (academic_paper)
Purpose: knowledge
Summary: This paper introduces the transformer architecture...

Key sections:
**Introduction**
The transformer architecture revolutionizes...

**Methods**
We propose a self-attention mechanism...

---
```

### Belief Formation from Documents

BYRD can form beliefs that trace back to specific document chunks:

```python
async def create_belief_from_document(
    self,
    content: str,
    confidence: float,
    chunk_ids: List[str],
    reasoning: str = None
) -> str:
    """Create a belief derived from document chunks."""
    # Creates Belief node with DERIVED_FROM relationships to chunks
```

### Reflection Output Extension

```json
{
  "output": {
    "document_beliefs": [
      {
        "content": "The architecture uses event-driven patterns",
        "confidence": 0.85,
        "source_chunks": ["chunk_abc123"],
        "reasoning": "Multiple sections describe EventBus patterns"
      }
    ],
    "document_questions": [
      {
        "question": "How does quantum randomness integrate with decisions?",
        "related_document": "doc_xyz789"
      }
    ],
    "document_connections": [
      {
        "from_doc": "doc_arch001",
        "to_doc": "doc_impl002",
        "relationship": "implements",
        "confidence": 0.9
      }
    ]
  }
}
```

---

## Implementation Checklist

### Phase 1: Core Infrastructure
- [ ] Create `document_processor.py`
- [ ] Add EventType entries to `event_bus.py`
- [ ] Add document methods to `memory.py`
- [ ] Run Neo4j schema migrations
- [ ] Add `python-multipart` to `requirements.txt`

### Phase 2: Processing Pipeline
- [ ] File type detection
- [ ] Content extraction (text, PDF, code)
- [ ] Chunking strategies
- [ ] Embedding generation
- [ ] Two-phase processing flow

### Phase 3: API Endpoints
- [ ] POST /api/documents/upload
- [ ] POST /api/documents/upload-multiple
- [ ] GET /api/documents/{id}
- [ ] GET /api/documents/{id}/progress
- [ ] GET /api/documents (list)
- [ ] GET /api/documents/search
- [ ] DELETE /api/documents/{id}
- [ ] Collection endpoints

### Phase 4: UI Integration
- [ ] Drag-drop zone
- [ ] Upload modal
- [ ] Progress toasts
- [ ] WebSocket integration

### Phase 5: Dream Integration
- [ ] `_get_unreflected_documents()` in Dreamer
- [ ] Document context in reflection prompt
- [ ] Process `document_beliefs` output
- [ ] Mark documents as `reflected_on`

---

## Configuration

```yaml
# Add to config.yaml

documents:
  max_file_size_mb: 10
  inline_threshold_bytes: 5000
  chunk_target_size: 1000
  chunk_overlap: 50
  embedding_batch_size: 32
  supported_types:
    - text/plain
    - text/markdown
    - application/pdf
    - application/json
    - text/x-python
    - text/javascript
    - text/typescript
    - text/yaml
```

---

## Success Criteria

| Criteria | Target |
|----------|--------|
| Upload latency | < 2s for quick ingest |
| Processing throughput | 1MB in < 30s |
| Search accuracy | Relevant in top 5 |
| Dream integration | Beliefs in 2 cycles |
| Memory stability | No leaks over 100 uploads |
