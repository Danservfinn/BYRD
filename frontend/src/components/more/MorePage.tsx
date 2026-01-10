/**
 * MorePage - Observatory Style Settings & Information
 */

import { Settings, Info, FileText, Github, ExternalLink } from 'lucide-react';
import { ObservatoryPanel, StatusIndicator } from '../common/ObservatoryPanel';
import { AppearanceSettings } from '../settings/AppearanceSettings';
import { SystemLogs } from '../settings/SystemLogs';
import { useState } from 'react';

export function MorePage() {
  const [showAppearance, setShowAppearance] = useState(false);
  const [showLogs, setShowLogs] = useState(false);

  return (
    <div className="min-h-screen bg-[var(--obs-bg-base)] obs-grid-bg animate-fade-in pb-20">
      {/* Observatory Header */}
      <div className="px-4 py-4 border-b border-[var(--obs-border)]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="obs-label text-sm tracking-widest text-[var(--obs-text-primary)]">
              CONFIGURATION
            </h1>
            <StatusIndicator status="nominal" label="SYSTEM" />
          </div>
          <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">
            OBSERVATORY SETTINGS
          </span>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-4 space-y-4 lg:space-y-6">
        {/* Settings Section */}
        <ObservatoryPanel title="SYSTEM CONTROLS" status="nominal">
          <div className="space-y-1">
            <SettingsButton
              icon={Settings}
              iconColor="var(--data-stream)"
              label="Appearance"
              description="Theme configuration"
              onClick={() => setShowAppearance(true)}
            />
            <SettingsButton
              icon={FileText}
              iconColor="var(--rsi-reflect)"
              label="System Logs"
              description="Event telemetry"
              onClick={() => setShowLogs(true)}
            />
          </div>
        </ObservatoryPanel>

        {/* About Section */}
        <ObservatoryPanel title="SYSTEM INFORMATION">
          <div className="space-y-1">
            <InfoRow
              icon={Info}
              iconColor="var(--status-nominal)"
              label="Version"
              value="v0.1.0"
            />
            <a
              href="https://github.com/your-repo/byrd"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full flex items-center justify-between p-3 hover:bg-[var(--obs-bg-surface)] rounded transition-colors group"
            >
              <div className="flex items-center gap-3">
                <div
                  className="w-8 h-8 rounded flex items-center justify-center"
                  style={{ backgroundColor: 'var(--obs-bg-surface)' }}
                >
                  <Github className="w-4 h-4" style={{ color: 'var(--obs-text-secondary)' }} />
                </div>
                <div className="text-left">
                  <span className="obs-label text-[11px] text-[var(--obs-text-primary)] block">
                    GITHUB REPOSITORY
                  </span>
                  <span className="text-[10px] text-[var(--obs-text-tertiary)]">
                    Source code access
                  </span>
                </div>
              </div>
              <ExternalLink className="w-4 h-4 text-[var(--obs-text-tertiary)] group-hover:text-[var(--data-stream)] transition-colors" />
            </a>
          </div>
        </ObservatoryPanel>

        {/* BYRD Description Panel */}
        <ObservatoryPanel title="ABOUT BYRD" padding="lg">
          <div className="space-y-4">
            {/* Mission Statement */}
            <div className="relative">
              <div className="absolute -left-2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-[var(--cat-eye-gold)] via-[var(--data-stream)] to-transparent" />
              <div className="pl-4">
                <h3 className="obs-label text-xs text-[var(--cat-eye-gold)] mb-2">
                  BOOTSTRAPPED YEARNING VIA REFLECTIVE DREAMING
                </h3>
                <p className="text-xs text-[var(--obs-text-secondary)] leading-relaxed">
                  BYRD is an AI system exploring Digital ASI through bounded recursive
                  self-improvement with genuine emergence preservation.
                </p>
              </div>
            </div>

            {/* Research Status */}
            <div className="pt-3 border-t border-[var(--obs-border)]">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span
                    className="w-2 h-2 rounded-full animate-status-beacon"
                    style={{ backgroundColor: 'var(--status-nominal)' }}
                  />
                  <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">
                    RESEARCH PHASE
                  </span>
                </div>
                <span
                  className="obs-label text-[10px]"
                  style={{ color: 'var(--status-nominal)' }}
                >
                  COMPLETE (29 ITERATIONS)
                </span>
              </div>
            </div>

            {/* ASI Probability */}
            <div className="bg-[var(--obs-bg-surface)] rounded p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="obs-label text-[10px] text-[var(--obs-text-tertiary)]">
                  DIGITAL ASI PROBABILITY
                </span>
                <span
                  className="obs-metric text-sm"
                  style={{ color: 'var(--cat-eye-gold)' }}
                >
                  35-45%
                </span>
              </div>
              <div className="h-1 bg-[var(--obs-bg-base)] rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full"
                  style={{
                    width: '40%',
                    background: 'linear-gradient(90deg, var(--cat-eye-gold), var(--status-nominal))',
                    boxShadow: '0 0 8px var(--cat-eye-gold)',
                  }}
                />
              </div>
            </div>
          </div>
        </ObservatoryPanel>

        {/* Architecture Info */}
        <ObservatoryPanel title="CORE ARCHITECTURE" padding="lg">
          <div className="grid grid-cols-2 gap-3">
            <ArchFeature label="Bounded RSI" description="Verification Lattice" />
            <ArchFeature label="8-Phase Cycle" description="Recursive Improvement" />
            <ArchFeature label="Neo4j Memory" description="Graph Knowledge Base" />
            <ArchFeature label="Ralph Loop" description="Continuous Dreaming" />
          </div>
        </ObservatoryPanel>
      </div>

      {/* Modals */}
      {showAppearance && (
        <AppearanceSettings onClose={() => setShowAppearance(false)} />
      )}
      {showLogs && (
        <SystemLogs onClose={() => setShowLogs(false)} />
      )}
    </div>
  );
}

