import { describe, it, expect, beforeEach } from 'vitest'
import { act } from '@testing-library/react'
import { useUIStore } from '../../stores/uiStore'

describe('uiStore', () => {
  beforeEach(() => {
    // Reset to default state
    act(() => {
      useUIStore.setState({
        currentTab: 'home',
        theme: 'system',
        breakpoint: 'mobile',
        isLoading: false,
        isByrdChatOpen: false,
      })
    })
  })

  describe('initial state', () => {
    it('should have home as default tab', () => {
      expect(useUIStore.getState().currentTab).toBe('home')
    })

    it('should have system as default theme', () => {
      expect(useUIStore.getState().theme).toBe('system')
    })

    it('should have mobile as default breakpoint', () => {
      expect(useUIStore.getState().breakpoint).toBe('mobile')
    })

    it('should have isLoading as false', () => {
      expect(useUIStore.getState().isLoading).toBe(false)
    })

    it('should have isByrdChatOpen as false', () => {
      expect(useUIStore.getState().isByrdChatOpen).toBe(false)
    })
  })

  describe('setCurrentTab', () => {
    it('should set current tab to home', () => {
      act(() => {
        useUIStore.getState().setCurrentTab('home')
      })
      expect(useUIStore.getState().currentTab).toBe('home')
    })

    it('should set current tab to byrd', () => {
      act(() => {
        useUIStore.getState().setCurrentTab('byrd')
      })
      expect(useUIStore.getState().currentTab).toBe('byrd')
    })

    it('should set current tab to rsi', () => {
      act(() => {
        useUIStore.getState().setCurrentTab('rsi')
      })
      expect(useUIStore.getState().currentTab).toBe('rsi')
    })

    it('should set current tab to memory', () => {
      act(() => {
        useUIStore.getState().setCurrentTab('memory')
      })
      expect(useUIStore.getState().currentTab).toBe('memory')
    })

    it('should set current tab to economic', () => {
      act(() => {
        useUIStore.getState().setCurrentTab('economic')
      })
      expect(useUIStore.getState().currentTab).toBe('economic')
    })

    it('should set current tab to more', () => {
      act(() => {
        useUIStore.getState().setCurrentTab('more')
      })
      expect(useUIStore.getState().currentTab).toBe('more')
    })
  })

  describe('setTheme', () => {
    it('should set theme to light', () => {
      act(() => {
        useUIStore.getState().setTheme('light')
      })
      expect(useUIStore.getState().theme).toBe('light')
    })

    it('should set theme to dark', () => {
      act(() => {
        useUIStore.getState().setTheme('dark')
      })
      expect(useUIStore.getState().theme).toBe('dark')
    })

    it('should set theme to system', () => {
      act(() => {
        useUIStore.getState().setTheme('dark')
        useUIStore.getState().setTheme('system')
      })
      expect(useUIStore.getState().theme).toBe('system')
    })
  })

  describe('setBreakpoint', () => {
    it('should set breakpoint to mobile', () => {
      act(() => {
        useUIStore.getState().setBreakpoint('mobile')
      })
      expect(useUIStore.getState().breakpoint).toBe('mobile')
    })

    it('should set breakpoint to tablet', () => {
      act(() => {
        useUIStore.getState().setBreakpoint('tablet')
      })
      expect(useUIStore.getState().breakpoint).toBe('tablet')
    })

    it('should set breakpoint to desktop', () => {
      act(() => {
        useUIStore.getState().setBreakpoint('desktop')
      })
      expect(useUIStore.getState().breakpoint).toBe('desktop')
    })
  })

  describe('setIsLoading', () => {
    it('should set loading to true', () => {
      act(() => {
        useUIStore.getState().setIsLoading(true)
      })
      expect(useUIStore.getState().isLoading).toBe(true)
    })

    it('should set loading to false', () => {
      act(() => {
        useUIStore.getState().setIsLoading(true)
        useUIStore.getState().setIsLoading(false)
      })
      expect(useUIStore.getState().isLoading).toBe(false)
    })
  })

  describe('setIsByrdChatOpen', () => {
    it('should open BYRD chat', () => {
      act(() => {
        useUIStore.getState().setIsByrdChatOpen(true)
      })
      expect(useUIStore.getState().isByrdChatOpen).toBe(true)
    })

    it('should close BYRD chat', () => {
      act(() => {
        useUIStore.getState().setIsByrdChatOpen(true)
        useUIStore.getState().setIsByrdChatOpen(false)
      })
      expect(useUIStore.getState().isByrdChatOpen).toBe(false)
    })
  })

  describe('state persistence', () => {
    it('should maintain state across multiple actions', () => {
      act(() => {
        useUIStore.getState().setCurrentTab('rsi')
        useUIStore.getState().setTheme('dark')
        useUIStore.getState().setBreakpoint('desktop')
        useUIStore.getState().setIsLoading(true)
        useUIStore.getState().setIsByrdChatOpen(true)
      })

      const state = useUIStore.getState()
      expect(state.currentTab).toBe('rsi')
      expect(state.theme).toBe('dark')
      expect(state.breakpoint).toBe('desktop')
      expect(state.isLoading).toBe(true)
      expect(state.isByrdChatOpen).toBe(true)
    })

    it('should allow partial state updates without affecting other state', () => {
      act(() => {
        useUIStore.getState().setCurrentTab('memory')
      })

      // Other state should remain unchanged
      expect(useUIStore.getState().theme).toBe('system')
      expect(useUIStore.getState().breakpoint).toBe('mobile')
      expect(useUIStore.getState().isLoading).toBe(false)
    })
  })
})
