import { useCallback, useState } from 'react';
import type { SystemStatus } from '../types/events';

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
  const getRSIStatus = useCallback(async () => {
    return fetchWithError('/rsi/status');
  }, [fetchWithError]);

  const getRSIMetrics = useCallback(async () => {
    return fetchWithError('/rsi/metrics');
  }, [fetchWithError]);

  const getRalphLoopStatus = useCallback(async () => {
    return fetchWithError('/rsi/ralph-loop');
  }, [fetchWithError]);

  // Economic endpoints
  const getTreasuryStatus = useCallback(async () => {
    return fetchWithError('/economic/treasury');
  }, [fetchWithError]);

  const getRevenueReport = useCallback(async () => {
    return fetchWithError('/economic/revenue');
  }, [fetchWithError]);

  const getMarketplaceListings = useCallback(async () => {
    return fetchWithError('/economic/marketplace');
  }, [fetchWithError]);

  // Scaling endpoints
  const getGrowthRate = useCallback(async () => {
    return fetchWithError('/scaling/growth-rate');
  }, [fetchWithError]);

  const getExplosionPhase = useCallback(async () => {
    return fetchWithError('/scaling/explosion-phase');
  }, [fetchWithError]);

  // Verification endpoints
  const getHumanAnchoringQueue = useCallback(async () => {
    return fetchWithError('/verification/human-anchoring');
  }, [fetchWithError]);

  const processHumanValidation = useCallback(async (requestId: string, response: { approved: boolean; notes?: string }) => {
    return fetchWithError(`/verification/human-anchoring/${requestId}`, {
      method: 'POST',
      body: JSON.stringify(response),
    });
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
    // Verification
    getHumanAnchoringQueue,
    processHumanValidation,
  };
}
