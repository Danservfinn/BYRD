---
title: Visualization System
link: visualization-system
type: metadata
ontological_relations: []
tags: [visualization, 3d, webgl, mind-space, ego-space, websocket]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-24T00:00:00Z
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
- **Belief Nodes**: Yellow spheres (size = confidence)
- **Desire Nodes**: Magenta spheres (size = intensity)
- **Capability Nodes**: Green spheres
- **Connections**: Synaptic lines showing relationships
- **Physics**: Nodes organize through repulsion and gravity

### Ego Space
Embodied representation with black cat avatar.
- **Cat Avatar**: Animated 3D cat representing BYRD's ego
- **Ambient Animation**: Blinking, breathing, ear twitching
- **Thought Bubbles**: Inner voice displayed near avatar
- **Starfield Environment**: Deep space background

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

## Starting the Visualization

```bash
# Start server
python server.py

# Open in browser
# Mind Space: http://localhost:8000/byrd-3d-visualization.html
# Ego Space:  http://localhost:8000/byrd-cat-visualization.html
```
