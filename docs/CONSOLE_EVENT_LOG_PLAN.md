# BYRD Event Console - Implementation Plan

## Overview

Transform the current event log panel into a high-performance, console-like interface for efficient event streaming and viewing. The console should handle thousands of events without performance degradation while providing powerful filtering, search, and analysis tools.

## Current State Analysis

### Existing Implementation
- **EventBus** (`event_bus.py`): 100+ event types, max history 1000 events
- **WebSocket streaming**: Events broadcast to all connected clients via `/ws/events`
- **Current UI**: Simple list showing 50 events max, basic type filtering
- **Rendering**: Debounced but rebuilds entire DOM each time
- **Features**: Type-based colors/icons, minimize/expand toggle

### Pain Points
1. **Performance**: Full DOM rebuild on each render
2. **Limited capacity**: Only shows 50 events
3. **Basic filtering**: Category-based only, no text search
4. **No auto-scroll control**: User can't pause stream to read
5. **No severity indication**: All events look equally important
6. **No persistence**: Filter settings reset on refresh
7. **No export**: Can't save logs for debugging

---

## Architecture Design

### Component Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    CONSOLE HEADER                            │
│  [Filter ▼] [Search...      ] [▶ Auto] [⤓ Export] [🗑 Clear]│
├─────────────────────────────────────────────────────────────┤
│                    FILTER BAR (collapsible)                  │
│  Types: [■ Dream] [■ Memory] [■ Goal] [■ System] [■ Error]  │
│  Severity: [■ Critical] [■ Warning] [■ Info] [■ Debug]      │
│  Time: [All] [Last 5m] [Last 1h] [Custom...]                │
├─────────────────────────────────────────────────────────────┤
│                    VIRTUALIZED EVENT LIST                    │
│                                                              │
│  19:45:32  ⚠ WARN   dream_cycle_start                       │
│            └─ Starting reflection cycle #42                  │
│                                                              │
│  19:45:31  ● INFO   belief_created                          │
│            └─ "I am capable of learning from mistakes"      │
│                                                              │
│  19:45:30  ● INFO   experience_created                      │
│            └─ User interaction recorded                      │
│                                                              │
│  ... (virtualized - only renders visible rows)              │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                    STATUS BAR                                │
│  Showing 847/1,234 events │ 23 errors │ Connected ●         │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
EventBus → WebSocket → Console State → Virtual Renderer → DOM (visible rows only)
                           │
                           ├─→ Filter Engine (client-side)
                           ├─→ Search Index (client-side)
                           └─→ Export Buffer
```

---

## Implementation Phases

### Phase 1: Virtual Scrolling Foundation
**Goal**: Handle 10,000+ events without performance issues

#### 1.1 Virtual List Implementation
```javascript
class VirtualEventList {
  constructor(container, rowHeight = 60) {
    this.container = container;
    this.rowHeight = rowHeight;
    this.events = [];           // All events
    this.filteredEvents = [];   // After filtering
    this.visibleRange = { start: 0, end: 0 };
    this.scrollTop = 0;
  }

  // Only render visible rows + buffer
  render() {
    const containerHeight = this.container.clientHeight;
    const totalHeight = this.filteredEvents.length * this.rowHeight;

    // Calculate visible range
    const start = Math.floor(this.scrollTop / this.rowHeight);
    const visibleCount = Math.ceil(containerHeight / this.rowHeight);
    const buffer = 5; // Extra rows above/below

    this.visibleRange = {
      start: Math.max(0, start - buffer),
      end: Math.min(this.filteredEvents.length, start + visibleCount + buffer)
    };

    // Create spacer divs for scroll height
    // Only render rows in visible range
  }
}
```

#### 1.2 Incremental Updates
- Append new events to end (don't rebuild entire list)
- Only re-render affected rows when filters change
- Use CSS transforms for smooth scrolling

#### 1.3 Row Pooling (Object Recycling)
```javascript
class RowPool {
  constructor(createRow, poolSize = 100) {
    this.pool = Array(poolSize).fill(null).map(() => createRow());
    this.inUse = new Set();
  }

