#!/usr/bin/env python3
"""Preliminary strip-foundation width and depth guidance for low-rise timber-frame
homes. Line load from the wall, allowable bearing pressure from the site
investigation (or a cautious default), NHBC-style depth guidance on clay.

PRELIMINARY ONLY. Foundation design needs a site investigation and a chartered engineer.

Usage: python3 foundation.py --line-load 25 --bearing 100 [--soil clay-high] [--tree-distance 8 --tree-height 20 --water-demand high]
  line-load: characteristic (SLS) load per metre of wall, kN/m
  bearing:   allowable bearing pressure, kN/m² (from SI; 75-150 typical for firm clays)
"""
import argparse, json

MIN_DEPTH = {"granular": 0.45, "clay-low": 0.75, "clay-medium": 0.9, "clay-high": 1.0}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--line-load", type=float, required=True)
    p.add_argument("--bearing", type=float, required=True)
    p.add_argument("--soil", default="clay-high", choices=MIN_DEPTH)
    p.add_argument("--tree-distance", type=float)
    p.add_argument("--tree-height", type=float)
    p.add_argument("--water-demand", choices=["low", "moderate", "high"])
    a = p.parse_args()
    width = max(0.45, a.line_load / a.bearing)
    depth = MIN_DEPTH[a.soil]
    notes = []
    if a.tree_distance is not None and a.soil.startswith("clay"):
        ratio = a.tree_distance / a.tree_height if a.tree_height else 99
        if ratio < 1.25 and a.water_demand in ("high", "moderate"):
            notes.append("tree within its zone of influence on shrinkable clay: NHBC 4.2 depth likely 1.5-3.0 m; piles (screw/bored) often cheaper above ~2.5 m")
            depth = max(depth, 1.5)
        elif ratio < 2:
            notes.append("tree influence possible: check NHBC 4.2 charts")
    if depth > 2.5:
        notes.append("consider piled foundations with ground beams")
    print(json.dumps({"strip_width_m": round(width, 2), "min_depth_m": depth,
                      "bearing_used_kPa": a.bearing, "notes": notes}, indent=1))
    print("PRELIMINARY ONLY - foundation design requires a site investigation and a chartered engineer.")


if __name__ == "__main__":
    main()
