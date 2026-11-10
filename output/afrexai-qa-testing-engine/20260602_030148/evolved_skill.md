---
category: software-development
description: "> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software."
name: afrexai-qa-testing-engine
---

# QA & Testing Engine — Complete Software Quality System

> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software.

## Overview

This skill provides a structured, risk-based approach to software quality assurance. Follow the phases in order:

1. **Strategy Design** — Define scope, risk profile, and test types
2. **Unit Testing** — Test individual functions and business logic
3. **Integration Testing** — Verify service boundaries and API contracts
4. **End-to-End Testing** — Validate complete user workflows
5. **Specialized Testing** — Performance, security, accessibility
6. **Execution & Reporting** — Run tests and communicate results

---

## Phase 1: Test Strategy Design

Design your testing approach before writing any tests. A solid strategy prevents wasted effort on low-value tests while ensuring critical paths are covered.

### Strategy Brief Template

yaml
project:
  name: "Project identifier"
  type: web-app | api | mobile | library | cli | data-pipeline
  languages: [typescript, python, go, java]
  frameworks: [react, express, django, spring]
  
risk_profile:
  data_sensitivity: low | medium | high | critical
  # low: public data, internal tools
  # medium: user accounts, preferences
  # high: PII, financial records, health data
  # critical: payment processing, medical systems
  
  user_impact: internal | b2b | b2c | life-safety
  deployment_frequency: daily | weekly | monthly
  regulatory: [none, SOC2, HIPAA, PCI-DSS, GDPR]

test_scope:
  in_scope: []
  # List specific features, services, or components to test
  
  out_of_scope: []
  # Explicitly excluded items with justification

environments:
  dev: { url: "", db: "local" }
  staging: { url: "", db: "seeded" }
  prod: { url: "", smoke_only: true }
### Test Type Decision Matrix

Use this matrix to determine which test types to invest in based on your risk profile:

| Risk Profile | Unit | Integration | E2E | Performance | Security | Accessibility |
|---|---|---|---|---|---|---|
| Internal tool | ✅ Core logic | ✅ API | ⚠️ Happy path | ❌ | ⚠️ Basic auth | ❌ |
| B2B SaaS | ✅ Full | ✅ Full | ✅ Critical flows | ✅ Load tests | ✅ OWASP Top 10 | ✅ WCAG AA |
| B2C high-traffic | ✅ Full | ✅ Full | ✅ Full suite | ✅ Stress + soak | ✅ Full | ✅ WCAG AA |
| Financial/Health | ✅ Full + mutation | ✅ Full + contract | ✅ Full + chaos | ✅ Full suite | ✅ Pen test | ✅ WCAG AAA |

### Test Pyramid

The test pyramid guides where to invest your testing effort:

/  E2E  \          5-10% — Critical user journeys only
        / Integration \     20-30% — API contracts, service boundaries
       /    Unit Tests   \  60-70% — Business logic, pure functions
**Foundation**: Most tests should be unit tests — they're fast, reliable, and cheap to maintain.

**Anti-Patterns to Avoid**:

| Anti-Pattern | Problem | Solution |
|---|---|---|
| **Ice cream cone** | More E2E than unit tests | Push coverage down the pyramid |
| **Hourglass** | Unit + E2E, no integration | Add contract testing between services |
| **Cookie jar** | Only test easy paths | Cover edge cases, error handling, boundaries |

---

## Phase 2: Unit Testing Mastery

Unit tests verify individual functions, classes, and modules in isolation. They form the foundation of your test suite.

### The AAA Pattern

Structure every test with **Arrange-Act-Assert**:

