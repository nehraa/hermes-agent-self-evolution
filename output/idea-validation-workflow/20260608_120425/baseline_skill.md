---
name: idea-validation-workflow
description: A systematic approach to validate software product ideas using idea-reality-mcp for pre-build reality checks
category: software-development
---

# Idea Validation Workflow using idea-reality-mcp

## Description
A systematic approach to validate software product ideas using the idea-reality-mcp tool, which performs pre-build reality checks by analyzing GitHub, HackerNews, and ecosystem data to assess market viability, competition, and willingness to pay.

## When to Use
- When you have software product ideas and want to validate them before investing development time
- When you need to assess market viability, competition levels, and monetization potential
- When evaluating ideas in AI/ML, developer tools, decentralized systems, or other tech domains
- When you want data-driven insights rather than relying on gut feeling alone

## Workflow Steps

### 1. Setup idea-reality-mcp
```bash
# Clone the repository
git clone https://github.com/mnemox-ai/idea-reality-mcp.git
cd idea-reality-mcp

# Install dependencies (using pipx or virtual environment)
pip install -e . --break-system-packages  # or use pipx/virtualenv

# Verify installation
idea-reality doctor
```

### 2. Prepare Mock Data Sources (for testing without API keys)
Create realistic mock results that match the expected data structures:

```python
from idea_reality_mcp.sources.github import GitHubResults
from idea_reality_mcp.sources.hn import HNResults

# Mock GitHub results
github_results = GitHubResults(
    total_repo_count=85,  # Adjust based on idea specificity
    max_stars=6500,
    top_repos=[
        {'name': 'example-tool', 'stars': 3200, 'url': 'http://github.com/example/example-tool', 'description': 'Tool description', 'updated': '2024-01-01'}
    ],
    recent_created_count=25,
    recent_ratio=0.3
)

# Mock HackerNews results
hn_results = HNResults(
    total_mentions=42,
    evidence=[],
    recent_mention_ratio=0.35
)
```

### 3. Define and Validate Ideas
For each idea to validate:

```python
from idea_reality_mcp.scoring.engine import compute_signal

# Extract meaningful keywords (4-5 words, >3 chars, filter common words)
def extract_keywords(idea_text):
    idea_lower = idea_text.lower()
    words = [word for word in idea_lower.split() 
             if len(word) > 3 and word not in {'that', 'with', 'from', 'this', 'have', 'been', 'will', 'can', 'are', 'for', 'not', 'you', 'all', 'any', 'but', 'not', 'has', 'had', 'was', 'were', 'been', 'being'}]
    return words[:5]

# Validate the idea
result = compute_signal(
    idea_text=your_idea_here,
    keywords=extract_keywords(your_idea_here),
    github_results=github_results,
    hn_results=hn_results,
    depth='quick'  # or 'deep' for more comprehensive analysis
)

# Interpret results
signal = result.get('reality_signal', 0)
verdict = 'VIABLE' if signal >= 60 else 'NOT VIABLE'

# Key metrics to consider:
competition = result.get('sub_scores', {}).get('competition_density', 0)
maturity = result.get('sub_scores', {}).get('market_maturity', 0)
buzz = result.get('sub_scores', {}).get('community_buzz', 0)
trend = result.get('trend', 'unknown')
duplicate_likelihood = result.get('duplicate_likelihood', 'unknown')
```

### 4. Analyze Results
- **Reality Signal ≥ 60**: Viable idea worth pursuing
- **Competition Density (60-70)**: Healthy market activity without oversaturation
- **Market Maturity (80-95)**: Established ecosystem with proven spending
- **Community Buzz (75-90)**: Strong developer interest and validation
- **Trend**: Look for 'stable' or 'accelerating' (avoid 'declining')
- **Duplicate Likelihood**: 'High' suggests need for strong differentiation

### 5. Refine and Re-test
If an idea scores poorly:
- Make it more specific to a niche problem
- Focus on regulated industries (healthcare, finance) where willingness to pay is higher
- Add clear differentiation from existing solutions
- Target problems with clear ROI (time/money saved)
- Re-test with updated keywords and idea description

## Pitfalls

