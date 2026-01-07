import { ModuleRegistry } from './ModuleRegistry';
import { NASCandidates } from './NASCandidates';
import { CompositionGraph } from './CompositionGraph';

export function PlasticityPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
          Cognitive Plasticity
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Module composition and architecture search
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ModuleRegistry />
        <NASCandidates />
      </div>

      <CompositionGraph />
    </div>
  );
}
