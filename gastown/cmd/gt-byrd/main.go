// Gastown-BYRD: Parallel RSI Agent Execution Layer
//
// Phase 2 of the Q-DE-RSI architecture. Gastown provides:
// - Parallel agent execution (multiple RSI cycles concurrently)
// - Neo4j connection pooling and shared memory access
// - gRPC-based inter-agent communication
// - Horizontal scaling with load balancing
//
// Agents:
// - Dreamer: Runs reflection cycles, emits emergent desires
// - Coder: Executes TDD practice in code domain
// - Crystallizer: Extracts heuristics from successful trajectories
// - Infrastructure: Quantum randomness, metrics, coordination

package main

import (
	"context"
	"flag"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/byrd-ai/gastown/internal/agents/coder"
	"github.com/byrd-ai/gastown/internal/agents/crystallizer"
	"github.com/byrd-ai/gastown/internal/agents/dreamer"
	"github.com/byrd-ai/gastown/internal/agents/infrastructure"
	"github.com/byrd-ai/gastown/internal/neo4j"
	"github.com/byrd-ai/gastown/pkg/types"
	"gopkg.in/yaml.v3"
)

// Config holds Gastown configuration
type Config struct {
	Neo4j      neo4j.Config      `yaml:"neo4j"`
	Agents     AgentConfig       `yaml:"agents"`
	GRPC       GRPCConfig        `yaml:"grpc"`
	Monitoring MonitoringConfig  `yaml:"monitoring"`
}

type AgentConfig struct {
	Dreamers      int           `yaml:"dreamers"`       // Number of parallel dreamer agents
	Coders        int           `yaml:"coders"`         // Number of parallel coder agents
	Crystallizers int           `yaml:"crystallizers"`  // Number of crystallizer agents
	CycleInterval time.Duration `yaml:"cycle_interval"` // Time between cycles
}

type GRPCConfig struct {
	Port int `yaml:"port"`
}

type MonitoringConfig struct {
	MetricsPort int  `yaml:"metrics_port"`
	EnablePprof bool `yaml:"enable_pprof"`
}

func main() {
	// Parse command line flags
	configPath := flag.String("config", "configs/gastown.yaml", "Path to configuration file")
	flag.Parse()

	// Load configuration
	config, err := loadConfig(*configPath)
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	// Create context with cancellation
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Initialize Neo4j connection pool
	pool, err := neo4j.NewPool(ctx, config.Neo4j)
	if err != nil {
		log.Fatalf("Failed to create Neo4j pool: %v", err)
	}
	defer pool.Close()

	log.Println("Connected to Neo4j")

	// Initialize infrastructure (quantum, metrics, coordination)
	infra, err := infrastructure.New(ctx, pool)
	if err != nil {
		log.Fatalf("Failed to initialize infrastructure: %v", err)
	}

	log.Println("Infrastructure initialized")

	// Create agent orchestrator
	orchestrator := NewOrchestrator(pool, infra, config.Agents)

	// Start agents
	if err := orchestrator.Start(ctx); err != nil {
		log.Fatalf("Failed to start orchestrator: %v", err)
	}

	log.Printf("Gastown started: %d dreamers, %d coders, %d crystallizers",
		config.Agents.Dreamers, config.Agents.Coders, config.Agents.Crystallizers)

	// Wait for shutdown signal
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan

	log.Println("Shutting down...")
	cancel()

	// Graceful shutdown
	orchestrator.Stop()
	log.Println("Gastown stopped")
}

// Orchestrator manages parallel agent execution
type Orchestrator struct {
	pool     *neo4j.Pool
	infra    *infrastructure.Infrastructure
	config   AgentConfig
	dreamers []*dreamer.Agent
	coders   []*coder.Agent
	crystals []*crystallizer.Agent
}

func NewOrchestrator(pool *neo4j.Pool, infra *infrastructure.Infrastructure, config AgentConfig) *Orchestrator {
	return &Orchestrator{
		pool:   pool,
		infra:  infra,
		config: config,
	}
}

func (o *Orchestrator) Start(ctx context.Context) error {
	// Start dreamer agents
	for i := 0; i < o.config.Dreamers; i++ {
		agent, err := dreamer.New(ctx, o.pool, o.infra, i)
		if err != nil {
			return err
		}
		o.dreamers = append(o.dreamers, agent)
		go agent.Run(ctx, o.config.CycleInterval)
	}

	// Start coder agents
	for i := 0; i < o.config.Coders; i++ {
		agent, err := coder.New(ctx, o.pool, o.infra, i)
		if err != nil {
			return err
		}
		o.coders = append(o.coders, agent)
		go agent.Run(ctx, o.config.CycleInterval)
	}

	// Start crystallizer agents
	for i := 0; i < o.config.Crystallizers; i++ {
		agent, err := crystallizer.New(ctx, o.pool, o.infra, i)
		if err != nil {
			return err
		}
		o.crystals = append(o.crystals, agent)
		go agent.Run(ctx, o.config.CycleInterval*5) // Crystallize less frequently
	}

	return nil
}

func (o *Orchestrator) Stop() {
	// Stop all agents gracefully
	for _, d := range o.dreamers {
		d.Stop()
	}
	for _, c := range o.coders {
		c.Stop()
	}
	for _, cr := range o.crystals {
		cr.Stop()
	}
}

func loadConfig(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		// Return defaults if config doesn't exist
		return &Config{
			Neo4j: neo4j.Config{
				URI:      os.Getenv("NEO4J_URI"),
				User:     os.Getenv("NEO4J_USER"),
				Password: os.Getenv("NEO4J_PASSWORD"),
				PoolSize: 20,
			},
			Agents: AgentConfig{
				Dreamers:      2,
				Coders:        4,
				Crystallizers: 1,
				CycleInterval: 30 * time.Second,
			},
			GRPC: GRPCConfig{
				Port: 50051,
			},
			Monitoring: MonitoringConfig{
				MetricsPort: 9090,
				EnablePprof: true,
			},
		}, nil
	}

	var config Config
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, err
	}

	return &config, nil
}

// Compile-time interface checks
var _ types.AgentOrchestrator = (*Orchestrator)(nil)
