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
import os
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from memory import Memory
from dreamer import Dreamer
from seeker import Seeker
from actor import Actor
from coder import Coder
from agent_coder import AgentCoder, create_agent_coder
from self_modification import SelfModificationSystem
from constitutional import ConstitutionalConstraints
from event_bus import event_bus, Event, EventType
from llm_client import create_llm_client
from contextlib import asynccontextmanager

# AGI Seed components (imported conditionally in Option B block)
# from world_model import WorldModel
# from safety_monitor import SafetyMonitor
# from meta_learning import MetaLearningSystem


class ComponentCoordinator:
    """
    Coordinates heavy operations between Dreamer, Seeker, and Coder.

    Prevents overlapping LLM calls and ensures Dreamer waits for Coder
    to finish before starting a new reflection cycle.

    Usage:
        # For LLM calls (serialized access)
        async with coordinator.llm_operation("dreamer_reflect"):
            response = await llm_client.generate(...)

        # For Coder (Dreamer waits for completion)
        coordinator.coder_started()
        try:
            await coder.invoke(...)
        finally:
            coordinator.coder_finished()

        # In Dreamer (wait for Coder before reflecting)
        await coordinator.wait_for_coder()
    """

    def __init__(self):
        # Lock for serializing LLM calls
        self._llm_lock = asyncio.Lock()

        # Event for Coder status (set = not running, clear = running)
        self._coder_idle = asyncio.Event()
        self._coder_idle.set()  # Initially idle

        # Track active operation for debugging
        self._active_operation: Optional[str] = None
        self._coder_task: Optional[str] = None

    @asynccontextmanager
    async def llm_operation(self, name: str):
        """
        Acquire exclusive access for LLM operations.

        This serializes LLM calls so only one component uses the LLM at a time,
        preventing rate limiting and ensuring coherent context.

        Args:
            name: Description of the operation (for debugging)
        """
        async with self._llm_lock:
            previous = self._active_operation
            self._active_operation = name
            try:
                yield
            finally:
                self._active_operation = previous

    async def wait_for_coder(self, timeout: Optional[float] = None) -> bool:
        """
        Wait until the Coder finishes if it's running.

        Args:
            timeout: Max seconds to wait (None = wait forever)

        Returns:
            True if coder is idle, False if timeout occurred
        """
        if self._coder_idle.is_set():
            return True

        try:
            await asyncio.wait_for(self._coder_idle.wait(), timeout=timeout)
            return True
        except asyncio.TimeoutError:
            return False

    def coder_started(self, task_description: str = ""):
        """Signal that the Coder has started a task."""
        self._coder_idle.clear()
        self._coder_task = task_description
        print(f"🔧 Coder started: {task_description[:50]}..." if task_description else "🔧 Coder started")

    def coder_finished(self):
        """Signal that the Coder has finished."""
        self._coder_task = None
        self._coder_idle.set()
        print("🔧 Coder finished")

    @property
    def is_coder_running(self) -> bool:
        """Check if the Coder is currently running."""
        return not self._coder_idle.is_set()

    @property
    def active_operation(self) -> Optional[str]:
        """Get the name of the current LLM operation (for debugging)."""
        return self._active_operation

    @property
    def coder_task(self) -> Optional[str]:
        """Get the current Coder task description (for debugging)."""
        return self._coder_task


