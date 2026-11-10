---
name: industrial-brutalist-ui
description: Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian color, analog degradation effects. For data-heavy dashboards, portfolios, or editorial sites that need to feel like declassified blueprints.
---

# SKILL: Industrial Brutalism & Tactical Telemetry UI

## 1. Skill Overview

**Name:** Industrial Brutalism & Tactical Telemetry Interface Engineering
**Discipline:** Web interface architecture synthesizing mid-century Swiss typographic design, industrial manufacturing manuals, and retro-futuristic aerospace/military terminal interfaces.
**Objective:** Construct digital environments that project raw functionality, mechanical precision, and high data density — deliberately discarding conventional consumer UI patterns.

## 2. Visual Archetypes

Choose ONE paradigm per project. Do not alternate or mix modes within the same interface.

### 2.1 Swiss Industrial Print

Derived from 1960s corporate identity systems and heavy machinery blueprints.

**Characteristics:**
- High-contrast light modes (newsprint/off-white substrates)
- Monolithic, heavy sans-serif typography
- Unforgiving structural grids with visible dividing lines
- Aggressive, asymmetric negative space
- Oversized viewport-bleeding numerals or letterforms
- Primary red as alert/accent color
- Helvetica, Akzidenz-Grotesk, or Univers typefaces

**Mood Reference:** Braun catalogs, Zurich airport signage, cold war-era technical manuals

### 2.2 Tactical Telemetry & CRT Terminal

Derived from classified military databases, legacy mainframes, and aerospace HUDs.

**Characteristics:**
- Dark mode exclusivity
- High-density tabular data presentation
- Monospaced typography dominance
- Technical framing devices (ASCII brackets, crosshairs, coordinate markers)
- Simulated hardware limitations
- Phosphor glow, scanlines, low bit-depth rendering
- VT323, Space Mono, or IBM Plex Mono typefaces

**Mood Reference:** WarGames (1983), NORAD terminals, submarine sonar displays

## 3. Typographic Architecture

Typography serves as primary structural infrastructure. Imagery is secondary.

### 3.1 Scale System

Use extreme variance in scale, weight, and spacing:

Display:    8rem - 20rem     (headlines, hero numerals)
H1:         3rem - 6rem      (section headers)
H2:         1.5rem - 3rem    (subsection labels)
Body:       1rem - 1.125rem  (readable density)
Caption:    0.75rem - 0.875rem (metadata, timestamps)
Mono:       0.625rem - 0.875rem (data readouts)
### 3.2 Weight Distribution

- Heavy weights (700-900) for structural elements
- Light weights (300-400) for secondary content
- No medium weights — extremes only
- Letter-spacing: tight (-0.02em to -0.05em) for display, loose (0.1em to 0.2em) for labels

### 3.3 Line Height Rules

- Display text: 0.85 - 0.95 (tight, impactful)
- Body text: 1.2 - 1.4 (readable density)
- Data tables: 1.0 - 1.2 (tabular alignment)
- All caps labels: 1.5 - 2.0 (legibility compensation)

## 4. Color Systems

### 4.1 Swiss Industrial Palette

| Role | Hex | Usage |
|------|-----|-------|
| Background | `#F5F5F0` | Off-white newsprint base |
| Surface | `#FFFFFF` | Card backgrounds |
| Text Primary | `#1A1A1A` | Near-black body copy |
| Text Secondary | `#666666` | Metadata, captions |
| Grid Lines | `#CCCCCC` | Structural dividers |
| Accent Red | `#E8000D` | Alerts, critical data |
| Accent Yellow | `#FFD500` | Highlights, warnings |

### 4.2 Tactical Terminal Palette

| Role | Hex | Usage |
|------|-----|-------|
| Background | `#0A0A0A` | Deep black base |
| Surface | `#141414` | Elevated panels |
| Grid Lines | `#1F1F1F` | Subtle structure |
| Text Primary | `#00FF41` | Phosphor green |
| Text Secondary | `#008F11` | Dimmed readouts |
| Accent Cyan | `#00D4FF` | Interactive elements |
| Alert Red | `#FF2D2D` | Critical warnings |
| Amber | `#FFB000` | Caution states |

