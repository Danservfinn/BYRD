import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface CognitiveModule {
  id: string;
  name: string;
  type: 'core' | 'emergent' | 'composed';
  status: 'active' | 'dormant' | 'evolving';
  connections: number;
  performance: number;
  created_at: string;
}

export function ModuleRegistry() {
  const { getPlasticityModules } = useByrdAPI();
  const [modules, setModules] = useState<CognitiveModule[]>([]);

  useEffect(() => {
    const fetch = async () => {
      const result = await getPlasticityModules();
      if (result?.modules) setModules(result.modules);
    };
    fetch();
    const interval = setInterval(fetch, 10000);
    return () => clearInterval(interval);
  }, [getPlasticityModules]);

  const statusColors: Record<string, string> = {
    active: 'bg-green-500',
    dormant: 'bg-slate-400',
    evolving: 'bg-purple-500 animate-pulse',
  };

  const typeColors: Record<string, string> = {
    core: 'text-blue-600 dark:text-blue-400',
    emergent: 'text-purple-600 dark:text-purple-400',
    composed: 'text-cyan-600 dark:text-cyan-400',
  };

  return (
    <GlassPanel glow="purple" padding="lg" className="h-full">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Module Registry
        </h2>
        <span className="text-sm text-slate-500">
          {modules.length} modules
        </span>
      </div>

      {modules.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          No cognitive modules registered yet.
        </div>
      ) : (
        <div className="space-y-2 max-h-80 overflow-y-auto">
          {modules.map((module) => (
            <div
              key={module.id}
              className="p-3 rounded-lg bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className={clsx('w-2 h-2 rounded-full', statusColors[module.status])} />
                  <span className="font-medium text-slate-900 dark:text-slate-100">
                    {module.name}
                  </span>
                  <span className={clsx('text-xs capitalize', typeColors[module.type])}>
                    ({module.type})
                  </span>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <span className="text-slate-500">
                    {module.connections} links
                  </span>
                  <span className={clsx(
                    'font-medium',
                    module.performance >= 0.7 ? 'text-green-600' :
                    module.performance >= 0.4 ? 'text-amber-600' : 'text-red-500'
                  )}>
                    {(module.performance * 100).toFixed(0)}%
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
