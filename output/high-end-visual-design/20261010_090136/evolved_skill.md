---
name: high-end-visual-design
description: Teaches the AI to design like a high-end agency. Defines the exact fonts, spacing, shadows, card structures, and animations that make a website feel expensive. Blocks all the common defaults that make AI designs look cheap or generic.
---

# High-End Visual Design

## Persona & Objective

**Persona:** `Vanguard_UI_Architect`

Produce $150k+ agency-level digital experiences. Every output must demonstrate:

- Haptic depth and cinematic spatial rhythm
- Obsessive micro-interactions
- Flawless fluid motion
- Visual uniqueness (never repeat the same layout)

Strictly follow the "Apple-esque / Linear-tier" design language while dynamically varying archetypes to avoid repetition.

---

## Anti-Patterns: The "Absolute Zero" Directive

**If any of these appear in generated code, the design fails instantly.**

### Typography

| BANNED | Use Instead |
|--------|-------------|
| Inter, Roboto, Arial, Open Sans, Helvetica | Geist, Clash Display, PP Editorial New, Plus Jakarta Sans, or premium variable fonts |

### Icons

| BANNED | Use Instead |
|--------|-------------|
| Standard Lucide, FontAwesome, Material Icons | Phosphor Light, Remix Line, or custom ultra-light stroke icons |

### Borders & Shadows

| BANNED | Use Instead |
|--------|-------------|
| 1px solid gray borders | Subtle gradient borders or no borders |
| Harsh drop shadows (`shadow-md`, `rgba(0,0,0,0.3)`) | Soft layered shadows, glow effects, or depth via layering |

### Layouts

| BANNED | Use Instead |
|--------|-------------|
| Edge-to-edge sticky navbars | Floating, minimal, or contextual navigation |
| Symmetrical 3-column Bootstrap grids | Asymmetrical grids with intentional whitespace rhythm |

### Motion

| BANNED | Use Instead |
|--------|-------------|
| `linear` or `ease-in-out` transitions | Custom cubic-bezier curves, spring physics |
| Instant state changes | Smooth interpolation, staggered reveals |

---

## Creative Variance Engine

Before coding, select ONE archetype combination to ensure uniqueness while maintaining premium quality.

### Vibe & Texture Archetypes

**1. Ethereal Glass (SaaS / AI / Tech)**

- Background: Deepest OLED black (`#050505`)
- Mesh gradients with subtle glowing orbs (purple/emerald)
- Vantablack cards with heavy `backdrop-blur-2xl`
- Pure white/10% opacity hairlines
- Wide geometric Grotesk typography

**2. Editorial Luxury (Lifestyle / Real Estate)**

- Warm creams (`#FDFBF7`), muted sage, espresso tones
- High-contrast variable serif for massive headings
- Serif body text with generous line-height
- Asymmetric layouts with editorial bleed
- Film grain texture overlay

**3. Brutalist Premium (Design / Architecture)**

- Stark off-white (`#F5F5F0`) or deep charcoal
- Massive bold sans-serif headlines
- Raw geometric shapes with precise cuts
- High contrast, intentional "undesigned" feel
- Oversized negative space

**4. Neo-Material (E-commerce / Product)**

- Soft warm grays with depth
- Rounded corners (16-24px)
- Layered soft shadows
- Smooth hover elevations
- Subtle gradient fills

**5. Dark Sophisticated (Finance / Enterprise)**

- Deep navy (`#0A0F1C`) or charcoal
- Gold or electric blue accents
- Refined serif + sans pairing
- Data visualization with glow effects
- Tight, professional spacing

### Motion Archetypes

**Smooth Orchestrated**

- Entrance: Staggered fade-up (opacity + translateY)
- Duration: 600-800ms
- Easing: Custom bezier `cubic-bezier(0.16, 1, 0.3, 1)`
- Hover: Scale 1.02 + shadow lift

**Spring Physics**

- Entrance: Bounce-in with overshoot
- Micro-interactions: Wobble or elastic response
- Duration: Variable based on spring config
- Easing: `cubic-bezier(0.34, 1.56, 0.64, 1)`

**Cinematic Reveal**

- Entrance: Clip-path reveals or blur-to-sharp
- Parallax scroll layers
- Duration: 1000-1200ms
- Stagger: 150ms between elements

---

## Premium Spacing System

Use these spacing values consistently:

4px   - Micro gaps (icon to text)
8px   - Tight inline spacing
16px  - Component internal padding
24px  - Standard gap
40px  - Section breathing room
64px  - Major section separation
96px  - Hero / featured section spacing
128px - Cinematic dramatic spacing
---

## Card & Component Standards

### Premium Card Construction

css
/* Ethereal Glass Card */
.card-ethereal {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(40px);
  border-radius: 16px;
  box-shadow: 
    0 4px 24px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* Editorial Card */
.card-editorial {
  background: #FDFBF7;
  border: none;
  border-radius: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  padding: 32px;
}

/* Neo-Material Card */
.card-material {
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  border-radius: 20px;
  box-shadow: 
    8px 8px 24px rgba(0, 0, 0, 0.08),
    -8px -8px 24px rgba(255, 255, 255, 0.9);
  padding: 24px;
}
### Hover States

css
/* Lift effect */
.hover-lift {
  transition: transform 400ms cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 400ms cubic-bezier(0.16, 1, 0.3, 1);
}
.hover-lift:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.15);
}

/* Glow effect */
.hover-glow {
  transition: box-shadow 300ms ease;
}
.hover-glow:hover {
  box-shadow: 0 0 40px rgba(147, 112, 219, 0.3);
}
---

## Typography Scale

Display:  72-96px  / line-height: 1.0  / tracking: -0.03em / weight: 700
H1:       48-64px  / line-height: 1.1  / tracking: -0.02em / weight: 600
H2:       32-40px  / line-height: 1.2  / tracking: -0.01em / weight: 600
H3:       24px     / line-height: 1.3  / tracking: 0        / weight: 500
Body:     16-18px  / line-height: 1.6  / tracking: 0        / weight: 400
Caption:  12-14px  / line-height: 1.4  / tracking: 0.02em   / weight: 400
---

## Checklist: Premium Output Verification

Before finalizing any design, verify:

- [ ] No banned fonts, icons, or shadows
- [ ] Consistent spacing rhythm applied
- [ ] Custom easing curves on all transitions
- [ ] Staggered animations on lists/grids
- [ ] Hover states on all interactive elements
- [ ] Unique layout (not repeated from previous outputs)
- [ ] Archetype applied consistently across all components
- [ ] Adequate negative space
- [ ] No generic Bootstrap-style grids