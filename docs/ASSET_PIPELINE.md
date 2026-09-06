# Hollowlight Asset Pipeline

## Asset philosophy

Use three tiers instead of hand-authoring everything:

1. **Runtime procedural materials** for high-volume surfaces: concrete, painted drywall, dirty plaster, rubber, metal, glass, tile, wood, grime and wetness. Material parameters are seedable and generated from compact data rather than storing thousands of texture files.
2. **Blender procedural geometry** for reusable structural/prop families: doors, frames, lockers, pipes, cable trays, ducts, lights, furniture, crates, machines and architectural modules. One generator produces many deterministic variants.
3. **Hand-shaped hero meshes** only where silhouette, animation or narrative importance justifies the cost: antagonist, major machines, distinctive landmarks, key props and puzzle-specific objects.

## Geometry rules

- Real-world scale in meters.
- Apply transforms before export.
- Separate collision geometry from render geometry.
- Prefer modular dimensions based on a common 0.25 m grid.
- Keep origin placement intentional: hinges at door hinges, prop bases on floor, machinery at its interaction point.
- Generate clean UVs for assets that need baked detail; otherwise allow runtime material coordinates.
- LODs are generated for medium/high-poly families where useful.
- No unique mesh for trivial variation. Variation belongs in parameters.

## Texture rules

### Runtime generated

Use shader parameters/noise for:
- base color variation
- roughness variation
- micro-normal detail
- dirt/grime masks
- edge wear masks
- stains
- subtle moisture
- emissive variation

These should remain cheap enough for the 850M target. Large-scale baked textures are reserved for assets where procedural shading cannot reproduce the required appearance.

### Baked/generated files

Use Blender-generated texture atlases only for:
- hero assets
- complex baked normals/AO
- decals requiring authored composition
- assets whose material appearance must remain identical across machines

## Folder layout

```text
assets/
  generated/
    meshes/
    textures/
    materials/
    manifests/
  authored/
  audio/
  decals/
tools/
  blender/
    generate_assets.py
    generators/
```

## Generator contract

Every generator should accept:

- `seed`
- `variant`
- `quality`
- `output_directory`

The same seed must reproduce the same asset. Variant changes should alter appearance or secondary geometry without breaking gameplay dimensions.

## Initial rollout

The first generator family establishes the pipeline with:

- modular wall panel
- interior door + frame
- metal locker
- wooden crate
- ceiling light fixture
- pipe segment
- cable tray
- small utility table

The generator also creates a small demonstration scene containing several deterministic variants. This is deliberately boring engineering work, because boring engineering work is what prevents the game from becoming a pile of attractive garbage later.

## Runtime material architecture

The C++ renderer will eventually load compact material descriptions containing:

```text
base_material
seed
base_color
roughness
metallic
normal_strength
noise_scale
noise_strength
dirt_amount
wear_amount
wetness
emission
```

The renderer derives high-frequency detail in shaders. Gameplay-critical surfaces must never depend on a texture that procedural generation could accidentally omit.

## Validation

Asset generation will eventually run in CI with checks for:

- deterministic output
- valid dimensions
- missing materials
- non-manifold geometry where forbidden
- invalid transforms
- excessive triangle counts
- missing collision tags
- invalid export paths
- duplicate asset IDs
