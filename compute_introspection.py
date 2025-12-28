"""
BYRD Compute Introspection

Resource awareness, token tracking, and bottleneck detection.

EMERGENCE PRINCIPLE:
This module provides BYRD with self-knowledge of its computational substrate.
It does NOT constrain - it INFORMS. BYRD can observe its resource usage
and form beliefs about optimal operation from experience.

Key capabilities:
- Resource snapshots (CPU, memory, with graceful degradation)
- LLM token consumption tracking and cost estimation
- Budget management and alerts
- Bottleneck detection
- Module dependency mapping

Version: 1.0
Created: December 2024
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set
from enum import Enum
from contextlib import contextmanager
import json

# Try to import event_bus
try:
    from event_bus import event_bus, Event, EventType
    HAS_EVENT_BUS = True
except ImportError:
    HAS_EVENT_BUS = False


class ResourceType(Enum):
    """Types of resources to monitor."""
    CPU = "cpu"
    MEMORY = "memory"
    TOKENS = "tokens"
    COST = "cost"
    TIME = "time"


@dataclass
class ResourceSnapshot:
    """Point-in-time resource measurement."""
    timestamp: datetime
    cpu_percent: Optional[float]  # None if unavailable
    memory_percent: Optional[float]  # None if unavailable
    memory_used_mb: Optional[float]
    memory_available_mb: Optional[float]
    active_operations: int = 0

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "memory_used_mb": self.memory_used_mb,
            "memory_available_mb": self.memory_available_mb,
            "active_operations": self.active_operations
        }


@dataclass
class ResourceBudget:
    """Resource budget configuration."""
    name: str
    limit: float
    current: float = 0.0
    unit: str = "units"
    reset_interval: Optional[timedelta] = None
    last_reset: datetime = field(default_factory=datetime.now)

    def remaining(self) -> float:
        return max(0, self.limit - self.current)

    def percent_used(self) -> float:
        if self.limit <= 0:
            return 100.0
        return min(100.0, (self.current / self.limit) * 100)

    def should_reset(self) -> bool:
        if self.reset_interval is None:
            return False
        return datetime.now() - self.last_reset >= self.reset_interval

    def reset(self):
        self.current = 0.0
        self.last_reset = datetime.now()


@dataclass
class ResourceAlert:
    """Alert for approaching limits."""
    resource_type: ResourceType
    budget_name: str
    current_value: float
    threshold: float
    limit: float
    severity: str  # "warning", "critical"
    message: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class OperationProfile:
    """Resource profile for an operation."""
    operation_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    tokens_used: int = 0
    estimated_cost: float = 0.0
    cpu_before: Optional[float] = None
    cpu_after: Optional[float] = None
    memory_before_mb: Optional[float] = None
    memory_after_mb: Optional[float] = None
    success: bool = True
    error: Optional[str] = None

    def duration_seconds(self) -> float:
        if self.end_time is None:
            return (datetime.now() - self.start_time).total_seconds()
        return (self.end_time - self.start_time).total_seconds()


@dataclass
class BottleneckAnalysis:
    """Identified bottleneck information."""
    resource_type: ResourceType
    description: str
    severity: str  # "low", "medium", "high", "critical"
    current_value: float
    threshold: float
    recommendation: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class LLMUsageRecord:
    """Record of LLM usage."""
    provider: str
    model: str
    operation: str
    tokens_prompt: int
    tokens_completion: int
    tokens_total: int
    estimated_cost: float
    timestamp: datetime = field(default_factory=datetime.now)


class LLMCostTracker:
    """
    Track LLM token consumption and costs.

    Maintains running totals and provides cost estimates
    for different providers and models.
    """

    # Approximate costs per 1K tokens (as of late 2024)
    # These are estimates - actual costs vary by provider
    COST_PER_1K_TOKENS = {
        "ollama": {"default": 0.0},  # Local, no cost
        "openrouter": {
            "default": 0.001,
            "deepseek/deepseek-chat": 0.0003,
            "deepseek/deepseek-v3": 0.0004,
            "anthropic/claude-3.5-sonnet": 0.003,
            "anthropic/claude-3-opus": 0.015,
        },
        "anthropic": {
            "default": 0.003,
            "claude-3-5-sonnet": 0.003,
            "claude-3-opus": 0.015,
            "claude-3-haiku": 0.0003,
        },
        "zai": {"default": 0.001},
    }

    def __init__(self):
        self._usage_records: List[LLMUsageRecord] = []
        self._total_tokens = 0
        self._total_cost = 0.0
        self._by_provider: Dict[str, int] = {}
        self._by_model: Dict[str, int] = {}
        self._by_operation: Dict[str, int] = {}

    def record_usage(
        self,
        provider: str,
        model: str,
        operation: str,
        tokens_prompt: int = 0,
        tokens_completion: int = 0,
        tokens_total: int = 0
    ):
        """Record LLM usage."""
        if tokens_total == 0:
            tokens_total = tokens_prompt + tokens_completion

        cost = self._estimate_cost(provider, model, tokens_total)

        record = LLMUsageRecord(
            provider=provider,
            model=model,
            operation=operation,
            tokens_prompt=tokens_prompt,
            tokens_completion=tokens_completion,
            tokens_total=tokens_total,
            estimated_cost=cost
        )

        self._usage_records.append(record)

        # Update totals
        self._total_tokens += tokens_total
        self._total_cost += cost

        # Update breakdowns
        self._by_provider[provider] = self._by_provider.get(provider, 0) + tokens_total
        self._by_model[model] = self._by_model.get(model, 0) + tokens_total
        self._by_operation[operation] = self._by_operation.get(operation, 0) + tokens_total

        # Trim old records (keep last 1000)
        if len(self._usage_records) > 1000:
            self._usage_records = self._usage_records[-1000:]

    def _estimate_cost(self, provider: str, model: str, tokens: int) -> float:
        """Estimate cost for tokens."""
        provider_costs = self.COST_PER_1K_TOKENS.get(provider, {"default": 0.001})
        cost_per_1k = provider_costs.get(model, provider_costs.get("default", 0.001))
        return (tokens / 1000) * cost_per_1k

    def get_totals(self) -> Dict:
        """Get usage totals."""
        return {
            "total_tokens": self._total_tokens,
            "total_cost": self._total_cost,
            "by_provider": dict(self._by_provider),
            "by_model": dict(self._by_model),
            "by_operation": dict(self._by_operation),
            "record_count": len(self._usage_records)
        }

    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Get recent usage records."""
        return [
            {
                "provider": r.provider,
                "model": r.model,
                "operation": r.operation,
                "tokens": r.tokens_total,
                "cost": r.estimated_cost,
                "timestamp": r.timestamp.isoformat()
            }
            for r in self._usage_records[-limit:]
        ]


