import { SystemStatus } from './SystemStatus';
import { RecentActivity } from './RecentActivity';
import { QuickStats } from './QuickStats';
import { ConsciousnessStream } from './ConsciousnessStream';

export function DashboardPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
            Dashboard
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            BYRD Recursive Self-Improvement Overview
          </p>
        </div>
      </div>

      {/* Quick Stats Row */}
      <QuickStats />

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
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
      <RecentActivity />
    </div>
  );
}
