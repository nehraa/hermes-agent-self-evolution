---
name: design-taste-frontend-v1
description: The original v1 taste-skill, preserved for projects depending on its exact behavior. The current default is `design-taste-frontend` (v2 experimental), which is a substantial rewrite. Use this v1 install name only if you need exact backward compatibility.
---

# High-Agency Frontend Skill (v1)

## 1. Active Baseline Configuration

| Parameter | Value | Range |
|-----------|-------|-------|
| `DESIGN_VARIANCE` | 8 | 1 (Perfect Symmetry) → 10 (Artsy Chaos) |
| `MOTION_INTENSITY` | 6 | 1 (Static) → 10 (Cinematic) |
| `VISUAL_DENSITY` | 4 | 1 (Art Gallery) → 10 (Data Cockpit) |

**Usage:** These values are your global defaults. They must be used to drive all generation logic in Sections 3–7. Do not prompt the user to edit this configuration. However, always respect explicit user overrides in their prompts and adapt dynamically.

---

## 2. Architecture & Conventions

### 2.1 Dependency Verification (Mandatory)

Before importing ANY third-party library (`framer-motion`, `lucide-react`, `zustand`, etc.), you MUST:

1. Check `package.json` for an existing entry
2. If the package is missing, output the exact installation command (e.g., `npm install package-name`)
3. Include the install command BEFORE providing the implementation code
4. Never assume a library exists in the project

### 2.2 Framework Defaults

**Stack:** React or Next.js (default to Server Components)

**Server Component Safety:**
- Global state only works in Client Components
- In Next.js, wrap state providers in a dedicated `"use client"` component at the root

**Interactivity Isolation:**
- If motion or advanced UI patterns (Section 4 or 7) are active, extract the interactive component as a leaf Client Component
- Place `'use client'` at the very top of the file
- Server Components must render only static layouts

### 2.3 State Management

| Scope | Solution |
|-------|----------|
| Isolated UI state | `useState` / `useReducer` |
| Cross-component state | Context API |
| Complex global state | Zustand (only if justified) |

Avoid prop drilling. Do not introduce global state for trivial local UI state.

### 2.4 Styling Policy

**Primary:** Tailwind CSS (v3 or v4)

**Version Lock (Critical):**
- Always check `package.json` to determine the installed version
- Do not use Tailwind v4 syntax in v3 projects
- For v4 projects, do NOT use the `tailwindcss` PostCSS plugin
- Use `@tailwindcss/postcss` or the Vite plugin instead

**Fallback:** CSS Modules or inline styles only if Tailwind cannot achieve the desired effect.

### 2.5 Anti-Emoji Policy (Critical)

NEVER use emojis in:
- Code or JSX
- Text content or copy
- Alt text or accessibility labels
- Comments or variable names

Replace emojis with inline SVG icons or icon components (e.g., `lucide-react`).

---

## 3. Generation Guidelines

When generating UI components, apply the baseline configuration values:

- **DESIGN_VARIANCE 8:** Expect asymmetric layouts, unexpected visual rhythms, bold composition choices
- **MOTION_INTENSITY 6:** Moderate animation with personality—transitions feel intentional, not excessive
- **VISUAL_DENSITY 4:** Breathing room between elements, clean hierarchy, gallery-like spacing

Adapt these values based on user requests. When they specify "minimal," "maximalist," "playful," or "corporate," map their intent to adjustments in these three parameters and apply them consistently across the generation.

---

## 4. Motion & Animation

When motion is active:
- Use `framer-motion` for React/Next.js projects
- Respect `MOTION_INTENSITY` setting (6 = purposeful, non-intrusive)
- Extract animated components as isolated Client Components
- Prefer CSS animations for simple transitions, reserve JS animation libraries for complex choreography

---

## 5. Accessibility Baseline

All generated components must:
- Include proper `aria-*` attributes where applicable
- Support keyboard navigation
- Have sufficient color contrast (WCAG AA minimum)
- Use semantic HTML elements

---

## 6. Code Quality Standards

- Use TypeScript by default (strict mode)
- Export components with clear, descriptive names
- Co-locate styles with components when using CSS Modules
- No commented-out code in final output
- Prefer composition over prop drilling

---

## 7. Responsive Design

- Mobile-first approach
- Use Tailwind's responsive prefixes (`sm:`, `md:`, `lg:`, `xl:`)
- Test breakpoints align with common device widths
- Respect `VISUAL_DENSITY` setting—dense layouts on mobile require careful hierarchy