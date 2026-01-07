import { useCallback, useState } from 'react';
import type { SystemStatus } from '../types/events';
import type {
  RSIMetricsResponse,
  TreasuryResponse,
  RevenueResponse,
  MarketplaceResponse,
  PlasticityModulesResponse,
  NASCandidatesResponse,
  ScalingMetricsResponse,
  VerificationStatusResponse,
  HumanAnchoringQueueResponse,
  DirectionResponse,
  GovernanceHistoryResponse,
  GovernanceCommandResponse,
  DesireInjectionResponse,
  MemoryGraphResponse,
  RSIStatusResponse,
} from '../types/api';

const API_BASE = '/api';

export function useByrdAPI() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchWithError = useCallback(async <T>(url: string, options?: RequestInit): Promise<T | null> => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}${url}`, {
        headers: {
          'Content-Type': 'application/json',
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error';
      setError(message);
      console.error(`API Error: ${message}`);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getStatus = useCallback(async (): Promise<SystemStatus | null> => {
    return fetchWithError<SystemStatus>('/status');
  }, [fetchWithError]);

  const startByrd = useCallback(async (): Promise<boolean> => {
    const result = await fetchWithError('/start', { method: 'POST' });
    return result !== null;
  }, [fetchWithError]);

  const stopByrd = useCallback(async (): Promise<boolean> => {
    const result = await fetchWithError('/stop', { method: 'POST' });
    return result !== null;
  }, [fetchWithError]);

  const resetByrd = useCallback(async (hardReset = false): Promise<boolean> => {
    const result = await fetchWithError('/reset', {
      method: 'POST',
      body: JSON.stringify({ hard_reset: hardReset }),
    });
    return result !== null;
  }, [fetchWithError]);

  // RSI-specific endpoints
  const getRSIStatus = useCallback(async (): Promise<RSIStatusResponse | null> => {
    return fetchWithError<RSIStatusResponse>('/rsi/status');
  }, [fetchWithError]);

  const getRSIMetrics = useCallback(async (): Promise<RSIMetricsResponse | null> => {
    return fetchWithError<RSIMetricsResponse>('/rsi/metrics');
  }, [fetchWithError]);

  const getRalphLoopStatus = useCallback(async () => {
    return fetchWithError('/rsi/ralph-loop');
  }, [fetchWithError]);

  // Economic endpoints
  const getTreasuryStatus = useCallback(async (): Promise<TreasuryResponse | null> => {
    return fetchWithError<TreasuryResponse>('/economic/treasury');
  }, [fetchWithError]);

  const getRevenueReport = useCallback(async (): Promise<RevenueResponse | null> => {
    return fetchWithError<RevenueResponse>('/economic/revenue');
  }, [fetchWithError]);

  const getMarketplaceListings = useCallback(async (): Promise<MarketplaceResponse | null> => {
    return fetchWithError<MarketplaceResponse>('/economic/marketplace');
  }, [fetchWithError]);

  // Scaling endpoints
  const getGrowthRate = useCallback(async () => {
    return fetchWithError('/scaling/growth-rate');
  }, [fetchWithError]);

  const getExplosionPhase = useCallback(async () => {
    return fetchWithError('/scaling/explosion-phase');
  }, [fetchWithError]);

  // Verification endpoints
  const getHumanAnchoringQueue = useCallback(async (): Promise<HumanAnchoringQueueResponse | null> => {
    return fetchWithError<HumanAnchoringQueueResponse>('/verification/human-anchoring');
  }, [fetchWithError]);

  const processHumanValidation = useCallback(async (requestId: string, response: { approved: boolean; notes?: string }) => {
    return fetchWithError(`/verification/human-anchoring/${requestId}`, {
      method: 'POST',
      body: JSON.stringify(response),
    });
  }, [fetchWithError]);

  const submitAnchoringResponse = useCallback(async (requestId: string, approved: boolean) => {
    return fetchWithError(`/verification/human-anchoring/${requestId}`, {
      method: 'POST',
      body: JSON.stringify({ approved }),
    });
  }, [fetchWithError]);

  const getVerificationStatus = useCallback(async (): Promise<VerificationStatusResponse | null> => {
    return fetchWithError<VerificationStatusResponse>('/verification/status');
  }, [fetchWithError]);

  // Plasticity endpoints
  const getPlasticityModules = useCallback(async (): Promise<PlasticityModulesResponse | null> => {
    return fetchWithError<PlasticityModulesResponse>('/plasticity/modules');
  }, [fetchWithError]);

  const getNASCandidates = useCallback(async (): Promise<NASCandidatesResponse | null> => {
    return fetchWithError<NASCandidatesResponse>('/plasticity/nas');
  }, [fetchWithError]);

  // Scaling endpoints (additional)
  const getScalingMetrics = useCallback(async (): Promise<ScalingMetricsResponse | null> => {
    return fetchWithError<ScalingMetricsResponse>('/scaling/metrics');
  }, [fetchWithError]);

  // Control endpoints
  const startRSICycle = useCallback(async () => {
    return fetchWithError('/rsi/cycle', { method: 'POST' });
  }, [fetchWithError]);

  const stopRSICycle = useCallback(async () => {
    return fetchWithError('/rsi/stop', { method: 'POST' });
  }, [fetchWithError]);

  const resetSystem = useCallback(async () => {
    return fetchWithError('/system/reset', { method: 'POST' });
  }, [fetchWithError]);

  const getSystemStatus = useCallback(async () => {
    return fetchWithError('/system/status');
  }, [fetchWithError]);

  // Governance endpoints
  const getDirection = useCallback(async (): Promise<DirectionResponse | null> => {
    return fetchWithError<DirectionResponse>('/governance/direction');
  }, [fetchWithError]);

  const updateDirection = useCallback(async (content: string) => {
    return fetchWithError('/governance/direction', {
      method: 'POST',
      body: JSON.stringify({ content }),
    });
  }, [fetchWithError]);

  const sendGovernanceCommand = useCallback(async (command: string): Promise<GovernanceCommandResponse | null> => {
    return fetchWithError<GovernanceCommandResponse>('/governance/command', {
      method: 'POST',
      body: JSON.stringify({ command }),
    });
  }, [fetchWithError]);

  const getGovernanceHistory = useCallback(async (): Promise<GovernanceHistoryResponse | null> => {
    return fetchWithError<GovernanceHistoryResponse>('/governance/history');
  }, [fetchWithError]);

  const injectDesire = useCallback(async (description: string, urgency: number): Promise<DesireInjectionResponse | null> => {
    return fetchWithError<DesireInjectionResponse>('/governance/inject-desire', {
      method: 'POST',
      body: JSON.stringify({ description, urgency }),
    });
  }, [fetchWithError]);

  const getInjectedDesires = useCallback(async () => {
    return fetchWithError('/governance/desires');
  }, [fetchWithError]);

  // Memory/Visualization endpoints
  const getMemoryGraph = useCallback(async (): Promise<MemoryGraphResponse | null> => {
    return fetchWithError<MemoryGraphResponse>('/memory/graph');
  }, [fetchWithError]);

  return {
    loading,
    error,
    // System controls
    getStatus,
    startByrd,
    stopByrd,
    resetByrd,
    // RSI
    getRSIStatus,
    getRSIMetrics,
    getRalphLoopStatus,
    // Economic
    getTreasuryStatus,
    getRevenueReport,
    getMarketplaceListings,
    // Scaling
    getGrowthRate,
    getExplosionPhase,
    getScalingMetrics,
    // Verification
    getHumanAnchoringQueue,
    processHumanValidation,
    submitAnchoringResponse,
    getVerificationStatus,
    // Plasticity
    getPlasticityModules,
    getNASCandidates,
    // Controls
    startRSICycle,
    stopRSICycle,
    resetSystem,
    getSystemStatus,
    // Governance
    getDirection,
    updateDirection,
    sendGovernanceCommand,
    getGovernanceHistory,
    injectDesire,
    getInjectedDesires,
    // Memory/Visualization
    getMemoryGraph,
  };
}
