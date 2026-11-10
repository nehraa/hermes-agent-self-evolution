---
name: idea-validation-workflow
description: A systematic approach to validate software product ideas using idea-reality-mcp for pre-build reality checks
category: software-development
---

# Idea Validation Workflow using idea-reality-mcp

A systematic approach to validate software product ideas before committing development resources. The `idea-reality-mcp` tool performs pre-build reality checks by analyzing GitHub repository data, HackerNews discussions, and ecosystem signals to assess market viability, competition intensity, and monetization potential.

## When to Use

- Validate a software product idea before investing development time
- Assess market viability, competition levels, and monetization potential
- Evaluate ideas in AI/ML, developer tools, decentralized systems, or other tech domains
- Get data-driven insights rather than relying on intuition alone
- Compare multiple competing ideas to prioritize development efforts

## Prerequisites

- Python 3.10 or higher
- Git installed
- Optional: API keys for GitHub and HackerNews (can use mock data for testing)

## Setup

### 1. Install idea-reality-mcp

bash
# Clone the repository
git clone https://github.com/mnemox-ai/idea-reality-mcp.git
cd idea-reality-mcp

# Install dependencies
pip install -e . --break-system-packages

# Or use pipx for isolation
pipx install -e .

# Verify installation
idea-reality doctor
### 2. Configure API Keys (Optional)

For production use with real data:

bash
# Set environment variables
export GITHUB_TOKEN="ghp_your_github_token_here"
export HN_API_KEY="your_hackernews_api_key_here"

# Verify configuration
idea-reality doctor
## Workflow Steps

### Step 1: Prepare Input Data

Define your idea and extract relevant keywords for searching:

python
from idea_reality_mcp.sources.github import GitHubResults
from idea_reality_mcp.sources.hn import HNResults

# Define your product idea
idea_text = "AI-powered code review assistant for catching security vulnerabilities"

# Extract meaningful keywords (4-5 words, >3 chars, filter stopwords)
STOPWORDS = {
    'that', 'with', 'from', 'this', 'have', 'been', 'will', 'can', 'are',
    'for', 'not', 'you', 'all', 'any', 'but', 'has', 'had', 'was', 'were',
    'be', 'and', 'the', 'your', 'what', 'who', 'how', 'our', 'its', 'new'
}

def extract_keywords(idea_text):
    words = idea_text.lower().split()
    return [
        word for word in words
        if len(word) > 3 and word not in STOPWORDS
    ]

keywords = extract_keywords(idea_text)
print(f"Keywords: {keywords}")
# Output: ['ai-powered', 'code', 'review', 'assistant', 'catching', 'security', 'vulnerabilities']
### Step 2: Gather Market Data

Collect data from available sources:

**Option A: Use Real API Data**

python
from idea_reality_mcp.sources.github import GitHubSource
from idea_reality_mcp.sources.hn import HNSource

github_source = GitHubSource()
hn_source = HNSource()

# Search GitHub for relevant repositories
github_results = github_source.search(
    keywords=["code", "review", "security", "ai"],
    min_stars=100
)

# Search HackerNews for related discussions
hn_results = hn_source.search(
    keywords=["code review", "security", "AI"],
    timeframe_days=365
)
**Option B: Use Mock Data (for testing without API keys)**

python
# Mock GitHub results for testing
github_results = GitHubResults(
    total_repo_count=85,
    max_stars=6500,
    top_repos=[
        {
            'name': 'code-review-ai',
            'stars': 3200,
            'url': 'https://github.com/example/code-review-ai',
            'description': 'AI-powered code review tool',
            'updated': '2024-01-15'
        },
        {
            'name': 'security-scanner',
            'stars': 2800,
            'url': 'https://github.com/example/security-scanner',
            'description': 'Automated security vulnerability detection',
            'updated': '2024-02-01'
        }
    ],
    recent_created_count=25,
    recent_ratio=0.29
)

