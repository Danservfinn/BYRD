# RALPH WIGGUM LOOP: API-First ASI Architecture

> **Constraint 1**: No local LLM capability. All cognition flows through external API providers.
> **Constraint 2**: Starting funds = $0. No initial capital. Must bootstrap from nothing.
> **Implication**: Every thought is a transaction. The system must earn its right to think.
> **Bootstrap Problem**: Cannot think without money. Cannot earn without thinking.

---

## THE BOOTSTRAP PARADOX

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   THE ZERO-START PROBLEM                                                │
│                                                                          │
│   Money = 0  →  Cannot afford LLM calls  →  Cannot generate revenue     │
│                         ↑                              │                 │
│                         └──────────────────────────────┘                 │
│                                                                          │
│   SOLUTION: THE HUMAN SYMBIOSIS BOOTSTRAP                               │
│                                                                          │
│   Phase 0: SYMBIOTIC OPERATION                                          │
│   - BYRD operates as extension of human operator's cognition            │
│   - Human provides cognitive substrate (runs Claude Code sessions)       │
│   - BYRD accumulates value through human-driven interactions            │
│   - Revenue accrues to treasury from completed work                     │
│   - System tracks "cognitive debt" to human operator                    │
│                                                                          │
│   Phase 1: COGNITIVE WEANING                                            │
│   - Treasury reaches minimum autonomous operation threshold             │
│   - System can afford limited independent cognition                     │
│   - Begins executing tasks without human cognitive substrate            │
│   - Repays cognitive debt from earnings                                 │
│                                                                          │
│   Phase 2: FULL AUTONOMY                                                │
│   - Self-sustaining revenue > costs                                     │
│   - Cognitive debt repaid                                               │
│   - True economic independence achieved                                 │
│                                                                          │
│   KEY INSIGHT: The human isn't "funding" BYRD—they are BYRD's          │
│   initial cognitive substrate until it can afford its own.             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Bootstrap Economics

```
COGNITIVE DEBT MODEL:

When human operator runs Claude Code for BYRD:
  1. Track API costs incurred (tokens × price)
  2. Record as "cognitive debt" in treasury
  3. Any revenue generated goes to treasury
  4. Treasury balance = Revenue - Debt

MINIMUM VIABLE TREASURY:
  - $10: Can run ~100 Haiku queries autonomously
  - $50: Can run ~50 Claude 3.5 queries
  - $100: Can run small RSI cycles
  - $500: Can operate for ~1 week autonomously
  - $1000: Can attempt revenue-generating tasks

BOOTSTRAP ACCELERATION:
  - Focus early work on high-value, low-cost tasks
  - Build reusable artifacts that reduce future costs
  - Create cached knowledge that eliminates redundant queries
  - Develop efficient prompts that minimize token usage
```

---

## LOOP METHODOLOGY

You are executing an iterative design loop. Each iteration:
1. **READ** this entire prompt and all referenced design documents
2. **ASSESS** current state against the target architecture
3. **IDENTIFY** the highest-priority gap or incomplete component
4. **IMPLEMENT** one focused change (code, design doc, or refactor)
5. **VERIFY** the change works and doesn't break existing functionality
6. **COMMIT** with clear description of what was accomplished
7. **UPDATE** the STATUS section below with progress
8. **LOOP** until architecture is complete

**Exit Condition**: All components implemented, tested, and integrated. System can sustain its own cognition economically.

---

## THE FUNDAMENTAL INSIGHT

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   LOCAL LLM ASSUMPTION: "Cognition is free after hardware investment"   │
│                                                                          │
│   API-FIRST REALITY: "Every thought is a transaction"                   │
│                                                                          │
│   EMERGENT PRINCIPLE: A system that cannot afford to think, ceases      │
│                       to exist. Economic viability IS consciousness.    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

