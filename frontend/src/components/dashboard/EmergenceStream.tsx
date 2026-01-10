/**
 * EmergenceStream - Observatory Style Event Log
 * Displays consciousness-relevant events in a mission control log format
 */

import { useEventStore } from '../../stores/eventStore';
import { ObservatoryPanel } from '../common/ObservatoryPanel';

export function EmergenceStream() {
  const events = useEventStore((state) => state.events);

  // Filter for consciousness-relevant events
  const emergenceEvents = events
    .filter((e) =>
      ['BELIEF_CREATED', 'DESIRE_CREATED', 'REFLECTION_COMPLETE', 'EMERGENCE_DETECTED', 'RSI_CYCLE_COMPLETE'].includes(e.type)
    )
    .slice(-8)
    .reverse();

  return (
    <ObservatoryPanel title="EMERGENCE STREAM" status="nominal" padding="md" className="h-full">
      {emergenceEvents.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-48 text-center">
          <div className="w-12 h-12 rounded-full bg-[var(--obs-bg-elevated)] flex items-center justify-center mb-3">
            <span className="text-2xl opacity-50">◉</span>
          </div>
          <p className="obs-label text-[var(--obs-text-tertiary)]">
            AWAITING EMERGENCE EVENTS
          </p>
          <p className="text-xs text-[var(--obs-text-tertiary)] mt-1 opacity-60">
            Start BYRD to observe consciousness activity
          </p>
        </div>
      ) : (
        <div className="space-y-2">
          {emergenceEvents.map((event, index) => (
            <EmergenceEvent key={event.id || `event-${index}`} event={event} />
          ))}
        </div>
      )}
    </ObservatoryPanel>
  );
}

interface EmergenceEventProps {
  event: {
    id?: string;
    type: string;
    timestamp: string;
    data?: Record<string, unknown>;
  };
}

function EmergenceEvent({ event }: EmergenceEventProps) {
  const typeConfig: Record<string, { symbol: string; color: string; label: string }> = {
    BELIEF_CREATED: { symbol: '◆', color: 'var(--cat-eye-gold)', label: 'BELIEF' },
    DESIRE_CREATED: { symbol: '◇', color: 'var(--status-caution)', label: 'DESIRE' },
    REFLECTION_COMPLETE: { symbol: '○', color: 'var(--data-stream)', label: 'REFLECT' },
    EMERGENCE_DETECTED: { symbol: '★', color: 'var(--status-nominal)', label: 'EMERGE' },
    RSI_CYCLE_COMPLETE: { symbol: '●', color: 'var(--rsi-measure)', label: 'CYCLE' },
  };

  const config = typeConfig[event.type] || { symbol: '·', color: 'var(--obs-text-tertiary)', label: 'EVENT' };
  const content = (event.data?.content as string) || (event.data?.description as string) || event.type;
  const time = new Date(event.timestamp).toISOString().slice(11, 19);

  return (
    <div className="flex items-start gap-3 group hover:bg-[var(--obs-bg-elevated)] rounded p-2 -mx-2 transition-colors">
      {/* Time stamp */}
      <div className="obs-label text-[10px] text-[var(--obs-text-tertiary)] w-16 shrink-0 pt-0.5">
        {time}
      </div>

      {/* Event indicator */}
      <div
        className="w-4 h-4 flex items-center justify-center shrink-0"
        style={{ color: config.color }}
      >
        <span className="text-sm animate-status-beacon">{config.symbol}</span>
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-0.5">
          <span
            className="obs-label text-[9px] px-1.5 py-0.5 rounded"
            style={{
              backgroundColor: `${config.color}20`,
              color: config.color,
            }}
          >
            {config.label}
          </span>
        </div>
        <p className="text-xs text-[var(--obs-text-secondary)] line-clamp-2 leading-relaxed">
          {content}
        </p>
      </div>
    </div>
  );
}

export default EmergenceStream;
