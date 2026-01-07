// Economic Autonomy types

export type AssetType = 'btc' | 'eth' | 'usdc' | 'usd' | 'compute';
export type AllocationCategory = 'operational' | 'compute' | 'training' | 'reserve' | 'growth';
export type TreasuryMode = 'simulation' | 'testnet' | 'mainnet';

export interface TreasuryStatus {
  mode: TreasuryMode;
  balances: Record<AssetType, number>;
  allocations: Record<AllocationCategory, number>;
  total_value_usd: number;
  last_transaction?: {
    type: 'deposit' | 'withdrawal' | 'allocation';
    amount: number;
    asset: AssetType;
    timestamp: string;
  };
}

export interface RevenueReport {
  period_start: string;
  period_end: string;
  total_revenue: number;
  currency: string;
  by_service: Record<string, number>;
  by_source: Record<string, number>;
  requests_completed: number;
  requests_failed: number;
}

export interface ServiceListing {
  id: string;
  name: string;
  description: string;
  category: string;
  price: {
    amount: number;
    currency: string;
    model: 'per_token' | 'per_request' | 'subscription';
  };
  status: 'draft' | 'active' | 'suspended' | 'retired';
  sales_count: number;
  rating: number;
}

export interface TrainingInvestment {
  id: string;
  goal_name: string;
  investment_type: 'compute' | 'data' | 'fine_tuning' | 'architecture' | 'capability';
  amount: number;
  status: 'proposed' | 'approved' | 'executing' | 'completed' | 'failed';
  expected_roi: number;
  actual_roi?: number;
  created_at: string;
  completed_at?: string;
}

export interface MarketplaceStats {
  total_listings: number;
  active_listings: number;
  total_sales: number;
  total_revenue: number;
  top_services: Array<{
    id: string;
    name: string;
    sales: number;
  }>;
}
