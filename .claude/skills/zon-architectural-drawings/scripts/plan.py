#!/usr/bin/env python3
"""Draw a scaled floor plan from a JSON spec in millimetres.

Rooms are clear internal rectangles. Walls are whatever is left between rooms
and the external envelope, so room areas are exact and wall thickness shows up
as real gaps. Output: SVG (true scale on A3), plus PNG/PDF via render.py.

Usage: python3 plan.py spec.json out_basename
"""
import json, math, sys

PAPER_W, PAPER_H = 420.0, 297.0          # A3 landscape, mm
MARGIN = 18.0
SCALES = [50, 100, 200]

FLOOR = {"wood": "#DCC29C", "tile": "#C9CDD0", "stone": "#D8D2C6", "carpet": "#E4DCCF", "ext": "#E9E4DA"}
WALL = "#2B2B2B"
INK = "#1F1F1F"
ACCENT = "#8C5A3A"


def die(msg):
    sys.exit("plan.py: " + msg)


def check(spec):
    """Return (warnings, totals). Fails hard on geometry that cannot be right."""
    W, H = spec["internal"]["w"], spec["internal"]["h"]
    rooms = spec["rooms"]
    warns = []
    for r in rooms:
        x, y, w, h = r["x"], r["y"], r["w"], r["h"]
        if w <= 0 or h <= 0:
            die(f"room {r['name']} has non-positive size")
        if x < 0 or y < 0 or x + w > W + 0.5 or y + h > H + 0.5:
            die(f"room {r['name']} sits outside the internal envelope {W}x{H}")
    for i, a in enumerate(rooms):
        for b in rooms[i + 1:]:
            ox = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
            oy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
            if ox > 0.5 and oy > 0.5:
                die(f"rooms {a['name']} and {b['name']} overlap")
    net = sum(r["w"] * r["h"] for r in rooms) / 1e6
    internal = W * H / 1e6
    t = spec.get("wall_ext", 300)
    gia = internal  # GIA is measured to the internal face of external walls (RICS)
    gea = (W + 2 * t) * (H + 2 * t) / 1e6
    walls_share = (internal - net) / internal
    if walls_share > 0.12:
        warns.append(f"internal walls/voids take {walls_share:.0%} of GIA; expected 5-10%: check for missing rooms")
    if walls_share < 0.02 and len(rooms) > 2:
        warns.append(f"internal walls take only {walls_share:.0%} of GIA; rooms may be drawn without wall gaps")
    if spec.get("declared_area"):
        d = spec["declared_area"]
        if abs(d - gia) / d > 0.03:
            warns.append(f"declared area {d} m² differs from drawn GIA {gia:.1f} m² by {abs(d-gia)/d:.0%}")
    return warns, {"net": net, "gia": gia, "gea": gea}


def pick_scale(Wext, Hext):
    avail_w = PAPER_W - 2 * MARGIN - 30
    avail_h = PAPER_H - 2 * MARGIN - 40
    for s in SCALES:
        if Wext / s <= avail_w and Hext / s <= avail_h:
            return s
    die("building too large for A3 at 1:200")


