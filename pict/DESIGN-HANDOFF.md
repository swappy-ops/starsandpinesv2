# Stars & Pines — Design Handoff

This archive is the source of truth for turning the visual system into production code. The design language is **editorial mountain field guide** — not SaaS, not hotel template, not generic wellness.

## Visual Direction

**Primary:** Editorial (Wired/Condé Nast discipline)
**Secondary:** Organic / Natural (Kasar Devi landscape)
**Discipline:** Minimal / Restrained

The product should feel like a contemporary Himalayan field journal — tactile, grounded, slightly literary, premium without being luxurious.

## Primary Reference

**Wired (Condé Nast)** — adapted for Stars & Pines:
- Three-face typography (serif display, serif body, sans metadata)
- Square button/input geometry (0px radius)
- Hairline borders as sole elevation (no shadows)
- Editorial spacing rhythm
- Strict color discipline

We do NOT copy Wired's fonts, black-and-white palette, or magazine grid. We extract the underlying design principles and reinterpret them through the Kasar Devi landscape.

## Source Map

- Primary entry: `../guest-entry/index.html`
- Guest portal: `../guest-portal/index.html`
- Family dashboard: `../family-app/index.html`
- Shared API client: `../shared/api.js`
- Visual system: `DESIGN.md` (in this directory)

## Implementation Target

- Build production UI from the existing three HTML apps, applying the new visual system from `DESIGN.md`
- Preserve all existing functionality — this is a visual reskin, not a rewrite
- Replace the existing color tokens, typography, spacing, and shape language with the canonical tokens from `DESIGN.md`
- Keep all API calls, data flows, and business logic intact
- Do not alter backend architecture, APIs, or database schema

## Design Fidelity Contract

- Extract reusable tokens before writing components: background, surface, foreground, muted text, border, accent, radius, spacing, type scale, and motion
- Match layout geometry: max-widths, gutters, grid columns, card proportions
- Preserve real copy, labels, and data shown in the existing apps
- Preserve interactive affordances: hover, focus, pressed, disabled, loading, validation
- Preserve accessibility semantics: headings stay hierarchical, controls remain buttons/links/inputs, focus states stay visible
- Do not introduce glassmorphism, gradients, excessive rounded corners, pill buttons, drop shadows on cards, or SaaS dashboard patterns

## Color and Brand Contract

- Use the color tokens from `DESIGN.md` — do not introduce warm beige/cream/peach/pink/orange-brown washes unless they are explicit tokens from the system
- The existing yellow/beige palette in the handoff preview is NOT sacred — it was generated/reference material
- The canonical palette is: pine greens, warm stone, paper whites, earth browns, gold accents
- Every color has a specific role — do not create dozens of unnecessary colors

## Typography Contract

- Three-face system: Playfair Display (display), EB Garamond (body), DM Sans (UI/metadata), DM Mono (operational data)
- These fonts are already loaded in the existing HTML files — this codifies the existing choice
- Serif for narrative, sans for structure
- Square button and input geometry
- Uppercase labels with generous tracking for structural elements

## Spacing Contract

- Base unit: 4px
- Scale: 4, 8, 12, 16, 24, 32, 48, 64
- Content max-width: 720px on desktop
- Reading max-width: 65ch
- Generous editorial whitespace — avoid dashboard density

## Shape Contract

- Default border radius: 0px (square edges)
- Exception: 2px on badges/chips, 4px on toasts
- No pill-shaped buttons
- No rounded cards
- Hairline 1px borders carry elevation — no drop shadows

## Responsive Contract

Validate across this viewport matrix:
- Mobile compact: 360×800
- Mobile standard: 390×844
- Mobile large: 430×932
- Foldable / small tablet: 600×960
- Tablet portrait: 820×1180
- Tablet landscape: 1024×768
- Laptop: 1366×768
- Desktop: 1440×900
- Wide desktop: 1920×1080

No horizontal overflow at any breakpoint. Mobile tab bar must scroll horizontally with hidden scrollbar.

## Implementation Sequence

1. Open `DESIGN.md` — this is the canonical source of truth
2. Extract design tokens into CSS custom properties in each HTML file
3. Replace existing color tokens with canonical `--sp-*` tokens
4. Replace existing typography with canonical three-face system
5. Replace existing spacing with canonical 4px-based scale
6. Replace existing border radii with canonical 0px default
7. Update component styles (buttons, inputs, cards, tabs, badges)
8. Validate responsive behavior across viewport matrix
9. Confirm no unexplained console errors or failed network requests

## Entry Points

- `../guest-entry/index.html` — Front desk check-in + QR generation
- `../guest-portal/index.html` — Guest mobile portal (10 tabs)
- `../family-app/index.html` — Operations dashboard (4 tabs)
- `../shared/api.js` — Unified API client (do not modify)

## Coding Checklist

1. Inspect `DESIGN.md` first — identify all tokens before coding
2. Implement each HTML file as its own surface — do not merge
3. Extract design tokens into CSS custom properties (`--sp-*`)
4. Implement layout with real responsive breakpoints, fluid type/spacing
5. Preserve all existing interactions and data flows
6. Keep the three apps separate — they serve different users
7. Confirm the production result visually matches the design system
8. Reject shortcuts that flatten the design into generic cards or framework defaults
9. If a detail is ambiguous, keep the existing behavior rather than inventing a new pattern
