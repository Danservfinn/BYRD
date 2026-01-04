// Package grpc provides gRPC server and service implementations
package grpc

import (
	"context"
	"fmt"
	"log"
	"net"

	"github.com/byrd-ai/gastown/internal/agents/infrastructure"
	"github.com/byrd-ai/gastown/internal/neo4j"
	"github.com/byrd-ai/gastown/pkg/types"
	"google.golang.org/grpc"
)

// Server wraps the gRPC server with RSI services
type Server struct {
	grpcServer *grpc.Server
	pool       *neo4j.Pool
	infra      *infrastructure.Infrastructure
	queries    *neo4j.Queries
	port       int
}

// NewServer creates a new gRPC server
func NewServer(pool *neo4j.Pool, infra *infrastructure.Infrastructure, port int) *Server {
	return &Server{
		grpcServer: grpc.NewServer(),
		pool:       pool,
		infra:      infra,
		queries:    infra.Queries(),
		port:       port,
	}
}

// Start starts the gRPC server
func (s *Server) Start(ctx context.Context) error {
	// Register services
	// Note: In production, generate pb.go files from rsi.proto
	// and register actual service implementations

	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", s.port))
	if err != nil {
		return fmt.Errorf("failed to listen: %w", err)
	}

	log.Printf("gRPC server starting on port %d", s.port)

	go func() {
		<-ctx.Done()
		log.Println("Shutting down gRPC server...")
		s.grpcServer.GracefulStop()
	}()

	return s.grpcServer.Serve(lis)
}

// Stop stops the gRPC server
func (s *Server) Stop() {
	s.grpcServer.GracefulStop()
}

// DesireServiceImpl implements the DesireService
type DesireServiceImpl struct {
	queries *neo4j.Queries
}

// NewDesireService creates a new DesireService implementation
func NewDesireService(queries *neo4j.Queries) *DesireServiceImpl {
	return &DesireServiceImpl{queries: queries}
}

// SubmitDesire stores a new verified desire
func (s *DesireServiceImpl) SubmitDesire(ctx context.Context, d *types.Desire) error {
	return s.queries.StoreDesire(ctx, *d)
}

// GetPendingDesires retrieves unprocessed desires
func (s *DesireServiceImpl) GetPendingDesires(ctx context.Context, domain types.Domain, limit int) ([]types.Desire, error) {
	return s.queries.GetPendingDesires(ctx, limit)
}

// TrajectoryServiceImpl implements the TrajectoryService
type TrajectoryServiceImpl struct {
	queries *neo4j.Queries
}

// NewTrajectoryService creates a new TrajectoryService implementation
func NewTrajectoryService(queries *neo4j.Queries) *TrajectoryServiceImpl {
	return &TrajectoryServiceImpl{queries: queries}
}

// StoreTrajectory stores a learning trajectory
func (s *TrajectoryServiceImpl) StoreTrajectory(ctx context.Context, t *types.Trajectory) error {
	return s.queries.StoreTrajectory(ctx, *t)
}

// GetTrajectories retrieves trajectories for a domain
func (s *TrajectoryServiceImpl) GetTrajectories(ctx context.Context, domain types.Domain, limit int, successOnly, includeBootstrap bool) ([]types.Trajectory, error) {
	return s.queries.GetSuccessfulTrajectories(ctx, domain, limit, includeBootstrap)
}

// HeuristicServiceImpl implements the HeuristicService
type HeuristicServiceImpl struct {
	queries *neo4j.Queries
}

// NewHeuristicService creates a new HeuristicService implementation
func NewHeuristicService(queries *neo4j.Queries) *HeuristicServiceImpl {
	return &HeuristicServiceImpl{queries: queries}
}

// StoreHeuristic stores a crystallized heuristic
func (s *HeuristicServiceImpl) StoreHeuristic(ctx context.Context, h *types.Heuristic) error {
	return s.queries.StoreHeuristic(ctx, *h)
}

// GetHeuristics retrieves heuristics for a domain
func (s *HeuristicServiceImpl) GetHeuristics(ctx context.Context, domain types.Domain) ([]types.Heuristic, error) {
	return s.queries.GetHeuristicsByDomain(ctx, domain)
}

// IncrementUsage increments heuristic usage count
func (s *HeuristicServiceImpl) IncrementUsage(ctx context.Context, id string) error {
	return s.queries.IncrementHeuristicUsage(ctx, id)
}

// MetricsServiceImpl implements the MetricsService
type MetricsServiceImpl struct {
	metrics *infrastructure.MetricsCollector
}

// NewMetricsService creates a new MetricsService implementation
func NewMetricsService(metrics *infrastructure.MetricsCollector) *MetricsServiceImpl {
	return &MetricsServiceImpl{metrics: metrics}
}

// GetMetrics retrieves current RSI metrics
func (s *MetricsServiceImpl) GetMetrics(ctx context.Context) (*types.RSIMetrics, error) {
	return s.metrics.GetMetrics(ctx)
}

// ValidatePhaseGate checks Phase Gate criteria
func (s *MetricsServiceImpl) ValidatePhaseGate(ctx context.Context) (bool, map[string]bool, error) {
	return s.metrics.ValidatePhaseGate(ctx)
}
