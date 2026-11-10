---
category: software-development
description: "> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software."
name: afrexai-qa-testing-engine
---

# QA & Testing Engine — Complete Software Quality System

> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software.

---

## Phase 1: Test Strategy Design

Before writing a single test, define your testing approach. A solid strategy prevents wasted effort and ensures you test what matters.

### Strategy Brief Template

yaml
project:
  name: ""
  type: web-app | api | mobile | library | cli | data-pipeline
  languages: [typescript, python, go, java]
  frameworks: [react, express, django, spring]

risk_profile:
  data_sensitivity: low | medium | high | critical  # PII, financial, health data
  user_impact: internal | b2b | b2c | life-safety
  deployment_frequency: daily | weekly | monthly
  regulatory: [none, SOC2, HIPAA, PCI-DSS, GDPR]

test_scope:
  in_scope: []      # Features, services, components to test
  out_of_scope: []  # Explicitly excluded (include reasoning)

environments:
  dev: { url: "", db: "local" }
  staging: { url: "", db: "seeded" }
  prod: { url: "", smoke_only: true }

success_criteria:
  coverage_target: 80%       # Line, branch, or mutation
  performance: "< 200ms p95"
  accessibility: "WCAG AA"
### Test Type Decision Matrix

| Risk Profile | Unit | Integration | E2E | Performance | Security | Accessibility |
|---|---|---|---|---|---|---|
| Internal tool | ✅ Core logic | ✅ API | ⚠️ Happy path | ❌ | ⚠️ Basic auth | ❌ |
| B2B SaaS | ✅ Full | ✅ Full | ✅ Critical flows | ✅ Load tests | ✅ OWASP Top 10 | ✅ WCAG AA |
| B2C high-traffic | ✅ Full | ✅ Full | ✅ Full suite | ✅ Stress + soak | ✅ Full suite | ✅ WCAG AA |
| Financial/Health | ✅ Full + mutation | ✅ Full + contracts | ✅ Full + chaos | ✅ Full suite | ✅ Pen test | ✅ WCAG AAA |

### Test Pyramid Architecture

/  E2E  \          5-10% — Critical user journeys only
        / Integration \     20-30% — API contracts, service boundaries
       /    Unit Tests   \  60-70% — Business logic, pure functions
**Anti-pattern: Ice cream cone** — E2E tests exceed unit tests. Result: slow, flaky, expensive pipelines. Fix by pushing coverage DOWN the pyramid.

**Anti-pattern: Hourglass** — Abundant unit + E2E tests, no integration layer. Result: missed contract bugs between services.

---

## Phase 2: Unit Testing Mastery

### The AAA Pattern (Arrange-Act-Assert)

Structure every unit test with three distinct phases:

typescript
describe('PricingCalculator', () => {
  // Group by behavior, not by method name
  describe('when customer has volume discount eligibility', () => {
    it('applies 15% discount to total order', () => {
      // Arrange — set up test data and dependencies
      const calculator = new PricingCalculator();
      const order = createOrder({ items: 500, customerTier: 'gold' });

      // Act — execute the behavior under test
      const result = calculator.calculateTotal(order);

      // Assert — verify expected outcomes
      expect(result.discount).toBe(0.15);
      expect(result.finalPrice).toBe(425);
    });

    it('caps discount at $1000 maximum', () => {
      // Arrange
      const calculator = new PricingCalculator();
      const order = createOrder({ items: 10000, customerTier: 'platinum' });

      // Act
      const result = calculator.calculateTotal(order);

      // Assert
      expect(result.discount).toBe(1000); // Not 0.20 * 10000
    });
  });
});
### Naming Conventions

| Pattern | Format | Example |
|---|---|---|
| Describe | Noun + behavior context | `UserService`, `when session expires` |
| It | Expected outcome verb | `applies discount`, `returns error`, `creates record` |

**Good:** `describe('OrderProcessor'), it('applies shipping discount when order exceeds $50')`

**Bad:** `describe('testOrder'), it('should work correctly')`

### Test Data Strategies

