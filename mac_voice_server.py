#!/usr/bin/env python3
"""
Mac Chatterbox TTS Server

A local TTS server for BYRD that runs on your Mac, providing free unlimited
voice synthesis with emotion tag support. Designed to be exposed via
Cloudflare Tunnel for remote access.

Features:
- OpenAI-compatible /v1/audio/speech endpoint
- Emotion tags: [laugh], [sigh], [chuckle], [gasp], [breath], [cough]
- Apple Silicon (MPS) acceleration
- Voice cloning from reference audio
- Health monitoring

Setup:
    pip install chatterbox-tts fastapi uvicorn python-multipart

Run:
    python mac_voice_server.py

Cloudflare Tunnel:
    cloudflared tunnel --url http://localhost:5050

Usage from BYRD:
    Set HOME_VOICE_URL environment variable to your tunnel URL
"""

import argparse
import asyncio
import io
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

import torch
import torchaudio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mac_voice_server")

# FastAPI imports
try:
    from fastapi import FastAPI, HTTPException, UploadFile, File, Form
    from fastapi.responses import Response, JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    logger.error("FastAPI not installed. Run: pip install fastapi uvicorn python-multipart")
    sys.exit(1)

# Chatterbox TTS import
try:
    from chatterbox.tts import ChatterboxTTS
except ImportError:
    logger.error("Chatterbox TTS not installed. Run: pip install chatterbox-tts")
    sys.exit(1)


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_PORT = 5050
MODEL_CACHE_DIR = Path.home() / ".cache" / "chatterbox"
VOICE_REF_DIR = Path.home() / ".byrd" / "voices"


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
# Server
# =============================================================================

app = FastAPI(
    title="BYRD Home Voice Server",
    description="Chatterbox TTS server for BYRD voice synthesis",
    version="1.0.0"
)

# CORS for tunnel access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
model: Optional[ChatterboxTTS] = None
model_device: str = "cpu"
voice_references: dict = {}  # Cache of loaded voice references
startup_time: float = 0
request_count: int = 0
success_count: int = 0


def get_device() -> str:
    """Determine the best available device."""
    if torch.backends.mps.is_available():
        return "mps"  # Apple Silicon
    elif torch.cuda.is_available():
        return "cuda"
    return "cpu"


def load_model():
    """Load the Chatterbox TTS model."""
    global model, model_device

    model_device = get_device()
    logger.info(f"Loading Chatterbox TTS on {model_device}...")

    try:
        model = ChatterboxTTS.from_pretrained(device=model_device)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


def load_voice_reference(voice_name: str) -> Optional[tuple]:
    """
    Load a voice reference audio file.

    Args:
        voice_name: Name of the voice (looks for {voice_name}.wav in VOICE_REF_DIR)

    Returns:
        Tuple of (audio_tensor, sample_rate) or None
    """
    global voice_references

    if voice_name in voice_references:
        return voice_references[voice_name]

    # Look for voice file
    VOICE_REF_DIR.mkdir(parents=True, exist_ok=True)

    for ext in [".wav", ".mp3", ".flac", ".ogg"]:
        voice_path = VOICE_REF_DIR / f"{voice_name}{ext}"
        if voice_path.exists():
            try:
                audio, sr = torchaudio.load(str(voice_path))
                voice_references[voice_name] = (audio, sr)
                logger.info(f"Loaded voice reference: {voice_name}")
                return (audio, sr)
            except Exception as e:
                logger.error(f"Failed to load voice {voice_name}: {e}")

    return None


