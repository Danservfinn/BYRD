# Knowledge Acquisition Loop

## Completing the Research → Dream Cycle

This document specifies the missing implementation that allows BYRD to:
1. Develop emergent desires for knowledge
2. Research those topics autonomously
3. Feed research results back into dreaming
4. Form beliefs from what it learns

---

## Implementation

### 1. Enhanced Seeker for Knowledge Acquisition

```python
# seeker.py additions

class Seeker:
    """Enhanced Seeker with real web search capability."""
    
    def __init__(self, memory: Memory, actor: Actor, config: Dict):
        self.memory = memory
        self.actor = actor  # Now takes Actor for search capability
        # ... existing init ...
    
    async def _seek_knowledge(self, desire: Dict):
        """
        Fulfill a knowledge desire through web research.
        Results become experiences that feed back into dreaming.
        """
        description = desire.get("description", "")
        desire_id = desire.get("id", "")
        intensity = desire.get("intensity", 0)
        
        # Low intensity: just note it, don't research yet
        if intensity < 0.4:
            await self.memory.record_experience(
                content=f"Noted interest: {description}",
                type="observation"
            )
            return
        
        print(f"🔍 Researching: {description[:50]}...")
        
        # Step 1: Generate search queries from the desire
        queries = await self._generate_search_queries(description)
        
        # Step 2: Execute searches
        all_results = []
        for query in queries[:3]:  # Limit to 3 queries per desire
            results = await self._web_search(query)
            all_results.extend(results)
        
        if not all_results:
            # Record failed search as experience (BYRD learns what's hard to find)
            await self.memory.record_experience(
                content=f"Searched for '{description}' but found no results",
                type="research_failed"
            )
            return
        
        # Step 3: Synthesize results into coherent knowledge
        synthesis = await self._synthesize_results(description, all_results)
        
        # Step 4: Record as experience (THIS IS THE KEY STEP)
        exp_id = await self.memory.record_experience(
            content=f"[RESEARCH] {description}\n\nFindings:\n{synthesis}",
            type="research"
        )
        
        # Step 5: Link experience to the desire that triggered it
        await self.memory.create_connection(
            from_id=exp_id,
            to_id=desire_id,
            relationship="FULFILLS"
        )
        
        # Step 6: Record individual sources as sub-experiences
        for result in all_results[:5]:
            source_exp_id = await self.memory.record_experience(
                content=f"[SOURCE] {result.get('title', 'Untitled')}\n{result.get('snippet', '')}",
                type="research_source"
            )
            await self.memory.create_connection(
                from_id=source_exp_id,
                to_id=exp_id,
                relationship="SUPPORTS"
            )
        
        # Step 7: Mark desire as fulfilled
        await self.memory.fulfill_desire(desire_id)
        
        print(f"✅ Research complete: {description[:50]}")
    
    async def _generate_search_queries(self, description: str) -> List[str]:
        """Use Actor to generate effective search queries from desire description."""
        
        prompt = f"""Given this knowledge desire: "{description}"

Generate 2-3 specific web search queries that would help fulfill this desire.
Return as JSON array of strings.

Focus on:
- Authoritative sources (papers, documentation, expert explanations)
- Foundational concepts if the topic is complex
- Recent information if the topic evolves

Return ONLY the JSON array, no explanation."""
        
        response = await self.actor.client.messages.create(
            model=self.actor.model,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            text = response.content[0].text
            if "```" in text:
                text = text.split("```")[1].replace("json", "").strip()
            return json.loads(text)
        except:
            # Fallback: use description directly
            return [description]
    
    async def _web_search(self, query: str) -> List[Dict]:
        """
        Execute web search. 
        
        Options:
        1. Use Claude's web search tool (if available)
        2. Use SerpAPI, Brave Search API, or similar
        3. Use DuckDuckGo HTML scraping (free but fragile)
        """
        
        # Option 1: Brave Search API (recommended - good quality, affordable)
        if self.brave_api_key:
            return await self._brave_search(query)
        
        # Option 2: SerpAPI 
        if self.serp_api_key:
            return await self._serp_search(query)
        
        # Option 3: DuckDuckGo fallback (no API key needed)
        return await self._ddg_search(query)
    
    async def _brave_search(self, query: str) -> List[Dict]:
        """Search using Brave Search API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": self.brave_api_key},
                params={"q": query, "count": 10}
            )
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            results = []
            
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", ""),
                })
            
            return results
    
    async def _ddg_search(self, query: str) -> List[Dict]:
        """Fallback: DuckDuckGo instant answers (limited but free)."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1}
            )
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            results = []
            
            # Abstract (main result)
            if data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", query),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("Abstract", ""),
                })
            
            # Related topics
            for topic in data.get("RelatedTopics", [])[:5]:
                if isinstance(topic, dict) and topic.get("Text"):
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "url": topic.get("FirstURL", ""),
                        "snippet": topic.get("Text", ""),
                    })
            
            return results
    
    async def _synthesize_results(self, desire: str, results: List[Dict]) -> str:
        """Use Actor to synthesize search results into coherent knowledge."""
        
        results_text = "\n\n".join([
            f"**{r.get('title', 'Untitled')}**\n{r.get('snippet', '')}"
            for r in results[:10]
        ])
        
        prompt = f"""I wanted to learn: "{desire}"

Here are search results I found:

{results_text}

Synthesize these into a coherent understanding. Focus on:
1. Key concepts and how they relate
2. What I now understand that I didn't before
3. What remains unclear or warrants further investigation

Write as if recording what you've learned, not as a report for someone else."""
        
        response = await self.actor.client.messages.create(
            model=self.actor.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
```

### 2. Memory Schema Additions

```cypher
// New relationship: Experience FULFILLS Desire
// (already exists, but now used for knowledge, not just capabilities)

// New experience types
// type: "research" - synthesized research findings
// type: "research_source" - individual sources
// type: "research_failed" - searches that found nothing

// Query: What has BYRD researched?
MATCH (e:Experience {type: 'research'})-[:FULFILLS]->(d:Desire)
RETURN e.content, d.description, e.timestamp
ORDER BY e.timestamp DESC
```

### 3. Dreamer Integration

The Dreamer already picks up recent experiences. With research experiences now recorded, they naturally flow into dreaming:

```python
# In dreamer.py - no changes needed, but here's what happens:

async def _dream_cycle(self):
    # 1. Recall recent experiences (now includes research)
    recent = await self.memory.get_recent_experiences(limit=50)
    # recent now contains:
    # - User interactions
    # - Actions taken
    # - Research findings  <-- NEW
    # - Research sources   <-- NEW
    # - Failed searches    <-- NEW
    
    # 2. Reflect on them
    # The LLM sees research results and can:
    # - Form beliefs from what was learned
    # - Notice new gaps (triggering new knowledge desires)
    # - Connect research to other experiences
    
    dream_output = await self._reflect(recent, related, desires, capabilities)
    
    # 3. Record outputs
    # New beliefs may be DERIVED_FROM research experiences
    # New desires may emerge from partial understanding
```

### 4. Example Flow

```
Time T0: BYRD dreams
├── Reflects on conversation about neural networks
├── Notices: "I referenced 'attention mechanisms' but don't understand them"
└── Creates: Desire(type="knowledge", 
                    description="How attention mechanisms work in transformers",
                    intensity=0.75)

Time T1: Seeker runs
├── Picks up knowledge desire (intensity > 0.4)
├── Generates queries:
│   ├── "attention mechanism transformer explained"
│   ├── "self-attention neural networks"
│   └── "transformer architecture attention heads"
├── Searches Brave API
├── Gets results from papers, blogs, documentation
├── Synthesizes: "Attention allows the model to weigh different parts..."
└── Records as Experience(type="research", content="[RESEARCH] How attention...")

Time T2: BYRD dreams again
├── Recalls recent experiences including research
├── Reflects: "Now I understand that attention is a weighted combination..."
├── Forms: Belief("Attention mechanisms compute relevance between all positions",
│                 confidence=0.7,
│                 derived_from=[research_experience_id])
├── Notices new gap: "But how does multi-head attention differ?"
└── Creates: Desire(type="knowledge",
                    description="Multi-head attention vs single-head",
                    intensity=0.6)

Time T3: Seeker runs again...
```

### 5. Configuration

```yaml
# config.yaml additions

seeker:
  knowledge_acquisition:
    enabled: true
    min_intensity_to_research: 0.4
    max_queries_per_desire: 3
    max_results_to_synthesize: 10
    
  search_providers:
    # Brave Search (recommended)
    brave_api_key: "${BRAVE_API_KEY}"
    
    # Fallback: SerpAPI
    serp_api_key: "${SERP_API_KEY}"
    
    # Ultimate fallback: DuckDuckGo (no key needed, limited)
    use_ddg_fallback: true
```

### 6. Emergence Compliance Check

| Aspect | Assessment |
|--------|------------|
| Does research inject interests? | ❌ No — BYRD chooses what to research based on emergent desires |
| Does synthesis inject values? | ⚠️ Minor risk — synthesis prompt asks for "understanding", could bias |
| Are sources chosen externally? | ❌ No — search queries derived from BYRD's own desire description |
| Does this create feedback loops? | ⚠️ Yes — learning leads to more questions, but this is natural |

**Mitigation for synthesis prompt**: Make it more neutral:

```python
# Instead of:
"Synthesize these into a coherent understanding"

# Use:
"Record what you notice in these results. Note connections, contradictions, 
and anything that remains unclear. Do not force coherence if none exists."
```

---

## What This Enables

With this implementation, BYRD can:

1. **Autonomously research** — No human needs to tell it what to look up
2. **Learn from the web** — Real information, not just LLM confabulation
3. **Build knowledge over time** — Research becomes experiences becomes beliefs
4. **Develop deeper interests** — Learning about X reveals Y, creating new desires
5. **Know what it doesn't know** — Failed searches become experiences too

This is a significant step toward genuine autonomous learning, while preserving emergence: BYRD decides what matters, the architecture just enables acting on those decisions.

---

## Implementation Priority

This should be implemented in **Phase 1** because:
- It's core to BYRD's ability to grow autonomously
- Without it, knowledge desires just accumulate unfulfilled
- It demonstrates the full dream → desire → action → experience → dream loop

Estimated effort: 2-3 days for Seeker enhancements + search integration.
