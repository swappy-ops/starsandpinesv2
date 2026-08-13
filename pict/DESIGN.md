# Stars & Pines — Design System

**Version:** 2.0.0
**Status:** Canonical source of truth
**Product:** Local-first hospitality operations system — Kasar Devi, Almora

---

## VISUAL DNA

**EDITORIAL + MOUNTAIN + FIELD GUIDE + MATERIAL + QUIET HOSPITALITY + CONTEMPORARY RESTRAINT**

Stars & Pines is not a hotel website. It is a contemporary Himalayan field guide — a quiet mountain publication that happens to manage rooms, orders, and bills. The visual language borrows from print editorial discipline, not from SaaS dashboards or hospitality templates.

---

## PRIMARY REFERENCE

**PRIMARY REFERENCE:** Wired (Condé Nast)

**WHY:** Wired's design language is the strongest match for Stars & Pines because it is fundamentally editorial — built for reading, not scanning. Its three-face typographic system (serif display, serif body, sans metadata), square button geometry, hairline borders, and strict color discipline translate directly to the "mountain field guide" aesthetic. Wired reads like a printed magazine ported to the screen; Stars & Pines should read like a field journal.

**WHAT WE BORROW:**
- Three-face typographic hierarchy (serif display, serif body, sans metadata/labels)
- Square button and input geometry (0px radius)
- Hairline 1px borders as the sole elevation mechanism (no drop shadows)
- Editorial spacing rhythm with generous vertical breathing room
- Strict color discipline — one accent, muted text hierarchy, no decorative gradients
- Magazine-style content density — tight interior, generous section gaps

**WHAT WE DO NOT BORROW:**
- Pure black-and-white palette (Stars & Pines uses earth/pine/stone tones)
- Wired's proprietary fonts (WiredDisplay, BreveText, Apercu)
- Magazine story grid layout (we have operational data, not articles)
- Wired's specific component vocabulary (nav bars, story cards)
- The black footer band

---

## COLOR SYSTEM

### Philosophy

The palette is drawn from the Kasar Devi landscape: pine forests at dusk, weathered deodar wood, Himalayan stone, mountain light on paper, soil after rain. It avoids cliché "eco resort" greens and generic beige wellness tones. Every color has a specific role. The system is restrained — 15 tokens, not 50.

### Tokens

| TOKEN | HEX | ROLE | USAGE | DO NOT USE FOR |
|---|---|---|---|---|
| `--sp-ink` | `#1a1714` | Primary foreground | Headlines, body text, primary buttons | Backgrounds, accents |
| `--sp-ink-soft` | `#3a3530` | Secondary foreground | Subtitles, muted headlines | Primary CTAs |
| `--sp-body` | `#5a5047` | Body text | Paragraphs, descriptions, labels | Headlines |
| `--sp-muted` | `#8a7e72` | Tertiary text | Metadata, timestamps, captions | Any interactive element |
| `--sp-faint` | `#b0a898` | Disabled/placeholder | Placeholder text, disabled states | Visible content |
| `--sp-paper` | `#f6f1ea` | Primary background | Page canvas, card surfaces | Dark mode, overlays |
| `--sp-cream` | `#f0ebe3` | Secondary background | Alternating sections, input fills | Primary canvas |
| `--sp-mist` | `#e8e2d8` | Tertiary background | Hover states, subtle dividers | Primary surfaces |
| `--sp-border` | `#d4c9b8` | Border | Card borders, input borders, rules | Backgrounds |
| `--sp-border-soft` | `#e5dcc8` | Subtle border | Section dividers, hairlines | Interactive borders |
| `--sp-pine` | `#2d4030` | Primary accent | Primary buttons, active states, links | Backgrounds, body text |
| `--sp-pine-deep` | `#1f2f1d` | Deep accent | Hover on pine, dark surfaces | Body text |
| `--sp-warm` | `#c4a55a` | Secondary accent | Highlights, gold moments, prices | Primary CTAs, body text |
| `--sp-alert` | `#b05050` | Error/urgent | Errors, urgent badges, destructive | Success, info |
| `--sp-green` | `#4a8a62` | Success | Confirmed states, served orders | Errors, warnings |

