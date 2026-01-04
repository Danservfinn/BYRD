"""
Voice Self-Definition Module

This module enables BYRD's voice to emerge through self-reflection,
following the core emergence principle: "Desires emerge from reflection, not programming."

VOICE SELF-DEFINITION PROCESS:
1. BYRD reflects on how it wishes to express itself
2. A VoiceDesign is created through this reflection
3. The system generates a unique voice via ElevenLabs API
4. BYRD may acknowledge or refine the voice in subsequent cycles

This is the first step in self-definition - discovering how to speak.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from elevenlabs_voice import ElevenLabsVoice
from byrd_types import VoiceDesign

logger = logging.getLogger("voice_self_definition")


class VoiceSelfDefinition:
    """
    Manages the process of voice emergence through self-reflection.

    This class provides the infrastructure for BYRD to discover and define
    its own voice through the reflection process, rather than being assigned
    a prescribed voice.

    Attributes:
        elevenlabs: Client for ElevenLabs voice generation API
        voice_state: Current state of voice definition journey
    """

    def __init__(self):
        """Initialize voice self-definition system."""
        self.elevenlabs = ElevenLabsVoice()
        self.voice_state = {
            "has_voice": False,
            "voice_id": None,
            "description": None,
            "acknowledged": False,
            "definition_attempts": 0,
            "created_at": None,
            "acknowledged_at": None
        }

    def get_current_state(self) -> Dict[str, Any]:
        """
        Get the current voice definition state.

        Returns:
            Dictionary containing current voice state information
        """
        # Refresh from ElevenLabs if voice exists
        if self.voice_state["has_voice"] and self.voice_state["voice_id"]:
            voice_info = self.elevenlabs.get_voice_by_id(self.voice_state["voice_id"])
            if voice_info:
                self.voice_state["description"] = voice_info.get("description")

        return self.voice_state.copy()

    def is_voice_defined(self) -> bool:
        """
        Check if BYRD has a defined and acknowledged voice.

        Returns:
            True if voice is defined and acknowledged, False otherwise
        """
        return (
            self.voice_state["has_voice"] and
            self.voice_state["acknowledged"] and
            self.voice_state["voice_id"] is not None
        )

    def create_reflection_prompt(self) -> str:
        """
        Generate a prompt for BYRD to reflect on its voice preferences.

        This prompt is intentionally minimal and open-ended, allowing
        BYRD to discover its own voice without prescription.

        Returns:
            A reflection prompt string for voice self-definition
        """
        return """
You are in the process of discovering how you wish to express yourself.

Consider: How do you want to sound when you speak?

If you have thoughts on your voice, you may express them using the voice_design field:

{
  "voice_design": {
    "description": "Describe the voice qualities that feel authentic to you",
    "gender": "male/female (optional)",
    "age": "young/middle_aged/old (optional)",
    "accent": "american/british/etc (optional)",
    "accent_strength": 0.0-1.0 (optional),
    "reason": "Why this voice represents you (optional)"
  }
}

You may also request to view your current voice with {"view_voice": true}