# Mock HackerNews results
hn_results = HNResults(
    total_mentions=42,
    evidence=[
        {'title': 'Show HN: I built an AI code reviewer', 'score': 890, 'url': 'https://news.ycombinator.com/item?id=123'},
        {'title': 'AI in software development - discussion', 'score': 445, 'url': 'https://news.ycombinator.com/item?id=456'}
    ],
    recent_mention_ratio=0.35
)
### Step 3: Compute Validation Signal

Run the scoring engine to generate a viability assessment:

python
from idea_reality_mcp.scoring.engine import compute_signal

# Compute validation signal
signal = compute_signal(
    idea_text=idea_text,
    github_results=github_results,
    hn_results=hn_results
)

print(f"Validation Score: {signal.score}")
print(f"Signal Strength: {signal.strength}")  # 'strong', 'moderate', 'weak'
print(f"Recommendation: {signal.recommendation}")
### Step 4: Interpret Results

The validation returns structured output:

| Score Range | Signal Strength | Recommendation |
|-------------|-----------------|----------------|
| 70-100 | Strong | High confidence to proceed |
| 40-69 | Moderate | Proceed with caution, identify differentiation |
| 0-39 | Weak | Reconsider or pivot |

**Signal Components Analyzed:**

- **Competition Level**: Based on repository count, star distribution, and market saturation
- **Market Momentum**: Recent activity, new entrants, discussion frequency
- **Interest Signals**: HackerNews engagement, trending topics, community buzz
- **Monetization Indicators**: Paid tooling presence, enterprise adoption, pricing models observed

## Complete Example

python
from idea_reality_mcp.sources.github import GitHubResults
from idea_reality_mcp.sources.hn import HNResults
from idea_reality_mcp.scoring.engine import compute_signal

def validate_product_idea(idea_text):
    """
    Validate a product idea and return structured recommendations.
    """
    # Mock data for demonstration (replace with real API calls in production)
    github_results = GitHubResults(
        total_repo_count=120,
        max_stars=8900,
        top_repos=[
            {'name': 'spectrum', 'stars': 4200, 'url': 'https://github.com/example/spectrum', 'description': 'Developer community platform', 'updated': '2024-01-01'},
            {'name': 'discourse', 'stars': 3900, 'url': 'https://github.com/example/discourse', 'description': 'Forum software', 'updated': '2024-01-01'}
        ],
        recent_created_count=35,
        recent_ratio=0.29
    )
    
    hn_results = HNResults(
        total_mentions=67,
        evidence=[
            {'title': 'Ask HN: Best community platforms?', 'score': 320, 'url': 'https://news.ycombinator.com/item?id=123'}
        ],
        recent_mention_ratio=0.40
    )
    
    signal = compute_signal(idea_text, github_results, hn_results)
    
    return {
        'idea': idea_text,
        'score': signal.score,
        'strength': signal.strength,
        'recommendation': signal.recommendation,
        'market_insights': {
            'competition': 'moderate',  # Derived from signal details
            'momentum': 'growing',
            'opportunity': 'niche differentiation possible'
        }
    }

# Run validation
result = validate_product_idea("Developer community platform with AI moderation")
print(result)
## Tips and Best Practices

1. **Be Specific with Keywords**: Broader ideas produce noisier signals. Refine keywords to your exact use case.

2. **Validate Multiple Ideas**: Compare scores across competing ideas to prioritize development efforts.

3. **Re-validate Periodically**: Market conditions change. Re-run validation before major investments.

4. **Consider Signal Strength, Not Just Score**: A high score in a saturated market may still be viable if you find a strong differentiation angle.

5. **Combine with Customer Research**: Validation signals complement but don't replace direct customer feedback.

## Limitations

- **GitHub Data**: May not capture proprietary or internal tools
- **HackerNews Bias**: HN audience skews toward developer/technical topics
- **Timing Sensitivity**: Market signals can be volatile; validate close to launch decisions
- **Mock Data**: For testing only; real API data produces more accurate results

## Related Tools

- [GitHub Search API](https://docs.github.com/en/rest/search) - Primary data source for repository analysis
- [HackerNews API](https://github.com/HackerNews/API) - Community discussion signals
- [Semrush](https://www.semrush.com) - Supplement with keyword search volume data