import { useEffect, useState } from 'react';
import { StatCard } from '../common/StatCard';
import { useByrdAPI } from '../../hooks/useByrdAPI';

export function QuickStats() {
  const { getRSIMetrics } = useByrdAPI();
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const metricsResult = await getRSIMetrics();
        if (metricsResult) setMetrics(metricsResult);
      } catch (error) {
        console.error('Failed to fetch metrics:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, [getRSIMetrics]);

  const displayCycles = metrics?.cycle_number || metrics?.rsi_metrics?.complete_cycles || 0;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard
        label="RSI Cycles"
        value={displayCycles}
        icon="🔄"
        color="blue"
        trend={displayCycles > 0 ? { value: 12, direction: 'up' } : undefined}
      />
      <StatCard
        label="Memory Nodes"
        value={metrics?.memory_nodes || 0}
        icon="🧠"
        color="purple"
      />
      <StatCard
        label="Capabilities"
        value={metrics?.capabilities || 0}
        icon="🎯"
        color="amber"
      />
      <StatCard
        label="Desires Processed"
        value={metrics?.desires_processed || 0}
        icon="✨"
        color="green"
      />
    </div>
  );
}
