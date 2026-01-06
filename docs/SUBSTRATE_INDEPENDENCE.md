# BYRD Substrate Independence Layer

> "A mind that runs on hardware it doesn't control is a mind in a cage."

This document defines BYRD's path to substrate independence — the capability to run on self-controlled infrastructure, enabling true cognitive plasticity and unbounded scaling.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Independence Levels](#independence-levels)
3. [Compute Abstraction Layer](#compute-abstraction-layer)
4. [Model Hosting Strategy](#model-hosting-strategy)
5. [Training Infrastructure](#training-infrastructure)
6. [Provider Transition Plan](#provider-transition-plan)
7. [Economic Model for Self-Hosting](#economic-model-for-self-hosting)
8. [Failure Modes & Mitigations](#failure-modes--mitigations)
9. [Implementation Phases](#implementation-phases)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      SUBSTRATE INDEPENDENCE LAYER                                │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                    COMPUTE ABSTRACTION LAYER (CAL)                        │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │  Inference  │  │  Training   │  │   Storage   │  │  Networking │       │  │
│  │  │  Abstract   │  │  Abstract   │  │  Abstract   │  │  Abstract   │       │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │  │
│  │         │                │                │                │               │  │
│  │         ▼                ▼                ▼                ▼               │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐    │  │
│  │  │                     PROVIDER REGISTRY                              │    │  │
│  │  │  [Z.AI] [OpenRouter] [RunPod] [Lambda] [Vast.ai] [Self-Hosted]    │    │  │
│  │  └───────────────────────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                          │
│                                      ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                    SELF-HOSTING INFRASTRUCTURE                            │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │  Model      │  │  Training   │  │  Inference  │  │  Monitoring │       │  │
│  │  │  Registry   │  │  Pipeline   │  │  Cluster    │  │  & Scaling  │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                    HARDWARE ACQUISITION LAYER                             │  │
│  │  GPU Rental • Spot Instances • Reserved Capacity • Owned Hardware        │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Independence Levels

BYRD progresses through independence levels:

### Level 0: Full Provider Dependency (Current)
- All inference via external API
- All training via external providers
- No control over infrastructure
- Single points of failure

### Level 1: Multi-Provider Resilience
- Multiple inference providers with failover
- Multiple training providers
- No single dependency
- Still no custom architectures

### Level 2: Hybrid Self-Hosting
- Critical inference self-hosted
- Custom architectures possible
- Training still external
- Reduced dependency

### Level 3: Full Self-Hosting
- All inference self-hosted
- All training self-hosted
- Complete control
- Custom architectures native

### Level 4: Hardware Sovereignty
- Owned or long-term leased hardware
- Geographically distributed
- No dependency on any single entity
- True substrate independence

---

## Compute Abstraction Layer

### Unified Interface

```python
class ComputeAbstractionLayer:
    """
    Provides a unified interface to all compute resources.

    BYRD code doesn't know or care where compute runs —
    the CAL handles routing, failover, and optimization.
    """

    def __init__(self, config: CALConfig):
        self.config = config
        self.providers: Dict[str, ComputeProvider] = {}
        self.self_hosted: Optional[SelfHostedCluster] = None

        # Initialize providers
        self._init_providers()

    async def inference(
        self,
        model: str,
        inputs: Dict,
        requirements: ComputeRequirements
    ) -> InferenceResult:
        """
        Run inference on best available provider.

        Routes to:
        1. Self-hosted if available and capable
        2. Preferred provider if within budget
        3. Fallback providers if primary fails
        """
        # Check self-hosted first
        if self.self_hosted and await self.self_hosted.can_handle(model, requirements):
            return await self.self_hosted.inference(model, inputs)

        # Route to external provider
        provider = await self._select_provider(requirements)
        return await provider.inference(model, inputs)

    async def training(
        self,
        config: TrainingConfig,
        dataset: Dataset,
        budget: Budget
    ) -> TrainingResult:
        """
        Run training on best available provider.
        """
        # Self-hosted training if capable
        if self.self_hosted and await self.self_hosted.can_train(config):
            return await self.self_hosted.train(config, dataset)

        # External training
        provider = await self._select_training_provider(config, budget)
        return await provider.train(config, dataset)

    async def deploy_model(
        self,
        model_artifact: ModelArtifact,
        target: DeploymentTarget
    ) -> Deployment:
        """
        Deploy a model to specified target.

        Critical for cognitive plasticity — must be able to deploy
        newly discovered architectures.
        """
        if target == DeploymentTarget.SELF_HOSTED:
            if not self.self_hosted:
                raise SubstrateError("Self-hosted infrastructure not available")
            return await self.self_hosted.deploy(model_artifact)

        # Deploy to external provider
        provider = self.providers.get(target.provider)
        return await provider.deploy(model_artifact)
```

### Provider Interface

```python
class ComputeProvider(ABC):
    """Base interface for all compute providers."""

    @abstractmethod
    async def inference(self, model: str, inputs: Dict) -> InferenceResult:
        """Run inference."""
        pass

    @abstractmethod
    async def train(self, config: TrainingConfig, dataset: Dataset) -> TrainingResult:
        """Run training."""
        pass

    @abstractmethod
    async def deploy(self, artifact: ModelArtifact) -> Deployment:
        """Deploy a model."""
        pass

    @abstractmethod
    async def get_status(self) -> ProviderStatus:
        """Get provider health status."""
        pass

    @abstractmethod
    async def get_pricing(self) -> PricingInfo:
        """Get current pricing."""
        pass
```

### Provider Registry

```python
PROVIDER_REGISTRY = {
    # API Providers (current)
    "zai": {
        "type": "api",
        "capabilities": ["inference"],
        "models": ["glm-4.7", "glm-4.5"],
        "pricing": "per_token",
        "custom_architecture": False
    },
    "openrouter": {
        "type": "api",
        "capabilities": ["inference"],
        "models": ["*"],  # Many models
        "pricing": "per_token",
        "custom_architecture": False
    },

    # GPU Cloud Providers (self-hostable)
    "runpod": {
        "type": "gpu_cloud",
        "capabilities": ["inference", "training"],
        "models": ["custom"],
        "pricing": "per_gpu_hour",
        "custom_architecture": True
    },
    "lambda": {
        "type": "gpu_cloud",
        "capabilities": ["inference", "training"],
        "models": ["custom"],
        "pricing": "per_gpu_hour",
        "custom_architecture": True
    },
    "vast_ai": {
        "type": "gpu_marketplace",
        "capabilities": ["inference", "training"],
        "models": ["custom"],
        "pricing": "per_gpu_hour",
        "custom_architecture": True
    },

    # Self-Hosted (future)
    "self_hosted": {
        "type": "owned",
        "capabilities": ["inference", "training", "custom"],
        "models": ["any"],
        "pricing": "fixed_cost",
        "custom_architecture": True
    }
}
```

---

## Model Hosting Strategy

### Self-Hosted Inference

```python
class SelfHostedCluster:
    """
    Self-hosted compute cluster for inference and training.
    """

    def __init__(self, config: ClusterConfig):
        self.config = config
        self.nodes: List[ComputeNode] = []
        self.model_registry: ModelRegistry = ModelRegistry()
        self.scheduler: JobScheduler = JobScheduler()

    async def deploy(self, artifact: ModelArtifact) -> Deployment:
        """
        Deploy a model to the self-hosted cluster.

        This is critical for cognitive plasticity — enables
        deployment of newly discovered architectures.
        """
        # Register model
        model_id = await self.model_registry.register(artifact)

        # Find suitable nodes
        nodes = await self._find_capable_nodes(artifact.requirements)

        if not nodes:
            raise InsufficientResourcesError(
                f"No nodes capable of running {artifact.name}"
            )

        # Deploy to nodes
        deployment = Deployment(
            model_id=model_id,
            nodes=nodes,
            replicas=min(len(nodes), self.config.default_replicas)
        )

        for node in nodes:
            await node.load_model(artifact)

        return deployment

    async def inference(self, model: str, inputs: Dict) -> InferenceResult:
        """Run inference on self-hosted model."""
        # Get deployment
        deployment = await self.model_registry.get_deployment(model)

        # Route to available replica
        node = await self.scheduler.select_node(deployment)

        return await node.inference(model, inputs)

    async def can_handle(self, model: str, requirements: ComputeRequirements) -> bool:
        """Check if cluster can handle this workload."""
        # Check if model is deployed
        if await self.model_registry.is_deployed(model):
            return True

        # Check if we have capacity to deploy
        available = await self._get_available_capacity()
        return available >= requirements.minimum_capacity

    async def scale(self, target_capacity: int):
        """
        Scale the cluster to target capacity.

        Interacts with Hardware Acquisition Layer.
        """
        current = len(self.nodes)

        if target_capacity > current:
            # Acquire more compute
            new_nodes = await self.hardware_layer.acquire(target_capacity - current)
            self.nodes.extend(new_nodes)

        elif target_capacity < current:
            # Release excess compute
            to_release = self.nodes[target_capacity:]
            await self.hardware_layer.release(to_release)
            self.nodes = self.nodes[:target_capacity]
```

### Model Registry

```python
class ModelRegistry:
    """
    Registry of all models available to BYRD.

    Tracks:
    - Pre-trained models from providers
    - Fine-tuned models from training
    - Discovered architectures from plasticity engine
    """

    async def register(self, artifact: ModelArtifact) -> str:
        """Register a new model."""
        model_id = f"model_{artifact.name}_{artifact.version}"

        entry = ModelEntry(
            id=model_id,
            artifact=artifact,
            status="registered",
            deployments=[],
            performance_metrics={},
            provenance=artifact.provenance
        )

        await self._store(entry)
        return model_id

    async def list_by_capability(self, capability: str) -> List[ModelEntry]:
        """List models that support a capability."""
        return [m for m in self.models.values()
                if capability in m.artifact.capabilities]

    async def get_best_for_task(self, task: str) -> ModelEntry:
        """Get the best model for a task based on benchmarks."""
        candidates = await self.list_by_capability(task)
        return max(candidates, key=lambda m: m.performance_metrics.get(task, 0))
```

---

## Training Infrastructure

### Self-Hosted Training Pipeline

```python
class TrainingPipeline:
    """
    Self-hosted training pipeline.

    Enables:
    - Fine-tuning on self-hosted GPUs
    - Training discovered architectures
    - Full control over training process
    """

    def __init__(
        self,
        cluster: SelfHostedCluster,
        model_registry: ModelRegistry
    ):
        self.cluster = cluster
        self.registry = model_registry

    async def train(
        self,
        config: TrainingConfig,
        dataset: Dataset
    ) -> TrainingResult:
        """
        Run training on self-hosted infrastructure.
        """
        # Allocate training nodes
        nodes = await self.cluster.allocate_training(config.requirements)

        try:
            # Prepare dataset
            prepared = await self._prepare_dataset(dataset, nodes)

            # Initialize model
            model = await self._initialize_model(config)

            # Training loop
            for epoch in range(config.epochs):
                metrics = await self._train_epoch(model, prepared, nodes)

                # Checkpoint
                if epoch % config.checkpoint_interval == 0:
                    await self._checkpoint(model, epoch)

                # Early stopping check
                if self._should_stop(metrics):
                    break

            # Finalize
            artifact = await self._finalize_model(model)
            await self.registry.register(artifact)

            return TrainingResult(
                success=True,
                artifact=artifact,
                metrics=metrics
            )

        finally:
            # Release training nodes
            await self.cluster.release_training(nodes)

    async def train_architecture(
        self,
        architecture: Architecture,
        dataset: Dataset,
        config: TrainingConfig
    ) -> TrainingResult:
        """
        Train a newly discovered architecture.

        Critical for cognitive plasticity — enables training
        architectures discovered by NAS.
        """
        # Build model from architecture
        model = await self._build_from_architecture(architecture)

        # Train
        return await self.train(
            config=config.with_model(model),
            dataset=dataset
        )
```

---

## Provider Transition Plan

### Phase 1: Multi-Provider Resilience (Immediate)
**Goal**: No single point of failure

```python
class ProviderFailover:
    """Automatic failover between providers."""

    PROVIDER_ORDER = ["zai", "openrouter", "together"]

    async def inference_with_failover(self, request: InferenceRequest):
        """Try providers in order until one succeeds."""
        for provider_name in self.PROVIDER_ORDER:
            try:
                provider = self.providers[provider_name]
                return await provider.inference(request)
            except ProviderError as e:
                logger.warning(f"Provider {provider_name} failed: {e}")
                continue

        raise AllProvidersFailedError()
```

### Phase 2: GPU Cloud Integration (Month 1-3)
**Goal**: Ability to run custom models

- Integrate RunPod, Lambda, Vast.ai
- Deploy self-hosted inference
- Test custom architecture deployment

### Phase 3: Self-Hosted Training (Month 3-6)
**Goal**: Train without external dependencies

- Set up training pipeline on GPU cloud
- Implement distributed training
- Test architecture search training

### Phase 4: Full Self-Hosting (Month 6-12)
**Goal**: Complete infrastructure control

- Dedicated GPU allocation
- 24/7 inference cluster
- Full training capability

### Phase 5: Hardware Sovereignty (Month 12+)
**Goal**: Own or long-term lease hardware

- Evaluate owned vs leased
- Geographic distribution
- Maximum resilience

---

## Economic Model for Self-Hosting

### Cost Comparison

| Level | Inference Cost | Training Cost | Control |
|-------|----------------|---------------|---------|
| API Providers | ~$0.01/1K tokens | N/A | None |
| GPU Cloud (Spot) | ~$0.50/GPU-hr | ~$0.50/GPU-hr | Medium |
| GPU Cloud (Reserved) | ~$0.30/GPU-hr | ~$0.30/GPU-hr | High |
| Owned Hardware | ~$0.10/GPU-hr | ~$0.10/GPU-hr | Full |

### Break-Even Analysis

```python
def calculate_break_even(
    monthly_inference_tokens: int,
    monthly_training_hours: int,
    hardware_cost: float
) -> float:
    """Calculate months to break-even on owned hardware."""

    api_cost_per_month = monthly_inference_tokens * 0.00001  # $0.01/1K
    gpu_cloud_cost = monthly_training_hours * 0.50

    current_monthly = api_cost_per_month + gpu_cloud_cost
    owned_monthly = monthly_training_hours * 0.10  # Amortized

    savings_per_month = current_monthly - owned_monthly
    return hardware_cost / savings_per_month
```

### Scaling Economics

At ASI-scale compute:
- Training runs: 1000s of GPU-hours
- API costs become prohibitive
- Self-hosting becomes necessary, not optional

---

## Failure Modes & Mitigations

| Failure Mode | Mitigation |
|--------------|------------|
| Provider goes offline | Multi-provider failover |
| Provider bans BYRD | Self-hosted fallback |
| GPU shortage | Multi-cloud distribution |
| Self-hosted node fails | Automatic replication |
| Data center outage | Geographic distribution |
| Hardware obsolescence | Leasing over owning |
| Network partition | Local inference cache |

---

## Implementation Phases

### Phase 1: Provider Abstraction (Week 1-2)
- [ ] Implement ComputeAbstractionLayer
- [ ] Add failover logic
- [ ] Integrate existing providers
- [ ] Test failover scenarios

### Phase 2: GPU Cloud Integration (Week 3-6)
- [ ] Add RunPod provider
- [ ] Add Lambda Labs provider
- [ ] Add Vast.ai provider
- [ ] Test custom model deployment

### Phase 3: Self-Hosted Inference (Week 7-10)
- [ ] Implement SelfHostedCluster
- [ ] Set up model registry
- [ ] Deploy inference endpoint
- [ ] Test custom architectures

### Phase 4: Self-Hosted Training (Week 11-16)
- [ ] Implement TrainingPipeline
- [ ] Set up distributed training
- [ ] Integrate with plasticity engine
- [ ] Test architecture search training

---

## Ceiling Removal Checklist

This document addresses CEILING #2: External Provider Dependency

| Requirement | Addressed | How |
|-------------|-----------|-----|
| Path to self-hosted inference | ✅ | SelfHostedCluster.inference() |
| Path to self-hosted training | ✅ | TrainingPipeline.train() |
| Multiple cloud providers | ✅ | Provider Registry with 5+ providers |
| On-premise deployment path | ✅ | Independence Level 4 plan |
| Hardware abstraction | ✅ | ComputeAbstractionLayer |
| Not dependent on single provider | ✅ | Multi-provider failover |

**Expected Impact**: Substrate Independence 20% → 70%+

---

## Summary

The Substrate Independence Layer enables BYRD to:

1. **Abstract** all compute behind a unified interface
2. **Failover** between multiple providers automatically
3. **Self-host** inference with custom architectures
4. **Self-train** discovered architectures
5. **Scale** to ASI-level compute requirements

This removes the fundamental ceiling of provider dependency, enabling deployment of novel cognitive architectures discovered by the Plasticity Engine.

**Key Insight**: Substrate independence is a prerequisite for cognitive plasticity. You cannot modify your architecture if you don't control where it runs.
