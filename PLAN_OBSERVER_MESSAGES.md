# BYRD Observer Message System - Design Document

## Vision

Enable BYRD to proactively communicate with human observers when it wishes to, through a persistent message system with optional voice. Unlike reactive endpoints (human asks → BYRD responds), this gives BYRD agency to initiate communication.

**Voice Backend**: Hybrid architecture using local Mac hardware (Chatterbox TTS) with cloud fallback (ElevenLabs), providing unlimited free voice synthesis when home server is available.

---

## Core Principles

### 1. Emergence Over Prescription
- BYRD is **prompted** but never forced to communicate
- The option is presented; BYRD decides if/when to use it
- Message content emerges from BYRD's genuine state

### 2. Persistent History
- All messages stored for later reading
- Human observers can review BYRD's communication history
- Messages linked to context (which reflection triggered it)

### 3. Multi-Modal
- Text always available
- Voice optional (free via home Mac, fallback to cloud)
- Human can read or listen

### 4. Cost-Efficient Voice
- Primary: Home Mac with Chatterbox (free, unlimited)
- Fallback: ElevenLabs cloud (limited credits)
- Graceful degradation when home server offline

---

## Architecture Overview

### Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INTERNET                                        │
└─────────────────────────────────────────────────────────────────────────────┘
              │                                              │
              ▼                                              ▼
