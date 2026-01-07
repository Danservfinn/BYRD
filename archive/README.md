# BYRD Archive

This directory contains deprecated code preserved for historical reference.

## Contents

### `/v1/` - Original Implementation
The first version of BYRD before the ASI architecture redesign. Contains:
- Original dreamer implementation
- Early memory systems
- Initial RSI experiments

### `/experimental/` - Experimental Features
Features that were prototyped but not integrated:
- Various experimental approaches
- Proof-of-concept implementations

### `/frontend-archive/` (sibling directory)
Legacy HTML visualizations replaced by React frontend:
- `byrd-architecture.html` - Static architecture diagram
- `byrd-3d-visualization.html` - Three.js 3D mind space
- `byrd-memory-topology.html` - Neo4j graph visualization
- `byrd-dream-visualization.html` - Dream state visualization
- `byrd-cat-visualization.html` - Category visualization
- WebGL tests and experiments

## Why Archived

These files were archived during the January 2026 implementation phase to:
1. Eliminate conflicts with the new React frontend
2. Preserve historical context for debugging
3. Clean the workspace for focused development

## Do Not

- Move these files back to active directories
- Reference these files in new code
- Delete without team consensus

## See Also

- `/docs/IMPLEMENTATION_PLAN.md` - Current implementation plan
- `/frontend/` - Active React frontend
- `/ARCHITECTURE.md` - Current system architecture

---

*Archived: January 7, 2026*
