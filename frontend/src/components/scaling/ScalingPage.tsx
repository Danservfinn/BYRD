import { GrowthRateGauge } from './GrowthRateGauge';
import { ExplosionPhaseIndicator } from './ExplosionPhaseIndicator';
import { EntropicDriftMonitor } from './EntropicDriftMonitor';

export function ScalingPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
          Scaling & Growth
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Capability explosion and entropic drift monitoring
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <GrowthRateGauge />
        <ExplosionPhaseIndicator />
        <div className="lg:col-span-1">
          <EntropicDriftMonitor />
        </div>
      </div>
    </div>
  );
}