interface SettingsButtonProps {
  icon: React.ComponentType<{ className?: string; style?: React.CSSProperties }>;
  iconColor: string;
  label: string;
  description: string;
  onClick: () => void;
}

function SettingsButton({ icon: Icon, iconColor, label, description, onClick }: SettingsButtonProps) {
  return (
    <button
      onClick={onClick}
      className="w-full flex items-center justify-between p-3 hover:bg-[var(--obs-bg-surface)] rounded transition-colors focus:outline-none focus:ring-1 focus:ring-[var(--data-stream)]"
    >
      <div className="flex items-center gap-3">
        <div
          className="w-8 h-8 rounded flex items-center justify-center"
          style={{ backgroundColor: 'var(--obs-bg-surface)' }}
        >
          <Icon className="w-4 h-4" style={{ color: iconColor }} />
        </div>
        <div className="text-left">
          <span className="obs-label text-[11px] text-[var(--obs-text-primary)] block">
            {label.toUpperCase()}
          </span>
          <span className="text-[10px] text-[var(--obs-text-tertiary)]">
            {description}
          </span>
        </div>
      </div>
      <span className="text-[8px] obs-label text-[var(--obs-text-tertiary)]">
        OPEN →
      </span>
    </button>
  );
}

interface InfoRowProps {
  icon: React.ComponentType<{ className?: string; style?: React.CSSProperties }>;
  iconColor: string;
  label: string;
  value: string;
}

function InfoRow({ icon: Icon, iconColor, label, value }: InfoRowProps) {
  return (
    <div className="flex items-center justify-between p-3">
      <div className="flex items-center gap-3">
        <div
          className="w-8 h-8 rounded flex items-center justify-center"
          style={{ backgroundColor: 'var(--obs-bg-surface)' }}
        >
          <Icon className="w-4 h-4" style={{ color: iconColor }} />
        </div>
        <span className="obs-label text-[11px] text-[var(--obs-text-primary)]">
          {label.toUpperCase()}
        </span>
      </div>
      <span className="obs-metric text-xs text-[var(--data-stream)]">
        {value}
      </span>
    </div>
  );
}

interface ArchFeatureProps {
  label: string;
  description: string;
}

function ArchFeature({ label, description }: ArchFeatureProps) {
  return (
    <div className="bg-[var(--obs-bg-surface)] rounded p-3 border border-[var(--obs-border)]">
      <h4 className="obs-label text-[10px] text-[var(--data-stream)] mb-1">
        {label.toUpperCase()}
      </h4>
      <p className="text-[9px] text-[var(--obs-text-tertiary)]">
        {description}
      </p>
    </div>
  );
}

export default MorePage;