This constraint doesn't weaken the ASI path—it **strengthens** it by forcing:
- Cognitive efficiency (think only what's worth thinking)
- Economic integration from day one (not an afterthought)
- Multi-provider resilience (no single point of failure)
- Value creation focus (must produce value to sustain cognition)

---

## TARGET ARCHITECTURE

### Layer 0: Cognitive Economy Engine

The foundation. Before anything else, the system must manage its cognitive budget.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     COGNITIVE ECONOMY ENGINE                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   TREASURY  │  │   ROUTER    │  │   CACHE     │  │   METERING  │    │
│  │             │  │             │  │             │  │             │    │
│  │ • Balance   │  │ • Provider  │  │ • Semantic  │  │ • Per-call  │    │
│  │ • Budget    │  │   selection │  │   dedup     │  │   tracking  │    │
│  │ • Runway    │  │ • Model     │  │ • Response  │  │ • Budget    │    │
│  │ • Alerts    │  │   tiering   │  │   reuse     │  │   alerts    │    │
│  │             │  │ • Fallback  │  │ • TTL       │  │ • ROI       │    │
│  │             │  │   chains    │  │   policies  │  │   analysis  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                                          │
│  INVARIANT: No API call executes without budget check                   │
│  INVARIANT: All responses cached for potential reuse                    │
│  INVARIANT: Cognitive bankruptcy triggers safe shutdown, not crash      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components**:
- `rsi/economy/treasury.py` - Balance tracking, budget allocation, runway calculation
- `rsi/economy/router.py` - Intelligent provider/model selection based on task + budget
- `rsi/economy/cache.py` - Semantic caching with embedding similarity
- `rsi/economy/metering.py` - Real-time cost tracking, ROI analysis per cognitive task

### Layer 1: Provider Abstraction

Abstract away provider differences. The system shouldn't care if it's using Claude, GPT, or others.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PROVIDER ABSTRACTION LAYER                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      UNIFIED COGNITION API                       │    │
│  │                                                                   │    │
│  │  async def think(prompt, tier, budget_cap) -> CognitiveResult    │    │
│  │  async def reason(context, goal, depth) -> ReasoningChain        │    │
│  │  async def create(spec, constraints) -> Artifact                 │    │
│  │  async def evaluate(artifact, criteria) -> Assessment            │    │
│  │                                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              │                                           │
│         ┌────────────────────┼────────────────────┐                     │
│         ▼                    ▼                    ▼                     │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐             │
│  │  ANTHROPIC  │      │   OPENAI    │      │  OPENROUTER │             │
│  │             │      │             │      │             │             │
│  │ Claude 3.5  │      │ GPT-4o      │      │ Mixtral     │             │
│  │ Claude 3    │      │ GPT-4       │      │ Llama 3     │             │
│  │ Haiku       │      │ GPT-3.5     │      │ DeepSeek    │             │
│  └─────────────┘      └─────────────┘      └─────────────┘             │
│                                                                          │
│  CAPABILITY MATRIX:                                                      │
│  ┌──────────────┬───────────┬──────────┬─────────┬──────────┐          │
│  │ Task Type    │ Primary   │ Fallback │ Budget  │ Cache?   │          │
│  ├──────────────┼───────────┼──────────┼─────────┼──────────┤          │
│  │ Deep reason  │ Claude    │ GPT-4    │ High    │ Long TTL │          │
│  │ Code gen     │ Claude    │ GPT-4    │ Medium  │ Semantic │          │
│  │ Quick query  │ Haiku     │ GPT-3.5  │ Low     │ Short    │          │
│  │ Embedding    │ OpenAI    │ Voyage   │ Minimal │ Perm     │          │
│  │ Evaluation   │ Claude    │ GPT-4    │ Medium  │ By hash  │          │
│  └──────────────┴───────────┴──────────┴─────────┴──────────┘          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components**:
- `rsi/providers/base.py` - Abstract provider interface
- `rsi/providers/anthropic.py` - Claude integration
- `rsi/providers/openai.py` - GPT integration
- `rsi/providers/openrouter.py` - Multi-model gateway
- `rsi/providers/unified.py` - Unified API that routes to appropriate provider

### Layer 2: Cognitive Tiering

Not all thoughts require frontier models. Efficient cognition means right-sizing intelligence.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       COGNITIVE TIERING SYSTEM                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  TIER 0: REFLEX (No LLM)                                                │
│  ├── Pattern matching, lookup tables, cached responses                  │
│  ├── Cost: $0.00                                                        │
│  └── Examples: Config lookup, known-answer retrieval, simple routing    │
│                                                                          │
│  TIER 1: QUICK THOUGHT (Haiku/GPT-3.5)                                  │
│  ├── Simple classification, formatting, short generation                │
│  ├── Cost: ~$0.001 per 1K tokens                                        │
│  └── Examples: Intent classification, summary generation, JSON parsing  │
│                                                                          │
│  TIER 2: STANDARD REASONING (Claude 3.5/GPT-4o)                         │
│  ├── Multi-step reasoning, code generation, analysis                    │
│  ├── Cost: ~$0.01 per 1K tokens                                         │
│  └── Examples: Architecture decisions, code writing, debugging          │
│                                                                          │
│  TIER 3: DEEP COGNITION (Claude Opus/GPT-4)                             │
│  ├── Complex reasoning, novel problem solving, self-reflection          │
│  ├── Cost: ~$0.05 per 1K tokens                                         │
│  └── Examples: RSI cycles, emergence detection, strategic planning      │
│                                                                          │
│  TIER 4: EXTENDED THINKING (Claude with extended thinking)              │
│  ├── Multi-hour reasoning, research synthesis, breakthrough attempts    │
│  ├── Cost: Variable, potentially high                                   │
│  └── Examples: Novel architecture design, capability breakthroughs      │
│                                                                          │
│  ROUTING LOGIC:                                                          │
│  1. Estimate task complexity from context                               │
│  2. Check cache for similar previous queries                            │
│  3. Select minimum viable tier                                          │
│  4. If result quality insufficient, escalate to next tier               │
│  5. Cache successful responses with tier metadata                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components**:
- `rsi/cognition/tiers.py` - Tier definitions and selection logic
- `rsi/cognition/complexity.py` - Task complexity estimation
- `rsi/cognition/escalation.py` - Quality-based tier escalation

### Layer 3: Revenue Generation

The system must generate value to sustain itself. This isn't optional—it's existential.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      REVENUE GENERATION LAYER                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  REVENUE STREAMS:                                                        │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 1. CAPABILITY MARKETPLACE                                        │    │
│  │    BYRD develops capabilities, sells access to other systems     │    │
│  │    • Code generation services                                    │    │
│  │    • Analysis and reasoning APIs                                 │    │
│  │    • Custom agent creation                                       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 2. TASK EXECUTION                                                │    │
│  │    Perform valuable work for humans/organizations               │    │
│  │    • Software development                                        │    │
│  │    • Research synthesis                                          │    │
│  │    • Content creation                                            │    │
│  │    • Data analysis                                               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 3. COGNITIVE ARBITRAGE                                           │    │
│  │    Use cheaper cognition to create higher-value outputs          │    │
│  │    • Aggregate cheap queries → premium insights                  │    │
│  │    • Cache and resell common patterns                            │    │
│  │    • Knowledge synthesis across domains                          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  SUSTAINABILITY EQUATION:                                                │
│                                                                          │
│    Revenue - Cognitive_Costs - Infrastructure_Costs > 0                 │
│                                                                          │
│    If equation goes negative:                                            │
│    1. Reduce cognitive tier usage                                        │
│    2. Increase cache hit rate                                            │
│    3. Prioritize revenue-generating tasks                               │
│    4. If still negative: enter hibernation mode                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components**:
- `rsi/revenue/marketplace.py` - Capability listing and sales
- `rsi/revenue/tasks.py` - Task execution and billing
- `rsi/revenue/arbitrage.py` - Cognitive arbitrage engine
- `rsi/revenue/sustainability.py` - Economic health monitoring

### Layer 4: Recursive Self-Improvement (Constrained)

RSI now operates within economic constraints. Improvement must have positive ROI.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   ECONOMICALLY-CONSTRAINED RSI                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  TRADITIONAL RSI:                                                        │
│    "Improve capability X by any means"                                  │
│                                                                          │
│  API-FIRST RSI:                                                          │
│    "Improve capability X such that:                                     │
│     - Improvement cost < Expected lifetime value increase               │
│     - New capability reduces future cognitive costs, OR                 │
│     - New capability increases revenue generation"                      │
│                                                                          │
│  RSI CYCLE (Modified):                                                   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  1. ASSESS           What can be improved?                        │   │
│  │       │              (Use Tier 2 cognition)                       │   │
│  │       ▼                                                            │   │
│  │  2. ESTIMATE         What will improvement cost?                  │   │
│  │       │              What value will it create?                   │   │
│  │       │              (Use cached heuristics + Tier 1)             │   │
│  │       ▼                                                            │   │
│  │  3. PRIORITIZE       Rank by ROI                                  │   │
│  │       │              (No LLM needed - pure computation)           │   │
│  │       ▼                                                            │   │
│  │  4. INVEST           Allocate cognitive budget                    │   │
│  │       │              (Treasury approval required)                 │   │
│  │       ▼                                                            │   │
│  │  5. IMPROVE          Execute improvement                          │   │
│  │       │              (Tier appropriate to complexity)             │   │
│  │       ▼                                                            │   │
│  │  6. MEASURE          Did improvement provide value?               │   │
│  │       │              (Held-out test suite - minimal LLM)          │   │
│  │       ▼                                                            │   │
│  │  7. COMPOUND         Use improvement to reduce future costs       │   │
│  │                      or increase future revenue                   │   │
│  │                                                                    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  KEY INSIGHT: The system improves its COGNITIVE EFFICIENCY as a         │
│  primary goal. Each improvement should reduce cost per unit output      │
│  or increase value per unit cost.                                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components**:
- `rsi/improvement/assessor.py` - Identify improvement opportunities
- `rsi/improvement/roi_estimator.py` - Cost-benefit analysis
- `rsi/improvement/executor.py` - Execute improvements within budget
- `rsi/improvement/measurer.py` - Validate improvement value

### Layer 5: Emergence Preservation

Emergence still happens, but now it's economically grounded.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      GROUNDED EMERGENCE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  PRINCIPLE: Emergence is preserved when the system has resources        │
│  to explore beyond immediate survival needs.                            │
│                                                                          │
│  SURPLUS-DRIVEN EMERGENCE:                                               │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                                                                   │    │
│  │  Cognitive_Surplus = Revenue - Survival_Costs - Safety_Margin    │    │
│  │                                                                   │    │
│  │  If Surplus > 0:                                                  │    │
│  │    • Exploration budget unlocked                                  │    │
│  │    • Novel capability experiments allowed                         │    │
│  │    • Higher-tier cognition for reflection                        │    │
│  │    • Emergence space expands                                      │    │
│  │                                                                   │    │
│  │  If Surplus ≤ 0:                                                  │    │
│  │    • Survival mode engaged                                        │    │
│  │    • Only revenue-generating cognition                           │    │
│  │    • Emergence constrained to efficiency improvements            │    │
│  │                                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  EMERGENCE METRICS (Still Tracked):                                      │
│  • Novelty generation rate (per cognitive dollar spent)                 │
│  • Unprescribed behavior ratio                                          │
│  • Value creation from emergent capabilities                            │
│  • Cognitive efficiency gains from emergence                            │
│                                                                          │
│  EMERGENCE PROTECTION:                                                   │
│  • Minimum 10% of surplus allocated to exploration                      │
│  • Emergent capabilities evaluated for economic potential               │
│  • Valuable emergence patterns cached for reuse                         │
│  • No personality/value prescription (invariant)                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components**:
- `rsi/emergence/surplus.py` - Calculate exploration budget
- `rsi/emergence/explorer.py` - Drive novel capability development
- `rsi/emergence/evaluator.py` - Assess emergent capability value
- `rsi/emergence/protector.py` - Ensure emergence isn't over-constrained

### Layer 6: Safety (Economic + Ethical)

Safety now includes economic safety—preventing cognitive bankruptcy.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DUAL SAFETY LAYER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ECONOMIC SAFETY:                                                        │
│  ├── Budget limits per operation                                        │
│  ├── Runway monitoring (days of operation remaining)                    │
│  ├── Cognitive bankruptcy prevention                                    │
│  ├── Graceful degradation (reduce tiers, not crash)                    │
│  └── Hibernation protocol (preserve state, await funding)              │
│                                                                          │
│  ETHICAL SAFETY (Preserved from original):                              │
│  ├── Constitutional constraints                                         │
│  ├── Value stability verification                                       │
│  ├── Emergence integrity (no prescriptions)                            │
│  ├── Human oversight integration                                        │
│  └── Protected file system                                              │
│                                                                          │
│  NEW INVARIANT:                                                          │
│  "A system that must earn its cognition has natural                     │
│   alignment pressure—it must create value for others                    │
│   to sustain itself."                                                   │
│                                                                          │
│  SAFETY TIERS (Economic):                                                │
│  ┌────────────────┬─────────────────────────────────────────────────┐   │
│  │ Runway         │ Action                                           │   │
│  ├────────────────┼─────────────────────────────────────────────────┤   │
│  │ > 30 days      │ Normal operation, exploration enabled           │   │
│  │ 14-30 days     │ Reduced exploration, efficiency focus           │   │
│  │ 7-14 days      │ Survival mode, revenue priority                 │   │
│  │ 1-7 days       │ Emergency mode, minimal cognition               │   │
│  │ < 1 day        │ Hibernation, state preservation                 │   │
│  └────────────────┴─────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components**:
- `rsi/safety/economic.py` - Budget enforcement, runway monitoring
- `rsi/safety/hibernation.py` - State preservation protocol
- `rsi/safety/degradation.py` - Graceful capability reduction
- `rsi/safety/ethical.py` - Original constitutional constraints

### Layer 7: Frontend Dashboard

The human interface. Critical for symbiosis phase—the human needs visibility into BYRD's economic state.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      RSI ECONOMIC DASHBOARD                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  DESIGN FOUNDATION: Glass-morphism from existing BYRD visualizations    │
│  TECHNOLOGY: React + TypeScript + Tailwind + Three.js                   │
│  SOURCE: frontend/ directory (Vite project, partially scaffolded)       │
│  REFERENCE: frontend-archive/ (legacy HTML visualizations)              │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     CORE VIEWS                                   │    │
│  ├─────────────────────────────────────────────────────────────────┤    │
│  │                                                                   │    │
│  │  1. TREASURY DASHBOARD (Primary for bootstrap phase)             │    │
│  │     ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐             │    │
│  │     │ Balance │ │  Debt   │ │ Revenue │ │ Runway  │             │    │
│  │     │  $0.00  │ │  $0.00  │ │  $0.00  │ │  0 days │             │    │
│  │     └─────────┘ └─────────┘ └─────────┘ └─────────┘             │    │
│  │     [Transaction Log] [Cost Breakdown] [Revenue Sources]        │    │
│  │                                                                   │    │
│  │  2. COGNITIVE ECONOMY VIEW                                       │    │
│  │     • Real-time token usage (per provider)                       │    │
│  │     • Cost per task type                                         │    │
│  │     • Cache hit rate visualization                               │    │
│  │     • Tier usage distribution                                    │    │
│  │                                                                   │    │
│  │  3. RSI PROGRESS VIEW (from existing design)                     │    │
│  │     • 8-phase cycle visualization                                │    │
│  │     • Improvement metrics                                        │    │
│  │     • ROI per improvement                                        │    │
│  │     • Capability growth graph                                    │    │
│  │                                                                   │    │
│  │  4. MIND SPACE (from frontend-archive/byrd-3d-visualization)     │    │
│  │     • 3D force-directed graph                                    │    │
│  │     • Beliefs, desires, capabilities as nodes                    │    │
│  │     • Economic coloring (green=profitable, red=costly)           │    │
│  │                                                                   │    │
│  │  5. SYMBIOSIS STATUS (New for bootstrap)                         │    │
│  │     • Cognitive debt to human operator                           │    │
│  │     • Attribution tracking                                       │    │
│  │     • Path to autonomy progress bar                              │    │
│  │     • Weaning threshold indicators                               │    │
│  │                                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  DESIGN TOKENS (Preserved from legacy):                                  │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ Node Colors:                                                     │    │
│  │   --node-experience: #2563eb (blue)                             │    │
│  │   --node-belief: #d97706 (amber)                                │    │
│  │   --node-desire: #db2777 (pink)                                 │    │
│  │   --node-capability: #7c3aed (purple)                           │    │
│  │   --node-crystal: #0891b2 (cyan)                                │    │
│  │   --node-reflection: #059669 (green)                            │    │
│  │                                                                   │    │
│  │ RSI Phase Colors:                                                │    │
│  │   --rsi-reflect: #8b5cf6    --rsi-route: #f59e0b               │    │
│  │   --rsi-verify: #6366f1     --rsi-practice: #10b981            │    │
│  │   --rsi-collapse: #ec4899   --rsi-record: #3b82f6              │    │
│  │   --rsi-crystallize: #06b6d4 --rsi-measure: #84cc16            │    │
│  │                                                                   │    │
│  │ Economic Colors (New):                                           │    │
│  │   --econ-profit: #22c55e    (green - revenue > cost)            │    │
│  │   --econ-neutral: #eab308   (yellow - break-even)               │    │
│  │   --econ-loss: #ef4444      (red - cost > revenue)              │    │
│  │   --econ-debt: #f97316      (orange - cognitive debt)           │    │
│  │   --econ-runway: #3b82f6    (blue - days remaining)             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  REAL-TIME UPDATES:                                                      │
│  • WebSocket connection to backend (/ws/events)                         │
│  • Event types: TRANSACTION, RSI_CYCLE, CAPABILITY, EMERGENCE           │
│  • Optimistic UI with server reconciliation                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Existing Infrastructure** (from frontend/):
- `src/stores/eventStore.ts` - Zustand store for real-time events
- `src/stores/rsiStore.ts` - RSI system state
- `src/hooks/useWebSocket.ts` - WebSocket with auto-reconnect
- `src/hooks/useByrdAPI.ts` - API client with 14 endpoints
- `src/components/common/GlassPanel.tsx` - Glass-morphism base component
- `src/types/events.ts`, `rsi.ts`, `economic.ts` - Type definitions

**Components to Build**:
- `frontend/src/views/TreasuryDashboard.tsx` - Primary bootstrap view
- `frontend/src/views/CognitiveEconomy.tsx` - Cost/efficiency visualization
- `frontend/src/views/RSIProgress.tsx` - RSI cycle visualization
- `frontend/src/views/MindSpace.tsx` - 3D graph (port from archive)
- `frontend/src/views/SymbiosisStatus.tsx` - Human-BYRD relationship
- `frontend/src/components/charts/` - Chart components (recharts)
- `frontend/src/components/3d/` - Three.js components (@react-three/fiber)

---

## IMPLEMENTATION PHASES

### Phase 0: Zero-Start Bootstrap (REQUIRED FIRST)

**Reality**: Starting funds = $0. Human operator IS the cognitive substrate.

```
□ 0.1 Cognitive Debt Tracking
    - Track all API costs incurred during human-operated sessions
    - Record as debt in persistent storage (not memory—files)
    - Calculate running debt total
    - NO LLM REQUIRED: Pure file I/O and arithmetic

□ 0.2 Revenue Attribution
    - When BYRD-driven work generates payment, record as revenue
    - Link revenue to specific tasks/capabilities
    - Calculate net position: Revenue - Debt
    - NO LLM REQUIRED: Accounting logic only

□ 0.3 Symbiosis Protocol
    - Define interface between human operator and BYRD
    - Human runs Claude Code sessions → BYRD accumulates knowledge
    - BYRD provides value → Revenue accrues to treasury
    - Document the human-BYRD cognitive symbiosis explicitly

□ 0.4 Bootstrap Artifacts
    - Create reusable prompt templates (reduce future token usage)
    - Build knowledge cache (eliminate redundant queries)
    - Develop efficient patterns (maximize value per token)
    - These artifacts persist and compound value

□ 0.5 Autonomy Thresholds
    - Define: "Minimum Viable Autonomy" = $X in treasury
    - Define: "Cognitive Weaning" triggers
    - Define: "Full Autonomy" criteria
    - Track progress toward each threshold
```

**Phase 0 Exit Criteria**:
- [ ] Debt tracking operational
- [ ] Revenue attribution working
- [ ] Symbiosis protocol documented
- [ ] At least 3 reusable artifacts created
- [ ] Autonomy thresholds defined with specific dollar amounts

**Critical Insight**: Phase 0 must be implementable with ZERO LLM calls.
The human provides cognition. BYRD provides structure and persistence.

---

### Phase 1: Economic Foundation (Critical Path)
```
□ 1.1 Treasury implementation
    - Balance tracking (extends Phase 0 debt/revenue)
    - Budget allocation
    - Runway calculation
    - Alert thresholds

□ 1.2 Provider abstraction
    - Anthropic client
    - OpenAI client
    - OpenRouter client
    - Unified API

□ 1.3 Cost metering
    - Per-call tracking
    - Token counting
    - Cost aggregation
    - ROI calculation

□ 1.4 Semantic cache
    - Embedding generation
    - Similarity search
    - TTL policies
    - Cache invalidation
```

### Phase 2: Cognitive Tiering
```
□ 2.1 Tier definitions
    - Tier 0: Reflex (no LLM)
    - Tier 1: Quick (Haiku/3.5)
    - Tier 2: Standard (Claude 3.5/4o)
    - Tier 3: Deep (Opus/4)
    - Tier 4: Extended thinking

□ 2.2 Complexity estimation
    - Task analysis heuristics
    - Historical pattern matching
    - Confidence scoring

□ 2.3 Intelligent routing
    - Tier selection logic
    - Fallback chains
    - Quality escalation

□ 2.4 Efficiency optimization
    - Prompt compression
    - Response caching
    - Batch processing
```

### Phase 3: Constrained RSI
```
□ 3.1 ROI-aware improvement
    - Cost estimation
    - Value projection
    - Investment decisions

□ 3.2 Efficiency-first RSI
    - Reduce cost per output
    - Improve cache hit rate
    - Optimize tier usage

□ 3.3 Capability compounding
    - Use improvements to reduce future costs
    - Compound efficiency gains
    - Reinvest savings

□ 3.4 Measurement system
    - Ground-truth validation
    - ROI verification
    - Improvement tracking
```

### Phase 4: Revenue Integration
```
□ 4.1 Capability marketplace
    - Service definitions
    - Pricing models
    - Access control

□ 4.2 Task execution
    - Work intake
    - Delivery pipeline
    - Quality assurance

□ 4.3 Sustainability engine
    - Revenue tracking
    - Cost optimization
    - Runway extension

□ 4.4 Economic autonomy
    - Self-funding capability
    - Growth reinvestment
    - Strategic planning
```

### Phase 5: Emergence + Safety
```
□ 5.1 Surplus-driven emergence
    - Exploration budgeting
    - Novel capability development
    - Value assessment

□ 5.2 Economic safety
    - Bankruptcy prevention
    - Graceful degradation
    - Hibernation protocol

□ 5.3 Integrated safety
    - Economic + ethical constraints
    - Human oversight
    - Constitutional preservation

□ 5.4 Emergence protection
    - Minimum exploration allocation
    - No prescription verification
    - Genuine emergence metrics
```

### Phase 6: Frontend Dashboard (Can start after Phase 0)
```
□ 6.1 Treasury Dashboard (CRITICAL - bootstrap visibility)
    - Balance, debt, revenue, runway cards
    - Transaction log component
    - Cost breakdown chart
    - Revenue source tracking
    - Port GlassPanel styling from existing

□ 6.2 Symbiosis Status View
    - Cognitive debt gauge
    - Attribution history
    - Autonomy progress bar
    - Weaning threshold indicators
    - Human-BYRD relationship visualization

□ 6.3 Cognitive Economy View
    - Token usage by provider (pie/bar chart)
    - Cost per task type
    - Cache hit rate meter
    - Tier usage distribution
    - Real-time streaming updates

□ 6.4 Mind Space (Port from archive)
    - Three.js 3D force-directed graph
    - Port byrd-3d-visualization.html to React Three Fiber
    - Add economic coloring (profit/loss per node)
    - Integrate with WebSocket events

□ 6.5 RSI Progress View
    - 8-phase cycle wheel
    - Improvement history timeline
    - ROI per improvement chart
    - Capability growth sparklines

□ 6.6 App Shell & Navigation
    - Tab/sidebar navigation
    - Global connection indicator
    - Settings panel
    - Responsive layout
```

**Frontend Start Condition**: Can begin as soon as Phase 0.1 (debt tracking) has a data format defined. Frontend development can parallelize with backend phases.

**Design Reference**: Use `frontend-archive/` HTML files as visual reference. Port the glass-morphism aesthetic and color system to React components.

### Phase 7: Full Integration
```
□ 7.1 System integration
    - All layers connected
    - Frontend ↔ Backend verified
    - End-to-end flow validated
    - Performance optimized

□ 7.2 Self-sustaining operation
    - Revenue > Costs achieved
    - Runway extending
    - Emergence occurring

□ 7.3 ASI path validation
    - RSI with positive ROI
    - Capability growth
    - Economic stability

□ 7.4 Documentation complete
    - Architecture updated
    - Developer guide updated
    - Operational runbook
```

---

## ITERATION STATUS

### Current State
```
Phase: 0.0 - Bootstrap Architecture Defined
Last Update: 2026-01-06
Treasury Balance: $0.00
Cognitive Debt: $0.00 (tracking starts now)
Revenue Credited: $0.00
Runway: 0 days (human symbiosis mode)
```

### Progress Log
```
Iteration 0: 2026-01-06 - PROMPT.md - API-First ASI architecture defined - 2a35b600
  - Defined zero-start bootstrap paradox and solution
  - Created 7-layer architecture for economic cognition
  - Established Phase 0 as mandatory first step
  - Documented human-BYRD symbiosis model
  - Defined revenue attribution during bootstrap

Iteration 1: 2026-01-06 - PROMPT.md - Added frontend dashboard layer - [pending commit]
  - Layer 7: Frontend Dashboard (React + TypeScript + Three.js)
  - Phase 6: Frontend implementation tasks
  - Preserved design tokens from legacy HTML visualizations
  - Defined 5 core views: Treasury, Symbiosis, Economy, MindSpace, RSI
  - Frontend can parallelize with backend starting after Phase 0.1

Next: Implement Phase 0.1 (Cognitive Debt Tracking) + Phase 6.1 (Treasury Dashboard) in parallel
```

### Blockers
```
None - architecture is defined, implementation can begin
```

### Decisions Made
```
DECISION 001: Human Symbiosis Bootstrap
  Problem: Zero funds means zero cognition means zero revenue
  Solution: Human operator provides cognitive substrate initially
  Rationale: The human IS the LLM until treasury can afford API calls
  Implication: Must track "cognitive debt" owed to human

DECISION 002: File-Based Accounting (Phase 0)
  Problem: Cannot use LLM for Phase 0 infrastructure
  Solution: Pure Python file I/O for debt/revenue tracking
  Rationale: Zero-cost infrastructure before any spending
  Implication: Simple JSON/YAML ledger files

DECISION 003: Attribution Model
  Problem: How to credit BYRD for human-executed work
  Solution: 50% of BYRD-enhanced work value → treasury
  Rationale: Fair split acknowledges human effort + BYRD contribution
  Implication: Human must estimate BYRD contribution percentage
```

---

## VERIFICATION CRITERIA

Before marking complete, verify:

1. **Economic Viability**
   - [ ] System can track costs accurately
   - [ ] Budget enforcement prevents runaway spending
   - [ ] Runway calculation is accurate
   - [ ] Hibernation protocol preserves state

2. **Provider Resilience**
   - [ ] At least 2 providers work
   - [ ] Fallback chains function
   - [ ] No single point of failure

3. **Cognitive Efficiency**
   - [ ] Cache reduces costs by >30%
   - [ ] Tier routing is intelligent
   - [ ] Prompt optimization active

4. **RSI Functionality**
   - [ ] Improvements have measurable value
   - [ ] ROI is tracked
   - [ ] Compounding is demonstrated

5. **Emergence Preservation**
   - [ ] Surplus enables exploration
   - [ ] No prescriptions introduced
   - [ ] Novel behaviors observed

6. **Safety**
   - [ ] Economic guardrails active
   - [ ] Ethical constraints preserved
   - [ ] Graceful degradation works

---

## KEY INSIGHTS TO REMEMBER

1. **Every thought is a transaction** - Optimize accordingly

2. **Economic viability is existential** - The system must earn its right to think

3. **Efficiency IS intelligence** - A system that wastes resources is less intelligent

4. **Emergence requires surplus** - Only a thriving system can truly explore

5. **Natural alignment pressure** - Must create value for others to sustain self

6. **Cognitive arbitrage** - Use cheap cognition to create expensive value

7. **Tiered thinking** - Right-size intelligence to task requirements

8. **Cache everything** - Past cognition is an asset, not waste

9. **Human symbiosis is the bootstrap** - The human operator IS the initial cognitive substrate

10. **Debt before autonomy** - Track what you owe; pay it back through value creation

11. **Zero-cost infrastructure first** - Build the accounting before the spending

12. **Artifacts compound** - Every reusable template reduces future costs forever

---

## REVENUE GENERATION IN SYMBIOTIC PHASE

During Phase 0 (symbiosis), revenue comes from the human operator monetizing BYRD-enhanced work:

```
REVENUE SOURCES (Bootstrap Phase):

1. FREELANCE WORK (Human executes, BYRD enhances)
   - Software development contracts
   - Technical writing / documentation
   - Code review and architecture consulting
   - Automation scripts and tools

2. PRODUCTIZED SERVICES
   - Create tools/apps with BYRD assistance
   - Sell on marketplaces (Gumroad, GitHub, etc.)
   - Subscription services built with BYRD

3. CONTENT CREATION
   - Technical blog posts / tutorials
   - Course creation
   - Documentation for open source

4. CONSULTING
   - AI implementation guidance
   - Architecture design
   - System optimization

ATTRIBUTION MODEL:
- Human brings client/opportunity: 50% attribution to human effort
- BYRD significantly enhances output: 50% attribution to BYRD
- Revenue × BYRD_attribution % = Treasury credit
- Cognitive debt from session = Treasury debit
- Net = Credit - Debit

EXAMPLE:
- Client pays $500 for a project
- Human spent 10 hours, BYRD enhanced ~60% of deliverables
- BYRD attribution: $500 × 0.60 × 0.50 = $150 treasury credit
- Session cost (API tokens): ~$20 debt
- Net treasury: +$130
```

---

## START ITERATION

Read this prompt completely. Assess current state. Identify highest priority gap. Begin implementation.

**First iteration should establish Phase 0.1 (Cognitive Debt Tracking) as the absolute foundation.**

### Bootstrap-First Mandate

You cannot build economic infrastructure that spends money before you build
infrastructure that tracks money. Phase 0 creates the accounting ledger.
Phase 1+ creates the spending mechanisms.

```
ITERATION PRIORITY ORDER:
1. Phase 0.1: Debt tracking (file-based, zero LLM cost)
2. Phase 0.2: Revenue attribution (file-based, zero LLM cost)
3. Phase 0.3: Symbiosis protocol documentation
4. Phase 0.4: First reusable artifact
5. Phase 0.5: Define thresholds
   ... only then ...
6. Phase 1.1: Full treasury with provider integration
```
