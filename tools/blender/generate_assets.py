"""Hollowlight procedural asset factory.

Run with Blender's Python interpreter, for example:
    blender --background --python tools/blender/generate_assets.py

The script works both from Blender's Scripting workspace and from the command line.
"""

from __future__ import annotations

import math
import os
import random
from pathlib import Path

import bpy


def find_project_root() -> Path:
    """Find the Hollowlight repository regardless of how Blender launched us."""
    override = os.environ.get("HOLLOWLIGHT_ROOT")
    if override:
        root = Path(override).expanduser().resolve()
        if (root / "tools" / "blender").is_dir():
            return root

    script_file = globals().get("__file__")
    if script_file:
        path = Path(script_file)
        if path.is_absolute():
            path = path.resolve()
            for parent in path.parents:
                if (parent / "tools" / "blender").is_dir():
                    return parent

    for text in bpy.data.texts:
        if text.filepath:
            path = Path(bpy.path.abspath(text.filepath)).resolve()
            for parent in path.parents:
                if (parent / "tools" / "blender").is_dir():
                    return parent

    for start in (Path.cwd().resolve(),):
        for parent in (start, *start.parents):
            if (parent / "tools" / "blender").is_dir():
                return parent

    raise RuntimeError(
        "Could not locate the Hollowlight project. Open this script from "
        "the repository or set HOLLOWLIGHT_ROOT to the repository folder."
    )


ROOT = find_project_root()
OUTPUT = ROOT / "assets" / "generated"
MESH_DIR = OUTPUT / "meshes"
MATERIAL_DIR = OUTPUT / "materials"
MANIFEST_DIR = OUTPUT / "manifests"


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (
        bpy.data.meshes,
        bpy.data.curves,
        bpy.data.materials,
        bpy.data.cameras,
        bpy.data.lights,
    ):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def ensure_dirs() -> None:
    for path in (MESH_DIR, MATERIAL_DIR, MANIFEST_DIR):
        path.mkdir(parents=True, exist_ok=True)


