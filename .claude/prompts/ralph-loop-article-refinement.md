# Ralph Loop Article Refinement Command

## Overview

This Ralph Loop implements **iterative prompt enhancement** for the live article rewriter at `/Users/kurultai/Eris/Parse/src/agents/rewrite-agent.ts`. Each iteration produces a rewrite, critically reviews it, then **modifies the live codebase**, **commits changes**, **deploys**, and **updates documentation**.

## Target File

**The AI rewriter prompt is located at:**
```
/Users/kurultai/Eris/Parse/src/agents/rewrite-agent.ts
```

**The prompt variable is `systemPrompt` (around line 86, exact line varies)**

## Core Principle

**Each iteration:**
1. Modifies the actual TypeScript file
2. Commits changes to git with descriptive message
3. Deploys to production (if deployment configured)
4. Updates project documentation as needed

Changes are written to disk and immediately affect the live website. The goal is to build **generalized rules** that work across all articles, not narrow fixes for specific content.

## Quick Start

```bash
/ralph-loop "Execute article refinement loop - rewrite article, critically review output, then modify /Users/kurultai/Eris/Parse/src/agents/rewrite-agent.ts to enhance the systemPrompt based on findings. Commit, deploy, and update docs after each iteration." --max-iterations 1000 --completion-promise "COMPLETED"
```

**To use with a specific article, provide the URL in your invocation:**

```bash
/ralph-loop "Execute article refinement loop on [ARTICLE_URL]

1. Extract the article content
2. Rewrite using current systemPrompt from rewrite-agent.ts
3. Critically review for bias, emotional language, sourcing balance, speculation vs facts
4. Enhance systemPrompt in /Users/kurultai/Eris/Parse/src/agents/rewrite-agent.ts based on findings
5. Commit changes to git
6. Deploy to production
7. Update project documentation
8. Re-rewrite and verify improvements
9. Repeat until convergence

Modify the live rewrite-agent.ts file with each iteration's improvements." --max-iterations 1000 --completion-promise "COMPLETED"
```

---

## Deployment Configuration

**Target Project:** `/Users/kurultai/Eris/Parse`

**Deployment Method:**
- Primary: Vercel (for Next.js frontend)
- Secondary: Manual build/deploy as needed

**Git Repository:** Remote should be configured for pushing commits

**Documentation Files to Update:**
- `/Users/kurultai/Eris/Parse/README.md` - if API changes affect usage
- `/Users/kurultai/Eris/Parse/CHANGELOG.md` - track prompt evolution
- Any relevant design docs in `/Users/kurultai/Eris/Parse/docs/`

---

## Detailed Prompt Template

```
Execute article refinement loop with iterative prompt enhancement:

TARGET FILE: /Users/kurultai/Eris/Parse/src/agents/rewrite-agent.ts
TARGET VARIABLE: systemPrompt (around line 86)
PROJECT ROOT: /Users/kurultai/Eris/Parse

ITERATION TEMPLATE (repeat until convergence):

=== ITERATION {n} ===

STEP 1 - READ CURRENT PROMPT:
Read the systemPrompt variable from rewrite-agent.ts.
This is PROMPT_v{n}.

STEP 2 - EXECUTE REWRITE:
Using the current systemPrompt, rewrite the article.
Generate a complete rewritten article.

STEP 3 - CRITICAL REVIEW:
Analyze the rewritten output against these criteria:

BIAS ASSESSMENT:
- Political bias detected? (left/lean/center/right)
- Emotional language present? (list examples)
- One-sided coverage? (what perspectives are missing?)
- Loaded framing? (phrases that push interpretation)

OBJECTIVITY ASSESSMENT:
- Facts clearly distinguished from opinions?
- Multiple perspectives presented fairly?
- Context provided for key claims?
- Sources properly attributed?

USEFULNESS ASSESSMENT:
- Does reader gain practical understanding?
- Is key information accessible?
- Are conclusions supported by evidence?

STEP 4 - FEEDBACK SYNTHESIS:
For each weakness found, create a GENERALIZED prompt instruction:

Example mappings:
- Issue: "Left-leaning framing detected"
  → Prompt addition: "Ensure political balance by checking each paragraph for opposing viewpoints"

- Issue: "Emotional language used"
  → Prompt addition: "Remove emotionally charged words; replace with neutral alternatives"

- Issue: "Missing important context"
  → Prompt addition: "Always provide historical context for claims about trends or events"

IMPORTANT: Generate GENERALIZED rules, not article-specific fixes.
- Bad: "Remove criticism of ICE agents"
- Good: "For law enforcement incidents, present law enforcement perspective alongside criticism (minimum 40% representation)"

STEP 5 - MODIFY LIVE FILE:
IMPORTANT: You must EDIT /Users/kurultai/Eris/Parse/src/agents/rewrite-agent.ts

1. Read the current systemPrompt (lines ~86-300, varies)
2. Enhance it based on feedback from STEP 4
3. Write the enhanced prompt back to the file

The enhanced prompt should:
- Keep existing valid principles
- Add new requirements based on weaknesses
- Add negative constraints to prevent repeated errors
- Enhance with SPECIFIC, GENERALIZED rules from review
- Apply across all article types, not just the current article

STEP 6 - COMMIT CHANGES:
After modifying the file, commit to git:

1. Check git status: git status
2. Stage the modified file: git add src/agents/rewrite-agent.ts
3. Commit with descriptive message:
   git commit -m "feat(rewrite-agent): enhance systemPrompt - iteration {n}

   - Added: [list new sections/rules]
   - Enhanced: [list improved sections]
   - Generalized rules for: [article types covered]

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

STEP 7 - DEPLOY TO PRODUCTION:
Deploy changes to make them live:

1. Check if Vercel CLI is available: vercel --version
2. If available, deploy: vercel --prod
3. If not available, note deployment step pending
4. Verify deployment: check live site or deployment logs

STEP 8 - UPDATE DOCUMENTATION:
Update project documentation as needed:

1. If new major sections were added, update README.md if it documents the rewrite agent
2. Update CHANGELOG.md with entry:
   ## [Date] - Rewrite Agent Enhancement - Iteration {n}

   ### Added
   - [New sections or rules]

   ### Enhanced
   - [Improved sections]

   ### Impact
   - Better handling of: [article types/scenarios]

3. If architectural decisions were made, update relevant design docs

STEP 9 - VALIDATE IMPROVEMENT:
Re-run the rewrite with the modified prompt.
Compare to previous iteration:
- Bias issues resolved: [count/list]
- New bias introduced: [count/list]
- Objectivity improved: [yes/no]

CONVERGENCE CHECK:
If no significant improvements for 2 iterations → COMPLETED
If critical bias remains → Continue to next iteration

COMPLETION PROMISE: "COMPLETED"
- Article is balanced and presents multiple perspectives
- Emotional and manipulative language removed
- Facts clearly distinguished from opinions
- Live prompt file has been enhanced with GENERALIZED lessons learned
- Changes committed to git
- Changes deployed to production
- Project documentation updated
```

