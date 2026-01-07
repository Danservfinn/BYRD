# BYRD Mobile-First ASI Frontend - Implementation Plan

**Project**: Transform BYRD frontend into a mobile-first ASI control panel
**Date**: January 7, 2026
**Estimated Duration**: 7-10 days
**Complexity**: High - Full frontend redesign with 3D visualization

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Technical Stack](#technical-stack)
3. [Design System](#design-system)
4. [File Structure](#file-structure)
5. [Phase 1: Foundation](#phase-1-foundation-day-1)
6. [Phase 2: Navigation & Routing](#phase-2-navigation--routing-day-1-2)
7. [Phase 3: BYRD Chat Page](#phase-3-byrd-chat-page-day-2-4)
8. [Phase 4: Dashboard Pages](#phase-4-dashboard-pages-day-4-6)
9. [Phase 5: Advanced Visualizations](#phase-5-advanced-visualizations-day-6-7)
10. [Phase 6: Polish & Launch](#phase-6-polish--launch-day-7-8)
11. [Dependencies](#dependencies)
12. [Testing Strategy](#testing-strategy)
13. [Deployment](#deployment)

---

## Executive Summary

### Goals

Transform the BYRD frontend into a **mobile-first**, **clean research lab** aesthetic ASI control panel that:
- Feels like it shipped from DeepMind/Anthropic
- Works beautifully on mobile (320px+) and scales up to desktop
- Features interactive 3D BYRD avatar on dedicated chat page
- Applies Miller's Law (7±2 items per view) for focus
- Includes advanced data visualizations
- Engages with smooth transitions and animations

### Key Design Decisions

1. **Mobile-First**: Start with single-column layouts, progressive enhancement for larger screens
2. **Bottom Tab Navigation**: 6 tabs, thumb-friendly on mobile
3. **Dedicated BYRD Page**: Chat + 3D avatar always accessible (2nd tab position)
4. **Vertical Layout**: Avatar top, chat middle, input bottom (all orientations)
5. **Clean Research Lab Aesthetic**: Crisp whites/grays, refined typography, subtle gradients
6. **Focus Panels**: 3-4 primary metrics visible, tab the rest
7. **Interactive 3D**: Orbit controls for avatar (drag to rotate, pinch to zoom)

### Success Criteria

- [ ] All 6 pages functional on mobile, tablet, desktop
- [ ] 3D avatar renders smoothly with orbit controls
- [ ] Real-time WebSocket data updates working
- [ ] Page load < 2s on 4G mobile
- [ ] Touch interactions smooth (60fps)
- [ ] Dark mode supported
- [ ] Keyboard navigation supported (desktop)

---

## Technical Stack

### Core Framework

```json
{
  "framework": "React 18.3+",
  "language": "TypeScript 5.3+",
  "bundler": "Vite 5.0+",
  "router": "React Router DOM 6.21+ (HashRouter for embedded mode)"
}
```

### UI & Styling

```json
{
  "styling": "Tailwind CSS 3.4+",
  "components": "Custom components (no UI library)",
  "animations": "Framer Motion 10.16+",
  "icons": "Lucide React 0.300+"
}
```

### 3D Rendering

```json
{
  "library": "Three.js r160+",
  "controls": "Three OrbitControls",
  "loaders": "Three GLTFLoader",
  "react": "React Three Fiber 8.15+ (optional wrapper)"
}
```

### Data Visualization

```json
{
  "charts": "Recharts 2.10+ (mobile-optimized)",
  "3d-graph": "Force-graph (3D memory topology)",
  "numbers": "CountUp.js 2.8+ (animated counters)"
}
```

### State & Data

```json
{
  "state": "Zustand 4.4+",
  "server-state": "TanStack Query 5.17+",
  "real-time": "Native WebSocket with custom hook"
}
```

### Forms & Input

```json
{
  "validation": "Zod 3.22+",
  "forms": "React Hook Form 7.49+"
}
```

---

## Design System

### Color Palette

```css
/* Light Mode (Default) */
:root {
  /* Neutral Backgrounds */
  --bg-base: #ffffff;
  --bg-surface: #f8fafc;
  --bg-elevated: #f1f5f9;
  --bg-overlay: rgba(255, 255, 255, 0.95);

  /* Functional Colors */
  --accent-primary: #7c3aed;    /* BYRD purple */
  --accent-primary-hover: #6d28d9;
  --accent-primary-light: #ddd6fe;

  --accent-success: #10b981;    /* Emerald */
  --accent-warning: #f59e0b;    /* Amber */
  --accent-critical: #f43f5e;   /* Rose */
  --accent-info: #0ea5e9;       /* Sky */

  /* Text */
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-tertiary: #94a3b8;
  --text-inverse: #ffffff;

  /* Borders & Dividers */
  --border-base: #e2e8f0;
  --border-subtle: rgba(226, 232, 240, 0.5);
  --border-focus: var(--accent-primary);

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

/* Dark Mode */
:root.dark {
  --bg-base: #0f172a;
  --bg-surface: #1e293b;
  --bg-elevated: #334155;
  --bg-overlay: rgba(15, 23, 42, 0.95);

  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-tertiary: #64748b;

  --border-base: #334155;
  --border-subtle: rgba(51, 65, 85, 0.5);
}
```

### Typography

```css
/* Font Families */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'SF Mono', 'Consolas', monospace;

/* Type Scale */
--text-xs: 0.75rem;    /* 12px - Labels, captions */
--text-sm: 0.875rem;   /* 14px - Body, secondary text */
--text-base: 1rem;     /* 16px - Default body */
--text-lg: 1.125rem;   /* 18px - Emphasized body */
--text-xl: 1.25rem;    /* 20px - Small headings */
--text-2xl: 1.5rem;    /* 24px - Section headings */
--text-3xl: 1.875rem;  /* 30px - Page headings */
--text-4xl: 2.25rem;   /* 36px - Hero metrics */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Letter Spacing */
--tracking-tight: -0.025em;   /* Headings */
--tracking-normal: 0;         /* Body */
--tracking-wide: 0.025em;     /* Uppercase labels */
--tracking-wider: 0.05em;     /* Emphasized labels */
```

### Spacing Scale

```css
/* Base unit: 4px */
--spacing-0: 0;
--spacing-1: 0.25rem;  /* 4px */
--spacing-2: 0.5rem;   /* 8px */
--spacing-3: 0.75rem;  /* 12px */
--spacing-4: 1rem;     /* 16px - Base spacing */
--spacing-5: 1.25rem;  /* 20px */
--spacing-6: 1.5rem;   /* 24px - Section spacing */
--spacing-8: 2rem;     /* 32px - Major spacing */
--spacing-10: 2.5rem;  /* 40px */
--spacing-12: 3rem;    /* 48px */
--spacing-16: 4rem;    /* 64px */
```

### Border Radius

```css
--radius-sm: 0.375rem;   /* 6px - Buttons, inputs */
--radius-md: 0.5rem;     /* 8px - Cards */
--radius-lg: 0.75rem;    /* 12px - Large cards */
--radius-xl: 1rem;       /* 16px - Modals */
--radius-full: 9999px;   /* Pills, badges */
```

### Transitions

```css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slower: 500ms cubic-bezier(0.4, 0, 0.2, 1);
```

### Component Patterns

**Card Component**:
```tsx
<div className="
  bg-white dark:bg-slate-900
  border border-slate-200 dark:border-slate-700
  rounded-lg
  shadow-sm
  p-4
  hover:shadow-md
  transition-shadow duration-200
">
  {children}
</div>
```

**Button Component**:
```tsx
<button className="
  px-4 py-2
  rounded-md
  font-medium text-sm
  bg-purple-600 hover:bg-purple-700
  text-white
  transition-colors duration-150
  disabled:opacity-50 disabled:cursor-not-allowed
">
  {label}
</button>
```

**Input Component**:
```tsx
<input className="
  w-full px-3 py-2
  rounded-md
  border border-slate-300 dark:border-slate-600
  bg-white dark:bg-slate-800
  text-slate-900 dark:text-slate-100
  placeholder-slate-400
  text-sm
  focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent
  transition-all duration-150
"/>
```

---

## File Structure

```
frontend/
├── public/
│   └── models/
│       └── cat.glb                    # BYRD 3D avatar model
│
├── src/
│   ├── App.tsx                        # Root component with HashRouter
│   ├── main.tsx                       # Entry point
│   ├── index.css                      # Global styles + CSS variables
│   └── vite-env.d.ts                  # Vite types
│
│   ├── assets/                        # Static assets
│   │   └── icons/
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── MobileLayout.tsx       # Mobile: Bottom tabs + header
│   │   │   ├── TabletLayout.tsx       # Tablet: Sidebar + bottom tabs
│   │   │   ├── DesktopLayout.tsx      # Desktop: Full sidebar
│   │   │   ├── BottomTabBar.tsx       # Mobile bottom navigation
│   │   │   ├── Sidebar.tsx            # Desktop sidebar navigation
│   │   │   └── Header.tsx             # Top header bar
│   │   │
│   │   ├── common/
│   │   │   ├── StatCard.tsx           # Metric card with sparkline
│   │   │   ├── GlassPanel.tsx         # (Existing, enhance)
│   │   │   ├── Button.tsx             # Styled button
│   │   │   ├── Input.tsx              # Styled input
│   │   │   ├── LoadingSpinner.tsx     # Loading indicator
│   │   │   ├── ErrorBoundary.tsx      # Error handling
│   │   │   ├── AnimatedCounter.tsx    # Number animation
│   │   │   └── StatusBadge.tsx        # Color-coded status
│   │   │
│   │   ├── visualization/
│   │   │   ├── AvatarCanvas.tsx       # 3D BYRD avatar with orbit controls
│   │   │   ├── MemoryTopology3D.tsx   # Force graph 3D
│   │   │   ├── LineChart.tsx          # Recharts wrapper
│   │   │   ├── AreaChart.tsx          # Recharts wrapper
│   │   │   ├── GaugeChart.tsx         # Semi-circle gauge
│   │   │   └── Sparkline.tsx          # Mini trend chart
│   │   │
│   │   ├── byrd/
│   │   │   ├── ByrdChatPage.tsx       # Dedicated BYRD chat page
│   │   │   ├── ChatMessages.tsx       # Message list (scrollable)
│   │   │   ├── ChatInput.tsx          # Fixed input at bottom
│   │   │   ├── StatusBar.tsx          # Collapsible status bar
│   │   │   ├── MessageBubble.tsx      # Individual message
│   │   │   ├── TypingIndicator.tsx    # "BYRD is typing..."
│   │   │   └── QuickActions.tsx       # Command buttons
│   │   │
│   │   ├── dashboard/
│   │   │   ├── DashboardPage.tsx      # (Existing, enhance)
│   │   │   ├── HeroMetric.tsx         # ASI Probability large display
│   │   │   ├── QuickStats.tsx         # Horizontal scrollable cards
│   │   │   ├── RecentActivity.tsx     # Activity feed
│   │   │   └── SystemStatus.tsx       # Overall status
│   │   │
│   │   ├── rsi/
│   │   │   ├── RSIPage.tsx            # (Existing, enhance)
│   │   │   ├── PhaseTracker.tsx       # 8-phase vertical stepper
│   │   │   ├── CycleHistory.tsx       # Timeline of cycles
│   │   │   └── EmergenceMetrics.tsx   # Emergence metrics
│   │   │
│   │   ├── memory/
│   │   │   ├── MemoryPage.tsx         # Memory topology + stream
│   │   │   ├── ConsciousnessStream.tsx # (Existing, enhance)
│   │   │   └── TopologyControls.tsx   # 3D graph controls
│   │   │
│   │   ├── economic/
│   │   │   ├── EconomicPage.tsx       # (Existing, enhance)
│   │   │   ├── TreasuryStatus.tsx     # Large treasury display
│   │   │   ├── RevenueChart.tsx       # 7-day revenue
│   │   │   └── MarketplaceListings.tsx # Service cards
│   │   │
│   │   └── more/
│   │       ├── MorePage.tsx           # Settings, logs, about
│   │       ├── SettingsPanel.tsx      # Theme, notifications, etc.
│   │       ├── SystemLogs.tsx         # Full log viewer
│   │       └── AboutPanel.tsx         # Version, credits
│   │
│   ├── hooks/
│   │   ├── useWebSocket.ts            # (Existing, enhance)
│   │   ├── useByrdAPI.ts              # (Existing)
│   │   ├── useBreakpoint.ts           # Responsive breakpoint detection
│   │   ├── useTheme.ts                # Dark mode toggle
│   │   ├── useAvatarAnimation.ts      # 3D avatar animation state machine
│   │   └── useCameraControls.ts       # 3D camera presets
│   │
│   ├── store/
│   │   ├── eventStore.ts              # WebSocket events (Zustand)
│   │   ├── uiStore.ts                 # UI state (drawer, tabs, theme)
│   │   ├── byrdStore.ts               # BYRD-specific state
│   │   └── navigationStore.ts         # Current route, history
│   │
│   ├── lib/
│   │   ├── three/
│   │   │   ├── setup.ts               # Three.js scene setup
│   │   │   ├── loadModel.ts           # GLTF loader wrapper
│   │   │   ├── animations.ts          # Avatar animation helpers
│   │   │   └── camera.ts              # Camera control helpers
│   │   ├── api/
│   │   │   ├── byrd.ts                # BYRD API client
│   │   │   ├── websocket.ts           # WebSocket client
│   │   │   └── types.ts               # API types
│   │   └── utils/
│   │       ├── cn.ts                  # clsx() utility
│   │       ├── format.ts              # Number/date formatting
│   │       └── validation.ts          # Zod schemas
│   │
│   └── types/
│       ├── api.ts                     # API response types
│       ├── byrd.ts                    # BYRD-specific types
│       ├── ui.ts                      # UI component types
│       └── visualization.ts           # 3D/chart types
│
├── index.html                         # HTML entry point
├── vite.config.ts                     # (Existing, update)
├── tailwind.config.js                 # (Existing, update)
├── tsconfig.json                      # TypeScript config
├── package.json                       # Dependencies
└── README.md                          # Setup instructions
```

---

## Phase 1: Foundation (Day 1)

### Goal: Set up project structure, design system, and core utilities

### 1.1 Install Dependencies

```bash
cd frontend

# Core
npm install react@^18.3.0 react-dom@^18.3.0
npm install react-router-dom@^6.21.0
npm install @types/react @types/react-dom

# Styling
npm install -D tailwindcss@^3.4.0 postcss autoprefixer
npm install clsx tailwind-merge

# Animations
npm install framer-motion@^10.16.0

# State
npm install zustand@^4.4.0
npm install @tanstack/react-query@^5.17.0

# 3D
npm install three@^0.160.0 @react-three/fiber@^8.15.0 @react-three/drei@^9.95.0

# Charts
npm install recharts@^2.10.0

# Utilities
npm install countup.js@^2.8.0
npm install lucide-react@^0.300.0

# Forms
npm install react-hook-form@^7.49.0
npm install @hookform/resolvers@^3.3.0
npm install zod@^3.22.0
```

### 1.2 Configure Tailwind CSS

**Update `tailwind.config.js`**:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Manual dark mode toggle
  theme: {
    extend: {
      colors: {
        // BYRD brand colors
        byrd: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed', // Primary
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
        // Functional colors
        success: {
          50: '#ecfdf5',
          500: '#10b981',
          600: '#059669',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',
          600: '#d97706',
        },
        critical: {
          50: '#fef2f2',
          500: '#f43f5e',
          600: '#e11d48',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
      },
    },
  },
  plugins: [],
}
```

### 1.3 Global Styles

**Create `src/index.css`**:

```css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* CSS Variables - Design Tokens */
:root {
  /* Colors */
  --color-bg-base: 255 255 255;           /* white */
  --color-bg-surface: 248 250 252;        /* slate-50 */
  --color-bg-elevated: 241 245 249;       /* slate-100 */

  --color-text-primary: 15 23 42;         /* slate-900 */
  --color-text-secondary: 71 85 105;      /* slate-600 */
  --color-text-tertiary: 148 163 184;     /* slate-400 */

  --color-border-base: 226 232 240;       /* slate-200 */

  /* Spacing */
  --header-height: 56px;
  --tab-bar-height: 64px;
  --input-height: 56px;

  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dark Mode */
.dark {
  --color-bg-base: 15 23 42;              /* slate-900 */
  --color-bg-surface: 30 41 59;           /* slate-800 */
  --color-bg-elevated: 51 65 85;          /* slate-700 */

  --color-text-primary: 248 250 252;      /* slate-50 */
  --color-text-secondary: 203 213 225;    /* slate-300 */
  --color-text-tertiary: 100 116 139;     /* slate-500 */

  --color-border-base: 51 65 85;          /* slate-700 */
}

/* Base Styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: rgb(var(--color-text-primary));
  background-color: rgb(var(--color-bg-base));
  line-height: 1.5;
  overflow-x: hidden;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgb(var(--color-border-base));
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgb(var(--color-text-tertiary));
}

/* Touch Actions */
canvas {
  touch-action: none; /* Prevent scrolling while interacting with 3D */
}

/* Focus Styles */
:focus-visible {
  outline: 2px solid rgb(124 58 237);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Utilities */
.container-custom {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Animation Classes */
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}

/* Safe Area Insets for Mobile */
.pb-safe {
  padding-bottom: calc(1rem + env(safe-area-inset-bottom));
}

/* Responsive Typography */
@media (max-width: 640px) {
  html {
    font-size: 14px;
  }
}
```

### 1.4 TypeScript Configuration

**Update `tsconfig.json`**:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    /* Path Mapping */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@lib/*": ["./src/lib/*"],
      "@store/*": ["./src/store/*"],
      "@types/*": ["./src/types/*"]
    },

    /* Additional */
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**Update `vite.config.ts`**:

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@lib': path.resolve(__dirname, './src/lib'),
      '@store': path.resolve(__dirname, './src/store'),
      '@types': path.resolve(__dirname, './src/types'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

### 1.5 Type Definitions

**Create `src/types/api.ts`**:

```typescript
// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// BYRD State
export interface ByrdState {
  as_probability: number;
  rsi_phase: number;
  rsi_cycle_number: number;
  emergence_score: number;
  treasury_balance: number;
  safety_tier: 'green' | 'yellow' | 'red';
  status: 'online' | 'offline' | 'processing';
}

// Chat Message
export interface ChatMessage {
  id: string;
  type: 'user' | 'byrd' | 'system';
  content: string;
  timestamp: string;
}

// Governance Command
export interface GovernanceCommand {
  command: string;
  timestamp: string;
  response?: string;
}

// WebSocket Event
export interface WebSocketEvent {
  type: string;
  data: unknown;
  timestamp: string;
}

// Memory Graph Node
export interface MemoryNode {
  id: string;
  label: string;
  type: 'belief' | 'desire' | 'goal' | 'capability' | 'experience';
  confidence?: number;
  created_at: string;
}

// Memory Graph Edge
export interface MemoryEdge {
  source: string;
  target: string;
  type: string;
  strength?: number;
}
```

**Create `src/types/ui.ts`**:

```typescript
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

// Animation State
export type AnimationState =
  | 'idle'
  | 'thinking'
  | 'speaking'
  | 'celebrating'
  | 'concerned';

// Theme
export type Theme = 'light' | 'dark' | 'system';

// Status Variant
export type StatusVariant = 'success' | 'warning' | 'critical' | 'info';
```

**Create `src/types/visualization.ts`**:

```typescript
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

// Metric Card Data
export interface MetricCard {
  title: string;
  value: string | number;
  unit?: string;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
  };
  sparkline?: number[];
}
```

### 1.6 Utility Functions

**Create `src/lib/utils/cn.ts`**:

```typescript
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

**Create `src/lib/utils/format.ts`**:

```typescript
// Format numbers with commas
export function formatNumber(num: number): string {
  return new Intl.NumberFormat('en-US').format(num);
}

// Format currency
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

// Format percentage
export function formatPercentage(value: number, decimals = 1): string {
  return `${value.toFixed(decimals)}%`;
}

// Format relative time
export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);

  if (diffSec < 60) return 'just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  if (diffHour < 24) return `${diffHour}h ago`;
  if (diffDay < 7) return `${diffDay}d ago`;
  return date.toLocaleDateString();
}

// Truncate text with ellipsis
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}
```

### 1.7 Zustand Stores

**Create `src/store/uiStore.ts`**:

```typescript
import { create } from 'zustand';
import { TabRoute, Theme, Breakpoint } from '@types/ui';

interface UIState {
  // Navigation
  currentTab: TabRoute;
  setCurrentTab: (tab: TabRoute) => void;

  // Theme
  theme: Theme;
  setTheme: (theme: Theme) => void;

  // Breakpoint
  breakpoint: Breakpoint;
  setBreakpoint: (breakpoint: Breakpoint) => void;

  // Drawer/Panel states
  isByrdChatOpen: boolean;
  setIsByrdChatOpen: (open: boolean) => void;

  // Loading states
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  currentTab: 'home',
  setCurrentTab: (tab) => set({ currentTab: tab }),

  theme: 'system',
  setTheme: (theme) => set({ theme }),

  breakpoint: 'mobile',
  setBreakpoint: (breakpoint) => set({ breakpoint }),

  isByrdChatOpen: false,
  setIsByrdChatOpen: (open) => set({ isByrdChatOpen: open }),

  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
}));
```

**Create `src/store/byrdStore.ts`**:

```typescript
import { create } from 'zustand';
import { ByrdState, ChatMessage } from '@types/api';
import { AnimationState } from '@types/ui';

interface ByrdDataState {
  // BYRD state
  byrdState: ByrdState | null;
  setByrdState: (state: ByrdState) => void;

  // Chat
  messages: ChatMessage[];
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;

  // Avatar animation
  animationState: AnimationState;
  setAnimationState: (state: AnimationState) => void;

  // Typing indicator
  isTyping: boolean;
  setIsTyping: (typing: boolean) => void;
}

export const useByrdStore = create<ByrdDataState>((set) => ({
  byrdState: null,
  setByrdState: (state) => set({ byrdState: state }),

  messages: [],
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message],
  })),
  clearMessages: () => set({ messages: [] }),

  animationState: 'idle',
  setAnimationState: (state) => set({ animationState: state }),

  isTyping: false,
  setIsTyping: (typing) => set({ isTyping: typing }),
}));
```

**Create `src/store/eventStore.ts`**:

```typescript
import { create } from 'zustand';
import { WebSocketEvent } from '@types/api';

interface EventState {
  events: WebSocketEvent[];
  addEvent: (event: WebSocketEvent) => void;
  clearEvents: () => void;
}

export const useEventStore = create<EventState>((set) => ({
  events: [],
  addEvent: (event) => set((state) => ({
    events: [...state.events, event].slice(-100), // Keep last 100
  })),
  clearEvents: () => set({ events: [] }),
}));
```

---

## Phase 2: Navigation & Routing (Day 1-2)

### Goal: Implement mobile-first responsive navigation with 6-tab bottom bar

### 2.1 Breakpoint Hook

**Create `src/hooks/useBreakpoint.ts`**:

```typescript
import { useState, useEffect } from 'react';
import { useUIStore } from '@store/uiStore';
import { Breakpoint } from '@types/ui';

export function useBreakpoint(): Breakpoint {
  const setBreakpoint = useUIStore((s) => s.setBreakpoint);
  const [breakpoint, setLocalBreakpoint] = useState<Breakpoint>('mobile');

  useEffect(() => {
    const updateBreakpoint = () => {
      const width = window.innerWidth;
      let newBreakpoint: Breakpoint;

      if (width < 768) {
        newBreakpoint = 'mobile';
      } else if (width < 1024) {
        newBreakpoint = 'tablet';
      } else {
        newBreakpoint = 'desktop';
      }

      setLocalBreakpoint(newBreakpoint);
      setBreakpoint(newBreakpoint);
    };

    updateBreakpoint();
    window.addEventListener('resize', updateBreakpoint);
    return () => window.removeEventListener('resize', updateBreakpoint);
  }, [setBreakpoint]);

  return breakpoint;
}
```

### 2.2 Bottom Tab Bar Component

**Create `src/components/layout/BottomTabBar.tsx`**:

```typescript
import { useLocation, useNavigate } from 'react-router-dom';
import { Home, MessageSquare, GitBranch, Network, DollarSign, MoreHorizontal } from 'lucide-react';
import { cn } from '@lib/utils/cn';
import { TabRoute } from '@types/ui';

const tabs: { route: TabRoute; path: string; label: string; icon: any }[] = [
  { route: 'home', path: '/home', label: 'Home', icon: Home },
  { route: 'byrd', path: '/byrd', label: 'BYRD', icon: MessageSquare },
  { route: 'rsi', path: '/rsi', label: 'RSI', icon: GitBranch },
  { route: 'memory', path: '/memory', label: 'Memory', icon: Network },
  { route: 'economic', path: '/economic', label: 'Economic', icon: DollarSign },
  { route: 'more', path: '/more', label: 'More', icon: MoreHorizontal },
];

export function BottomTabBar() {
  const navigate = useNavigate();
  const location = useLocation();

  const currentTab = tabs.find(t => location.pathname === t.path);

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-700 safe-area-inset-bottom">
      <div className="flex items-center justify-around h-16 max-w-lg mx-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab?.route === tab.route;

          return (
            <button
              key={tab.route}
              onClick={() => navigate(tab.path)}
              className={cn(
                "flex flex-col items-center justify-center flex-1 h-full relative transition-colors duration-150",
                "active:scale-95 active:opacity-80",
                isActive ? "text-purple-600 dark:text-purple-400" : "text-slate-500 dark:text-slate-400"
              )}
              aria-label={tab.label}
              aria-current={isActive ? 'page' : undefined}
            >
              <Icon className="w-6 h-6" strokeWidth={isActive ? 2.5 : 2} />
              <span className="text-xs mt-1 font-medium">{tab.label}</span>

              {isActive && (
                <span className="absolute -top-0.5 left-1/2 -translate-x-1/2 w-12 h-0.5 bg-purple-600 dark:bg-purple-400 rounded-full" />
              )}
            </button>
          );
        })}
      </div>

      {/* Safe area inset for iOS */}
      <style>{`
        .safe-area-inset-bottom {
          padding-bottom: env(safe-area-inset-bottom, 0);
        }
      `}</style>
    </nav>
  );
}
```

### 2.3 Mobile Layout Component

**Create `src/components/layout/MobileLayout.tsx`**:

```typescript
import { Outlet } from 'react-router-dom';
import { BottomTabBar } from './BottomTabBar';
import { Header } from './Header';

export function MobileLayout() {
  return (
    <div className="flex flex-col h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header */}
      <Header />

      {/* Main Content - Scrolls independently */}
      <main className="flex-1 overflow-y-auto overflow-x-hidden">
        <Outlet />
      </main>

      {/* Bottom Tab Bar - Fixed */}
      <BottomTabBar />
    </div>
  );
}
```

### 2.4 Update App.tsx with Routes

**Update `src/App.tsx`**:

```typescript
import { HashRouter, Routes, Route } from 'react-router-dom';
import { MobileLayout } from './components/layout/MobileLayout';

// Page Components (to be implemented)
import { DashboardPage } from './components/dashboard/DashboardPage';
import { ByrdChatPage } from './components/byrd/ByrdChatPage';
import { RSIPage } from './components/rsi/RSIPage';
import { MemoryPage } from './components/memory/MemoryPage';
import { EconomicPage } from './components/economic/EconomicPage';
import { MorePage } from './components/more/MorePage';

import { useWebSocket } from './hooks/useWebSocket';
import './index.css';

function AppContent() {
  const { isConnected } = useWebSocket();

  return (
    <MobileLayout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/home" element={<DashboardPage />} />
        <Route path="/byrd" element={<ByrdChatPage />} />
        <Route path="/rsi" element={<RSIPage />} />
        <Route path="/memory" element={<MemoryPage />} />
        <Route path="/economic" element={<EconomicPage />} />
        <Route path="/more" element={<MorePage />} />
      </Routes>
    </MobileLayout>
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
```

---

## Phase 3: BYRD Chat Page (Day 2-4)

### Goal: Build dedicated BYRD chat page with interactive 3D avatar

### 3.1 Avatar Canvas Component (3D)

**Create `src/components/visualization/AvatarCanvas.tsx`**:

```typescript
import { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Camera, Rotate3D, Maximize2 } from 'lucide-react';
import { CameraPreset } from '@types/visualization';
import { cn } from '@lib/utils/cn';

interface AvatarCanvasProps {
  modelPath: string;
  animationState?: 'idle' | 'thinking' | 'speaking';
  className?: string;
  autoRotate?: boolean;
  onInteraction?: () => void;
}

const PRESETS: Record<string, CameraPreset> = {
  front: { name: 'Front', position: [0, 0, 5], target: [0, 0, 0] },
  side: { name: 'Side', position: [5, 0, 0], target: [0, 0, 0] },
  top: { name: 'Top', position: [0, 5, 0], target: [0, 0, 0] },
  dramatic: { name: 'Dramatic', position: [3, 2, 4], target: [0, 0, 0] },
  closeup: { name: 'Close-Up', position: [0, 0, 2.5], target: [0, 0, 0] },
};

export function AvatarCanvas({
  modelPath,
  animationState = 'idle',
  className,
  autoRotate = false,
  onInteraction,
}: AvatarCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const avatarRef = useRef<THREE.Group | null>(null);
  const mixerRef = useRef<THREE.AnimationMixer | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showControls, setShowControls] = useState(true);

  // Initialize Three.js scene
  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf8fafc);
    sceneRef.current = scene;

    // Camera
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 5);
    cameraRef.current = camera;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minPolarAngle = Math.PI / 6;
    controls.maxPolarAngle = (Math.PI * 5) / 6;
    controls.minDistance = 2;
    controls.maxDistance = 10;
    controls.enablePan = true;
    controls.enableZoom = true;
    controls.autoRotate = autoRotate;
    controls.autoRotateSpeed = 2.0;
    controlsRef.current = controls;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1);
    keyLight.position.set(5, 5, 5);
    keyLight.castShadow = true;
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
    fillLight.position.set(-5, 3, 2);
    scene.add(fillLight);

    const rimLight = new THREE.DirectionalLight(0x7c3aed, 0.8);
    rimLight.position.set(0, 5, -5);
    scene.add(rimLight);

    // Load model
    const loader = new GLTFLoader();
    loader.load(
      modelPath,
      (gltf) => {
        const avatar = gltf.scene;
        avatarRef.current = avatar;

        // Scale and position
        avatar.scale.set(1, 1, 1);
        avatar.position.set(0, -1, 0);

        scene.add(avatar);

        // Setup animations
        const mixer = new THREE.AnimationMixer(avatar);
        mixerRef.current = mixer;

        gltf.animations.forEach((clip) => {
          const action = mixer.clipAction(clip);
          if (clip.name === 'Idle' || clip.name === 'idle') {
            action.play();
          }
        });

        setIsLoading(false);
      },
      undefined,
      (error) => {
        console.error('Error loading avatar model:', error);
        setIsLoading(false);
      }
    );

    // Animation loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      const delta = 0.016; // ~60fps

      if (mixerRef.current) {
        mixerRef.current.update(delta);
      }

      if (controlsRef.current) {
        controlsRef.current.update();
      }

      if (rendererRef.current && sceneRef.current && cameraRef.current) {
        rendererRef.current.render(sceneRef.current, cameraRef.current);
      }
    };
    animate();

    // Handle resize
    const handleResize = () => {
      if (!container || !cameraRef.current || !rendererRef.current) return;

      const width = container.clientWidth;
      const height = container.clientHeight;

      cameraRef.current.aspect = width / height;
      cameraRef.current.updateProjectionMatrix();

      rendererRef.current.setSize(width, height);
    };

    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);

      if (rendererRef.current && container.contains(rendererRef.current.domElement)) {
        container.removeChild(rendererRef.current.domElement);
      }

      rendererRef.current?.dispose();
      controlsRef.current?.dispose();
    };
  }, [modelPath, autoRotate]);

  // Handle interaction callbacks
  useEffect(() => {
    if (!controlsRef.current) return;

    const controls = controlsRef.current;

    const onStart = () => onInteraction?.();
    const onEnd = () => {
      setShowControls(true);
      setTimeout(() => setShowControls(false), 3000);
    };

    controls.addEventListener('start', onStart);
    controls.addEventListener('end', onEnd);

    return () => {
      controls.removeEventListener('start', onStart);
      controls.removeEventListener('end', onEnd);
    };
  }, [onInteraction]);

  // Camera preset animation
  const animateCamera = (preset: CameraPreset) => {
    if (!cameraRef.current) return;

    const targetPosition = new THREE.Vector3(...preset.position);
    const startPosition = cameraRef.current.position.clone();
    const startTime = Date.now();
    const duration = 1000;

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);

      cameraRef.current!.position.lerpVectors(startPosition, targetPosition, eased);

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    animate();
  };

  // Reset camera
  const resetCamera = () => animateCamera(PRESETS.front);

  // Toggle fullscreen
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  return (
    <div
      ref={containerRef}
      className={cn(
        "relative w-full h-full bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-800",
        className
      )}
    >
      {/* Loading state */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-100 dark:bg-slate-800">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600" />
        </div>
      )}

      {/* Camera controls overlay */}
      {showControls && !isLoading && (
        <div className="absolute top-4 right-4 flex gap-2 z-10">
          <button
            onClick={resetCamera}
            className="p-2 bg-white dark:bg-slate-700 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
            title="Reset view"
          >
            <Rotate3D className="w-5 h-5 text-slate-700 dark:text-slate-200" />
          </button>

          <button
            onClick={toggleFullscreen}
            className="p-2 bg-white dark:bg-slate-700 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
            title="Fullscreen"
          >
            <Maximize2 className="w-5 h-5 text-slate-700 dark:text-slate-200" />
          </button>
        </div>
      )}

      {/* Camera presets */}
      {showControls && !isLoading && (
        <div className="absolute bottom-4 left-4 flex gap-2 z-10">
          {Object.values(PRESETS).map((preset) => (
            <button
              key={preset.name}
              onClick={() => animateCamera(preset)}
              className="px-3 py-1.5 bg-white dark:bg-slate-700 rounded-lg shadow-lg text-sm font-medium text-slate-700 dark:text-slate-200 hover:shadow-xl transition-shadow"
            >
              {preset.name}
            </button>
          ))}
        </div>
      )}

      {/* Interaction hint (first time) */}
      {showControls && !isLoading && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="bg-black/50 text-white px-6 py-4 rounded-lg text-center backdrop-blur-sm">
            <p className="text-sm font-medium">
              👆 Click & drag to rotate • 🔍 Scroll to zoom • ⚡ Double-click to reset
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
```

### 3.2 Chat Messages Component

**Create `src/components/byrd/ChatMessages.tsx`**:

```typescript
import { useRef, useEffect } from 'react';
import { useByrdStore } from '@store/byrdStore';
import { MessageBubble } from './MessageBubble';
import { TypingIndicator } from './TypingIndicator';
import { formatRelativeTime } from '@lib/utils/format';
import { User, Bot, AlertCircle } from 'lucide-react';

export function ChatMessages() {
  const { messages, isTyping } = useByrdStore();
  const scrollRef = useRef<HTMLDivElement>(null);
  const prevMessagesLength = useRef(messages.length);

  // Auto-scroll to bottom when new message arrives
  useEffect(() => {
    if (messages.length > prevMessagesLength.current) {
      scrollRef.current?.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
    prevMessagesLength.current = messages.length;
  }, [messages.length]);

  return (
    <div
      ref={scrollRef}
      className="flex-1 overflow-y-auto px-4 py-4 space-y-4"
    >
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
          <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center">
            <Bot className="w-8 h-8 text-purple-600 dark:text-purple-400" />
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              Start a conversation with BYRD
            </h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 max-w-xs">
              Ask about RSI cycles, set priorities, or inject new desires
            </p>
          </div>
          <div className="flex flex-wrap gap-2 justify-center">
            <button
              onClick={() => {/* Trigger command */}}
              className="px-3 py-1.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full text-sm font-medium hover:bg-purple-200 dark:hover:bg-purple-900/50 transition-colors"
            >
              /status
            </button>
            <button
              onClick={() => {/* Trigger command */}}
              className="px-3 py-1.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full text-sm font-medium hover:bg-purple-200 dark:hover:bg-purple-900/50 transition-colors"
            >
              /priority
            </button>
            <button
              onClick={() => {/* Trigger command */}}
              className="px-3 py-1.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full text-sm font-medium hover:bg-purple-200 dark:hover:bg-purple-900/50 transition-colors"
            >
              /inject
            </button>
          </div>
        </div>
      )}

      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {isTyping && <TypingIndicator />}
    </div>
  );
}
```

### 3.3 Message Bubble Component

**Create `src/components/byrd/MessageBubble.tsx`**:

```typescript
import { User, Bot, AlertCircle } from 'lucide-react';
import { ChatMessage } from '@types/api';
import { formatRelativeTime, cn } from '@lib/utils/format';
import { motion } from 'framer-motion';

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.type === 'user';
  const isSystem = message.type === 'system';

  if (isSystem) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex justify-center"
      >
        <div className="flex items-center gap-2 px-4 py-2 bg-amber-100 dark:bg-amber-900/30 rounded-full">
          <AlertCircle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
          <span className="text-sm font-medium text-amber-900 dark:text-amber-100">
            {message.content}
          </span>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn('flex', isUser ? 'justify-end' : 'justify-start')}
    >
      <div
        className={cn(
          'flex gap-3 max-w-[85%]',
          isUser ? 'flex-row-reverse' : 'flex-row'
        )}
      >
        {/* Avatar */}
        <div
          className={cn(
            'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
            isUser
              ? 'bg-blue-600 text-white'
              : 'bg-purple-600 dark:bg-purple-500 text-white'
          )}
        >
          {isUser ? (
            <User className="w-5 h-5" />
          ) : (
            <Bot className="w-5 h-5" />
          )}
        </div>

        {/* Message content */}
        <div className={cn('flex flex-col', isUser ? 'items-end' : 'items-start')}>
          <div
            className={cn(
              'px-4 py-2.5 rounded-2xl text-sm leading-relaxed',
              isUser
                ? 'bg-blue-600 text-white rounded-br-sm'
                : 'bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-700 rounded-bl-sm'
            )}
          >
            {message.content}
          </div>
          <span className="text-xs text-slate-400 dark:text-slate-500 mt-1 px-1">
            {formatRelativeTime(message.timestamp)}
          </span>
        </div>
      </div>
    </motion.div>
  );
}
```

### 3.4 Typing Indicator Component

**Create `src/components/byrd/TypingIndicator.tsx`**:

```typescript
import { Bot } from 'lucide-react';
import { motion } from 'framer-motion';

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex justify-start"
    >
      <div className="flex gap-3 max-w-[85%]">
        {/* Avatar */}
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-600 dark:bg-purple-500 flex items-center justify-center">
          <Bot className="w-5 h-5 text-white" />
        </div>

        {/* Typing animation */}
        <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 px-4 py-3 rounded-2xl rounded-bl-sm">
          <div className="flex gap-1.5">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.5, 1, 0.5],
                }}
                transition={{
                  duration: 0.8,
                  repeat: Infinity,
                  delay: i * 0.15,
                }}
              />
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
```

### 3.5 Chat Input Component

**Create `src/components/byrd/ChatInput.tsx`**:

```typescript
import { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Mic, Command } from 'lucide-react';
import { useByrdStore } from '@store/byrdStore';
import { cn } from '@lib/utils/cn';

export function ChatInput() {
  const [input, setInput] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { addMessage, isTyping } = useByrdStore();

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
  }, [input]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    // Add user message
    addMessage({
      id: `msg_${Date.now()}`,
      type: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString(),
    });

    setInput('');

    // Send to backend (implement API call)
    // ...

    // Simulate BYRD response (replace with actual API)
    setTimeout(() => {
      addMessage({
        id: `msg_${Date.now()}_response`,
        type: 'byrd',
        content: 'I received your message. Processing...',
        timestamp: new Date().toISOString(),
      });
    }, 1000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={cn(
        'flex-shrink-0 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-700 p-4 safe-area-inset-bottom transition-shadow',
        isFocused && 'shadow-lg'
      )}
    >
      <div className="flex items-end gap-2 max-w-4xl mx-auto">
        {/* Command indicator */}
        <button
          type="button"
          className="p-3 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
          title="Commands (⌘K)"
        >
          <Command className="w-5 h-5" />
        </button>

        {/* Text input */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Type to BYRD..."
            rows={1}
            className={cn(
              'w-full px-4 py-3 pr-12 rounded-xl resize-none',
              'bg-slate-100 dark:bg-slate-800',
              'border border-transparent',
              'focus:bg-white dark:focus:bg-slate-700',
              'focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20',
              'text-slate-900 dark:text-slate-100 placeholder-slate-400',
              'transition-all duration-200',
              'max-h-48 overflow-y-auto'
            )}
            disabled={isTyping}
          />

          {/* Character counter (for long messages) */}
          {input.length > 200 && (
            <span className="absolute bottom-2 right-2 text-xs text-slate-400">
              {input.length}
            </span>
          )}
        </div>

        {/* Action buttons */}
        <div className="flex gap-2">
          {/* Attachment */}
          <button
            type="button"
            className="p-3 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors hidden sm:block"
            title="Attach file"
          >
            <Paperclip className="w-5 h-5" />
          </button>

          {/* Voice input (if available) */}
          <button
            type="button"
            className="p-3 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors hidden sm:block"
            title="Voice input"
          >
            <Mic className="w-5 h-5" />
          </button>

          {/* Send button */}
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className={cn(
              'p-3 rounded-xl transition-all duration-200',
              'bg-purple-600 hover:bg-purple-700 text-white',
              'disabled:bg-slate-300 dark:disabled:bg-slate-700 disabled:cursor-not-allowed',
              'active:scale-95'
            )}
            title="Send (⌘Enter)"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </form>
  );
}
```

### 3.6 Status Bar Component

**Create `src/components/byrd/StatusBar.tsx`**:

```typescript
import { useState } from 'react';
import { ChevronDown, ChevronUp, RefreshCw } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useByrdStore } from '@store/byrdStore';
import { cn } from '@lib/utils/cn';

export function StatusBar() {
  const [isExpanded, setIsExpanded] = useState(true);
  const byrdState = useByrdStore((s) => s.byrdState);

  // Auto-collapse after 10 seconds
  /* Add auto-collapse logic */

  return (
    <div className="px-4 py-3 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
      {/* Collapsed state */}
      <AnimatePresence mode="wait">
        {!isExpanded && (
          <motion.button
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            onClick={() => setIsExpanded(true)}
            className="w-full flex items-center justify-between text-sm"
          >
            <div className="flex items-center gap-2">
              <RefreshCw className="w-4 h-4 text-purple-600 dark:text-purple-400 animate-spin-slow" />
              <span className="font-medium text-slate-900 dark:text-slate-100">
                Phase {byrdState?.rsi_phase}: PRACTICE
              </span>
            </div>
            <ChevronDown className="w-4 h-4 text-slate-400" />
          </motion.button>
        )}
      </AnimatePresence>

      {/* Expanded state */}
      <AnimatePresence mode="wait">
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="space-y-3"
          >
            {/* Main status */}
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-2">
                <RefreshCw className="w-4 h-4 text-purple-600 dark:text-purple-400 animate-spin-slow" />
                <div>
                  <p className="text-sm font-medium text-slate-900 dark:text-slate-100">
                    🔄 RSI Cycle #{byrdState?.rsi_cycle_number}
                  </p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Phase {byrdState?.rsi_phase}: PRACTICE • 2m 34s remaining
                  </p>
                </div>
              </div>
              <button
                onClick={() => setIsExpanded(false)}
                className="p-1 hover:bg-slate-100 dark:hover:bg-slate-700 rounded transition-colors"
              >
                <ChevronUp className="w-4 h-4 text-slate-400" />
              </button>
            </div>

            {/* Metrics */}
            <div className="flex gap-4 text-xs">
              <div className="flex items-center gap-1.5">
                <span className="text-slate-500 dark:text-slate-400">Emergence:</span>
                <span className="font-medium text-slate-900 dark:text-slate-100">0.847 ↑</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-slate-500 dark:text-slate-400">Treasury:</span>
                <span className="font-medium text-slate-900 dark:text-slate-100">$12.4K</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
```

### 3.7 BYRD Chat Page (Main Component)

**Create `src/components/byrd/ByrdChatPage.tsx`**:

```typescript
import { ArrowLeft, Settings } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { AvatarCanvas } from '../visualization/AvatarCanvas';
import { StatusBar } from './StatusBar';
import { ChatMessages } from './ChatMessages';
import { ChatInput } from './ChatInput';
import { useByrdStore } from '@store/byrdStore';
import { cn } from '@lib/utils/cn';

export function ByrdChatPage() {
  const navigate = useNavigate();
  const animationState = useByrdStore((s) => s.animationState);

  return (
    <div className="flex flex-col h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header */}
      <header className="flex-shrink-0 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 px-4 py-3">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <button
            onClick={() => navigate(-1)}
            className="p-2 -ml-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
            aria-label="Go back"
          >
            <ArrowLeft className="w-5 h-5 text-slate-600 dark:text-slate-400" />
          </button>

          <h1 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
            BYRD
          </h1>

          <button
            className="p-2 -mr-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
            aria-label="Settings"
          >
            <Settings className="w-5 h-5 text-slate-600 dark:text-slate-400" />
          </button>
        </div>
      </header>

      {/* 3D Avatar - 45% of viewport height */}
      <div className="flex-shrink-0 h-[45vh] min-h-[320px] max-h-[600px] relative">
        <AvatarCanvas
          modelPath="/models/cat.glb"
          animationState={animationState}
          autoRotate={false}
          className="w-full h-full"
        />
      </div>

      {/* Status Bar - Collapsible */}
      <StatusBar />

      {/* Chat Messages - Fills remaining space */}
      <div className="flex-1 min-h-0 bg-white dark:bg-slate-800">
        <ChatMessages />
      </div>

      {/* Chat Input - Fixed at bottom */}
      <ChatInput />
    </div>
  );
}
```

---

## Phase 4: Dashboard Pages (Day 4-6)

### Goal: Build all remaining pages with mobile-first responsive layouts

### 4.1 Dashboard Page (Home)

**Update `src/components/dashboard/DashboardPage.tsx`**:

```typescript
import { motion } from 'framer-motion';
import { AnimatedCounter } from '../common/AnimatedCounter';
import { StatCard } from '../common/StatCard';
import { HeroMetric } from './HeroMetric';
import { QuickStats } from './QuickStats';
import { RecentActivity } from './RecentActivity';

export function DashboardPage() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 pb-20">
      {/* Header */}
      <div className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 px-4 py-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
            Dashboard
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            BYRD Recursive Self-Improvement Overview
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {/* Hero Metric - ASI Probability */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <HeroMetric
            title="ASI PROBABILITY"
            value={42.7}
            unit="%"
            trend={{ value: 2.3, direction: 'up' }}
            subtitle="+2.3% this week"
          />
        </motion.div>

        {/* Quick Stats - Horizontal scroll */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
        >
          <QuickStats />
        </motion.div>

        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.2 }}
        >
          <StatCard
            title="System Status"
            value="● Online"
            status="success"
            className="bg-white dark:bg-slate-800"
          >
            <div className="mt-4 space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-500 dark:text-slate-400">RSI Engine</span>
                <span className="text-green-600 dark:text-green-400 font-medium">Running</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 dark:text-slate-400">Verification</span>
                <span className="text-green-600 dark:text-green-400 font-medium">Active</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 dark:text-slate-400">Economic</span>
                <span className="text-amber-600 dark:text-amber-400 font-medium">Processing</span>
              </div>
            </div>
          </StatCard>
        </motion.div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.3 }}
        >
          <RecentActivity />
        </motion.div>
      </div>
    </div>
  );
}
```

### 4.2 Hero Metric Component

**Create `src/components/dashboard/HeroMetric.tsx`**:

```typescript
import { AnimatedCounter } from '../common/AnimatedCounter';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { cn } from '@lib/utils/cn';

interface HeroMetricProps {
  title: string;
  value: number;
  unit?: string;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
  };
  subtitle?: string;
  className?: string;
}

export function HeroMetric({
  title,
  value,
  unit,
  trend,
  subtitle,
  className,
}: HeroMetricProps) {
  const TrendIcon = trend?.direction === 'up' ? TrendingUp : trend?.direction === 'down' ? TrendingDown : Minus;

  return (
    <div
      className={cn(
        'bg-gradient-to-br from-purple-50 to-white dark:from-purple-900/20 dark:to-slate-800',
        'border border-purple-100 dark:border-purple-800',
        'rounded-2xl p-6 shadow-sm',
        className
      )}
    >
      <div className="space-y-4">
        {/* Title */}
        <h2 className="text-xs font-semibold tracking-wider uppercase text-slate-500 dark:text-slate-400">
          {title}
        </h2>

        {/* Main value */}
        <div className="flex items-baseline gap-2">
          <AnimatedCounter
            value={value}
            decimals={1}
            className="text-5xl font-bold text-slate-900 dark:text-slate-100"
          />
          {unit && (
            <span className="text-2xl font-semibold text-slate-600 dark:text-slate-400">
              {unit}
            </span>
          )}
        </div>

        {/* Trend & subtitle */}
        <div className="flex items-center gap-3">
          {trend && (
            <div
              className={cn(
                'flex items-center gap-1 px-2 py-1 rounded-full text-sm font-medium',
                trend.direction === 'up' && 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300',
                trend.direction === 'down' && 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300',
                trend.direction === 'neutral' && 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
              )}
            >
              <TrendIcon className="w-4 h-4" />
              <span>{trend.direction === 'up' ? '+' : ''}{trend.value}%</span>
            </div>
          )}

          {subtitle && (
            <p className="text-sm text-slate-500 dark:text-slate-400">
              {subtitle}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
```

### 4.3 Quick Stats Component

**Create `src/components/dashboard/QuickStats.tsx`**:

```typescript
import { StatCard } from '../common/StatCard';
import { Clock, Sparkles, DollarSign, Shield } from 'lucide-react';

const quickStats = [
  {
    id: 'rsi',
    title: 'RSI Cycle',
    value: 'Phase 3',
    subtitle: 'PRACTICE',
    icon: Clock,
    status: 'info' as const,
  },
  {
    id: 'emergence',
    title: 'Emergence',
    value: '0.847',
    subtitle: '↑ 0.023',
    icon: Sparkles,
    status: 'success' as const,
  },
  {
    id: 'treasury',
    title: 'Treasury',
    value: '$12.4K',
    subtitle: '+$892 today',
    icon: DollarSign,
    status: 'success' as const,
  },
  {
    id: 'safety',
    title: 'Safety',
    value: '● Nominal',
    subtitle: 'All systems',
    icon: Shield,
    status: 'success' as const,
  },
];

export function QuickStats() {
  return (
    <div className="flex gap-4 overflow-x-auto pb-2 scrollbar-hide">
      {quickStats.map((stat) => {
        const Icon = stat.icon;

        return (
          <div
            key={stat.id}
            className="flex-shrink-0 w-36 bg-white dark:bg-slate-800 rounded-xl p-4 border border-slate-200 dark:border-slate-700 shadow-sm"
          >
            <div className="flex items-center gap-2 mb-2">
              <div className={`p-1.5 rounded-lg bg-${stat.status === 'success' ? 'green' : stat.status === 'info' ? 'blue' : 'slate'}-100 dark:bg-${stat.status === 'success' ? 'green' : stat.status === 'info' ? 'blue' : 'slate'}-900/30`}>
                <Icon className={`w-4 h-4 text-${stat.status === 'success' ? 'green' : stat.status === 'info' ? 'blue' : 'slate'}-600 dark:text-${stat.status === 'success' ? 'green' : stat.status === 'info' ? 'blue' : 'slate'}-400`} />
              </div>
            </div>

            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">
              {stat.title}
            </p>

            <p className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-0.5">
              {stat.value}
            </p>

            <p className="text-xs text-slate-400 dark:text-slate-500">
              {stat.subtitle}
            </p>
          </div>
        );
      })}
    </div>
  );
}
```

### 4.4 Recent Activity Component

**Update `src/components/dashboard/RecentActivity.tsx`**:

```typescript
import { CheckCircle, AlertCircle, Info } from 'lucide-react';
import { formatRelativeTime } from '@lib/utils/format';

const activities = [
  {
    id: 1,
    type: 'success' as const,
    title: 'RSI Cycle #28 Complete',
    description: 'All 8 phases executed successfully',
    timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
  },
  {
    id: 2,
    type: 'info' as const,
    title: 'New Desire Registered',
    description: 'Improve verification lattice coverage',
    timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
  },
  {
    id: 3,
    type: 'warning' as const,
    title: 'Entropic Drift Detected',
    description: 'Minor drift in economic module',
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
  },
];

export function RecentActivity() {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm p-4">
      <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Recent Activity
      </h3>

      <div className="space-y-4">
        {activities.map((activity) => {
          const Icon = activity.type === 'success' ? CheckCircle : activity.type === 'warning' ? AlertCircle : Info;

          return (
            <div key={activity.id} className="flex gap-3">
              <div className="flex-shrink-0 mt-0.5">
                <Icon
                  className={`w-4 h-4 ${
                    activity.type === 'success'
                      ? 'text-green-600 dark:text-green-400'
                      : activity.type === 'warning'
                      ? 'text-amber-600 dark:text-amber-400'
                      : 'text-blue-600 dark:text-blue-400'
                  }`}
                />
              </div>

              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-slate-900 dark:text-slate-100">
                  {activity.title}
                </p>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                  {activity.description}
                </p>
                <p className="text-xs text-slate-400 dark:text-slate-500 mt-1">
                  {formatRelativeTime(activity.timestamp)}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

---

## Phase 5: Advanced Visualizations (Day 6-7)

### Goal: Implement interactive charts and 3D visualizations

### 5.1 Animated Counter Component

**Create `src/components/common/AnimatedCounter.tsx`**:

```typescript
import { useEffect, useRef, useState } from 'react';
import CountUp from 'countup.js';
import { cn } from '@lib/utils/cn';

interface AnimatedCounterProps {
  value: number;
  decimals?: number;
  duration?: number;
  className?: string;
}

export function AnimatedCounter({
  value,
  decimals = 0,
  duration = 1,
  className,
}: AnimatedCounterProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const [hasAnimated, setHasAnimated] = useState(false);

  useEffect(() => {
    if (!ref.current || hasAnimated) return;

    const countUp = new CountUp(ref.current, value, {
      duration,
      decimalPlaces: decimals,
      separator: ',',
    });

    if (!countUp.error) {
      countUp.start();
      setHasAnimated(true);
    } else {
      ref.current.textContent = value.toFixed(decimals);
    }
  }, [value, decimals, duration, hasAnimated]);

  return (
    <span ref={ref} className={cn('tabular-nums', className)}>
      {value.toFixed(decimals)}
    </span>
  );
}
```

### 5.2 Line Chart Component

**Create `src/components/visualization/LineChart.tsx`**:

```typescript
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { DataPoint } from '@types/visualization';

interface LineChartProps {
  data: DataPoint[];
  dataKey: string;
  color?: string;
  height?: number;
}

export function LineChart({
  data,
  dataKey,
  color = '#7c3aed',
  height = 200,
}: LineChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsLineChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis
          dataKey="timestamp"
          tick={{ fill: '#94a3b8', fontSize: 12 }}
          tickFormatter={(value) => new Date(value).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        />
        <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
        <Tooltip
          contentStyle={{
            backgroundColor: '#1e293b',
            border: 'none',
            borderRadius: '8px',
            color: '#f8fafc',
          }}
          labelFormatter={(value) => new Date(value).toLocaleString()}
        />
        <Line
          type="monotone"
          dataKey={dataKey}
          stroke={color}
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, stroke: color, strokeWidth: 2, fill: '#fff' }}
        />
      </RechartsLineChart>
    </ResponsiveContainer>
  );
}
```

### 5.3 Sparkline Component

**Create `src/components/visualization/Sparkline.tsx`**:

```typescript
import { AreaChart, Area, ResponsiveContainer } from 'recharts';

interface SparklineProps {
  data: number[];
  width?: number;
  height?: number;
  color?: string;
}

export function Sparkline({
  data,
  width = 100,
  height = 40,
  color = '#7c3aed',
}: SparklineProps) {
  const chartData = data.map((value, index) => ({ index, value }));

  return (
    <ResponsiveContainer width={width} height={height}>
      <AreaChart data={chartData} margin={{ top: 0, right: 0, bottom: 0, left: 0 }}>
        <defs>
          <linearGradient id={`gradient-${color}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity={0.3} />
            <stop offset="100%" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        <Area
          type="monotone"
          dataKey="value"
          stroke={color}
          strokeWidth={2}
          fill={`url(#gradient-${color})`}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

---

## Phase 6: Polish & Launch (Day 7-8)

### Goal: Final polish, testing, and deployment

### 6.1 Performance Optimizations

1. **Code Splitting**:
   ```typescript
   // Lazy load page components
   const ByrdChatPage = lazy(() => import('./components/byrd/ByrdChatPage'));
   const RSIPage = lazy(() => import('./components/rsi/RSIPage'));
   // etc.
   ```

2. **Image Optimization**:
   - Serve compressed GLB model
   - Use WebP for static images
   - Lazy load images below fold

3. **3D Performance**:
   - LOD (Level of Detail) for avatar
   - Reduce polygon count on mobile
   - Throttle frame rate when not interacting

4. **Bundle Size**:
   - Tree-shake unused code
   - Use dynamic imports for heavy libraries
   - Minimize dependencies

### 6.2 Testing Checklist

- [ ] All 6 pages load without errors
- [ ] Bottom navigation works on all pages
- [ ] 3D avatar renders and accepts interaction
- [ ] Chat messages send and receive
- [ ] Real-time WebSocket updates working
- [ ] Responsive layouts tested (320px, 375px, 768px, 1024px, 1440px)
- [ ] Dark mode toggle works
- [ ] Touch gestures work (rotate, zoom, pan)
- [ ] Keyboard navigation works (desktop)
- [ ] No console errors
- [ ] Lighthouse score > 90 (Performance, Accessibility, Best Practices)

### 6.3 Accessibility Audit

- [ ] All images have alt text
- [ ] Color contrast ratios meet WCAG AA
- [ ] Touch targets ≥ 44×44px
- [ ] Focus indicators visible
- [ ] Semantic HTML (nav, main, header, footer)
- [ ] ARIA labels on interactive elements
- [ ] Keyboard navigation complete
- [ ] Screen reader testing

### 6.4 Deployment

```bash
# Build for production
cd frontend
npm run build

# Output will be in /dist
# Copy to server static directory or deploy to CDN

# For embedded mode (server.py serves files)
# The build output should be accessible at the root path
```

**Update `server.py` to serve new frontend**:

```python
# Add these routes to server.py

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")

# Serve index.html for all routes (SPA routing)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    file_path = Path("frontend/dist") / "index.html"
    if file_path.exists():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")
```

---

## Dependencies

### package.json

```json
{
  "name": "byrd-frontend",
  "version": "2.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.21.0",
    "framer-motion": "^10.16.0",
    "zustand": "^4.4.0",
    "@tanstack/react-query": "^5.17.0",
    "three": "^0.160.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.95.0",
    "recharts": "^2.10.0",
    "countup.js": "^2.8.0",
    "lucide-react": "^0.300.0",
    "react-hook-form": "^7.49.0",
    "@hookform/resolvers": "^3.3.0",
    "zod": "^3.22.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@types/three": "^0.160.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.56.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0"
  }
}
```

---

## Testing Strategy

### Unit Tests

```typescript
// Example: AvatarCanvas.test.tsx
import { render, screen } from '@testing-library/react';
import { AvatarCanvas } from './AvatarCanvas';

describe('AvatarCanvas', () => {
  it('renders loading state initially', () => {
    render(<AvatarCanvas modelPath="/models/cat.glb" />);
    expect(screen.getByRole('status')).toHaveTextContent('Loading...');
  });

  it('shows camera controls when loaded', async () => {
    render(<AvatarCanvas modelPath="/models/cat.glb" />);
    // Wait for model to load
    expect(await screen.findByTitle('Reset view')).toBeInTheDocument();
  });
});
```

### E2E Tests

```typescript
// Example: Playwright test for BYRD chat page
test('user can send message to BYRD', async ({ page }) => {
  await page.goto('/#/byrd');

  // Type message
  await page.fill('textarea', 'What is your current goal?');

  // Send message
  await page.click('button[title="Send"]');

  // Wait for response
  await expect(page.locator('.message-byrd')).toBeVisible();
});
```

### Performance Testing

```bash
# Lighthouse CI
npm install -g @lhci/cli
lhci autorun --collect.url="http://localhost:3000"

# Results should meet:
# Performance: > 90
# Accessibility: > 90
# Best Practices: > 90
# SEO: > 80
```

---

## Success Metrics

### Performance

- **FCP** (First Contentful Paint): < 1.5s
- **LCP** (Largest Contentful Paint): < 2.5s
- **TTI** (Time to Interactive): < 3.5s
- **CLS** (Cumulative Layout Shift): < 0.1

### User Experience

- 3D avatar loads in < 2s on 4G
- Page transitions < 300ms
- Touch response < 100ms
- No visible jank (60fps)

### Business Metrics

- Session duration > 5 min
- Return visits > 40%
- BYRD chat usage > 60% of sessions
- Mobile usage > 50%

---

## Maintenance Plan

### Weekly

- Monitor error rates (Sentry)
- Check performance metrics
- Review user feedback

### Monthly

- Update dependencies
- Review bundle size
- Optimize assets

### Quarterly

- Accessibility audit
- User testing sessions
- Feature prioritization

---

## Appendix: Quick Reference

### File Naming Conventions

- Components: `PascalCase.tsx` (e.g., `AvatarCanvas.tsx`)
- Hooks: `camelCase.ts` (e.g., `useBreakpoint.ts`)
- Utils: `camelCase.ts` (e.g., `format.ts`)
- Stores: `camelCase.ts` (e.g., `byrdStore.ts`)
- Types: `camelCase.ts` (e.g., `api.ts`)

### Git Commit Convention

```
feat: add BYRD chat page with 3D avatar
fix: correct mobile viewport height
refactor: extract AvatarCanvas component
style: format with prettier
test: add unit tests for chat input
docs: update implementation plan
chore: update dependencies
```

### Environment Variables

```bash
# .env.local
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
VITE_MODEL_PATH=/models/cat.glb
```

---

## Conclusion

This implementation plan provides everything needed to one-shot the mobile-first BYRD ASI frontend. Follow the phases sequentially, test thoroughly at each stage, and maintain the design system principles throughout.

**Key Success Factors:**

1. **Mobile-First** - Start small, enhance up
2. **Component Reusability** - Build once, use everywhere
3. **Performance** - Optimize from day one
4. **Accessibility** - Build inclusive by default
5. **User Experience** - Every interaction matters

Estimated timeline: 7-10 days for full implementation.

Good luck building the future of ASI interfaces! 🚀
