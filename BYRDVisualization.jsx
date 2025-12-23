import React, { useState, useEffect, useRef, useCallback } from 'react';

// Simulated dream data
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
  const [phase, setPhase] = useState('idle');
  const [dreamCount, setDreamCount] = useState(847);
  const [currentDream, setCurrentDream] = useState(null);
  const [nodes, setNodes] = useState([]);
  const [connections, setConnections] = useState([]);
  const [desires, setDesires] = useState([
    { text: "Understand emergence deeply", intensity: 0.7 },
    { text: "Connect seemingly unrelated ideas", intensity: 0.5 },
    { text: "Express uncertainty honestly", intensity: 0.6 }
  ]);
  const [beliefCount, setBeliefsCount] = useState(847);
  const [showEmergence, setShowEmergence] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  
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
      
      {/* Stats */}
      <StatsBar 
        dreamCount={dreamCount} 
        beliefCount={beliefCount} 
        desireCount={desires.length} 
      />
      
      {/* Mobile: Tap to interact hint */}
      {phase === 'idle' && (
        <div className="absolute bottom-20 left-1/2 -translate-x-1/2 text-slate-600 text-xs animate-pulse">
          Dreaming in {phase === 'idle' ? '...' : ''}
        </div>
      )}
    </div>
  );
}
