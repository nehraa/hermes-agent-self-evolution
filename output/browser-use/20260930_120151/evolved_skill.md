---
name: browser-use
description: "AI-powered web browser automation using browser-use — autonomously navigates, clicks, types, extracts from any website. Install once, use forever."
category: automation
---

# browser-use Skill

AI-powered web browser automation powered by an LLM agent that autonomously interacts with any website — navigating pages, clicking elements, filling forms, and extracting content. Ideal for tasks requiring JavaScript rendering, authentication, CAPTCHAs, or multi-step flows that static scraping cannot handle.

## Setup

**Already complete.** The environment is installed at `~/.hermes/browser-use/`.

bash
cd ~/.hermes/browser-use
source .venv/bin/activate
If you ever need to reinstall dependencies:

bash
uv sync
uvx browser-use install   # reinstalls Chromium + system dependencies
## Quick Start

### Python API

python
import asyncio
from browser_use import Agent, ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

async def main():
    agent = Agent(
        task="Find the current price of Claude Pro on anthropic.com pricing page",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
### CLI

bash
cd ~/.hermes/browser-use && source .venv/bin/activate

browser-use --agent-task "Find the top post on Hacker News right now" \
  --llm-provider anthropic \
  --llm-model claude-sonnet-4-0
## LLM Options

### Recommended: BrowserUse Cloud

Fastest option (3-5x speed improvement), lower cost, built-in stealth features.

1. Get API key at https://cloud.browser-use.com/new-api-key
2. Set environment variable: `export BROWSER_USE_API_KEY="your-key"`

python
from browser_use import Agent, ChatBrowserUse

agent = Agent(task="...", llm=ChatBrowserUse())
### Anthropic (Default)

python
from browser_use import Agent, ChatAnthropic

agent = Agent(
    task="...",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
### Cloud Browser Mode (Production)

Uses browser-use's remote browsers — bypasses anti-bot detection, no local browser needed.

python
from browser_use import Browser, BrowserConfig

browser = Browser(config=BrowserConfig(cloud=True))
## Common Patterns

### Research: Pricing Pages Behind Login

Many AI service pricing pages (Kling, Runway, Sora, etc.) hide credit costs until authenticated. The video/image generation UI typically displays costs before creation. Use this research sequence:

1. Navigate to pricing page: `/app/membership/membership-plan`
2. Dismiss login interstitials if possible (often optional for reading prices)
3. Navigate to generation UI: `/app/generate/video` — credit cost appears before generation
4. If blocked from generation UI, check external review sites: `aitoolanalysis.com`, `magichour.ai`, `segmind.com` — these often publish plan comparisons with actual credit costs

### Form Automation

python
agent = Agent(
    task="Go to example.com/contact, fill in name 'John Doe', email 'john@example.com', "
         "subject 'Support Request', and click submit. Report any success message.",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
### Content Extraction

python
agent = Agent(
    task="Extract all job listings from linkedin.com/jobs/search?q=python+developer&location=Remote. "
         "Return a list of job titles, companies, and links.",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
## Tips

- **Be specific in tasks**: Instead of "find prices", say "extract all pricing tiers and their monthly costs from the pricing page"
- **Chain complex tasks**: For multi-step flows, either describe the full sequence in one task or run multiple agents sequentially
- **Error handling**: The agent retries failed actions automatically; very slow pages may need longer timeout configuration
- **Stealth**: For sites with anti-bot measures, use `BrowserConfig(cloud=True)` or BrowserUse Cloud LLM