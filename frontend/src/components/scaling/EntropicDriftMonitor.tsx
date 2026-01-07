import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface DriftMetrics {
  solution_diversity: number;
  benchmark_trend: number;
  strategy_entropy: number;
  generalization_gap: number;
  overall_severity: 'none' | 'minor' | 'moderate' | 'severe' | 'critical';
  recommendations: string[];
}

export function EntropicDriftMonitor() {
  const { getScalingMetrics } = useByrdAPI();
  const [drift, setDrift] = useState<DriftMetrics | null>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getScalingMetrics();
      if (result?.entropic_drift) setDrift(result.entropic_drift);
    };
    fetch();
    const interval = setInterval(fetch, 5000);
    return () => clearInterval(interval);
  }, [getScalingMetrics]);

  const severityColors: Record<string, string> = {
    none: 'text-green-600 bg-green-100 dark:bg-green-900/30',
    minor: 'text-blue-600 bg-blue-100 dark:bg-blue-900/30',
    moderate: 'text-amber-600 bg-amber-100 dark:bg-amber-900/30',
    severe: 'text-orange-600 bg-orange-100 dark:bg-orange-900/30',
    critical: 'text-red-600 bg-red-100 dark:bg-red-900/30',
  };

  const metricLabels = [
    { key: 'solution_diversity', label: 'Solution Diversity', color: 'purple' },
    { key: 'benchmark_trend', label: 'Benchmark Trend', color: 'blue' },
    { key: 'strategy_entropy', label: 'Strategy Entropy', color: 'amber' },
    { key: 'generalization_gap', label: 'Generalization Gap', color: 'red' },
  ] as const;

  const getMetricColor = (value: number, key: string) => {
    // Higher is worse for generalization_gap, lower is worse for others
    if (key === 'generalization_gap') {
      return value > 0.3 ? 'text-red-500' : value > 0.15 ? 'text-amber-500' : 'text-green-500';
    }
    return value < 0.3 ? 'text-red-500' : value < 0.5 ? 'text-amber-500' : 'text-green-500';
  };

  return (
    <GlassPanel glow="red" padding="lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Entropic Drift
        </h2>
        {drift && (
          <span className={clsx(
            'px-2 py-0.5 rounded text-xs font-medium capitalize',
            severityColors[drift.overall_severity]
          )}>
            {drift.overall_severity}
          </span>
        )}
      </div>

      {!drift ? (
        <div className="text-center py-8 text-slate-400">
          No drift data available.
        </div>
      ) : (
        <div className="space-y-4">
          {/* Metric bars */}
          <div className="space-y-3">
            {metricLabels.map(({ key, label }) => {
              const value = drift[key as keyof DriftMetrics] as number;
              return (
                <div key={key}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-500">{label}</span>
                    <span className={clsx('font-medium', getMetricColor(value, key))}>
                      {(value * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className={clsx(
                        'h-full rounded-full transition-all',
                        key === 'generalization_gap'
                          ? value > 0.3 ? 'bg-red-500' : value > 0.15 ? 'bg-amber-500' : 'bg-green-500'
                          : value < 0.3 ? 'bg-red-500' : value < 0.5 ? 'bg-amber-500' : 'bg-green-500'
                      )}
                      style={{ width: `${value * 100}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          {/* Recommendations */}
          {drift.recommendations && drift.recommendations.length > 0 && (
            <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
              <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                Recommendations
              </h3>
              <ul className="space-y-1">
                {drift.recommendations.slice(0, 3).map((rec, i) => (
                  <li key={i} className="text-xs text-slate-500 flex items-start gap-2">
                    <span className="text-amber-500">!</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </GlassPanel>
  );
}
