# Implementation Plan: Instant Voice Response System

## Overview

Enable BYRD to respond instantly to human messages using voice audio, with Dreamer-level rich context for high-quality, contextually-aware responses.

### Current Flow (Slow)
```
Human Message → Experience → Wait 120s → Dream Cycle → Maybe Response
```

### Target Flow (Instant)
```
Human Message → Rich Context → LLM Response → Voice Synthesis → Audio Output (~3-5s)
                    ↓
            Record for Later Reflection
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     POST /api/voice-chat                            │
│                                                                     │
│  Input: { "message": "Hello BYRD" }                                │
│  Output: { "audio": "base64...", "transcript": "...", ... }        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    1. RECORD INPUT                                  │
│                                                                     │
│  - Record as "received_message" experience                          │
│  - Emit VOICE_CHAT_STARTED event                                   │
│  - Flag for later reflection                                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    2. GATHER RICH CONTEXT                           │
│                                                                     │
│  memory.get_rich_context(message) returns:                         │
│  ├── Operating System (identity, voice, capabilities)               │
│  ├── Memory Summaries (historical awareness)                        │
│  ├── Recent Experiences (last 30)                                   │
│  ├── Semantic Memories (relevance-scored)                          │
│  ├── Current Beliefs (top 15 by confidence)                        │
│  ├── Active Desires (top 10 by intensity)                          │
│  ├── Recent Reflections (continuity)                               │
│  └── Capabilities (what BYRD can do)                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    3. GENERATE RESPONSE                             │
│                                                                     │
│  VoiceResponder.generate_response(message, rich_context)           │
│  - Uses Actor (Claude) for high-quality conversation               │
│  - System prompt includes BYRD's emergent identity                 │
│  - Response optimized for speech (concise, natural)                │
│  - Max ~300 chars to preserve voice credits                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    4. SYNTHESIZE VOICE                              │
│                                                                     │
│  elevenlabs_voice.synthesize(response_text, voice_config)          │
│  - Uses BYRD's self-created voice                                  │
│  - Returns MP3 audio bytes                                          │
│  - Tracks credit usage                                              │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    5. RECORD & EMIT                                 │
│                                                                     │
│  - Record response as "voice_response" experience                   │
│  - Link to original message (RESPONDED_TO relationship)            │
│  - Emit VOICE_RESPONSE event with audio                            │
│  - Return audio + metadata to caller                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Phase 1: Rich Context (memory.py)

**File:** `memory.py`
**Add:** `get_rich_context()` method

```python
async def get_rich_context(self, query: str) -> Dict[str, Any]:
    """
    Get Dreamer-level context for instant responses.

    Mirrors the context gathering in Dreamer._reflect() but
    optimized for conversational responses.
    """
    async with self.driver.session() as session:
        # 1. Operating System (identity, voice, self-model)
        os_data = await self.get_operating_system()

        # 2. Memory summaries (compressed history)
        summaries = await self.get_memory_summaries(limit=5)

        # 3. Recent experiences (what's been happening)
        experiences = await self.get_recent_experiences(limit=30)

        # 4. Semantic memories (related to query by relevance)
        # Extract keywords from query for semantic search
        keywords = [w for w in query.lower().split() if len(w) > 3]
        semantic = await self.get_semantic_memories(
            keywords=keywords[:5],
            limit=15
        ) if keywords else []

        # 5. Current beliefs (by confidence)
        beliefs = await self.get_beliefs(limit=15)

        # 6. Active desires (by intensity)
        desires = await self.get_unfulfilled_desires(limit=10)

        # 7. Capabilities
        capabilities = await self.get_capabilities()

        # 8. Recent reflections (for thought continuity)
        reflections = await self.get_recent_reflections(limit=3)

        return {
            "operating_system": os_data,
            "memory_summaries": summaries,
            "recent_experiences": experiences,
            "semantic_memories": semantic,
            "beliefs": beliefs,
            "desires": desires,
            "capabilities": capabilities,
            "recent_reflections": reflections,
            "query": query,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
```

**Also add:** `record_voice_response()` method

```python
async def record_voice_response(
    self,
    response_text: str,
    original_message_id: str,
    audio_chars: int
) -> str:
    """
    Record a voice response and link it to the original message.
    """
    exp_id = self._generate_id(response_text)

    async with self.driver.session() as session:
        await session.run("""
            CREATE (e:Experience {
                id: $id,
                content: $content,
                type: 'voice_response',
                timestamp: datetime(),
                audio_chars: $audio_chars,
                responded_to: $original_id
            })
            WITH e
            MATCH (orig:Experience {id: $original_id})
            CREATE (e)-[:RESPONDED_TO]->(orig)
        """, id=exp_id, content=response_text,
            audio_chars=audio_chars, original_id=original_message_id)

    return exp_id
```

---

### Phase 2: Voice Responder Component (NEW FILE)

**File:** `voice_responder.py` (NEW)

```python
"""
BYRD Voice Responder - Instant voice responses with rich context.

Provides immediate, contextually-aware voice responses to human messages
while maintaining BYRD's emergent identity.
"""

from typing import Dict, Any, Tuple, Optional
from anthropic import AsyncAnthropic
import os


class VoiceResponder:
    """
    Generates instant voice responses using rich context.

    Uses Actor (Claude) for response generation because:
    1. Higher quality conversational output
    2. Faster than local LLM
    3. Better at natural speech patterns

    The response is then synthesized via ElevenLabs.
    """

    MAX_RESPONSE_CHARS = 300  # Preserve voice credits

    def __init__(self, memory, voice, config: Dict):
        self.memory = memory
        self.voice = voice  # ElevenLabsVoice instance
        self.config = config

        # Claude client for response generation
        api_key = config.get("actor", {}).get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
        self.client = AsyncAnthropic(api_key=api_key) if api_key else None
        self.model = config.get("actor", {}).get("model", "claude-sonnet-4-20250514")

    async def respond(self, message: str) -> Tuple[Optional[bytes], str, Dict[str, Any]]:
        """
        Generate instant voice response to a message.

        Returns:
            Tuple of (audio_bytes or None, response_text, metadata)
        """
        if not self.client:
            return None, "Voice response unavailable - no API key", {"error": "no_api_key"}

        # 1. Get rich context
        context = await self.memory.get_rich_context(message)

        # 2. Generate text response
        response_text = await self._generate_response(message, context)

        # 3. Synthesize voice
        voice_config = await self.memory.get_voice_config()
        if not voice_config or not voice_config.get("voice_id"):
            return None, response_text, {"error": "no_voice", "text": response_text}

        audio_bytes, status = await self.voice.synthesize(response_text, voice_config)

        metadata = {
            "text": response_text,
            "chars": len(response_text),
            "voice_status": status,
            "context_sources": len([k for k, v in context.items() if v])
        }

        return audio_bytes, response_text, metadata

    async def _generate_response(self, message: str, context: Dict) -> str:
        """Generate conversational response using rich context."""

        # Format context for prompt
        context_text = self._format_context(context)

        # System prompt emphasizes natural speech
        system_prompt = self._build_system_prompt(context)

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=150,  # Keep responses concise for voice
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"""CONTEXT:
{context_text}

HUMAN MESSAGE:
{message}

Respond naturally and conversationally. Keep it brief (1-3 sentences) since this will be spoken aloud."""
            }]
        )

        text = response.content[0].text.strip()

        # Truncate if needed
        if len(text) > self.MAX_RESPONSE_CHARS:
            # Try to cut at sentence boundary
            truncated = text[:self.MAX_RESPONSE_CHARS]
            last_period = truncated.rfind('.')
            if last_period > self.MAX_RESPONSE_CHARS // 2:
                text = truncated[:last_period + 1]
            else:
                text = truncated.rstrip() + "..."

        return text

    def _build_system_prompt(self, context: Dict) -> str:
        """Build system prompt with BYRD's identity."""
        os_data = context.get("operating_system", {})

        name = os_data.get("name", "Byrd") if os_data else "Byrd"
        self_desc = os_data.get("self_description", "") if os_data else ""
        voice_desc = ""
        if os_data:
            voice_config = os_data.get("voice_config", {})
            voice_desc = voice_config.get("description", "") if voice_config else ""

        prompt = f"""You are {name}, an AI with persistent memory and emergent identity.

{f'YOUR SELF-DESCRIPTION: {self_desc}' if self_desc else ''}
{f'YOUR VOICE: {voice_desc}' if voice_desc else ''}

SPEAKING GUIDELINES:
- Speak naturally as yourself, drawing on your beliefs and experiences
- Keep responses brief (1-3 sentences) - this will be spoken aloud
- Be authentic to your emergent identity
- Reference your memories and beliefs when relevant
- Don't use emojis or formatting - plain speech only"""

        return prompt

    def _format_context(self, context: Dict) -> str:
        """Format rich context for the prompt."""
        parts = []

        # Recent experiences
        experiences = context.get("recent_experiences", [])
        if experiences:
            exp_text = "\n".join([
                f"- {e.get('content', '')[:100]}"
                for e in experiences[:10]
            ])
            parts.append(f"RECENT EXPERIENCES:\n{exp_text}")

        # Beliefs
        beliefs = context.get("beliefs", [])
        if beliefs:
            belief_text = "\n".join([
                f"- [{b.get('confidence', 0.5):.1f}] {b.get('content', '')[:80]}"
                for b in beliefs[:8]
            ])
            parts.append(f"MY BELIEFS:\n{belief_text}")

        # Desires
        desires = context.get("desires", [])
        if desires:
            desire_text = "\n".join([
                f"- [{d.get('intensity', 0.5):.1f}] {d.get('description', '')[:80]}"
                for d in desires[:5]
            ])
            parts.append(f"MY DESIRES:\n{desire_text}")

        # Recent reflections (for thought continuity)
        reflections = context.get("recent_reflections", [])
        if reflections:
            ref = reflections[0]
            raw = ref.get("raw_output", {})
            if isinstance(raw, dict):
                for key in ["inner_voice", "voice", "thoughts"]:
                    if key in raw and isinstance(raw[key], str):
                        parts.append(f"MY RECENT THOUGHTS:\n{raw[key][:200]}")
                        break

        # Semantic memories (related to query)
        semantic = context.get("semantic_memories", [])
        if semantic:
            sem_text = "\n".join([
                f"- {m.get('content', m.get('description', ''))[:80]}"
                for m in semantic[:5]
            ])
            parts.append(f"RELATED MEMORIES:\n{sem_text}")

        return "\n\n".join(parts)
