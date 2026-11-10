---
name: industrial-brutalist-ui
description: Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian color, analog degradation effects. For data-heavy dashboards, portfolios, or editorial sites that need to feel like declassified blueprints.
---

# SKILL: Industrial Brutalist UI

## 1. Overview

This skill defines the principles and techniques for building web interfaces that merge mid-century Swiss typographic design with industrial manufacturing aesthetics and retro-futuristic military terminal interfaces. The resulting interfaces project raw functionality, mechanical precision, and high data density—deliberately rejecting conventional consumer UI patterns.

**Core Philosophy:** Function as aesthetic. Structure as ornament. Data as design material.

## 2. Visual Modes

Choose ONE mode per project. Do not mix modes within the same interface.

### 2.1 Swiss Industrial Print

**Inspiration:** 1960s corporate identity systems, heavy machinery blueprints, engineering datasheets.

**Characteristics:**
- Light mode only (newsprint, off-white, cream substrates)
- Monolithic, heavy sans-serif typography (e.g., Neue Haas Grotesk, Akkurat, Aktiv Grotesk)
- Rigid modular grids with visible dividing lines
- Asymmetric negative space
- Oversized numerals or letterforms that bleed to viewport edges
- Primary red as the dominant accent/alert color
- Minimal ornamentation—structure is the decoration

**Color Palette:**
css
:root {
  --paper: #F5F2EB;
  --ink: #1A1A1A;
  --grid-line: #CCCCCC;
  --accent-red: #E8000D;
  --accent-blue: #0047AB;
}
### 2.2 Tactical Telemetry / CRT Terminal

**Inspiration:** Classified military databases, legacy mainframes, aerospace HUDs, NORAD readouts.

**Characteristics:**
- Dark mode exclusivity
- High-density tabular data presentation
- Monospaced typography throughout (e.g., IBM Plex Mono, JetBrains Mono, Space Mono)
- ASCII framing devices: `[ ]`, `{ }`, `//`, `||`
- Crosshairs, reticles, coordinate grids
- Simulated hardware limitations

**Color Palette:**
css
:root {
  --terminal-bg: #0A0A0A;
  --phosphor-green: #33FF33;
  --phosphor-amber: #FFB000;
  --scanline: rgba(0, 0, 0, 0.3);
  --grid-dim: #1A3A1A;
  --alert-red: #FF3333;
}
## 3. Typography System

Typography is the primary structural element. Imagery is secondary.

### 3.1 Scale & Hierarchy

Create extreme contrast between type sizes. The system relies on jarring scale shifts.

| Role | Size | Weight | Leading |
|------|------|--------|---------|
| Display | 8rem – 20vw | 700–900 | 0.85 |
| H1 | 4rem – 8rem | 700 | 1.0 |
| H2 | 2rem – 4rem | 500 | 1.1 |
| Body | 1rem (16px) | 400 | 1.5 |
| Caption/Label | 0.75rem | 700 | 1.2 |
| Data/Mono | 0.875rem | 400 | 1.4 |

**Key Rule:** Body text should feel lost between the massive display type and dense data labels.

### 3.2 Spacing

- Use fixed units (px, rem) — never fluid scaling
- Generous margins at macro scale
- Tight gutters at micro scale
- Grid subdivisions: 8px base unit

css
:root {
  --space-unit: 8px;
  --space-xs: calc(var(--space-unit) * 1);   /* 8px */
  --space-sm: calc(var(--space-unit) * 2);   /* 16px */
  --space-md: calc(var(--space-unit) * 4);   /* 32px */
  --space-lg: calc(var(--space-unit) * 8);   /* 64px */
  --space-xl: calc(var(--space-unit) * 16);  /* 128px */
}
## 4. Grid System

### 4.1 Swiss Industrial Grid

12-column grid with visible borders and generous gutters.

css
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1px;
  background-color: var(--ink);
  border: 2px solid var(--ink);
}

.grid-cell {
  background-color: var(--paper);
  padding: var(--space-md);
}
### 4.2 Terminal Grid

Dense, borderless table structures with ASCII dividers.

