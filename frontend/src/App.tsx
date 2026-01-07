import { HashRouter, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import { AppLayout } from './components/layout';
import { DashboardPage } from './components/dashboard';
import { RSIPage } from './components/rsi';
import { EconomicPage } from './components/economic';
import { PlasticityPage } from './components/plasticity';
import { ScalingPage } from './components/scaling';
import { VerificationPage } from './components/verification';
import { ControlPanel } from './components/controls';
import { MemoryTopology } from './components/visualization';
import { useWebSocket } from './hooks/useWebSocket';
import './App.css';

function AppContent() {
  // Initialize WebSocket connection
  const { isConnected } = useWebSocket();

  useEffect(() => {
    console.log(`WebSocket connection status: ${isConnected ? 'connected' : 'disconnected'}`);
  }, [isConnected]);

  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/rsi" element={<RSIPage />} />
        <Route path="/economic" element={<EconomicPage />} />
        <Route path="/plasticity" element={<PlasticityPage />} />
        <Route path="/scaling" element={<ScalingPage />} />
        <Route path="/verification" element={<VerificationPage />} />
        <Route path="/controls" element={<ControlPanel />} />
        <Route path="/visualization" element={<MemoryTopology />} />
      </Routes>
    </AppLayout>
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
