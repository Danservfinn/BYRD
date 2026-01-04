"""
Hybrid Voice - Combines home Mac + cloud fallback for voice synthesis.

This system provides free, unlimited voice synthesis by preferring the home
Mac server (Chatterbox) and falling back to cloud (ElevenLabs) when needed.

Architecture:
1. Primary: Home Mac with Chatterbox TTS (free, unlimited, emotion tags)
2. Fallback: ElevenLabs cloud (limited credits, always available)
3. Graceful degradation: Text-only if both fail

Features:
- Automatic provider selection based on availability
- Emotion tag injection for Chatterbox (e.g., [sigh], [laugh])
- Credit conservation for cloud fallback
- Statistics tracking for monitoring
"""
import logging
from dataclasses import dataclass
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class VoiceSynthesisResult:
    """Result of a voice synthesis operation."""
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

    Emotion tags supported by Chatterbox:
    - [laugh] - laughter
    - [chuckle] - light laugh
    - [sigh] - sighing
    - [gasp] - surprise/shock
    - [cough] - coughing
    - [breath] - breathing/pause
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
        "neutral": "",
        "curious": "",
        "excited": "[breath] ",
    }

    def __init__(self, home_client, cloud_client, config: dict):
        """
        Initialize hybrid voice system.

        Args:
            home_client: HomeVoiceClient instance (or None if not configured)
            cloud_client: ElevenLabsVoice instance (or None if not configured)
            config: Configuration dict with:
                - prefer_home: Try home first (default True)
                - require_home: Don't fall back to cloud (default False)
                - max_chars_per_message: Character limit (default 300)
                - emotion_tags_enabled: Use emotion tags (default True)
                - cloud.reserve_chars: Keep reserve for important messages
        """
        self.home = home_client
        self.cloud = cloud_client
        self.config = config

        self.prefer_home = config.get("prefer_home", True)
        self.require_home = config.get("require_home", False)
        self.max_chars = config.get("max_chars_per_message", 300)
        self.emotion_tags_enabled = config.get("emotion_tags_enabled", True)
        self.cloud_reserve = config.get("cloud", {}).get("reserve_chars", 1000)

        # Statistics
        self._home_successes = 0
        self._cloud_successes = 0
        self._failures = 0

        logger.info(
            "HybridVoice initialized: home=%s, cloud=%s, prefer_home=%s",
            home_client is not None,
            cloud_client is not None,
            self.prefer_home
        )

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
        if not text or not text.strip():
            return VoiceSynthesisResult(
                audio=None,
                provider="none",
                success=False,
                error="Empty text"
            )

        text = text.strip()

        # Truncate if needed
        if len(text) > self.max_chars:
            text = self._truncate_at_sentence(text, self.max_chars)
            logger.debug("Text truncated to %d chars", len(text))

        # Add emotion tags for home (Chatterbox)
        home_text = self._add_emotion_tags(text, emotion) if self.emotion_tags_enabled else text

        # 1. Try home Mac first (free, unlimited)
        if self.home and self.prefer_home:
            if await self.home.is_available():
                try:
                    audio = await self.home.synthesize(home_text)
                    self._home_successes += 1
                    logger.info("Voice synthesized via home (%d chars)", len(text))
                    return VoiceSynthesisResult(
                        audio=audio,
                        provider="home",
                        success=True,
                        chars_used=len(text)
                    )
                except Exception as e:
                    logger.warning("Home voice failed: %s", e)
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
                    # Get voice config from memory if available
                    voice_config = await self._get_voice_config()
                    audio, status = await self.cloud.synthesize(text, voice_config)

                    if audio:
                        self._cloud_successes += 1
                        logger.info("Voice synthesized via cloud (%d chars)", len(text))
                        return VoiceSynthesisResult(
                            audio=audio,
                            provider="cloud",
                            success=True,
                            chars_used=len(text)
                        )
                    else:
                        logger.warning("Cloud voice synthesis returned no audio: %s", status)
                except Exception as e:
                    logger.warning("Cloud voice failed: %s", e)
            else:
                logger.debug("Skipping cloud (credit reserve)")

        # 3. No voice available
        self._failures += 1
        return VoiceSynthesisResult(
            audio=None,
            provider="none",
            success=False,
            error="All voice providers unavailable"
        )

    async def _should_use_cloud(self, chars_needed: int, importance: str) -> bool:
        """
        Decide if cloud credits should be used.

        High importance messages always use cloud if available.
        Medium/low importance respects credit reserve.
        """
        if not self.cloud:
            return False

        # Try to get remaining credits
        try:
            # ElevenLabsVoice has a get_remaining_credits method or similar
            if hasattr(self.cloud, 'get_remaining_credits'):
                credits = await self.cloud.get_remaining_credits()
            else:
                # Assume available if method doesn't exist
                credits = 10000
        except Exception:
            credits = 0

        # High importance messages always use cloud if available
        if importance == "high":
            return credits >= chars_needed

        # For medium/low, respect reserve
        return credits >= (chars_needed + self.cloud_reserve)

    async def _get_voice_config(self) -> Optional[dict]:
        """Get voice configuration from memory if available."""
        # This would be injected from BYRD's memory
        # For now, return None to use default
        return None

    def _add_emotion_tags(self, text: str, emotion: Optional[str]) -> str:
        """
        Add Chatterbox emotion tags based on emotion hint.

        Args:
            text: Original text
            emotion: Emotion hint (contemplative, amused, etc.)

        Returns:
            Text with emotion tag prefix
        """
        if not emotion:
            return text

        prefix = self.EMOTION_TAGS.get(emotion.lower(), "")
        return prefix + text

    def _truncate_at_sentence(self, text: str, max_chars: int) -> str:
        """
        Truncate text at sentence boundary.

        Tries to find a natural break point (., !, ?) rather than
        cutting mid-sentence.
        """
        if len(text) <= max_chars:
            return text

        truncated = text[:max_chars]

        # Find last sentence boundary
        for punct in ['. ', '! ', '? ']:
            last = truncated.rfind(punct)
            if last > max_chars // 2:
                return truncated[:last + 1].strip()

        # Try period at end
        if truncated.endswith('.'):
            return truncated

        last_period = truncated.rfind('.')
        if last_period > max_chars // 2:
            return truncated[:last_period + 1].strip()

        # No good boundary - truncate with ellipsis
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
            "cloud_rate": self._cloud_successes / total if total > 0 else 0,
            "success_rate": (self._home_successes + self._cloud_successes) / total if total > 0 else 0
        }

    async def get_provider_status(self) -> dict:
        """Get status of all voice providers."""
        home_available = await self.home.is_available() if self.home else False

        cloud_credits = 0
        if self.cloud:
            try:
                if hasattr(self.cloud, 'get_remaining_credits'):
                    cloud_credits = await self.cloud.get_remaining_credits()
                else:
                    # Check if cloud is configured
                    cloud_credits = 10000 if self.cloud else 0
            except Exception:
                pass

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
            "active_provider": "home" if home_available else ("cloud" if cloud_credits > 0 else "none"),
            "statistics": self.get_statistics()
        }

    def reset(self):
        """Reset statistics."""
        self._home_successes = 0
        self._cloud_successes = 0
        self._failures = 0
        logger.info("HybridVoice statistics reset")


