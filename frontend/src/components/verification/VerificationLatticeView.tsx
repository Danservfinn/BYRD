import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface VerifierStatus {
  id: string;
  name: string;
  type: 'execution' | 'property' | 'llm_critique' | 'adversarial' | 'human_spot';
  status: 'active' | 'pending' | 'error' | 'disabled';
  last_result: 'pass' | 'fail' | 'inconclusive' | null;
  confidence: number;
  checks_performed: number;
}

interface LatticeStatus {
  verifiers: VerifierStatus[];
  consensus_threshold: number;
  last_consensus: boolean;
  total_verifications: number;
}

export function VerificationLatticeView() {
  const { getVerificationStatus } = useByrdAPI();
  const [lattice, setLattice] = useState<LatticeStatus | null>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getVerificationStatus();
      if (result?.lattice) {
        // Type assertion to ensure verifiers match VerifierStatus interface
        const typedLattice: LatticeStatus = {
          ...result.lattice,
          verifiers: result.lattice.verifiers.map(v => ({
            ...v,
            type: (v.type as 'execution' | 'property' | 'llm_critique' | 'adversarial' | 'human_spot') || 'execution'
          }))
        };
        setLattice(typedLattice);
      }
    };
    fetch();
    const interval = setInterval(fetch, 5000);
    return () => clearInterval(interval);
  }, [getVerificationStatus]);

  const typeIcons: Record<string, string> = {
    execution: '⚙️',
    property: '📋',
    llm_critique: '🤖',
    adversarial: '⚔️',
    human_spot: '👤',
  };

  const statusColors: Record<string, string> = {
    active: 'bg-green-500',
    pending: 'bg-amber-500 animate-pulse',
    error: 'bg-red-500',
    disabled: 'bg-slate-400',
  };

  const resultColors: Record<string, string> = {
    pass: 'text-green-600',
    fail: 'text-red-500',
    inconclusive: 'text-amber-600',
  };

  return (
    <GlassPanel glow="cyan" padding="lg" className="h-full">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Verification Lattice
        </h2>
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-500">
            Consensus: {((lattice?.consensus_threshold || 0.6) * 100).toFixed(0)}%
          </span>
          {lattice?.last_consensus !== undefined && (
            <span className={clsx(
              'px-2 py-0.5 rounded text-xs font-medium',
              lattice.last_consensus
                ? 'bg-green-100 text-green-600 dark:bg-green-900/30'
                : 'bg-red-100 text-red-600 dark:bg-red-900/30'
            )}>
              {lattice.last_consensus ? 'PASS' : 'FAIL'}
            </span>
          )}
        </div>
      </div>

      {!lattice?.verifiers || lattice.verifiers.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          No verifiers configured.
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {lattice.verifiers.map((verifier) => (
            <div
              key={verifier.id}
              className="p-3 rounded-lg bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700"
            >
              <div className="flex items-center gap-2 mb-2">
                <div className={clsx('w-2 h-2 rounded-full', statusColors[verifier.status])} />
                <span className="text-lg">{typeIcons[verifier.type]}</span>
                <span className="font-medium text-slate-900 dark:text-slate-100 text-sm">
                  {verifier.name}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-slate-500">Last Result</span>
                  <div className={clsx('font-medium capitalize', resultColors[verifier.last_result || ''] || 'text-slate-400')}>
                    {verifier.last_result || 'N/A'}
                  </div>
                </div>
                <div>
                  <span className="text-slate-500">Confidence</span>
                  <div className="font-medium text-slate-900 dark:text-slate-100">
                    {(verifier.confidence * 100).toFixed(0)}%
                  </div>
                </div>
              </div>

              <div className="mt-2 pt-2 border-t border-slate-200 dark:border-slate-700 text-xs text-slate-500">
                {verifier.checks_performed} checks performed
              </div>
            </div>
          ))}
        </div>
      )}

      {lattice && (
        <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700 text-center text-sm text-slate-500">
          Total verifications: {lattice.total_verifications}
        </div>
      )}
    </GlassPanel>
  );
}
