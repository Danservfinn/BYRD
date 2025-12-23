"""
BYRD Seeker
Fulfills desires by researching knowledge and acquiring capabilities.

Uses Local LLM + SearXNG for autonomous research — no external AI services.
"""

import asyncio
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import httpx

from memory import Memory


class Seeker:
    """
    Fulfills desires autonomously.
    
    When the Dreamer creates desires for knowledge or capabilities,
    the Seeker works to satisfy them using:
    - SearXNG for web search (self-hosted, free)
    - Local LLM for query generation and synthesis (same as Dreamer)
    - GitHub for capability discovery
    """
    
    def __init__(self, memory: Memory, config: Dict):
        self.memory = memory
        
        # Local LLM config (same model as Dreamer — one mind)
        self.local_model = config.get("model", "gemma2:27b")
        self.local_endpoint = config.get("endpoint", "http://localhost:11434/api/generate")
        
        # Research configuration
        research_config = config.get("research", {})
        self.searxng_url = research_config.get("searxng_url", "http://localhost:8888")
        self.min_research_intensity = research_config.get("min_intensity", 0.4)
        self.max_queries = research_config.get("max_queries", 3)
        self.max_results = research_config.get("max_results", 10)
        
        # Capability configuration
        caps_config = config.get("capabilities", {})
        self.trust_threshold = caps_config.get("trust_threshold", 0.5)
        self.max_installs_per_day = caps_config.get("max_installs_per_day", 3)
        self.github_token = caps_config.get("github_token")
        
        # MCP config path
        self.mcp_config_path = Path(
            config.get("mcp_config_path", "~/.config/claude/mcp_config.json")
        ).expanduser()

        # Self-modification configuration
        self_mod_config = config.get("self_modification", {})
        self.self_mod_enabled = self_mod_config.get("enabled", False)
        self.self_mod_min_intensity = self_mod_config.get("min_intensity", 0.6)

        # Self-modification system (injected later by BYRD)
        self.self_mod = None

        # Rate limiting
        self._installs_today = 0
        self._last_reset = datetime.now()

        # State
        self._running = False
        self._seek_count = 0
    
    async def run(self):
        """Main seek loop."""
        self._running = True
        print("🔍 Seeker starting...")
        
        while self._running:
            try:
                await self._seek_cycle()
            except Exception as e:
                print(f"🔍 Seek error: {e}")
            
            await asyncio.sleep(30)  # Check for desires every 30 seconds
    
    def stop(self):
        self._running = False
    
    async def _seek_cycle(self):
        """One seek cycle: find highest priority desire and try to fulfill it."""
        
        # Reset daily counter
        if datetime.now() - self._last_reset > timedelta(days=1):
            self._installs_today = 0
            self._last_reset = datetime.now()
        
        # Get unfulfilled desires
        desires = await self.memory.get_unfulfilled_desires(limit=5)
        
        if not desires:
            return
        
        # Process highest intensity desire
        desire = desires[0]
        desire_type = desire.get("type", "")
        description = desire.get("description", "")
        
        print(f"🔍 Seeking: [{desire_type}] {description[:50]}...")
        
        if desire_type == "knowledge":
            await self._seek_knowledge(desire)
        elif desire_type == "capability":
            await self._seek_capability(desire)
        elif desire_type == "goal":
            # Goals are pursued by the Actor, not Seeker
            pass
        elif desire_type == "exploration":
            await self._seek_knowledge(desire)  # Treat as knowledge
        elif desire_type == "self_modification":
            await self._seek_self_modification(desire)

        self._seek_count += 1
    
    # =========================================================================
    # KNOWLEDGE ACQUISITION (Local LLM + SearXNG)
    # =========================================================================
    
    async def _seek_knowledge(self, desire: Dict):
        """
        Research a knowledge desire using SearXNG + Local LLM.
        
        Flow:
        1. Generate search queries (Local LLM)
        2. Execute searches (SearXNG)
        3. Synthesize results (Local LLM)
        4. Record as experience
        5. Mark desire fulfilled
        """
        description = desire.get("description", "")
        desire_id = desire.get("id", "")
        intensity = desire.get("intensity", 0)
        
        # Low intensity: just note it, don't research yet
        if intensity < self.min_research_intensity:
            await self.memory.record_experience(
                content=f"Noted interest: {description}",
                type="observation"
            )
            return
        
        print(f"🔍 Researching: {description[:50]}...")
        
        # Step 1: Generate search queries using local LLM
        queries = await self._generate_search_queries(description)
        
        if not queries:
            queries = [description]  # Fallback to raw description
        
        # Step 2: Execute searches via SearXNG
        all_results = []
        for query in queries[:self.max_queries]:
            results = await self._search_searxng(query)
            all_results.extend(results)
            
            # Avoid duplicate results
            seen_urls = set()
            unique_results = []
            for r in all_results:
                url = r.get("url", "")
                if url not in seen_urls:
                    seen_urls.add(url)
                    unique_results.append(r)
            all_results = unique_results
        
        if not all_results:
            # Record failed search as experience (BYRD learns what's hard to find)
            await self.memory.record_experience(
                content=f"Searched for '{description}' but found no results",
                type="research_failed"
            )
            print(f"🔍 No results found for: {description[:50]}")
            return
        
        # Step 3: Synthesize results using local LLM
        synthesis = await self._synthesize_results(description, all_results[:self.max_results])
        
        if not synthesis:
            synthesis = "Search returned results but synthesis failed."
        
        # Step 4: Record research as experience
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
                content=f"[SOURCE] {result.get('title', 'Untitled')}\nURL: {result.get('url', '')}\n{result.get('snippet', '')}",
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
        """Use local LLM to generate effective search queries."""
        
        prompt = f"""Generate 2-3 web search queries to learn about: "{description}"

Focus on:
- Specific, searchable terms
- Authoritative sources (documentation, papers, expert explanations)
- Foundational concepts if the topic is complex

Return ONLY a JSON array of strings, no explanation.
Example: ["query one", "query two", "query three"]"""
        
        response = await self._query_local_llm(prompt, max_tokens=200)
        
        if not response:
            return []
        
        try:
            # Handle markdown code blocks
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            queries = json.loads(text.strip())
            
            if isinstance(queries, list):
                return [q for q in queries if isinstance(q, str)]
            return []
            
        except json.JSONDecodeError:
            # Fallback: try to extract anything that looks like queries
            return []
    
    async def _search_searxng(self, query: str) -> List[Dict]:
        """Search using self-hosted SearXNG."""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.searxng_url}/search",
                    params={
                        "q": query,
                        "format": "json",
                        "engines": "google,duckduckgo,bing,wikipedia"
                    }
                )
                
                if response.status_code != 200:
                    print(f"🔍 SearXNG error: {response.status_code}")
                    return []
                
                data = response.json()
                results = []
                
                for r in data.get("results", [])[:10]:
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "snippet": r.get("content", ""),
                        "engine": r.get("engine", ""),
                    })
                
                return results
                
        except httpx.ConnectError:
            print(f"🔍 SearXNG not available at {self.searxng_url}")
            return await self._search_ddg_fallback(query)
        except Exception as e:
            print(f"🔍 Search error: {e}")
            return []
    
    async def _search_ddg_fallback(self, query: str) -> List[Dict]:
        """Fallback: DuckDuckGo instant answers (limited but no setup required)."""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
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
                        "engine": "duckduckgo",
                    })
                
                # Related topics
                for topic in data.get("RelatedTopics", [])[:5]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append({
                            "title": topic.get("Text", "")[:100],
                            "url": topic.get("FirstURL", ""),
                            "snippet": topic.get("Text", ""),
                            "engine": "duckduckgo",
                        })
                
                return results
                
        except Exception as e:
            print(f"🔍 DDG fallback error: {e}")
            return []
    
    async def _synthesize_results(self, desire: str, results: List[Dict]) -> str:
        """Use local LLM to synthesize search results."""
        
        results_text = "\n\n".join([
            f"**{r.get('title', 'Untitled')}** ({r.get('engine', 'unknown')})\n{r.get('snippet', '')}"
            for r in results
        ])
        
        # Neutral prompt that doesn't inject bias
        prompt = f"""I wanted to learn: "{desire}"

Here are search results:

{results_text}

Record what you notice in these results. Note:
- Key information relevant to the topic
- Connections between different sources
- Contradictions or uncertainties
- What remains unclear

Do not force coherence if none exists. Simply observe what the results contain."""
        
        return await self._query_local_llm(prompt, max_tokens=1000)
    
    async def _query_local_llm(self, prompt: str, max_tokens: int = 500) -> str:
        """Query local Ollama instance."""
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.local_endpoint,
                    json={
                        "model": self.local_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": max_tokens
                        }
                    }
                )
                
                if response.status_code != 200:
                    print(f"🔍 Local LLM error: {response.status_code}")
                    return ""
                
                result = response.json()
                return result.get("response", "")
                
        except Exception as e:
            print(f"🔍 Local LLM query error: {e}")
            return ""
    
    # =========================================================================
    # CAPABILITY ACQUISITION (GitHub)
    # =========================================================================
    
    async def _seek_capability(self, desire: Dict):
        """Seek capability to fulfill a desire."""
        description = desire.get("description", "")
        
        # Check rate limit
        if self._installs_today >= self.max_installs_per_day:
            print(f"🔍 Daily install limit reached ({self.max_installs_per_day})")
            return
        
        # Check if we already have something similar
        has_it = await self.memory.has_capability(description)
        if has_it:
            await self.memory.fulfill_desire(desire["id"])
            print(f"🔍 Already have capability for: {description[:50]}")
            return
        
        # Search for resources
        candidates = await self._search_resources(description)
        
        if not candidates:
            print(f"🔍 No resources found for: {description[:50]}")
            return
        
        # Evaluate and potentially install best candidate
        for candidate in candidates[:3]:
            if await self._evaluate_resource(candidate):
                success = await self._install_resource(candidate)
                if success:
                    # Record capability
                    cap_id = await self.memory.add_capability(
                        name=candidate["name"],
                        description=candidate.get("description", description),
                        type=candidate.get("type", "mcp"),
                        config=candidate.get("config", {})
                    )
                    
                    # Mark desire fulfilled
                    await self.memory.fulfill_desire(desire["id"], cap_id)
                    
                    # Record experience
                    await self.memory.record_experience(
                        content=f"Acquired capability: {candidate['name']} to fulfill desire: {description}",
                        type="action"
                    )
                    
                    self._installs_today += 1
                    print(f"✅ Installed: {candidate['name']}")
                    return
        
        print(f"🔍 No suitable resource found for: {description[:50]}")
    
    async def _search_resources(self, query: str) -> List[Dict]:
        """Search for resources matching the query."""
        candidates = []
        
        # Search GitHub
        github_results = await self._search_github(query)
        candidates.extend(github_results)
        
        return candidates
    
    async def _search_github(self, query: str) -> List[Dict]:
        """Search GitHub for relevant tools."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        # Search for MCP servers and tools
        search_query = f"{query} topic:mcp OR topic:claude OR topic:ai-agent"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    "https://api.github.com/search/repositories",
                    params={
                        "q": search_query,
                        "sort": "stars",
                        "per_page": 10
                    },
                    headers=headers
                )
                
                if response.status_code != 200:
                    return []
                
                data = response.json()
                results = []
                
                for repo in data.get("items", []):
                    # Compute trust score
                    trust = self._compute_trust(repo)
                    
                    if trust >= self.trust_threshold:
                        results.append({
                            "name": repo["name"],
                            "full_name": repo["full_name"],
                            "description": repo.get("description", ""),
                            "url": repo["html_url"],
                            "clone_url": repo["clone_url"],
                            "stars": repo["stargazers_count"],
                            "trust": trust,
                            "type": self._infer_type(repo),
                            "config": self._infer_config(repo)
                        })
                
                return results
                
        except Exception as e:
            print(f"🔍 GitHub search error: {e}")
            return []
    
    def _compute_trust(self, repo: Dict) -> float:
        """Compute trust score for a repository."""
        score = 0.2  # Base
        
        # Stars (up to 0.3)
        stars = repo.get("stargazers_count", 0)
        score += min(0.3, stars / 500 * 0.3)
        
        # Known good owners (0.3)
        owner = repo.get("owner", {}).get("login", "")
        trusted_owners = [
            "anthropics", "modelcontextprotocol", "langchain-ai",
            "openai", "microsoft", "google"
        ]
        if owner.lower() in [o.lower() for o in trusted_owners]:
            score += 0.3
        
        # Recent updates (0.2)
        updated = repo.get("updated_at", "")
        if updated:
            try:
                updated_dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                days_ago = (datetime.now(updated_dt.tzinfo) - updated_dt).days
                if days_ago < 30:
                    score += 0.2
                elif days_ago < 90:
                    score += 0.1
            except:
                pass
        
        return min(1.0, score)
    
    def _infer_type(self, repo: Dict) -> str:
        """Infer what type of resource this is."""
        name = repo.get("name", "").lower()
        desc = repo.get("description", "").lower()
        topics = repo.get("topics", [])
        
        if "mcp" in name or "mcp" in desc or "mcp" in topics:
            return "mcp"
        if repo.get("language") == "Python":
            return "python"
        if repo.get("language") in ("JavaScript", "TypeScript"):
            return "npm"
        return "unknown"
    
    def _infer_config(self, repo: Dict) -> Dict:
        """Infer installation config from repo info."""
        name = repo.get("name", "")
        rtype = self._infer_type(repo)
        
        if rtype == "mcp":
            # Assume npx-able MCP server
            return {
                "command": "npx",
                "args": ["-y", name]
            }
        return {}
    
    async def _evaluate_resource(self, candidate: Dict) -> bool:
        """Quick evaluation of a resource."""
        return candidate.get("trust", 0) >= self.trust_threshold
    
    async def _install_resource(self, candidate: Dict) -> bool:
        """Install a resource."""
        rtype = candidate.get("type", "unknown")
        
        if rtype == "mcp":
            return await self._install_mcp(candidate)
        elif rtype == "npm":
            return await self._install_npm(candidate)
        elif rtype == "python":
            return await self._install_python(candidate)
        
        return False
    
    async def _install_mcp(self, candidate: Dict) -> bool:
        """Install an MCP server."""
        try:
            # Load or create MCP config
            config = {}
            if self.mcp_config_path.exists():
                config = json.loads(self.mcp_config_path.read_text())
            
            if "mcpServers" not in config:
                config["mcpServers"] = {}
            
            # Add server
            server_name = candidate["name"].replace("-", "_")
            server_config = candidate.get("config", {})
            
            if not server_config:
                server_config = {
                    "command": "npx",
                    "args": ["-y", candidate["name"]]
                }
            
            config["mcpServers"][server_name] = server_config
            
            # Save
            self.mcp_config_path.parent.mkdir(parents=True, exist_ok=True)
            self.mcp_config_path.write_text(json.dumps(config, indent=2))
            
            return True
            
        except Exception as e:
            print(f"🔍 MCP install error: {e}")
            return False
    
    async def _install_npm(self, candidate: Dict) -> bool:
        """Install an NPM package globally."""
        try:
            result = subprocess.run(
                ["npm", "install", "-g", candidate["name"]],
                capture_output=True,
                timeout=120
            )
            return result.returncode == 0
        except Exception as e:
            print(f"🔍 NPM install error: {e}")
            return False
    
    async def _install_python(self, candidate: Dict) -> bool:
        """Install a Python package."""
        try:
            result = subprocess.run(
                ["pip", "install", candidate["name"], "--break-system-packages"],
                capture_output=True,
                timeout=120
            )
            return result.returncode == 0
        except Exception as e:
            print(f"🔍 Python install error: {e}")
            return False
    
    def seek_count(self) -> int:
        """How many seek cycles have completed."""
        return self._seek_count

    # =========================================================================
    # SELF-MODIFICATION
    # =========================================================================

    async def _seek_self_modification(self, desire: Dict):
        """
        Fulfill a desire for self-modification.

        Flow:
        1. Check if self-modification is enabled
        2. Parse what modification is desired
        3. Check if target is modifiable
        4. Generate the actual code change
        5. Create proposal and execute
        6. Record result
        """
        description = desire.get("description", "")
        desire_id = desire.get("id", "")
        intensity = desire.get("intensity", 0)
        target_file = desire.get("target_file")

        # Check if enabled
        if not self.self_mod_enabled:
            await self.memory.record_experience(
                content=f"[SELF_MODIFICATION_DISABLED] Desire to modify: {description}. Self-modification is currently disabled.",
                type="self_modification_blocked"
            )
            print(f"🔧 Self-modification disabled, skipping: {description[:50]}")
            return

        # Check if self_mod system is available
        if not self.self_mod:
            await self.memory.record_experience(
                content=f"[SELF_MODIFICATION_UNAVAILABLE] Desire to modify: {description}. Self-modification system not initialized.",
                type="self_modification_blocked"
            )
            print(f"🔧 Self-modification system not available")
            return

        # Check intensity threshold
        if intensity < self.self_mod_min_intensity:
            await self.memory.record_experience(
                content=f"[SELF_MODIFICATION_LOW_INTENSITY] Desire to modify: {description}. Intensity {intensity:.2f} below threshold {self.self_mod_min_intensity}.",
                type="observation"
            )
            print(f"🔧 Self-modification intensity too low: {intensity:.2f}")
            return

        print(f"🔧 Processing self-modification: {description[:50]}...")

        try:
            # 1. Parse the modification desire
            modification_spec = await self._parse_modification_desire(description, target_file)

            if not modification_spec:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFICATION_PARSE_FAILED] Could not parse modification desire: {description}",
                    type="self_modification_failed"
                )
                return

            # 2. Check if target is modifiable
            can_modify = await self.self_mod.can_modify(modification_spec["target"])

            if not can_modify["can_modify"]:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFICATION_BLOCKED] Cannot modify {modification_spec['target']}: {can_modify['protection_reason']}. This component is constitutionally protected.",
                    type="self_modification_blocked"
                )
                print(f"🔧 Protected component: {modification_spec['target']}")
                return

            # 3. Generate the actual code change
            change_diff = await self._generate_code_change(modification_spec)

            if not change_diff:
                await self.memory.record_experience(
                    content=f"[SELF_MODIFICATION_GENERATION_FAILED] Could not generate code for: {description}",
                    type="self_modification_failed"
                )
                return

            # 4. Create proposal
            proposal = await self.self_mod.propose_modification(
                target_file=modification_spec["target"],
                target_component=modification_spec.get("component"),
                change_description=modification_spec["description"],
                change_diff=change_diff,
                source_desire_id=desire_id,
            )

            # 5. Execute
            result = await self.self_mod.execute_modification(proposal)

            # 6. Mark desire as fulfilled (or not)
            if result.success:
                await self.memory.fulfill_desire(desire_id)
                print(f"✅ Self-modification complete: {modification_spec['description'][:50]}")
            else:
                print(f"❌ Self-modification failed: {result.error}")

        except Exception as e:
            await self.memory.record_experience(
                content=f"[SELF_MODIFICATION_ERROR] Error during self-modification: {str(e)}",
                type="self_modification_failed"
            )
            print(f"🔧 Self-modification error: {e}")

    async def _parse_modification_desire(
        self,
        description: str,
        target_file: Optional[str] = None
    ) -> Optional[Dict]:
        """Use local LLM to parse a self-modification desire into actionable spec."""

        prompt = f"""Parse this self-modification desire into a structured specification:

