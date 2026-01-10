/**
 * Safe localStorage utilities for contexts where localStorage may be unavailable
 * (iframe contexts, private browsing, etc.)
 */

/**
 * Safely retrieve a value from localStorage with fallback for restricted contexts
 */
export function safeGetStorage(key: string): string | null {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

/**
 * Safely set a value in localStorage with silent failure for restricted contexts
 */
export function safeSetStorage(key: string, value: string): void {
  try {
    localStorage.setItem(key, value);
  } catch {
    // Silently fail in contexts where localStorage is not available
  }
}
