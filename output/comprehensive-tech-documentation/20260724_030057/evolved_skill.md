---
category: software-development
description: "Creates layered, comprehensive technical documentation for projects, skills, or systems. Use when user requests 'write technical documentation', 'explain how this works', or 'document the architecture'. Produces 3-4 documents with different depths and purposes."
name: comprehensive-tech-documentation
---

# Comprehensive Technical Documentation

Creates a complete documentation suite that serves different audiences and use cases, from quick reference to deep technical analysis.

## When to Use

Use this skill when the user requests:

- "写技术文档" / "Write technical documentation"
- "解释原理" / "Explain how it works"
- "画架构图" / "Draw architecture diagram"
- "快速参考" / "Quick reference guide"
- "写导航索引" / "Create documentation index"
- Any request to document a system, skill, or architecture

## Documentation Suite

| User Request | Output |
|--------------|--------|
| General documentation | Full 4-document suite |
| Explain how it works | Technical Principles + Architecture |
| Quick reference only | Quick Reference Guide |
| Visual diagrams | Architecture Visualization |
| Navigation/index | Navigation Index |

## The Four Documents

### 1. 📖 Technical Principles (`技术原理文档.md`)

**Purpose**: Deep understanding of the system

**Contains**:
- System overview and purpose
- Design philosophy and decisions
- Core concepts and terminology
- Implementation details
- Best practices and patterns
- Known limitations

**Target audience**: Developers, contributors  
**Reading time**: 30-60 minutes

---

### 2. 📊 Architecture Visualization (`架构与流程可视化.md`)

**Purpose**: Visual representation of structure and flow

**Contains**:
- System architecture diagram (Mermaid)
- Component relationships
- Data flow diagrams
- Sequence diagrams for key operations
- State machines (if applicable)
- ERD for data models

**Target audience**: Architects, visual learners  
**Reading time**: 15-30 minutes

---

### 3. 🔖 Quick Reference Guide (`快速参考指南.md`)

**Purpose**: Rapid lookup during actual use

**Contains**:
- Quick start commands
- Template snippets
- Common use cases with examples
- Field/parameter definitions
- Configuration options
- Troubleshooting common issues
- FAQ

**Target audience**: All users (most frequently accessed)  
**Reading time**: 5-15 minutes

---

### 4. 🗺️ Navigation Index (`README-文档索引.md`)

**Purpose**: Guide users to the right document

**Contains**:
- Document overview table
- Learning paths by role
- Scenario-based navigation
- FAQ with document links
- Changelog or version info

**Target audience**: First-time users, anyone seeking guidance  
**Reading time**: 5 minutes

---

## Workflow

### Phase 1: Discovery

Gather information about the system:

1. **Identify the subject**: What are we documenting? (skill, project, system, API)
2. **Determine scope**: What should be included vs excluded?
3. **Understand the audience**: Developers? End users? Architects?
4. **Collect artifacts**: Existing code, specs, diagrams, or explanations

### Phase 2: Analysis

Analyze the system to understand:

- **Core components**: What are the main building blocks?
- **Relationships**: How do components interact?
- **Data flows**: What data moves through the system?
- **Processes**: What operations does the system perform?
- **Edge cases**: What are error states and boundaries?

### Phase 3: Document Creation

Create documents in order of dependency:

1. **Technical Principles** — Foundation for all other docs
2. **Architecture Visualization** — Visual representation of principles
3. **Quick Reference Guide** — Practical applications of the above
4. **Navigation Index** — Guide to access all documents

### Phase 4: Review

Ensure quality:

- [ ] All documents are internally consistent
- [ ] Diagrams match written descriptions
- [ ] Examples are accurate and runnable
- [ ] Cross-references between docs are correct
- [ ] Terminology is consistent throughout

---

## Output Format

Each document should follow this structure:

markdown
# [Document Title]

## Overview
Brief description of what this document covers.

## [Main Sections]
Content with appropriate headings.

## Quick Links
Links to related documents in the suite.
## Mermaid Diagram Standards

Use consistent styling for diagrams:

mermaid
graph TD
    A[Component A] --> B[Component B]
    B --> C[Component C]
    C --> D[(Data Store)]
    
    style A fill:#e1f5fe
    style D fill:#fff3e0
---

## Example Output

For a skill called "code-reviewer", create:

技术原理文档.md      - How the skill analyzes code
架构与流程可视化.md  - Mermaid diagrams of the review flow
快速参考指南.md      - Commands and templates for users
README-文档索引.md   - How to navigate the docs