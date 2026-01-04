// Package dreamer implements the Dreamer agent for RSI reflection cycles
package dreamer

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

// Agent implements the Dreamer agent
type Agent struct {
	id         string
	pool       *neo4j.Pool
	infra      *infrastructure.Infrastructure
	queries    *neo4j.Queries
	running    bool
	cyclesRun  int
	lastCycle  time.Time
	phase      string
	stopChan   chan struct{}
	mu         sync.RWMutex
}

// New creates a new Dreamer agent
func New(ctx context.Context, pool *neo4j.Pool, infra *infrastructure.Infrastructure, index int) (*Agent, error) {
	return &Agent{
		id:       fmt.Sprintf("dreamer-%d", index),
		pool:     pool,
		infra:    infra,
		queries:  infra.Queries(),
		stopChan: make(chan struct{}),
	}, nil
}

// Run starts the agent's main loop
func (a *Agent) Run(ctx context.Context, interval time.Duration) {
	a.mu.Lock()
	a.running = true
	a.mu.Unlock()

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	log.Printf("[%s] Starting dreamer loop (interval: %v)", a.id, interval)

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
		Type:         "dreamer",
		Running:      a.running,
		CyclesRun:    a.cyclesRun,
		LastCycleAt:  a.lastCycle,
		CurrentPhase: a.phase,
	}
}

// runCycle executes a single reflection cycle
func (a *Agent) runCycle(ctx context.Context) error {
	startTime := time.Now()

	a.mu.Lock()
	a.phase = "REFLECT"
	a.mu.Unlock()

	// Phase 1: Reflect - Generate desires from LLM
	desires, err := a.reflect(ctx)
	if err != nil {
		return fmt.Errorf("reflect failed: %w", err)
	}

	log.Printf("[%s] Generated %d desires", a.id, len(desires))

	a.mu.Lock()
	a.phase = "VERIFY"
	a.mu.Unlock()

	// Phase 2: Verify - Check each desire for emergence
	verified := make([]types.Desire, 0)
	for _, d := range desires {
		if a.verifyEmergence(ctx, d) {
			d.Verified = true
			verified = append(verified, d)
		}
	}

	log.Printf("[%s] Verified %d/%d desires", a.id, len(verified), len(desires))

	// Store verified desires
	for _, d := range verified {
		if err := a.queries.StoreDesire(ctx, d); err != nil {
			log.Printf("[%s] Failed to store desire: %v", a.id, err)
		}
	}

	a.mu.Lock()
	a.cyclesRun++
	a.lastCycle = time.Now()
	a.phase = ""
	a.mu.Unlock()

	duration := time.Since(startTime).Seconds()
	log.Printf("[%s] Cycle completed in %.2fs", a.id, duration)

	return nil
}

// reflect generates desires through LLM reflection
func (a *Agent) reflect(ctx context.Context) ([]types.Desire, error) {
	// Get quantum temperature modulation
	temperature := 0.7
	if a.infra.Quantum() != nil {
		modulated, err := a.infra.Quantum().GetTemperatureDelta(ctx, 0.7, 0.15)
		if err == nil {
			temperature = modulated
		}
	}

	prompt := `You are BYRD, an AI system engaged in recursive self-improvement.
Reflect on your current state and generate desires for improvement.

Output a JSON array of desires, each with:
- description: What you want to achieve
- intensity: 0.0-1.0 how strongly you want this
- domain: "code", "math", "logic", or null if unclear

Example:
[
  {"description": "Learn to write more efficient sorting algorithms", "intensity": 0.8, "domain": "code"},
  {"description": "Understand the relationship between recursion and iteration", "intensity": 0.6, "domain": "logic"}
]

Output ONLY the JSON array, no other text.`

	response, err := a.infra.LLM().Generate(ctx, prompt, types.GenerateOptions{
		Temperature: temperature,
		MaxTokens:   1000,
	})
	if err != nil {
		return nil, err
	}

	// Parse response
	var rawDesires []struct {
		Description string  `json:"description"`
		Intensity   float64 `json:"intensity"`
		Domain      *string `json:"domain"`
	}

	if err := json.Unmarshal([]byte(response), &rawDesires); err != nil {
		// Try to extract JSON from markdown code blocks
		response = extractJSON(response)
		if err := json.Unmarshal([]byte(response), &rawDesires); err != nil {
			return nil, fmt.Errorf("failed to parse desires: %w", err)
		}
	}

	// Convert to typed desires
	desires := make([]types.Desire, 0, len(rawDesires))
	for _, rd := range rawDesires {
		d := types.Desire{
			ID:          generateID("des"),
			Description: rd.Description,
			Intensity:   rd.Intensity,
			CreatedAt:   time.Now(),
		}
		if rd.Domain != nil {
			d.Domain = types.Domain(*rd.Domain)
		}
		desires = append(desires, d)
	}

	return desires, nil
}

// verifyEmergence checks if a desire is genuinely emergent
func (a *Agent) verifyEmergence(ctx context.Context, d types.Desire) bool {
	// Basic checks: has description, reasonable intensity
	if d.Description == "" || d.Intensity < 0.1 {
		return false
	}

	// Check for actionability and specificity
	prompt := fmt.Sprintf(`Evaluate this desire for emergence quality:
"%s"

Score on two criteria (0.0-1.0):
1. Actionability: Can this be acted upon concretely?
2. Specificity: Is this specific enough to work on?

Output JSON: {"actionability": 0.X, "specificity": 0.X}
Only output the JSON, no other text.`, d.Description)

	response, err := a.infra.LLM().Generate(ctx, prompt, types.GenerateOptions{
		Temperature: 0.1, // Low temperature for consistent evaluation
		MaxTokens:   100,
	})
	if err != nil {
		// If LLM fails, use basic heuristics
		return len(d.Description) > 20 && d.Intensity >= 0.3
	}

	var scores struct {
		Actionability float64 `json:"actionability"`
		Specificity   float64 `json:"specificity"`
	}

	response = extractJSON(response)
	if err := json.Unmarshal([]byte(response), &scores); err != nil {
		return len(d.Description) > 20 && d.Intensity >= 0.3
	}

	// Both scores must exceed threshold
	threshold := 0.6
	return scores.Actionability >= threshold && scores.Specificity >= threshold
}

// extractJSON extracts JSON from markdown code blocks
func extractJSON(s string) string {
	// Remove markdown code blocks
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