| Strategy | Use When | Example |
|---|---|---|
| Factories | Tests need consistent objects | `createUser({ role: 'admin' })` |
| Random generation | Property-based testing | `faker.internet.email()` |
| Inline literals | Single specific case | `{ name: 'Test', active: true }` |
| Fixtures (files) | Complex or real-world data | `users.json`, `responses/` |

### Mocking Best Practices

typescript
// ✅ Good — mock at boundaries, not internals
describe('OrderService', () => {
  it('sends confirmation email on successful order', async () => {
    const emailService = { send: jest.fn().mockResolvedValue({ id: '123' }) };
    const orderService = new OrderService(emailService);

    await orderService.completeOrder({ userId: '1', total: 99.99 });

    expect(emailService.send).toHaveBeenCalledWith(
      expect.objectContaining({ template: 'order-confirmation' })
    );
  });
});

// ❌ Bad — mocking everything, testing nothing
it('calls repository correctly', () => {
  const repo = { findById: jest.fn().mockReturnValue({}) };
  const service = new Service(repo as any);
  service.get(1);
  expect(repo.findById).toHaveBeenCalled(); // Tests implementation, not behavior
});
---

## Phase 3: Integration Testing

### Scope and Purpose

Integration tests verify that components work together correctly — database queries, API calls, file operations, message queues.

### Database Testing Patterns

typescript
describe('UserRepository', () => {
  // Use transactions to auto-rollback after each test
  beforeEach(async () => {
    await db.query('BEGIN');
  });

  afterEach(async () => {
    await db.query('ROLLBACK');
  });

  it('creates user with encrypted password', async () => {
    const repo = new UserRepository(db);

    const user = await repo.create({
      email: 'test@example.com',
      password: 'plaintext123'
    });

    expect(user.passwordHash).not.toBe('plaintext123');
    expect(user.passwordHash).toMatch(/^\$2[aby]?\$\d{2}\$/); // bcrypt format
  });

  it('prevents duplicate emails', async () => {
    const repo = new UserRepository(db);
    await repo.create({ email: 'taken@example.com', password: 'pass' });

    await expect(
      repo.create({ email: 'taken@example.com', password: 'pass2' })
    ).rejects.toThrow('UNIQUE constraint');
  });
});
### API Contract Testing

typescript
describe('Payment API contract', () => {
  it('accepts valid payment request shape', async () => {
    const response = await fetch('/api/payments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: 99.99,
        currency: 'USD',
        source: 'tok_visa'
      })
    });

    expect(response.status).toBe(201);
    expect(response.body).toMatchSchema({
      type: 'object',
      required: ['id', 'status', 'createdAt'],
      properties: {
        id: { type: 'string', format: 'uuid' },
        status: { type: 'string', enum: ['pending', 'succeeded', 'failed'] }
      }
    });
  });
});
---

## Phase 4: End-to-End Testing

### When to Use E2E

E2E tests simulate real user workflows. Use sparingly for:

- Critical user journeys (login, checkout, signup)
- Flows spanning multiple pages/services
- Payment and authentication pipelines

### Page Object Model

typescript
// pages/LoginPage.ts
class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email-input"]', email);
    await this.page.fill('[data-testid="password-input"]', password);
    await this.page.click('[data-testid="submit-button"]');
  }

  getErrorMessage() {
    return this.page.textContent('[data-testid="error-message"]');
  }
}

// tests/login.spec.ts
test('shows error on invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'wrongpassword');

  expect(loginPage.getErrorMessage()).toContain('Invalid credentials');
});
### Critical Flow Checklist

| Flow | Pages | Key Assertions |
|---|---|---|
| New user signup | Landing → Signup → Email verify → Dashboard | User created, redirected correctly |
| Purchase checkout | Cart → Checkout → Payment → Confirmation | Charge created, inventory decremented |
| Password reset | Login → Reset request → Email → New password | Token valid once, password changed |

---

## Phase 5: Performance Testing

### Types of Performance Tests

