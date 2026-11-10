---
name: browser-use
description: "AI-powered web browser automation using browser-use — autonomously navigates, clicks, types, extracts from any website. Install once, use forever."
category: automation
---

# browser-use Skill

AI-powered web browser automation. An AI agent autonomously interacts with any website — navigates, clicks, fills forms, extracts content — driven by an LLM. Use whenever you need to interact with a website that requires JavaScript rendering, authentication, or multi-step flows that static scraping can't handle.

---

## Setup (One-Time — Already Done)

bash
cd ~/.hermes/browser-use
uv venv --python 3.11 .venv
source .venv/bin/activate
uv sync
uvx browser-use install   # installs Chromium + dependencies
**Location**: `~/.hermes/browser-use/` — already cloned and installed.

**Note**: Activate the virtual environment before running scripts:
bash
source ~/.hermes/browser-use/.venv/bin/activate
---

## Quick Start

### Python Script

python
import asyncio
from browser_use import Agent, ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

async def main():
    agent = Agent(
        task="Find the top HN post and summarize it",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    await agent.run()

asyncio.run(main())
### CLI

bash
cd ~/.hermes/browser-use
source .venv/bin/activate

uvx browser-use \
  --agent-task "Find the top HN post" \
  --llm-provider anthropic \
  --llm-model claude-sonnet-4-0
---

## Preferred LLM

**`ChatBrowserUse`** — optimized for browser automation, 3-5x faster and more cost-effective.

1. Get API key: https://cloud.browser-use.com/new-api-key
2. Set environment variable:

bash
export BROWSER_USE_API_KEY="your-key-here"
3. Use in script:

python
from browser_use import Agent, ChatBrowserUse

async def main():
    agent = Agent(
        task="Your instruction here",
        llm=ChatBrowserUse()
    )
    await agent.run()
### Fallback: Claude

python
from browser_use import Agent, ChatAnthropic

agent = Agent(
    task="Your instruction here",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
---

## Cloud Browser (Production / Stealth)

Use browser-use's cloud infrastructure for better stealth and reliability.

python
from browser_use import Browser, BrowserConfig

browser = Browser(config=BrowserConfig(cloud=True))
**Environment variable required:**
bash
export BROWSER_USE_API_KEY="your-key-here"
---

## Research Pattern: Pricing Pages Behind Login

Many AI service pricing pages (Kling, Runway, etc.) don't show credit costs until logged in. Use this sequence:

1. **Navigate to pricing page**: `/app/membership/membership-plan`
2. **Bypass login interstitial**: Often optional for reading prices — click "Skip" or "Continue as Guest"
3. **Navigate to generation UI**: `/app/generate/video` — credit cost shown before generation
4. **Fallback**: If still logged out, check plan comparison tables on external review sites:
   - aitoolanalysis.com
   - magichour.ai
   - segmind.com

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Module not found` | Ensure venv is activated: `source .venv/bin/activate` |
| Cloud browser fails | Verify `BROWSER_USE_API_KEY` is set |
| Slow automation | Use `ChatBrowserUse` instead of Claude |
| Elements not found | Add more context in task description, or add `max_steps` |
| Login required | Use CLI with `--headless=false` to manually log in first |

---

## Common Task Examples

### Extract structured data from a page
python
task = """Go to example.com/pricing, extract all plan names, prices, 
and features into a markdown table"""
### Multi-step form submission
python
task = """Navigate to example.com/contact, fill out the form with:
- Name: Test User
- Email: test@example.com
- Message: Hello
Submit the form and confirm success."""
### Research and compare
python
task = """Search for 'best AI video tools 2024', visit the top 3 results,
and create a comparison table of features and pricing."""