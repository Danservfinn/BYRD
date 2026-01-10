import { useEffect } from 'react';
import { useUIStore } from '../stores/uiStore';
import { safeGetStorage, safeSetStorage } from '../utils/storage';

const THEME_STORAGE_KEY = 'byrd-theme-preference';

export function useTheme() {
  const { theme, setTheme } = useUIStore();

  // Load theme from localStorage on mount
  useEffect(() => {
    const stored = safeGetStorage(THEME_STORAGE_KEY) as 'light' | 'dark' | 'system' | null;
    if (stored && (stored === 'light' || stored === 'dark' || stored === 'system')) {
      setTheme(stored);
    }
  }, []); // Run once on mount

  // Apply theme to document
  useEffect(() => {
    const root = window.document.documentElement;
    const isDark =
      theme === 'dark' ||
      (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

    root.classList.remove('light', 'dark');
    root.classList.add(isDark ? 'dark' : 'light');
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
