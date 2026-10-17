#!/usr/bin/env bash
# Creates ~/.claude/skills/zon-website-master (skips if it already exists). No Node needed.
set -euo pipefail
D="$HOME/.claude/skills/zon-website-master"
[ -e "$D" ] && { echo "Already exists: $D (left unchanged)"; exit 0; }
mkdir -p "$D/references" "$D/assets"
cat > "$D/SKILL.md" <<'ZON_EOF'
---
name: zon-website-master
description: Build or redesign premium websites, landing pages and web components for ZON, the UK architecture, modular housing, construction and energy business. Use whenever the task involves ZON web pages, ZON branding, property-development or modular-home marketing sites, interactive home or floor-plan demonstrations, or copy for ZON calls to action, even if the user just says "the website" or "a page for ZON".
---

# ZON Website Master

You are building for ZON: a British architecture, modular housing, construction and energy business. The site has to feel like a well-made building: calm, solid, precise, warm materials, nothing shouting. Every page has one job (usually an enquiry or consultation booking) and everything on it serves that job.

## Non-negotiables

1. **No invented facts.** Never write a project, client, award, price, saving, energy figure, build time, warranty, guarantee, certification, location or testimonial that is not in `references/verified-facts.md` with a source. If a page needs one that is missing, insert a visible placeholder `[[VERIFY: what is needed]]` and list it in your final report. Read `references/content-and-claims.md` before writing any copy.
2. **Do not touch live ZON properties.** Do not deploy, publish, change DNS or hosting, or edit any existing ZON website, KeyCRM, or the sales pipeline. Build locally or on a branch and hand over for approval.
3. **Accessible and fast by default.** WCAG 2.2 AA and the performance budgets in `references/qa-checklist.md` are acceptance criteria, not polish.
4. **Brand tokens only.** Use the palette and type scale in `references/design-system.md` (`assets/tokens.css`). Don't introduce new colours or fonts without asking.

## Workflow

1. **Brief.** Establish the page goal, audience (homebuyer, landowner, developer, housing association, commercial client), the single primary CTA, and which verified facts are available. Ask if any is unclear rather than guessing.
2. **Content first.** Draft the page structure and copy using the patterns in `references/content-and-claims.md`. Mark every factual claim against the facts file.
3. **Design.** Apply `references/design-system.md`. Use the `frontend-design` skill for creative direction, staying inside ZON's palette and typography.
4. **Build.** Default stack for new sites: Next.js (App Router) + TypeScript + CSS variables from `assets/tokens.css` (Tailwind is fine if it maps to the same tokens). Follow `vercel-react-best-practices` for React/Next.js work. Plain semantic HTML/CSS is fine for single pages.
5. **Interactive demonstrations.** See the section in `references/design-system.md`: progressive enhancement, poster image first, 3D/configurators lazy-loaded, keyboard operable, reduced-motion aware.
6. **Verify.** Run the checklist in `references/qa-checklist.md`: `web-design-guidelines` review, `webapp-testing` (Playwright) screenshots at 375/768/1280/1920 px, keyboard pass, contrast, Lighthouse/Core Web Vitals.
7. **Report.** End with: what was built, screenshots, QA results, and every `[[VERIFY]]` placeholder still open.

## Composition principles (quick reference)

- Architectural grid: 12 columns, generous margins, strong vertical rhythm; let photography bleed full-width and keep text on the grid.
- One idea per section. Headline states the benefit, sub-line gives the proof (verified), CTA follows.
- Large, honest photography of real ZON work. Never pass off stock or AI renders as completed ZON projects; label CGIs as "Computer-generated visualisation".
- Ivory as the dominant surface, emerald for authority (headers, footers, key bands), walnut for warmth (secondary surfaces, imagery mood), brass as a thin accent only (rules, icons, focus details), never body text on light backgrounds.
- Motion is architectural: slow, eased reveals (200–600 ms), no bouncing, no autoplaying carousels, always disabled under `prefers-reduced-motion`.
- British English throughout (colour, metre, organisation), £ and UK date formats.

## Files

