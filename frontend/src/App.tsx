import { HashRouter, Routes, Route } from 'react-router-dom';
import { lazy, Suspense, useEffect, useState } from 'react';
import { MobileLayout } from './components/layout/MobileLayout';
import { useWebSocket } from './hooks/useWebSocket';
import { useByrdAPI } from './hooks/useByrdAPI';
import { LoadingSpinner } from './components/common/LoadingSpinner';
import { DemoModeBanner } from './components/common/DemoModeBanner';
import './index.css';

// Lazy load page components for better performance
const DashboardPage = lazy(() => import('./components/dashboard/DashboardPage').then(m => ({ default: m.DashboardPage })));
const ByrdChatPage = lazy(() => import('./components/byrd/ByrdChatPage').then(m => ({ default: m.ByrdChatPage })));
const RSIPage = lazy(() => import('./components/rsi/RSIPage').then(m => ({ default: m.RSIPage })));
const MemoryPage = lazy(() => import('./components/memory/MemoryPage').then(m => ({ default: m.MemoryPage })));
const EconomicPage = lazy(() => import('./components/economic/EconomicPage').then(m => ({ default: m.EconomicPage })));
const MorePage = lazy(() => import('./components/more/MorePage').then(m => ({ default: m.MorePage })));

// Loading fallback component
function PageLoader() {
  return (
    <div className="flex items-center justify-center h-screen bg-slate-50 dark:bg-slate-900">
      <LoadingSpinner size="lg" />
    </div>
  );
}

function AppContent() {
  // Initialize WebSocket connection and check backend availability
  const { isConnected } = useWebSocket();
  const { backendAvailable } = useByrdAPI();
  const [bannerDismissed, setBannerDismissed] = useState(false);

  useEffect(() => {
    console.log(`WebSocket connection status: ${isConnected ? 'connected' : 'disconnected'}`);
  }, [isConnected]);

  const showDemoBanner = backendAvailable === false && !bannerDismissed;

  return (
    <>
      {showDemoBanner && <DemoModeBanner onDismiss={() => setBannerDismissed(true)} />}
      <Suspense fallback={<PageLoader />}>
        <MobileLayout>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/home" element={<DashboardPage />} />
            <Route path="/byrd" element={<ByrdChatPage />} />
            <Route path="/rsi" element={<RSIPage />} />
            <Route path="/memory" element={<MemoryPage />} />
            <Route path="/economic" element={<EconomicPage />} />
            <Route path="/more" element={<MorePage />} />
          </Routes>
        </MobileLayout>
      </Suspense>
    </>
  );
}

function App() {
  return (
    <HashRouter>
      <AppContent />
    </HashRouter>
  );
}

export default App;
