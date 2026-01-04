#!/usr/bin/env python3
"""Run genesis and capture all output"""

import io
import sys
from contextlib import redirect_stdout, redirect_stderr
import asyncio

# Capture all output
output = io.StringIO()
error_output = io.StringIO()

with redirect_stdout(output), redirect_stderr(error_output):
    try:
        from genesis_reflect_constraint import genesis_create_zai_constraint
        result = asyncio.run(genesis_create_zai_constraint())
    except Exception as e:
        print(f"EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        result = None

# Now print everything
print("=== STDOUT ===")
stdout_text = output.getvalue()
print(stdout_text if stdout_text else "(empty)")

print("\n=== STDERR ===")
stderr_text = error_output.getvalue()
print(stderr_text if stderr_text else "(empty)")

print(f"\n=== RESULT ===")
print(f"Function returned: {result}")

sys.exit(0 if result else 1)
