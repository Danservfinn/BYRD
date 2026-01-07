import type { GraphNode } from './MemoryTopology';
import { clsx } from 'clsx';

interface NodeRendererProps {
  node: GraphNode;
  isSelected?: boolean;
  onClick?: () => void;
  typeColors: Record<string, string>;
}

/**
 * 2D node renderer component for list/detail views.
 * The 3D visualization uses canvas rendering directly.
 */
export function NodeRenderer({ node, isSelected, onClick, typeColors }: NodeRendererProps) {
  const color = typeColors[node.type] || '#64748b';

  return (
    <div
      onClick={onClick}
      className={clsx(
        'p-3 rounded-lg border transition-all cursor-pointer',
        isSelected
          ? 'border-2 shadow-lg'
          : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
      )}
      style={{
        borderColor: isSelected ? color : undefined,
        boxShadow: isSelected ? `0 0 20px ${color}40` : undefined,
      }}
    >
      <div className="flex items-center gap-3">
        {/* Node indicator */}
        <div
          className="w-4 h-4 rounded-full flex-shrink-0"
          style={{ backgroundColor: color }}
        />

        {/* Node info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span
              className="text-xs font-medium uppercase px-1.5 py-0.5 rounded"
              style={{
                backgroundColor: `${color}20`,
                color: color,
              }}
            >
              {node.type}
            </span>
            <span className="text-xs text-slate-500">
              {(node.strength * 100).toFixed(0)}%
            </span>
          </div>
          <p className="text-sm text-slate-900 dark:text-slate-100 mt-1 line-clamp-2">
            {node.label}
          </p>
        </div>
      </div>
    </div>
  );
}

/**
 * Mini node indicator for compact views
 */
export function NodeIndicator({
  type,
  size = 'md',
  typeColors,
}: {
  type: GraphNode['type'];
  size?: 'sm' | 'md' | 'lg';
  typeColors: Record<string, string>;
}) {
  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
  };

  return (
    <div
      className={clsx('rounded-full', sizeClasses[size])}
      style={{ backgroundColor: typeColors[type] || '#64748b' }}
      title={type}
    />
  );
}

/**
 * Node type legend
 */
export function NodeTypeLegend({ typeColors }: { typeColors: Record<string, string> }) {
  const types: GraphNode['type'][] = [
    'belief',
    'desire',
    'experience',
    'reflection',
    'capability',
    'goal',
  ];

  return (
    <div className="flex flex-wrap gap-4">
      {types.map((type) => (
        <div key={type} className="flex items-center gap-2">
          <NodeIndicator type={type} size="sm" typeColors={typeColors} />
          <span className="text-xs text-slate-600 dark:text-slate-400 capitalize">
            {type}
          </span>
        </div>
      ))}
    </div>
  );
}
