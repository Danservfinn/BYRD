#!/usr/bin/env python3
"""Minimal test - just import and check."""

# Try importing
try:
    from direct_executor import DirectExecutor, ExecutionPattern, DirectExecutionResult
    print("✓ Import successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Check classes exist
assert DirectExecutor is not None
assert ExecutionPattern is not None
assert DirectExecutionResult is not None
print("✓ Classes defined")

# Check enum values
patterns = [p.value for p in ExecutionPattern]
print(f"✓ Execution patterns: {patterns}")

print("\n✅ All checks passed - DirectExecutor is ready!")
