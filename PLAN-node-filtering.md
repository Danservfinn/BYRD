# Node Filtering Implementation Plan

## Overview

Add interactive filtering to the BYRD 3D visualization, allowing users to show/hide specific node types and filter by other criteria. This improves both usability (focus on what matters) and performance (fewer nodes = smoother rendering).

## Current State Analysis

### Existing Infrastructure
- `NODE_COLORS` object defines all node types (belief, desire, goal, experience, reflection, etc.)
- Stats bar shows counts: `Beliefs: X | Desires: X | Goals: X | Reflect: X | Exp: X`
- `loadExistingGraph(excludeTypes)` already accepts an array of types to exclude
- `createNode3D()` has a limit check but no type filtering
- `nodes3D` array holds all rendered 3D meshes

### Node Types (from NODE_COLORS)
1. **Core types**: belief, desire, goal, experience, reflection
2. **Extended types**: capability, identity, prediction, task
3. **Special types**: operatingsystem, ostemplate, crystal
4. **Custom types**: Dynamically assigned from CUSTOM_TYPE_COLORS

---

## Implementation Plan

### Phase 1: Type Toggle Filters (Core Feature)

**Goal**: Make stat items clickable to toggle visibility of that node type.

#### 1.1 Add Filter State
```javascript
// Add near STATE section (~line 1488)
const nodeTypeFilters = {
  belief: true,
  desire: true,
  goal: true,
  experience: true,
  reflection: true,
  capability: true,
  insight: true,
  // ... other types default to true
};

function isTypeVisible(type) {
  const normalizedType = type?.toLowerCase() || 'experience';
  return nodeTypeFilters[normalizedType] !== false; // Default visible
}
```

#### 1.2 Update Stats Bar UI (lines 675-686)
Change from plain text spans to clickable toggle buttons:

```html
<!-- Before -->
<span class="stat-type text-amber-600" data-type="belief">Beliefs: <span id="belief-count">0</span></span>

<!-- After -->
<button class="stat-toggle active" data-type="belief" onclick="toggleTypeFilter('belief')">
  <span class="stat-dot" style="background: #d97706"></span>
  <span class="stat-label">Beliefs</span>
  <span class="stat-count" id="belief-count">0</span>
</button>
```

Add CSS for toggle states:
```css
.stat-toggle {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
}
.stat-toggle:hover {
  background: rgba(0,0,0,0.05);
}
.stat-toggle.active .stat-dot {
  opacity: 1;
}
.stat-toggle:not(.active) {
  opacity: 0.4;
}
.stat-toggle:not(.active) .stat-dot {
  background: #9ca3af !important;
}
.stat-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
```

#### 1.3 Implement Toggle Function
```javascript
function toggleTypeFilter(type) {
  nodeTypeFilters[type] = !nodeTypeFilters[type];

  // Update button visual state
  const btn = document.querySelector(`[data-type="${type}"]`);
  btn?.classList.toggle('active', nodeTypeFilters[type]);

  // Apply filter to existing nodes
  applyTypeFilters();
}

function applyTypeFilters() {
  nodes3D.forEach(node => {
    const type = node.userData.type?.toLowerCase();
    const visible = isTypeVisible(type);
    node.visible = visible;
  });

  // Also filter graph mode nodes
  if (graphState.nodeIdToMesh) {
    graphState.nodeIdToMesh.forEach((mesh, id) => {
      const type = mesh.userData.type?.toLowerCase();
      mesh.visible = isTypeVisible(type);
    });
  }

  // Update relationship line visibility
  updateRelationshipVisibility();
}

function updateRelationshipVisibility() {
  // Hide lines where either endpoint is hidden
  connections3D.forEach(conn => {
    const nodeA = nodes3D.find(n => n.userData.id === conn.userData.nodeA);
    const nodeB = nodes3D.find(n => n.userData.id === conn.userData.nodeB);
    conn.visible = nodeA?.visible && nodeB?.visible;
  });

  graphState.relationshipLines.forEach(line => {
    const sourceVisible = isTypeVisible(/* get source type */);
    const targetVisible = isTypeVisible(/* get target type */);
    line.visible = sourceVisible && targetVisible;
  });
}
```

