import { useState } from 'react';
import { ChevronDown, ChevronUp, RefreshCw } from 'lucide-react';

export function StatusBar() {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="px-4 py-2 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
      {/* Collapsed state */}
      {!isExpanded && (
        <button
          onClick={() => setIsExpanded(true)}
          className="w-full flex items-center justify-between text-sm"
        >
          <div className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4 text-purple-600 dark:text-purple-400 animate-spin" />
            <span className="font-medium text-slate-900 dark:text-slate-100">
              Phase 3: PRACTICE
            </span>
          </div>
          <ChevronDown className="w-4 h-4 text-slate-400" />
        </button>
      )}

      {/* Expanded state */}
      {isExpanded && (
        <div className="space-y-2">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <RefreshCw className="w-4 h-4 text-purple-600 dark:text-purple-400 animate-spin-slow" />
              <div>
                <p className="text-sm font-medium text-slate-900 dark:text-slate-100">
                  🔄 RSI Cycle #28
                </p>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Phase 3: PRACTICE • 2m 34s remaining
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsExpanded(false)}
              className="p-1 hover:bg-slate-100 dark:hover:bg-slate-700 rounded transition-colors"
            >
              <ChevronUp className="w-4 h-4 text-slate-400" />
            </button>
          </div>

          {/* Metrics */}
          <div className="flex gap-4 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="text-slate-500 dark:text-slate-400">Emergence:</span>
              <span className="font-medium text-slate-900 dark:text-slate-100">0.847 ↑</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="text-slate-500 dark:text-slate-400">Treasury:</span>
              <span className="font-medium text-slate-900 dark:text-slate-100">$12.4K</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
