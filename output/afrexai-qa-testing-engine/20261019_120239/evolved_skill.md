---
category: software-development
description: "> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software."
name: afrexai-qa-testing-engine
---

# QA & Testing Engine — Complete Software Quality System

> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software.

## Phase 1: Test Strategy Design

Before writing a single test, design the strategy.

### Strategy Brief Template

yaml
project:
  name: ""
  type: web-app | api | mobile | library | cli | data-pipeline
  languages: [typescript, python, go, java]
  frameworks: [react, express, django, spring]
  
risk_profile:
  data_sensitivity: low | medium | high | critical  # PII, financial, health
  user_impact: internal | b2b | b2c | life-safety
  deployment_frequency: daily | weekly | monthly
  regulatory: [none, SOC2, HIPAA, PCI-DSS, GDPR]

test_scope:
  in_scope: []    # Features, services, components
  out_of_scope: [] # Explicitly excluded (with reason)
  
environments:
  dev: { url: "", db: "local" }
  staging: { url: "", db: "seeded" }
  prod: { url: "", smoke_only: true }
### Test Type Decision Matrix

| Risk Profile | Unit | Integration | E2E | Performance | Security | Accessibility |
|---|---|---|---|---|---|---|
| Internal tool | ✅ Core | ✅ API | ⚠️ Happy path | ❌ | ⚠️ Basic | ❌ |
| B2B SaaS | ✅ Full | ✅ Full | ✅ Critical flows | ✅ Load | ✅ OWASP Top 10 | ✅ WCAG AA |
| B2C high-traffic | ✅ Full | ✅ Full | ✅ Full | ✅ Stress + soak | ✅ Full | ✅ WCAG AA |
| Financial/Health | ✅ Full + mutation | ✅ Full + contract | ✅ Full + chaos | ✅ Full suite | ✅ Pen test | ✅ WCAG AAA |

### Test Pyramid Architecture

/  E2E  \          5-10% — Critical user journeys only
        / Integration \     20-30% — API contracts, service boundaries
       /    Unit Tests   \  60-70% — Business logic, pure functions
**Anti-pattern: Ice cream cone** — More E2E than unit tests. Slow, flaky, expensive. Fix by pushing test coverage DOWN the pyramid.

**Anti-pattern: Hourglass** — Lots of unit + E2E, no integration. Misses contract bugs between services.

---

## Phase 2: Unit Testing Mastery

### The AAA Pattern (Arrange-Act-Assert)

Every unit test follows this structure:

typescript
describe('PricingCalculator', () => {
  // Group by behavior, not by method
  describe('when customer has volume discount eligibility', () => {
    it('applies 15% discount to total order', () => {
      // Arrange
      const calculator = new PricingCalculator();
      const order = { items: [...], customerTier: 'premium' };
      
      // Act
      const result = calculator.calculate(order);
      
      // Assert
      expect(result.discount).toBe(15);
      expect(result.total).toBeLessThan(order.subtotal);
    });
    
    it('does not apply discount when order is below minimum threshold', () => {
      // Arrange
      const calculator = new PricingCalculator({ minOrderForDiscount: 1000 });
      const order = { items: [...], total: 500, customerTier: 'premium' };
      
      // Act
      const result = calculator.calculate(order);
      
      // Assert
      expect(result.discount).toBe(0);
    });
  });
});
### Naming Conventions

methodname_STATE_EXPECTATION

✅ calculate_nullInput_throwsError
✅ authenticate_expiredToken_returnsUnauthorized
✅ parseDate_invalidFormat_returnsNull

❌ test1
❌ calculateTest
❌ whenUserIsLoggedIn
### Test Doubles

| Type | Use When | Example |
|---|---|---|
| **Stub** | Need specific return values | `getUser() → { id: 1 }` |
| **Spy** | Need to verify calls happened | Track email sent count |
| **Mock** | Need to verify interactions | AuthService called once |
| **Fake** | Need simplified implementation | InMemoryDatabase |

typescript
// Stub — controlled responses
const userService = {
  getUser: jest.fn().mockResolvedValue({ id: 1, name: 'Alice' })
};

// Spy — observation without control
const mailer = { send: jest.fn() };
service.sendWelcome(mailer);
expect(mailer.send).toHaveBeenCalledWith(expect.objectContaining({ to: 'alice@example.com' }));

