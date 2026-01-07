import { X, Moon, Sun, Monitor, Check } from 'lucide-react';
import { GlassPanel } from '../common/GlassPanel';
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
      name: 'Light',
      description: 'Clean and bright',
      icon: Sun,
    },
    {
      id: 'dark' as const,
      name: 'Dark',
      description: 'Easy on the eyes',
      icon: Moon,
    },
    {
      id: 'system' as const,
      name: 'System',
      description: 'Follows your device',
      icon: Monitor,
    },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/50 backdrop-blur-sm animate-fade-in">
      <div className="w-full sm:max-w-md bg-white dark:bg-slate-800 rounded-t-2xl sm:rounded-2xl shadow-2xl animate-slide-up max-h-[80vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 px-4 py-3 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              Appearance
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Customize your visual experience
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500"
            aria-label="Close settings"
          >
            <X className="w-5 h-5 text-slate-600 dark:text-slate-400" />
          </button>
        </div>

        {/* Theme Selection */}
        <div className="p-4 space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
              Color Theme
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
                      "w-full flex items-center justify-between p-4 rounded-lg border-2 transition-all",
                      isActive
                        ? "border-purple-600 dark:border-purple-400 bg-purple-50 dark:bg-purple-900/20"
                        : "border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600"
                    )}
                    aria-label={`Select ${themeOption.name} theme`}
                    aria-pressed={isActive}
                  >
                    <div className="flex items-center gap-3">
                      <div className={cn(
                        "p-2 rounded-lg",
                        isActive ? "bg-purple-600 dark:bg-purple-400" : "bg-slate-100 dark:bg-slate-700"
                      )}>
                        <Icon className={cn(
                          "w-5 h-5",
                          isActive ? "text-white" : "text-slate-600 dark:text-slate-400"
                        )} />
                      </div>
                      <div className="text-left">
                        <span className="block text-sm font-medium text-slate-900 dark:text-slate-100">
                          {themeOption.name}
                        </span>
                        <span className="block text-xs text-slate-500 dark:text-slate-400">
                          {themeOption.description}
                        </span>
                      </div>
                    </div>
                    {isActive && (
                      <Check className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Info Panel */}
          <GlassPanel padding="sm">
            <div className="flex gap-3">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                  <Monitor className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                </div>
              </div>
              <div className="flex-1">
                <h4 className="text-sm font-medium text-slate-900 dark:text-slate-100 mb-1">
                  About themes
                </h4>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  Your theme preference is saved automatically and will persist across sessions.
                  The System theme automatically switches between light and dark based on your
                  device settings.
                </p>
              </div>
            </div>
          </GlassPanel>
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700 px-4 py-3">
          <button
            onClick={onClose}
            className="w-full py-2.5 px-4 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
