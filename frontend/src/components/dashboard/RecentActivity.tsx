import { useEventStore } from '../../stores/eventStore';
import { GlassPanel } from '../common/GlassPanel';
import type { ByrdEvent } from '../../types/events';

export function RecentActivity() {
  const events = useEventStore((state) => state.events);

  // Get last 10 events
  const recentEvents = events.slice(-10).reverse();

  return (
    <GlassPanel glow="none" padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Recent Activity
      </h2>

      {recentEvents.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          No events yet. Start BYRD to see activity.
        </div>
      ) : (
        <div className="space-y-2">
          {recentEvents.map((event) => (
            <EventRow key={event.id} event={event} />
          ))}
        </div>
      )}
    </GlassPanel>
  );
}

function EventRow({ event }: { event: ByrdEvent }) {
  const eventConfig = getEventConfig(event.type);

  return (
    <div className="flex items-start gap-3 py-2 border-b border-slate-100 dark:border-slate-800 last:border-0">
      <span
        className="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm shrink-0"
        style={{ backgroundColor: eventConfig.color }}
      >
        {eventConfig.icon}
      </span>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-medium text-slate-900 dark:text-slate-100 text-sm">
            {eventConfig.label}
          </span>
          <span className="text-xs text-slate-400">
            {formatTime(event.timestamp)}
          </span>
        </div>
        <p className="text-sm text-slate-500 dark:text-slate-400 truncate">
          {getEventDescription(event)}
        </p>
      </div>
    </div>
  );
}

function getEventConfig(type: string): { icon: string; color: string; label: string } {
  const configs: Record<string, { icon: string; color: string; label: string }> = {
    BELIEF_CREATED: { icon: '💭', color: 'var(--node-belief)', label: 'Belief Created' },
    DESIRE_CREATED: { icon: '✨', color: 'var(--node-desire)', label: 'Desire Created' },
    CAPABILITY_ACQUIRED: { icon: '🎯', color: 'var(--node-capability)', label: 'Capability Acquired' },
    RSI_CYCLE_COMPLETE: { icon: '🔄', color: 'var(--rsi-measure)', label: 'RSI Cycle Complete' },
    RSI_PHASE: { icon: '▶️', color: 'var(--rsi-practice)', label: 'Phase Transition' },
    EMERGENCE_DETECTED: { icon: '🌟', color: '#7c3aed', label: 'Emergence Detected' },
    HEURISTIC_CRYSTALLIZED: { icon: '💎', color: 'var(--node-crystal)', label: 'Heuristic Crystallized' },
    EXPERIENCE_RECORDED: { icon: '📝', color: 'var(--node-experience)', label: 'Experience Recorded' },
    REFLECTION_COMPLETE: { icon: '🔮', color: 'var(--node-reflection)', label: 'Reflection Complete' },
    GOAL_SET: { icon: '🎯', color: 'var(--node-goal)', label: 'Goal Set' },
    SYSTEM: { icon: '⚙️', color: '#64748b', label: 'System' },
    ERROR: { icon: '❌', color: '#ef4444', label: 'Error' },
  };

  return configs[type] || { icon: '📌', color: '#64748b', label: type };
}

function getEventDescription(event: ByrdEvent): string {
  if (event.data?.description && typeof event.data.description === 'string') return event.data.description;
  if (event.data?.content && typeof event.data.content === 'string') return event.data.content;
  if (event.data?.phase && typeof event.data.phase === 'string') return `Phase: ${event.data.phase}`;
  if (event.data?.message && typeof event.data.message === 'string') return event.data.message;
  return JSON.stringify(event.data || {}).slice(0, 100);
}

function formatTime(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}