// Mock — strict expectations
jest.mock('./paymentGateway', () => ({
  charge: jest.fn().mockResolvedValue({ success: true })
}));
### Coverage Thresholds

yaml
statements: 80    # Minimum viable
branches: 75
functions: 80
lines: 80

# Critical business logic
billing:
  statements: 95
  branches: 90
> **Rule**: High coverage ≠ good tests. A 100% covered function with no assertions is worthless. Target meaningful coverage of critical paths.

---

## Phase 3: Integration Testing

### Service Boundary Testing

Test how your service interacts with:
- Databases (queries, migrations, transactions)
- External APIs (contracts, timeouts, retries)
- Message queues (publish/subscribe patterns)
- Caching layers (invalidation, TTL)

python
# pytest + FastAPI
@pytest.fixture
def test_db():
    """Fresh database for each test."""
    db = TestDatabase(seed=True)
    yield db
    db.cleanup()

@pytest.fixture
def api_client(test_db):
    """Authenticated test client."""
    return TestClient(app, headers={
        "Authorization": f"Bearer {generate_test_token()}"
    })

def test_create_order_updates_inventory(api_client, test_db):
    # Arrange
    initial_stock = test_db.get_product_stock("SKU-001")
    
    # Act
    response = api_client.post("/orders", json={
        "items": [{"sku": "SKU-001", "quantity": 2}]
    })
    
    # Assert
    assert response.status_code == 201
    assert test_db.get_product_stock("SKU-001") == initial_stock - 2
    
    # Verify audit log
    assert test_db.audit_log[-1].action == "ORDER_CREATED"
### Contract Testing (Pact)

typescript
// consumer-pact.ts
const interaction = {
  state: 'user with id 123 exists',
  uponReceiving: 'a request for user 123',
  withRequest: {
    method: 'GET',
    path: '/users/123',
    headers: { Accept: 'application/json' }
  },
  willRespondWith: {
    status: 200,
    body: {
      id: 123,
      name: 'Alice',
      email: 'alice@example.com'
    }
  }
};
---

## Phase 4: End-to-End Testing

### When to Write E2E Tests

| Criteria | Write E2E? |
|---|---|
| Critical user journey (checkout, auth, signup) | ✅ Always |
| Complex multi-step workflow | ✅ Always |
| Cross-browser rendering | ✅ Always |
| Happy path variations | ⚠️ Limited |
| Edge cases | ❌ Never (unit test) |
| Data processing logic | ❌ Never (unit test) |

### Playwright Best Practices

typescript
// ✅ Page Object Model — reduce duplication
class LoginPage {
  constructor(private page: Page) {}
  
  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email-input"]', email);
    await this.page.fill('[data-testid="password-input"]', password);
    await this.page.click('[data-testid="submit-button"]');
  }
}

// ✅ Use test IDs, not selectors
await page.click('[data-testid="add-to-cart"]');

// ❌ Fragile selectors
await page.click('.product-list > div:nth-child(3) > button');

// ✅ Explicit waits over arbitrary delays
await page.waitForResponse('**/api/checkout');

// ❌ Never use sleep
await page.waitForTimeout(2000);
### E2E Test Organization

tests/
├── e2e/
│   ├── critical/           # Must pass before release
│   │   ├── auth.spec.ts
│   │   ├── checkout.spec.ts
│   │   └── account-deletion.spec.ts
│   ├── smoke/              # Quick sanity checks
│   │   └── health.spec.ts
│   └── regression/         # Full suite, runs nightly
│       └── full-journey.spec.ts
---

## Phase 5: Performance Testing

### Test Types

| Type | Purpose | Duration |
|---|---|---|
| **Load** | Normal expected traffic | 15-30 min |
| **Stress** | Breaking point identification | 30-60 min |
| **Soak** | Memory leaks, degradation | 4-8 hours |
| **Spike** | Sudden traffic bursts | 10-30 min |

### k6 Scripting

javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },   // Steady state
    { duration: '2m', target: 200 },   // Stress
    { duration: '5m', target: 200 },   // Steady state
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],   // Error rate < 1%
  },
};

