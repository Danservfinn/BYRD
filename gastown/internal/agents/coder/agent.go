// Package coder implements the Coder agent for TDD practice in the code domain
package coder

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"sync"
	"time"

	"github.com/byrd-ai/gastown/internal/agents/infrastructure"
	"github.com/byrd-ai/gastown/internal/neo4j"
	"github.com/byrd-ai/gastown/pkg/types"
)

// Agent implements the Coder agent for TDD practice
type Agent struct {
	id          string
	pool        *neo4j.Pool
	infra       *infrastructure.Infrastructure
	queries     *neo4j.Queries
	running     bool
	cyclesRun   int
	lastCycle   time.Time
	phase       string
	workDir     string
	maxAttempts int
	stopChan    chan struct{}
	mu          sync.RWMutex
}

// New creates a new Coder agent
func New(ctx context.Context, pool *neo4j.Pool, infra *infrastructure.Infrastructure, index int) (*Agent, error) {
	workDir := filepath.Join(os.TempDir(), fmt.Sprintf("gastown_coder_%d", index))
	if err := os.MkdirAll(workDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create work directory: %w", err)
	}

	return &Agent{
		id:          fmt.Sprintf("coder-%d", index),
		pool:        pool,
		infra:       infra,
		queries:     infra.Queries(),
		workDir:     workDir,
		maxAttempts: 5,
		stopChan:    make(chan struct{}),
	}, nil
}

// Run starts the agent's main loop
func (a *Agent) Run(ctx context.Context, interval time.Duration) {
	a.mu.Lock()
	a.running = true
	a.mu.Unlock()

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	log.Printf("[%s] Starting coder loop (interval: %v)", a.id, interval)

	for {
		select {
		case <-ctx.Done():
			log.Printf("[%s] Context cancelled, stopping", a.id)
			return
		case <-a.stopChan:
			log.Printf("[%s] Stop signal received", a.id)
			return
		case <-ticker.C:
			if err := a.runCycle(ctx); err != nil {
				log.Printf("[%s] Cycle error: %v", a.id, err)
			}
		}
	}
}

// Stop gracefully stops the agent
func (a *Agent) Stop() {
	a.mu.Lock()
	defer a.mu.Unlock()
	if a.running {
		close(a.stopChan)
		a.running = false
	}
}

// ID returns the agent's identifier
func (a *Agent) ID() string {
	return a.id
}

// Status returns the agent's current status
func (a *Agent) Status() types.AgentStatus {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return types.AgentStatus{
		ID:           a.id,
		Type:         "coder",
		Running:      a.running,
		CyclesRun:    a.cyclesRun,
		LastCycleAt:  a.lastCycle,
		CurrentPhase: a.phase,
	}
}

// runCycle executes a single TDD practice cycle
func (a *Agent) runCycle(ctx context.Context) error {
	startTime := time.Now()

	// Get pending code desires
	a.mu.Lock()
	a.phase = "FETCH"
	a.mu.Unlock()

	desires, err := a.queries.GetPendingDesires(ctx, 1)
	if err != nil {
		return fmt.Errorf("failed to get desires: %w", err)
	}

	if len(desires) == 0 {
		log.Printf("[%s] No pending code desires", a.id)
		return nil
	}

	desire := desires[0]
	if desire.Domain != types.DomainCode {
		// Skip non-code desires
		return nil
	}

	log.Printf("[%s] Processing desire: %s", a.id, desire.Description)

	// Phase: Generate problem and tests
	a.mu.Lock()
	a.phase = "GENERATE"
	a.mu.Unlock()

	problem, tests, err := a.generateProblem(ctx, desire)
	if err != nil {
		return fmt.Errorf("failed to generate problem: %w", err)
	}

	// Phase: Practice TDD
	a.mu.Lock()
	a.phase = "PRACTICE"
	a.mu.Unlock()

	result, err := a.practice(ctx, problem, tests)
	if err != nil {
		log.Printf("[%s] Practice failed: %v", a.id, err)
		result = &types.PracticeResult{Success: false, Error: err.Error()}
	}

	// Phase: Record trajectory
	a.mu.Lock()
	a.phase = "RECORD"
	a.mu.Unlock()

	trajectory := types.Trajectory{
		ID:          generateID("traj"),
		DesireID:    desire.ID,
		Domain:      types.DomainCode,
		Problem:     problem.Description,
		Solution:    result.Solution,
		Approach:    problem.Approach,
		Success:     result.Success,
		IsBootstrap: false,
		CreatedAt:   time.Now(),
	}

	if err := a.queries.StoreTrajectory(ctx, trajectory); err != nil {
		log.Printf("[%s] Failed to store trajectory: %v", a.id, err)
	}

	a.mu.Lock()
	a.cyclesRun++
	a.lastCycle = time.Now()
	a.phase = ""
	a.mu.Unlock()

	duration := time.Since(startTime).Seconds()
	status := "FAILED"
	if result.Success {
		status = "SUCCESS"
	}
	log.Printf("[%s] Cycle completed: %s in %.2fs", a.id, status, duration)

	return nil
}

// Problem represents a coding problem with tests
type Problem struct {
	Description string
	TestCode    string
	Approach    string
}

