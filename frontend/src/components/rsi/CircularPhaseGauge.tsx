/**
 * CircularPhaseGauge - Observatory Style RSI Phase Visualization
 * Inspired by nuclear reactor status displays
 */

import { useEffect, useState, useMemo } from 'react';
import { useByrdAPI } from '../../hooks/useByrdAPI';

const PHASES = [
  { id: 'reflect', name: 'REFLECT', shortName: 'R' },
  { id: 'verify', name: 'VERIFY', shortName: 'V' },
  { id: 'collapse', name: 'COLLAPSE', shortName: 'C' },
  { id: 'route', name: 'ROUTE', shortName: 'R' },
  { id: 'practice', name: 'PRACTICE', shortName: 'P' },
  { id: 'record', name: 'RECORD', shortName: 'R' },
  { id: 'crystallize', name: 'CRYSTALLIZE', shortName: 'C' },
  { id: 'measure', name: 'MEASURE', shortName: 'M' },
];

interface CircularPhaseGaugeProps {
  size?: number;
  className?: string;
}

export function CircularPhaseGauge({ size = 320, className = '' }: CircularPhaseGaugeProps) {
  const { getRSIStatus } = useByrdAPI();
  const [currentPhase, setCurrentPhase] = useState<string | null>(null);
  const [completedPhases, setCompletedPhases] = useState<string[]>([]);

  useEffect(() => {
    const fetchStatus = async () => {
      const result = await getRSIStatus();
      if (result) {
        setCurrentPhase(result.current_phase || null);
        setCompletedPhases(result.completed_phases || []);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, [getRSIStatus]);

  const currentIndex = PHASES.findIndex((p) => p.id === currentPhase);

  // SVG calculations
  const center = size / 2;
  const outerRadius = size / 2 - 20;
  const innerRadius = outerRadius - 40;
  const phaseArc = (2 * Math.PI) / PHASES.length;

  // Generate arc paths for each phase segment
  const segments = useMemo(() => {
    return PHASES.map((phase, index) => {
      const startAngle = index * phaseArc - Math.PI / 2;
      const endAngle = startAngle + phaseArc;
      const gap = 0.02; // Small gap between segments

      const x1 = center + outerRadius * Math.cos(startAngle + gap);
      const y1 = center + outerRadius * Math.sin(startAngle + gap);
      const x2 = center + outerRadius * Math.cos(endAngle - gap);
      const y2 = center + outerRadius * Math.sin(endAngle - gap);
      const x3 = center + innerRadius * Math.cos(endAngle - gap);
      const y3 = center + innerRadius * Math.sin(endAngle - gap);
      const x4 = center + innerRadius * Math.cos(startAngle + gap);
      const y4 = center + innerRadius * Math.sin(startAngle + gap);

      const largeArc = phaseArc > Math.PI ? 1 : 0;

      const path = `
        M ${x1} ${y1}
        A ${outerRadius} ${outerRadius} 0 ${largeArc} 1 ${x2} ${y2}
        L ${x3} ${y3}
        A ${innerRadius} ${innerRadius} 0 ${largeArc} 0 ${x4} ${y4}
        Z
      `;

      // Label position
      const labelAngle = startAngle + phaseArc / 2;
      const labelRadius = (outerRadius + innerRadius) / 2;
      const labelX = center + labelRadius * Math.cos(labelAngle);
      const labelY = center + labelRadius * Math.sin(labelAngle);

      return { ...phase, path, labelX, labelY, index };
    });
  }, [size, center, outerRadius, innerRadius, phaseArc]);

  return (
    <div className={`relative ${className}`}>
      <svg width={size} height={size} className="overflow-visible">
        <defs>
          {/* Glow filter for active phase */}
          <filter id="phaseGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          {/* Scanline pattern */}
          <pattern id="scanlines" patternUnits="userSpaceOnUse" width="4" height="4">
            <line x1="0" y1="0" x2="4" y2="0" stroke="rgba(0,255,255,0.03)" strokeWidth="1" />
          </pattern>
        </defs>

        {/* Background circle with grid */}
        <circle
          cx={center}
          cy={center}
          r={outerRadius + 10}
          fill="var(--obs-bg-elevated)"
          stroke="var(--obs-border)"
          strokeWidth="1"
        />

        {/* Inner decorative rings */}
        <circle
          cx={center}
          cy={center}
          r={innerRadius - 20}
          fill="none"
          stroke="var(--obs-border)"
          strokeWidth="0.5"
          strokeDasharray="4 4"
        />
        <circle
          cx={center}
          cy={center}
          r={innerRadius - 40}
          fill="none"
          stroke="var(--obs-border)"
          strokeWidth="0.5"
        />

        {/* Phase segments */}
        {segments.map((segment) => {
          const isActive = segment.id === currentPhase;
          const isCompleted = completedPhases.includes(segment.id);
          const isPending = !isActive && !isCompleted;

          return (
            <g key={segment.id}>
              <path
                d={segment.path}
                fill={
                  isActive || isCompleted
                    ? `var(--rsi-${segment.id})`
                    : 'var(--obs-bg-surface)'
                }
                stroke={isActive ? `var(--rsi-${segment.id})` : 'var(--obs-border)'}
                strokeWidth={isActive ? 2 : 1}
                opacity={isPending ? 0.3 : isCompleted ? 0.8 : 1}
                filter={isActive ? 'url(#phaseGlow)' : undefined}
                className={isActive ? 'animate-emergence-pulse' : ''}
              />
              <text
                x={segment.labelX}
                y={segment.labelY}
                textAnchor="middle"
                dominantBaseline="middle"
                className="obs-label"
                fontSize="12"
                fill={
                  isActive || isCompleted
                    ? 'white'
                    : 'var(--obs-text-tertiary)'
                }
                fontWeight={isActive ? 'bold' : 'normal'}
              >
                {segment.shortName}
              </text>
            </g>
          );
        })}

        {/* Center display */}
        <circle
          cx={center}
          cy={center}
          r={innerRadius - 50}
          fill="var(--obs-bg-base)"
          stroke="var(--obs-border)"
          strokeWidth="1"
        />

        {/* Center content */}
        <text
          x={center}
          y={center - 15}
          textAnchor="middle"
          className="obs-label"
          fontSize="10"
          fill="var(--obs-text-tertiary)"
        >
          RSI PHASE
        </text>
        <text
          x={center}
          y={center + 10}
          textAnchor="middle"
          className="obs-metric"
          fontSize="16"
          fill={currentPhase ? `var(--rsi-${currentPhase})` : 'var(--obs-text-secondary)'}
        >
          {currentPhase?.toUpperCase() || 'IDLE'}
        </text>
        <text
          x={center}
          y={center + 35}
          textAnchor="middle"
          className="obs-label"
          fontSize="9"
          fill="var(--obs-text-tertiary)"
        >
          {completedPhases.length}/8 COMPLETE
        </text>

        {/* Active phase indicator arrow */}
        {currentIndex >= 0 && (
          <g transform={`rotate(${currentIndex * 45 - 90}, ${center}, ${center})`}>
            <polygon
              points={`${center},${center - outerRadius - 5} ${center - 6},${center - outerRadius - 15} ${center + 6},${center - outerRadius - 15}`}
              fill={`var(--rsi-${currentPhase})`}
              className="animate-status-beacon"
            />
          </g>
        )}

        {/* Scanline overlay */}
        <circle
          cx={center}
          cy={center}
          r={outerRadius}
          fill="url(#scanlines)"
          pointerEvents="none"
        />
      </svg>

      {/* Phase legend */}
      <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 observatory-panel px-3 py-2">
        <div className="flex items-center gap-2">
          <span
            className="w-2 h-2 rounded-full animate-status-beacon"
            style={{
              backgroundColor: currentPhase
                ? `var(--rsi-${currentPhase})`
                : 'var(--obs-text-tertiary)',
            }}
          />
          <span className="obs-label text-[10px] text-[var(--obs-text-secondary)]">
            {currentPhase
              ? PHASES.find((p) => p.id === currentPhase)?.name
              : 'AWAITING CYCLE'}
          </span>
        </div>
      </div>
    </div>
  );
}

export default CircularPhaseGauge;
