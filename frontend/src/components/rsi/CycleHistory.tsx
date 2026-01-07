import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

export function CycleHistory() {
  const { getRSIMetrics } = useByrdAPI();
  const [cycles, setCycles] = useState<any[]>([]);

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
    <GlassPanel glow="none" padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Cycle History
      </h2>

      {cycles.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          No cycles recorded yet.
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-700">
                <th className="text-left py-2 px-3 text-slate-500 font-medium">Cycle</th>
                <th className="text-left py-2 px-3 text-slate-500 font-medium">Phase Reached</th>
                <th className="text-left py-2 px-3 text-slate-500 font-medium">Domain</th>
                <th className="text-left py-2 px-3 text-slate-500 font-medium">Desires</th>
                <th className="text-left py-2 px-3 text-slate-500 font-medium">Practice</th>
                <th className="text-left py-2 px-3 text-slate-500 font-medium">Heuristic</th>
                <th className="text-left py-2 px-3 text-slate-500 font-medium">Time</th>
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
    </GlassPanel>
  );
}

function CycleRow({ cycle }: { cycle: any }) {
  const phaseColors: Record<string, string> = {
    reflect: 'text-purple-600',
    verify: 'text-indigo-600',
    collapse: 'text-pink-600',
    route: 'text-amber-600',
    practice: 'text-green-600',
    record: 'text-blue-600',
    crystallize: 'text-cyan-600',
    measure: 'text-lime-600',
  };

  return (
    <tr className="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50">
      <td className="py-2 px-3 font-mono text-xs">
        {cycle.cycle_id?.split('_').pop() || '-'}
      </td>
      <td className="py-2 px-3">
        <span className={clsx('font-medium capitalize', phaseColors[cycle.phase_reached] || 'text-slate-600')}>
          {cycle.phase_reached || '-'}
        </span>
      </td>
      <td className="py-2 px-3">
        {cycle.domain ? (
          <span className="px-2 py-0.5 rounded text-xs bg-slate-100 dark:bg-slate-800">
            {cycle.domain}
          </span>
        ) : (
          <span className="text-slate-400">-</span>
        )}
      </td>
      <td className="py-2 px-3">
        <span className="text-green-600">{cycle.desires_verified || 0}</span>
        <span className="text-slate-400">/</span>
        <span className="text-slate-600">{cycle.desires_generated || 0}</span>
      </td>
      <td className="py-2 px-3">
        {cycle.practice_attempted ? (
          <span className={cycle.practice_succeeded ? 'text-green-600' : 'text-red-500'}>
            {cycle.practice_succeeded ? '✓' : '✗'}
          </span>
        ) : (
          <span className="text-slate-400">-</span>
        )}
      </td>
      <td className="py-2 px-3">
        {cycle.heuristic_crystallized ? (
          <span className="text-cyan-600" title={cycle.heuristic_crystallized}>
            💎
          </span>
        ) : (
          <span className="text-slate-400">-</span>
        )}
      </td>
      <td className="py-2 px-3 text-slate-500 text-xs">
        {formatTime(cycle.completed_at)}
      </td>
    </tr>
  );
}

function formatTime(timestamp: string): string {
  if (!timestamp) return '-';
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
