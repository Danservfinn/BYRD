// UI Component Types

// Layout Breakpoints
export type Breakpoint = 'mobile' | 'tablet' | 'desktop';

// Tab Routes
export type TabRoute =
  | 'home'
  | 'byrd'
  | 'rsi'
  | 'memory'
  | 'economic'
  | 'more';

// Animation State for 3D Avatar
export type AnimationState =
  | 'idle'
  | 'thinking'
  | 'speaking'
  | 'celebrating'
  | 'concerned';

// Theme Mode
export type Theme = 'light' | 'dark' | 'system';

// Status Variant
export type StatusVariant = 'success' | 'warning' | 'critical' | 'info';

// Navigation Items
export interface NavItem {
  route: TabRoute;
  path: string;
  label: string;
  icon: string;
}

// Metric Card Data
export interface MetricData {
  title: string;
  value: string | number;
  unit?: string;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
  };
  sparkline?: number[];
}
