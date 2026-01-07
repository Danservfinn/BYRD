import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface AnchoringRequest {
  id: string;
  type: 'spot_check' | 'calibration' | 'override' | 'approval';
  priority: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  context: string;
  created_at: string;
  expires_at: string | null;
}

export function HumanAnchoringQueue() {
  const { getHumanAnchoringQueue, submitAnchoringResponse } = useByrdAPI();
  const [queue, setQueue] = useState<AnchoringRequest[]>([]);
  const [responding, setResponding] = useState<string | null>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getHumanAnchoringQueue();
      if (result?.queue) setQueue(result.queue);
    };
    fetch();
    const interval = setInterval(fetch, 5000);
    return () => clearInterval(interval);
  }, [getHumanAnchoringQueue]);

  const handleResponse = async (id: string, approved: boolean) => {
    setResponding(id);
    try {
      await submitAnchoringResponse(id, approved);
      setQueue(prev => prev.filter(r => r.id !== id));
    } finally {
      setResponding(null);
    }
  };

  const priorityColors: Record<string, string> = {
    low: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
    medium: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
    high: 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400',
    critical: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400',
  };

  const typeIcons: Record<string, string> = {
    spot_check: '🔍',
    calibration: '⚖️',
    override: '🔓',
    approval: '✓',
  };

  return (
    <GlassPanel glow="blue" padding="lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Human Anchoring Queue
        </h2>
        <span className="text-sm text-slate-500">
          {queue.length} pending
        </span>
      </div>

      {queue.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          No pending anchoring requests.
        </div>
      ) : (
        <div className="space-y-3">
          {queue.map((request) => (
            <div
              key={request.id}
              className="p-4 rounded-lg bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{typeIcons[request.type]}</span>
                  <div>
                    <span className="font-medium text-slate-900 dark:text-slate-100 capitalize">
                      {request.type.replace('_', ' ')}
                    </span>
                    <span className={clsx(
                      'ml-2 px-2 py-0.5 rounded text-xs font-medium capitalize',
                      priorityColors[request.priority]
                    )}>
                      {request.priority}
                    </span>
                  </div>
                </div>
                <span className="text-xs text-slate-500">
                  {new Date(request.created_at).toLocaleTimeString()}
                </span>
              </div>

              <p className="text-sm text-slate-700 dark:text-slate-300 mb-2">
                {request.description}
              </p>

              {request.context && (
                <div className="text-xs text-slate-500 bg-slate-100 dark:bg-slate-800 rounded p-2 mb-3 font-mono">
                  {request.context}
                </div>
              )}

              <div className="flex items-center justify-end gap-2">
                <button
                  onClick={() => handleResponse(request.id, false)}
                  disabled={responding === request.id}
                  className="px-3 py-1.5 text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors disabled:opacity-50"
                >
                  Reject
                </button>
                <button
                  onClick={() => handleResponse(request.id, true)}
                  disabled={responding === request.id}
                  className="px-3 py-1.5 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded transition-colors disabled:opacity-50"
                >
                  Approve
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </GlassPanel>
  );
}
