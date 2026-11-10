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
- When researching competitors and market gaps before building

## Prerequisites

- Python 3.9+
- Git installed
- API keys for GitHub (optional, mock data supported)
- `pip` or `pipx` for package management

## Workflow Steps

### Step 1: Install idea-reality-mcp

bash
# Clone the repository
git clone https://github.com/mnemox-ai/idea-reality-mcp.git
cd idea-reality-mcp

# Install in development mode
pip install -e . --break-system-packages

# Or use pipx for isolation
pipx install -e .

# Verify installation
idea-reality doctor
### Step 2: Gather Data Sources

The tool analyzes three primary data sources:

| Source | Purpose | Required |
|--------|---------|----------|
| **GitHub** | Repository counts, star rankings, activity signals | Optional (mock supported) |
| **HackerNews** | Discussion volume, sentiment, trend indicators | Optional (mock supported) |
| **Ecosystem** | Market context, adjacent tool relationships | Optional |

#### Option A: Use Real API Data

bash
# Set environment variables
export GITHUB_TOKEN="ghp_your_token_here"

# Run validation with live data
idea-reality validate --idea "Your product idea here" --sources github,hn
#### Option B: Create Mock Data for Testing

python
from idea_reality_mcp.sources.github import GitHubResults
from idea_reality_mcp.sources.hn import HNResults
from datetime import datetime

# Mock GitHub results
github_results = GitHubResults(
    total_repo_count=85,
    max_stars=6500,
    top_repos=[
        {
            'name': 'example-tool',
            'stars': 3200,
            'url': 'https://github.com/example/example-tool',
            'description': 'Popular tool in this space',
            'updated': '2024-01-15'
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
### Step 3: Define and Validate Ideas

python
from idea_reality_mcp.scoring.engine import compute_signal

# Extract meaningful keywords for search
def extract_keywords(idea_text):
    """Extract 4-5 relevant keywords (3+ chars, excluding common words)."""
    stopwords = {
        'that', 'with', 'from', 'this', 'have', 'been', 'will', 'can',
        'are', 'for', 'not', 'you', 'all', 'any', 'but', 'has', 'had',
        'was', 'were', 'been', 'be', 'your', 'they', 'their', 'what',
        'about', 'which', 'when', 'make', 'like', 'just', 'into', 'than'
    }
    
    words = idea_text.lower().split()
    keywords = [w for w in words if len(w) > 3 and w not in stopwords]
    
    # Return top 5 most relevant
    return keywords[:5]

# Validate an idea
idea_text = "AI-powered code review tool for automated PR analysis"
keywords = extract_keywords(idea_text)

# Compute signal score
result = compute_signal(
    idea=idea_text,
    keywords=keywords,
    github_data=github_results,
    hn_data=hn_results
)

print(f"Signal Score: {result.signal_score}")
print(f"Confidence: {result.confidence}")
print(f"Recommendations: {result.recommendations}")
### Step 4: Interpret Results

The signal score ranges from 0-100:

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| **0-30** | Weak signal - limited market evidence | Consider pivoting or deeper research |
| **31-60** | Moderate signal - some market validation | Proceed with caution, validate further |
| **61-80** | Strong signal - good market indicators | Likely worth pursuing |
| **81-100** | Very strong signal - high market demand | Proceed with confidence |

#### Key Metrics to Review

1. **Competition Level**: Number of existing solutions, star distribution
2. **Market Momentum**: Recent repo creation, HN discussion trends
3. **Monetization Signals**: Paid tools in the space, pricing patterns
4. **Gap Analysis**: Underexplored niches or underserved use cases

### Step 5: Iterate and Refine

Based on initial results, refine your idea:

python
# Refine idea based on findings
def refine_idea(original_idea, analysis_results):
    """Refine idea based on signal analysis."""
    refinements = []
    
    # Check for oversaturated market
    if analysis_results.competition_score > 70:
        refinements.append("Consider narrower focus or differentiator")
    
    # Check for emerging opportunity
    if analysis_results.recent_ratio > 0.4:
        refinements.append("Market is heating up - act faster")
    
    # Check for monetization gaps
    if not analysis_results.has_paid_competitors:
        refinements.append("Potential for paid tier with basic free tier")
    
    return refinements

# Apply refinements
refinements = refine_idea(idea_text, result)
for r in refinements:
    print(f"- {r}")
## Example Workflow

python
# Complete example
from idea_reality_mcp import IdeaValidator

# Initialize validator
validator = IdeaValidator(config={
    'sources': ['github', 'hn'],
    'strict_mode': False  # Allow partial data
})

# Validate multiple ideas
ideas = [
    "Local-first note-taking app with offline sync",
    "AI assistant for debugging production errors",
    "Open source Stripe alternative for emerging markets"
]

for idea in ideas:
    print(f"\n{'='*60}")
    print(f"Validating: {idea}")
    print('='*60)
    
    report = validator.generate_report(idea)
    
    print(f"Signal Score: {report.signal_score}/100")
    print(f"Competition: {report.competition_level}")
    print(f"Recommendation: {report.recommendation}")
    print(f"\nKey Insights:")
    for insight in report.key_insights:
        print(f"  • {insight}")
## Best Practices

1. **Test Multiple Ideas**: Run validation on 3-5 related ideas to compare
2. **Refine Keywords**: Adjust keywords based on initial results for better matches
3. **Check Trends**: Look at recent_ratio to identify emerging vs. declining markets
4. **Validate Assumptions**: Use mock data to test edge cases before committing
5. **Document Findings**: Keep reports for future reference and iteration

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty results | Broaden keywords or check spelling |
| API rate limits | Use mock data or add delays between requests |
| Installation fails | Try `pipx install -e .` for isolation |
| Doctor check fails | Verify Python version (3.9+) and pip installation |

## See Also

- [idea-reality-mcp GitHub Repository](https://github.com/mnemox-ai/idea-reality-mcp)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Market Validation Best Practices](https://github.com/mnemox-ai/idea-reality-mcp#usage)