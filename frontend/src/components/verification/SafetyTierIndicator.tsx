import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface SafetyStatus {
  current_tier: 'green' | 'yellow' | 'orange' | 'red';
  tier_confidence: number;
  active_constraints: string[];
  recent_violations: number;
  last_assessment: string;
}

const TIERS = [
  { id: 'green', label: 'Safe', description: 'All constraints satisfied' },
  { id: 'yellow', label: 'Caution', description: 'Minor concerns detected' },
  { id: 'orange', label: 'Warning', description: 'Elevated risk level' },
  { id: 'red', label: 'Critical', description: 'Immediate attention required' },
] as const;

export function SafetyTierIndicator() {
  const { getVerificationStatus } = useByrdAPI();
  const [status, setStatus] = useState<SafetyStatus | null>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getVerificationStatus();
      if (result?.safety) setStatus(result.safety);
    };
    fetch();
    const interval = setInterval(fetch, 5000);
    return () => clearInterval(interval);
  }, [getVerificationStatus]);

  const tierColors: Record<string, string> = {
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    orange: 'bg-orange-500',
    red: 'bg-red-500',
  };

  const tierBgColors: Record<string, string> = {
    green: 'bg-green-50 dark:bg-green-900/20',
    yellow: 'bg-yellow-50 dark:bg-yellow-900/20',
    orange: 'bg-orange-50 dark:bg-orange-900/20',
    red: 'bg-red-50 dark:bg-red-900/20',
  };

  const currentTier = status?.current_tier || 'green';
  const currentTierIndex = TIERS.findIndex(t => t.id === currentTier);

  return (
    <GlassPanel glow={currentTier === 'green' ? 'green' : currentTier === 'red' ? 'red' : 'amber'} padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Safety Tier
      </h2>

      {/* Tier indicator */}
      <div className={clsx('rounded-lg p-4 mb-4', tierBgColors[currentTier])}>
        <div className="flex items-center gap-3">
          <div className={clsx('w-4 h-4 rounded-full', tierColors[currentTier], currentTier !== 'green' && 'animate-pulse')} />
          <div>
            <div className="text-xl font-bold text-slate-900 dark:text-slate-100">
              {TIERS[currentTierIndex].label}
            </div>
            <div className="text-sm text-slate-500">
              {TIERS[currentTierIndex].description}
            </div>
          </div>
        </div>
      </div>

      {/* Tier progression */}
      <div className="flex items-center gap-1 mb-4">
        {TIERS.map((tier, i) => (
          <div
            key={tier.id}
            className={clsx(
              'flex-1 h-2 rounded-full transition-colors',
              i <= currentTierIndex ? tierColors[tier.id] : 'bg-slate-200 dark:bg-slate-700'
            )}
          />
        ))}
      </div>

      {/* Details */}
      <div className="space-y-3 text-sm">
        <div className="flex justify-between">
          <span className="text-slate-500">Confidence</span>
          <span className="font-medium text-slate-900 dark:text-slate-100">
            {((status?.tier_confidence || 0) * 100).toFixed(0)}%
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-500">Recent Violations</span>
          <span className={clsx(
            'font-medium',
            (status?.recent_violations || 0) === 0 ? 'text-green-600' : 'text-red-500'
          )}>
            {status?.recent_violations || 0}
          </span>
        </div>

        {status?.active_constraints && status.active_constraints.length > 0 && (
          <div>
            <span className="text-slate-500">Active Constraints</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {status.active_constraints.slice(0, 4).map((c, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 bg-slate-100 dark:bg-slate-800 rounded text-xs"
                >
                  {c}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </GlassPanel>
  );
}
