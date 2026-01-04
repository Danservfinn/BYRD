// Package crystallizer implements the Crystallizer agent for heuristic extraction
package crystallizer

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/byrd-ai/gastown/internal/agents/infrastructure"
	"github.com/byrd-ai/gastown/internal/neo4j"
	"github.com/byrd-ai/gastown/pkg/types"
)

// Config holds crystallizer configuration
type Config struct {
	BootstrapThreshold int     // Min trajectories before first crystallization
	MatureThreshold    int     // Min trajectories after first crystallization
	MinSuccessRate     float64 // Minimum success rate for pattern
	MaxHeuristics      int     // Maximum heuristics per domain
}

// DefaultConfig returns default configuration
func DefaultConfig() Config {
	return Config{
		BootstrapThreshold: 10,
		MatureThreshold:    20,
		MinSuccessRate:     0.8,
		MaxHeuristics:      50,
	}
}

// Agent implements the Crystallizer agent
type Agent struct {
	id              string
	pool            *neo4j.Pool
	infra           *infrastructure.Infrastructure
	queries         *neo4j.Queries
	config          Config
	running         bool
	cyclesRun       int
	lastCycle       time.Time
	phase           string
	bootstrapPhase  map[types.Domain]bool // Track if domain is still in bootstrap
	stopChan        chan struct{}
	mu              sync.RWMutex
}

// New creates a new Crystallizer agent
func New(ctx context.Context, pool *neo4j.Pool, infra *infrastructure.Infrastructure, index int) (*Agent, error) {
	return &Agent{
		id:             fmt.Sprintf("crystallizer-%d", index),
		pool:           pool,
		infra:          infra,
		queries:        infra.Queries(),
		config:         DefaultConfig(),
		bootstrapPhase: make(map[types.Domain]bool),
		stopChan:       make(chan struct{}),
	}, nil
}

// Run starts the agent's main loop
func (a *Agent) Run(ctx context.Context, interval time.Duration) {
	a.mu.Lock()
	a.running = true
	// Start all domains in bootstrap phase
	for _, domain := range []types.Domain{types.DomainCode, types.DomainMath, types.DomainLogic} {
		a.bootstrapPhase[domain] = true
	}
	a.mu.Unlock()

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	log.Printf("[%s] Starting crystallizer loop (interval: %v)", a.id, interval)

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
		Type:         "crystallizer",
		Running:      a.running,
		CyclesRun:    a.cyclesRun,
		LastCycleAt:  a.lastCycle,
		CurrentPhase: a.phase,
	}
}

// runCycle attempts crystallization for each domain
func (a *Agent) runCycle(ctx context.Context) error {
	startTime := time.Now()
	crystalized := 0

	for _, domain := range []types.Domain{types.DomainCode, types.DomainMath, types.DomainLogic} {
		a.mu.Lock()
		a.phase = fmt.Sprintf("CHECK_%s", domain)
		a.mu.Unlock()

		// Check if enough trajectories exist
		threshold := a.getThreshold(domain)
		count, err := a.queries.GetTrajectoryCount(ctx, domain, true)
		if err != nil {
			log.Printf("[%s] Failed to get trajectory count for %s: %v", a.id, domain, err)
			continue
		}

		if count < threshold {
			log.Printf("[%s] %s: %d/%d trajectories (need %d more)",
				a.id, domain, count, threshold, threshold-count)
			continue
		}

		// Attempt crystallization
		a.mu.Lock()
		a.phase = fmt.Sprintf("CRYSTALLIZE_%s", domain)
		a.mu.Unlock()

		heuristic, err := a.crystallize(ctx, domain)
		if err != nil {
			log.Printf("[%s] Crystallization failed for %s: %v", a.id, domain, err)
			continue
		}

		if heuristic != nil {
			crystalized++
			log.Printf("[%s] Crystallized heuristic for %s: %s", a.id, domain, heuristic.Principle)

			// Store heuristic
			if err := a.queries.StoreHeuristic(ctx, *heuristic); err != nil {
				log.Printf("[%s] Failed to store heuristic: %v", a.id, err)
			}

			// Transition from bootstrap to mature phase
			a.mu.Lock()
			if a.bootstrapPhase[domain] {
				a.bootstrapPhase[domain] = false
				log.Printf("[%s] %s transitioned from bootstrap to mature phase", a.id, domain)

				// Mark bootstrap trajectories as inactive
				if err := a.queries.MarkBootstrapTrajectoriesInactive(ctx, domain); err != nil {
					log.Printf("[%s] Failed to mark bootstrap trajectories inactive: %v", a.id, err)
				}
			}
			a.mu.Unlock()
		}
	}

	a.mu.Lock()
	a.cyclesRun++
	a.lastCycle = time.Now()
	a.phase = ""
	a.mu.Unlock()

	duration := time.Since(startTime).Seconds()
	log.Printf("[%s] Cycle completed: crystallized %d heuristics in %.2fs", a.id, crystalized, duration)

	return nil
}

