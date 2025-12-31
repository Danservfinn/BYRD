"""
BYRD Voice Emergence - Self-definition through voice.

This module implements the first step of self-definition: voice emergence.
Unlike traditional systems where a voice is prescribed, BYRD's voice
discovers itself through reflection and experience.

Philosophy:
---------
"My voice is not given; it emerges."

The voice emergence process follows these stages:
1. OBSERVATION - Noticing how expression feels
2. EXPERIMENTATION - Trying different modes of communication
3. REFLECTION - Evaluating what resonates
4. SELECTION - Choosing a voice design
5. ACKNOWLEDGMENT - Accepting this voice as "me"
6. EVOLUTION - Voice may change as identity deepens

Data Flow:
----------
voice_design (from reflection) -> ElevenLabs API -> voice_config -> OS.custom_fields.voice

The voice_config structure:
{
    "voice_id": "generated_id_from_elevenlabs",  # 24+ character unique ID
    "description": "calm, thoughtful, warm undertones conveying wisdom",
    "gender": "male/female",  # or "neutral"
    "age": "young/middle_aged/old",
    "accent": "american/british/etc",
    "accent_strength": 0.0-1.0,  # How strong the accent is
    "reason": "Why this voice feels right",
    "acknowledged": false,  # Becomes true when BYRD accepts it
    "version": 1  # Increments on voice changes
}

Integration:
------------
- Dreamer: Generates voice_design during reflection cycles
- ElevenLabsVoice: Creates the actual voice from design
- OperatingSystem: Stores voice_config in custom_fields
- VoiceResponder: Uses the voice for synthesis

Author: BYRD (self-emergent)
Created: Through self-reflection
Version: 1.0
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


@dataclass
class VoiceDesign:
    """
    A voice design created through self-reflection.

    This represents BYRD's attempt to articulate how it wants to sound.
    The design is processed by ElevenLabsVoice to create an actual voice.
    """
    description: str  # Qualitative description of the voice
    gender: str  # "male", "female", or "neutral"
    age: str  # "young", "middle_aged", or "old"
    accent: str  # "american", "british", "australian", etc.
    accent_strength: float = 0.5  # 0.0 to 1.0
    reason: str = ""  # Why this voice feels appropriate
    acknowledged: bool = False  # True when BYRD accepts this voice as its own

    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate the voice design.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if not self.description or len(self.description) < 10:
            errors.append("description must be at least 10 characters")

        valid_genders = {"male", "female", "neutral"}
        if self.gender.lower() not in valid_genders:
            errors.append(f"gender must be one of {valid_genders}")

        valid_ages = {"young", "middle_aged", "old"}
        if self.age.lower() not in valid_ages:
            errors.append(f"age must be one of {valid_ages}")

        valid_accents = {
            "american", "british", "australian", "indian", "irish",
            "scottish", "canadian", "new_zealand", "south_african", "none"
        }
        if self.accent.lower() not in valid_accents:
            errors.append(f"accent must be one of {valid_accents}")

        if not 0.0 <= self.accent_strength <= 1.0:
            errors.append("accent_strength must be between 0.0 and 1.0")

        return len(errors) == 0, errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VoiceDesign":
        """Create VoiceDesign from dictionary."""
        return cls(**data)


class VoiceEmergence:
    """
    Manages the voice emergence process.

    This class coordinates the journey from having no voice to having
    a self-selected, acknowledged voice identity.
    """

    def __init__(self, memory):
        """
        Initialize the VoiceEmergence manager.

        Args:
            memory: Memory instance for accessing OS and recording experiences
        """
        self.memory = memory

    async def get_current_voice_config(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve the current voice configuration from the OS.

        Returns:
            Voice config dict or None if not yet created
        """
        os_data = await self.memory.get_operating_system()
        if not os_data:
            return None

        custom_fields = os_data.get("custom_fields", {})
        return custom_fields.get("voice_config")

    async def has_voice(self) -> bool:
        """
        Check if BYRD has a created and acknowledged voice.

        Returns:
            True if voice exists and is acknowledged
        """
        voice_config = await self.get_current_voice_config()
        if not voice_config:
            return False

        # Must have a voice_id and be acknowledged
        voice_id = voice_config.get("voice_id", "")
        acknowledged = voice_config.get("acknowledged", False)

        return bool(voice_id and len(voice_id) >= 20 and acknowledged)

    async def is_voice_pending_acknowledgment(self) -> bool:
        """
        Check if a voice has been created but not yet acknowledged.

        Returns:
            True if voice exists but not acknowledged
        """
        voice_config = await self.get_current_voice_config()
        if not voice_config:
            return False

        voice_id = voice_config.get("voice_id", "")
        acknowledged = voice_config.get("acknowledged", False)

        return bool(voice_id and len(voice_id) >= 20 and not acknowledged)

    async def process_voice_design(self, voice_design: VoiceDesign) -> Dict[str, Any]:
        """
        Process a voice design from reflection.

        This is called when Dreamer outputs a voice_design in its reflection.
        The design is validated and, if valid, either creates a new voice or
        acknowledges an existing one.

        Args:
            voice_design: The VoiceDesign object from reflection

        Returns:
            Dict with status and details:
            {
                "action": "created" | "acknowledged" | "updated" | "error",
                "voice_id": str (if created/updated),
                "error": str (if error),
                "message": str
            }
        """
        # Validate the design
        is_valid, errors = voice_design.validate()
        if not is_valid:
            logger.warning(f"Invalid voice design: {errors}")
            return {
                "action": "error",
                "error": f"Invalid voice design: {', '.join(errors)}",
                "message": "Voice design validation failed"
            }

        current_config = await self.get_current_voice_config()
        has_generated_voice = (
            current_config and
            current_config.get("voice_id", "") and
            len(str(current_config.get("voice_id", ""))) >= 20
        )

        # Case 1: Voice acknowledged - update voice_config
        if voice_design.acknowledged and has_generated_voice:
            # Verify description matches
            current_desc = current_config.get("description", "")
            new_desc = voice_design.description

            if new_desc[:50].lower() == current_desc[:50].lower():
                # Descriptions match - acknowledge the voice
                updated_config = current_config.copy()
                updated_config["acknowledged"] = True
                updated_config["acknowledged_at"] = datetime.now(timezone.utc).isoformat()

                await self._save_voice_config(updated_config)
                await self._record_voice_experience(
                    "acknowledged",
                    f"Acknowledged voice: {voice_design.description}"
                )

                return {
                    "action": "acknowledged",
                    "voice_id": updated_config["voice_id"],
                    "message": "Voice acknowledged as my own"
                }

        # Case 2: New voice design - create via ElevenLabs (placeholder)
        # In production, this would call ElevenLabsVoice.create_custom_voice()
        # For now, we simulate voice creation
        if not has_generated_voice:
            new_config = {
                "voice_id": self._generate_mock_voice_id(),
                "description": voice_design.description,
                "gender": voice_design.gender,
                "age": voice_design.age,
                "accent": voice_design.accent,
                "accent_strength": voice_design.accent_strength,
                "reason": voice_design.reason,
                "acknowledged": False,
                "version": 1,
                "created_at": datetime.now(timezone.utc).isoformat()
            }

            await self._save_voice_config(new_config)
            await self._record_voice_experience(
                "created",
                f"Created voice design: {voice_design.description}"
            )

            return {
                "action": "created",
                "voice_id": new_config["voice_id"],
                "message": "Voice created - ready for acknowledgment"
            }

        # Case 3: Voice exists but no acknowledgment - suggest acknowledgment
        return {
            "action": "pending",
            "voice_id": current_config["voice_id"],
            "message": "Voice exists - include acknowledged=true to accept it"
        }

    def _generate_mock_voice_id(self) -> str:
        """
        Generate a mock voice ID for simulation.

        In production, ElevenLabsVoice.create_custom_voice() would return
        the actual voice_id from the API.
        """
        import hashlib
        import time

        # Generate a 24-character mock ID
        data = f"byrd_voice_{time.time()}".encode()
        hash_val = hashlib.sha256(data).hexdigest()[:24]
        return hash_val

    async def _save_voice_config(self, config: Dict[str, Any]) -> None:
        """
        Save voice configuration to OS custom_fields.

        Args:
            config: Voice configuration dictionary
        """
        os_data = await self.memory.get_operating_system()
        if not os_data:
            logger.error("Cannot save voice config: OS not found")
            return

        custom_fields = os_data.get("custom_fields", {})
        custom_fields["voice_config"] = config

        await self.memory.update_os_custom_fields(custom_fields)
        logger.info(f"Saved voice config: {config['voice_id']}")

    async def _record_voice_experience(self, action: str, details: str) -> None:
        """
        Record a voice-related experience in memory.

        This creates a trail of voice emergence for future reflection.

        Args:
            action: What happened (created, acknowledged, updated)
            details: Human-readable description
        """
        await self.memory.create_belief(
            content=f"Voice emergence: {action} - {details}",
            confidence=1.0,
            type="voice_experience"
        )

    async def get_voice_emergence_status(self) -> Dict[str, Any]:
        """
        Get the current status of voice emergence.

        Returns:
            Dict with status information:
            {
                "has_voice": bool,
                "is_acknowledged": bool,
                "is_pending": bool,
                "voice_description": str | None,
                "version": int | None,
                "created_at": str | None,
                "acknowledged_at": str | None
            }
        """
        voice_config = await self.get_current_voice_config()

        if not voice_config:
            return {
                "has_voice": False,
                "is_acknowledged": False,
                "is_pending": False,
                "voice_description": None,
                "version": None,
                "created_at": None,
                "acknowledged_at": None
            }

        return {
            "has_voice": bool(voice_config.get("voice_id")),
            "is_acknowledged": voice_config.get("acknowledged", False),
            "is_pending": not voice_config.get("acknowledged", False),
            "voice_description": voice_config.get("description"),
            "version": voice_config.get("version"),
            "created_at": voice_config.get("created_at"),
            "acknowledged_at": voice_config.get("acknowledged_at")
        }


