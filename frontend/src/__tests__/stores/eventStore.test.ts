import { describe, it, expect, beforeEach } from 'vitest'
import { act } from '@testing-library/react'
import { useEventStore } from '../../stores/eventStore'
import type { ByrdEvent } from '../../types/events'

describe('eventStore', () => {
  beforeEach(() => {
    // Reset the store before each test
    act(() => {
      useEventStore.getState().clearEvents()
      useEventStore.getState().setConnected(false)
    })
  })

  describe('initial state', () => {
    it('should have empty events array', () => {
      const state = useEventStore.getState()
      expect(state.events).toEqual([])
    })

    it('should have connected as false', () => {
      const state = useEventStore.getState()
      expect(state.connected).toBe(false)
    })

    it('should have null lastEventTime', () => {
      const state = useEventStore.getState()
      expect(state.lastEventTime).toBeNull()
    })
  })

  describe('addEvent', () => {
    it('should add event to the beginning of events array', () => {
      const event: ByrdEvent = {
        type: 'belief_created',
        data: { content: 'Test belief' },
        timestamp: '2026-01-01T00:00:00Z',
        id: 'evt_1',
      }

      act(() => {
        useEventStore.getState().addEvent(event)
      })

      const state = useEventStore.getState()
      expect(state.events).toHaveLength(1)
      expect(state.events[0]).toEqual(event)
    })

    it('should prepend new events (newest first)', () => {
      const event1: ByrdEvent = {
        type: 'belief_created',
        data: { content: 'First' },
        timestamp: '2026-01-01T00:00:00Z',
        id: 'evt_1',
      }
      const event2: ByrdEvent = {
        type: 'desire_created',
        data: { description: 'Second' },
        timestamp: '2026-01-01T00:01:00Z',
        id: 'evt_2',
      }

      act(() => {
        useEventStore.getState().addEvent(event1)
        useEventStore.getState().addEvent(event2)
      })

      const state = useEventStore.getState()
      expect(state.events).toHaveLength(2)
      expect(state.events[0].id).toBe('evt_2') // Newest first
      expect(state.events[1].id).toBe('evt_1')
    })

    it('should update lastEventTime', () => {
      const timestamp = '2026-01-01T00:00:00Z'
      const event: ByrdEvent = {
        type: 'rsi_cycle_start',
        data: {},
        timestamp,
        id: 'evt_1',
      }

      act(() => {
        useEventStore.getState().addEvent(event)
      })

      expect(useEventStore.getState().lastEventTime).toBe(timestamp)
    })

    it('should limit events to MAX_EVENTS (500)', () => {
      const MAX_EVENTS = 500

      // Add 600 events
      act(() => {
        for (let i = 0; i < 600; i++) {
          useEventStore.getState().addEvent({
            type: 'belief_created',
            data: { index: i },
            timestamp: `2026-01-01T00:00:${String(i % 60).padStart(2, '0')}Z`,
            id: `evt_${i}`,
          })
        }
      })

      const state = useEventStore.getState()
      expect(state.events).toHaveLength(MAX_EVENTS)
      // Most recent events should be kept
      expect(state.events[0].id).toBe('evt_599')
    })
  })

  describe('setConnected', () => {
    it('should set connected to true', () => {
      act(() => {
        useEventStore.getState().setConnected(true)
      })

      expect(useEventStore.getState().connected).toBe(true)
    })

    it('should set connected to false', () => {
      act(() => {
        useEventStore.getState().setConnected(true)
        useEventStore.getState().setConnected(false)
      })

      expect(useEventStore.getState().connected).toBe(false)
    })
  })

  describe('clearEvents', () => {
    it('should clear all events', () => {
      // Add some events first
      act(() => {
        useEventStore.getState().addEvent({
          type: 'belief_created',
          data: {},
          timestamp: '2026-01-01T00:00:00Z',
          id: 'evt_1',
        })
        useEventStore.getState().addEvent({
          type: 'desire_created',
          data: {},
          timestamp: '2026-01-01T00:01:00Z',
          id: 'evt_2',
        })
      })

      expect(useEventStore.getState().events).toHaveLength(2)

      act(() => {
        useEventStore.getState().clearEvents()
      })

      expect(useEventStore.getState().events).toHaveLength(0)
    })

    it('should reset lastEventTime to null', () => {
      act(() => {
        useEventStore.getState().addEvent({
          type: 'belief_created',
          data: {},
          timestamp: '2026-01-01T00:00:00Z',
          id: 'evt_1',
        })
      })

      expect(useEventStore.getState().lastEventTime).not.toBeNull()

      act(() => {
        useEventStore.getState().clearEvents()
      })

      expect(useEventStore.getState().lastEventTime).toBeNull()
    })
  })

  describe('getEventsByType', () => {
    beforeEach(() => {
      act(() => {
        useEventStore.getState().addEvent({
          type: 'belief_created',
          data: { content: 'Belief 1' },
          timestamp: '2026-01-01T00:00:00Z',
          id: 'evt_1',
        })
        useEventStore.getState().addEvent({
          type: 'desire_created',
          data: { description: 'Desire 1' },
          timestamp: '2026-01-01T00:01:00Z',
          id: 'evt_2',
        })
        useEventStore.getState().addEvent({
          type: 'belief_created',
          data: { content: 'Belief 2' },
          timestamp: '2026-01-01T00:02:00Z',
          id: 'evt_3',
        })
        useEventStore.getState().addEvent({
          type: 'rsi_cycle_start',
          data: { phase: 'REFLECT' },
          timestamp: '2026-01-01T00:03:00Z',
          id: 'evt_4',
        })
      })
    })

    it('should return events of specified type', () => {
      const beliefs = useEventStore.getState().getEventsByType('belief_created')

      expect(beliefs).toHaveLength(2)
      expect(beliefs.every((e) => e.type === 'belief_created')).toBe(true)
    })

    it('should return empty array if no events of type exist', () => {
      const events = useEventStore.getState().getEventsByType('quantum_influence')

      expect(events).toHaveLength(0)
    })

    it('should return single event if only one matches', () => {
      const rsiEvents = useEventStore.getState().getEventsByType('rsi_cycle_start')

      expect(rsiEvents).toHaveLength(1)
      expect(rsiEvents[0].id).toBe('evt_4')
    })
  })

  describe('event types', () => {
    it('should handle system events', () => {
      act(() => {
        useEventStore.getState().addEvent({
          type: 'system_started',
          data: { version: '1.0.0' },
          timestamp: '2026-01-01T00:00:00Z',
        })
      })

      expect(useEventStore.getState().events[0].type).toBe('system_started')
    })

    it('should handle RSI events', () => {
      act(() => {
        useEventStore.getState().addEvent({
          type: 'rsi_cycle_complete',
          data: { cycle_id: 42, improvement: 0.02 },
          timestamp: '2026-01-01T00:00:00Z',
        })
      })

      expect(useEventStore.getState().events[0].type).toBe('rsi_cycle_complete')
    })

    it('should handle plasticity events', () => {
      act(() => {
        useEventStore.getState().addEvent({
          type: 'plasticity_composition',
          data: { modules: ['m1', 'm2'] },
          timestamp: '2026-01-01T00:00:00Z',
        })
      })

      expect(useEventStore.getState().events[0].type).toBe('plasticity_composition')
    })

    it('should handle economic events', () => {
      act(() => {
        useEventStore.getState().addEvent({
          type: 'treasury_deposit',
          data: { amount: 1000, currency: 'USD' },
          timestamp: '2026-01-01T00:00:00Z',
        })
      })

      expect(useEventStore.getState().events[0].type).toBe('treasury_deposit')
    })

    it('should handle verification events', () => {
      act(() => {
        useEventStore.getState().addEvent({
          type: 'human_anchor_requested',
          data: { request_id: 'req_123' },
          timestamp: '2026-01-01T00:00:00Z',
        })
      })

      expect(useEventStore.getState().events[0].type).toBe('human_anchor_requested')
    })
  })
})