def make_principled(name: str, color, roughness: float, metallic: float = 0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic

    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 5.0
    noise.inputs["Detail"].default_value = 3.0
    noise.inputs["Roughness"].default_value = 0.7

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = tuple(max(0.0, c * 0.55) for c in color[:3]) + (1.0,)
    ramp.color_ramp.elements[1].color = tuple(min(1.0, c * 1.25) for c in color[:3]) + (1.0,)
    ramp.color_ramp.elements[0].position = 0.28
    ramp.color_ramp.elements[1].position = 0.72

    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def add_box(name: str, location, scale, material=None, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (scale[0] / 2, scale[1] / 2, scale[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0:
        mod = obj.modifiers.new("EdgeSoftening", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    if material:
        obj.data.materials.append(material)
    return obj


def add_cylinder(name: str, location, radius, depth, material=None, rotation=(0, 0, 0), vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj


def wall_panel(rng: random.Random, index: int):
    plaster = make_principled(f"MAT_Plaster_{index}", (0.30, 0.28, 0.24, 1), 0.88)
    trim = make_principled(f"MAT_Trim_{index}", (0.08, 0.075, 0.065, 1), 0.72)
    add_box(f"WallPanel_{index}", (0, 0, 1.5), (3.0, 0.18, 3.0), plaster)
    add_box(f"WallTrim_{index}", (0, -0.11, 0.55), (3.0, 0.08, 0.12), trim)
    if rng.random() < 0.75:
        add_box(
            f"DamageStrip_{index}",
            (rng.uniform(-0.8, 0.8), -0.105, rng.uniform(1.0, 2.3)),
            (rng.uniform(0.3, 1.1), 0.025, rng.uniform(0.03, 0.10)),
            trim,
        )


def door(rng: random.Random, index: int):
    metal = make_principled(f"MAT_DoorMetal_{index}", (0.12, 0.13, 0.12, 1), 0.58, 0.35)
    frame = make_principled(f"MAT_DoorFrame_{index}", (0.055, 0.06, 0.055, 1), 0.68, 0.45)
    add_box(f"Door_{index}", (0, 0, 1.05), (0.92, 0.10, 2.10), metal, 0.025)
    add_box(f"DoorFrameL_{index}", (-0.51, 0, 1.1), (0.10, 0.18, 2.30), frame, 0.02)
    add_box(f"DoorFrameR_{index}", (0.51, 0, 1.1), (0.10, 0.18, 2.30), frame, 0.02)
    add_box(f"DoorFrameT_{index}", (0, 0, 2.25), (1.12, 0.18, 0.10), frame, 0.02)
    add_cylinder(f"Handle_{index}", (0.31, -0.09, 1.05), 0.035, 0.13, frame, rotation=(math.pi / 2, 0, 0), vertices=12)


def locker(rng: random.Random, index: int):
    body = make_principled(f"MAT_Locker_{index}", (0.16, 0.18, 0.17, 1), 0.62, 0.55)
    accent = make_principled(f"MAT_LockerAccent_{index}", (0.08, 0.09, 0.085, 1), 0.55, 0.65)
    add_box(f"LockerBody_{index}", (0, 0, 1.0), (0.65, 0.45, 2.0), body, 0.025)
    for z in (0.72, 1.32):
        add_box(f"LockerSeam_{index}_{z}", (0, -0.235, z), (0.56, 0.025, 0.018), accent)
    for z in (0.95, 1.55):
        add_box(f"LockerVent_{index}_{z}", (0, -0.24, z), (0.28, 0.02, 0.018), accent)


def crate(rng: random.Random, index: int):
    wood = make_principled(f"MAT_Crate_{index}", (0.22, 0.12, 0.055, 1), 0.91)
    slat = make_principled(f"MAT_CrateSlat_{index}", (0.11, 0.06, 0.025, 1), 0.88)
    add_box(f"CrateBody_{index}", (0, 0, 0.45), (0.9, 0.9, 0.9), wood, 0.025)
    for x in (-0.30, 0.30):
        add_box(f"CrateBandX_{index}_{x}", (x, -0.47, 0.45), (0.09, 0.05, 0.88), slat)
    for y in (-0.30, 0.30):
        add_box(f"CrateBandY_{index}_{y}", (-0.47, y, 0.45), (0.05, 0.09, 0.88), slat)


def ceiling_light(rng: random.Random, index: int):
    metal = make_principled(f"MAT_LightMetal_{index}", (0.18, 0.18, 0.16, 1), 0.52, 0.7)
    glass = make_principled(f"MAT_LightGlass_{index}", (0.65, 0.68, 0.62, 1), 0.25)
    add_box(f"LightHousing_{index}", (0, 0, 2.95), (1.2, 0.28, 0.10), metal, 0.025)
    add_box(f"LightDiffuser_{index}", (0, -0.01, 2.88), (0.95, 0.24, 0.05), glass, 0.012)


def pipe_segment(rng: random.Random, index: int):
    pipe = make_principled(f"MAT_Pipe_{index}", (0.16, 0.17, 0.15, 1), 0.58, 0.72)
    length = rng.choice((1.5, 2.0, 2.5, 3.0))
    add_cylinder(f"Pipe_{index}", (0, 0, 1.8), 0.065, length, pipe, rotation=(0, math.pi / 2, 0), vertices=16)
    add_cylinder(f"PipeCollarA_{index}", (-length * 0.34, 0, 1.8), 0.09, 0.12, pipe, rotation=(0, math.pi / 2, 0), vertices=16)
    add_cylinder(f"PipeCollarB_{index}", (length * 0.34, 0, 1.8), 0.09, 0.12, pipe, rotation=(0, math.pi / 2, 0), vertices=16)


def cable_tray(rng: random.Random, index: int):
    metal = make_principled(f"MAT_CableTray_{index}", (0.09, 0.095, 0.085, 1), 0.62, 0.65)
    add_box(f"TrayBase_{index}", (0, 0, 2.55), (2.5, 0.28, 0.06), metal)
    add_box(f"TraySideA_{index}", (0, -0.16, 2.68), (2.5, 0.035, 0.25), metal)
    add_box(f"TraySideB_{index}", (0, 0.16, 2.68), (2.5, 0.035, 0.25), metal)


def utility_table(rng: random.Random, index: int):
    top = make_principled(f"MAT_TableTop_{index}", (0.19, 0.17, 0.14, 1), 0.83)
    legs = make_principled(f"MAT_TableLegs_{index}", (0.075, 0.08, 0.075, 1), 0.56, 0.65)
    add_box(f"TableTop_{index}", (0, 0, 1.0), (1.4, 0.65, 0.10), top, 0.025)
    for x in (-0.58, 0.58):
        for y in (-0.23, 0.23):
            add_box(f"TableLeg_{index}_{x}_{y}", (x, y, 0.5), (0.07, 0.07, 1.0), legs, 0.01)


def save_asset(asset_name: str) -> None:
    bpy.ops.wm.save_as_mainfile(filepath=str(MESH_DIR / f"{asset_name}.blend"))


def main() -> None:
    ensure_dirs()
    clear_scene()
    seed = int(os.environ.get("HOLLOWLIGHT_ASSET_SEED", "1337"))
    rng = random.Random(seed)

    generators = [
        ("wall_panel", wall_panel),
        ("door", door),
        ("locker", locker),
        ("crate", crate),
        ("ceiling_light", ceiling_light),
        ("pipe_segment", pipe_segment),
        ("cable_tray", cable_tray),
        ("utility_table", utility_table),
    ]

    manifest = [f"seed={seed}"]
    for asset_name, generator in generators:
        clear_scene()
        generator(rng, 0)
        save_asset(asset_name)
        manifest.append(asset_name)

    clear_scene()
    for i, (_, generator) in enumerate(generators):
        generator(rng, i)
        for obj in bpy.context.scene.objects:
            if obj.type == "MESH":
                obj.location.x += (i % 4) * 3.0
                obj.location.y += (i // 4) * 3.0
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT / "Hollowlight_AssetFactory_Demo.blend"))

    (MANIFEST_DIR / "asset_factory_manifest.txt").write_text(
        "\n".join(manifest) + "\n", encoding="utf-8"
    )
    print(f"Hollowlight asset factory complete. Root: {ROOT}. Seed: {seed}")


if __name__ == "__main__":
    main()
