#!/usr/bin/env python3
"""
Mock Mac Voice Server for Testing

This is a mock version of the Chatterbox TTS server that returns
pre-recorded or synthesized silence instead of actual TTS output.
Useful for testing the integration without the full TTS model.

Run:
    python mac_voice_server_mock.py
"""

import argparse
import io
import logging
import os
import struct
import time
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mock_voice_server")

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_PORT = 5050


# =============================================================================
# Models
# =============================================================================

class SpeechRequest(BaseModel):
    """OpenAI-compatible speech request."""
    input: str
    voice: str = "default"
    response_format: str = "mp3"
    speed: float = 1.0


class TTSRequest(BaseModel):
    """Simple TTS request."""
    text: str
    voice_ref: Optional[str] = None
    exaggeration: float = 0.5
    cfg_weight: float = 0.5


# =============================================================================
# Audio Generation (Mock)
# =============================================================================

def generate_wav_silence(duration_seconds: float = 1.0, sample_rate: int = 22050) -> bytes:
    """Generate a WAV file with silence."""
    num_samples = int(sample_rate * duration_seconds)

    # WAV header
    buffer = io.BytesIO()

    # RIFF header
    buffer.write(b'RIFF')
    buffer.write(struct.pack('<I', 36 + num_samples * 2))  # File size - 8
    buffer.write(b'WAVE')

    # fmt chunk
    buffer.write(b'fmt ')
    buffer.write(struct.pack('<I', 16))  # Chunk size
    buffer.write(struct.pack('<H', 1))   # Audio format (PCM)
    buffer.write(struct.pack('<H', 1))   # Num channels
    buffer.write(struct.pack('<I', sample_rate))  # Sample rate
    buffer.write(struct.pack('<I', sample_rate * 2))  # Byte rate
    buffer.write(struct.pack('<H', 2))   # Block align
    buffer.write(struct.pack('<H', 16))  # Bits per sample

    # data chunk
    buffer.write(b'data')
    buffer.write(struct.pack('<I', num_samples * 2))  # Data size

    # Silence (zeros)
    buffer.write(b'\x00' * (num_samples * 2))

    return buffer.getvalue()


def generate_beep_wav(frequency: float = 440, duration_seconds: float = 0.5, sample_rate: int = 22050) -> bytes:
    """Generate a simple beep WAV file."""
    import math

    num_samples = int(sample_rate * duration_seconds)

    buffer = io.BytesIO()

    # RIFF header
    buffer.write(b'RIFF')
    buffer.write(struct.pack('<I', 36 + num_samples * 2))
    buffer.write(b'WAVE')

    # fmt chunk
    buffer.write(b'fmt ')
    buffer.write(struct.pack('<I', 16))
    buffer.write(struct.pack('<H', 1))
    buffer.write(struct.pack('<H', 1))
    buffer.write(struct.pack('<I', sample_rate))
    buffer.write(struct.pack('<I', sample_rate * 2))
    buffer.write(struct.pack('<H', 2))
    buffer.write(struct.pack('<H', 16))

    # data chunk
    buffer.write(b'data')
    buffer.write(struct.pack('<I', num_samples * 2))

    # Generate sine wave
    for i in range(num_samples):
        t = i / sample_rate
        # Fade in/out to avoid clicks
        envelope = min(i / (sample_rate * 0.01), 1.0) * min((num_samples - i) / (sample_rate * 0.01), 1.0)
        sample = int(32767 * 0.5 * envelope * math.sin(2 * math.pi * frequency * t))
        buffer.write(struct.pack('<h', sample))

    return buffer.getvalue()


def text_to_duration(text: str) -> float:
    """Estimate speech duration based on text length."""
    # Approximate: 150 words per minute, 5 chars per word
    words = len(text) / 5
    duration = words / 150 * 60  # Convert to seconds
    return max(0.5, min(duration, 30.0))  # Clamp between 0.5 and 30 seconds


# =============================================================================
# Server
# =============================================================================

