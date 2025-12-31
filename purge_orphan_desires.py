#!/usr/bin/env python3
"""
Purge Zombie Desires Related to Orphan Reconciliation

This script marks all desires related to orphan reconciliation as fulfilled,
stopping them from consuming cycles on a solved problem.

Usage:
    python purge_orphan_desires.py [--dry-run]
"""

import asyncio
import sys
import os
from datetime import datetime

# Neo4j connection settings
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

def log(message):
    """Simple logging function."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} {message}")

async def main_async(dry_run=False):
    """Main async function."""
    log("=" * 60)
    log("ORPHAN DESIRE PURGE - ZOMBIE ELIMINATION")
    log("=" * 60)
    log(f"Connecting to Neo4j at {NEO4J_URI}")

    try:
        from neo4j import AsyncGraphDatabase
    except ImportError:
        log("ERROR: neo4j package not installed")
        log("Install with: pip install neo4j")
        return

    driver = None
    try:
        driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        async with driver.session() as session:
            # Get orphan-related desires
            query = """
                MATCH (d:Desire {fulfilled: false})
                WHERE 
                    toLower(d.description) CONTAINS 'orphan'
                    OR toLower(d.type) CONTAINS 'orphan'
                    OR toLower(d.target) CONTAINS 'orphan'
                RETURN d.id as id,
                       d.description as description,
                       d.status as status,
                       d.intensity as intensity
                ORDER BY d.intensity DESC
            """
            result = await session.run(query)
            orphan_desires = await result.data()
            
            count = len(orphan_desires)
            log(f"\nFound {count} unfulfilled desires related to orphan reconciliation")

            if count == 0:
                log("\n✓ No orphan desires to purge - cycle budget is clean")
                return

            # List them
            log(f"\nDesires consuming cycles:")
            for d in orphan_desires[:20]:
                log(f"  🔶 [{d.get('id', 'unknown')[:16]}] {d.get('description', 'no description')[:60]}")
            
            if len(orphan_desires) > 20:
                log(f"  ... and {len(orphan_desires) - 20} more zombie desires")

            if dry_run:
                log("\n[DRY RUN] No changes performed")
                log(f"Would free cycle budget from {count} zombie desires")
                return

            # Confirm and proceed
            log(f"\n⚠️  Marking {count} desires as fulfilled...")
            log("These zombie desires will no longer consume cycle budget.")
            
            # Perform fulfillment
            fulfilled_count = 0
            for d in orphan_desires:
                desire_id = d['id']
                update_query = """
                    MATCH (d:Desire {id: $id})
                    SET d.fulfilled = true,
                        d.status = 'fulfilled',
                        d.fulfilled_at = datetime(),
                        d.fulfilled_by = 'system_purge',
                        d.outcome = 'Purged as zombie desire - orphan reconciliation is solved'
                    RETURN count(d) as count
                """
                try:
                    result = await session.run(update_query, id=desire_id)
                    record = await result.single()
                    if record and record["count"] > 0:
                        fulfilled_count += 1
                        log(f"  ✓ Fulfilled: {d['description'][:50]}...")
                except Exception as e:
                    log(f"  ! Failed to fulfill {desire_id}: {e}")
            
            log(f"\n✓ Purged {fulfilled_count} orphan-related desires")
            log("✓ Zombie desires eliminated. Cycle budget freed.")
            log("✓ Solved problem no longer drives new desires.")

    except Exception as e:
        log(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            await driver.close()

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    asyncio.run(main_async(dry_run=dry_run))
