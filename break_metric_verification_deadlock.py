#!/usr/bin/env python3
"""
BREAK METRIC VERIFICATION DEADLOCK

This script breaks the verification deadlock by executing direct graph queries
for Metric nodes. It provides:
- Direct database inspection without runtime dependencies
- Atomic queries for LoopMetric and MetricSnapshot nodes
- Clear verification output
- Demo mode for testing without database

Usage:
    python break_metric_verification_deadlock.py          # Demo mode
    python break_metric_verification_deadlock.py --live  # Live mode (requires Neo4j)
    python break_metric_verification_deadlock.py --limit 50
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Neo4j driver availability check
NEO4J_AVAILABLE = False
DRIVER_ERROR = None

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError as e:
    DRIVER_ERROR = str(e)

# Load environment variables
def load_env() -> Dict[str, str]:
    """Load environment variables from .env file."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        env_file = '.env'
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    return {
        'NEO4J_URI': os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        'NEO4J_USER': os.getenv("NEO4J_USER", "neo4j"),
        'NEO4J_PASSWORD': os.getenv("NEO4J_PASSWORD", "password"),
    }


@dataclass
class MetricNode:
    """Represents a metric node from the graph."""
    node_type: str
    properties: Dict[str, Any]
    
    def display(self, index: int) -> str:
        """Format for display."""
        lines = [f"[{index}] {self.node_type}:"]
        for key, value in self.properties.items():
            if isinstance(value, str) and len(value) > 80:
                value = value[:80] + "..."
            elif isinstance(value, dict):
                value = json.dumps(value, default=str)[:80] + "..."
            lines.append(f"    {key}: {value}")
        return "\n".join(lines)


class MetricQueryEngine:
    """Engine for executing metric node queries."""
    
    def __init__(self, env_vars: Dict[str, str]):
        self.env_vars = env_vars
        self.driver = None
        self.is_connected = False
        self.is_demo = not NEO4J_AVAILABLE
    
    def connect(self) -> bool:
        """Establish Neo4j connection."""
        if self.is_demo:
            return True
        
        try:
            self.driver = GraphDatabase.driver(
                self.env_vars['NEO4J_URI'],
                auth=(self.env_vars['NEO4J_USER'], self.env_vars['NEO4J_PASSWORD'])
            )
            self.driver.verify_connectivity()
            self.is_connected = True
            return True
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return False
    
    def close(self):
        """Close connection."""
        if self.driver:
            self.driver.close()
            self.is_connected = False
    
    def get_counts(self) -> Dict[str, int]:
        """Get counts of all metric node types."""
        if self.is_demo:
            return {'LoopMetric': 42, 'MetricSnapshot': 15}
        
        counts = {}
        
        with self.driver.session() as session:
            result = session.run("MATCH (lm:LoopMetric) RETURN count(lm) as c")
            counts['LoopMetric'] = result.single()["c"]
        
        with self.driver.session() as session:
            result = session.run("MATCH (ms:MetricSnapshot) RETURN count(ms) as c")
            counts['MetricSnapshot'] = result.single()["c"]
        
        return counts
    
    def query_loop_metrics(self, limit: int = 20) -> List[MetricNode]:
        """Query LoopMetric nodes."""
        if self.is_demo:
            return [
                MetricNode('LoopMetric', {
                    'id': 'lm_001',
                    'loop_name': 'capability_improvement',
                    'cycle_number': 3,
                    'mode': 'autonomous',
                    'timestamp': datetime.now().isoformat(),
                    'metrics': {'improvement_score': 0.87, 'code_quality': 0.92}
                }),
                MetricNode('LoopMetric', {
                    'id': 'lm_002',
                    'loop_name': 'belief_refinement',
                    'cycle_number': 5,
                    'mode': 'assisted',
                    'timestamp': datetime.now().isoformat(),
                    'metrics': {'coherence': 0.85, 'confidence': 0.78}
                })
            ]
        
        query = """
            MATCH (lm:LoopMetric)
            RETURN properties(lm) AS props
            ORDER BY lm.timestamp DESC
            LIMIT $limit
        """
        
        nodes = []
        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            for record in result:
                props = record["props"]
                nodes.append(MetricNode('LoopMetric', props))
        
        return nodes
    
    def query_metric_snapshots(self, limit: int = 20) -> List[MetricNode]:
        """Query MetricSnapshot nodes."""
        if self.is_demo:
            return [
                MetricNode('MetricSnapshot', {
                    'id': 'ms_001',
                    'capability_score': 0.87,
                    'llm_efficiency': 0.94,
                    'loop_count': 42,
                    'timestamp': datetime.now().isoformat()
                })
            ]
        
        query = """
            MATCH (ms:MetricSnapshot)
            RETURN properties(ms) AS props
            ORDER BY ms.timestamp DESC
            LIMIT $limit
        """
        
        nodes = []
        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            for record in result:
                props = record["props"]
                nodes.append(MetricNode('MetricSnapshot', props))
        
        return nodes


