import { HashRouter, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import { MobileLayout } from './components/layout/MobileLayout';
import { DashboardPage } from './components/dashboard/DashboardPage';
import { ByrdChatPage } from './components/byrd/ByrdChatPage';
import { RSIPage } from './components/rsi/RSIPage';
import { MemoryPage } from './components/memory/MemoryPage';
import { EconomicPage } from './components/economic/EconomicPage';
import { MorePage } from './components/more/MorePage';
import { useWebSocket } from './hooks/useWebSocket';
import './index.css';

function AppContent() {
  // Initialize WebSocket connection
  const { isConnected } = useWebSocket();

  useEffect(() => {
    console.log(`WebSocket connection status: ${isConnected ? 'connected' : 'disconnected'}`);
  }, [isConnected]);

  return (
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
