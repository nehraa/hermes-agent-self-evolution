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

## Prerequisites

- Python 3.10+ installed
- Git installed
- (Optional) API keys for GitHub and HackerNews for live data

## Workflow Steps

### 1. Setup idea-reality-mcp

bash
# Clone the repository
git clone https://github.com/mnemox-ai/idea-reality-mcp.git
cd idea-reality-mcp

# Install dependencies (using pipx or virtual environment recommended)
pip install -e . --break-system-packages

# Verify installation
idea-reality doctor
### 2. Prepare Data Sources

**Option A: Use Mock Data (for testing without API keys)**

Create realistic mock results that match the expected data structures:

python
from idea_reality_mcp.sources.github import GitHubResults
from idea_reality_mcp.sources.hn import HNResults

# Mock GitHub results - adjust values based on idea specificity
github_results = GitHubResults(
    total_repo_count=85,
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
**Option B: Use Live Data (with API keys)**

Set environment variables before running:

bash
export GITHUB_TOKEN="ghp_your_github_token_here"
export HN_API_KEY="your_hackernews_api_key"
### 3. Define and Validate Ideas

For each idea to validate:

python
from idea_reality_mcp.scoring.engine import compute_signal

# Extract meaningful keywords (4-5 words, >3 chars, filter common words)
def extract_keywords(idea_text):
    """Extract meaningful keywords from idea description."""
    stop_words = {
        'that', 'with', 'from', 'this', 'have', 'been', 'will',
        'can', 'are', 'for', 'not', 'you', 'all', 'any', 'but',
        'has', 'had', 'was', 'were', 'be', 'their', 'they',
        'what', 'which', 'your', 'our', 'out', 'who', 'them'
    }
    idea_lower = idea_text.lower()
    words = [
        word for word in idea_lower.split()
        if len(word) > 3 and word not in stop_words
    ]
    return words[:5]  # Return top 5 keywords

# Example idea
idea_text = "AI-powered code review tool for catching security vulnerabilities"
keywords = extract_keywords(idea_text)

# Validate the idea
result = compute_signal(
    keywords=keywords,
    github_results=github_results,
    hn_results=hn_results
)

print(f"Validation Score: {result.signal_score}")
print(f"Recommendation: {result.recommendation}")
### 4. Interpret Results

The validation returns scores and recommendations:

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| 0.0 - 0.3 | Weak signal | Reconsider or pivot idea |
| 0.3 - 0.5 | Moderate signal | Validate further with user research |
| 0.5 - 0.7 | Strong signal | Proceed with MVP development |
| 0.7 - 1.0 | Very strong signal | High confidence - prioritize development |

### 5. Iterate and Refine

If initial results are weak:

- Refine keywords to be more specific
- Broaden or narrow the idea scope
- Test adjacent market segments
- Consider geographic or vertical focus

## Example Validation Session

python
# Complete example with multiple ideas
ideas = [
    "Local-first note-taking app with offline sync",
    "AI-powered code review for security vulnerabilities",
    "Decentralized social media platform"
]

for idea in ideas:
    keywords = extract_keywords(idea)
    result = compute_signal(keywords, github_results, hn_results)
    print(f"\nIdea: {idea}")
    print(f"Keywords: {keywords}")
    print(f"Score: {result.signal_score:.2f}")
    print(f"Details: {result.breakdown}")
## Troubleshooting

**Issue: "idea-reality: command not found"**
- Ensure the installation completed successfully
- Check that your Python environment's bin directory is in PATH
- Try reinstalling: `pip install -e .`

**Issue: "API rate limit exceeded"**
- Use mock data for testing
- Add delay between requests
- Use authenticated requests with API keys

**Issue: "No results found"**
- Broaden keywords (too specific terms yield no matches)
- Check spelling of technical terms
- Try alternative terminology

## Best Practices

1. **Validate multiple ideas** - Compare at least 3-5 ideas before deciding
2. **Be specific with keywords** - Too generic yields noise; too specific yields nothing
3. **Combine with user research** - Market data complements (not replaces) customer interviews
4. **Re-validate periodically** - Markets change; re-check assumptions quarterly
5. **Trust the data, but verify** - Use as one input among many in your decision-making