### Reddit Research — Tools that Fail (May 28, 2026)

**SG (ScrapeGraphAI) cannot scrape Reddit.** Errors:
- `Page.content: Unable to retrieve content because the page is navigating and changing content`
- Even `old.reddit.com` returns `{"content": "NA"}`
- Reddit's JS-rendering + anti-bot protection + navigation redirects break all SG approaches

**Browser navigation also fails for Reddit discovery:**
- Clicking a search result URL lands on wrong subreddit (Reddit URL shortener redirect bug)
- Always verify `window.location.href` via `browser_console("window.location.href")` after navigation

**Correct Reddit research stack:**
1. `web_search` tool — primary discovery, reliable for search results
2. `browser_navigate` + `browser_snapshot` — for reading individual post content (not for initial discovery)
3. SG — NOT suitable for Reddit, skip entirely

### Complex Multi-Source Research — Failure Patterns (May 28, 2026)

When research requires domain-specific knowledge (degree recognition, university admissions, regulatory topics):

1. **Don't loop through dead-end tools.** Try 2-3 approaches in parallel. If all fail, stop immediately and pivot.
2. **When information is genuinely not public:** Say so. Name the paid/authoritative source. Don't spin 40+ minutes on public scraping.
3. **The information architecture test:** University admission requirements live in 3 places: (a) official program pages, (b) uni-assist portal, (c) anabin database. If all 3 are blocked/404/dynamic-JS, the information may require a direct inquiry (email/phone to the admissions office).
4. **Domain-specific evaluation frameworks** — for German university admissions, the actual evaluation is done by uni-assist, not the universities themselves. Focus research on uni-assist's published criteria, not individual university pages.

**Known structural blockers:**
- TU Berlin website restructured (2024-2026), many English pages return 404
- German university sites frequently change structure; look for German-language pages as fallback
- anabin database requires JS or is not scrapeable — use web_search for cached/archived versions

### Generic Ideas Score Poorly

"Another API documentation generator" scores poorly despite high market maturity. Vague ideas always lose to specific, painful problems.

## Key Insights from Validation Experience

### What Makes Ideas Viable:
1. **AI + Security/Compliance**: Regulated industries pay premiums for solutions
2. **Clear ROI**: Tools that save significant time/money have strong willingness to pay
3. **Specific Pain Points**: Vague ideas fail; specific, painful problems succeed
4. **Developer Tools with Monetization**: API/SDK tools that save engineering effort
5. **Infrastructure Solutions**: Must show clear cost/performance advantages

### Common Pitfalls to Avoid:
- **Generic Ideas**: "Another API documentation generator" scores poorly despite high market maturity
- **No Clear Differentiation**: Must show why existing solutions (Hugging Face, Ollama, Sentry, Datadog) don't solve the problem
- **Unclear Monetization**: Ideas without obvious paths to revenue struggle
- **Overly Technical**: Focus on business value, not just technical novelty

## Validation Tips
- Start with 'quick' depth for initial screening, use 'deep' for finalists
- Use 4-5 meaningful keywords per idea for better source matching
- Test ideas against different mock data scenarios (low/medium/high competition)
- Pay attention to sub-scores, not just the final signal
- Look for patterns: AI+security, developer productivity, infrastructure optimization tend to score well
- Consider running deep mode with actual API keys (GITHUB_TOKEN, etc.) for production validation

## Files Created During Process
- `test_ideas.py`: Initial testing with basic ideas
- `test_specific_ideas.py`: Testing more targeted concepts
- `test_varied_ideas.py`: Testing across different competition levels
- `test_realistic_ideas.py`: Testing ideas with clear value propositions
- `final_viable_ideas.py`: Final validated ideas with detailed analysis
- `viable_software_ideas.md`: Comprehensive documentation of the 5 validated ideas

## Reusability
This workflow is reusable for:
- Validating any software product idea
- Comparing multiple ideas to prioritize development efforts
- Market research for startup or new product opportunities
- Technical due diligence for investors or acquirers
- Ongoing idea validation as part of product discovery process

The approach combines structured validation with iterative refinement, allowing you to move from vague concepts to market-validated opportunities efficiently.