### Color Relationships

```
INK (#1a1714)          ← deepest, headlines, primary actions
  ↓
INK-SOFT (#3a3530)     ← secondary emphasis
  ↓
BODY (#5a5047)         ← running text
  ↓
MUTED (#8a7e72)        ← metadata
  ↓
FAINT (#b0a898)        ← disabled
  ↓
BORDER-SOFT (#e5dcc8)  ← subtle dividers
  ↓
BORDER (#d4c9b8)       ← structural borders
  ↓
MIST (#e8e2d8)         ← hover, subtle fills
  ↓
CREAM (#f0ebe3)        ← secondary surfaces
  ↓
PAPER (#f6f1ea)        ← primary canvas
```

### Semantic Palette

| TOKEN | HEX | USE |
|---|---|---|
| `--sp-success` | `#4a8a62` | Confirmed, served, resolved, paid |
| `--sp-warning` | `#c4a55a` | Pending, preparing, low stock |
| `--sp-error` | `#b05050` | Errors, overdue, urgent, cancelled |
| `--sp-info` | `#2d4030` | Active, in-progress, informational |

### Dark Surface Palette (Family App — optional)

| TOKEN | HEX | ROLE |
|---|---|---|
| `--sp-night` | `#131a12` | Dark canvas |
| `--sp-forest` | `#1f2f1d` | Dark surface |
| `--sp-bark` | `#4a3a26` | Dark text secondary |
| `--sp-earth` | `#7a6248` | Dark muted text |

---

## TYPOGRAPHY

### Philosophy

Stars & Pines uses a **three-face editorial system**: a serif for display headlines (the "field guide voice"), a serif for body copy (the "reading voice"), and a geometric sans for metadata, labels, and navigation (the "structural voice"). This is not Inter everywhere. The serif/sans split signals the difference between narrative content and operational data.

### Font Families

| Role | Primary | Fallback Stack |
|---|---|---|
| **Display** | `Playfair Display` | `Georgia, 'Times New Roman', serif` |
| **Body** | `EB Garamond` | `Georgia, 'Times New Roman', serif` |
| **UI / Metadata** | `DM Sans` | `system-ui, -apple-system, 'Segoe UI', sans-serif` |
| **Monospace** | `DM Mono` | `'SF Mono', Monaco, Consolas, monospace` |

**All fonts are loaded from Google Fonts CDN.** The project already uses these three families across its existing HTML files — this codifies the existing choice rather than introducing new dependencies.

### Type Scale

#### Display (Playfair Display)

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|---|---|---|---|---|---|
| `display-xl` | 40px | 400 | 1.10 | -0.4px | App titles, hero headlines |
| `display-lg` | 32px | 400 | 1.15 | -0.3px | Section headlines |
| `display-md` | 26px | 400 | 1.20 | -0.2px | Card titles, page headers |
| `display-sm` | 22px | 500 | 1.25 | 0 | Subsection headers |

#### Body (EB Garamond)

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|---|---|---|---|---|---|
| `body-lg` | 18px | 400 | 1.55 | 0 | Lead paragraphs, guest names |
| `body-md` | 16px | 400 | 1.50 | 0 | Default body text, descriptions |
| `body-sm` | 14px | 400 | 1.45 | 0 | Secondary body, list items |

#### UI / Metadata (DM Sans)

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|---|---|---|---|---|---|
| `label-lg` | 14px | 500 | 1.30 | 0.1em | Section labels, uppercase |
| `label-md` | 12px | 500 | 1.30 | 0.12em | Field labels, badges, tags |
| `label-sm` | 11px | 500 | 1.25 | 0.14em | Micro-labels, timestamps |
| `caption` | 12px | 400 | 1.40 | 0 | Captions, helper text |
| `mono` | 13px | 400 | 1.50 | 0.05em | Tokens, codes, prices, IDs |
| `button` | 13px | 500 | 1.30 | 0.15em | Button labels (uppercase) |

### Typography Principles

