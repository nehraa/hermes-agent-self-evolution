---
category: software-development
description: "> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software."
name: afrexai-qa-testing-engine
---

# QA & Testing Engine — Complete Software Quality System

> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software.

---

## Phase 1: Test Strategy Design

Before writing a single test, establish your strategy. This prevents common failures: missing coverage areas, over-investment in low-value tests, and unclear quality gates.

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
  in_scope: []      # Features, services, components under test
  out_of_scope: []  # Explicitly excluded (with business reason)
  
environments:
  dev: { url: "", db: "local", purpose: "Development iteration" }
  staging: { url: "", db: "seeded", purpose: "Integration & QA" }
  prod: { url: "", smoke_only: true, purpose: "Smoke verification only" }

quality_gates:
  min_coverage: 80          # Line coverage threshold
  max_flaky_rate: 2         # Allowable flaky test percentage
  blocker_issues: []        # Issue types that block deployment
  required_approvals: 1     # Number of required reviewers
### Test Type Decision Matrix

Choose your testing investment based on risk and impact:

| Risk Profile | Unit | Integration | E2E | Performance | Security | Accessibility |
|-------------|------|-------------|-----|-------------|----------|---------------|
| Internal tool | ✅ Core logic | ✅ API layer | ⚠️ Happy path only | ❌ | ⚠️ Basic auth | ❌ |
| B2B SaaS | ✅ Full suite | ✅ Full suite | ✅ Critical flows | ✅ Load testing | ✅ OWASP Top 10 | ✅ WCAG AA |
| B2C high-traffic | ✅ Full suite | ✅ Full suite | ✅ Comprehensive | ✅ Stress + soak | ✅ Full security | ✅ WCAG AA |
| Financial/Health | ✅ Full + mutation | ✅ Full + contract | ✅ Full + chaos | ✅ Full suite | ✅ Pen test required | ✅ WCAG AAA |

### Test Pyramid Architecture

/  E2E  \          5-10% — Critical user journeys only
        / Integration \     20-30% — API contracts, service boundaries
       /    Unit Tests   \  60-70% — Business logic, pure functions
**Anti-pattern: Ice cream cone** — More E2E than unit tests. Results: slow pipelines, flaky suites, expensive maintenance. Fix by migrating E2E coverage down to unit/integration levels.

**Anti-pattern: Hourglass** — Lots of unit + E2E, no integration. Results: contract bugs, missed service integration failures, late discovery. Fix by adding integration tests at service boundaries.

---

## Phase 2: Unit Testing Mastery

### The AAA Pattern (Arrange-Act-Assert)

Every unit test follows this structure:

typescript
describe('PricingCalculator', () => {
  // Group by behavior, not by method name
  describe('when customer has volume discount eligibility', () => {
    
    // ARRANGE: Set up test data and conditions
    const customer = createCustomer({ tier: 'gold', lifetimeValue: 50000 });
    const pricingRequest = { basePrice: 1000, quantity: 100 };
    
    // ACT: Execute the behavior under test
    const result = calculatePrice(customer, pricingRequest);
    
    // ASSERT: Verify the expected outcome
    expect(result.finalPrice).toBe(85000); // 15% volume discount applied
    expect(result.discountApplied).toBe(true);
  });
});
### Naming Convention

Use the format: `should_[expected behavior]_when_[condition]`

| Bad Name | Good Name |
|----------|-----------|
| `test1` | `should return 404 when user does not exist` |
| `testCalculate` | `should apply tier discount when order exceeds $1000` |
| `errorTest` | `should throw ValidationError when email format is invalid` |

### Mocking Strategy

Mock at the boundary of your system, not inside it:

typescript
// ✅ GOOD: Mock external dependencies
describe('OrderService', () => {
  it('should send confirmation email on successful order', async () => {
    const mockEmailService = { send: jest.fn().mockResolvedValue(true) };
    const orderService = new OrderService({
      emailService: mockEmailService,
      // Real implementations for internal dependencies
    });
    
    await orderService.createOrder(testOrder);
    
    expect(mockEmailService.send).toHaveBeenCalledWith({
      to: testOrder.customerEmail,
      subject: 'Order Confirmed',
    });
  });
});
### Test Coverage Requirements

