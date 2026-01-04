// Package neo4j provides connection pooling and query utilities for Neo4j
package neo4j

import (
	"context"
	"fmt"
	"sync"
	"time"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

// Config holds Neo4j connection configuration
type Config struct {
	URI       string `yaml:"uri"`
	User      string `yaml:"user"`
	Password  string `yaml:"password"`
	PoolSize  int    `yaml:"pool_size"`
	Database  string `yaml:"database"`
}

// Pool manages Neo4j driver and session pooling
type Pool struct {
	driver   neo4j.DriverWithContext
	config   Config
	mu       sync.RWMutex
	sessions int
}

// NewPool creates a new Neo4j connection pool
func NewPool(ctx context.Context, config Config) (*Pool, error) {
	// Set defaults
	if config.PoolSize == 0 {
		config.PoolSize = 20
	}
	if config.Database == "" {
		config.Database = "neo4j"
	}

	// Create driver
	driver, err := neo4j.NewDriverWithContext(
		config.URI,
		neo4j.BasicAuth(config.User, config.Password, ""),
		func(c *neo4j.Config) {
			c.MaxConnectionPoolSize = config.PoolSize
			c.MaxConnectionLifetime = 30 * time.Minute
			c.ConnectionAcquisitionTimeout = 10 * time.Second
		},
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create Neo4j driver: %w", err)
	}

	// Verify connectivity
	if err := driver.VerifyConnectivity(ctx); err != nil {
		driver.Close(ctx)
		return nil, fmt.Errorf("failed to verify Neo4j connectivity: %w", err)
	}

	return &Pool{
		driver: driver,
		config: config,
	}, nil
}

// Session returns a Neo4j session for queries
func (p *Pool) Session(ctx context.Context) neo4j.SessionWithContext {
	p.mu.Lock()
	p.sessions++
	p.mu.Unlock()

	return p.driver.NewSession(ctx, neo4j.SessionConfig{
		DatabaseName: p.config.Database,
	})
}

// Close closes the driver and all connections
func (p *Pool) Close() error {
	return p.driver.Close(context.Background())
}

// Stats returns pool statistics
func (p *Pool) Stats() PoolStats {
	p.mu.RLock()
	defer p.mu.RUnlock()
	return PoolStats{
		ActiveSessions: p.sessions,
		MaxPoolSize:    p.config.PoolSize,
	}
}

// PoolStats contains pool statistics
type PoolStats struct {
	ActiveSessions int
	MaxPoolSize    int
}
