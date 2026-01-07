import { TrendingUp, Brain } from 'lucide-react';
import { GlassPanel } from '../common/GlassPanel';
import { AnimatedCounter } from '../common/AnimatedCounter';

interface HeroMetricProps {
  value: number;
  trend?: number;
  label?: string;
}

export function HeroMetric({
  value,
  trend,
  label = 'Digital ASI Probability'
}: HeroMetricProps) {
  return (
    <GlassPanel className="relative overflow-hidden">
      {/* Background gradient decoration */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-purple-500/10 to-transparent rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />

      <div className="relative">
        {/* Label */}
        <div className="flex items-center gap-2 mb-2">
          <Brain className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          <h2 className="text-sm font-medium text-slate-600 dark:text-slate-400">
            {label}
          </h2>
        </div>

        {/* Main metric display */}
        <div className="flex items-baseline gap-3">
          <div className="flex items-baseline">
            <span className="text-6xl lg:text-7xl font-bold text-slate-900 dark:text-slate-100 tabular-nums">
              <AnimatedCounter value={value} decimals={1} />
            </span>
            <span className="text-3xl lg:text-4xl font-semibold text-slate-700 dark:text-slate-300 ml-1">
              %
            </span>
          </div>

          {/* Trend indicator */}
          {trend !== undefined && (
            <div className={`
              flex items-center gap-1 px-2 py-1 rounded-lg text-sm font-medium
              ${trend > 0 ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300' : ''}
              ${trend < 0 ? 'bg-rose-100 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300' : ''}
              ${trend === 0 ? 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400' : ''}
            `}>
              <TrendingUp className={`w-4 h-4 ${trend < 0 ? 'rotate-180' : ''}`} />
              <span className="tabular-nums">
                {Math.abs(trend).toFixed(1)}%
              </span>
            </div>
          )}
        </div>

        {/* Description */}
        <p className="mt-3 text-sm text-slate-600 dark:text-slate-400 max-w-md">
          Research phase complete (29 iterations). Bounded RSI validated.
        </p>
      </div>
    </GlassPanel>
  );
}