def audio_to_bytes(audio_tensor: torch.Tensor, sample_rate: int, format: str = "mp3") -> bytes:
    """Convert audio tensor to bytes in specified format."""
    buffer = io.BytesIO()

    # Ensure correct shape (channels, samples)
    if audio_tensor.dim() == 1:
        audio_tensor = audio_tensor.unsqueeze(0)

    # Move to CPU if needed
    audio_tensor = audio_tensor.cpu()

    if format == "wav":
        torchaudio.save(buffer, audio_tensor, sample_rate, format="wav")
    else:
        # MP3 requires additional backend
        try:
            torchaudio.save(buffer, audio_tensor, sample_rate, format="mp3")
        except Exception:
            # Fallback to WAV if MP3 encoding fails
            logger.warning("MP3 encoding failed, using WAV")
            buffer = io.BytesIO()
            torchaudio.save(buffer, audio_tensor, sample_rate, format="wav")

    buffer.seek(0)
    return buffer.read()


# =============================================================================
# Endpoints
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    global startup_time
    startup_time = time.time()

    # Load model in background to not block startup
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, load_model)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy" if model is not None else "loading",
        "model_loaded": model is not None,
        "device": model_device,
        "uptime_seconds": time.time() - startup_time if startup_time > 0 else 0
    }


@app.get("/")
async def root():
    """Root endpoint with server info."""
    return {
        "name": "BYRD Home Voice Server",
        "version": "1.0.0",
        "model": "Chatterbox TTS",
        "device": model_device,
        "status": "ready" if model is not None else "loading"
    }


@app.get("/api/ui/initial-data")
async def get_initial_data():
    """Get server info (used by home_voice_client for status)."""
    # List available voice references
    voices = ["default"]
    if VOICE_REF_DIR.exists():
        for f in VOICE_REF_DIR.iterdir():
            if f.suffix in [".wav", ".mp3", ".flac", ".ogg"]:
                voices.append(f.stem)

    return {
        "predefined_voices": voices,
        "device": model_device,
        "emotion_tags": ["[laugh]", "[sigh]", "[chuckle]", "[gasp]", "[breath]", "[cough]"],
        "request_count": request_count,
        "success_count": success_count,
        "uptime_seconds": time.time() - startup_time if startup_time > 0 else 0
    }


@app.post("/v1/audio/speech")
async def openai_speech(request: SpeechRequest):
    """
    OpenAI-compatible speech endpoint.

    This is the primary endpoint used by BYRD's home_voice_client.

    Args:
        request: SpeechRequest with input text, voice, and format

    Returns:
        Audio bytes in requested format
    """
    global request_count, success_count

    if model is None:
        raise HTTPException(status_code=503, detail="Model still loading")

    request_count += 1

    try:
        text = request.input
        voice = request.voice
        format = request.response_format

        logger.info(f"Synthesizing: '{text[:50]}...' (voice={voice}, format={format})")

        # Load voice reference if specified
        voice_ref = None
        # Get voice reference path if specified
        voice_ref_path = None
        if voice and voice != "default":
            # Look for voice reference file
            voice_path = VOICE_REF_DIR / f"{voice}.wav"
            if voice_path.exists():
                voice_ref_path = str(voice_path)
                logger.info(f"Using voice reference: {voice_ref_path}")

        # Generate speech
        # Chatterbox supports emotion tags directly in the text
        audio = model.generate(
            text=text,
            audio_prompt_path=voice_ref_path,  # Path to reference audio or None for default
            exaggeration=0.5,  # Emotion intensity
            cfg_weight=0.5    # Classifier-free guidance
        )

        # Get sample rate from model
        sample_rate = model.sr

        # Convert to bytes
        audio_bytes = audio_to_bytes(audio, sample_rate, format)

        success_count += 1
        logger.info(f"Generated {len(audio_bytes)} bytes of audio")

        media_type = "audio/mpeg" if format == "mp3" else "audio/wav"
        return Response(content=audio_bytes, media_type=media_type)

    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/synthesize")