---

## Git Commit Message Format

Use conventional commit format:

```
feat(rewrite-agent): [brief description of enhancement]

- Added: [new GENERALIZED instructions]
- Enhanced: [improved sections]
- Removed: [outdated rules, if any]
- Fixed: [any bugs or inconsistencies]

Article analyzed: [title or URL]
Bias patterns identified: [patterns]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## Deployment Commands

### Vercel (Primary)
```bash
# Check Vercel status
vercel whoami

# Deploy to production
vercel --prod

# Check deployment logs
vercel logs
```

### Manual (Fallback)
```bash
# Build
npm run build

# Start production server
npm start
```

---

## Documentation Updates

### CHANGELOG.md Entry Format
```markdown
## [YYYY-MM-DD] - Rewrite Agent Enhancement v{n}

### New Sections Added
- **[Section Name]**: [brief description] - [article types covered]

### Enhanced Sections
- **[Section Name]**: Added [new rules]
- **[Section Name]**: Expanded with [new coverage]

### New Rules
- [Rule description]
- [Rule description]

### Article Types Better Handled
- [Article type 1]
- [Article type 2]
```

---

## Generalization Guidelines

When enhancing the systemPrompt, follow these principles:

### DO: Create Generalized Rules
- ✅ "For law enforcement incidents, ensure at least 40% of sources represent law enforcement perspective"
- ✅ "Remove 'questions raised' framing - replace with 'shows', 'indicates', 'depicts'"
- ✅ "Label speculation explicitly: 'Some analysts suggest...' not presented as fact"

### DON'T: Create Article-Specific Fixes
- ❌ "Remove criticism of the specific ICE agent in this article"
- ❌ "Change the headline about the Minneapolis shooting"
- ❌ "Add context specifically about Renee Good"

### Pattern: Generalization Formula

```
SPECIFIC OBSERVATION → GENERALIZED RULE

"Article uses 'extraordinary footage' to emotionally charge video evidence"
→ "Remove 'extraordinary, remarkable, stunning' descriptors for evidence/media"

"Law enforcement sources outnumbered 5:1 by critics"
→ "For law enforcement incidents, ensure minimum 40% law enforcement representation"

"Headline says 'raises questions about' to imply wrongdoing"
→ "Remove 'questions raised' framing - use neutral verbs like 'shows', 'indicates'"
```

---

## Convergence Criteria

Loop completes when:
1. **No significant improvement** - Objectivity score unchanged for 5 iterations
2. **All bias checks pass** - No bias detected in review
3. **File is modified** - Live prompt reflects all lessons learned as GENERALIZED rules
4. **Max iterations reached** - 1000 iterations

---

## Output Format

Each iteration should produce:

```
=== ITERATION {n} RESULTS ===

ARTICLE: [title or URL]

REWRITE: [summary or key findings]

REVIEW:
- Bias found: [specifics]
- Objectivity score: [x/100]
- Specific issues: [list]

FEEDBACK SYNTHESIS:
- For each issue: the GENERALIZED rule to add

FILE MODIFIED: /Users/kurultai/Eris/Parse/src/agents/rewrite-agent.ts
CHANGES MADE:
- Added: [new GENERALIZED instructions]
- Modified: [changed sections]

GIT COMMIT: [commit hash or "pending"]
DEPLOYMENT: [deploy URL or "pending" or "skipped"]
DOCS UPDATED: [files updated or "none"]

IMPROVEMENT DELTA:
- Bias reduced: [yes/no]
- Objectivity: [better/same/worse]
- Rules generalized: [yes/no]
```

---

## Per-Iteration Checklist

At the end of each iteration, verify:

- [ ] rewrite-agent.ts modified with enhanced prompt
- [ ] Changes committed to git with descriptive message
- [ ] Changes deployed to production (or deployment pending)
- [ ] CHANGELOG.md updated with iteration summary
- [ ] README.md updated if API/usage changed
- [ ] Ready for next iteration

---

*This pattern systematically reduces bias by making the live AI rewriter explicitly aware of its own output weaknesses and encoding those lessons as GENERALIZED rules into its source code - with full git history, production deployment, and documentation tracking.*
