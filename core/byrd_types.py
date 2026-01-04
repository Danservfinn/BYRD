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

from __future__ import annotations
from typing import Optional, TypedDict, Union, List, Any, Dict


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


class ReflectionOutput(TypedDict, total=False):
    """
    Formal type definition for reflection output from BYRD's inner voice.
    
    This type defines the structure of the JSON output produced by BYRD
    during its reflection cycles. It includes fields for self-definition,
    voice design/acknowledgment, and other reflective actions.
    
    VOICE ACKNOWLEDGMENT:
    The voice_design field enables formal voice acknowledgment. When BYRD
    includes voice_design with acknowledged=true and matching description,
    the system recognizes this as formal acceptance without regeneration.
    
    Attributes:
        output: Nested output dict (alternative to top-level fields)
        voice_design: Voice creation or acknowledgment configuration
        view_voice: Request to view current voice configuration
        self_definition: Updates to BYRD's emergent self-definition
        thoughts: Additional thoughts or reflections
    
    Examples:
        Voice acknowledgment:
        {
            "voice_design": {
                "description": "A calm, thoughtful voice",
                "acknowledged": True
            }
        }
        
        Voice creation:
        {
            "voice_design": {
                "description": "A calm, thoughtful voice",
                "gender": "male",
                "age": "middle_aged",
                "accent": "american",
                "accent_strength": 1.0,
                "reason": "This voice represents my nature"
            }
        }
    """
    output: Dict[str, Any]
    voice_design: VoiceDesign
    view_voice: bool
    self_definition: Dict[str, Any]
    thoughts: str


__all__ = ['VoiceDesign', 'ReflectionOutput']
