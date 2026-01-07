import { TreasuryStatus } from './TreasuryStatus';
import { RevenueChart } from './RevenueChart';
import { MarketplaceListings } from './MarketplaceListings';

export function EconomicPage() {
  return (
    <div className="space-y-4 lg:space-y-6 animate-fade-in pb-20">
      {/* Header */}
      <div className="px-4">
        <h1 className="text-xl lg:text-2xl font-bold text-slate-900 dark:text-slate-100">
          Economic Agency
        </h1>
        <p className="text-xs lg:text-sm text-slate-500 dark:text-slate-400">
          Self-sustaining economic operations
        </p>
      </div>

      {/* Treasury and Revenue Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6 px-4">
        <TreasuryStatus />
        <div className="lg:col-span-2">
          <RevenueChart />
        </div>
      </div>

      {/* Marketplace Listings */}
      <div className="px-4">
        <MarketplaceListings />
      </div>
    </div>
  );
}
