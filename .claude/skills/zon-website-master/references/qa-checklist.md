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
