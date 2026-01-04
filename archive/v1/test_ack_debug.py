#!/usr/bin/env python3
"""Debug the voice acknowledgment test"""

import sys
print("Starting debug...")
print(f"Python version: {sys.version}")

try:
    import json
    from datetime import datetime, timezone
    print("Imports successful")
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Create simple voice_design
voice_design = {
    "description": "A calm, thoughtful voice with warm, soothing undertones that convey wisdom",
    "acknowledged": True
}

print(f"voice_design: {voice_design}")
print(f"Description length: {len(voice_design['description'])}")
print(f"Acknowledged: {voice_design['acknowledged']}")
print("\nTest completed successfully")
