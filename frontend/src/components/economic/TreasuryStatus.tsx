import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

export function TreasuryStatus() {
  const { getTreasuryStatus } = useByrdAPI();
  const [treasury, setTreasury] = useState<any>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getTreasuryStatus();
      if (result) setTreasury(result);
    };
    fetch();
    const interval = setInterval(fetch, 10000);
    return () => clearInterval(interval);
  }, [getTreasuryStatus]);

  return (
    <GlassPanel glow="amber" padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Treasury
      </h2>

      <div className="text-center py-4">
        <div className="text-4xl font-bold text-amber-600">
          ${(treasury?.balance || 0).toFixed(2)}
        </div>
        <div className="text-sm text-slate-500 mt-1">Current Balance</div>
      </div>

      <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-200 dark:border-slate-700">
        <div className="text-center">
          <div className="text-lg font-semibold text-green-600">
            +${(treasury?.total_revenue || 0).toFixed(2)}
          </div>
          <div className="text-xs text-slate-500">Total Revenue</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-semibold text-red-500">
            -${(treasury?.total_expenses || 0).toFixed(2)}
          </div>
          <div className="text-xs text-slate-500">Total Expenses</div>
        </div>
      </div>
    </GlassPanel>
  );
}
