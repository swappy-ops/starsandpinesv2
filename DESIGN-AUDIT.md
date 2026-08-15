# Stars & Pines V2 Design Audit

**Date:** 2026-08-15
**Scope:** `family-app/`, `guest-entry/`, `guest-portal/`
**Reference:** `pict/DESIGN.md`, `pict/VISUAL-SYSTEM.md`, rendered browser checks at desktop and 390px mobile widths

## Summary

The three surfaces load and preserve the intended editorial/mountain direction: restrained palette, serif display typography, square primary surfaces, and no decorative gradients in the current entry points. The main gaps are interaction accessibility, small operational controls, and visual drift in the guest portal.

## Findings

### High: Guest Entry rail is not semantic navigation

**Location:** `guest-entry/index.html:325-326`

**Issue:** The desktop and mobile navigation is generated with `.screen::before` as a text string. It is visible in the UI but is not a `nav`, link, or button, so keyboard and assistive-technology users cannot navigate it. The browser accessibility tree exposes the rail as plain text.

**Fix:** Replace the pseudo-element with a real `<nav aria-label="Guest entry">` containing links or buttons, and use CSS only for layout and styling.

### High: Focus indicators do not meet the design system

**Locations:** `family-app/index.html:453-463`, `guest-entry/index.html:153-172`, `guest-portal/index.html:35`, `guest-portal/index.html:180`

**Issue:** Inputs explicitly remove the native outline. Focus is then represented by a 1px warm border, or has no dedicated focus rule in the portal. The canonical system requires a clearly visible 2px focus treatment, normally pine.

**Fix:** Add `:focus-visible` styles with a 2px `--sp-pine` outline or border and a 2px offset. Keep the focus treatment visible against both light and dark surfaces.

### High: Guest portal navigation text is too small

**Location:** `guest-portal/index.html:52-53`

**Issue:** Tab labels are `0.5rem` and tab numbers are `0.45rem`, approximately 8px and 7px. Ten tabs are presented in one horizontal navigation, making labels difficult to scan and tap reliably. This is below the design system's 11px minimum metadata scale.

**Fix:** Use at least the `label-sm` size for labels, increase horizontal padding and active-state contrast, and consider grouping the ten destinations into a primary set plus an overflow or secondary menu on narrow screens.

### Medium: Guest portal cards drift from the square, border-led language

**Location:** `guest-portal/index.html:223`

**Issue:** `.menu-item` adds `border-radius: 4px` and a drop shadow. The canonical card treatment is square with a 1px border and no shadow. The mixed `--pms-*` token layer also makes this surface visually less consistent with Family and Guest Entry.

**Fix:** Remove the shadow and use `border-radius: var(--radius-none)` for standard cards. Keep the 4px exception only for toasts or similarly small utility surfaces.

### Medium: Family operational actions are undersized

**Locations:** `family-app/index.html:290-300`, `family-app/index.html:337-349`

**Issue:** General action buttons have no minimum height, while inventory actions use 2px vertical padding and `0.55rem` text. These controls are visually subordinate and create small touch targets on mobile.

**Fix:** Apply the shared 36px minimum button height to `.btn`, and give `.inv-btn` a compact but usable minimum height and visible focus state. Preserve the tighter density on desktop if needed, but relax it below 768px.

### Medium: Family surface is still incomplete as an operations information architecture

**Location:** `family-app/index.html:618-621`; documented in `DESIGN-IMPLEMENTATION-PLAN.md:34-35`

**Issue:** The visible dashboard exposes only Property, Kitchen, Inventory, and Checkout. Housekeeping, guest requests, grievances, staff/operations, and unified alerts are not represented even though the backend supports most of them. This is a product/navigation gap rather than a cosmetic issue.

**Fix:** Add visible destinations only where existing routes and states are wired, or explicitly label the missing areas as unavailable/follow-up. Do not leave backend-backed operational work hidden from staff.

### Low: Missing favicon produces a console error on every surface

**Location:** all three entry points

**Issue:** Browser checks report `GET /favicon.ico 404`. This does not change layout, but it is a persistent runtime quality signal and can be avoided with a small local favicon or an explicit icon link.

**Fix:** Add a local favicon and reference it from each entry point, or return a valid `/favicon.ico` from the server.

## Responsive Check

- Family App: no horizontal overflow observed at 390px after authentication; navigation correctly becomes horizontally scrollable.
- Guest Portal: no horizontal overflow observed at 390px access screen.
- Guest Entry: the 390px media rule collapses the form to one column and the rail/content layout fits the viewport. The rail remains difficult to use because it is decorative text rather than controls.

## Recommended Order

1. Replace Guest Entry's pseudo-element rail with semantic navigation.
2. Restore visible focus states and normalize minimum touch targets.
3. Fix Guest Portal tab scale and card token drift.
4. Decide and implement the missing Family operational destinations.
5. Add the favicon and rerun browser checks at 390px, 768px, and 1440px.
