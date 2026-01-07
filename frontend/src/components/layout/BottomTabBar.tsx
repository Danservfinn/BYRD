import { useLocation, useNavigate } from 'react-router-dom';
import { Home, MessageSquare, GitBranch, Network, DollarSign, MoreHorizontal } from 'lucide-react';
import { cn } from '@lib/utils/cn';
import type { TabRoute } from '../../types/ui';

interface TabItem {
  route: TabRoute;
  path: string;
  label: string;
  icon: any;
}

const tabs: TabItem[] = [
  { route: 'home' as TabRoute, path: '/home', label: 'Home', icon: Home },
  { route: 'byrd' as TabRoute, path: '/byrd', label: 'BYRD', icon: MessageSquare },
  { route: 'rsi' as TabRoute, path: '/rsi', label: 'RSI', icon: GitBranch },
  { route: 'memory' as TabRoute, path: '/memory', label: 'Memory', icon: Network },
  { route: 'economic' as TabRoute, path: '/economic', label: 'Economic', icon: DollarSign },
  { route: 'more' as TabRoute, path: '/more', label: 'More', icon: MoreHorizontal },
];

export function BottomTabBar() {
  const navigate = useNavigate();
  const location = useLocation();

  const currentTab = tabs.find(t => location.pathname === t.path);

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-700">
      <div className="flex items-center justify-around h-16 max-w-lg mx-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab?.route === tab.route;

          return (
            <button
              key={tab.route}
              onClick={() => navigate(tab.path)}
              className={cn(
                "flex flex-col items-center justify-center flex-1 h-full relative transition-colors duration-150",
                "active:scale-95 active:opacity-80",
                isActive ? "text-purple-600 dark:text-purple-400" : "text-slate-500 dark:text-slate-400"
              )}
              aria-label={tab.label}
              aria-current={isActive ? 'page' : undefined}
            >
              <Icon className="w-6 h-6" strokeWidth={isActive ? 2.5 : 2} />
              <span className="text-xs mt-1 font-medium">{tab.label}</span>

              {isActive && (
                <span className="absolute -top-0.5 left-1/2 -translate-x-1/2 w-12 h-0.5 bg-purple-600 dark:bg-purple-400 rounded-full" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
