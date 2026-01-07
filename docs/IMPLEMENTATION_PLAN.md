# BYRD Full-Stack Implementation Plan

**Created**: January 7, 2026
**Status**: Ready for implementation
**Scope**: Complete frontend, backend integration, archive cleanup

---

## Executive Summary

BYRD's backend is **95% complete** (~50,000 LOC). The frontend is **scaffolded but empty** (App.tsx is still the Vite starter template). This plan focuses on:

1. Archive deprecated code to eliminate conflicts
2. Integrate novel RSI architecture from research (Verification Lattice, CAO)
3. Implement all frontend components
4. Wire everything together

---

## Phase 0: Archive Deprecated Code

**Purpose**: Clean workspace, eliminate conflicts, preserve history

### Tasks

| Task | Source | Destination | Reason |
|------|--------|-------------|--------|
| Move root HTML files | `/*.html` | `archive/legacy-html/` | Replaced by React |
| Create archive README | - | `archive/README.md` | Document archive contents |

**Files to archive**:
- Any remaining HTML visualization files in root (if any)

**Note**: `frontend-archive/` and `archive/v1/` already exist with legacy code.

**Complexity**: S (1 hour)

---

## Phase 1: Backend - Novel RSI Architecture Integration

### 1.1 Verification Lattice [L]

**Create**: `/Users/kurultai/BYRD/rsi/verification/lattice.py`

```python
# Multi-verifier composition that exceeds single-verifier ceiling
class VerificationLattice:
    verifiers = [
        ExecutionTests(),      # Ground truth
        PropertyChecks(),      # Invariants
        LLMCritique(),         # Semantic review
        AdversarialProbes(),   # Robustness
        HumanSpotChecks()      # Calibration
    ]
    threshold = 0.6  # 60% agreement required

    async def verify(improvement) -> VerificationResult
```

**Integrates with**:
- `rsi/verification/scale_invariant.py`
- `rsi/verification/human_anchoring.py`

### 1.2 Complexity-Aware Orchestration (CAO) [M]

**Create**: `/Users/kurultai/BYRD/rsi/orchestration/cao.py`

```python
class ComplexityDetector:
    COLLAPSE_THRESHOLD = 0.45  # From Apple research

    async def estimate_complexity(task) -> float
    async def should_decompose(task) -> bool

class AgentRouter:
    # Multi-agent only when predicted accuracy < 45%
    async def should_use_multi_agent(task) -> bool
```

### 1.3 Domain Stratification [S]

**Modify**: `/Users/kurultai/BYRD/rsi/engine.py`

Add effort allocation constants:
```python
DOMAIN_WEIGHTS = {
    "stratum_1": 0.60,  # Fully verifiable (code, math)
    "stratum_2": 0.30,  # Partially verifiable (planning)
    "stratum_3": 0.10,  # Weakly verifiable (creative)
}
```

### 1.4 Entropic Drift Detection [M]

**Create**: `/Users/kurultai/BYRD/rsi/verification/entropic_drift.py`

```python
class EntropicDriftMonitor:
    def detect_drift(metrics) -> bool:
        # Monitor: solution diversity, held-out benchmarks,
        # generalization gap, strategy entropy
```

### 1.5 Emergent Strategy Competition [M]

**Enhance**: `/Users/kurultai/BYRD/rsi/orchestration/ralph_loop.py`

Add strategy pool with weighted competition and discovery.

---

## Phase 2: Frontend Implementation

**Base Path**: `/Users/kurultai/BYRD/frontend/src/`

### 2.1 Layout Components [M]

**Directory**: `components/layout/`

| File | Purpose |
|------|---------|
| `AppLayout.tsx` | Main layout with sidebar + header |
| `Sidebar.tsx` | Navigation sidebar |
| `Header.tsx` | Top header with status |
| `index.ts` | Exports |

### 2.2 Dashboard Components [M]

**Directory**: `components/dashboard/`

| File | Purpose |
|------|---------|
| `DashboardPage.tsx` | Main dashboard container |
| `SystemStatus.tsx` | BYRD running/stopped status |
| `RecentActivity.tsx` | Event stream (WebSocket) |
| `QuickStats.tsx` | Memory/capability counts |
| `ConsciousnessStream.tsx` | Real-time consciousness |
| `index.ts` | Exports |

