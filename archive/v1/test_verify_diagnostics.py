#!/usr/bin/env python3
"""Diagnostic test to identify why verify_voice_acknowledgment.py fails."""

import sys
import json
from datetime import datetime, timezone

# Simulated voice config
SAMPLE_VOICE_CONFIG = {
    "voice_id": "abc123def456789012345",
    "description": "A calm, thoughtful voice with warm, soothing undertones that convey wisdom",
    "gender": "male",
    "age": "middle_aged",
    "accent": "american",
    "accent_strength": 1.0,
    "stability": 0.5,
    "similarity_boost": 0.75,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "reason": "Initial voice creation",
    "generation_status": "generated",
    "is_generated": True,
    "acknowledged": False,
    "version": 1,
    "credits": {
        "monthly_used": 0,
        "monthly_limit": 10000,
        "period_start": datetime.now(timezone.utc).replace(day=1).isoformat(),
        "exhausted": False,
        "low_warning_sent": False
    }
}

def test_acknowledgment_detection():
    """Test the acknowledgment detection logic."""
    print("\n=== Testing Voice Acknowledgment Detection ===\n")
    
    try:
        # Test 1: Pure acknowledgment
        print("Test 1: Pure acknowledgment with matching description")
        voice_design = {
            "description": "A calm, thoughtful voice with warm, soothing undertones that convey wisdom",
            "acknowledged": True
        }
        
        current_voice_config = SAMPLE_VOICE_CONFIG.copy()
        current_description = current_voice_config.get("description", "")
        description = voice_design.get("description", "")
        acknowledged = voice_design.get("acknowledged", False)
        
        print(f"  description len: {len(description)}")
        print(f"  current_description len: {len(current_description)}")
        
        has_generated_voice = current_voice_config.get("voice_id") and len(str(current_voice_config.get("voice_id"))) >= 20
        description_similar = (
            len(description) >= 20 and
            len(current_description) >= 20 and
            description[:50].lower() == current_description[:50].lower()
        )
        
        print(f"  acknowledged={acknowledged}")
        print(f"  has_generated_voice={has_generated_voice}")
        print(f"  description_similar={description_similar}")
        print(f"  desc[:50]={description[:50]!r}")
        print(f"  cur_desc[:50]={current_description[:50]!r}")
        
        is_acknowledgment = (
            acknowledged and 
            current_voice_config and 
            has_generated_voice and 
            description_similar
        )
        
        print(f"  Result: is_acknowledgment={is_acknowledgment}")
        
        if is_acknowledgment != True:
            print("  ✗ FAIL: Should recognize pure acknowledgment")
            return False
        print("  ✓ PASS\n")
        
        return True
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_acknowledgment_detection()
    if success:
        print("\n✓ Test passed")
        sys.exit(0)
    else:
        print("\n✗ Test failed")
        sys.exit(1)
