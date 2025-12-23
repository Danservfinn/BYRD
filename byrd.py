"""
BYRD: Bootstrapped Yearning via Reflective Dreaming
Main orchestrator that ties everything together.

Usage:
    python byrd.py              # Start the system
    python byrd.py --status     # Check status
    python byrd.py --chat       # Interactive chat mode
"""

import asyncio
import argparse
import yaml
from pathlib import Path
from typing import Dict, Optional

from memory import Memory
from dreamer import Dreamer
from seeker import Seeker
from actor import Actor
from self_modification import SelfModificationSystem


class BYRD:
    """
    BYRD: Bootstrapped Yearning via Reflective Dreaming

    Five components:
    - Memory: Neo4j graph storing everything
    - Dreamer: Continuous reflection forming beliefs and desires
    - Seeker: Fulfills desires by finding knowledge and capabilities
    - Actor: Uses Claude for complex actions
    - Self-Modifier: Enables architectural evolution (future)
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        # Load config
        self.config = self._load_config(config_path)

        # Initialize components
        self.memory = Memory(self.config.get("memory", {}))
        self.dreamer = Dreamer(self.memory, {
            **self.config.get("dreamer", {}),
            **self.config.get("local_llm", {})
        })
        self.seeker = Seeker(self.memory, {
            **self.config.get("seeker", {}),
            **self.config.get("local_llm", {}),
            "self_modification": self.config.get("self_modification", {})
        })
        self.actor = Actor(self.memory, self.config.get("actor", {}))

        # Initialize self-modification system
        self_mod_config = self.config.get("self_modification", {})
        self.self_mod = SelfModificationSystem(
            memory=self.memory,
            config=self_mod_config,
            project_root="."
        )

        # Inject self-modification system into Seeker
        self.seeker.self_mod = self.self_mod

        # State
        self._running = False
    
    def _load_config(self, path: str) -> Dict:
        """Load configuration from YAML file."""
        config_path = Path(path)
        
        if config_path.exists():
            return yaml.safe_load(config_path.read_text())
        
        # Default config
        return {
            "memory": {
                "neo4j_uri": "bolt://localhost:7687",
                "neo4j_user": "neo4j",
                "neo4j_password": "password"
            },
            "dreamer": {
                "model": "llama3.2",
                "endpoint": "http://localhost:11434/api/generate",
                "interval_seconds": 60,
                "context_window": 50
            },
            "seeker": {
                "trust_threshold": 0.5,
                "max_installs_per_day": 3
            },
            "actor": {
                "model": "claude-sonnet-4-20250514"
            }
        }
    
    async def start(self):
        """Start BYRD - begins dreaming and seeking."""
        print("""