## 5. Grid System

### 5.1 Swiss Grid Specifications

- 12-column base grid
- Gutters: 1rem - 2rem (visible or implied)
- Margins: 2rem minimum (mobile), 4rem+ (desktop)
- Division lines: 1px solid, never subtle
- Asymmetric layouts preferred (7/5, 8/4, 9/3 splits)
- Content may break grid for emphasis (viewport bleeds)

### 5.2 Terminal Grid Specifications

- Character-based alignment (monospace grid)
- 80-character column width reference
- Box-drawing characters for structure (┌─┐│└┘)
- Coordinate overlays (0,0 origin markers)
- HUD-style framing elements

## 6. Analog Degradation Effects

Apply sparingly to simulate hardware limitations and material wear.

### 6.1 CRT Terminal Effects

- **Scanlines:** Horizontal lines at 2px intervals, 5-15% opacity
- **Phosphor glow:** Text-shadow with color-matched blur (0 0 10px)
- **Screen curvature:** Subtle barrel distortion on container edges
- **Flicker:** Opacity animation (99% to 100%) at 0.05s intervals
- **Vignette:** Radial gradient overlay darkening corners

### 6.2 Print Degradation Effects

- **Halftone:** CSS repeating-radial-gradient simulating dot screens
- **Ink bleed:** Text-shadow with slight blur and offset
- **Paper texture:** Noise overlay at 3-5% opacity
- **Registration marks:** Corner crop marks, color separation targets

### 6.3 Dithering Patterns

- Implement via CSS gradients for 1-bit aesthetic
- Use ordered dithering for images
- 2-color maximum (black/white or green/black)

## 7. Component Patterns

### 7.1 Data Tables

- Full-width with visible borders
- Alternating row backgrounds (subtle)
- Fixed headers with bottom border
- Monospace numerals, right-aligned
- Row hover: accent color highlight

### 7.2 Navigation

- Horizontal rule separators between items
- All caps labels
- Current state: underline or background block
- No rounded corners
- Size indicators for active sections

### 7.3 Buttons

- Rectangular only (no border-radius)
- 1px or 2px solid borders
- Uppercase text
- States: default, hover (invert), active (pressed block), disabled (50% opacity)
- Size: compact (28-32px height) or large (48-56px height)

### 7.4 Cards/Panels

- Visible border (1px solid)
- No shadows or minimal (1px offset)
- Header sections with heavy border-bottom
- Content padding: 1.5rem
- No rounded corners

### 7.5 Status Indicators

- ASCII-style brackets: `[ACTIVE]` `[STANDBY]` `[FAULT]`
- Blinking animation for critical states
- Color-coded: green (nominal), amber (warning), red (fault)

## 8. Motion Philosophy

- Minimal, purposeful animation only
- Linear or step() easing (no ease curves)
- Typewriter text reveals
- Blinking cursors and status lights
- Glitch effects for state changes (0.1s duration max)
- Scan line sweeps on page transitions

## 9. Iconography

- Geometric, angular forms only
- Stroke-based, consistent weight
- No organic curves or rounded caps
- Custom SVGs matching grid alignment
- Size: 16px, 24px, or 32px (powers of 2)

## 10. Implementation Guidelines

### 10.1 Font Loading

html
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;800&display=swap" rel="stylesheet">
### 10.2 CSS Custom Properties

css
:root {
  /* Swiss Industrial */
  --bg-primary: #F5F5F0;
  --text-primary: #1A1A1A;
  --accent-red: #E8000D;
  --grid-line: #CCCCCC;

  /* Terminal */
  --bg-terminal: #0A0A0A;
  --phosphor-green: #00FF41;
  --phosphor-dim: #008F11;
  --terminal-cyan: #00D4FF;

  /* Typography */
  --font-display: 'Barlow Condensed', sans-serif;
  --font-mono: 'Space Mono', monospace;
}
### 10.3 Performance Considerations

- Limit animated scanlines to CSS-only (no JS)
- Use `will-change` sparingly for animated elements
- Preload web fonts to prevent FOUT
- Apply noise textures via SVG filters or CSS gradients (not raster images)
- Test degradation effects on low-end devices