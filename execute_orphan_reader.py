#!/usr/bin/env python3
"""
Execute Orphan Reader - Expose Orphan Content in Reflection Context

This script executes the orphan_reader module to:
1. Query orphan nodes from the memory system
2. Classify orphans using the taxonomy system
3. Select high-priority orphans for reflection
4. Expose orphan content to the reflection processing context
5. Track exposure and generate reflection summaries

Usage:
    python execute_orphan_reader.py [--batch-size N] [--priority-threshold X]

Examples:
    python execute_orphan_reader.py                    # Use defaults
    python execute_orphan_reader.py --batch-size 10     # Process 10 orphans
    python execute_orphan_reader.py --priority 0.7      # High priority only
"""

import asyncio
import argparse
import json
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Import required modules
from memory import Memory
from orphan_reader import (
    OrphanReader,
    ReflectionBatch,
    DEFAULT_BATCH_SIZE,
    DEFAULT_PRIORITY_THRESHOLD
)
from orphan_taxonomy import StructuralCategory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OrphanReaderExecutor:
    """
    Executor for the orphan_reader module.
    
    This class orchestrates the process of reading, analyzing, and exposing
    orphan content to the reflection context.
    """
    
    def __init__(
        self,
        memory_uri: str = "bolt://localhost:7687",
        username: str = "neo4j",
        password: str = "password"
    ):
        """
        Initialize the executor with a memory connection.
        
        Args:
            memory_uri: Neo4j connection URI
            username: Database username
            password: Database password
        """
        self.memory = Memory(memory_uri, username, password)
        self.reader: Optional[OrphanReader] = None
        
    async def initialize(self):
        """Initialize the memory connection and orphan reader."""
        try:
            await self.memory.initialize()
            self.reader = OrphanReader(self.memory)
            logger.info("OrphanReader initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            return False
            
    async def close(self):
        """Close the memory connection."""
        if self.memory:
            await self.memory.close()
            logger.info("Memory connection closed")
            
    async def execute(
        self,
        batch_size: int = DEFAULT_BATCH_SIZE,
        priority_threshold: float = DEFAULT_PRIORITY_THRESHOLD,
        categories: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Execute the orphan reader workflow.
        
        Args:
            batch_size: Number of orphans to process
            priority_threshold: Minimum priority score (0-1)
            categories: Filter to specific categories
            
        Returns:
            Execution results dictionary
        """
        if not self.reader:
            raise RuntimeError("OrphanReader not initialized. Call initialize() first.")
            
        logger.info(f"\n{'='*70}")
        logger.info("ORPHAN READER EXECUTION")
        logger.info(f"{'='*70}")
        
        results = {
            'execution_timestamp': datetime.now().isoformat(),
            'configuration': {
                'batch_size': batch_size,
                'priority_threshold': priority_threshold,
                'categories': [c.value for c in categories] if categories else 'all'
            },
            'orphans_retrieved': {},
            'exposure_results': {},
            'summary': {}
        }
        
        # Step 1: Retrieve orphans for reflection
        logger.info("\n[STEP 1] Retrieving orphans for reflection...")
        batch = await self.reader.get_orphans_for_reflection(
            batch_size=batch_size,
            priority_threshold=priority_threshold,
            categories=categories
        )
        
        results['orphans_retrieved'] = {
            'total_contexts': len(batch.contexts),
            'total_priority': batch.total_priority,
            'batch_timestamp': batch.batch_timestamp.isoformat(),
            'categories': list(batch.categories) if batch.categories else []
        }
        
        logger.info(f"  ✓ Retrieved {len(batch.contexts)} orphan contexts")
        logger.info(f"  ✓ Total priority score: {batch.total_priority:.3f}")
        
        # Step 2: Display orphan details
        logger.info("\n[STEP 2] Orphan Context Details:")
        for i, context in enumerate(batch.contexts, 1):
            orphan = context.orphan
            logger.info(f"\n  Orphan {i}: {orphan.id}")
            logger.info(f"    Type: {orphan.node_type}")
            logger.info(f"    Category: {orphan.structural_category.value if orphan.structural_category else 'N/A'}")
            logger.info(f"    Priority: {orphan.priority.value if orphan.priority else 'N/A'}")
            logger.info(f"    Semantic Density: {orphan.semantic_density:.3f}")
            logger.info(f"    Age: {orphan.age_hours:.1f} hours")
            logger.info(f"    Ready for Reflection: {context.reflection_ready}")
            if context.suggested_prompt:
                prompt_preview = context.suggested_prompt[:100]
                logger.info(f"    Prompt: {prompt_preview}...")
        
        # Step 3: Expose to reflection
        logger.info("\n[STEP 3] Exposing orphans to reflection context...")
        
        async def reflection_callback(context):
            """Custom callback for reflection exposure."""
            logger.info(f"    → Exposed {context.orphan.id} to reflection")
            
        exposure_results = await self.reader.expose_to_reflection(
            batch,
            reflection_callback=reflection_callback
        )
        
        results['exposure_results'] = exposure_results
        
        logger.info(f"  ✓ Exposed: {exposure_results['exposed_count']}")
        logger.info(f"  ✓ Successful: {exposure_results['successful_count']}")
        logger.info(f"  ✓ Failed: {exposure_results['failed_count']}")
        
        # Step 4: Generate summary
        logger.info("\n[STEP 4] Generating reflection summary...")
        summary = await self.reader.get_reflection_summary()
        results['summary'] = summary
        
        logger.info(f"  Total orphans exposed: {summary.get('total_exposed', 0)}")
        logger.info(f"  Pending orphans: {summary.get('pending_orphans', 0)}")
        
        return results
        
    def format_output(self, results: Dict[str, Any]) -> str:
        """
        Format execution results for display.
        
        Args:
            results: Execution results dictionary
            
        Returns:
            Formatted string output
        """
        output = []
        output.append(f"\n{'='*70}")
        output.append("ORPHAN READER EXECUTION COMPLETE")
        output.append(f"{'='*70}\n")
        
        # Configuration
        config = results['configuration']
        output.append("Configuration:")
        output.append(f"  Batch Size: {config['batch_size']}")
        output.append(f"  Priority Threshold: {config['priority_threshold']}")
        output.append(f"  Categories: {config['categories']}")
        
        # Retrieval Results
        retrieved = results['orphans_retrieved']
        output.append(f"\nRetrieval Results:")
        output.append(f"  Contexts Retrieved: {retrieved['total_contexts']}")
        output.append(f"  Total Priority Score: {retrieved['total_priority']:.3f}")
        
        # Exposure Results
        exposure = results['exposure_results']
        output.append(f"\nExposure Results:")
        output.append(f"  Exposed to Reflection: {exposure['exposed_count']}")
        output.append(f"  Successful: {exposure['successful_count']}")
        output.append(f"  Failed: {exposure['failed_count']}")
        
        if exposure['orphan_ids']:
            output.append(f"\n  Exposed Orphan IDs:")
            for orphan_id in exposure['orphan_ids']:
                output.append(f"    - {orphan_id}")
        
        # Summary
        summary = results['summary']
        output.append(f"\nReflection Summary:")
        output.append(f"  Total Exposed: {summary.get('total_exposed', 'N/A')}")
        output.append(f"  Pending Orphans: {summary.get('pending_orphans', 'N/A')}")
        
        output.append(f"\nExecution Time: {results['execution_timestamp']}")
        output.append(f"{'='*70}\n")
        
        return "\n".join(output)


async def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Execute orphan_reader to expose orphan content in reflection context"
    )
    parser.add_argument(
        '--batch-size', '-b',
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Number of orphans to process (default: {DEFAULT_BATCH_SIZE})"
    )
    parser.add_argument(
        '--priority', '-p',
        type=float,
        default=DEFAULT_PRIORITY_THRESHOLD,
        help=f"Minimum priority threshold 0-1 (default: {DEFAULT_PRIORITY_THRESHOLD})"
    )
    parser.add_argument(
        '--category', '-c',
        action='append',
        choices=[c.value for c in StructuralCategory],
        help="Filter to specific structural category (can use multiple times)"
    )
    parser.add_argument(
        '--output-json', '-j',
        action='store_true',
        help="Output results as JSON instead of formatted text"
    )
    parser.add_argument(
        '--memory-uri',
        default="bolt://localhost:7687",
        help="Neo4j connection URI (default: bolt://localhost:7687)"
    )
    
    args = parser.parse_args()
    
    # Parse categories if provided
    categories = None
    if args.category:
        categories = [StructuralCategory(c) for c in args.category]
    
    # Create executor
    executor = OrphanReaderExecutor(
        memory_uri=args.memory_uri,
        username="neo4j",
        password="password"
    )
    
    try:
        # Initialize
        if not await executor.initialize():
            print("ERROR: Failed to initialize memory connection")
            sys.exit(1)
        
        # Execute
        results = await executor.execute(
            batch_size=args.batch_size,
            priority_threshold=args.priority,
            categories=categories
        )
        
        # Output
        if args.output_json:
            print(json.dumps(results, indent=2, default=str))
        else:
            print(executor.format_output(results))
            
    except KeyboardInterrupt:
        logger.info("\nExecution interrupted by user")
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await executor.close()


if __name__ == "__main__":
    asyncio.run(main())