async def synthesize(request: TTSRequest):
    """
    Simple synthesis endpoint.

    Alternative to OpenAI-compatible endpoint with more control.
    """
    global request_count, success_count

    if model is None:
        raise HTTPException(status_code=503, detail="Model still loading")

    request_count += 1

    try:
        # Get voice reference path if specified
        voice_ref_path = None
        if request.voice_ref:
            voice_path = VOICE_REF_DIR / f"{request.voice_ref}.wav"
            if voice_path.exists():
                voice_ref_path = str(voice_path)

        # Generate speech
        audio = model.generate(
            text=request.text,
            audio_prompt_path=voice_ref_path,
            exaggeration=request.exaggeration,
            cfg_weight=request.cfg_weight
        )

        # Convert to MP3
        audio_bytes = audio_to_bytes(audio, model.sr, "mp3")

        success_count += 1
        return Response(content=audio_bytes, media_type="audio/mpeg")

    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-voice")
async def upload_voice(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload a voice reference audio file.

    Args:
        name: Name for this voice
        file: Audio file (WAV, MP3, FLAC, OGG)

    Returns:
        Success message
    """
    VOICE_REF_DIR.mkdir(parents=True, exist_ok=True)

    # Validate file type
    allowed_extensions = [".wav", ".mp3", ".flac", ".ogg"]
    ext = Path(file.filename).suffix.lower() if file.filename else ".wav"
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {allowed_extensions}"
        )

    # Save file
    voice_path = VOICE_REF_DIR / f"{name}{ext}"
    try:
        content = await file.read()
        voice_path.write_bytes(content)

        # Clear cache to reload
        if name in voice_references:
            del voice_references[name]

        logger.info(f"Saved voice reference: {name} ({len(content)} bytes)")
        return {"success": True, "name": name, "path": str(voice_path)}

    except Exception as e:
        logger.error(f"Failed to save voice: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/voices")
async def list_voices():
    """List available voice references."""
    voices = [{"name": "default", "builtin": True}]

    if VOICE_REF_DIR.exists():
        for f in VOICE_REF_DIR.iterdir():
            if f.suffix in [".wav", ".mp3", ".flac", ".ogg"]:
                voices.append({
                    "name": f.stem,
                    "path": str(f),
                    "size_bytes": f.stat().st_size,
                    "builtin": False
                })

    return {"voices": voices}


@app.get("/stats")
async def get_stats():
    """Get server statistics."""
    return {
        "device": model_device,
        "model_loaded": model is not None,
        "uptime_seconds": time.time() - startup_time if startup_time > 0 else 0,
        "request_count": request_count,
        "success_count": success_count,
        "failure_count": request_count - success_count,
        "success_rate": success_count / request_count if request_count > 0 else 0,
        "voice_cache_size": len(voice_references)
    }


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="BYRD Home Voice Server - Chatterbox TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mac_voice_server.py                    # Run on default port 5050
  python mac_voice_server.py --port 8080        # Run on port 8080
  python mac_voice_server.py --host 0.0.0.0     # Listen on all interfaces

Cloudflare Tunnel:
  cloudflared tunnel --url http://localhost:5050

Voice References:
  Place .wav/.mp3 files in ~/.byrd/voices/ to use custom voices.
  Example: ~/.byrd/voices/byrd.wav

Emotion Tags:
  Include tags in text for expressive speech:
  - [laugh]   Laughter
  - [sigh]    Sighing
  - [chuckle] Light laugh
  - [gasp]    Surprise
  - [breath]  Breathing/pause
  - [cough]   Coughing
        """
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=int(os.environ.get("PORT", DEFAULT_PORT)),
        help=f"Port to listen on (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--host", "-H",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )

    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           BYRD Home Voice Server - Chatterbox TTS            ║
╠══════════════════════════════════════════════════════════════╣
║  Listening on: http://{args.host}:{args.port:<26}║
║  Device: {get_device():<50}║
║  Voice refs: ~/.byrd/voices/                                 ║
╠══════════════════════════════════════════════════════════════╣
║  Cloudflare Tunnel:                                          ║
║    cloudflared tunnel --url http://localhost:{args.port:<15}║
╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "mac_voice_server:app" if args.reload else app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
