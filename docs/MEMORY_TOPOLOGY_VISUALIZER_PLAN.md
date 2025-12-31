# Memory Topology Visualizer - Implementation Plan

## Overview

A new visualization page (`byrd-memory-topology.html`) that displays BYRD's memory as **relationship-derived 3D geometry**. Instead of showing nodes and edges, we show the **shape of memory** - the geometric structures that emerge from how memories relate to each other.

**Core Insight**: When memories are interconnected, they define geometric shapes:
- 3 interconnected nodes → triangle face
- 4 interconnected nodes → tetrahedron
- Clusters of related nodes → organic crystalline structures

## Visual Design (Supermemory-Inspired)

### Color Palette

```javascript
const TOPOLOGY_COLORS = {
  // Background
  background: '#0f1419',           // Deep space
  backgroundSecondary: '#1a1f29',  // Slightly lighter

  // Glass-morphism layers
  glass: {
    fill: 'rgba(147, 197, 253, 0.08)',    // Subtle blue glass
    border: 'rgba(147, 197, 253, 0.35)',  // Border glow
    glow: 'rgba(147, 197, 253, 0.5)',     // Active glow
    highlight: 'rgba(255, 255, 255, 0.1)' // Inner highlight
  },

  // Relationship surface colors (by type)
  surfaces: {
    derived: 'rgba(147, 197, 253, 0.15)',   // Blue - DERIVED_FROM chains
    causal: 'rgba(251, 191, 36, 0.15)',     // Amber - causal relationships
    contradiction: 'rgba(244, 63, 94, 0.15)', // Rose - CONTRADICTS
    support: 'rgba(34, 211, 238, 0.15)',    // Cyan - SUPPORTS
    cluster: 'rgba(168, 85, 247, 0.15)'     // Violet - emergent clusters
  },

  // Node accent colors (vertices of shapes)
  nodes: {
    experience: '#60a5fa',   // Blue
    belief: '#fbbf24',       // Amber
    desire: '#f472b6',       // Pink
    capability: '#a78bfa',   // Violet
    crystal: '#22d3ee',      // Cyan
    reflection: '#34d399'    // Emerald
  },

  // Status indicators
  status: {
    forgotten: 'rgba(220, 38, 38, 0.15)',
    expiring: 'rgba(251, 165, 36, 0.8)',
    new: 'rgba(16, 185, 129, 0.4)',
    active: 'rgba(147, 197, 253, 0.6)'
  },

  // Text
  text: {
    primary: '#ffffff',
    secondary: '#e2e8f0',
    muted: '#94a3b8'
  }
};
```

### Visual Effects

1. **Glass-morphism surfaces**: Relationship triangles/polyhedra rendered with transparency and backdrop blur
2. **Bloom glow**: Blue-tinted UnrealBloomPass on active elements
3. **Particle dust**: Subtle floating particles in background
4. **Edge ribbons**: Flowing curved tubes for relationship chains
5. **Pulse animations**: New structures pulse into existence

---

## Architecture

### 1. Data Pipeline

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   /api/graph    │────▶│   Consolidator   │────▶│ Topology Engine │
│  (all nodes)    │     │   (2000 limit)   │     │   (geometry)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  Three.js Scene │
                                                 │ (glass surfaces)│
                                                 └─────────────────┘
```

### 2. Node Consolidation Strategy (2000 Limit)

#### Consolidation Hierarchy

```
Level 0: Individual Nodes (raw from Neo4j)
    ↓ (if > 2000 nodes)
Level 1: Temporal Clusters
    - Experiences > 7 days old → grouped by day
    - Each day-cluster = 1 meta-node
    ↓ (if still > 2000)
Level 2: Type Clusters
    - Group by type + time window
    - e.g., "Experiences from Dec 15-21" = 1 meta-node
    ↓ (if still > 2000)
Level 3: Connectivity Clusters
    - Use Louvain community detection
    - Each community = 1 meta-node with convex hull
