/**
 * AppearanceSettings - Observatory Style Theme Configuration Modal
 */

import { X, Moon, Sun, Monitor, Check } from 'lucide-react';
import { useTheme } from '../../hooks/useTheme';
import { cn } from '@lib/utils/cn';

interface AppearanceSettingsProps {
  onClose: () => void;
}

export function AppearanceSettings({ onClose }: AppearanceSettingsProps) {
  const { theme, setTheme } = useTheme();

  const themes = [
    {
      id: 'light' as const,
      name: 'DIURNAL',
      description: 'Standard illumination',
      icon: Sun,
      color: 'var(--status-caution)',
    },
    {
      id: 'dark' as const,
      name: 'OBSERVATORY',
      description: 'Deep space optimized',
      icon: Moon,
      color: 'var(--data-stream)',
    },
    {
      id: 'system' as const,
      name: 'ADAPTIVE',
      description: 'Follows system clock',
      icon: Monitor,
      color: 'var(--rsi-reflect)',
    },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="w-full sm:max-w-md bg-[var(--obs-bg-elevated)] rounded-t-lg sm:rounded-lg shadow-2xl animate-slide-up max-h-[80vh] overflow-y-auto border border-[var(--obs-border)]">
        {/* Header */}
        <div className="sticky top-0 bg-[var(--obs-bg-elevated)] border-b border-[var(--obs-border)] px-4 py-3 flex items-center justify-between">
          <div>
            <h2 className="obs-label text-sm tracking-widest text-[var(--obs-text-primary)]">
              APPEARANCE
            </h2>
            <p className="text-[10px] text-[var(--obs-text-tertiary)]">
              Visual configuration module
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-[var(--obs-bg-surface)] rounded transition-colors focus:outline-none focus:ring-1 focus:ring-[var(--data-stream)]"
            aria-label="Close settings"
          >
            <X className="w-5 h-5 text-[var(--obs-text-tertiary)]" />
          </button>
        </div>

        {/* Theme Selection */}
        <div className="p-4 space-y-4">
          <div>
            <h3 className="obs-label text-[10px] text-[var(--obs-text-tertiary)] mb-3">
              COLOR SCHEME
            </h3>
            <div className="space-y-2">
              {themes.map((themeOption) => {
                const Icon = themeOption.icon;
                const isActive = theme === themeOption.id;

                return (
                  <button
                    key={themeOption.id}
                    onClick={() => setTheme(themeOption.id)}
                    className={cn(
                      "w-full flex items-center justify-between p-4 rounded border transition-all",
                      isActive
                        ? "border-[var(--data-stream)] bg-[var(--obs-bg-surface)]"
                        : "border-[var(--obs-border)] hover:border-[var(--obs-text-tertiary)] hover:bg-[var(--obs-bg-surface)]"
                    )}
                    aria-label={`Select ${themeOption.name} theme`}
                    aria-pressed={isActive}
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={cn(
                          "w-10 h-10 rounded flex items-center justify-center transition-all",
                          isActive ? "shadow-[0_0_12px_var(--data-stream)]" : ""
                        )}
                        style={{
                          backgroundColor: isActive ? 'var(--obs-bg-base)' : 'var(--obs-bg-surface)',
                          border: isActive ? `1px solid ${themeOption.color}` : '1px solid var(--obs-border)',
                        }}
                      >
                        <Icon
                          className="w-5 h-5"
                          style={{ color: isActive ? themeOption.color : 'var(--obs-text-tertiary)' }}
                        />
                      </div>
                      <div className="text-left">
                        <span className="obs-label text-[11px] text-[var(--obs-text-primary)] block">
                          {themeOption.name}
                        </span>
                        <span className="text-[10px] text-[var(--obs-text-tertiary)]">
                          {themeOption.description}
                        </span>
                      </div>
                    </div>
                    {isActive && (
                      <div
                        className="w-6 h-6 rounded flex items-center justify-center"
                        style={{ backgroundColor: 'var(--data-stream)' }}
                      >
                        <Check className="w-4 h-4 text-[var(--obs-bg-base)]" />
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Info Panel */}
          <div className="bg-[var(--obs-bg-surface)] rounded p-4 border border-[var(--obs-border)]">
            <div className="flex gap-3">
              <div className="flex-shrink-0">
                <div
                  className="w-8 h-8 rounded flex items-center justify-center"
                  style={{
                    backgroundColor: 'var(--obs-bg-base)',
                    border: '1px solid var(--data-stream)',
                  }}
                >
                  <Monitor className="w-4 h-4" style={{ color: 'var(--data-stream)' }} />
                </div>
              </div>
              <div className="flex-1">
                <h4 className="obs-label text-[10px] text-[var(--obs-text-primary)] mb-1">
                  THEME PERSISTENCE
                </h4>
                <p className="text-[10px] text-[var(--obs-text-tertiary)] leading-relaxed">
                  Configuration is preserved in local storage.
                  ADAPTIVE mode synchronizes with your operating system preferences.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-[var(--obs-bg-elevated)] border-t border-[var(--obs-border)] px-4 py-3">
          <button
            onClick={onClose}
            className="w-full py-2.5 px-4 bg-[var(--data-stream)] hover:brightness-110 text-[var(--obs-bg-base)] font-medium rounded transition-all focus:outline-none focus:ring-2 focus:ring-[var(--data-stream)] focus:ring-offset-2 focus:ring-offset-[var(--obs-bg-elevated)] obs-label text-xs tracking-wider"
          >
            CONFIRM
          </button>
        </div>
      </div>
    </div>
  );
}