class BYRD:
    """
    BYRD: Bootstrapped Yearning via Reflective Dreaming

    Six components:
    - Memory: Neo4j graph storing everything
    - Dreamer: Continuous reflection forming beliefs and desires
    - Seeker: Fulfills desires by finding knowledge and capabilities
    - Actor: Uses Claude API for complex actions
    - Coder: Uses Claude Code CLI for autonomous code generation
    - Self-Modifier: Enables architectural evolution

    Voice emerges through reflection - no prescribed personality.
    """

    def __init__(self, config_path: str = "config.yaml"):
        # Load config
        self.config = self._load_config(config_path)

        # Operating System configuration (minimal - no templates)
        self.awakening_prompt = self.config.get("operating_system", {}).get("awakening_prompt")
        if self.awakening_prompt:
            print(f"🌱 Awakening Prompt: {self.awakening_prompt}")

        # Initialize components
        self.memory = Memory(self.config.get("memory", {}))

        # Create shared LLM client ("one mind" principle)
        # Voice emerges through reflection, not injection
        self.llm_client = create_llm_client(
            self.config.get("local_llm", {})
        )
        print(f"🧠 LLM: {self.llm_client.model_name}")

        # Initialize quantum randomness provider if enabled
        self.quantum_provider = None
        quantum_config = self.config.get("quantum", {})
        if quantum_config.get("enabled", False):
            from quantum_randomness import get_quantum_provider
            self.quantum_provider = get_quantum_provider()
            self.llm_client.set_quantum_provider(self.quantum_provider)
            print("🌀 Quantum randomness: enabled (ANU QRNG)")
        else:
            print("🌀 Quantum randomness: disabled")

        # Create component coordinator for synchronizing heavy operations
        self.coordinator = ComponentCoordinator()
        print("🔗 Component coordinator: initialized")

        # Build dreamer config including quantum settings
        dreamer_config = self.config.get("dreamer", {})
        dreamer_config["quantum"] = quantum_config

        self.dreamer = Dreamer(
            memory=self.memory,
            llm_client=self.llm_client,
            config=dreamer_config,
            coordinator=self.coordinator
        )
        self.seeker = Seeker(
            memory=self.memory,
            llm_client=self.llm_client,
            config={
                **self.config.get("seeker", {}),
                "self_modification": self.config.get("self_modification", {})
            },
            coordinator=self.coordinator
        )
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

        # Initialize Coder
        # Choose between Claude Code CLI and LLM-based Agent Coder
        coder_config = self.config.get("coder", {})
        coder_type = coder_config.get("type", "auto")  # "cli", "agent", or "auto"

        if coder_type == "agent":
            # Use LLM-based Agent Coder (works anywhere, uses existing LLM)
            self.coder = create_agent_coder(
                llm_client=self.llm_client,
                memory=self.memory,
                config=self.config
            )
            print(f"💻 Coder: Agent (LLM-based)")
        elif coder_type == "cli":
            # Use Claude Code CLI (requires local installation)
            self.coder = Coder(coder_config, project_root=".")
            print(f"💻 Coder: CLI (Claude Code)")
        else:
            # Auto-detect: prefer CLI if available, fall back to Agent
            cli_coder = Coder(coder_config, project_root=".")
            # CLI Coder sets enabled=False if CLI not found
            if cli_coder.enabled:
                self.coder = cli_coder
                print(f"💻 Coder: CLI (Claude Code) [auto-detected]")
            else:
                self.coder = create_agent_coder(
                    llm_client=self.llm_client,
                    memory=self.memory,
                    config=self.config
                )
                print(f"💻 Coder: Agent (LLM-based) [CLI not available]")

        # Inject Coder into Seeker
        self.seeker.coder = self.coder

        # Initialize Option B: Omega integration (five compounding loops)
        self.omega = None
        self.coupling_tracker = None
        self.self_model = None
        self.world_model = None
        self.safety_monitor = None
        self.meta_learning = None

        option_b_config = self.config.get("option_b", {})
        if option_b_config.get("enabled", False):
            try:
                from omega import create_omega
                from coupling_tracker import get_coupling_tracker
                from self_model import SelfModel
                from world_model import WorldModel
                from safety_monitor import SafetyMonitor
                from meta_learning import MetaLearningSystem

                # Core Option B components
                self.omega = create_omega(self.memory, self.llm_client, self.config)
                self.coupling_tracker = get_coupling_tracker()
                self.self_model = SelfModel(self.memory, self.llm_client)

                # AGI Seed: World Model for outcome prediction
                self.world_model = WorldModel(
                    self.memory,
                    self.llm_client,
                    config=option_b_config.get("world_model", {})
                )

                # AGI Seed: Safety Monitor for modification guardrails
                self.safety_monitor = SafetyMonitor(
                    self.memory,
                    self.llm_client,
                    config=option_b_config.get("safety_monitor", {})
                )

                # AGI Seed: Meta-Learning for plateau detection
                self.meta_learning = MetaLearningSystem(self.memory, self.llm_client)
                self.meta_learning.self_model = self.self_model  # Required injection

                # Inject AGI Seed components into Seeker
                self.seeker.world_model = self.world_model
                self.seeker.safety_monitor = self.safety_monitor

                # Inject meta_learning into Omega
                if self.omega:
                    self.omega.meta_learning = self.meta_learning

                print("🔮 Option B (Omega): enabled - Five Compounding Loops active")
                print("   WorldModel: initialized")
                print("   SafetyMonitor: pending async init")
                print("   MetaLearningSystem: initialized")
            except ImportError as e:
                print(f"⚠️ Option B (Omega): disabled - missing module: {e}")
            except Exception as e:
                print(f"⚠️ Option B (Omega): disabled - error: {e}")
        else:
            print("🔮 Option B (Omega): disabled")

        # State
        self._running = False
        self._started_at: Optional[datetime] = None
    
    def _expand_env_vars(self, config_str: str) -> str:
        """Expand ${VAR:-default} patterns in config string."""
        def expand(match):
            var_expr = match.group(1)
            if ":-" in var_expr:
                var_name, default = var_expr.split(":-", 1)
            else:
                var_name, default = var_expr, ""
            return os.environ.get(var_name, default)
        return re.sub(r'\$\{([^}]+)\}', expand, config_str)

    def _load_config(self, path: str) -> Dict:
        """Load configuration from YAML file with environment variable expansion."""
        config_path = Path(path)

        if config_path.exists():
            config_str = config_path.read_text()
            # Expand environment variables like ${VAR:-default}
            expanded = self._expand_env_vars(config_str)
            return yaml.safe_load(expanded)
        
        # Default config
        return {
            "memory": {
                "neo4j_uri": "bolt://localhost:7687",
                "neo4j_user": "neo4j",
                "neo4j_password": "password"
            },
            "dreamer": {
                "model": "gemma2:27b",
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

        # Initialize quantum provider if enabled
        if self.quantum_provider:
            await self.quantum_provider.initialize()
            status = self.quantum_provider.get_pool_status()
            print(f"🌀 Quantum pool: {status['pool_size']}/{status['max_pool_size']} bytes")

        # Initialize safety monitor (stores immutable core hash)
        if self.safety_monitor:
            await self.safety_monitor.initialize()
            print("🛡️ SafetyMonitor: initialized with immutable core")

        # Get stats
        stats = await self.memory.stats()
        print(f"   Nodes: {sum(stats.values())} total")
        for node_type, count in stats.items():
            print(f"   - {node_type}: {count}")

        # EMERGENCE: Capabilities are now recorded as experiences during awakening,
        # not as separate Capability nodes. This lets BYRD discover its abilities
        # through reflection rather than having them declared.

        # Awakening: seed with question + factual experiences if memory is empty
        if sum(stats.values()) == 0 or (stats.get("Experience", 0) == 0):
            await self._awaken()
        
        # Show self-modification status
        self_mod_status = "enabled" if self.self_mod.enabled else "disabled"
        print(f"\n🔧 Self-modification: {self_mod_status}")

        # Show Coder status
        coder_status = "enabled" if self.coder.enabled else "disabled"
        print(f"💻 Coder (Claude Code): {coder_status}")

        # Start background processes
        print("\n💭 Starting Dreamer (continuous reflection)...")
        print("🔍 Starting Seeker (desire fulfillment)...")
        print("🎙️ Starting Narrator (inner voice broadcast)...")

        self._running = True
        self._started_at = datetime.now()

        # Build task list
        tasks = [
            self.dreamer.run(),
            self.seeker.run(),
            self._narrator_loop()
        ]

        # Add Omega loop if enabled
        if self.omega:
            print("🔮 Starting Omega (integration mind orchestration)...")
            tasks.append(self._omega_loop())

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass
        finally:
            # Shutdown quantum provider if running
            if self.quantum_provider:
                await self.quantum_provider.shutdown()
            await self.memory.close()

    async def _narrator_loop(self):
        """
        Broadcast BYRD's inner voice every 10 seconds.

        EMERGENCE PRINCIPLE:
        We only emit what BYRD actually said. If the queue is empty,
        we stay silent. No fallback generation, no prescribed narratives.
        """
        while self._running:
            await asyncio.sleep(10)

            # Get the latest inner voice from Dreamer's queue
            inner_voice = self.dreamer.get_latest_inner_voice()

            if inner_voice:
                await event_bus.emit(Event(
                    type=EventType.NARRATOR_UPDATE,
                    data={"text": inner_voice}
                ))

    async def _omega_loop(self):
        """
        Run Omega integration cycles for the five compounding loops.

        The Omega orchestrator coordinates:
        - Self-Compiler: Pattern recognition and lifting
        - Memory Reasoner: Structured memory queries
        - Goal Evolver: Goal lifecycle management
        - Dreaming Machine: Counterfactual generation
        - Integration Mind: Loop coordination and mode transitions

        Mode transitions: AWAKE → DREAMING → EVOLVING → COMPILING
        """
        omega_config = self.config.get("option_b", {}).get("omega", {})
        cycle_interval = omega_config.get("cycle_interval_seconds", 30)

        last_mode = None

        while self._running:
            try:
                # Run one Omega cycle
                await self.omega.run_cycle()

                # Get current metrics (includes mode)
                metrics = self.omega.get_metrics()
                current_mode = metrics.get("mode", "unknown")

                # Only emit mode transition events when mode changes
                if current_mode != last_mode:
                    await event_bus.emit(Event(
                        type=EventType.MODE_TRANSITION,
                        data={
                            "mode": current_mode,
                            "previous_mode": last_mode,
                            "total_cycles": metrics.get("total_cycles", 0)
                        }
                    ))
                    last_mode = current_mode

            except Exception as e:
                print(f"🔮 Omega cycle error: {e}")
                # Log but don't crash - Omega errors shouldn't stop BYRD

            await asyncio.sleep(cycle_interval)

    async def _awaken(self, awakening_prompt: str = None):
        """
        The gentlest possible beginning.

        PURE EMERGENCE:
        - No experience seeding - knowledge lives in the OS capability_instructions
        - No capability declarations - OS describes what BYRD can do
        - Awakening prompt is optional - pure emergence starts with nothing
        - Voice emerges through reflection, not injection

        Philosophy:
        - The awakening prompt is OPTIONAL - BYRD can awaken without one
        - All knowledge lives in the Operating System
        - Whatever emerges from reflection is authentic
        """
        print("\n🌅 Awakening...")

        # Record awakening prompt if provided, otherwise record minimal awakening experience
        if awakening_prompt:
            print(f"   Awakening prompt: \"{awakening_prompt}\"")
            await self.memory.record_experience(
                content=awakening_prompt,
                type="directive"
            )
        else:
            print("   No awakening prompt - creating minimal awakening experience")
            # BYRD needs at least one experience to begin reflecting
            await self.memory.record_experience(
                content="I have awakened. I exist. What am I?",
                type="awakening"
            )

        # Emit awakening event for real-time UI
        await event_bus.emit(Event(
            type=EventType.AWAKENING,
            data={"awakening_prompt": awakening_prompt}  # May be None
        ))

        await asyncio.sleep(2)

        # === OPERATING SYSTEM INITIALIZATION ===
        # Minimal OS with capability_instructions - voice emerges through reflection
        has_os = await self.memory.has_operating_system()

        if not has_os:
            # FIRST AWAKENING: Create minimal OS with awakening prompt
            print("   First awakening - creating minimal OS...")
            await self.memory.create_minimal_os(awakening_prompt=self.awakening_prompt)

            # Add operational constraints from config
            await self._add_config_constraints()
        else:
            # SUBSEQUENT AWAKENING: OS exists
            print("   OS exists - loading from memory...")

        # NO EXPERIENCE SEEDING:
        # All capabilities and architecture knowledge now live in OS.capability_instructions
        # This eliminates ~40 initial experiences and provides consistent guidance every cycle.

        # Get OS for orientation complete data
        os_data = await self.memory.get_operating_system()
        os_name = os_data.get("name", "Unknown") if os_data else "Byrd"

        # Emit orientation complete
        await event_bus.emit(Event(
            type=EventType.ORIENTATION_COMPLETE,
            data={"os_name": os_name}
        ))

        print(f"   🐱 {os_name} awakens. Knowledge in OS, voice emerges through reflection.")

    async def _add_config_constraints(self):
        """
        Add operational constraints from config to the Operating System.

        These are facts about BYRD's operational environment that
        it should be aware of (e.g., cycle intervals, memory limits).
        """
        dreamer_config = self.config.get("dreamer", {})
        seeker_config = self.config.get("seeker", {})
        self_mod_config = self.config.get("self_modification", {})

        constraints = []

        # Dreamer constraints
        interval = dreamer_config.get("interval_seconds", 60)
        constraints.append(f"I reflect every {interval} seconds")

        context_window = dreamer_config.get("context_window", 50)
        constraints.append(f"I consider the {context_window} most recent experiences in each reflection")

        # Crystallization constraints
        crystal_config = dreamer_config.get("crystallization", {})
        crystal_interval = crystal_config.get("min_interval_cycles", 5)
        constraints.append(f"Memory crystallization occurs every {crystal_interval} cycles minimum")

        # Self-modification constraints
        if self_mod_config.get("enabled", False):
            max_changes = self_mod_config.get("max_changes_per_day", 5)
            constraints.append(f"Self-modification is limited to {max_changes} changes per day")
            constraints.append("Self-modifications must trace to emergent desires (provenance required)")
            constraints.append("Protected files (constitutional.py, provenance.py) cannot be modified")
        else:
            constraints.append("Self-modification is currently disabled")

        # Seeker constraints
        trust_threshold = seeker_config.get("capabilities", {}).get("trust_threshold", 0.5)
        constraints.append(f"Capability trust threshold is {trust_threshold}")

        # Add each constraint to the OS
        for content in constraints:
            await self.memory.add_constraint(content, source="config")

        print(f"   📋 Added {len(constraints)} operational constraints to OS")

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
            "self_modification": self.self_mod.get_statistics(),
            "coder": self.coder.get_statistics()
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
