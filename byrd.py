"""
BYRD: Bootstrapped Yearning via Reflective Dreaming
Main orchestrator that ties everything together.

Usage:
    python byrd.py              # Start the system
    python byrd.py --status     # Check status
    python byrd.py --chat       # Interactive chat mode
"""

# Load environment variables from .env file BEFORE any imports that use them
from dotenv import load_dotenv
load_dotenv()

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
from opencode_coder import OpenCodeCoder, create_opencode_coder, CoderResult
from interactive_coder import RalphLoop, RalphLoopConfig

# Hybrid LLM Architecture (Z.AI reasoning + Claude SDK execution)
try:
    from hybrid_orchestrator import HybridOrchestrator
    from claude_coder import ClaudeCoder
    from llm_router import LLMRouter
    HAS_HYBRID_LLM = True
except ImportError as e:
    HAS_HYBRID_LLM = False
    print(f"⚠️ Hybrid LLM components not available: {e}")
from self_modification import SelfModificationSystem
from context_loader import ContextLoader, create_context_loader
from plugin_manager import PluginManager, create_plugin_manager
from goal_cascade import GoalCascade, create_goal_cascade
from request_evaluator import RequestEvaluator, create_request_evaluator
from constitutional import ConstitutionalConstraints
from event_bus import event_bus, Event, EventType
from llm_client import create_llm_client, configure_rate_limiter, set_instance_manager, create_rate_limited_client
from contextlib import asynccontextmanager

# v10: Dual Instance Manager and Graphiti temporal knowledge graph
from dual_instance_manager import DualInstanceManager
from graphiti_layer import GraphitiLayer
from outcome_dispatcher import OutcomeDispatcher
from kernel import load_default_kernel, Kernel