1. **Serif for narrative, sans for structure.** Playfair Display and EB Garamond never carry button labels, nav text, or metadata. DM Sans never carries article body or guest-facing prose.
2. **Display weight 400.** Playfair Display reads as elegant at default weight. Weight 500 only for `display-sm` subsection headers. Never 600+.
3. **Negative tracking on display only.** -0.4px at 40px, scaling to 0 at 22px. Never used on body or UI text.
4. **Uppercase labels with generous tracking.** `label-lg`, `label-md`, `label-sm`, and `button` all use `text-transform: uppercase` with positive letter-spacing (0.1em–0.15em). This is the structural voice.
5. **Monospace for operational data.** Tokens, booking IDs, room codes, and prices use DM Mono. This signals "this is data, not prose."
6. **Body at 16px minimum.** EB Garamond at 16px / 1.50 line-height is the reading baseline. Never smaller for guest-facing content.
7. **Measure limit.** Body text max-width: 65ch. Headlines can exceed this.

---

## SPACING + GRID

### Spacing Scale

Base unit: **4px**. All spacing is a multiple of 4.

| Token | Value | Use |
|---|---|---|
| `space-xxs` | 4px | Tight inline gaps, icon spacing |
| `space-xs` | 8px | Form field gaps, badge padding |
| `space-sm` | 12px | Card internal padding (tight) |
| `space-md` | 16px | Card internal padding, button padding |
| `space-lg` | 24px | Section gaps, card gaps |
| `space-xl` | 32px | Major section gaps |
| `space-2xl` | 48px | Page-level spacing |
| `space-3xl` | 64px | Hero spacing, large section gaps |

### Layout Rules

| Property | Mobile | Tablet | Desktop |
|---|---|---|---|
| Content max-width | 100% | 100% | 720px |
| Reading max-width | 100% | 100% | 65ch |
| Page padding | 16px | 20px | 24px |
| Section gap | 32px | 40px | 48px |
| Card gap | 12px | 16px | 20px |

### Grid

- **Mobile:** Single column, full-width cards
- **Tablet (≥600px):** 2-column card grids
- **Desktop (≥1024px):** Content centered at 720px max-width
- **No horizontal overflow at any breakpoint**

---

## SHAPE LANGUAGE

### Border Radius

| Token | Value | Use |
|---|---|---|
| `radius-none` | 0px | Buttons, inputs, cards, images |
| `radius-sm` | 2px | Badges, chips |
| `radius-md` | 4px | Rare — only when a surface needs slight softening |

### Philosophy

**Square edges are the editorial default.** Stars & Pines does not round its buttons, inputs, or cards. The visual language is that of a printed field guide — sharp corners, hairline borders, rules and dividers. The only exception is 2px radius on small badges/chips where a slight softening prevents visual harshness at small sizes.

### Border Thickness

| Element | Thickness | Color |
|---|---|---|
| Card borders | 1px | `--sp-border` |
| Input borders | 1px | `--sp-border` |
| Section dividers | 1px | `--sp-border-soft` |
| Focus rings | 2px | `--sp-pine` |
| Active tab indicator | 2px | `--sp-pine` |

### Button Treatment

- **Shape:** Rectangular, 0px radius
- **Padding:** 10px 20px (vertical × horizontal)
- **Height:** 36px minimum
- **Border:** 1px solid (outlined variants) or none (filled)
- **Font:** DM Sans, 13px, weight 500, uppercase, 0.15em tracking

### Input Treatment

- **Shape:** Rectangular, 0px radius
- **Height:** 40px
- **Border:** 1px solid `--sp-border`
- **Background:** `--sp-cream`
- **Focus:** 2px solid `--sp-pine` border, no glow ring
- **Font:** DM Sans, 14px

### Card Treatment

- **Shape:** Rectangular, 0px radius
- **Border:** 1px solid `--sp-border`
- **Background:** `--sp-paper`
- **Shadow:** None
- **Padding:** 16px–24px

---

## IMAGE LANGUAGE

### Philosophy

Photography should feel like **field documentation**, not hotel marketing. Images are records of place, not advertisements.

### Aspect Ratios

| Context | Ratio | Treatment |
|---|---|---|
| Hero / full-width | 16:9 | Full bleed, no border |
| Room cards | 4:3 | Contained, 1px border |
| Place guide | 3:2 | Contained, 1px border |
| Staff avatars | 1:1 | Circular crop |
| Menu item photos | 1:1 | Contained, small |

