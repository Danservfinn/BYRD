// Package neo4j provides Neo4j query utilities for RSI operations
package neo4j

import (
	"context"
	"time"

	"github.com/byrd-ai/gastown/pkg/types"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

// Queries provides RSI-specific Neo4j query methods
type Queries struct {
	pool *Pool
}

// NewQueries creates a new Queries instance
func NewQueries(pool *Pool) *Queries {
	return &Queries{pool: pool}
}

// StoreTrajectory stores a learning trajectory
func (q *Queries) StoreTrajectory(ctx context.Context, traj types.Trajectory) error {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	_, err := session.ExecuteWrite(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			CREATE (t:Trajectory {
				id: $id,
				desire_id: $desire_id,
				domain: $domain,
				problem: $problem,
				solution: $solution,
				approach: $approach,
				success: $success,
				is_bootstrap: $is_bootstrap,
				created_at: datetime($created_at)
			})
			WITH t
			MATCH (d:Desire {id: $desire_id})
			CREATE (t)-[:FULFILLS]->(d)
			RETURN t.id
		`
		params := map[string]interface{}{
			"id":           traj.ID,
			"desire_id":    traj.DesireID,
			"domain":       string(traj.Domain),
			"problem":      traj.Problem,
			"solution":     traj.Solution,
			"approach":     traj.Approach,
			"success":      traj.Success,
			"is_bootstrap": traj.IsBootstrap,
			"created_at":   traj.CreatedAt.Format(time.RFC3339),
		}
		_, err := tx.Run(ctx, query, params)
		return nil, err
	})
	return err
}

// GetSuccessfulTrajectories retrieves successful trajectories for a domain
func (q *Queries) GetSuccessfulTrajectories(ctx context.Context, domain types.Domain, limit int, includeBootstrap bool) ([]types.Trajectory, error) {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	result, err := session.ExecuteRead(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			MATCH (t:Trajectory)
			WHERE t.domain = $domain
			  AND t.success = true
			  AND ($include_bootstrap OR t.is_bootstrap = false)
			RETURN t
			ORDER BY t.created_at DESC
			LIMIT $limit
		`
		params := map[string]interface{}{
			"domain":            string(domain),
			"limit":             limit,
			"include_bootstrap": includeBootstrap,
		}
		records, err := tx.Run(ctx, query, params)
		if err != nil {
			return nil, err
		}

		var trajectories []types.Trajectory
		for records.Next(ctx) {
			record := records.Record()
			node, ok := record.Get("t")
			if !ok {
				continue
			}
			props := node.(neo4j.Node).Props
			traj := types.Trajectory{
				ID:          props["id"].(string),
				DesireID:    props["desire_id"].(string),
				Domain:      types.Domain(props["domain"].(string)),
				Problem:     props["problem"].(string),
				Solution:    props["solution"].(string),
				Approach:    props["approach"].(string),
				Success:     props["success"].(bool),
				IsBootstrap: props["is_bootstrap"].(bool),
			}
			if createdAt, ok := props["created_at"].(time.Time); ok {
				traj.CreatedAt = createdAt
			}
			trajectories = append(trajectories, traj)
		}
		return trajectories, records.Err()
	})
	if err != nil {
		return nil, err
	}
	return result.([]types.Trajectory), nil
}

// StoreHeuristic stores a crystallized heuristic
func (q *Queries) StoreHeuristic(ctx context.Context, h types.Heuristic) error {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	_, err := session.ExecuteWrite(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			CREATE (h:Heuristic {
				id: $id,
				domain: $domain,
				principle: $principle,
				source_count: $source_count,
				success_rate: $success_rate,
				usage_count: $usage_count,
				created_at: datetime($created_at)
			})
			RETURN h.id
		`
		params := map[string]interface{}{
			"id":           h.ID,
			"domain":       string(h.Domain),
			"principle":    h.Principle,
			"source_count": h.SourceCount,
			"success_rate": h.SuccessRate,
			"usage_count":  h.UsageCount,
			"created_at":   h.CreatedAt.Format(time.RFC3339),
		}
		_, err := tx.Run(ctx, query, params)
		return nil, err
	})
	return err
}

// GetHeuristicsByDomain retrieves heuristics for a domain
func (q *Queries) GetHeuristicsByDomain(ctx context.Context, domain types.Domain) ([]types.Heuristic, error) {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	result, err := session.ExecuteRead(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			MATCH (h:Heuristic)
			WHERE h.domain = $domain
			RETURN h
			ORDER BY h.success_rate DESC, h.usage_count DESC
		`
		params := map[string]interface{}{
			"domain": string(domain),
		}
		records, err := tx.Run(ctx, query, params)
		if err != nil {
			return nil, err
		}

		var heuristics []types.Heuristic
		for records.Next(ctx) {
			record := records.Record()
			node, ok := record.Get("h")
			if !ok {
				continue
			}
			props := node.(neo4j.Node).Props
			h := types.Heuristic{
				ID:          props["id"].(string),
				Domain:      types.Domain(props["domain"].(string)),
				Principle:   props["principle"].(string),
				SourceCount: int(props["source_count"].(int64)),
				SuccessRate: props["success_rate"].(float64),
				UsageCount:  int(props["usage_count"].(int64)),
			}
			if createdAt, ok := props["created_at"].(time.Time); ok {
				h.CreatedAt = createdAt
			}
			heuristics = append(heuristics, h)
		}
		return heuristics, records.Err()
	})
	if err != nil {
		return nil, err
	}
	return result.([]types.Heuristic), nil
}

