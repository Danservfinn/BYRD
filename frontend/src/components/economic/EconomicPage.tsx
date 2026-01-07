import { TreasuryStatus } from './TreasuryStatus';
import { RevenueChart } from './RevenueChart';
import { MarketplaceListings } from './MarketplaceListings';

export function EconomicPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
          Economic Agency
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Self-sustaining economic operations
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <TreasuryStatus />
        <div className="lg:col-span-2">
          <RevenueChart />
        </div>
      </div>

      <MarketplaceListings />
    </div>
  );
}
