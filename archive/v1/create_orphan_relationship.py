#!/usr/bin/env python3
"""
Atomic Cypher Query: Create One Relationship Between Orphan Nodes

This script executes a single atomic Cypher query to create
one relationship between two orphan (isolated) nodes in the
BYRD Neo4j graph database.

Usage:
    python create_orphan_relationship.py

The query:
1. Finds two orphan Experience nodes with no relationships
2. Creates a RELATED_TO relationship between them
3. Returns the IDs of the connected nodes
"""

import asyncio
import os
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OrphanConnector:
    """Executes atomic relationship creation between orphan nodes."""

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None

    async def connect(self):
        """Establish connection to Neo4j."""
        self.driver = AsyncGraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )
        print(f"✓ Connected to Neo4j at {self.uri}")

    async def create_orphan_relationship(self):
        """
        Execute ONE atomic Cypher query to create ONE relationship
        between orphan nodes.

        Returns:
            dict: Information about the created relationship
        """
        # THE ATOMIC CYPHER QUERY
        # This single query finds two orphan Experience nodes
        # and creates exactly one relationship between them.
        query = """
        MATCH (a:Experience), (b:Experience)
        WHERE NOT (a)--()
          AND NOT (b)--()
          AND a.id <> b.id
          AND NOT coalesce(a.archived, false)
          AND NOT coalesce(b.archived, false)
        WITH a, b
        LIMIT 1
        CREATE (a)-[r:RELATED_TO {created_at: datetime(), reason: 'orphan_reconciliation'}]->(b)
        RETURN a.id as source_id, a.type as source_type,
               b.id as target_id, b.type as target_type,
               type(r) as relationship_type, r.created_at as created_at
        """

        async with self.driver.session() as session:
            result = await session.run(query)
            record = await result.single()

            if record:
                return {
                    "success": True,
                    "source_id": record["source_id"],
                    "source_type": record["source_type"],
                    "target_id": record["target_id"],
                    "target_type": record["target_type"],
                    "relationship_type": record["relationship_type"],
                    "created_at": str(record["created_at"]),
                    "query": query.strip()
                }
            else:
                return {
                    "success": False,
                    "message": "No orphan nodes found to connect",
                    "query": query.strip()
                }

    async def close(self):
        """Close the database connection."""
        if self.driver:
            await self.driver.close()
            print("✓ Connection closed")


async def main():
    """Execute the atomic orphan connection."""
    print("="*60)
    print("ATOMIC ORPHAN CONNECTION")
    print("="*60)

    connector = OrphanConnector()

    try:
        await connector.connect()
        result = await connector.create_orphan_relationship()

        print("\nQuery Executed:")
        print("-"*60)
        print(result["query"])
        print("-"*60)

        if result["success"]:
            print("\n✓ RELATIONSHIP CREATED")
            print(f"  Source:  {result['source_type']}({result['source_id']})")
            print(f"  Target:  {result['target_type']}({result['target_id']})")
            print(f"  Type:    {result['relationship_type']}")
            print(f"  Created: {result['created_at']}")
        else:
            print(f"\n⚠ {result['message']}")

        print("\n" + "="*60)
        print("DONE")
        print("="*60)

    finally:
        await connector.close()


if __name__ == "__main__":
    asyncio.run(main())
