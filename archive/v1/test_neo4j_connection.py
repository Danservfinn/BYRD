#!/usr/bin/env python3
"""Test Neo4j connection."""

import asyncio
import os
from datetime import datetime

# Neo4j connection settings
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

async def test_connection():
    try:
        from neo4j import AsyncGraphDatabase
    except ImportError:
        print("ERROR: neo4j package not installed")
        return False

    driver = None
    try:
        driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        async with driver.session() as session:
            # Test basic query
            result = await session.run("RETURN 'Connected' as status")
            record = await result.single()
            print(f"Neo4j connection test: {record['status']}")
            
            # Test counting desires
            result = await session.run("MATCH (d:Desire) RETURN count(d) as count")
            record = await result.single()
            print(f"Total desires in database: {record['count']}")
            
            return True
    except Exception as e:
        print(f"Connection error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if driver:
            await driver.close()

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    print(f"Test {'passed' if success else 'failed'}")
