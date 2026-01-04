// Package types defines shared types for Gastown agents
package types

import (
	"context"
	"time"
)

// Domain represents a verifiable learning domain
type Domain string

const (
	DomainCode  Domain = "code"
	DomainMath  Domain = "math"
	DomainLogic Domain = "logic"
)

// Desire represents an emergent desire from reflection
type Desire struct {
	ID          string                 `json:"id"`
	Description string                 `json:"description"`
	Intensity   float64                `json:"intensity"`
	Domain      Domain                 `json:"domain,omitempty"`
	Verified    bool                   `json:"verified"`
	CreatedAt   time.Time              `json:"created_at"`
	Metadata    map[string]interface{} `json:"metadata,omitempty"`
}

// Trajectory represents a learning trajectory (problem-solution pair)
type Trajectory struct {
	ID           string                 `json:"id"`
	DesireID     string                 `json:"desire_id"`
	Domain       Domain                 `json:"domain"`
	Problem      string                 `json:"problem"`
	Solution     string                 `json:"solution"`
	Approach     string                 `json:"approach"`
	Success      bool                   `json:"success"`
	Metadata     map[string]interface{} `json:"metadata,omitempty"`
	CreatedAt    time.Time              `json:"created_at"`
	IsBootstrap  bool                   `json:"is_bootstrap"`
}

// Heuristic represents a crystallized learning principle
type Heuristic struct {
	ID            string    `json:"id"`
	Domain        Domain    `json:"domain"`
	Principle     string    `json:"principle"`
	SourceCount   int       `json:"source_count"`
	SuccessRate   float64   `json:"success_rate"`
	UsageCount    int       `json:"usage_count"`
	CreatedAt     time.Time `json:"created_at"`
}

// PracticeResult represents the outcome of a practice session
type PracticeResult struct {
	Success      bool    `json:"success"`
	Solution     string  `json:"solution,omitempty"`
	Error        string  `json:"error,omitempty"`
	Attempts     int     `json:"attempts"`
	Duration     float64 `json:"duration_seconds"`
}

// CycleResult represents the outcome of an RSI cycle
type CycleResult struct {
	CycleID            string        `json:"cycle_id"`
	PhaseReached       CyclePhase    `json:"phase_reached"`
	DesiresGenerated   int           `json:"desires_generated"`
	DesiresVerified    int           `json:"desires_verified"`
	PracticeSucceeded  bool          `json:"practice_succeeded"`
	TrajectoryStored   bool          `json:"trajectory_stored"`
	HeuristicCrystallized bool       `json:"heuristic_crystallized"`
	Duration           float64       `json:"duration_seconds"`
	Error              string        `json:"error,omitempty"`
}

// CyclePhase represents phases of the RSI cycle
type CyclePhase int

const (
	PhaseReflect CyclePhase = iota
	PhaseVerify
	PhaseCollapse
	PhaseRoute
	PhasePractice
	PhaseRecord
	PhaseCrystallize
	PhaseMeasure
	PhaseComplete
)

func (p CyclePhase) String() string {
	names := []string{
		"REFLECT", "VERIFY", "COLLAPSE", "ROUTE",
		"PRACTICE", "RECORD", "CRYSTALLIZE", "MEASURE", "COMPLETE",
	}
	if int(p) < len(names) {
		return names[p]
	}
	return "UNKNOWN"
}

// RSIMetrics contains metrics for hypothesis validation
type RSIMetrics struct {
	TotalReflections      int     `json:"total_reflections"`
	EmergentDesires       int     `json:"emergent_desires"`
	ActivationRate        float64 `json:"activation_rate"`
	TotalTrajectories     int     `json:"total_trajectories"`
	SuccessfulTrajectories int    `json:"successful_trajectories"`
	TrajectorySuccessRate float64 `json:"trajectory_success_rate"`
	HeuristicsExtracted   int     `json:"heuristics_extracted"`
	CompleteCycles        int     `json:"complete_cycles"`
	DirectionVariance     float64 `json:"direction_variance"`
	TestPassRate          float64 `json:"test_pass_rate"`
}

// Agent defines the interface for RSI agents
type Agent interface {
	// Run starts the agent's main loop
	Run(ctx context.Context, interval time.Duration)
	// Stop gracefully stops the agent
	Stop()
	// ID returns the agent's identifier
	ID() string
	// Status returns the agent's current status
	Status() AgentStatus
}

// AgentStatus represents an agent's current state
type AgentStatus struct {
	ID           string    `json:"id"`
	Type         string    `json:"type"`
	Running      bool      `json:"running"`
	CyclesRun    int       `json:"cycles_run"`
	LastCycleAt  time.Time `json:"last_cycle_at"`
	CurrentPhase string    `json:"current_phase,omitempty"`
	Error        string    `json:"error,omitempty"`
}

// AgentOrchestrator defines the interface for the agent coordinator
type AgentOrchestrator interface {
	// Start begins all agents
	Start(ctx context.Context) error
	// Stop gracefully stops all agents
	Stop()
}

// MemoryPool defines the interface for Neo4j connection pooling
type MemoryPool interface {
	// GetSession returns a Neo4j session from the pool
	GetSession(ctx context.Context) (Session, error)
	// Close closes all connections in the pool
	Close() error
}

// Session defines the interface for Neo4j sessions
type Session interface {
	// Run executes a Cypher query
	Run(ctx context.Context, query string, params map[string]interface{}) (Result, error)
	// Close returns the session to the pool
	Close() error
}

// Result defines the interface for query results
type Result interface {
	// Next moves to the next record
	Next() bool
	// Record returns the current record
	Record() Record
	// Err returns any error that occurred
	Err() error
}

// Record defines the interface for a result record
type Record interface {
	// Get returns a value by key
	Get(key string) (interface{}, bool)
	// Values returns all values
	Values() []interface{}
}

// QuantumProvider defines the interface for quantum randomness
type QuantumProvider interface {
	// GetFloat returns a random float in [0, 1)
	GetFloat(ctx context.Context) (float64, string, error)
	// GetTemperatureDelta returns a temperature modulation value
	GetTemperatureDelta(ctx context.Context, base, maxDelta float64) (float64, error)
}

// LLMClient defines the interface for LLM API calls
type LLMClient interface {
	// Generate generates text from a prompt
	Generate(ctx context.Context, prompt string, opts GenerateOptions) (string, error)
}

// GenerateOptions contains options for LLM generation
type GenerateOptions struct {
	Temperature float64 `json:"temperature"`
	MaxTokens   int     `json:"max_tokens"`
	Model       string  `json:"model,omitempty"`
}
