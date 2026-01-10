/**
 * Header - Observatory Style Navigation
 */

import { ArrowLeft, Settings, Moon, Sun } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../../hooks/useTheme';
import { StatusIndicator } from '../common/ObservatoryPanel';

interface HeaderProps {
  title?: string;
  showBack?: boolean;
  showSettings?: boolean;
  status?: 'nominal' | 'caution' | 'critical' | 'inactive';
}

export function Header({
  title = 'BYRD',
  showBack = false,
  showSettings = true,
  status = 'inactive',
}: HeaderProps) {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

  return (
    <header className="flex-shrink-0 bg-[var(--obs-bg-surface)] border-b border-[var(--obs-border)] px-4 py-3">
      <div className="flex items-center justify-between max-w-4xl mx-auto">
        {/* Left: Back button + Title + Status */}
        <div className="flex items-center gap-3">
          {showBack && (
            <button
              onClick={() => navigate(-1)}
              className="p-2 -ml-2 hover:bg-[var(--obs-bg-elevated)] rounded transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--data-stream)]"
              aria-label="Go back"
            >
              <ArrowLeft className="w-5 h-5 text-[var(--obs-text-secondary)]" />
            </button>
          )}
          <h1 className="obs-label text-sm tracking-widest text-[var(--obs-text-primary)]">
            {title}
          </h1>
          <StatusIndicator status={status} size="sm" />
        </div>

        {/* Right: Theme toggle + Settings */}
        <div className="flex items-center gap-2">
          <button
            onClick={toggleTheme}
            className="p-2 rounded hover:bg-[var(--obs-bg-elevated)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--data-stream)]"
            aria-label="Toggle theme"
          >
            {isDark ? (
              <Sun className="w-5 h-5 text-[var(--cat-eye-gold)]" />
            ) : (
              <Moon className="w-5 h-5 text-[var(--obs-text-secondary)]" />
            )}
          </button>

          {showSettings && (
            <button
              onClick={() => navigate('/more')}
              className="p-2 rounded hover:bg-[var(--obs-bg-elevated)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--data-stream)]"
              aria-label="Settings"
            >
              <Settings className="w-5 h-5 text-[var(--obs-text-secondary)]" />
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