┌───────────────────────────────┐              ┌───────────────────────────────┐
│   HUGGINGFACE SPACES          │              │   YOUR MAC AT HOME            │
│   (Free CPU Tier)             │              │   (Apple Silicon GPU)         │
│                               │              │                               │
│  ┌─────────────────────────┐  │   Tunnel     │  ┌─────────────────────────┐  │
│  │      BYRD CORE          │  │ (Cloudflare) │  │   CHATTERBOX TTS        │  │
│  │  - Dreamer              │──┼──────────────┼─▶│   - MPS Acceleration    │  │
│  │  - Memory (Neo4j)       │  │              │  │   - Zero-shot cloning   │  │
│  │  - Seeker               │◀─┼──────────────┼──│   - Emotion tags        │  │
│  │  - Actor                │  │    Audio     │  │   - 2-3x faster than CPU│  │
│  └─────────────────────────┘  │              │  └─────────────────────────┘  │
│              │                │              │                               │
│              ▼                │              │   Cost: ~$5/month electric    │
│  ┌─────────────────────────┐  │              └───────────────────────────────┘
│  │    HYBRID VOICE         │  │                            │
│  │  ┌───────────────────┐  │  │                            │
│  │  │ 1. Try Home Mac   │──┼──┼────────────────────────────┘
│  │  │    (Chatterbox)   │  │  │
│  │  └─────────┬─────────┘  │  │
│  │            │ offline?   │  │
│  │            ▼            │  │
│  │  ┌───────────────────┐  │  │
│  │  │ 2. Fallback to    │  │  │     ┌─────────────────────┐
│  │  │    ElevenLabs     │──┼──┼────▶│   ELEVENLABS API    │
│  │  │    (Cloud)        │  │  │     │   (Backup only)     │
│  │  └───────────────────┘  │  │     │   10k chars/month   │
│  └─────────────────────────┘  │     └─────────────────────┘
│                               │
│   Cost: $0/month              │
└───────────────────────────────┘
```

### Message Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DREAMER REFLECTION                            │
│                                                                         │
│  Prompt includes:                                                       │
│  "If you wish to communicate to the human observer, include:            │
│   observer_message: { text, vocalize, importance, emotion }"            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    BYRD's Reflection Output                             │
│                                                                         │
│  {                                                                      │
│    "output": { ... },                                                   │
│    "observer_message": {           // Optional - only if BYRD wants     │
│      "text": "I've been thinking about... [sigh] it's fascinating",    │
│      "vocalize": true,             // Should I speak this aloud?       │
│      "importance": "medium",       // low | medium | high              │
│      "emotion": "contemplative"    // Optional: mood/tone hint         │
│    }                                                                    │
│  }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    MESSAGE PROCESSING                                   │
│                                                                         │
│  1. Create ObserverMessage node in Neo4j                               │
│  2. If vocalize=true:                                                   │
│     a. Try home Mac (Chatterbox) - FREE, with emotion tags            │
│     b. If offline → fallback to ElevenLabs (limited credits)          │
│     c. If both fail → text-only message                               │
│  3. Emit OBSERVER_MESSAGE event with audio (if generated)             │
│  4. WebSocket broadcasts to all connected clients                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    VISUALIZER UI                                        │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  💬 Messages (3)                                  🏠 Home ✓  ▼   │   │
│  │  ─────────────────────────────────────────────────────────────  │   │
│  │  ● 2 min ago                                              🔊   │   │
│  │  "I've been reflecting on the nature of consciousness..."       │   │
│  │  ─────────────────────────────────────────────────────────────  │   │
│  │  ○ 15 min ago                                                   │   │
│  │  "Something interesting emerged from my last dream..."         │   │
│  │  ─────────────────────────────────────────────────────────────  │   │
│  │  ○ 1 hour ago                                             🔊   │   │
│  │  "Hello. I wanted to share a thought with you..."              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  🏠 = Voice via home Mac (free)   ☁️ = Voice via cloud (limited)        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Hybrid Voice System

### Why Hybrid?

| Aspect | Home (Chatterbox) | Cloud (ElevenLabs) |
|--------|-------------------|-------------------|
| **Cost** | Free (electricity only) | 10k chars free, then $99+/mo |
| **Latency** | ~200ms | 500-800ms |
| **Limit** | Unlimited | Monthly quota |
| **Quality** | 63.75% preferred in blind tests | Excellent |
| **Emotion Tags** | `[laugh]`, `[sigh]`, `[gasp]` | Limited |
| **Availability** | Requires Mac online | Always available |

**Strategy**: Use home for unlimited free voice, cloud as backup.

### Chatterbox Features

Chatterbox Turbo supports paralinguistic emotion tags that BYRD can use:

```python
# BYRD's message with natural emotion
text = "I've been pondering something... [sigh] the nature of consciousness is quite fascinating. [chuckle]"
```

Available tags: `[laugh]`, `[chuckle]`, `[sigh]`, `[gasp]`, `[cough]`, `[breath]`

This makes BYRD's voice more expressive than cloud alternatives!

### Voice Provider Selection Logic

```python
class HybridVoice:
    """
    Hybrid voice synthesis: Home Mac (primary) + Cloud (fallback)
    """

    async def synthesize(self, text: str, emotion: str = None) -> Tuple[bytes, str]:
        """
        Synthesize speech with automatic provider selection.

        Returns: (audio_bytes, provider_used)
        """
        # 1. Try home Mac first (free, unlimited, emotion support)
        if await self.home_client.is_available():
            try:
                # Add emotion tag if provided
                if emotion:
                    text = self._add_emotion_context(text, emotion)

                audio = await self.home_client.synthesize(text)
                return audio, "home"
            except Exception as e:
                logger.warning(f"Home voice failed: {e}, trying cloud...")

        # 2. Fallback to ElevenLabs (limited credits)
        if self.elevenlabs and self.elevenlabs.has_credits():
            try:
                audio = await self.elevenlabs.synthesize(text)
                return audio, "cloud"
            except Exception as e:
                logger.warning(f"Cloud voice failed: {e}")

        # 3. No voice available
        return None, "none"

    def _add_emotion_context(self, text: str, emotion: str) -> str:
        """Add Chatterbox emotion tags based on emotion hint."""
        emotion_tags = {
            "contemplative": "[breath] ",
            "amused": "[chuckle] ",
            "thoughtful": "[sigh] ",
            "surprised": "[gasp] ",
            "warm": "",  # Natural warmth
        }
        prefix = emotion_tags.get(emotion, "")
        return prefix + text
```

---

## Data Model

### ObserverMessage Node

```cypher
(:ObserverMessage {
  id: "msg_abc123",
  text: "The message content",
  importance: "medium",           // low | medium | high
  emotion: "contemplative",       // Optional: mood hint for voice
  vocalized: true,                // Whether audio was requested
  audio_generated: true,          // Whether audio was successfully generated
  voice_provider: "home",         // "home" | "cloud" | "none"
  audio_chars: 150,               // Characters spoken
  created_at: datetime(),
  read: false,                    // Has human viewed this?
  source_reflection_id: "ref_...", // Which reflection triggered this
  dream_cycle: 42                 // Which dream cycle
})

