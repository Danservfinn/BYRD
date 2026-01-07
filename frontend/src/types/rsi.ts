// RSI (Recursive Self-Improvement) types

export type RSIPhase =
  | 'phase_0_archive'      // Foundation
  | 'phase_1_foundation'   // Core RSI
  | 'phase_2_enablement'   // ASI Enablement
  | 'phase_3_advanced'     // Advanced (NAS, MetaArchitect)
  | 'phase_4_scaling'      // Scale & Safety
  | 'phase_5_economic';    // Economic Autonomy

export interface PhaseStatus {
  phase: RSIPhase;
  name: string;
  description: string;
  progress: number;  // 0-100
  completed: boolean;
  components: ComponentStatus[];
}

export interface ComponentStatus {
  id: string;
  name: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  tests_passing?: number;
  tests_total?: number;
}

// Ralph Loop
export interface RalphLoopStatus {
  running: boolean;
  iteration: number;
  max_iterations: number | null;
  completion_promise: string | null;
  current_phase: string;
  last_result?: {
    success: boolean;
    duration_ms: number;
    changes_made: number;
  };
}

// Growth & Scaling
export type ExplosionPhase = 'normal' | 'elevated' | 'high' | 'critical' | 'runaway';

export interface GrowthMetrics {
  current_rate: number;  // percentage per hour
  trend: 'increasing' | 'stable' | 'decreasing';
  phase: ExplosionPhase;
  resource_utilization: number;  // 0-100
  value_drift: number;  // 0-1, lower is safer
}

// Safety & Verification
export type SafetyTier = 'automatic' | 'verified' | 'reviewed' | 'human_oversight' | 'constitutional';

export interface SafetyStatus {
  current_tier: SafetyTier;
  pending_approvals: number;
  recent_decisions: Array<{
    id: string;
    tier: SafetyTier;
    decision: 'approved' | 'rejected';
    timestamp: string;
  }>;
}

export interface HumanAnchorRequest {
  id: string;
  type: string;
  description: string;
  claim: string;
  importance: number;
  created_at: string;
  status: 'pending' | 'approved' | 'rejected';
}

// Plasticity
export interface ModuleInfo {
  id: string;
  name: string;
  type: string;
  version: string;
  status: 'active' | 'inactive' | 'deprecated';
  dependencies: string[];
}

export interface NASCandidate {
  id: string;
  architecture: string;
  performance_score: number;
  efficiency_score: number;
  status: 'evaluating' | 'accepted' | 'rejected';
}

// Scale-Invariant Metrics
export interface ScaleInvariantMetric {
  id: string;
  name: string;
  domain: 'emergence' | 'coherence' | 'alignment' | 'capability' | 'efficiency';
  value: number;  // 0-100
  trend: number;  // percentage change
  threshold_low: number;
  threshold_high: number;
}
