import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

const PHASES = [
  { id: 'reflect', name: 'Reflect', icon: '🔮', description: 'Generate improvement desires' },
  { id: 'verify', name: 'Verify', icon: '✓', description: 'Check emergence validity' },
  { id: 'collapse', name: 'Collapse', icon: '🎲', description: 'Quantum selection' },
  { id: 'route', name: 'Route', icon: '🔀', description: 'Domain classification' },
  { id: 'practice', name: 'Practice', icon: '🎯', description: 'TDD execution' },
  { id: 'record', name: 'Record', icon: '📝', description: 'Store trajectory' },
  { id: 'crystallize', name: 'Crystallize', icon: '💎', description: 'Extract heuristics' },
  { id: 'measure', name: 'Measure', icon: '📊', description: 'Track metrics' },
];

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

export function PhaseTracker() {
  const { getRSIStatus } = useByrdAPI();
  const [currentPhase, setCurrentPhase] = useState<string | null>(null);
  const [completedPhases, setCompletedPhases] = useState<string[]>([]);

  useEffect(() => {
    const fetchStatus = async () => {
      const result = await getRSIStatus();
      if (result) {
        setCurrentPhase(result.current_phase || null);
        setCompletedPhases(result.completed_phases || []);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, [getRSIStatus]);

  return (
    <GlassPanel glow="blue" padding="lg">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Phase Tracker
        </h2>
        <span className="text-sm text-slate-500">
          {currentPhase ? `Active: ${currentPhase}` : 'Idle'}
        </span>
      </div>

      <div className="relative">
        {/* Progress Line */}
        <div className="absolute top-8 left-0 right-0 h-1 bg-slate-200 dark:bg-slate-700 rounded" />
        <div
          className="absolute top-8 left-0 h-1 bg-gradient-to-r from-purple-500 via-blue-500 to-green-500 rounded transition-all duration-500"
          style={{ width: `${(completedPhases.length / PHASES.length) * 100}%` }}
        />

        {/* Phase Nodes */}
        <div className="relative flex justify-between">
          {PHASES.map((phase) => {
            const isActive = currentPhase === phase.id;
            const isCompleted = completedPhases.includes(phase.id);
            const isPending = !isActive && !isCompleted;

            return (
              <div key={phase.id} className="flex flex-col items-center w-20">
                <div
                  className={clsx(
                    'w-16 h-16 rounded-full flex items-center justify-center text-2xl transition-all duration-300',
                    isActive && 'ring-4 ring-offset-2 ring-offset-white dark:ring-offset-slate-900 animate-pulse',
                    isCompleted && 'scale-90',
                    isPending && 'opacity-40'
                  )}
                  style={{
                    backgroundColor: isCompleted || isActive ? phaseColors[phase.id] : 'rgba(100, 116, 139, 0.2)',
                    boxShadow: isActive ? `0 0 20px ${phaseColors[phase.id]}` : 'none',
                    '--tw-ring-color': isActive ? phaseColors[phase.id] : undefined,
                  } as React.CSSProperties}
                >
                  {isCompleted ? '✓' : phase.icon}
                </div>
                <span className={clsx(
                  'mt-3 text-xs font-medium text-center',
                  isActive ? 'text-slate-900 dark:text-slate-100' : 'text-slate-500'
                )}>
                  {phase.name}
                </span>
                <span className="text-xs text-slate-400 text-center mt-1 hidden lg:block">
                  {phase.description}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </GlassPanel>
  );
}