```

#### Consolidation Algorithm

```javascript
async function consolidateNodes(rawNodes, rawRelationships, limit = 2000) {
  if (rawNodes.length <= limit) {
    return { nodes: rawNodes, relationships: rawRelationships, level: 0 };
  }

  // Phase 1: Temporal consolidation (old stuff first)
  const now = Date.now();
  const DAY_MS = 86400000;
  const WEEK_MS = DAY_MS * 7;

  const recent = [];      // < 7 days
  const older = [];       // >= 7 days

  rawNodes.forEach(node => {
    const age = now - new Date(node.timestamp).getTime();
    if (age < WEEK_MS) recent.push(node);
    else older.push(node);
  });

  // Group older nodes by day
  const dayBuckets = new Map();
  older.forEach(node => {
    const dayKey = new Date(node.timestamp).toISOString().split('T')[0];
    if (!dayBuckets.has(dayKey)) dayBuckets.set(dayKey, []);
    dayBuckets.get(dayKey).push(node);
  });

  // Create meta-nodes for each day
  const metaNodes = [];
  dayBuckets.forEach((nodes, day) => {
    metaNodes.push({
      id: `meta_${day}`,
      type: 'meta_cluster',
      label: `${day} (${nodes.length} memories)`,
      constituent_ids: nodes.map(n => n.id),
      count: nodes.length,
      centroid: computeCentroid(nodes),
      timestamp: day,
      importance: nodes.reduce((sum, n) => sum + (n.importance || 0.5), 0) / nodes.length
    });
  });

  const consolidated = [...recent, ...metaNodes];

  // Phase 2: If still over limit, apply Louvain clustering
  if (consolidated.length > limit) {
    return applyLouvainClustering(consolidated, rawRelationships, limit);
  }

  // Rebuild relationships for meta-nodes
  const consolidatedRels = rebuildRelationships(rawRelationships, consolidated);

  return {
    nodes: consolidated,
    relationships: consolidatedRels,
    level: 1,
    stats: {
      original: rawNodes.length,
      consolidated: consolidated.length,
      metaNodes: metaNodes.length
    }
  };
}
```

#### Meta-Node Visual Representation

Meta-nodes (consolidated clusters) are rendered as **convex hulls** of their constituent nodes' positions:

```javascript
function createMetaNodeGeometry(metaNode) {
  // Get positions of constituent nodes (or estimate from relationships)
  const positions = metaNode.constituent_positions ||
    estimatePositionsFromRelationships(metaNode);

  // Compute convex hull
  const hull = computeConvexHull3D(positions);

  // Create glass mesh
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(hull.vertices, 3));
  geometry.setIndex(hull.indices);
  geometry.computeVertexNormals();

  const material = new THREE.MeshPhysicalMaterial({
    color: TOPOLOGY_COLORS.surfaces.cluster,
    transparent: true,
    opacity: 0.15,
    roughness: 0.1,
    metalness: 0.0,
    transmission: 0.6,
    thickness: 0.5,
    side: THREE.DoubleSide
  });

  return new THREE.Mesh(geometry, material);
}
```

---

### 3. Relationship-Derived Geometry System

The core innovation: **relationships define surfaces, not just lines**.

#### Geometry Types

| Relationship Pattern | Geometry | Description |
|---------------------|----------|-------------|
| A→B→C (chain) | Ribbon/Tube | Flowing path through memories |
| A↔B↔C (triangle) | Triangle Face | Three mutually related memories |
| A↔B↔C↔D (tetrahedron) | Tetrahedron | Four fully connected memories |
| Star (A→B,C,D,E) | Radial Burst | Central concept with connections |
| Cluster (community) | Convex Hull | Organic crystalline shape |
| A⇄B (bidirectional) | Double Helix | Mutual reinforcement |

#### Clique Detection Algorithm

```javascript
/**
 * Find all cliques (fully connected subgraphs) in the relationship graph.
 * These become 3D polyhedra.
 */
