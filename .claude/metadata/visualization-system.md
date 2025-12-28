---
title: Visualization System
link: visualization-system
type: metadata
ontological_relations: []
tags: [visualization, 3d, webgl, mind-space, ego-space, websocket, cat-animation, state-machine]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-28T12:00:00Z
uuid: v1s2u3a4-5678-90ab-cdef-visualize0001
---

## Purpose
Real-time 3D visualization of BYRD's cognitive state through WebSocket-based event streaming.

## Files
- `/Users/kurultai/BYRD/byrd-3d-visualization.html` - Mind Space (neural network)
- `/Users/kurultai/BYRD/byrd-architecture.html` - Architecture View (system modules)
- `/Users/kurultai/BYRD/byrd-cat-visualization.html` - Ego Space (cat avatar)
- `/Users/kurultai/BYRD/server.py` - WebSocket + REST API server

## Visualization Modes

### Mind Space
3D neural network visualization showing beliefs, desires, and connections.
- **Belief Nodes**: Amber spheres (size = confidence)
- **Desire Nodes**: Rose spheres (size = intensity)
- **Capability Nodes**: Violet spheres
- **Reflection Nodes**: Emerald spheres
- **Experience Nodes**: Sky blue spheres
- **OS Node**: Black cat head at center (BYRD's self-model)
- **Connections**: Dark slate lines (0x475569) for visibility on light background
- **Physics**: Force-directed with spring forces, connection-weighted gravity toward center
- **Node Scaling**: Logarithmic scaling based on connection count (hub nodes appear larger)

#### System Reset Behavior
On `system_reset` event:
1. Dream/seek counters reset to 0 immediately
2. Visualization cleared
3. Fresh status fetched from server after 1.5s

### Ego Space
Embodied representation with black cat avatar.
- **Cat Avatar**: Animated 3D cat representing BYRD's ego
- **Ambient Animation**: Blinking, breathing, ear twitching
- **Thought Bubbles**: Inner voice displayed near avatar
- **Starfield Environment**: Deep space background
- **Cat Animation System**: Event-driven animations (see below)

## Cat Animation System

The cat avatar is a living visualization of BYRD's cognitive state, driven by real backend events.

### State Machine
9 distinct behavioral states with smooth eased transitions:
- `IDLE` - Default: slow breathing, occasional blink
- `DREAMING` - Dream cycle: eyes half-closed, purple aura
- `SEEKING` - Research: dilated pupils, perked ears
- `PROCESSING` - Coding: focused eyes, thinking particles
- `ALERT` - New desire: wide eyes, rotated ears
- `SATISFIED` - Fulfilled: squinted eyes (cat smile), purr
- `FRUSTRATED` - Stuck: flattened ears, agitated
- `CONNECTING` - Memory access: whiskers extend to nodes
- `QUANTUM` - Collapse: pupils contract, freeze, burst

### Body Controllers
- **EyeController**: Pupil dilation, blinking, glow, look-at
- **EarController**: Alert rotation, random twitches
- **BodyPoseController**: Breathing, sway, posture changes
- **WhiskerController**: 12 whiskers (6/side) that connect to memory nodes

### Particle Effects
- **Aura System**: Purple/gold orbital particles during dreaming
- **Thought Particles**: Rising bubbles on `inner_voice` events
- **Quantum Burst**: Visual effect on `quantum_collapse`

### Audio Feedback
- Web Audio API synthesis (no external files)
- Tones: chime (440Hz), success (523Hz), quantum (330Hz)
- Toggle via UI button

### Event Coverage
Maps 40+ backend events to animations across categories:
dream cycle, seek cycle, desires, memory, quantum, coder, system

### Graph Mode
Full memory graph exploration (within Mind Space).
- **All Node Types**: Including reflections and custom types
- **Physics Simulation**: Interactive node dragging
- **Connection Display**: All relationships visible

### Architecture View
3D orbital visualization of BYRD's system architecture.
- **Central Memory Core**: Icosahedron at center representing Neo4j
- **Orbiting Modules**: Dreamer, Seeker, Actor, Coder, EventBus, Quantum, Ego
- **Data Flow Lines**: Color-coded curved lines showing data movement
- **Click Interactions**: Select modules to highlight connections
- **Real-time Updates**: Reflects current module status (active/idle/disabled)
- **API Endpoint**: `/api/architecture` provides live system data

## Genesis Modal
Displays BYRD's non-emergent foundations:
- Ego configuration used
- Seed questions
- Constitutional constraints

## WebSocket Protocol

### Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

### Event Format
```json
{
  "type": "belief_created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "id": "belief_abc123",
    "content": "...",
    "confidence": 0.85
  }
}
```

## REST API Endpoints

### Status
`GET /api/status` - System status including:
- Running state
- Dream/seek counts (persisted in Neo4j)
- Memory statistics
- Quantum status
- OS (Operating System) self-model
- AGI Runner metrics (if Option B enabled):
  - `enabled`, `bootstrapped`, `cycle_count`
  - `improvement_rate`, `goals_injected`, `research_indexed`
  - `patterns_seeded`, `recent_cycles`

### Control
- `POST /api/reset` - Reset BYRD (clears memory, restarts)
- `POST /api/start` - Start dream/seek cycles
- `POST /api/stop` - Stop dream/seek cycles

### Memory
- `POST /api/experience/message` - Send message to BYRD
- `GET /api/omega/metrics` - Option B loop metrics

## Starting the Visualization

```bash
# Start server
python server.py

# Open in browser
# Mind Space: http://localhost:8000/byrd-3d-visualization.html
# Ego Space:  http://localhost:8000/byrd-cat-visualization.html
```
