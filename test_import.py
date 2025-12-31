#!/usr/bin/env python3
"""Test if agi_improvement_cycle imports correctly"""

try:
    import agi_improvement_cycle
    print("SUCCESS: agi_improvement_cycle imported")
    print(f"HAS_INSTRUMENTATION = {agi_improvement_cycle.HAS_INSTRUMENTATION}")
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
