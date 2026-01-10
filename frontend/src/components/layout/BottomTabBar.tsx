/**
 * BottomTabBar - Observatory Style Navigation
 */

import { useLocation, useNavigate } from 'react-router-dom';
import { Home, MessageSquare, GitBranch, Network, DollarSign, MoreHorizontal } from 'lucide-react';
import { cn } from '@lib/utils/cn';
import type { TabRoute } from '../../types/ui';

interface TabItem {
  route: TabRoute;
  path: string;
  label: string;
  icon: React.ComponentType<{ className?: string; strokeWidth?: number }>;
}

const tabs: TabItem[] = [
  { route: 'home' as TabRoute, path: '/home', label: 'HOME', icon: Home },
  { route: 'byrd' as TabRoute, path: '/byrd', label: 'BYRD', icon: MessageSquare },
  { route: 'rsi' as TabRoute, path: '/rsi', label: 'RSI', icon: GitBranch },
  { route: 'memory' as TabRoute, path: '/memory', label: 'MEM', icon: Network },
  { route: 'economic' as TabRoute, path: '/economic', label: 'ECON', icon: DollarSign },
  { route: 'more' as TabRoute, path: '/more', label: 'MORE', icon: MoreHorizontal },
];

export function BottomTabBar() {
  const navigate = useNavigate();
  const location = useLocation();

  const currentTab = tabs.find(t => location.pathname === t.path);

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-[var(--obs-bg-surface)] border-t border-[var(--obs-border)]">
      <div className="flex items-center justify-around h-16 max-w-lg mx-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab?.route === tab.route;

          return (
            <button
              key={tab.route}
              onClick={() => navigate(tab.path)}
              className={cn(
                "flex flex-col items-center justify-center flex-1 h-full relative transition-all duration-150",
                "active:scale-95 active:opacity-80",
                isActive
                  ? "text-[var(--data-stream)]"
                  : "text-[var(--obs-text-tertiary)] hover:text-[var(--obs-text-secondary)]"
              )}
              aria-label={tab.label}
              aria-current={isActive ? 'page' : undefined}
            >
              <Icon
                className={cn("w-5 h-5", isActive && "drop-shadow-[0_0_8px_var(--data-stream)]")}
                strokeWidth={isActive ? 2.5 : 2}
              />
              <span className="obs-label text-[9px] mt-1 tracking-wider">{tab.label}</span>

              {isActive && (
                <span className="absolute -top-0.5 left-1/2 -translate-x-1/2 w-10 h-0.5 bg-[var(--data-stream)] rounded-full shadow-[0_0_8px_var(--data-stream-glow)]" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
