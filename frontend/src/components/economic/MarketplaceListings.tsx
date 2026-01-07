import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface Listing {
  id: string;
  type: 'service' | 'capability' | 'knowledge';
  title: string;
  description: string;
  price: number;
  status: 'active' | 'pending' | 'sold';
  created_at: string;
}

export function MarketplaceListings() {
  const { getMarketplaceListings } = useByrdAPI();
  const [listings, setListings] = useState<Listing[]>([]);

  useEffect(() => {
    const fetch = async () => {
      const result = await getMarketplaceListings();
      if (result?.listings) setListings(result.listings);
    };
    fetch();
    const interval = setInterval(fetch, 15000);
    return () => clearInterval(interval);
  }, [getMarketplaceListings]);

  const statusColors: Record<string, string> = {
    active: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
    pending: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400',
    sold: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
  };

  const typeIcons: Record<string, string> = {
    service: '🔧',
    capability: '⚡',
    knowledge: '📚',
  };

  return (
    <GlassPanel glow="none" padding="lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Marketplace Listings
        </h2>
        <span className="text-sm text-slate-500">
          {listings.filter(l => l.status === 'active').length} active
        </span>
      </div>

      {listings.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          No marketplace listings yet.
        </div>
      ) : (
        <div className="space-y-3">
          {listings.map((listing) => (
            <div
              key={listing.id}
              className="p-3 rounded-lg bg-white/50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{typeIcons[listing.type]}</span>
                  <div>
                    <h3 className="font-medium text-slate-900 dark:text-slate-100">
                      {listing.title}
                    </h3>
                    <p className="text-sm text-slate-500 line-clamp-1">
                      {listing.description}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-green-600">
                    ${listing.price.toFixed(2)}
                  </span>
                  <span className={clsx(
                    'px-2 py-0.5 rounded text-xs font-medium capitalize',
                    statusColors[listing.status]
                  )}>
                    {listing.status}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </GlassPanel>
  );
}
