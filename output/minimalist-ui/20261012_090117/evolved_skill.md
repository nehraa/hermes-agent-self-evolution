---
name: minimalist-ui
description: Clean editorial-style interfaces. Warm monochrome palette, typographic contrast, flat bento grids, muted pastels. No gradients, no heavy shadows.
---

# Minimalist UI Directive

Generate refined, editorial-style web interfaces with warm monochrome palettes, deliberate typographic hierarchy, generous whitespace, and flat component architecture. Reject generic SaaS patterns in favor of document-inspired design.

---

## Typography

### Font Stack

**Sans-Serif** (body text, UI, buttons):
css
font-family: 'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', system-ui, sans-serif;
**Serif** (headlines, quotes, editorial moments):
css
font-family: 'Newsreader', 'Playfair Display', 'Instrument Serif', 'Lyon Text', Georgia, serif;
### Typography Rules

- Establish **extreme typographic contrast** between headings and body — large headlines (32px+), restrained body text (16-18px)
- Apply tight tracking on editorial serifs: `letter-spacing: -0.02em`
- Body text: 16-18px with `line-height: 1.5-1.6`
- Avoid: Inter, Roboto, Open Sans, Arial

---

## Color Palette

### Warm Monochrome Foundation

| Token | Hex | Usage |
|-------|-----|-------|
| Background | `#FAFAF8` | Page background, warm white |
| Surface | `#F5F5F2` | Cards, elevated elements |
| Border | `#E8E8E4` | Dividers, card outlines |
| Text Primary | `#1A1A18` | Headlines, primary content |
| Text Secondary | `#6B6B66` | Body text, descriptions |
| Text Tertiary | `#9C9C96` | Captions, metadata |

### Muted Pastel Accents

Use **sparingly** for interactive states, hover feedback, or category labels:

- **Sage**: `#B8C4B8`
- **Blush**: `#D4C4C4`
- **Dust**: `#C4C4B8`

---

## Layout System

### Bento Grid

- Use CSS Grid for **asymmetric, magazine-style** compositions
- Deliberately mix card sizes: `1x1`, `2x1`, `1x2`, `2x2`
- Gutter spacing: `24px` to `32px`

### Whitespace

- Container padding: `48px` minimum on edges
- Vertical rhythm: multiples of `8px`
- Section separation: `80px` to `120px`

### Borders

- Use `1px solid` borders instead of shadows for card definition
- Border radius: `4px` to `8px` maximum
- **Never** use `rounded-full` on containers or primary buttons

---

## Components

### Cards

- Flat backgrounds (`#F5F5F2`) with `1px` borders (`#E8E8E4`)
- No drop shadows — or shadows with `opacity < 0.05`
- Internal padding: `24px`
- Border radius: `6px`

### Buttons

**Primary**:
- Background: `#1A1A18`
- Text: `#FAFAF8`
- Height: `40px` to `48px`

**Secondary**:
- Background: transparent
- Border: `1px solid #E8E8E4`
- Text: `#1A1A18`

**Ghost**:
- Background: transparent
- Text: `#6B6B66`
- Hover: text color shifts to `#1A1A18`

All buttons: `border-radius: 4px`, no shadows

### Icons

- Use custom SVG primitives or Phosphor Icons, Lucide, or Heroicons (outline style)
- Stroke weight: `1.5px` to `2px`
- Size: `20px` to `24px` for inline, `32px` for feature icons
- Color inherits from text color (`currentColor`)

---

## Anti-Patterns

**Avoid**:
- Gradient backgrounds or button fills
- Heavy drop shadows (`box-shadow: 0 4px 12px rgba(0,0,0,0.15)`)
- Rounded-full containers or buttons
- Inter, Roboto, Open Sans, or Arial typefaces
- Card shadows exceeding `opacity: 0.05`
- Generic SaaS layouts (centered hero, icon-heavy feature grids)

**Prefer**:
- Document-inspired layouts with clear typographic hierarchy
- Flat, bordered components
- Editorial imagery and pull quotes
- Generous whitespace and breathing room