| Component Type | Target Coverage | Critical Paths |
|----------------|-----------------|----------------|
| Business logic | 90%+ | All branches, edge cases |
| Data models | 80%+ | Validation, transformation |
| Utilities | 95%+ | All input combinations |
| Controllers | 70%+ | Happy path, key error cases |
| UI components | 60%+ | User interactions, states |

---

## Phase 3: Integration Testing

### API Contract Testing

Define contracts explicitly and test against them:

yaml
# contract: user-service.yaml
openapi: "3.0.0"
paths:
  /users/{id}:
    get:
      responses:
        200:
          schema:
            type: object
            properties:
              id: { type: string, format: uuid }
              email: { type: string, format: email }
              createdAt: { type: string, format: date-time }
typescript
// consumer-side contract test
describe('User Service Integration', () => {
  it('should handle pagination parameters correctly', async () => {
    const response = await api.get('/users?page=2&limit=50');
    
    expect(response.status).toBe(200);
    expect(response.headers['x-total-count']).toBeDefined();
    expect(response.data).toHaveLength(50);
    expect(response.data[0].id).toMatch(/^[0-9a-f-]{36}$/);
  });
});
### Database Integration Tests

typescript
describe('UserRepository', () => {
  beforeEach(async () => {
    await db.query('BEGIN');
    await seedTestData();
  });
  
  afterEach(async () => {
    await db.query('ROLLBACK'); // Isolated, no side effects
  });
  
  it('should find users by email case-insensitively', async () => {
    const user = await userRepo.findByEmail('Test@Example.com');
    
    expect(user).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });
});
### Service-to-Service Tests

typescript
describe('Order Processing Pipeline', () => {
  it('should update inventory when order is placed', async () => {
    const initialStock = await inventoryService.getStock(PRODUCT_ID);
    
    await orderService.placeOrder({ productId: PRODUCT_ID, quantity: 5 });
    
    const updatedStock = await inventoryService.getStock(PRODUCT_ID);
    expect(updatedStock).toBe(initialStock - 5);
  });
  
  it('should rollback inventory on payment failure', async () => {
    const initialStock = await inventoryService.getStock(PRODUCT_ID);
    
    await expect(
      orderService.placeOrder({ 
        productId: PRODUCT_ID, 
        quantity: 5, 
        paymentMethod: 'invalid' 
      })
    ).rejects.toThrow('Payment declined');
    
    const finalStock = await inventoryService.getStock(PRODUCT_ID);
    expect(finalStock).toBe(initialStock); // Inventory restored
  });
});
---

## Phase 4: End-to-End Testing

### Critical User Journey Selection

Identify 5-15 journeys that represent core business value:

1. User registration and email verification
2. Authentication (login/logout/reset)
3. Core transaction flow (purchase, booking, submission)
4. Critical data operations (create, update, delete)
5. Error and recovery scenarios

### E2E Test Structure

typescript
// test/e2e/checkout.spec.ts
describe('Checkout Flow', () => {
  beforeEach(async () => {
    await page.goto('/cart');
    await page.addToCart(VALID_PRODUCT_ID);
  });
  
  it('should complete purchase with valid payment', async () => {
    await page.fill('[data-testid="email"]', 'customer@example.com');
    await page.fill('[data-testid="card-number"]', '4242424242424242');
    await page.fill('[data-testid="expiry"]', '12/26');
    await page.fill('[data-testid="cvc"]', '123');
    await page.click('[data-testid="submit-payment"]');
    
    await expect(page.locator('.success-message')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('.order-id')).toContainText(/^ORD-\d+$/);
  });
  
  it('should show validation errors for invalid card', async () => {
    await page.fill('[data-testid="card-number"]', 'invalid');
    await page.click('[data-testid="submit-payment"]');
    
    await expect(page.locator('.error-message')).toContainText('Invalid card number');
  });
});
### Test Data Management

