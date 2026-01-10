import { clsx } from 'clsx';
import type { ReactNode } from 'react';

type PanelStatus = 'nominal' | 'caution' | 'critical' | 'inactive';

interface ObservatoryPanelProps {
  children: ReactNode;
  className?: string;
  title?: string;
  status?: PanelStatus;
  showScanlines?: boolean;
  showCorners?: boolean;
  active?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

const statusClasses: Record<PanelStatus, string> = {
  nominal: 'status-nominal',
  caution: 'status-caution',
  critical: 'status-critical',
  inactive: '',
};

const paddingClasses = {
  none: '',
  sm: 'p-2 lg:p-3',
  md: 'p-3 lg:p-4',
  lg: 'p-4 lg:p-6',
};

export function ObservatoryPanel({
  children,
  className = '',
  title,
  status,
  showScanlines = true,
  showCorners = true,
  active = false,
  padding = 'md',
}: ObservatoryPanelProps) {
  return (
    <div
      className={clsx(
        'observatory-panel',
        showCorners && 'observatory-panel-corners',
        status && statusClasses[status],
        active && 'active',
        !showScanlines && 'before:hidden',
        paddingClasses[padding],
        className
      )}
    >
      {title && (
        <div className="obs-label mb-2 flex items-center gap-2">
          {status && (
            <span
              className={clsx(
                'status-dot',
                status === 'nominal' && 'status-dot-nominal',
                status === 'caution' && 'status-dot-caution',
                status === 'critical' && 'status-dot-critical',
                status === 'inactive' && 'status-dot-inactive'
              )}
            />
          )}
          <span>{title}</span>
        </div>
      )}
      <div className="relative z-10">{children}</div>
    </div>
  );
}

// Sub-components for Observatory UI elements

interface StatusIndicatorProps {
  status: PanelStatus;
  label?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function StatusIndicator({ status, label, size = 'md' }: StatusIndicatorProps) {
  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-2.5 h-2.5',
    lg: 'w-3 h-3',
  };

  return (
    <div className="flex items-center gap-2">
      <span
        className={clsx(
          'rounded-full animate-status-beacon',
          sizeClasses[size],
          status === 'nominal' && 'bg-[var(--status-nominal)] shadow-[0_0_8px_var(--status-nominal-glow)]',
          status === 'caution' && 'bg-[var(--status-caution)] shadow-[0_0_8px_var(--status-caution-glow)]',
          status === 'critical' && 'bg-[var(--status-critical)] shadow-[0_0_8px_var(--status-critical-glow)]',
          status === 'inactive' && 'bg-[var(--status-inactive)] animate-none'
        )}
      />
      {label && (
        <span
          className={clsx(
            'obs-label',
            status === 'nominal' && 'text-[var(--status-nominal)]',
            status === 'caution' && 'text-[var(--status-caution)]',
            status === 'critical' && 'text-[var(--status-critical)]',
            status === 'inactive' && 'text-[var(--status-inactive)]'
          )}
        >
          {label}
        </span>
      )}
    </div>
  );
}

interface MetricReadoutProps {
  value: string | number;
  label?: string;
  unit?: string;
  trend?: 'up' | 'down' | 'stable';
  trendValue?: string;
  size?: 'md' | 'lg' | 'xl';
  status?: PanelStatus;
}

export function MetricReadout({
  value,
  label,
  unit,
  trend,
  trendValue,
  size = 'lg',
  status = 'nominal',
}: MetricReadoutProps) {
  const sizeClasses = {
    md: 'text-2xl',
    lg: 'obs-metric-lg',
    xl: 'obs-metric-xl',
  };

  const statusColors = {
    nominal: 'text-[var(--status-nominal)]',
    caution: 'text-[var(--status-caution)]',
    critical: 'text-[var(--status-critical)]',
    inactive: 'text-[var(--obs-text-tertiary)]',
  };

  return (
    <div className="flex flex-col">
      {label && <span className="obs-label mb-1">{label}</span>}
      <div className="flex items-baseline gap-1">
        <span className={clsx('obs-metric animate-metric-pulse', sizeClasses[size], statusColors[status])}>
          {value}
        </span>
        {unit && <span className="obs-label text-[var(--obs-text-tertiary)]">{unit}</span>}
      </div>
      {trend && trendValue && (
        <div className="flex items-center gap-1 mt-1">
          <span
            className={clsx(
              'text-xs font-mono',
              trend === 'up' && 'text-[var(--status-nominal)]',
              trend === 'down' && 'text-[var(--status-critical)]',
              trend === 'stable' && 'text-[var(--obs-text-tertiary)]'
            )}
          >
            {trend === 'up' && '▲'}
            {trend === 'down' && '▼'}
            {trend === 'stable' && '─'}
            {' '}
            {trendValue}
          </span>
        </div>
      )}
    </div>
  );
}

interface DataStreamBarProps {
  active?: boolean;
  className?: string;
}

export function DataStreamBar({ active = true, className }: DataStreamBarProps) {
  if (!active) return null;
  return (
    <div className={clsx('overflow-hidden', className)}>
      <div className="data-stream-bar w-full" />
    </div>
  );
}
