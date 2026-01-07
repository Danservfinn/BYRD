import { useEffect, useRef, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';

interface ModuleNode {
  id: string;
  name: string;
  type: 'core' | 'emergent' | 'composed';
  x: number;
  y: number;
}

interface ModuleLink {
  source: string;
  target: string;
  strength: number;
}

export function CompositionGraph() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { getPlasticityModules } = useByrdAPI();
  const [nodes, setNodes] = useState<ModuleNode[]>([]);
  const [links, setLinks] = useState<ModuleLink[]>([]);

  useEffect(() => {
    const fetch = async () => {
      const result = await getPlasticityModules();
      if (result?.graph) {
        // Type assertion to ensure nodes match ModuleNode interface
        setNodes((result.graph.nodes || []).map(n => ({
          ...n,
          type: (n.type as 'core' | 'emergent' | 'composed') || 'emergent'
        })));
        setLinks(result.graph.links || []);
      }
    };
    fetch();
    const interval = setInterval(fetch, 10000);
    return () => clearInterval(interval);
  }, [getPlasticityModules]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.fillStyle = 'rgba(15, 23, 42, 0.02)';
    ctx.fillRect(0, 0, width, height);

    if (nodes.length === 0) {
      // Draw placeholder
      ctx.fillStyle = '#94a3b8';
      ctx.font = '14px system-ui';
      ctx.textAlign = 'center';
      ctx.fillText('Module composition graph will appear here', width / 2, height / 2);
      return;
    }

    const nodePositions: Record<string, { x: number; y: number }> = {};

    // Position nodes in a circle if no positions provided
    nodes.forEach((node, i) => {
      const angle = (i / nodes.length) * Math.PI * 2;
      const radius = Math.min(width, height) * 0.35;
      nodePositions[node.id] = {
        x: node.x || width / 2 + Math.cos(angle) * radius,
        y: node.y || height / 2 + Math.sin(angle) * radius,
      };
    });

    // Draw links
    links.forEach((link) => {
      const source = nodePositions[link.source];
      const target = nodePositions[link.target];
      if (!source || !target) return;

      ctx.beginPath();
      ctx.moveTo(source.x, source.y);
      ctx.lineTo(target.x, target.y);
      ctx.strokeStyle = `rgba(139, 92, 246, ${link.strength * 0.5})`;
      ctx.lineWidth = link.strength * 3;
      ctx.stroke();
    });

    // Draw nodes
    const typeColors: Record<string, string> = {
      core: '#3b82f6',
      emergent: '#a855f7',
      composed: '#06b6d4',
    };

    nodes.forEach((node) => {
      const pos = nodePositions[node.id];
      if (!pos) return;

      // Node circle
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, 12, 0, Math.PI * 2);
      ctx.fillStyle = typeColors[node.type] || '#64748b';
      ctx.fill();

      // Node border
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Node label
      ctx.fillStyle = '#e2e8f0';
      ctx.font = '11px system-ui';
      ctx.textAlign = 'center';
      ctx.fillText(node.name, pos.x, pos.y + 28);
    });
  }, [nodes, links]);

  return (
    <GlassPanel glow="purple" padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Module Composition Graph
      </h2>

      <div className="relative rounded-lg overflow-hidden bg-slate-900/50">
        <canvas
          ref={canvasRef}
          width={800}
          height={400}
          className="w-full h-64"
        />
      </div>

      <div className="flex items-center justify-center gap-6 mt-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-blue-500" />
          <span className="text-slate-500">Core</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-purple-500" />
          <span className="text-slate-500">Emergent</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-cyan-500" />
          <span className="text-slate-500">Composed</span>
        </div>
      </div>
    </GlassPanel>
  );
}