def svg(spec):
    W, H = spec["internal"]["w"], spec["internal"]["h"]
    t = spec.get("wall_ext", 300)
    Wext, Hext = W + 2 * t, H + 2 * t
    s = spec.get("scale") or pick_scale(Wext + 1600, Hext + 1600)
    k = 1.0 / s  # paper mm per real mm
    ox = (PAPER_W - Wext * k) / 2 + 6
    oy = MARGIN + 30 + (PAPER_H - 2 * MARGIN - 55 - Hext * k) / 2
    P = lambda x, y: (ox + (x + t) * k, oy + (y + t) * k)   # internal coords -> paper
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAPER_W}mm" height="{PAPER_H}mm" viewBox="0 0 {PAPER_W} {PAPER_H}">',
         f'<rect width="{PAPER_W}" height="{PAPER_H}" fill="#FFFFFF"/>']
    font = 'font-family="Inter, Helvetica, Arial, sans-serif"'

    # envelope solid, rooms punched out
    x0, y0 = ox, oy
    o.append(f'<rect x="{x0:.3f}" y="{y0:.3f}" width="{Wext*k:.3f}" height="{Hext*k:.3f}" fill="{WALL}"/>')
    for r in spec["rooms"]:
        px, py = P(r["x"], r["y"])
        o.append(f'<rect x="{px:.3f}" y="{py:.3f}" width="{r["w"]*k:.3f}" height="{r["h"]*k:.3f}" fill="{FLOOR.get(r.get("floor","wood"), "#DCC29C")}"/>')
        if r.get("floor", "wood") == "tile":
            step = 300
            for gx in range(int(r["x"]) + step, int(r["x"] + r["w"]), step):
                a, b = P(gx, r["y"]); _, c = P(gx, r["y"] + r["h"])
                o.append(f'<line x1="{a:.3f}" y1="{b:.3f}" x2="{a:.3f}" y2="{c:.3f}" stroke="#B4B9BC" stroke-width="0.08"/>')
            for gy in range(int(r["y"]) + step, int(r["y"] + r["h"]), step):
                a, b = P(r["x"], gy); c, _ = P(r["x"] + r["w"], gy)
                o.append(f'<line x1="{a:.3f}" y1="{b:.3f}" x2="{c:.3f}" y2="{b:.3f}" stroke="#B4B9BC" stroke-width="0.08"/>')

    # openings
    for d in spec.get("doors", []):
        o += door(d, P, k, t)
    for w in spec.get("windows", []):
        o += window(w, P, k, t, W, H)
    for f in spec.get("furniture", []):
        o += furniture(f, P, k)

    # labels
    for r in spec["rooms"]:
        if not r["name"]:
            continue
        cx, cy = P(r["x"] + r["w"] / 2, r["y"] + r["h"] / 2)
        if "label_at" in r:
            cx, cy = P(*r["label_at"])
        area = r["w"] * r["h"] / 1e6
        fs = min(3.2, max(1.8, min(r["w"], r["h"]) * k / 6))
        lines = r["name"].split("\n")
        for i, line in enumerate(lines):
            yy = cy + (i - len(lines) / 2) * fs * 1.2
            o.append(f'<text x="{cx:.3f}" y="{yy:.3f}" {font} font-size="{fs:.2f}" font-weight="600" fill="{INK}" text-anchor="middle">{esc(line)}</text>')
        o.append(f'<text x="{cx:.3f}" y="{cy + len(lines)/2*fs*1.2:.3f}" {font} font-size="{fs*0.9:.2f}" fill="{INK}" text-anchor="middle">{area:.2f} m²</text>')
        if spec.get("show_room_dims", True):
            o.append(f'<text x="{cx:.3f}" y="{cy + (len(lines)/2+1)*fs*1.2:.3f}" {font} font-size="{fs*0.7:.2f}" fill="#555" text-anchor="middle">{r["w"]:.0f} × {r["h"]:.0f}</text>')

    # dimension chains
    o += dims(spec, P, k, t, W, H, font)

    # title block
    warns, tot = check(spec)
    o.append(f'<text x="{MARGIN}" y="{MARGIN+4}" {font} font-size="7" font-weight="300" letter-spacing="1.2" fill="#1C1814">{esc(spec["name"].upper())}</text>')
    sub = spec.get("subtitle", "")
    o.append(f'<text x="{MARGIN}" y="{MARGIN+11}" {font} font-size="3.6" fill="{ACCENT}">{esc(sub)}</text>')
    info = f'GIA {tot["gia"]:.1f} m² · net room area {tot["net"]:.1f} m² · external {Wext/1000:.2f} × {Hext/1000:.2f} m · scale 1:{s} @ A3'
    o.append(f'<text x="{PAPER_W-MARGIN}" y="{MARGIN+4}" {font} font-size="3" fill="{INK}" text-anchor="end">{info}</text>')
    o.append(f'<text x="{PAPER_W-MARGIN}" y="{MARGIN+9}" {font} font-size="2.4" fill="#666" text-anchor="end">All dimensions in mm. Clear internal room sizes. Do not scale from screen.</text>')
    o += scalebar(PAPER_W - MARGIN - 5 * 1000 / s - 14, PAPER_H - MARGIN + 2, s, font)
    o += north(MARGIN + 6, PAPER_H - MARGIN - 4, spec.get("north_deg", 0))
    o.append("</svg>")
    return "\n".join(o), warns, tot, s


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;")


def door(d, P, k, t):
    """d: {room-edge wall: 'h' or 'v', x, y (hinge, internal coords), width, swing: +1/-1, gap: wall thickness}"""
    x, y, w = d["x"], d["y"], d["width"]
    g = d.get("wall", 100)
    sw = d.get("swing", 1)
    out = []
    if d["orient"] == "h":
        a, b = P(x, y - g / 2 if not d.get("external") else y - t / 2)
        th = (t if d.get("external") else g)
        px, py = P(x, y)
        out.append(f'<rect x="{px:.3f}" y="{py - th*k/2 - 0.05:.3f}" width="{w*k:.3f}" height="{th*k + 0.1:.3f}" fill="#EFE6D6"/>')
        ex, ey = P(x, y + sw * w)
        out.append(f'<line x1="{px:.3f}" y1="{py:.3f}" x2="{ex:.3f}" y2="{ey:.3f}" stroke="{INK}" stroke-width="0.25"/>')
        fx, fy = P(x + w, y)
        sweep = 0 if sw > 0 else 1
        out.append(f'<path d="M{ex:.3f} {ey:.3f} A{w*k:.3f} {w*k:.3f} 0 0 {sweep} {fx:.3f} {fy:.3f}" fill="none" stroke="#777" stroke-width="0.15"/>')
    else:
        th = (t if d.get("external") else g)
        px, py = P(x, y)
        out.append(f'<rect x="{px - th*k/2 - 0.05:.3f}" y="{py:.3f}" width="{th*k + 0.1:.3f}" height="{w*k:.3f}" fill="#EFE6D6"/>')
        ex, ey = P(x + sw * w, y)
        out.append(f'<line x1="{px:.3f}" y1="{py:.3f}" x2="{ex:.3f}" y2="{ey:.3f}" stroke="{INK}" stroke-width="0.25"/>')
        fx, fy = P(x, y + w)
        sweep = 1 if sw > 0 else 0
        out.append(f'<path d="M{ex:.3f} {ey:.3f} A{w*k:.3f} {w*k:.3f} 0 0 {sweep} {fx:.3f} {fy:.3f}" fill="none" stroke="#777" stroke-width="0.15"/>')
    return out


