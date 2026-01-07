import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface ExplosionPhase {
  current: 'dormant' | 'awakening' | 'accelerating' | 'explosive' | 'transcendent';
  progress: number;
  threshold: number;
  estimated_transition: string | null;
}

const PHASES = ['dormant', 'awakening', 'accelerating', 'explosive', 'transcendent'] as const;

export function ExplosionPhaseIndicator() {
  const { getScalingMetrics } = useByrdAPI();
  const [phase, setPhase] = useState<ExplosionPhase | null>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getScalingMetrics();
      if (result?.explosion_phase) setPhase(result.explosion_phase);
    };
    fetch();
    const interval = setInterval(fetch, 5000);
    return () => clearInterval(interval);
  }, [getScalingMetrics]);

  const currentIndex = PHASES.indexOf(phase?.current || 'dormant');

  const phaseColors: Record<string, string> = {
    dormant: 'bg-slate-400',
    awakening: 'bg-blue-500',
    accelerating: 'bg-amber-500',
    explosive: 'bg-orange-500',
    transcendent: 'bg-purple-500',
  };

  const phaseDescriptions: Record<string, string> = {
    dormant: 'System in learning mode',
    awakening: 'Initial capability emergence',
    accelerating: 'Rapid improvement phase',
    explosive: 'Exponential growth detected',
    transcendent: 'Beyond baseline metrics',
  };

  return (
    <GlassPanel glow="amber" padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Capability Explosion Phase
      </h2>

      <div className="space-y-4">
        {/* Phase progression */}
        <div className="flex items-center gap-1">
          {PHASES.map((p, i) => (
            <div key={p} className="flex-1 flex flex-col items-center">
              <div
                className={clsx(
                  'w-full h-2 rounded-full transition-colors',
                  i <= currentIndex ? phaseColors[p] : 'bg-slate-200 dark:bg-slate-700'
                )}
              />
              <span className={clsx(
                'text-xs mt-1 capitalize',
                i === currentIndex ? 'text-slate-900 dark:text-slate-100 font-medium' : 'text-slate-400'
              )}>
                {p}
              </span>
            </div>
          ))}
        </div>

        {/* Current phase details */}
        <div className="text-center py-4 border-t border-slate-200 dark:border-slate-700">
          <div className="text-2xl font-bold text-slate-900 dark:text-slate-100 capitalize">
            {phase?.current || 'dormant'}
          </div>
          <div className="text-sm text-slate-500 mt-1">
            {phaseDescriptions[phase?.current || 'dormant']}
          </div>
        </div>

        {/* Progress to next phase */}
        {phase && currentIndex < PHASES.length - 1 && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-500">Progress to next phase</span>
              <span className="font-medium text-slate-900 dark:text-slate-100">
                {((phase.progress / phase.threshold) * 100).toFixed(0)}%
              </span>
            </div>
            <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
              <div
                className={clsx('h-full rounded-full transition-all duration-500', phaseColors[PHASES[currentIndex + 1]])}
                style={{ width: `${Math.min((phase.progress / phase.threshold) * 100, 100)}%` }}
              />
            </div>
            {phase.estimated_transition && (
              <div className="text-xs text-slate-500 text-center">
                Estimated transition: {phase.estimated_transition}
              </div>
            )}
          </div>
        )}
      </div>
    </GlassPanel>
  );
}