#### 1.4 Update Node Creation to Respect Filters
Modify `createNode3D()` to check filter state:
```javascript
function createNode3D(type, content, id, importance = 0.5) {
  // Existing limit check...

  // Add filter check
  if (!isTypeVisible(type)) {
    console.log(`Skipping ${type} node (filtered out)`);
    return null;
  }

  // ... rest of function
}
```

#### 1.5 Add Quick Filter Buttons
Add "Show All" and "Hide All" buttons:
```html
<div class="filter-actions">
  <button onclick="showAllTypes()" class="text-xs">Show All</button>
  <button onclick="hideAllTypes()" class="text-xs">Hide All</button>
</div>
```

```javascript
function showAllTypes() {
  Object.keys(nodeTypeFilters).forEach(type => nodeTypeFilters[type] = true);
  document.querySelectorAll('.stat-toggle').forEach(btn => btn.classList.add('active'));
  applyTypeFilters();
}

function hideAllTypes() {
  Object.keys(nodeTypeFilters).forEach(type => nodeTypeFilters[type] = false);
  document.querySelectorAll('.stat-toggle').forEach(btn => btn.classList.remove('active'));
  applyTypeFilters();
}
```

---

### Phase 2: Filter Panel with Advanced Options

**Goal**: Add a collapsible filter panel with additional filtering criteria.

#### 2.1 Add Filter Panel UI
Insert after stats bar or as a slide-out panel:

```html
<div id="filter-panel" class="filter-panel hidden">
  <div class="filter-header">
    <span>Filters</span>
    <button onclick="toggleFilterPanel()">×</button>
  </div>

  <!-- Type Filters (checkboxes) -->
  <div class="filter-section">
    <div class="filter-section-title">Node Types</div>
    <div id="type-checkboxes" class="filter-checkboxes">
      <!-- Generated dynamically -->
    </div>
  </div>

  <!-- Recency Filter -->
  <div class="filter-section">
    <div class="filter-section-title">Time Range</div>
    <select id="recency-filter" onchange="applyRecencyFilter()">
      <option value="all">All Time</option>
      <option value="1h">Last Hour</option>
      <option value="24h">Last 24 Hours</option>
      <option value="7d">Last 7 Days</option>
      <option value="30d">Last 30 Days</option>
    </select>
  </div>

  <!-- Confidence/Importance Threshold -->
  <div class="filter-section">
    <div class="filter-section-title">Min Importance</div>
    <input type="range" id="importance-filter" min="0" max="100" value="0"
           oninput="applyImportanceFilter(this.value)">
    <span id="importance-value">0%</span>
  </div>

  <!-- Connection Count Filter -->
  <div class="filter-section">
    <div class="filter-section-title">Min Connections</div>
    <input type="range" id="connection-filter" min="0" max="10" value="0"
           oninput="applyConnectionFilter(this.value)">
    <span id="connection-value">0</span>
  </div>
</div>
```

#### 2.2 Add Filter Button to Controls
```html
<button id="btn-filter" onclick="toggleFilterPanel()"
        class="px-3 py-2 rounded-lg text-sm font-medium bg-indigo-100 border border-indigo-300 text-indigo-700">
  🔍 Filter
</button>
```

