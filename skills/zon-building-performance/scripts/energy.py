#!/usr/bin/env python3
"""Fabric U-values, design heat loss and heat-pump sizing, PV yield — early-stage.

Usage:
  python3 energy.py uvalue layers.json          # U-value of one element
  python3 energy.py heatloss house.json         # room-by-room heat loss + ASHP size + PV

U-value: 1 / (Rsi + sum(d/lambda) + Rse). Bridged layers (timber studs in insulation)
use the simple parallel-path area weighting, which is slightly optimistic compared
with BS EN ISO 6946's combined method; add ~5-10 % or use a manufacturer's calculation
for Building Regulations.

Heat loss (BS EN 12831 simplified, as used for MCS sizing):
  fabric = sum(U * A) * (Ti - Te);  ventilation = 0.33 * n * V * (Ti - Te)
NOT a SAP calculation. Part L compliance needs SAP 10 / the Home Energy Model by an accredited assessor.
"""
import json, sys

RS = {"wall": (0.13, 0.04), "roof": (0.10, 0.04), "floor": (0.17, 0.04), "window": (0, 0)}
PART_L_2021_LIMITS = {"wall": 0.26, "roof": 0.16, "floor": 0.18, "window": 1.6, "door": 1.6}
NOTIONAL_2021 = {"wall": 0.18, "roof": 0.11, "floor": 0.13, "window": 1.2, "door": 1.0}


def uvalue(el):
    rsi, rse = RS[el["type"]]
    R_unbridged = rsi + rse
    R_bridged = rsi + rse
    frac = 0.0
    for L in el["layers"]:
        d = L["d_mm"] / 1000
        if "bridge" in L:
            frac = L["bridge"]["fraction"]
            R_unbridged += d / L["lambda"]
            R_bridged += d / L["bridge"]["lambda"]
        else:
            R_unbridged += d / L["lambda"]
            R_bridged += d / L["lambda"]
    U = (1 - frac) / R_unbridged + frac / R_bridged
    return round(U, 3)


def heatloss(h):
    Te = h.get("external_design_temp", -2.0)
    out, total = [], 0.0
    for r in h["rooms"]:
        Ti = r.get("temp", 21)
        dT = Ti - Te
        fabric = sum(e["U"] * e["area"] for e in r["elements"]) * dT
        vent = 0.33 * r.get("ach", 0.5) * r["volume"] * dT
        q = fabric + vent
        total += q
        out.append({"room": r["name"], "W": round(q), "W_per_m2": round(q / r["floor_area"]) if r.get("floor_area") else None})
    hp_kw = total / 1000
    res = {"external_design_temp_C": Te, "rooms": out, "total_W": round(total),
           "heat_pump_kW_min": round(hp_kw, 1),
           "heat_pump_kW_suggested": round(hp_kw * 1.1 + 0.5, 1),
           "note": "add domestic hot water recovery; final sizing by MCS installer"}
    if "pv_kwp" in h:
        y = h.get("pv_yield_kwh_per_kwp", 950)
        res["pv_kWh_per_year"] = round(h["pv_kwp"] * y)
    if "fabric_check" in h:
        flags = []
        for k, u in h["fabric_check"].items():
            if u > PART_L_2021_LIMITS.get(k, 99):
                flags.append(f"{k} U={u} above Part L 2021 limiting value {PART_L_2021_LIMITS[k]}")
            elif u > NOTIONAL_2021.get(k, 99):
                flags.append(f"{k} U={u} worse than notional {NOTIONAL_2021[k]}: compensate elsewhere in SAP")
        res["fabric_flags"] = flags
    return res


if __name__ == "__main__":
    mode, path = sys.argv[1], sys.argv[2]
    data = json.load(open(path))
    print(json.dumps(uvalue(data) if mode == "uvalue" else heatloss(data), indent=1))
