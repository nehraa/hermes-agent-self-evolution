---
category: software-development
name: senior-security
description: Security engineering toolkit for threat modeling, vulnerability analysis, secure architecture design, and penetration testing. Includes STRIDE analysis, OWASP guidance, cryptography patterns, security scanning tools, and incident response workflows.
triggers:
  - "security architecture"
  - "threat modeling"
  - "STRIDE analysis"
  - "penetration testing"
  - "vulnerability assessment"
  - "secure coding"
  - "OWASP"
  - "application security"
  - "cryptography implementation"
  - "secret scanning"
  - "security audit"
  - "zero trust"
  - "CVE remediation"
  - "attack surface"
  - "security review"
---

# Senior Security Engineer Toolkit

Comprehensive security engineering tools for threat modeling, vulnerability analysis, secure architecture design, penetration testing, and incident response.

---

## Table of Contents

1. [Threat Modeling Workflow](#threat-modeling-workflow)
2. [Security Architecture Workflow](#security-architecture-workflow)
3. [Vulnerability Assessment Workflow](#vulnerability-assessment-workflow)
4. [Secure Code Review Workflow](#secure-code-review-workflow)
5. [Incident Response Workflow](#incident-response-workflow)
6. [Cryptography Patterns](#cryptography-patterns)
7. [Security Tools Reference](#security-tools-reference)
8. [OWASP Top 10 Checklist](#owasp-top-10-checklist)
9. [Zero Trust Implementation](#zero-trust-implementation)

---

## Threat Modeling Workflow

Identify, analyze, and prioritize security threats using structured methodologies.

### Step 1: Define Scope and Boundaries

□ Identify all assets requiring protection (data, systems, credentials)
□ Map trust boundaries between:
  - External entities (users, third-party services)
  - Internal components (microservices, modules)
  - Data stores (databases, caches, message queues)
□ Document system boundaries and entry points
□ Identify authentication/authorization boundaries
### Step 2: Create Data Flow Diagram (DFD)

Document these elements for each component:

| Element | Description | Example |
|---------|-------------|---------|
| External Entity | Users or systems outside trust boundary | End users, OAuth providers |
| Process | Application components that transform data | API handlers, microservices |
| Data Store | Persistent or temporary data storage | PostgreSQL, Redis, S3 |
| Data Flow | Data movement between elements | REST APIs, gRPC, message queues |

### Step 3: Apply STRIDE Threat Model

Analyze each DFD element against STRIDE categories:

| Threat Category | Property Violated | Example Attack | Common Mitigation |
|-----------------|-------------------|----------------|-------------------|
| **S**poofing | Authentication | Stolen credentials, session hijacking | MFA, certificate pinning, secure session management |
| **T**ampering | Integrity | SQL injection, man-in-the-middle | Input validation, TLS, digital signatures |
| **R**epudiation | Non-repudiation | Denying actions performed | Audit logging, cryptographic logging |
| **I**nformation Disclosure | Confidentiality | Data breach, credential exposure | Encryption at rest/transit, access controls |
| **D**enial of Service | Availability | DDoS, resource exhaustion | Rate limiting, autoscaling, CDN |
| **E**levation of Privilege | Authorization | Privilege escalation, buffer overflow | Least privilege, input validation, sandboxing |

### Step 4: Risk Scoring with DREAD

Score each identified threat (1-10 scale):

| Factor | Question | Weight |
|--------|----------|--------|
| **D**amage | How severe is the impact if exploited? | High |
| **R**eproducibility | How reliably can it be reproduced? | Medium |
| **E**xploitability | How difficult is it to exploit? | Medium |
| **A**ffected Users | What percentage of users are impacted? | High |
| **D**iscoverability | How easily can it be found? | Low |

**Risk Score = (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5**

| Score Range | Priority | Action |
|-------------|----------|--------|
| 8-10 | Critical | Immediate remediation (< 24 hours) |
| 6-7.9 | High | Short-term fix (< 1 week) |
| 4-5.9 | Medium | Planned fix (< 1 month) |
| < 4 | Low | Accept risk or defer |

### Step 5: Define and Document Mitigations

For each threat, document:

markdown
## Threat: [Name]
- **STRIDE Category:** [Category]
- **Risk Score:** [Score]
- **Affected Component:** [Component]
- **Attack Vector:** [How it's exploited]
- **Mitigation Strategy:** [Security control]
- **Implementation:** [Specific changes needed]
- **Test/Validation:** [How to verify fix]
### Validation Checklist

- [ ] All DFD elements documented
- [ ] Trust boundaries identified
- [ ] STRIDE analysis completed for each element
- [ ] All threats scored using DREAD
- [ ] Mitigations defined for all high/critical risks
- [ ] Threat model reviewed by security team
- [ ] Document approved and stored centrally

---

## Security Architecture Workflow

Design and review security architecture for systems and applications.

### Architecture Review Checklist

#### Authentication & Authorization

□ Authentication mechanisms
  - MFA implementation (TOTP, hardware keys, biometrics)
  - Password policies (complexity, rotation, breach detection)
  - OAuth 2.0 / OIDC implementation
  - API key management and rotation

□ Authorization models
  - RBAC (Role-Based Access Control) implementation
  - ABAC (Attribute-Based Access Control) if needed
  - Least privilege enforcement
  - Privilege separation patterns
#### Data Protection

□ Encryption at rest
  - Algorithm: AES-256 (minimum)
  - Key management: AWS KMS, HashiCorp Vault, Azure Key Vault
  - Key rotation policies

□ Encryption in transit
  - TLS 1.2 minimum, TLS 1.3 preferred
  - Certificate management (auto-renewal, pinning)
  - mTLS for service-to-service communication

□ Data classification
  - Public, Internal, Confidential, Restricted
  - Handling requirements for each classification
#### Network Security

□ Network segmentation (VPCs, subnets, security groups)
□ Firewall rules and network policies
□ Ingress/egress controls
□ CDN and WAF configuration
□ DNS security (DNSSEC, DNS filtering)
#### Resilience & Availability

□ DDoS protection mechanisms
□ Rate limiting strategies
□ Circuit breaker patterns
□ Failover and disaster recovery
□ Backup and restore procedures
### Architecture Decision Record (ADR) Template

markdown
# ADR-[Number]: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[Problem statement and constraints]

## Decision
[Chosen approach with rationale]

## Consequences
- **Positive:** [Benefits]
- **Negative:** [Trade-offs and risks]
- **Risks:** [Security implications]

## Security Considerations
[How this decision impacts security posture]

## Alternatives Considered
[Other options and why they were rejected]
---

## Vulnerability Assessment Workflow

Systematic approach to identifying and remediating vulnerabilities.

### Phase 1: Discovery

#### Automated Scanning

| Tool | Use Case | Command |
|------|----------|--------|
| **OWASP ZAP** | Web application scanning | `zap-cli quick-scan https://target.com` |
| **Nikto** | Web server scanning | `nikto -h https://target.com` |
| **Nuclei** | Vulnerability templates | `nuclei -u https://target.com` |
| **Semgrep** | Static code scanning | `semgrep --config=auto .` |
| **Trivy** | Container/image scanning | `trivy image <image-name>` |
| **Grype** | SBOM vulnerability scanning | `grype <image-name>` |

#### Manual Testing

- Code review for business logic vulnerabilities
- Authentication bypass testing
- Authorization escalation attempts
- Input manipulation and injection testing
- Session management testing

### Phase 2: Analysis and Classification

#### CVE Assessment

markdown
## CVE-[ID]: [Vulnerability Title]

### Severity
- **CVSS Score:** [X.X]
- **CVSS Vector:** [Vector string]
- **Severity Level:** [Critical/High/Medium/Low]

### Affected Components
- [Component Name]: [Version Range]
- [Dependency Name]: [Version Range]

### Technical Details
[Description of vulnerability and impact]

### Exploitation Scenarios
[How an attacker could exploit this]

### Remediation
- **Fix Version:** [Version number]
- **Workaround:** [Temporary mitigation if no fix available]
- **Patch URL:** [Link to official patch]

### Detection
[How to detect if vulnerable/exploited]
#### False Positive Triage

| Check | Question |
|-------|----------|
| Environment | Is the affected component actually in scope? |
| Configuration | Is the vulnerable feature/setting actually enabled? |
| Exploitability | Can this be exploited in our context? |
| Impact | What is the actual business impact if exploited? |

### Phase 3: Remediation Tracking

markdown
## Vulnerability Remediation Tracker

| ID | Vulnerability | Severity | Status | Owner | Due Date | Evidence |
|----|---------------|----------|--------|-------|----------|----------|
| VULN-001 | SQL Injection in /api/users | Critical | In Progress | @dev-lead | 2024-01-15 | Code review |
| VULN-002 | Outdated OpenSSL | High | Open | @infra | 2024-01-20 | Scan report |
---

## Secure Code Review Workflow

Systematic code review focusing on security vulnerabilities.

### Review Checklist by Category

#### Input Validation

□ All user input validated before processing
□ Type checking implemented
□ Length limits enforced
□ Allowlist validation preferred over blocklist
□ Sanitization for context (HTML, SQL, OS commands)
□ File upload validation (type, size, content)
□ URL validation for redirects
#### Authentication

□ Passwords hashed with bcrypt/Argon2/scrypt
□ Password reset tokens are cryptographically random
□ Session tokens expire appropriately
□ Session invalidation on logout
□ Account lockout policies implemented
□ MFA available for sensitive operations
#### Authorization

□ Every request authorized (defense in depth)
□ Role/permission checks server-side only
□ Horizontal privilege separation enforced
□ IDOR (Insecure Direct Object Reference) prevented
□ Admin functions have additional controls
#### Data Handling

□ Sensitive data not logged
□ PII encrypted or masked in storage
□ Secrets not in code (use secrets manager)
□ Database queries use parameterized statements
□ File paths validated (path traversal prevention)
#### Cryptography

□ No custom crypto implementations
□ Secure random number generation (crypto.random)
□ Key sizes meet current standards (AES-256, RSA-4096)
□ Keys rotated appropriately
□ No hardcoded credentials or keys
### Secure Code Review Comment Template

markdown
## [SEVERITY] [CWE-ID]: [Brief Title]

**File:** `src/path/file.ext:123`
**Issue:** [Description of vulnerability]
**Risk:** [What could happen if exploited]

**Recommendation:**
[language]
// Example of secure code
secure_implementation();
**References:**
- CWE-[number]: [CWE title]
- [Relevant security guideline or article]
---

## Incident Response Workflow

Structured approach to handling security incidents.

### Incident Classification

| Severity | Definition | Response Time |
|----------|------------|---------------|
| **P0 - Critical** | Active breach, data exfiltration, ransomware | Immediate (< 15 min) |
| **P1 - High** | Confirmed vulnerability exploitation, malware | < 1 hour |
| **P2 - Medium** | Suspicious activity, potential breach | < 4 hours |
| **P3 - Low** | Failed attack attempts, minor policy violations | < 24 hours |

### Incident Response Phases

#### Phase 1: Detection & Identification

markdown
## Incident Report: [INC-YYYYMMDD-XXX]

### Initial Detection
- **Detected By:** [Source]
- **Detection Time:** [Timestamp]
- **Initial Indicator:** [What triggered the alert]

### Classification
- **Severity:** [P0/P1/P2/P3]
- **Category:** [Malware/Phishing/Data Breach/DDoS/Insider/Other]
- **Affected Systems:** [List]
- **Data Impact:** [Confidentiality/Integrity/Availability]
#### Phase 2: Containment

□ Isolate affected systems (network segmentation)
□ Block malicious IP addresses
□ Revoke compromised credentials
□ Enable enhanced logging/monitoring
□ Preserve evidence (disk images, memory dumps, logs)
□ Document timeline of actions taken
#### Phase 3: Eradication

□ Remove malware/backdoors
□ Patch vulnerable systems
□ Reset compromised credentials
□ Update firewall/rules signatures
□ Verify no persistence mechanisms remain
#### Phase 4: Recovery

□ Restore from clean backups
□ Rebuild compromised systems
□ Gradually restore services
□ Monitor for recurrence
□ Validate integrity of restored systems
#### Phase 5: Post-Incident Review

markdown
## Post-Incident Review

### Summary
[What happened, impact, duration]

### Root Cause Analysis
[Technical and process root causes]

### Timeline
- [Time]: [Event]
- [Time]: [Event]

### Lessons Learned
- **What Went Well:** [Successes]
- **What Could Be Improved:** [Gaps identified]
- **Action Items:** [Specific improvements]

### Metrics
- **Detection Time:** [Duration]
- **Containment Time:** [Duration]
- **Total Incident Duration:** [Duration]
- **Systems Affected:** [Count]
- **Records/Users Affected:** [Count]
---

## Cryptography Patterns

### Symmetric Encryption

typescript
// Recommended: AES-256-GCM for authenticated encryption
import { randomBytes, createCipheriv, createDecipheriv } from 'crypto';

function encrypt(plaintext: string, key: Buffer): { ciphertext: Buffer; iv: Buffer; tag: Buffer } {
  const iv = randomBytes(12); // GCM standard IV size
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  
  let ciphertext = cipher.update(plaintext, 'utf8');
  ciphertext = Buffer.concat([ciphertext, cipher.final()]);
  const tag = cipher.getAuthTag();
  
  return { ciphertext, iv, tag };
}

function decrypt(ciphertext: Buffer, key: Buffer, iv: Buffer, tag: Buffer): string {
  const decipher = createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(tag);
  
  let plaintext = decipher.update(ciphertext);
  plaintext = Buffer.concat([plaintext, decipher.final()]);
  
  return plaintext.toString('utf8');
}
### Asymmetric Encryption

typescript
// Recommended: RSA-OAEP for encryption, ECDSA for signing
// For key exchange: ECDH with P-384 or X25519

import { generateKeyPairSync, publicEncrypt, privateDecrypt } from 'crypto';

// Key generation
const { publicKey, privateKey } = generateKeyPairSync('rsa', {
  modulusLength: 4096,
  publicKeyEncoding: { type: 'spki', format: 'pem' },
  privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
});

// Encrypt with public key
function encryptWithPublicKey(data: string, pubKey: string): Buffer {
  return publicEncrypt(
    { key: pubKey, oaepHash: 'sha256' },
    Buffer.from(data)
  );
}
### Password Hashing

typescript
import { hash, verify } from '@node-rs/argon2';

async function hashPassword(password: string): Promise<string> {
  return hash(password, {
    memoryCost: 65536, // 64 MB
    timeCost: 3,       // 3 iterations
    parallelism: 4
  });
}

async function verifyPassword(hash: string, password: string): Promise<boolean> {
  return verify(hash, password);
}
### Key Derivation

typescript
import { pbkdf2Sync, randomBytes } from 'crypto';

function deriveKey(password: string, salt: Buffer, iterations: number = 100000): Buffer {
  return pbkdf2Sync(password, salt, iterations, 32, 'sha256');
}

// Usage
const salt = randomBytes(16);
const key = deriveKey('password', salt);
### Secure Random Generation

typescript
import { randomBytes, randomUUID } from 'crypto';

// For tokens, session IDs, nonces
const token = randomBytes(32).toString('hex');
const uuid = randomUUID(); // UUID v4
### Cryptographic Anti-Patterns to Avoid

| Anti-Pattern | Risk | Correct Approach |
|--------------|------|------------------|
| `Math.random()` for security | Predictable, exploitable | Use `crypto.randomBytes()` |
| MD5/SHA1 for passwords | Collision attacks, fast to crack | Use Argon2, bcrypt, scrypt |
| ECB mode encryption | Pattern leakage | Use GCM, CBC with IV |
| Hardcoded keys | Key exposure in source | Use secrets manager (Vault, KMS) |
| AES-128 for sensitive data | Weaker key space | Use AES-256 minimum |
| RSA-1024 | Insufficient for modern threats | Use RSA-4096 or ECC (P-384/X25519) |
| ECB mode for files | Pattern leakage | Use GCM or CBC with unique IV |

---

## Security Tools Reference

### Static Application Security Testing (SAST)

| Tool | Language | License | Command |
|------|----------|---------|---------|
| **Semgrep** | Multi | Apache/MIT | `semgrep --config=auto src/` |
| **SonarQube** | Multi | Commercial/Enterprise | `sonar-scanner` |
| **Bandit** | Python | Apache | `bandit -r ./` |
| **ESLint + security** | JavaScript/TypeScript | MIT | `eslint --plugin security .` |
| **Gosec** | Go | Apache | `gosec ./...` |
| **FindBugs** | Java | LGPL | `mvn findbugs:findbugs` |

### Dynamic Application Security Testing (DAST)

| Tool | Type | License | Use Case |
|------|------|---------|----------|
| **OWASP ZAP** | Web scanner | Apache | Automated scanning, proxy-based |
| **Burp Suite** | Web proxy/scanner | Commercial | Manual testing, professional |
| **Nuclei** | Template-based | MIT | Custom vulnerability templates |
| **Nikto** | Web server scanner | GPL | Server misconfiguration |

### Secret Scanning

| Tool | Scope | License |
|------|-------|---------|
| **GitLeaks** | Git history, commits | MIT |
| **TruffleHog** | Git history, file scanning | AGPL |
| **Semgrep Secrets** | CI/CD, IDE integration | Commercial |
| **AWS Secrets Detector** | AWS credential patterns | AWS CLA |

### Dependency Scanning

| Tool | Type | Command |
|------|------|---------|
| **npm audit** | JavaScript | `npm audit --audit-level=high` |
| **Snyk** | Multi-language | `snyk test` |
| **Dependabot** | GitHub-native | Auto-enabled |
| **Renovate** | Multi-language | Config-driven |
| **Trivy** | Containers | `trivy fs --security-checks vuln .` |
| **Grype** | SBOM-based | `grype dir:.` |

### Infrastructure Security

| Tool | Purpose | Use Case |
|------|---------|----------|
| **tfsec** | Terraform scanning | IaC security |
| **Checkov** | Multi-IaC | Terraform, Kubernetes, Docker |
| **kubesec** | Kubernetes manifests | Security scoring |
| **OPA/Conftest** | Policy as code | Custom security policies |

---

## OWASP Top 10 Checklist

### A01:2021 – Broken Access Control

□ Access controls enforced server-side
□ Principle of least privilege applied
□ IDOR prevention implemented
□ Vertical and horizontal access controls tested
□ Rate limiting on API endpoints
□ CORS policies properly configured
□ Direct object reference validation
### A02:2021 – Cryptographic Failures

□ Encryption for data at rest (AES-256+)
□ Encryption for data in transit (TLS 1.2+)
□ No sensitive data in URLs or logs
□ Proper key management implemented
□ Default credentials removed/changed
□ Sufficient key lengths used
### A03:2021 – Injection

□ Parameterized queries for all database access
□ Input validation on all entry points
□ Output encoding for context (HTML, JS, SQL, LDAP)
□ ORM usage with proper configuration
□ Command injection prevention
□ No string concatenation in queries/commands
### A04:2021 – Insecure Design

□ Threat modeling performed
□ Secure design patterns documented
□ Security requirements defined
□ Abuse cases identified
□ Rate limiting implemented
□ WAF/CDN for protection
### A05:2021 – Security Misconfiguration

□ Hardening guidelines followed
□ Unnecessary features removed/disabled
□ Error handling doesn't leak information
□ Default accounts changed
□ Security headers configured
□ Automated security configuration verification
### A06:2021 – Vulnerable and Outdated Components

□ Software inventory maintained
□ Dependencies monitored for vulnerabilities
□ Unsupported components replaced
□ Auto-update policy for security patches
□ Regular vulnerability scanning
□ Software Bill of Materials (SBOM) generated
### A07:2021 – Identification and Authentication Failures

□ MFA implemented for all users
□ Weak password policies rejected
□ Session IDs rotated after login
□ Session timeout enforced
□ Credentials not logged or exposed
□ Account lockout implemented
□ Password reset tokens are single-use
### A08:2021 – Software and Data Integrity Failures

□ Code signing for critical software
□ CI/CD pipeline security
□ Integrity verification for dependencies
□ No unsigned/deserialized untrusted data
□ Configuration as code validated
### A09:2021 – Security Logging and Monitoring Failures

□ Security events logged (auth, access, errors)
□ Logs protected from tampering
□ Centralized log aggregation
□ Alert thresholds defined
□ Incident response procedures documented
□ Regular log review process
### A10:2021 – Server-Side Request Forgery (SSRF)

□ URL validation implemented
□ Allowlist for allowed domains/IPs
□ Network segmentation applied
□ No user-provided URLs for backend requests
□ Default deny for outbound connections
---

## Zero Trust Implementation

### Core Principles

1. **Never Trust, Always Verify** – No implicit access based on network location
2. **Least Privilege Access** – Just-in-time, just-enough access
3. **Assume Breach** – Minimize blast radius, verify end-to-end encryption

### Implementation Checklist

#### Identity & Access Management

□ Multi-factor authentication (MFA) enforced
□ Single Sign-On (SSO) implemented
□ Privileged Access Management (PAM) for admin access
□ Just-in-time (JIT) access provisioning
□ Identity lifecycle management automated
□ User behavior analytics (UEBA) deployed
#### Device Security

□ Device inventory maintained
□ Endpoint detection and response (EDR)
□ Device compliance policies enforced
□ Mobile Device Management (MDM) implemented
□ Certificate-based device authentication
□ Regular patching verified
#### Network Security

□ Microsegmentation implemented
□ East-west traffic inspection
□ DNS-layer security
□ Network access control (NAC)
□ Software-defined perimeter (SDP)
□ No implicit trust between services (mTLS)
#### Application Security

□ OAuth 2.0 / OIDC for application authentication
□ API gateway with authentication/authorization
□ Application-layer encryption
□ Continuous security validation
□ Web Application Firewall (WAF)
#### Data Security

□ Data classification implemented
□ Data loss prevention (DLP)
□ Information rights management
□ Encryption in transit and at rest
□ Access based on data sensitivity
### Zero Trust Architecture Reference

┌─────────────────────────────────────────────────────────────┐
│                        USER                                  │
│              (Managed Device, MFA Verified)                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    IDENTITY PROVIDER                         │
│         (AuthN/AuthZ, Policy Engine, Risk Scoring)           │
└─────────────────────────┬───────────────────────────────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  Workloads  │  Workloads  │  Workloads  │
│  (East/West)│  (North/South│  (Data)      │
│  Microsegment│ Segments)   │              │
└─────────┘ └─────────┘ └─────────┘
---

## Quick Reference

### Common Security HTTP Headers

http
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
### Security Contact Template

markdown
## Security Contact Information

For security vulnerabilities or concerns, please:
- Email: security@yourcompany.com
- Bug Bounty: https://bugbounty.yourcompany.com
- PGP Key: [Fingerprint]

Expected response times:
- Critical: < 24 hours
- High: < 7 days
- Medium: < 30 days
- Low: Best effort

Please do NOT include sensitive data in initial reports.
### Security Review Request Template

markdown
## Security Review Request

### Project Information
- **Project Name:** [Name]
- **Owner:** [Team/Individual]
- **Review Type:** [Architecture/Code/Config/Pentest]
- **Requested Date:** [Date]
- **Required Completion:** [Date]

### Scope
- [System/Component 1]
- [System/Component 2]

### Critical Features
[Features that handle sensitive data or have security implications]

### Compliance Requirements
[PCI-DSS, SOC2, HIPAA, GDPR, etc.]

### Previous Security Reviews
[Link to prior reviews and findings]
---

*Last updated: 2024 | Maintainer: Security Team*