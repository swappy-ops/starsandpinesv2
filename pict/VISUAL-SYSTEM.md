# Stars & Pines — Visual System

A concise implementation reference for the Stars & Pines visual system. This document distills `DESIGN.md` into actionable CSS tokens and component patterns.

---

## CSS Custom Properties

```css
:root {
  /* ─── Foreground ─── */
  --sp-ink:        #1a1714;
  --sp-ink-soft:   #3a3530;
  --sp-body:       #5a5047;
  --sp-muted:      #8a7e72;
  --sp-faint:      #b0a898;

  /* ─── Background ─── */
  --sp-paper:      #f6f1ea;
  --sp-cream:      #f0ebe3;
  --sp-mist:       #e8e2d8;

  /* ─── Borders ─── */
  --sp-border:     #d4c9b8;
  --sp-border-soft:#e5dcc8;

  /* ─── Accents ─── */
  --sp-pine:       #2d4030;
  --sp-pine-deep:  #1f2f1d;
  --sp-warm:       #c4a55a;

  /* ─── Semantic ─── */
  --sp-alert:      #b05050;
  --sp-green:      #4a8a62;

  /* ─── Dark Surface (Family App optional) ─── */
  --sp-night:      #131a12;
  --sp-forest:     #1f2f1d;
  --sp-bark:       #4a3a26;
  --sp-earth:      #7a6248;

  /* ─── Typography ─── */
  --sp-font-display: 'Playfair Display', Georgia, 'Times New Roman', serif;
  --sp-font-body:    'EB Garamond', Georgia, 'Times New Roman', serif;
  --sp-font-ui:      'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --sp-font-mono:    'DM Mono', 'SF Mono', Monaco, Consolas, monospace;

  /* ─── Type Scale ─── */
  --sp-display-xl:   40px;
  --sp-display-lg:   32px;
  --sp-display-md:   26px;
  --sp-display-sm:   22px;
  --sp-body-lg:      18px;
  --sp-body-md:      16px;
  --sp-body-sm:      14px;
  --sp-label-lg:     14px;
  --sp-label-md:     12px;
  --sp-label-sm:     11px;
  --sp-caption:      12px;
  --sp-mono:         13px;
  --sp-button:       13px;

  /* ─── Spacing ─── */
  --space-xxs: 4px;
  --space-xs:  8px;
  --space-sm:  12px;
  --space-md:  16px;
  --space-lg:  24px;
  --space-xl:  32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  /* ─── Radius ─── */
  --radius-none: 0px;
  --radius-sm:   2px;
  --radius-md:   4px;

  /* ─── Motion ─── */
  --duration-fast: 150ms;
  --duration-mid:  200ms;
  --duration-slow: 300ms;
  --ease-out:      cubic-bezier(0.215, 0.61, 0.355, 1);
  --ease-in-out:   cubic-bezier(0.645, 0.045, 0.355, 1);
}
```

---

## Base Reset

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html {
  font-size: 16px;
  -webkit-text-size-adjust: 100%;
}

body {
  font-family: var(--sp-font-ui);
  font-size: var(--sp-body-md);
  line-height: 1.5;
  color: var(--sp-body);
  background: var(--sp-paper);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3, h4 {
  font-family: var(--sp-font-display);
  font-weight: 400;
  color: var(--sp-ink);
  line-height: 1.2;
}

a {
  color: var(--sp-pine);
  text-decoration: none;
}

a:hover {
  color: var(--sp-pine-deep);
  text-decoration: underline;
}
```

---

## Component Patterns

### Buttons

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--sp-font-ui);
  font-size: var(--sp-button);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  padding: 10px 20px;
  min-height: 36px;
  border: 1px solid transparent;
  border-radius: var(--radius-none);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
}

.btn:focus-visible {
  outline: 2px solid var(--sp-pine);
  outline-offset: 2px;
}

.btn:active {
  transform: translateY(1px);
}

.btn:disabled {
  background: var(--sp-faint);
  color: var(--sp-muted);
  cursor: not-allowed;
}

/* Filled (primary) */
.btn-primary {
  background: var(--sp-pine);
  color: #fff;
}

.btn-primary:hover {
  background: var(--sp-pine-deep);
}

/* Outlined */
.btn-outline {
  background: transparent;
  color: var(--sp-pine);
  border-color: var(--sp-pine);
}

.btn-outline:hover {
  background: var(--sp-cream);
}

/* Ghost */
.btn-ghost {
  background: transparent;
  color: var(--sp-body);
}

.btn-ghost:hover {
  color: var(--sp-ink);
}
```

### Inputs

```css
.input {
  display: block;
  width: 100%;
  height: 40px;
  padding: 0 var(--space-sm);
  font-family: var(--sp-font-ui);
  font-size: 14px;
  color: var(--sp-ink);
  background: var(--sp-cream);
  border: 1px solid var(--sp-border);
  border-radius: var(--radius-none);
  outline: none;
  transition: border-color var(--duration-fast) var(--ease-in-out);
}

.input:focus {
  border-color: var(--sp-pine);
  border-width: 2px;
  padding: 0 calc(var(--space-sm) - 1px);
}

.input::placeholder {
  color: var(--sp-faint);
}

.input:disabled {
  background: var(--sp-mist);
  color: var(--sp-faint);
}

.input-error {
  border-color: var(--sp-alert);
  border-width: 2px;
}
```

### Cards

```css
.card {
  background: var(--sp-paper);
  border: 1px solid var(--sp-border);
  border-radius: var(--radius-none);
  padding: var(--space-md);
}

.card-title {
  font-family: var(--sp-font-display);
  font-size: var(--sp-display-sm);
  color: var(--sp-ink);
  margin-bottom: var(--space-xs);
}

.card-body {
  font-family: var(--sp-font-body);
  font-size: var(--sp-body-md);
  color: var(--sp-body);
  line-height: 1.5;
}

.card-meta {
  font-family: var(--sp-font-ui);
  font-size: var(--sp-label-md);
  color: var(--sp-muted);
  margin-top: var(--space-xs);
}
```

### Tabs

```css
.tab-bar {
  display: flex;
  border-bottom: 1px solid var(--sp-border-soft);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.tab-bar::-webkit-scrollbar {
  display: none;
}

.tab-btn {
  flex: 0 0 auto;
  padding: var(--space-xs) var(--space-sm);
  font-family: var(--sp-font-ui);
  font-size: var(--sp-label-md);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--sp-muted);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: color var(--duration-fast) var(--ease-in-out);
  white-space: nowrap;
  min-height: 44px;
  display: flex;
  align-items: center;
}

.tab-btn.active {
  color: var(--sp-ink);
  border-bottom-color: var(--sp-pine);
}

.tab-btn:hover {
  color: var(--sp-body);
}
```

### Badges

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  font-family: var(--sp-font-ui);
  font-size: var(--sp-label-sm);
  font-weight: 500;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.badge-success {
  background: rgba(74, 138, 98, 0.12);
  color: var(--sp-green);
}

.badge-warning {
  background: rgba(196, 165, 90, 0.12);
  color: var(--sp-warm);
}

.badge-error {
  background: rgba(176, 80, 80, 0.12);
  color: var(--sp-alert);
}

.badge-neutral {
  background: var(--sp-mist);
  color: var(--sp-body);
}
```

### Labels

```css
.label {
  display: block;
  font-family: var(--sp-font-ui);
  font-size: var(--sp-label-lg);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--sp-muted);
  margin-bottom: var(--space-xs);
}

