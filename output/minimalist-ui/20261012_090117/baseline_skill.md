---
name: minimalist-ui
description: Clean editorial-style interfaces. Warm monochrome palette, typographic contrast, flat bento grids, muted pastels. No gradients, no heavy shadows.
---

# Minimalist UI Directive

## Purpose

Generate refined, editorial-style web interfaces with warm monochrome palettes, deliberate typographic hierarchy, generous whitespace, and flat component architecture. Reject generic SaaS patterns in favor of document-inspired design.

---

## Typography

### Sans-Serif (Body, UI, Buttons)
Use geometric or system-native fonts with character:

css
font-family: 'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', system-ui, sans-serif;
### Serif (Headlines, Quotes, Editorial Moments)
Use elegant editorial typefaces:

css
font-family: 'Newsreader', 'Playfair Display', 'Instrument Serif', 'Lyon Text', Georgia, serif;
### Rules
- Establish extreme typographic contrast between headings and body text
- Use tight tracking on editorial serifs: `letter-spacing: -0.02em`
- Body text should remain readable at 16-18px with 1.5-1.6 line height
- Avoid Inter, Roboto, Open Sans, and Arial

---

## Color Palette

### Warm Monochrome Foundation
- **Background**: `#FAFAF8` (warm white)
- **Surface**: `#F5F5F2` (light warm gray)
- **Border**: `#E8E8E4` (subtle warm gray)
- **Text Primary**: `#1A1A18` (near-black)
- **Text Secondary**: `#6B6B66` (warm medium gray)
- **Text Tertiary**: `#9C9C96` (muted gray)

### Muted Pastel Accents
Use sparingly for interactive states or emphasis:
- Sage: `#B8C4B8`
- Blush: `#D4C4C4`
- Dust: `#C4C4B8`

---

## Layout System

### Bento Grid
- Use CSS Grid with asymmetric, magazine-style compositions
- Mix card sizes deliberately (1x1, 2x1, 1x2, 2x2)
- Maintain consistent gutters: `24px` to `32px`

### Whitespace
- Apply generous padding: `48px` minimum on container edges
- Use vertical rhythm with multiples of `8px`
- Create breathing room between sections: `80px` to `120px`

### Borders
- Use `1px` solid borders instead of shadows for card definition
- Border radius: `4px` to `8px` maximum (never `rounded-full` on containers or primary buttons)

---

## Components

### Cards
- Flat backgrounds with subtle borders
- No drop shadows, or shadows with `opacity < 0.05`
- Internal padding: `24px`

### Buttons
- Primary: Solid dark background, light text
- Secondary: Bordered, transparent background
- Border radius: `4px`
- Height: `40px` to `48px`

### Icons
- Use custom SVG primitives or icon library alternatives to Lucide/Feather/Heroicons
- Stroke weight: `1.5px` or `2px`
- Size: `20px` to `24px`

### Navigation
- Simple text links or minimal icon+text combinations
- No heavy glassmorphism effects
- Sticky headers allowed with subtle `backdrop-filter: blur(8px)`

---

## Prohibited Elements

| Banned | Reason |
|--------|--------|
| Gradients on large areas | Unsuitable for editorial aesthetic |
| Neon colors | Contradicts warm monochrome palette |
| Heavy shadows (`shadow-md`+) | Violates flat architecture |
| Pill-shaped containers | Too casual for this style |
| Emojis | Use SVG icons instead |
| Generic placeholders ("Lorem Ipsum", "John Doe") | Use realistic, contextual content |
| AI clichés ("Elevate", "Seamless", "Next-Gen") | Use plain, specific language |

---

## CSS Reset Reference

css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'SF Pro Display', system-ui, sans-serif;
  background: #FAFAF8;
  color: #1A1A18;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

::selection {
  background: #1A1A18;
  color: #FAFAF8;
}