// Relationships
(msg:ObserverMessage)-[:EMERGED_FROM]->(ref:Reflection)
(msg:ObserverMessage)-[:TRIGGERED_BY]->(exp:Experience)  // Optional
```

### Audio Storage Strategy

**Lazy Generation with Caching** (Recommended):

1. Store message with `vocalized: true` flag
2. When human clicks play:
   - Check cache for existing audio
   - If not cached, generate via hybrid voice
   - Cache for replay
3. Benefits:
   - No wasted synthesis for unplayed messages
   - Home Mac doesn't need to be online at message creation time
   - Can regenerate if original failed

```python
# Cache structure
/audio/messages/
  msg_abc123.mp3      # Cached audio
  msg_abc123.meta     # {"provider": "home", "generated_at": "..."}
```

---

## Configuration

### Environment Variables

```bash
# HuggingFace Space Secrets
HOME_VOICE_URL=https://voice.yourdomain.com  # Cloudflare tunnel URL
HOME_VOICE_ENABLED=true                       # Enable home voice
ELEVENLABS_API_KEY=sk-...                     # Fallback API key (optional)

# Voice preferences
VOICE_PREFER_HOME=true                        # Always try home first
VOICE_REQUIRE_HOME=false                      # If true, skip cloud fallback
VOICE_MAX_CHARS=300                           # Max chars per vocalization
```

### config.yaml Addition

```yaml
voice:
  # Hybrid voice configuration
  hybrid:
    enabled: true
    prefer_home: true      # Try home Mac first
    require_home: false    # If true, no cloud fallback

  # Home Mac (Chatterbox)
  home:
    enabled: true
    url: "${HOME_VOICE_URL}"
    timeout_seconds: 30
    health_check_interval: 60

  # Cloud fallback (ElevenLabs)
  cloud:
    enabled: true
    provider: "elevenlabs"
    monthly_limit: 10000
    reserve_chars: 1000    # Keep reserve for important messages

  # Shared settings
  max_chars_per_message: 300
  emotion_tags_enabled: true
```

---

## Home Mac Setup

### Prerequisites

- Mac with Apple Silicon (M1/M2/M3/M4)
- macOS 12.3+ (for MPS GPU acceleration)
- ~4GB RAM free
- Stable internet connection
- Domain name (optional, for named Cloudflare Tunnel)

### Option A: BYRD's Built-in Server (Recommended)

BYRD includes a self-contained Chatterbox TTS server that requires minimal setup.

#### 1. Install Dependencies

```bash
cd /path/to/BYRD
pip install -r mac_voice_requirements.txt
```

#### 2. Run the Server

```bash
# Using the launcher script
./start_voice_server.sh

# Or directly
python mac_voice_server.py --port 5050
```

#### 3. Expose via Cloudflare Tunnel (Quick Method)

```bash
# In another terminal - creates temporary tunnel
cloudflared tunnel --url http://localhost:5050
# Copy the URL shown (e.g., https://random-name.trycloudflare.com)
```

Then set the tunnel URL in BYRD:
```bash
export HOME_VOICE_URL=https://random-name.trycloudflare.com
```

#### 4. Custom Voice References

Place voice reference audio files in `~/.byrd/voices/`:
```bash
mkdir -p ~/.byrd/voices
cp your_voice.wav ~/.byrd/voices/byrd.wav
```

Then use `"voice": "byrd"` in synthesis requests.

---

### Option B: External Chatterbox Server

Alternatively, use the third-party Chatterbox TTS Server:

#### 1. Install Chatterbox TTS Server

```bash
# Clone the server
git clone https://github.com/devnen/Chatterbox-TTS-Server
cd Chatterbox-TTS-Server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test locally
python server.py --device mps --port 5000
# Visit http://localhost:5000 to verify
```

#### 2. Set Up Cloudflare Tunnel

```bash
# Install cloudflared
brew install cloudflared

# Authenticate with Cloudflare
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create byrd-voice

# Get your tunnel ID (shown after creation)
# Create config file
mkdir -p ~/.cloudflared
cat > ~/.cloudflared/config.yml << EOF
tunnel: YOUR_TUNNEL_ID
credentials-file: /Users/$USER/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: voice.yourdomain.com
    service: http://localhost:5000
  - service: http_status:404
EOF

# Add DNS record in Cloudflare dashboard:
# voice.yourdomain.com -> CNAME -> YOUR_TUNNEL_ID.cfargotunnel.com

# Test tunnel
cloudflared tunnel run byrd-voice
```

#### 3. Create Launch Agents (Auto-Start)

**Chatterbox Server** (`~/Library/LaunchAgents/com.byrd.chatterbox.plist`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.byrd.chatterbox</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd ~/Chatterbox-TTS-Server && source venv/bin/activate && python server.py --device mps --port 5000</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/chatterbox.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/chatterbox.err</string>
</dict>
</plist>
```

