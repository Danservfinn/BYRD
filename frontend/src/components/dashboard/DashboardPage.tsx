import { SystemStatus } from './SystemStatus';
import { RecentActivity } from './RecentActivity';
import { QuickStats } from './QuickStats';
import { ConsciousnessStream } from './ConsciousnessStream';
import { HeroMetric } from './HeroMetric';

export function DashboardPage() {
  return (
    <div className="space-y-4 lg:space-y-6 animate-fade-in pb-20">
      {/* Header */}
      <div className="px-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl lg:text-2xl font-bold text-slate-900 dark:text-slate-100">
              Dashboard
            </h1>
            <p className="text-xs lg:text-sm text-slate-500 dark:text-slate-400">
              BYRD Recursive Self-Improvement Overview
            </p>
          </div>
        </div>
      </div>

      {/* Hero Metric - ASI Probability */}
      <div className="px-4">
        <HeroMetric value={42.5} trend={2.3} />
      </div>

      {/* Quick Stats Row - Horizontal scroll on mobile */}
      <div className="px-4">
        <QuickStats />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6 px-4">
        {/* System Status - Larger panel */}
        <div className="lg:col-span-2">
          <SystemStatus />
        </div>

        {/* Consciousness Stream */}
        <div className="lg:col-span-1">
          <ConsciousnessStream />
        </div>
      </div>

      {/* Activity Feed */}
      <div className="px-4">
        <RecentActivity />
      </div>
    </div>
  );
}