function findCliques(nodes, relationships) {
  const adjacency = buildAdjacencyMap(nodes, relationships);
  const cliques = {
    triangles: [],    // 3-cliques → triangle faces
    tetrahedra: [],   // 4-cliques → tetrahedra
    higher: []        // 5+ cliques → complex polyhedra
  };

  // Bron-Kerbosch algorithm for maximal clique detection
  function bronKerbosch(R, P, X) {
    if (P.size === 0 && X.size === 0) {
      if (R.size >= 3) {
        const clique = Array.from(R);
        if (clique.length === 3) cliques.triangles.push(clique);
        else if (clique.length === 4) cliques.tetrahedra.push(clique);
        else cliques.higher.push(clique);
      }
      return;
    }

    const pivot = [...P, ...X][0];
    const pivotNeighbors = adjacency.get(pivot) || new Set();

    for (const v of P) {
      if (pivotNeighbors.has(v)) continue;

      const neighbors = adjacency.get(v) || new Set();
      bronKerbosch(
        new Set([...R, v]),
        new Set([...P].filter(n => neighbors.has(n))),
        new Set([...X].filter(n => neighbors.has(n)))
      );
      P.delete(v);
      X.add(v);
    }
  }

  bronKerbosch(new Set(), new Set(nodes.map(n => n.id)), new Set());
  return cliques;
}
```

#### Rendering Cliques as Geometry

```javascript
function renderCliques(cliques, nodePositions, scene) {
  const meshes = [];

  // Render triangles as glass faces
  cliques.triangles.forEach(triangle => {
    const positions = triangle.map(id => nodePositions.get(id));
    const geometry = new THREE.BufferGeometry();

    const vertices = new Float32Array([
      ...positions[0].toArray(),
      ...positions[1].toArray(),
      ...positions[2].toArray()
    ]);

    geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    geometry.computeVertexNormals();

    const material = createGlassMaterial(TOPOLOGY_COLORS.surfaces.derived);
    const mesh = new THREE.Mesh(geometry, material);
    mesh.userData = { type: 'triangle', nodeIds: triangle };

    scene.add(mesh);
    meshes.push(mesh);
  });

  // Render tetrahedra as 4-faced polyhedra
  cliques.tetrahedra.forEach(tetra => {
    const positions = tetra.map(id => nodePositions.get(id));
    const geometry = createTetrahedronGeometry(positions);
    const material = createGlassMaterial(TOPOLOGY_COLORS.surfaces.causal);

    const mesh = new THREE.Mesh(geometry, material);
    mesh.userData = { type: 'tetrahedron', nodeIds: tetra };

    scene.add(mesh);
    meshes.push(mesh);
  });

  // Render higher cliques as convex hulls
  cliques.higher.forEach(clique => {
    const positions = clique.map(id => nodePositions.get(id));
    const hull = computeConvexHull3D(positions);
    const geometry = createHullGeometry(hull);
    const material = createGlassMaterial(TOPOLOGY_COLORS.surfaces.cluster);

    const mesh = new THREE.Mesh(geometry, material);
    mesh.userData = { type: 'polyhedron', nodeIds: clique };

    scene.add(mesh);
    meshes.push(mesh);
  });

  return meshes;
}
```

#### Glass Material Shader

```javascript
function createGlassMaterial(baseColor) {
  return new THREE.ShaderMaterial({
    uniforms: {
      baseColor: { value: new THREE.Color(baseColor) },
      glassOpacity: { value: 0.15 },
      fresnelPower: { value: 2.0 },
      glowIntensity: { value: 0.3 },
      time: { value: 0 }
    },
    vertexShader: `
      varying vec3 vNormal;
      varying vec3 vViewPosition;
      varying vec2 vUv;

      void main() {
        vNormal = normalize(normalMatrix * normal);
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        vViewPosition = -mvPosition.xyz;
        vUv = uv;
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      uniform vec3 baseColor;
      uniform float glassOpacity;
      uniform float fresnelPower;
      uniform float glowIntensity;
      uniform float time;

      varying vec3 vNormal;
      varying vec3 vViewPosition;
      varying vec2 vUv;

      void main() {
        // Fresnel effect for glass edges
        vec3 viewDir = normalize(vViewPosition);
        float fresnel = pow(1.0 - abs(dot(viewDir, vNormal)), fresnelPower);

        // Base glass color with fresnel glow
        vec3 glass = baseColor * glassOpacity;
        vec3 edgeGlow = baseColor * fresnel * glowIntensity;

        // Subtle animation
        float pulse = 0.95 + 0.05 * sin(time * 2.0);

        vec3 finalColor = (glass + edgeGlow) * pulse;
        float finalAlpha = glassOpacity + fresnel * 0.3;

        gl_FragColor = vec4(finalColor, finalAlpha);
      }
    `,
    transparent: true,
    side: THREE.DoubleSide,
    depthWrite: false,
    blending: THREE.NormalBlending
  });
}
```

---

### 4. Relationship Chain Visualization

Chains of relationships (A→B→C→D) are rendered as flowing ribbons:

```javascript
function renderRelationshipChains(relationships, nodePositions, scene) {
  // Group relationships into chains
  const chains = findChains(relationships);

  chains.forEach(chain => {
    const points = chain.nodeIds.map(id => nodePositions.get(id));

    // Create smooth curve through points
    const curve = new THREE.CatmullRomCurve3(points, false, 'centripetal', 0.5);

    // Create tube geometry
    const tubeGeometry = new THREE.TubeGeometry(curve, 64, 0.3, 8, false);

    // Gradient material based on chain type
    const material = new THREE.ShaderMaterial({
      uniforms: {
        startColor: { value: new THREE.Color(TOPOLOGY_COLORS.nodes[chain.startType]) },
        endColor: { value: new THREE.Color(TOPOLOGY_COLORS.nodes[chain.endType]) },
        opacity: { value: 0.6 },
        time: { value: 0 }
      },
      vertexShader: `
        attribute float tubeT;
        varying float vT;
        void main() {
          vT = tubeT;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 startColor;
        uniform vec3 endColor;
        uniform float opacity;
        uniform float time;
        varying float vT;

        void main() {
          vec3 color = mix(startColor, endColor, vT);

          // Flowing animation
          float flow = fract(vT - time * 0.3);
          float pulse = smoothstep(0.0, 0.1, flow) * smoothstep(0.3, 0.2, flow);
          color += pulse * 0.3;

          gl_FragColor = vec4(color, opacity);
        }
      `,
      transparent: true
    });

    const tube = new THREE.Mesh(tubeGeometry, material);
    tube.userData = { type: 'chain', nodeIds: chain.nodeIds };
    scene.add(tube);
  });
}
```

---

### 5. Interactive Features

#### Expansion of Meta-Nodes

When a meta-node (consolidated cluster) is clicked, it expands to show constituent nodes:

```javascript
async function expandMetaNode(metaNode, scene) {
  // Fetch full data for constituent nodes
  const constituents = await fetch(`/api/nodes/batch?ids=${metaNode.constituent_ids.join(',')}`);

  // Animate expansion
  const expandAnimation = new TWEEN.Tween({ scale: 0, opacity: 0 })
    .to({ scale: 1, opacity: 1 }, 500)
    .easing(TWEEN.Easing.Elastic.Out)
    .onUpdate(({ scale, opacity }) => {
      constituents.forEach((node, i) => {
        const mesh = nodeToMesh(node);
        mesh.scale.setScalar(scale);
        mesh.material.opacity = opacity;

        // Position in sphere around meta-node centroid
        const phi = Math.acos(-1 + (2 * i + 1) / constituents.length);
        const theta = Math.sqrt(constituents.length * Math.PI) * phi;
        const radius = 5 + Math.sqrt(constituents.length);

        mesh.position.set(
          metaNode.position.x + radius * Math.cos(theta) * Math.sin(phi),
          metaNode.position.y + radius * Math.sin(theta) * Math.sin(phi),
          metaNode.position.z + radius * Math.cos(phi)
        );
      });
    });

  // Fade out meta-node hull
  const collapseHull = new TWEEN.Tween(metaNode.mesh.material)
    .to({ opacity: 0 }, 300)
    .onComplete(() => scene.remove(metaNode.mesh));

  expandAnimation.start();
  collapseHull.start();
}
```

#### Hover Effects

```javascript
function onNodeHover(node) {
  // Highlight connected structures
  const connected = findConnectedStructures(node.id);

  connected.triangles.forEach(tri => {
    tri.material.uniforms.glowIntensity.value = 0.6;
    tri.material.uniforms.glassOpacity.value = 0.3;
  });

  // Dim unconnected
  allMeshes.forEach(mesh => {
    if (!connected.all.has(mesh)) {
      mesh.material.opacity *= 0.2;
    }
  });

  // Show info panel
  showInfoPanel(node, connected);
}
```

#### Zoom-Based Level of Detail

```javascript
function updateLOD(cameraDistance) {
  if (cameraDistance > 200) {
    // Far: Show only meta-nodes and major structures
    showConsolidatedView();
  } else if (cameraDistance > 100) {
    // Medium: Show clusters with outline
    showClusterOutlines();
  } else {
    // Close: Show individual nodes and all surfaces
    showFullDetail();
  }
}
```

---

### 6. UI Components

#### Stats Bar (Top)

```html
<div class="stats-bar">
  <div class="stat">
    <span class="stat-icon">&#x25B2;</span>
    <span class="stat-label">Triangles</span>
    <span class="stat-value" id="triangle-count">0</span>
  </div>
  <div class="stat">
    <span class="stat-icon">&#x25C6;</span>
    <span class="stat-label">Tetrahedra</span>
    <span class="stat-value" id="tetra-count">0</span>
  </div>
  <div class="stat">
    <span class="stat-icon">&#x2B21;</span>
    <span class="stat-label">Polyhedra</span>
    <span class="stat-value" id="poly-count">0</span>
  </div>
  <div class="stat">
    <span class="stat-icon">&#x25CF;</span>
    <span class="stat-label">Nodes</span>
    <span class="stat-value" id="node-count">0/2000</span>
  </div>
