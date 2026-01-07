import { useEffect } from 'react';
import { useUIStore } from '../stores/uiStore';

export function useTheme() {
  const { theme, setTheme } = useUIStore();

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

    if (isDark) {
      setTheme('light');
      root.classList.remove('dark');
      root.classList.add('light');
    } else {
      setTheme('dark');
      root.classList.remove('light');
      root.classList.add('dark');
    }
  };

  return { theme, toggleTheme, setTheme };
}
