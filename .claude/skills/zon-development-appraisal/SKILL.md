---
name: zon-development-appraisal
description: Residential development appraisal for ZON schemes — GDV, total development cost, project profit, margins, residual land value, senior debt / partner equity split, preferred return (simple vs compound), residual profit to ZON, and side-by-side scenarios (private sale, affordable housing, cost overrun, delay). Use this whenever the user asks whether a site or scheme makes money, how much to pay for land, what investors get, how a change in prices, build cost, unit mix or affordable housing moves profit, or needs numbers for an investor deck or Excel model — even if they only say "порахуй", "фінмодель", "прибуток", "скільки платити за землю" or paste a table of homes and prices.
---

# Development appraisal

Investors and lenders read three separate things, and mixing them is the most common way a deck loses credibility:
1. **Project economics** — GDV, TDC, project profit before any partner return.
2. **Partner return** — capital, preferred return, cover.
3. **Developer residual** — what is left for ZON after partners.

Never call project profit "ZON's profit". Always show a planning/affordable case next to the private-sale case until S106 terms are agreed, not in small print.

## Workflow

1. **Inputs.** Get the unit schedule (type, count, GIA, price), land price, build rate and what it includes, obligations, finance terms. Copy `references/wivenhoe-inputs.json` as the template. Mark each input as confirmed (agent letter, QS, term sheet) or assumed.
2. **Sanity checks before running:**
   - Build rate: is it the full turnkey cost per m² GIA, or a shell/frame price? A frame-only price needs foundations, fit-out, kitchens, bathrooms, services, warranty and prelims on top (often +£800–1,100/m²). Ask.
   - Areas: GIA of habitable space, not including garages/terraces. Cross-check with zon-architectural-drawings when plans exist.
   - Prices: compare £/ft² with local new-build evidence; small units achieve higher £/m².
   - Affordable housing count is rounded up from total homes, and the S106 may fix which type and tenure.
3. **Run** `python3 scripts/appraisal.py inputs.json --md summary.md`. Scenarios override any input with `"set"` and prices with `"price_factor"`.
4. **Report** the three layers, the scenarios table, the residual land value at the target margin, and the two or three inputs that move profit most (run ±10% on price and build cost).

## Conventions (state them in the output)

- Contingency and professional fees are % of build + external works.
- Finance: interest on 50% average drawdown of construction-related costs over the programme, plus land and acquisition costs for the full term plus any planning delay. It is an approximation; a monthly cash flow replaces it once the lender's terms are known.
- 70/30 debt/equity on TDC is illustrative; lenders set LTC/LTV, fees and drawdowns in the term sheet.
- Preferred return: say whether it is simple (capital × rate × years) or compound/IRR, and that it accrues on drawn and outstanding capital. Suggested wording: "Target 12% annual preferred return, calculated on drawn and outstanding partner capital. Final return depends on the timing of drawdowns and repayments."
- Typical lender target: 17–20% profit on GDV for private sale; below ~12% most lenders decline.
- Investor-facing figures are indicative and must not be presented as a guaranteed return; UK financial promotion rules (FSMA s21) apply to distribution.

## Excel

When the user wants a spreadsheet, build it with formulas (xlsx skill) using the same structure, and check that it reproduces the script's numbers to the pound.