</div>
```

#### Legend Panel (Bottom Left)

```html
<div class="legend-panel">
  <h3>Memory Topology</h3>
  <div class="legend-item">
    <div class="legend-color" style="background: rgba(147,197,253,0.3)"></div>
    <span>Derivation Surfaces</span>
  </div>
  <div class="legend-item">
    <div class="legend-color" style="background: rgba(251,191,36,0.3)"></div>
    <span>Causal Structures</span>
  </div>
  <div class="legend-item">
    <div class="legend-color" style="background: rgba(244,63,94,0.3)"></div>
    <span>Contradiction Zones</span>
  </div>
  <div class="legend-item">
    <div class="legend-color" style="background: rgba(168,85,247,0.3)"></div>
    <span>Emergent Clusters</span>
  </div>
</div>
```

#### Info Panel (Right Side)

```html
<div class="info-panel glass-panel">
  <h3 id="info-title">Selected Structure</h3>
  <div id="info-type" class="info-row">
    <span class="info-label">Type</span>
    <span class="info-value">Tetrahedron</span>
  </div>
  <div id="info-nodes" class="info-row">
    <span class="info-label">Nodes</span>
    <span class="info-value">4 memories</span>
  </div>
  <div id="info-relationships" class="info-row">
    <span class="info-label">Relationships</span>
    <span class="info-value">6 connections</span>
  </div>
  <div id="info-content" class="info-content">
    <!-- Node details appear here -->
  </div>
