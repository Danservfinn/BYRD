/**
 * CycleHistory - Observatory Style RSI Cycle Log
 */

import { useEffect, useState } from 'react';
import { ObservatoryPanel } from '../common/ObservatoryPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

interface Cycle {
  cycle_id?: string;
  phase_reached?: string;
  domain?: string;
  desires_generated?: number;
  desires_verified?: number;
  practice_attempted?: boolean;
  practice_succeeded?: boolean;
  heuristic_crystallized?: string;
  completed_at?: string;
}

export function CycleHistory() {
  const { getRSIMetrics } = useByrdAPI();
  const [cycles, setCycles] = useState<Cycle[]>([]);

  useEffect(() => {
    const fetchCycles = async () => {
      const result = await getRSIMetrics();
      if (result?.recent_cycles) {
        setCycles(result.recent_cycles);
      }
    };

    fetchCycles();
    const interval = setInterval(fetchCycles, 5000);
    return () => clearInterval(interval);
  }, [getRSIMetrics]);

  return (
    <ObservatoryPanel title="CYCLE HISTORY" padding="md">
      {cycles.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <div className="w-12 h-12 rounded-full bg-[var(--obs-bg-elevated)] flex items-center justify-center mb-3">
            <span className="text-2xl opacity-30">◯</span>
          </div>
          <p className="obs-label text-[var(--obs-text-tertiary)]">
            NO CYCLES RECORDED
          </p>
          <p className="text-xs text-[var(--obs-text-tertiary)] mt-1 opacity-60">
            Start an RSI cycle to see history
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto scrollbar-thin">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[var(--obs-border)]">
                <th className="obs-label text-[9px] text-left py-2 px-3 text-[var(--obs-text-tertiary)]">
                  CYCLE
                </th>
                <th className="obs-label text-[9px] text-left py-2 px-3 text-[var(--obs-text-tertiary)]">
                  PHASE
                </th>
                <th className="obs-label text-[9px] text-left py-2 px-3 text-[var(--obs-text-tertiary)]">
                  DOMAIN
                </th>
                <th className="obs-label text-[9px] text-left py-2 px-3 text-[var(--obs-text-tertiary)]">
                  DESIRES
                </th>
                <th className="obs-label text-[9px] text-left py-2 px-3 text-[var(--obs-text-tertiary)]">
                  PRACTICE
                </th>
                <th className="obs-label text-[9px] text-left py-2 px-3 text-[var(--obs-text-tertiary)]">
                  HEURISTIC
                </th>
                <th className="obs-label text-[9px] text-left py-2 px-3 text-[var(--obs-text-tertiary)]">
                  TIME
                </th>
              </tr>
            </thead>
            <tbody>
              {cycles.map((cycle, index) => (
                <CycleRow key={cycle.cycle_id || index} cycle={cycle} />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </ObservatoryPanel>
  );
}

function CycleRow({ cycle }: { cycle: Cycle }) {
  const phaseColor = cycle.phase_reached
    ? `var(--rsi-${cycle.phase_reached})`
    : 'var(--obs-text-tertiary)';

  return (
    <tr className="border-b border-[var(--obs-border)]/50 hover:bg-[var(--obs-bg-elevated)] transition-colors">
      <td className="py-2 px-3 font-mono text-xs text-[var(--obs-text-secondary)]">
        {cycle.cycle_id?.split('_').pop()?.slice(-6) || '-'}
      </td>
      <td className="py-2 px-3">
        <span
          className="obs-label text-[10px] uppercase"
          style={{ color: phaseColor }}
        >
          {cycle.phase_reached || '-'}
        </span>
      </td>
      <td className="py-2 px-3">
        {cycle.domain ? (
          <span className="obs-label text-[9px] px-2 py-0.5 rounded bg-[var(--obs-bg-elevated)] text-[var(--obs-text-secondary)]">
            {cycle.domain.toUpperCase()}
          </span>
        ) : (
          <span className="text-[var(--obs-text-tertiary)]">-</span>
        )}
      </td>
      <td className="py-2 px-3">
        <span className="text-[var(--status-nominal)]">
          {cycle.desires_verified || 0}
        </span>
        <span className="text-[var(--obs-text-tertiary)]">/</span>
        <span className="text-[var(--obs-text-secondary)]">
          {cycle.desires_generated || 0}
        </span>
      </td>
      <td className="py-2 px-3">
        {cycle.practice_attempted ? (
          <span
            className={
              cycle.practice_succeeded
                ? 'text-[var(--status-nominal)]'
                : 'text-[var(--status-critical)]'
            }
          >
            {cycle.practice_succeeded ? '✓' : '✗'}
          </span>
        ) : (
          <span className="text-[var(--obs-text-tertiary)]">-</span>
        )}
      </td>
      <td className="py-2 px-3">
        {cycle.heuristic_crystallized ? (
          <span
            className="text-[var(--rsi-crystallize)]"
            title={cycle.heuristic_crystallized}
          >
            💎
          </span>
        ) : (
          <span className="text-[var(--obs-text-tertiary)]">-</span>
        )}
      </td>
      <td className="py-2 px-3 text-[var(--obs-text-tertiary)] text-xs font-mono">
        {formatTime(cycle.completed_at)}
      </td>
    </tr>
  );
}

function formatTime(timestamp?: string): string {
  if (!timestamp) return '-';
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export default CycleHistory;
