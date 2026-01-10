/**
 * EmergenceMetrics - Observatory Style Emergence Monitor
 */

import { useEffect, useState } from 'react';
import { ObservatoryPanel, MetricReadout } from '../common/ObservatoryPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

interface RSIMetricsData {
  activation_rate?: number;
  trajectory_success_rate?: number;
  direction_variance?: number;
  emergent_desires?: number;
  trajectories_stored?: number;
  heuristics_crystallized?: number;
  domain_distribution?: Record<string, number>;
}

export function EmergenceMetrics() {
  const { getRSIMetrics } = useByrdAPI();
  const [rsiMetrics, setRsiMetrics] = useState<RSIMetricsData>({});

  useEffect(() => {
    const fetchMetrics = async () => {
      const result = await getRSIMetrics();
      if (result) {
        // The API may return rsi_metrics or direct metrics
        const metricsData = (result as unknown as { rsi_metrics?: RSIMetricsData }).rsi_metrics || {};
        setRsiMetrics(metricsData);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, [getRSIMetrics]);

  const activationRate = rsiMetrics.activation_rate || 0;

  return (
    <ObservatoryPanel
      title="EMERGENCE METRICS"
      status={activationRate > 0.5 ? 'nominal' : activationRate > 0 ? 'caution' : 'inactive'}
      padding="lg"
    >
      <div className="space-y-4">
        {/* Key Metrics Bars */}
        <EmergenceBar
          label="ACTIVATION RATE"
          value={rsiMetrics.activation_rate || 0}
          color="var(--status-nominal)"
          description="Rate of emergent desire activation"
        />
        <EmergenceBar
          label="TRAJECTORY SUCCESS"
          value={rsiMetrics.trajectory_success_rate || 0}
          color="var(--data-stream)"
          description="Practice trajectory success rate"
        />
        <EmergenceBar
          label="DIRECTION VARIANCE"
          value={Math.min(1, (rsiMetrics.direction_variance || 0) * 2)}
          color="var(--cat-eye-gold)"
          description="Diversity of improvement directions"
        />

        {/* Counts */}
        <div className="pt-4 border-t border-[var(--obs-border)]">
          <div className="grid grid-cols-3 gap-4 text-center">
            <MetricReadout
              label="DESIRES"
              value={rsiMetrics.emergent_desires?.toString() || '0'}
              size="md"
              status="nominal"
            />
            <MetricReadout
              label="TRAJECTORIES"
              value={rsiMetrics.trajectories_stored?.toString() || '0'}
              size="md"
            />
            <MetricReadout
              label="HEURISTICS"
              value={rsiMetrics.heuristics_crystallized?.toString() || '0'}
              size="md"
              status={
                (rsiMetrics.heuristics_crystallized || 0) > 0 ? 'nominal' : undefined
              }
            />
          </div>
        </div>

        {/* Domain Distribution */}
        {rsiMetrics.domain_distribution &&
          Object.keys(rsiMetrics.domain_distribution).length > 0 && (
            <div className="pt-4 border-t border-[var(--obs-border)]">
              <span className="obs-label text-[9px] text-[var(--obs-text-tertiary)]">
                DOMAIN DISTRIBUTION
              </span>
              <div className="flex gap-2 mt-2 flex-wrap">
                {Object.entries(rsiMetrics.domain_distribution).map(
                  ([domain, count]) => (
                    <DomainBadge key={domain} domain={domain} count={count} />
                  )
                )}
              </div>
            </div>
          )}
      </div>
    </ObservatoryPanel>
  );
}

interface EmergenceBarProps {
  label: string;
  value: number;
  color: string;
  description: string;
}

function EmergenceBar({ label, value, color, description }: EmergenceBarProps) {
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">{label}</span>
        <span className="obs-metric text-sm" style={{ color }}>
          {(value * 100).toFixed(1)}%
        </span>
      </div>
      <div className="h-2 bg-[var(--obs-bg-elevated)] rounded-full overflow-hidden">
        <div
          className="h-full transition-all duration-500"
          style={{
            width: `${Math.min(100, value * 100)}%`,
            backgroundColor: color,
            boxShadow: value > 0.5 ? `0 0 8px ${color}` : 'none',
          }}
        />
      </div>
      <p className="text-[9px] text-[var(--obs-text-tertiary)] mt-1">{description}</p>
    </div>
  );
}

function DomainBadge({ domain, count }: { domain: string; count: number }) {
  const domainColors: Record<string, string> = {
    code: 'var(--rsi-practice)',
    math: 'var(--status-nominal)',
    logic: 'var(--rsi-reflect)',
    planning: 'var(--cat-eye-gold)',
    creative: 'var(--rsi-collapse)',
  };

  const color = domainColors[domain] || 'var(--obs-text-tertiary)';

  return (
    <span
      className="obs-label text-[10px] px-2 py-1 rounded"
      style={{
        backgroundColor: `color-mix(in srgb, ${color} 20%, transparent)`,
        color: color,
        border: `1px solid ${color}40`,
      }}
    >
      {domain.toUpperCase()}: {count}
    </span>
  );
}

export default EmergenceMetrics;