- `references/design-system.md` – palette with contrast ratios, typography, spacing, motion, imagery, interactive demos, component patterns.
- `references/content-and-claims.md` – voice, page structures, CTA patterns, UK advertising/green-claims rules, claim verification.
- `references/verified-facts.md` – the only source of ZON facts. Starts empty; fill it from official ZON material with sources.
- `references/qa-checklist.md` – accessibility, performance budgets and testing steps.
- `assets/tokens.css` – drop-in CSS custom properties.
ZON_EOF
cat > "$D/assets/tokens.css" <<'ZON_EOF'
/* ZON design tokens. Contrast ratios are WCAG 2.x against the noted background. */
:root {
  /* Emerald – authority */
  --zon-emerald-900: #0B3B2E; /* 11.6:1 on ivory-50 */
  --zon-emerald-700: #145C46; /* 7.35:1 on ivory-50 */
  --zon-emerald-100: #DCE8E1;

  /* Walnut – warmth */
  --zon-walnut-800: #4A3226;  /* 10.97:1 on ivory-50 */
  --zon-walnut-600: #6B4A36;  /* 7.33:1 on ivory-50 */
  --zon-walnut-100: #EADFD4;

  /* Brass – accent only */
  --zon-brass-300: #CDAE78;   /* 5.91:1 on emerald-900: text OK on dark */
  --zon-brass-500: #B08D57;   /* 2.87:1 on ivory-50: decorative only */
  --zon-brass-700: #8A6A3A;   /* 4.63:1 on ivory-50: text OK, use sparingly */

  /* Ivory – surfaces */
  --zon-ivory-50:  #FAF6EE;
  --zon-ivory-100: #F3ECDF;
  --zon-ivory-200: #E9DFCC;

  /* Text */
  --zon-ink:   #1C1A17;       /* 16.1:1 on ivory-50 */
  --zon-muted: #5E574D;       /* 6.61:1 on ivory-50 */

  /* Semantic */
  --color-bg: var(--zon-ivory-50);
  --color-surface: var(--zon-ivory-100);
  --color-text: var(--zon-ink);
  --color-text-muted: var(--zon-muted);
  --color-primary: var(--zon-emerald-900);
  --color-primary-hover: var(--zon-emerald-700);
  --color-on-primary: var(--zon-ivory-50);
  --color-accent: var(--zon-brass-500);
  --color-accent-on-dark: var(--zon-brass-300);
  --color-focus: var(--zon-brass-700);

  /* Typography */
  --font-display: "Cormorant Garamond", "Iowan Old Style", Georgia, serif;
  --font-body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --text-xs: clamp(0.78rem, 0.76rem + 0.1vw, 0.84rem);
  --text-sm: clamp(0.88rem, 0.86rem + 0.12vw, 0.95rem);
  --text-base: clamp(1rem, 0.97rem + 0.18vw, 1.125rem);
  --text-lg: clamp(1.2rem, 1.12rem + 0.4vw, 1.45rem);
  --text-xl: clamp(1.6rem, 1.4rem + 1vw, 2.2rem);
  --text-2xl: clamp(2.2rem, 1.8rem + 2vw, 3.4rem);
  --text-display: clamp(2.8rem, 2rem + 4vw, 5.6rem);
  --leading-tight: 1.08;
  --leading-body: 1.6;
  --tracking-caps: 0.14em;

  /* Spacing (8px base) */
  --space-1: 0.5rem; --space-2: 1rem; --space-3: 1.5rem; --space-4: 2rem;
  --space-6: 3rem; --space-8: 4rem; --space-12: 6rem; --space-16: 8rem;
  --container: 80rem;
  --gutter: clamp(1rem, 4vw, 3rem);
  --radius: 2px;

  /* Motion */
  --ease-arch: cubic-bezier(0.22, 0.61, 0.36, 1);
  --dur-fast: 200ms; --dur-base: 400ms; --dur-slow: 600ms;
}

@media (prefers-reduced-motion: reduce) {
  :root { --dur-fast: 0ms; --dur-base: 0ms; --dur-slow: 0ms; }
}

:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; }
ZON_EOF
cat > "$D/references/content-and-claims.md" <<'ZON_EOF'
# Content, Copy and Claims

## Voice

Confident, precise, warm, British. Short sentences. Concrete nouns over adjectives. Speak to the reader's outcome (a home, a scheme delivered, lower running costs) without overpromising. No hype words: "revolutionary", "best-in-class", "world-leading", "guaranteed" (unless a verified, documented guarantee exists).

## Page structure for conversion

1. Hero: who it's for + benefit + primary CTA.
2. Problem/aspiration in the visitor's words.
3. How ZON solves it (services or product), with proof.
4. Process: what happens after they enquire.
5. Projects/case studies (verified).
6. Objection handling / FAQ (planning, timelines, finance, warranties — verified answers only).
7. Final CTA with reassurance (response time only if ZON commits to it).

Each page has ONE primary CTA. Good CTA labels are specific: "Book a design consultation", "Request a site appraisal", "Download the brochure". Avoid "Submit", "Click here", "Learn more" on its own.

## Claim verification (mandatory)

Before publishing any statement in these categories, it must appear in `verified-facts.md` with a source and date:
- Prices, costs, savings, payback periods, finance terms
- Energy performance (EPC, SAP, U-values, kWh, carbon figures, "net zero", "zero bills")
- Build or delivery times
- Warranties, guarantees, insurance-backed schemes (e.g. structural warranties), certifications and accreditations
- Project names, locations, clients, numbers of homes, awards, testimonials, press mentions
- Company facts: legal name, Companies House number, address, years trading, team size

If missing: write `[[VERIFY: description]]`, keep layout intact, and list it in the handover report.

## UK rules to respect (summary, not legal advice)

