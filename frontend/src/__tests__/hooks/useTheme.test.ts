import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useTheme } from '../../hooks/useTheme'
import { useUIStore } from '../../stores/uiStore'
import { localStorageMock } from '../setup'

// Mock the uiStore
vi.mock('../../stores/uiStore', () => ({
  useUIStore: vi.fn(),
}))

const THEME_STORAGE_KEY = 'byrd-theme-preference'

// Create a persistent matchMedia mock
const createMatchMediaMock = (matches: boolean) => {
  return vi.fn().mockImplementation((query: string) => ({
    matches: query === '(prefers-color-scheme: dark)' ? matches : false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  }))
}

describe('useTheme', () => {
  let mockTheme: 'light' | 'dark' | 'system'
  let mockSetTheme: ReturnType<typeof vi.fn>
  let documentClassList: DOMTokenList

  beforeEach(() => {
    vi.clearAllMocks()

    mockTheme = 'system'
    mockSetTheme = vi.fn((newTheme) => {
      mockTheme = newTheme
    })

    // Setup useUIStore mock
    vi.mocked(useUIStore).mockImplementation(() => ({
      theme: mockTheme,
      setTheme: mockSetTheme,
    }))

    localStorageMock.getItem.mockReturnValue(null)
    localStorageMock.setItem.mockImplementation(() => {})

    // Setup document.documentElement.classList mock
    documentClassList = document.documentElement.classList
    documentClassList.remove('light', 'dark')

    // Ensure matchMedia is mocked (defaults to dark preference)
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: createMatchMediaMock(true),
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
    documentClassList.remove('light', 'dark')
  })

  describe('initialization', () => {
    it('should return theme from store', () => {
      mockTheme = 'dark'
      vi.mocked(useUIStore).mockImplementation(() => ({
        theme: mockTheme,
        setTheme: mockSetTheme,
      }))

      const { result } = renderHook(() => useTheme())

      expect(result.current.theme).toBe('dark')
    })

    it('should load theme from localStorage on mount', () => {
      localStorageMock.getItem.mockReturnValue('dark')

      renderHook(() => useTheme())

      expect(localStorageMock.getItem).toHaveBeenCalledWith(THEME_STORAGE_KEY)
      expect(mockSetTheme).toHaveBeenCalledWith('dark')
    })

    it('should not set theme if localStorage returns invalid value', () => {
      localStorageMock.getItem.mockReturnValue('invalid-theme')

      renderHook(() => useTheme())

      expect(mockSetTheme).not.toHaveBeenCalled()
    })

    it('should accept light theme from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('light')

      renderHook(() => useTheme())

      expect(mockSetTheme).toHaveBeenCalledWith('light')
    })

    it('should accept system theme from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('system')

      renderHook(() => useTheme())

      expect(mockSetTheme).toHaveBeenCalledWith('system')
    })

    it('should handle localStorage errors gracefully', () => {
      localStorageMock.getItem.mockImplementation(() => {
        throw new Error('Storage error')
      })

      // Should not throw
      expect(() => renderHook(() => useTheme())).not.toThrow()
    })
  })

  describe('theme application', () => {
    it('should add dark class when theme is dark', () => {
      mockTheme = 'dark'
      vi.mocked(useUIStore).mockImplementation(() => ({
        theme: mockTheme,
        setTheme: mockSetTheme,
      }))

      renderHook(() => useTheme())

      expect(documentClassList.contains('dark')).toBe(true)
      expect(documentClassList.contains('light')).toBe(false)
    })

    it('should add light class when theme is light', () => {
      mockTheme = 'light'
      vi.mocked(useUIStore).mockImplementation(() => ({
        theme: mockTheme,
        setTheme: mockSetTheme,
      }))

      renderHook(() => useTheme())

      expect(documentClassList.contains('light')).toBe(true)
      expect(documentClassList.contains('dark')).toBe(false)
    })

    it('should use system preference when theme is system', () => {
      mockTheme = 'system'
      vi.mocked(useUIStore).mockImplementation(() => ({
        theme: mockTheme,
        setTheme: mockSetTheme,
      }))

      // matchMedia is mocked to return dark preference
      renderHook(() => useTheme())

      expect(documentClassList.contains('dark')).toBe(true)
    })

    it('should remove old theme class when theme changes', () => {
      documentClassList.add('light')

      mockTheme = 'dark'
      vi.mocked(useUIStore).mockImplementation(() => ({
        theme: mockTheme,
        setTheme: mockSetTheme,
      }))

      renderHook(() => useTheme())

      expect(documentClassList.contains('light')).toBe(false)
      expect(documentClassList.contains('dark')).toBe(true)
    })
  })

  describe('toggleTheme', () => {
    it('should toggle from dark to light', () => {
      documentClassList.add('dark')

      const { result } = renderHook(() => useTheme())

      act(() => {
        result.current.toggleTheme()
      })

      expect(mockSetTheme).toHaveBeenCalledWith('light')
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        THEME_STORAGE_KEY,
        'light'
      )
    })

    it('should toggle from light to dark', () => {
      // Set theme to 'light' so the effect applies light class
      mockTheme = 'light'
      vi.mocked(useUIStore).mockImplementation(() => ({
        theme: mockTheme,
        setTheme: mockSetTheme,
      }))

      // Override matchMedia to prefer light (not dark)
      Object.defineProperty(window, 'matchMedia', {
        writable: true,
        value: createMatchMediaMock(false), // false = light preference
      })

      const { result } = renderHook(() => useTheme())

      // After effect runs, classList should have 'light'
      expect(documentClassList.contains('light')).toBe(true)

      act(() => {
        result.current.toggleTheme()
      })

      // toggleTheme checks classList.contains('dark') - if dark is not there, it sets dark
      expect(mockSetTheme).toHaveBeenCalledWith('dark')
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        THEME_STORAGE_KEY,
        'dark'
      )
    })

    it('should update document classes immediately', () => {
      documentClassList.add('dark')

      const { result } = renderHook(() => useTheme())

      act(() => {
        result.current.toggleTheme()
      })

      expect(documentClassList.contains('light')).toBe(true)
      expect(documentClassList.contains('dark')).toBe(false)
    })
  })

  describe('setTheme (with persistence)', () => {
    it('should set theme and persist to localStorage', () => {
      const { result } = renderHook(() => useTheme())

      act(() => {
        result.current.setTheme('dark')
      })

      expect(mockSetTheme).toHaveBeenCalledWith('dark')
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        THEME_STORAGE_KEY,
        'dark'
      )
    })

    it('should set light theme with persistence', () => {
      const { result } = renderHook(() => useTheme())

      act(() => {
        result.current.setTheme('light')
      })

      expect(mockSetTheme).toHaveBeenCalledWith('light')
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        THEME_STORAGE_KEY,
        'light'
      )
    })

    it('should set system theme with persistence', () => {
      const { result } = renderHook(() => useTheme())

      act(() => {
        result.current.setTheme('system')
      })

      expect(mockSetTheme).toHaveBeenCalledWith('system')
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        THEME_STORAGE_KEY,
        'system'
      )
    })

    it('should handle localStorage errors on setTheme', () => {
      localStorageMock.setItem.mockImplementation(() => {
        throw new Error('Storage error')
      })

      const { result } = renderHook(() => useTheme())

      // Should not throw
      expect(() => {
        act(() => {
          result.current.setTheme('dark')
        })
      }).not.toThrow()

      // Store should still be updated
      expect(mockSetTheme).toHaveBeenCalledWith('dark')
    })
  })

  describe('system preference detection', () => {
    it('should detect dark preference from matchMedia', () => {
      // Our mock returns dark preference
      mockTheme = 'system'
      vi.mocked(useUIStore).mockImplementation(() => ({
        theme: mockTheme,
        setTheme: mockSetTheme,
      }))

      renderHook(() => useTheme())

      expect(documentClassList.contains('dark')).toBe(true)
    })

    it('should apply light when system preference is light', () => {
      // Override matchMedia mock for this test
      Object.defineProperty(window, 'matchMedia', {
        writable: true,
        value: vi.fn().mockImplementation((query: string) => ({
          matches: false, // light preference
          media: query,
          onchange: null,
          addListener: vi.fn(),
          removeListener: vi.fn(),
          addEventListener: vi.fn(),
          removeEventListener: vi.fn(),
          dispatchEvent: vi.fn(),
        })),
      })

      mockTheme = 'system'
      vi.mocked(useUIStore).mockImplementation(() => ({
        theme: mockTheme,
        setTheme: mockSetTheme,
      }))

      renderHook(() => useTheme())

      expect(documentClassList.contains('light')).toBe(true)
      expect(documentClassList.contains('dark')).toBe(false)
    })
  })

  describe('returned values', () => {
    it('should return theme, toggleTheme, and setTheme', () => {
      const { result } = renderHook(() => useTheme())

      expect(result.current).toHaveProperty('theme')
      expect(result.current).toHaveProperty('toggleTheme')
      expect(result.current).toHaveProperty('setTheme')
      expect(typeof result.current.toggleTheme).toBe('function')
      expect(typeof result.current.setTheme).toBe('function')
    })
  })
})
