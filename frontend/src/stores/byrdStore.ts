import { create } from 'zustand';
import { ByrdState, ChatMessage } from '@types/api';
import { AnimationState } from '@types/ui';

interface ByrdDataState {
  // BYRD state
  byrdState: ByrdState | null;
  setByrdState: (state: ByrdState) => void;

  // Chat
  messages: ChatMessage[];
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;

  // Avatar animation
  animationState: AnimationState;
  setAnimationState: (state: AnimationState) => void;

  // Typing indicator
  isTyping: boolean;
  setIsTyping: (typing: boolean) => void;
}

export const useByrdStore = create<ByrdDataState>((set) => ({
  byrdState: null,
  setByrdState: (state) => set({ byrdState: state }),

  messages: [],
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message],
  })),
  clearMessages: () => set({ messages: [] }),

  animationState: 'idle',
  setAnimationState: (state) => set({ animationState: state }),

  isTyping: false,
  setIsTyping: (typing) => set({ isTyping: typing }),
}));
