---
category: software-development
description: This skill enables Claude to build and run automated QA testing bots that simulate real user journeys across websites and web applications.
name: qa-testing-bots
---

# Automated QA Testing Bots

Build and run automated QA testing bots that simulate real user journeys across websites and web applications — catching bugs, broken flows, and regressions before your users do.

**Powered by Apify** with Puppeteer and Playwright under the hood.

> Create a free Apify account: https://www.apify.com/?fpr=dx06p

---

## Capabilities

- **User Journey Simulation** — Test complete flows: signup, login, checkout, form submissions
- **Broken Link Detection** — Find all 404 errors and dead links across your entire site
- **UI Validation** — Verify buttons, inputs, modals, and dropdowns are present and functional
- **Regression Testing** — Catch newly introduced bugs after deployments
- **Visual Debugging** — Capture screenshots and video recordings at each step
- **Cross-Device Testing** — Test across desktop, tablet, and mobile viewports
- **Performance Monitoring** — Assert response times and flag slow pages

---

## Setup

### 1. Get Your Apify API Token

1. Sign up at [apify.com](https://www.apify.com/?fpr=dx06p)
2. Go to **Settings → Integrations**: https://console.apify.com/account/integrations
3. Copy your **Personal API Token**
4. Export it as an environment variable:

bash
export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
### 2. Install the Client

bash
npm install apify-client
---

## Available Actors

| Actor | Use Case |
|---|---|
| `apify/puppeteer-scraper` | Full browser automation, form testing, click flows |
| `apify/playwright-scraper` | Cross-browser testing (Chrome, Firefox, WebKit) |
| `apify/broken-links-checker` | Detect all 404s and broken links site-wide |
| `apify/website-content-crawler` | Crawl all pages and validate structure |

---

## Examples

### Test a User Registration Flow

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com/signup" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;
    const results = { steps: [], passed: true, errors: [] };

    // Step 1 — Verify page loads
    await page.waitForSelector("form#signup");
    results.steps.push("✓ Signup page loaded");

    // Step 2 — Fill and submit form
    await page.fill("input[name='email']", "test@example.com");
    await page.fill("input[name='password']", "SecurePass123!");
    await page.click("button[type='submit']");

    // Step 3 — Verify success
    await page.waitForSelector(".success-message", { timeout: 5000 });
    results.steps.push("✓ Registration successful");

    return results;
  }
});

console.log(run.output);
### Check for Broken Links

javascript
const run = await client.actor("apify/broken-links-checker").call({
  startUrls: [{ url: "https://your-site.com" }],
  maxConcurrency: 5,
  maxResponseTime: 10000
});

console.log(`Found ${run.output.brokenLinks.length} broken links`);
run.output.brokenLinks.forEach(link => {
  console.log(`${link.statusCode} — ${link.url}`);
});
### Test Multiple Viewports

javascript
const viewports = [
  { name: "mobile", width: 375, height: 667 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1920, height: 1080 }
];

for (const vp of viewports) {
  const run = await client.actor("apify/playwright-scraper").call({
    startUrls: [{ url: "https://your-app.com" }],
    pageFunction: async function pageFunction(context) {
      const { page } = context;
      await page.setViewportSize({ width: vp.width, height: vp.height });
      // ... run tests with this viewport
    }
  });
  console.log(`${vp.name}: ${run.status}`);
}
---

## Best Practices

1. **Start with crawlable URLs** — Use sitemap.xml or a known starting point
2. **Set realistic timeouts** — Account for slow network conditions
3. **Limit concurrency** — Avoid overwhelming your target server
4. **Store outputs** — Save results to Apify dataset or export to JSON
5. **Schedule regular runs** — Run tests after each deployment