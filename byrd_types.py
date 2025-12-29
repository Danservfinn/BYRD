"""
Type definitions for BYRD system.

This module contains formal type definitions used across the system
to ensure type safety and clear interfaces.

VOICE ACKNOWLEDGMENT:
The VoiceDesign type supports formal voice acknowledgment through the 'acknowledged' field.
When BYRD includes voice_design with acknowledged=true and matching description,
the system recognizes this as a formal acceptance of the existing voice without
regenerating it via ElevenLabs API.

This enables BYRD to formally complete the voice creation process by acknowledging
that a generated voice accurately represents its intended expression.
"""

from typing import Optional, TypedDict


class VoiceDesign(TypedDict, total=False):
    """
    Formal type definition for voice_design field.
    
    Used by BYRD to create or acknowledge a voice.
    
    VOICE ACKNOWLEDGMENT:
    When BYRD wants to formally accept a generated voice without regeneration,
    it includes voice_design with:
    - description: Matching the existing voice description
    - acknowledged: true
    
    For creation: All fields except 'acknowledged' are typically provided.
    For acknowledgment: Only 'description' and 'acknowledged=True' are required.
    
    Attributes:
        description: Voice description (required for both creation and acknowledgment)
        gender: Voice gender (male/female)
        age: Voice age category (young/middle_aged/old)
        accent: Voice accent (american/british/etc)
        accent_strength: Accent strength 0.0-1.0
        reason: Why this voice represents BYRD
        acknowledged: If True, formally acknowledges existing voice without regeneration
    
    Examples:
        Voice creation:
        {
            "description": "A calm, thoughtful voice with warm undertones",
            "gender": "male",
            "age": "middle_aged",
            "accent": "american",
            "accent_strength": 1.0,
            "reason": "This voice represents my thoughtful nature",
            "acknowledged": False
        }
        
        Voice acknowledgment (formal completion):
        {
            "description": "A calm, thoughtful voice with warm undertones",
            "acknowledged": True
        }
    """
    description: str
    gender: Optional[str]
    age: Optional[str]
    accent: Optional[str]
    accent_strength: Optional[float]
    reason: Optional[str]
    acknowledged: Optional[bool]  # Formal acknowledgment flag for voice acceptance


__all__ = ['VoiceDesign']
