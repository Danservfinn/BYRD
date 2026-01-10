/**
 * MemoryPage - Observatory Style Memory Topology Display
 */

import { ObservatoryPanel, StatusIndicator, MetricReadout } from '../common/ObservatoryPanel';
import { EmergenceStream } from '../dashboard/EmergenceStream';
import { useEventStore } from '../../stores/eventStore';

export function MemoryPage() {
  const events = useEventStore((state) => state.events);
  const connected = useEventStore((state) => state.connected);

  // Calculate memory metrics from events
  const beliefCount = events.filter((e) => e.type === 'belief_created').length;
  const desireCount = events.filter((e) => e.type === 'desire_created').length;
  const experienceCount = events.filter((e) => e.type === 'experience_created').length;

  return (
    <div className="min-h-screen bg-[var(--obs-bg-base)] obs-grid-bg animate-fade-in pb-20">
      {/* Observatory Header */}
      <div className="px-4 py-4 border-b border-[var(--obs-border)]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="obs-label text-sm tracking-widest text-[var(--obs-text-primary)]">
              MEMORY TOPOLOGY
            </h1>
            <StatusIndicator
              status={connected ? 'nominal' : 'inactive'}
              label={connected ? 'CONNECTED' : 'OFFLINE'}
            />
          </div>
          <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">
            NEO4J GRAPH INTERFACE
          </span>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-4 space-y-4 lg:space-y-6">
        {/* Memory Statistics */}
        <ObservatoryPanel title="GRAPH STATISTICS" status={connected ? 'nominal' : 'inactive'} padding="lg">
          <div className="grid grid-cols-3 gap-6">
            <MetricReadout
              label="BELIEFS"
              value={beliefCount.toString()}
              size="lg"
              status={beliefCount > 0 ? 'nominal' : undefined}
            />
            <MetricReadout
              label="DESIRES"
              value={desireCount.toString()}
              size="lg"
              status={desireCount > 0 ? 'caution' : undefined}
            />
            <MetricReadout
              label="EXPERIENCES"
              value={experienceCount.toString()}
              size="lg"
            />
          </div>
        </ObservatoryPanel>

        {/* Memory Graph Placeholder */}
        <ObservatoryPanel title="NEURAL TOPOLOGY" padding="none">
          <div className="relative h-[300px] lg:h-[400px] flex items-center justify-center">
            <MemoryGraphPlaceholder />
          </div>
        </ObservatoryPanel>

        {/* Emergence Stream */}
        <EmergenceStream />
      </div>
    </div>
  );
}

function MemoryGraphPlaceholder() {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8">
      {/* Animated rings representing graph nodes */}
      <div className="relative w-32 h-32 mb-6">
        {/* Central node */}
        <div className="absolute inset-1/3 bg-[var(--cat-eye-gold)] rounded-full animate-emergence-pulse shadow-[0_0_30px_var(--cat-eye-gold)]" />

        {/* Orbiting rings */}
        <div className="absolute inset-0 border-2 border-[var(--data-stream)]/30 rounded-full animate-scanner" />
        <div
          className="absolute inset-2 border border-[var(--rsi-reflect)]/20 rounded-full"
          style={{ animationDelay: '0.5s', animation: 'scannerRotate 12s linear infinite reverse' }}
        />
        <div
          className="absolute inset-4 border border-[var(--status-nominal)]/20 rounded-full"
          style={{ animationDelay: '1s', animation: 'scannerRotate 10s linear infinite' }}
        />

        {/* Satellite nodes */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1 w-3 h-3 bg-[var(--data-stream)] rounded-full shadow-[0_0_10px_var(--data-stream)]" />
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1 w-2 h-2 bg-[var(--rsi-practice)] rounded-full" />
        <div className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-1 w-2 h-2 bg-[var(--rsi-reflect)] rounded-full" />
        <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1 w-2 h-2 bg-[var(--status-nominal)] rounded-full" />
      </div>

      <h3 className="obs-label text-sm text-[var(--obs-text-primary)] mb-2">
        MEMORY GRAPH VISUALIZATION
      </h3>
      <p className="text-xs text-[var(--obs-text-tertiary)] max-w-xs">
        3D force-directed graph of BYRD's belief network.
        <br />
        Connect to backend to populate nodes.
      </p>

      {/* Node type legend */}
      <div className="flex gap-4 mt-4">
        <NodeLegend color="var(--cat-eye-gold)" label="BELIEFS" />
        <NodeLegend color="var(--data-stream)" label="DESIRES" />
        <NodeLegend color="var(--status-nominal)" label="CAPABILITIES" />
      </div>
    </div>
  );
}

function NodeLegend({ color, label }: { color: string; label: string }) {
  return (
    <div className="flex items-center gap-2">
      <div
        className="w-2 h-2 rounded-full"
        style={{ backgroundColor: color, boxShadow: `0 0 6px ${color}` }}
      />
      <span className="obs-label text-[8px] text-[var(--obs-text-tertiary)]">{label}</span>
    </div>
  );
}

export default MemoryPage;
