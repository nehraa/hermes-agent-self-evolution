---
category: software-development
name: comprehensive-tech-documentation
description: "Creates layered, comprehensive technical documentation for projects, skills, or systems. Use when user requests 'write technical documentation', 'explain how this works', or 'document the architecture'. Produces 3-4 documents with different depths and purposes."
---

# Comprehensive Technical Documentation

Creates a complete documentation suite that serves different audiences and use cases, from quick reference to deep technical analysis.

## When to Use

Use this skill when the user asks to:
- Write technical documentation
- Document a system or architecture
- Explain how something works
- Create project documentation
- Generate API or code documentation

## Documentation Suite Overview

| User Request | Documentation Output |
|--------------|---------------------|
| "Write docs" or "写技术文档" | Full 4-document suite |
| "Explain how it works" or "解释原理" | Technical Principles + Architecture |
| "Quick reference" or "快速参考" | Quick Reference Guide only |
| "Draw architecture" or "画架构图" | Architecture Visualization |
| "Create index" or "写导航索引" | Navigation Index |

## The Four Documents

### 1. 📖 Technical Principles (`技术原理文档.md`)

**Purpose**: Deep technical understanding of the system

**Contents**:
- System overview and core concepts
- Design philosophy and architectural decisions
- Detailed implementation explanation
- Key algorithms and data structures
- Best practices and patterns
- Security considerations

**Target audience**: Developers, contributors, technical leads
**Reading time**: 30-60 minutes

---

### 2. 📊 Architecture Visualization (`架构与流程可视化.md`)

**Purpose**: Visual representation of system structure

**Contents**:
- System architecture diagrams (Mermaid)
- Component interaction diagrams
- Data flow diagrams
- Sequence diagrams for key operations
- State machines and process flows
- Deployment topology

**Target audience**: Architects, technical leads, visual learners
**Reading time**: 15-30 minutes

---

### 3. 🔖 Quick Reference Guide (`快速参考指南.md`)

**Purpose**: Fast lookup and common tasks

**Contents**:
- Getting started steps
- Command cheat sheet
- Configuration templates
- Field/method reference tables
- Common patterns with examples
- Troubleshooting guide
- FAQ

**Target audience**: All users (most frequently accessed)
**Reading time**: 5-15 minutes

---

### 4. 🗺️ Navigation Index (`文档索引.md`)

**Purpose**: Guide users to the right document

**Contents**:
- Document comparison table
- Learning paths by role (developer, operator, contributor)
- Scenario-based navigation (troubleshooting, setup, customization)
- FAQ with document links

**Target audience**: First-time users, anyone needing orientation
**Reading time**: 5 minutes

---

## Workflow

### Phase 1: Analysis

1. **Understand the system**
   - Identify the core purpose and scope
   - Determine target audience level
   - Note existing documentation (if any)

2. **Plan the documentation suite**
   - Adjust depth based on system complexity
   - For simple projects: Quick Reference + Index only
   - For medium projects: All four documents
   - For complex systems: Add additional focused documents

### Phase 2: Content Creation

Create documents in this order (dependency order):

1. **Technical Principles** — establishes the authoritative source
2. **Architecture Visualization** — references principles for context
3. **Quick Reference** — summarizes key information from above
4. **Navigation Index** — links everything together

### Phase 3: Review

1. Verify cross-references between documents are accurate
2. Ensure consistent terminology throughout
3. Check diagrams render correctly in markdown viewers
4. Validate all code examples and commands work
5. Confirm reading times match actual content

---

## Document Naming Convention

| Document | Chinese Name | English Name |
|----------|--------------|--------------|
| Technical Principles | 技术原理文档.md | technical-principles.md |
| Architecture | 架构与流程可视化.md | architecture.md |
| Quick Reference | 快速参考指南.md | quick-reference.md |
| Navigation Index | 文档索引.md | README.md |

---

## Quality Checklist

- [ ] All code examples are tested and working
- [ ] Diagrams use consistent styling (Mermaid)
- [ ] Terms are defined at first use
- [ ] Cross-references link to correct documents
- [ ] Reading times are realistic
- [ ] Each document has a clear target audience
- [ ] Navigation Index covers common user scenarios