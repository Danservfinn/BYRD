# Ralph Loop Testing Plan - Backend & Frontend

**Prompt**: Execute comprehensive testing of BYRD full-stack implementation to ensure all components work correctly together.

---

## Testing Objectives

Validate that the complete BYRD implementation meets all success criteria from IMPLEMENTATION_PLAN.md through systematic testing of:
- Backend RSI architecture components
- Frontend React components
- API endpoints and WebSocket communication
- Integration between frontend and backend
- 3D visualization and real-time updates

---

## Phase 1: Backend Testing

### 1.1 Unit Tests

**Target**: All backend tests pass

**Files to Test**:
- `tests/test_verification_lattice.py`
- `tests/test_cao.py`
- `tests/test_entropic_drift.py`

**Commands**:
```bash
cd /Users/kurultai/BYRD
python -m pytest tests/test_verification_lattice.py -v
python -m pytest tests/test_cao.py -v
python -m pytest tests/test_entropic_drift.py -v
```

**Success Criteria**:
- All tests pass without errors
- Test coverage > 80% for novel RSI components
- No import errors or missing dependencies

**If Tests Fail**:
1. Read test error message
2. Check implementation file for missing classes/methods
3. Update test to match actual implementation (or fix implementation)
4. Re-run tests
5. Document fixes in testing notes

---

### 1.2 Backend Module Import Tests

**Target**: All backend modules can be imported

**Test Script**:
```python
# Test all RSI modules can be imported
from rsi.verification.lattice import VerificationLattice
from rsi.verification.entropic_drift import EntropicDriftMonitor
from rsi.orchestration.cao import ComplexityAwareOrchestrator
from rsi.orchestration.strategy_competition import StrategyPool
from rsi.engine import RSIEngine
```

**Command**:
```bash
python -c "from rsi.verification.lattice import VerificationLattice; print('✓ VerificationLattice imports')"
python -c "from rsi.orchestration.cao import ComplexityAwareOrchestrator; print('✓ CAO imports')"
```

**Success Criteria**:
- All modules import without errors
- No circular import dependencies

---

## Phase 2: Frontend Build Testing

### 2.1 TypeScript Compilation

**Target**: Frontend compiles without TypeScript errors

**Commands**:
```bash
cd /Users/kurultai/BYRD/frontend
npm run build
```

**Success Criteria**:
- Build completes successfully
- No TypeScript errors
- Dist folder created with bundled assets
- Build time < 60 seconds

**If Build Fails**:
1. Check error messages for type mismatches
2. Fix type assertions in components
3. Ensure all imports resolve correctly
4. Re-run build

---

### 2.2 Development Server Test

**Target**: Dev server starts without errors

**Commands**:
```bash
cd /Users/kurultai/BYRD/frontend
npm run dev
```

**Success Criteria**:
- Server starts on http://localhost:5173
- No build errors in console
- Hot Module Replacement (HMR) works
- All 8 routes accessible

**Manual Verification**:
1. Open browser to http://localhost:5173
2. Navigate through all 8 routes:
   - http://localhost:5173/ (Dashboard)
   - http://localhost:5173/rsi
   - http://localhost:5173/economic
   - http://localhost:5173/plasticity
   - http://localhost:5173/scaling
   - http://localhost:5173/verification
   - http://localhost:5173/controls
   - http://localhost:5173/visualization
3. Verify each page renders without console errors
4. Check browser console for any React warnings

---

## Phase 3: API Endpoint Testing

### 3.1 Server Startup Test

**Target**: BYRD server starts successfully

**Commands**:
```bash
cd /Users/kurultai/BYRD
python server.py
```

**Success Criteria**:
- Server starts on http://localhost:8000
- No startup errors
- WebSocket endpoint initialized
- All API routes registered

**API Endpoints to Verify**:
```bash
# Health check
curl http://localhost:8000/api/version

# RSI endpoints
curl http://localhost:8000/api/rsi/status
curl http://localhost:8000/api/rsi/metrics
curl http://localhost:8000/api/rsi/phases

# Plasticity endpoints
curl http://localhost:8000/api/plasticity/modules

# Scaling endpoints
curl http://localhost:8000/api/scaling/metrics

# Governance endpoints
curl http://localhost:8000/api/governance/direction

# Consciousness endpoints
curl http://localhost:8000/api/consciousness/frames
```

**Success Criteria**:
- All endpoints return JSON responses
- No 404 or 500 errors
- Response structure matches API types

---

## Phase 4: Integration Testing

### 4.1 WebSocket Connection Test

**Target**: Frontend connects to WebSocket successfully

**Test Steps**:
1. Start server: `python server.py`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser to http://localhost:5173
4. Check for WebSocket connection indicator in header
5. Monitor browser console for WebSocket messages

