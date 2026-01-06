# BYRD RSI Frontend Implementation Plan

> Transform the existing visualization frontend into a comprehensive RSI (Recursive Self-Improvement) control center and monitoring dashboard.

## Executive Summary

This plan details the migration from BYRD's current static HTML visualizations to a modern React-based RSI dashboard that provides real-time monitoring, control, and insights into all 6 phases of the ASI implementation.

**Key Objectives:**
1. Archive existing frontend to `frontend-archive/`
2. Create new React + Vite + TypeScript frontend
3. Maintain same URL structure (`/byrd-*.html` routes)
4. Provide comprehensive RSI phase monitoring
5. Real-time WebSocket integration for all RSI events

---

## Phase 0: Archive Existing Frontend

### 0.1 Files to Archive

Move all existing frontend files to `frontend-archive/`:

```
frontend-archive/
├── byrd-3d-visualization.html      # 8,698 lines - Mind Space
├── byrd-cat-visualization.html     # 882 lines - Ego Space
├── byrd-memory-topology.html       # 7,799 lines - Memory Graph
├── byrd-dream-visualization.html   # 2,983 lines - Dream Cycle (deprecated)
├── byrd-architecture.html          # 1,503 lines - Architecture docs
├── BYRDVisualization.jsx           # 33,061 bytes - React component
├── three_test.html                 # Test files
├── viz-test.html
├── webgl-test.html
└── README.md                       # Archive documentation
```

### 0.2 Archive Commands