### 2.3 RSI Components [M]

**Directory**: `components/rsi/`

| File | Purpose |
|------|---------|
| `RSIPage.tsx` | RSI dashboard |
| `PhaseTracker.tsx` | 8-phase cycle visualization |
| `RalphLoopStatus.tsx` | Iteration status |
| `EmergenceMetrics.tsx` | Emergence detection |
| `CycleHistory.tsx` | Historical cycles |
| `index.ts` | Exports |

### 2.4 Economic Components [S]

**Directory**: `components/economic/`

| File | Purpose |
|------|---------|
| `EconomicPage.tsx` | Economic dashboard |
| `TreasuryStatus.tsx` | Balance display |
| `RevenueChart.tsx` | Revenue over time (Recharts) |
| `MarketplaceListings.tsx` | Service listings |
| `index.ts` | Exports |

### 2.5 Plasticity Components [M]

**Directory**: `components/plasticity/`

| File | Purpose |
|------|---------|
| `PlasticityPage.tsx` | Plasticity dashboard |
| `ModuleRegistry.tsx` | Cognitive modules list |
| `NASCandidates.tsx` | NAS search results |
| `CompositionGraph.tsx` | 3D module graph (Three.js) |
| `index.ts` | Exports |

### 2.6 Scaling Components [M]

**Directory**: `components/scaling/`

| File | Purpose |
|------|---------|
| `ScalingPage.tsx` | Scaling dashboard |
| `GrowthRateGauge.tsx` | Growth rate visual |
| `ExplosionPhaseIndicator.tsx` | Phase indicator |
| `EntropicDriftMonitor.tsx` | Drift visualization |
| `index.ts` | Exports |

### 2.7 Verification Components [M]

**Directory**: `components/verification/`

| File | Purpose |
|------|---------|
| `VerificationPage.tsx` | Verification dashboard |
| `HumanAnchoringQueue.tsx` | Pending approvals |
| `SafetyTierIndicator.tsx` | Safety tier display |
| `VerificationLatticeView.tsx` | Lattice verifier status |
| `index.ts` | Exports |

### 2.8 Controls Components [M]

**Directory**: `components/controls/`

| File | Purpose |
|------|---------|
| `ControlPanel.tsx` | Start/stop/reset controls |
| `DirectionEditor.tsx` | Edit direction.md |
| `GovernanceConsole.tsx` | Interactive governance |
| `DesireInjector.tsx` | Inject desires |
| `index.ts` | Exports |

### 2.9 3D Visualization Components [L]

**Directory**: `components/visualization/`

| File | Purpose |
|------|---------|
| `MemoryTopology.tsx` | 3D Neo4j graph (React Three Fiber) |
| `ForceGraph3D.tsx` | Force-directed layout |
| `NodeRenderer.tsx` | Node type rendering |
| `index.ts` | Exports |

---

## Phase 3: App Integration

### 3.1 Replace App.tsx [M]

**File**: `/Users/kurultai/BYRD/frontend/src/App.tsx`

Currently: Vite starter template (counter demo)

Replace with:
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AppLayout } from './components/layout'
import { DashboardPage } from './components/dashboard'
import { RSIPage } from './components/rsi'
// ... other pages

function App() {
  return (
    <BrowserRouter>
      <AppLayout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/rsi" element={<RSIPage />} />
          <Route path="/economic" element={<EconomicPage />} />
          <Route path="/plasticity" element={<PlasticityPage />} />
          <Route path="/scaling" element={<ScalingPage />} />
          <Route path="/verification" element={<VerificationPage />} />
          <Route path="/controls" element={<ControlPanel />} />
          <Route path="/visualization" element={<MemoryTopology />} />
        </Routes>
      </AppLayout>
    </BrowserRouter>
  )
}
```

### 3.2 WebSocket Integration [S]

- Connect `useWebSocket` hook on app mount
- Route events to Zustand stores
- Components subscribe reactively

### 3.3 API Integration [S]

- Use existing `useByrdAPI` hook
- Load initial state on mount
- Polling for non-realtime data

---

## Phase 4: Server API Enhancements

**File**: `/Users/kurultai/BYRD/server.py`

### New Endpoints Needed

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/rsi/cycle` | POST | Trigger RSI cycle |
| `/api/rsi/phases` | GET | Current phase status |
| `/api/rsi/lattice` | GET | Verification lattice status |
| `/api/plasticity/modules` | GET | List modules |
| `/api/plasticity/nas` | GET | NAS candidates |
| `/api/scaling/drift` | GET | Entropic drift metrics |
| `/api/governance/direction` | GET/POST | Direction file |
| `/api/consciousness/frames` | GET | Recent frames |

