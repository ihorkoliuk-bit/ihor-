---
name: zon-building-performance
description: Early-stage energy and comfort engineering for new UK homes — wall/roof/floor U-values from layer build-ups, room-by-room design heat loss and air-source heat pump sizing, PV yield, Part L 2021 limiting/notional checks, Future Homes Standard (from 24 March 2027) implications, Part O overheating risk from glazing, and ventilation (dMEV/MVHR). Use this whenever the user asks how warm, efficient or cheap to run a ZON house will be, what insulation or wall build-up to use, what size heat pump or solar array, whether big glazed gables cause overheating, what "Zero Bills" or EPC rating is realistic, or wants energy claims for marketing checked — including "енергоефективність", "тепловий насос", "сонячні панелі", "утеплення".
---

# Building performance (energy, heat, comfort)

The point is to make design and marketing claims that survive SAP, the MCS installer and the Advertising Standards Authority. Early numbers from this skill steer the design; compliance comes from an accredited SAP / Home Energy Model assessor and an MCS-certified installer.

## Workflow

1. **Fabric.** For each element write the layers (thickness, conductivity λ; bridged stud layers with timber fraction 0.12–0.18) and run `python3 scripts/energy.py uvalue element.json`. Compare with targets below.
2. **Heat loss.** Build a room list from the plan (areas, volumes, external wall/window/roof/floor areas with U-values, design temps 21 °C living, 18 °C bedrooms, 22 °C bathrooms; external −2 °C for Essex unless the MCS design temperature for the postcode differs) and run `python3 scripts/energy.py heatloss house.json`. Well-insulated new homes typically land at 20–35 W/m².
3. **Heat pump.** Size from the total plus a hot-water allowance; small homes often suit 4–5 kW units (smallest common sizes), so the controlling factor is noise, siting (MCS 020 / permitted development distance rules) and hot-water cylinder space.
4. **PV.** kWp × ~950 kWh/kWp/year for south-facing roofs in East Anglia (≈ 800 east/west). Say what share of annual use it covers, never "zero bills" unless a tariff product guarantees it.
5. **Overheating (Part O).** Large south/west glazing (glazed gables) raises risk; the simplified method caps glazing as a % of floor area and requires openable area for purge ventilation; otherwise dynamic (TM59) modelling. Flag it at concept stage — it can force smaller glass, shading or brise-soleil.
6. **Report** U-values vs targets, heat loss by room, heat pump and PV sizes, overheating risk, and the claims that are safe to put in a deck.

## Targets

| Element | Part L 2021 limit | Part L 2021 notional | Good FHS-ready practice |
|---|---|---|---|
| External wall | 0.26 | 0.18 | 0.15–0.18 |
| Roof | 0.16 | 0.11 | 0.10–0.11 |
| Ground floor | 0.18 | 0.13 | 0.11–0.13 |
| Windows | 1.6 | 1.2 | 0.8–1.2 (triple ~0.8) |
| Air permeability | 8 m³/h·m² @50 Pa | 5 | 3 or below with MVHR |

Future Homes Standard: in force for new dwellings in England from 24 March 2027 with a transitional period for sites already commenced (check the regulations for the cut-off). It makes low-carbon heating (heat pumps) the default and expects on-site PV; gas boilers are effectively ruled out. Designs starting now should assume FHS.

## Marketing claims

Safe: "air-source heat pump, solar PV and high insulation designed to keep running costs low", "EPC B/A expected (subject to SAP)". Unsafe without proof: "zero bills", "fully autonomous", "net zero home" (a product name — Octopus "Zero Bills" — and an ASA risk).