def window(w, P, k, t, W, H):
    side, a, L = w["side"], w["from"], w["width"]
    out = []
    if side in ("top", "bottom"):
        y = -t if side == "top" else H
        px, py = P(a, y)
        out.append(f'<rect x="{px:.3f}" y="{py:.3f}" width="{L*k:.3f}" height="{t*k:.3f}" fill="#FFFFFF"/>')
        for f in (0.2, 0.5, 0.8):
            out.append(f'<line x1="{px:.3f}" y1="{py + t*k*f:.3f}" x2="{px + L*k:.3f}" y2="{py + t*k*f:.3f}" stroke="#6E9BB8" stroke-width="0.2"/>')
    else:
        x = -t if side == "left" else W
        px, py = P(x, a)
        out.append(f'<rect x="{px:.3f}" y="{py:.3f}" width="{t*k:.3f}" height="{L*k:.3f}" fill="#FFFFFF"/>')
        for f in (0.2, 0.5, 0.8):
            out.append(f'<line x1="{px + t*k*f:.3f}" y1="{py:.3f}" x2="{px + t*k*f:.3f}" y2="{py + L*k:.3f}" stroke="#6E9BB8" stroke-width="0.2"/>')
    return out


def furniture(f, P, k):
    kind, x, y, w, h = f["type"], f["x"], f["y"], f["w"], f["h"]
    px, py = P(x, y); ww, hh = w * k, h * k
    st = 'stroke="#8F8A82" stroke-width="0.15"'
    if kind == "bed":
        return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" rx="0.4" fill="#F6F2EA" {st}/>',
                f'<rect x="{px+0.3:.3f}" y="{py + hh*0.3:.3f}" width="{ww-0.6:.3f}" height="{hh*0.68:.3f}" rx="0.3" fill="#7F8F69"/>']
    if kind == "sofa":
        return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" rx="0.8" fill="#EEE8DE" {st}/>']
    if kind == "table":
        return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" rx="0.3" fill="#E8D5B6" {st}/>']
    if kind == "kitchen":
        return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" fill="#EFE7D8" {st}/>']
    if kind == "wardrobe":
        return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" fill="#B9926A" {st}/>']
    if kind == "wc":
        return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh*0.3:.3f}" fill="#FFF" {st}/>',
                f'<ellipse cx="{px+ww/2:.3f}" cy="{py+hh*0.64:.3f}" rx="{ww*0.42:.3f}" ry="{hh*0.34:.3f}" fill="#FFF" {st}/>']
    if kind in ("basin", "sink"):
        return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" rx="0.3" fill="#FFF" {st}/>',
                f'<ellipse cx="{px+ww/2:.3f}" cy="{py+hh/2:.3f}" rx="{ww*0.3:.3f}" ry="{hh*0.28:.3f}" fill="#E4E8EA"/>']
    if kind == "shower":
        return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" fill="#E1E4E6" {st}/>',
                f'<path d="M{px:.3f} {py:.3f}L{px+ww:.3f} {py+hh:.3f}M{px+ww:.3f} {py:.3f}L{px:.3f} {py+hh:.3f}" {st}/>']
    if kind == "bath":
        return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" rx="1.2" fill="#FFF" {st}/>']
    if kind == "stairs":
        n = max(3, int(round((h if h > w else w) / 250)))
        out = [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" fill="#E7D7BC" {st}/>']
        for i in range(1, n):
            if h > w:
                out.append(f'<line x1="{px:.3f}" y1="{py + hh*i/n:.3f}" x2="{px+ww:.3f}" y2="{py + hh*i/n:.3f}" {st}/>')
            else:
                out.append(f'<line x1="{px + ww*i/n:.3f}" y1="{py:.3f}" x2="{px + ww*i/n:.3f}" y2="{py+hh:.3f}" {st}/>')
        return out
    return [f'<rect x="{px:.3f}" y="{py:.3f}" width="{ww:.3f}" height="{hh:.3f}" fill="#DDD" {st}/>']


def dim_line(x1, y1, x2, y2, label, font, horiz=True):
    out = [f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="#333" stroke-width="0.18"/>']
    for (x, y) in ((x1, y1), (x2, y2)):
        out.append(f'<line x1="{x-0.8:.3f}" y1="{y+0.8:.3f}" x2="{x+0.8:.3f}" y2="{y-0.8:.3f}" stroke="#333" stroke-width="0.3"/>')
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if horiz:
        out.append(f'<text x="{mx:.3f}" y="{my-0.8:.3f}" {font} font-size="2.2" fill="#222" text-anchor="middle">{label}</text>')
    else:
        out.append(f'<text x="{mx-0.8:.3f}" y="{my:.3f}" {font} font-size="2.2" fill="#222" text-anchor="middle" transform="rotate(-90 {mx-0.8:.3f} {my:.3f})">{label}</text>')
    return out


def dims(spec, P, k, t, W, H, font):
    out = []
    # overall external
    ax, ay = P(-t, -t); bx, by = P(W + t, H + t)
    out += dim_line(ax, ay - 12, bx, ay - 12, f"{W + 2*t:,.0f}".replace(",", " "), font)
    out += dim_line(ax - 12, ay, ax - 12, by, f"{H + 2*t:,.0f}".replace(",", " "), font, horiz=False)
    for xx in (ax, bx):
        out.append(f'<line x1="{xx:.3f}" y1="{ay-13.5:.3f}" x2="{xx:.3f}" y2="{ay-1:.3f}" stroke="#999" stroke-width="0.1"/>')
    for yy in (ay, by):
        out.append(f'<line x1="{ax-13.5:.3f}" y1="{yy:.3f}" x2="{ax-1:.3f}" y2="{yy:.3f}" stroke="#999" stroke-width="0.1"/>')
    # internal chain along the top: room edges touching the top inner face
    xs = sorted({0, W} | {r["x"] for r in spec["rooms"] if r["y"] < 1} | {r["x"] + r["w"] for r in spec["rooms"] if r["y"] < 1})
    xs = [-t] + xs + [W + t]
    for a, b in zip(xs, xs[1:]):
        if b - a < 1:
            continue
        p1, _ = P(a, 0); p2, _ = P(b, 0)
        out += dim_line(p1, ay - 6, p2, ay - 6, f"{b-a:.0f}", font)
    ys = sorted({0, H} | {r["y"] for r in spec["rooms"] if r["x"] < 1} | {r["y"] + r["h"] for r in spec["rooms"] if r["x"] < 1})
    ys = [-t] + ys + [H + t]
    for a, b in zip(ys, ys[1:]):
        if b - a < 1:
            continue
        _, q1 = P(0, a); _, q2 = P(0, b)
        out += dim_line(ax - 6, q1, ax - 6, q2, f"{b-a:.0f}", font, horiz=False)
    return out


def scalebar(x, y, s, font):
    out = []
    seg = 1000 / s  # 1 m on paper
    for i in range(5):
        fill = "#1F1F1F" if i % 2 == 0 else "#FFFFFF"
        out.append(f'<rect x="{x + i*seg:.3f}" y="{y-2:.3f}" width="{seg:.3f}" height="1.4" fill="{fill}" stroke="#1F1F1F" stroke-width="0.15"/>')
    out.append(f'<text x="{x:.3f}" y="{y+2:.3f}" {font} font-size="2.2" fill="#222">0</text>')
    out.append(f'<text x="{x + 5*seg:.3f}" y="{y+2:.3f}" {font} font-size="2.2" fill="#222" text-anchor="middle">5 m</text>')
    out.append(f'<text x="{x + 5*seg + 4:.3f}" y="{y-0.6:.3f}" {font} font-size="2.2" fill="#222">1:{s}</text>')
    return out


def north(x, y, deg):
    return [f'<g transform="rotate({deg} {x} {y})"><path d="M{x} {y-6} L{x+2.2} {y+2} L{x} {y} L{x-2.2} {y+2} Z" fill="#1F1F1F"/></g>',
            f'<text x="{x}" y="{y+6}" font-family="Inter, Arial" font-size="2.6" text-anchor="middle">N</text>']


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    s, warns, tot, scale = svg(spec)
    open(out + ".svg", "w").write(s)
    print(json.dumps({"svg": out + ".svg", "scale": f"1:{scale}", "gia_m2": round(tot["gia"], 2),
                      "net_room_area_m2": round(tot["net"], 2), "gea_m2": round(tot["gea"], 2),
                      "warnings": warns}, ensure_ascii=False, indent=1))
