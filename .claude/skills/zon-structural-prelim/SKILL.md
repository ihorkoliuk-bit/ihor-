---
name: zon-structural-prelim
description: Preliminary structural sizing and checks for low-rise timber-frame / modular homes — loads to Eurocode with UK National Annex, timber joist, rafter and beam sizing (bending, shear, deflection to EN 1995), strip foundation width and depth on clay with tree influence, and a list of what the structural engineer must design. Use this whenever the user asks whether a span, beam, roof, floor or foundation will work, what size members a ZON house needs, why a quote includes piles, or wants to sanity-check an engineer's or manufacturer's design — including "розрахунок", "балка", "фундамент", "проліт", "навантаження" — but always as early-stage guidance, never as the final design.
---

# Preliminary structural design

Use this to size things early enough to price them and to spot designs that will not work (a 6 m clear span in solid C24, a 3 m-deep foundation near an oak on clay). It is not a structural design. In England, Building Regulations Part A, warranty providers and lenders require calculations and drawings by a chartered structural engineer (IStructE or ICE). Every output says so; keep that line in what you send the user.

## Workflow

1. Establish the structural system: timber frame / SIPs / CLT / modular volumetric, roof type and pitch, spans, where the load-bearing walls are (use the plan from zon-architectural-drawings).
2. Loads: take characteristic values from `references/loads.md`; state the snow and wind assumptions.
3. Members: `python3 scripts/timber.py --span 4.2 --gk 0.5 --qk 1.5 --b 47 --h 220 --floor` or `--sweep` for the smallest standard depth that passes. Rafters: use the on-slope permanent load and the larger of roof imposed and snow, `--load-duration short` for snow-governed checks only if the engineer agrees; default medium.
4. Foundations: `python3 scripts/foundation.py --line-load 25 --bearing 100 --soil clay-high` plus tree data. North Essex is largely London Clay (high shrinkage) — expect ≥1.0 m strips, deeper or piled near trees. Screw piles suit lightweight timber-frame homes and are fast.
5. Report: member sizes with utilisation, foundation type and depth band, assumptions, and the engineer's scope.

## What the engineer must cover (put in the brief)

Frame and racking design (wind), roof structure incl. any glazed gable and ridge beam, lintels over large openings, first-floor structure and stair trimmers for two-storey types, connections and hold-downs, foundation design from a site investigation, drainage interaction (soakaways ≥5 m from foundations), and Part A calculations for Building Control and the warranty provider.

## Common ZON pitfalls

- Full-height glazed gables remove racking wall: needs a portal or steel/glulam frame — price it.
- Vaulted ceilings without ceiling ties need a structural ridge beam.
- Modular units: transport and lifting loads govern, not in-service loads; manufacturer's engineer designs them.
- In-roof PV and heavy tiles add permanent load; check rafters when changing roof finish.