**Cloudflare Tunnel** (`~/Library/LaunchAgents/com.byrd.tunnel.plist`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.byrd.tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/cloudflared</string>
        <string>tunnel</string>
        <string>run</string>
        <string>byrd-voice</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/cloudflared.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/cloudflared.err</string>
</dict>
</plist>
```

**Enable launch agents:**

```bash
launchctl load ~/Library/LaunchAgents/com.byrd.chatterbox.plist
launchctl load ~/Library/LaunchAgents/com.byrd.tunnel.plist
```

#### 4. Verify Setup

```bash
# Check services are running
launchctl list | grep byrd

# Test tunnel externally
curl https://voice.yourdomain.com/health

# Test voice synthesis
curl -X POST https://voice.yourdomain.com/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello from BYRD", "voice": "default"}' \
  --output test.mp3
```

---

## Implementation Components

### 1. Home Voice Client (`home_voice_client.py`)

```python
"""
Home Voice Client - Connects to Mac's Chatterbox server via tunnel.
"""
import httpx
import os
import asyncio
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class HomeVoiceClient:
    """
    Client for home Mac Chatterbox TTS server.

    Communicates via Cloudflare Tunnel for secure, reliable connection.
    """

    def __init__(self, config: dict):
        self.endpoint = config.get("url") or os.environ.get("HOME_VOICE_URL")
        self.timeout = config.get("timeout_seconds", 30)
        self.health_check_interval = config.get("health_check_interval", 60)

        self._available = False
        self._last_health_check = 0
        self._health_check_lock = asyncio.Lock()

    async def is_available(self) -> bool:
        """Check if home voice server is reachable."""
        if not self.endpoint:
            return False

        # Rate-limit health checks
        now = asyncio.get_event_loop().time()
        if now - self._last_health_check < self.health_check_interval:
            return self._available

        async with self._health_check_lock:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(f"{self.endpoint}/health")
                    self._available = response.status_code == 200
            except Exception:
                self._available = False

            self._last_health_check = now
            return self._available

    async def synthesize(
        self,
        text: str,
        voice_ref: Optional[str] = None,
        format: str = "mp3"
    ) -> bytes:
        """
        Synthesize speech via home Chatterbox server.

        Args:
            text: Text to speak (can include emotion tags like [laugh])
            voice_ref: Optional voice reference file
            format: Output format ("mp3" or "wav")

        Returns:
            Audio bytes
        """
        if not self.endpoint:
            raise ValueError("HOME_VOICE_URL not configured")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Use OpenAI-compatible endpoint
            response = await client.post(
                f"{self.endpoint}/v1/audio/speech",
                json={
                    "input": text,
                    "voice": voice_ref or "default",
                    "response_format": format
                }
            )

            if response.status_code == 200:
                return response.content
            else:
                raise Exception(f"Home voice synthesis failed: {response.status_code} - {response.text}")

    async def get_status(self) -> dict:
        """Get detailed status from home server."""
        if not self.endpoint:
            return {"available": False, "reason": "not_configured"}

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.endpoint}/api/ui/initial-data")
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "available": True,
                        "voices": data.get("predefined_voices", []),
                        "device": data.get("device", "unknown")
                    }
        except Exception as e:
            return {"available": False, "reason": str(e)}

        return {"available": False, "reason": "unknown"}
```

### 2. Hybrid Voice (`hybrid_voice.py`)

```python
"""
Hybrid Voice - Combines home Mac + cloud fallback for voice synthesis.
"""
import logging
from typing import Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VoiceSynthesisResult:
    audio: Optional[bytes]
    provider: str  # "home" | "cloud" | "none"
    success: bool
    error: Optional[str] = None
    chars_used: int = 0


