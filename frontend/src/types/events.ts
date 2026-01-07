// WebSocket event types from BYRD backend

export type EventType =
  // System events
  | 'system_started'
  | 'system_stopped'
  | 'system_reset'
  | 'awakening'

  // Core events
  | 'experience_created'
  | 'belief_created'
  | 'desire_created'
  | 'capability_added'
  | 'reflection_created'
  | 'dream_cycle_start'
  | 'dream_cycle_end'
  | 'seek_cycle_start'
  | 'inner_voice'

  // RSI events
  | 'rsi_cycle_start'
  | 'rsi_cycle_complete'
  | 'rsi_emergence_verified'
  | 'rsi_heuristic_crystallized'

  // Plasticity events
  | 'plasticity_module_registered'
  | 'plasticity_composition'
  | 'nas_candidate_found'
  | 'meta_architect_proposal'

  // Scaling events
  | 'growth_rate_update'
  | 'explosion_phase_change'
  | 'resource_scaling'
  | 'value_stability_alert'

  // Economic events
  | 'treasury_deposit'
  | 'treasury_allocation'
  | 'service_purchase'
  | 'investment_complete'
  | 'revenue_update'

  // Verification events
  | 'human_anchor_requested'
  | 'human_anchor_processed'
  | 'safety_tier_change'
  | 'cross_scale_verification'

  // Quantum events
  | 'quantum_influence';

export interface ByrdEvent {
  type: EventType;
  data: Record<string, unknown>;
  timestamp: string;
  id?: string;
}

export interface SystemStatus {
  running: boolean;
  dream_count: number;
  seek_count: number;
  capabilities: string[];
  desires: Array<{
    id: string;
    description: string;
    intensity: number;
  }>;
  beliefs: Array<{
    id: string;
    content: string;
    confidence: number;
  }>;
}