typescript
// factories/testData.ts
export const testUsers = {
  valid: {
    email: 'testuser@example.com',
    password: 'SecurePass123!',
    verified: true,
  },
  invalid: {
    email: 'not-an-email',
    password: '123',
    verified: false,
  },
};

export const testProducts = {
  inStock: { id: 'prod_123', stock: 100, price: 29.99 },
  lowStock: { id: 'prod_456', stock: 2, price: 49.99 },
  outOfStock: { id: 'prod_789', stock: 0, price: 19.99 },
};
---

## Phase 5: Performance Testing

### Load Test Scenarios

typescript
// test/performance/load.spec.ts
import k6 from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },   // Steady state
    { duration: '2m', target: 200 },   // Stress
    { duration: '5m', target: 200 },   // Steady high
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],    // Less than 1% failures
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
### Performance Thresholds

| Endpoint Type | P50 | P95 | P99 | Max Failure Rate |
|---------------|-----|-----|-----|------------------|
| Simple read | <50ms | <100ms | <200ms | <0.1% |
| API call | <100ms | <250ms | <500ms | <0.5% |
| Complex query | <200ms | <500ms | <1s | <1% |
| File upload | <1s | <3s | <5s | <1% |
| Payment processing | <500ms | <1s | <2s | <0.01% |

---

## Phase 6: Security Testing

### OWASP Top 10 Coverage

| Vulnerability | Test Strategy | Automation |
|--------------|---------------|------------|
| Injection | Fuzz inputs, verify sanitization | ✅ SAST + DAST |
| Broken Auth | Test session management, token handling | ✅ Integration tests |
| Sensitive Data | Verify encryption, masking in logs | ✅ Automated scanning |
| XXE | Test XML parsing endpoints | ✅ Dependency check |
| Broken Access | Test authorization across roles | ✅ Role-based tests |
| Security Misconfig | Verify headers, defaults | ✅ Config audits |
| XSS | Reflected, stored, DOM XSS tests | ✅ Automated + manual |
| Insecure Deserialization | Fuzz deserialization endpoints | ✅ Fuzzing suite |
| Using Components with Known Vulnerabilities | Dependency scanning | ✅ CI/CD integration |
| Insufficient Logging | Verify audit trail completeness | ✅ Log analysis |

### Security Test Examples

typescript
describe('Authentication Security', () => {
  it('should lock account after 5 failed login attempts', async () => {
    for (let i = 0; i < 5; i++) {
      await api.post('/auth/login', {
        email: 'target@example.com',
        password: 'wrongpassword',
      });
    }
    
    const response = await api.post('/auth/login', {
      email: 'target@example.com',
      password: 'CorrectPassword123!',
    });
    
    expect(response.status).toBe(423); // Locked
    expect(response.data.message).toContain('account locked');
  });
  
  it('should not reveal user existence in error messages', async () => {
    const response = await api.post('/auth/login', {
      email: 'nonexistent@example.com',
      password: 'anypassword',
    });
    
    // Should show generic message, not "User not found"
    expect(response.data.message).toBe('Invalid credentials');
  });
});
---

## Phase 7: Test Reporting & Metrics

### Required Metrics Dashboard

Track these metrics at minimum:

yaml
metrics:
  coverage:
    line_coverage: 85    # Target: 80%+
    branch_coverage: 75 # Target: 70%+
    function_coverage: 90
    
  quality:
    test_flakiness_rate: 2    # Target: <2%
    avg_test_duration_ms: 150
    suite_pass_rate: 98
    
  risk:
    critical_bugs_in_prod: 0
    security_vulnerabilities: 0
    ux_blockers: 0
    
  velocity:
    tests_per_pr: 15
    review_time_hours: 4
    failed_build_recovery_minutes: 30
### Test Report Structure

Every test run should produce:

markdown
# Test Execution Report — [DATE]

## Summary
- **Total Tests**: 1,247
- **Passed**: 1,241 (99.5%)
- **Failed**: 6 (0.5%)
- **Skipped**: 0
- **Duration**: 4m 32s