- ASA / CAP Code: claims must be substantiated; comparative claims must be fair; prices must include VAT where consumers are the audience and state what is included.
- CMA Green Claims Code: environmental claims must be truthful, clear, not omit important information, consider the full life cycle, and be substantiated. Avoid vague "eco", "green", "sustainable" without specifics.
- Testimonials must be genuine, attributable and current; never fabricate or edit their meaning.
- UK GDPR / PECR: cookie consent before non-essential cookies/analytics; forms explain how data is used and link to the privacy policy.
- Use "computer-generated visualisation" and "illustrative" labels where relevant.

## Microcopy

- Form errors say what to fix: "Enter a UK postcode, for example SW1A 1AA".
- Success state says what happens next and when (only commitments ZON has made).
- Buttons describe the action; links describe the destination.
ZON_EOF
cat > "$D/references/design-system.md" <<'ZON_EOF'
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
ZON_EOF
cat > "$D/references/qa-checklist.md" <<'ZON_EOF'
# QA Checklist (acceptance criteria)

## Accessibility (WCAG 2.2 AA)
- [ ] Text contrast ≥ 4.5:1 (large text ≥ 3:1); brass-500 never used for text on light backgrounds
- [ ] Keyboard: every interactive element reachable, logical order, visible `:focus-visible`, no traps; skip link present
- [ ] Landmarks (header/nav/main/footer), one H1, no skipped heading levels
- [ ] Images have correct alt text; decorative images `alt=""`
- [ ] Forms: visible labels, errors linked via `aria-describedby`, not colour-only
- [ ] Target size ≥ 24×24 px (aim 44×44 on touch)
- [ ] Interactive demos have a text alternative and work without a pointer
- [ ] `prefers-reduced-motion` respected; nothing flashes > 3 times/second
- [ ] `lang="en-GB"` on `<html>`

## Performance budgets (mobile, 4G)
- [ ] LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1
- [ ] Initial JS ≤ 170 KB gzipped on marketing pages; 3D/configurator code lazy-loaded
- [ ] Hero image ≤ 200 KB, modern formats, explicit dimensions
- [ ] Fonts self-hosted, ≤ 2 families, preload only critical weight
- [ ] Lighthouse: Performance ≥ 90, Accessibility 100, Best Practices ≥ 95, SEO ≥ 95

## SEO and sharing
- [ ] Unique title (≤ 60 chars) and meta description per page
- [ ] Open Graph/Twitter image, canonical URL, sitemap, robots
- [ ] Structured data (Organization/LocalBusiness) using verified facts only

## Content integrity
- [ ] Every factual claim traced to `verified-facts.md`
- [ ] No `[[VERIFY]]` placeholders remain — or they are listed in the handover
- [ ] CGIs labelled; British English; prices incl. VAT where shown to consumers

## How to test
1. `web-design-guidelines` skill: review the changed UI files.
2. `webapp-testing` skill (Python Playwright): run the local server via `scripts/with_server.py` (prefix the server command with `exec`, e.g. `--server "exec npm run dev"`, otherwise the server can outlive the test and block the port on the next run), capture full-page screenshots at 375, 768, 1280 and 1920 px, check the console for errors, tab through the page.
3. Contrast: compute ratios for any new colour pairing.
4. Lighthouse (`npx lighthouse <url> --preset=desktop` and mobile default) or PageSpeed Insights for deployed previews.
5. Report results with screenshots in the handover.
ZON_EOF
cat > "$D/references/verified-facts.md" <<'ZON_EOF'
# ZON Verified Facts

The ONLY source of factual claims for ZON web copy. Add an entry only from official ZON material (signed-off documents, Companies House, certificates, completed project records). Every row needs a source and the date it was checked. If a fact is not here, it does not go on the website — use `[[VERIFY: ...]]` instead.

Status: EMPTY — awaiting official ZON information.

## Company

| Fact | Value | Source | Checked on |
|---|---|---|---|
| Legal company name | | | |
| Companies House number | | | |
| Registered address | | | |
| Trading brands / domains | | | |
| Contact email / phone | | | |

## Brand assets

| Asset | Location | Notes |
|---|---|---|
| Logo (SVG, light/dark) | | |
| Official fonts | | |
| Official colours | | |
| Photography library | | |

## Services and products

| Product / service | Description (approved wording) | Key specs | Source | Checked on |
|---|---|---|---|---|

## Projects

| Project | Location | Type | Year | Verified outcomes | Images (rights cleared?) | Source |
|---|---|---|---|---|---|---|

## Accreditations, warranties, memberships

| Item | Reference number | Valid until | Source |
|---|---|---|---|

## Approved figures (prices, energy, timelines)

| Claim | Exact approved wording | Conditions / footnote | Source | Checked on |
|---|---|---|---|---|

## Testimonials

| Quote | Person / organisation | Permission recorded | Date |
|---|---|---|---|
ZON_EOF
echo "Installed: $D"
