/**
 * SystemLogs - Observatory Style Event Telemetry Modal
 */

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
    label: 'INFO',
    color: 'var(--data-stream)',
    bgColor: 'rgba(0, 255, 255, 0.1)',
  },
  warning: {
    icon: AlertTriangle,
    label: 'WARN',
    color: 'var(--status-caution)',
    bgColor: 'rgba(255, 170, 0, 0.1)',
  },
  error: {
    icon: AlertCircle,
    label: 'ERROR',
    color: 'var(--status-critical)',
    bgColor: 'rgba(255, 51, 102, 0.1)',
  },
  debug: {
    icon: Bug,
    label: 'DEBUG',
    color: 'var(--obs-text-tertiary)',
    bgColor: 'rgba(107, 114, 128, 0.1)',
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
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="w-full sm:max-w-2xl bg-[var(--obs-bg-elevated)] rounded-t-lg sm:rounded-lg shadow-2xl animate-slide-up max-h-[85vh] flex flex-col border border-[var(--obs-border)]">
        {/* Header */}
        <div className="flex-shrink-0 bg-[var(--obs-bg-elevated)] border-b border-[var(--obs-border)] px-4 py-3 flex items-center justify-between">
          <div>
            <h2 className="obs-label text-sm tracking-widest text-[var(--obs-text-primary)]">
              SYSTEM TELEMETRY
            </h2>
            <p className="text-[10px] text-[var(--obs-text-tertiary)]">
              Real-time event stream monitoring
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-[var(--obs-bg-surface)] rounded transition-colors focus:outline-none focus:ring-1 focus:ring-[var(--data-stream)]"
            aria-label="Close logs"
          >
            <X className="w-5 h-5 text-[var(--obs-text-tertiary)]" />
          </button>
        </div>

        {/* Filters */}
        <div className="flex-shrink-0 border-b border-[var(--obs-border)] px-4 py-2">
          <div className="flex gap-2 overflow-x-auto scrollbar-hide">
            <FilterButton
              active={selectedLevel === 'all'}
              onClick={() => setSelectedLevel('all')}
              color="var(--obs-text-primary)"
              label={`ALL (${logCounts.all})`}
            />
            <FilterButton
              active={selectedLevel === 'info'}
              onClick={() => setSelectedLevel('info')}
              color="var(--data-stream)"
              label={`INFO (${logCounts.info})`}
            />
            <FilterButton
              active={selectedLevel === 'warning'}
              onClick={() => setSelectedLevel('warning')}
              color="var(--status-caution)"
              label={`WARN (${logCounts.warning})`}
            />
            <FilterButton
              active={selectedLevel === 'error'}
              onClick={() => setSelectedLevel('error')}
              color="var(--status-critical)"
              label={`ERROR (${logCounts.error})`}
            />
            <FilterButton
              active={selectedLevel === 'debug'}
              onClick={() => setSelectedLevel('debug')}
              color="var(--obs-text-tertiary)"
              label={`DEBUG (${logCounts.debug})`}
            />
          </div>
        </div>

        {/* Logs List */}
        <div className="flex-1 overflow-y-auto px-4 py-3 space-y-2">
          {filteredLogs.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div
                className="w-16 h-16 rounded flex items-center justify-center mb-4"
                style={{
                  backgroundColor: 'var(--obs-bg-surface)',
                  border: '1px solid var(--obs-border)',
                }}
              >
                <Info className="w-8 h-8" style={{ color: 'var(--obs-text-tertiary)' }} />
              </div>
              <p className="obs-label text-xs text-[var(--obs-text-primary)] mb-1">
                NO EVENTS RECORDED
              </p>
              <p className="text-[10px] text-[var(--obs-text-tertiary)]">
                {selectedLevel === 'all' ? 'Awaiting system telemetry...' : `No ${selectedLevel.toUpperCase()} events in buffer`}
              </p>
            </div>
          ) : (
            filteredLogs.map((log) => {
              const config = LEVEL_CONFIG[log.level];
              const Icon = config.icon;

              return (
                <div
                  key={log.id}
                  className="bg-[var(--obs-bg-surface)] rounded p-3 hover:bg-[var(--obs-bg-base)] transition-colors group border border-[var(--obs-border)]"
                >
                  <div className="flex items-start gap-3">
                    <div
                      className="p-1.5 rounded"
                      style={{ backgroundColor: config.bgColor }}
                    >
                      <Icon className="w-4 h-4" style={{ color: config.color }} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span
                          className="obs-label text-[9px]"
                          style={{ color: config.color }}
                        >
                          {config.label}
                        </span>
                        <span className="text-[8px] text-[var(--obs-text-tertiary)]">•</span>
                        <span className="obs-label text-[9px] text-[var(--obs-text-tertiary)]">
                          {log.source}
                        </span>
                      </div>
                      <p className="text-xs text-[var(--obs-text-secondary)] mb-2 font-mono">
                        {log.message}
                      </p>
                      <p className="text-[9px] text-[var(--obs-text-tertiary)] font-mono">
                        {new Date(log.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <button
                      onClick={() => handleCopy(log)}
                      className={cn(
                        "p-2 rounded transition-all opacity-0 group-hover:opacity-100",
                        copiedId === log.id
                          ? "bg-[var(--status-nominal)]/20 text-[var(--status-nominal)]"
                          : "hover:bg-[var(--obs-bg-elevated)] text-[var(--obs-text-tertiary)]"
                      )}
                      aria-label="Copy log entry"
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
        <div className="flex-shrink-0 bg-[var(--obs-bg-elevated)] border-t border-[var(--obs-border)] px-4 py-3 flex gap-2">
          <button
            onClick={handleClear}
            disabled={logs.length === 0}
            className="flex-1 py-2.5 px-4 bg-[var(--obs-bg-surface)] hover:bg-[var(--obs-bg-base)] disabled:opacity-50 disabled:cursor-not-allowed text-[var(--obs-text-secondary)] font-medium rounded transition-all focus:outline-none focus:ring-1 focus:ring-[var(--data-stream)] flex items-center justify-center gap-2 border border-[var(--obs-border)] obs-label text-[10px] tracking-wider"
          >
            <Trash2 className="w-4 h-4" />
            CLEAR BUFFER
          </button>
          <button
            onClick={onClose}
            className="flex-1 py-2.5 px-4 bg-[var(--data-stream)] hover:brightness-110 text-[var(--obs-bg-base)] font-medium rounded transition-all focus:outline-none focus:ring-2 focus:ring-[var(--data-stream)] obs-label text-[10px] tracking-wider"
          >
            CLOSE
          </button>
        </div>
      </div>
    </div>
  );
}

interface FilterButtonProps {
  active: boolean;
  onClick: () => void;
  color: string;
  label: string;
}

function FilterButton({ active, onClick, color, label }: FilterButtonProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "px-3 py-1.5 rounded text-[10px] font-medium whitespace-nowrap transition-all obs-label",
        active
          ? "shadow-[0_0_8px_var(--data-stream)]"
          : "bg-[var(--obs-bg-surface)] text-[var(--obs-text-tertiary)] hover:bg-[var(--obs-bg-base)] border border-[var(--obs-border)]"
      )}
      style={active ? { backgroundColor: color, color: 'var(--obs-bg-base)' } : {}}
    >
      {label}
    </button>
  );
}
