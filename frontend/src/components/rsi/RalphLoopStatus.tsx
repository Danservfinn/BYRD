import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

export function RalphLoopStatus() {
  const { getRalphLoopStatus } = useByrdAPI();
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      const result = await getRalphLoopStatus();
      if (result) setStatus(result);
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, [getRalphLoopStatus]);

  return (
    <GlassPanel glow="purple" padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Ralph Loop
      </h2>

      <div className="space-y-4">
        {/* Status Indicator */}
        <div className="flex items-center gap-3">
          <span className={`w-3 h-3 rounded-full ${status?.running ? 'bg-green-500 animate-pulse' : 'bg-slate-400'}`} />
          <span className="text-slate-700 dark:text-slate-300">
            {status?.running ? 'Running' : 'Stopped'}
          </span>
        </div>

        {/* Statistics Grid */}
        <div className="grid grid-cols-2 gap-4">
          <StatItem label="Iterations" value={status?.iterations_completed || 0} />
          <StatItem label="Total Time" value={formatDuration(status?.total_time_seconds || 0)} />
          <StatItem label="Tokens Used" value={formatNumber(status?.total_tokens || 0)} />
          <StatItem label="Cost" value={`$${(status?.total_cost_usd || 0).toFixed(2)}`} />
        </div>

        {/* Emergence Confidence */}
        <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-slate-500">Emergence Confidence</span>
            <span className="text-sm font-medium text-slate-900 dark:text-slate-100">
              {((status?.last_emergence?.confidence || 0) * 100).toFixed(1)}%
            </span>
          </div>
          <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
              style={{ width: `${(status?.last_emergence?.confidence || 0) * 100}%` }}
            />
          </div>
        </div>

        {/* Termination Reason (if stopped) */}
        {status?.terminated && (
          <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
            <span className="text-xs text-slate-500 uppercase tracking-wide">
              Termination Reason
            </span>
            <p className="text-sm text-slate-700 dark:text-slate-300 mt-1">
              {formatTerminationReason(status?.reason)}
            </p>
          </div>
        )}
      </div>
    </GlassPanel>
  );
}

function StatItem({ label, value }: { label: string; value: string | number }) {
  return (
    <div>
      <div className="text-xs text-slate-500 uppercase tracking-wide">{label}</div>
      <div className="text-lg font-semibold text-slate-900 dark:text-slate-100">{value}</div>
    </div>
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
