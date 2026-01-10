import { describe, it, expect, beforeEach } from 'vitest'
import { act } from '@testing-library/react'
import { useRSIStore } from '../../stores/rsiStore'
import type { PhaseStatus, RalphLoopStatus, GrowthMetrics, SafetyStatus, ScaleInvariantMetric } from '../../types/rsi'
import type { TreasuryStatus, RevenueReport, MarketplaceStats } from '../../types/economic'

describe('rsiStore', () => {
  beforeEach(() => {
    // Reset to default state
    act(() => {
      useRSIStore.setState({
        phases: [
          { phase: 'phase_0_archive', name: 'Archive', description: 'Pre-ASI codebase snapshot', progress: 100, completed: true, components: [] },
          { phase: 'phase_1_foundation', name: 'Foundation', description: 'Core RSI components', progress: 100, completed: true, components: [] },
          { phase: 'phase_2_enablement', name: 'Enablement', description: 'ASI enablement core', progress: 100, completed: true, components: [] },
          { phase: 'phase_3_advanced', name: 'Advanced', description: 'NAS, MetaArchitect, Recursion', progress: 100, completed: true, components: [] },
          { phase: 'phase_4_scaling', name: 'Scale & Safety', description: 'Capability explosion handling', progress: 100, completed: true, components: [] },
          { phase: 'phase_5_economic', name: 'Economic', description: 'Economic autonomy', progress: 100, completed: true, components: [] },
        ],
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
      })
    })
  })

  describe('initial state', () => {
    it('should have 6 phases by default', () => {
      expect(useRSIStore.getState().phases).toHaveLength(6)
    })

    it('should have phase_5_economic as current phase', () => {
      expect(useRSIStore.getState().currentPhase).toBe('phase_5_economic')
    })

    it('should have ralph loop not running', () => {
      expect(useRSIStore.getState().ralphLoop.running).toBe(false)
    })

    it('should have default growth metrics', () => {
      const metrics = useRSIStore.getState().growthMetrics
      expect(metrics.current_rate).toBe(0)
      expect(metrics.trend).toBe('stable')
      expect(metrics.phase).toBe('normal')
    })

    it('should have automatic safety tier', () => {
      expect(useRSIStore.getState().safetyStatus.current_tier).toBe('automatic')
    })

    it('should have empty scale invariant metrics', () => {
      expect(useRSIStore.getState().scaleInvariantMetrics).toHaveLength(0)
    })

    it('should have null economic statuses', () => {
      expect(useRSIStore.getState().treasuryStatus).toBeNull()
      expect(useRSIStore.getState().revenueReport).toBeNull()
      expect(useRSIStore.getState().marketplaceStats).toBeNull()
    })
  })

  describe('setPhases', () => {
    it('should update phases', () => {
      const newPhases: PhaseStatus[] = [
        { phase: 'phase_0_archive', name: 'Archive', description: 'Updated', progress: 50, completed: false, components: [] },
      ]

      act(() => {
        useRSIStore.getState().setPhases(newPhases)
      })

      expect(useRSIStore.getState().phases).toHaveLength(1)
      expect(useRSIStore.getState().phases[0].progress).toBe(50)
    })

    it('should replace all phases', () => {
      const newPhases: PhaseStatus[] = [
        { phase: 'phase_1_foundation', name: 'Foundation', description: 'Test', progress: 25, completed: false, components: ['comp1'] },
        { phase: 'phase_2_enablement', name: 'Enablement', description: 'Test2', progress: 75, completed: false, components: [] },
      ]

      act(() => {
        useRSIStore.getState().setPhases(newPhases)
      })

      expect(useRSIStore.getState().phases).toEqual(newPhases)
    })
  })

  describe('setRalphLoop', () => {
    it('should set ralph loop to running', () => {
      const newStatus: RalphLoopStatus = {
        running: true,
        iteration: 5,
        max_iterations: 100,
        completion_promise: null,
        current_phase: 'REFLECT',
      }

      act(() => {
        useRSIStore.getState().setRalphLoop(newStatus)
      })

      expect(useRSIStore.getState().ralphLoop.running).toBe(true)
      expect(useRSIStore.getState().ralphLoop.iteration).toBe(5)
      expect(useRSIStore.getState().ralphLoop.current_phase).toBe('REFLECT')
    })

    it('should update iteration count', () => {
      act(() => {
        useRSIStore.getState().setRalphLoop({
          ...useRSIStore.getState().ralphLoop,
          iteration: 42,
        })
      })

      expect(useRSIStore.getState().ralphLoop.iteration).toBe(42)
    })

    it('should update current phase', () => {
      act(() => {
        useRSIStore.getState().setRalphLoop({
          ...useRSIStore.getState().ralphLoop,
          current_phase: 'CRYSTALLIZE',
        })
      })

      expect(useRSIStore.getState().ralphLoop.current_phase).toBe('CRYSTALLIZE')
    })
  })

  describe('setGrowthMetrics', () => {
    it('should update growth metrics', () => {
      const newMetrics: GrowthMetrics = {
        current_rate: 0.05,
        trend: 'accelerating',
        phase: 'explosive',
        resource_utilization: 0.8,
        value_drift: 0.02,
      }

      act(() => {
        useRSIStore.getState().setGrowthMetrics(newMetrics)
      })

      expect(useRSIStore.getState().growthMetrics).toEqual(newMetrics)
    })

    it('should update individual metric values', () => {
      act(() => {
        useRSIStore.getState().setGrowthMetrics({
          ...useRSIStore.getState().growthMetrics,
          current_rate: 0.15,
        })
      })

      expect(useRSIStore.getState().growthMetrics.current_rate).toBe(0.15)
    })
  })

  describe('setSafetyStatus', () => {
    it('should update safety status', () => {
      const newStatus: SafetyStatus = {
        current_tier: 'human_required',
        pending_approvals: 3,
        recent_decisions: [
          { id: 'd1', decision: 'approved', timestamp: '2026-01-01' },
        ],
      }

      act(() => {
        useRSIStore.getState().setSafetyStatus(newStatus)
      })

      expect(useRSIStore.getState().safetyStatus.current_tier).toBe('human_required')
      expect(useRSIStore.getState().safetyStatus.pending_approvals).toBe(3)
    })

    it('should update pending approvals count', () => {
      act(() => {
        useRSIStore.getState().setSafetyStatus({
          ...useRSIStore.getState().safetyStatus,
          pending_approvals: 10,
        })
      })

      expect(useRSIStore.getState().safetyStatus.pending_approvals).toBe(10)
    })
  })

  describe('setScaleInvariantMetrics', () => {
    it('should set scale invariant metrics', () => {
      const metrics: ScaleInvariantMetric[] = [
        { name: 'metric1', value: 0.95, threshold: 0.9 },
        { name: 'metric2', value: 0.88, threshold: 0.85 },
      ]

      act(() => {
        useRSIStore.getState().setScaleInvariantMetrics(metrics)
      })

      expect(useRSIStore.getState().scaleInvariantMetrics).toHaveLength(2)
      expect(useRSIStore.getState().scaleInvariantMetrics[0].name).toBe('metric1')
    })

    it('should replace all metrics', () => {
      // First set some metrics
      act(() => {
        useRSIStore.getState().setScaleInvariantMetrics([
          { name: 'old', value: 0.5, threshold: 0.5 },
        ])
      })

      // Then replace with new metrics
      act(() => {
        useRSIStore.getState().setScaleInvariantMetrics([
          { name: 'new', value: 0.9, threshold: 0.8 },
        ])
      })

      expect(useRSIStore.getState().scaleInvariantMetrics).toHaveLength(1)
      expect(useRSIStore.getState().scaleInvariantMetrics[0].name).toBe('new')
    })
  })

  describe('setTreasuryStatus', () => {
    it('should set treasury status', () => {
      const treasury: TreasuryStatus = {
        balance: 10000,
        currency: 'USD',
        last_deposit: '2026-01-01T00:00:00Z',
        allocations: { research: 5000, operations: 5000 },
      }

      act(() => {
        useRSIStore.getState().setTreasuryStatus(treasury)
      })

      expect(useRSIStore.getState().treasuryStatus).toEqual(treasury)
    })

    it('should update existing treasury status', () => {
      act(() => {
        useRSIStore.getState().setTreasuryStatus({
          balance: 5000,
          currency: 'USD',
          last_deposit: '2026-01-01',
          allocations: {},
        })
      })

      act(() => {
        useRSIStore.getState().setTreasuryStatus({
          balance: 15000,
          currency: 'EUR',
          last_deposit: '2026-01-02',
          allocations: {},
        })
      })

      expect(useRSIStore.getState().treasuryStatus?.balance).toBe(15000)
      expect(useRSIStore.getState().treasuryStatus?.currency).toBe('EUR')
    })
  })

  describe('setRevenueReport', () => {
    it('should set revenue report', () => {
      const report: RevenueReport = {
        total: 50000,
        by_source: { api: 30000, marketplace: 20000 },
        period: 'monthly',
        start_date: '2026-01-01',
        end_date: '2026-01-31',
      }

      act(() => {
        useRSIStore.getState().setRevenueReport(report)
      })

      expect(useRSIStore.getState().revenueReport).toEqual(report)
    })

    it('should replace existing revenue report', () => {
      act(() => {
        useRSIStore.getState().setRevenueReport({
          total: 1000,
          by_source: {},
          period: 'weekly',
          start_date: '',
          end_date: '',
        })
      })

      act(() => {
        useRSIStore.getState().setRevenueReport({
          total: 5000,
          by_source: { training: 5000 },
          period: 'monthly',
          start_date: '',
          end_date: '',
        })
      })

      expect(useRSIStore.getState().revenueReport?.total).toBe(5000)
    })
  })

  describe('setMarketplaceStats', () => {
    it('should set marketplace stats', () => {
      const stats: MarketplaceStats = {
        total_listings: 50,
        total_sales: 100,
        revenue: 25000,
        top_items: ['Module A', 'Module B'],
      }

      act(() => {
        useRSIStore.getState().setMarketplaceStats(stats)
      })

      expect(useRSIStore.getState().marketplaceStats).toEqual(stats)
    })
  })

  describe('state interactions', () => {
    it('should maintain independent state updates', () => {
      act(() => {
        useRSIStore.getState().setRalphLoop({
          ...useRSIStore.getState().ralphLoop,
          running: true,
          iteration: 10,
        })
      })

      // Other state should remain unchanged
      expect(useRSIStore.getState().phases).toHaveLength(6)
      expect(useRSIStore.getState().treasuryStatus).toBeNull()
    })

    it('should handle multiple simultaneous updates', () => {
      act(() => {
        useRSIStore.getState().setRalphLoop({
          running: true,
          iteration: 5,
          max_iterations: 100,
          completion_promise: null,
          current_phase: 'VERIFY',
        })
        useRSIStore.getState().setGrowthMetrics({
          current_rate: 0.1,
          trend: 'accelerating',
          phase: 'explosive',
          resource_utilization: 0.9,
          value_drift: 0.01,
        })
        useRSIStore.getState().setSafetyStatus({
          current_tier: 'collaborative',
          pending_approvals: 5,
          recent_decisions: [],
        })
      })

      const state = useRSIStore.getState()
      expect(state.ralphLoop.running).toBe(true)
      expect(state.growthMetrics.current_rate).toBe(0.1)
      expect(state.safetyStatus.current_tier).toBe('collaborative')
    })
  })
})