typescript
describe('PricingCalculator', () => {
  // Group tests by behavior, not by method name
  describe('when customer has volume discount eligibility', () => {
    
    it('applies 15% discount for orders over $1000', () => {
      // Arrange
      const calculator = new PricingCalculator();
      const order = { items: [...], subtotal: 1500 };
      
      // Act
      const result = calculator.calculateTotal(order);
      
      // Assert
      expect(result.total).toBe(1275); // 15% off
      expect(result.discountApplied).toBe(0.15);
    });
    
    it('does not apply discount below $1000 threshold', () => {
      const result = new PricingCalculator().calculateTotal({ subtotal: 500 });
      expect(result.discountApplied).toBe(0);
    });
    
    it('caps total discount at $500 per order', () => {
      const result = new PricingCalculator().calculateTotal({ subtotal: 10000 });
      expect(result.totalDiscount).toBeLessThanOrEqual(500);
    });
  });
});
### What to Test

**✅ Test these**:

- Business logic and calculations
- Input validation and boundary conditions
- Error handling paths
- State transitions
- Pure functions with predictable outputs

**❌ Don't test these**:

- Framework internals (let maintainers test those)
- Trivial getters/setters (test the logic, not the accessors)
- Third-party library code
- Private implementation details

### Naming Conventions

Use descriptive test names that document expected behavior:

typescript
// ❌ Poor: "test1", "shouldWork"
test('valid email returns true');
should('work');

// ✅ Excellent: Documents behavior and edge cases
test('returns true when email matches RFC 5322 pattern');
test('returns false when email exceeds 254 character limit');
test('returns false when domain has no TLD');
### Mocking Strategy

Mock only external dependencies, never internal modules:

typescript
// ✅ Correct: Mock external services
jest.mock('./emailService');
jest.mock('./paymentGateway');

// ❌ Incorrect: Mocking your own modules
jest.mock('./validators'); // Don't mock what you're testing
### Coverage Targets

| Component Type | Target Coverage |
|---|---|
| Business logic / services | 90%+ |
| Utility functions | 85%+ |
| Controllers / handlers | 70%+ |
| UI components | 60%+ (behavior) |

---

## Phase 3: Integration Testing

Integration tests verify that components work correctly together, focusing on API contracts, database interactions, and service boundaries.

### API Contract Testing

Verify API responses match expected schemas:

typescript
// Using Pact or OpenAPI validators
describe('User API Contract', () => {
  it('returns user object matching schema', async () => {
    const response = await request(app).get('/api/users/123');
    
    expect(response.status).toBe(200);
    expect(response.body).toMatchSchema({
      id: { type: 'string', format: 'uuid' },
      email: { type: 'string', format: 'email' },
      createdAt: { type: 'string', format: 'date-time' },
      role: { enum: ['admin', 'user', 'viewer'] }
    });
  });
  
  it('rejects requests without required authentication', async () => {
    const response = await request(app).get('/api/users/123');
    expect(response.status).toBe(401);
  });
});
### Database Integration Tests

Test data layer interactions with real or containerized databases:

typescript
describe('UserRepository', () => {
  let db: TestDatabase;
  
  beforeEach(async () => {
    db = await TestDatabase.create();
  });
  
  afterEach(async () => {
    await db.cleanup();
  });
  
  it('persists user and retrieves by id', async () => {
    const user = await db.users.create({
      email: 'test@example.com',
      name: 'Test User'
    });
    
    const retrieved = await db.users.findById(user.id);
    
    expect(retrieved.email).toBe('test@example.com');
  });
  
  it('throws on duplicate email', async () => {
    await db.users.create({ email: 'taken@example.com' });
    
    await expect(
      db.users.create({ email: 'taken@example.com' })
    ).rejects.toThrow('Email already exists');
  });
});
### Service-to-Service Integration

Test communication between internal services:

typescript
describe('OrderService → InventoryService', () => {
  it('decrements inventory when order is placed', async () => {
    const initialStock = await inventoryService.getStock('SKU-001');
    
    await orderService.placeOrder({
      items: [{ sku: 'SKU-001', quantity: 2 }]
    });
    
    const newStock = await inventoryService.getStock('SKU-001');
    expect(newStock).toBe(initialStock - 2);
  });
});
---

## Phase 4: End-to-End Testing