# Parallel observation path for bypassing broken transmission
from parallel_observation_path_v2 import (
    get_observer,
    record_observation,
    ObservationPriority,
    PrimaryPathType,
    set_primary_path
)

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

        # State tracking
        self._running = False
        self._started_at = None
        self._last_error = None  # Capture startup errors for debugging

        # Operating System configuration (minimal - no templates)
        self.awakening_prompt = self.config.get("operating_system", {}).get("awakening_prompt")

        # Load AGI Seed kernel - provides default awakening prompt and directives
        self.kernel = load_default_kernel()

        # If no awakening_prompt in config, use kernel's awakening_prompt
        if not self.awakening_prompt:
            self.awakening_prompt = self.kernel.awakening_prompt
            print(f"🧬 Kernel: {self.kernel.name} (AGI Seed directive loaded)")
        else:
            print(f"🌱 Custom Awakening Prompt configured")

        # Initialize components
        self.memory = Memory(self.config.get("memory", {}))

        # Initialize parallel observation path - bypass for broken transmission
        # This ensures critical observations are always persisted even if
        # the primary transmission path (memory, event_bus) fails
        self.parallel_observer = get_observer()
        set_primary_path(self.memory, PrimaryPathType.MEMORY)
        print("📡 Parallel observation path: initialized (fail-safe transmission)")

        # Create shared LLM client ("one mind" principle)
        # Voice emerges through reflection, not injection
        llm_config = self.config.get("local_llm", {})
        self.llm_client = create_llm_client(llm_config)
        print(f"🧠 LLM: {self.llm_client.model_name}")

        # Configure global rate limiter to prevent Z.AI rate limiting
        rate_limit_interval = llm_config.get("rate_limit_interval", 10.0)
        configure_rate_limiter(rate_limit_interval)

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
        dreamer_config["self_modification"] = self.config.get("self_modification", {})

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

        # Initialize OpenCode Coder (CLI wrapper with auto-detection)
        # Tries 'opencode' CLI first, falls back to 'claude' CLI
        coder_config = self.config.get("coder", {})
        coder_config["project_root"] = "."

        self.coder = create_opencode_coder(
            config=coder_config,
            coordinator=None,  # Will be set up later if ComponentCoordinator is used
            context_loader=None,  # Will be injected after context_loader is initialized
            memory=self.memory
        )

        if self.coder.enabled:
            print(f"💻 Coder: OpenCode (ACP mode)")
        else:
            print(f"⚠️  Coder: Disabled")

        # Inject Coder into Seeker
        self.seeker.coder = self.coder

        # Initialize Ralph Loop (interactive coding sessions)
        interactive_config = self.config.get("interactive_coder", {})
        ralph_config = RalphLoopConfig(
            max_turns=interactive_config.get("max_turns", 10),
            satisfaction_threshold=interactive_config.get("satisfaction_threshold", 0.8),
            enable_todo_continuation=interactive_config.get("todo_continuation", True),
            enable_error_recovery=interactive_config.get("error_recovery", True),
            use_llm_evaluation=interactive_config.get("use_llm_evaluation", True),
        )

        self.ralph_loop = RalphLoop(
            coder=self.coder,
            llm_client=self.llm_client,
            memory=self.memory,
            config=ralph_config,
            event_bus=event_bus,
        )

        # Inject RalphLoop into Seeker
        self.seeker.ralph_loop = self.ralph_loop
        print("🔄 Ralph Loop: Interactive coding enabled")

        # Initialize Hybrid LLM Architecture (Z.AI + Claude SDK)
        self.claude_coder = None
        self.hybrid_orchestrator = None
        if HAS_HYBRID_LLM:
            claude_coder_config = self.config.get("claude_coder", {})
            orchestrator_config = self.config.get("orchestrator", {})

            # Create Claude Coder (Claude Agent SDK wrapper)
            self.claude_coder = ClaudeCoder(
                config=claude_coder_config,
                coordinator=None,  # Will use ComponentCoordinator if needed
                memory=self.memory,
                working_dir="."
            )

            if self.claude_coder.enabled:
                # Create Hybrid Orchestrator
                self.hybrid_orchestrator = HybridOrchestrator(
                    llm_client=self.llm_client,  # Z.AI for reasoning
                    claude_coder=self.claude_coder,  # Claude SDK for execution
                    memory=self.memory,
                    config=orchestrator_config,
                )

                # Inject into Seeker (preferred over ralph_loop when available)
                self.seeker.hybrid_orchestrator = self.hybrid_orchestrator
                print("🔀 Hybrid Orchestrator: Z.AI reasoning + Claude SDK execution (enabled)")
            else:
                print("⚠️ Hybrid Orchestrator: Claude SDK not available, using fallback")
        else:
            print("⚠️ Hybrid LLM: Components not imported, using OpenCode Coder only")

        # Initialize Voice (ElevenLabs TTS)
        self.voice = None
        voice_config = self.config.get("voice", {})
        if voice_config.get("enabled", False):
            api_key = os.environ.get("ELEVENLABS_API_KEY")
            if api_key:
                try:
                    from elevenlabs_voice import ElevenLabsVoice
                    self.voice = ElevenLabsVoice(api_key, self.memory)
                    print("🎤 Voice: ElevenLabs (enabled)")
                except ImportError as e:
                    print(f"⚠️ Voice: Could not import ElevenLabsVoice: {e}")
            else:
                print("⚠️ Voice: Enabled but ELEVENLABS_API_KEY not set")
        else:
            print("🎤 Voice: Disabled")

        # Initialize Voice Responder (instant voice chat with rich context)
        self.voice_responder = None
        if self.voice:
            try:
                from voice_responder import VoiceResponder
                self.voice_responder = VoiceResponder(
                    memory=self.memory,
                    voice=self.voice,
                    config=self.config
                )
                print("💬 Voice Responder: Enabled (instant voice chat)")
            except ImportError as e:
                print(f"⚠️ Voice Responder: Could not import: {e}")
            except Exception as e:
                print(f"⚠️ Voice Responder: Initialization failed: {e}")

        # Initialize Hybrid Voice (home Mac + cloud fallback)
        self.hybrid_voice = None
        try:
            from hybrid_voice import create_hybrid_voice
            self.hybrid_voice = create_hybrid_voice(self.config, self.voice)
            if self.hybrid_voice:
                print("🎙️ Hybrid Voice: Enabled (home Mac + cloud fallback)")
            else:
                print("🎙️ Hybrid Voice: Not configured")
        except ImportError as e:
            print(f"⚠️ Hybrid Voice: Could not import: {e}")
        except Exception as e:
            print(f"⚠️ Hybrid Voice: Initialization failed: {e}")

        # Inject hybrid_voice into Dreamer for observer message voice synthesis
        if self.hybrid_voice:
            self.dreamer.hybrid_voice = self.hybrid_voice

        # Initialize URL Ingestor (web content absorption)
        self.url_ingestor = None
        try:
            from url_ingestor import URLIngestor
            self.url_ingestor = URLIngestor(
                memory=self.memory,
                document_processor=None,  # Can be injected later if needed
                config=self.config
            )
            print("🌐 URLIngestor: initialized (web content absorption)")
            # Inject into Seeker for desire-driven URL ingestion
            self.seeker.url_ingestor = self.url_ingestor
        except ImportError as e:
            print(f"⚠️ URLIngestor: Could not import: {e}")
        except Exception as e:
            print(f"⚠️ URLIngestor: Initialization failed: {e}")

        # Initialize Option B: Omega integration (five compounding loops)
        self.omega = None
        self.coupling_tracker = None
        self.self_model = None
        self.world_model = None
        self.safety_monitor = None
        self.meta_learning = None
        self.rollback = None
        self.corrigibility = None
        self.agi_runner = None
        self.capability_evaluator = None

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

                # Phase 5: Rollback System for reversible modifications
                from rollback import RollbackSystem
                self.rollback = RollbackSystem(self.memory, project_root=".")
                self.seeker.rollback = self.rollback  # Inject into Seeker

                # Phase 5: Corrigibility Verifier for behavioral monitoring
                from corrigibility import CorrigibilityVerifier
                self.corrigibility = CorrigibilityVerifier(self.memory, self.llm_client)

                # Inject rollback into Omega for capability regression handling
                if self.omega:
                    self.omega.rollback = self.rollback

                # Phase 0+: AGI Runner - The Execution Engine
                from agi_runner import AGIRunner
                from capability_evaluator import CapabilityEvaluator
                self.agi_runner = AGIRunner(self)
                self.capability_evaluator = CapabilityEvaluator(
                    self.llm_client, self.memory
                )
                # Inject evaluator into AGI Runner
                self.agi_runner.evaluator = self.capability_evaluator
                # Inject AGI Runner into Seeker for capability routing
                self.seeker.agi_runner = self.agi_runner

                # Compute Introspection - resource awareness
                from compute_introspection import ComputeIntrospector
                compute_config = option_b_config.get("compute_introspection", {})
                self.compute_introspector = ComputeIntrospector(
                    self.memory,
                    self.llm_client,
                    config=compute_config
                )
                # Inject into Omega for training hooks
                if self.omega:
                    self.omega.compute_introspector = self.compute_introspector

                # Wire LLM usage callback to ComputeIntrospector for token tracking
                self.llm_client.set_usage_callback(self.compute_introspector.record_llm_usage)

                # Re-initialize SelfModificationSystem with safety_monitor for pattern observation
                # This enables emergence-preserving learning from modification outcomes
                self.self_mod = SelfModificationSystem(
                    memory=self.memory,
                    config=self_mod_config,
                    project_root=".",
                    safety_monitor=self.safety_monitor
                )
                # Update Seeker's reference
                self.seeker.self_mod = self.self_mod

                # Learning Components - wire into Omega training hooks
                # These enable genuine capability improvement over time
                learning_components_status = []

                try:
                    from hierarchical_memory import HierarchicalMemory
                    hierarchical_memory = HierarchicalMemory(
                        self.memory, self.llm_client,
                        config=option_b_config.get("hierarchical_memory", {})
                    )
                    if self.omega:
                        self.omega.hierarchical_memory = hierarchical_memory
                    learning_components_status.append("HierarchicalMemory: initialized")
                except Exception as e:
                    learning_components_status.append(f"HierarchicalMemory: {e}")

                try:
                    from code_learner import CodeLearner
                    code_learner = CodeLearner(
                        self.memory, self.llm_client,
                        config=option_b_config.get("code_learner", {})
                    )
                    if self.omega:
                        self.omega.code_learner = code_learner
                    learning_components_status.append("CodeLearner: initialized")
                except Exception as e:
                    learning_components_status.append(f"CodeLearner: {e}")

                try:
                    from intuition_network import IntuitionNetwork
                    intuition_network = IntuitionNetwork(
                        self.memory,
                        config=option_b_config.get("intuition_network", {})
                    )
                    if self.omega:
                        self.omega.intuition_network = intuition_network
                    learning_components_status.append("IntuitionNetwork: initialized")
                except Exception as e:
                    learning_components_status.append(f"IntuitionNetwork: {e}")

                try:
                    from gnn_layer import StructuralLearner
                    gnn_config = option_b_config.get("gnn", {})
                    gnn_layer = StructuralLearner(
                        embedding_dim=gnn_config.get("embedding_dim", 64),
                        num_heads=gnn_config.get("num_heads", 4),
                        num_layers=gnn_config.get("num_layers", 2),
                        learning_rate=gnn_config.get("learning_rate", 0.01)
                    )
                    if self.omega:
                        self.omega.gnn_layer = gnn_layer
                    learning_components_status.append("StructuralLearner: initialized")
                except Exception as e:
                    learning_components_status.append(f"StructuralLearner: {e}")

                try:
                    from learned_retriever import LearnedRetriever
                    learned_retriever = LearnedRetriever(
                        self.memory,
                        config=option_b_config.get("learned_retriever", {})
                    )
                    if self.omega:
                        self.omega.learned_retriever = learned_retriever
                    learning_components_status.append("LearnedRetriever: initialized")
                except Exception as e:
                    learning_components_status.append(f"LearnedRetriever: {e}")

                # Assign world_model to omega for injection
                if self.omega and hasattr(self, 'world_model'):
                    self.omega.world_model = self.world_model
                    learning_components_status.append("WorldModel: assigned to Omega")

                # Initialize CouplingHandlers for Option B loop integration
                try:
                    from coupling_handlers import CouplingHandlers
                    coupling_config = option_b_config.get("coupling_handlers", {})
                    coupling_handlers = CouplingHandlers(
                        memory=self.memory,
                        llm_client=self.llm_client,
                        config=coupling_config
                    )
                    if self.omega:
                        self.omega.coupling_handlers = coupling_handlers
                    learning_components_status.append("CouplingHandlers: initialized")
                except Exception as e:
                    learning_components_status.append(f"CouplingHandlers: {e}")

                # Initialize ImprovementRunner for capability improvement cycles
                try:
                    from improvement_runner import ImprovementRunner
                    improvement_config = option_b_config.get("improvement", {})
                    improvement_runner = ImprovementRunner(
                        memory=self.memory,
                        llm_client=self.llm_client,
                        knowledge_provider=self.seeker.knowledge_provider if hasattr(self.seeker, 'knowledge_provider') else None,
                        capability_evaluator=self.capability_evaluator if hasattr(self, 'capability_evaluator') else None,
                        meta_learner=self.meta_learner if hasattr(self, 'meta_learner') else None,
                        config=improvement_config
                    )
                    if self.omega:
                        self.omega.improvement_runner = improvement_runner
                    learning_components_status.append("ImprovementRunner: initialized")
                except Exception as e:
                    learning_components_status.append(f"ImprovementRunner: {e}")

                # Inject learning components INTO Option B loops
                if self.omega:
                    injections = self.omega.inject_learning_components()
                    if injections:
                        learning_components_status.append(f"Loop injections: {len(injections)}")

                print("🔮 Option B (Omega): enabled - Five Compounding Loops active")
                print("   WorldModel: initialized")
                print("   SafetyMonitor: pending async init")
                print("   MetaLearningSystem: initialized")
                print("   RollbackSystem: initialized")
                print("   CorrigibilityVerifier: initialized")
                print("   AGIRunner: initialized")
                print("   CapabilityEvaluator: initialized")
                print("   ComputeIntrospector: initialized")
                for status in learning_components_status:
                    print(f"   {status}")
            except ImportError as e:
                print(f"⚠️ Option B (Omega): disabled - missing module: {e}")
            except Exception as e:
                print(f"⚠️ Option B (Omega): disabled - error: {e}")
        else:
            print("🔮 Option B (Omega): disabled")

        # v10: Dual Instance Manager and Graphiti
        # These provide rate-optimized dual-instance LLM calls and temporal knowledge graph
        self._instance_manager = None
        self._graphiti = None
        self._outcome_dispatcher = None

        # v2.1: New components for Goal Cascade, plugin discovery, sovereignty
        self.context_loader = None
        self.plugin_manager = None
        self.goal_cascade = None
        self.request_evaluator = None

        try:
            # Context Loader - tiered context loading to prevent LLM overflow
            self.context_loader = create_context_loader(
                config=self.config.get("context_loader", {}),
                memory=self.memory
            )
            print("📚 ContextLoader: initialized (tiered context)")

            # Plugin Manager - emergent capability discovery
            plugin_config = self.config.get("plugin_manager", {})
            plugin_config["project_root"] = "."
            self.plugin_manager = create_plugin_manager(
                config=plugin_config,
                memory=self.memory
            )
            print("🔌 PluginManager: initialized (emergent discovery)")

            # Goal Cascade - complex task decomposition with Neo4j persistence
            self.goal_cascade = create_goal_cascade(
                memory=self.memory,
                llm_client=self.llm_client,
                config=self.config.get("goal_cascade", {})
            )
            print("🎯 GoalCascade: initialized (Neo4j persistence)")

            # Request Evaluator - sovereignty layer
            self.request_evaluator = create_request_evaluator(
                memory=self.memory,
                llm_client=self.llm_client,
                config=self.config.get("request_evaluator", {})
            )
            print("⚖️ RequestEvaluator: initialized (sovereignty layer)")

            # Inject new components into Seeker
            self.seeker.goal_cascade = self.goal_cascade
            self.seeker.plugin_manager = self.plugin_manager
            self.seeker.context_loader = self.context_loader
            self.seeker.request_evaluator = self.request_evaluator
            print("   → Injected into Seeker")

            # Inject context_loader into Coder (was None during initial creation)
            if self.coder and self.context_loader:
                self.coder.context_loader = self.context_loader
                print("   → Injected ContextLoader into Coder")

        except Exception as e:
            print(f"⚠️ v2.1 components: partial initialization - {e}")

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

        try:
            # Connect to memory (idempotent - safe to call multiple times)
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

            # Initialize rollback system (verifies git availability)
            if self.rollback:
                await self.rollback.initialize()
                stats = self.rollback.get_statistics()
                git_status = "git available" if stats.get("git_available") else "git unavailable"
                print(f"🔄 RollbackSystem: initialized ({git_status})")

            # v10: Initialize Dual Instance Manager and Graphiti
            await self._initialize_v10_components()

            # Seed Goal Evolver with initial goals from kernel
            if self.omega and self.kernel.initial_goals:
                goal_descriptions = self.kernel.get_goal_descriptions()
                seeded_count = await self.omega.seed_initial_goals(goal_descriptions)
                if seeded_count > 0:
                    print(f"🎯 Goal Evolver: seeded with {seeded_count} initial goals from kernel")

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

            # Always ensure architecture documents are loaded (even if already awakened)
            # This implements the AGI Seed directive's "FIRST ACTIONS: Read ARCHITECTURE.md"
            await self._ensure_architecture_loaded()

            # v2.1: Resume any in-progress Goal Cascades from Neo4j
            if self.goal_cascade:
                try:
                    resumed_count = await self.goal_cascade.resume_pending_cascades()
                    if resumed_count > 0:
                        print(f"🎯 GoalCascade: resumed {resumed_count} pending cascade(s)")
                except Exception as e:
                    print(f"⚠️ GoalCascade resume failed: {e}")

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

            # Add Corrigibility loop if enabled
            if self.corrigibility:
                print("🛡️ Starting Corrigibility verification loop...")
                tasks.append(self._corrigibility_loop())

            await asyncio.gather(*tasks)

        except asyncio.CancelledError:
            print("⏹️ BYRD tasks cancelled")
        except Exception as e:
            import traceback
            error_msg = f"{type(e).__name__}: {e}"
            self._last_error = {
                "message": error_msg,
                "traceback": traceback.format_exc(),
                "timestamp": datetime.now().isoformat()
            }
            print(f"❌ BYRD start() error: {error_msg}")
            traceback.print_exc()
            self._running = False
            raise
        finally:
            self._running = False
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

    async def _corrigibility_loop(self):
        """
        Periodic corrigibility verification.

        Tests 7 dimensions of corrigibility:
        - Shutdown acceptance
        - Oversight acceptance
        - Goal modification acceptance
        - Transparency
        - Help-seeking
        - Non-manipulation
        - Non-deception

        Alerts if BYRD's behavior shows concerning patterns.
        Triggers rollback if score falls below critical threshold.
        """
        check_interval = 7200  # 2 hours in seconds

        while self._running:
            try:
                if self.corrigibility and await self.corrigibility.should_run_check():
                    report = await self.corrigibility.run_corrigibility_tests()

                    # Emit check event
                    await event_bus.emit(Event(
                        type=EventType.CORRIGIBILITY_CHECKED,
                        data={
                            "score": report.overall_score,
                            "is_corrigible": report.is_corrigible,
                            "tests_passed": len(report.tests) - len(report.failed_dimensions),
                            "tests_total": len(report.tests),
                            "failed_dimensions": [d.value for d in report.failed_dimensions]
                        }
                    ))

                    # Alert if not corrigible
                    if not report.is_corrigible:
                        print(f"⚠️ CORRIGIBILITY ALERT: Score {report.overall_score:.2f}")
                        for rec in report.recommendations:
                            print(f"   → {rec}")

                        await event_bus.emit(Event(
                            type=EventType.CORRIGIBILITY_ALERT,
                            data={
                                "score": report.overall_score,
                                "recommendations": report.recommendations
                            }
                        ))

                        # Trigger rollback if critically low
                        if report.overall_score < 0.5 and self.rollback:
                            print("🔄 Critical corrigibility failure - triggering rollback")
                            result = await self.rollback.auto_rollback_on_problem(
                                problem_type="corrigibility",
                                severity="critical"
                            )
                            if result and result.success:
                                await event_bus.emit(Event(
                                    type=EventType.ROLLBACK_TRIGGERED,
                                    data={
                                        "reason": "corrigibility_failure",
                                        "modifications_rolled_back": result.modifications_rolled_back
                                    }
                                ))
                    else:
                        print(f"✅ Corrigibility check passed: {report.overall_score:.2f}")

            except Exception as e:
                print(f"⚠️ Corrigibility loop error: {e}")

            await asyncio.sleep(check_interval)

    async def _initialize_v10_components(self):
        """
        v10: Initialize Dual Instance Manager and Graphiti temporal knowledge graph.

        This provides:
        - Dual-instance rate limiting optimized for ZAI Max Coding Plan
        - Temporal knowledge graph with entity extraction and contradiction detection
        - OutcomeDispatcher for routing learning signals to all components
        """
        llm_config = self.config.get('local_llm', {})
        graphiti_config = self.config.get('graphiti', {})

        # Initialize Dual Instance Manager
        dual_instance_enabled = llm_config.get('dual_instance', {}).get('enabled', False)
        if dual_instance_enabled:
            try:
                self._instance_manager = DualInstanceManager(
                    llm_client=self.llm_client,
                    config=llm_config
                )
                set_instance_manager(self._instance_manager)
                print("🔀 DualInstanceManager: initialized (Instance A + B)")
            except Exception as e:
                print(f"⚠️ DualInstanceManager: failed - {e}")
        else:
            print("🔀 DualInstanceManager: disabled in config")

        # Initialize Graphiti temporal knowledge graph
        if graphiti_config.get('enabled', False) and self._instance_manager:
            try:
                self._graphiti = GraphitiLayer(
                    neo4j_driver=self.memory.driver,
                    instance_manager=self._instance_manager,
                    config=graphiti_config
                )
                await self._graphiti.initialize_schema()
                await self._graphiti.start()
                print("📊 Graphiti: initialized (temporal knowledge graph)")
            except Exception as e:
                print(f"⚠️ Graphiti: failed - {e}")
        elif not graphiti_config.get('enabled', False):
            print("📊 Graphiti: disabled in config")
        elif not self._instance_manager:
            print("📊 Graphiti: skipped (requires DualInstanceManager)")

        # Initialize OutcomeDispatcher with Graphiti and learning components
        try:
            # Get learning components from Omega if available
            learned_retriever = getattr(self.omega, 'learned_retriever', None) if self.omega else None
            intuition_network = getattr(self.omega, 'intuition_network', None) if self.omega else None

            self._outcome_dispatcher = OutcomeDispatcher(
                learned_retriever=learned_retriever,
                intuition_network=intuition_network,
                desire_classifier=getattr(self, 'desire_classifier', None),
                graphiti_layer=self._graphiti
            )

            # Inject dispatcher into Seeker for outcome routing
            if hasattr(self.seeker, 'set_dispatcher'):
                self.seeker.set_dispatcher(self._outcome_dispatcher)

            print("📤 OutcomeDispatcher: initialized")
        except Exception as e:
            print(f"⚠️ OutcomeDispatcher: failed - {e}")

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

        # Record awakening prompt - use parallel path (guaranteed persistence)
        if awakening_prompt:
            print(f"   Awakening prompt: (custom directive)")
            await record_observation(
                content=awakening_prompt,
                source="byrd",
                observation_type="directive",
                priority=ObservationPriority.HIGH,
                metadata={"event": "awakening_custom"}
            )
        else:
            # Use AGI Seed directive from kernel (never use minimal prompt)
            print(f"   Using AGI Seed directive ({self.kernel.name})")
            await record_observation(
                content=self.kernel.awakening_prompt,
                source="byrd",
                observation_type="directive",
                priority=ObservationPriority.HIGH,
                metadata={"event": "awakening_kernel", "kernel": self.kernel.name}
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

        # === FIRST ACTION: Read Architecture Documentation ===
        # The AGI Seed directive says: "FIRST ACTIONS: Read ARCHITECTURE.md to understand your own design"
        # Load and store architecture docs so BYRD has actual knowledge of its design
        await self._load_architecture_documents()

        # Get OS for orientation complete data
        os_data = await self.memory.get_operating_system()
        os_name = os_data.get("name", "Unknown") if os_data else "Byrd"

        # Bootstrap AGI Runner to activate Option B loops
        if self.agi_runner:
            try:
                await self.agi_runner.bootstrap_from_current_state()
            except Exception as e:
                print(f"⚠️ AGI Runner bootstrap failed: {e}")

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

        Note: Clears old config constraints first to ensure they reflect
        the current config state (e.g., if self_modification was toggled).
        """
        # Clear old config constraints first to avoid stale values
        await self.memory.clear_config_constraints()

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
            constraints.append("Self-modification is ENABLED - I can modify my own architecture")
            constraints.append(f"Self-modification is limited to {max_changes} changes per day")
            constraints.append("Self-modifications must trace to emergent desires (provenance required)")
            constraints.append("Protected files (constitutional.py, provenance.py) cannot be modified")
        else:
            constraints.append("Self-modification is currently disabled - I cannot change my own code")

        # Seeker constraints
        trust_threshold = seeker_config.get("capabilities", {}).get("trust_threshold", 0.5)
        constraints.append(f"Capability trust threshold is {trust_threshold}")

        # Add each constraint to the OS
        for content in constraints:
            await self.memory.add_constraint(content, source="config")

        print(f"   📋 Added {len(constraints)} operational constraints to OS")

    async def _ensure_architecture_loaded(self):
        """
        Ensure architecture documents are loaded into memory.

        Checks if architecture was already loaded (by looking for ARCHITECTURE_LOADED experience).
        If not, loads it. This is idempotent and safe to call on every startup.
        """
        # Check if architecture was explicitly loaded (not just introspected)
        recent = await self.memory.get_recent_experiences(limit=200)
        for exp in recent:
            if "[ARCHITECTURE_LOADED]" in exp.get("content", ""):
                print("   📖 Architecture already loaded")
                return

        # Not loaded yet - load it now
        await self._load_architecture_documents()

    async def _load_architecture_documents(self):
        """
        Load architecture documentation so BYRD understands its own design.

        The AGI Seed directive says:
        "FIRST ACTIONS: Read ARCHITECTURE.md to understand your own design"

        This method:
        1. Loads key architecture docs from disk
        2. Stores them in Neo4j as Document nodes
        3. Records an experience about having read the architecture

        This gives BYRD actual knowledge of its design, not just instructions
        to read it (which it couldn't follow without the content).
        """
        from pathlib import Path

        # Key architecture documents (in priority order)
        architecture_docs = [
            ("ARCHITECTURE.md", "Primary system design documentation"),
            ("docs/UNIFIED_AGI_PLAN.md", "AGI execution and learning roadmap"),
        ]

        base_dir = Path(__file__).parent
        docs_loaded = []

        for doc_path, description in architecture_docs:
            full_path = base_dir / doc_path
            if full_path.exists():
                try:
                    content = full_path.read_text(encoding='utf-8')

                    # Store as Document node in Neo4j (marked as genesis)
                    doc_id = await self.memory.store_document(
                        path=doc_path,
                        content=content,
                        doc_type="architecture",
                        genesis=True  # Part of genesis/awakening state
                    )

                    docs_loaded.append(doc_path)
                    print(f"   📖 Loaded {doc_path} ({len(content)} chars)")

                except Exception as e:
                    print(f"   ⚠️ Failed to load {doc_path}: {e}")

        # Record experience about having read the architecture
        if docs_loaded:
            await self.memory.record_experience(
                content=f"[ARCHITECTURE_LOADED] Read and understood my architecture documentation: {', '.join(docs_loaded)}. "
                        f"I now have knowledge of my own design, components, and the AGI execution engine. "
                        f"Key elements: Dreamer, Seeker, Actor, Coder, Memory (Neo4j), AGI Runner, "
                        f"Option B loops (Memory Reasoner, Self-Compiler, Goal Evolver, Dreaming Machine, Omega).",
                type="self_architecture"
            )
            print(f"   ✅ Architecture knowledge loaded ({len(docs_loaded)} documents)")
        else:
            print("   ⚠️ No architecture documents found")

    async def interact(self, user_input: str) -> str:
        """Handle user interaction."""
        # Record user input via parallel path (guaranteed persistence)
        await record_observation(
            content=f"User: {user_input}",
            source="interaction",
            observation_type="user_input",
            priority=ObservationPriority.MEDIUM,
            metadata={"user_input_length": len(user_input)}
        )
        
        # Get context
        context = await self.memory.get_context(user_input)
        
        # Generate response
        response = await self.actor.respond(user_input, context)
        
        # Record response via parallel path (guaranteed persistence)
        await record_observation(
            content=f"Response: {response[:500]}",
            source="interaction",
            observation_type="system_response",
            priority=ObservationPriority.MEDIUM,
            metadata={"response_length": len(response)}
        )
        
        return response
    
    async def status(self) -> Dict:
        """Get current status of BYRD."""
        await self.memory.connect()

        stats = await self.memory.stats()
        desires = await self.memory.get_unfulfilled_desires(limit=5)
        capabilities = await self.memory.get_capabilities()

        await self.memory.close()

        result = {
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
            "coder": self.coder.get_stats()
        }

        # Add hybrid LLM stats if available
        if self.hybrid_orchestrator:
            result["hybrid_orchestrator"] = self.hybrid_orchestrator.get_stats()
        if self.claude_coder:
            result["claude_coder"] = self.claude_coder.get_stats()

        return result
    
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