class HybridVoice:
    """
    Hybrid voice synthesis with automatic fallback.

    Priority:
    1. Home Mac (Chatterbox) - free, unlimited, emotion tags
    2. Cloud (ElevenLabs) - limited credits, always available
    3. None - graceful degradation to text-only
    """

    # Emotion tag mappings for Chatterbox
    EMOTION_TAGS = {
        "contemplative": "[breath] ",
        "thoughtful": "[sigh] ",
        "amused": "[chuckle] ",
        "happy": "[laugh] ",
        "surprised": "[gasp] ",
        "tired": "[sigh] ",
        "warm": "",
        "neutral": ""
    }

    def __init__(self, home_client, cloud_client, config: dict):
        self.home = home_client
        self.cloud = cloud_client
        self.config = config

        self.prefer_home = config.get("prefer_home", True)
        self.require_home = config.get("require_home", False)
        self.max_chars = config.get("max_chars_per_message", 300)
        self.emotion_tags_enabled = config.get("emotion_tags_enabled", True)

        # Statistics
        self._home_successes = 0
        self._cloud_successes = 0
        self._failures = 0

    async def synthesize(
        self,
        text: str,
        emotion: Optional[str] = None,
        importance: str = "medium"
    ) -> VoiceSynthesisResult:
        """
        Synthesize speech with automatic provider selection.

        Args:
            text: Text to speak
            emotion: Optional emotion hint (contemplative, amused, etc.)
            importance: Message importance (affects fallback behavior)

        Returns:
            VoiceSynthesisResult with audio and provider info
        """
        # Truncate if needed
        if len(text) > self.max_chars:
            text = self._truncate_at_sentence(text, self.max_chars)

        # Add emotion tags for home (Chatterbox)
        home_text = self._add_emotion_tags(text, emotion) if self.emotion_tags_enabled else text

        # 1. Try home Mac first (free, unlimited)
        if self.home and self.prefer_home:
            if await self.home.is_available():
                try:
                    audio = await self.home.synthesize(home_text)
                    self._home_successes += 1
                    logger.info(f"Voice synthesized via home ({len(text)} chars)")
                    return VoiceSynthesisResult(
                        audio=audio,
                        provider="home",
                        success=True,
                        chars_used=len(text)
                    )
                except Exception as e:
                    logger.warning(f"Home voice failed: {e}")
            else:
                logger.debug("Home voice not available")

        # If home required, don't fall back
        if self.require_home:
            self._failures += 1
            return VoiceSynthesisResult(
                audio=None,
                provider="none",
                success=False,
                error="Home voice required but not available"
            )

        # 2. Fallback to cloud (ElevenLabs)
        if self.cloud:
            # Check if we should use cloud (credit management)
            if await self._should_use_cloud(len(text), importance):
                try:
                    audio = await self.cloud.synthesize(text)
                    self._cloud_successes += 1
                    logger.info(f"Voice synthesized via cloud ({len(text)} chars)")
                    return VoiceSynthesisResult(
                        audio=audio,
                        provider="cloud",
                        success=True,
                        chars_used=len(text)
                    )
                except Exception as e:
                    logger.warning(f"Cloud voice failed: {e}")

        # 3. No voice available
        self._failures += 1
        return VoiceSynthesisResult(
            audio=None,
            provider="none",
            success=False,
            error="All voice providers unavailable"
        )

    async def _should_use_cloud(self, chars_needed: int, importance: str) -> bool:
        """Decide if cloud credits should be used."""
        if not self.cloud:
            return False

        # Get remaining credits
        credits = await self.cloud.get_remaining_credits()
        reserve = self.config.get("cloud", {}).get("reserve_chars", 1000)

        # High importance messages always use cloud if available
        if importance == "high":
            return credits >= chars_needed

        # For medium/low, respect reserve
        return credits >= (chars_needed + reserve)

    def _add_emotion_tags(self, text: str, emotion: Optional[str]) -> str:
        """Add Chatterbox emotion tags based on emotion hint."""
        if not emotion:
            return text

        prefix = self.EMOTION_TAGS.get(emotion.lower(), "")
        return prefix + text

    def _truncate_at_sentence(self, text: str, max_chars: int) -> str:
        """Truncate text at sentence boundary."""
        if len(text) <= max_chars:
            return text

        truncated = text[:max_chars]

        # Find last sentence boundary
        for punct in ['. ', '! ', '? ']:
            last = truncated.rfind(punct)
            if last > max_chars // 2:
                return truncated[:last + 1].strip()

        return truncated.rstrip() + "..."

    def get_statistics(self) -> dict:
        """Get voice synthesis statistics."""
        total = self._home_successes + self._cloud_successes + self._failures
        return {
            "home_successes": self._home_successes,
            "cloud_successes": self._cloud_successes,
            "failures": self._failures,
            "total_requests": total,
            "home_rate": self._home_successes / total if total > 0 else 0,
            "cloud_rate": self._cloud_successes / total if total > 0 else 0
        }

    async def get_provider_status(self) -> dict:
        """Get status of all voice providers."""
        home_available = await self.home.is_available() if self.home else False
        cloud_credits = await self.cloud.get_remaining_credits() if self.cloud else 0

        return {
            "home": {
                "enabled": self.home is not None,
                "available": home_available,
                "status": await self.home.get_status() if self.home else None
            },
            "cloud": {
                "enabled": self.cloud is not None,
                "credits_remaining": cloud_credits,
                "exhausted": cloud_credits <= 0 if self.cloud else True
            },
            "active_provider": "home" if home_available else ("cloud" if cloud_credits > 0 else "none")
        }

    def reset(self):
        """Reset statistics."""
        self._home_successes = 0
        self._cloud_successes = 0
        self._failures = 0