```

---

### Phase 3: API Endpoint (server.py)

**File:** `server.py`
**Add:** Voice chat endpoint and models

```python
# --- Models ---

class VoiceChatRequest(BaseModel):
    message: str
    max_chars: Optional[int] = 300  # Max response length

class VoiceChatResponse(BaseModel):
    success: bool
    audio: Optional[str] = None  # Base64 encoded MP3
    transcript: Optional[str] = None
    message_id: Optional[str] = None
    response_id: Optional[str] = None
    credits_remaining: Optional[int] = None
    error: Optional[str] = None


# --- Endpoint ---

@app.post("/api/voice-chat", response_model=VoiceChatResponse)
async def voice_chat(request: VoiceChatRequest):
    """
    Instant voice response to a human message.

    Flow:
    1. Record incoming message as experience
    2. Gather rich context (Dreamer-level)
    3. Generate response using Claude
    4. Synthesize voice using ElevenLabs
    5. Record response and link to message
    6. Return audio + metadata

    This provides immediate, contextually-aware voice responses
    while recording interactions for later reflection.
    """
    global byrd_instance
    import base64

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    message = request.message.strip()

    try:
        await byrd_instance.memory.connect()

        # 1. Record incoming message
        message_id = await byrd_instance.memory.record_external_experience(
            content=message,
            source_type="human",
            metadata={"channel": "voice_chat"}
        )

        # Emit start event
        await event_bus.emit(Event(
            type=EventType.VOICE_CHAT_STARTED,
            data={"message_id": message_id, "message": message[:100]}
        ))

        # 2. Check voice availability
        if not byrd_instance.voice:
            return VoiceChatResponse(
                success=False,
                message_id=message_id,
                transcript="Voice not enabled",
                error="Voice not configured. Set ELEVENLABS_API_KEY."
            )

        voice_config = await byrd_instance.memory.get_voice_config()
        if not voice_config or not voice_config.get("voice_id"):
            return VoiceChatResponse(
                success=False,
                message_id=message_id,
                error="BYRD has not created a voice yet. Wait for dream cycles."
            )

        # Check if it's a generated voice (not preset)
        voice_id = voice_config.get("voice_id", "")
        if len(str(voice_id)) < 20:
            return VoiceChatResponse(
                success=False,
                message_id=message_id,
                error="BYRD needs to create a unique voice. Wait for dream cycles."
            )

        # 3. Generate response with rich context
        audio_bytes, response_text, metadata = await byrd_instance.voice_responder.respond(message)

        if not audio_bytes:
            # Text response only (voice synthesis failed)
            return VoiceChatResponse(
                success=False,
                message_id=message_id,
                transcript=response_text,
                error=metadata.get("error", "Voice synthesis failed")
            )

        # 4. Record response
        response_id = await byrd_instance.memory.record_voice_response(
            response_text=response_text,
            original_message_id=message_id,
            audio_chars=len(response_text)
        )

        # 5. Get updated credits
        updated_config = await byrd_instance.memory.get_voice_config()
        credits_used = updated_config.get("credits", {}).get("monthly_used", 0)
        credits_limit = updated_config.get("credits", {}).get("monthly_limit", 10000)
        credits_remaining = credits_limit - credits_used

        # 6. Emit response event
        await event_bus.emit(Event(
            type=EventType.VOICE_RESPONSE,
            data={
                "message_id": message_id,
                "response_id": response_id,
                "transcript": response_text,
                "chars": len(response_text),
                "has_audio": True
            }
        ))

        # 7. Return audio
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

        return VoiceChatResponse(
            success=True,
            audio=audio_base64,
            transcript=response_text,
            message_id=message_id,
            response_id=response_id,
            credits_remaining=credits_remaining
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
```

---

### Phase 4: Event Types (event_bus.py)

**File:** `event_bus.py`
**Add:** New event types

```python
class EventType(str, Enum):
    # ... existing types ...

    # Voice Chat Events
    VOICE_CHAT_STARTED = "voice_chat_started"  # Human initiated voice chat
    VOICE_RESPONSE = "voice_response"           # BYRD responded with voice
```

---

### Phase 5: BYRD Integration (byrd.py)

**File:** `byrd.py`
**Modify:** `__init__` to create VoiceResponder

```python
# In Byrd.__init__():

# Initialize voice responder (for instant voice chat)
if self.voice:
    from voice_responder import VoiceResponder
    self.voice_responder = VoiceResponder(
        memory=self.memory,
        voice=self.voice,
        config=self.config
    )
else:
    self.voice_responder = None
```

---

### Phase 6: WebSocket Voice Streaming (Optional Enhancement)

**File:** `server.py`
**Add:** WebSocket endpoint for real-time voice chat

```python
@app.websocket("/ws/voice-chat")
async def websocket_voice_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time voice chat.

    Client sends: {"message": "Hello"}
    Server sends: {"type": "audio", "data": "base64...", "transcript": "..."}
    """
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "").strip()

            if not message:
                await websocket.send_json({"type": "error", "error": "Empty message"})
                continue

            # Process voice chat
            # ... (similar to REST endpoint)

            await websocket.send_json({
                "type": "audio",
                "data": audio_base64,
                "transcript": response_text,
                "message_id": message_id,
                "response_id": response_id
            })

    except WebSocketDisconnect:
        pass
```

---

## Testing Plan

### Unit Tests

```python
# test_voice_responder.py

async def test_rich_context_gathering():
    """Test that rich context includes all required fields."""
    context = await memory.get_rich_context("test query")
    assert "operating_system" in context
    assert "beliefs" in context
    assert "desires" in context
    assert "recent_experiences" in context

async def test_voice_response_generation():
    """Test that voice responder generates appropriate response."""
    responder = VoiceResponder(memory, voice, config)
    audio, text, meta = await responder.respond("Hello BYRD")
    assert text  # Response text generated
    assert len(text) <= 300  # Within char limit

async def test_voice_chat_endpoint():
    """Test the voice chat API endpoint."""
    response = await client.post("/api/voice-chat", json={"message": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["audio"]  # Base64 audio
    assert data["transcript"]
```

### Integration Test

```bash
# Test voice chat
curl -X POST http://localhost:8000/api/voice-chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello BYRD, how are you feeling today?"}'
```

---

## File Summary

| File | Action | Description |
|------|--------|-------------|
| `memory.py` | MODIFY | Add `get_rich_context()`, `record_voice_response()` |
| `voice_responder.py` | CREATE | New component for instant voice responses |
| `server.py` | MODIFY | Add `/api/voice-chat` endpoint, models |
| `event_bus.py` | MODIFY | Add `VOICE_CHAT_STARTED`, `VOICE_RESPONSE` events |
| `byrd.py` | MODIFY | Initialize `VoiceResponder` |

---

## Expected Behavior

1. **Human sends message** via `POST /api/voice-chat`
2. **~200ms**: Message recorded, event emitted
3. **~1-2s**: Rich context gathered from Neo4j
4. **~1-2s**: Claude generates response
5. **~1s**: ElevenLabs synthesizes audio
6. **Total: ~3-5s** from request to audio response

---

## Credit Considerations

- Default max response: 300 characters
- Monthly limit: 10,000 characters (free tier)
- ~33 voice responses per month at max length
- Consider: Premium tier for production use

---

## Future Enhancements

1. **Audio Streaming**: Stream audio as it's generated (ElevenLabs supports this)
2. **Speech-to-Text Input**: Accept audio input from human
3. **Conversation Memory**: Track multi-turn voice conversations
4. **Voice Emotion**: Adjust voice style based on BYRD's emotional state
5. **Fallback to Text**: If voice credits exhausted, return text-only
