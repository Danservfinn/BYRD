import { useState, useEffect } from 'react';
import { useUIStore } from '@store/uiStore';
import { Breakpoint } from '@types/ui';

export function useBreakpoint(): Breakpoint {
  const setBreakpoint = useUIStore((s) => s.setBreakpoint);
  const [breakpoint, setLocalBreakpoint] = useState<Breakpoint>('mobile');

  useEffect(() => {
    const updateBreakpoint = () => {
      const width = window.innerWidth;
      let newBreakpoint: Breakpoint;

      if (width < 768) {
        newBreakpoint = 'mobile';
      } else if (width < 1024) {
        newBreakpoint = 'tablet';
      } else {
        newBreakpoint = 'desktop';
      }

      setLocalBreakpoint(newBreakpoint);
      setBreakpoint(newBreakpoint);
    };

    updateBreakpoint();
    window.addEventListener('resize', updateBreakpoint);
    return () => window.removeEventListener('resize', updateBreakpoint);
  }, [setBreakpoint]);

  return breakpoint;
}
