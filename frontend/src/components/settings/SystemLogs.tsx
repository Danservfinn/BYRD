import { X, AlertCircle, Info, AlertTriangle, Bug, Copy, Trash2 } from 'lucide-react';
import { cn } from '@lib/utils/cn';
import { useState } from 'react';

interface LogEntry {
  id: string;
  timestamp: string;
  level: 'info' | 'warning' | 'error' | 'debug';
  source: string;
  message: string;
}

interface SystemLogsProps {
  onClose: () => void;
}

// Mock log data - in production, this would come from the backend
const MOCK_LOGS: LogEntry[] = [
  {
    id: '1',
    timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    level: 'info',
    source: 'BYRD.Core',
    message: 'Ralph Loop cycle 33 completed successfully',
  },
  {
    id: '2',
    timestamp: new Date(Date.now() - 1000 * 60 * 4).toISOString(),
    level: 'debug',
    source: 'RSI.Engine',
    message: 'Phase REFLECT: Analyzed 47 recent experiences',
  },
  {
    id: '3',
    timestamp: new Date(Date.now() - 1000 * 60 * 3).toISOString(),
    level: 'info',
    source: 'Memory.System',
    message: 'Created 3 new belief nodes from reflection cycle',
  },
  {
    id: '4',
    timestamp: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
    level: 'warning',
    source: 'Orchestration',
    message: 'Complexity score 0.52 above threshold, using decomposition strategy',
  },
  {
    id: '5',
    timestamp: new Date(Date.now() - 1000 * 60 * 1).toISOString(),
    level: 'debug',
    source: 'Verification',
    message: 'Lattice verification: 4/5 verifiers passed (80% agreement)',
  },
  {
    id: '6',
    timestamp: new Date().toISOString(),
    level: 'info',
    source: 'BYRD.Core',
    message: 'Frontend deployment to HuggingFace Spaces complete',
  },
];

const LEVEL_CONFIG = {
  info: {
    icon: Info,
    label: 'Info',
    color: 'text-blue-600 dark:text-blue-400',
    bgColor: 'bg-blue-100 dark:bg-blue-900/30',
  },
  warning: {
    icon: AlertTriangle,
    label: 'Warning',
    color: 'text-amber-600 dark:text-amber-400',
    bgColor: 'bg-amber-100 dark:bg-amber-900/30',
  },
  error: {
    icon: AlertCircle,
    label: 'Error',
    color: 'text-red-600 dark:text-red-400',
    bgColor: 'bg-red-100 dark:bg-red-900/30',
  },
  debug: {
    icon: Bug,
    label: 'Debug',
    color: 'text-slate-600 dark:text-slate-400',
    bgColor: 'bg-slate-100 dark:bg-slate-700/50',
  },
};

