import { PhaseTracker } from './PhaseTracker';
import { RalphLoopStatus } from './RalphLoopStatus';
import { EmergenceMetrics } from './EmergenceMetrics';
import { CycleHistory } from './CycleHistory';

export function RSIPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
          RSI Engine
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          8-Phase Recursive Self-Improvement Cycle
        </p>
      </div>

      {/* Phase Tracker - Full Width */}
      <PhaseTracker />

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RalphLoopStatus />
        <EmergenceMetrics />
      </div>

      {/* Cycle History */}
      <CycleHistory />
    </div>
  );
}
