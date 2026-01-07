import { PhaseTracker } from './PhaseTracker';
import { RalphLoopStatus } from './RalphLoopStatus';
import { EmergenceMetrics } from './EmergenceMetrics';
import { CycleHistory } from './CycleHistory';

export function RSIPage() {
  return (
    <div className="space-y-4 lg:space-y-6 animate-fade-in pb-20">
      {/* Header */}
      <div className="px-4">
        <h1 className="text-xl lg:text-2xl font-bold text-slate-900 dark:text-slate-100">
          RSI Engine
        </h1>
        <p className="text-xs lg:text-sm text-slate-500 dark:text-slate-400">
          8-Phase Recursive Self-Improvement Cycle
        </p>
      </div>

      {/* Phase Tracker - Full Width */}
      <div className="px-4">
        <PhaseTracker />
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6 px-4">
        <RalphLoopStatus />
        <EmergenceMetrics />
      </div>

      {/* Cycle History */}
      <div className="px-4">
        <CycleHistory />
      </div>
    </div>
  );
}