| Type | Purpose | Metrics |
|---|---|---|
| Load | Normal expected traffic | Response time, throughput |
| Stress | Breakpoint identification | Max users, degradation pattern |
| Soak | Memory leaks, degradation over time | Resource usage after 2+ hours |
| Spike | Sudden traffic increases | Recovery time |

### Performance Test Structure

typescript
// Using k6, Artillery, or similar

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },   // Steady state
    { duration: '2m', target: 200 },   // Spike
    { duration: '5m', target: 200 },   // High load
    { duration: '5m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],    // <1% failure rate
  },
};

export default function () {
  const response = http.get('https://api.example.com/users');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
### Performance Test Scenarios

yaml
scenarios:
  - name: "Browse catalog"
    weight: 60
    flow:
      - GET /products
      - GET /products/:id

  - name: "Complete purchase"
    weight: 10
    flow:
      - POST /cart
      - POST /checkout
      - GET /orders/confirmation

  - name: "User authentication"
    weight: 30
    flow:
      - POST /auth/login
      - GET /profile
      - POST /auth/logout
---

## Phase 6: Security Testing

### Security Test Categories

| Category | Tools | Focus |
|---|---|---|
| SAST | ESLint security plugins, SonarQube | Code-level vulnerabilities |
| DAST | OWASP ZAP, Burp Suite | Running application testing |
| Dependency | npm audit, Snyk, Dependabot | Known vulnerabilities in packages |
| Secret scanning | Gitleaks, TruffleHog | Committed credentials |

### OWASP Top 10 Checklist

- [ ] **A01: Broken Access Control** — Verify authorization on every endpoint
- [ ] **A02: Cryptographic Failures** — No sensitive data in URLs, proper hashing
- [ ] **A03: Injection** — Parameterized queries, input validation
- [ ] **A04: Insecure Design** — Rate limiting, brute force protection
- [ ] **A05: Security Misconfiguration** — Default creds removed, error handling
- [ ] **A06: Vulnerable Components** — Updated dependencies, no known CVEs
- [ ] **A07: Auth Failures** — Session timeout, secure token handling
- [ ] **A08: Data Integrity Failures** — CSRF tokens, integrity checks
- [ ] **A09: Logging Failures** — Audit logs for sensitive operations
- [ ] **A10: SSRF** — URL validation, block internal IP access

### Security Test Examples

typescript
describe('Security headers', () => {
  it('includes Content-Security-Policy header', async () => {
    const response = await fetch('https://example.com');
    expect(response.headers['content-security-policy']).toBeDefined();
  });
});

describe('Rate limiting', () => {
  it('blocks requests exceeding 100/minute per IP', async () => {
    const requests = Array(150).fill(null).map(() =>
      fetch('/api/search', { method: 'POST', body: JSON.stringify({ q: 'test' }) })
    );

    const results = await Promise.all(requests);
    const rateLimited = results.filter(r => r.status === 429);

    expect(rateLimited.length).toBeGreaterThan(0);
  });
});
---

## Phase 7: Test Automation & CI/CD

### Test Execution Strategy

yaml
pipeline:
  on_push:
    - lint              # Fast, catches obvious issues
    - type_check        # TypeScript types
    - unit_tests        # Fast feedback, high coverage
    - integration_tests # Requires database/service
    - e2e_tests         # Slowest, critical paths only

  on_merge_to_main:
    - full_e2e_suite    # All critical flows
    - performance_tests  # Under load conditions
    - security_scan      # Full vulnerability scan

  scheduled:
    - soak_test         # 8-hour stability test
    - dependency_audit   # Weekly vulnerability check
### Test Reporting

| Report Type | Contents | Audience |
|---|---|---|
| Coverage | Line/branch %, uncovered lines | Developers |
| Trend | Pass/fail over time, flakiness | Team lead, QA |
| Failure analysis | Root cause, affected users | Engineers |
| Executive summary | Quality score, risk assessment | Management |

### Common CI/CD Patterns

yaml
# GitHub Actions example
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:unit
      - run: npm run test:integration
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost/test_db

  e2e:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
      - run: npm run test:e2e
        env:
          BASE_URL: ${{ steps.deploy.outputs.url }}
---

## Phase 8: Test Coverage & Quality Metrics

### Coverage Types

| Type | Measures | Target |
|---|---|---|
| Line coverage | Executed lines | 80%+ |
| Branch coverage | Decision outcomes | 80%+ |
| Function coverage | Called functions | 100% |
| Statement coverage | Individual statements | 90%+ |

### Coverage Anti-Patterns

**Don't chase 100% coverage.** High coverage with low quality tests provides false confidence.

typescript
// ❌ Bad — coverage theater, tests nothing meaningful
it('has a test', () => {
  expect(true).toBe(true);
});

// ✅ Good — tests actual behavior
it('throws error when price is negative', () => {
  expect(() => calculateDiscount(-10)).toThrow('Price must be positive');
});
### Quality Metrics to Track

| Metric | Formula | Target |
|---|---|---|
| Flakiness rate | Failed flaky tests / Total test runs | < 2% |
| MTTD | Mean time to detect defect | < 1 hour |
| MTTR | Mean time to repair | < 4 hours |
| Defect escape rate | Prod bugs / Total bugs | < 15% |

---

## Phase 9: Accessibility Testing

### WCAG 2.1 Requirements (AA Level)

| Principle | Requirement | Test Method |
|---|---|---|
| Perceivable | Alt text for images | Automated + manual review |
| Perceivable | Color contrast 4.5:1 | axe-core, Lighthouse |
| Operable | Keyboard navigation | Manual testing |
| Operable | No seizure-inducing content | Automated check |
| Understandable | Error identification | Manual testing |
| Understandable | Consistent navigation | Manual testing |
| Robust | Valid HTML | W3C validator, axe-core |

### Accessibility Test Examples

typescript
describe('Accessibility', () => {
  it('page has proper heading hierarchy', async () => {
    const { get headings } = await new AxeBuilder({ page })
      .include('main')
      .analyze();

    const headingLevels = headings.map(h => h.level);
    expect(headingLevels).toEqual([1, 2, 2, 3]); // Logical order
  });

  it('form inputs have associated labels', async () => {
    const violations = await new AxeBuilder({ page })
      .include('form')
      .withRules(['label'])
      .analyze();

    expect(violations.length).toBe(0);
  });
});
### Accessibility Checklist

- [ ] All images have meaningful alt text (or `alt=""` for decorative)
- [ ] Color is not the only indicator of state
- [ ] Focus is visible on interactive elements
- [ ] Form errors are announced and explained
- [ ] Page has one `<h1>`, logical heading order
- [ ] Links have descriptive text (not "click here")
- [ ] Touch targets are at least 44x44px
- [ ] Text can be resized to 200% without loss of function

---

## Quick Reference: Test Execution Commands

bash
# Unit tests
npm test                    # Run all unit tests
npm test -- --coverage      # With coverage report
npm test -- --watch         # Watch mode

# Integration tests
npm run test:integration     # Requires services running
npm run test:integration -- --db-reset  # Fresh database

# E2E tests
npm run test:e2e            # Headless
npm run test:e2e -- --headed # Visible browser

# Performance tests
npx k6 run load-test.js
npx artillery run load-test.yml

# Security tests
npm audit                    # Dependency vulnerabilities
npx zap-cli quick-scan https://example.com

# Accessibility tests
npx playwright test --project=a11y
---

## Common Pitfalls & Fixes

| Pitfall | Symptom | Fix |
|---|---|---|
| Brittle selectors | Tests fail on UI changes | Use `data-testid` attributes, semantic HTML |
| Shared mutable state | Flaky tests | Use `beforeEach` cleanup, immutable fixtures |
| Testing implementation | Tests break on refactor | Test behavior, not methods |
| No test isolation | Order-dependent failures | Randomize test order, clean state |
| Slow test suite | Developers skip tests | Parallelize, use test impact analysis |
| No feedback loop | Bugs reach production | Shift left, add pre-commit hooks |

---

*This testing methodology adapts to your project context. Start with Phase 1 (Strategy) and work through phases as needed. Not every project requires every phase — use professional judgment to match testing depth to project risk.*