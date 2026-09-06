import bpy
import os
from pathlib import Path

SEED = int(os.environ.get('HOLLOWLIGHT_ASSET_SEED', '1337'))
OUT = Path('assets/generated/meshes/office')
OUT.mkdir(parents=True, exist_ok=True)


def material(name, color, roughness=0.65, metallic=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    return m

PANEL = material('Office_PaintedMetal', (0.24, 0.25, 0.23), 0.55, 0.35)
WOOD = material('Office_Wood', (0.25, 0.17, 0.11), 0.72)
BLACK = material('Office_Plastic', (0.035, 0.04, 0.04), 0.5)
PAPER = material('Office_Paper', (0.55, 0.53, 0.47), 0.9)


def box(name, loc, size, mat, bevel=0.025):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = tuple(v / 2 for v in size)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        b = o.modifiers.new('SoftEdges', 'BEVEL')
        b.width, b.segments = bevel, 2
    o.data.materials.append(mat)
    return o


def save(name):
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f'{name}.blend'))


def desk():
    box('DeskTop', (0, 1.0, 0), (1.8, 0.75, 0.10), WOOD)
    for x in (-0.75, 0.75):
        for y in (-0.27, 0.27):
            box('DeskLeg', (x, y, -0.55), (0.08, 0.08, 1.1), PANEL, 0.01)
    box('CableTray', (0, 0.8, -0.22), (1.2, 0.12, 0.08), BLACK, 0.01)
    save('office_desk')


def chair():
    box('Seat', (0, 0, 0), (0.55, 0.55, 0.12), BLACK)
    box('Back', (0, 0.23, 0.48), (0.55, 0.10, 0.9), BLACK)
    for x in (-0.22, 0.22):
        for y in (-0.22, 0.22):
            box('Leg', (x, y, -0.38), (0.055, 0.055, 0.7), PANEL, 0.01)
    save('office_chair')


def filing_cabinet():
    box('Cabinet', (0, 0, 0), (0.7, 0.65, 1.4), PANEL)
    for z in (-0.45, -0.15, 0.15, 0.45):
        box('Drawer', (0, -0.34, z), (0.58, 0.035, 0.24), PANEL, 0.008)
        box('Handle', (0, -0.37, z), (0.18, 0.025, 0.025), BLACK, 0.005)
    save('office_filing_cabinet')


def computer_terminal():
    box('Monitor', (0, 0, 0.7), (0.75, 0.10, 0.48), BLACK, 0.04)
    box('Screen', (0, -0.057, 0.72), (0.60, 0.015, 0.34), PAPER, 0.005)
    box('Stand', (0, 0, 0.38), (0.10, 0.18, 0.35), PANEL, 0.02)
    box('Keyboard', (0, -0.3, 0.18), (0.58, 0.25, 0.05), BLACK, 0.015)
    save('office_terminal')


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for fn in (desk, chair, filing_cabinet, computer_terminal):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    fn()
print('Hollowlight office assets generated with seed', SEED)
