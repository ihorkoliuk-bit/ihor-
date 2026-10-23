import sys, json
S = 100  # px per metre
M = 1.6  # margin metres
def svg(spec):
    W, H = spec["w"], spec["h"]
    vw, vh = (W + 2*M)*S, (H + 2*M + 0.5)*S
    o = []
    X = lambda x: (x+M)*S
    Y = lambda y: (y+M+0.5)*S
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{vw:.0f}" height="{vh:.0f}" viewBox="0 0 {vw:.0f} {vh:.0f}">')
    o.append('''<defs>
<pattern id="wood" width="120" height="16" patternUnits="userSpaceOnUse"><rect width="120" height="16" fill="#D9BC93"/><path d="M0 15.5H120" stroke="#C5A57A" stroke-width="1"/><path d="M60 0V16" stroke="#C9AA80" stroke-width="1"/></pattern>
<pattern id="wood2" width="120" height="16" patternUnits="userSpaceOnUse" x="60" y="8"><rect width="120" height="16" fill="#D3B48A"/><path d="M0 15.5H120" stroke="#C09F74" stroke-width="1"/><path d="M30 0V16" stroke="#C4A479" stroke-width="1"/></pattern>
<pattern id="tile" width="30" height="30" patternUnits="userSpaceOnUse"><rect width="30" height="30" fill="#C3C6C8"/><path d="M0 29.5H30M29.5 0V30" stroke="#AEB2B5" stroke-width="1"/></pattern>
<pattern id="mat" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#E7DED2"/><circle cx="4" cy="4" r="1.2" fill="#D6CBBC"/></pattern>
</defs>''')
    o.append(f'<rect width="{vw:.0f}" height="{vh:.0f}" fill="#FFFFFF"/>')
    # floors
    for r in spec["rooms"]:
        x,y,w,h = r["r"]; fill = "url(#tile)" if r.get("t")=="tile" else ("url(#wood2)" if r.get("t")=="wood2" else "url(#wood)")
        o.append(f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" fill="{fill}"/>')
    # furniture
    for f in spec.get("furn", []):
        k = f[0]; x,y,w,h = f[1:5]; ex = f[5] if len(f)>5 else {}
        x0,y0,ww,hh = X(x),Y(y),w*S,h*S
        if k=="bed":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" rx="6" fill="#F4F0E8" stroke="#BFB6A8" stroke-width="2"/>')
            # blanket covering lower 60% along long axis
            if ex.get("head")=="right":
                o.append(f'<rect x="{x0}" y="{y0+3}" width="{ww*0.62}" height="{hh-6}" rx="4" fill="#7A8C64"/>')
                for i in (0.28,0.72):
                    o.append(f'<rect x="{x0+ww*0.8}" y="{y0+hh*i-hh*0.18}" width="{ww*0.15}" height="{hh*0.36}" rx="6" fill="#FFFFFF" stroke="#CFC6B8"/>')
            elif ex.get("head")=="left":
                o.append(f'<rect x="{x0+ww*0.38}" y="{y0+3}" width="{ww*0.62}" height="{hh-6}" rx="4" fill="#7A8C64"/>')
                for i in (0.28,0.72):
                    o.append(f'<rect x="{x0+ww*0.05}" y="{y0+hh*i-hh*0.18}" width="{ww*0.15}" height="{hh*0.36}" rx="6" fill="#FFFFFF" stroke="#CFC6B8"/>')
            else:  # head top
                o.append(f'<rect x="{x0+3}" y="{y0+hh*0.38}" width="{ww-6}" height="{hh*0.62}" rx="4" fill="#7A8C64"/>')
                for i in (0.28,0.72):
                    o.append(f'<rect x="{x0+ww*i-ww*0.18}" y="{y0+hh*0.05}" width="{ww*0.36}" height="{hh*0.15}" rx="6" fill="#FFFFFF" stroke="#CFC6B8"/>')
        elif k=="sofa":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" rx="10" fill="#EDE7DD" stroke="#C9BFAF" stroke-width="2"/>')
            o.append(f'<rect x="{x0+12}" y="{y0+12}" width="{ww-24}" height="{hh-24}" rx="8" fill="#F5F1EA" stroke="#D8CFC2"/>')
        elif k=="rug":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" fill="url(#mat)"/>')
        elif k=="table":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" rx="4" fill="#E9D7B9" stroke="#B89A70" stroke-width="2"/>')
            n = ex.get("chairs",2)
            for i in range(n):
                cx = x0 + ww*(i+0.5)/n - 18
                o.append(f'<rect x="{cx}" y="{y0-34}" width="36" height="28" rx="8" fill="#8A6A4A"/>')
                o.append(f'<rect x="{cx}" y="{y0+hh+6}" width="36" height="28" rx="8" fill="#8A6A4A"/>')
        elif k=="round":
            o.append(f'<circle cx="{x0+ww/2}" cy="{y0+hh/2}" r="{ww/2}" fill="#A8794D" stroke="#7E5835" stroke-width="2"/>')
        elif k=="kitchen":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" fill="#EFE6D6" stroke="#B9AA92" stroke-width="2"/>')
            if ww>hh:
                o.append(f'<rect x="{x0+ww*0.25}" y="{y0+hh*0.18}" width="{hh*0.9}" height="{hh*0.64}" rx="6" fill="#9EA3A6"/>')
                o.append(f'<rect x="{x0+ww*0.55}" y="{y0+hh*0.12}" width="{hh*1.0}" height="{hh*0.76}" fill="#2E2E2E"/>')
            else:
                o.append(f'<rect x="{x0+ww*0.18}" y="{y0+hh*0.25}" width="{ww*0.64}" height="{ww*0.9}" rx="6" fill="#9EA3A6"/>')
                o.append(f'<rect x="{x0+ww*0.12}" y="{y0+hh*0.55}" width="{ww*0.76}" height="{ww*1.0}" fill="#2E2E2E"/>')
        elif k=="wardrobe":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" fill="#B38A5E" stroke="#8C6640" stroke-width="2"/>')
        elif k=="desk":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" fill="#C69C6D" stroke="#8C6640" stroke-width="2"/>')
            o.append(f'<circle cx="{x0+ww/2}" cy="{y0+hh+28}" r="22" fill="#5C5650"/>')
        elif k=="wc":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh*0.3}" rx="4" fill="#FFFFFF" stroke="#9AA0A4" stroke-width="2"/>')
            o.append(f'<ellipse cx="{x0+ww/2}" cy="{y0+hh*0.62}" rx="{ww*0.42}" ry="{hh*0.36}" fill="#FFFFFF" stroke="#9AA0A4" stroke-width="2"/>')
        elif k=="shower":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" fill="#D7DBDD" stroke="#9AA0A4" stroke-width="2"/>')
            o.append(f'<path d="M{x0} {y0}L{x0+ww} {y0+hh}M{x0+ww} {y0}L{x0} {y0+hh}" stroke="#AEB4B8" stroke-width="1.5"/>')
        elif k=="bath":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" rx="18" fill="#FFFFFF" stroke="#9AA0A4" stroke-width="2"/>')
            o.append(f'<rect x="{x0+12}" y="{y0+12}" width="{ww-24}" height="{hh-24}" rx="14" fill="#EEF1F2"/>')
        elif k=="sink":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" rx="6" fill="#FFFFFF" stroke="#9AA0A4" stroke-width="2"/>')
            o.append(f'<ellipse cx="{x0+ww/2}" cy="{y0+hh/2}" rx="{ww*0.3}" ry="{hh*0.28}" fill="#E3E7E9"/>')
        elif k=="washer":
            o.append(f'<rect x="{x0}" y="{y0}" width="{ww}" height="{hh}" rx="4" fill="#FFFFFF" stroke="#9AA0A4" stroke-width="2"/>')
            o.append(f'<circle cx="{x0+ww/2}" cy="{y0+hh/2}" r="{min(ww,hh)*0.3}" fill="#5D6266"/>')
        elif k=="plant":
            for a in range(8):
                import math
                ang = a*math.pi/4
                o.append(f'<ellipse cx="{x0+ww/2+math.cos(ang)*ww*0.22}" cy="{y0+hh/2+math.sin(ang)*hh*0.22}" rx="{ww*0.22}" ry="{hh*0.1}" transform="rotate({a*45} {x0+ww/2+math.cos(ang)*ww*0.22} {y0+hh/2+math.sin(ang)*hh*0.22})" fill="#5E7F4A"/>')
    # internal walls (room outlines)
    for r in spec["rooms"]:
        x,y,w,h = r["r"]
        o.append(f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" fill="none" stroke="#2B2B2B" stroke-width="12"/>')
    # exterior wall
    o.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{W*S}" height="{H*S}" fill="none" stroke="#2B2B2B" stroke-width="30"/>')
    for nx,ny,nw,nh in spec.get("cut", []):
        o.append(f'<rect x="{X(nx)}" y="{Y(ny)}" width="{nw*S}" height="{nh*S+20}" fill="#FFFFFF"/>')
        o.append(f'<path d="M{X(nx)} {Y(ny+nh)+15} V{Y(ny)} H{X(nx+nw)} V{Y(ny+nh)+15}" fill="none" stroke="#2B2B2B" stroke-width="30"/>')
    # windows: (side, start, length)
    for side, a, L in spec.get("windows", []):
        if side in "tb":
            yy = Y(0) if side=="t" else Y(H)
            o.append(f'<rect x="{X(a)}" y="{yy-16}" width="{L*S}" height="32" fill="#FFFFFF"/>')
            for d in (-8,0,8): o.append(f'<line x1="{X(a)}" y1="{yy+d}" x2="{X(a+L)}" y2="{yy+d}" stroke="#7FA7C2" stroke-width="3"/>')
        else:
            xx = X(0) if side=="l" else X(W)
            o.append(f'<rect x="{xx-16}" y="{Y(a)}" width="32" height="{L*S}" fill="#FFFFFF"/>')
            for d in (-8,0,8): o.append(f'<line x1="{xx+d}" y1="{Y(a)}" x2="{xx+d}" y2="{Y(a+L)}" stroke="#7FA7C2" stroke-width="3"/>')
    # doors: (x,y, width, orient) orient: h = opening along x on a horizontal wall, swing dir sign; v similar
    for d in spec.get("doors", []):
        x,y,L,orient,sg = d
        if orient=="h":
            o.append(f'<rect x="{X(x)}" y="{Y(y)-17}" width="{L*S}" height="34" fill="#E9DCC6"/>')
            o.append(f'<line x1="{X(x)}" y1="{Y(y)}" x2="{X(x)}" y2="{Y(y)+sg*L*S}" stroke="#2B2B2B" stroke-width="3"/>')
            o.append(f'<path d="M{X(x)} {Y(y)+sg*L*S} A{L*S} {L*S} 0 0 {0 if sg>0 else 1} {X(x+L)} {Y(y)}" fill="none" stroke="#6B6B6B" stroke-width="2"/>')
        else:
            o.append(f'<rect x="{X(x)-17}" y="{Y(y)}" width="34" height="{L*S}" fill="#E9DCC6"/>')
            o.append(f'<line x1="{X(x)}" y1="{Y(y)}" x2="{X(x)+sg*L*S}" y2="{Y(y)}" stroke="#2B2B2B" stroke-width="3"/>')
            o.append(f'<path d="M{X(x)+sg*L*S} {Y(y)} A{L*S} {L*S} 0 0 {1 if sg>0 else 0} {X(x)} {Y(y+L)}" fill="none" stroke="#6B6B6B" stroke-width="2"/>')
    # labels
    for r in spec["rooms"]:
        x,y,w,h = r["r"]; lx, ly = r.get("lp",(x+w/2, y+h/2))
        name, area = r["n"], r["a"]
        lines = name.split("\n")
        fs = r.get("fs", 30)
        for i,l in enumerate(lines):
            o.append(f'<text x="{X(lx)}" y="{Y(ly)+(i-len(lines)/2)*fs*1.15}" font-family="Inter" font-size="{fs}" font-weight="500" fill="#1F1F1F" text-anchor="middle" paint-order="stroke" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="5">{l}</text>')
        if area: o.append(f'<text x="{X(lx)}" y="{Y(ly)+(len(lines)/2)*fs*1.15+4}" font-family="Inter" font-size="{fs}" font-weight="400" fill="#1F1F1F" text-anchor="middle" paint-order="stroke" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="5">{area} m²</text>')
    # dimensions
    if spec.get("nodims"):
        o.append(f'<text x="{X(0)}" y="{0.75*S}" font-family="Inter" font-size="44" font-weight="300" letter-spacing="6" fill="#1C1814">{spec["title"]}</text>')
        o.append(f'<text x="{X(0)}" y="{1.25*S}" font-family="Inter" font-size="30" font-weight="400" fill="#8C5A3A">{spec["sub"]}</text>')
        o.append("</svg>"); return "\n".join(o)
    yy = Y(H)+1.0*S
    o.append(f'<line x1="{X(0)}" y1="{yy}" x2="{X(W)}" y2="{yy}" stroke="#333" stroke-width="2"/>')
    for xx in (X(0),X(W)): o.append(f'<line x1="{xx}" y1="{yy-14}" x2="{xx}" y2="{yy+14}" stroke="#333" stroke-width="2"/>')
    o.append(f'<rect x="{(X(0)+X(W))/2-90}" y="{yy-22}" width="180" height="44" fill="#FFFFFF"/><text x="{(X(0)+X(W))/2}" y="{yy+13}" font-family="Inter" font-size="36" text-anchor="middle" fill="#1F1F1F">{int(W*1000):,}</text>'.replace(",", " "))
    xx = X(0)-1.0*S
    o.append(f'<line x1="{xx}" y1="{Y(0)}" x2="{xx}" y2="{Y(H)}" stroke="#333" stroke-width="2"/>')
    for y2 in (Y(0),Y(H)): o.append(f'<line x1="{xx-14}" y1="{y2}" x2="{xx+14}" y2="{y2}" stroke="#333" stroke-width="2"/>')
    cy=(Y(0)+Y(H))/2
    o.append(f'<rect x="{xx-22}" y="{cy-80}" width="44" height="160" fill="#FFFFFF"/><text x="{xx}" y="{cy}" font-family="Inter" font-size="36" text-anchor="middle" fill="#1F1F1F" transform="rotate(-90 {xx} {cy})" dy="12">{int(H*1000):,}</text>'.replace(",", " "))
    # title
    o.append(f'<text x="{X(0)}" y="{0.75*S}" font-family="Inter" font-size="44" font-weight="300" letter-spacing="6" fill="#1C1814">{spec["title"]}</text>')
    o.append(f'<text x="{X(0)}" y="{1.25*S}" font-family="Inter" font-size="30" font-weight="400" fill="#8C5A3A">{spec["sub"]}</text>')
    o.append('</svg>')
    return "\n".join(o)
spec = json.load(open(sys.argv[1]))
open(sys.argv[2],"w").write(f'<!doctype html><html><body style="margin:0;background:#fff">{svg(spec)}</body></html>')
W=(spec["w"]+2*M)*S; H=(spec["h"]+2*M+0.5)*S
print(int(W), int(H))
