---
category: software-development
description: "Creates layered, comprehensive technical documentation for projects, skills, or systems. Use when user requests 'write technical documentation', 'explain how this works', or 'document the architecture'. Produces 3-4 documents with different depths and purposes."
name: comprehensive-tech-documentation
---

# Comprehensive Technical Documentation

Creates a complete documentation suite that serves different audiences and use cases, from quick reference to deep technical analysis.

## Quick Reference

| User Request | Documentation Output |
|--------------|---------------------|
| `"写技术文档"` or `"Write docs"` | Full 4-document suite |
| `"解释原理"` or `"Explain how it works"` | Technical Principles + Architecture |
| `"快速参考"` or `"Quick reference"` | Quick Reference Guide only |
| `"画架构图"` or `"Draw architecture"` | Architecture Visualization only |
| `"写导航索引"` or `"Create index"` | Navigation Index only |

## When to Use This Skill

Use this skill when you need to document:

- Complex systems with multiple components
- APIs or SDKs with multiple endpoints
- Architecture spanning multiple services
- Projects requiring onboarding documentation
- Systems needing both conceptual and practical guidance

## The Documentation Suite

Create these documents based on project scope (all 4 for full projects, select relevant ones for smaller scope):

### 1. 📖 Technical Principles (技术原理文档.md)

**Purpose**: Deep understanding of how the system works

**Contents**:
- System overview and design philosophy
- Core concepts and terminology
- Detailed implementation explanation
- Design decisions and trade-offs
- Best practices and patterns
- Known limitations

**Target audience**: Developers, contributors, technical leads
**Reading time**: 30-60 minutes

---

### 2. 📊 Architecture Visualization (架构与流程可视化.md)

**Purpose**: Visual representation of system structure

**Contents**:
- Mermaid architecture diagrams
- Component relationship diagrams
- Data flow diagrams
- Sequence diagrams for key workflows
- State machines
- Deployment topology

**Target audience**: Architects, technical leads, visual learners
**Reading time**: 15-30 minutes

---

### 3. 🔖 Quick Reference Guide (快速参考指南.md)

**Purpose**: Fast lookup for common tasks

**Contents**:
- Getting started steps
- Command cheat sheets
- Configuration templates
- Field/type definitions
- Common patterns with examples
- Troubleshooting guide
- FAQ with solutions

**Target audience**: All users (most frequently accessed)
**Reading time**: 5-15 minutes

---

### 4. 🗺️ Navigation Index (README-文档索引.md or 文档索引.md)

**Purpose**: Guide users to the right document

**Contents**:
- Document overview table
- Learning paths by role
- Scenario-based navigation guide
- Quick decision tree
- FAQ linking to relevant sections

**Target audience**: First-time users, anyone needing orientation
**Reading time**: 5 minutes

---

## Step-by-Step Workflow

### Phase 1: Analysis

1. **Identify the system scope**
   - What are the core components?
   - Who are the target users?
   - What is the deployment context?

2. **Determine documentation scope**
   - Full suite (4 docs): Complex systems, new projects
   - Core + Quick Ref (2-3 docs): APIs, tools, libraries
   - Single doc: Specific features, minor additions

3. **Gather information**
   - Review existing code or specifications
   - Identify key concepts and relationships
   - Note common questions or pain points

### Phase 2: Document Creation

**Create documents in this order** (each informs the next):

1. **Technical Principles** → Foundation for all other docs
2. **Architecture Visualization** → Visual representation of principles
3. **Quick Reference Guide** → Practical application of principles
4. **Navigation Index** → Entry point linking all documents

### Phase 3: Review

1. Verify consistency across documents
2. Ensure cross-references are accurate
3. Check that all code examples work
4. Validate diagram accuracy
5. Confirm audience appropriateness

---

## Document Naming Convention

| Document Type | English Filename | Chinese Filename |
|---------------|------------------|------------------|
| Technical Principles | `TECHNICAL_PRINCIPLES.md` | `技术原理文档.md` |
| Architecture | `ARCHITECTURE.md` | `架构与流程可视化.md` |
| Quick Reference | `QUICK_REFERENCE.md` | `快速参考指南.md` |
| Navigation Index | `README.md` or `DOCUMENTATION_INDEX.md` | `文档索引.md` |

---

## Output Format

Generate each document as a complete, standalone file with:

- Clear frontmatter (if applicable)
- Descriptive headings
- Code blocks with language hints
- Diagrams with Mermaid syntax
- Tables for structured information
- Cross-references to related documents

---

## Example Response Structure

When generating a full suite:

markdown
## Documentation Suite Created

### 📖 Technical Principles
[Full document content]

### 📊 Architecture Visualization
[Full document content]

### 🔖 Quick Reference Guide
[Full document content]

### 🗺️ Navigation Index
[Full document content]