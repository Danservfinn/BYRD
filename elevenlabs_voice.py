"""
ElevenLabs Text-to-Speech integration for BYRD.

Provides voice synthesis with credit tracking for the free tier (10k chars/month).
BYRD self-emergently selects its voice during the first dream cycle.
"""

import httpx
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, Any
import json


class ElevenLabsVoice:
    """ElevenLabs TTS client with credit tracking."""

    API_URL = "https://api.elevenlabs.io/v1"

    # Available voices on ElevenLabs free tier
    VOICES = {
        "rachel": {
            "id": "21m00Tcm4TlvDq8ikWAM",
            "gender": "female",
            "desc": "calm, warm, American",
            "style": "conversational"
        },
        "domi": {
            "id": "AZnzlk1XvdvUeBnXmlld",
            "gender": "female",
            "desc": "strong, confident, American",
            "style": "assertive"
        },
        "bella": {
            "id": "EXAVITQu4vr4xnSDxMaL",
            "gender": "female",
            "desc": "soft, gentle, American",
            "style": "soothing"
        },
        "antoni": {
            "id": "ErXwobaYiN019PkySvjV",
            "gender": "male",
            "desc": "expressive, well-rounded, American",
            "style": "dynamic"
        },
        "elli": {
            "id": "MF3mGyEYCl7XYWbV9V6O",
            "gender": "female",
            "desc": "young, bright, American",
            "style": "energetic"
        },
        "josh": {
            "id": "TxGEqnHWrfWFTfGW9XjX",
            "gender": "male",
            "desc": "deep, narrative, American",
            "style": "contemplative"
        },
        "arnold": {
            "id": "VR6AewLTigWG4xSOukaG",
            "gender": "male",
            "desc": "crisp, authoritative, American",
            "style": "commanding"
        },
        "adam": {
            "id": "pNInz6obpgDQGcFmaJgB",
            "gender": "male",
            "desc": "deep, confident, American",
            "style": "grounded"
        },
        "sam": {
            "id": "yoZ06aMxZJJ28mfd3POQ",
            "gender": "male",
            "desc": "raspy, authentic, American",
            "style": "raw"
        },
    }

    MONTHLY_LIMIT = 10000  # Free tier character limit
    LOW_CREDIT_THRESHOLD = 1000  # Warn when below this

    def __init__(self, api_key: str, memory=None):
        """
        Initialize ElevenLabs voice client.

        Args:
            api_key: ElevenLabs API key
            memory: Memory instance for credit tracking in OS
        """
        self.api_key = api_key
        self.memory = memory
        self._credits_cache = None
        self._cache_time = None

    async def get_credits(self) -> Dict[str, Any]:
        """
        Get current credit status from OS.

        Returns:
            Credits dict with monthly_used, monthly_limit, exhausted, etc.
        """
        if not self.memory:
            return {
                "monthly_used": 0,
                "monthly_limit": self.MONTHLY_LIMIT,
                "exhausted": False,
                "period_start": datetime.now(timezone.utc).replace(day=1).isoformat()
            }

        os_data = await self.memory.get_operating_system()
        if not os_data:
            return self._default_credits()

        voice_config = os_data.get("voice_config", {})
        credits = voice_config.get("credits", {})

        if not credits:
            return self._default_credits()

        # Check if we need to reset (new month)
        period_start = credits.get("period_start")
        if period_start:
            try:
                if isinstance(period_start, str):
                    start_date = datetime.fromisoformat(period_start.replace('Z', '+00:00'))
                else:
                    start_date = period_start

                now = datetime.now(timezone.utc)
                if now.month != start_date.month or now.year != start_date.year:
                    # New month - reset credits
                    credits = self._default_credits()
                    await self._update_credits(credits)
                    print(f"🎤 Voice credits reset for new month")
            except Exception as e:
                print(f"Error checking credit period: {e}")

        return credits

    def _default_credits(self) -> Dict[str, Any]:
        """Get default credits structure."""
        return {
            "monthly_used": 0,
            "monthly_limit": self.MONTHLY_LIMIT,
            "period_start": datetime.now(timezone.utc).replace(day=1).isoformat(),
            "exhausted": False,
            "low_warning_sent": False
        }

    async def _update_credits(self, credits: Dict[str, Any]):
        """Update credit tracking in OS."""
        if not self.memory:
            return

        try:
            os_data = await self.memory.get_operating_system()
            if not os_data:
                return

            voice_config = os_data.get("voice_config", {})
            voice_config["credits"] = credits
            await self.memory.update_os_field("voice_config", voice_config)
        except Exception as e:
            print(f"Error updating voice credits: {e}")

    async def get_remaining_credits(self) -> int:
        """Get remaining character credits for this month."""
        credits = await self.get_credits()
        return credits.get("monthly_limit", self.MONTHLY_LIMIT) - credits.get("monthly_used", 0)

    async def synthesize(
        self,
        text: str,
        voice_config: Dict[str, Any]
    ) -> Tuple[Optional[bytes], str]:
        """
        Generate speech from text using ElevenLabs API.

        Args:
            text: Text to synthesize
            voice_config: Voice configuration with voice_id, stability, similarity_boost

        Returns:
            Tuple of (audio_bytes or None, status_message)
        """
        if not text or not text.strip():
            return None, "No text provided"

        text = text.strip()
        chars_needed = len(text)

        # Check credits
        credits = await self.get_credits()
        remaining = credits.get("monthly_limit", self.MONTHLY_LIMIT) - credits.get("monthly_used", 0)

        if credits.get("exhausted") or remaining < chars_needed:
            return None, f"Voice credits exhausted ({remaining} remaining, need {chars_needed})"

        # Get voice ID
        voice_name = voice_config.get("voice_id", "josh").lower()
        voice_info = self.VOICES.get(voice_name)
        if not voice_info:
            voice_info = self.VOICES["josh"]  # Default fallback
            voice_name = "josh"

        voice_id = voice_info["id"]

        # Voice settings
        stability = float(voice_config.get("stability", 0.5))
        similarity_boost = float(voice_config.get("similarity_boost", 0.75))

        # Clamp values to valid range
        stability = max(0.0, min(1.0, stability))
        similarity_boost = max(0.0, min(1.0, similarity_boost))

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.API_URL}/text-to-speech/{voice_id}",
                    headers={
                        "xi-api-key": self.api_key,
                        "Content-Type": "application/json",
                        "Accept": "audio/mpeg",
                    },
                    json={
                        "text": text,
                        "model_id": "eleven_turbo_v2_5",  # Updated: v1 models deprecated on free tier
                        "voice_settings": {
                            "stability": stability,
                            "similarity_boost": similarity_boost,
                        }
                    }
                )

                if response.status_code == 200:
                    audio_bytes = response.content

                    # Update credits
                    credits["monthly_used"] = credits.get("monthly_used", 0) + chars_needed
                    new_remaining = credits["monthly_limit"] - credits["monthly_used"]

                    if new_remaining <= 0:
                        credits["exhausted"] = True

                    await self._update_credits(credits)

                    return audio_bytes, f"OK ({new_remaining} chars remaining)"

                elif response.status_code == 401:
                    error_detail = response.text[:200] if response.text else "No details"
                    return None, f"Invalid API key (401): {error_detail}"

                elif response.status_code == 429:
                    return None, "Rate limited - try again later"

                else:
                    error_text = response.text[:200] if response.text else "Unknown error"
                    return None, f"ElevenLabs error {response.status_code}: {error_text}"

        except httpx.TimeoutException:
            return None, "Request timed out"
        except httpx.ConnectError:
            return None, "Could not connect to ElevenLabs"
        except Exception as e:
            return None, f"TTS error: {str(e)}"

    @classmethod
    def get_voice_list(cls) -> str:
        """Get formatted list of available voices for prompts."""
        lines = []
        for name, info in cls.VOICES.items():
            lines.append(f"  - {name}: {info['gender']}, {info['desc']}")
        return "\n".join(lines)

    @classmethod
    def get_voice_info(cls, voice_name: str) -> Optional[Dict[str, Any]]:
        """Get info about a specific voice."""
        return cls.VOICES.get(voice_name.lower())

    async def check_api_key(self) -> bool:
        """Verify the API key is valid by checking voices endpoint."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Use /voices endpoint instead of /user (doesn't require user_read permission)
                response = await client.get(
                    f"{self.API_URL}/voices",
                    headers={"xi-api-key": self.api_key}
                )
                return response.status_code == 200
        except Exception:
            return False
