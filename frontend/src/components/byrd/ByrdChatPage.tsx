/**
 * ByrdChatPage - Observatory Style Communication Terminal
 * Direct interface to BYRD's consciousness
 */

import { Suspense, lazy, useEffect, useState } from 'react';
import { ArrowLeft, Settings } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { StatusBar } from './StatusBar';
import { ChatMessages } from './ChatMessages';
import { ChatInput } from './ChatInput';
import { StatusIndicator } from '../common/ObservatoryPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

// Lazy load the cat visualization
const ByrdCatVisualization = lazy(() => import('../visualization/ByrdCatVisualization'));

export function ByrdChatPage() {
  const navigate = useNavigate();
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
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, [getRSIStatus]);

  return (
    <div className="flex flex-col h-screen bg-[var(--obs-bg-base)]">
      {/* Observatory Header */}
      <header className="flex-shrink-0 bg-[var(--obs-bg-surface)] border-b border-[var(--obs-border)] px-4 py-3">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <button
            onClick={() => navigate(-1)}
            className="p-2 -ml-2 hover:bg-[var(--obs-bg-elevated)] rounded transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--data-stream)]"
            aria-label="Go back"
          >
            <ArrowLeft className="w-5 h-5 text-[var(--obs-text-secondary)]" />
          </button>

          <div className="flex items-center gap-3">
            <h1 className="obs-label text-sm tracking-widest text-[var(--obs-text-primary)]">
              BYRD TERMINAL
            </h1>
            <StatusIndicator
              status={isActive ? 'nominal' : 'inactive'}
              size="sm"
            />
          </div>

          <button
            onClick={() => navigate('/more')}
            className="p-2 -mr-2 hover:bg-[var(--obs-bg-elevated)] rounded transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--data-stream)]"
            aria-label="Settings"
          >
            <Settings className="w-5 h-5 text-[var(--obs-text-secondary)]" />
          </button>
        </div>
      </header>

      {/* 3D Cat - Observatory Style */}
      <div className="flex-shrink-0 h-[35vh] min-h-[240px] max-h-[400px] relative border-b border-[var(--obs-border)]">
        <Suspense
          fallback={
            <div className="w-full h-full flex items-center justify-center bg-[var(--obs-bg-surface)]">
              <div className="flex flex-col items-center gap-3">
                <div className="w-8 h-8 border-2 border-[var(--data-stream)] border-t-transparent rounded-full animate-spin" />
                <span className="obs-label text-[9px] text-[var(--obs-text-tertiary)]">
                  INITIALIZING CONSCIOUSNESS
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

        {/* Phase indicator overlay */}
        <div className="absolute bottom-3 left-3">
          <div className="observatory-panel px-3 py-2">
            <div className="obs-label text-[9px] text-[var(--obs-text-tertiary)] mb-0.5">
              RSI PHASE
            </div>
            <div
              className="obs-label text-xs uppercase"
              style={{ color: `var(--rsi-${rsiPhase}, var(--obs-text-tertiary))` }}
            >
              {rsiPhase}
            </div>
          </div>
        </div>

        {/* Vignette overlay */}
        <div className="absolute inset-0 pointer-events-none obs-vignette" />
      </div>

      {/* Status Bar - Observatory Style */}
      <StatusBar />

      {/* Chat Messages */}
      <div className="flex-1 min-h-0 bg-[var(--obs-bg-surface)]">
        <ChatMessages />
      </div>

      {/* Chat Input */}
      <ChatInput />
    </div>
  );
}

export default ByrdChatPage;