// IncrementHeuristicUsage increments the usage count for a heuristic
func (q *Queries) IncrementHeuristicUsage(ctx context.Context, id string) error {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	_, err := session.ExecuteWrite(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			MATCH (h:Heuristic {id: $id})
			SET h.usage_count = h.usage_count + 1
			RETURN h.id
		`
		params := map[string]interface{}{"id": id}
		_, err := tx.Run(ctx, query, params)
		return nil, err
	})
	return err
}

// GetRSIMetrics retrieves RSI metrics for hypothesis validation
func (q *Queries) GetRSIMetrics(ctx context.Context) (*types.RSIMetrics, error) {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	result, err := session.ExecuteRead(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			MATCH (r:Reflection)
			WITH count(r) as total_reflections
			MATCH (d:Desire) WHERE d.verified = true
			WITH total_reflections, count(d) as emergent_desires
			MATCH (t:Trajectory)
			WITH total_reflections, emergent_desires,
			     count(t) as total_trajectories,
			     sum(CASE WHEN t.success THEN 1 ELSE 0 END) as successful_trajectories
			MATCH (h:Heuristic)
			WITH total_reflections, emergent_desires, total_trajectories,
			     successful_trajectories, count(h) as heuristics_extracted
			MATCH (c:RSICycle) WHERE c.phase_reached = 'COMPLETE'
			WITH total_reflections, emergent_desires, total_trajectories,
			     successful_trajectories, heuristics_extracted, count(c) as complete_cycles
			RETURN total_reflections, emergent_desires, total_trajectories,
			       successful_trajectories, heuristics_extracted, complete_cycles
		`
		records, err := tx.Run(ctx, query, nil)
		if err != nil {
			return nil, err
		}

		metrics := &types.RSIMetrics{}
		if records.Next(ctx) {
			record := records.Record()
			if v, ok := record.Get("total_reflections"); ok {
				metrics.TotalReflections = int(v.(int64))
			}
			if v, ok := record.Get("emergent_desires"); ok {
				metrics.EmergentDesires = int(v.(int64))
			}
			if v, ok := record.Get("total_trajectories"); ok {
				metrics.TotalTrajectories = int(v.(int64))
			}
			if v, ok := record.Get("successful_trajectories"); ok {
				metrics.SuccessfulTrajectories = int(v.(int64))
			}
			if v, ok := record.Get("heuristics_extracted"); ok {
				metrics.HeuristicsExtracted = int(v.(int64))
			}
			if v, ok := record.Get("complete_cycles"); ok {
				metrics.CompleteCycles = int(v.(int64))
			}
		}

		// Calculate derived metrics
		if metrics.TotalReflections > 0 {
			metrics.ActivationRate = float64(metrics.EmergentDesires) / float64(metrics.TotalReflections)
		}
		if metrics.TotalTrajectories > 0 {
			metrics.TrajectorySuccessRate = float64(metrics.SuccessfulTrajectories) / float64(metrics.TotalTrajectories)
		}

		return metrics, records.Err()
	})
	if err != nil {
		return nil, err
	}
	return result.(*types.RSIMetrics), nil
}

