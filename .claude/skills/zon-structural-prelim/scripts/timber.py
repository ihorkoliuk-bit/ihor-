#!/usr/bin/env python3
"""Preliminary sizing of solid/glulam timber members to Eurocode 5 (EN 1995-1-1)
with UK National Annex partial factors. Simply supported member, uniform load.

FOR EARLY DESIGN AND COST PLANNING ONLY. Final design and Building Regulations
Part A submission must be by a chartered structural engineer.

Usage:
  python3 timber.py --span 4.2 --spacing 0.4 --gk 0.5 --qk 1.5 --b 47 --h 220 --grade C24 \
                    [--service 1] [--load-duration medium] [--limit 250]
  gk, qk in kN/m² of floor/roof area; spacing in m; b, h in mm; span in m.
  Add --sweep to try standard depths and report the smallest that passes.
"""
import argparse, json

GRADES = {  # EN 338 / EN 14080: fm,k  fv,k  E0,mean  rho_k   (N/mm², kg/m³)
    "C16": (16, 3.2, 8000, 310),
    "C24": (24, 4.0, 11000, 350),
    "GL24h": (24, 3.5, 11500, 385),
    "GL28h": (28, 3.5, 12600, 425),
}
KMOD = {1: {"permanent": 0.6, "long": 0.7, "medium": 0.8, "short": 0.9},
        2: {"permanent": 0.6, "long": 0.7, "medium": 0.8, "short": 0.9},
        3: {"permanent": 0.5, "long": 0.55, "medium": 0.65, "short": 0.7}}
KDEF = {1: 0.6, 2: 0.8, 3: 2.0}           # solid timber
GAMMA_M = {"C16": 1.3, "C24": 1.3, "GL24h": 1.25, "GL28h": 1.25}
PSI2 = 0.3                                # domestic floors (category A)
DEPTHS = [97, 120, 145, 170, 195, 220, 245, 270, 295]


def check(a, h):
    fmk, fvk, E, _ = GRADES[a.grade]
    L = a.span * 1000.0                    # mm
    w_g = a.gk * a.spacing                 # kN/m = N/mm
    w_q = a.qk * a.spacing
    w_uls = 1.35 * w_g + 1.5 * w_q         # EN 1990 eq. 6.10
    M = w_uls * L ** 2 / 8                 # N·mm
    V = w_uls * L / 2                      # N
    b = a.b
    W = b * h ** 2 / 6
    I = b * h ** 3 / 12
    kmod = KMOD[a.service][a.load_duration]
    kh = min((150 / h) ** 0.2, 1.3) if (h < 150 and a.grade.startswith("C")) else 1.0
    gm = GAMMA_M[a.grade]
    fmd = kmod * kh * fmk / gm
    fvd = kmod * fvk / gm
    sig = M / W
    tau = 1.5 * V / (0.67 * b * h)         # kcr = 0.67
    u = lambda w: 5 * w * L ** 4 / (384 * E * I)
    u_fin = u(w_g) * (1 + KDEF[a.service]) + u(w_q) * (1 + PSI2 * KDEF[a.service])
    lim = L / a.limit
    if a.floor:
        lim = min(lim, 14.0)               # UK NA practical cap for domestic floors
    return {
        "section_mm": f"{b:.0f}x{h:.0f} {a.grade} @ {a.spacing*1000:.0f} c/c",
        "span_m": a.span,
        "bending_util": round(sig / fmd, 2),
        "shear_util": round(tau / fvd, 2),
        "deflection_mm": round(u_fin, 1), "deflection_limit_mm": round(lim, 1),
        "deflection_util": round(u_fin / lim, 2),
        "pass": sig <= fmd and tau <= fvd and u_fin <= lim,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--span", type=float, required=True)
    p.add_argument("--spacing", type=float, default=0.4)
    p.add_argument("--gk", type=float, required=True)
    p.add_argument("--qk", type=float, required=True)
    p.add_argument("--b", type=float, default=47)
    p.add_argument("--h", type=float, default=220)
    p.add_argument("--grade", default="C24", choices=GRADES)
    p.add_argument("--service", type=int, default=1, choices=[1, 2, 3])
    p.add_argument("--load-duration", dest="load_duration", default="medium", choices=["permanent", "long", "medium", "short"])
    p.add_argument("--limit", type=float, default=250)
    p.add_argument("--floor", action="store_true", help="apply the 14 mm cap for domestic floors")
    p.add_argument("--sweep", action="store_true")
    a = p.parse_args()
    if a.sweep:
        res = None
        for h in DEPTHS:
            r = check(a, h)
            if r["pass"]:
                res = r
                break
        print(json.dumps(res or {"pass": False, "note": "no standard depth passes; reduce span or spacing, or use glulam/steel"}, indent=1))
    else:
        print(json.dumps(check(a, a.h), indent=1))
    print("PRELIMINARY ONLY - to be designed and signed off by a chartered structural engineer.")


if __name__ == "__main__":
    main()
