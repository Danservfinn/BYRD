import { useEventStore } from '../../stores/eventStore';

export function ConnectionIndicator() {
  const connected = useEventStore((state) => state.connected);

  return (
    <div className="flex items-center gap-2">
      <span
        className={`w-2 h-2 rounded-full ${
          connected
            ? 'bg-green-500 animate-pulse-glow'
            : 'bg-red-500'
        }`}
      />
      <span className="text-xs text-slate-500 dark:text-slate-400">
        {connected ? 'Connected' : 'Disconnected'}
      </span>
    </div>
  );
}
