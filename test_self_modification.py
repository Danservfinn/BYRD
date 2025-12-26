"""
Test script to verify BYRD's self-modification capability is accessible.

This performs a safe, non-destructive test by:
1. Checking if the self-modification system is enabled
2. Verifying constitutional constraints are in place
3. Testing provenance tracing (without creating actual modifications)
4. Checking if the coder component is available

Run with: python test_self_modification.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


async def test_self_modification_capability():
    """Test whether self-modification capability is accessible."""

    results = {
        "config_enabled": False,
        "system_initialized": False,
        "constitutional_constraints_working": False,
        "protected_files_defined": False,
        "modifiable_files_defined": False,
        "coder_available": False,
        "coder_cli_found": False,
        "provenance_system_working": False,
        "memory_connected": False,
        "errors": []
    }

    print("=" * 60)
    print("BYRD Self-Modification Capability Test")
    print("=" * 60)
    print()

    # 1. Load configuration
    print("[1] Loading configuration...")
    try:
        import yaml
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)

        self_mod_config = config.get("self_modification", {})
        results["config_enabled"] = self_mod_config.get("enabled", False)
        print(f"    ✓ Config loaded: self_modification.enabled = {results['config_enabled']}")
    except Exception as e:
        results["errors"].append(f"Config load failed: {e}")
        print(f"    ✗ Config load failed: {e}")

    # 2. Test constitutional constraints
    print("\n[2] Testing constitutional constraints...")
    try:
        from constitutional import ConstitutionalConstraints

        # Check protected files
        protected = ConstitutionalConstraints.PROTECTED_FILES
        results["protected_files_defined"] = len(protected) > 0
        print(f"    ✓ Protected files defined: {protected}")

        # Check modifiable files
        modifiable = ConstitutionalConstraints.MODIFIABLE_FILES
        results["modifiable_files_defined"] = len(modifiable) > 0
        print(f"    ✓ Modifiable files defined: {list(modifiable)[:5]}...")

        # Test constraint validation
        is_protected = ConstitutionalConstraints.is_protected("provenance.py")
        is_modifiable = ConstitutionalConstraints.is_modifiable("dreamer.py")
        results["constitutional_constraints_working"] = is_protected and is_modifiable
        print(f"    ✓ provenance.py protected: {is_protected}")
        print(f"    ✓ dreamer.py modifiable: {is_modifiable}")

    except Exception as e:
        results["errors"].append(f"Constitutional constraints failed: {e}")
        print(f"    ✗ Constitutional constraints failed: {e}")

    # 3. Initialize memory
    print("\n[3] Initializing memory connection...")
    try:
        from memory import Memory

        memory = Memory(config.get("memory", {}))
        await memory.connect()
        results["memory_connected"] = True
        print("    ✓ Memory connected to Neo4j")

    except Exception as e:
        results["errors"].append(f"Memory connection failed: {e}")
        print(f"    ✗ Memory connection failed: {e}")
        memory = None

    # 4. Initialize self-modification system
    print("\n[4] Initializing self-modification system...")
    try:
        from self_modification import SelfModificationSystem

        self_mod = SelfModificationSystem(
            memory=memory,
            config=self_mod_config,
            project_root=str(Path(__file__).parent)
        )
        results["system_initialized"] = True
        print(f"    ✓ SelfModificationSystem initialized")
        print(f"    ✓ Enabled: {self_mod.enabled}")
        print(f"    ✓ Max per day: {self_mod.max_per_day}")
        print(f"    ✓ Require health check: {self_mod.require_health_check}")
        print(f"    ✓ Auto rollback: {self_mod.auto_rollback}")

    except Exception as e:
        results["errors"].append(f"Self-modification system failed: {e}")
        print(f"    ✗ Self-modification system failed: {e}")

    # 5. Test provenance tracer
    print("\n[5] Testing provenance system...")
    try:
        from provenance import ProvenanceTracer

        if memory and results["memory_connected"]:
            tracer = ProvenanceTracer(memory)
            results["provenance_system_working"] = True
            print("    ✓ ProvenanceTracer initialized")

            # Test hash computation (no DB interaction)
            test_hash = tracer.compute_verification_hash(
                "test_mod_001",
                "test_desire_001",
                ["exp_001", "exp_002"],
                "2025-12-26T00:00:00"
            )
            print(f"    ✓ Hash computation works: {test_hash[:16]}...")
        else:
            print("    ⊘ Skipped (memory not connected)")

    except Exception as e:
        results["errors"].append(f"Provenance system failed: {e}")
        print(f"    ✗ Provenance system failed: {e}")

    # 6. Test coder availability
    print("\n[6] Testing coder component...")
    try:
        from coder import Coder

        coder_config = config.get("coder", {})
        coder = Coder(coder_config, project_root=str(Path(__file__).parent))

        results["coder_available"] = True
        results["coder_cli_found"] = coder.enabled

        print(f"    ✓ Coder initialized")
        print(f"    ✓ CLI path: {coder.cli_path}")
        print(f"    ✓ CLI found: {coder.enabled}")
        print(f"    ✓ Max turns: {coder.max_turns}")
        print(f"    ✓ Allowed tools: {coder.allowed_tools}")

    except Exception as e:
        results["errors"].append(f"Coder failed: {e}")
        print(f"    ✗ Coder failed: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_checks = [
        ("Configuration enabled", results["config_enabled"]),
        ("System initialized", results["system_initialized"]),
        ("Constitutional constraints", results["constitutional_constraints_working"]),
        ("Protected files defined", results["protected_files_defined"]),
        ("Modifiable files defined", results["modifiable_files_defined"]),
        ("Memory connected", results["memory_connected"]),
        ("Provenance system", results["provenance_system_working"]),
        ("Coder component", results["coder_available"]),
        ("Coder CLI found", results["coder_cli_found"]),
    ]

    passed = sum(1 for _, v in all_checks if v)
    total = len(all_checks)

    for name, status in all_checks:
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {name}: {'PASS' if status else 'FAIL'}")

    print()
    print(f"Result: {passed}/{total} checks passed")

    # Capability assessment
    capability_accessible = (
        results["config_enabled"] and
        results["system_initialized"] and
        results["constitutional_constraints_working"] and
        results["coder_cli_found"]
    )

    print()
    if capability_accessible:
        print("🟢 SELF-MODIFICATION CAPABILITY IS ACCESSIBLE")
        print("   BYRD can modify its own code through the Seeker's self_modify strategy")
    else:
        missing = []
        if not results["config_enabled"]:
            missing.append("config.yaml self_modification.enabled = false")
        if not results["system_initialized"]:
            missing.append("SelfModificationSystem failed to initialize")
        if not results["coder_cli_found"]:
            missing.append("Claude Code CLI not found")

        print("🔴 SELF-MODIFICATION CAPABILITY IS NOT FULLY ACCESSIBLE")
        print("   Missing components:")
        for m in missing:
            print(f"   - {m}")

    if results["errors"]:
        print()
        print("Errors encountered:")
        for err in results["errors"]:
            print(f"  - {err}")

    # Cleanup
    if memory:
        await memory.close()

    return results


if __name__ == "__main__":
    results = asyncio.run(test_self_modification_capability())
