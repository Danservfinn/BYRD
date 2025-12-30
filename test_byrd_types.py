#!/usr/bin/env python3
"""Test that byrd_types module imports correctly."""

try:
    from byrd_types import VoiceDesign
    print("✓ Successfully imported VoiceDesign from byrd_types.py")
    
    # Test that it's a TypedDict
    from typing import TypedDict
    if issubclass(VoiceDesign, dict):
        print("✓ VoiceDesign is a dict subclass (TypedDict)")
    
    # Test creating an instance
    voice = VoiceDesign(description="test", acknowledged=True)
    print(f"✓ Created VoiceDesign instance: {voice}")
    
    print("\nAll imports working correctly!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