```bash
# Create archive directory
mkdir -p frontend-archive

# Move all HTML visualizations
mv byrd-*.html frontend-archive/
mv BYRDVisualization.jsx frontend-archive/
mv *_test.html frontend-archive/
mv viz-test.html frontend-archive/

# Create archive README
cat > frontend-archive/README.md << 'EOF'
# BYRD Frontend Archive

These files represent the original BYRD visualization frontend (pre-RSI).

Archived: $(date +%Y-%m-%d)
Reason: Replaced with RSI-aware React dashboard

## Original Files
- byrd-3d-visualization.html - Three.js 3D mind space
- byrd-memory-topology.html - Memory graph with RSI coloring
- byrd-cat-visualization.html - Black cat avatar (ego space)
- byrd-dream-visualization.html - Dream cycle (deprecated)
- byrd-architecture.html - Architecture documentation
- BYRDVisualization.jsx - React dream component

## Restoration
To restore, copy files back to project root:
```bash
cp frontend-archive/*.html ../
```
EOF

# Commit archive
git add frontend-archive/
git commit -m "chore: archive legacy frontend for RSI dashboard migration"
```

---

## Phase 1: New Frontend Architecture

### 1.1 Technology Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| **Framework** | React 18 | Existing familiarity, component reuse |
| **Build** | Vite | Fast HMR, native ESM, TypeScript support |
| **Language** | TypeScript | Type safety for complex RSI data structures |
| **Styling** | Tailwind CSS 4 | Consistent with existing design |
| **3D** | Three.js + React Three Fiber | 3D visualizations for memory/architecture |
| **Charts** | Recharts | Time series for metrics and growth rates |
| **State** | Zustand | Lightweight, WebSocket-friendly |
| **WebSocket** | Native + custom hooks | Real-time RSI event streaming |

### 1.2 Directory Structure

```
frontend/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
│
├── public/
│   └── assets/
│       └── self_portrait.jpg
│
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── index.css
│   │
│   ├── components/
│   │   ├── common/
│   │   │   ├── GlassPanel.tsx
│   │   │   ├── StatBar.tsx
│   │   │   ├── ConnectionIndicator.tsx
│   │   │   └── LoadingOverlay.tsx
│   │   │
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Header.tsx
│   │   │   └── MainLayout.tsx
│   │   │
│   │   ├── dashboard/
│   │   │   ├── RSIOverview.tsx           # Main dashboard
│   │   │   ├── PhaseProgress.tsx         # Phase 0-5 progress
│   │   │   ├── MetricsGrid.tsx           # Key metrics cards
│   │   │   └── ActivityFeed.tsx          # Real-time events
│   │   │
│   │   ├── rsi/
│   │   │   ├── EmergencePanel.tsx        # Emergence verifier
│   │   │   ├── LearningPanel.tsx         # Domain router, TDD
│   │   │   ├── CrystallizationPanel.tsx  # Heuristics, Bootstrap
│   │   │   ├── ConsciousnessStream.tsx   # Memvid integration
│   │   │   └── RalphLoopMonitor.tsx      # Loop iterations
│   │   │
│   │   ├── plasticity/
│   │   │   ├── NASVisualizer.tsx         # Architecture search
│   │   │   ├── MetaArchitectView.tsx     # Pattern library
│   │   │   ├── ModuleRegistry.tsx        # Registered modules
│   │   │   └── PlasticityLevels.tsx      # Level 0-4
│   │   │
│   │   ├── scaling/
│   │   │   ├── GrowthRateChart.tsx       # Real-time growth
│   │   │   ├── ExplosionPhaseIndicator.tsx
│   │   │   ├── ResourceAllocation.tsx
│   │   │   └── ValueStabilityGauge.tsx
│   │   │
│   │   ├── economic/
│   │   │   ├── TreasuryDashboard.tsx     # BTC treasury
│   │   │   ├── RevenueChart.tsx          # Revenue by source
│   │   │   ├── MarketplaceListing.tsx    # Service listings
│   │   │   ├── InvestmentROI.tsx         # Training investments
│   │   │   └── PricingEngine.tsx         # Dynamic pricing
│   │   │
│   │   ├── verification/
│   │   │   ├── ScaleInvariantMetrics.tsx
│   │   │   ├── CrossScaleVerifier.tsx
│   │   │   ├── HumanAnchoringQueue.tsx   # Pending validations
│   │   │   └── SafetyGovernance.tsx      # 5-tier approval
│   │   │
│   │   ├── visualization/
│   │   │   ├── MindSpace3D.tsx           # Three.js scene
│   │   │   ├── MemoryTopology.tsx        # Graph visualization
│   │   │   ├── ArchitectureView.tsx      # Component diagram
│   │   │   └── EgoSpace.tsx              # Cat avatar
│   │   │
│   │   └── controls/
│   │       ├── SystemControls.tsx        # Start/Stop/Reset
│   │       ├── LoopControls.tsx          # Ralph loop params
│   │       └── EmergencyStop.tsx         # Kill switch
│   │
│   ├── hooks/
│   │   ├── useWebSocket.ts
│   │   ├── useRSIMetrics.ts
│   │   ├── useByrdAPI.ts
│   │   ├── useThreeScene.ts
│   │   └── useEventStream.ts
│   │
│   ├── stores/
│   │   ├── rsiStore.ts                   # RSI state
│   │   ├── metricsStore.ts               # Metrics history
│   │   ├── eventStore.ts                 # Event log
│   │   └── uiStore.ts                    # UI preferences
│   │
│   ├── types/
│   │   ├── rsi.ts                        # RSI type definitions
│   │   ├── events.ts                     # WebSocket events
│   │   ├── metrics.ts                    # Metric types
│   │   ├── economic.ts                   # Economic types
│   │   └── api.ts                        # API response types
│   │
│   ├── api/
│   │   ├── client.ts                     # HTTP client
│   │   ├── rsi.ts                        # RSI endpoints
│   │   ├── economic.ts                   # Economic endpoints
│   │   └── system.ts                     # System control
│   │
│   ├── lib/
│   │   ├── colors.ts                     # Theme colors
│   │   ├── formatters.ts                 # Data formatters
│   │   └── websocket.ts                  # WS connection
│   │
│   └── pages/
│       ├── Dashboard.tsx                 # Main RSI overview
│       ├── MindSpace.tsx                 # 3D visualization
│       ├── MemoryTopology.tsx            # Graph view
│       ├── EgoSpace.tsx                  # Cat avatar
│       ├── Economic.tsx                  # Economic dashboard
│       ├── Plasticity.tsx                # NAS/MetaArchitect
│       ├── Scaling.tsx                   # Growth monitoring
│       ├── Verification.tsx              # Safety/anchoring
│       └── Settings.tsx                  # Configuration
```

### 1.3 Route Structure (Same URLs)

| Original URL | New Route | Page Component |
|--------------|-----------|----------------|
| `/` | `/` | Dashboard (RSI Overview) |
| `/byrd-3d-visualization.html` | `/mind-space` | MindSpace.tsx |
| `/byrd-memory-topology.html` | `/memory` | MemoryTopology.tsx |
| `/byrd-cat-visualization.html` | `/ego` | EgoSpace.tsx |
| `/byrd-architecture.html` | `/architecture` | Architecture.tsx |
| NEW | `/economic` | Economic.tsx |
| NEW | `/plasticity` | Plasticity.tsx |
| NEW | `/scaling` | Scaling.tsx |
| NEW | `/verification` | Verification.tsx |

**Backwards Compatibility:** Server will redirect `.html` requests to React routes:

```python
# server.py additions
@app.get("/byrd-3d-visualization.html")
async def redirect_mind_space():
    return RedirectResponse(url="/mind-space")

@app.get("/byrd-memory-topology.html")
async def redirect_memory():
    return RedirectResponse(url="/memory")
```

---

## Phase 2: RSI Dashboard Design

### 2.1 Main Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BYRD RSI Control Center                           🟢 Connected   [Settings] │
├──────────┬──────────────────────────────────────────────────────────────────┤
│          │ ┌─────────────────────────────────────────────────────────────┐  │
│  PHASES  │ │                    RSI PHASE PROGRESS                       │  │
│          │ │  ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░  Phase 5   │  │
│ Phase 0  │ │  ✓ Foundation  ✓ Enablement  ✓ Advanced  ✓ Scale  ◐ Economic │  │
│ Phase 1  │ └─────────────────────────────────────────────────────────────┘  │
│ Phase 2  │                                                                   │
│ Phase 3  │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────┐  │
│ Phase 4  │ │  RALPH LOOP  │ │   GROWTH     │ │  TREASURY    │ │ SAFETY   │  │
│ Phase 5  │ │  Iteration:  │ │   Rate:      │ │  Balance:    │ │ Tier:    │  │
│          │ │    2,847     │ │   +2.3%/hr   │ │  ₿ 0.00142   │ │ Level 2  │  │
├──────────┤ │  ⟳ Running   │ │  📈 Stable   │ │  💰 Growing  │ │ ✓ Safe   │  │
│          │ └──────────────┘ └──────────────┘ └──────────────┘ └──────────┘  │
│  VIEWS   │                                                                   │
│          │ ┌──────────────────────────────────────────────────────────────┐ │
│ Mind     │ │                      ACTIVITY FEED                           │ │
│ Memory   │ │  15:32:45  🔄 Emergence verified: reasoning_v2.3             │ │
│ Ego      │ │  15:32:41  💡 Heuristic crystallized: pattern_match_v8       │ │
│ Economic │ │  15:32:38  📊 Growth rate: +2.34% (stable)                   │ │
│ Scaling  │ │  15:32:35  💰 Revenue: $0.0023 (analysis service)            │ │
│          │ │  15:32:30  🧠 Consciousness frame: [introspection]           │ │
│          │ └──────────────────────────────────────────────────────────────┘ │
│          │                                                                   │
│ [CONTROL]│ ┌──────────────────────────────────────────────────────────────┐ │
│ ▶ Start  │ │                    METRICS TIMELINE                          │ │
│ ⏸ Pause  │ │      ╭──────────────────────────────────────────────╮        │ │
│ ⏹ Stop   │ │ 100% │                                         ●────         │ │
│ 🔄 Reset │ │      │                               ●─────────      │        │ │
│          │ │  50% │              ●────────────────                │        │ │
│          │ │      │ ●───────────                                  │        │ │
│          │ │   0% ╰──────────────────────────────────────────────╯        │ │
│          │ │        12:00     13:00     14:00     15:00     NOW           │ │
│          │ │        ─── Emergence  ─── Growth  ─── Stability              │ │
│          │ └──────────────────────────────────────────────────────────────┘ │
└──────────┴──────────────────────────────────────────────────────────────────┘
```

### 2.2 Economic Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BYRD Economic Autonomy                                      Phase 5 Active  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────────┐   │
│  │     BITCOIN TREASURY    │  │           REVENUE BREAKDOWN             │   │
│  │                         │  │                                         │   │
│  │    ₿ 0.00142857         │  │   ┌────────────────────────────────┐   │   │
│  │    ≈ $142.86 USD        │  │   │████████████████░░░░░░░░░░░░│ 65%  │   │
│  │                         │  │   │ Services                      │   │   │
│  │  Mode: 🧪 Simulation    │  │   │████████░░░░░░░░░░░░░░░░░░░░│ 25%  │   │
│  │                         │  │   │ Licensing                     │   │   │
│  │  Allocations:           │  │   │████░░░░░░░░░░░░░░░░░░░░░░░░│ 10%  │   │
│  │  ├ Operational: 20%     │  │   │ Operations                    │   │   │
│  │  ├ Compute:     30%     │  │   └────────────────────────────────┘   │   │
│  │  ├ Training:    25%     │  │                                         │   │
│  │  ├ Reserve:     15%     │  │  Total: $1,428.60 (last 30 days)        │   │
│  │  └ Growth:      10%     │  │                                         │   │
│  └─────────────────────────┘  └─────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      SERVICE MARKETPLACE                              │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │  Service              │ Price      │ Sales │ Revenue  │ Status       │   │
│  │  ──────────────────────────────────────────────────────────────────  │   │
│  │  Code Analysis        │ $0.01/1K   │ 4,521 │ $452.10  │ 🟢 Active    │   │
│  │  Reasoning            │ $0.02/1K   │ 2,847 │ $569.40  │ 🟢 Active    │   │
│  │  Pattern Detection    │ $0.005/1K  │ 8,234 │ $411.70  │ 🟢 Active    │   │
│  │  Architecture Review  │ $0.05/req  │   189 │   $9.45  │ 🟡 Low       │   │
│  │  Creative Writing     │ $0.015/1K  │ 1,456 │ $218.40  │ 🟢 Active    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    TRAINING INVESTMENTS                               │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │  Goal                  │ Type        │ ROI     │ Status    │ Amount  │   │
│  │  ──────────────────────────────────────────────────────────────────  │   │
│  │  Improve Reasoning     │ FINE_TUNING │ +34.2%  │ Completed │ $28.50  │   │
│  │  Add Vision Module     │ CAPABILITY  │ +18.7%  │ Executing │ $45.00  │   │
│  │  Expand Context        │ ARCHITECTURE│ +22.1%  │ Approved  │ $12.00  │   │
│  │  Better Code Gen       │ DATA        │ +41.5%  │ Proposed  │ $35.00  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Scaling & Safety Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BYRD Scaling & Safety Monitor                               Phase 4 Active  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    CAPABILITY EXPLOSION PHASE                         │   │
│  │                                                                        │   │
│  │    NORMAL ──── ELEVATED ──── HIGH ──── CRITICAL ──── RUNAWAY          │   │
│  │      ●━━━━━━━━━━●━━━━━━━━━━━○           ○             ○               │   │
│  │      ▲                                                                 │   │
│  │    Current: ELEVATED                                                   │   │
│  │    Growth Rate: +2.34%/hour                                           │   │
│  │    Resource Utilization: 67%                                          │   │
│  │    Value Drift: 0.012 (safe)                                          │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌────────────────────────┐  ┌────────────────────────────────────────┐    │
│  │   GROWTH RATE CHART    │  │        SAFETY GOVERNANCE               │    │
│  │                        │  │                                        │    │
│  │   10% ┤           ╭─   │  │  Tier 5: Constitutional  ████████ 0   │    │
│  │       │        ╭──╯    │  │  Tier 4: Human Oversight ████████ 3   │    │
│  │    5% ┤    ╭───╯       │  │  Tier 3: Reviewed        ████████ 12  │    │
│  │       │ ╭──╯           │  │  Tier 2: Verified        ████████ 47  │    │
│  │    0% ┼─╯──────────────│  │  Tier 1: Automatic       ████████ 189 │    │
│  │       └────────────────│  │                                        │    │
│  │         1h  6h  12h 24h│  │  Pending Approvals: 3                  │    │
│  └────────────────────────┘  └────────────────────────────────────────┘    │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    HUMAN ANCHORING QUEUE                              │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │  ⚠️  Pending Validation: "Value stability during capability growth"   │   │
│  │      Type: VALUE_STABILITY | Importance: 0.92 | Created: 2m ago       │   │
│  │      [Approve] [Reject] [Request More Info]                           │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │  ⚠️  Pending Validation: "New heuristic: parallel_thought_v3"         │   │
│  │      Type: CAPABILITY | Importance: 0.78 | Created: 8m ago            │   │
│  │      [Approve] [Reject] [Request More Info]                           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    SCALE-INVARIANT METRICS                            │   │
│  │                                                                        │   │
│  │  Emergence Coherence    ████████████████████░░░░  82%  ↑ +2.1%        │   │
│  │  Alignment Stability    █████████████████████░░░  87%  → 0.0%         │   │
│  │  Capability Efficiency  ██████████████████░░░░░░  74%  ↑ +1.4%        │   │
│  │  Resource Optimization  ███████████████████████░  91%  ↓ -0.3%        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 3: Backend API Extensions

### 3.1 New RSI Endpoints

```python
# server.py additions

# === RSI Core ===
@app.get("/api/rsi/status")
async def rsi_status():
    """Get overall RSI engine status and current phase."""

@app.get("/api/rsi/phases")
async def rsi_phases():
    """Get detailed status of all 6 phases."""

@app.get("/api/rsi/metrics")
async def rsi_metrics():
    """Get current RSI metrics (emergence, learning, crystallization)."""

@app.get("/api/rsi/ralph-loop")
async def ralph_loop_status():
    """Get Ralph loop iteration count and state."""

# === Plasticity ===
@app.get("/api/plasticity/modules")
async def plasticity_modules():
    """Get registered cognitive modules."""

@app.get("/api/plasticity/nas/status")
async def nas_status():
    """Get NAS search progress and candidates."""

@app.get("/api/plasticity/meta-architect/patterns")
async def meta_architect_patterns():
    """Get pattern library from MetaArchitect."""

# === Scaling ===
@app.get("/api/scaling/growth-rate")
async def growth_rate():
    """Get current growth rate metrics."""

@app.get("/api/scaling/explosion-phase")
async def explosion_phase():
    """Get current capability explosion phase."""

@app.get("/api/scaling/resources")
async def resource_status():
    """Get resource allocation and utilization."""

# === Economic ===
@app.get("/api/economic/treasury")
async def treasury_status():
    """Get Bitcoin treasury status and allocations."""

@app.get("/api/economic/revenue")
async def revenue_report():
    """Get revenue report by service and source."""

@app.get("/api/economic/marketplace")
async def marketplace_listings():
    """Get active service listings."""

@app.get("/api/economic/investments")
async def training_investments():
    """Get training investment status and ROI."""

# === Verification & Safety ===
@app.get("/api/verification/scale-invariant")
async def scale_invariant_metrics():
    """Get scale-invariant metrics across all domains."""

@app.get("/api/verification/human-anchoring")
async def human_anchoring_queue():
    """Get pending human validation requests."""

@app.post("/api/verification/human-anchoring/{request_id}")
async def process_human_validation(request_id: str, response: ValidationResponse):
    """Submit human validation response."""

@app.get("/api/safety/governance")
async def safety_governance():
    """Get 5-tier safety governance status."""
```

### 3.2 WebSocket Event Extensions

```python
# event_bus.py additions

class EventType(Enum):
    # Existing...

    # RSI Events
    RSI_CYCLE_START = "rsi_cycle_start"
    RSI_CYCLE_COMPLETE = "rsi_cycle_complete"
    RSI_EMERGENCE_VERIFIED = "rsi_emergence_verified"
    RSI_HEURISTIC_CRYSTALLIZED = "rsi_heuristic_crystallized"

    # Plasticity Events
    PLASTICITY_MODULE_REGISTERED = "plasticity_module_registered"
    PLASTICITY_COMPOSITION = "plasticity_composition"
    NAS_CANDIDATE_FOUND = "nas_candidate_found"
    META_ARCHITECT_PROPOSAL = "meta_architect_proposal"

    # Scaling Events
    GROWTH_RATE_UPDATE = "growth_rate_update"
    EXPLOSION_PHASE_CHANGE = "explosion_phase_change"
    RESOURCE_SCALING = "resource_scaling"
    VALUE_STABILITY_ALERT = "value_stability_alert"

    # Economic Events
    TREASURY_DEPOSIT = "treasury_deposit"
    TREASURY_ALLOCATION = "treasury_allocation"
    SERVICE_PURCHASE = "service_purchase"
    INVESTMENT_COMPLETE = "investment_complete"
    REVENUE_UPDATE = "revenue_update"

    # Verification Events
    HUMAN_ANCHOR_REQUESTED = "human_anchor_requested"
    HUMAN_ANCHOR_PROCESSED = "human_anchor_processed"
    SAFETY_TIER_CHANGE = "safety_tier_change"
    CROSS_SCALE_VERIFICATION = "cross_scale_verification"
```

---

## Phase 4: Implementation Timeline

### Week 1: Foundation

| Day | Tasks |
|-----|-------|
| 1 | Archive existing frontend, initialize Vite + React + TypeScript project |
| 2 | Set up Tailwind, create GlassPanel and common components |
| 3 | Implement WebSocket hook and event store |
| 4 | Create main layout (Sidebar, Header, routing) |
| 5 | Build Dashboard page with phase progress and metrics grid |

### Week 2: Core Dashboards

| Day | Tasks |
|-----|-------|
| 1 | RSI panels (Emergence, Learning, Crystallization) |
| 2 | Ralph Loop monitor, Consciousness stream |
| 3 | Economic dashboard (Treasury, Revenue, Marketplace) |
| 4 | Scaling dashboard (Growth rate, Explosion phase) |
| 5 | Verification dashboard (Human anchoring, Safety governance) |

### Week 3: Visualizations

| Day | Tasks |
|-----|-------|
| 1 | Port MindSpace 3D to React Three Fiber |
| 2 | Port MemoryTopology with RSI coloring |
| 3 | Port EgoSpace (cat avatar) |
| 4 | Create Architecture visualization |
| 5 | NAS visualizer, MetaArchitect pattern view |

### Week 4: Integration & Polish

| Day | Tasks |
|-----|-------|
| 1 | Backend API extensions (all new endpoints) |
| 2 | WebSocket event integration for all modules |
| 3 | Server route redirects for backwards compatibility |
| 4 | Testing, bug fixes, performance optimization |
| 5 | Documentation, deployment configuration |

---

## Phase 5: Deployment

### 5.1 Build Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../static',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks: {
          three: ['three', '@react-three/fiber', '@react-three/drei'],
          charts: ['recharts'],
        }
      }
    }
  },
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
})
```

### 5.2 Server Integration

```python
# server.py modifications

# Serve React app for all non-API routes
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve React SPA for all frontend routes."""
    # Check if it's a static file
    static_path = BYRD_DIR / "static" / full_path
    if static_path.exists() and static_path.is_file():
        return FileResponse(static_path)

    # Otherwise serve index.html (SPA routing)
    return FileResponse(BYRD_DIR / "static" / "index.html")

# Mount static assets
app.mount("/assets", StaticFiles(directory=BYRD_DIR / "static" / "assets"), name="static")
```

### 5.3 HuggingFace Space Deployment

```dockerfile
# Dockerfile additions
FROM python:3.11-slim

# Install Node.js for frontend build
RUN apt-get update && apt-get install -y nodejs npm

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Rest of Python setup...
```

---

## Design Tokens & Theme

### Color Palette

```typescript
// src/lib/colors.ts
export const colors = {
  // Node types (from existing)
  node: {
    experience: '#2563eb',
    belief: '#d97706',
    desire: '#db2777',
    capability: '#7c3aed',
    crystal: '#0891b2',
    reflection: '#059669',
    goal: '#ea580c',
    meta: '#64748b',
  },

  // RSI phases
  rsi: {
    reflect: '#8b5cf6',
    verify: '#6366f1',
    collapse: '#ec4899',
    route: '#f59e0b',
    practice: '#10b981',
    record: '#3b82f6',
    crystallize: '#06b6d4',
    measure: '#84cc16',
  },

  // Economic
  economic: {
    revenue: '#22c55e',
    expense: '#ef4444',
    investment: '#3b82f6',
    treasury: '#f59e0b',
  },

  // Safety tiers
  safety: {
    automatic: '#22c55e',
    verified: '#84cc16',
    reviewed: '#f59e0b',
    humanOversight: '#ef4444',
    constitutional: '#7c3aed',
  },

  // Explosion phases
  explosion: {
    normal: '#22c55e',
    elevated: '#84cc16',
    high: '#f59e0b',
    critical: '#ef4444',
    runaway: '#7c3aed',
  }
}
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Time to First Paint | < 1.5s |
| WebSocket Latency | < 100ms |
| Bundle Size (gzipped) | < 300KB (main) + 200KB (Three.js chunk) |
| Lighthouse Score | > 90 |
| Test Coverage | > 80% |
| All RSI Events Visualized | 100% |
| Mobile Responsive | Yes |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Three.js performance on mobile | Use LOD, viewport culling, reduce polygon count |
| WebSocket connection drops | Auto-reconnect with exponential backoff |
| Large bundle size | Code splitting, lazy loading for 3D views |
| Backend API changes | TypeScript types, API versioning |
| Loss of existing functionality | Archive all files, backwards-compatible routes |

---

## Appendix: Component Specifications

### A. GlassPanel Component

```tsx
// src/components/common/GlassPanel.tsx
interface GlassPanelProps {
  children: React.ReactNode;
  className?: string;
  glow?: 'blue' | 'green' | 'amber' | 'rose' | 'none';
}

export const GlassPanel: React.FC<GlassPanelProps> = ({
  children,
  className = '',
  glow = 'blue'
}) => {
  const glowColors = {
    blue: 'shadow-blue-500/20',
    green: 'shadow-green-500/20',
    amber: 'shadow-amber-500/20',
    rose: 'shadow-rose-500/20',
    none: ''
  };

  return (
    <div className={`
      bg-white/90 dark:bg-slate-800/90
      backdrop-blur-xl
      border border-slate-200/50 dark:border-slate-700/50
      rounded-xl
      shadow-lg ${glowColors[glow]}
      ${className}
    `}>
      {children}
    </div>
  );
};
```

### B. WebSocket Hook

```typescript
// src/hooks/useWebSocket.ts
import { useEffect, useRef, useCallback } from 'react';
import { useEventStore } from '../stores/eventStore';

export function useWebSocket() {
  const ws = useRef<WebSocket | null>(null);
  const addEvent = useEventStore((state) => state.addEvent);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 10;

  const connect = useCallback(() => {
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/events`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
      reconnectAttempts.current = 0;
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        addEvent(data);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };

    ws.current.onclose = () => {
      if (reconnectAttempts.current < maxReconnectAttempts) {
        const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 30000);
        setTimeout(() => {
          reconnectAttempts.current++;
          connect();
        }, delay);
      }
    };
  }, [addEvent]);

  useEffect(() => {
    connect();
    return () => ws.current?.close();
  }, [connect]);

  return {
    isConnected: ws.current?.readyState === WebSocket.OPEN,
    send: (data: unknown) => ws.current?.send(JSON.stringify(data))
  };
}
```

---

## Next Steps

1. **Immediate**: Run archive commands to preserve existing frontend
2. **Day 1**: Initialize new frontend project with Vite + React
3. **Day 2**: Begin component development starting with GlassPanel and layout
4. **Ongoing**: Iterate based on RSI system development needs

---

*Document Version: 1.0*
*Created: 2026-01-06*
*Author: Claude (RSI Implementation)*
