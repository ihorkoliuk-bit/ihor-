# Spec format

All lengths in millimetres. Origin (0, 0) is the inside face of the top-left external wall; x to the right, y down.

## Floor plan (`plan.py`)

```json
{
  "name": "Lake House",
  "subtitle": "2 bedrooms + study · single storey",
  "internal": {"w": 13400, "h": 7400},      // clear internal envelope
  "wall_ext": 300,                           // external wall thickness
  "declared_area": 92.0,                     // optional: catalogue figure to check against
  "scale": 100,                              // optional: force 1:50 / 1:100 / 1:200
  "north_deg": 0,                            // optional: rotation of the north arrow
  "show_room_dims": true,
  "rooms": [
    {"name": "Kitchen / Living\nDining", "x": 0, "y": 0, "w": 3520, "h": 7400,
     "floor": "wood", "label_at": [1300, 3500]}
  ],
  "doors": [
    {"orient": "h", "x": 3900, "y": 7550, "width": 1000, "swing": -1, "external": true},
    {"orient": "v", "x": 3570, "y": 3600, "width": 900, "swing": -1}
  ],
  "windows": [{"side": "top", "from": 500, "width": 1800}],
  "furniture": [{"type": "bed", "x": 7200, "y": 300, "w": 1600, "h": 2000}]
}
```

- **rooms**: clear rectangles. Leave the partition thickness (normally 100) as a gap between neighbours; overlapping rooms are rejected. L-shaped rooms: split them into two rectangles with no gap between them, the same `floor`, and the name on the larger part (give the other part `"name": ""` and it gets no label). Its area is reported in the total but not on the sheet, so state the combined area in the room name if it matters.
- **floor**: `wood`, `tile` (gridded 300 mm), `stone`, `carpet`, `ext`.
- **doors**: `orient` is the wall direction — `h` for a horizontal wall, `v` for a vertical one. `x, y` is the hinge point on the wall centre line (for a 100 mm partition between rooms ending at y=3400 and starting at y=3500, use y=3450). `swing` +1 opens towards +y (h) or +x (v). `external: true` uses the external wall thickness (y = internal height + wall/2 for the bottom wall, −wall/2 for the top).
- **windows**: `side` top/bottom/left/right, `from` offset along that wall from the origin, `width`.
- **furniture types**: bed, sofa, table, kitchen, wardrobe, wc, basin, shower, bath, stairs. Use real sizes: double bed 1500×2000, king 1600×2000, single 900×2000, WC 400×650, basin 550×450, shower 900×900, bath 1700×750, kitchen run depth 600.

## Elevations (`elevation.py`)

```json
{
  "name": "Lake House",
  "elevations": [
    {"name": "Gable elevation (garden)", "width": 8000, "eaves": 2700, "ridge": 5900,
     "roof": "gable-front",          // or "eaves-front" for the long side
     "wall": "dark-timber", "gable_fill": "timber", "roof_mat": "metal",
     "plinth": 450, "overhang": 250,
     "bands": [{"x": 0, "w": 1200, "from": 450, "to": 2700, "mat": "dark-timber"}],
     "openings": [
       {"x": 800, "sill": 450, "w": 6400, "h": 2250, "panes": 4},
       {"x": 1400, "sill": 2900, "w": 5200, "h": 2300, "gable": true},
       {"x": 3900, "sill": 450, "w": 1000, "h": 2100, "type": "door"}
     ]}
  ]
}
```

Materials: brick, timber, dark-timber, render, stone, metal, tile, glass, door. Heights are above finished floor level; `width` is the external width of that face.
