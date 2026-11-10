---
name: stitch-design-taste
description: Semantic Design System Skill for Google Stitch. Generates agent-friendly DESIGN.md files that enforce premium, anti-generic UI standards — strict typography, calibrated color, asymmetric layouts, perpetual micro-motion, and hardware-accelerated performance.
---

# Stitch Design Taste

A semantic design system skill for generating Stitch-ready `DESIGN.md` files. Translates anti-generic UI principles into Stitch's natural-language format so the AI agent produces premium, non-corporate interfaces.

## Purpose

This skill produces a `DESIGN.md` file that serves as the **single source of truth** for all screen generation in Google Stitch. Stitch interprets design through descriptive "Visual Descriptions" paired with precise values. The generated file encodes:

- Visual atmosphere and mood
- Calibrated color palettes with hex codes
- Typographic hierarchy and font specifications
- Component interaction states
- Layout principles and grid systems
- Motion philosophy with physics specs
- Explicitly banned AI design clichés

## Prerequisites

- Access to Google Stitch at [labs.google/stitch](https://labs.google/stitch)
- Optional: Stitch MCP Server for programmatic integration (Cursor, Antigravity, Gemini CLI)

## Output Structure

Generate a `DESIGN.md` file containing these sections in order:

### 1. Atmosphere

Define three axes with scores from 1–10:

| Axis | Scale | Description |
|------|-------|-------------|
| **Density** | 1–3: "Art Gallery Airy" · 4–7: "Daily App Balanced" · 8–10: "Cockpit Dense" | Information density and whitespace ratio |
| **Variance** | 1–3: "Predictable Symmetric" · 4–7: "Offset Asymmetric" · 8–10: "Artsy Chaotic" | Layout predictability and visual tension |
| **Motion** | 1–3: "Static Restrained" · 4–7: "Fluid CSS" · 8–10: "Cinematic Choreography" | Animation ambition and interaction feedback |

**Default baseline:** Variance 8, Motion 6, Density 4. Adjust based on project description.

Include 2–3 evocative adjectives capturing the mood (e.g., "confident minimalism," "editorial warmth," "technical precision").

### 2. Color System

For each color, provide:

[Descriptive Name] — #HEXCODE
Role: [functional description]
Usage: [where/how to apply]
**Required entries:**

- **Background Primary** — base surface
- **Background Secondary** — elevated surfaces, cards
- **Background Tertiary** — modals, overlays
- **Text Primary** — headings, key content
- **Text Secondary** — body, descriptions
- **Text Tertiary** — captions, metadata
- **Accent Primary** — CTAs, key actions
- **Accent Secondary** — supporting highlights
- **Semantic Colors** — success, warning, error, info (if applicable)

**Example entry:**

Slate — #1A1A2E
Role: Deep neutral background
Usage: Primary surfaces, creates depth contrast
**Rules:**

- Provide exact hex codes, never vague names like "dark blue"
- Limit palette to 8–12 distinct colors maximum
- Ensure sufficient contrast ratios (4.5:1 minimum for body text)

### 3. Typography

Define the complete font stack:

Primary: [Font Name] — [weights] — Fallback stack
[Usage description and hierarchy]

Secondary: [Font Name] — [weights] — Fallback stack
[Usage description and hierarchy]

Mono: [Font Name] — [weights] — Fallback stack
[Usage for code, data, technical elements]
**Type Scale:**

| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Display | [n]px | [w] | [lh] | Hero headlines |
| H1 | [n]px | [w] | [lh] | Page titles |
| H2 | [n]px | [w] | [lh] | Section headers |
| H3 | [n]px | [w] | [lh] | Subsection headers |
| Body | [n]px | [w] | [lh] | Default text |
| Caption | [n]px | [w] | [lh] | Supporting text |
| Mono | [n]px | [w] | [lh] | Code, data |

**Anti-patterns:**

- Never use Inter, Roboto, Arial, or system-ui as primary fonts
- Avoid numeric font sizes (use px or rem consistently)
- No all-caps for body text

### 4. Components

Define each UI element with states:

#### Buttons

Primary Button
Default: [bg], [text], [border-radius]
Hover: [bg shift], [shadow], [transform]
Active: [scale], [bg darken]
Disabled: [opacity], [cursor: not-allowed]
Loading: [spinner], [text: "..."]
#### Cards

Surface Card
Default: [bg], [border], [shadow], [border-radius]
Hover: [shadow lift], [border highlight]
Interactive: [cursor pointer], [slight scale on hover]
#### Inputs

Text Input
Default: [bg], [border], [placeholder color]
Focus: [border color], [ring/glow]
Error: [border color], [error text], [icon]
Filled: [text color], [clear button visibility]
### 5. Layout System

**Grid:**

- Column count: [n]
- Gutter: [n]px
- Margin: [n]px (mobile) / [n]px (desktop)
- Max content width: [n]px

**Spacing Scale:**

4px  — micro gaps, icon padding
8px  — tight grouping
12px — default element spacing
16px — section padding
24px — card padding
32px — section gaps
48px — major section breaks
64px+ — hero spacing
**Responsive Strategy:**

- Mobile breakpoint: [n]px
- Tablet breakpoint: [n]px
- Desktop breakpoint: [n]px
- [Describe mobile-first adjustments]

**Layout Rules:**

- No equal padding on all sides (use asymmetric spacing)
- Offset elements intentionally — avoid perfect grid alignment
- Stack vertically on mobile; consider side-by-side on desktop
- Use negative space as an active design element

### 6. Motion Philosophy

**Animation Engine:** CSS transitions and keyframes (avoid JS animation libraries unless specified)

**Spring Physics:**

Standard: mass 1, stiffness [n], damping [n]
Snappy: mass 1, stiffness [n], damping [n]
Bouncy: mass 1, stiffness [n], damping [n]
**Duration Scale:**

| Speed | Duration | Usage |
|-------|----------|-------|
| Instant | 100ms | Micro-interactions, hover states |
| Fast | 150–200ms | Buttons, toggles |
| Normal | 250–300ms | Cards, modals |
| Slow | 400–500ms | Page transitions |
| Dramatic | 600ms+ | Hero animations |

**Easing:**

- `cubic-bezier(0.4, 0, 0.2, 1)` — standard ease
- `cubic-bezier(0, 0, 0.2, 1)` — decelerate (enter)
- `cubic-bezier(0.4, 0, 1, 1)` — accelerate (exit)
- `cubic-bezier(0.68, -0.55, 0.265, 1.55)` — overshoot

**Perpetual Micro-Motion:**

- Hover: subtle scale (1.02), shadow lift, color shift
- Focus: ring appears with fade-in
- Active: slight press-down (scale 0.98)
- Page load: staggered fade-in for lists (50ms delay between items)
- Scroll: parallax on hero images, sticky header with backdrop blur

**Performance Rules:**

- Use `transform` and `opacity` only for animations
- Never animate `width`, `height`, `top`, `left`, `margin`
- Apply `will-change` sparingly for complex animations
- Test on low-end devices

### 7. Anti-Patterns

Explicitly ban these AI design clichés:

- ❌ "Get Started" or "Welcome to [App]" hero text
- ❌ Generic illustration sets (blob backgrounds, generic people)
- ❌ Rounded corners everywhere (8px radius maximum)
- ❌ Gradient backgrounds (dark → darker only, or solid)
- ❌ Notification dots on every nav item
- ❌ Floating action buttons without consideration
- ❌ Full-width banners or hero sections
- ❌ "Loading..." skeleton screens with gray rectangles
- ❌ Bottom sheet modals for critical actions
- ❌ Card-heavy layouts with no visual hierarchy
- ❌ Avatar circles with gradient backgrounds
- ❌ "Last updated" or "v1.0" badges in UI
- ❌ Decorative underlines on links
- ❌ Hamburger menus on desktop

**Replace with:**

- ✅ Specific, contextual microcopy
- ✅ High-quality photography or intentional abstract graphics
- ✅ Sharp corners (0–4px) or generous rounding (12–16px)
- ✅ Deep, layered backgrounds with subtle color shifts
- ✅ Selective notification indicators (only for critical items)
- ✅ Contextual action placement (FAB is a decision, not a default)
- ✅ Contained, breathing layouts with asymmetric composition
- ✅ Skeleton screens with actual content structure
- ✅ Centered modal dialogs for critical actions
- ✅ Varied card treatment: some elevated, some flat, some outlined
- ✅ Authentic photography or minimal abstract shapes
- ✅ Version info in settings or footer only
- ✅ No underlines; use color, weight, or underline on hover only
- ✅ Collapsed hamburger menu only when nav items are 5+

### 8. Visual Description Template

Include this template at the end of `DESIGN.md` for Stitch reference:

markdown
## Visual Description for Stitch

When generating screens, use this format:

"[Component name] in [state]: A [adjective] [element type] featuring [specific color] [background/text/border], [typography spec], with [motion behavior] on interaction. [Any special treatment or positioning]."

Example:
"Primary button in default state: A confident rectangular button featuring deep navy (#0A1628) background with bright coral (#FF6B4A) text in 14px medium-weight sans-serif, with no border-radius, scaling to 0.98 on press with a 150ms ease-out transition."
## Usage Instructions

1. **Collect inputs** — Review project brief, existing designs, or user description
2. **Set baseline** — Choose default scores or adjust for project needs
3. **Map palette** — Define colors with precise hex codes and roles
4. **Define typography** — Specify fonts, sizes, weights, line heights
5. **Document components** — Cover states for buttons, cards, inputs, nav
6. **Establish layout** — Define grid, spacing scale, responsive breakpoints
7. **Specify motion** — Set duration, easing, spring physics, micro-interactions
8. **Ban clichés** — List anti-patterns explicitly
9. **Add template** — Include Visual Description format for Stitch agents

## Integration

Reference this `DESIGN.md` in all Stitch prompts:

Following the design system in DESIGN.md, generate [screen description].
The file ensures consistent, premium output across all generated screens.