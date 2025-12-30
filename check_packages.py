#!/usr/bin/env python3
"""Check if neo4j package is available."""
import sys

print("Checking installed packages...")
try:
    import pkg_resources
    installed = [d.project_name for d in pkg_resources.working_set]
    if 'neo4j' in installed or 'neo4j-driver' in installed:
        print("✓ neo4j package is installed")
    else:
        print("✗ neo4j package NOT found")
        print("\nInstalled packages:")
        for pkg in sorted(installed):
            print(f"  - {pkg}")
except ImportError:
    print("pkg_resources not available, trying direct import...")
    try:
        import neo4j
        print(f"✓ neo4j imported successfully: {neo4j.__version__}")
    except ImportError as e:
        print(f"✗ Cannot import neo4j: {e}")

print("\nDone.")
