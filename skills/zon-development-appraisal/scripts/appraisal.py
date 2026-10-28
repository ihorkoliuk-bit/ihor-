#!/usr/bin/env python3
"""Residential development appraisal: GDV -> TDC -> project profit -> partner
preferred return -> residual to the developer, for several scenarios.

Usage: python3 appraisal.py inputs.json [--md out.md]
Prints a JSON result; with --md also writes a markdown summary.

Method (same as the ZON Wivenhoe model):
  build      = sum(count * gia) * build_rate  (+ extra_build items)
  contingency, fees = % of (build + external works)
  sales      = sales_pct * GDV + sales_legal_per_unit * units
  finance    = rate * (avg_draw * costs_ex_land_ex_finance * months/12
                       + (land + land_costs) * (months + delay)/12)
  affordable = n_aff homes of the chosen type sold at aff_value_pct of market
"""
import json, math, sys, copy


def run(base, sc):
    p = copy.deepcopy(base)
    for k, v in sc.get("set", {}).items():
        p[k] = v
    units = p["units"]
    pf = sc.get("price_factor", 1.0)
    n = sum(u["count"] for u in units)
    area = sum(u["count"] * u["gia"] for u in units)
    market = sum(u["count"] * u["price"] for u in units) * pf

    aff_share = p.get("affordable_share", 0.0)
    n_aff = math.ceil(n * aff_share - 1e-9) if aff_share else 0
    aff_type = p.get("affordable_type", units[0]["name"])
    aff_unit = next(u for u in units if u["name"] == aff_type)
    if n_aff > aff_unit["count"]:
        raise SystemExit(f"{n_aff} affordable homes needed but only {aff_unit['count']} {aff_type}")
    aff_discount = n_aff * aff_unit["price"] * pf * (1 - p.get("affordable_value_pct", 0.6))
    gdv = market - aff_discount + p.get("other_income", 0)

    build = area * p["build_rate"] + sum(p.get("extra_build", {}).values())
    ext = p["external_works"] if "external_works" in p else p["external_per_unit"] * n
    base_be = build + ext
    cont = base_be * p.get("contingency_pct", 0.05)
    fees = base_be * p.get("fees_pct", 0.10)
    oblig = sum(p.get("obligations", {}).values())
    sales = gdv * p.get("sales_pct", 0.025) + p.get("sales_legal_per_unit", 1500) * n
    land = p["land"]
    land_costs = p.get("land_costs", land * p.get("land_costs_pct", 0.06))
    pre_fin = build + ext + cont + fees + oblig + sales
    months, delay = p.get("months", 24), p.get("delay_months", 0)
    finance = p.get("finance_rate", 0.09) * (p.get("avg_draw", 0.5) * pre_fin * months / 12
                                             + (land + land_costs) * (months + delay) / 12)
    tdc = pre_fin + land + land_costs + finance
    profit = gdv - tdc

    eq = tdc * (1 - p.get("debt_ltc", 0.70))
    pr = p.get("pref_rate", 0.12)
    pm = p.get("pref_months", months)
    pref_simple = eq * pr * pm / 12
    pref_compound = eq * ((1 + pr) ** (pm / 12) - 1)
    pref = pref_compound if p.get("pref_basis") == "compound" else pref_simple
    paid = min(pref, max(profit, 0))
    return {
        "scenario": sc["name"], "homes": n, "gia_m2": round(area, 1),
        "market_value": round(market), "affordable_homes": n_aff, "affordable_discount": round(aff_discount),
        "gdv": round(gdv),
        "costs": {"land": round(land), "land_costs": round(land_costs), "build": round(build),
                  "external_works": round(ext), "contingency": round(cont), "fees": round(fees),
                  "obligations": round(oblig), "sales": round(sales), "finance": round(finance)},
        "tdc": round(tdc), "profit": round(profit),
        "margin_on_gdv": round(profit / gdv, 4) if gdv else None,
        "margin_on_cost": round(profit / tdc, 4) if tdc else None,
        "profit_per_home": round(profit / n),
        "senior_debt": round(tdc - eq), "partner_capital": round(eq),
        "pref_return": round(pref), "pref_return_simple": round(pref_simple), "pref_return_compound": round(pref_compound),
        "pref_paid": round(paid), "pref_shortfall": round(pref - paid),
        "residual_to_developer": round(max(profit - pref, 0)),
        "cover": round(profit / pref, 2) if pref else None,
        "moic": round((eq + paid) / eq, 2) if eq else None,
        "rlv_at_target": rlv(p, gdv, pre_fin, months, delay),
    }


def rlv(p, gdv, pre_fin, months, delay):
    """Max land price that still leaves target_margin on GDV."""
    t = p.get("target_margin", 0.20)
    r = p.get("finance_rate", 0.09)
    lc = p.get("land_costs_pct", 0.06)
    fin_b = r * p.get("avg_draw", 0.5) * pre_fin * months / 12
    avail = gdv * (1 - t) - pre_fin - fin_b
    return round(avail / ((1 + lc) * (1 + r * (months + delay) / 12)))


def fmt(x):
    return f"£{x:,.0f}" if x >= 0 else f"(£{-x:,.0f})"


def md(results):
    cols = [r["scenario"] for r in results]
    rows = [("GDV", "gdv", fmt), ("Total development cost", "tdc", fmt), ("Project profit", "profit", fmt),
            ("Margin on GDV", "margin_on_gdv", lambda v: f"{v:.1%}"), ("Margin on cost", "margin_on_cost", lambda v: f"{v:.1%}"),
            ("Partner capital", "partner_capital", fmt), ("Preferred return", "pref_return", fmt),
            ("Residual to developer, pre-tax", "residual_to_developer", fmt), ("Cover of partner return", "cover", lambda v: f"{v:.2f}×"),
            ("Max land price at target margin", "rlv_at_target", fmt)]
    out = ["| Measure | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    for lab, key, f in rows:
        out.append(f"| {lab} | " + " | ".join(f(r[key]) if r[key] is not None else "–" for r in results) + " |")
    return "\n".join(out)


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    res = [run(data["base"], sc) for sc in data.get("scenarios", [{"name": "Base"}])]
    print(json.dumps(res, indent=1))
    if "--md" in sys.argv:
        open(sys.argv[sys.argv.index("--md") + 1], "w").write(md(res) + "\n")
