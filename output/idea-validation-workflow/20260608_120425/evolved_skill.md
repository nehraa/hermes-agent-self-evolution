---
name: idea-validation-workflow
description: A systematic approach to validate software product ideas using idea-reality-mcp for pre-build reality checks
category: software-development
---

# Idea Validation Workflow

A systematic approach to validate software product ideas before committing development resources. This workflow uses `idea-reality-mcp` to perform pre-build reality checks by analyzing GitHub, HackerNews, and ecosystem data—providing data-driven insights into market viability, competition, and monetization potential.

## When to Use This Workflow

- **Pre-development validation** — Before investing time or resources into a new product idea
- **Market assessment** — When you need objective data on competition levels and market saturation
- **Opportunity discovery** — When exploring ideas in AI/ML, developer tools, decentralized systems, or other technical domains
- **Investment decisions** — When deciding which ideas to prioritize or deprioritize
- **Thesis validation** — When you have a gut feeling and want to validate it with real data

## Prerequisites

- Python 3.10+
- Git
- pip or pipx for dependency management
- (Optional) API keys for GitHub and HackerNews data enrichment

## Workflow Steps

### Step 1: Install idea-reality-mcp

bash
# Clone the repository
git clone https://github.com/mnemox-ai/idea-reality-mcp.git
cd idea-reality-mcp

# Install in development mode (use pipx or virtualenv recommended)
pip install -e . --break-system-packages

# Verify installation
idea-reality doctor
The `doctor` command validates your environment and reports any missing dependencies.

### Step 2: Configure Data Sources

The tool supports real API connections and mock data for testing:

**Option A: Use Real API Keys (Recommended)**

bash
export GITHUB_TOKEN="ghp_your_token_here"
export HN_API_KEY="your_hn_key"  # if applicable
**Option B: Use Mock Data (for testing without API keys)**

Create realistic mock data matching expected structures:

python
from idea_reality_mcp.sources.github import GitHubResults
from idea_reality_mcp.sources.hn import HNResults

# Mock GitHub results
github_results = GitHubResults(
    total_repo_count=85,
    max_stars=6500,
    top_repos=[
        {
            'name': 'example-tool',
            'stars': 3200,
            'url': 'https://github.com/example/example-tool',
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
### Step 3: Define and Analyze Your Idea

Extract meaningful keywords from your idea and run validation:

python
from idea_reality_mcp.scoring.engine import compute_signal

def extract_keywords(idea_text):
    """Extract 4-5 meaningful keywords from idea text."""
    stop_words = {
        'that', 'with', 'from', 'this', 'have', 'been', 'will',
        'can', 'are', 'for', 'not', 'you', 'all', 'any', 'but',
        'has', 'had', 'was', 'were', 'be', 'being', 'been',
        'your', 'what', 'about', 'which', 'when', 'make', 'like',
        'time', 'just', 'know', 'take', 'people', 'into', 'year'
    }
    words = [
        word for word in idea_text.lower().split()
        if len(word) > 3 and word not in stop_words
    ]
    return words[:5]  # Return top 5 keywords

# Example usage
idea_text = "AI-powered code review assistant for development teams"
keywords = extract_keywords(idea_text)
print(f"Keywords: {keywords}")
### Step 4: Compute Validation Signal

Run the scoring engine to generate a market viability report:

python
from idea_reality_mcp.scoring.engine import compute_signal
from idea_reality_mcp.sources.github import GitHubResults
from idea_reality_mcp.sources.hn import HNResults

# Prepare your data sources
github_results = GitHubResults(
    total_repo_count=85,
    max_stars=6500,
    top_repos=[...],
    recent_created_count=25,
    recent_ratio=0.3
)

hn_results = HNResults(
    total_mentions=42,
    evidence=[],
    recent_mention_ratio=0.35
)

# Compute signal
result = compute_signal(
    keywords=["ai", "code", "review", "assistant"],
    github=github_results,
    hn=hn_results
)

print(f"Signal Score: {result.signal_score}")
print(f"Market Indicators: {result.indicators}")
print(f"Recommendations: {result.recommendations}")
### Step 5: Interpret Results

The output provides:

| Signal Score | Interpretation | Action |
|--------------|----------------|--------|
| 0.0 - 0.3 | Weak signal — low market interest | Consider pivoting or abandoning |
| 0.3 - 0.6 | Moderate signal — some market activity | Validate further, assess differentiation |
| 0.6 - 1.0 | Strong signal — active market | Proceed with confidence, focus on differentiation |

Key indicators to examine:

- **Repo count** — How many similar solutions exist?
- **Max stars** — What's the ceiling for market leaders?
- **Recent ratio** — Is the market growing or stagnating?
- **HN mentions** — Is there active discussion and interest?
- **Competition landscape** — Direct vs. indirect competitors

### Step 6: Make Decisions

Use validation results to guide your next steps:

**High Signal Ideas:**
- Proceed to detailed planning
- Identify unique differentiators
- Plan MVP scope

**Moderate Signal Ideas:**
- Investigate niche opportunities
- Research specific pain points not addressed by competitors
- Consider adjacent markets

**Low Signal Ideas:**
- Abandon or radically pivot
- Reconsider target audience
- Validate problem statement with potential users

## CLI Usage

For quick validation via command line:

bash
# Validate an idea
idea-reality validate "AI code review for teams"

# Generate full report
idea-reality analyze --idea "decentralized note taking app" --format json

# Check specific market
idea-reality market-check --keywords "code generation" "AI" "developer tools"
## Best Practices

1. **Test multiple idea variants** — Run validation on several close ideas to find the most viable option
2. **Use specific keywords** — More specific keywords yield more accurate results than vague ones
3. **Check trend direction** — Compare recent_ratio against historical data if available
4. **Combine with user research** — Data analysis complements, not replaces, talking to potential users
5. **Re-validate periodically** — Markets change; re-run validation before major investments

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: idea-reality` | Re-run pip install with --break-system-packages or use virtual environment |
| `Authentication error` | Verify GitHub token has correct permissions |
| `Rate limit exceeded` | Wait or use mock data mode |
| `No results found` | Broaden keywords or check spelling |

## Example Output Structure

json
{
  "signal_score": 0.72,
  "market_indicators": {
    "github_repos": 85,
    "max_stars": 6500,
    "hn_mentions": 42,
    "recent_growth": 0.35
  },
  "recommendations": [
    "Market shows active interest with moderate competition",
    "Opportunity exists in differentiation",
    "Focus on specific use case rather than broad tool"
  ],
  "keywords_analyzed": ["ai", "code", "review", "assistant"]
}
---

This workflow transforms "gut feeling" decisions into data-driven validation, helping you focus development resources on ideas with real market potential.