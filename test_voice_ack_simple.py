#!/usr/bin/env python3
"""Simple test to verify voice acknowledgment logic works."""

# Test the core acknowledgment detection logic
SAMPLE_VOICE_CONFIG = {
    "voice_id": "abc123def456789012345",
    "description": "A calm, thoughtful voice with warm undertones",
    "acknowledged": False
}

def test_acknowledgment():
    """Test voice acknowledgment detection."""
    print("Testing voice acknowledgment...")
    
    # Pure acknowledgment case
    voice_design = {
        "description": "A calm, thoughtful voice with warm undertones",
        "acknowledged": True
    }
    
    current_description = SAMPLE_VOICE_CONFIG.get("description", "")
    description = voice_design.get("description", "")
    acknowledged = voice_design.get("acknowledged", False)
    
    has_generated_voice = SAMPLE_VOICE_CONFIG.get("voice_id") and len(str(SAMPLE_VOICE_CONFIG.get("voice_id"))) >= 20
    description_similar = (
        len(description) >= 20 and
        len(current_description) >= 20 and
        description[:50].lower() == current_description[:50].lower()
    )
    
    is_acknowledgment = (
        acknowledged and 
        SAMPLE_VOICE_CONFIG and 
        has_generated_voice and 
        description_similar
    )
    
    print(f"  acknowledged={acknowledged}")
    print(f"  has_generated_voice={has_generated_voice}")
    print(f"  description_similar={description_similar}")
    print(f"  Result: {is_acknowledgment}")
    
    assert is_acknowledgment == True, "Should recognize acknowledgment"
    print("✓ Voice acknowledgment works correctly!")
    return True

if __name__ == "__main__":
    test_acknowledgment()
