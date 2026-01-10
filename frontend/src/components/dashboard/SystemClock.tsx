/**
 * SystemClock - Observatory UTC Time Display
 * Shows current time in UTC format like mission control
 */

import { useEffect, useState } from 'react';

interface SystemClockProps {
  className?: string;
}

export function SystemClock({ className = '' }: SystemClockProps) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const formatTime = (date: Date): string => {
    return date.toISOString().slice(11, 19);
  };

  const formatDate = (date: Date): string => {
    return date.toISOString().slice(0, 10);
  };

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <div className="obs-metric text-lg text-[var(--data-stream)] animate-metric-pulse">
        {formatTime(time)}
      </div>
      <div className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">
        UTC
      </div>
      <div className="obs-label text-[10px] text-[var(--obs-text-secondary)]">
        {formatDate(time)}
      </div>
    </div>
  );
}

export default SystemClock;
