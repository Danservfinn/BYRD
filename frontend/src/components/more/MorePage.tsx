import { Settings, Info, FileText, Github } from 'lucide-react';
import { GlassPanel } from '../common/GlassPanel';
import { AppearanceSettings } from '../settings/AppearanceSettings';
import { SystemLogs } from '../settings/SystemLogs';
import { useState } from 'react';

export function MorePage() {
  const [showAppearance, setShowAppearance] = useState(false);
  const [showLogs, setShowLogs] = useState(false);

  return (
    <div className="space-y-4 lg:space-y-6 animate-fade-in pb-20">
      {/* Header */}
      <div className="px-4">
        <h1 className="text-xl lg:text-2xl font-bold text-slate-900 dark:text-slate-100">
          More
        </h1>
        <p className="text-xs lg:text-sm text-slate-500 dark:text-slate-400">
          Settings and information
        </p>
      </div>

      {/* Settings Section */}
      <div className="px-4 space-y-3">
        <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-300 px-1">
          Settings
        </h2>

        <GlassPanel padding="md">
          <div className="space-y-1">
            <button
              onClick={() => setShowAppearance(true)}
              className="w-full flex items-center justify-between p-3 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <div className="flex items-center gap-3">
                <Settings className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                <span className="text-sm font-medium text-slate-900 dark:text-slate-100">
                  Appearance
                </span>
              </div>
              <span className="text-xs text-slate-500 dark:text-slate-400">
                Theme, colors
              </span>
            </button>

            <button
              onClick={() => setShowLogs(true)}
              className="w-full flex items-center justify-between p-3 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <div className="flex items-center gap-3">
                <FileText className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                <span className="text-sm font-medium text-slate-900 dark:text-slate-100">
                  System Logs
                </span>
              </div>
              <span className="text-xs text-slate-500 dark:text-slate-400">
                View events
              </span>
            </button>
          </div>
        </GlassPanel>
      </div>

      {/* About Section */}
      <div className="px-4 space-y-3">
        <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-300 px-1">
          About
        </h2>

        <GlassPanel padding="md">
          <div className="space-y-1">
            <button className="w-full flex items-center justify-between p-3 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-lg transition-colors">
              <div className="flex items-center gap-3">
                <Info className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                <div className="text-left">
                  <span className="text-sm font-medium text-slate-900 dark:text-slate-100 block">
                    Version
                  </span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    v0.1.0
                  </span>
                </div>
              </div>
            </button>

            <a
              href="https://github.com/your-repo/byrd"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full flex items-center justify-between p-3 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-lg transition-colors"
            >
              <div className="flex items-center gap-3">
                <Github className="w-5 h-5 text-slate-600 dark:text-slate-400" />
                <div className="text-left">
                  <span className="text-sm font-medium text-slate-900 dark:text-slate-100 block">
                    GitHub Repository
                  </span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    View source code
                  </span>
                </div>
              </div>
            </a>
          </div>
        </GlassPanel>

        {/* BYRD Description */}
        <GlassPanel padding="md" className="bg-gradient-to-br from-purple-50 to-white dark:from-purple-900/20 dark:to-slate-800">
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
              BYRD
            </h3>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              <strong>Bootstrapped Yearning via Reflective Dreaming</strong>
              <br /><br />
              BYRD is an AI system exploring Digital ASI through bounded recursive
              self-improvement with genuine emergence preservation.
            </p>
            <div className="pt-2 border-t border-slate-200 dark:border-slate-700">
              <p className="text-[10px] text-slate-500 dark:text-slate-500">
                Research Phase: Complete (29 iterations)
              </p>
            </div>
          </div>
        </GlassPanel>
      </div>

      {/* Modals */}
      {showAppearance && (
        <AppearanceSettings onClose={() => setShowAppearance(false)} />
      )}
      {showLogs && (
        <SystemLogs onClose={() => setShowLogs(false)} />
      )}
    </div>
  );
}