export function SystemLogs({ onClose }: SystemLogsProps) {
  const [logs, setLogs] = useState<LogEntry[]>(MOCK_LOGS);
  const [selectedLevel, setSelectedLevel] = useState<'all' | LogEntry['level']>('all');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const filteredLogs = selectedLevel === 'all'
    ? logs
    : logs.filter(log => log.level === selectedLevel);

  const handleCopy = (log: LogEntry) => {
    const text = `[${log.level.toUpperCase()}] ${new Date(log.timestamp).toLocaleString()} - ${log.source}: ${log.message}`;
    navigator.clipboard.writeText(text);
    setCopiedId(log.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleClear = () => {
    setLogs([]);
  };

  const logCounts = {
    all: logs.length,
    info: logs.filter(l => l.level === 'info').length,
    warning: logs.filter(l => l.level === 'warning').length,
    error: logs.filter(l => l.level === 'error').length,
    debug: logs.filter(l => l.level === 'debug').length,
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/50 backdrop-blur-sm animate-fade-in">
      <div className="w-full sm:max-w-2xl bg-white dark:bg-slate-800 rounded-t-2xl sm:rounded-2xl shadow-2xl animate-slide-up max-h-[85vh] flex flex-col">
        {/* Header */}
        <div className="flex-shrink-0 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 px-4 py-3 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              System Logs
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Real-time system events and debugging information
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500"
            aria-label="Close logs"
          >
            <X className="w-5 h-5 text-slate-600 dark:text-slate-400" />
          </button>
        </div>

        {/* Filters */}
        <div className="flex-shrink-0 border-b border-slate-200 dark:border-slate-700 px-4 py-2">
          <div className="flex gap-2 overflow-x-auto scrollbar-hide">
            <button
              onClick={() => setSelectedLevel('all')}
              className={cn(
                "px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors",
                selectedLevel === 'all'
                  ? "bg-purple-600 text-white"
                  : "bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600"
              )}
            >
              All ({logCounts.all})
            </button>
            <button
              onClick={() => setSelectedLevel('info')}
              className={cn(
                "px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors",
                selectedLevel === 'info'
                  ? "bg-blue-600 text-white"
                  : "bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600"
              )}
            >
              Info ({logCounts.info})
            </button>
            <button
              onClick={() => setSelectedLevel('warning')}
              className={cn(
                "px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors",
                selectedLevel === 'warning'
                  ? "bg-amber-600 text-white"
                  : "bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600"
              )}
            >
              Warnings ({logCounts.warning})
            </button>
            <button
              onClick={() => setSelectedLevel('error')}
              className={cn(
                "px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors",
                selectedLevel === 'error'
                  ? "bg-red-600 text-white"
                  : "bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600"
              )}
            >
              Errors ({logCounts.error})
            </button>
            <button
              onClick={() => setSelectedLevel('debug')}
              className={cn(
                "px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors",
                selectedLevel === 'debug'
                  ? "bg-slate-600 text-white"
                  : "bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600"
              )}
            >
              Debug ({logCounts.debug})
            </button>
          </div>
        </div>

        {/* Logs List */}
        <div className="flex-1 overflow-y-auto px-4 py-3 space-y-2">
          {filteredLogs.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="w-16 h-16 rounded-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center mb-4">
                <Info className="w-8 h-8 text-slate-400" />
              </div>
              <p className="text-sm font-medium text-slate-900 dark:text-slate-100 mb-1">
                No logs found
              </p>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {selectedLevel === 'all' ? 'No system events recorded yet' : `No ${selectedLevel} logs to display`}
              </p>
            </div>
          ) : (
            filteredLogs.map((log) => {
              const config = LEVEL_CONFIG[log.level];
              const Icon = config.icon;

              return (
                <div
                  key={log.id}
                  className="bg-slate-50 dark:bg-slate-900/50 rounded-lg p-3 hover:bg-slate-100 dark:hover:bg-slate-900 transition-colors group"
                >
                  <div className="flex items-start gap-3">
                    <div className={cn("p-1.5 rounded-lg", config.bgColor)}>
                      <Icon className={cn("w-4 h-4", config.color)} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={cn("text-xs font-medium", config.color)}>
                          {config.label}
                        </span>
                        <span className="text-xs text-slate-400">•</span>
                        <span className="text-xs text-slate-500 dark:text-slate-400">
                          {log.source}
                        </span>
                      </div>
                      <p className="text-sm text-slate-700 dark:text-slate-300 mb-2">
                        {log.message}
                      </p>
                      <p className="text-xs text-slate-400 dark:text-slate-500">
                        {new Date(log.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <button
                      onClick={() => handleCopy(log)}
                      className={cn(
                        "p-2 rounded-lg transition-all opacity-0 group-hover:opacity-100",
                        copiedId === log.id
                          ? "bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400"
                          : "hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500"
                      )}
                      aria-label={`Copy log entry`}
                    >
                      <Copy className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="flex-shrink-0 bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700 px-4 py-3 flex gap-2">
          <button
            onClick={handleClear}
            disabled={logs.length === 0}
            className="flex-1 py-2.5 px-4 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed text-slate-700 dark:text-slate-300 font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 flex items-center justify-center gap-2"
          >
            <Trash2 className="w-4 h-4" />
            Clear Logs
          </button>
          <button
            onClick={onClose}
            className="flex-1 py-2.5 px-4 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