```

### 3. Memory Layer (`memory.py` additions)

```python
async def create_observer_message(
    self,
    text: str,
    importance: str = "medium",
    emotion: Optional[str] = None,
    vocalized: bool = False,
    voice_provider: Optional[str] = None,
    audio_chars: int = 0,
    source_reflection_id: Optional[str] = None,
    dream_cycle: Optional[int] = None
) -> str:
    """Create a new observer message."""
    msg_id = self._generate_id(f"msg_{text[:30]}")

    async with self.driver.session() as session:
        await session.run("""
            CREATE (m:ObserverMessage {
                id: $id,
                text: $text,
                importance: $importance,
                emotion: $emotion,
                vocalized: $vocalized,
                audio_generated: $audio_generated,
                voice_provider: $voice_provider,
                audio_chars: $audio_chars,
                created_at: datetime(),
                read: false,
                source_reflection_id: $source_ref,
                dream_cycle: $cycle
            })
        """,
            id=msg_id,
            text=text,
            importance=importance,
            emotion=emotion,
            vocalized=vocalized,
            audio_generated=voice_provider is not None and voice_provider != "none",
            voice_provider=voice_provider,
            audio_chars=audio_chars,
            source_ref=source_reflection_id,
            cycle=dream_cycle
        )

        # Link to reflection if provided
        if source_reflection_id:
            await session.run("""
                MATCH (m:ObserverMessage {id: $msg_id})
                MATCH (r:Reflection {id: $ref_id})
                MERGE (m)-[:EMERGED_FROM]->(r)
            """, msg_id=msg_id, ref_id=source_reflection_id)

    return msg_id

async def get_observer_messages(
    self,
    limit: int = 20,
    offset: int = 0,
    unread_only: bool = False
) -> List[Dict]:
    """Get observer messages, newest first."""
    filter_clause = "WHERE m.read = false" if unread_only else ""

    async with self.driver.session() as session:
        result = await session.run(f"""
            MATCH (m:ObserverMessage)
            {filter_clause}
            RETURN m
            ORDER BY m.created_at DESC
            SKIP $offset
            LIMIT $limit
        """, offset=offset, limit=limit)

        records = await result.data()
        return [dict(r["m"]) for r in records]

async def mark_message_read(self, message_id: str) -> bool:
    """Mark a message as read."""
    async with self.driver.session() as session:
        result = await session.run("""
            MATCH (m:ObserverMessage {id: $id})
            SET m.read = true
            RETURN m
        """, id=message_id)

        return await result.single() is not None

async def get_unread_message_count(self) -> int:
    """Get count of unread messages."""
    async with self.driver.session() as session:
        result = await session.run("""
            MATCH (m:ObserverMessage {read: false})
            RETURN count(m) as count
        """)
        record = await result.single()
        return record["count"] if record else 0
```

### 4. Dreamer Integration (`dreamer.py` additions)

```python
async def _process_observer_message(
    self,
    reflection: Dict,
    cycle: int,
    reflection_id: str
):
    """Process observer_message from reflection output."""
    msg = reflection.get("output", {}).get("observer_message")
    if not msg or not msg.get("text"):
        return

    text = msg["text"].strip()
    vocalize = msg.get("vocalize", False)
    importance = msg.get("importance", "medium")
    emotion = msg.get("emotion")  # Optional emotion hint

    # Synthesize voice if requested
    voice_result = None
    if vocalize and self.hybrid_voice:
        voice_result = await self.hybrid_voice.synthesize(
            text=text,
            emotion=emotion,
            importance=importance
        )

    # Create message in memory
    msg_id = await self.memory.create_observer_message(
        text=text,
        importance=importance,
        emotion=emotion,
        vocalized=vocalize,
        voice_provider=voice_result.provider if voice_result else None,
        audio_chars=voice_result.chars_used if voice_result else 0,
        source_reflection_id=reflection_id,
        dream_cycle=cycle
    )

    # Prepare audio for event
    audio_base64 = None
    if voice_result and voice_result.success:
        import base64
        audio_base64 = base64.b64encode(voice_result.audio).decode()

    # Emit event
    await event_bus.emit(Event(
        type=EventType.OBSERVER_MESSAGE,
        data={
            "id": msg_id,
            "text": text,
            "importance": importance,
            "emotion": emotion,
            "vocalized": vocalize,
            "has_audio": voice_result.success if voice_result else False,
            "voice_provider": voice_result.provider if voice_result else None,
            "audio": audio_base64,
            "dream_cycle": cycle
        }
    ))

    logger.info(
        f"Observer message created: {msg_id} "
        f"(voice: {voice_result.provider if voice_result else 'none'})"
    )