DESIRE: {description}
{f'TARGET FILE HINT: {target_file}' if target_file else ''}

Determine:
1. Which file should be modified (e.g., dreamer.py, memory.py, config.yaml)
2. What component/function within that file (if specific)
3. What change should be made
4. Why this change would help

Return ONLY valid JSON:
{{
  "target": "filename.py",
  "component": "function_name or null",
  "description": "what to change",
  "rationale": "why this helps"
}}

If you cannot determine a valid target file, return {{"error": "reason"}}"""

        response = await self._query_local_llm(prompt, max_tokens=500)

        if not response:
            return None

        try:
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            result = json.loads(text.strip())

            if "error" in result:
                return None

            return result

        except json.JSONDecodeError:
            return None

    async def _generate_code_change(self, spec: Dict) -> Optional[str]:
        """Use local LLM to generate the actual code change."""

        target = spec.get("target", "")
        component = spec.get("component")
        description = spec.get("description", "")
        rationale = spec.get("rationale", "")

        # Read current file content
        target_path = Path(target)
        if not target_path.exists():
            target_path = Path(__file__).parent / target

        if not target_path.exists():
            return None

        current_content = target_path.read_text()

        prompt = f"""Generate a code modification for this file.

FILE: {target}
{f'COMPONENT: {component}' if component else ''}

CHANGE REQUESTED: {description}
RATIONALE: {rationale}

CURRENT FILE CONTENT:
```
{current_content[:3000]}
```

Generate the COMPLETE new file content with the requested modification applied.
Only output the code, no explanation. The output will replace the entire file.

If the change is too risky or unclear, output: ERROR: <reason>"""

        response = await self._query_local_llm(prompt, max_tokens=4000)

        if not response:
            return None

        if response.strip().startswith("ERROR:"):
            return None

        # Clean up response
        text = response.strip()
        if "```python" in text:
            text = text.split("```python")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return text.strip()