E2E tests simulate real user workflows through the complete application stack. Keep these focused and minimal — they are slow and fragile.

### When to Use E2E

- Critical user journeys (login, checkout, submission)
- Multi-step workflows spanning multiple pages
- Third-party integrations (payment, auth providers)

### Page Object Model

Structure E2E tests for maintainability:

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
    await this.page.click('[data-testid="login-button"]');
  }
  
  getErrorMessage() {
    return this.page.textContent('[data-testid="error-message"]');
  }
}

// tests/login.spec.ts
test('shows error for invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('wrong@example.com', 'wrongpass');
  
  expect(loginPage.getErrorMessage()).toContain('Invalid credentials');
});
### Critical User Journeys

Identify and prioritize flows:

| Priority | Flow | Why |
|---|---|---|
| P0 | Sign up / Sign in | Gate to all other features |
| P0 | Complete purchase | Revenue critical |
| P0 | Password reset | Security requirement |
| P1 | Profile update | User trust |
| P1 | Search and browse | Core engagement |
| P2 | Settings changes | Lower impact |

### Handling Flakiness

E2E tests are inherently unstable. Mitigate with:

typescript
// 1. Wait for specific conditions, not arbitrary delays
await page.waitForSelector('[data-testid="success-message"]');

// 2. Use test retries sparingly
// playwright.config.ts
export default {
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined
};

// 3. Isolate test data per test
test('unique test', async ({ page }) => {
  const testEmail = `test-${Date.now()}@example.com`;
  // Each run gets unique data
});
---

## Phase 5: Specialized Testing

### Performance Testing

**Load Testing**: Verify system behavior under expected traffic:

typescript
// Using k6
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Steady state
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% under 500ms
    http_req_failed: ['rate<0.01'],   // Less than 1% failures
  },
};

export default function() {
  const res = http.get('https://api.example.com/products');
  check(res, { 'status was 200': (r) => r.status === 200 });
  sleep(1);
}
**Stress Testing**: Find breaking points:

typescript
export const options = {
  stages: [
    { duration: '1m', target: 1000 },  // Rapid increase
    { duration: '5m', target: 1000 },
    { duration: '1m', target: 5000 }, // Exceed capacity
  ],
};
**Soak Testing**: Find memory leaks over time:

typescript
export const options = {
  duration: '60m',
  vus: 50,
  // Monitor for: memory growth, increasing response times, errors
};
### Security Testing

**OWASP Top 10 Coverage**:

| Vulnerability | Test Approach |
|---|---|
| Injection | Test SQL/NoSQL/command injection vectors |
| Broken Auth | Test weak passwords, session handling |
| Sensitive Data | Verify encryption, no exposure in logs |
| XXE | Test XML upload/parsing |
| Broken Access | Test authorization between roles |
| Misconfiguration | Verify security headers, defaults |
| XSS | Test reflected/stored XSS vectors |
| Insecure Deserialization | Test malicious payloads |
| Vulnerable Components | Scan dependencies for CVEs |
| Insufficient Logging | Verify audit trail completeness |

typescript
describe('Security: Authentication', () => {
  it('locks account after 5 failed attempts', async () => {
    for (let i = 0; i < 5; i++) {
      await api.login('user@example.com', 'wrongpassword');
    }
    
    const response = await api.login('user@example.com', 'correctpassword');
    expect(response.status).toBe(423); // Locked
  });
  
  it('session expires after 30 minutes of inactivity', async () => {
    await api.login('user@example.com', 'password');
    await page.waitForTimeout(31 * 60 * 1000); // 31 minutes
    
    const response = await api.get('/api/user/profile');
    expect(response.status).toBe(401);
  });
});
### Accessibility Testing

Ensure your application is usable by people with disabilities.

**WCAG 2.1 AA Requirements**:

