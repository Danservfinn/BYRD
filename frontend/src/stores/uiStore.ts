import { create } from 'zustand';
import type { TabRoute, Theme, Breakpoint } from '../types/ui';

interface UIState {
  // Navigation
  currentTab: TabRoute;
  setCurrentTab: (tab: TabRoute) => void;

  // Theme
  theme: Theme;
  setTheme: (theme: Theme) => void;

  // Responsive
  breakpoint: Breakpoint;
  setBreakpoint: (breakpoint: Breakpoint) => void;

  // UI States
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;

  isByrdChatOpen: boolean;
  setIsByrdChatOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  // Navigation
  currentTab: 'home',
  setCurrentTab: (tab) => set({ currentTab: tab }),

  // Theme - default to system preference
  theme: 'system',
  setTheme: (theme) => set({ theme }),

  // Responsive
  breakpoint: 'mobile',
  setBreakpoint: (breakpoint) => set({ breakpoint }),

  // UI States
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),

  isByrdChatOpen: false,
  setIsByrdChatOpen: (open) => set({ isByrdChatOpen: open }),
}));