</div>
```

---

### 7. Performance Optimizations

#### Instanced Rendering for Nodes

```javascript
// Use InstancedMesh for nodes (same geometry, different positions/colors)
const nodeGeometry = new THREE.IcosahedronGeometry(0.5, 1);
const nodeMaterial = new THREE.MeshPhysicalMaterial({
  transparent: true,
  opacity: 0.8
});

const instancedNodes = new THREE.InstancedMesh(
  nodeGeometry,
  nodeMaterial,
  2000  // Max instances
);

// Set per-instance transforms
nodes.forEach((node, i) => {
  const matrix = new THREE.Matrix4();
  matrix.setPosition(node.position);
  matrix.scale(new THREE.Vector3(node.size, node.size, node.size));
  instancedNodes.setMatrixAt(i, matrix);
  instancedNodes.setColorAt(i, new THREE.Color(TOPOLOGY_COLORS.nodes[node.type]));
});

instancedNodes.count = nodes.length;
instancedNodes.instanceMatrix.needsUpdate = true;
instancedNodes.instanceColor.needsUpdate = true;
```

#### Frustum Culling for Surfaces

```javascript
// Only render surfaces visible in camera frustum
function updateVisibleSurfaces(camera, surfaces) {
  const frustum = new THREE.Frustum();
  frustum.setFromProjectionMatrix(
    new THREE.Matrix4().multiplyMatrices(
      camera.projectionMatrix,
      camera.matrixWorldInverse
    )
  );

  surfaces.forEach(surface => {
    surface.visible = frustum.intersectsObject(surface);
  });
}
```

#### Web Worker for Clique Detection

```javascript
// Heavy computation in worker thread
const cliqueWorker = new Worker('clique-worker.js');

