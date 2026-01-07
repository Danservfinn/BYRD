import { create } from 'zustand';
import type { ChatMessage } from '../types/api';

export interface ByrdState {
  cycle_id: string | null;
  phase: string | null;
  emergence_score: number | null;
  treasury_balance: number | null;
}

interface ByrdDataState {
  byrdState: ByrdState | null;
  messages: ChatMessage[];
  animationState: 'idle' | 'thinking' | 'speaking' | 'celebrating' | 'concerned';
  isTyping: boolean;

  setByrdState: (state: ByrdState) => void;
  setAnimationState: (state: 'idle' | 'thinking' | 'speaking' | 'celebrating' | 'concerned') => void;
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;
  setTyping: (typing: boolean) => void;
}

export const useByrdStore = create<ByrdDataState>((set) => ({
  byrdState: null,
  messages: [],
  animationState: 'idle',
  isTyping: false,

  setByrdState: (state) => set({ byrdState: state }),

  setAnimationState: (state) => set({ animationState: state }),

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  clearMessages: () => set({ messages: [] }),

  setTyping: (typing) => set({ isTyping: typing }),
}));
