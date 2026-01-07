import { create } from 'zustand';
import type { ByrdEvent } from '../types/events';

interface EventStore {
  events: ByrdEvent[];
  connected: boolean;
  lastEventTime: string | null;

  addEvent: (event: ByrdEvent) => void;
  setConnected: (connected: boolean) => void;
  clearEvents: () => void;
  getEventsByType: (type: string) => ByrdEvent[];
}

const MAX_EVENTS = 500;

export const useEventStore = create<EventStore>((set, get) => ({
  events: [],
  connected: false,
  lastEventTime: null,

  addEvent: (event) => {
    set((state) => ({
      events: [event, ...state.events].slice(0, MAX_EVENTS),
      lastEventTime: event.timestamp,
    }));
  },

  setConnected: (connected) => set({ connected }),

  clearEvents: () => set({ events: [], lastEventTime: null }),

  getEventsByType: (type) => {
    return get().events.filter((e) => e.type === type);
  },
}));
