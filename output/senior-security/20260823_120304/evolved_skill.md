---
name: "senior-security"
description: Security engineering toolkit for threat modeling, vulnerability analysis, secure architecture, and penetration testing. Includes STRIDE analysis, OWASP guidance, cryptography patterns, and security scanning tools. Use when the user asks about security reviews, threat analysis, vulnerability assessments, secure coding practices, security audits, attack surface analysis, CVE remediation, or security best practices.
triggers:
  - security architecture
  - threat modeling
  - STRIDE analysis
  - penetration testing
  - vulnerability assessment
  - secure coding
  - OWASP
  - application security
  - cryptography implementation
  - secret scanning
  - security audit
  - zero trust
---
# Senior Security Engineer Toolkit

Comprehensive security engineering resources for threat modeling, vulnerability analysis, secure architecture design, and penetration testing.

---

## Table of Contents

- [Threat Modeling Workflow](#threat-modeling-workflow)
- [Security Architecture Workflow](#security-architecture-workflow)
- [Vulnerability Assessment Workflow](#vulnerability-assessment-workflow)
- [Secure Code Review Checklist](#secure-code-review-checklist)
- [Incident Response Workflow](#incident-response-workflow)
- [Cryptography Best Practices](#cryptography-best-practices)
- [Security Tools Reference](#security-tools-reference)
- [Reference Tables](#reference-tables)

---

## Threat Modeling Workflow

Systematic approach to identifying, analyzing, and mitigating security threats using proven methodologies.

### Step 1: Define Scope and Boundaries

- **Identify critical assets**: Data, systems, credentials, intellectual property
- **Map trust boundaries**: Where trust levels change between components
- **Document assumptions**: Security assumptions about each component
- **Establish data classification**: Sensitivity levels of processed data

### Step 2: Create Data Flow Diagram (DFD)

| Element | Symbol | Description |
|---------|--------|-------------|
| External Entity | Square | Users, external services, third-party APIs |
| Process | Circle | Application components, microservices, functions |
| Data Store | Open Rectangle | Databases, caches, file storage, message queues |
| Data Flow | Arrow | APIs, network connections, inter-process communication |

### Step 3: Apply STRIDE Analysis

For each DFD element, evaluate against STRIDE threat categories:

| Threat | Property Violated | Common Attack Vectors |
|--------|-------------------|----------------------|
| **S**poofing | Authentication | Session hijacking, credential theft, token forgery |
| **T**ampering | Integrity | SQL injection, man-in-the-middle, XSS |
| **R**epudiation | Non-repudiation | Log tampering, missing audit trails |
| **I**nformation Disclosure | Confidentiality | Data breaches, SSRF, insecure logging |
| **D**enial of Service | Availability | DDoS, resource exhaustion, algorithmic complexity |
| **E**levation of Privilege | Authorization | Privilege escalation, IDOR, broken access control |

### Step 4: Risk Scoring with DREAD

Calculate risk score for each threat (1-10 scale):

| Factor | Question | Weight |
|--------|----------|--------|
| **D**amage | How severe is the impact if exploited? | High |
| **R**eproducibility | How reliably can this be exploited? | High |
| **E**xploitability | How difficult is it to exploit? | Medium |
| **A**ffected Users | What percentage of users are impacted? | Medium |
| **D**iscoverability | How easily can this vulnerability be found? | Low |

**Risk Rating**: (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5

- **Critical (9-10)**: Immediate remediation required
- **High (7-8)**: Remediate within 1-2 sprints
- **Medium (4-6)**: Schedule remediation in current release
- **Low (1-3)**: Address when capacity allows

### Step 5: Define Mitigations

For each threat, document:

- **Preventive control**: Stop the attack entirely
- **Detective control**: Detect when attack occurs
- **Corrective control**: Recover from attack impact
- **Acceptance criteria**: What defines successful mitigation

### Threat Model Validation Checklist

- [ ] All external entities documented and categorized
- [ ] All trust boundaries identified and justified
- [ ] Data flows mapped with sensitivity labels
- [ ] STRIDE analysis applied to every DFD element
- [ ] DREAD scores calculated and documented
- [ ] Mitigations defined for all High/Critical threats
- [ ] Threat model reviewed by at least one peer
- [ ] Updates scheduled for architectural changes

---

## Security Architecture Workflow

### Architecture Review Checklist

Evaluate proposed architectures against security principles:

**Authentication & Authorization**
- [ ] Multi-factor authentication implemented
- [ ] Role-based access control (RBAC) defined
- [ ] Principle of least privilege enforced
- [ ] Session management follows security best practices
- [ ] Token-based auth uses secure algorithms (RS256, ES256)

**Data Protection**
- [ ] Data encrypted at rest (AES-256)
- [ ] Data encrypted in transit (TLS 1.3)
- [ ] Secrets managed via vault solutions (not code/config)
- [ ] Encryption keys rotated according to policy
- [ ] Sensitive data minimized in logs and errors

**Infrastructure Security**
- [ ] Network segmentation implemented
- [ ] Firewall rules follow deny-by-default
- [ ] Container images scanned for vulnerabilities
- [ ] Infrastructure as Code reviewed for security
- [ ] Cloud security posture management enabled

### Zero Trust Architecture Principles

| Principle | Implementation |
|-----------|----------------|
| Never trust, always verify | Every request authenticated and authorized |
| Least privilege access | Just-in-time access provisioning |
| Assume breach | Log and monitor all activity |
| Verify explicitly | Use all available data points for decisions |
| Device health | Endpoint protection and compliance checks |

---

## Vulnerability Assessment Workflow

### Discovery Phase

1. **Asset Inventory**: Enumerate all in-scope systems and components
2. **Port/Service Discovery**: Identify running services and versions
3. **Vulnerability Scanning**: Automated scanning with:
   - Network scanners (Nessus, OpenVAS)
   - Web application scanners (Burp Suite, OWASP ZAP)
   - Container scanners (Trivy, Clair)
   - Dependency scanners (OWASP Dependency-Check, Snyk)

4. **Manual Testing**: Human-led testing for business logic flaws

### Analysis Phase

| Severity | CVSS Score | Response Time |
|----------|------------|---------------|
| Critical | 9.0-10.0 | 24 hours |
| High | 7.0-8.9 | 7 days |
| Medium | 4.0-6.9 | 30 days |
| Low | 0.1-3.9 | 90 days |

### Remediation Phase

1. **Immediate containment** for actively exploited vulnerabilities
2. **Root cause analysis** to identify systemic issues
3. **Patch/fix deployment** following change management
4. **Verification testing** to confirm remediation
5. **Post-remediation scanning** to validate closure

### CVE Remediation Prioritization

Evaluate CVEs using:

- **Exploitability metrics**: Attack vector, complexity, privileges required
- **Impact metrics**: Confidentiality, integrity, availability impact
- **Threat intelligence**: Active exploitation in wild
- **Environmental metrics**: Your specific configuration exposure

---

## Secure Code Review Checklist

### Input Validation

- [ ] All user input validated before processing
- [ ] Validation uses allowlists (not blocklists)
- [ ] Server-side validation performed (not just client-side)
- [ ] File uploads validated by content type and magic bytes
- [ ] URL redirects validated against allowlist
- [ ] XML/JSON parsing uses secure configurations

### Authentication

- [ ] Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
- [ ] Password policy enforces complexity requirements
- [ ] Account lockout implemented to prevent brute force
- [ ] Session tokens are cryptographically random
- [ ] Sessions invalidated on logout and timeout
- [ ] MFA available for sensitive operations

### Authorization

- [ ] Access control checks on every protected endpoint
- [ ] Direct object references validated (IDOR prevention)
- [ ] Admin functions require elevated privileges
- [ ] Cross-tenant data access prevented
- [ ] API rate limiting implemented

### Data Protection

- [ ] Sensitive data not logged
- [ ] PII encrypted at rest and in transit
- [ ] Secrets not stored in version control
- [ ] Error messages don't reveal system details
- [ ] Database queries use parameterized statements
- [ ] Encryption keys loaded from secure storage

### Cryptographic Practices

- [ ] TLS 1.2+ for all external connections
- [ ] Strong cipher suites configured
- [ ] Certificate validation implemented correctly
- [ ] Random number generation uses secure sources
- [ ] No custom cryptographic implementations
- [ ] Keys rotated according to data sensitivity

### Error Handling

- [ ] Generic error messages shown to users
- [ ] Detailed errors logged server-side only
- [ ] Exceptions don't leak stack traces
- [ ] Graceful degradation for security failures
- [ ] Failed security operations logged

---

## Incident Response Workflow

### Preparation

- [ ] Incident response plan documented
- [ ] Contact list for security team maintained
- [ ] Incident response tools prepared
- [ ] Team trained on procedures
- [ ] Regular tabletop exercises conducted

### Detection & Analysis

| Phase | Activities |
|-------|------------|
| Detection | Monitor alerts, user reports, automated detections |
| Triage | Classify severity, determine scope |
| Analysis | Identify attack vectors, affected systems, data exposure |
| Documentation | Record timeline, evidence, actions taken |

### Containment

**Short-term (immediate)**
- Isolate affected systems
- Block malicious IPs/accounts
- Preserve evidence

**Long-term (strategic)**
- Deploy temporary fixes
- Enhance monitoring
- Prepare communication

### Eradication & Recovery

1. Remove malware/backdoors
2. Patch vulnerabilities exploited
3. Reset compromised credentials
4. Restore from clean backups
5. Verify system integrity
6. Gradual return to operations

### Post-Incident

- [ ] Conduct lessons learned review
- [ ] Update documentation and procedures
- [ ] Implement preventive measures
- [ ] Brief relevant stakeholders
- [ ] Close incident with all artifacts archived

---

## Cryptography Best Practices

### Algorithm Selection

| Use Case | Recommended | Avoid |
|----------|-------------|-------|
| Symmetric encryption | AES-256-GCM | DES, 3DES, AES-ECB |
| Asymmetric encryption | RSA-3072+, EC (P-384+) | RSA-1024, ECC curves <256-bit |
| Hashing (passwords) | bcrypt, Argon2id, scrypt | MD5, SHA1, SHA256 alone |
| Hashing (integrity) | SHA-256+, SHA-3 | MD5, SHA1 |
| Digital signatures | ECDSA, RSA-PSS | DSA, MD5withRSA |
| MAC | HMAC-SHA256+ | MD5-based HMAC |

### Key Management

- **Key generation**: Use cryptographically secure random number generators
- **Key storage**: Hardware Security Modules (HSM) or key vaults (AWS KMS, HashiCorp Vault)
- **Key rotation**: Implement automated rotation based on data sensitivity
- **Key destruction**: Secure erasure when keys are no longer needed
- **Key separation**: Different keys for different purposes

### Secret Scanning Patterns

| Secret Type | Pattern Indicators |
|-------------|-------------------|
| AWS Keys | `AKIA` followed by 16 characters |
| Private Keys | `-----BEGIN [RSA/DSA/EC] PRIVATE KEY-----` |
| API Keys | Long alphanumeric strings in headers/urls |
| JWT Tokens | Base64 strings with `eyJ` prefix |
| Database URLs | `jdbc:`, `mongodb:`, `postgres://` with credentials |
| Git Tokens | `ghp_`, `gho_`, `glpat-`, `x化lab` prefixes |

### Secure Configuration

nginx
# TLS Configuration Example
ssl_protocols TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;
ssl_session_timeout 1d;
ssl_session_tickets off;
---

## Security Tools Reference

### Static Application Security Testing (SAST)

| Tool | Language | Integration |
|------|----------|-------------|
| Semgrep | Multiple | CI/CD, IDE |
| SonarQube | Multiple | CI/CD |
| Bandit | Python | CLI, CI/CD |
| Gosec | Go | CLI, CI/CD |
| ESLint (security) | JavaScript | IDE, CI/CD |

### Dynamic Application Security Testing (DAST)

| Tool | Type | Use Case |
|------|------|----------|
| OWASP ZAP | Automated | Web app scanning |
| Burp Suite | Manual/Automated | Web app testing |
| Nuclei | Template-based | Rapid scanning |
| sqlmap | SQL injection | Database assessment |

### Dependency Scanning

| Tool | Database | CI/CD Support |
|------|----------|----------------|
| Snyk | Extensive | Native |
| OWASP Dependency-Check | NVD | Plugin-based |
| Trivy | NVD, own | Container native |
| Grype | NVD | Container native |
| npm audit | npm DB | Node.js native |

### Secret Scanning

| Tool | Scope | Pre-commit |
|------|-------|------------|
| Gitleaks | Git history, local | Yes |
| TruffleHog | Git history, S3, etc. | Yes |
| GitHub Secret Scanning | Repository | Automatic |
| pre-commit hooks | Pre-commit | Yes |

### Container Security

| Tool | Function | Runtime |
|------|----------|---------|
| Trivy | Vulnerability scanning | No |
| Clair | Vulnerability scanning | No |
| Falco | Runtime security | Yes |
| Sysdig Secure | Runtime security | Yes |
| Aqua Security | Full platform | Yes |

### Infrastructure Scanning

| Tool | Target | Notes |
|------|--------|-------|
| Nessus | Network, devices | Enterprise |
| OpenVAS | Network | Open source |
| Nmap | Network discovery | Scriptable |
| ScoutSuite | Cloud environments | Multi-cloud |

---

## Reference Tables

### OWASP Top 10 (2021)

| Rank | Category | Key Mitigations |
|------|----------|-----------------|
| A01 | Broken Access Control | Access control testing, deny by default |
| A02 | Cryptographic Failures | Encryption, key management, data minimization |
| A03 | Injection | Parameterized queries, input validation |
| A04 | Insecure Design | Threat modeling, secure design patterns |
| A05 | Security Misconfiguration | Hardening, automation, patches |
| A06 | Vulnerable Components | Inventory, patching, removal of unused |
| A07 | Auth Failures | MFA, weak password prevention |
| A08 | Software/Data Integrity | Code signing, dependency verification |
| A09 | Logging Failures | Comprehensive logging, alerting |
| A10 | SSRF | Network segmentation, URL validation |

### Common Attack Surface Areas

| Area | Common Vulnerabilities | Testing Approach |
|------|----------------------|------------------|
| Authentication | Weak passwords, brute force, session fixation | Manual testing, credential stuffing tools |
| Authorization | IDOR, privilege escalation, horizontal access | Access control matrix testing |
| Input Handling | Injection, XSS, XXE, path traversal | Fuzzing, payload testing |
| APIs | Mass assignment, rate limiting, auth bypass | API-specific scanners |
| Cryptography | Weak algorithms, key management | Configuration review, implementation testing |
| Business Logic | Workflow bypasses, race conditions | Manual scenario testing |

### Security Headers Reference

| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| Content-Security-Policy | XSS prevention | `default-src 'self'` |
| X-Frame-Options | Clickjacking prevention | `DENY` or `SAMEORIGIN` |
| Strict-Transport-Security | HTTPS enforcement | `max-age=31536000; includeSubDomains` |
| X-Content-Type-Options | MIME sniffing prevention | `nosniff` |
| Referrer-Policy | Referrer leakage control | `strict-origin-when-cross-origin` |
| Permissions-Policy | Feature restrictions | Minimal required features |

---

*Document Version: 1.0*  
*Last Updated: Security Engineering Best Practices*