## Failed Tests (Action Required)
| Test | Error | Frequency | Priority |
|------|-------|-----------|----------|
| checkout/payment_decline | Timeout on Stripe API | Intermittent | High |
| auth/session_expire | Token refresh race condition | Consistent | Critical |

## Coverage Summary
- **Lines**: 85.3% (+0.2% from main)
- **Branches**: 74.1% (-0.5% from main)
- **New Code**: 100% covered

## Recommendations
1. Investigate payment timeout — may indicate Stripe API degradation
2. Review session refresh logic for race conditions
---

## Phase 8: CI/CD Integration

### Pipeline Test Gates

yaml
# .github/workflows/test.yml
stages:
  - name: unit-tests
    trigger: [push, pr]
    required: true
    timeout: 10m
    coverage_threshold: 80
    
  - name: integration-tests
    trigger: [push, pr]
    required: true
    timeout: 20m
    requires: [unit-tests]
    
  - name: e2e-tests
    trigger: [push to staging, release]
    required: true
    timeout: 30m
    requires: [integration-tests]
    
  - name: security-scan
    trigger: [push, pr, schedule]
    required: true
    timeout: 15m
    blocker: [high, critical vulnerabilities]
    
  - name: performance-tests
    trigger: [push to staging, schedule]
    required: false
    timeout: 45m
    warning_threshold: p95 > 500ms
### Quality Gates Checklist

Before any deployment:

- [ ] All unit tests pass (100%)
- [ ] Coverage meets threshold (80%+)
- [ ] No new high/critical security vulnerabilities
- [ ] Integration tests pass
- [ ] E2E smoke tests pass
- [ ] Performance baselines maintained
- [ ] No blocking accessibility violations
- [ ] Code review approved
- [ ] Documentation updated (if required)

---

## Quick Reference Card

### Test Selection Flowchart

Is it a pure function/class?
├─ YES → Unit test (Arrange-Act-Assert)
└─ NO → Does it involve service boundaries?
        ├─ YES → Integration test
        └─ NO → Is it a user journey?
                ├─ YES → E2E test (critical paths only)
                └─ NO → Consider: is this worth testing at all?
### When to Use Each Test Type

| Use Case | Test Type | Example |
|----------|-----------|---------|
| Validate business logic | Unit | Price calculation, discount rules |
| Verify data persistence | Unit + Integration | Repository methods |
| Check API contracts | Integration | Endpoint responses, headers |
| Confirm multi-service flow | Integration | Order → Payment → Inventory |
| Verify user-facing behavior | E2E | Complete checkout, registration |
| Measure response under load | Performance | Concurrent user simulation |
| Find security vulnerabilities | Security | Auth bypass, injection, XSS |

### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Testing implementation | Brittle tests, constant breaks | Test behavior, not internals |
| Shared mutable state | Flaky tests, order dependency | Use setup/teardown, factories |
| Over-mocking | Tests pass but app breaks | Mock at boundaries only |
| One test per method | Unclear purpose, duplication | One test per behavior/scenario |
| No test data strategy | Inconsistent data, hidden coupling | Use factories and fixtures |

---

## Appendix: Testing Checklist by Project Type

### Web Application
- [ ] Unit tests for components and hooks
- [ ] Integration tests for API routes
- [ ] E2E tests for registration, login, primary user flows
- [ ] Accessibility tests (WCAG AA compliance)
- [ ] Cross-browser compatibility tests
- [ ] Performance tests for page load

### API/Backend Service
- [ ] Unit tests for business logic and services
- [ ] Integration tests for database operations
- [ ] Contract tests for API endpoints
- [ ] Security tests for auth and data validation
- [ ] Performance tests for endpoint latency

### Data Pipeline
- [ ] Unit tests for transformation functions
- [ ] Integration tests with test data sources
- [ ] Schema validation tests
- [ ] Error handling and retry logic tests
- [ ] Performance tests for data volume

### Library/Package
- [ ] Unit tests for all public APIs (100% coverage target)
- [ ] Integration tests for common use cases
- [ ] Type checking tests
- [ ] Compatibility tests across environments

---

*Last updated: 2024 | This methodology should be adapted to your project's specific risk profile, team size, and quality requirements.*