export default function() {
  const res = http.get('https://api.example.com/products');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
### Performance Budget

yaml
api:
  p50_latency: < 50ms
  p95_latency: < 200ms
  p99_latency: < 500ms
  error_rate: < 0.1%

frontend:
  LCP: < 2.5s
  FID: < 100ms
  CLS: < 0.1
  bundle_size: < 250kb gzipped
---

## Phase 6: Security Testing

### OWASP Top 10 Checklist

typescript
// Security test examples
describe('Security Tests', () => {
  it('prevents SQL injection in search', async () => {
    const response = await request(app)
      .get('/search?q=' + '\'; DROP TABLE users; --');
    
    expect(response.status).not.toBe(500);
    expect(response.body).not.toContain('SQL');
  });
  
  it('enforces rate limiting on login endpoint', async () => {
    const attempts = Array(101).fill(null).map(() => 
      request(app).post('/auth/login')
    );
    
    const responses = await Promise.all(attempts);
    const lastResponse = responses[responses.length - 1];
    
    expect(lastResponse.status).toBe(429);
  });
  
  it('sets secure cookie attributes', async () => {
    const response = await request(app).post('/auth/login');
    const cookie = response.headers['set-cookie'][0];
    
    expect(cookie).toContain('HttpOnly');
    expect(cookie).toContain('Secure');
    expect(cookie).toContain('SameSite=Strict');
  });
});
### Security Headers to Test

✅ Content-Security-Policy
✅ X-Frame-Options: DENY
✅ X-Content-Type-Options: nosniff
✅ Strict-Transport-Security
✅ X-XSS-Protection
✅ Referrer-Policy: strict-origin-when-cross-origin
---

## Phase 7: Test Execution & Reporting

### CI/CD Pipeline Integration

yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run unit tests
        run: npm test -- --coverage --ci
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
      redis:
        image: redis:7
    steps:
      - uses: actions/checkout@v4
      - name: Run integration tests
        run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run critical E2E
        run: npx playwright test --project=critical
        if: github.event_name == 'push'

  performance-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run k6 load test
        run: k6 run load-test.js
    # Runs on schedule, not every push
### Test Reports That Matter

| Metric | Target | Action if Breached |
|---|---|---|
| **Flaky test rate** | < 1% | Immediate investigation |
| **Test duration** | Unit < 5min, E2E < 30min | Parallelization |
| **Coverage trend** | Stable or increasing | Reject PRs decreasing coverage |
| **Bug escape rate** | < 5% in prod | Improve test design |

### Test Report Template

markdown
## Test Report — Sprint 42

### Summary
- **Total Tests**: 847
- **Passed**: 844 (99.6%)
- **Failed**: 2 (flaky, under investigation)
- **Skipped**: 1 (feature delayed)

### Coverage
- Statements: 87% (+2%)
- Branches: 82% (+1%)
- Functions: 91% (stable)

### Quality Gates
- [x] All critical E2E passing
- [x] No new security vulnerabilities
- [x] Performance within budget
- [x] Accessibility audit passed

### Risk Assessment
⚠️ New payment integration has 2 integration tests (expand before launch)
✅ Auth refactor fully covered

### Recommendation
**APPROVED** for staging deployment
---

## Quick Reference

### Test Selection Decision Tree

Is it business logic or pure function?
├── YES → Unit test (100% coverage target)
└── NO → Continue

Is it service boundary interaction?
├── YES → Integration test (Pact if external)
└── NO → Continue

Is it critical user journey?
├── YES → E2E test (Playwright/Cypress)
└── NO → Skip (unit covers behavior)
### Anti-Patterns Quick List

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Testing implementation | Breaks on refactor | Test behavior, not internals |
| Shared mutable state | Flaky tests | Fresh fixtures per test |
| Asserting on timestamps | Random failures | Mock time or use windows |
| Deep equality on entire objects | Brittle | Assert specific fields |
| Tests that depend on order | Parallelization blocked | Isolation per test |

### Essential Tools by Language

| Language | Unit | Integration | E2E | Performance |
|---|---|---|---|---|
| JavaScript/TypeScript | Jest, Vitest | Supertest | Playwright, Cypress | k6, Lighthouse |
| Python | pytest, unittest | pytest-django, httpx | Playwright | k6, locust |
| Go | testing, testify | go-sqlmock | Playwright | k6, hey |
| Java | JUnit 5, Spock | TestContainers | Playwright | JMeter, Gatling |

---

> **Remember**: Tests are documentation. Write them for the developer who will maintain this code in 6 months — including future you.