import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

export function SystemStatus() {
  const { getRSIStatus, loading } = useByrdAPI();
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      const result = await getRSIStatus();
      if (result) {
        setStatus(result);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, [getRSIStatus]);

  return (
    <GlassPanel glow="blue" padding="lg" className="h-full">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          System Status
        </h2>
        <StatusBadge status={status?.running ? 'running' : 'idle'} />
      </div>

      {loading && !status ? (
        <div className="flex items-center justify-center h-32">
          <span className="text-slate-400 animate-pulse">Loading...</span>
        </div>
      ) : (
        <div className="space-y-4">
          {/* RSI Phase Indicator */}
          <div>
            <label className="text-xs text-slate-500 uppercase tracking-wide">
              Current Phase
            </label>
            <div className="flex items-center gap-2 mt-1">
              <PhaseIndicator phase={status?.current_phase || 'idle'} />
            </div>
          </div>

          {/* RSI Cycle Progress */}
          <div>
            <label className="text-xs text-slate-500 uppercase tracking-wide">
              Cycle Progress
            </label>
            <div className="grid grid-cols-8 gap-1 mt-2">
              {['reflect', 'verify', 'collapse', 'route', 'practice', 'record', 'crystallize', 'measure'].map((phase) => (
                <PhaseBlock
                  key={phase}
                  phase={phase}
                  active={status?.current_phase === phase}
                  completed={isPhaseCompleted(status?.completed_phases, phase)}
                />
              ))}
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-200 dark:border-slate-700">
            <MiniStat label="Cycles" value={status?.cycle_count || 0} />
            <MiniStat label="Heuristics" value={status?.heuristics_count || 0} />
            <MiniStat label="Beliefs" value={status?.beliefs_count || 0} />
            <MiniStat label="Capabilities" value={status?.capabilities_count || 0} />
          </div>
        </div>
      )}
    </GlassPanel>
  );
}

function StatusBadge({ status }: { status: 'running' | 'idle' | 'error' }) {
  const config = {
    running: { bg: 'bg-green-100 dark:bg-green-900/30', text: 'text-green-700 dark:text-green-400', label: 'Running' },
    idle: { bg: 'bg-slate-100 dark:bg-slate-800', text: 'text-slate-600 dark:text-slate-400', label: 'Idle' },
    error: { bg: 'bg-red-100 dark:bg-red-900/30', text: 'text-red-700 dark:text-red-400', label: 'Error' },
  };
  const c = config[status];
  return (
    <span className={`px-2 py-1 rounded text-xs font-medium ${c.bg} ${c.text}`}>
      {c.label}
    </span>
  );
}

function PhaseIndicator({ phase }: { phase: string }) {
  const phaseColors: Record<string, string> = {
    reflect: 'var(--rsi-reflect)',
    verify: 'var(--rsi-verify)',
    collapse: 'var(--rsi-collapse)',
    route: 'var(--rsi-route)',
    practice: 'var(--rsi-practice)',
    record: 'var(--rsi-record)',
    crystallize: 'var(--rsi-crystallize)',
    measure: 'var(--rsi-measure)',
    idle: '#64748b',
  };

  return (
    <div className="flex items-center gap-2">
      <span
        className="w-3 h-3 rounded-full"
        style={{ backgroundColor: phaseColors[phase] || phaseColors.idle }}
      />
      <span className="text-lg font-medium text-slate-900 dark:text-slate-100 capitalize">
        {phase}
      </span>
    </div>
  );
}

function PhaseBlock({ phase, active, completed }: { phase: string; active: boolean; completed: boolean }) {
  const phaseColors: Record<string, string> = {
    reflect: 'var(--rsi-reflect)',
    verify: 'var(--rsi-verify)',
    collapse: 'var(--rsi-collapse)',
    route: 'var(--rsi-route)',
    practice: 'var(--rsi-practice)',
    record: 'var(--rsi-record)',
    crystallize: 'var(--rsi-crystallize)',
    measure: 'var(--rsi-measure)',
  };

  return (
    <div
      className={`h-8 rounded flex items-center justify-center text-xs ${
        active ? 'animate-pulse' : ''
      }`}
      style={{
        backgroundColor: completed || active ? phaseColors[phase] : 'rgba(100, 116, 139, 0.2)',
        opacity: completed ? 1 : active ? 0.8 : 0.3,
      }}
      title={phase.charAt(0).toUpperCase() + phase.slice(1)}
    >
      <span className="text-white font-medium">
        {phase.charAt(0).toUpperCase()}
      </span>
    </div>
  );
}

function MiniStat({ label, value }: { label: string; value: number | string }) {
  return (
    <div>
      <div className="text-xs text-slate-500 uppercase tracking-wide">{label}</div>
      <div className="text-xl font-semibold text-slate-900 dark:text-slate-100">{value}</div>
    </div>
  );
}

function isPhaseCompleted(completedPhases: string[] | undefined, phase: string): boolean {
  if (!completedPhases) return false;
  return completedPhases.includes(phase);
}
