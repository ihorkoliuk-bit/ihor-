#!/usr/bin/env python3
"""Render an A3 SVG drawing to PDF (true scale) and PNG with headless Chromium.

Usage: python3 render.py drawing.svg [--png-dpi 200]
Writes drawing.pdf and drawing.png next to the SVG.
"""
import os, shutil, subprocess, sys, tempfile

def chrome():
    for c in ("/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "chromium", "chromium-browser", "google-chrome"):
        p = c if os.path.isabs(c) and os.path.exists(c) else shutil.which(c)
        if p:
            return p
    import glob
    hits = glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")
    if hits:
        return hits[0]
    sys.exit("render.py: no Chromium found")

def main():
    svg = os.path.abspath(sys.argv[1])
    dpi = int(sys.argv[sys.argv.index("--png-dpi") + 1]) if "--png-dpi" in sys.argv else 200
    base = svg[:-4]
    html = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False)
    html.write('<!doctype html><html><head><meta charset="utf-8"><style>@page{size:420mm 297mm;margin:0}'
               'html,body{margin:0;padding:0}img{display:block;width:420mm;height:297mm}</style></head>'
               f'<body><img src="file://{svg}"></body></html>')
    html.close()
    c = chrome()
    subprocess.run([c, "--headless", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                    "--no-pdf-header-footer", f"--print-to-pdf={base}.pdf", "file://" + html.name],
                   check=True, capture_output=True)
    # PNG from the PDF so both are identical and nothing is clipped
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", base + ".pdf", base], check=True)
    os.unlink(html.name)
    print(base + ".pdf\n" + base + ".png")

if __name__ == "__main__":
    main()
