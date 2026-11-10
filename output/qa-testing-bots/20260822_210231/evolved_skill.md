---
category: software-development
description: This skill enables Claude to build and run automated QA testing bots that simulate real user journeys across websites and web applications — catching bugs, broken flows, and regressions before your users do.
name: qa-testing-bots
---

# Automated QA Testing Bots Skill

## Overview

This skill enables Claude to build and run **automated QA testing bots** that simulate real user journeys across websites and web applications — catching bugs, broken flows, and regressions before your users do.

Powered by **Apify** with Puppeteer and Playwright under the hood.

> 🔗 Sign up for Apify here: https://www.apify.com/?fpr=dx06p

---

## What This Skill Does

- Simulate complete **user journeys** (signup, login, checkout, form submission)
- Detect **broken links**, **404 errors**, and **failed redirects** across an entire site
- Validate **UI elements** — buttons, inputs, modals, dropdowns — are present and functional
- Run **regression tests** after deployments to catch newly introduced bugs
- Take **screenshots and video recordings** at each step for visual debugging
- Test across multiple **viewports** (desktop, tablet, mobile)
- Assert **response times** and flag pages that are too slow

---

## Step 1 — Get Your Apify API Token

1. Sign up for a free account at **https://www.apify.com/?fpr=dx06p**
2. Navigate to **Settings → Integrations**
   - Direct link: https://console.apify.com/account/integrations
3. Copy your **Personal API Token**: `apify_api_xxxxxxxxxxxxxxxx`
4. Set it as an environment variable:

bash
export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
> **Security Note:** Never hardcode your API token. Always use environment variables or a `.env` file (add `.env` to `.gitignore`).

---

## Step 2 — Install Dependencies

bash
npm install apify-client
Or with yarn:

bash
yarn add apify-client
---

## Quick Start: Running an Actor

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

async function runTest() {
  const run = await client.actor("apify/puppeteer-scraper").call({
    startUrls: [{ url: "https://example.com" }],
    pageFunction: async ({ page }) => {
      const title = await page.title();
      console.log(`Page title: ${title}`);
      return { title };
    }
  });

  console.log("Run completed:", run.status);
  console.log("Results:", run.output);
}
---

## Available Actors

| Actor ID | Use Case | Best For |
|----------|----------|----------|
| `apify/puppeteer-scraper` | Full browser automation, form testing, click flows | Complex user interactions |
| `apify/playwright-scraper` | Cross-browser testing (Chrome, Firefox, WebKit) | Multi-browser validation |
| `apify/broken-links-checker` | Detect all 404s and broken links site-wide | Link health audits |
| `apify/website-content-crawler` | Crawl all pages and validate structure | Site-wide content validation |

---

## Example 1: Test User Registration Flow

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

async function testRegistrationFlow() {
  const run = await client.actor("apify/puppeteer-scraper").call({
    startUrls: [{ url: "https://your-app.com/signup" }],
    pageFunction: async function pageFunction({ page, request }) {
      const { url } = request;
      const results = {
        url,
        steps: [],
        passed: true,
        errors: []
      };

      try {
        // Step 1 — Verify page loads
        await page.waitForLoadState("networkidle");
        results.steps.push({ action: "page_load", status: "ok" });

        // Step 2 — Fill registration form
        await page.fill('input[name="email"]', 'test@example.com');
        await page.fill('input[name="password"]', 'SecurePass123!');
        await page.fill('input[name="confirmPassword"]', 'SecurePass123!');
        results.steps.push({ action: "form_filled", status: "ok" });

        // Step 3 — Submit form
        await page.click('button[type="submit"]');

        // Step 4 — Wait for redirect or response
        await page.waitForURL(/\/(dashboard|welcome|home)/, { timeout: 10000 });
        results.steps.push({
          action: "redirect",
          status: "ok",
          finalUrl: page.url()
        });

      } catch (error) {
        results.passed = false;
        results.errors.push({
          step: results.steps.length,
          message: error.message,
          screenshot: await page.screenshot({ fullPage: true })
        });
      }

      return results;
    },
    maxConcurrency: 1
  });

  // Check results
  const dataset = await client.datasets.get(run.defaultDatasetId);
  const { items } = await dataset.listItems({ limit: 100 });

  items.forEach((result) => {
    console.log(`\nTest: ${result.url}`);
    console.log(`Passed: ${result.passed}`);
    if (result.errors.length > 0) {
      console.log("Errors:", result.errors);
    }
  });
}
---

## Example 2: Detect Broken Links Across Site

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

async function checkBrokenLinks(siteUrl) {
  const run = await client.actor("apify/broken-links-checker").call({
    startUrls: [{ url: siteUrl }],
    max crawl depth: 10,
    excludeUrlPatterns: [
      "*.pdf",
      "*.zip",
      "*/api/*",
      "*/admin/*"
    ]
  });

  // Fetch results
  const dataset = await client.datasets.get(run.defaultDatasetId);
  const { items } = await dataset.listItems({ limit: 1000 });

  const brokenLinks = items.filter(item => item.httpStatus >= 400);
  const summary = {
    totalChecked: items.length,
    brokenCount: brokenLinks.length,
    brokenLinks: brokenLinks.map(link => ({
      url: link.url,
      status: link.httpStatus,
      source: link.parentUrl
    }))
  };

  console.log(`\nLink Health Report for: ${siteUrl}`);
  console.log(`Total links checked: ${summary.totalChecked}`);
  console.log(`Broken links found: ${summary.brokenCount}`);

  if (summary.brokenCount > 0) {
    console.log("\n--- Broken Links ---");
    summary.brokenLinks.forEach(link => {
      console.log(`  ${link.status} | ${link.url}`);
      console.log(`    Source: ${link.source}`);
    });
  }

  return summary;
}

