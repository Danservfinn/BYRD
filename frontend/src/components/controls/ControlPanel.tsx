import { useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { DirectionEditor } from './DirectionEditor';
import { GovernanceConsole } from './GovernanceConsole';
import { DesireInjector } from './DesireInjector';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

export function ControlPanel() {
  const { startRSICycle, stopRSICycle, resetSystem } = useByrdAPI();
  const [systemState, setSystemState] = useState<'running' | 'stopped' | 'paused'>('stopped');
  const [loading, setLoading] = useState<string | null>(null);

  const handleStart = async () => {
    setLoading('start');
    try {
      await startRSICycle();
      setSystemState('running');
    } finally {
      setLoading(null);
    }
  };

  const handleStop = async () => {
    setLoading('stop');
    try {
      await stopRSICycle();
      setSystemState('stopped');
    } finally {
      setLoading(null);
    }
  };

  const handleReset = async () => {
    if (!confirm('Are you sure you want to reset the system? This will clear all current state.')) {
      return;
    }
    setLoading('reset');
    try {
      await resetSystem();
      setSystemState('stopped');
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
          Control Panel
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          System controls and governance interface
        </p>
      </div>

      {/* Main controls */}
      <GlassPanel glow="blue" padding="lg">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
          System Controls
        </h2>

        <div className="flex items-center gap-4 mb-4">
          <div className="flex items-center gap-2">
            <div className={clsx(
              'w-3 h-3 rounded-full',
              systemState === 'running' ? 'bg-green-500 animate-pulse' :
              systemState === 'paused' ? 'bg-amber-500' : 'bg-slate-400'
            )} />
            <span className="text-sm font-medium text-slate-700 dark:text-slate-300 capitalize">
              {systemState}
            </span>
          </div>
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            onClick={handleStart}
            disabled={systemState === 'running' || loading !== null}
            className={clsx(
              'px-4 py-2 rounded-lg font-medium text-white transition-colors',
              systemState === 'running' || loading !== null
                ? 'bg-slate-400 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700'
            )}
          >
            {loading === 'start' ? 'Starting...' : 'Start RSI Cycle'}
          </button>

          <button
            onClick={handleStop}
            disabled={systemState !== 'running' || loading !== null}
            className={clsx(
              'px-4 py-2 rounded-lg font-medium text-white transition-colors',
              systemState !== 'running' || loading !== null
                ? 'bg-slate-400 cursor-not-allowed'
                : 'bg-amber-600 hover:bg-amber-700'
            )}
          >
            {loading === 'stop' ? 'Stopping...' : 'Stop'}
          </button>

          <button
            onClick={handleReset}
            disabled={loading !== null}
            className={clsx(
              'px-4 py-2 rounded-lg font-medium transition-colors',
              loading !== null
                ? 'bg-slate-400 text-white cursor-not-allowed'
                : 'bg-red-100 text-red-600 hover:bg-red-200 dark:bg-red-900/30 dark:text-red-400 dark:hover:bg-red-900/50'
            )}
          >
            {loading === 'reset' ? 'Resetting...' : 'Reset System'}
          </button>
        </div>
      </GlassPanel>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DirectionEditor />
        <DesireInjector />
      </div>

      <GovernanceConsole />
    </div>
  );
}
