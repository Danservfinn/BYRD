/**
 * EconomicPage - Observatory Style Economic Agency Dashboard
 */

import { TreasuryStatus } from './TreasuryStatus';
import { RevenueChart } from './RevenueChart';
import { MarketplaceListings } from './MarketplaceListings';
import { StatusIndicator } from '../common/ObservatoryPanel';

export function EconomicPage() {
  return (
    <div className="min-h-screen bg-[var(--obs-bg-base)] obs-grid-bg animate-fade-in pb-20">
      {/* Observatory Header */}
      <div className="px-4 py-4 border-b border-[var(--obs-border)]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="obs-label text-sm tracking-widest text-[var(--obs-text-primary)]">
              ECONOMIC AGENCY
            </h1>
            <StatusIndicator
              status="nominal"
              label="ACTIVE"
            />
          </div>
          <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">
            SELF-SUSTAINING OPERATIONS
          </span>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-4 space-y-4 lg:space-y-6">
        {/* Treasury and Revenue Chart */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6">
          <TreasuryStatus />
          <div className="lg:col-span-2">
            <RevenueChart />
          </div>
        </div>

        {/* Marketplace Listings */}
        <MarketplaceListings />
      </div>
    </div>
  );
}

export default EconomicPage;
