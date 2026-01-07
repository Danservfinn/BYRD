// API Response Types

export interface ChatMessage {
  id: string;
  type: 'user' | 'byrd' | 'system';
  content: string;
  timestamp: string;
}

export interface RSIMetricsResponse {
  recent_cycles?: Array<{
    cycle_id: string;
    phase_reached: string;
    domain?: string;
    desires_generated?: number;
    desires_verified?: number;
    practice_attempted?: boolean;
    practice_succeeded?: boolean;
    heuristic_crystallized?: string;
    completed_at?: string;
  }>;
  current_phase?: string;
  completed_phases?: string[];
}

export interface TreasuryResponse {
  balance: number;
  total_revenue: number;
  total_expenses: number;
}

export interface RevenueResponse {
  history: Array<{
    date: string;
    revenue: number;
    expenses: number;
  }>;
}

export interface MarketplaceResponse {
  listings: Array<{
    id: string;
    type: 'service' | 'capability' | 'knowledge';
    title: string;
    description: string;
    price: number;
    status: 'active' | 'pending' | 'sold';
    created_at: string;
  }>;
}

export interface PlasticityModulesResponse {
  modules: Array<{
    id: string;
    name: string;
    type: 'core' | 'emergent' | 'composed';
    status: 'active' | 'dormant' | 'evolving';
    connections: number;
    performance: number;
    created_at: string;
  }>;
  graph?: {
    nodes: Array<{
      id: string;
      name: string;
      type: string;
      x?: number;
      y?: number;
    }>;
    links: Array<{
      source: string;
      target: string;
      strength: number;
    }>;
  };
}

export interface NASCandidatesResponse {
  candidates: Array<{
    id: string;
    architecture: string;
    fitness: number;
    generation: number;
    status: 'evaluating' | 'promising' | 'rejected' | 'selected';
    metrics: {
      accuracy: number;
      efficiency: number;
      novelty: number;
    };
  }>;
}

export interface ScalingMetricsResponse {
  growth?: {
    current_rate: number;
    target_rate: number;
    trend: 'accelerating' | 'stable' | 'decelerating';
    history: number[];
  };
  explosion_phase?: {
    current: 'dormant' | 'awakening' | 'accelerating' | 'explosive' | 'transcendent';
    progress: number;
    threshold: number;
    estimated_transition: string | null;
  };
  entropic_drift?: {
    solution_diversity: number;
    benchmark_trend: number;
    strategy_entropy: number;
    generalization_gap: number;
    overall_severity: 'none' | 'minor' | 'moderate' | 'severe' | 'critical';
    recommendations: string[];
  };
}

export interface VerificationStatusResponse {
  lattice?: {
    verifiers: Array<{
      id: string;
      name: string;
      type: string;
      status: 'active' | 'pending' | 'error' | 'disabled';
      last_result: 'pass' | 'fail' | 'inconclusive' | null;
      confidence: number;
      checks_performed: number;
    }>;
    consensus_threshold: number;
    last_consensus: boolean;
    total_verifications: number;
  };
  safety?: {
    current_tier: 'green' | 'yellow' | 'orange' | 'red';
    tier_confidence: number;
    active_constraints: string[];
    recent_violations: number;
    last_assessment: string;
  };
}

export interface HumanAnchoringQueueResponse {
  queue: Array<{
    id: string;
    type: 'spot_check' | 'calibration' | 'override' | 'approval';
    priority: 'low' | 'medium' | 'high' | 'critical';
    description: string;
    context: string;
    created_at: string;
    expires_at: string | null;
  }>;
}

export interface DirectionResponse {
  content: string;
}

export interface GovernanceHistoryResponse {
  messages: Array<{
    id: string;
    type: 'user' | 'system' | 'byrd';
    content: string;
    timestamp: string;
  }>;
}

export interface GovernanceCommandResponse {
  response: string;
}

export interface DesireInjectionResponse {
  desire: {
    id: string;
    description: string;
    urgency: number;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    injected_at: string;
  };
}

export interface MemoryGraphResponse {
  graph: {
    nodes: Array<{
      id: string;
      type: 'belief' | 'desire' | 'experience' | 'reflection' | 'capability' | 'goal';
      label: string;
      strength: number;
      created_at: string;
    }>;
    links: Array<{
      source: string;
      target: string;
      type: string;
      weight: number;
    }>;
  };
}

export interface RSIStatusResponse {
  current_phase?: string;
  completed_phases?: string[];
  phases?: string[];
}
