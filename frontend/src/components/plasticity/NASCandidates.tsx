import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface NASCandidate {
  id: string;
  architecture: string;
  fitness: number;
  generation: number;
  status: 'evaluating' | 'promising' | 'rejected' | 'selected';
  metrics: {
    accuracy: number;
    efficiency: number;
    novelty: number;
  };
}

export function NASCandidates() {
  const { getNASCandidates } = useByrdAPI();
  const [candidates, setCandidates] = useState<NASCandidate[]>([]);

  useEffect(() => {
    const fetch = async () => {
      const result = await getNASCandidates();
      if (result?.candidates) setCandidates(result.candidates);
    };
    fetch();
    const interval = setInterval(fetch, 5000);
    return () => clearInterval(interval);
  }, [getNASCandidates]);

  const statusIcons: Record<string, string> = {
    evaluating: '...',
    promising: '✨',
    rejected: '✗',
    selected: '✓',
  };

  const statusColors: Record<string, string> = {
    evaluating: 'text-amber-600',
    promising: 'text-purple-600',
    rejected: 'text-red-500',
    selected: 'text-green-600',
  };

  return (
    <GlassPanel glow="cyan" padding="lg" className="h-full">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Neural Architecture Search
        </h2>
        <span className="text-sm text-slate-500">
          Gen {candidates[0]?.generation || 0}
        </span>
      </div>

      {candidates.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          No NAS candidates being evaluated.
        </div>
      ) : (
        <div className="space-y-2 max-h-80 overflow-y-auto">
          {candidates.map((candidate) => (
            <div
              key={candidate.id}
              className="p-3 rounded-lg bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-sm text-slate-700 dark:text-slate-300">
                  {candidate.architecture}
                </span>
                <span className={clsx('font-medium', statusColors[candidate.status])}>
                  {statusIcons[candidate.status]}
                </span>
              </div>

              <div className="flex gap-4 text-xs">
                <div className="flex items-center gap-1">
                  <span className="text-slate-500">Fit:</span>
                  <span className="font-medium text-purple-600">
                    {(candidate.fitness * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex items-center gap-1">
                  <span className="text-slate-500">Acc:</span>
                  <span className="font-medium text-blue-600">
                    {(candidate.metrics.accuracy * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="flex items-center gap-1">
                  <span className="text-slate-500">Eff:</span>
                  <span className="font-medium text-green-600">
                    {(candidate.metrics.efficiency * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="flex items-center gap-1">
                  <span className="text-slate-500">Nov:</span>
                  <span className="font-medium text-amber-600">
                    {(candidate.metrics.novelty * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </GlassPanel>
  );
}
