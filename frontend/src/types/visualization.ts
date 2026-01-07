// Visualization and 3D Types

// 3D Camera Preset
export interface CameraPreset {
  name: string;
  position: [number, number, number];
  target: [number, number, number];
}

// Chart Data Point
export interface DataPoint {
  timestamp: string;
  value: number;
  label?: string;
}

// Time Series Data
export interface TimeSeriesData {
  timestamp: string;
  value: number;
  metadata?: Record<string, unknown>;
}

// 3D Graph Node
export interface GraphNode {
  id: string;
  label: string;
  type: string;
  value?: number;
  metadata?: Record<string, unknown>;
}

// 3D Graph Link
export interface GraphLink {
  source: string;
  target: string;
  type?: string;
  value?: number;
}

// Chart Config
export interface ChartConfig {
  title?: string;
  color?: string;
  height?: number;
  showGrid?: boolean;
  showTooltip?: boolean;
}
