---
name: stitch-design-taste
description: Semantic Design System Skill for Google Stitch. Generates agent-friendly DESIGN.md files that enforce premium, anti-generic UI standards — strict typography, calibrated color, asymmetric layouts, perpetual micro-motion, and hardware-accelerated performance.
---

# Stitch Design Taste — Semantic Design System Skill

## Overview

This skill generates `DESIGN.md` files optimized for Google Stitch screen generation. It translates battle-tested anti-generic frontend engineering directives into Stitch's native semantic design language — descriptive, natural-language rules paired with precise values that Stitch's AI agent can interpret to produce premium, non-generic interfaces.

The generated `DESIGN.md` serves as the **single source of truth** for prompting Stitch to generate new screens that align with a curated, high-agency design language.

## Prerequisites

- Access to Google Stitch via [labs.google/stitch](https://labs.google/stitch)
- Optional: Stitch MCP Server for programmatic integration with Cursor, Antigravity, or Gemini CLI

## Core Objectives

Generate a `DESIGN.md` file that encodes:

1. **Visual atmosphere** — mood, density, and design philosophy
2. **Color calibration** — neutrals, accents, and explicitly banned patterns with hex codes
3. **Typographic architecture** — font stacks, scale hierarchy, and anti-patterns
4. **Component behaviors** — buttons, cards, inputs with interaction states
5. **Layout principles** — grid systems, spacing philosophy, responsive strategy
6. **Motion philosophy** — animation engine specs, spring physics, perpetual micro-interactions
7. **Anti-patterns** — explicit list of banned AI design clichés

---

## Analysis & Synthesis Instructions

### Step 1: Define the Atmosphere

Evaluate the target project's intent using these taste spectrum scales:

| Dimension | Scale |
|-----------|-------|
| **Density** | `1` Art Gallery Airy → `5` Daily App Balanced → `10` Cockpit Dense |
| **Variance** | `1` Predictable Symmetric → `5` Offset Asymmetric → `10` Artsy Chaotic |
| **Motion** | `1` Static Restrained → `5` Fluid CSS → `10` Cinematic Choreography |

**Default baseline:** Variance `8`, Motion `6`, Density `4`

Adapt dynamically based on the user's vibe description. Document chosen values explicitly in the output.

### Step 2: Map the Color Palette

For each color, provide:

- **Descriptive Name** (e.g., "Warm Stone", "Electric Indigo")
- **Hex Code** (e.g., `#1A1A1E`)
- **Functional Role** (e.g., "Primary background", "Interactive accent", "Semantic error")

**Required sections:**

Backgrounds (2-3):   Page, Surface, Elevated
Text (3-4):          Primary, Secondary, Tertiary, Inverse
Accents (2-3):       Interactive, Emphasis, System
Neutrals (2-3):      Border, Divider, Overlay
Semantics (0-4):     Success, Warning, Error, Info
### Step 3: Define Typography Architecture

**Font Stack Specification:**

Display:     "Instrument Serif", Georgia, serif
Body:        "Inter", -apple-system, sans-serif
Mono:        "JetBrains Mono", "Fira Code", monospace
**Scale Hierarchy:**

| Role | Size | Weight | Line Height | Letter Spacing |
|------|------|--------|-------------|----------------|
| Hero | 64px | 400 | 1.0 | -0.03em |
| H1 | 48px | 600 | 1.1 | -0.02em |
| H2 | 32px | 600 | 1.2 | -0.01em |
| H3 | 24px | 600 | 1.3 | 0 |
| Body | 16px | 400 | 1.5 | 0 |
| Caption | 13px | 500 | 1.4 | 0.02em |

**Anti-patterns to ban:**

- All caps headings
- Under 14px body text
- Font weights below 400 for body copy
- System fonts as primary (Arial, Helvetica, Times New Roman)

### Step 4: Document Component Behaviors

Define interaction states for each component type:

**Buttons:**

Default:   bg: accent, text: white, shadow: none
Hover:     bg: accent-darken-10%, transform: translateY(-1px)
Active:    bg: accent-darken-15%, transform: translateY(0)
Disabled:  bg: neutral-200, text: neutral-500, cursor: not-allowed
Loading:   opacity: 0.7, spinner visible
**Cards:**

Default:   bg: surface, border: 1px neutral-200, radius: 16px
Hover:     border-color: accent, shadow: 0 8px 32px rgba(0,0,0,0.08)
Active:    shadow: 0 2px 8px rgba(0,0,0,0.04)
**Inputs:**

Default:   border: 1px neutral-300, bg: white
Focus:     border: 2px accent, ring: 4px accent/20%
Error:     border: 2px semantic-error, ring: none
Disabled:  bg: neutral-100, text: neutral-400
### Step 5: Establish Layout Principles

**Grid System:**

Columns:    12 (desktop), 6 (tablet), 4 (mobile)
Gutter:     24px (desktop), 16px (mobile)
Max Width:  1280px
Margin:     24px (mobile), 48px (tablet), 80px (desktop)
**Spacing Scale:**

space-1:   4px    (micro gaps)
space-2:   8px    (tight grouping)
space-3:   16px   (component internal)
space-4:   24px   (between components)
space-6:   40px   (section padding)
space-8:   64px   (major section breaks)
space-12:  96px   (hero padding)
**Asymmetry Rule:**
Avoid center-aligned layouts. Use intentional offsets: text blocks at 60-70% width, images bleeding edge-to-edge, navigation offset from grid.

### Step 6: Specify Motion Philosophy

**Spring Physics Presets:**

Snappy:    mass: 0.8, tension: 400, friction: 30
Smooth:    mass: 1, tension: 200, friction: 25
Bouncy:    mass: 1.2, tension: 300, friction: 15
**Duration Scale:**

| Type | Duration |
|------|----------|
| Micro (hover, toggle) | 120-200ms |
| Standard (expand, collapse) | 250-350ms |
| Emphasis (reveals, modals) | 400-500ms |
| Choreography (stagger delay) | 60-100ms per item |

**Perpetual Motion Rule:**
Never create fully static interfaces. Every idle state should contain subtle ambient motion:

- Breathing shadows on cards (opacity 0.4→0.6, 3s loop)
- Gentle gradient shifts on backgrounds
- Floating elements with subtle Y translation
- Cursor-following parallax on hero sections

**GPU Acceleration:**
Always use `transform` and `opacity` for animations. Never animate `top`, `left`, `width`, `height`, or `margin` directly.

### Step 7: Enumerate Anti-Patterns

Explicitly ban these AI design clichés:

- **Gradients:** Full-bleed gradient backgrounds (subtle gradients ≤15° angle OK)
- **Glassmorphism:** Frosted glass effects, backdrop-blur on everything
- **Shadows:** Default drop shadows without intentional direction/intensity
- **Typography:** Inter as body font, generic system fonts
- **Icons:** Phosphor/Lucide icon sets as default (specify alternatives)
- **Colors:** Pure white `#FFFFFF` backgrounds, pure black `#000000` text
- **Borders:** Uniform 1px borders everywhere
- **Spacing:** Even 8px/16px/24px rhythm with no variation
- **Cards:** Equal padding (24px) on all cards regardless of content
- **Shadows:** Blue-tinted shadows on cards (e.g., `rgba(59, 130, 246, 0.1)`)
- **Layouts:** Centered hero text, symmetrical grids, equal-width columns
- **Images:** Rounded corner images inside rounded cards (visual redundancy)
- **Interactions:** Instant state changes, no hover/focus feedback

---

## Output Format

Structure the generated `DESIGN.md` as follows:

markdown
# Design Language — [Project Name]

## Atmosphere
- Density: [1-10]
- Variance: [1-10]
- Motion: [1-10]
- Tone: [2-3 sentence vibe description]

## Color System
[Table with Name | Hex | Role for each color]

## Typography
[Font stack and scale table]

## Components
[Interaction specs for each component type]

## Layout
[Grid, spacing, and asymmetry rules]

## Motion
[Spring presets, duration scale, ambient motion specs]

## Anti-Patterns
[Explicit banned patterns list]
---

## Usage Notes

1. **Review before use:** Always validate generated colors for contrast ratios (minimum 4.5:1 for body text)
2. **Iterate with Stitch:** Use initial `DESIGN.md` as baseline, refine based on Stitch's output
3. **Override explicitly:** Any design decision not covered defaults to "professional restraint" — avoid rather than guess
4. **Version control:** Include a `version: "1.0"` field in the frontmatter for tracking iterations