cliqueWorker.postMessage({
  nodes: nodes.map(n => ({ id: n.id, ...n })),
  relationships: relationships
});

cliqueWorker.onmessage = (e) => {
  const { triangles, tetrahedra, higher } = e.data;
  renderCliques({ triangles, tetrahedra, higher }, nodePositions, scene);
};
```

---

## File Structure

```
byrd/
├── byrd-memory-topology.html      # Main visualization page
├── js/
│   ├── topology-engine.js         # Clique detection, geometry generation
│   ├── consolidation.js           # Node consolidation logic
│   ├── glass-materials.js         # Glass-morphism shaders
│   └── clique-worker.js           # Web worker for heavy computation
└── css/
    └── topology-styles.css        # Dark theme styles
```

---

## API Additions

### New Endpoint: `/api/graph/topology`

Returns pre-computed topology data for visualization:

```python
@app.get("/api/graph/topology")
async def get_graph_topology(limit: int = 2000, consolidation_level: int = 1):
    """
    Get graph with topology analysis.

    Returns:
    - nodes: Consolidated nodes (respecting limit)
    - relationships: Relationships between visible nodes
    - topology: Pre-computed cliques and chains
    - stats: Consolidation statistics
    """
    graph = await byrd_instance.memory.get_full_graph()

    # Consolidate if needed
    consolidated = consolidate_nodes(graph.nodes, graph.relationships, limit)

    # Compute topology
    topology = compute_topology(consolidated.nodes, consolidated.relationships)

    return {
        "nodes": consolidated.nodes,
        "relationships": consolidated.relationships,
        "topology": {
            "triangles": topology.triangles,
            "tetrahedra": topology.tetrahedra,
            "higher": topology.higher,
            "chains": topology.chains
        },
        "stats": {
            "original_count": len(graph.nodes),
            "consolidated_count": len(consolidated.nodes),
            "consolidation_level": consolidated.level,
            "triangle_count": len(topology.triangles),
            "tetrahedra_count": len(topology.tetrahedra)
        }
    }