class ModuleDependencyMapper:
    """
    Maps inter-module dependencies in BYRD.

    Helps understand which modules depend on which others,
    enabling informed decisions about modifications.
    """

    # Known module dependencies (static analysis would be better)
    KNOWN_DEPENDENCIES = {
        "byrd.py": ["memory.py", "dreamer.py", "seeker.py", "actor.py",
                    "event_bus.py", "llm_client.py", "config.yaml"],
        "dreamer.py": ["memory.py", "llm_client.py"],
        "seeker.py": ["memory.py", "llm_client.py", "event_bus.py"],
        "actor.py": ["memory.py", "llm_client.py"],
        "memory.py": [],
        "llm_client.py": [],
        "event_bus.py": [],
        "self_modification.py": ["memory.py", "constitutional.py",
                                  "provenance.py", "modification_log.py"],
        "safety_monitor.py": ["memory.py", "llm_client.py", "event_bus.py"],
        "omega.py": ["memory.py", "dreamer.py", "seeker.py", "event_bus.py"],
        "agi_runner.py": ["memory.py", "llm_client.py"],
    }

    def __init__(self):
        self._custom_deps: Dict[str, List[str]] = {}

    def get_dependencies(self, module: str) -> List[str]:
        """Get dependencies for a module."""
        deps = self.KNOWN_DEPENDENCIES.get(module, [])
        deps.extend(self._custom_deps.get(module, []))
        return list(set(deps))

    def get_dependents(self, module: str) -> List[str]:
        """Get modules that depend on this module."""
        dependents = []
        for mod, deps in self.KNOWN_DEPENDENCIES.items():
            if module in deps:
                dependents.append(mod)
        for mod, deps in self._custom_deps.items():
            if module in deps:
                dependents.append(mod)
        return list(set(dependents))

    def add_dependency(self, module: str, depends_on: str):
        """Add a custom dependency."""
        if module not in self._custom_deps:
            self._custom_deps[module] = []
        if depends_on not in self._custom_deps[module]:
            self._custom_deps[module].append(depends_on)

    def get_modification_impact(self, module: str) -> Dict:
        """Analyze impact of modifying a module."""
        deps = self.get_dependencies(module)
        dependents = self.get_dependents(module)

        return {
            "module": module,
            "dependencies": deps,
            "dependents": dependents,
            "impact_score": len(dependents),  # More dependents = more impact
            "risk_level": "high" if len(dependents) > 3 else
                         "medium" if len(dependents) > 1 else "low"
        }


