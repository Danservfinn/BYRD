import { create } from 'zustand';
import type {
  RSIPhase,
  PhaseStatus,
  RalphLoopStatus,
  GrowthMetrics,
  SafetyStatus,
  ScaleInvariantMetric
} from '../types/rsi';
import type { TreasuryStatus, RevenueReport, MarketplaceStats } from '../types/economic';

interface RSIStore {
  // Phase tracking
  phases: PhaseStatus[];
  currentPhase: RSIPhase;

  // Ralph Loop
  ralphLoop: RalphLoopStatus;

  // Growth & Scaling
  growthMetrics: GrowthMetrics;

  // Safety
  safetyStatus: SafetyStatus;
  scaleInvariantMetrics: ScaleInvariantMetric[];

  // Economic
  treasuryStatus: TreasuryStatus | null;
  revenueReport: RevenueReport | null;
  marketplaceStats: MarketplaceStats | null;

  // Actions
  setPhases: (phases: PhaseStatus[]) => void;
  setRalphLoop: (status: RalphLoopStatus) => void;
  setGrowthMetrics: (metrics: GrowthMetrics) => void;
  setSafetyStatus: (status: SafetyStatus) => void;
  setScaleInvariantMetrics: (metrics: ScaleInvariantMetric[]) => void;
  setTreasuryStatus: (status: TreasuryStatus) => void;
  setRevenueReport: (report: RevenueReport) => void;
  setMarketplaceStats: (stats: MarketplaceStats) => void;
}

const defaultPhases: PhaseStatus[] = [
  { phase: 'phase_0_archive', name: 'Archive', description: 'Pre-ASI codebase snapshot', progress: 100, completed: true, components: [] },
  { phase: 'phase_1_foundation', name: 'Foundation', description: 'Core RSI components', progress: 100, completed: true, components: [] },
  { phase: 'phase_2_enablement', name: 'Enablement', description: 'ASI enablement core', progress: 100, completed: true, components: [] },
  { phase: 'phase_3_advanced', name: 'Advanced', description: 'NAS, MetaArchitect, Recursion', progress: 100, completed: true, components: [] },
  { phase: 'phase_4_scaling', name: 'Scale & Safety', description: 'Capability explosion handling', progress: 100, completed: true, components: [] },
  { phase: 'phase_5_economic', name: 'Economic', description: 'Economic autonomy', progress: 100, completed: true, components: [] },
];

export const useRSIStore = create<RSIStore>((set) => ({
  phases: defaultPhases,
  currentPhase: 'phase_5_economic',

  ralphLoop: {
    running: false,
    iteration: 0,
    max_iterations: null,
    completion_promise: null,
    current_phase: 'idle',
  },

  growthMetrics: {
    current_rate: 0,
    trend: 'stable',
    phase: 'normal',
    resource_utilization: 0,
    value_drift: 0,
  },

  safetyStatus: {
    current_tier: 'automatic',
    pending_approvals: 0,
    recent_decisions: [],
  },

  scaleInvariantMetrics: [],
  treasuryStatus: null,
  revenueReport: null,
  marketplaceStats: null,

  setPhases: (phases) => set({ phases }),
  setRalphLoop: (ralphLoop) => set({ ralphLoop }),
  setGrowthMetrics: (growthMetrics) => set({ growthMetrics }),
  setSafetyStatus: (safetyStatus) => set({ safetyStatus }),
  setScaleInvariantMetrics: (scaleInvariantMetrics) => set({ scaleInvariantMetrics }),
  setTreasuryStatus: (treasuryStatus) => set({ treasuryStatus }),
  setRevenueReport: (revenueReport) => set({ revenueReport }),
  setMarketplaceStats: (marketplaceStats) => set({ marketplaceStats }),
}));
