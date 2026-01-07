import { useEffect, useRef, useCallback } from 'react';
import type { GraphData, GraphNode } from './MemoryTopology';

interface ForceGraph3DProps {
  data: GraphData;
  onNodeClick?: (node: GraphNode) => void;
  typeColors: Record<string, string>;
}

// Simulation node with position
interface SimNode extends GraphNode {
  x: number;
  y: number;
  z: number;
  vx: number;
  vy: number;
  vz: number;
}

export function ForceGraph3D({ data, onNodeClick, typeColors }: ForceGraph3DProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number | undefined>(undefined);
  const nodesRef = useRef<SimNode[]>([]);
  const rotationRef = useRef({ x: 0, y: 0 });
  const isDragging = useRef(false);
  const lastMouse = useRef({ x: 0, y: 0 });

  // Initialize nodes with random positions
  useEffect(() => {
    nodesRef.current = data.nodes.map((node) => ({
      ...node,
      x: (Math.random() - 0.5) * 200,
      y: (Math.random() - 0.5) * 200,
      z: (Math.random() - 0.5) * 200,
      vx: 0,
      vy: 0,
      vz: 0,
    }));
  }, [data.nodes]);

  // Force simulation step
  const simulate = useCallback(() => {
    const nodes = nodesRef.current;
    const links = data.links;

    // Apply forces
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i];

      // Repulsion between nodes
      for (let j = i + 1; j < nodes.length; j++) {
        const other = nodes[j];
        const dx = other.x - node.x;
        const dy = other.y - node.y;
        const dz = other.z - node.z;
        const dist = Math.sqrt(dx * dx + dy * dy + dz * dz) || 1;
        const force = 500 / (dist * dist);

        node.vx -= (dx / dist) * force;
        node.vy -= (dy / dist) * force;
        node.vz -= (dz / dist) * force;
        other.vx += (dx / dist) * force;
        other.vy += (dy / dist) * force;
        other.vz += (dz / dist) * force;
      }

      // Centering force
      node.vx -= node.x * 0.01;
      node.vy -= node.y * 0.01;
      node.vz -= node.z * 0.01;
    }

    // Link attraction
    for (const link of links) {
      const source = nodes.find((n) => n.id === link.source);
      const target = nodes.find((n) => n.id === link.target);
      if (!source || !target) continue;

      const dx = target.x - source.x;
      const dy = target.y - source.y;
      const dz = target.z - source.z;
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz) || 1;
      const force = (dist - 50) * 0.01 * link.weight;

      source.vx += (dx / dist) * force;
      source.vy += (dy / dist) * force;
      source.vz += (dz / dist) * force;
      target.vx -= (dx / dist) * force;
      target.vy -= (dy / dist) * force;
      target.vz -= (dz / dist) * force;
    }

    // Apply velocity with damping
    for (const node of nodes) {
      node.x += node.vx * 0.1;
      node.y += node.vy * 0.1;
      node.z += node.vz * 0.1;
      node.vx *= 0.9;
      node.vy *= 0.9;
      node.vz *= 0.9;
    }
  }, [data.links]);

  // Render loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const render = () => {
      const width = canvas.width;
      const height = canvas.height;
      const cx = width / 2;
      const cy = height / 2;

      // Clear
      ctx.fillStyle = 'rgba(15, 23, 42, 0.95)';
      ctx.fillRect(0, 0, width, height);

      simulate();

      const nodes = nodesRef.current;
      const links = data.links;
      const rx = rotationRef.current.x;
      const ry = rotationRef.current.y;

      // Project 3D to 2D with rotation
      const project = (x: number, y: number, z: number) => {
        // Rotate around Y
        const x1 = x * Math.cos(ry) - z * Math.sin(ry);
        const z1 = x * Math.sin(ry) + z * Math.cos(ry);
        // Rotate around X
        const y1 = y * Math.cos(rx) - z1 * Math.sin(rx);
        const z2 = y * Math.sin(rx) + z1 * Math.cos(rx);
        // Perspective
        const scale = 400 / (400 + z2);
        return { x: cx + x1 * scale, y: cy + y1 * scale, scale };
      };

      // Sort by Z for proper rendering order
      const sortedNodes = [...nodes].sort((a, b) => {
        const az = a.z * Math.cos(rx) + a.y * Math.sin(rx);
        const bz = b.z * Math.cos(rx) + b.y * Math.sin(rx);
        return bz - az;
      });

      // Draw links
      ctx.globalAlpha = 0.3;
      for (const link of links) {
        const source = nodes.find((n) => n.id === link.source);
        const target = nodes.find((n) => n.id === link.target);
        if (!source || !target) continue;

        const p1 = project(source.x, source.y, source.z);
        const p2 = project(target.x, target.y, target.z);

        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.strokeStyle = '#64748b';
        ctx.lineWidth = link.weight * 2;
        ctx.stroke();
      }

      // Draw nodes
      ctx.globalAlpha = 1;
      for (const node of sortedNodes) {
        const p = project(node.x, node.y, node.z);
        const radius = 6 * p.scale * (0.5 + node.strength * 0.5);

        // Glow
        const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius * 2);
        const color = typeColors[node.type] || '#64748b';
        gradient.addColorStop(0, color);
        gradient.addColorStop(1, 'transparent');
        ctx.beginPath();
        ctx.arc(p.x, p.y, radius * 2, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.globalAlpha = 0.3;
        ctx.fill();

        // Node
        ctx.beginPath();
        ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.globalAlpha = 1;
        ctx.fill();

        // Border
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Auto-rotate slowly
      if (!isDragging.current) {
        rotationRef.current.y += 0.002;
      }

      animationRef.current = requestAnimationFrame(render);
    };

    render();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [data.links, simulate, typeColors]);

  // Mouse interaction
  const handleMouseDown = (e: React.MouseEvent) => {
    isDragging.current = true;
    lastMouse.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging.current) return;
    const dx = e.clientX - lastMouse.current.x;
    const dy = e.clientY - lastMouse.current.y;
    rotationRef.current.y += dx * 0.005;
    rotationRef.current.x += dy * 0.005;
    lastMouse.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseUp = () => {
    isDragging.current = false;
  };

  const handleClick = (e: React.MouseEvent) => {
    if (!canvasRef.current || !onNodeClick) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const cx = canvasRef.current.width / 2;
    const cy = canvasRef.current.height / 2;
    const rx = rotationRef.current.x;
    const ry = rotationRef.current.y;

    // Find clicked node
    for (const node of nodesRef.current) {
      const x1 = node.x * Math.cos(ry) - node.z * Math.sin(ry);
      const z1 = node.x * Math.sin(ry) + node.z * Math.cos(ry);
      const y1 = node.y * Math.cos(rx) - z1 * Math.sin(rx);
      const z2 = node.y * Math.sin(rx) + z1 * Math.cos(rx);
      const scale = 400 / (400 + z2);
      const px = cx + x1 * scale;
      const py = cy + y1 * scale;
      const radius = 6 * scale * (0.5 + node.strength * 0.5);

      const dist = Math.sqrt((x - px) ** 2 + (y - py) ** 2);
      if (dist < radius + 5) {
        onNodeClick(node);
        return;
      }
    }
  };

  return (
    <canvas
      ref={canvasRef}
      width={800}
      height={500}
      className="w-full h-full cursor-grab active:cursor-grabbing"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onClick={handleClick}
    />
  );
}
