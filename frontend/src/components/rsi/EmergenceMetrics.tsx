import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

export function EmergenceMetrics() {
  const { getRSIMetrics } = useByrdAPI();
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      const result = await getRSIMetrics();
      if (result) setMetrics(result);
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, [getRSIMetrics]);

  const rsiMetrics = metrics?.rsi_metrics || {};

  return (
    <GlassPanel glow="green" padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Emergence Metrics
      </h2>

      <div className="space-y-4">
        {/* Key Metrics */}
        <MetricBar
          label="Activation Rate"
          value={rsiMetrics.activation_rate || 0}
          color="green"
          description="Rate of emergent desire activation"
        />
        <MetricBar
          label="Trajectory Success"
          value={rsiMetrics.trajectory_success_rate || 0}
          color="blue"
          description="Practice trajectory success rate"
        />
        <MetricBar
          label="Direction Variance"
          value={Math.min(1, (rsiMetrics.direction_variance || 0) * 2)}
          color="amber"
          description="Diversity of improvement directions"
        />

        {/* Counts */}
        <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                {rsiMetrics.emergent_desires || 0}
              </div>
              <div className="text-xs text-slate-500">Desires</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                {rsiMetrics.trajectories_stored || 0}
              </div>
              <div className="text-xs text-slate-500">Trajectories</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                {rsiMetrics.heuristics_crystallized || 0}
              </div>
              <div className="text-xs text-slate-500">Heuristics</div>
            </div>
          </div>
        </div>

        {/* Domain Distribution */}
        {rsiMetrics.domain_distribution && Object.keys(rsiMetrics.domain_distribution).length > 0 && (
          <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
            <span className="text-xs text-slate-500 uppercase tracking-wide">
              Domain Distribution
            </span>
            <div className="flex gap-2 mt-2 flex-wrap">
              {Object.entries(rsiMetrics.domain_distribution).map(([domain, count]) => (
                <DomainBadge key={domain} domain={domain} count={count as number} />
              ))}
            </div>
          </div>
        )}
      </div>
    </GlassPanel>
  );
}

function MetricBar({
  label,
  value,
  color,
  description,
}: {
  label: string;
  value: number;
  color: 'green' | 'blue' | 'amber' | 'purple';
  description: string;
}) {
  const colorClasses = {
    green: 'from-green-400 to-green-600',
    blue: 'from-blue-400 to-blue-600',
    amber: 'from-amber-400 to-amber-600',
    purple: 'from-purple-400 to-purple-600',
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm text-slate-700 dark:text-slate-300">{label}</span>
        <span className="text-sm font-medium text-slate-900 dark:text-slate-100">
          {(value * 100).toFixed(1)}%
        </span>
      </div>
      <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
        <div
          className={`h-full bg-gradient-to-r ${colorClasses[color]} transition-all duration-500`}
          style={{ width: `${Math.min(100, value * 100)}%` }}
        />
      </div>
      <p className="text-xs text-slate-400 mt-1">{description}</p>
    </div>
  );
}

function DomainBadge({ domain, count }: { domain: string; count: number }) {
  const domainColors: Record<string, string> = {
    code: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
    math: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
    logic: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
    planning: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400',
    creative: 'bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-400',
  };

  return (
    <span
      className={`px-2 py-1 rounded text-xs font-medium ${domainColors[domain] || 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-400'}`}
    >
      {domain}: {count}
    </span>
  );
}