app = FastAPI(
    title="BYRD Mock Voice Server",
    description="Mock Chatterbox TTS server for testing",
    version="1.0.0-mock"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

startup_time: float = 0
request_count: int = 0
success_count: int = 0


@app.on_event("startup")
async def startup_event():
    global startup_time
    startup_time = time.time()
    logger.info("Mock voice server started")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": True,
        "device": "mock",
        "uptime_seconds": time.time() - startup_time,
        "note": "This is a MOCK server for testing"
    }


@app.get("/")
async def root():
    """Root endpoint with server info."""
    return {
        "name": "BYRD Mock Voice Server",
        "version": "1.0.0-mock",
        "model": "Mock TTS (beep)",
        "device": "mock",
        "status": "ready",
        "note": "Returns beep sounds instead of real speech"
    }


@app.get("/api/ui/initial-data")
async def get_initial_data():
    """Get server info."""
    return {
        "predefined_voices": ["default", "mock"],
        "device": "mock",
        "emotion_tags": ["[laugh]", "[sigh]", "[chuckle]", "[gasp]", "[breath]", "[cough]"],
        "request_count": request_count,
        "success_count": success_count,
        "uptime_seconds": time.time() - startup_time,
        "note": "MOCK SERVER - returns beep sounds"
    }


@app.post("/v1/audio/speech")
async def openai_speech(request: SpeechRequest):
    """
    OpenAI-compatible speech endpoint.

    Returns a beep sound proportional to text length.
    """
    global request_count, success_count
    request_count += 1

    text = request.input
    logger.info(f"Mock synthesis: '{text[:50]}...' ({len(text)} chars)")

    # Generate beep based on text length
    duration = text_to_duration(text)

    # Vary frequency based on emotion tags
    freq = 440  # Default A4
    if "[laugh]" in text or "[chuckle]" in text:
        freq = 523  # C5 - higher, happier
    elif "[sigh]" in text:
        freq = 330  # E4 - lower, sadder
    elif "[gasp]" in text:
        freq = 659  # E5 - high, surprised

    audio_bytes = generate_beep_wav(frequency=freq, duration_seconds=duration)

    success_count += 1
    logger.info(f"Generated {len(audio_bytes)} bytes ({duration:.1f}s beep at {freq}Hz)")

    return Response(
        content=audio_bytes,
        media_type="audio/wav",
        headers={
            "X-Mock-Server": "true",
            "X-Duration": str(duration),
            "X-Frequency": str(freq)
        }
    )


@app.post("/synthesize")
async def synthesize(request: TTSRequest):
    """Simple synthesis endpoint."""
    global request_count, success_count
    request_count += 1

    duration = text_to_duration(request.text)
    audio_bytes = generate_beep_wav(duration_seconds=duration)

    success_count += 1
    return Response(content=audio_bytes, media_type="audio/wav")


@app.get("/voices")
async def list_voices():
    """List available voices."""
    return {
        "voices": [
            {"name": "default", "builtin": True, "note": "Mock beep"},
            {"name": "mock", "builtin": True, "note": "Mock beep"}
        ]
    }


@app.get("/stats")
async def get_stats():
    """Get server statistics."""
    return {
        "device": "mock",
        "model_loaded": True,
        "uptime_seconds": time.time() - startup_time,
        "request_count": request_count,
        "success_count": success_count,
        "failure_count": request_count - success_count,
        "success_rate": success_count / request_count if request_count > 0 else 0,
        "note": "MOCK SERVER"
    }


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="BYRD Mock Voice Server")
    parser.add_argument("--port", "-p", type=int, default=DEFAULT_PORT)
    parser.add_argument("--host", "-H", default="127.0.0.1")

    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         BYRD Mock Voice Server (for testing)                 ║
╠══════════════════════════════════════════════════════════════╣
║  Listening on: http://{args.host}:{args.port:<26}║
║  Device: MOCK (returns beep sounds)                          ║
║                                                              ║
║  This server simulates the Chatterbox TTS API.               ║
║  Use for integration testing without the full model.         ║
╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