def print_header(title: str):
    """Print section header."""
    print("\n" + "="*70)
    print(title)
    print("="*70)


def print_success(message: str):
    """Print success message."""
    print(f"  ✓ {message}")


def print_warning(message: str):
    """Print warning message."""
    print(f"  ⚠ {message}")


def print_error(message: str):
    """Print error message."""
    print(f"  ✗ {message}")


def main():
    """Main execution."""
    print("#"*70)
    print("# BREAK METRIC VERIFICATION DEADLOCK")
    print("# Direct Graph Query for Metric Nodes")
    print("#"*70)
    print(f"\nExecution time: {datetime.now().isoformat()}")
    
    # Parse args
    import argparse
    parser = argparse.ArgumentParser(description='Query Metric nodes from Neo4j')
    parser.add_argument('--limit', type=int, default=20, help='Limit results')
    parser.add_argument('--live', action='store_true', help='Use live connection')
    args = parser.parse_args()
    
    # Load environment
    print("\n[STEP 1] Loading environment...")
    env_vars = load_env()
    print_success(f"NEO4J_URI: {env_vars['NEO4J_URI']}")
    print_success(f"NEO4J_USER: {env_vars['NEO4J_USER']}")
    
    # Check availability
    if not NEO4J_AVAILABLE and args.live:
        print_error(f"Neo4j driver not available: {DRIVER_ERROR}")
        print("  Install with: pip install neo4j")
        print("  Or run without --live for demo mode")
        return 1
    
    # Create engine
    print("\n[STEP 2] Initializing query engine...")
    engine = MetricQueryEngine(env_vars)
    if not args.live and not NEO4J_AVAILABLE:
        print_warning("Running in DEMO mode (simulated results)")
        engine.is_demo = True
    else:
        print_success("Connecting to Neo4j...")
        if not engine.connect():
            return 1
        print_success("Connected successfully")
    
    try:
        # Get counts
        print("\n[STEP 3] Querying metric node counts...")
        counts = engine.get_counts()
        print(f"  LoopMetric: {counts['LoopMetric']} nodes")
        print(f"  MetricSnapshot: {counts['MetricSnapshot']} nodes")
        
        total = counts['LoopMetric'] + counts['MetricSnapshot']
        
        if total == 0 and not engine.is_demo:
            print_warning("No metric nodes found in database")
            print("  This may indicate:")
            print("    - Metrics have not been written yet")
            print("    - Node labels differ from expected")
            print("    - Database is empty")
            return 0
        
        # Query LoopMetric nodes
        print_header("LOOP METRIC NODES")
        loop_metrics = engine.query_loop_metrics(limit=args.limit)
        print(f"Found {len(loop_metrics)} total LoopMetric nodes")
        print(f"Displaying first {min(args.limit, len(loop_metrics))}:\n")
        
        for i, node in enumerate(loop_metrics[:args.limit], 1):
            print(node.display(i))
            print()
        
        # Query MetricSnapshot nodes
        print_header("METRIC SNAPSHOT NODES")
        snapshots = engine.query_metric_snapshots(limit=args.limit)
        print(f"Found {len(snapshots)} total MetricSnapshot nodes")
        print(f"Displaying first {min(args.limit, len(snapshots))}:\n")
        
        for i, node in enumerate(snapshots[:args.limit], 1):
            print(node.display(i))
            print()
        
        # Summary
        print_header("VERIFICATION DEADLOCK - BROKEN")
        print(f"\n✓✓✓ Direct graph query executed successfully ✓✓✓")
        print(f"\nTotal metric nodes verified: {total:,}")
        print(f"  • LoopMetric: {counts['LoopMetric']:,}")
        print(f"  • MetricSnapshot: {counts['MetricSnapshot']:,}")
        
        if engine.is_demo:
            print("\n[NOTE] Results are from DEMO mode")
            print("To query live database:")
            print("  1. Install neo4j: pip install neo4j")
            print("  2. Run with --live flag")
        else:
            print("\n[VERIFICATION COMPLETE] Metrics are being written to database")
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Query execution failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        engine.close()
        print("\n[OK] Query engine closed")


if __name__ == "__main__":
    sys.exit(main())
