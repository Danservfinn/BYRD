/**
 * StatusBar - Observatory Style RSI Status Display
 */

import { useState, useEffect } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { useByrdAPI } from '../../hooks/useByrdAPI';

export function StatusBar() {
  const [isExpanded, setIsExpanded] = useState(true);
  const { getRSIStatus, getRalphLoopStatus } = useByrdAPI();
  const [phase, setPhase] = useState<string | null>(null);
  const [cycleNumber, setCycleNumber] = useState(0);
  const [emergenceConfidence, setEmergenceConfidence] = useState(0);
  const [treasury] = useState(0);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const rsiResult = await getRSIStatus();
        if (rsiResult) {
          setPhase(rsiResult.current_phase || null);
          setCycleNumber(rsiResult.completed_phases?.length || 0);
        }

        const ralphResult = await getRalphLoopStatus();
        if (ralphResult) {
          setEmergenceConfidence((ralphResult as { last_emergence?: { confidence?: number } }).last_emergence?.confidence || 0);
        }
      } catch (error) {
        console.error('Status fetch failed:', error);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, [getRSIStatus, getRalphLoopStatus]);

  const phaseColor = phase ? `var(--rsi-${phase})` : 'var(--obs-text-tertiary)';

  return (
    <div className="px-4 py-2 bg-[var(--obs-bg-elevated)] border-b border-[var(--obs-border)]">
      {/* Collapsed state */}
      {!isExpanded && (
        <button
          onClick={() => setIsExpanded(true)}
          className="w-full flex items-center justify-between text-sm"
        >
          <div className="flex items-center gap-3">
            <span
              className="w-2 h-2 rounded-full animate-status-beacon"
              style={{ backgroundColor: phase ? phaseColor : 'var(--obs-text-tertiary)' }}
            />
            <span className="obs-label text-[11px] text-[var(--obs-text-secondary)]">
              {phase ? `PHASE: ${phase.toUpperCase()}` : 'STANDBY'}
            </span>
          </div>
          <ChevronDown className="w-4 h-4 text-[var(--obs-text-tertiary)]" />
        </button>
      )}

      {/* Expanded state */}
      {isExpanded && (
        <div className="space-y-2">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <span
                className="w-2 h-2 rounded-full animate-status-beacon"
                style={{ backgroundColor: phase ? phaseColor : 'var(--obs-text-tertiary)' }}
              />
              <div>
                <p className="obs-label text-[11px] text-[var(--obs-text-primary)]">
                  RSI CYCLE #{cycleNumber}
                </p>
                <p className="text-[10px] text-[var(--obs-text-tertiary)]">
                  {phase ? (
                    <>
                      Phase:{' '}
                      <span style={{ color: phaseColor }}>
                        {phase.toUpperCase()}
                      </span>
                    </>
                  ) : (
                    'Awaiting cycle start'
                  )}
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsExpanded(false)}
              className="p-1 hover:bg-[var(--obs-bg-surface)] rounded transition-colors"
            >
              <ChevronUp className="w-4 h-4 text-[var(--obs-text-tertiary)]" />
            </button>
          </div>

          {/* Metrics */}
          <div className="flex gap-6 text-[10px]">
            <div className="flex items-center gap-2">
              <span className="obs-label text-[var(--obs-text-tertiary)]">EMERGENCE:</span>
              <span
                className="obs-metric"
                style={{ color: 'var(--cat-eye-gold)' }}
              >
                {(emergenceConfidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="obs-label text-[var(--obs-text-tertiary)]">TREASURY:</span>
              <span
                className="obs-metric"
                style={{ color: 'var(--status-nominal)' }}
              >
                ${treasury > 1000 ? `${(treasury / 1000).toFixed(1)}K` : treasury.toFixed(0)}
              </span>
            </div>
          </div>

          {/* Progress bar */}
          <div className="h-1 bg-[var(--obs-bg-surface)] rounded-full overflow-hidden">
            <div
              className="h-full transition-all duration-500"
              style={{
                width: `${(emergenceConfidence * 100)}%`,
                background: `linear-gradient(90deg, var(--data-stream), var(--cat-eye-gold))`,
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default StatusBar;
