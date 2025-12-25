#!/usr/bin/env python3
"""
Operating System Node Verification Script

Manual verification of the OS node implementation.
Run with: python tests/verify_os_node.py

Requires:
- Neo4j running (docker-compose up -d)
- BYRD not running (to avoid conflicts)
"""

import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml

# ANSI colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")


def failure(msg):
    print(f"{RED}✗ {msg}{RESET}")


def info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")


def warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")


def header(msg):
    print(f"\n{BOLD}{msg}{RESET}")
    print("=" * len(msg))


def expand_env_vars(config_str: str) -> str:
    """Expand environment variables like ${VAR:-default}."""
    import re
    def expand(match):
        var_expr = match.group(1)
        if ":-" in var_expr:
            var_name, default = var_expr.split(":-", 1)
        else:
            var_name, default = var_expr, ""
        return os.environ.get(var_name, default)
    return re.sub(r'\$\{([^}]+)\}', expand, config_str)


async def run_verification():
    """Run all verification checks."""

    # Load config with env var expansion
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
    with open(config_path) as f:
        config_str = f.read()
    expanded = expand_env_vars(config_str)
    config = yaml.safe_load(expanded)

    header("1. MEMORY CONNECTION")

    try:
        from memory import Memory
        memory = Memory(config.get("memory", {}))
        await memory.connect()
        success("Connected to Neo4j")
    except Exception as e:
        failure(f"Failed to connect to Neo4j: {e}")
        return

    header("2. TEMPLATE MANAGEMENT")

    try:
        # Ensure templates exist
        await memory.ensure_os_templates()
        success("Templates ensured")

        # Get black-cat template
        black_cat = await memory.get_os_template("black-cat")
        if black_cat:
            success(f"Retrieved black-cat template: {black_cat.get('name', 'unknown')}")
            info(f"  Archetype: {black_cat.get('archetype', 'unknown')}")
            info(f"  Seeds: {len(black_cat.get('seeds', []))}")
        else:
            failure("Could not retrieve black-cat template")

        # Get emergent template
        emergent = await memory.get_os_template("emergent")
        if emergent:
            success(f"Retrieved emergent template: {emergent.get('name', 'unknown')}")
        else:
            failure("Could not retrieve emergent template")

    except Exception as e:
        failure(f"Template management failed: {e}")
        import traceback
        traceback.print_exc()

    header("3. OPERATING SYSTEM LIFECYCLE")

    try:
        # Check if OS exists
        has_os = await memory.has_operating_system()
        info(f"OS exists: {has_os}")

        if has_os:
            # Get existing OS
            os_node = await memory.get_operating_system()
            if os_node:
                success(f"Retrieved OS: {os_node.get('name', 'unknown')} v{os_node.get('version', 0)}")
                info(f"  Archetype: {os_node.get('archetype', 'unknown')}")
                info(f"  Template: {os_node.get('template_id', 'unknown')}")
                info(f"  Current Focus: {os_node.get('current_focus')}")
                info(f"  Emotional Tone: {os_node.get('emotional_tone')}")
        else:
            # Create OS from template
            info("Creating OS from black-cat template...")
            await memory.create_os_from_template("black-cat")
            success("OS created from template")

            os_node = await memory.get_operating_system()
            if os_node:
                success(f"Verified OS: {os_node.get('name', 'unknown')} v{os_node.get('version', 0)}")

    except Exception as e:
        failure(f"OS lifecycle test failed: {e}")
        import traceback
        traceback.print_exc()

    header("4. OS UPDATES")

    try:
        # Update freely mutable field
        await memory.update_operating_system(
            updates={"set_field": {"current_focus": "verification testing"}},
            source="test"
        )
        success("Updated current_focus (freely mutable)")

        # Verify update
        os_node = await memory.get_operating_system()
        if os_node and os_node.get("current_focus") == "verification testing":
            success("Verified current_focus update")
        else:
            failure("current_focus not updated correctly")

        # Update with custom field
        await memory.update_operating_system(
            updates={"set_field": {"test_metric": 42}},
            source="test"
        )
        success("Added custom field test_metric")

        # Verify custom field
        os_node = await memory.get_operating_system()
        if os_node and os_node.get("test_metric") == 42:
            success("Verified custom field")
        else:
            warning("Custom field may not have persisted correctly")

    except Exception as e:
        failure(f"OS update test failed: {e}")
        import traceback
        traceback.print_exc()

    header("5. VERSION HISTORY")

    try:
        history = await memory.get_os_version_history(limit=5)
        success(f"Retrieved version history: {len(history)} versions")
        for v in history[:3]:
            info(f"  Version {v.get('version', '?')}: {v.get('modification_source', 'unknown')}")

    except Exception as e:
        failure(f"Version history test failed: {e}")
        import traceback
        traceback.print_exc()

    header("6. OS FOR PROMPT")

    try:
        prompt_text = await memory.get_os_for_prompt()
        if prompt_text:
            success(f"Generated prompt text ({len(prompt_text)} chars)")
            # Show first 200 chars
            preview = prompt_text[:200].replace('\n', ' ')
            info(f"  Preview: {preview}...")
        else:
            warning("No prompt text generated (OS may not exist)")

    except Exception as e:
        failure(f"Prompt generation failed: {e}")
        import traceback
        traceback.print_exc()

    header("7. VOICE RETRIEVAL")

    try:
        voice = await memory.get_os_voice()
        if voice:
            success(f"Retrieved voice ({len(voice)} chars)")
            preview = voice[:100].replace('\n', ' ')
            info(f"  Preview: {preview}...")
        else:
            info("No voice set (may be intentional for emergent template)")

    except Exception as e:
        failure(f"Voice retrieval failed: {e}")

    header("8. RESET TO TEMPLATE")

    try:
        # Note: This will reset the OS - uncomment to test
        # await memory.reset_to_template("black-cat")
        # success("Reset to black-cat template")

        info("Reset test skipped (uncomment to run)")
        info("To test: await memory.reset_to_template('black-cat')")

    except Exception as e:
        failure(f"Reset test failed: {e}")

    header("9. CLEANUP")

    try:
        # Remove test metric
        await memory.update_operating_system(
            updates={"deprecate_field": "test_metric"},
            source="test_cleanup"
        )
        success("Cleaned up test_metric field")

        # Reset current_focus
        await memory.update_operating_system(
            updates={"set_field": {"current_focus": None}},
            source="test_cleanup"
        )
        success("Reset current_focus to null")

    except Exception as e:
        warning(f"Cleanup encountered issue: {e}")

    header("10. DIRECT NEO4J QUERIES")

    try:
        async with memory.driver.session() as session:
            # Count OS nodes
            result = await session.run("MATCH (os:OperatingSystem) RETURN count(os) as count")
            record = await result.single()
            count = record["count"] if record else 0
            info(f"OperatingSystem nodes: {count}")

            # Count templates
            result = await session.run("MATCH (t:OSTemplate) RETURN count(t) as count")
            record = await result.single()
            count = record["count"] if record else 0
            info(f"OSTemplate nodes: {count}")

            # Count seeds
            result = await session.run("MATCH (s:Seed) RETURN count(s) as count")
            record = await result.single()
            count = record["count"] if record else 0
            info(f"Seed nodes: {count}")

            # Count constraints
            result = await session.run("MATCH (c:Constraint) RETURN count(c) as count")
            record = await result.single()
            count = record["count"] if record else 0
            info(f"Constraint nodes: {count}")

            success("Direct Neo4j queries completed")

    except Exception as e:
        failure(f"Direct queries failed: {e}")

    header("VERIFICATION COMPLETE")
    print()


if __name__ == "__main__":
    print(f"\n{BOLD}Operating System Node Verification{RESET}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        asyncio.run(run_verification())
    except KeyboardInterrupt:
        print("\nVerification interrupted")
    except Exception as e:
        print(f"\n{RED}Fatal error: {e}{RESET}")
        import traceback
        traceback.print_exc()
