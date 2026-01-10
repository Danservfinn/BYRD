/**
 * useTheme - Theme management hook with Observatory Dark as default
 *
 * The Observatory theme uses dark mode by default for the CERN/NASA
 * mission control aesthetic. Users can toggle to light mode if preferred.
 */

import { useEffect } from 'react';
import { useUIStore } from '../stores/uiStore';
import { safeGetStorage, safeSetStorage } from '../utils/storage';

const THEME_STORAGE_KEY = 'byrd-theme-preference';

// Default to dark theme for Observatory aesthetic
const DEFAULT_THEME = 'dark';

export function useTheme() {
  const { theme, setTheme } = useUIStore();

  // Load theme from localStorage on mount, default to dark (Observatory)
  useEffect(() => {
    const stored = safeGetStorage(THEME_STORAGE_KEY) as 'light' | 'dark' | 'system' | null;
    if (stored && (stored === 'light' || stored === 'dark' || stored === 'system')) {
      setTheme(stored);
    } else {
      // No stored preference - default to dark for Observatory aesthetic
      setTheme(DEFAULT_THEME);
      safeSetStorage(THEME_STORAGE_KEY, DEFAULT_THEME);
    }
  }, []); // Run once on mount

  // Apply theme to document
  useEffect(() => {
    const root = window.document.documentElement;
    const isDark =
      theme === 'dark' ||
      (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

    root.classList.remove('light', 'dark', 'observatory');
    root.classList.add(isDark ? 'dark' : 'light');
    // Add observatory class for dark mode (extra styles)
    if (isDark) {
      root.classList.add('observatory');
    }
  }, [theme]);

  const toggleTheme = () => {
    const isDark = window.document.documentElement.classList.contains('dark');
    const newTheme = isDark ? 'light' : 'dark';
    setTheme(newTheme);
    safeSetStorage(THEME_STORAGE_KEY, newTheme);
  };

  // Override setTheme to also persist to localStorage
  const setThemeWithPersistence = (newTheme: 'light' | 'dark' | 'system') => {
    setTheme(newTheme);
    safeSetStorage(THEME_STORAGE_KEY, newTheme);
  };

  return { theme, toggleTheme, setTheme: setThemeWithPersistence };
}
