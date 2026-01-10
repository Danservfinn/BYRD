import { describe, it, expect, beforeEach } from 'vitest'
import { act } from '@testing-library/react'
import { useByrdStore, type ByrdState } from '../../stores/byrdStore'
import type { ChatMessage } from '../../types/api'

describe('byrdStore', () => {
  beforeEach(() => {
    // Reset to default state
    act(() => {
      useByrdStore.setState({
        byrdState: null,
        messages: [],
        animationState: 'idle',
        isTyping: false,
      })
    })
  })

  describe('initial state', () => {
    it('should have null byrdState', () => {
      expect(useByrdStore.getState().byrdState).toBeNull()
    })

    it('should have empty messages array', () => {
      expect(useByrdStore.getState().messages).toEqual([])
    })

    it('should have idle animation state', () => {
      expect(useByrdStore.getState().animationState).toBe('idle')
    })

    it('should have isTyping as false', () => {
      expect(useByrdStore.getState().isTyping).toBe(false)
    })
  })

  describe('setByrdState', () => {
    it('should set BYRD state', () => {
      const newState: ByrdState = {
        cycle_id: 'cycle_123',
        phase: 'REFLECT',
        emergence_score: 0.85,
        treasury_balance: 10000,
      }

      act(() => {
        useByrdStore.getState().setByrdState(newState)
      })

      expect(useByrdStore.getState().byrdState).toEqual(newState)
    })

    it('should update existing BYRD state', () => {
      act(() => {
        useByrdStore.getState().setByrdState({
          cycle_id: 'cycle_1',
          phase: 'REFLECT',
          emergence_score: 0.5,
          treasury_balance: 1000,
        })
      })

      act(() => {
        useByrdStore.getState().setByrdState({
          cycle_id: 'cycle_2',
          phase: 'VERIFY',
          emergence_score: 0.75,
          treasury_balance: 2000,
        })
      })

      expect(useByrdStore.getState().byrdState?.cycle_id).toBe('cycle_2')
      expect(useByrdStore.getState().byrdState?.phase).toBe('VERIFY')
    })

    it('should allow null values in state fields', () => {
      const partialState: ByrdState = {
        cycle_id: null,
        phase: null,
        emergence_score: null,
        treasury_balance: null,
      }

      act(() => {
        useByrdStore.getState().setByrdState(partialState)
      })

      expect(useByrdStore.getState().byrdState?.cycle_id).toBeNull()
      expect(useByrdStore.getState().byrdState?.emergence_score).toBeNull()
    })
  })

  describe('setAnimationState', () => {
    it('should set animation to idle', () => {
      act(() => {
        useByrdStore.getState().setAnimationState('idle')
      })
      expect(useByrdStore.getState().animationState).toBe('idle')
    })

    it('should set animation to thinking', () => {
      act(() => {
        useByrdStore.getState().setAnimationState('thinking')
      })
      expect(useByrdStore.getState().animationState).toBe('thinking')
    })

    it('should set animation to speaking', () => {
      act(() => {
        useByrdStore.getState().setAnimationState('speaking')
      })
      expect(useByrdStore.getState().animationState).toBe('speaking')
    })

    it('should set animation to celebrating', () => {
      act(() => {
        useByrdStore.getState().setAnimationState('celebrating')
      })
      expect(useByrdStore.getState().animationState).toBe('celebrating')
    })

    it('should set animation to concerned', () => {
      act(() => {
        useByrdStore.getState().setAnimationState('concerned')
      })
      expect(useByrdStore.getState().animationState).toBe('concerned')
    })

    it('should transition between animation states', () => {
      act(() => {
        useByrdStore.getState().setAnimationState('thinking')
      })
      expect(useByrdStore.getState().animationState).toBe('thinking')

      act(() => {
        useByrdStore.getState().setAnimationState('speaking')
      })
      expect(useByrdStore.getState().animationState).toBe('speaking')

      act(() => {
        useByrdStore.getState().setAnimationState('idle')
      })
      expect(useByrdStore.getState().animationState).toBe('idle')
    })
  })

  describe('addMessage', () => {
    it('should add message to empty messages array', () => {
      const message: ChatMessage = {
        id: 'msg_1',
        role: 'user',
        content: 'Hello BYRD!',
        timestamp: '2026-01-01T00:00:00Z',
      }

      act(() => {
        useByrdStore.getState().addMessage(message)
      })

      expect(useByrdStore.getState().messages).toHaveLength(1)
      expect(useByrdStore.getState().messages[0]).toEqual(message)
    })

    it('should append messages to existing array', () => {
      const message1: ChatMessage = {
        id: 'msg_1',
        role: 'user',
        content: 'Hello',
        timestamp: '2026-01-01T00:00:00Z',
      }
      const message2: ChatMessage = {
        id: 'msg_2',
        role: 'assistant',
        content: 'Hi there!',
        timestamp: '2026-01-01T00:00:01Z',
      }

      act(() => {
        useByrdStore.getState().addMessage(message1)
        useByrdStore.getState().addMessage(message2)
      })

      expect(useByrdStore.getState().messages).toHaveLength(2)
      expect(useByrdStore.getState().messages[0].id).toBe('msg_1')
      expect(useByrdStore.getState().messages[1].id).toBe('msg_2')
    })

    it('should preserve message order', () => {
      const messages: ChatMessage[] = [
        { id: 'msg_1', role: 'user', content: 'First', timestamp: '' },
        { id: 'msg_2', role: 'assistant', content: 'Second', timestamp: '' },
        { id: 'msg_3', role: 'user', content: 'Third', timestamp: '' },
      ]

      act(() => {
        messages.forEach((m) => useByrdStore.getState().addMessage(m))
      })

      expect(useByrdStore.getState().messages.map((m) => m.id)).toEqual([
        'msg_1',
        'msg_2',
        'msg_3',
      ])
    })

    it('should handle messages with different roles', () => {
      act(() => {
        useByrdStore.getState().addMessage({
          id: 'msg_1',
          role: 'user',
          content: 'User message',
          timestamp: '',
        })
        useByrdStore.getState().addMessage({
          id: 'msg_2',
          role: 'assistant',
          content: 'Assistant message',
          timestamp: '',
        })
        useByrdStore.getState().addMessage({
          id: 'msg_3',
          role: 'system',
          content: 'System message',
          timestamp: '',
        })
      })

      const messages = useByrdStore.getState().messages
      expect(messages[0].role).toBe('user')
      expect(messages[1].role).toBe('assistant')
      expect(messages[2].role).toBe('system')
    })
  })

  describe('clearMessages', () => {
    it('should clear all messages', () => {
      act(() => {
        useByrdStore.getState().addMessage({
          id: 'msg_1',
          role: 'user',
          content: 'Test',
          timestamp: '',
        })
        useByrdStore.getState().addMessage({
          id: 'msg_2',
          role: 'assistant',
          content: 'Response',
          timestamp: '',
        })
      })

      expect(useByrdStore.getState().messages).toHaveLength(2)

      act(() => {
        useByrdStore.getState().clearMessages()
      })

      expect(useByrdStore.getState().messages).toHaveLength(0)
    })

    it('should handle clearing empty messages array', () => {
      act(() => {
        useByrdStore.getState().clearMessages()
      })

      expect(useByrdStore.getState().messages).toHaveLength(0)
    })

    it('should not affect other state', () => {
      act(() => {
        useByrdStore.getState().setByrdState({
          cycle_id: 'cycle_1',
          phase: 'REFLECT',
          emergence_score: 0.5,
          treasury_balance: 1000,
        })
        useByrdStore.getState().setAnimationState('thinking')
        useByrdStore.getState().addMessage({
          id: 'msg_1',
          role: 'user',
          content: 'Test',
          timestamp: '',
        })
      })

      act(() => {
        useByrdStore.getState().clearMessages()
      })

      expect(useByrdStore.getState().byrdState?.cycle_id).toBe('cycle_1')
      expect(useByrdStore.getState().animationState).toBe('thinking')
    })
  })

  describe('setTyping', () => {
    it('should set typing to true', () => {
      act(() => {
        useByrdStore.getState().setTyping(true)
      })
      expect(useByrdStore.getState().isTyping).toBe(true)
    })

    it('should set typing to false', () => {
      act(() => {
        useByrdStore.getState().setTyping(true)
        useByrdStore.getState().setTyping(false)
      })
      expect(useByrdStore.getState().isTyping).toBe(false)
    })

    it('should toggle typing state', () => {
      act(() => {
        useByrdStore.getState().setTyping(true)
      })
      expect(useByrdStore.getState().isTyping).toBe(true)

      act(() => {
        useByrdStore.getState().setTyping(false)
      })
      expect(useByrdStore.getState().isTyping).toBe(false)

      act(() => {
        useByrdStore.getState().setTyping(true)
      })
      expect(useByrdStore.getState().isTyping).toBe(true)
    })
  })

  describe('state interactions', () => {
    it('should handle typical chat flow', () => {
      // User starts typing
      act(() => {
        useByrdStore.getState().setTyping(true)
      })
      expect(useByrdStore.getState().isTyping).toBe(true)

      // User sends message
      act(() => {
        useByrdStore.getState().setTyping(false)
        useByrdStore.getState().addMessage({
          id: 'msg_1',
          role: 'user',
          content: 'What is your current state?',
          timestamp: new Date().toISOString(),
        })
      })

      expect(useByrdStore.getState().isTyping).toBe(false)
      expect(useByrdStore.getState().messages).toHaveLength(1)

      // BYRD starts thinking
      act(() => {
        useByrdStore.getState().setAnimationState('thinking')
      })
      expect(useByrdStore.getState().animationState).toBe('thinking')

      // BYRD responds
      act(() => {
        useByrdStore.getState().setAnimationState('speaking')
        useByrdStore.getState().addMessage({
          id: 'msg_2',
          role: 'assistant',
          content: 'I am in the REFLECT phase...',
          timestamp: new Date().toISOString(),
        })
      })

      expect(useByrdStore.getState().animationState).toBe('speaking')
      expect(useByrdStore.getState().messages).toHaveLength(2)

      // BYRD goes back to idle
      act(() => {
        useByrdStore.getState().setAnimationState('idle')
      })
      expect(useByrdStore.getState().animationState).toBe('idle')
    })

    it('should maintain all state properties independently', () => {
      act(() => {
        useByrdStore.getState().setByrdState({
          cycle_id: 'cycle_100',
          phase: 'CRYSTALLIZE',
          emergence_score: 0.92,
          treasury_balance: 50000,
        })
        useByrdStore.getState().setAnimationState('celebrating')
        useByrdStore.getState().addMessage({
          id: 'msg_1',
          role: 'assistant',
          content: 'Achievement unlocked!',
          timestamp: '',
        })
        useByrdStore.getState().setTyping(false)
      })

      const state = useByrdStore.getState()
      expect(state.byrdState?.cycle_id).toBe('cycle_100')
      expect(state.byrdState?.emergence_score).toBe(0.92)
      expect(state.animationState).toBe('celebrating')
      expect(state.messages).toHaveLength(1)
      expect(state.isTyping).toBe(false)
    })
  })
})
