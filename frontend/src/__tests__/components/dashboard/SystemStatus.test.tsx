import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { SystemStatus } from '../../../components/dashboard/SystemStatus'

// Mock the useByrdAPI hook
vi.mock('../../../hooks/useByrdAPI', () => ({
  useByrdAPI: vi.fn(),
}))

import { useByrdAPI } from '../../../hooks/useByrdAPI'

describe('SystemStatus', () => {
  let mockGetRSIStatus: ReturnType<typeof vi.fn>

  beforeEach(() => {
    mockGetRSIStatus = vi.fn().mockResolvedValue({
      current_phase: 'idle',
      cycle_number: 0,
    })

    vi.mocked(useByrdAPI).mockReturnValue({
      getRSIStatus: mockGetRSIStatus,
      loading: false,
      error: null,
      backendAvailable: true,
      getStatus: vi.fn(),
      startByrd: vi.fn(),
      stopByrd: vi.fn(),
      resetByrd: vi.fn(),
      getRSIMetrics: vi.fn(),
      getRalphLoopStatus: vi.fn(),
      getTreasuryStatus: vi.fn(),
      getRevenueReport: vi.fn(),
      getMarketplaceListings: vi.fn(),
      getGrowthRate: vi.fn(),
      getExplosionPhase: vi.fn(),
      getScalingMetrics: vi.fn(),
      getHumanAnchoringQueue: vi.fn(),
      processHumanValidation: vi.fn(),
      submitAnchoringResponse: vi.fn(),
      getVerificationStatus: vi.fn(),
      getPlasticityModules: vi.fn(),
      getNASCandidates: vi.fn(),
      startRSICycle: vi.fn(),
      stopRSICycle: vi.fn(),
      resetSystem: vi.fn(),
      getSystemStatus: vi.fn(),
      getDirection: vi.fn(),
      updateDirection: vi.fn(),
      sendGovernanceCommand: vi.fn(),
      getGovernanceHistory: vi.fn(),
      injectDesire: vi.fn(),
      getInjectedDesires: vi.fn(),
      getMemoryGraph: vi.fn(),
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('rendering', () => {
    it('should render loading state when loading and no status', () => {
      mockGetRSIStatus.mockResolvedValue(null)
      vi.mocked(useByrdAPI).mockReturnValue({
        ...vi.mocked(useByrdAPI)(),
        loading: true,
      })

      render(<SystemStatus />)

      expect(screen.getByText('Loading...')).toBeInTheDocument()
    })

    it('should render system status header', async () => {
      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('System Status')).toBeInTheDocument()
      })
    })

    it('should display idle status when no phase is active', async () => {
      mockGetRSIStatus.mockResolvedValue({
        current_phase: null,
        cycle_number: 0,
      })

      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('Idle')).toBeInTheDocument()
      })
    })

    it('should display running status when phase is active', async () => {
      mockGetRSIStatus.mockResolvedValue({
        current_phase: 'reflect',
        cycle_number: 5,
      })

      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('Running')).toBeInTheDocument()
      })
    })
  })

  describe('RSI status fetching', () => {
    it('should fetch RSI status on mount', async () => {
      render(<SystemStatus />)

      await waitFor(() => {
        expect(mockGetRSIStatus).toHaveBeenCalled()
      })
    })

    it('should handle fetch errors gracefully', async () => {
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
      mockGetRSIStatus.mockRejectedValue(new Error('Network error'))

      render(<SystemStatus />)

      await waitFor(() => {
        expect(consoleSpy).toHaveBeenCalledWith(
          'Failed to fetch RSI status:',
          expect.any(Error)
        )
      })

      consoleSpy.mockRestore()
    })
  })

  describe('phase display', () => {
    it('should display current phase label', async () => {
      mockGetRSIStatus.mockResolvedValue({
        current_phase: 'reflect',
        cycle_number: 10,
      })

      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('reflect')).toBeInTheDocument()
      })
    })

    it('should display all 8 RSI phase blocks', async () => {
      mockGetRSIStatus.mockResolvedValue({
        current_phase: 'verify',
        cycle_number: 5,
        completed_phases: ['reflect'],
      })

      render(<SystemStatus />)

      await waitFor(() => {
        // Check for phase block titles (abbreviated)
        expect(screen.getByTitle('Reflect')).toBeInTheDocument()
        expect(screen.getByTitle('Verify')).toBeInTheDocument()
        expect(screen.getByTitle('Collapse')).toBeInTheDocument()
        expect(screen.getByTitle('Route')).toBeInTheDocument()
        expect(screen.getByTitle('Practice')).toBeInTheDocument()
        expect(screen.getByTitle('Record')).toBeInTheDocument()
        expect(screen.getByTitle('Crystallize')).toBeInTheDocument()
        expect(screen.getByTitle('Measure')).toBeInTheDocument()
      })
    })
  })

  describe('stats display', () => {
    it('should display cycle count', async () => {
      mockGetRSIStatus.mockResolvedValue({
        current_phase: 'crystallize',
        cycle_number: 42,
      })

      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('Cycles')).toBeInTheDocument()
        expect(screen.getByText('42')).toBeInTheDocument()
      })
    })

    it('should display total_cycles when cycle_number is missing', async () => {
      mockGetRSIStatus.mockResolvedValue({
        current_phase: 'measure',
        total_cycles: 100,
      })

      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('100')).toBeInTheDocument()
      })
    })

    it('should display heuristics count', async () => {
      mockGetRSIStatus.mockResolvedValue({
        current_phase: 'reflect',
        desires_selected: 15,
      })

      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('Heuristics')).toBeInTheDocument()
      })
    })

    it('should display beliefs count', async () => {
      mockGetRSIStatus.mockResolvedValue({
        current_phase: 'verify',
        desires_verified: 8,
      })

      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('Beliefs')).toBeInTheDocument()
      })
    })

    it('should display capabilities count', async () => {
      mockGetRSIStatus.mockResolvedValue({
        current_phase: 'practice',
        desires_generated: 25,
      })

      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('Capabilities')).toBeInTheDocument()
      })
    })
  })

  describe('null/undefined handling', () => {
    it('should handle null response gracefully', async () => {
      mockGetRSIStatus.mockResolvedValue(null)

      render(<SystemStatus />)

      await waitFor(() => {
        // Should not crash
        expect(screen.getByText('System Status')).toBeInTheDocument()
      })
    })

    it('should handle empty response gracefully', async () => {
      mockGetRSIStatus.mockResolvedValue({})

      render(<SystemStatus />)

      await waitFor(() => {
        expect(screen.getByText('idle')).toBeInTheDocument()
        expect(screen.getByText('Idle')).toBeInTheDocument()
      })
    })
  })
})
