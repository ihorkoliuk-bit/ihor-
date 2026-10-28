#!/usr/bin/env python3
"""Draw scaled elevations (A3) from a JSON spec in millimetres.

The drawings double as the geometry reference for image generators: feed the
PNG to the render tool as a control/reference image so the render keeps the
real proportions, window positions and roof pitch.

Usage: python3 elevation.py spec.json out_basename
"""
import json, math, sys

PAPER_W, PAPER_H, MARGIN = 420.0, 297.0, 18.0
INK = "#1F1F1F"
MAT = {"brick": "#B5654A", "timber": "#C9A57A", "dark-timber": "#4A4038", "render": "#ECE6DB",
       "stone": "#BDB3A3", "metal": "#3A3D40", "tile": "#3E3B39", "glass": "#BFD3DF", "door": "#5B4636"}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;")


def draw_one(e, x0, base, k, font):
    """x0, base: paper coords of the left end of the ground line."""
    o = []
    W, eaves, ridge = e["width"], e["eaves"], e["ridge"]
    ov = e.get("overhang", 300)
    Y = lambda h: base - h * k
    X = lambda x: x0 + x * k
    # walls
    o.append(f'<rect x="{X(0):.3f}" y="{Y(eaves):.3f}" width="{W*k:.3f}" height="{eaves*k:.3f}" fill="{MAT.get(e.get("wall","render"))}" stroke="{INK}" stroke-width="0.3"/>')
    for b in e.get("bands", []):   # cladding zones: x, w, from_h, to_h, material
        o.append(f'<rect x="{X(b["x"]):.3f}" y="{Y(b["to"]):.3f}" width="{b["w"]*k:.3f}" height="{(b["to"]-b["from"])*k:.3f}" fill="{MAT.get(b["mat"], "#ccc")}" stroke="{INK}" stroke-width="0.15"/>')
    if e.get("plinth"):
        o.append(f'<rect x="{X(0):.3f}" y="{Y(e["plinth"]):.3f}" width="{W*k:.3f}" height="{e["plinth"]*k:.3f}" fill="{MAT["stone"]}" stroke="{INK}" stroke-width="0.2"/>')
    # roof
    rm = MAT.get(e.get("roof_mat", "tile"))
    if e.get("roof", "gable-front") == "gable-front":
        gable = e.get("gable_fill")
        if gable:
            o.append(f'<path d="M{X(0):.3f} {Y(eaves):.3f} L{X(W/2):.3f} {Y(ridge):.3f} L{X(W):.3f} {Y(eaves):.3f} Z" fill="{MAT.get(gable)}" stroke="{INK}" stroke-width="0.2"/>')
        o.append(f'<path d="M{X(-ov):.3f} {Y(eaves - ov*(ridge-eaves)/(W/2)):.3f} L{X(W/2):.3f} {Y(ridge):.3f} L{X(W+ov):.3f} {Y(eaves - ov*(ridge-eaves)/(W/2)):.3f}" fill="none" stroke="{rm}" stroke-width="{max(0.6, 250*k):.3f}" stroke-linejoin="miter"/>')
        pitch = math.degrees(math.atan((ridge - eaves) / (W / 2)))
    else:  # eaves to the front: roof seen as a slope band
        o.append(f'<rect x="{X(-ov):.3f}" y="{Y(ridge):.3f}" width="{(W+2*ov)*k:.3f}" height="{(ridge-eaves+120)*k:.3f}" fill="{rm}" stroke="{INK}" stroke-width="0.3"/>')
        pitch = None
    # openings
    for op in e.get("openings", []):
        x, sill, w, h = op["x"], op.get("sill", 0), op["w"], op["h"]
        if op.get("gable") and e.get("roof", "gable-front") == "gable-front":
            # triangular glazing following the roof pitch: x/w define the base, h the height above sill
            o.append(f'<path d="M{X(x):.3f} {Y(sill):.3f} L{X(x+w/2):.3f} {Y(sill+h):.3f} L{X(x+w):.3f} {Y(sill):.3f} Z" fill="{MAT["glass"]}" stroke="{INK}" stroke-width="0.35"/>')
            continue
        fill = MAT["door"] if op.get("type") == "door" else MAT["glass"]
        o.append(f'<rect x="{X(x):.3f}" y="{Y(sill+h):.3f}" width="{w*k:.3f}" height="{h*k:.3f}" fill="{fill}" stroke="{INK}" stroke-width="0.35"/>')
        for m in range(1, op.get("panes", 1)):
            mx = X(x + w * m / op["panes"])
            o.append(f'<line x1="{mx:.3f}" y1="{Y(sill+h):.3f}" x2="{mx:.3f}" y2="{Y(sill):.3f}" stroke="{INK}" stroke-width="0.25"/>')
    # ground and levels
    o.append(f'<line x1="{X(-1500):.3f}" y1="{base:.3f}" x2="{X(W+1500):.3f}" y2="{base:.3f}" stroke="{INK}" stroke-width="0.5"/>')
    for h, lab in ((0, "GL / FFL ±0"), (eaves, f"Eaves +{eaves:.0f}"), (ridge, f"Ridge +{ridge:.0f}")):
        o.append(f'<line x1="{X(W)+16:.3f}" y1="{Y(h):.3f}" x2="{X(W)+24:.3f}" y2="{Y(h):.3f}" stroke="#555" stroke-width="0.15"/>')
        o.append(f'<text x="{X(W)+25:.3f}" y="{Y(h)+0.8:.3f}" {font} font-size="2.2" fill="#222">{lab}</text>')
    # width dimension
    o.append(f'<line x1="{X(0):.3f}" y1="{base+7:.3f}" x2="{X(W):.3f}" y2="{base+7:.3f}" stroke="#333" stroke-width="0.18"/>')
    for xx in (X(0), X(W)):
        o.append(f'<line x1="{xx-0.8:.3f}" y1="{base+7.8:.3f}" x2="{xx+0.8:.3f}" y2="{base+6.2:.3f}" stroke="#333" stroke-width="0.3"/>')
    o.append(f'<text x="{(X(0)+X(W))/2:.3f}" y="{base+6.2:.3f}" {font} font-size="2.2" text-anchor="middle">{W:.0f}</text>')
    title = e["name"] + (f" · roof pitch {pitch:.0f}°" if pitch else "")
    o.append(f'<text x="{X(0):.3f}" y="{base+13:.3f}" {font} font-size="3" font-weight="600" fill="{INK}">{esc(title)}</text>')
    return o


