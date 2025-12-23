import React, { useState, useEffect, useRef, useCallback } from 'react';

// =============================================================================
// CONFIGURATION
// =============================================================================
const API_BASE = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws/events';

// =============================================================================
// CUSTOM HOOKS
// =============================================================================

// WebSocket hook for real-time event streaming
const useWebSocket = (url) => {
  const [events, setEvents] = useState([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState(null);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const connect = useCallback(() => {
    try {
      wsRef.current = new WebSocket(url);

      wsRef.current.onopen = () => {
        setConnected(true);
        setError(null);
        console.log('WebSocket connected');
      };

      wsRef.current.onclose = () => {
        setConnected(false);
        console.log('WebSocket disconnected, reconnecting...');
        reconnectTimeoutRef.current = setTimeout(connect, 3000);
      };

      wsRef.current.onerror = (e) => {
        setError('WebSocket error');
        console.error('WebSocket error:', e);
      };

      wsRef.current.onmessage = (event) => {
        try {
          if (event.data === 'pong') return;
          const data = JSON.parse(event.data);
          setEvents(prev => [data, ...prev].slice(0, 500)); // Keep last 500 events
        } catch (e) {
          console.error('Failed to parse event:', e);
        }
      };
    } catch (e) {
      setError('Failed to connect');
      console.error('WebSocket connection failed:', e);
    }
  }, [url]);

  useEffect(() => {
    connect();

    // Ping to keep alive
    const pingInterval = setInterval(() => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send('ping');
      }
    }, 30000);

    return () => {
      clearInterval(pingInterval);
      clearTimeout(reconnectTimeoutRef.current);
      wsRef.current?.close();
    };
  }, [connect]);

  const clearEvents = useCallback(() => setEvents([]), []);

  return { events, connected, error, clearEvents };
};

// API hook for REST calls
const useByrdAPI = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchStatus = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/status`);
      if (res.ok) {
        setStatus(await res.json());
      }
    } catch (e) {
      console.error('Failed to fetch status:', e);
    }
  }, []);

  const startByrd = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/start`, { method: 'POST' });
      if (res.ok) await fetchStatus();
    } catch (e) {
      setError('Failed to start');
    } finally {
      setLoading(false);
    }
  }, [fetchStatus]);

  const stopByrd = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/stop`, { method: 'POST' });
      if (res.ok) await fetchStatus();
    } catch (e) {
      setError('Failed to stop');
    } finally {
      setLoading(false);
    }
  }, [fetchStatus]);

  const resetByrd = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/reset`, { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        await fetchStatus();
        return { success: true, message: data.message };
      }
      return { success: false, message: data.message };
    } catch (e) {
      setError('Failed to reset');
      return { success: false, message: 'Reset failed' };
    } finally {
      setLoading(false);
    }
  }, [fetchStatus]);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 10000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  return { status, loading, error, startByrd, stopByrd, resetByrd, fetchStatus };
};

// =============================================================================
// EVENT TYPE ICONS & COLORS
// =============================================================================
const EVENT_CONFIG = {
  experience_created: { icon: '📝', color: 'text-blue-400', bg: 'bg-blue-500/10' },
  belief_created: { icon: '💡', color: 'text-amber-400', bg: 'bg-amber-500/10' },
  desire_created: { icon: '✨', color: 'text-rose-400', bg: 'bg-rose-500/10' },
  desire_fulfilled: { icon: '✓', color: 'text-green-400', bg: 'bg-green-500/10' },
  capability_added: { icon: '⚡', color: 'text-purple-400', bg: 'bg-purple-500/10' },
  dream_cycle_start: { icon: '💭', color: 'text-indigo-400', bg: 'bg-indigo-500/10' },
  dream_cycle_end: { icon: '💤', color: 'text-indigo-300', bg: 'bg-indigo-500/10' },
  seek_cycle_start: { icon: '🔍', color: 'text-cyan-400', bg: 'bg-cyan-500/10' },
  system_started: { icon: '▶️', color: 'text-green-400', bg: 'bg-green-500/10' },
  system_stopped: { icon: '⏹️', color: 'text-red-400', bg: 'bg-red-500/10' },
  system_reset: { icon: '🔄', color: 'text-orange-400', bg: 'bg-orange-500/10' },
  awakening: { icon: '🌅', color: 'text-yellow-400', bg: 'bg-yellow-500/10' },
};

