# Hollowlight Model Rollout

## Tier A: architectural kit

Built as modular, dimension-locked pieces. Mostly procedural geometry with a small number of authored variants.

- floor slabs
- ceiling slabs
- wall panels
- corner panels
- pillars
- beams
- door frames
- windows
- stairs
- railings
- elevator pieces
- service hatches
- vents
- ducts
- cable trays
- pipe families
- electrical cabinets
- utility panels

**Method:** Blender generators create geometry families; the C++ renderer supplies runtime material variation.

## Tier B: repeatable props

- lockers
- shelves
- crates
- bins
- carts
- tables
- chairs
- benches
- filing cabinets
- office desks
- arcade cabinets
- vending machines
- trash cans
- cleaning carts
- barriers
- signage frames
- fire extinguishers
- emergency equipment

**Method:** procedural base mesh + seeded dimensions/details + runtime materials. Only distinctive silhouettes receive bespoke meshes.

## Tier C: mechanical/environmental props

- generators
- breaker panels
- fuse boxes
- electrical transformers
- pumps
- compressors
- maintenance machines
- ventilation equipment
- security cameras
- control consoles
- ticket machines
- service terminals
- elevators and mechanisms
- amusement-ride components

**Method:** procedural construction from reusable subcomponents, followed by authored detail passes for hero machines.

## Tier D: hero props

- master control console
- central power system
- major puzzle machines
- important keys/tools
- distinctive escape-route mechanisms
- major environmental landmarks

**Method:** bespoke Blender meshes, baked detail only where justified, runtime material layer retained for variation and dirt.

## Tier E: antagonist

The antagonist is not generated as a generic prop. It gets a dedicated authored model, multiple LODs, a rig, animation set and material variants. Procedural systems may generate secondary damage/wear but never alter gameplay-critical silhouette or animation structure.

## Texture strategy by asset

| Asset class | Geometry | Base material | Unique textures |
|---|---|---|---|
| Architecture | Procedural modular | Runtime procedural | Rare |
| Common props | Procedural | Runtime procedural | Rare |
| Machines | Procedural + authored details | Runtime + masks | Sometimes |
| Hero props | Authored | Runtime + baked maps | Yes |
| Antagonist | Authored | Runtime + authored maps | Yes |

## Runtime texture families

The renderer will provide deterministic material functions for:

- concrete
- plaster
- painted metal
- galvanized metal
- rusted metal
- stainless steel
- dirty glass
- rubber
- dark wood
- painted wood
- ceramic tile
- vinyl flooring
- carpet
- plastic
- grime
- dust
- moisture
- surface scratches
- edge wear

Each material receives a seed and parameter block so identical assets can still look slightly different without duplicating texture files.

## Production order

1. Architectural kit
2. Doors/windows/locks
3. Utility infrastructure
4. Furniture/storage
5. Entertainment props
6. Office props
7. Maintenance machines
8. Puzzle machinery
9. Hero props
10. Antagonist
11. Damage/decal library
12. Final environment dressing

## Non-negotiable constraints

- gameplay collision cannot depend on decorative geometry
- generated variants preserve interaction points and bounding dimensions
- every generator has deterministic seeds
- no texture duplication for trivial color/wear differences
- triangle budgets are defined per asset family
- LODs are required where screen-space cost warrants them
- visual detail must not destroy readability in darkness