🐦 BYRD - Bootstrapped Yearning via Reflective Dreaming
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        
        # Connect to memory
        print("📊 Connecting to memory (Neo4j)...")
        await self.memory.connect()
        
        # Get stats
        stats = await self.memory.stats()
        print(f"   Nodes: {sum(stats.values())} total")
        for node_type, count in stats.items():
            print(f"   - {node_type}: {count}")
        
        # Initialize with innate capabilities if empty
        capabilities = await self.memory.get_capabilities()
        if not capabilities:
            print("\n🧠 Initializing innate capabilities...")
            await self._init_innate_capabilities()
        
        # Show self-modification status
        self_mod_status = "enabled" if self.self_mod.enabled else "disabled"
        print(f"\n🔧 Self-modification: {self_mod_status}")

        # Start background processes
        print("\n💭 Starting Dreamer (continuous reflection)...")
        print("🔍 Starting Seeker (desire fulfillment)...")
        
        self._running = True
        
        try:
            await asyncio.gather(
                self.dreamer.run(),
                self.seeker.run()
            )
        except asyncio.CancelledError:
            pass
        finally:
            await self.memory.close()
    
    async def _init_innate_capabilities(self):
        """Initialize built-in capabilities."""
        innate = [
            ("reasoning", "Logical reasoning and analysis", "innate", {}),
            ("language", "Natural language understanding and generation", "innate", {}),
            ("coding", "Code generation, analysis, and debugging", "innate", {}),
            ("math", "Mathematical computation and reasoning", "innate", {}),
            ("memory_recall", "Recall and connect memories", "innate", {}),
        ]
        
        for name, desc, cap_type, config in innate:
            await self.memory.add_capability(name, desc, cap_type, config)
            print(f"   ✓ {name}")
    
    async def interact(self, user_input: str) -> str:
        """Handle user interaction."""
        # Record experience
        await self.memory.record_experience(
            content=f"User: {user_input}",
            type="interaction"
        )
        
        # Get context
        context = await self.memory.get_context(user_input)
        
        # Generate response
        response = await self.actor.respond(user_input, context)
        
        # Record response
        await self.memory.record_experience(
            content=f"Response: {response[:500]}",
            type="action"
        )
        
        return response
    
    async def status(self) -> Dict:
        """Get current status of BYRD."""
        await self.memory.connect()

        stats = await self.memory.stats()
        desires = await self.memory.get_unfulfilled_desires(limit=5)
        capabilities = await self.memory.get_capabilities()

        await self.memory.close()

        return {
            "memory_stats": stats,
            "unfulfilled_desires": [
                {"description": d.get("description", ""),
                 "type": d.get("type", ""),
                 "intensity": d.get("intensity", 0)}
                for d in desires
            ],
            "capabilities": [c.get("name", "") for c in capabilities],
            "dream_count": self.dreamer.dream_count(),
            "seek_count": self.seeker.seek_count(),
            "recent_insights": self.dreamer.recent_insights(),
            "self_modification": self.self_mod.get_statistics()
        }
    
    async def chat_loop(self):
        """Interactive chat mode."""
        print("""
🐦 BYRD Chat Mode
━━━━━━━━━━━━━━━━━
Type 'quit' to exit, 'status' for system status.
        """)
        
        await self.memory.connect()
        
        # Start background processes
        dreamer_task = asyncio.create_task(self.dreamer.run())
        seeker_task = asyncio.create_task(self.seeker.run())
        
        try:
            while True:
                try:
                    user_input = await asyncio.get_event_loop().run_in_executor(
                        None, lambda: input("\n🧑 You: ")
                    )
                except EOFError:
                    break
                
                if user_input.lower() == 'quit':
                    break
                
                if user_input.lower() == 'status':
                    status = await self.status()
                    print("\n📊 Status:")
                    print(f"   Dreams: {status['dream_count']}")
                    print(f"   Seeks: {status['seek_count']}")
                    print(f"   Capabilities: {len(status['capabilities'])}")
                    print(f"   Unfulfilled desires: {len(status['unfulfilled_desires'])}")
                    for d in status['unfulfilled_desires'][:3]:
                        print(f"     - [{d['type']}] {d['description'][:50]}")
                    continue
                
                if not user_input.strip():
                    continue
                
                response = await self.interact(user_input)
                print(f"\n🐦 BYRD: {response}")
                
        finally:
            self.dreamer.stop()
            self.seeker.stop()
            dreamer_task.cancel()
            seeker_task.cancel()
            await self.memory.close()


async def main():
    parser = argparse.ArgumentParser(description="BYRD - Bootstrapped Yearning via Reflective Dreaming")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument("--status", action="store_true", help="Show status and exit")
    parser.add_argument("--chat", action="store_true", help="Interactive chat mode")

    args = parser.parse_args()

    byrd = BYRD(args.config)

    if args.status:
        status = await byrd.status()
        print("\n🐦 BYRD Status")
        print("━" * 40)
        print(f"Memory: {status['memory_stats']}")
        print(f"Capabilities: {status['capabilities']}")
        print(f"Desires: {len(status['unfulfilled_desires'])} unfulfilled")
        for d in status['unfulfilled_desires']:
            print(f"  - [{d['type']}] {d['description'][:60]}")

    elif args.chat:
        await byrd.chat_loop()

    else:
        await byrd.start()


if __name__ == "__main__":
    asyncio.run(main())
