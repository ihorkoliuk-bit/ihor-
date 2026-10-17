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
