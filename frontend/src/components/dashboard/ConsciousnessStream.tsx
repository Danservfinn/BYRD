import { useEventStore } from '../../stores/eventStore';
import { GlassPanel } from '../common/GlassPanel';

export function ConsciousnessStream() {
  const events = useEventStore((state) => state.events);

  // Filter for consciousness-relevant events
  const consciousnessEvents = events
    .filter((e) =>
      ['BELIEF_CREATED', 'DESIRE_CREATED', 'REFLECTION_COMPLETE', 'EMERGENCE_DETECTED'].includes(e.type)
    )
    .slice(-8)
    .reverse();

  return (
    <GlassPanel glow="purple" padding="lg" className="h-full">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Consciousness Stream
      </h2>

      {consciousnessEvents.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-48 text-center">
          <span className="text-4xl mb-2">🧠</span>
          <p className="text-slate-400 text-sm">
            Consciousness stream is quiet.
            <br />
            Start BYRD to observe emergence.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {consciousnessEvents.map((event) => (
            <ConsciousnessEvent key={event.id} event={event} />
          ))}
        </div>
      )}
    </GlassPanel>
  );
}

function ConsciousnessEvent({ event }: { event: any }) {
  const typeConfig: Record<string, { icon: string; color: string }> = {
    BELIEF_CREATED: { icon: '💭', color: 'var(--node-belief)' },
    DESIRE_CREATED: { icon: '✨', color: 'var(--node-desire)' },
    REFLECTION_COMPLETE: { icon: '🔮', color: 'var(--node-reflection)' },
    EMERGENCE_DETECTED: { icon: '🌟', color: '#7c3aed' },
  };

  const config = typeConfig[event.type] || { icon: '📌', color: '#64748b' };
  const content = event.data?.content || event.data?.description || event.type;

  return (
    <div className="relative pl-6 pb-3 border-l-2 border-slate-200 dark:border-slate-700 last:border-0">
      <span
        className="absolute left-[-5px] top-1 w-2 h-2 rounded-full"
        style={{ backgroundColor: config.color }}
      />
      <div className="flex items-start gap-2">
        <span>{config.icon}</span>
        <div className="flex-1 min-w-0">
          <p className="text-sm text-slate-700 dark:text-slate-300 line-clamp-2">
            {content}
          </p>
          <p className="text-xs text-slate-400 mt-0.5">
            {new Date(event.timestamp).toLocaleTimeString()}
          </p>
        </div>
      </div>
    </div>
  );
}
