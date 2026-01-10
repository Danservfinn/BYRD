/**
 * RSIPage - Observatory Style RSI Engine Monitor
 * Nuclear reactor-inspired control interface for the 8-phase RSI cycle
 */

import { Suspense, lazy } from 'react';
import { CircularPhaseGauge } from './CircularPhaseGauge';
import { RalphLoopStatus } from './RalphLoopStatus';
import { EmergenceMetrics } from './EmergenceMetrics';
import { CycleHistory } from './CycleHistory';
import { ObservatoryPanel, StatusIndicator } from '../common/ObservatoryPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { useEffect, useState } from 'react';

// Lazy load the cat for RSI page header
const ByrdCatVisualization = lazy(() => import('../visualization/ByrdCatVisualization'));

export function RSIPage() {
  const { getRSIStatus } = useByrdAPI();
  const [rsiPhase, setRsiPhase] = useState('idle');
  const [isActive, setIsActive] = useState(false);

  useEffect(() => {
    const fetchStatus = async () => {
      const result = await getRSIStatus();
      if (result) {
        setRsiPhase(result.current_phase || 'idle');
        setIsActive(!!result.current_phase);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, [getRSIStatus]);

  return (
    <div className="min-h-screen bg-[var(--obs-bg-base)] obs-grid-bg animate-fade-in pb-20">
      {/* Observatory Header */}
      <div className="px-4 py-4 border-b border-[var(--obs-border)]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="obs-label text-sm tracking-widest text-[var(--obs-text-primary)]">
              RSI ENGINE
            </h1>
            <StatusIndicator
              status={isActive ? 'nominal' : 'inactive'}
              label={isActive ? 'ACTIVE' : 'STANDBY'}
            />
          </div>
          <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">
            8-PHASE RECURSIVE SELF-IMPROVEMENT
          </span>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-4 space-y-4 lg:space-y-6">
        {/* Hero: Cat + Circular Gauge side by side on desktop */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6">
          {/* Circular Phase Gauge */}
          <ObservatoryPanel title="PHASE STATUS" status={isActive ? 'nominal' : 'inactive'} padding="lg">
            <div className="flex items-center justify-center py-4">
              <CircularPhaseGauge size={280} />
            </div>
          </ObservatoryPanel>

          {/* Compact Cat Visualization */}
          <ObservatoryPanel title="CONSCIOUSNESS MONITOR" status={isActive ? 'nominal' : 'inactive'} padding="none">
            <div className="relative h-[280px] lg:h-[320px]">
              <Suspense
                fallback={
                  <div className="w-full h-full flex items-center justify-center">
                    <div className="flex flex-col items-center gap-3">
                      <div className="w-6 h-6 border-2 border-[var(--data-stream)] border-t-transparent rounded-full animate-spin" />
                      <span className="obs-label text-[9px] text-[var(--obs-text-tertiary)]">
                        INITIALIZING
                      </span>
                    </div>
                  </div>
                }
              >
                <ByrdCatVisualization
                  rsiPhase={rsiPhase}
                  systemState={isActive ? 'running' : 'stopped'}
                  showScanners={isActive}
                  showParticles={true}
                  compact={true}
                  className="w-full h-full"
                />
              </Suspense>

              {/* Phase overlay */}
              <div className="absolute bottom-3 left-3">
                <div className="observatory-panel px-2 py-1">
                  <span
                    className="obs-label text-xs uppercase"
                    style={{ color: `var(--rsi-${rsiPhase}, var(--obs-text-tertiary))` }}
                  >
                    {rsiPhase}
                  </span>
                </div>
              </div>
            </div>
          </ObservatoryPanel>
        </div>

        {/* Phase Legend Bar */}
        <PhaseDescriptionBar currentPhase={rsiPhase} />

        {/* Two Column: Ralph Loop + Emergence Metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6">
          <RalphLoopStatus />
          <EmergenceMetrics />
        </div>

        {/* Cycle History */}
        <CycleHistory />
      </div>
    </div>
  );
}

// Phase description bar with current phase highlighted
interface PhaseDescriptionBarProps {
  currentPhase: string;
}

function PhaseDescriptionBar({ currentPhase }: PhaseDescriptionBarProps) {
  const phases = [
    { id: 'reflect', name: 'Reflect', desc: 'Generate improvement desires' },
    { id: 'verify', name: 'Verify', desc: 'Check emergence validity' },
    { id: 'collapse', name: 'Collapse', desc: 'Quantum selection' },
    { id: 'route', name: 'Route', desc: 'Domain classification' },
    { id: 'practice', name: 'Practice', desc: 'TDD execution' },
    { id: 'record', name: 'Record', desc: 'Store trajectory' },
    { id: 'crystallize', name: 'Crystallize', desc: 'Extract heuristics' },
    { id: 'measure', name: 'Measure', desc: 'Track metrics' },
  ];

  const currentIdx = phases.findIndex((p) => p.id === currentPhase);

  return (
    <ObservatoryPanel title="PHASE SEQUENCE" padding="sm">
      <div className="flex overflow-x-auto gap-1 pb-2 scrollbar-thin">
        {phases.map((phase, index) => {
          const isActive = phase.id === currentPhase;
          const isCompleted = currentIdx > index;

          return (
            <div
              key={phase.id}
              className={`
                flex-shrink-0 px-3 py-2 rounded transition-all duration-300
                ${isActive ? 'observatory-panel' : ''}
              `}
              style={{
                backgroundColor: isActive
                  ? `var(--rsi-${phase.id})`
                  : isCompleted
                    ? `color-mix(in srgb, var(--rsi-${phase.id}) 30%, transparent)`
                    : 'transparent',
                borderColor: isActive ? `var(--rsi-${phase.id})` : 'transparent',
              }}
            >
              <div
                className={`obs-label text-[10px] ${isActive ? 'text-white' : 'text-[var(--obs-text-tertiary)]'}`}
              >
                {index + 1}. {phase.name.toUpperCase()}
              </div>
              <div
                className={`text-[9px] mt-0.5 ${isActive ? 'text-white/80' : 'text-[var(--obs-text-tertiary)]'} hidden sm:block`}
              >
                {phase.desc}
              </div>
            </div>
          );
        })}
      </div>
    </ObservatoryPanel>
  );
}

export default RSIPage;