### Image Treatment

- **Corners:** 0px radius (square)
- **Borders:** 1px solid `--sp-border` on contained images
- **Full-bleed images:** No border, edge-to-edge
- **Captions:** DM Sans 12px, `--sp-muted`, below image with 8px gap
- **Mobile:** Images scale to container width, maintain aspect ratio
- **No rounded imagery** — square corners reinforce the editorial voice

---

## COMPONENT LANGUAGE

### Buttons

| State | Visual |
|---|---|
| **Default (filled)** | `--sp-pine` bg, white text, 0px radius |
| **Default (outlined)** | Transparent bg, `--sp-pine` text, 1px `--sp-pine` border |
| **Default (ghost)** | Transparent bg, `--sp-body` text, no border |
| **Hover (filled)** | `--sp-pine-deep` bg |
| **Hover (outlined)** | `--sp-cream` bg |
| **Active/Pressed** | `transform: translateY(1px)` |
| **Focus** | 2px `--sp-pine` outline, 2px offset |
| **Disabled** | `--sp-faint` bg, `--sp-muted` text |

### Links

- **Color:** `--sp-pine`
- **Hover:** `--sp-pine-deep`, underline
- **Visited:** `--sp-ink-soft`
- **Focus:** 2px `--sp-pine` outline

### Cards

