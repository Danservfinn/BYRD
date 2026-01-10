/**
 * RalphLoopStatus - Observatory Style Ralph Loop Monitor
 */

import { useEffect, useState } from 'react';
import { ObservatoryPanel, MetricReadout, StatusIndicator } from '../common/ObservatoryPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

export function RalphLoopStatus() {
  const { getRalphLoopStatus } = useByrdAPI();
  const [status, setStatus] = useState<{
    running?: boolean;
    iterations_completed?: number;
    total_time_seconds?: number;
    total_tokens?: number;
    total_cost_usd?: number;
    last_emergence?: { confidence?: number };
    terminated?: boolean;
    reason?: string;
  } | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      const result = await getRalphLoopStatus();
      if (result) setStatus(result);
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, [getRalphLoopStatus]);

  const panelStatus = status?.running ? 'nominal' : status?.terminated ? 'caution' : 'inactive';

  return (
    <ObservatoryPanel title="RALPH LOOP" status={panelStatus} padding="lg">
      <div className="space-y-4">
        {/* Status Indicator */}
        <div className="flex items-center justify-between">
          <StatusIndicator
            status={status?.running ? 'nominal' : 'inactive'}
            label={status?.running ? 'RUNNING' : 'STOPPED'}
            size="md"
          />
          {status?.terminated && (
            <span className="obs-label text-[9px] px-2 py-1 rounded bg-[var(--status-caution)]/20 text-[var(--status-caution)]">
              TERMINATED
            </span>
          )}
        </div>

        {/* Statistics Grid */}
        <div className="grid grid-cols-2 gap-4">
          <MetricReadout
            label="ITERATIONS"
            value={status?.iterations_completed?.toString() || '0'}
            size="md"
            status={status?.running ? 'nominal' : 'inactive'}
          />
          <MetricReadout
            label="RUNTIME"
            value={formatDuration(status?.total_time_seconds || 0)}
            size="md"
          />
          <MetricReadout
            label="TOKENS"
            value={formatNumber(status?.total_tokens || 0)}
            size="md"
          />
          <MetricReadout
            label="COST"
            value={`$${(status?.total_cost_usd || 0).toFixed(2)}`}
            size="md"
            status={(status?.total_cost_usd || 0) > 10 ? 'caution' : undefined}
          />
        </div>

        {/* Emergence Confidence */}
        <div className="pt-4 border-t border-[var(--obs-border)]">
          <div className="flex items-center justify-between mb-2">
            <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">
              EMERGENCE CONFIDENCE
            </span>
            <span className="obs-metric text-sm" style={{ color: 'var(--cat-eye-gold)' }}>
              {((status?.last_emergence?.confidence || 0) * 100).toFixed(1)}%
            </span>
          </div>
          <div className="h-2 bg-[var(--obs-bg-elevated)] rounded-full overflow-hidden">
            <div
              className="h-full transition-all duration-500"
              style={{
                width: `${(status?.last_emergence?.confidence || 0) * 100}%`,
                background: `linear-gradient(90deg, var(--rsi-reflect), var(--cat-eye-gold))`,
              }}
            />
          </div>
        </div>

        {/* Termination Reason (if stopped) */}
        {status?.terminated && status?.reason && (
          <div className="pt-4 border-t border-[var(--obs-border)]">
            <span className="obs-label text-[9px] text-[var(--obs-text-tertiary)]">
              TERMINATION REASON
            </span>
            <p className="text-xs text-[var(--obs-text-secondary)] mt-1">
              {formatTerminationReason(status.reason)}
            </p>
          </div>
        )}
      </div>
    </ObservatoryPanel>
  );
}

function formatDuration(seconds: number): string {
  if (seconds < 60) return `${Math.floor(seconds)}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
}

function formatNumber(num: number): string {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return num.toString();
}

function formatTerminationReason(reason: string): string {
  const reasons: Record<string, string> = {
    emergence_detected: 'Genuine emergence detected',
    max_iterations: 'Maximum iterations reached',
    max_cost: 'Cost limit exceeded',
    max_time: 'Time limit exceeded',
    error: 'Error occurred',
    manual_stop: 'Manually stopped',
  };
  return reasons[reason] || reason;
}

export default RalphLoopStatus;
