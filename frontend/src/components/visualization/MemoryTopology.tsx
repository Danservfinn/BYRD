import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { ForceGraph3D } from './ForceGraph3D';
import { useByrdAPI } from '../../hooks/useByrdAPI';

export interface GraphNode {
  id: string;
  type: 'belief' | 'desire' | 'experience' | 'reflection' | 'capability' | 'goal';
  label: string;
  strength: number;
  created_at: string;
}

export interface GraphLink {
  source: string;
  target: string;
  type: string;
  weight: number;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

export function MemoryTopology() {
  const { getMemoryGraph } = useByrdAPI();
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [filter, setFilter] = useState<string | null>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getMemoryGraph();
      if (result?.graph) {
        setGraphData(result.graph);
      }
    };
    fetch();
    const interval = setInterval(fetch, 10000);
    return () => clearInterval(interval);
  }, [getMemoryGraph]);

  const filteredData: GraphData = filter
    ? {
        nodes: graphData.nodes.filter(n => n.type === filter),
        links: graphData.links.filter(l => {
          const sourceNode = graphData.nodes.find(n => n.id === l.source);
          const targetNode = graphData.nodes.find(n => n.id === l.target);
          return sourceNode?.type === filter && targetNode?.type === filter;
        }),
      }
    : graphData;

  const nodeTypes = ['belief', 'desire', 'experience', 'reflection', 'capability', 'goal'] as const;

  const typeColors: Record<string, string> = {
    belief: '#3b82f6',
    desire: '#f59e0b',
    experience: '#10b981',
    reflection: '#8b5cf6',
    capability: '#06b6d4',
    goal: '#ef4444',
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
          Memory Topology
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          3D visualization of BYRD's memory graph
        </p>
      </div>

      {/* Controls */}
      <GlassPanel glow="none" padding="md">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Filter by type:
          </span>
          <button
            onClick={() => setFilter(null)}
            className={`px-3 py-1 rounded text-sm transition-colors ${
              filter === null
                ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300'
            }`}
          >
            All
          </button>
          {nodeTypes.map((type) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`px-3 py-1 rounded text-sm capitalize transition-colors ${
                filter === type
                  ? 'text-white'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300'
              }`}
              style={filter === type ? { backgroundColor: typeColors[type] } : undefined}
            >
              {type}
            </button>
          ))}
        </div>
      </GlassPanel>

      {/* 3D Graph */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3">
          <GlassPanel glow="cyan" padding="none" className="overflow-hidden">
            <div className="h-[500px]">
              <ForceGraph3D
                data={filteredData}
                onNodeClick={setSelectedNode}
                typeColors={typeColors}
              />
            </div>
          </GlassPanel>
        </div>

        {/* Node details */}
        <div className="lg:col-span-1">
          <GlassPanel glow="none" padding="lg" className="h-full">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Node Details
            </h3>

            {selectedNode ? (
              <div className="space-y-3">
                <div>
                  <span className="text-xs text-slate-500">Type</span>
                  <div
                    className="font-medium capitalize"
                    style={{ color: typeColors[selectedNode.type] }}
                  >
                    {selectedNode.type}
                  </div>
                </div>

                <div>
                  <span className="text-xs text-slate-500">Label</span>
                  <div className="text-sm text-slate-900 dark:text-slate-100">
                    {selectedNode.label}
                  </div>
                </div>

                <div>
                  <span className="text-xs text-slate-500">Strength</span>
                  <div className="text-sm text-slate-900 dark:text-slate-100">
                    {(selectedNode.strength * 100).toFixed(0)}%
                  </div>
                </div>

                <div>
                  <span className="text-xs text-slate-500">Created</span>
                  <div className="text-sm text-slate-900 dark:text-slate-100">
                    {new Date(selectedNode.created_at).toLocaleString()}
                  </div>
                </div>

                <div>
                  <span className="text-xs text-slate-500">ID</span>
                  <div className="text-xs font-mono text-slate-500 break-all">
                    {selectedNode.id}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-slate-400 text-sm">
                Click a node to view details
              </div>
            )}
          </GlassPanel>
        </div>
      </div>

      {/* Legend */}
      <GlassPanel glow="none" padding="md">
        <div className="flex flex-wrap items-center justify-center gap-6">
          {nodeTypes.map((type) => (
            <div key={type} className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: typeColors[type] }}
              />
              <span className="text-sm text-slate-600 dark:text-slate-400 capitalize">
                {type}
              </span>
              <span className="text-xs text-slate-400">
                ({filteredData.nodes.filter(n => n.type === type).length})
              </span>
            </div>
          ))}
        </div>
      </GlassPanel>
    </div>
  );
}