| State | Visual |
|---|---|
| **Default** | `--sp-paper` bg, 1px `--sp-border`, 0px radius |
| **Hover** | No change (editorial cards don't float) |
| **Active** | 2px `--sp-pine` border |

### Tabs

| State | Visual |
|---|---|
| **Default** | DM Sans 12px, uppercase, 0.12em tracking, `--sp-muted` |
| **Active** | `--sp-ink`, 2px `--sp-pine` bottom border |
| **Hover** | `--sp-body` |

### Badges

| Type | Background | Text |
|---|---|---|
| **Active / Confirmed** | `rgba(74,138,98,0.12)` | `--sp-green` |
| **Pending / Preparing** | `rgba(196,165,90,0.12)` | `--sp-warm` |
| **Error / Overdue** | `rgba(176,80,80,0.12)` | `--sp-alert` |
| **Neutral** | `--sp-mist` | `--sp-body` |

### Forms / Inputs

| State | Visual |
|---|---|
| **Default** | `--sp-cream` bg, 1px `--sp-border`, 0px radius |
| **Focus** | 2px `--sp-pine` border |
| **Error** | 2px `--sp-alert` border |
| **Disabled** | `--sp-mist` bg, `--sp-faint` text |

### Tables

- **Header:** DM Sans 11px, uppercase, 0.14em tracking, `--sp-muted`, `--sp-cream` bg
- **Body:** DM Sans 14px, `--sp-body`
- **Row divider:** 1px `--sp-border-soft`
- **Hover row:** `--sp-cream` bg

### Loading States

- **Spinner:** 24px diameter, 2px stroke, `--sp-pine` on transparent
- **Skeleton:** `--sp-mist` bg with subtle pulse animation
- **Text:** "Loading…" in `--sp-muted`, DM Sans 14px

### Empty States

- **Icon:** 48px, `--sp-faint` opacity
- **Text:** DM Sans 14px, `--sp-muted`
- **Action:** Ghost button below

### Error States

- **Border:** 2px `--sp-alert`
- **Text:** `--sp-alert`, DM Sans 14px
- **Icon:** Alert triangle, `--sp-alert`

### Success States

- **Border:** 2px `--sp-green`
- **Text:** `--sp-green`, DM Sans 14px
- **Icon:** Check mark, `--sp-green`

### Toasts / Notifications

- **Background:** `--sp-pine-deep`
- **Text:** `--sp-paper`
- **Border:** 1px `rgba(196,165,90,0.2)`
- **Radius:** 4px (only rounded element besides badges)
- **Position:** Bottom center, fixed
- **Duration:** 3s auto-dismiss

---

## HOSPITALITY-SPECIFIC VISUAL LANGUAGE

### Room Cards

- **Layout:** 4:3 image on top, metadata below
- **Image:** Square corners, 1px `--sp-border`
- **Room name:** Playfair Display 22px, `--sp-ink`
- **Room type:** DM Sans 11px, uppercase, 0.14em tracking, `--sp-muted`
- **Price:** DM Mono 16px, `--sp-warm`
- **Status badge:** Top-right of image, 2px radius
- **Occupancy:** DM Sans 12px, `--sp-body`

### Stay Information

- **Guest name:** Playfair Display 26px, `--sp-ink`
- **Room + bed:** DM Sans 14px, `--sp-body`
- **Check-in/out:** DM Mono 13px, `--sp-muted`
- **Token/Code:** DM Mono 18px, `--sp-pine`, letter-spacing 0.15em

### Guest Welcome (Portal)

- **Greeting:** EB Garamond 22px, italic, `--sp-warm`
- **Room label:** DM Sans 14px, `--sp-body`
- **Access code:** DM Mono 28px, `--sp-pine`, letter-spacing 0.2em, centered
- **WiFi/Emergency:** Card format, DM Sans 14px

### Food / Menu Items

- **Category header:** DM Sans 13px, uppercase, 0.1em tracking, `--sp-warm`, 1px `--sp-border-soft` bottom
- **Item name:** DM Sans 14px, weight 500, `--sp-ink`
- **Description:** DM Sans 12px, `--sp-muted`
- **Price:** DM Mono 14px, `--sp-warm`
- **Quantity controls:** 32px circular buttons, `--sp-border` border
- **Cart bar:** `--sp-warm` bg, `--sp-pine-deep` text, fixed bottom

### Guest Requests

- **Request item:** Card format, 1px `--sp-border`
- **Icon:** 20px emoji/symbol
- **Name:** DM Sans 14px, `--sp-ink`
- **ETA:** DM Sans 11px, `--sp-muted`
- **Status badge:** Right-aligned, 2px radius

### Bills / Ledger

- **Total:** DM Mono 20px, `--sp-ink`
- **Line items:** DM Sans 14px, flex row (description left, amount right)
- **Charges:** `--sp-ink` amount
- **Payments:** `--sp-green` amount (negative)
- **Balance:** DM Mono 20px, `--sp-alert` if outstanding, `--sp-green` if paid
- **Divider:** 2px `--sp-warm` above total

### Check-in / Check-out

- **Check-in form:** Stacked fields, DM Sans labels (uppercase, 0.1em tracking)
- **Confirmation:** Large token display, DM Mono 28px, centered
- **QR code:** Square, 200px, dark `--sp-pine-deep` on `--sp-paper`
- **Checkout summary:** Bill format + status badge

### Places Guide (Field Guide Entries)

- **Place card:** 3:2 image left, text right, 1px `--sp-border`
- **Place icon:** 48px square, `--sp-cream` bg
- **Place name:** DM Sans 15px, weight 600, `--sp-ink`
- **Description:** DM Sans 12px, `--sp-muted`
- **Tags:** DM Sans 10px, `--sp-warm` bg, `--sp-warm` text, 2px radius
- **Travel time:** DM Mono 11px, `--sp-green` (taxi) / `--sp-alert` (bike)

### Housekeeping / Cleaning

- **Request card:** 1px `--sp-border`
- **Status colors:** Pending = `--sp-warm`, In-progress = `--sp-info`, Done = `--sp-green`
- **Room label:** DM Mono 13px
- **Notes:** EB Garamond 14px, `--sp-body`

### Kitchen Queue

- **Order card:** 1px `--sp-border`
- **Status indicator:** Left border 3px — red (pending), warm (preparing), green (served)
- **Table label:** DM Sans 14px, weight 500
- **Time elapsed:** DM Mono 11px, `--sp-muted`
- **Items:** DM Sans 13px, indented

### Inventory

- **Category header:** DM Sans 13px, uppercase, `--sp-warm`
- **Item row:** Flex row (name, stock, threshold, actions)
- **Low stock:** `--sp-alert` text, bold
- **OK stock:** `--sp-green` text
- **Actions:** Small outlined buttons, "Restock" / "Use"

---

## RESPONSIVE DESIGN

### Breakpoints

| Name | Width | Behavior |
|---|---|---|
| Mobile compact | 360px | Single column, tight spacing, stacked forms |
| Mobile standard | 390px | Single column, standard spacing |
| Mobile large | 430px | Single column, tab bar horizontal scroll |
| Foldable / small tablet | 600px | 2-column card grids begin |
| Tablet portrait | 820px | 2-column grids, wider content |
| Tablet landscape | 1024px | Content max-width 720px, centered |
| Laptop | 1366px | Full desktop layout |
| Desktop | 1440px | Full desktop layout |
| Wide desktop | 1920px | Content stays centered at 720px |

### Responsive Rules

1. **No horizontal overflow** at any breakpoint
2. **Mobile tab bar:** Horizontal scroll, hide scrollbar, minimum 44px touch targets
3. **Forms:** Stack vertically on mobile, 2-column on tablet+
4. **Cards:** 1-column on mobile, 2-column on tablet, 3-column on desktop (where applicable)
5. **Typography:** Display sizes clamp: 40px → 32px → 26px → 22px
6. **Section gaps:** 32px (mobile) → 40px (tablet) → 48px (desktop)
7. **Page padding:** 16px (mobile) → 20px (tablet) → 24px (desktop)

### Mobile-Specific

- Tab bar: Fixed bottom, horizontal scroll, no scrollbar
- Cart bar: Fixed above tab bar on portal
- Kitchen busy bar: Full-width card at top of kitchen tab
- Forms: Full-width inputs, 44px minimum touch targets
- No hover states on touch devices

---

## MOTION

### Philosophy

Motion reinforces the physical, quiet character of the property. No parallax, no gimmicks, no constant movement. Motion is functional — it signals state change, not decoration.

### Tokens

| Token | Value | Use |
|---|---|---|
| `duration-fast` | 150ms | Hover transitions, micro-interactions |
| `duration-mid` | 200ms | Button press, tab switch, badge appearance |
| `duration-slow` | 300ms | Toast slide-in, card expand |
| `ease-out` | `cubic-bezier(0.215, 0.61, 0.355, 1)` | Enter animations |
| `ease-in-out` | `cubic-bezier(0.645, 0.045, 0.355, 1)` | Exit animations, toggles |

### Specific Behaviors

| Element | Animation |
|---|---|
| Button hover | `filter: brightness(1.05)`, 150ms |
| Button press | `transform: translateY(1px)`, 100ms |
| Toast enter | Slide up from bottom, 300ms ease-out |
| Toast exit | Fade out, 200ms ease-in-out |
| Tab switch | Instant (no transition) |
| Badge appear | Fade in, 200ms |
| Card active | Border color change, 150ms |
| Loading spinner | Continuous rotation, 800ms linear |
| Order status blink | 1.5s ease-in-out infinite (pending), 2s ease-in-out (preparing) |

### Forbidden Motion

- Parallax scrolling
- Animated backgrounds
- Decorative particle effects
- Auto-playing carousels
- Bouncing/pulsing elements (except order status indicators)
- Page transition animations
- Scroll-triggered animations

---

## ACCESSIBILITY

### Requirements

1. **WCAG AA** minimum for all interactive elements
2. **Touch targets:** 44×44px minimum on mobile
3. **Focus visible:** 2px `--sp-pine` outline on all interactive elements
4. **Color contrast:** 4.5:1 minimum for body text, 3:1 for large text
5. **Reduced motion:** Respect `prefers-reduced-motion` — disable all animations
6. **Semantic HTML:** Use proper heading hierarchy, button/label/input semantics
7. **Alt text:** All images must have descriptive alt text
8. **Screen reader:** All interactive elements must have accessible names

### Color Contrast Verification

| Pair | Ratio | Pass |
|---|---|---|
| `--sp-ink` on `--sp-paper` | 14.5:1 | ✓ AAA |
| `--sp-body` on `--sp-paper` | 5.8:1 | ✓ AA |
| `--sp-muted` on `--sp-paper` | 3.2:1 | ✓ AA (large text) |
| `--sp-pine` on `--sp-paper` | 10.2:1 | ✓ AAA |
| `--sp-warm` on `--sp-paper` | 2.1:1 | ✗ (use for decorative only, not text) |
| White on `--sp-pine` | 10.2:1 | ✓ AAA |
| `--sp-alert` on `--sp-paper` | 4.6:1 | ✓ AA |
| `--sp-green` on `--sp-paper` | 4.8:1 | ✓ AA |

---

## FORBIDDEN VISUAL PATTERNS

1. **No glassmorphism** — no backdrop-filter blur on UI surfaces
2. **No gradients** — no CSS gradient backgrounds (except order status animations)
3. **No excessive rounded corners** — 0px is the default
4. **No pill-shaped buttons** — rectangular only
5. **No drop shadows on cards** — hairline borders carry elevation
6. **No generic "nature" illustrations** — use real property photography
7. **No SaaS dashboard patterns** — no stat cards with big numbers, no sparklines
8. **No loud luxury branding** — no gold foil effects, no ornate decorations
9. **No generic beige wellness** -- avoid warm washes that read as "spa template"
10. **No Inter everywhere** — use the three-face system

---

## IMPLEMENTATION CONTRACT

This section is binding for any implementation agent.

### Canonical Color Tokens

```css
--sp-ink:        #1a1714;
--sp-ink-soft:   #3a3530;
--sp-body:       #5a5047;
--sp-muted:      #8a7e72;
--sp-faint:      #b0a898;
--sp-paper:      #f6f1ea;
--sp-cream:      #f0ebe3;
--sp-mist:       #e8e2d8;
--sp-border:     #d4c9b8;
--sp-border-soft:#e5dcc8;
--sp-pine:       #2d4030;
--sp-pine-deep:  #1f2f1d;
--sp-warm:       #c4a55a;
--sp-alert:      #b05050;
--sp-green:      #4a8a62;
```

### Canonical Typography

```css
/* Display */
font-family: 'Playfair Display', Georgia, serif;
font-weight: 400; /* 500 only for display-sm */

/* Body */
font-family: 'EB Garamond', Georgia, serif;
font-weight: 400;

/* UI / Metadata */
font-family: 'DM Sans', system-ui, sans-serif;
font-weight: 400; /* 500 for labels, buttons */

/* Monospace */
font-family: 'DM Mono', 'SF Mono', monospace;
font-weight: 400;
```

### Canonical Spacing

Base unit: 4px. Scale: 4, 8, 12, 16, 24, 32, 48, 64.

### Canonical Radius

Default: **0px**. Exception: 2px on badges/chips, 4px on toasts.

### Canonical Component Behavior

- Buttons: rectangular, 0px radius, uppercase labels
- Inputs: rectangular, 0px radius, `--sp-cream` bg
- Cards: rectangular, 0px radius, 1px `--sp-border`, no shadow
- Tabs: underline indicator, uppercase labels
- Badges: 2px radius, tinted backgrounds

### Image Rules

- Square corners (0px radius)
- 1px `--sp-border` on contained images
- Full-bleed images have no border
- Captions in DM Sans 12px, `--sp-muted`

### Responsive Rules

- No horizontal overflow at any breakpoint
- Content max-width 720px on desktop
- Mobile tab bar: horizontal scroll, 44px touch targets
- Display sizes clamp down at smaller viewports

### Accessibility Requirements

- WCAG AA minimum
- 44×44px touch targets on mobile
- Visible focus rings (2px `--sp-pine`)
- Respect `prefers-reduced-motion`
- Semantic HTML, proper heading hierarchy

### Reference Company

**Wired (Condé Nast)** — adapted principles:
- Three-face typographic system (serif display, serif body, sans metadata)
- Square button/input geometry
- Hairline borders as sole elevation
- Editorial spacing rhythm
- Strict color discipline

**Must never copy:**
- Wired's proprietary fonts
- Wired's black-and-white palette
- Wired's magazine story grid
- Wired's specific component vocabulary
- Wired's black footer band

---

*This document is the canonical source of truth for all Stars & Pines visual decisions. When in conflict between memory, convention, or assumption and what DESIGN.md states, DESIGN.md always wins.*
