"""
Home Voice Client - Connects to Mac's Chatterbox TTS server remotely.

This client communicates with a local Chatterbox TTS server running on your
Mac at home, exposed via a reverse proxy. This provides free, unlimited
voice synthesis with emotion tag support.

Setup:
1. Install Chatterbox TTS Server on your Mac
2. Expose it via your preferred method (ngrok, tailscale, etc.)
3. Set HOME_VOICE_URL environment variable to your server URL

See PLAN_OBSERVER_MESSAGES.md for detailed setup instructions.
"""
import asyncio
import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


class HomeVoiceClient:
    """
    Client for home Mac Chatterbox TTS server.

    Communicates via secure remote connection.
    Supports emotion tags like [laugh], [sigh], [chuckle] for expressive speech.
    """

    def __init__(self, config: dict):
        """
        Initialize the home voice client.

        Args:
            config: Configuration dict with:
                - url: Server URL (or from HOME_VOICE_URL env var)
                - timeout_seconds: Request timeout (default 30)
                - health_check_interval: How often to check availability (default 60)
        """
        self.endpoint = config.get("url") or os.environ.get("HOME_VOICE_URL")
        self.timeout = config.get("timeout_seconds", 30)
        self.health_check_interval = config.get("health_check_interval", 60)

        self._available = False
        self._last_health_check = 0
        self._health_check_lock = asyncio.Lock()

        # Statistics
        self._request_count = 0
        self._success_count = 0
        self._failure_count = 0

        if self.endpoint:
            logger.info("HomeVoiceClient initialized: %s", self.endpoint)
        else:
            logger.warning("HomeVoiceClient: No HOME_VOICE_URL configured")

    async def is_available(self) -> bool:
        """
        Check if home voice server is reachable.

        Uses cached result if checked recently (within health_check_interval).

        Returns:
            True if server is reachable and healthy
        """
        if not self.endpoint:
            return False

        # Rate-limit health checks
        now = asyncio.get_event_loop().time()
        if now - self._last_health_check < self.health_check_interval:
            return self._available

        async with self._health_check_lock:
            # Double-check after acquiring lock
            now = asyncio.get_event_loop().time()
            if now - self._last_health_check < self.health_check_interval:
                return self._available

            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(f"{self.endpoint}/health")
                    self._available = response.status_code == 200
                    if self._available:
                        logger.debug("Home voice server is available")
                    else:
                        logger.debug("Home voice server returned %d", response.status_code)
            except Exception as e:
                self._available = False
                logger.debug("Home voice server not available: %s", e)

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
            text: Text to speak (can include emotion tags like [laugh], [sigh])
            voice_ref: Optional voice reference file/name
            format: Output format ("mp3" or "wav")

        Returns:
            Audio bytes

        Raises:
            ValueError: If HOME_VOICE_URL not configured
            Exception: If synthesis fails
        """
        if not self.endpoint:
            raise ValueError("HOME_VOICE_URL not configured")

        self._request_count += 1

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Use OpenAI-compatible endpoint (Chatterbox TTS Server supports this)
                response = await client.post(
                    f"{self.endpoint}/v1/audio/speech",
                    json={
                        "input": text,
                        "voice": voice_ref or "default",
                        "response_format": format
                    }
                )

                if response.status_code == 200:
                    self._success_count += 1
                    logger.debug("Home voice synthesis succeeded: %d bytes", len(response.content))
                    return response.content
                else:
                    self._failure_count += 1
                    raise Exception(
                        f"Home voice synthesis failed: {response.status_code} - {response.text}"
                    )

        except Exception as e:
            self._failure_count += 1
            logger.error("Home voice synthesis error: %s", e)
            raise

    async def get_status(self) -> dict:
        """
        Get detailed status from home server.

        Returns:
            Dict with availability, voices, device info
        """
        if not self.endpoint:
            return {"available": False, "reason": "not_configured"}

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Try to get server info
                response = await client.get(f"{self.endpoint}/api/ui/initial-data")
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "available": True,
                        "voices": data.get("predefined_voices", []),
                        "device": data.get("device", "unknown"),
                        "endpoint": self.endpoint
                    }

                # Fallback to health check
                response = await client.get(f"{self.endpoint}/health")
                return {
                    "available": response.status_code == 200,
                    "endpoint": self.endpoint,
                    "health_status": response.status_code
                }

        except Exception as e:
            return {
                "available": False,
                "reason": str(e),
                "endpoint": self.endpoint
            }

    def get_statistics(self) -> dict:
        """Get client statistics."""
        total = self._request_count
        return {
            "request_count": self._request_count,
            "success_count": self._success_count,
            "failure_count": self._failure_count,
            "success_rate": self._success_count / total if total > 0 else 0,
            "is_configured": self.endpoint is not None,
            "cached_availability": self._available
        }

    def reset(self):
        """Reset statistics and cached state."""
        self._request_count = 0
        self._success_count = 0
        self._failure_count = 0
        self._available = False
        self._last_health_check = 0
        logger.info("HomeVoiceClient reset")

    def invalidate_cache(self):
        """Force next is_available() to check server."""
        self._last_health_check = 0
