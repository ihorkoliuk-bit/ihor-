# ZON Design System

Status: working default. If official ZON brand guidelines (logo files, fonts, exact colours) exist, they override this file. Record the source in `verified-facts.md` under "Brand assets".

## Palette

| Token | Hex | Role | Contrast on ivory-50 |
|---|---|---|---|
| emerald-900 | #0B3B2E | Primary: headers, footer, primary buttons, key bands | 11.6:1 |
| emerald-700 | #145C46 | Hover, links, secondary emphasis | 7.35:1 |
| walnut-800 | #4A3226 | Warm dark surfaces, captions over imagery | 10.97:1 |
| walnut-600 | #6B4A36 | Secondary text accents | 7.33:1 |
| brass-300 | #CDAE78 | Accent text/icons on emerald or walnut (5.9:1 / 5.6:1) | n/a |
| brass-500 | #B08D57 | Rules, dividers, icon strokes on light. Decorative only | 2.87:1 (fails text) |
| brass-700 | #8A6A3A | Small accent text and focus rings on light | 4.63:1 |
| ivory-50 | #FAF6EE | Page background | — |
| ivory-100/200 | #F3ECDF / #E9DFCC | Cards, alternating sections | — |
| ink | #1C1A17 | Body text | 16.1:1 |
| muted | #5E574D | Secondary text | 6.61:1 |

Proportion guide: ~70% ivory, ~20% emerald, ~8% walnut/imagery, ~2% brass. Pure white (#FFF) and pure black are not used.

## Typography

- Display: a refined serif (default Cormorant Garamond, weights 500–600) for H1/H2 and pull quotes. Tight leading (1.05–1.12), slight negative tracking at large sizes.
- Body/UI: a neutral grotesque (default Inter, 400/500/600). 16–18 px body, 1.6 leading, 60–75 characters per line.
- Small caps labels: body font, 600, uppercase, `--tracking-caps`, `--text-xs`, brass-700 on light or brass-300 on dark.
- Self-host fonts (`next/font` or local WOFF2), `font-display: swap`, subset to Latin, preload only the display weight used above the fold.
- Hierarchy: one H1 per page; never skip heading levels; numerals tabular in tables and specs.

## Layout and composition

- 12-column grid, max content width 80rem, fluid gutters. Asymmetric splits (7/5, 8/4) feel more architectural than 6/6.
- Define fractional tracks as `minmax(0, 7fr) minmax(0, 5fr)`, not `7fr 5fr`: a bare `fr` track cannot shrink below its longest word, so display-size headings push the page into horizontal scroll at tablet widths. Add `overflow-wrap: break-word` to display headings.
- Section spacing 6–8rem desktop, 3–4rem mobile. Generous whitespace is part of the premium signal.
- Thin brass rules (1px) and drawing-style details (dimension lines, grid marks) can reference architectural drawings; use sparingly.
- Square or 2px corners. No heavy shadows; use tonal surfaces and hairlines instead.
- Mobile first: design the 375px layout first, then enhance. Touch targets ≥ 44×44 px. Sticky mobile CTA bar only if it does not cover content.

## Imagery

- Real ZON photography of completed work is the strongest asset. Prefer wide, natural-light architectural shots, interiors with materials visible, construction/factory process shots for credibility.
- CGIs and AI-generated images must be labelled "Computer-generated visualisation" and never captioned as a completed project.
- Every image: meaningful `alt` (or empty `alt=""` if decorative), explicit width/height or aspect-ratio, AVIF/WebP via `next/image` or `<picture>`, responsive `sizes`, lazy below the fold, `fetchpriority="high"` only for the LCP hero.
- Hero images ≤ 200 KB at 1600px wide where possible.

## Motion

- Purpose: guide attention, show spatial relationships (e.g. module assembly), confirm interaction. Never decoration for its own sake.
- Durations 200–600 ms with `--ease-arch`. Reveal on scroll: opacity + translateY ≤ 24px, once only.
- Animate only `transform` and `opacity`. No scroll-jacking, no parallax on mobile, no autoplay carousels, no infinite loops near text.
- `prefers-reduced-motion: reduce` removes all non-essential motion (tokens set durations to 0).
- Prefer CSS and the View Transitions API; reach for a JS library (e.g. Motion) only when needed, and lazy-load it.

## Interactive home demonstrations

Typical patterns: floor-plan explorer (hotspots per room), module configurator (choose layout/finish), 360° interior tour, 3D model viewer, before/after slider, build-sequence timeline.

Rules:
1. Progressive enhancement: render a static poster image + text description first; load the interactive layer on user intent or when in viewport (`IntersectionObserver`, dynamic import).
2. 3D: `<model-viewer>` or three.js/react-three-fiber, compressed glTF/GLB (Draco/Meshopt), budget ≤ 5 MB total, no loading on Save-Data or slow connections without consent.
3. Fully keyboard operable, visible focus, ARIA labels on hotspots, text alternative listing the same information.
4. Any dimensions, areas, specifications or prices shown in a demo must come from `verified-facts.md`; otherwise use `[[VERIFY]]`.
5. Label demos of designs that are not yet built as "Illustrative design".

## Components (patterns)

- Header: logo left, 4–6 nav items, primary CTA button right (emerald). Collapses to an accessible disclosure menu on mobile.
- Hero: H1 (benefit), one-line proof, primary + secondary CTA, real photo.
- Proof band: verified figures only, each with a footnote/source link.
- Project card: image, location, type, year, short outcome (verified), link to case study.
- Process steps: numbered, 3–6 steps, each with what the client does and what ZON does.
- Enquiry form: as few fields as possible (name, email, phone optional, postcode, project type, message), inline validation, clear privacy notice linking to the privacy policy, honeypot or privacy-friendly anti-spam. Do not wire it to KeyCRM or any live system without approval.
- Footer: emerald-900, company legal name, registered number and address (from facts file), contact, policies, accreditations (verified only).
