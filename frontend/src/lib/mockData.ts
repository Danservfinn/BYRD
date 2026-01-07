/**
 * Mock data for BYRD demo when backend is disconnected.
 * This showcases what the system looks like with real data.
 */

import type { ByrdEvent } from '../types/events';

export const MOCK_EVENTS: ByrdEvent[] = [
  {
    id: 'mock-1',
    type: 'system_started',
    timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    data: {
      message: 'BYRD system initialized',
      version: '1.0.0'
    }
  },
  {
    id: 'mock-2',
    type: 'belief_created',
    timestamp: new Date(Date.now() - 1000 * 60 * 4).toISOString(),
    data: {
      content: 'Recursive self-improvement requires verification bounds',
      confidence: 0.92,
      source: 'reflection'
    }
  },
  {
    id: 'mock-3',
    type: 'desire_created',
    timestamp: new Date(Date.now() - 1000 * 60 * 3).toISOString(),
    data: {
      description: 'Improve verification coverage to 95%',
      urgency: 0.85,
      domain: 'verification'
    }
  },
  {
    id: 'mock-4',
    type: 'rsi_cycle_complete',
    timestamp: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
    data: {
      cycle_id: 'rsi-cycle-42',
      phase_reached: 'MEASURE',
      duration_ms: 45000,
      improvements: ['Added property checks', 'Refactored memory graph']
    }
  },
  {
    id: 'mock-5',
    type: 'rsi_emergence_verified',
    timestamp: new Date(Date.now() - 1000 * 60 * 1).toISOString(),
    data: {
      type: 'novel_strategy',
      description: 'Discovered new verification pattern combining execution + semantic analysis',
      confidence: 0.78
    }
  },
  {
    id: 'mock-6',
    type: 'rsi_heuristic_crystallized',
    timestamp: new Date(Date.now() - 1000 * 50).toISOString(),
    data: {
      heuristic: 'Multi-verifier consensus exceeds individual verifier accuracy',
      domain: 'verification',
      confidence: 0.95
    }
  },
  {
    id: 'mock-7',
    type: 'experience_created',
    timestamp: new Date(Date.now() - 1000 * 40).toISOString(),
    data: {
      content: 'Successfully verified improvement using lattice approach',
      type: 'verification'
    }
  },
  {
    id: 'mock-8',
    type: 'rsi_cycle_start',
    timestamp: new Date(Date.now() - 1000 * 30).toISOString(),
    data: {
      phase: 'PRACTICE',
      cycle_id: 'rsi-cycle-43',
      status: 'active'
    }
  },
  {
    id: 'mock-9',
    type: 'capability_added',
    timestamp: new Date(Date.now() - 1000 * 20).toISOString(),
    data: {
      capability: 'complexity-aware task routing',
      proficiency: 0.87
    }
  },
  {
    id: 'mock-10',
    type: 'reflection_created',
    timestamp: new Date(Date.now() - 1000 * 10).toISOString(),
    data: {
      insights_count: 5,
      beliefs_created: 3,
      depth: 'deep'
    }
  }
];

export const MOCK_SYSTEM_STATUS = {
  status: 'running',
  cycle_id: 'rsi-cycle-43',
  current_phase: 'PRACTICE',
  completed_phases: ['REFLECT', 'VERIFY', 'COLLAPSE', 'ROUTE'],
  uptime_seconds: 7200,
  memory_nodes: 1247,
  capabilities: 89,
  desires_processed: 156
};

export const MOCK_RSI_STATUS = {
  current_phase: 'PRACTICE',
  cycle_number: 43,
  total_cycles: 43,
  phase_progress: 0.67,
  completed_phases: ['REFLECT', 'VERIFY', 'COLLAPSE', 'ROUTE'],
  phase_description: 'Executing practice with TDD approach',
  desires_generated: 8,
  desires_verified: 5,
  desires_selected: 1
};

export const MOCK_VERIFICATION_STATUS = {
  verifiers: [
    {
      id: 'execution',
      name: 'Execution Tests',
      type: 'execution',
      status: 'active',
      last_result: 'pass',
      confidence: 0.95,
      checks_performed: 234
    },
    {
      id: 'property',
      name: 'Property Checks',
      type: 'property',
      status: 'active',
      last_result: 'pass',
      confidence: 0.88,
      checks_performed: 156
    },
    {
      id: 'llm_critique',
      name: 'LLM Critique',
      type: 'llm_critique',
      status: 'active',
      last_result: 'pass',
      confidence: 0.82,
      checks_performed: 89
    },
    {
      id: 'adversarial',
      name: 'Adversarial Probes',
      type: 'adversarial',
      status: 'active',
      last_result: 'inconclusive',
      confidence: 0.65,
      checks_performed: 45
    },
    {
      id: 'human_spot',
      name: 'Human Spot Checks',
      type: 'human_spot',
      status: 'pending',
      last_result: null,
      confidence: 0.0,
      checks_performed: 0
    }
  ],
  consensus_threshold: 0.6,
  last_consensus: true,
  total_verifications: 524
};

export const MOCK_ECONOMIC_STATUS = {
  treasury_balance: 847.32,
  currency: 'credits',
  revenue_this_month: 2341.56,
  revenue_last_month: 1892.43,
  growth_rate: 23.7,
  active_services: 5,
  pending_requests: 3
};

export const MOCK_PLASTICITY_MODULES = [
  {
    id: 'core-1',
    name: 'Memory Graph Reasoner',
    type: 'core',
    description: 'Neo4j-based graph reasoning',
    complexity: 0.78
  },
  {
    id: 'core-2',
    name: 'Quantum Collapse',
    type: 'core',
    description: 'Quantum-inspired desire selection',
    complexity: 0.82
  },
  {
    id: 'emergent-1',
    name: 'Verification Lattice',
    type: 'emergent',
    description: 'Multi-verifier composition',
    complexity: 0.91
  },
  {
    id: 'emergent-2',
    name: 'Complexity Router',
    type: 'emergent',
    description: '45% collapse threshold routing',
    complexity: 0.75
  },
  {
    id: 'composed-1',
    name: 'Bounded RSI Engine',
    type: 'composed',
    description: 'Lattice + Router + Stratification',
    complexity: 0.94
  }
];

export const MOCK_SCALING_METRICS = {
  growth_rate: 2.34,
  phase: 'explosive',
  entropic_drift: 0.12,
  generalization_gap: 0.08,
  capability_diversity: 0.87
};

export const MOCK_CONSCIOUSNESS_FRAMES = [
  {
    cycle_id: 'rsi-cycle-43',
    beliefs_delta: 3,
    capabilities_delta: 1,
    entropy_score: 0.73,
    timestamp: new Date(Date.now() - 1000 * 60).toISOString()
  },
  {
    cycle_id: 'rsi-cycle-42',
    beliefs_delta: 2,
    capabilities_delta: 0,
    entropy_score: 0.68,
    timestamp: new Date(Date.now() - 1000 * 120).toISOString()
  },
  {
    cycle_id: 'rsi-cycle-41',
    beliefs_delta: 5,
    capabilities_delta: 2,
    entropy_score: 0.71,
    timestamp: new Date(Date.now() - 1000 * 180).toISOString()
  }
];

/**
 * Initialize mock data if store is empty
 */
export function initializeMockData(store: any) {
  if (store.events.length === 0) {
    MOCK_EVENTS.forEach(event => store.addEvent(event));
  }
}
