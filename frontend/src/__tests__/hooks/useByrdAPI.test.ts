import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, waitFor, act } from '@testing-library/react'
import { useByrdAPI } from '../../hooks/useByrdAPI'
import { localStorageMock } from '../setup'

const API_BASE = 'https://byrd-api-production.up.railway.app/api'

describe('useByrdAPI', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorageMock.getItem.mockReturnValue(null)
    localStorageMock.setItem.mockImplementation(() => {})
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('initialization', () => {
    it('should initialize with loading false and no error', async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
      } as Response)

      const { result } = renderHook(() => useByrdAPI())

      expect(result.current.loading).toBe(false)
      expect(result.current.error).toBeNull()
    })

    it('should check backend availability on mount', async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
      } as Response)

      renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          `${API_BASE}/status`,
          expect.objectContaining({ method: 'HEAD' })
        )
      })
    })

    it('should use cached backend availability from localStorage', async () => {
      localStorageMock.getItem.mockReturnValue('true')

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })
    })

    it('should set backendAvailable to false when HEAD request fails', async () => {
      vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'))

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(false)
      })

      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'byrd_backend_available',
        'false'
      )
    })

    it('should set backendAvailable to true when HEAD request succeeds', async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
      } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'byrd_backend_available',
        'true'
      )
    })
  })

  describe('getStatus', () => {
    it('should fetch system status successfully', async () => {
      const mockStatus = {
        running: true,
        dream_count: 5,
        seek_count: 10,
        capabilities: ['reasoning', 'coding'],
        desires: [],
        beliefs: [],
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockStatus),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let status: typeof mockStatus | null = null
      await act(async () => {
        status = await result.current.getStatus()
      })

      expect(status).toEqual(mockStatus)
    })

    it('should return null when backend is unavailable', async () => {
      vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'))

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(false)
      })

      let status: unknown = 'not-null'
      await act(async () => {
        status = await result.current.getStatus()
      })

      expect(status).toBeNull()
    })

    it('should handle HTTP errors gracefully', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: false,
          status: 500,
          statusText: 'Internal Server Error',
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let status: unknown = 'not-null'
      await act(async () => {
        status = await result.current.getStatus()
      })

      expect(status).toBeNull()
      expect(result.current.error).toBe('HTTP 500: Internal Server Error')
    })
  })

  describe('startByrd', () => {
    it('should send POST request to start endpoint', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ success: true }),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let success = false
      await act(async () => {
        success = await result.current.startByrd()
      })

      expect(success).toBe(true)
      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/start`,
        expect.objectContaining({ method: 'POST' })
      )
    })
  })

  describe('stopByrd', () => {
    it('should send POST request to stop endpoint', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ success: true }),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let success = false
      await act(async () => {
        success = await result.current.stopByrd()
      })

      expect(success).toBe(true)
      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/stop`,
        expect.objectContaining({ method: 'POST' })
      )
    })
  })

  describe('resetByrd', () => {
    it('should send POST request with hard_reset parameter', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ success: true }),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      await act(async () => {
        await result.current.resetByrd(true)
      })

      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/reset`,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ hard_reset: true }),
        })
      )
    })

    it('should default hard_reset to false', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ success: true }),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      await act(async () => {
        await result.current.resetByrd()
      })

      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/reset`,
        expect.objectContaining({
          body: JSON.stringify({ hard_reset: false }),
        })
      )
    })
  })

  describe('getRSIStatus', () => {
    it('should fetch RSI status successfully', async () => {
      const mockRSIStatus = {
        phase: 'REFLECT',
        cycle_count: 42,
        improvement_delta: 0.05,
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockRSIStatus),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let status: typeof mockRSIStatus | null = null
      await act(async () => {
        status = await result.current.getRSIStatus()
      })

      expect(status).toEqual(mockRSIStatus)
      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/rsi/status`,
        expect.objectContaining({
          headers: { 'Content-Type': 'application/json' },
        })
      )
    })
  })

  describe('getRSIMetrics', () => {
    it('should fetch RSI metrics successfully', async () => {
      const mockMetrics = {
        cycles_completed: 100,
        average_improvement: 0.02,
        verification_success_rate: 0.95,
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockMetrics),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let metrics: typeof mockMetrics | null = null
      await act(async () => {
        metrics = await result.current.getRSIMetrics()
      })

      expect(metrics).toEqual(mockMetrics)
    })
  })

  describe('Economic endpoints', () => {
    it('should fetch treasury status', async () => {
      const mockTreasury = {
        balance: 1000,
        currency: 'USD',
        last_deposit: '2026-01-01T00:00:00Z',
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockTreasury),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let treasury: typeof mockTreasury | null = null
      await act(async () => {
        treasury = await result.current.getTreasuryStatus()
      })

      expect(treasury).toEqual(mockTreasury)
    })

    it('should fetch revenue report', async () => {
      const mockRevenue = {
        total: 5000,
        by_source: { api: 3000, marketplace: 2000 },
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockRevenue),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let revenue: typeof mockRevenue | null = null
      await act(async () => {
        revenue = await result.current.getRevenueReport()
      })

      expect(revenue).toEqual(mockRevenue)
    })

    it('should fetch marketplace listings', async () => {
      const mockListings = {
        items: [
          { id: '1', name: 'Module A', price: 100 },
          { id: '2', name: 'Module B', price: 200 },
        ],
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockListings),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let listings: typeof mockListings | null = null
      await act(async () => {
        listings = await result.current.getMarketplaceListings()
      })

      expect(listings).toEqual(mockListings)
    })
  })

  describe('Verification endpoints', () => {
    it('should fetch human anchoring queue', async () => {
      const mockQueue = {
        items: [{ id: '1', request: 'Approve modification', urgency: 'high' }],
        total: 1,
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockQueue),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let queue: typeof mockQueue | null = null
      await act(async () => {
        queue = await result.current.getHumanAnchoringQueue()
      })

      expect(queue).toEqual(mockQueue)
    })

    it('should process human validation', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ success: true }),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      await act(async () => {
        await result.current.processHumanValidation('req_123', {
          approved: true,
          notes: 'Looks good',
        })
      })

      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/verification/human-anchoring/req_123`,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ approved: true, notes: 'Looks good' }),
        })
      )
    })

    it('should submit anchoring response', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ success: true }),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      await act(async () => {
        await result.current.submitAnchoringResponse('req_456', false)
      })

      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/verification/human-anchoring/req_456`,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ approved: false }),
        })
      )
    })

    it('should fetch verification status', async () => {
      const mockStatus = {
        lattice_health: 'healthy',
        verifiers_active: 5,
        pending_validations: 3,
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockStatus),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let status: typeof mockStatus | null = null
      await act(async () => {
        status = await result.current.getVerificationStatus()
      })

      expect(status).toEqual(mockStatus)
    })
  })

  describe('Plasticity endpoints', () => {
    it('should fetch plasticity modules', async () => {
      const mockModules = {
        modules: [
          { id: 'm1', name: 'Reasoning', active: true },
          { id: 'm2', name: 'Planning', active: false },
        ],
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockModules),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let modules: typeof mockModules | null = null
      await act(async () => {
        modules = await result.current.getPlasticityModules()
      })

      expect(modules).toEqual(mockModules)
    })

    it('should fetch NAS candidates', async () => {
      const mockCandidates = {
        candidates: [
          { id: 'c1', architecture: 'transformer', score: 0.95 },
        ],
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockCandidates),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let candidates: typeof mockCandidates | null = null
      await act(async () => {
        candidates = await result.current.getNASCandidates()
      })

      expect(candidates).toEqual(mockCandidates)
    })
  })

  describe('Governance endpoints', () => {
    it('should fetch direction', async () => {
      const mockDirection = {
        content: 'Focus on capability improvements',
        updated_at: '2026-01-01T00:00:00Z',
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockDirection),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let direction: typeof mockDirection | null = null
      await act(async () => {
        direction = await result.current.getDirection()
      })

      expect(direction).toEqual(mockDirection)
    })

    it('should update direction', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ success: true }),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      await act(async () => {
        await result.current.updateDirection('New direction content')
      })

      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/governance/direction`,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ content: 'New direction content' }),
        })
      )
    })

    it('should send governance command', async () => {
      const mockResponse = {
        result: 'Command executed',
        timestamp: '2026-01-01T00:00:00Z',
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockResponse),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let response: typeof mockResponse | null = null
      await act(async () => {
        response = await result.current.sendGovernanceCommand('status')
      })

      expect(response).toEqual(mockResponse)
      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/governance/command`,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ command: 'status' }),
        })
      )
    })

    it('should inject desire', async () => {
      const mockResponse = {
        desire_id: 'd_123',
        created: true,
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockResponse),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let response: typeof mockResponse | null = null
      await act(async () => {
        response = await result.current.injectDesire(
          'Improve reasoning capability',
          0.8
        )
      })

      expect(response).toEqual(mockResponse)
      expect(fetch).toHaveBeenCalledWith(
        `${API_BASE}/governance/inject-desire`,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            description: 'Improve reasoning capability',
            urgency: 0.8,
          }),
        })
      )
    })
  })

  describe('Memory endpoints', () => {
    it('should fetch memory graph', async () => {
      const mockGraph = {
        nodes: [
          { id: 'n1', type: 'belief', content: 'Test belief' },
        ],
        edges: [
          { source: 'n1', target: 'n2', type: 'derived_from' },
        ],
      }

      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve(mockGraph),
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      let graph: typeof mockGraph | null = null
      await act(async () => {
        graph = await result.current.getMemoryGraph()
      })

      expect(graph).toEqual(mockGraph)
    })
  })

  describe('Error handling', () => {
    it('should mark backend as unavailable on 404', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockResolvedValueOnce({
          ok: false,
          status: 404,
          statusText: 'Not Found',
        } as Response)

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      await act(async () => {
        await result.current.getStatus()
      })

      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'byrd_backend_available',
        'false'
      )
    })

    it('should mark backend as unavailable on fetch failure', async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce({ ok: true } as Response) // HEAD request
        .mockRejectedValueOnce(new Error('Failed to fetch'))

      const { result } = renderHook(() => useByrdAPI())

      await waitFor(() => {
        expect(result.current.backendAvailable).toBe(true)
      })

      await act(async () => {
        await result.current.getStatus()
      })

      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'byrd_backend_available',
        'false'
      )
    })
  })
})
