import { clsx } from 'clsx';
import type { ReactNode } from 'react';
import { GlassPanel } from './GlassPanel';

interface StatCardProps {
  label: string;
  value: string | number;
  icon?: ReactNode;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
  };
  color?: 'blue' | 'green' | 'amber' | 'rose' | 'purple';
  size?: 'sm' | 'md' | 'lg';
}

const colorClasses = {
  blue: 'text-blue-600 dark:text-blue-400',
  green: 'text-green-600 dark:text-green-400',
  amber: 'text-amber-600 dark:text-amber-400',
  rose: 'text-rose-600 dark:text-rose-400',
  purple: 'text-purple-600 dark:text-purple-400',
};

const trendColors = {
  up: 'text-green-500',
  down: 'text-red-500',
  neutral: 'text-slate-500',
};

const trendIcons = {
  up: '↑',
  down: '↓',
  neutral: '→',
};

export function StatCard({
  label,
  value,
  icon,
  trend,
  color = 'blue',
  size = 'md',
}: StatCardProps) {
  return (
    <GlassPanel padding="sm" glow={color === 'blue' ? 'blue' : 'none'} className="active:scale-[0.98] transition-transform">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <p className="text-[10px] sm:text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide truncate">
            {label}
          </p>
          <p className={clsx(
            'font-semibold tabular-nums mt-0.5 truncate',
            colorClasses[color],
            size === 'sm' ? 'text-lg' : size === 'lg' ? 'text-3xl' : 'text-xl lg:text-2xl'
          )}>
            {value}
          </p>
          {trend && (
            <p className={clsx('text-[10px] sm:text-xs mt-1', trendColors[trend.direction])}>
              {trendIcons[trend.direction]} {Math.abs(trend.value)}%
            </p>
          )}
        </div>
        {icon && (
          <div className={clsx('text-xl sm:text-2xl opacity-60 flex-shrink-0', colorClasses[color])}>
            {icon}
          </div>
        )}
      </div>
    </GlassPanel>
  );
}
