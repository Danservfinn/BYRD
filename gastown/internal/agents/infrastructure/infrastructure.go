// Package infrastructure provides shared infrastructure for RSI agents
package infrastructure

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"

	"github.com/byrd-ai/gastown/internal/neo4j"
	"github.com/byrd-ai/gastown/pkg/types"
)

// Infrastructure provides shared services for agents
type Infrastructure struct {
	pool     *neo4j.Pool
	queries  *neo4j.Queries
	quantum  *QuantumProvider
	llm      *LLMClient
	metrics  *MetricsCollector
	mu       sync.RWMutex
}

// New creates a new Infrastructure instance
func New(ctx context.Context, pool *neo4j.Pool) (*Infrastructure, error) {
	queries := neo4j.NewQueries(pool)

	quantum, err := NewQuantumProvider(ctx)
	if err != nil {
		// Quantum is optional, continue without it
		quantum = nil
	}

	llm, err := NewLLMClient(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to create LLM client: %w", err)
	}

	return &Infrastructure{
		pool:    pool,
		queries: queries,
		quantum: quantum,
		llm:     llm,
		metrics: NewMetricsCollector(queries),
	}, nil
}

// Queries returns the Neo4j queries interface
func (i *Infrastructure) Queries() *neo4j.Queries {
	return i.queries
}

// Quantum returns the quantum provider (may be nil)
func (i *Infrastructure) Quantum() *QuantumProvider {
	return i.quantum
}

// LLM returns the LLM client
func (i *Infrastructure) LLM() *LLMClient {
	return i.llm
}

// Metrics returns the metrics collector
func (i *Infrastructure) Metrics() *MetricsCollector {
	return i.metrics
}

// QuantumProvider provides quantum randomness from ANU QRNG
type QuantumProvider struct {
	pool       []byte
	poolMu     sync.Mutex
	poolSize   int
	lowWater   int
	lastFetch  time.Time
	minFetchMs int
	httpClient *http.Client
}

// NewQuantumProvider creates a new quantum provider
func NewQuantumProvider(ctx context.Context) (*QuantumProvider, error) {
	qp := &QuantumProvider{
		poolSize:   256,
		lowWater:   64,
		minFetchMs: 5000,
		httpClient: &http.Client{Timeout: 10 * time.Second},
	}

	// Initial pool fill
	if err := qp.refillPool(ctx); err != nil {
		return nil, err
	}

	return qp, nil
}

// GetFloat returns a quantum random float in [0, 1)
func (qp *QuantumProvider) GetFloat(ctx context.Context) (float64, string, error) {
	qp.poolMu.Lock()
	defer qp.poolMu.Unlock()

	// Refill if low
	if len(qp.pool) < qp.lowWater {
		go qp.refillPool(ctx)
	}

	if len(qp.pool) >= 8 {
		// Use 8 bytes to create a float
		bytes := qp.pool[:8]
		qp.pool = qp.pool[8:]

		// Convert to float64 in [0, 1)
		var value uint64
		for i := 0; i < 8; i++ {
			value = (value << 8) | uint64(bytes[i])
		}
		f := float64(value) / float64(1<<64)
		return f, "quantum", nil
	}

	// Fallback to classical
	return classicalRandom(), "classical", nil
}

// GetTemperatureDelta returns a quantum-modulated temperature delta
func (qp *QuantumProvider) GetTemperatureDelta(ctx context.Context, base, maxDelta float64) (float64, error) {
	f, _, err := qp.GetFloat(ctx)
	if err != nil {
		return base, err
	}
	// Map [0, 1) to [-maxDelta, +maxDelta]
	delta := (f - 0.5) * 2 * maxDelta
	return base + delta, nil
}

