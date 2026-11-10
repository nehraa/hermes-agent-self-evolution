---
name: idea-validation-workflow
description: A systematic approach to validate software product ideas using idea-reality-mcp for pre-build reality checks
category: software-development
---

# Idea Validation Workflow

## Description
A systematic approach to validate software product ideas using the `idea-reality-mcp` tool. This workflow performs pre-build reality checks by analyzing GitHub, HackerNews, and ecosystem data to assess market viability, competition density, and monetization potential.

## When to Use
- Before investing development time in a new software product
- When assessing market viability and competitive landscape
- When evaluating monetization potential for ideas in AI/ML, developer tools, decentralized systems, or other technical domains
- When you need data-driven insights instead of relying on intuition alone
- When comparing multiple competing ideas to prioritize development

## Prerequisites
- Python 3.9+ installed
- Git installed
- API keys for GitHub and HackerNews (optional, can use mock data for testing)

---

## Workflow Steps

### Step 1: Setup idea-reality-mcp

Clone and install the tool:

bash
git clone https://github.com/mnemox-ai/idea-reality-mcp.git
cd idea-reality-mcp
pip install -e . --break-system-packages
For isolated installation, use `pipx` or a virtual environment:

bash
pipx install -e .
# or
python -m venv .venv && source .venv/bin/activate && pip install -e .
Verify the installation:

bash
idea-reality doctor
Expected output confirms all dependencies are properly installed.

### Step 2: Configure API Keys (Optional)

For live data, configure your API keys:

bash
export GITHUB_TOKEN="ghp_your_github_token_here"
export HN_API_KEY="your_hackernews_api_key_here"
Without API keys, the tool uses mock data or cached results.

### Step 3: Create Mock Data for Testing

When testing without API keys or when developing locally, create realistic mock results:

python
from idea_reality_mcp.sources.github import GitHubResults
from idea_reality_mcp.sources.hn import HNResults

# Mock GitHub results - adjust values based on your idea's specificity
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
### Step 4: Define and Validate Your Ideas

Prepare your idea text and extract meaningful keywords for analysis:

python
from idea_reality_mcp.scoring.engine import compute_signal

# Define your idea
idea_text = "AI-powered code review tool for detecting security vulnerabilities"

# Extract meaningful keywords (4-5 words, >3 chars, filter common words)
def extract_keywords(idea_text):
    idea_lower = idea_text.lower()
    stop_words = {
        'that', 'with', 'from', 'this', 'have', 'been', 'will', 'can',
        'are', 'for', 'not', 'you', 'all', 'any', 'but', 'has', 'had',
        'was', 'were', 'be', 'been', 'being', 'their', 'them', 'they',
        'your', 'what', 'when', 'where', 'which', 'who', 'how', 'about'
    }
    words = [
        word for word in idea_lower.split()
        if len(word) > 3 and word not in stop_words
    ]
    return ' '.join(words[:5])  # Limit to 5 most important words

keywords = extract_keywords(idea_text)
### Step 5: Run Validation Analysis

Execute the validation with your data:

python
# Run the signal computation
validation_result = compute_signal(
    github_results=github_results,
    hn_results=hn_results,
    keywords=keywords
)

# Extract key metrics
signal_score = validation_result.get('signal_score', 0)
market_opportunity = validation_result.get('market_opportunity', 'unknown')
competitive_density = validation_result.get('competitive_density', 'unknown')
monetization_potential = validation_result.get('monetization_potential', 'unknown')
### Step 6: Interpret Results

| Signal Score | Market Opportunity | Interpretation |
|-------------|-------------------|----------------|
| 0.7 - 1.0 | High | Strong demand signals, consider proceeding |
| 0.4 - 0.7 | Medium | Mixed signals, validate further or pivot |
| 0.0 - 0.4 | Low | Weak signals, reconsider or abandon |

**Additional factors to consider:**

- **Competition density**: High competition with established players suggests differentiation challenges
- **Monetization potential**: Check if similar products successfully monetize
- **Recent activity**: High recent repo creation and HN mentions indicate active market interest
- **Star distribution**: If top repos have 10k+ stars, market may be saturated

### Step 7: Validate Multiple Ideas

Compare ideas to prioritize development:

python
ideas = [
    "AI-powered code review tool",
    "Decentralized file storage system",
    "Real-time collaboration whiteboard",
    "Automated API documentation generator"
]

results = []
for idea in ideas:
    keywords = extract_keywords(idea)
    # Run validation (using real API or mock data)
    result = compute_signal(
        github_results=fetch_github_data(keywords),
        hn_results=fetch_hn_data(keywords),
        keywords=keywords
    )
    results.append({
        'idea': idea,
        'score': result.get('signal_score', 0),
        'opportunity': result.get('market_opportunity', 'unknown')
    })

# Sort by signal score
prioritized = sorted(results, key=lambda x: x['score'], reverse=True)
---

## Decision Framework

After validation, decide using this matrix:

| Signal | Competition | Action |
|--------|-------------|--------|
| High | Low | **Proceed immediately** - strong opportunity |
| High | High | **Proceed with differentiation** - validate unique angle |
| Low | Low | **Investigate further** - may be untapped or under-served |
| Low | High | **Reconsider** - challenging market position |

---

## Limitations

- **Data freshness**: GitHub and HN data may not capture all market signals
- **Niche ideas**: Very technical or domain-specific ideas may have insufficient data
- **Emerging markets**: New technologies without existing discussions may score low despite potential
- **Geographic bias**: HN and GitHub communities skew toward certain demographics

Use these results as one input among many in your decision-making process.

---

## Quick Reference Commands

bash
# Install
git clone https://github.com/mnemox-ai/idea-reality-mcp.git && cd idea-reality-mcp && pip install -e .

# Verify installation
idea-reality doctor

# Run with live data (requires API keys)
idea-reality validate --idea "your product idea here"