---
category: software-development
name: comprehensive-tech-documentation
description: "Creates layered, comprehensive technical documentation for projects, skills, or systems. Use when user requests 'write technical documentation', 'explain how this works', or 'document the architecture'. Produces 3-4 documents with different depths and purposes."
---

# Comprehensive Technical Documentation

Creates a complete documentation suite that serves different audiences and use cases, from quick reference to deep technical analysis.

## Quick Reference

| User Request | Documentation Output |
|--------------|---------------------|
| `写技术文档` / `write docs` / `document this` | Full 4-document suite |
| `解释原理` / `explain how it works` | Technical Principles + Architecture |
| `快速参考` / `quick reference` | Quick Reference Guide only |
| `画架构图` / `draw architecture` | Architecture Visualization |
| `写导航索引` / `create index` | Navigation Index |
| `写README` / `write readme` | Navigation Index (as README) |

## When to Use

Use this skill when documenting:
- Complex software systems
- Technical skills or capabilities
- APIs or services
- Architecture patterns
- Multi-component projects

## The Documentation Suite

Create these documents based on project scope:

### 1. 📖 Technical Principles (`技术原理文档.md`)

**Purpose**: Deep technical understanding

**Contents**:
- System overview and purpose
- Core concepts and terminology
- Design philosophy and decisions
- Implementation details
- Data structures and algorithms
- Best practices and patterns
- Known limitations

**Target audience**: Developers, contributors
**Reading time**: 30-60 minutes

---

### 2. 📊 Architecture Visualization (`架构与流程可视化.md`)

**Purpose**: Visual representation of system structure

**Contents** (use Mermaid diagrams):
- System architecture diagrams
- Component relationships
- Data flow diagrams
- Sequence diagrams for key workflows
- State machines
- Deployment topology

**Target audience**: Architects, visual learners, team leads
**Reading time**: 15-30 minutes

---

### 3. 🔖 Quick Reference Guide (`快速参考指南.md`)

**Purpose**: Fast answers and lookup

**Contents**:
- Common use cases with examples
- Command cheat sheets
- Configuration templates
- Field/type definitions
- Error codes and troubleshooting
- FAQ section

**Target audience**: All users (most frequently consulted)
**Reading time**: 5-15 minutes

---

### 4. 🗺️ Navigation Index (`README-文档索引.md` or `文档索引.md`)

**Purpose**: Guide users to the right document

**Contents**:
- Document comparison table
- Learning paths by role
- Scenario-based navigation guide
- FAQ with direct document links
- Quick links to each doc

**Target audience**: First-time users, anyone seeking orientation
**Reading time**: 5 minutes

---

## Step-by-Step Workflow

### Phase 1: Analysis

1. **Identify the subject**: What are we documenting?
2. **Assess scope**: Simple tool or complex system?
3. **Determine audience**: Developers, end-users, or mixed?
4. **Select documents**: Which 2-4 docs are needed?

### Phase 2: Content Creation

**For Technical Principles**:
- Start with high-level overview
- Explain key concepts before details
- Document design decisions with rationale
- Include code examples for critical paths
- Add "why" explanations, not just "what"

**For Architecture Visualization**:
- Identify main components
- Map data flow between components
- Define boundaries and interfaces
- Create Mermaid diagrams for each view
- Include both logical and physical views if relevant

**For Quick Reference**:
- Lead with most common use cases
- Use code blocks for all examples
- Include copy-paste ready templates
- Add troubleshooting section for frequent issues
- Keep explanations minimal

**For Navigation Index**:
- Match document to user scenarios
- Provide clear "start here" guidance
- Link to specific sections, not just documents
- Include a visual document relationship diagram

### Phase 3: Refinement

1. Check for consistency across documents
2. Verify cross-references are accurate
3. Ensure tone matches audience level
4. Add file header with metadata (date, version, maintainer)

---

## Document Selection Guide

| Project Type | Recommended Docs |
|--------------|------------------|
| Simple script/tool | Principles + Quick Reference |
| API or service | All 4 documents |
| Framework/library | All 4 documents |
| Architecture explanation | Architecture + Principles |
| Onboarding documentation | Navigation Index + Quick Reference |
| Internal system | Architecture + Principles |

---

## Output Format

Name each document with the Chinese filename as primary, English as secondary (optional):

docs/
├── 技术原理文档.md
├── 架构与流程可视化.md
├── 快速参考指南.md
└── 文档索引.md
Or for English-preferred projects:

docs/
├── technical-principles.md
├── architecture-visualization.md
├── quick-reference.md
└── navigation-index.md
---

## Tips for Better Documentation

- **Be specific**: Use actual names, values, and examples
- **Show don't tell**: Code examples > paragraphs of explanation
- **Consider the reader**: What do they already know?
- **Update regularly**: Documentation rots; mark when last verified
- **One concept per section**: Easier to scan and reference