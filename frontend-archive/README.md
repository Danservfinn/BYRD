# BYRD Frontend Archive

These files represent the original BYRD visualization frontend (pre-RSI dashboard).

**Archived:** 2026-01-06
**Reason:** Replaced with RSI-aware React dashboard

## Original Files

| File | Size | Purpose |
|------|------|---------|
| `byrd-3d-visualization.html` | 297KB | Three.js 3D mind space with force-directed graph |
| `byrd-memory-topology.html` | 263KB | Memory graph with RSI phase coloring |
| `byrd-architecture.html` | 84KB | Architecture documentation viewer |
| `byrd-dream-visualization.html` | 112KB | Dream cycle visualization (deprecated) |
| `byrd-cat-visualization.html` | 27KB | Black cat avatar (ego space) |
| `BYRDVisualization.jsx` | 33KB | React dream component |
| `three_test.html` | 1KB | Three.js test |
| `viz-test.html` | 2KB | Visualization test |
| `webgl-test.html` | 1KB | WebGL test |

## Technologies Used

- **Three.js v0.160.0** - 3D WebGL rendering
- **Tailwind CSS v4** - Utility-first styling (CDN)
- **WebSocket** - Real-time event streaming
- **Canvas API** - Cat avatar animations

## Key Features

1. **Mind Space** - 3D neural network visualization of beliefs, desires, capabilities
2. **Memory Topology** - Force-directed graph with RSI phase coloring
3. **Ego Space** - Animated cat avatar with thought bubbles
4. **Real-time Updates** - WebSocket-based event streaming

## Restoration

To restore these files for reference or rollback:

```bash
# Copy single file
cp frontend-archive/byrd-3d-visualization.html ./

# Restore all
cp frontend-archive/*.html ./
cp frontend-archive/*.jsx ./
```

## Design Tokens (Preserved)

```css
/* Node Colors */
--node-experience: #2563eb;
--node-belief: #d97706;
--node-desire: #db2777;
--node-capability: #7c3aed;
--node-crystal: #0891b2;
--node-reflection: #059669;

/* RSI Phase Colors */
--rsi-reflect: #8b5cf6;
--rsi-verify: #6366f1;
--rsi-collapse: #ec4899;
--rsi-route: #f59e0b;
--rsi-practice: #10b981;
--rsi-record: #3b82f6;
--rsi-crystallize: #06b6d4;
--rsi-measure: #84cc16;
```

## API Endpoints Used

- `GET /api/status` - System status
- `POST /api/start` - Start BYRD
- `POST /api/stop` - Stop BYRD
- `POST /api/reset` - Reset all state
- `WS /ws/events` - Real-time event stream

---

*This archive preserves the original frontend for reference during the RSI dashboard migration.*
