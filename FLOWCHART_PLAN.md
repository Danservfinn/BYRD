# Architecture Flowchart Redesign Plan

## Overview

Replace the current 3D orbital visualization with an interactive 2D SVG flowchart that clearly shows BYRD's component architecture, data flows, and relationships.

## Current State Analysis

**Current Implementation** (`byrd-architecture.html`):
- 675 lines using Three.js for 3D rendering
- Orbital module visualization with Memory at center
- Animated modules rotating on orbits
- Curved bezier data flow lines
- Click interaction to highlight connections
- Right panel for module details

**Issues with 3D approach**:
- Harder to see all connections at once
- Animation can be distracting
- Not immediately clear which components connect to which
- Depth perception makes flow direction unclear

## Proposed Flowchart Design

### Layout Structure

```
┌──────────────────────────────────────────────────────────────────────┐
│                              HEADER                                   │
│  [Back] BYRD Architecture                        [Running] [Refresh] │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                         ┌─────────────┐                               │
│                         │   QUANTUM   │                               │
│                         │  PROVIDER   │                               │
│                         └──────┬──────┘                               │
│                                │ randomness                           │
│                                ▼                                      │
│   ┌───────────┐         ┌───────────┐         ┌───────────┐          │
│   │  SEEKER   │◄───────▶│  MEMORY   │◄───────▶│  DREAMER  │          │
│   │ (research)│         │  (Neo4j)  │         │ (reflect) │          │
│   └─────┬─────┘         └─────┬─────┘         └─────┬─────┘          │
│         │                     │                     │                 │
│         │ pattern     context │ events     beliefs │                 │
│         ▼             ▼       │    ▼       desires ▼                 │
│   ┌───────────┐  ┌───────────┐│┌───────────┐ ┌───────────┐          │
│   │   CODER   │  │   ACTOR   │││ EVENT BUS │ │ NARRATOR  │          │
│   │  (build)  │  │ (respond) │││ (stream)  │ │  (voice)  │          │
│   └─────┬─────┘  └───────────┘│└─────┬─────┘ └───────────┘          │
│         │                     │      │                               │
│         ▼                     ▼      ▼                               │
│   ┌───────────┐         ┌───────────────────┐                        │
│   │SELF-MOD   │         │   VISUALIZATION   │                        │
│   │(evolve)   │         │   (browser)       │                        │
│   └───────────┘         └───────────────────┘                        │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────┬──────────────────────────────┐
│           DATA FLOW LEGEND            │        SELECTED MODULE       │
│  ─── Context  ─── Events  ─── Identity│   [Details panel]           │
│  ─── Research ─── Randomness          │                              │
└───────────────────────────────────────┴──────────────────────────────┘
```

### Technical Implementation

**Technology Stack**:
- Pure SVG (no Three.js dependency)
- CSS animations for subtle data flow effects
- Tailwind CSS for styling consistency
- Same API endpoint (`/api/architecture`)
- Maintain same color scheme (dark theme, violet accents)

### Component Boxes

Each component rendered as an SVG `<g>` group:

```svg
<g id="memory" class="component" data-module="Memory">
  <!-- Main box with gradient fill -->
  <rect x="350" y="200" width="160" height="80" rx="12"
        fill="url(#memoryGradient)" stroke="#3b82f6"/>

  <!-- Icon -->
  <circle cx="390" cy="240" r="16" fill="#3b82f6" opacity="0.3"/>
  <path d="..." fill="#3b82f6"/>

  <!-- Label -->
  <text x="430" y="235" class="component-title">MEMORY</text>
  <text x="430" y="255" class="component-subtitle">(Neo4j)</text>

  <!-- Status indicator -->
  <circle cx="498" cy="212" r="6" class="status-dot status-active"/>
</g>
```

### Data Flow Arrows

Animated SVG paths with directional markers:

```svg
<!-- Arrow definition -->
<defs>
  <marker id="arrowhead" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#a78bfa"/>
  </marker>

  <!-- Animated dash pattern -->
  <style>
    .flow-line {
      stroke-dasharray: 5 5;
      animation: flow 1s linear infinite;
    }
    @keyframes flow {
      to { stroke-dashoffset: -10; }
    }
  </style>
</defs>

<!-- Flow line -->
<path d="M430,280 L430,320" class="flow-line"
      stroke="#a78bfa" stroke-width="2"
      marker-end="url(#arrowhead)"/>
<text x="445" y="305" class="flow-label">context</text>
```

### Component Positions

```javascript
const COMPONENT_LAYOUT = {
  // Central hub
  Memory:     { x: 400, y: 200, w: 160, h: 80 },

  // Primary processors (left and right of Memory)
  Dreamer:    { x: 620, y: 200, w: 140, h: 70 },
  Seeker:     { x: 180, y: 200, w: 140, h: 70 },

  // Secondary (below Memory)
  Actor:      { x: 400, y: 340, w: 120, h: 60 },
  EventBus:   { x: 550, y: 340, w: 120, h: 60 },

  // Extensions
  Coder:      { x: 180, y: 340, w: 120, h: 60 },
  SelfMod:    { x: 180, y: 440, w: 120, h: 60 },
  Narrator:   { x: 620, y: 340, w: 120, h: 60 },

  // Infrastructure
  Quantum:    { x: 620, y: 80, w: 140, h: 60 },
  Visualizer: { x: 400, y: 440, w: 160, h: 60 },
};
```