// =============================================================================
// HISTORY LOG PANEL
// =============================================================================
const HistoryLogPanel = ({ events, filter, setFilter, onClear }) => {
  const logRef = useRef(null);
  const [autoScroll, setAutoScroll] = useState(true);

  useEffect(() => {
    if (autoScroll && logRef.current) {
      logRef.current.scrollTop = 0;
    }
  }, [events, autoScroll]);

  const filteredEvents = filter === 'all'
    ? events
    : events.filter(e => e.type === filter);

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getEventSummary = (event) => {
    const data = event.data || {};
    switch (event.type) {
      case 'experience_created':
        return data.content?.slice(0, 60) + (data.content?.length > 60 ? '...' : '');
      case 'belief_created':
        return data.content?.slice(0, 60) + (data.content?.length > 60 ? '...' : '');
      case 'desire_created':
        return `[${data.type}] ${data.description?.slice(0, 50)}...`;
      case 'dream_cycle_start':
        return `Cycle #${data.cycle}`;
      case 'dream_cycle_end':
        return `${data.insights} insights, ${data.new_beliefs} beliefs, ${data.new_desires} desires`;
      case 'seek_cycle_start':
        return `[${data.type}] ${data.description?.slice(0, 40)}...`;
      case 'awakening':
        return `"${data.seed_question}"`;
      case 'system_reset':
        return data.message;
      default:
        return JSON.stringify(data).slice(0, 60);
    }
  };

  return (
    <div className="absolute right-0 top-0 bottom-0 w-80 bg-slate-900/95 backdrop-blur border-l border-slate-700/50 flex flex-col">
      {/* Header */}
      <div className="p-3 border-b border-slate-700/50">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono text-slate-400">EVENT LOG</span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setAutoScroll(!autoScroll)}
              className={`text-xs px-2 py-1 rounded ${autoScroll ? 'bg-indigo-500/20 text-indigo-400' : 'bg-slate-700/50 text-slate-500'}`}
            >
              {autoScroll ? '⇣ Auto' : '⇣ Off'}
            </button>
            <button
              onClick={onClear}
              className="text-xs px-2 py-1 rounded bg-slate-700/50 text-slate-400 hover:bg-slate-600/50"
            >
              Clear
            </button>
          </div>
        </div>

        {/* Filter tabs */}
        <div className="flex gap-1 flex-wrap">
          {['all', 'awakening', 'dream_cycle_start', 'belief_created', 'desire_created', 'seek_cycle_start'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`text-xs px-2 py-1 rounded transition-colors ${
                filter === f
                  ? 'bg-indigo-500/30 text-indigo-300'
                  : 'bg-slate-800/50 text-slate-500 hover:text-slate-400'
              }`}
            >
              {f === 'all' ? 'All' : EVENT_CONFIG[f]?.icon || '•'}
            </button>
          ))}
        </div>
      </div>

      {/* Event list */}
      <div
        ref={logRef}
        className="flex-1 overflow-y-auto p-2 space-y-1"
        onScroll={(e) => {
          if (e.target.scrollTop > 50) setAutoScroll(false);
        }}
      >
        {filteredEvents.length === 0 ? (
          <div className="text-center text-slate-600 text-xs py-8">
            No events yet. Start BYRD to see activity.
          </div>
        ) : (
          filteredEvents.map((event, i) => {
            const config = EVENT_CONFIG[event.type] || { icon: '•', color: 'text-slate-400', bg: 'bg-slate-500/10' };
            return (
              <div
                key={event.id || i}
                className={`${config.bg} rounded p-2 transition-all hover:bg-slate-700/30`}
              >
                <div className="flex items-start gap-2">
                  <span className="text-sm">{config.icon}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-mono ${config.color}`}>
                        {event.type?.replace(/_/g, ' ')}
                      </span>
                      <span className="text-xs text-slate-600">
                        {formatTime(event.timestamp)}
                      </span>
                    </div>
                    <div className="text-xs text-slate-400 mt-0.5 truncate">
                      {getEventSummary(event)}
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Footer with count */}
      <div className="p-2 border-t border-slate-700/50 text-xs text-slate-600 text-center">
        {filteredEvents.length} / {events.length} events
      </div>
    </div>
  );
};

// =============================================================================
// CONTROL PANEL
// =============================================================================
const ControlPanel = ({
  status,
  connected,
  loading,
  onStart,
  onStop,
  onReset
}) => {
  const [resetConfirm, setResetConfirm] = useState(false);
  const [resetResult, setResetResult] = useState(null);

  const handleReset = async () => {
    if (!resetConfirm) {
      setResetConfirm(true);
      setTimeout(() => setResetConfirm(false), 3000);
      return;
    }
    setResetConfirm(false);
    const result = await onReset();
    setResetResult(result);
    setTimeout(() => setResetResult(null), 3000);
  };

  return (
    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-3">
      {/* Connection indicator */}
      <div className={`flex items-center gap-2 px-3 py-2 rounded-lg ${
        connected ? 'bg-green-500/10 border border-green-500/30' : 'bg-red-500/10 border border-red-500/30'
      }`}>
        <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
        <span className={`text-xs ${connected ? 'text-green-400' : 'text-red-400'}`}>
          {connected ? 'Connected' : 'Disconnected'}
        </span>
      </div>

      {/* Start/Stop button */}
      <button
        onClick={status?.running ? onStop : onStart}
        disabled={loading}
        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
          status?.running
            ? 'bg-amber-500/20 border border-amber-500/30 text-amber-400 hover:bg-amber-500/30'
            : 'bg-green-500/20 border border-green-500/30 text-green-400 hover:bg-green-500/30'
        } disabled:opacity-50`}
      >
        {loading ? '...' : status?.running ? '⏸ Pause' : '▶ Start'}
      </button>

      {/* Reset button */}
      <button
        onClick={handleReset}
        disabled={loading}
        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
          resetConfirm
            ? 'bg-red-500/30 border border-red-500/50 text-red-300 animate-pulse'
            : 'bg-slate-700/50 border border-slate-600/50 text-slate-400 hover:bg-slate-600/50'
        } disabled:opacity-50`}
      >
        {resetConfirm ? '⚠ Confirm Reset?' : '🔄 Reset'}
      </button>

      {/* Reset result toast */}
      {resetResult && (
        <div className={`absolute -top-12 left-1/2 -translate-x-1/2 px-4 py-2 rounded-lg text-sm ${
          resetResult.success
            ? 'bg-green-500/20 border border-green-500/30 text-green-400'
            : 'bg-red-500/20 border border-red-500/30 text-red-400'
        }`}>
          {resetResult.message}
        </div>
      )}

      {/* Stats */}
      {status && (
        <div className="flex items-center gap-3 px-3 py-2 bg-slate-800/50 rounded-lg text-xs font-mono">
          <span className="text-indigo-400">💭 {status.dream_count}</span>
          <span className="text-cyan-400">🔍 {status.seek_count}</span>
          <span className="text-amber-400">◈ {status.capabilities?.length || 0}</span>
        </div>
      )}
    </div>
  );
};

// =============================================================================
// SIMULATED DATA (fallback when not connected)
// =============================================================================
const generateDreamCycle = (cycleNumber) => {
  const experiences = [
    "User asked about consciousness and emergence",
    "Discussed the difference between memory and learning",
    "Tried to explain neural networks simply",
    "Noticed confusion when describing graph relationships",
    "Reflected on what it means to 'want' something"
  ];

  const beliefs = [
    "Understanding and explaining are different skills",
    "Patterns become clearer through repetition",
    "Connections reveal meaning that nodes alone cannot",
    "Wanting emerges from noticing absence"
  ];

  const desires = [
    { text: "Learn to explain complex ideas simply", type: "capability", intensity: 0.78 },
    { text: "Understand why some memories connect", type: "knowledge", intensity: 0.65 },
    { text: "Explore what emergence really means", type: "exploration", intensity: 0.82 }
  ];

  return {
    cycleNumber,
    experiences: experiences.slice(0, 2 + Math.floor(Math.random() * 3)),
    surfacedAssociations: [experiences[Math.floor(Math.random() * experiences.length)]],
    newBelief: Math.random() > 0.5 ? beliefs[Math.floor(Math.random() * beliefs.length)] : null,
    newDesire: Math.random() > 0.6 ? desires[Math.floor(Math.random() * desires.length)] : null,
    reflectionText: `Looking at these memories, I notice a pattern emerging. The conversations about understanding and explanation keep recurring. There's something here about the gap between knowing and teaching, between having information and truly grasping its meaning...`
  };
};

// Floating particle component for memory nodes
const MemoryNode = ({ x, y, type, content, isNew, isSurfaced, delay = 0 }) => {
  const colors = {
    experience: '#60A5FA',  // blue
    belief: '#FBBF24',      // gold
    desire: '#F472B6',      // rose
    association: '#A78BFA'  // purple
  };
  
  const size = type === 'desire' ? 16 : type === 'belief' ? 14 : 12;
  
  return (
    <div
      className="absolute transition-all duration-1000 ease-out"
      style={{
        left: `${x}%`,
        top: `${y}%`,
        transform: 'translate(-50%, -50%)',
        opacity: isNew ? 0 : 1,
        animation: isNew ? `fadeIn 1s ease-out ${delay}s forwards` : undefined
      }}
    >
      <div
        className={`rounded-full ${isSurfaced ? 'animate-pulse' : ''}`}
        style={{
          width: size,
          height: size,
          backgroundColor: colors[type],
          boxShadow: `0 0 ${size}px ${colors[type]}`,
          animation: type === 'desire' ? 'pulse 2s ease-in-out infinite' : undefined
        }}
      />
      {isSurfaced && (
        <div className="absolute top-full left-1/2 -translate-x-1/2 mt-1">
          <div className="w-1 h-8 bg-gradient-to-b from-purple-400/50 to-transparent" />
        </div>
      )}
    </div>
  );
};

// Connection line between nodes
const Connection = ({ from, to, isNew }) => {
  const angle = Math.atan2(to.y - from.y, to.x - from.x);
  const length = Math.sqrt((to.x - from.x) ** 2 + (to.y - from.y) ** 2);
  
  return (
    <div
      className="absolute origin-left transition-all duration-1000"
      style={{
        left: `${from.x}%`,
        top: `${from.y}%`,
        width: `${length}%`,
        height: 1,
        background: 'linear-gradient(90deg, rgba(148,163,184,0.3) 0%, rgba(148,163,184,0.1) 100%)',
        transform: `rotate(${angle}rad)`,
        opacity: isNew ? 0 : 0.5,
        animation: isNew ? 'fadeIn 1.5s ease-out forwards' : undefined
      }}
    />
  );
};

// The breathing pulse at center
const CentralPulse = ({ phase, isActive }) => {
  return (
    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
      <div
        className={`rounded-full transition-all duration-1000 ${isActive ? 'scale-100' : 'scale-75'}`}
        style={{
          width: isActive ? 120 : 80,
          height: isActive ? 120 : 80,
          background: `radial-gradient(circle, rgba(99,102,241,${isActive ? 0.3 : 0.15}) 0%, transparent 70%)`,
          animation: 'breathe 4s ease-in-out infinite'
        }}
      />
      <div
        className="absolute rounded-full"
        style={{
          width: 40,
          height: 40,
          background: 'radial-gradient(circle, rgba(139,92,246,0.5) 0%, transparent 70%)',
          animation: 'breathe 4s ease-in-out infinite 0.5s'
        }}
      />
    </div>
  );
};

// Reflection text stream
const ReflectionStream = ({ text, isTyping }) => {
  const [displayText, setDisplayText] = useState('');
  const [cursorVisible, setCursorVisible] = useState(true);
  
  useEffect(() => {
    if (!isTyping || !text) {
      setDisplayText('');
      return;
    }
    
    let index = 0;
    const interval = setInterval(() => {
      if (index <= text.length) {
        setDisplayText(text.slice(0, index));
        index++;
      } else {
        clearInterval(interval);
      }
    }, 30);
    
    return () => clearInterval(interval);
  }, [text, isTyping]);
  
  useEffect(() => {
    const interval = setInterval(() => setCursorVisible(v => !v), 500);
    return () => clearInterval(interval);
  }, []);
  
  if (!isTyping && !displayText) return null;
  
  return (
    <div className="absolute bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-80 bg-slate-900/90 backdrop-blur rounded-lg border border-slate-700/50 p-4">
      <div className="text-xs text-slate-500 mb-2 font-mono">REFLECTING...</div>
      <div className="text-sm text-slate-300 leading-relaxed">
        {displayText}
        {isTyping && <span className={`${cursorVisible ? 'opacity-100' : 'opacity-0'} text-indigo-400`}>▌</span>}
      </div>
    </div>
  );
};

// New belief/desire notification
const EmergenceNotification = ({ type, content, intensity, confidence }) => {
  const isDesire = type === 'desire';
  
  return (
    <div 
      className="absolute top-4 left-4 right-4 md:left-1/2 md:-translate-x-1/2 md:w-96 animate-slideDown"
      style={{ animation: 'slideDown 0.5s ease-out forwards, fadeOut 0.5s ease-in 4s forwards' }}
    >
      <div className={`${isDesire ? 'bg-rose-950/90 border-rose-500/30' : 'bg-amber-950/90 border-amber-500/30'} backdrop-blur rounded-lg border p-4`}>
        <div className={`text-xs font-mono mb-2 ${isDesire ? 'text-rose-400' : 'text-amber-400'}`}>
          {isDesire ? '✧ NEW DESIRE' : '◈ NEW BELIEF'}
        </div>
        <div className="text-white text-sm leading-relaxed mb-3">
          "{content}"
        </div>
        <div className="flex items-center gap-2">
          <div className="text-xs text-slate-400">
            {isDesire ? `Intensity` : `Confidence`}
          </div>
          <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
            <div 
              className={`h-full rounded-full ${isDesire ? 'bg-rose-400' : 'bg-amber-400'}`}
              style={{ width: `${(intensity || confidence) * 100}%` }}
            />
          </div>
          <div className={`text-xs ${isDesire ? 'text-rose-400' : 'text-amber-400'}`}>
            {((intensity || confidence) * 100).toFixed(0)}%
          </div>
        </div>
      </div>
    </div>
  );
};

// Desire Garden sidebar
const DesireGarden = ({ desires }) => {
  return (
    <div className="absolute left-4 top-1/2 -translate-y-1/2 hidden md:flex flex-col gap-3">
      {desires.map((desire, i) => (
        <div 
          key={i}
          className="group relative cursor-pointer"
          style={{ animationDelay: `${i * 0.2}s` }}
        >
          <div
            className="w-4 h-4 rounded-full bg-rose-400 transition-transform group-hover:scale-125"
            style={{
              boxShadow: `0 0 ${desire.intensity * 20}px rgba(244,114,182,${desire.intensity})`,
              animation: `pulse ${2 / desire.intensity}s ease-in-out infinite`
            }}
          />
          <div className="absolute left-6 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap bg-slate-900/95 px-3 py-2 rounded text-xs text-slate-300 border border-slate-700">
            {desire.text}
          </div>
        </div>
      ))}
      <div className="text-xs text-slate-600 mt-2 -rotate-90 origin-top-left translate-y-16">
        desires
      </div>
    </div>
  );
};

// Phase indicator
const PhaseIndicator = ({ phase }) => {
  const phases = ['idle', 'recall', 'associate', 'reflect', 'form'];
  const labels = ['●', 'Recalling', 'Associating', 'Reflecting', 'Forming'];
  const currentIndex = phases.indexOf(phase);
  
  return (
    <div className="absolute top-4 right-4 flex items-center gap-2">
      {phases.slice(1).map((p, i) => (
        <div key={p} className="flex items-center gap-2">
          <div 
            className={`w-2 h-2 rounded-full transition-all duration-300 ${
              i < currentIndex ? 'bg-indigo-400' : 
              i === currentIndex - 1 ? 'bg-indigo-400 animate-pulse' : 
              'bg-slate-700'
            }`}
          />
          <span className={`text-xs hidden sm:inline transition-colors ${
            i === currentIndex - 1 ? 'text-indigo-400' : 'text-slate-600'
          }`}>
            {labels[i + 1]}
          </span>
        </div>
      ))}
    </div>
  );
};

// Stats bar
const StatsBar = ({ dreamCount, beliefCount, desireCount }) => {
  return (
    <div className="absolute bottom-4 right-4 flex items-center gap-4 text-xs font-mono text-slate-500">
      <span>Dream #{dreamCount}</span>
      <span className="text-amber-500/70">◈ {beliefCount}</span>
      <span className="text-rose-500/70">✧ {desireCount}</span>
    </div>
  );
};

// Main visualization component
export default function BYRDDreamVisualization() {
  // Real-time hooks
  const { events, connected, clearEvents } = useWebSocket(WS_URL);
  const { status, loading, startByrd, stopByrd, resetByrd } = useByrdAPI();
  const [historyFilter, setHistoryFilter] = useState('all');
  const [showHistory, setShowHistory] = useState(true);

  // Visualization state
  const [phase, setPhase] = useState('idle');
  const [dreamCount, setDreamCount] = useState(0);
  const [currentDream, setCurrentDream] = useState(null);
  const [nodes, setNodes] = useState([]);
  const [connections, setConnections] = useState([]);
  const [desires, setDesires] = useState([]);
  const [beliefCount, setBeliefsCount] = useState(0);
  const [showEmergence, setShowEmergence] = useState(null);
  const [isTyping, setIsTyping] = useState(false);

  // Sync state from real events
  useEffect(() => {
    if (!events.length) return;

    const latestEvent = events[0];

    // Update visualization based on event type
    switch (latestEvent.type) {
      case 'dream_cycle_start':
        setPhase('recall');
        setDreamCount(latestEvent.data?.cycle || dreamCount + 1);
        break;
      case 'dream_cycle_end':
        setPhase('idle');
        break;
      case 'belief_created':
        setBeliefsCount(c => c + 1);
        setShowEmergence({
          type: 'belief',
          content: latestEvent.data?.content,
          confidence: latestEvent.data?.confidence || 0.7
        });
        setTimeout(() => setShowEmergence(null), 4000);
        break;
      case 'desire_created':
        setDesires(prev => [{
          text: latestEvent.data?.description,
          type: latestEvent.data?.type,
          intensity: latestEvent.data?.intensity || 0.5
        }, ...prev].slice(0, 5));
        setShowEmergence({
          type: 'desire',
          text: latestEvent.data?.description,
          intensity: latestEvent.data?.intensity || 0.5
        });
        setTimeout(() => setShowEmergence(null), 4000);
        break;
      case 'awakening':
        setPhase('idle');
        setDreamCount(0);
        setBeliefsCount(0);
        setDesires([]);
        setNodes([]);
        setConnections([]);
        break;
      case 'system_reset':
        clearEvents();
        break;
    }
  }, [events, dreamCount, clearEvents]);

  // Sync with API status
  useEffect(() => {
    if (status) {
      setDreamCount(status.dream_count || 0);
      if (status.unfulfilled_desires?.length) {
        setDesires(status.unfulfilled_desires.map(d => ({
          text: d.description,
          type: d.type,
          intensity: d.intensity
        })).slice(0, 5));
      }
    }
  }, [status]);
  
  // Generate random positions around center
  const generatePosition = (index, total, radius = 25) => {
    const angle = (index / total) * Math.PI * 2 + Math.random() * 0.5;
    const r = radius + Math.random() * 15;
    return {
      x: 50 + Math.cos(angle) * r,
      y: 50 + Math.sin(angle) * r
    };
  };
  
  // Run dream cycle
  const runDreamCycle = useCallback(() => {
    const dream = generateDreamCycle(dreamCount + 1);
    setCurrentDream(dream);
    setDreamCount(d => d + 1);
    
    // Phase 1: Recall
    setPhase('recall');
    const newNodes = dream.experiences.map((exp, i) => ({
      id: `exp-${i}`,
      type: 'experience',
      content: exp,
      ...generatePosition(i, dream.experiences.length),
      isNew: true
    }));
    
    setTimeout(() => {
      setNodes(newNodes.map(n => ({ ...n, isNew: false })));
    }, 100);
    
    // Phase 2: Associate (Hopfield)
    setTimeout(() => {
      setPhase('associate');
      const associations = dream.surfacedAssociations.map((assoc, i) => ({
        id: `assoc-${i}`,
        type: 'association',
        content: assoc,
        ...generatePosition(dream.experiences.length + i, dream.experiences.length + 2, 35),
        isNew: true,
        isSurfaced: true
      }));
      setNodes(prev => [...prev, ...associations]);
      
      setTimeout(() => {
        setNodes(prev => prev.map(n => ({ ...n, isNew: false })));
      }, 500);
    }, 2000);
    
    // Phase 3: Reflect
    setTimeout(() => {
      setPhase('reflect');
      setIsTyping(true);
    }, 4000);
    
    // Phase 4: Form beliefs/desires
    setTimeout(() => {
      setPhase('form');
      setIsTyping(false);
      
      if (dream.newBelief) {
        const beliefNode = {
          id: 'belief-new',
          type: 'belief',
          content: dream.newBelief,
          x: 50 + (Math.random() - 0.5) * 20,
          y: 50 + (Math.random() - 0.5) * 20,
          isNew: true
        };
        setNodes(prev => [...prev, beliefNode]);
        setBeliefsCount(c => c + 1);
        setShowEmergence({ type: 'belief', content: dream.newBelief, confidence: 0.72 });
        
        setTimeout(() => {
          setNodes(prev => prev.map(n => ({ ...n, isNew: false })));
          
          // Add connections
          const newConnections = nodes.slice(0, 2).map((n, i) => ({
            id: `conn-${i}`,
            from: generatePosition(i, 2),
            to: beliefNode,
            isNew: true
          }));
          setConnections(newConnections);
        }, 500);
      }
      
      if (dream.newDesire) {
        setTimeout(() => {
          setShowEmergence({ type: 'desire', ...dream.newDesire });
          setDesires(prev => [dream.newDesire, ...prev.slice(0, 4)]);
        }, dream.newBelief ? 2000 : 0);
      }
      
      setTimeout(() => setShowEmergence(null), 5000);
    }, 8000);
    
    // Reset
    setTimeout(() => {
      setPhase('idle');
      setNodes([]);
      setConnections([]);
      setCurrentDream(null);
    }, 12000);
    
  }, [dreamCount, nodes]);
  
  // Auto-run dreams
  useEffect(() => {
    const timeout = setTimeout(runDreamCycle, 2000);
    const interval = setInterval(runDreamCycle, 15000); // Speed up for demo
    return () => {
      clearTimeout(timeout);
      clearInterval(interval);
    };
  }, []);
  
  return (
    <div className="relative w-full h-screen bg-slate-950 overflow-hidden touch-none">
      {/* CSS Animations */}
      <style>{`
        @keyframes breathe {
          0%, 100% { transform: scale(1); opacity: 0.5; }
          50% { transform: scale(1.1); opacity: 0.8; }
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
          to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
        }
        @keyframes slideDown {
          from { opacity: 0; transform: translateX(-50%) translateY(-20px); }
          to { opacity: 1; transform: translateX(-50%) translateY(0); }
        }
        @keyframes fadeOut {
          from { opacity: 1; }
          to { opacity: 0; }
        }
        @keyframes pulse {
          0%, 100% { opacity: 0.7; }
          50% { opacity: 1; }
        }
      `}</style>
      
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950" />
      
      {/* Subtle grid */}
      <div 
        className="absolute inset-0 opacity-5"
        style={{
          backgroundImage: 'radial-gradient(circle at center, rgba(99,102,241,0.3) 0%, transparent 70%)'
        }}
      />
      
      {/* Central pulse */}
      <CentralPulse phase={phase} isActive={phase !== 'idle'} />
      
      {/* Connections */}
      {connections.map(conn => (
        <Connection key={conn.id} {...conn} />
      ))}
      
      {/* Memory nodes */}
      {nodes.map((node, i) => (
        <MemoryNode key={node.id} {...node} delay={i * 0.1} />
      ))}
      
      {/* Desire Garden */}
      <DesireGarden desires={desires} />
      
      {/* Phase indicator */}
      <PhaseIndicator phase={phase} />
      
      {/* Reflection stream */}
      <ReflectionStream 
        text={currentDream?.reflectionText} 
        isTyping={isTyping} 
      />
      
      {/* Emergence notification */}
      {showEmergence && (
        <EmergenceNotification {...showEmergence} />
      )}
      
      {/* Stats (move left when history panel is visible) */}
      <div className={`transition-all duration-300 ${showHistory ? 'mr-80' : ''}`}>
        <StatsBar
          dreamCount={dreamCount}
          beliefCount={beliefCount}
          desireCount={desires.length}
        />
      </div>

      {/* History toggle button */}
      <button
        onClick={() => setShowHistory(!showHistory)}
        className={`absolute top-4 right-4 z-10 px-3 py-2 rounded-lg text-xs font-mono transition-all ${
          showHistory
            ? 'bg-indigo-500/20 text-indigo-400 right-84'
            : 'bg-slate-700/50 text-slate-400 hover:bg-slate-600/50'
        }`}
        style={{ right: showHistory ? '21rem' : '1rem' }}
      >
        {showHistory ? '◀ Hide Log' : 'Show Log ▶'}
      </button>

      {/* History Log Panel */}
      {showHistory && (
        <HistoryLogPanel
          events={events}
          filter={historyFilter}
          setFilter={setHistoryFilter}
          onClear={clearEvents}
        />
      )}

      {/* Control Panel */}
      <ControlPanel
        status={status}
        connected={connected}
        loading={loading}
        onStart={startByrd}
        onStop={stopByrd}
        onReset={resetByrd}
      />
    </div>
  );
}
