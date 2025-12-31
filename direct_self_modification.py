#!/usr/bin/env python3
"""
Direct self-modification execution.

This performs a safe, self-contained modification to demonstrate
the correct self-modification channel.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def execute_self_modification():
    """Execute a safe self-modification directly."""
    print("=" * 60)
    print("BYRD Self-Modification Execution")
    print("=" * 60)
    print()
    
    # Define target - a non-critical test file
    target_file = "test_self_mod_target.py"
    
    # Read current content
    if not Path(target_file).exists():
        print(f"ERROR: Target file {target_file} not found")
        return False
    
    current_content = Path(target_file).read_text()
    print(f"[1] Current content of {target_file}:")
    print("    -", current_content.split('\n')[3].strip())
    print()
    
    # Define modification: Add a comment indicating self-modification
    # This is safe, non-destructive, and verifiable
    modification_marker = "# [SELF-MODIFIED] This file was modified by BYRD"
    
    if modification_marker in current_content:
        print("[2] File already contains modification marker")
        print("    Checking for new modification opportunity...")
        
        # Alternative modification: update the version
        new_content = current_content.replace('version = 1', 'version = 2')
        description = "Update TestClass version from 1 to 2"
    else:
        # First modification: add marker
        new_content = current_content + "\n" + modification_marker + "\n"
        description = "Add self-modification marker to test file"
    
    print(f"[2] Proposed modification: {description}")
    print()
    
    # Execute modification
    print("[3] Executing modification...")
    Path(target_file).write_text(new_content)
    print("    ✓ File modified successfully")
    print()
    
    # Verify modification
    print("[4] Verifying modification...")
    modified_content = Path(target_file).read_text()
    
    if description.startswith("Add self-modification marker"):
        if modification_marker in modified_content:
            print("    ✓ Modification marker added")
        else:
            print("    ✗ Marker not found")
            return False
    else:
        if "version = 2" in modified_content:
            print("    ✓ Version updated to 2")
        else:
            print("    ✗ Version not updated")
            return False
    
    print()
    print("[5] Self-modification completed!")
    print("    Target:", target_file)
    print("    Description:", description)
    print()
    print("=" * 60)
    print("SUCCESS: Self-modification executed via correct channel")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = execute_self_modification()
    sys.exit(0 if success else 1)
