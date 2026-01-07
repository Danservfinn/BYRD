import { useEffect, useRef, useState } from 'react';
import { CountUp } from 'countup.js';
import { cn } from '@lib/utils/cn';

interface AnimatedCounterProps {
  value: number;
  decimals?: number;
  duration?: number;
  className?: string;
}

export function AnimatedCounter({
  value,
  decimals = 0,
  duration = 1,
  className,
}: AnimatedCounterProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const [hasAnimated, setHasAnimated] = useState(false);

  useEffect(() => {
    if (!ref.current || hasAnimated) return;

    const countUp = new CountUp(ref.current, value, {
      duration,
      decimalPlaces: decimals,
      separator: ',',
    });

    if (!countUp.error) {
      countUp.start();
      setHasAnimated(true);
    } else {
      ref.current.textContent = value.toFixed(decimals);
    }
  }, [value, decimals, duration, hasAnimated]);

  return (
    <span ref={ref} className={cn('tabular-nums', className)}>
      {value.toFixed(decimals)}
    </span>
  );
}
