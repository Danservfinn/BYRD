# Ralph Loop Testing Command

## Quick Start

To execute the comprehensive testing plan with Ralph Loop:

```bash
/ralph-loop "Execute comprehensive BYRD testing plan - fix backend tests, frontend build, API endpoints, integration testing, and document results" --max-iterations 5 --completion-promise "ALL_TESTS_PASSING"
```

---

## Detailed Prompt

Use this prompt for the Ralph Loop:

```
Execute comprehensive testing of BYRD full-stack implementation following this plan:

ITERATION 1 - Backend Unit Tests:
- Run: python -m pytest tests/test_*.py -v
- Fix any failing tests by updating test assertions or implementation
- Ensure all import errors are resolved
- Success: All tests pass

ITERATION 2 - Frontend Build:
- Run: cd frontend && npm run build
- Fix TypeScript compilation errors
- Fix type assertion issues in components
- Success: Clean build with no errors

ITERATION 3 - API Testing:
- Start server: python server.py (in background)
- Test all API endpoints with curl
- Verify JSON responses
- Success: All endpoints respond correctly

ITERATION 4 - Integration Testing:
- Start frontend dev server: npm run dev
- Open browser to http://localhost:5173
- Navigate all 8 routes
- Test WebSocket connection
- Success: All routes load, WebSocket connected

ITERATION 5 - Documentation:
- Create test report with results
- List any remaining issues
- Document test coverage
- Success: Complete test report generated

COMPLETION PROMISE: "ALL_TESTS_PASSING"
- All backend tests pass
- Frontend builds successfully
- All routes accessible
- WebSocket connects
- API endpoints work
- Test report created
```

---

## Alternative: Backend-Focused Loop

```bash
/ralph-loop "Fix all backend unit tests to pass - update test assertions, fix imports, ensure verification lattice, CAO, and entropic drift tests all pass 100%" --max-iterations 3 --completion-promise "BACKEND_TESTS_PASSING"
```

---

## Alternative: Frontend-Focused Loop

```bash
/ralph-loop "Fix frontend TypeScript compilation and build - resolve all type errors, fix component imports, ensure clean build with zero errors" --max-iterations 3 --completion-promise "FRONTEND_BUILDS"
```

---

## Monitoring Progress

Check Ralph Loop status:

```bash
# Show current iteration and status
cat .claude/ralph-loop.local.md

# Show git commits from loop
git log --oneline -10

# Show test results
python -m pytest tests/ -v --tb=short
```

---

## Stopping the Loop

If you need to stop manually:

```bash
# Edit the loop file to deactivate
vim .claude/ralph-loop.local.md
# Change "active: true" to "active: false"
```

---

*Use the appropriate loop based on your testing priority.*