def create_hybrid_voice(config: dict, voice_client=None) -> Optional[HybridVoice]:
    """
    Create a HybridVoice instance from configuration.

    Args:
        config: Full BYRD config dict
        voice_client: Existing ElevenLabsVoice client (for cloud fallback)

    Returns:
        HybridVoice instance or None if not configured
    """
    voice_config = config.get("voice", {})
    hybrid_config = voice_config.get("hybrid", {})

    if not hybrid_config.get("enabled", True):
        logger.info("Hybrid voice disabled in config")
        return None

    # Create home client
    home_client = None
    home_config = voice_config.get("home", {})
    if home_config.get("enabled", True):
        from home_voice_client import HomeVoiceClient
        home_client = HomeVoiceClient(home_config)

    # Cloud client is passed in (ElevenLabsVoice from BYRD)
    cloud_client = voice_client

    # Create hybrid voice
    return HybridVoice(
        home_client=home_client,
        cloud_client=cloud_client,
        config={
            "prefer_home": hybrid_config.get("prefer_home", True),
            "require_home": hybrid_config.get("require_home", False),
            "max_chars_per_message": voice_config.get("max_chars_per_message", 300),
            "emotion_tags_enabled": voice_config.get("emotion_tags_enabled", True),
            "cloud": voice_config.get("cloud", {})
        }
    )