// generateProblem creates a coding problem and tests from a desire
func (a *Agent) generateProblem(ctx context.Context, desire types.Desire) (*Problem, string, error) {
	// Get relevant heuristics for the code domain
	heuristics, err := a.queries.GetHeuristicsByDomain(ctx, types.DomainCode)
	if err != nil {
		log.Printf("[%s] Failed to get heuristics: %v", a.id, err)
	}

	heuristicContext := ""
	for _, h := range heuristics {
		heuristicContext += fmt.Sprintf("- %s\n", h.Principle)
	}

	prompt := fmt.Sprintf(`Generate a Python coding problem and test suite for this desire:
"%s"

%s

Output JSON with:
{
  "description": "Problem statement",
  "approach": "Recommended approach/algorithm",
  "test_code": "Python pytest test code with at least 3 test cases",
  "starter_code": "Function signature with docstring"
}

The tests should be in pytest format and import the solution from 'solution.py'.
Only output the JSON, no other text.`, desire.Description,
		func() string {
			if heuristicContext != "" {
				return "Apply these learned heuristics:\n" + heuristicContext
			}
			return ""
		}())

	response, err := a.infra.LLM().Generate(ctx, prompt, types.GenerateOptions{
		Temperature: 0.3,
		MaxTokens:   2000,
	})
	if err != nil {
		return nil, "", err
	}

	var problemDef struct {
		Description string `json:"description"`
		Approach    string `json:"approach"`
		TestCode    string `json:"test_code"`
		StarterCode string `json:"starter_code"`
	}

	response = extractJSON(response)
	if err := json.Unmarshal([]byte(response), &problemDef); err != nil {
		return nil, "", fmt.Errorf("failed to parse problem: %w", err)
	}

	return &Problem{
		Description: problemDef.Description,
		TestCode:    problemDef.TestCode,
		Approach:    problemDef.Approach,
	}, problemDef.StarterCode, nil
}

// practice runs the TDD practice loop
func (a *Agent) practice(ctx context.Context, problem *Problem, starterCode string) (*types.PracticeResult, error) {
	// Write test file
	testPath := filepath.Join(a.workDir, "test_solution.py")
	if err := os.WriteFile(testPath, []byte(problem.TestCode), 0644); err != nil {
		return nil, fmt.Errorf("failed to write tests: %w", err)
	}

	// Write initial solution
	solutionPath := filepath.Join(a.workDir, "solution.py")
	currentSolution := starterCode

	for attempt := 1; attempt <= a.maxAttempts; attempt++ {
		log.Printf("[%s] Attempt %d/%d", a.id, attempt, a.maxAttempts)

		// Write current solution
		if err := os.WriteFile(solutionPath, []byte(currentSolution), 0644); err != nil {
			return nil, fmt.Errorf("failed to write solution: %w", err)
		}

		// Run tests
		passed, output := a.runTests(ctx)
		if passed {
			return &types.PracticeResult{
				Success:  true,
				Solution: currentSolution,
				Attempts: attempt,
			}, nil
		}

		// Generate improved solution
		improved, err := a.improveSolution(ctx, problem, currentSolution, output)
		if err != nil {
			return nil, fmt.Errorf("failed to improve solution: %w", err)
		}
		currentSolution = improved
	}

	return &types.PracticeResult{
		Success:  false,
		Solution: currentSolution,
		Attempts: a.maxAttempts,
		Error:    "Max attempts exceeded",
	}, nil
}

// runTests executes pytest and returns success/failure with output
func (a *Agent) runTests(ctx context.Context) (bool, string) {
	cmd := exec.CommandContext(ctx, "python", "-m", "pytest", "-v", "test_solution.py")
	cmd.Dir = a.workDir

	output, err := cmd.CombinedOutput()
	if err != nil {
		return false, string(output)
	}
	return true, string(output)
}

// improveSolution uses LLM to improve a failing solution
func (a *Agent) improveSolution(ctx context.Context, problem *Problem, current, testOutput string) (string, error) {
	prompt := fmt.Sprintf(`Fix this Python code to pass the tests.

Problem: %s

Current code:
%s

Test output:
%s

Output ONLY the corrected Python code, no explanations or markdown.`, problem.Description, current, testOutput)

	response, err := a.infra.LLM().Generate(ctx, prompt, types.GenerateOptions{
		Temperature: 0.2,
		MaxTokens:   1500,
	})
	if err != nil {
		return "", err
	}

	// Clean up response
	response = extractCode(response)
	return response, nil
}

// extractJSON extracts JSON from markdown code blocks
func extractJSON(s string) string {
	if len(s) > 7 && s[:7] == "```json" {
		s = s[7:]
	} else if len(s) > 3 && s[:3] == "```" {
		s = s[3:]
	}
	if len(s) > 3 && s[len(s)-3:] == "```" {
		s = s[:len(s)-3]
	}
	return s
}

// extractCode extracts Python code from markdown
func extractCode(s string) string {
	if len(s) > 9 && s[:9] == "```python" {
		s = s[9:]
	} else if len(s) > 3 && s[:3] == "```" {
		s = s[3:]
	}
	if len(s) > 3 && s[len(s)-3:] == "```" {
		s = s[:len(s)-3]
	}
	return s
}

// generateID generates a unique ID with prefix
func generateID(prefix string) string {
	return fmt.Sprintf("%s_%d", prefix, time.Now().UnixNano())
}

// Ensure Agent implements the Agent interface
var _ types.Agent = (*Agent)(nil)