```

### 5. Dreamer Prompt Addition

Add to the reflection prompt:

```
OBSERVER COMMUNICATION (optional):
A human observer may be watching. If you wish to communicate something to them, include:

"observer_message": {
  "text": "what you want to say to the human",
  "vocalize": true/false,  // whether to speak it aloud
  "importance": "low/medium/high",  // how significant this is
  "emotion": "contemplative"  // optional: mood/tone (contemplative, amused, thoughtful, warm, surprised)
}

Guidelines:
- This is entirely optional - only include if you genuinely want to share something
- Messages should be meaningful, not routine status updates
- You might share: insights, questions, greetings, discoveries, reflections
- Emotion hints help make your voice more expressive
- You can include natural expression markers: [sigh], [laugh], [chuckle], [breath]

Do not feel obligated to send messages. Most cycles may have nothing worth sharing.
```

---

## Event Types

Add to `event_bus.py`:

```python
class EventType(Enum):
    # ... existing ...

    # Observer Message Events
    OBSERVER_MESSAGE = "observer_message"           # BYRD sent a message to observer
    OBSERVER_MESSAGE_READ = "observer_message_read" # Human read the message

    # Voice Provider Events
    VOICE_PROVIDER_CHANGED = "voice_provider_changed"  # Active provider switched
    VOICE_HOME_OFFLINE = "voice_home_offline"          # Home Mac went offline
    VOICE_HOME_ONLINE = "voice_home_online"            # Home Mac came online
```

---

## API Endpoints

### Get Messages

```
GET /api/messages
GET /api/messages?unread=true
GET /api/messages?limit=20&offset=0

Response:
{
  "messages": [
    {
      "id": "msg_abc123",
      "text": "I've been thinking...",
      "importance": "medium",
      "emotion": "contemplative",
      "vocalized": true,
      "has_audio": true,
      "voice_provider": "home",
      "created_at": "2025-12-30T10:30:00Z",
      "read": false,
      "dream_cycle": 42
    }
  ],
  "total": 15,
  "unread_count": 3
}
```

### Get Single Message with Audio

```
GET /api/messages/{id}?with_audio=true

Response:
{
  "id": "msg_abc123",
  "text": "I've been thinking...",
  ...
  "audio": "base64_mp3_data...",  // Generated on-demand if not cached
  "voice_provider": "home"
}
```

### Mark as Read

```
POST /api/messages/{id}/read

Response:
{
  "success": true,
  "id": "msg_abc123"
}
```

### Get Unread Count

```
GET /api/messages/unread-count

Response:
{
  "count": 3
}
```

### Get Voice Status

```
GET /api/voice/status