---

## Phase 5: Testing

### Backend Tests
- `tests/test_verification_lattice.py`
- `tests/test_cao.py`
- `tests/test_entropic_drift.py`

### Frontend Tests
- Component rendering tests
- WebSocket event handling
- API integration tests

---

## Phase 6: Deployment

1. Build frontend: `cd frontend && npm run build` (outputs to `../static`)
2. Server serves from `/static`
3. Update `CLAUDE.md` with frontend commands
4. Test full integration

---

## Implementation Order (Critical Path)

```
Week 1:
├── Phase 0: Archive cleanup (1 day)
├── Phase 1.1: Verification Lattice (2 days)
├── Phase 1.2: CAO (1 day)
└── Phase 2.1-2.2: Layout + Dashboard (2 days)

Week 2:
├── Phase 2.3-2.4: RSI + Economic (2 days)
├── Phase 2.5-2.6: Plasticity + Scaling (2 days)
└── Phase 2.7-2.8: Verification + Controls (1 day)

Week 3:
├── Phase 2.9: 3D Visualization (2 days)
├── Phase 3: App Integration (1 day)
├── Phase 4: Server API (1 day)
└── Phase 5-6: Testing + Deploy (1 day)
```

---

## Critical Files Summary

### Backend (Create)
- `/Users/kurultai/BYRD/rsi/verification/lattice.py`
- `/Users/kurultai/BYRD/rsi/orchestration/cao.py`
- `/Users/kurultai/BYRD/rsi/verification/entropic_drift.py`

### Backend (Modify)
- `/Users/kurultai/BYRD/rsi/engine.py` (add domain stratification)
- `/Users/kurultai/BYRD/rsi/orchestration/ralph_loop.py` (add strategy competition)
- `/Users/kurultai/BYRD/server.py` (add new endpoints)

### Frontend (Create) - ~35 files
- `components/layout/*.tsx` (4 files)
- `components/dashboard/*.tsx` (6 files)
- `components/rsi/*.tsx` (6 files)
- `components/economic/*.tsx` (5 files)
- `components/plasticity/*.tsx` (5 files)
- `components/scaling/*.tsx` (5 files)
- `components/verification/*.tsx` (5 files)
- `components/controls/*.tsx` (5 files)
- `components/visualization/*.tsx` (4 files)

### Frontend (Modify)
- `/Users/kurultai/BYRD/frontend/src/App.tsx` (replace completely)

---

## Existing Assets to Leverage

### Already Complete (Use As-Is)
- `hooks/useByrdAPI.ts` - REST API client
- `hooks/useWebSocket.ts` - WebSocket connection
- `stores/eventStore.ts` - Event stream store
- `stores/rsiStore.ts` - System state store
- `types/events.ts` - 54 event types
- `types/rsi.ts` - RSI types
- `types/economic.ts` - Economic types
- `components/common/GlassPanel.tsx` - Glass-morphism container
- `components/common/StatCard.tsx` - Metric card
- `components/common/ConnectionIndicator.tsx` - WebSocket status

### Design System (CSS Variables in index.css)
- Node type colors (experience, belief, desire, capability, etc.)
- RSI phase colors (reflect, verify, collapse, etc.)
- Safety tier colors (automatic, verified, reviewed, human, constitutional)
- Glass-morphism tokens (fill, border, glow)

---

## Success Criteria

1. **Frontend renders** with all 8 pages accessible via router
2. **WebSocket connects** and displays real-time events
3. **3D visualization** shows Neo4j memory topology
4. **RSI controls** can trigger and monitor cycles
5. **Verification Lattice** integrates with RSI engine
6. **No deprecated code conflicts** (all archived)

---

*Plan version: 1.0*
*Estimated effort: 3 weeks*
*Dependencies: All npm packages already installed*