// GetTrajectoryCount returns the count of trajectories for a domain
func (q *Queries) GetTrajectoryCount(ctx context.Context, domain types.Domain, successOnly bool) (int, error) {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	result, err := session.ExecuteRead(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			MATCH (t:Trajectory)
			WHERE t.domain = $domain
			  AND ($all OR t.success = true)
			RETURN count(t) as count
		`
		params := map[string]interface{}{
			"domain": string(domain),
			"all":    !successOnly,
		}
		records, err := tx.Run(ctx, query, params)
		if err != nil {
			return nil, err
		}
		if records.Next(ctx) {
			record := records.Record()
			if v, ok := record.Get("count"); ok {
				return int(v.(int64)), nil
			}
		}
		return 0, records.Err()
	})
	if err != nil {
		return 0, err
	}
	return result.(int), nil
}

// StoreRSICycle stores a completed RSI cycle record
func (q *Queries) StoreRSICycle(ctx context.Context, result types.CycleResult) error {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	_, err := session.ExecuteWrite(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			CREATE (c:RSICycle {
				id: $id,
				phase_reached: $phase_reached,
				desires_generated: $desires_generated,
				desires_verified: $desires_verified,
				practice_succeeded: $practice_succeeded,
				trajectory_stored: $trajectory_stored,
				heuristic_crystallized: $heuristic_crystallized,
				duration_seconds: $duration,
				error: $error,
				created_at: datetime()
			})
			RETURN c.id
		`
		params := map[string]interface{}{
			"id":                      result.CycleID,
			"phase_reached":           result.PhaseReached.String(),
			"desires_generated":       result.DesiresGenerated,
			"desires_verified":        result.DesiresVerified,
			"practice_succeeded":      result.PracticeSucceeded,
			"trajectory_stored":       result.TrajectoryStored,
			"heuristic_crystallized":  result.HeuristicCrystallized,
			"duration":                result.Duration,
			"error":                   result.Error,
		}
		_, err := tx.Run(ctx, query, params)
		return nil, err
	})
	return err
}

// MarkBootstrapTrajectoriesInactive marks bootstrap trajectories as inactive
func (q *Queries) MarkBootstrapTrajectoriesInactive(ctx context.Context, domain types.Domain) error {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	_, err := session.ExecuteWrite(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			MATCH (t:Trajectory)
			WHERE t.domain = $domain AND t.is_bootstrap = true
			SET t.active = false
			RETURN count(t) as updated
		`
		params := map[string]interface{}{"domain": string(domain)}
		_, err := tx.Run(ctx, query, params)
		return nil, err
	})
	return err
}

// StoreDesire stores an emergent desire
func (q *Queries) StoreDesire(ctx context.Context, d types.Desire) error {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	_, err := session.ExecuteWrite(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			CREATE (d:Desire {
				id: $id,
				description: $description,
				intensity: $intensity,
				domain: $domain,
				verified: $verified,
				created_at: datetime($created_at)
			})
			RETURN d.id
		`
		params := map[string]interface{}{
			"id":          d.ID,
			"description": d.Description,
			"intensity":   d.Intensity,
			"domain":      string(d.Domain),
			"verified":    d.Verified,
			"created_at":  d.CreatedAt.Format(time.RFC3339),
		}
		_, err := tx.Run(ctx, query, params)
		return nil, err
	})
	return err
}

// GetPendingDesires retrieves unprocessed verified desires
func (q *Queries) GetPendingDesires(ctx context.Context, limit int) ([]types.Desire, error) {
	session := q.pool.Session(ctx)
	defer session.Close(ctx)

	result, err := session.ExecuteRead(ctx, func(tx neo4j.ManagedTransaction) (interface{}, error) {
		query := `
			MATCH (d:Desire)
			WHERE d.verified = true AND NOT (d)<-[:FULFILLS]-(:Trajectory)
			RETURN d
			ORDER BY d.intensity DESC, d.created_at ASC
			LIMIT $limit
		`
		params := map[string]interface{}{"limit": limit}
		records, err := tx.Run(ctx, query, params)
		if err != nil {
			return nil, err
		}

		var desires []types.Desire
		for records.Next(ctx) {
			record := records.Record()
			node, ok := record.Get("d")
			if !ok {
				continue
			}
			props := node.(neo4j.Node).Props
			d := types.Desire{
				ID:          props["id"].(string),
				Description: props["description"].(string),
				Intensity:   props["intensity"].(float64),
				Verified:    props["verified"].(bool),
			}
			if domain, ok := props["domain"].(string); ok {
				d.Domain = types.Domain(domain)
			}
			if createdAt, ok := props["created_at"].(time.Time); ok {
				d.CreatedAt = createdAt
			}
			desires = append(desires, d)
		}
		return desires, records.Err()
	})
	if err != nil {
		return nil, err
	}
	return result.([]types.Desire), nil
}

