#!/usr/bin/env python3
"""
EXECUTE: Connect Orphan Nodes - Break Analysis Paralysis

This script CONCRETELY connects orphan nodes in BYRD's memory graph.
No analysis, no planning - just execution.

Usage:
    python execute_orphan_connection.py [--count N]
"""

import asyncio
import os
import sys
import argparse
from datetime import datetime

# Load environment
from dotenv import load_dotenv
load_dotenv()

from neo4j import AsyncGraphDatabase


class OrphanConnector:
    """Concrete execution engine for connecting orphan nodes."""

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        self.connections_created = 0
        self.errors = []

    async def connect(self):
        """Establish connection to Neo4j."""
        self.driver = AsyncGraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )
        await self.driver.verify_connectivity()
        print(f"✓ Connected to Neo4j at {self.uri}")

    async def disconnect(self):
        """Close database connection."""
        if self.driver:
            await self.driver.close()
            print("✓ Disconnected from Neo4j")

    async def count_orphans(self):
        """Count current orphan nodes."""
        query = """
        MATCH (n)
        WHERE NOT (n)--()
          AND NOT coalesce(n.archived, false)
          AND NOT n:Mutation
          AND NOT n:QuantumMoment
        RETURN count(n) as count
        """
        async with self.driver.session() as session:
            result = await session.run(query)
            record = await result.single()
            return record["count"] if record else 0

    async def create_one_connection(self):
        """
        Execute ONE atomic connection between orphan nodes.
        Returns True if connection created, False if no orphans left.
        """
        query = """
        MATCH (a), (b)
        WHERE NOT (a)--()
          AND NOT (b)--()
          AND a.id <> b.id
          AND NOT coalesce(a.archived, false)
          AND NOT coalesce(b.archived, false)
          AND NOT a:Mutation
          AND NOT b:Mutation
          AND NOT a:QuantumMoment
          AND NOT b:QuantumMoment
        WITH a, b
        LIMIT 1
        CREATE (a)-[r:RELATED_TO {
            created_at: datetime(), 
            reason: 'orphan_reconciliation',
            method: 'concrete_execution'
        }]->(b)
        RETURN a.id as id_a, b.id as id_b, type(a) as type_a, type(b) as type_b
        """
        
        async with self.driver.session() as session:
            result = await session.run(query)
            record = await result.single()
            if record:
                self.connections_created += 1
                print(f"  [{self.connections_created}] Connected {record['type_a']}({record['id_a'][:16]}...) → {record['type_b']}({record['id_b'][:16]}...)")
                return True
            return False

    async def execute_connections(self, target_count: int = 10):
        """
        Execute connections until target reached or no orphans left.
        """
        print(f"\n{'='*60}")
        print("EXECUTE: Connecting Orphan Nodes")
        print(f"{'='*60}")
        print(f"Target: {target_count} connections")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Count initial orphans
        initial_orphans = await self.count_orphans()
        print(f"Initial orphan count: {initial_orphans}")
        print()
        
        if initial_orphans == 0:
            print("✓ No orphan nodes found - graph is fully connected!")
            return
        
        # Execute connections
        print("Creating connections...")
        connections_this_run = 0
        
        while connections_this_run < target_count:
            success = await self.create_one_connection()
            if not success:
                print("\n✓ No more orphan pairs available")
                break
            connections_this_run += 1
            
            # Small delay to avoid overwhelming database
            if connections_this_run % 5 == 0:
                await asyncio.sleep(0.1)
        
        # Final report
        final_orphans = await self.count_orphans()
        
        print()
        print(f"{'='*60}")
        print("EXECUTION COMPLETE")
        print(f"{'='*60}")
        print(f"Connections created: {self.connections_created}")
        print(f"Orphans before: {initial_orphans}")
        print(f"Orphans after: {final_orphans}")
        print(f"Orphans connected: {initial_orphans - final_orphans}")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")


async def main():
    """Main execution entry point."""
    parser = argparse.ArgumentParser(description="Connect orphan nodes")
    parser.add_argument("--count", type=int, default=10, 
                        help="Number of connections to create (default: 10)")
    args = parser.parse_args()
    
    connector = OrphanConnector()
    
    try:
        await connector.connect()
        await connector.execute_connections(target_count=args.count)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await connector.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