| Criterion | Implementation |
|---|---|
| Color contrast | 4.5:1 for normal text, 3:1 for large |
| Keyboard navigation | All interactive elements reachable |
| Screen reader support | Proper ARIA labels, semantic HTML |
| Focus indicators | Visible focus states |
| Form labels | All inputs have associated labels |
| Error identification | Errors described in text, not color alone |

typescript
describe('Accessibility', () => {
  it('page has proper heading hierarchy', async () => {
    const headings = await page.evaluate(() => {
      const hs = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
      return Array.from(hs).map(h => h.tagName);
    });
    
    // Should be: H1, H2, H3... not H1, H3, H2
    expect(headings).toEqual(['H1', 'H2', 'H3']);
  });
  
  it('all form inputs have labels', async () => {
    const inputs = await page.$$('input');
    for (const input of inputs) {
      const id = await input.getAttribute('id');
      const label = await page.$(`label[for="${id}"]`);
      expect(label).not.toBeNull();
    }
  });
});
---

## Phase 6: Execution & Reporting

### Test Execution Strategy

**Development Phase**:

bash
# Run unit tests on every file change
npm run test:unit -- --watch

# Run relevant tests when editing a module
npm run test:unit -- src/auth/login.test.ts
**Pre-merge Pipeline**:

bash
# Fast feedback: unit + integration only
npm run test:unit && npm run test:integration
**Post-merge Pipeline**:

bash
# Full suite including slow E2E tests
npm run test:unit
npm run test:integration
npm run test:e2e
npm run test:performance
npm run test:security
### CI/CD Integration

yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:e2e
### Test Reporting

**Coverage Reports**:

Generate coverage reports to identify untested code:

bash
npm run test:unit -- --coverage --coverageReporters=lcov
Target thresholds to maintain quality:

json
{
  "coverageThreshold": {
    "global": { "branches": 70, "functions": 70, "lines": 70, "statements": 70 },
    "src/services/": { "branches": 90, "functions": 90, "lines": 90 }
  }
}
**Test Results Dashboard**:

Track metrics over time:

| Metric | Target | Action if Breached |
|---|---|---|
| Test pass rate | > 99% | Block deployments |
| Flaky test rate | < 1% | Triage and fix |
| Coverage | > 80% | Add missing tests |
| Avg test duration | < 100ms (unit) | Optimize slow tests |
| E2E stability | > 95% | Fix infrastructure issues |

### Bug Triage Process

When tests fail, classify appropriately:

| Classification | Definition | Action |
|---|---|---|
| **Flaky** | Fails intermittently, passes on retry | Investigate timing, fix test |
| **Environment** | Fails due to infrastructure | Fix env, skip if third-party |
| **Regression** | New code broke existing behavior | Revert, fix code |
| **New Failure** | Existing test failed for new reason | Analyze, update test or code |

---

## Quick Reference

### Test Selection Flowchart

Is it a pure function?
├── YES → Unit test
└── NO → Does it involve external services?
    ├── YES → Integration test
    └── NO → Is it a critical user journey?
        ├── YES → E2E test
        └── NO → Still needed? Consider if value justifies cost
### Command Summary

| Command | Purpose |
|---|---|
| `npm run test:unit` | Run unit tests |
| `npm run test:unit -- --watch` | Watch mode for development |
| `npm run test:unit -- --coverage` | Generate coverage report |
| `npm run test:integration` | Run integration tests |
| `npm run test:e2e` | Run E2E tests |
| `npm run test:perf` | Run performance tests |
| `npm run test:all` | Run full test suite |

---

## Anti-Patterns Summary

| Anti-Pattern | Symptom | Solution |
|---|---|---|
| Testing implementation | Tests break on refactor | Test behavior, not internals |
| Excessive mocking | Tests pass but app breaks | Test with real dependencies when safe |
| Brittle assertions | Tests fail on whitespace changes | Test meaningful content only |
| Test interdependency | Order matters for tests | Make each test self-contained |
| Goldenmaster testing | Tests compare to saved outputs | Assert expected values explicitly |
| Skip, not fix | `test.skip()` everywhere | Fix tests or delete them |