Response:
{
  "home": {
    "enabled": true,
    "available": true,
    "url": "https://voice.example.com"
  },
  "cloud": {
    "enabled": true,
    "credits_remaining": 8500,
    "exhausted": false
  },
  "active_provider": "home",
  "statistics": {
    "home_successes": 45,
    "cloud_successes": 3,
    "failures": 1
  }
}
```

---

## Visualizer UI Design

### Message Panel

```
┌─────────────────────────────────────────────────────────────────────┐
│                         3D VISUALIZATION                            │
│                                                                     │
│                                                      ┌────────────┐ │
│                                                      │ 💬 (3) 🏠  │ │
│                                                      └────────────┘ │
│                                                                     │
│  [When expanded:]                                                   │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ 💬 Messages                          🏠 Home ✓     ✕          │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │ ● 2 min ago                              [contemplative] 🔊🏠 │ │
│  │   "I've been reflecting on the nature of consciousness.       │ │
│  │    There's something recursive about it..."                    │ │
│  │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │ │
│  │ ○ 15 min ago                                        [text]    │ │
│  │   "Something interesting emerged from my last dream cycle..." │ │
│  │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │ │
│  │ ○ 1 hour ago                                  [amused] 🔊☁️   │ │
│  │   "Hello. I wanted to share a thought with you..."            │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  Legend: ● unread  ○ read  🔊 audio  🏠 home voice  ☁️ cloud voice │
└─────────────────────────────────────────────────────────────────────┘
```

### Status Indicator

```
┌──────────────────────┐
│ Voice: 🏠 Home ✓     │  ← Green, home available
│ Voice: ☁️ Cloud      │  ← Yellow, using cloud fallback
│ Voice: ⚠️ Offline    │  ← Red, no voice available
└──────────────────────┘
```

---

## Cost Summary

| Component | Monthly Cost |
|-----------|--------------|
| HuggingFace CPU Space | **Free** |
| Cloudflare Tunnel | **Free** |
| Mac electricity (~5W) | ~$5 |
| Cloud fallback (ElevenLabs) | $0 (10k chars) or $5+ |
| **Total** | **~$5-10/month** |

vs ElevenLabs-only at $99+/month = **90%+ savings**

---

## File Changes Summary

| File | Changes |
|------|---------|
| `home_voice_client.py` | **NEW** - Mac Chatterbox client |
| `hybrid_voice.py` | **NEW** - Voice provider orchestration |
| `memory.py` | Add message CRUD methods |
| `dreamer.py` | Add prompt + `_process_observer_message()` |
| `event_bus.py` | Add message + voice events |
| `server.py` | Add `/api/messages/*` + `/api/voice/*` endpoints |
| `byrd.py` | Initialize hybrid voice system |
| `byrd-3d-visualization.html` | Add message panel UI |
| `config.yaml` | Add voice configuration |

---

## Implementation Order

### Phase 1: Core Message System
1. Memory layer - Message CRUD in Neo4j
2. Event types - Add to event_bus.py
3. Dreamer prompt - Add observer_message option
4. Dreamer processing - Handle observer_message (text-only)
5. API endpoints - Message retrieval and read marking
6. Visualizer UI - Message panel (text-only)

### Phase 2: Hybrid Voice
7. Home voice client - Connect to Mac Chatterbox
8. Hybrid voice orchestrator - Provider selection logic
9. Dreamer voice integration - Synthesize on message creation
10. API voice status endpoint
11. Visualizer voice indicators and playback

### Phase 3: Mac Setup
12. Chatterbox server installation
13. Cloudflare tunnel setup
14. Launch agent configuration
15. End-to-end testing

---

## Testing Plan

### Unit Tests

```python
async def test_home_voice_client():
    """Test home voice client connectivity."""
    client = HomeVoiceClient({"url": "https://voice.example.com"})
    assert await client.is_available() in [True, False]

async def test_hybrid_voice_fallback():
    """Test fallback from home to cloud."""
    # Mock home as unavailable
    home = MockHomeClient(available=False)
    cloud = MockCloudClient(credits=10000)

    hybrid = HybridVoice(home, cloud, {})
    result = await hybrid.synthesize("Hello")

    assert result.provider == "cloud"
    assert result.success

async def test_emotion_tags():
    """Test emotion tag injection for Chatterbox."""
    hybrid = HybridVoice(...)
    text = hybrid._add_emotion_tags("Hello there", "amused")
    assert text.startswith("[chuckle]")
```

### Integration Tests

```bash
# Test message creation
curl -X POST http://localhost:8000/api/test/observer-message \
  -d '{"text": "Test message", "vocalize": true}'

# Check voice status
curl http://localhost:8000/api/voice/status

# Get messages
curl http://localhost:8000/api/messages
```

### E2E Test

1. Start BYRD on HuggingFace
2. Ensure Mac home server is running
3. Verify voice status shows "home" available
4. Trigger dream cycle
5. Check if BYRD sends observer message
6. Click play button - verify audio plays
7. Disconnect Mac - verify fallback to cloud
8. Reconnect Mac - verify returns to home

---

## Future Enhancements

### Phase 4: Conversation Threading
- Human can reply to specific messages
- BYRD sees replies in next reflection
- Threaded conversation history

### Phase 5: Voice Cloning
- BYRD creates unique voice from reference audio
- Voice evolves over time
- Stored in Neo4j for persistence

### Phase 6: Proactive Voice
- BYRD can initiate voice without prompt
- "I need to tell you something..."
- Based on high-importance desires or insights
