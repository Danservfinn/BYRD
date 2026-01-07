import { create } from 'zustand';
import { TabRoute, Theme, Breakpoint } from '@types/ui';

interface UIState {
  // Navigation
  currentTab: TabRoute;
  setCurrentTab: (tab: TabRoute) => void;

  // Theme
  theme: Theme;
  setTheme: (theme: Theme) => void;

  // Breakpoint
  breakpoint: Breakpoint;
  setBreakpoint: (breakpoint: Breakpoint) => void;

  // Drawer/Panel states
  isByrdChatOpen: boolean;
  setIsByrdChatOpen: (open: boolean) => void;

  // Loading states
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  currentTab: 'home',
  setCurrentTab: (tab) => set({ currentTab: tab }),

  theme: 'system',
  setTheme: (theme) => set({ theme }),

  breakpoint: 'mobile',
  setBreakpoint: (breakpoint) => set({ breakpoint }),

  isByrdChatOpen: false,
  setIsByrdChatOpen: (open) => set({ isByrdChatOpen: open }),

  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
}));
