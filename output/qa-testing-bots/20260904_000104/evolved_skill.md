---
category: software-development
description: This skill enables Claude to build and run **automated QA testing bots** that simulate real user journeys across websites and web applications.
name: qa-testing-bots
---

# Automated QA Testing Bots Skill

## Overview

Build and run automated QA testing bots that simulate real user journeys across websites and web applications — catching bugs, broken flows, and regressions before your users do.

Powered by **Apify** with Puppeteer and Playwright under the hood.

> 🔗 Sign up for Apify here: https://www.apify.com/?fpr=dx06p

---

## What This Skill Does

- **Simulate complete user journeys** — signup, login, checkout, form submissions, multi-step flows
- **Detect broken links, 404 errors, and failed redirects** across entire sites
- **Validate UI elements** — buttons, inputs, modals, dropdowns — are present and functional
- **Run regression tests** after deployments to catch newly introduced bugs
- **Capture screenshots and video recordings** at each step for visual debugging
- **Test across multiple viewports** — desktop, tablet, mobile
- **Assert response times** and flag pages that exceed performance thresholds

---

## Step 1 — Get Your Apify API Token

1. Sign up at **https://www.apify.com/?fpr=dx06p** (free account available)
2. Go to **Settings → Integrations**
   - Direct link: https://console.apify.com/account/integrations
3. Copy your **Personal API Token**: `apify_api_xxxxxxxxxxxxxxxx`
4. Set it as an environment variable:

bash
export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
---

## Step 2 — Install Dependencies

bash
npm install apify-client
---

## Actors for QA Testing

| Actor ID | Best For |
|---|---|
| `apify/puppeteer-scraper` | Full browser automation, form testing, click flows |
| `apify/playwright-scraper` | Cross-browser testing (Chrome, Firefox, WebKit) |
| `apify/broken-links-checker` | Detect all 404s and broken links site-wide |
| `apify/website-content-crawler` | Crawl all pages and validate structure |

---

## Examples

### Test a Complete User Registration Flow

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com/signup" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;
    const results = { steps: [], passed: true, errors: [] };

    try {
      // Step 1 — Verify page loads
      await page.waitForLoadState('networkidle');
      results.steps.push({ name: 'Page Load', status: 'passed' });

      // Step 2 — Fill registration form
      await page.fill('#name', 'Test User');
      await page.fill('#email', 'test@example.com');
      await page.fill('#password', 'SecurePass123!');
      results.steps.push({ name: 'Form Fill', status: 'passed' });

      // Step 3 — Submit form
      await page.click('#signup-button');
      await page.waitForURL('**/dashboard**');
      results.steps.push({ name: 'Submission & Redirect', status: 'passed' });

      // Step 4 — Verify dashboard elements
      const welcome = await page.textContent('h1');
      if (!welcome.includes('Welcome')) {
        throw new Error('Welcome message not found');
      }
      results.steps.push({ name: 'Dashboard Verification', status: 'passed' });

      // Capture screenshot for debugging
      await page.screenshot({ path: 'signup-success.png' });

    } catch (error) {
      results.passed = false;
      results.errors.push(error.message);
      await page.screenshot({ path: 'signup-error.png' });
    }

    return results;
  }
});

console.log('Test Results:', run.output);
### Check for Broken Links Across a Website

javascript
const run = await client.actor("apify/broken-links-checker").call({
  startUrls: [{ url: "https://your-site.com" }],
  maxConcurrency: 5,
  maxPagesPerCrawl: 100
});

console.log('Broken Links Found:', run.output.brokenLinks);
console.log('Total Links Checked:', run.output.totalLinks);
### Cross-Device Responsive Testing

javascript
const viewports = [
  { name: 'Mobile', width: 375, height: 667 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Desktop', width: 1280, height: 720 }
];

for (const viewport of viewports) {
  await client.actor("apify/puppeteer-scraper").call({
    startUrls: [{ url: "https://your-app.com" }],
    pageFunction: async function pageFunction(context) {
      const { page } = context;
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.waitForLoadState('networkidle');
      // Check for layout breaks, overflow issues, hidden content
    },
    customData: { viewport: viewport.name }
  });
}
### Performance Regression Test

javascript
const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com/dashboard" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;
    const metrics = {};

    // Measure Time to First Byte
    const ttfb = await page.evaluate(() => {
      const entries = performance.getEntriesByType('navigation');
      return entries[0] ? entries[0].responseStart : null;
    });
    metrics.ttfb = ttfb;

    // Measure Largest Contentful Paint
    await page.waitForLoadState('networkidle');
    metrics.loadComplete = Date.now();

    // Assert performance threshold
    const PASS_THRESHOLD_MS = 2000;
    if (ttfb > PASS_THRESHOLD_MS) {
      throw new Error(`Page load exceeded threshold: ${ttfb}ms`);
    }

    return metrics;
  }
});
---

## Best Practices

1. **Use unique selectors** — Prefer `data-testid` attributes over CSS selectors for resilient element targeting
2. **Add explicit waits** — Use `waitForSelector` and `waitForLoadState` instead of arbitrary delays
3. **Capture state on failure** — Always take screenshots when tests fail for faster debugging
4. **Test in isolation** — Use test accounts and isolated environments to avoid side effects
5. **Set concurrency limits** — Reduce concurrency when testing rate-limited APIs

---

## Troubleshooting

| Issue | Solution |
|---|---|
| "Token invalid" error | Verify `APIFY_TOKEN` environment variable is set correctly |
| Elements not found | Use `waitForSelector` before interactions; check for iframes or shadow DOM |
| Rate limiting | Reduce `maxConcurrency`; add delays between requests |
| Captchas blocking tests | Use Apify Proxy with residential IPs or skip captcha-protected flows |