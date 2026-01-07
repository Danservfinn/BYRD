import { ConsciousnessStream } from '../dashboard/ConsciousnessStream';

export function MemoryPage() {
  return (
    <div className="space-y-4 lg:space-y-6 animate-fade-in pb-20">
      {/* Header */}
      <div className="px-4">
        <h1 className="text-xl lg:text-2xl font-bold text-slate-900 dark:text-slate-100">
          Memory Topology
        </h1>
        <p className="text-xs lg:text-sm text-slate-500 dark:text-slate-400">
          3D memory graph and consciousness stream
        </p>
      </div>

      {/* Consciousness Stream */}
      <div className="px-4">
        <ConsciousnessStream />
      </div>
    </div>
  );
}