**Success Criteria**:
- WebSocket connection established
- Connection indicator shows "Connected"
- No WebSocket errors in console
- Real-time events display in RecentActivity component

---

### 4.2 Component Integration Test

**Target**: All components load data from API

**Test Components**:
- DashboardPage: Loads system status
- RSIPage: Displays RSI cycle status
- VerificationPage: Shows verification lattice
- ConsciousnessStream: Displays consciousness frames

**Success Criteria**:
- Each component makes API calls
- Loading states display correctly
- Data renders when available
- Error handling works for API failures

---

## Phase 5: End-to-End Testing

### 5.1 RSI Cycle Execution Test

**Target**: Can trigger and monitor RSI cycle from UI

**Test Steps**:
1. Navigate to http://localhost:5173/controls
2. Click "Start RSI" button
3. Navigate to http://localhost:5173/rsi
4. Observe PhaseTracker updating
5. Verify RalphLoopStatus shows active cycle
6. Wait for cycle completion or click "Stop"

**Success Criteria**:
- RSI cycle starts successfully
- Phase tracker shows progress through 8 phases
- Cycle completion event appears in RecentActivity
- Stop button halts the cycle

---

### 5.2 3D Visualization Test

**Target**: Memory topology visualization renders

**Test Steps**:
1. Navigate to http://localhost:5173/visualization
2. Check if canvas renders
3. Look for node rendering (colored spheres)
4. Verify nodes are positioned in 3D space
5. Test mouse interaction (rotate, zoom)

**Success Criteria**:
- Canvas element displays
- Nodes render with correct colors by type
- Mouse rotation works
- Zoom functionality works
- No WebGL errors in console

---

## Phase 6: Regression Testing

### 6.1 Smoke Tests

**Target**: Critical paths work after changes

**Test Cases**:
1. Server starts → ✅
2. Frontend builds → ✅
3. Dev server runs → ✅
4. All 8 routes load → ✅
5. WebSocket connects → ✅
6. API endpoints respond → ✅

**Run After**: Any code changes

---

## Iteration Plan

### Iteration 1: Fix Failing Tests
- Run all test suites
- Identify failing tests
- Fix test imports (already done)
- Fix test assertions to match implementation
- Re-run until all pass

### Iteration 2: Fix Build Errors
- Run frontend build
- Fix TypeScript errors
- Fix import issues
- Re-build until success

### Iteration 3: Integration Testing
- Start server
- Start frontend
- Test all routes
- Test WebSocket
- Test API calls

### Iteration 4: E2E Testing
- Test RSI cycle from UI
- Test 3D visualization
- Test governance controls
- Test desire injection

### Iteration 5: Documentation
- Document test results
- Create test coverage report
- List any remaining issues
- Provide recommendations

---

## Completion Criteria

**The testing loop is COMPLETE when**:

1. ✅ All backend unit tests pass (test_verification_lattice, test_cao, test_entropic_drift)
2. ✅ Frontend builds without TypeScript errors
3. ✅ All 8 frontend routes load successfully in browser
4. ✅ WebSocket connection established and working
5. ✅ API endpoints return valid JSON responses
6. ✅ RSI cycle can be triggered from UI
7. ✅ 3D visualization renders (may need mock data if no Neo4j)
8. ✅ Test results documented
9. ✅ No critical bugs blocking deployment

---

## Test Report Template

After each iteration, create a test report:

```markdown
# Test Report - Iteration {N}

## Date
{timestamp}

## Tests Run
- Backend Unit Tests: {pass}/{fail}/{total}
- Frontend Build: {status}
- API Endpoints: {pass}/{fail}/{total}
- Integration Tests: {status}

## Issues Found
1. {issue description}
   - Severity: {critical|high|medium|low}
   - Status: {fixed|pending|deferred}

## Fixes Applied
1. {description of fix}

## Next Steps
- {what to do in next iteration}
```

---

## Ralph Loop Configuration

**Use this command to start the testing loop**:

```bash
/ralph-loop --max-iterations 5 --completion-promise "ALL_TESTS_PASSING"
```

**Prompt to feed**:
```
Execute comprehensive testing plan for BYRD full-stack implementation.

Phase 1: Fix backend unit tests
Phase 2: Fix frontend build
Phase 3: Test API endpoints
Phase 4: Test integration (WebSocket, components)
Phase 5: Document results

Run tests, fix issues, re-test until all success criteria met.
```

---

## Success Metrics

- **Backend Test Pass Rate**: 100%
- **Frontend Build Success**: Yes
- **Routes Accessible**: 8/8
- **WebSocket Connected**: Yes
- **API Endpoints Working**: 100%
- **Critical Bugs**: 0

---

*Created: January 7, 2026*
*Ralph Loop Testing Plan v1.0*