### Data Flows Configuration

```javascript
const DATA_FLOWS = [
  // Memory ↔ Dreamer
  { from: 'Memory', to: 'Dreamer', type: 'context', label: 'experiences' },
  { from: 'Dreamer', to: 'Memory', type: 'reflection', label: 'beliefs, desires' },

  // Memory ↔ Seeker
  { from: 'Memory', to: 'Seeker', type: 'context', label: 'desires' },
  { from: 'Seeker', to: 'Memory', type: 'research', label: 'research, caps' },

  // Memory ↔ Actor
  { from: 'Memory', to: 'Actor', type: 'context', label: 'context' },
  { from: 'Actor', to: 'Memory', type: 'action', label: 'experiences' },

  // Seeker → Coder
  { from: 'Seeker', to: 'Coder', type: 'action', label: 'code desires' },

  // Coder → SelfMod
  { from: 'Coder', to: 'SelfMod', type: 'modification', label: 'changes' },

  // Quantum → Dreamer
  { from: 'Quantum', to: 'Dreamer', type: 'randomness', label: 'entropy' },

  // Quantum → Narrator
  { from: 'Quantum', to: 'Narrator', type: 'randomness', label: 'entropy' },

  // Memory → EventBus
  { from: 'Memory', to: 'EventBus', type: 'event', label: 'changes' },

  // EventBus → Visualizer
  { from: 'EventBus', to: 'Visualizer', type: 'event', label: 'stream' },
];
```

### Color Scheme

```css
:root {
  /* Component colors (matching current) */
  --memory-color: #3b82f6;      /* Blue */
  --dreamer-color: #a78bfa;     /* Purple */
  --seeker-color: #22c55e;      /* Green */
  --actor-color: #fbbf24;       /* Amber */
  --coder-color: #f43f5e;       /* Rose */
  --quantum-color: #06b6d4;     /* Cyan */
  --eventbus-color: #14b8a6;    /* Teal */
  --ego-color: #ec4899;         /* Pink */
  --visualizer-color: #8b5cf6;  /* Violet */

  /* Flow line colors */
  --flow-reflection: #a78bfa;
  --flow-context: #3b82f6;
  --flow-research: #22c55e;
  --flow-event: #fbbf24;
  --flow-identity: #ec4899;
  --flow-randomness: #14b8a6;
  --flow-modification: #f43f5e;
}
```

### Interaction Features

1. **Hover Effects**:
   - Component box glows and scales slightly
   - Connected flow lines highlight
   - Tooltip shows component description

2. **Click Selection**:
   - Selected component highlighted with ring
   - All connected flows emphasized
   - Detail panel shows stats and description

3. **Flow Animation Toggle**:
   - Button to pause/resume flow animations
   - Helps focus on structure vs. dynamics

### Side Panel

Keep the existing right panel structure:
- Module list with status indicators
- Memory schema display
- External integrations
- Selected module details

### Responsive Considerations

```css
/* Scale SVG for smaller screens */
@media (max-width: 1200px) {
  .flowchart-container {
    transform: scale(0.8);
    transform-origin: top center;
  }
}

@media (max-width: 900px) {
  /* Stack layout vertically */
  .flowchart-container {
    transform: scale(0.6);
  }
  .side-panel {
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 200px;
  }
}
```

## Implementation Steps

### Phase 1: SVG Foundation
1. Create basic HTML structure with Tailwind
2. Implement SVG canvas with viewBox
3. Define gradients, markers, and styles
4. Create component box rendering function

### Phase 2: Layout & Components
1. Position all component boxes
2. Add icons for each component
3. Implement status indicators
4. Add labels and subtitles

### Phase 3: Data Flows
1. Calculate path points between components
2. Render arrow paths with markers
3. Add flow labels
4. Implement dash animation

### Phase 4: Interactivity
1. Hover effects on components
2. Click selection with highlighting
3. Flow emphasis on selection
4. Detail panel updates

### Phase 5: Data Integration
1. Fetch from `/api/architecture`
2. Map API data to component states
3. Update status indicators
4. Populate side panel

### Phase 6: Polish
1. Add smooth transitions
2. Test responsive behavior
3. Ensure accessibility (ARIA labels)
4. Performance optimization

## File Changes

| File | Action |
|------|--------|
| `byrd-architecture.html` | Complete rewrite |

## Preserved Features

- Same color scheme and glass-panel aesthetic
- Same API endpoint integration
- Same side panel layout
- Same header with back link
- Same data flow legend (updated for 2D)
- Module click → detail display

## Removed Features

- Three.js dependency
- 3D camera controls
- Orbital animations
- Perspective depth

## New Features

- Clear hierarchical layout
- Labeled flow arrows
- Better visibility of all connections
- Simpler mental model
- Faster load time (no 3D library)

## Success Criteria

1. All 9 components visible without interaction
2. All data flows clearly labeled and directional
3. Click on any component shows its connections
4. Same data from API displayed accurately
5. Works on screens >= 1024px wide
6. Load time < 1 second