```

---

## Implementation Phases

### Phase 1: Foundation (Day 1) - COMPLETED
- [x] Create `byrd-memory-topology.html` with dark theme
- [x] Set up Three.js scene with glass-morphism background
- [x] Implement basic node rendering with instancing
- [x] Add camera controls and basic UI

### Phase 2: Consolidation (Day 1-2) - COMPLETED
- [x] Implement temporal consolidation algorithm
- [x] Create meta-node geometry (convex hulls)
- [x] Add consolidation stats to UI
- [x] Test with large node counts

### Phase 3: Topology Engine (Day 2-3) - COMPLETED
- [x] Implement Bron-Kerbosch clique detection
- [x] Create triangle face geometry
- [x] Create tetrahedron geometry
- [x] Create higher polyhedra (convex hull)
- [x] Client-side computation with performance optimizations

### Phase 4: Visual Polish (Day 3-4) - COMPLETED
- [x] Implement glass-morphism shader with fresnel edge glow
- [x] Add bloom post-processing (UnrealBloomPass)
- [x] Create chain ribbon geometry with flow animation
- [x] Add pulse animations for new structures
- [x] Implement hover/selection effects
- [x] Particle dust background effect

### Phase 5: Interaction (Day 4) - COMPLETED
- [x] Meta-node expansion on double-click with golden-spiral sphere layout
- [x] Info panel with structure details (nodes, surfaces, clusters)
- [x] Zoom-based LOD (3 levels: close/medium/far)
- [x] Comprehensive keyboard shortcuts (R, Esc, E, F, I, C, G, 1/2/3, +/-, H, L, P)
- [x] Help panel with all shortcuts

### Phase 6: Integration (Day 5) - COMPLETED
- [x] Add `/api/graph/topology` endpoint with server-side topology computation
- [x] WebSocket integration for live updates with incremental node/relationship handling
- [x] Performance profiling panel (FPS, frame time, render time, draw calls, triangles)
- [x] Frustum culling for off-screen objects
- [x] Live update notifications and toggle (L key)
- [x] Documentation updated

---

## Usage Guide

### Accessing the Visualizer

1. Start the BYRD server: `python server.py`
2. Open in browser: `http://localhost:8000/byrd-memory-topology.html`

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `R` | Reset camera view |
| `Esc` | Deselect / Close panels |
| `E` | Expand/collapse selected cluster |
| `F` | Focus on selected object |
| `I` | Toggle info panel |
| `C` | Collapse all clusters |
| `G` | Toggle stats bar |
| `1/2/3` | Set detail level (close/medium/far) |
| `+/-` | Zoom in/out |
| `H` or `?` | Show help panel |
| `L` | Toggle live updates |
| `P` | Toggle performance panel |

### Mouse Controls

- **Left-drag**: Rotate view
- **Right-drag**: Pan view
- **Scroll**: Zoom in/out
- **Double-click**: Expand/collapse cluster hulls

### Features

#### Performance Panel (P key)
Shows real-time performance metrics:
- FPS (color-coded: green >50, yellow 30-50, red <30)
- Frame time (ms)
- Render time (ms)
- Draw calls
- Triangle count
- Visible/culled objects
- Memory usage

#### Live Updates (L key)
When enabled, new nodes and relationships animate into the scene with pulse effects and notifications appear at the bottom of the screen.

#### Level of Detail
The visualization automatically adjusts detail based on camera distance:
- **Close (<100 units)**: Full detail - all nodes, surfaces, edges
- **Medium (100-200 units)**: Major structures - tetrahedra and higher, important nodes, cluster hulls
- **Far (>200 units)**: Overview - cluster hulls only

---

## Success Metrics

1. **Performance**: Maintains 60fps with 2000 nodes
2. **Visual Appeal**: Dark glass-morphism aesthetic matching Supermemory
3. **Insight**: Users can see the "shape" of memory clusters
4. **Scalability**: Graceful consolidation for large graphs
5. **Interactivity**: Smooth expansion/collapse of meta-nodes

---

## Open Questions

1. Should relationship type affect surface color, or should we use a unified palette?
2. How should we handle overlapping surfaces (z-fighting)?
3. Should meta-nodes show a preview of their contents on hover?
4. What's the minimum clique size worth visualizing (3 or 4)?
5. Should we add an "explode" view that separates all clusters?
