import { useEffect } from 'react';
import { useUIStore } from '../stores/uiStore';

const THEME_STORAGE_KEY = 'byrd-theme-preference';

// Safe localStorage access with fallback for iframe contexts
const safeGetStorage = (key: string): string | null => {
  try {
    return localStorage.getItem(key);
  } catch (e) {
    // localStorage not available (iframe context, private browsing, etc.)
    return null;
  }
};

const safeSetStorage = (key: string, value: string): void => {
  try {
    localStorage.setItem(key, value);
  } catch (e) {
    // Silently fail in contexts where localStorage is not available
    console.debug('Theme preference not saved (storage not available)');
  }
};

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
    const root = window.document.documentElement;
    const isDark = root.classList.contains('dark');

    const newTheme = isDark ? 'light' : 'dark';
    setTheme(newTheme);
    safeSetStorage(THEME_STORAGE_KEY, newTheme);

    root.classList.remove('dark', 'light');
    root.classList.add(newTheme);
  };

  // Override setTheme to also persist to localStorage
  const setThemeWithPersistence = (newTheme: 'light' | 'dark' | 'system') => {
    setTheme(newTheme);
    safeSetStorage(THEME_STORAGE_KEY, newTheme);
  };

  return { theme, toggleTheme, setTheme: setThemeWithPersistence };
}
