import { clsx } from 'clsx';
import type { ReactNode } from 'react';

interface GlassPanelProps {
  children: ReactNode;
  className?: string;
  glow?: 'blue' | 'green' | 'amber' | 'rose' | 'purple' | 'none';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

const glowColors = {
  blue: 'shadow-blue-500/20 hover:shadow-blue-500/30',
  green: 'shadow-green-500/20 hover:shadow-green-500/30',
  amber: 'shadow-amber-500/20 hover:shadow-amber-500/30',
  rose: 'shadow-rose-500/20 hover:shadow-rose-500/30',
  purple: 'shadow-purple-500/20 hover:shadow-purple-500/30',
  none: '',
};

const paddingClasses = {
  none: '',
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6',
};

export function GlassPanel({
  children,
  className = '',
  glow = 'blue',
  padding = 'md',
}: GlassPanelProps) {
  return (
    <div
      className={clsx(
        'glass-panel transition-shadow duration-200',
        glowColors[glow],
        paddingClasses[padding],
        className
      )}
    >
      {children}
    </div>
  );
}
