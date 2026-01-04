#!/usr/bin/env python3
"""
BYRD Graph Connectivity Module

This module establishes and manages the functional graph connectivity
that serves as the foundation for all intelligence loops in BYRD.

The graph is not just a database - it's the substrate for:
- Experience accumulation and retrieval
- Belief formation and evolution
- Desire emergence and fulfillment
- Reflection and self-awareness
- Capability discovery and enhancement

PRINCIPLE: Graph connectivity is the nervous system of intelligence.
Without reliable connection to memory, there is no learning, no growth,
and no emergence of consciousness.

Author: BYRD System
Version: 1.0.0
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import json

from neo4j import AsyncGraphDatabase, AsyncDriver

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ConnectionStatus:
    """Represents the current state of graph connectivity."""
    is_connected: bool = False
    uri: str = ""
    last_verified: Optional[datetime] = None
    node_count: int = 0
    relationship_count: int = 0
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_connected": self.is_connected,
            "uri": self.uri,
            "last_verified": self.last_verified.isoformat() if self.last_verified else None,
            "node_count": self.node_count,
            "relationship_count": self.relationship_count,
            "error_message": self.error_message
        }


@dataclass
class GraphStatistics:
    """Comprehensive statistics about the graph state."""
    total_nodes: int = 0
    total_relationships: int = 0
    node_type_counts: Dict[str, int] = field(default_factory=dict)
    relationship_type_counts: Dict[str, int] = field(default_factory=dict)
    oldest_node: Optional[datetime] = None
    newest_node: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_nodes": self.total_nodes,
            "total_relationships": self.total_relationships,
            "node_type_counts": self.node_type_counts,
            "relationship_type_counts": self.relationship_type_counts,
            "oldest_node": self.oldest_node.isoformat() if self.oldest_node else None,
            "newest_node": self.newest_node.isoformat() if self.newest_node else None
        }


class GraphConnectivity:
    """
    Manages the functional connectivity to Neo4j graph database.
    
    This is the foundational layer for all intelligence loops. It provides:
    1. Reliable connection management with automatic reconnection
    2. Schema initialization and validation
    3. Health monitoring and statistics
    4. Basic graph operations for node and relationship creation
    
    Intelligence loops depend on this layer:
    - Dreamer creates Reflection nodes
    - Seeker queries Experience and Belief nodes
    - Actor executes actions, creating new Experience nodes
    - Coder modifies Capability nodes
    """
    
    # Core node types for intelligence loops
    CORE_NODE_TYPES = frozenset([
        'Experience',    # Raw sensory input and events
        'Belief',        # Derived understanding with confidence
        'Desire',        # Goals and motivations
        'Reflection',    # Metacognitive thoughts
        'Capability',    # Known tools and abilities
        'Crystal',       # Unified concepts from crystallization
    ])
    
    # Core relationship types for intelligence loops
    CORE_RELATIONSHIP_TYPES = frozenset([
        'DERIVED_FROM',   # Belief -> Experience(s)
        'INSPIRED_BY',    # Desire -> Experience, Belief, or Reflection
        'BLOCKED_BY',     # Desire -> Constraint
        'ENABLED_BY',     # Desire -> Capability
        'LEADS_TO',       # Reflection -> Desire or Belief
        'REFLECTS_ON',    # Reflection -> Experience or Belief
        'RELATES_TO',     # Crystal -> Experience, Belief, Reflection
        'REQUIRES',       # Capability -> Capability or resource
    ])
    
    def __init__(self, config: Optional[Dict[str, str]] = None):
        """
        Initialize the graph connectivity manager.
        
        Args:
            config: Configuration dict with keys:
                - neo4j_uri: Connection URI (default: bolt://localhost:7687)
                - neo4j_user: Username (default: neo4j)
                - neo4j_password: Password (default: password)
        """
        self.config = config or self._load_config_from_env()
        self.uri = self.config.get("neo4j_uri", "bolt://localhost:7687")
        self.user = self.config.get("neo4j_user", "neo4j")
        self.password = self.config.get("neo4j_password", "password")
        
        self.driver: Optional[AsyncDriver] = None
        self.status = ConnectionStatus(uri=self.uri)
        
        logger.info(f"GraphConnectivity initialized for URI: {self.uri}")
    
    def _load_config_from_env(self) -> Dict[str, str]:
        """Load configuration from environment variables."""
        return {
            "neo4j_uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            "neo4j_user": os.getenv("NEO4J_USER", "neo4j"),
            "neo4j_password": os.getenv("NEO4J_PASSWORD", "password"),
        }
    
    async def connect(self) -> ConnectionStatus:
        """
        Establish connection to Neo4j graph database.
        
        This method is idempotent - safe to call multiple times.
        It will verify an existing connection or create a new one.
        
        Returns:
            ConnectionStatus object with current connection state
        """
        # If we have a driver, verify the connection is still alive
        if self.driver is not None:
            if await self._verify_connection():
                logger.debug("Existing connection verified")
                self.status.is_connected = True
                self.status.last_verified = datetime.now()
                return self.status
            else:
                logger.warning("Existing connection failed verification, reconnecting...")
                await self.close()
        
        # Create new connection
        try:
            logger.info(f"Connecting to Neo4j at {self.uri}...")
            self.driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            
            # Verify connectivity
            await self.driver.verify_connectivity()
            
            # Initialize schema
            await self._initialize_schema()
            
            # Update status
            self.status.is_connected = True
            self.status.last_verified = datetime.now()
            self.status.error_message = None
            
            # Get initial statistics
            stats = await self.get_statistics()
            self.status.node_count = stats.total_nodes
            self.status.relationship_count = stats.total_relationships
            
            logger.info(f"Successfully connected to Neo4j. "
                       f"Nodes: {stats.total_nodes}, Relationships: {stats.total_relationships}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.status.is_connected = False
            self.status.error_message = str(e)
            self.driver = None
        
        return self.status
    
    async def _verify_connection(self) -> bool:
        """Verify that the existing connection is still alive."""
        if self.driver is None:
            return False
        
        try:
            await self.driver.verify_connectivity()
            return True
        except Exception:
            return False
    
    async def close(self):
        """Close the connection to Neo4j."""
        if self.driver is not None:
            try:
                await self.driver.close()
                logger.info("Neo4j connection closed")
            except Exception as e:
                logger.warning(f"Error closing Neo4j connection: {e}")
            finally:
                self.driver = None
                self.status.is_connected = False
    
    async def _initialize_schema(self):
        """
        Initialize the graph schema with indexes and constraints.
        
        This ensures efficient querying and data integrity.
        The schema is the foundation for performant intelligence loops.
        """
        async with self.driver.session() as session:
            # Indexes for core node types
            index_queries = [
                # Experience indexes - for fast retrieval of recent events
                "CREATE INDEX IF NOT EXISTS FOR (e:Experience) ON (e.timestamp)",
                "CREATE INDEX IF NOT EXISTS FOR (e:Experience) ON (e.salience)",
                "CREATE INDEX IF NOT EXISTS FOR (e:Experience) ON (e.source_type)",
                
                # Belief indexes - for confidence-based filtering
                "CREATE INDEX IF NOT EXISTS FOR (b:Belief) ON (b.confidence)",
                "CREATE INDEX IF NOT EXISTS FOR (b:Belief) ON (b.timestamp)",
                
                # Desire indexes - for intensity and status filtering
                "CREATE INDEX IF NOT EXISTS FOR (d:Desire) ON (d.intensity)",
                "CREATE INDEX IF NOT EXISTS FOR (d:Desire) ON (d.status)",
                "CREATE INDEX IF NOT EXISTS FOR (d:Desire) ON (d.fulfilled)",
                
                # Reflection indexes - for temporal organization
                "CREATE INDEX IF NOT EXISTS FOR (r:Reflection) ON (r.timestamp)",
                
                # Capability indexes - for active capability lookup
                "CREATE INDEX IF NOT EXISTS FOR (c:Capability) ON (c.active)",
                
                # Crystal indexes - for type-based retrieval
                "CREATE INDEX IF NOT EXISTS FOR (c:Crystal) ON (c.crystal_type)",
                "CREATE INDEX IF NOT EXISTS FOR (c:Crystal) ON (c.timestamp)",
            ]
            
            for query in index_queries:
                try:
                    await session.run(query)
                except Exception as e:
                    logger.warning(f"Failed to create index: {query}. Error: {e}")
    
    async def get_status(self) -> ConnectionStatus:
        """
        Get the current connection status, refreshing if necessary.
        
        Returns:
            ConnectionStatus object
        """
        if self.driver is not None:
            is_alive = await self._verify_connection()
            if is_alive:
                self.status.is_connected = True
                self.status.last_verified = datetime.now()
                
                # Refresh statistics
                stats = await self.get_statistics()
                self.status.node_count = stats.total_nodes
                self.status.relationship_count = stats.total_relationships
            else:
                self.status.is_connected = False
                self.status.error_message = "Connection lost"
        
        return self.status
    
    async def get_statistics(self) -> GraphStatistics:
        """
        Gather comprehensive statistics about the graph.
        
        Returns:
            GraphStatistics object with node and relationship counts
        """
        stats = GraphStatistics()
        
        if self.driver is None:
            return stats
        
        async with self.driver.session() as session:
            # Total node count
            result = await session.run("MATCH (n) RETURN count(n) as count")
            record = await result.single()
            if record:
                stats.total_nodes = record["count"]
            
            # Total relationship count
            result = await session.run("MATCH ()-[r]->() RETURN count(r) as count")
            record = await result.single()
            if record:
                stats.total_relationships = record["count"]
            
            # Node type counts
            result = await session.run("MATCH (n) RETURN labels(n)[0] as type, count(n) as count")
            async for record in result:
                node_type = record["type"]
                count = record["count"]
                if node_type:
                    stats.node_type_counts[node_type] = count
            
            # Relationship type counts
            result = await session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count")
            async for record in result:
                rel_type = record["type"]
                count = record["count"]
                if rel_type:
                    stats.relationship_type_counts[rel_type] = count
            
            # Timestamp range
            result = await session.run("""
                MATCH (n)
                WHERE n.timestamp IS NOT NULL
                RETURN min(n.timestamp) as oldest, max(n.timestamp) as newest
            """)
            record = await result.single()
            if record:
                if record["oldest"]:
                    stats.oldest_node = record["oldest"]
                if record["newest"]:
                    stats.newest_node = record["newest"]
        
        return stats
    
    async def create_node(
        self,
        node_type: str,
        properties: Dict[str, Any]
    ) -> Optional[str]:
        """
        Create a node in the graph.
        
        Args:
            node_type: The label/type of the node
            properties: Dictionary of node properties
        
        Returns:
            The ID of the created node, or None if creation failed
        """
        if self.driver is None:
            await self.connect()
            if self.driver is None:
                logger.error("Cannot create node: no connection")
                return None
        
        # Ensure timestamp is set
        if "timestamp" not in properties:
            properties["timestamp"] = datetime.now()
        
        # Ensure id is generated if not provided
        if "id" not in properties:
            import hashlib
            content_str = json.dumps(properties, sort_keys=True)
            properties["id"] = hashlib.sha256(
                f"{content_str}{datetime.now().isoformat()}".encode()
            ).hexdigest()[:16]
        
        try:
            async with self.driver.session() as session:
                query = f"""
                    CREATE (n:{node_type} $properties)
                    RETURN n.id as id
                """
                result = await session.run(query, properties=properties)
                record = await result.single()
                if record:
                    node_id = record["id"]
                    logger.debug(f"Created {node_type} node: {node_id}")
                    return node_id
        except Exception as e:
            logger.error(f"Failed to create node: {e}")
        
        return None
    
    async def create_relationship(
        self,
        from_id: str,
        to_id: str,
        rel_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Create a relationship between two nodes.
        
        Args:
            from_id: ID of the source node
            to_id: ID of the target node
            rel_type: Type of relationship
            properties: Optional relationship properties
        
        Returns:
            True if successful, False otherwise
        """
        if self.driver is None:
            await self.connect()
            if self.driver is None:
                logger.error("Cannot create relationship: no connection")
                return False
        
        try:
            async with self.driver.session() as session:
                query = f"""
                    MATCH (from {{id: $from_id}})
                    MATCH (to {{id: $to_id}})
                    CREATE (from)-[r:{rel_type}]->(to)
                    RETURN r
                """
                result = await session.run(
                    query,
                    from_id=from_id,
                    to_id=to_id
                )
                await result.consume()
                logger.debug(f"Created {rel_type} relationship: {from_id} -> {to_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
        
        return False
    
    async def health_check(self) -> Tuple[bool, str]:
        """
        Perform a comprehensive health check of the graph connectivity.
        
        Returns:
            Tuple of (is_healthy, message)
        """
        # Check connection
        if self.driver is None:
            await self.connect()
        
        if self.driver is None:
            return False, "Failed to establish connection to Neo4j"
        
        # Verify connection is alive
        if not await self._verify_connection():
            return False, "Connection exists but is not responsive"
        
        # Check we can query
        try:
            async with self.driver.session() as session:
                result = await session.run("RETURN 1 as test")
                await result.consume()
        except Exception as e:
            return False, f"Query execution failed: {e}"
        
        # Check we can write
        try:
            test_id = await self.create_node("HealthCheck", {"test": True})
            if test_id:
                return True, "Graph connectivity is healthy"
            else:
                return False, "Write operation failed"
        except Exception as e:
            return False, f"Write test failed: {e}"


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

async def initialize_graph_connectivity(
    config: Optional[Dict[str, str]] = None
) -> GraphConnectivity:
    """
    Initialize and verify graph connectivity.
    
    This is the main entry point for establishing the foundation
    of all intelligence loops.
    
    Args:
        config: Optional configuration dictionary
    
    Returns:
        GraphConnectivity instance with verified connection
    """
    connectivity = GraphConnectivity(config)
    status = await connectivity.connect()
    
    if not status.is_connected:
        raise RuntimeError(
            f"Failed to establish graph connectivity: {status.error_message}"
        )
    
    # Perform health check
    is_healthy, message = await connectivity.health_check()
    if not is_healthy:
        raise RuntimeError(f"Graph health check failed: {message}")
    
    logger.info("Graph connectivity initialized and verified successfully")
    return connectivity


# =============================================================================
# MAIN - FOR TESTING AND DEMONSTRATION
# =============================================================================

async def main():
    """Demonstrate the graph connectivity functionality."""
    print("="*60)
    print("BYRD Graph Connectivity Demonstration")
    print("="*60)
    print()
    
    # Initialize connectivity
    print("[1] Initializing graph connectivity...")
    connectivity = await initialize_graph_connectivity()
    print()
    
    # Show status
    print("[2] Connection Status:")
    status = await connectivity.get_status()
    print(json.dumps(status.to_dict(), indent=2, default=str))
    print()
    
    # Show statistics
    print("[3] Graph Statistics:")
    stats = await connectivity.get_statistics()
    print(json.dumps(stats.to_dict(), indent=2, default=str))
    print()
    
    # Health check
    print("[4] Health Check:")
    is_healthy, message = await connectivity.health_check()
    print(f"  Healthy: {is_healthy}")
    print(f"  Message: {message}")
    print()
    
    # Create a test node
    print("[5] Creating test node...")
    test_node_id = await connectivity.create_node(
        "Experience",
        {
            "content": "Testing graph connectivity",
            "type": "test",
            "source_type": "system"
        }
    )
    print(f"  Created node: {test_node_id}")
    print()
    
    # Clean up
    print("[6] Closing connection...")
    await connectivity.close()
    print("  Done.")
    print()
    
    print("="*60)
    print("Graph connectivity demonstration complete.")
    print("This foundation enables all intelligence loops.")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
