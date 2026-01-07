import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

export function GrowthRateGauge() {
  const { getScalingMetrics } = useByrdAPI();
  const [metrics, setMetrics] = useState<{
    current_rate: number;
    target_rate: number;
    trend: 'accelerating' | 'stable' | 'decelerating';
    history: number[];
  } | null>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getScalingMetrics();
      if (result?.growth) setMetrics(result.growth);
    };
    fetch();
    const interval = setInterval(fetch, 5000);
    return () => clearInterval(interval);
  }, [getScalingMetrics]);

  const rate = metrics?.current_rate || 0;
  const target = metrics?.target_rate || 1.0;
  const percentage = Math.min((rate / target) * 100, 100);

  const trendColors: Record<string, string> = {
    accelerating: 'text-green-600',
    stable: 'text-amber-600',
    decelerating: 'text-red-500',
  };

  const trendIcons: Record<string, string> = {
    accelerating: '↑',
    stable: '→',
    decelerating: '↓',
  };

  return (
    <GlassPanel glow="green" padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Growth Rate
      </h2>

      <div className="flex flex-col items-center py-4">
        {/* Gauge visualization */}
        <div className="relative w-40 h-20 overflow-hidden">
          <div className="absolute inset-0 border-8 border-slate-200 dark:border-slate-700 rounded-t-full" />
          <div
            className="absolute inset-0 border-8 border-green-500 rounded-t-full transition-all duration-500"
            style={{
              clipPath: `polygon(0 100%, 0 0, ${percentage}% 0, ${percentage}% 100%)`,
            }}
          />
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-4 h-4 bg-slate-900 dark:bg-white rounded-full" />
        </div>

        <div className="text-center mt-4">
          <div className="text-3xl font-bold text-slate-900 dark:text-slate-100">
            {(rate * 100).toFixed(1)}%
          </div>
          <div className="text-sm text-slate-500">
            of target ({(target * 100).toFixed(0)}%)
          </div>
        </div>

        {metrics?.trend && (
          <div className={clsx('flex items-center gap-1 mt-2', trendColors[metrics.trend])}>
            <span className="text-lg">{trendIcons[metrics.trend]}</span>
            <span className="text-sm capitalize">{metrics.trend}</span>
          </div>
        )}
      </div>

      {/* Mini sparkline */}
      {metrics?.history && metrics.history.length > 0 && (
        <div className="flex items-end h-8 gap-0.5 mt-4 border-t border-slate-200 dark:border-slate-700 pt-4">
          {metrics.history.slice(-20).map((value, i) => (
            <div
              key={i}
              className="flex-1 bg-green-500/50 rounded-t"
              style={{ height: `${value * 100}%` }}
            />
          ))}
        </div>
      )}
    </GlassPanel>
  );
}