def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    els = spec["elevations"]
    font = 'font-family="Inter, Helvetica, Arial, sans-serif"'
    cols = 1
    rows = len(els)
    cell_w = (PAPER_W - 2 * MARGIN) / cols
    cell_h = (PAPER_H - 2 * MARGIN - 20) / rows
    maxw = max(e["width"] + 2 * e.get("overhang", 300) for e in els)
    maxh = max(e["ridge"] for e in els)
    s = spec.get("scale")
    if not s:
        for s in (50, 100, 200):
            if maxw / s <= cell_w - 40 and maxh / s <= cell_h - 22:
                break
    k = 1 / s
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAPER_W}mm" height="{PAPER_H}mm" viewBox="0 0 {PAPER_W} {PAPER_H}">',
         f'<rect width="{PAPER_W}" height="{PAPER_H}" fill="#FFFFFF"/>',
         f'<text x="{MARGIN}" y="{MARGIN+4}" {font} font-size="7" font-weight="300" letter-spacing="1.2">{esc(spec["name"].upper())} · ELEVATIONS</text>',
         f'<text x="{PAPER_W-MARGIN}" y="{MARGIN+4}" {font} font-size="3" text-anchor="end">Scale 1:{s} @ A3 · dimensions in mm</text>']
    for i, e in enumerate(els):
        c, r = i % cols, i // cols
        x0 = MARGIN + c * cell_w + 20
        base = MARGIN + 20 + r * cell_h + (cell_h + e["ridge"] * k) / 2 - 6
        o += draw_one(e, x0, base, k, font)
    o.append("</svg>")
    open(out + ".svg", "w").write("\n".join(o))
    print(json.dumps({"svg": out + ".svg", "scale": f"1:{s}"}))


if __name__ == "__main__":
    main()