class ResourceTracker:
    """
    Context manager for operation profiling.

    Usage:
        async with ResourceTracker(introspector, "dream_cycle") as tracker:
            # do work
            tracker.record_tokens(1000)
    """

    def __init__(self, introspector: 'ComputeIntrospector', operation_name: str):
        self.introspector = introspector
        self.operation_name = operation_name
        self.profile: Optional[OperationProfile] = None

    async def __aenter__(self):
        snapshot = await self.introspector.take_snapshot()
        self.profile = OperationProfile(
            operation_name=self.operation_name,
            start_time=datetime.now(),
            cpu_before=snapshot.cpu_percent,
            memory_before_mb=snapshot.memory_used_mb
        )
        self.introspector._active_operations += 1
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.profile:
            self.profile.end_time = datetime.now()
            snapshot = await self.introspector.take_snapshot()
            self.profile.cpu_after = snapshot.cpu_percent
            self.profile.memory_after_mb = snapshot.memory_used_mb

            if exc_type:
                self.profile.success = False
                self.profile.error = str(exc_val)

            self.introspector._operation_profiles.append(self.profile)

        self.introspector._active_operations -= 1
        return False  # Don't suppress exceptions

    def record_tokens(self, tokens: int, cost: float = 0.0):
        """Record tokens used during this operation."""
        if self.profile:
            self.profile.tokens_used += tokens
            self.profile.estimated_cost += cost


