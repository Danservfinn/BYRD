import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export function RevenueChart() {
  const { getRevenueReport } = useByrdAPI();
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const fetch = async () => {
      const result = await getRevenueReport();
      if (result?.history) setData(result.history);
    };
    fetch();
    const interval = setInterval(fetch, 30000);
    return () => clearInterval(interval);
  }, [getRevenueReport]);

  // Mock data for display
  const displayData = data.length > 0 ? data : [
    { date: 'Mon', revenue: 0, expenses: 0 },
    { date: 'Tue', revenue: 0, expenses: 0 },
    { date: 'Wed', revenue: 0, expenses: 0 },
    { date: 'Thu', revenue: 0, expenses: 0 },
    { date: 'Fri', revenue: 0, expenses: 0 },
  ];

  return (
    <GlassPanel glow="green" padding="lg" className="h-full">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Revenue Over Time
      </h2>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={displayData}>
            <defs>
              <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorExpenses" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis
              dataKey="date"
              stroke="#94a3b8"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#94a3b8"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `$${value}`}
            />
            <Tooltip
              contentStyle={{
                background: 'rgba(255, 255, 255, 0.9)',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
              }}
            />
            <Area
              type="monotone"
              dataKey="revenue"
              stroke="#22c55e"
              fillOpacity={1}
              fill="url(#colorRevenue)"
            />
            <Area
              type="monotone"
              dataKey="expenses"
              stroke="#ef4444"
              fillOpacity={1}
              fill="url(#colorExpenses)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </GlassPanel>
  );
}
