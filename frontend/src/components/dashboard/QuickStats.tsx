import { useEffect, useState } from 'react';
import { StatCard } from '../common/StatCard';
import { useByrdAPI } from '../../hooks/useByrdAPI';

export function QuickStats() {
  const { getRSIMetrics, getRalphLoopStatus } = useByrdAPI();
  const [metrics, setMetrics] = useState<any>(null);
  const [loopStatus, setLoopStatus] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      const [metricsResult, loopResult] = await Promise.all([
        getRSIMetrics(),
        getRalphLoopStatus(),
      ]);
      if (metricsResult) setMetrics(metricsResult);
      if (loopResult) setLoopStatus(loopResult);
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, [getRSIMetrics, getRalphLoopStatus]);

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard
        label="RSI Cycles"
        value={metrics?.rsi_metrics?.complete_cycles || 0}
        icon="🔄"
        color="blue"
        trend={metrics?.rsi_metrics?.complete_cycles > 0 ? { value: 12, direction: 'up' } : undefined}
      />
      <StatCard
        label="Ralph Iterations"
        value={loopStatus?.iterations_completed || 0}
        icon="🔁"
        color="purple"
      />
      <StatCard
        label="Emergence Rate"
        value={`${((metrics?.rsi_metrics?.activation_rate || 0) * 100).toFixed(1)}%`}
        icon="✨"
        color="amber"
        trend={metrics?.rsi_metrics?.activation_rate > 0.5 ? { value: 5, direction: 'up' } : undefined}
      />
      <StatCard
        label="Heuristics"
        value={metrics?.rsi_metrics?.heuristics_crystallized || 0}
        icon="💎"
        color="green"
      />
    </div>
  );
}
