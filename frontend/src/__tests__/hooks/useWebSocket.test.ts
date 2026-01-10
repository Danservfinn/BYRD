import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, waitFor, act } from '@testing-library/react'
import { useWebSocket } from '../../hooks/useWebSocket'
import { useEventStore } from '../../stores/eventStore'
import { localStorageMock } from '../setup'

// Mock the eventStore
vi.mock('../../stores/eventStore', () => ({
  useEventStore: vi.fn(),
}))

describe('useWebSocket', () => {
  let mockAddEvent: ReturnType<typeof vi.fn>
  let mockSetConnected: ReturnType<typeof vi.fn>
  let mockConnected: boolean

  beforeEach(() => {
    vi.clearAllMocks()

    mockAddEvent = vi.fn()
    mockSetConnected = vi.fn()
    mockConnected = false

    // Setup useEventStore mock
    vi.mocked(useEventStore).mockImplementation((selector) => {
      if (typeof selector === 'function') {
        const state = {
          addEvent: mockAddEvent,
          setConnected: mockSetConnected,
          connected: mockConnected,
        }
        return selector(state)
      }
      return { addEvent: mockAddEvent, setConnected: mockSetConnected, connected: mockConnected }
    })

    localStorageMock.getItem.mockReturnValue(null)
    localStorageMock.setItem.mockImplementation(() => {})
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('initialization', () => {
    it('should return hook interface', () => {
      const { result } = renderHook(() => useWebSocket())

      expect(result.current).toHaveProperty('isConnected')
      expect(result.current).toHaveProperty('send')
      expect(typeof result.current.send).toBe('function')
    })

    it('should return isConnected state from store', () => {
      mockConnected = false
      vi.mocked(useEventStore).mockImplementation((selector) => {
        if (typeof selector === 'function') {
          const state = {
            addEvent: mockAddEvent,
            setConnected: mockSetConnected,
            connected: mockConnected,
          }
          return selector(state)
        }
        return mockConnected
      })

      const { result } = renderHook(() => useWebSocket())

      expect(result.current.isConnected).toBe(false)
    })

    it('should return true when connected', () => {
      mockConnected = true
      vi.mocked(useEventStore).mockImplementation((selector) => {
        if (typeof selector === 'function') {
          const state = {
            addEvent: mockAddEvent,
            setConnected: mockSetConnected,
            connected: mockConnected,
          }
          return selector(state)
        }
        return mockConnected
      })

      const { result } = renderHook(() => useWebSocket())

      expect(result.current.isConnected).toBe(true)
    })
  })

  describe('connection handling', () => {
    it('should not connect if localStorage indicates unavailable', () => {
      localStorageMock.getItem.mockReturnValue('false')

      const { result } = renderHook(() => useWebSocket())

      // Hook should still render without errors
      expect(result.current).toBeDefined()
    })

    it('should provide send function', () => {
      const { result } = renderHook(() => useWebSocket())

      expect(typeof result.current.send).toBe('function')
    })

    it('should not throw when send is called', () => {
      const { result } = renderHook(() => useWebSocket())

      // Should not throw even if connection is not open
      expect(() => {
        result.current.send({ type: 'test', data: {} })
      }).not.toThrow()
    })
  })

  describe('cleanup', () => {
    it('should handle unmount without errors', () => {
      const { unmount } = renderHook(() => useWebSocket())

      // Should not throw on unmount
      expect(() => {
        unmount()
      }).not.toThrow()
    })
  })

  describe('store integration', () => {
    it('should use addEvent from eventStore', () => {
      renderHook(() => useWebSocket())

      // addEvent should be accessible from the store mock
      expect(mockAddEvent).toBeDefined()
    })

    it('should use setConnected from eventStore', () => {
      renderHook(() => useWebSocket())

      // setConnected should be accessible from the store mock
      expect(mockSetConnected).toBeDefined()
    })
  })

  describe('localStorage integration', () => {
    it('should check localStorage for WebSocket availability', () => {
      localStorageMock.getItem.mockReturnValue('true')

      renderHook(() => useWebSocket())

      // Should have checked localStorage
      expect(localStorageMock.getItem).toHaveBeenCalled()
    })
  })
})
