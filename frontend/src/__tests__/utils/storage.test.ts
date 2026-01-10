import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { safeGetStorage, safeSetStorage } from '../../utils/storage'

describe('storage utilities', () => {
  let originalLocalStorage: Storage
  let mockGetItem: ReturnType<typeof vi.fn>
  let mockSetItem: ReturnType<typeof vi.fn>

  beforeEach(() => {
    // Store original localStorage
    originalLocalStorage = global.localStorage

    // Create mock functions
    mockGetItem = vi.fn()
    mockSetItem = vi.fn()

    // Mock localStorage
    global.localStorage = {
      getItem: mockGetItem,
      setItem: mockSetItem,
      removeItem: vi.fn(),
      clear: vi.fn(),
      get length() { return 0 },
      key: vi.fn(),
    } as unknown as Storage
  })

  afterEach(() => {
    // Restore original localStorage
    global.localStorage = originalLocalStorage
    vi.restoreAllMocks()
  })

  describe('safeGetStorage', () => {
    it('should return value from localStorage when available', () => {
      mockGetItem.mockReturnValue('dark')

      const result = safeGetStorage('theme')

      expect(result).toBe('dark')
      expect(mockGetItem).toHaveBeenCalledWith('theme')
    })

    it('should return null when key does not exist', () => {
      mockGetItem.mockReturnValue(null)

      const result = safeGetStorage('nonexistent')

      expect(result).toBeNull()
    })

    it('should handle localStorage SecurityError gracefully', () => {
      // Simulate iframe context where localStorage throws SecurityError
      mockGetItem.mockImplementation(() => {
        throw new DOMException('The operation is insecure.', 'SecurityError')
      })

      const result = safeGetStorage('theme')

      expect(result).toBeNull()
    })

    it('should handle generic Error from localStorage', () => {
      mockGetItem.mockImplementation(() => {
        throw new Error('localStorage not available')
      })

      const result = safeGetStorage('theme')

      expect(result).toBeNull()
    })

    it('should handle private browsing mode error', () => {
      // Some browsers throw QuotaExceededError in private browsing
      mockGetItem.mockImplementation(() => {
        const error = new DOMException('QuotaExceededError', 'QuotaExceededError')
        throw error
      })

      const result = safeGetStorage('theme')

      expect(result).toBeNull()
    })

    it('should return null for any exception', () => {
      mockGetItem.mockImplementation(() => {
        throw 'String error'
      })

      const result = safeGetStorage('any-key')

      expect(result).toBeNull()
    })
  })

  describe('safeSetStorage', () => {
    it('should set value in localStorage when available', () => {
      mockSetItem.mockImplementation(() => {})

      safeSetStorage('theme', 'light')

      expect(mockSetItem).toHaveBeenCalledWith('theme', 'light')
    })

    it('should handle localStorage SecurityError silently', () => {
      mockSetItem.mockImplementation(() => {
        throw new DOMException('The operation is insecure.', 'SecurityError')
      })

      // Should not throw
      expect(() => safeSetStorage('theme', 'light')).not.toThrow()
    })

    it('should handle generic Error from localStorage silently', () => {
      mockSetItem.mockImplementation(() => {
        throw new Error('localStorage not available')
      })

      // Should not throw
      expect(() => safeSetStorage('theme', 'dark')).not.toThrow()
    })

    it('should handle QuotaExceededError gracefully', () => {
      mockSetItem.mockImplementation(() => {
        throw new DOMException('Quota exceeded', 'QuotaExceededError')
      })

      // Should not throw
      expect(() => safeSetStorage('large-data', 'x'.repeat(10000000))).not.toThrow()
    })

    it('should handle any exception silently', () => {
      mockSetItem.mockImplementation(() => {
        throw 'String error'
      })

      expect(() => safeSetStorage('key', 'value')).not.toThrow()
    })

    it('should be callable multiple times without side effects on error', () => {
      let callCount = 0
      mockSetItem.mockImplementation(() => {
        callCount++
        throw new Error('Storage error')
      })

      safeSetStorage('key1', 'value1')
      safeSetStorage('key2', 'value2')

      expect(callCount).toBe(2)
    })
  })

  describe('integration scenarios', () => {
    it('should handle typical theme storage cycle', () => {
      // Get current theme (not set)
      mockGetItem.mockReturnValue(null)
      expect(safeGetStorage('theme')).toBeNull()

      // Set theme
      mockSetItem.mockImplementation(() => {})
      safeSetStorage('theme', 'dark')
      expect(mockSetItem).toHaveBeenCalledWith('theme', 'dark')

      // Get theme back
      mockGetItem.mockReturnValue('dark')
      expect(safeGetStorage('theme')).toBe('dark')
    })

    it('should handle setting and getting in restricted context', () => {
      // Simulate restricted context (iframe, private browsing)
      mockGetItem.mockImplementation(() => {
        throw new Error('Access denied')
      })
      mockSetItem.mockImplementation(() => {
        throw new Error('Access denied')
      })

      // Both operations should complete without throwing
      expect(() => {
        const value = safeGetStorage('theme')
        expect(value).toBeNull()

        safeSetStorage('theme', 'dark')
      }).not.toThrow()
    })

    it('should work with JSON stringified values', () => {
      const obj = { theme: 'dark', preference: 'high-contrast' }
      const jsonStr = JSON.stringify(obj)

      mockSetItem.mockImplementation(() => {})
      mockGetItem.mockReturnValue(jsonStr)

      safeSetStorage('settings', jsonStr)
      expect(mockSetItem).toHaveBeenCalledWith('settings', jsonStr)

      const result = safeGetStorage('settings')
      expect(result).toBe(jsonStr)
    })
  })

  describe('edge cases', () => {
    it('should handle empty string key', () => {
      mockGetItem.mockReturnValue('value')
      expect(safeGetStorage('')).toBe('value')

      mockSetItem.mockImplementation(() => {})
      safeSetStorage('', 'value')
      expect(mockSetItem).toHaveBeenCalledWith('', 'value')
    })

    it('should handle empty string value', () => {
      mockSetItem.mockImplementation(() => {})
      safeSetStorage('key', '')
      expect(mockSetItem).toHaveBeenCalledWith('key', '')
    })

    it('should handle undefined value (converted to string)', () => {
      mockSetItem.mockImplementation(() => {})
      safeSetStorage('key', undefined as unknown as string)
      expect(mockSetItem).toHaveBeenCalledWith('key', undefined as unknown as string)
    })

    it('should handle special characters in key and value', () => {
      const specialKey = 'byrd-theme-with-special-chars-@#$'
      const specialValue = 'dark-mode-émojis-🌙'

      mockSetItem.mockImplementation(() => {})
      mockGetItem.mockReturnValue(specialValue)

      safeSetStorage(specialKey, specialValue)
      expect(mockSetItem).toHaveBeenCalledWith(specialKey, specialValue)

      expect(safeGetStorage(specialKey)).toBe(specialValue)
    })

    it('should handle very long keys and values', () => {
      const longKey = 'a'.repeat(1000)
      const longValue = 'b'.repeat(10000)

      mockSetItem.mockImplementation(() => {})

      expect(() => safeSetStorage(longKey, longValue)).not.toThrow()
      expect(mockSetItem).toHaveBeenCalledWith(longKey, longValue)
    })
  })
})