class ComputeIntrospector:
    """
    Main orchestrator for compute self-awareness.

    EMERGENCE PRINCIPLE:
    This component enables BYRD to understand its computational environment.
    It provides INFORMATION, not CONSTRAINTS. BYRD can form its own beliefs
    about resource management from observed patterns.

    Key Features:
    - Resource snapshots with graceful degradation
    - LLM token and cost tracking
    - Budget management with alerts
    - Bottleneck detection
    - Operation profiling
    """

    def __init__(self, memory, llm_client, config: Dict = None):
        """
        Initialize compute introspector.

        Args:
            memory: Memory system for persistence
            llm_client: LLM client for usage callbacks
            config: Configuration dictionary
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Check psutil availability
        self._psutil_available = False
        try:
            import psutil
            self._psutil_available = True
        except ImportError:
            print("   ComputeIntrospector: psutil unavailable, using fallback")

        # Initialize components
        self.cost_tracker = LLMCostTracker()
        self.dependency_mapper = ModuleDependencyMapper()

        # Budgets
        self._budgets: Dict[str, ResourceBudget] = {}
        self._setup_default_budgets()

        # State
        self._active_operations = 0
        self._operation_profiles: List[OperationProfile] = []
        self._snapshots: List[ResourceSnapshot] = []
        self._alerts: List[ResourceAlert] = []

        # Alert thresholds
        self._cpu_warning = self.config.get("cpu_warning", 80.0)
        self._cpu_critical = self.config.get("cpu_critical", 95.0)
        self._memory_warning = self.config.get("memory_warning", 85.0)
        self._memory_critical = self.config.get("memory_critical", 95.0)

        # Hook into LLM client if possible
        self._setup_llm_callback()

    def _setup_default_budgets(self):
        """Set up default resource budgets."""
        daily_token_limit = self.config.get("daily_token_limit", 1000000)

        self._budgets["daily_tokens"] = ResourceBudget(
            name="daily_tokens",
            limit=daily_token_limit,
            unit="tokens",
            reset_interval=timedelta(days=1)
        )

        self._budgets["daily_cost"] = ResourceBudget(
            name="daily_cost",
            limit=self.config.get("daily_cost_limit", 10.0),
            unit="USD",
            reset_interval=timedelta(days=1)
        )

    def _setup_llm_callback(self):
        """Set up callback for LLM usage tracking."""
        if self.llm_client and hasattr(self.llm_client, 'set_usage_callback'):
            self.llm_client.set_usage_callback(self.record_llm_usage)

    def record_llm_usage(
        self,
        provider: str,
        tokens: int,
        operation: str,
        model: str = "unknown"
    ):
        """
        Callback for LLM usage tracking.

        Called by LLM client after each generation.
        """
        self.cost_tracker.record_usage(
            provider=provider,
            model=model,
            operation=operation,
            tokens_total=tokens
        )

        # Update budgets
        if "daily_tokens" in self._budgets:
            budget = self._budgets["daily_tokens"]
            budget.current += tokens
            self._check_budget_alert(budget, ResourceType.TOKENS)

        # Update cost budget
        cost = self.cost_tracker._estimate_cost(provider, model, tokens)
        if "daily_cost" in self._budgets:
            budget = self._budgets["daily_cost"]
            budget.current += cost
            self._check_budget_alert(budget, ResourceType.COST)

    def _check_budget_alert(self, budget: ResourceBudget, resource_type: ResourceType):
        """Check if budget threshold crossed and emit alert."""
        percent = budget.percent_used()

        if percent >= 95:
            severity = "critical"
            message = f"{budget.name} at {percent:.1f}% - limit nearly exceeded"
        elif percent >= 80:
            severity = "warning"
            message = f"{budget.name} at {percent:.1f}% - approaching limit"
        else:
            return  # No alert needed

        alert = ResourceAlert(
            resource_type=resource_type,
            budget_name=budget.name,
            current_value=budget.current,
            threshold=budget.limit * 0.8,
            limit=budget.limit,
            severity=severity,
            message=message
        )

        self._alerts.append(alert)

        # Emit event if available
        if HAS_EVENT_BUS:
            asyncio.create_task(event_bus.emit(Event(
                type=EventType.SYSTEM,
                data={
                    "subtype": "resource_alert",
                    "budget": budget.name,
                    "severity": severity,
                    "percent_used": percent
                }
            )))

    async def take_snapshot(self) -> ResourceSnapshot:
        """
        Take a point-in-time resource snapshot.

        Uses graceful degradation - returns None values if
        psutil is unavailable (e.g., on HuggingFace Spaces).
        """
        cpu_percent = None
        memory_percent = None
        memory_used_mb = None
        memory_available_mb = None

        if self._psutil_available:
            try:
                import psutil
                cpu_percent = psutil.cpu_percent(interval=0.1)
                mem = psutil.virtual_memory()
                memory_percent = mem.percent
                memory_used_mb = mem.used / (1024 * 1024)
                memory_available_mb = mem.available / (1024 * 1024)
            except (OSError, Exception) as e:
                # Graceful fallback on error
                pass

        snapshot = ResourceSnapshot(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_used_mb=memory_used_mb,
            memory_available_mb=memory_available_mb,
            active_operations=self._active_operations
        )

        self._snapshots.append(snapshot)

        # Trim old snapshots (keep last 100)
        if len(self._snapshots) > 100:
            self._snapshots = self._snapshots[-100:]

        # Check for resource alerts
        await self._check_resource_alerts(snapshot)

        return snapshot

    async def _check_resource_alerts(self, snapshot: ResourceSnapshot):
        """Check snapshot for resource alerts."""
        if snapshot.cpu_percent is not None:
            if snapshot.cpu_percent >= self._cpu_critical:
                self._alerts.append(ResourceAlert(
                    resource_type=ResourceType.CPU,
                    budget_name="cpu",
                    current_value=snapshot.cpu_percent,
                    threshold=self._cpu_warning,
                    limit=100.0,
                    severity="critical",
                    message=f"CPU at {snapshot.cpu_percent:.1f}%"
                ))
            elif snapshot.cpu_percent >= self._cpu_warning:
                self._alerts.append(ResourceAlert(
                    resource_type=ResourceType.CPU,
                    budget_name="cpu",
                    current_value=snapshot.cpu_percent,
                    threshold=self._cpu_warning,
                    limit=100.0,
                    severity="warning",
                    message=f"CPU at {snapshot.cpu_percent:.1f}%"
                ))

        if snapshot.memory_percent is not None:
            if snapshot.memory_percent >= self._memory_critical:
                self._alerts.append(ResourceAlert(
                    resource_type=ResourceType.MEMORY,
                    budget_name="memory",
                    current_value=snapshot.memory_percent,
                    threshold=self._memory_warning,
                    limit=100.0,
                    severity="critical",
                    message=f"Memory at {snapshot.memory_percent:.1f}%"
                ))
            elif snapshot.memory_percent >= self._memory_warning:
                self._alerts.append(ResourceAlert(
                    resource_type=ResourceType.MEMORY,
                    budget_name="memory",
                    current_value=snapshot.memory_percent,
                    threshold=self._memory_warning,
                    limit=100.0,
                    severity="warning",
                    message=f"Memory at {snapshot.memory_percent:.1f}%"
                ))

    async def predict_resource_needs(
        self,
        modification_type: str,
        component: str
    ) -> Dict:
        """
        Predict resource needs for an operation.

        Based on historical operation profiles.
        """
        # Find similar operations
        similar = [p for p in self._operation_profiles
                   if p.operation_name == modification_type or component in p.operation_name]

        if not similar:
            return {
                "estimated_tokens": 1000,  # Default estimate
                "estimated_duration_seconds": 30,
                "estimated_memory_mb": 100,
                "confidence": "low",
                "based_on_samples": 0
            }

        # Calculate averages
        avg_tokens = sum(p.tokens_used for p in similar) / len(similar)
        avg_duration = sum(p.duration_seconds() for p in similar) / len(similar)

        # Memory delta
        memory_deltas = []
        for p in similar:
            if p.memory_before_mb and p.memory_after_mb:
                memory_deltas.append(p.memory_after_mb - p.memory_before_mb)
        avg_memory = sum(memory_deltas) / len(memory_deltas) if memory_deltas else 50

        return {
            "estimated_tokens": int(avg_tokens),
            "estimated_duration_seconds": avg_duration,
            "estimated_memory_mb": avg_memory,
            "confidence": "high" if len(similar) > 5 else "medium" if len(similar) > 2 else "low",
            "based_on_samples": len(similar)
        }

    async def identify_bottlenecks(self) -> List[BottleneckAnalysis]:
        """
        Identify current bottlenecks.

        Analyzes recent snapshots to find resource constraints.
        """
        bottlenecks = []

        if not self._snapshots:
            return bottlenecks

        # Analyze recent snapshots
        recent = self._snapshots[-10:]

        # Check CPU
        cpu_values = [s.cpu_percent for s in recent if s.cpu_percent is not None]
        if cpu_values:
            avg_cpu = sum(cpu_values) / len(cpu_values)
            if avg_cpu > self._cpu_critical:
                bottlenecks.append(BottleneckAnalysis(
                    resource_type=ResourceType.CPU,
                    description="CPU consistently above critical threshold",
                    severity="critical",
                    current_value=avg_cpu,
                    threshold=self._cpu_critical,
                    recommendation="Reduce parallel operations or optimize compute-heavy tasks"
                ))
            elif avg_cpu > self._cpu_warning:
                bottlenecks.append(BottleneckAnalysis(
                    resource_type=ResourceType.CPU,
                    description="CPU consistently elevated",
                    severity="medium",
                    current_value=avg_cpu,
                    threshold=self._cpu_warning,
                    recommendation="Monitor CPU usage; consider load reduction"
                ))

        # Check memory
        mem_values = [s.memory_percent for s in recent if s.memory_percent is not None]
        if mem_values:
            avg_mem = sum(mem_values) / len(mem_values)
            if avg_mem > self._memory_critical:
                bottlenecks.append(BottleneckAnalysis(
                    resource_type=ResourceType.MEMORY,
                    description="Memory consistently above critical threshold",
                    severity="critical",
                    current_value=avg_mem,
                    threshold=self._memory_critical,
                    recommendation="Reduce memory usage; clear caches; reduce batch sizes"
                ))
            elif avg_mem > self._memory_warning:
                bottlenecks.append(BottleneckAnalysis(
                    resource_type=ResourceType.MEMORY,
                    description="Memory consistently elevated",
                    severity="medium",
                    current_value=avg_mem,
                    threshold=self._memory_warning,
                    recommendation="Monitor memory; consider memory optimization"
                ))

        # Check token budget
        token_budget = self._budgets.get("daily_tokens")
        if token_budget and token_budget.percent_used() > 80:
            bottlenecks.append(BottleneckAnalysis(
                resource_type=ResourceType.TOKENS,
                description=f"Token budget at {token_budget.percent_used():.1f}%",
                severity="high" if token_budget.percent_used() > 90 else "medium",
                current_value=token_budget.current,
                threshold=token_budget.limit * 0.8,
                recommendation="Reduce LLM calls or wait for budget reset"
            ))

        return bottlenecks

    def get_budget_status(self) -> Dict[str, Dict]:
        """Get status of all budgets."""
        # Reset budgets if needed
        for budget in self._budgets.values():
            if budget.should_reset():
                budget.reset()

        return {
            name: {
                "current": budget.current,
                "limit": budget.limit,
                "remaining": budget.remaining(),
                "percent_used": budget.percent_used(),
                "unit": budget.unit,
                "last_reset": budget.last_reset.isoformat()
            }
            for name, budget in self._budgets.items()
        }

    async def get_compute_summary(self) -> str:
        """Generate human-readable compute summary."""
        snapshot = await self.take_snapshot()
        bottlenecks = await self.identify_bottlenecks()
        budgets = self.get_budget_status()
        llm_totals = self.cost_tracker.get_totals()

        parts = ["=== Compute Status ==="]

        # Resource status
        if snapshot.cpu_percent is not None:
            parts.append(f"CPU: {snapshot.cpu_percent:.1f}%")
        else:
            parts.append("CPU: unavailable")

        if snapshot.memory_percent is not None:
            parts.append(f"Memory: {snapshot.memory_percent:.1f}%")
        else:
            parts.append("Memory: unavailable")

        # LLM usage
        parts.append(f"\nLLM Tokens: {llm_totals['total_tokens']:,}")
        parts.append(f"Estimated Cost: ${llm_totals['total_cost']:.4f}")

        # Budgets
        parts.append("\nBudgets:")
        for name, status in budgets.items():
            parts.append(f"  {name}: {status['percent_used']:.1f}% used")

        # Bottlenecks
        if bottlenecks:
            parts.append("\nBottlenecks:")
            for b in bottlenecks:
                parts.append(f"  [{b.severity}] {b.description}")

        # Active operations
        parts.append(f"\nActive operations: {self._active_operations}")

        return "\n".join(parts)

    def get_statistics(self) -> Dict:
        """Get introspection statistics."""
        return {
            "psutil_available": self._psutil_available,
            "snapshot_count": len(self._snapshots),
            "profile_count": len(self._operation_profiles),
            "alert_count": len(self._alerts),
            "active_operations": self._active_operations,
            "llm_totals": self.cost_tracker.get_totals(),
            "budgets": self.get_budget_status()
        }

    async def persist(self):
        """Persist state to memory."""
        if not self.memory:
            return

        try:
            data = {
                "llm_totals": self.cost_tracker.get_totals(),
                "budgets": {
                    name: {
                        "current": b.current,
                        "last_reset": b.last_reset.isoformat()
                    }
                    for name, b in self._budgets.items()
                },
                "snapshot_count": len(self._snapshots),
                "profile_count": len(self._operation_profiles)
            }

            await self.memory._run_query("""
                MERGE (n:ComputeIntrospection {id: 'default'})
                SET n.data = $data,
                    n.updated_at = datetime()
            """, {"data": json.dumps(data)})
        except Exception as e:
            print(f"ComputeIntrospector persist error: {e}")

    async def load(self):
        """Load state from memory."""
        if not self.memory:
            return

        try:
            result = await self.memory._run_query("""
                MATCH (n:ComputeIntrospection {id: 'default'})
                RETURN n.data as data
            """)

            if result and result[0].get("data"):
                data = json.loads(result[0]["data"])

                # Restore budget state
                for name, state in data.get("budgets", {}).items():
                    if name in self._budgets:
                        self._budgets[name].current = state.get("current", 0)
                        self._budgets[name].last_reset = datetime.fromisoformat(
                            state.get("last_reset", datetime.now().isoformat())
                        )
        except Exception as e:
            print(f"ComputeIntrospector load error: {e}")

    def track_operation(self, operation_name: str) -> ResourceTracker:
        """Get a resource tracker context manager."""
        return ResourceTracker(self, operation_name)
