import { Outlet } from 'react-router-dom';
import type { ReactNode } from 'react';
import { BottomTabBar } from './BottomTabBar';
import { Header } from './Header';

interface MobileLayoutProps {
  children?: ReactNode;
}

export function MobileLayout({ children }: MobileLayoutProps) {
  return (
    <div className="flex flex-col h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header */}
      <Header />

      {/* Main Content - Scrolls independently */}
      <main className="flex-1 overflow-y-auto overflow-x-hidden">
        {children || <Outlet />}
      </main>

      {/* Bottom Tab Bar - Fixed */}
      <BottomTabBar />
    </div>
  );
}
