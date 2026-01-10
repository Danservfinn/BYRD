/**
 * DashboardPage - Emergence Observatory Mission Control
 * CERN/NASA inspired interface for monitoring BYRD's consciousness
 */

import { Suspense, lazy } from 'react';
import { TelemetryPanel } from './TelemetryPanel';
import { EmergenceStream } from './EmergenceStream';
import { SystemClock } from './SystemClock';
import { ObservatoryPanel, MetricReadout, StatusIndicator } from '../common/ObservatoryPanel';
import { useRSIStore } from '../../stores/rsiStore';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { useEffect, useState } from 'react';

// Lazy load the 3D visualization for performance
const ByrdCatVisualization = lazy(() => import('../visualization/ByrdCatVisualization'));

export function DashboardPage() {
  const ralphLoop = useRSIStore((state) => state.ralphLoop);
  const [asiProbability] = useState(42.5);
  const [asiTrend] = useState(2.3);
  const { getRSIStatus } = useByrdAPI();
  const [rsiPhase, setRsiPhase] = useState('idle');
  const [systemState, setSystemState] = useState<'running' | 'stopped' | 'dreaming'>('stopped');

  // Fetch RSI status for phase
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const result = await getRSIStatus();
        if (result) {
          setRsiPhase(result.current_phase || 'idle');
          setSystemState(result.current_phase ? 'running' : 'stopped');
        }
      } catch (error) {
        console.error('Failed to fetch RSI status:', error);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, [getRSIStatus]);

  const isActive = ralphLoop.running || systemState === 'running';

  return (
    <div className="min-h-screen bg-[var(--obs-bg-base)] obs-grid-bg animate-fade-in pb-20">
      {/* Observatory Header */}
      <div className="px-4 py-4 border-b border-[var(--obs-border)]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="obs-label text-sm tracking-widest text-[var(--obs-text-primary)]">
              BYRD OBSERVATORY
            </h1>
            <StatusIndicator
              status={isActive ? 'nominal' : 'inactive'}
              label={isActive ? 'ONLINE' : 'STANDBY'}
            />
          </div>
          <SystemClock />
        </div>
      </div>

      {/* Main Content */}
      <div className="p-4 space-y-4 lg:space-y-6">
        {/* Cat Visualization - Central Hero */}
        <div className="relative h-[40vh] lg:h-[50vh] rounded overflow-hidden">
          <Suspense
            fallback={
              <div className="w-full h-full flex items-center justify-center bg-[var(--obs-bg-surface)]">
                <div className="flex flex-col items-center gap-3">
                  <div className="w-8 h-8 border-2 border-[var(--data-stream)] border-t-transparent rounded-full animate-spin" />
                  <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">
                    INITIALIZING CONSCIOUSNESS DISPLAY
                  </span>
                </div>
              </div>
            }
          >
            <ByrdCatVisualization
              rsiPhase={rsiPhase}
              systemState={systemState}
              showScanners={isActive}
              showParticles={true}
              className="w-full h-full"
            />
          </Suspense>

          {/* Overlay: Phase indicator */}
          <div className="absolute bottom-4 left-4">
            <div className="observatory-panel px-3 py-2">
              <div className="obs-label text-[9px] text-[var(--obs-text-tertiary)] mb-1">
                RSI PHASE
              </div>
              <div
                className="obs-metric text-lg uppercase"
                style={{ color: `var(--rsi-${rsiPhase}, var(--obs-text-tertiary))` }}
              >
                {rsiPhase}
              </div>
            </div>
          </div>

          {/* Overlay: ASI Probability */}
          <div className="absolute bottom-4 right-4">
            <div className="observatory-panel px-4 py-3">
              <MetricReadout
                label="ASI PROBABILITY"
                value={asiProbability.toFixed(1)}
                unit="%"
                trend={asiTrend > 0 ? 'up' : asiTrend < 0 ? 'down' : 'stable'}
                trendValue={`${Math.abs(asiTrend).toFixed(1)}%`}
                size="lg"
                status="nominal"
              />
            </div>
          </div>
        </div>

        {/* RSI Phase Progress Bar */}
        <RSIPhaseBar currentPhase={rsiPhase} />

        {/* Two Column Layout: Telemetry + Emergence */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <TelemetryPanel />
          <EmergenceStream />
        </div>
      </div>
    </div>
  );
}

// RSI Phase Progress Bar - Linear display of all 8 phases
interface RSIPhaseBarProps {
  currentPhase: string;
}

function RSIPhaseBar({ currentPhase }: RSIPhaseBarProps) {
  const phases = [
    { id: 'reflect', label: 'R', name: 'Reflect' },
    { id: 'verify', label: 'V', name: 'Verify' },
    { id: 'collapse', label: 'C', name: 'Collapse' },
    { id: 'route', label: 'R', name: 'Route' },
    { id: 'practice', label: 'P', name: 'Practice' },
    { id: 'record', label: 'R', name: 'Record' },
    { id: 'crystallize', label: 'C', name: 'Crystallize' },
    { id: 'measure', label: 'M', name: 'Measure' },
  ];

  const currentIndex = phases.findIndex((p) => p.id === currentPhase);

  return (
    <ObservatoryPanel title="RSI CYCLE PROGRESS" padding="md">
      <div className="flex items-center gap-1">
        {phases.map((phase, index) => {
          const isActive = phase.id === currentPhase;
          const isCompleted = currentIndex > index;
          const phaseColor = `var(--rsi-${phase.id})`;

          return (
            <div
              key={phase.id}
              className={`
                flex-1 h-10 rounded flex items-center justify-center relative
                transition-all duration-300
                ${isActive ? 'animate-emergence-pulse' : ''}
              `}
              style={{
                backgroundColor: isActive || isCompleted ? phaseColor : 'var(--obs-bg-elevated)',
                opacity: isActive ? 1 : isCompleted ? 0.8 : 0.3,
              }}
              title={phase.name}
            >
              <span
                className={`
                  obs-label text-xs font-bold
                  ${isActive || isCompleted ? 'text-white' : 'text-[var(--obs-text-tertiary)]'}
                `}
              >
                {phase.label}
              </span>

              {isActive && (
                <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-[var(--data-stream)]" />
              )}
            </div>
          );
        })}
      </div>

      {/* Phase name display */}
      <div className="mt-3 flex items-center justify-center gap-2">
        <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">CURRENT:</span>
        <span
          className="obs-label text-sm uppercase"
          style={{ color: `var(--rsi-${currentPhase}, var(--obs-text-tertiary))` }}
        >
          {currentPhase === 'idle' ? 'AWAITING CYCLE' : currentPhase}
        </span>
      </div>
    </ObservatoryPanel>
  );
}

export default DashboardPage;
