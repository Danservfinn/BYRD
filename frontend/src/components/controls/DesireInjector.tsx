import { useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface InjectedDesire {
  id: string;
  description: string;
  urgency: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  injected_at: string;
}

export function DesireInjector() {
  const { injectDesire } = useByrdAPI();
  const [description, setDescription] = useState('');
  const [urgency, setUrgency] = useState(0.5);
  const [injecting, setInjecting] = useState(false);
  const [recentDesires, setRecentDesires] = useState<InjectedDesire[]>([]);

  const handleInject = async () => {
    if (!description.trim() || injecting) return;

    setInjecting(true);
    try {
      const result = await injectDesire(description, urgency);
      if (result?.desire) {
        setRecentDesires(prev => [result.desire, ...prev].slice(0, 5));
        setDescription('');
        setUrgency(0.5);
      }
    } finally {
      setInjecting(false);
    }
  };

  const statusColors: Record<string, string> = {
    pending: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
    processing: 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400',
    completed: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
    failed: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400',
  };

  return (
    <GlassPanel glow="amber" padding="lg" className="h-full">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Desire Injector
      </h2>

      <p className="text-sm text-slate-500 mb-3">
        Inject desires for BYRD to discover strategies for achieving.
      </p>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
            Desire Description
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="What should BYRD work towards? (e.g., 'Improve code review accuracy')"
            className="w-full h-20 p-3 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 resize-none focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
            Urgency: {(urgency * 100).toFixed(0)}%
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={urgency}
            onChange={(e) => setUrgency(parseFloat(e.target.value))}
            className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-amber-500"
          />
          <div className="flex justify-between text-xs text-slate-500 mt-1">
            <span>Low</span>
            <span>Medium</span>
            <span>High</span>
          </div>
        </div>

        <button
          onClick={handleInject}
          disabled={!description.trim() || injecting}
          className={clsx(
            'w-full px-4 py-2 rounded-lg font-medium text-white transition-colors',
            !description.trim() || injecting
              ? 'bg-slate-400 cursor-not-allowed'
              : 'bg-amber-600 hover:bg-amber-700'
          )}
        >
          {injecting ? 'Injecting...' : 'Inject Desire'}
        </button>
      </div>

      {/* Recent injections */}
      {recentDesires.length > 0 && (
        <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
          <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            Recent Injections
          </h3>
          <div className="space-y-2">
            {recentDesires.map((desire) => (
              <div
                key={desire.id}
                className="p-2 rounded bg-white/50 dark:bg-slate-800/50 text-sm"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-slate-700 dark:text-slate-300 line-clamp-1">
                    {desire.description}
                  </span>
                  <span className={clsx(
                    'px-1.5 py-0.5 rounded text-xs font-medium capitalize',
                    statusColors[desire.status]
                  )}>
                    {desire.status}
                  </span>
                </div>
                <div className="text-xs text-slate-500">
                  Urgency: {(desire.urgency * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </GlassPanel>
  );
}
