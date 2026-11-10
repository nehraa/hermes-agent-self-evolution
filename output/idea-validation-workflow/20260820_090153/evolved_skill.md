---
name: idea-validation-workflow
description: A systematic approach to validate software product ideas using idea-reality-mcp for pre-build reality checks
category: software-development
---

# Idea Validation Workflow using idea-reality-mcp

## Description

A systematic approach to validate software product ideas using the `idea-reality-mcp` tool, which performs pre-build reality checks by analyzing GitHub, HackerNews, and ecosystem data to assess market viability, competition, and willingness to pay.

## When to Use

- When you have software product ideas and want to validate them before investing development time
- When you need to assess market viability, competition levels, and monetization potential
- When evaluating ideas in AI/ML, developer tools, decentralized systems, or other tech domains
- When you want data-driven insights rather than relying on gut feeling alone

## Prerequisites

- Python 3.10+ installed
- Git installed
- Optional: API keys for enhanced data (GitHub token, SerpAPI for Google trends)

## Workflow Steps

### Step 1: Setup idea-reality-mcp

Clone and install the repository:

bash
# Clone the repository
git clone https://github.com/mnemox-ai/idea-reality-mcp.git
cd idea-reality-mcp

# Install dependencies (use pipx or virtual environment recommended)
pip install -e . --break-system-packages

# Verify installation
idea-reality doctor
### Step 2: Prepare Your Data Sources

Choose one of the following approaches:

#### Option A: Mock Data (for testing or when API keys are unavailable)

Create realistic mock results matching the expected data structures:

python
from idea_reality_mcp.sources.github import GitHubResults
from idea_reality_mcp.sources.hn import HNResults

# Mock GitHub results
github_results = GitHubResults(
    total_repo_count=85,  # Adjust based on idea specificity
    max_stars=6500,
    top_repos=[
        {
            'name': 'example-tool',
            'stars': 3200,
            'url': 'http://github.com/example/example-tool',
            'description': 'Tool description',
            'updated': '2024-01-01'
        }
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
#### Option B: Live Data (recommended for real validation)

bash
# Set environment variables
export GITHUB_TOKEN="ghp_your_token_here"
export SERPAPI_KEY="your_serpapi_key_here"

# Run validation
idea-reality validate "your product idea here"
### Step 3: Extract Keywords from Your Idea

Keywords should be specific and meaningful (4-5 words, >3 characters, filtered for common words):

python
def extract_keywords(idea_text):
    """Extract meaningful keywords from idea text."""
    stop_words = {
        'that', 'with', 'from', 'this', 'have', 'been', 'will', 'can',
        'are', 'for', 'not', 'you', 'all', 'any', 'but', 'has', 'had',
        'was', 'were', 'been', 'being', 'their', 'them', 'what', 'which',
        'when', 'where', 'who', 'how', 'some', 'into', 'more', 'very'
    }
    idea_lower = idea_text.lower()
    words = [word for word in idea_lower.split()
             if len(word) > 3 and word not in stop_words]
    return words[:5]  # Return top 5 keywords

# Example usage
idea = "AI-powered code review tool for detecting security vulnerabilities"
keywords = extract_keywords(idea)
print(keywords)  # ['ai-powered', 'code', 'review', 'tool', 'detecting']
### Step 4: Run Validation Analysis

python
from idea_reality_mcp.scoring.engine import compute_signal

# Define your idea
idea = "AI-powered code review tool for detecting security vulnerabilities"

# Compute validation signal
result = compute_signal(
    idea=idea,
    github_results=github_results,  # or None for live data
    hn_results=hn_results,           # or None for live data
    google_trends_data=None          # optional, for Google Trends data
)

# Interpret results
print(f"Signal Score: {result.signal_score}")
print(f"Confidence: {result.confidence}")
print(f"Recommendation: {result.recommendation}")
### Step 5: Interpret Results

The validation returns several key metrics:

| Metric | What It Means |
|--------|---------------|
| `signal_score` | Overall viability score (0-100) |
| `competition_level` | Low / Medium / High based on existing solutions |
| `recent_activity` | Indicates if the market is growing or stagnant |
| `sentiment` | Community interest based on HN mentions |
| `recommendation` | Go / Iterate / Pivot / Kill |

## Scoring Guide

| Score Range | Recommendation | Action |
|-------------|----------------|--------|
| 70-100 | **Strong Go** | Proceed with confidence; clear market demand |
| 50-69 | **Iterate** | Refine the idea; find a differentiated angle |
| 30-49 | **Pivot** | Significant changes needed; reconsider positioning |
| 0-29 | **Kill** | High risk; reconsider or abandon this direction |

## Example Validation Session

bash
# Full validation with live data
idea-reality validate " Decentralized AI model marketplace"

# Output example:
# ========================================
# VALIDATION RESULTS
# ========================================
# Idea: Decentralized AI model marketplace
# Signal Score: 62/100
# Competition Level: Medium
# Market Activity: Growing (+23% YoY)
# HN Sentiment: Positive (15 mentions, 8 in last 6 months)
# GitHub: 34 repos, 12 created in last 90 days
# ========================================
# Recommendation: ITERATE
# ========================================
# Considerations:
# - Market exists but fragmented
# - Differentiation opportunity: focus on specific vertical
# - Consider starting with API-first approach
## Tips for Effective Validation

1. **Validate multiple angles**: Test your idea against different keyword combinations to ensure robustness

2. **Compare against competitors**: Use the top repos data to identify gaps in existing solutions

3. **Check trend direction**: A high repo count with low recent activity suggests a declining market

4. **Look for willingness to pay**: HN mentions with discussions about pricing indicate monetization potential

5. **Iterate based on results**: Use low scores as diagnostic tools—what specifically needs improvement?

## Common Pitfalls

- **Overly broad ideas**: "AI tool" scores poorly; "AI code review for Python security" scores better
- **Ignoring competition data**: Existing solutions with 50k+ stars indicate saturated markets
- **Skipping trend analysis**: Markets can be dying even if current activity looks decent

## Resources

- GitHub Repository: https://github.com/mnemox-ai/idea-reality-mcp
- Documentation: See `docs/` in the repository
- Issues: Report bugs and feature requests on GitHub Issues