.label-sm {
  font-size: var(--sp-label-md);
  letter-spacing: 0.12em;
}

.label-xs {
  font-size: var(--sp-label-sm);
  letter-spacing: 0.14em;
}
```

### Mono Data

```css
.mono {
  font-family: var(--sp-font-mono);
  font-size: var(--sp-mono);
  letter-spacing: 0.05em;
}

.mono-lg {
  font-size: 18px;
}

.mono-xl {
  font-size: 28px;
  letter-spacing: 0.15em;
}
```

### Toast

```css
.toast {
  position: fixed;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%) translateY(20px);
  background: var(--sp-pine-deep);
  color: var(--sp-paper);
  padding: 10px 20px;
  font-family: var(--sp-font-ui);
  font-size: var(--sp-body-sm);
  border-radius: var(--radius-md);
  border: 1px solid rgba(196, 165, 90, 0.2);
  z-index: 1000;
  opacity: 0;
  pointer-events: none;
  transition: all var(--duration-slow) var(--ease-out);
  white-space: nowrap;
}

.toast.visible {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
```

### Loading Spinner

```css
.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--sp-mist);
  border-top-color: var(--sp-pine);
  border-radius: 50%;
  animation: spin 800ms linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Empty State

```css
.empty-state {
  text-align: center;
  padding: var(--space-2xl) var(--space-md);
  color: var(--sp-muted);
}

.empty-state-icon {
  font-size: 48px;
  opacity: 0.5;
  margin-bottom: var(--space-sm);
}

.empty-state-text {
  font-family: var(--sp-font-ui);
  font-size: var(--sp-body-sm);
}
```

---

## Layout Utilities

```css
.wrap {
  max-width: 720px;
  margin: 0 auto;
  padding: var(--space-lg);
}

.reading {
  max-width: 65ch;
}

.section {
  margin-bottom: var(--space-xl);
}

.section-lg {
  margin-bottom: var(--space-2xl);
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-lg);
}

@media (min-width: 600px) {
  .grid-2 {
    grid-template-columns: 1fr 1fr;
  }
}

.flex-row {
  display: flex;
  gap: var(--space-md);
  align-items: center;
  flex-wrap: wrap;
}

.divider {
  border: none;
  border-top: 1px solid var(--sp-border-soft);
  margin: var(--space-lg) 0;
}

.divider-strong {
  border-top-color: var(--sp-border);
}
```

---

## Responsive Base

```css
/* Mobile */
body {
  padding: var(--space-md);
}

.section {
  margin-bottom: var(--space-lg);
}

/* Tablet */
@media (min-width: 600px) {
  body {
    padding: var(--space-lg);
  }

  .section {
    margin-bottom: var(--space-xl);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  body {
    padding: var(--space-xl);
  }

  .wrap {
    padding: var(--space-xl);
  }

  .section {
    margin-bottom: var(--space-2xl);
  }
}
```

---

## Accessibility

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

:focus-visible {
  outline: 2px solid var(--sp-pine);
  outline-offset: 2px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap" rel="stylesheet">
```

---

*This file is a distilled implementation reference. For the complete design system including philosophy, hospitality-specific patterns, and the implementation contract, see `DESIGN.md`.*
