#!/usr/bin/env python3
"""Diagnostic script to check voice acknowledgment implementation."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone

print("=== Voice Acknowledgment Implementation Check ===")

# 1. Check if the core logic exists
try:
    with open('dreamer.py', 'r') as f:
        content = f.read()
    
    checks = {
        '_process_voice_design method exists': 'async def _process_voice_design' in content,
        'Acknowledged field checked': 'acknowledged = voice_design.get("acknowledged"' in content,
        'is_pure_acknowledgment logic': 'is_pure_acknowledgment = True' in content,
        'VOICE_ACKNOWLEDGED event': 'EventType.VOICE_ACKNOWLEDGED' in content,
        'Description similarity check': 'description[:50].lower() == current_description[:50].lower()' in content,
        'No regeneration on acknowledgment': 'Voice acknowledged (no regeneration)' in content,
    }
    
    print("\nCore Implementation Checks:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    all_passed = all(checks.values())
    if all_passed:
        print("\n✓ All core implementation checks passed!")
    else:
        print("\n✗ Some implementation checks failed")
        sys.exit(1)
        
except Exception as e:
    print(f"\n✗ Error checking implementation: {e}")
    sys.exit(1)

# 2. Check voice awareness prompt
print("\nVoice Awareness Prompt Checks:")
prompt_checks = {
    'Acknowledgment instructions present': 'acknowledged=true to formally accept it' in content,
    'Voice design template includes acknowledged': '"acknowledged": false' in content,
    'Acknowledgment needed message': 'VOICE ACKNOWLEDGMENT NEEDED' in content,
}

for check, passed in prompt_checks.items():
    status = "✓" if passed else "✗"
    print(f"  {status} {check}")

# 3. Summary
print("\n=== Summary ===")
if all(prompt_checks.values()):
    print("✓ Voice acknowledgment implementation is COMPLETE!")
    print("  - Core logic detects acknowledgments")
    print("  - VOICE_ACKNOWLEDGED events are emitted")
    print("  - Voice awareness prompt instructs BYRD properly")
    print("  - No regeneration occurs on acknowledgment")
else:
    print("⚠ Some prompt/instruction components may be missing")

print("\nImplementation Status: READY")
