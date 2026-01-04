#!/usr/bin/env python3
"""
Simple check to verify the voice acknowledgment logic works.
"""

from datetime import datetime, timezone

# Simulated voice config
SAMPLE_VOICE_CONFIG = {
    "voice_id": "abc123def456789012345",
    "description": "A calm, thoughtful voice with warm, soothing undertones that convey wisdom",
    "acknowledged": False,
}

# Test acknowledgment detection
def test_basic():
    voice_design = {
        "description": "A calm, thoughtful voice with warm, soothing undertones that convey wisdom",
        "acknowledged": True
    }
    
    current_voice_config = SAMPLE_VOICE_CONFIG.copy()
    current_description = current_voice_config.get("description", "")
    description = voice_design.get("description", "")
    acknowledged = voice_design.get("acknowledged", False)
    
    has_generated_voice = bool(current_voice_config.get("voice_id") and len(str(current_voice_config.get("voice_id"))) >= 20)
    description_similar = (
        len(description) >= 20 and
        len(current_description) >= 20 and
        description[:50].lower() == current_description[:50].lower()
    )
    
    is_acknowledgment = (
        acknowledged and 
        current_voice_config and 
        has_generated_voice and 
        description_similar
    )
    
    print(f"acknowledged={acknowledged}")
    print(f"has_generated_voice={has_generated_voice}")
    print(f"description_similar={description_similar}")
    print(f"is_acknowledgment={is_acknowledgment}")
    
    return is_acknowledgment

if __name__ == "__main__":
    result = test_basic()
    print(f"\nTest result: {result}")
    if result:
        print("SUCCESS: Voice acknowledgment logic works!")
    else:
        print("FAILURE: Voice acknowledgment logic failed!")