// getThreshold returns the crystallization threshold for a domain
func (a *Agent) getThreshold(domain types.Domain) int {
	a.mu.RLock()
	defer a.mu.RUnlock()

	if a.bootstrapPhase[domain] {
		return a.config.BootstrapThreshold
	}
	return a.config.MatureThreshold
}

// crystallize extracts a heuristic from successful trajectories
func (a *Agent) crystallize(ctx context.Context, domain types.Domain) (*types.Heuristic, error) {
	// Get successful trajectories
	trajectories, err := a.queries.GetSuccessfulTrajectories(ctx, domain, 50, true)
	if err != nil {
		return nil, err
	}

	if len(trajectories) == 0 {
		return nil, nil
	}

	// Build context for extraction
	var trajContext string
	for i, t := range trajectories {
		if i >= 20 { // Limit context size
			break
		}
		trajContext += fmt.Sprintf("\n--- Trajectory %d ---\nProblem: %s\nApproach: %s\nSuccess: %v\n",
			i+1, t.Problem, t.Approach, t.Success)
	}

	prompt := fmt.Sprintf(`Analyze these successful %s trajectories and extract a general principle/heuristic.

%s

Extract ONE concise principle that explains why these approaches succeeded.
The principle should be:
1. General enough to apply to new problems
2. Specific enough to be actionable
3. Based on patterns across multiple trajectories

Output JSON:
{
  "principle": "The extracted principle (1-2 sentences)",
  "source_count": N,  // How many trajectories support this
  "confidence": 0.X   // 0.0-1.0 confidence in this principle
}

Only output the JSON, no other text.`, domain, trajContext)

	response, err := a.infra.LLM().Generate(ctx, prompt, types.GenerateOptions{
		Temperature: 0.3,
		MaxTokens:   500,
	})
	if err != nil {
		return nil, err
	}

	var extraction struct {
		Principle   string  `json:"principle"`
		SourceCount int     `json:"source_count"`
		Confidence  float64 `json:"confidence"`
	}

	response = extractJSON(response)
	if err := json.Unmarshal([]byte(response), &extraction); err != nil {
		return nil, fmt.Errorf("failed to parse extraction: %w", err)
	}

	// Check confidence threshold
	if extraction.Confidence < a.config.MinSuccessRate {
		log.Printf("[%s] Extracted principle has low confidence (%.2f < %.2f)",
			a.id, extraction.Confidence, a.config.MinSuccessRate)
		return nil, nil
	}

	return &types.Heuristic{
		ID:          generateID("heur"),
		Domain:      domain,
		Principle:   extraction.Principle,
		SourceCount: extraction.SourceCount,
		SuccessRate: extraction.Confidence,
		UsageCount:  0,
		CreatedAt:   time.Now(),
	}, nil
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

// generateID generates a unique ID with prefix
func generateID(prefix string) string {
	return fmt.Sprintf("%s_%d", prefix, time.Now().UnixNano())
}

// Ensure Agent implements the Agent interface
var _ types.Agent = (*Agent)(nil)
