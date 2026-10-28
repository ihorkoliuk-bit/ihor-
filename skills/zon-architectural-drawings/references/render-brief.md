# Render brief: keeping renders true to the drawings

Image generators invent proportions unless told otherwise. A render is "architecturally accurate" only if a viewer could measure the drawing and the render and get the same answer. So the brief does two things: it states the geometry in words, and it hands the tool the elevation drawing as a reference.

## Process

1. Draw the elevation with `elevation.py` first. Export the face you want to show as PNG.
2. Write one brief per camera view using the template below. Use numbers from the drawing, never round them into adjectives ("large window" → "full-height glazing 6.4 m wide, 2.25 m high, four panes").
3. In the render tool, attach the elevation PNG:
   - Midjourney: as an image prompt plus `--iw 1.5`; use `--ar` matching the view.
   - Flux / SDXL / ComfyUI: as a ControlNet (lineart or canny) input, strength 0.6–0.8.
   - D5 / Enscape / Twinmotion: model from the plan/elevation in SketchUp first; that is the only route to a true-to-geometry render.
4. Check the result against the drawing: count windows, compare ridge-to-eaves ratio, door position, cladding bands. Reject renders that add storeys, dormers, chimneys or extra windows.
5. Label every image "CGI — indicative" in investor material.

## Template

```
Photorealistic architectural exterior, [time of day], [season], eye-level camera at 1.6 m, [lens 24/35 mm], view from [garden / street / 45° corner].
Building: [single-storey / two-storey] [house type], external footprint [L] × [W] m, [roof type] roof at [pitch]° pitch, eaves +[eaves] mm, ridge +[ridge] mm, [overhang] mm overhang.
Walls: [material and colour by zone, e.g. vertical charred timber cladding full height on the corners, natural oak vertical boarding between], [plinth height and material].
Roof: [standing-seam black metal / dark slate tiles], [flush in-roof PV on the south slope if any].
Openings on this face (left to right): [list each with width × height and sill height].
Site: [English oak and silver birch, hornbeam hedges, permeable light paving]. No lake, river or pond unless on the site plan. No other buildings closer than [x] m. No skyscrapers or city skyline.
Style: natural light, realistic materials, no people, no text, no logos.
Negative: extra storey, dormer, chimney, balcony, extra windows, curved walls, distorted proportions, city background.
```

Fill everything in square brackets from the drawings; delete lines that do not apply. Keep the negative line: it removes the things generators add most often.