css
.data-table {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.875rem;
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  border-bottom: 1px solid var(--phosphor-green);
  padding: var(--space-sm);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.data-table td {
  padding: var(--space-sm);
  border-bottom: 1px solid var(--grid-dim);
}
## 5. Analog Degradation Effects

Apply these effects to simulate CRT monitors, aged newsprint, or industrial wear.

### 5.1 Scanlines (CRT)

css
.scanlines::after {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    to bottom,
    transparent 0px,
    transparent 2px,
    rgba(0, 0, 0, 0.15) 2px,
    rgba(0, 0, 0, 0.15) 4px
  );
  pointer-events: none;
  z-index: 9999;
}
### 5.2 Phosphor Glow

css
.phosphor-glow {
  text-shadow: 
    0 0 2px var(--phosphor-green),
    0 0 8px var(--phosphor-green),
    0 0 20px rgba(51, 255, 51, 0.4);
}
### 5.3 Halftone / Newsprint Texture

css
.halftone {
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.08'/%3E%3C/svg%3E");
}
### 5.4 Low-Bit Depth Dithering

css
.dithered {
  image-rendering: pixelated;
  /* Or simulate with CSS: */
  filter: contrast(1.2) brightness(0.95);
}
## 6. Component Patterns

### 6.1 Navigation (Swiss Industrial)

html
<nav class="nav-bar">
  <div class="nav-logo">CORP. IDENT. // 1962</div>
  <ul class="nav-links">
    <li><a href="#">DATASHEETS</a></li>
    <li><a href="#">SPECIFICATIONS</a></li>
    <li><a href="#">ARCHIVE</a></li>
  </ul>
  <div class="nav-ref">REF: DOC-7734-A</div>
</nav>
### 6.2 Data Card (Terminal)

html
<div class="terminal-card">
  <div class="card-header">
    <span class="card-label">[ SYS.STATUS ]</span>
    <span class="card-id">NODE-7F91</span>
  </div>
  <div class="card-body">
    <div class="data-row">
      <span class="label">TEMP</span>
      <span class="value">847.3°C</span>
    </div>
    <div class="data-row">
      <span class="label">PRESSURE</span>
      <span class="value">12.4 kPa</span>
    </div>
    <div class="data-row">
      <span class="label">STATUS</span>
      <span class="value status-nominal">NOMINAL</span>
    </div>
  </div>
</div>
### 6.3 Buttons

css
.btn-brutalist {
  background: var(--ink);
  color: var(--paper);
  border: 3px solid var(--ink);
  padding: var(--space-sm) var(--space-md);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.1s;
}

.btn-brutalist:hover {
  background: var(--accent-red);
  border-color: var(--accent-red);
}

.btn-terminal {
  background: transparent;
  color: var(--phosphor-green);
  border: 1px solid var(--phosphor-green);
  font-family: 'IBM Plex Mono', monospace;
  text-transform: uppercase;
  padding: var(--space-sm) var(--space-md);
}

.btn-terminal:hover {
  background: var(--phosphor-green);
  color: var(--terminal-bg);
  box-shadow: 0 0 10px var(--phosphor-green);
}
## 7. Layout Principles

1. **Asymmetry is mandatory.** Center-aligned layouts are forbidden.
2. **Overflow is acceptable.** Display text may bleed off-screen.
3. **Whitespace is structural, not decorative.** Large gaps separate content modules.
4. **Borders define hierarchy.** Box shadows are prohibited.
5. **Data density is a feature.** Don't hide information—display it with authority.

## 8. Anti-Patterns (What to Avoid)

- Rounded corners (border-radius: 0 is the only acceptable value)
- Drop shadows
- Gradient backgrounds
- Icon libraries (use ASCII, Unicode, or custom SVG marks)
- Stock photography
-柔性布局（fluid typography, percentage-based widths for structural elements）
- Hamburger menus
- Loading spinners (use progress bars or status text)

## 9. Implementation Checklist

- [ ] Define CSS custom properties for color and spacing
- [ ] Choose and implement grid system
- [ ] Select typography scale and apply classes
- [ ] Build 3–5 core components (nav, card, button, table, form)
- [ ] Add analog effects (scanlines, halftone, or glow)
- [ ] Test data-heavy scenarios—ensure density feels intentional
- [ ] Verify all interactive elements have visible focus states