import { HumanAnchoringQueue } from './HumanAnchoringQueue';
import { SafetyTierIndicator } from './SafetyTierIndicator';
import { VerificationLatticeView } from './VerificationLatticeView';

export function VerificationPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
          Verification & Safety
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Human anchoring, safety tiers, and verification lattice status
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <SafetyTierIndicator />
        <div className="lg:col-span-2">
          <VerificationLatticeView />
        </div>
      </div>

      <HumanAnchoringQueue />
    </div>
  );
}