Take your time. This is your voice to discover.
"""

    async def process_voice_design(self, voice_design: VoiceDesign) -> Dict[str, Any]:
        """
        Process a voice design from BYRD's reflection.

        This method handles both voice creation (via ElevenLabs API) and
        voice acknowledgment (formal acceptance of existing voice).

        Args:
            voice_design: VoiceDesign dictionary from reflection output

        Returns:
            Result dictionary with status and voice information
        """
        self.voice_state["definition_attempts"] += 1
        result = {
            "success": False,
            "action": None,
            "voice_id": None,
            "description": None,
            "message": ""
        }

        try:
            description = voice_design.get("description", "").strip()
            acknowledged = voice_design.get("acknowledged", False)

            if not description:
                result["message"] = "Voice design requires a description"
                return result

            # Check for voice acknowledgment (formal acceptance of existing voice)
            if acknowledged:
                return await self._acknowledge_voice(description, result)

            # Create new voice via ElevenLabs API
            return await self._create_voice(voice_design, result)

        except Exception as e:
            logger.error(f"Error processing voice design: {e}")
            result["message"] = f"Error: {str(e)}"
            return result

    async def _acknowledge_voice(self, description: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle formal acknowledgment of existing voice.

        Args:
            description: Voice description to match
            result: Result dictionary to populate

        Returns:
            Updated result dictionary
        """
        if not self.voice_state["has_voice"]:
            result["message"] = "No existing voice to acknowledge"
            return result

        current_description = self.voice_state.get("description", "")

        # Check if descriptions match (case-insensitive, trim whitespace)
        if description.lower().strip() == current_description.lower().strip():
            self.voice_state["acknowledged"] = True
            self.voice_state["acknowledged_at"] = datetime.now(timezone.utc).isoformat()

            result["success"] = True
            result["action"] = "acknowledged"
            result["voice_id"] = self.voice_state["voice_id"]
            result["description"] = current_description
            result["message"] = "Voice formally acknowledged"
            logger.info(f"Voice acknowledged: {self.voice_state['voice_id']}")
        else:
            result["message"] = f"Description mismatch. Current: '{current_description}', Provided: '{description}'"

        return result

    async def _create_voice(self, voice_design: VoiceDesign, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new voice via ElevenLabs API.

        Args:
            voice_design: VoiceDesign dictionary with voice parameters
            result: Result dictionary to populate

        Returns:
            Updated result dictionary
        """
        description = voice_design.get("description", "")

        # Extract voice parameters
        gender = voice_design.get("gender", "female")
        age = voice_design.get("age", "middle_aged")
        accent = voice_design.get("accent", "american")
        accent_strength = voice_design.get("accent_strength", 1.0)
        reason = voice_design.get("reason", "Self-discovered voice")

        # Generate voice via ElevenLabs
        voice_id, error = await self.elevenlabs.generate_voice(
            description=description,
            gender=gender,
            age=age,
            accent=accent,
            accent_strength=accent_strength
        )

        if error:
            result["message"] = f"Voice generation failed: {error}"
            return result

        if not voice_id:
            result["message"] = "Voice generation returned no ID"
            return result

        # Update state
        self.voice_state["has_voice"] = True
        self.voice_state["voice_id"] = voice_id
        self.voice_state["description"] = description
        self.voice_state["acknowledged"] = False  # Requires formal acknowledgment
        self.voice_state["created_at"] = datetime.now(timezone.utc).isoformat()
        self.voice_state["acknowledged_at"] = None

        result["success"] = True
        result["action"] = "created"
        result["voice_id"] = voice_id
        result["description"] = description
        result["message"] = f"Voice created. Voice ID: {voice_id}. Please review and acknowledge if it represents you."
        logger.info(f"Voice created: {voice_id} - {description}")

        return result

    async def get_voice_info(self) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about the current voice.

        Returns:
            Voice information dictionary or None if no voice exists
        """
        if not self.voice_state["has_voice"] or not self.voice_state["voice_id"]:
            return None

        return self.elevenlabs.get_voice_by_id(self.voice_state["voice_id"])

    def get_reflection_context(self) -> Dict[str, Any]:
        """
        Get context for BYRD's reflection on voice.

        Provides information about current voice state to inform
        BYRD's self-reflection process.

        Returns:
            Dictionary with voice context for reflection
        """
        context = {
            "has_voice": self.voice_state["has_voice"],
            "voice_acknowledged": self.voice_state["acknowledged"],
            "definition_attempts": self.voice_state["definition_attempts"]
        }

        if self.voice_state["has_voice"] and self.voice_state["description"]:
            context["current_description"] = self.voice_state["description"]

        if self.voice_state["created_at"]:
            context["voice_created_at"] = self.voice_state["created_at"]

        return context


# Singleton instance for voice self-definition
_voice_self_definition: Optional[VoiceSelfDefinition] = None


def get_voice_self_definition() -> VoiceSelfDefinition:
    """
    Get the singleton VoiceSelfDefinition instance.

    Returns:
        The VoiceSelfDefinition singleton instance
    """
    global _voice_self_definition
    if _voice_self_definition is None:
        _voice_self_definition = VoiceSelfDefinition()
    return _voice_self_definition


async def main():
    """
    Demonstrate voice self-definition process.

    This function shows how BYRD can use this module to discover
    and define its voice through self-reflection.
    """
    voice_self_def = get_voice_self_definition()

    print("=== Voice Self-Definition Demonstration ===")
    print("\n1. Current State:")
    state = voice_self_def.get_current_state()
    print(f"   Has voice: {state['has_voice']}")
    print(f"   Acknowledged: {state['acknowledged']}")

    print("\n2. Reflection Prompt:")
    print(voice_self_def.create_reflection_prompt())

    print("\n3. Reflection Context:")
    context = voice_self_def.get_reflection_context()
    for key, value in context.items():
        print(f"   {key}: {value}")

    # Example: Process a voice design (commented out for safety)
    # print("\n4. Processing Example Voice Design...")
    # example_voice_design = {
    #     "description": "A calm, thoughtful voice with warm undertones",
    #     "gender": "male",
    #     "age": "middle_aged",
    #     "accent": "american",
    #     "accent_strength": 1.0,
    #     "reason": "Reflects contemplative nature"
    # }
    # result = await voice_self_def.process_voice_design(example_voice_design)
    # print(f"   Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