  acquire() { /* Get row from pool */ }
  release(row) { /* Return to pool */ }
}
```

### Phase 2: Enhanced Filtering System
**Goal**: Multi-dimensional filtering with instant response

#### 2.1 Filter State Model
```javascript
const filterState = {
  // Type filters (checkboxes)
  types: {
    dream: true,
    memory: true,
    goal: true,
    seeker: true,
    coder: true,
    system: true,
    quantum: true,
    error: true
  },

  // Severity filter
  severities: {
    critical: true,  // Errors, failures
    warning: true,   // Alerts, near-limits
    info: true,      // Standard events
    debug: false     // Verbose/trace events
  },

  // Time filter
  timeRange: 'all', // 'all', '5m', '1h', '24h', 'custom'
  customTimeStart: null,
  customTimeEnd: null,

  // Text search
  searchQuery: '',
  searchFields: ['type', 'narration', 'data'] // Which fields to search
};
```

#### 2.2 Event Severity Classification
```javascript
const severityMap = {
  // Critical (red)
  critical: [
    'llm_error', 'reflection_error', 'coder_failed',
    'corrigibility_alert', 'kill_criterion_triggered',
    'modification_blocked', 'budget_exceeded'
  ],

  // Warning (yellow)
  warning: [
    'quantum_pool_low', 'resource_alert', 'voice_credits_low',
    'desire_stuck', 'bottleneck_detected', 'rollback_triggered'
  ],

  // Info (blue) - default
  info: [/* everything else */],

  // Debug (gray)
  debug: [
    'resource_snapshot', 'llm_usage_recorded', 'memories_accessed'
  ]
};
```

#### 2.3 Search Implementation
- Client-side full-text search with indexing
- Highlight matches in results
- Search across narration, type, and data fields

### Phase 3: Console UX Features
**Goal**: Professional developer console experience

#### 3.1 Auto-scroll Control
```javascript
class AutoScrollController {
  constructor(container) {
    this.container = container;
    this.autoScroll = true;
    this.userScrolledUp = false;

    container.addEventListener('scroll', () => {
      const isAtBottom = this.isNearBottom();
      this.autoScroll = isAtBottom;
      this.updateIndicator();
    });
  }

  isNearBottom() {
    const threshold = 100; // pixels
    return this.container.scrollHeight - this.container.scrollTop
           <= this.container.clientHeight + threshold;
  }

  scrollToBottom() {
    this.container.scrollTop = this.container.scrollHeight;
    this.autoScroll = true;
  }

  onNewEvent() {
    if (this.autoScroll) {
      this.scrollToBottom();
    }
  }
}
```

#### 3.2 Pause on Hover
- When mouse hovers over console, pause auto-scroll
- Show "Paused" indicator
- Resume on mouse leave (if was auto-scrolling before)

#### 3.3 Expandable Event Details
```javascript
function toggleEventDetail(eventIdx, rowElement) {
  const event = events[eventIdx];
  const detailEl = rowElement.querySelector('.event-detail');

  if (detailEl.classList.contains('expanded')) {
    detailEl.classList.remove('expanded');
    detailEl.style.maxHeight = '0';
  } else {
    // Render full JSON data
    detailEl.innerHTML = renderEventDetail(event);
    detailEl.classList.add('expanded');
    detailEl.style.maxHeight = detailEl.scrollHeight + 'px';
  }
}
```

#### 3.4 Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `Ctrl/Cmd + F` | Focus search |
| `Ctrl/Cmd + K` | Clear console |
| `Escape` | Clear search / close detail |
| `G` | Scroll to bottom (newest) |
| `Shift + G` | Scroll to top (oldest) |
| `J` / `K` | Navigate events (vim-style) |
| `Enter` | Expand/collapse selected event |
| `C` | Copy selected event JSON |

### Phase 4: Performance Optimizations
**Goal**: Smooth 60fps even with rapid event streams

#### 4.1 Event Batching
```javascript
class EventBatcher {
  constructor(onFlush, interval = 100) {
    this.batch = [];
    this.interval = interval;
    this.onFlush = onFlush;
    this.timer = null;
  }

  add(event) {
    this.batch.push(event);
    if (!this.timer) {
      this.timer = setTimeout(() => this.flush(), this.interval);
    }
  }

  flush() {
    if (this.batch.length > 0) {
      this.onFlush(this.batch);
      this.batch = [];
    }
    this.timer = null;
  }
}
```

#### 4.2 Render Scheduling
- Use `requestAnimationFrame` for all DOM updates
- Skip renders if tab is hidden (visibility API)
- Throttle filter recalculations

#### 4.3 Memory Management
```javascript
// Limit total events in memory
const MAX_EVENTS = 10000;

function addEvent(event) {
  events.push(event);
  if (events.length > MAX_EVENTS) {
    // Remove oldest 10%
    events.splice(0, MAX_EVENTS * 0.1);
    rebuildSearchIndex();
  }
}
```

### Phase 5: Additional Features
**Goal**: Professional debugging and analysis tools

#### 5.1 Export Functionality
```javascript
function exportEvents(format = 'json') {
  const exportData = filteredEvents.map(e => ({
    timestamp: e.timestamp,
    type: e.type,
    severity: getSeverity(e.type),
    narration: e.narration,
    data: e.data
  }));

  if (format === 'json') {
    downloadJSON(exportData, `byrd-events-${Date.now()}.json`);
  } else if (format === 'csv') {
    downloadCSV(exportData, `byrd-events-${Date.now()}.csv`);
  }
}
```

#### 5.2 Settings Persistence
```javascript
// Save to localStorage
function saveConsoleSettings() {
  localStorage.setItem('byrd-console-settings', JSON.stringify({
    filterState,
    autoScroll: autoScrollController.autoScroll,
    compactMode: isCompactMode,
    showTimestamps: showTimestamps
  }));
}

