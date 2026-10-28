---
name: zon-architectural-drawings
description: Produce dimensionally accurate house floor plans and elevations (true scale 1:50/1:100 on A3, PDF + PNG), check room areas against the declared GIA and UK space standards (NDSS, M4(2)), and write render briefs that keep image-generator renders consistent with the drawings. Use this whenever the user wants to draw, redraw, unify the style of, or check a floor plan, layout, elevation or façade of a house or bungalow; turns a sketch, catalogue plan, 3D cutaway or list of room sizes into a measured drawing; asks whether areas add up; or wants renders/visualisations of a house "with architectural accuracy" — even if they just say "make the plan nicer", "planning", "планування", "фасад", "рендер" or send a photo of a plan.
---

# ZON architectural drawings

Turn whatever the user has (catalogue plan, photo of a sketch, 3D cutaway, list of rooms) into measured drawings that a QS, planner or investor can trust, and give the render tool the geometry it needs so renders match the drawings.

What this skill can and cannot do — say it to the user up front when they ask for "renders":
- It **draws** plans and elevations from millimetre dimensions, to true scale, with every area computed from the geometry. That is the "architectural accuracy" part.
- It **does not generate photoreal renders**. It writes a render brief and supplies the elevation PNG as a reference image for Midjourney / Flux / D5 / Enscape, so proportions, window positions and roof pitch come from the drawing instead of the model's imagination.
- It is not a substitute for an architect's planning or Building Regulations drawings. Every sheet says "do not scale from screen"; final drawings come from the architect's CAD.

## Workflow

### 1. Collect the geometry (in mm)

You need, per floor:
- **External envelope** and **external wall thickness** (default 300 mm for timber-frame/SIP with cladding; ask if masonry, ~350 mm).
- **Rooms as clear internal rectangles**: name, x, y, width, height, measured from the inside face of the top-left external wall. Internal partitions are the gaps between rooms (default 100 mm).
- Doors (position, width, swing), windows (wall side, offset, width), stairs, sanitaryware and furniture if wanted.

Where these come from:
- A dimensioned catalogue plan: read the overall dimensions and room areas off it.
- A plan with areas but no room dimensions: derive widths from area ÷ depth, keeping the grid that the plan shows.
- A 3D cutaway or photo with no numbers: you can reproduce the layout, but **every size is a guess**. Draw it, label it "indicative layout — dimensions to be confirmed", and ask for the real sizes. Never present guessed sizes as measured.

### 2. Reconcile before drawing

Check, and tell the user plainly, before you polish anything:
- Do the room areas plus partitions fit inside the envelope? Internal GIA = (external length − 2 × wall) × (external width − 2 × wall). Partitions and voids normally take 5–10 % of GIA.
- Does the declared catalogue area match the drawn GIA? More than ~3 % apart means one of them is wrong. Example from this project: the 2-bed house listed as 9 × 7.5 m had rooms summing to 70.5 m², more than the whole 67.5 m² footprint — impossible, so the dimensions or the areas needed correcting.
- Is the declared area GIA, NIA, or including garage/terraces? Catalogue figures often include them (e.g. "317 m²" that was 170 m² living + garage + terraces). Investors and valuers need GIA of the habitable space.
- NDSS minimums and room rules: see `references/uk-standards.md`.

`plan.py` prints GIA, net room area, GEA and warnings; use them in your reply.

### 3. Draw

Write a spec JSON (see `references/spec-format.md`, and the worked example in `examples/lake-house.plan.json`), then:

```bash
python3 scripts/plan.py spec.json out/house-ground   # -> .svg + JSON report on stdout
python3 scripts/render.py out/house-ground.svg       # -> .pdf (true scale A3) + .png
python3 scripts/elevation.py elev.json out/house-elev && python3 scripts/render.py out/house-elev.svg
```

The scale is chosen automatically (1:50, then 1:100, 1:200) to fit A3; force it with `"scale": 100` when several sheets must match. For two-storey houses draw one spec per floor with the same envelope and the stair in the same place.

Look at the PNG before sending it. Move labels with `label_at` when they sit on furniture, and check that doors open into rooms, not into walls.

### 4. Elevations and renders

Elevations need eaves height, ridge height, plinth, roof type and every opening with sill and head heights. Pitch is computed from eaves, ridge and gable width and printed on the sheet, so check it is plausible (single-storey barnhouse roofs are often 35–45°).

For renders, follow `references/render-brief.md`: one brief per view, with the dimensions, materials and openings from the drawings, and the elevation PNG attached as a reference/control image.

### 5. Deliver

Send the PDF (for print, true scale) and PNG (for decks). In the reply give: scale, GIA, any mismatch you found, and which sizes are confirmed vs assumed. Keep the spec JSON next to the drawings so the next revision is a one-line change.

## Style

The default palette matches the ZON investor deck (warm oak floors, grey tiled wet rooms, near-black walls, Inter type, copper accent). Room labels show name, area to 0.01 m² and clear size in mm. English labels unless the user asks otherwise.