#### 2.3 Implement Advanced Filters
```javascript
const advancedFilters = {
  recency: 'all',        // 'all', '1h', '24h', '7d', '30d'
  minImportance: 0,      // 0-1
  minConnections: 0      // 0+
};

function applyRecencyFilter() {
  advancedFilters.recency = document.getElementById('recency-filter').value;
  applyAllFilters();
}

function applyImportanceFilter(value) {
  advancedFilters.minImportance = value / 100;
  document.getElementById('importance-value').textContent = value + '%';
  applyAllFilters();
}

function applyConnectionFilter(value) {
  advancedFilters.minConnections = parseInt(value);
  document.getElementById('connection-value').textContent = value;
  applyAllFilters();
}

function applyAllFilters() {
  const now = Date.now();
  const recencyMs = {
    'all': Infinity,
    '1h': 60 * 60 * 1000,
    '24h': 24 * 60 * 60 * 1000,
    '7d': 7 * 24 * 60 * 60 * 1000,
    '30d': 30 * 24 * 60 * 60 * 1000
  };

  nodes3D.forEach(node => {
    const data = node.userData;
    const type = data.type?.toLowerCase();

    // Type filter
    if (!isTypeVisible(type)) {
      node.visible = false;
      return;
    }

    // Recency filter
    if (advancedFilters.recency !== 'all') {
      const nodeTime = new Date(data.timestamp || data.created_at).getTime();
      if (now - nodeTime > recencyMs[advancedFilters.recency]) {
        node.visible = false;
        return;
      }
    }

    // Importance filter
    const importance = data.confidence || data.intensity || data.importance || 0.5;
    if (importance < advancedFilters.minImportance) {
      node.visible = false;
      return;
    }

    // Connection filter
    const connCount = connectionCounts.get(data.id) || 0;
    if (connCount < advancedFilters.minConnections) {
      node.visible = false;
      return;
    }

    node.visible = true;
  });

  updateRelationshipVisibility();
  updateFilteredCount();
}

function updateFilteredCount() {
  const visible = nodes3D.filter(n => n.visible).length;
  const total = nodes3D.length;
  // Update UI to show "Showing X of Y nodes"
}
```

---

### Phase 3: Search Filter (Optional Enhancement)

**Goal**: Add text search to filter nodes by content.

#### 3.1 Add Search Input
```html
<div class="search-container">
  <input type="text" id="node-search" placeholder="Search nodes..."
         oninput="debounce(applySearchFilter, 300)()">
  <button onclick="clearSearch()">×</button>
</div>
```

#### 3.2 Implement Search
```javascript
let searchQuery = '';

function applySearchFilter() {
  searchQuery = document.getElementById('node-search').value.toLowerCase().trim();
  applyAllFilters(); // Search integrates with other filters
}

// In applyAllFilters(), add:
if (searchQuery) {
  const content = (data.content || data.description || '').toLowerCase();
  if (!content.includes(searchQuery)) {
    node.visible = false;
    return;
  }
}
```

---

## File Changes Summary

### byrd-3d-visualization.html

1. **Add filter state variables** (~line 1490)
2. **Update stats bar HTML** (lines 675-686) - make clickable toggles
3. **Add filter panel HTML** (after stats bar)
4. **Add CSS for filter UI** (in style section)
5. **Add filter functions** (new section after STATE)
6. **Modify `createNode3D()`** - respect filter state
7. **Modify `loadExistingGraph()`** - apply filters after loading
8. **Add event listeners** for filter controls

---

## Testing Checklist

- [ ] Clicking type toggles hides/shows nodes of that type
- [ ] Hidden node's relationship lines are also hidden
- [ ] "Show All" / "Hide All" work correctly
- [ ] Filters persist when new nodes arrive via WebSocket
- [ ] Filter state survives mode switches (event → graph → event)
- [ ] Recency filter correctly filters by timestamp
- [ ] Importance threshold works for beliefs (confidence) and desires (intensity)
- [ ] Connection filter correctly uses connection counts
- [ ] Search highlights/filters matching nodes
- [ ] Performance remains acceptable with frequent filter changes
- [ ] UI feedback shows how many nodes are visible vs total

---

## Implementation Order

1. **Phase 1.1-1.3**: Type toggle state and functions (30 min)
2. **Phase 1.2**: Update stats bar UI (20 min)
3. **Phase 1.4**: Update node creation (10 min)
4. **Phase 1.5**: Quick filter buttons (10 min)
5. **Test Phase 1** thoroughly
6. **Phase 2**: Advanced filter panel (45 min)
7. **Phase 3**: Search (optional, 20 min)

Total estimated: ~2-3 hours

---

## Alternative Approaches Considered

1. **Server-side filtering**: Modify `/api/graph` to accept filter params
   - Pro: Less data transferred
   - Con: Slower feedback, more API changes needed

2. **Virtual scrolling / LOD**: Only render nearby nodes
   - Pro: Better for huge graphs
   - Con: Complex, loses overview

3. **Separate filter page**: Dedicated filtering UI
   - Pro: More space for controls
   - Con: Context switching, loses immersion

**Decision**: Client-side filtering is best for immediate feedback and keeps all data available for quick switching between filter states.