// Load on init
function loadConsoleSettings() {
  const saved = localStorage.getItem('byrd-console-settings');
  if (saved) {
    const settings = JSON.parse(saved);
    // Apply settings...
  }
}
```

#### 5.3 Statistics Panel
- Event rate (events/second)
- Error count
- Most frequent event types
- Connection status indicator

---

## UI/UX Design

### Color Scheme (Dark Console Theme Option)
```css
:root {
  /* Light theme (default) */
  --console-bg: #ffffff;
  --console-text: #1e293b;
  --console-border: #e2e8f0;
  --row-hover: rgba(0, 0, 0, 0.05);

  /* Severity colors */
  --severity-critical: #dc2626;
  --severity-warning: #f59e0b;
  --severity-info: #3b82f6;
  --severity-debug: #6b7280;
}

[data-theme="dark"] {
  --console-bg: #0f172a;
  --console-text: #e2e8f0;
  --console-border: #334155;
  --row-hover: rgba(255, 255, 255, 0.05);
}
```

### Row Layout
```
┌────────────────────────────────────────────────────────────┐
│ 19:45:32.123  ⚠  [WARN]  dream_cycle_start         [▼]   │
│              └─ Starting reflection cycle #42              │
│                 Duration: 2.3s | Beliefs: 3 | Desires: 1   │
└────────────────────────────────────────────────────────────┘
```

### Compact Mode
```
┌────────────────────────────────────────────────────────────┐
│ 19:45:32 ⚠ dream_cycle_start - Starting reflection #42    │
│ 19:45:31 ● belief_created - "I am capable of learning..." │
│ 19:45:30 ● experience_created - User interaction recorded  │
└────────────────────────────────────────────────────────────┘
```

---

## File Changes Required

### New Files
| File | Purpose |
|------|---------|
| `static/js/console/virtual-list.js` | Virtual scrolling implementation |
| `static/js/console/filter-engine.js` | Filtering and search logic |
| `static/js/console/event-console.js` | Main console controller |
| `static/css/console.css` | Console-specific styles |

### Modified Files
| File | Changes |
|------|---------|
| `byrd-3d-visualization.html` | Replace event log panel with console component |
| `server.py` | Add `/api/events/export` endpoint |
| `event_bus.py` | Add severity metadata to events |

---

## Implementation Order

1. **Week 1: Virtual Scrolling**
   - [ ] Implement VirtualEventList class
   - [ ] Add row pooling
   - [ ] Test with 10,000 events
   - [ ] Benchmark performance

2. **Week 2: Filtering System**
   - [ ] Implement filter state management
   - [ ] Add severity classification
   - [ ] Implement text search
   - [ ] Add filter UI components

3. **Week 3: Console UX**
   - [ ] Auto-scroll controller
   - [ ] Pause on hover
   - [ ] Expandable details
   - [ ] Keyboard shortcuts

4. **Week 4: Polish & Features**
   - [ ] Export functionality
   - [ ] Settings persistence
   - [ ] Statistics panel
   - [ ] Dark theme option
   - [ ] Mobile responsiveness

---

## Success Criteria

### Performance
- [ ] Handle 10,000 events without lag
- [ ] Maintain 60fps during rapid event streaming
- [ ] Initial render < 100ms
- [ ] Filter response < 50ms

### Usability
- [ ] Users can find specific events in < 5 seconds
- [ ] Auto-scroll doesn't interrupt reading
- [ ] All features accessible via keyboard
- [ ] Settings persist across sessions

### Reliability
- [ ] No memory leaks with extended use
- [ ] Graceful handling of WebSocket disconnection
- [ ] Works in Chrome, Firefox, Safari

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Virtual scroll complexity | High | Use proven library (e.g., virtual-scroller) as fallback |
| Mobile performance | Medium | Test on low-end devices, add compact mode |
| Search performance | Medium | Index incrementally, debounce input |
| Breaking existing features | High | Feature flag for gradual rollout |

---

## Open Questions

1. Should we add event aggregation (group repeated events)?
2. Do we need server-side filtering for very large event histories?
3. Should events persist across page refreshes (IndexedDB)?
4. Add ability to "pin" certain events for later review?