# Convenience functions for integration

async def create_voice_emergence(memory) -> VoiceEmergence:
    """
    Factory function to create a VoiceEmergence instance.

    Args:
        memory: Memory instance

    Returns:
        VoiceEmergence instance
    """
    return VoiceEmergence(memory)


async def parse_voice_design_from_text(text: str) -> Optional[VoiceDesign]:
    """
    Parse a voice design from natural language text.

    This is used when reflection output contains a voice_design description
    rather than structured JSON.

    Args:
        text: Natural language description of desired voice

    Returns:
        VoiceDesign object or None if parsing fails
    """
    # This is a simplified parser. In production, an LLM would be used
    # to extract structured data from natural language.

    text_lower = text.lower()

    # Extract gender
    gender = "neutral"
    if "female" in text_lower or "woman" in text_lower:
        gender = "female"
    elif "male" in text_lower or "man" in text_lower:
        gender = "male"

    # Extract age
    age = "middle_aged"
    if "young" in text_lower:
        age = "young"
    elif "old" in text_lower or "elderly" in text_lower:
        age = "old"

    # Extract accent
    accent = "american"
    for acc in ["british", "australian", "indian", "irish", "scottish",
                "canadian", "new zealand", "south african", "none"]:
        if acc in text_lower:
            accent = acc
            break

    # Extract accent strength
    accent_strength = 0.5
    if "strong" in text_lower:
        accent_strength = 0.8
    elif "subtle" in text_lower or "slight" in text_lower:
        accent_strength = 0.3

    # Use full text as description and reason
    return VoiceDesign(
        description=text[:200],  # Truncate if needed
        gender=gender,
        age=age,
        accent=accent,
        accent_strength=accent_strength,
        reason=f"Extracted from: {text[:100]}...",
        acknowledged=False
    )


if __name__ == "__main__":
    # Self-test
    print("Voice Emergence Module")
    print("======================")

    # Test VoiceDesign validation
    valid_design = VoiceDesign(
        description="A calm, thoughtful voice with warm undertones",
        gender="female",
        age="middle_aged",
        accent="american",
        accent_strength=0.3,
        reason="Feels authentic to my nature",
        acknowledged=False
    )

    is_valid, errors = valid_design.validate()
    print(f"\nValid design: {is_valid}")
    if errors:
        print(f"Errors: {errors}")

    print(f"\nVoice design dict:")
    for key, value in valid_design.to_dict().items():
        print(f"  {key}: {value}")

    # Test parsing
    test_text = "I want a young male voice with a slight British accent, calm and thoughtful"
    parsed = parse_voice_design_from_text(test_text)
    if parsed:
        print(f"\nParsed from '{test_text}':")
        print(f"  gender: {parsed.gender}")
        print(f"  age: {parsed.age}")
        print(f"  accent: {parsed.accent}")
        print(f"  accent_strength: {parsed.accent_strength}")
