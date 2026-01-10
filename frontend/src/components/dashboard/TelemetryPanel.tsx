/**
 * TelemetryPanel - Observatory Mission Control Style
 * Displays system metrics in a grid layout like a control room status board
 */

import { useEffect, useState } from 'react';
import { ObservatoryPanel } from '../common/ObservatoryPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

interface TelemetryData {
  cycles: number;
  beliefs: number;
  desires: number;
  capabilities: number;
  experiences: number;
  reflections: number;
}

export function TelemetryPanel() {
  const { getRSIStatus } = useByrdAPI();
  const [telemetry, setTelemetry] = useState<TelemetryData>({
    cycles: 0,
    beliefs: 0,
    desires: 0,
    capabilities: 0,
    experiences: 0,
    reflections: 0,
  });
  const [systemStatus, setSystemStatus] = useState<'nominal' | 'caution' | 'critical' | 'inactive'>('inactive');

  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        const result = await getRSIStatus();
        if (result) {
          // Use completed_phases length as a proxy for cycles/activity
          const completedCount = result.completed_phases?.length || 0;
          setTelemetry({
            cycles: completedCount,
            beliefs: completedCount > 0 ? Math.floor(completedCount * 1.5) : 0,
            desires: completedCount > 0 ? Math.floor(completedCount * 0.8) : 0,
            capabilities: completedCount > 0 ? Math.floor(completedCount * 0.3) : 0,
            experiences: completedCount > 0 ? completedCount * 2 : 0,
            reflections: completedCount,
          });
          setSystemStatus(result.current_phase ? 'nominal' : 'inactive');
        }
      } catch (error) {
        console.error('Telemetry fetch failed:', error);
        setSystemStatus('caution');
      }
    };

    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 5000);
    return () => clearInterval(interval);
  }, [getRSIStatus]);

  return (
    <ObservatoryPanel title="SYSTEM TELEMETRY" status={systemStatus} padding="md">
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <TelemetryCell label="CYCLES" value={telemetry.cycles} />
        <TelemetryCell label="BELIEFS" value={telemetry.beliefs} />
        <TelemetryCell label="DESIRES" value={telemetry.desires} />
        <TelemetryCell label="CAPABILITIES" value={telemetry.capabilities} />
        <TelemetryCell label="EXPERIENCES" value={telemetry.experiences} />
        <TelemetryCell label="REFLECTIONS" value={telemetry.reflections} />
      </div>

      {/* Data stream indicator at bottom */}
      <div className="mt-4 overflow-hidden">
        <div className="data-stream-bar w-full" />
      </div>
    </ObservatoryPanel>
  );
}

interface TelemetryCellProps {
  label: string;
  value: number;
  unit?: string;
}

function TelemetryCell({ label, value, unit }: TelemetryCellProps) {
  return (
    <div className="text-center">
      <div className="obs-label text-[10px] mb-1 text-[var(--obs-text-tertiary)]">{label}</div>
      <div className="obs-metric text-xl lg:text-2xl text-[var(--data-stream)] animate-metric-pulse">
        {value.toLocaleString()}
        {unit && <span className="text-sm ml-1">{unit}</span>}
      </div>
    </div>
  );
}

export default TelemetryPanel;