func (qp *QuantumProvider) refillPool(ctx context.Context) error {
	// Rate limit
	if time.Since(qp.lastFetch) < time.Duration(qp.minFetchMs)*time.Millisecond {
		return nil
	}

	url := fmt.Sprintf("https://qrng.anu.edu.au/API/jsonI.php?length=%d&type=uint8", qp.poolSize)
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return err
	}

	resp, err := qp.httpClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	var result struct {
		Data    []byte `json:"data"`
		Success bool   `json:"success"`
	}
	if err := json.Unmarshal(body, &result); err != nil {
		return err
	}

	if result.Success {
		qp.poolMu.Lock()
		qp.pool = append(qp.pool, result.Data...)
		qp.lastFetch = time.Now()
		qp.poolMu.Unlock()
	}

	return nil
}

func classicalRandom() float64 {
	// Use time-based pseudo-random as fallback
	return float64(time.Now().UnixNano()%1000000) / 1000000.0
}

// LLMClient provides LLM API access
type LLMClient struct {
	endpoint   string
	apiKey     string
	model      string
	httpClient *http.Client
	rateMu     sync.Mutex
	lastCall   time.Time
	minInterval time.Duration
}

// NewLLMClient creates a new LLM client
func NewLLMClient(ctx context.Context) (*LLMClient, error) {
	return &LLMClient{
		endpoint:    "https://open.bigmodel.cn/api/paas/v4/chat/completions",
		apiKey:      "", // Set from environment
		model:       "glm-4.7",
		httpClient:  &http.Client{Timeout: 60 * time.Second},
		minInterval: 8 * time.Second, // Rate limiting for Z.AI
	}, nil
}

// Generate generates text from a prompt
func (c *LLMClient) Generate(ctx context.Context, prompt string, opts types.GenerateOptions) (string, error) {
	// Rate limiting
	c.rateMu.Lock()
	if time.Since(c.lastCall) < c.minInterval {
		time.Sleep(c.minInterval - time.Since(c.lastCall))
	}
	c.lastCall = time.Now()
	c.rateMu.Unlock()

	// Build request
	model := c.model
	if opts.Model != "" {
		model = opts.Model
	}

	reqBody := map[string]interface{}{
		"model": model,
		"messages": []map[string]string{
			{"role": "user", "content": prompt},
		},
		"temperature": opts.Temperature,
		"max_tokens":  opts.MaxTokens,
	}

	bodyBytes, err := json.Marshal(reqBody)
	if err != nil {
		return "", err
	}

	req, err := http.NewRequestWithContext(ctx, "POST", c.endpoint,
		bytes.NewReader(bodyBytes))
	if err != nil {
		return "", err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+c.apiKey)

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var result struct {
		Choices []struct {
			Message struct {
				Content string `json:"content"`
			} `json:"message"`
		} `json:"choices"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}

	if len(result.Choices) > 0 {
		return result.Choices[0].Message.Content, nil
	}

	return "", fmt.Errorf("no response from LLM")
}

// MetricsCollector collects RSI metrics
type MetricsCollector struct {
	queries *neo4j.Queries
}

// NewMetricsCollector creates a new metrics collector
func NewMetricsCollector(queries *neo4j.Queries) *MetricsCollector {
	return &MetricsCollector{queries: queries}
}

// GetMetrics retrieves current RSI metrics
func (m *MetricsCollector) GetMetrics(ctx context.Context) (*types.RSIMetrics, error) {
	return m.queries.GetRSIMetrics(ctx)
}

// ValidatePhaseGate checks if Phase Gate criteria are met
func (m *MetricsCollector) ValidatePhaseGate(ctx context.Context) (bool, map[string]bool, error) {
	metrics, err := m.GetMetrics(ctx)
	if err != nil {
		return false, nil, err
	}

	criteria := map[string]bool{
		"H1_activation":    metrics.ActivationRate >= 0.50,
		"H6_transfer":      false, // Requires before/after comparison
		"H7_evolution":     false, // Requires baseline comparison
		"complete_cycles":  metrics.CompleteCycles >= 3,
	}

	allPassed := criteria["H1_activation"] && criteria["complete_cycles"]
	// H6 and H7 require additional state tracking

	return allPassed, criteria, nil
}