// Run: checkBrokenLinks("https://your-site.com");
---

## Example 3: Cross-Viewport Responsive Testing

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const viewports = [
  { name: "mobile", width: 375, height: 812 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1920, height: 1080 }
];

async function testResponsiveDesign(url) {
  const results = [];

  for (const viewport of viewports) {
    const run = await client.actor("apify/puppeteer-scraper").call({
      startUrls: [{ url }],
      pageFunction: async function pageFunction({ page }) {
        const issues = [];

        // Check critical elements exist
        const elements = [
          { selector: "nav", name: "Navigation" },
          { selector: "main", name: "Main content" },
          { selector: "footer", name: "Footer" },
          { selector: "button", name: "Buttons" },
          { selector: "a", name: "Links" }
        ];

        for (const el of elements) {
          const count = await page.locator(el.selector).count();
          if (count === 0) {
            issues.push(`Missing: ${el.name}`);
          }
        }

        // Check for horizontal scroll (layout break indicator)
        const hasHorizontalScroll = await page.evaluate(() => {
          return document.documentElement.scrollWidth > document.documentElement.clientWidth;
        });

        if (hasHorizontalScroll) {
          issues.push("Horizontal scroll detected - layout may be broken");
        }

        return {
          issues,
          viewport: process.env.APIFY_MEMORY_MBYTES // passed via environment
        };
      }
    });

    results.push({
      viewport: viewport.name,
      ...(await getResults(run))
    });
  }

  // Report
  console.log("\nResponsive Design Report");
  console.log("========================");
  results.forEach(r => {
    console.log(`\n${r.viewport}: ${r.issues.length === 0 ? "✓ No issues" : "⚠ Issues found"}`);
    r.issues.forEach(i => console.log(`  - ${i}`));
  });
}

async function getResults(run) {
  const dataset = await client.datasets.get(run.defaultDatasetId);
  const { items } = await dataset.listItems({ limit: 1 });
  return items[0] || { issues: [] };
}
---

## Example 4: Performance Regression Testing

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const THRESHOLD_MS = 3000; // Max acceptable load time

async function testPagePerformance(url) {
  const run = await client.actor("apify/puppeteer-scraper").call({
    startUrls: [{ url }],
    pageFunction: async function pageFunction({ page }) {
      const metrics = await page.evaluate(() => {
        const timing = performance.timing;
        return {
          domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
          fullLoad: timing.loadEventEnd - timing.navigationStart,
          firstPaint: performance.getEntriesByType("paint")[0]?.startTime || 0
        };
      });

      // Get network requests
      const slowRequests = [];
      page.on("response", response => {
        if (response.status() >= 200 && response.status() < 400) {
          // Check for slow responses handled separately
        }
      });

      return metrics;
    }
  });

  const dataset = await client.datasets.get(run.defaultDatasetId);
  const { items } = await dataset.listItems({ limit: 1 });
  const metrics = items[0];

  console.log(`\nPerformance Report for: ${url}`);
  console.log(`DOM Content Loaded: ${metrics.domContentLoaded}ms`);
  console.log(`Full Page Load: ${metrics.fullLoad}ms`);
  console.log(`First Paint: ${metrics.firstPaint.toFixed(0)}ms`);

  const passed = metrics.fullLoad <= THRESHOLD_MS;
  console.log(`\nStatus: ${passed ? "✓ PASSED" : "⚠ FAILED"} (threshold: ${THRESHOLD_MS}ms)`);

  return { passed, metrics, threshold: THRESHOLD_MS };
}
---

## Best Practices

### Error Handling

javascript
// Always wrap page interactions in try-catch
try {
  await page.waitForSelector('button[type="submit"]', { timeout: 5000 });
  await page.click('button[type="submit"]');
} catch (error) {
  console.error(`Failed at ${url}: ${error.message}`);
  await page.screenshot({ path: `error-${Date.now()}.png` });
  throw error;
}
### Waiting Strategies

javascript
// ❌ Avoid: fixed delays
await page.waitForTimeout(2000); // Flaky, slow

// ✓ Prefer: intelligent waits
await page.waitForLoadState("networkidle");  // Network settled
await page.waitForSelector("#content", { state: "visible" }); // Element visible
await page.waitForResponse(response => response.url().includes("/api/")); // API response
### Rate Limiting

javascript
const run = await client.actor("apify/puppeteer-scraper").call({
  // Limit concurrent pages
  maxConcurrency: 1,

  // Add delays between requests
  ...(await delay ? { delayAfterHit: 1000 } : {})
});
---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `403 Forbidden` errors | Site may block automated requests. Add `userAgent` and `extraHttpHeaders` or use proxy rotation |
| Form submissions fail | CSRF tokens may be required. Extract from page and include in requests |
| Login sessions don't persist | Use `page.context().storageState()` to save cookies between pages |
| Elements not found | Use `waitForSelector` instead of immediate queries. Check for iframes or shadow DOM |
| Scraper gets blocked | Add realistic headers, use proxies, and respect `robots.txt` |

---

## Next Steps

1. **Set up monitoring** — Schedule runs with Apify Scheduler for continuous testing
2. **Integrate with CI/CD** — Add QA bot runs to your deployment pipeline
3. **Store results** — Use Apify Datasets or webhooks to push results to Slack, PagerDuty, or your dashboard
4. **Explore Playwright** — For more advanced browser testing, try `apify/playwright-scraper`