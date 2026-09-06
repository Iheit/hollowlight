import bpy
import os
from pathlib import Path

SEED = int(os.environ.get('HOLLOWLIGHT_ASSET_SEED', '1337'))
OUT = Path('assets/generated/meshes/maintenance')
OUT.mkdir(parents=True, exist_ok=True)


def mat(name, color, roughness=0.55, metallic=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Roughness'].default_value = roughness
    b.inputs['Metallic'].default_value = metallic
    return m

METAL = mat('Maintenance_Metal', (0.13, 0.14, 0.14), 0.45, 0.8)
PAINT = mat('Maintenance_Painted', (0.28, 0.29, 0.27), 0.58, 0.35)
RUBBER = mat('Maintenance_Rubber', (0.025, 0.025, 0.022), 0.85)
WARNING = mat('Maintenance_Warning', (0.55, 0.35, 0.05), 0.5)


def box(name, loc, size, material, bevel=0.02):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = tuple(v / 2 for v in size)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new('Bevel', 'BEVEL')
        mod.width, mod.segments = bevel, 2
    o.data.materials.append(material)
    return o


def cyl(name, loc, radius, depth, material, rotation=(0, 0, 0), vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    return o


def save(name):
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f'{name}.blend'))


def generator():
    box('GeneratorBody', (0, 0, 0.8), (1.5, 0.8, 1.6), PAINT, 0.07)
    for x in (-0.45, 0, 0.45):
        cyl('Vent', (x, -0.43, 1.0), 0.12, 0.05, METAL, rotation=(1.5708, 0, 0))
    cyl('Exhaust', (0.4, 0, 1.75), 0.13, 0.55, METAL)
    box('WarningPanel', (-0.35, -0.43, 1.35), (0.45, 0.04, 0.25), WARNING, 0.01)
    save('maintenance_generator')


def breaker_panel():
    box('BreakerBox', (0, 0, 1.0), (0.8, 0.28, 1.5), PAINT, 0.04)
    for z in (0.45, 0.75, 1.05, 1.35):
        box('Breaker', (-0.12, -0.17, z), (0.12, 0.035, 0.09), METAL, 0.006)
    box('WarningStrip', (0.22, -0.17, 0.9), (0.18, 0.035, 0.65), WARNING, 0.006)
    save('maintenance_breaker_panel')


def pump():
    box('PumpBase', (0, 0, 0.2), (1.1, 0.7, 0.4), METAL, 0.04)
    cyl('PumpHousing', (0, 0, 0.65), 0.4, 0.65, PAINT, rotation=(0, 1.5708, 0))
    cyl('Pipe', (0.55, 0, 0.65), 0.10, 0.8, METAL, rotation=(0, 1.5708, 0))
    cyl('Pipe', (-0.55, 0, 0.65), 0.10, 0.8, METAL, rotation=(0, 1.5708, 0))
    save('maintenance_pump')


def control_console():
    box('ConsoleBody', (0, 0, 0.65), (1.4, 0.7, 1.3), PAINT, 0.05)
    box('ControlFace', (0, -0.37, 0.95), (1.0, 0.05, 0.45), METAL, 0.02)
    for x in (-0.35, 0, 0.35):
        cyl('Button', (x, -0.41, 1.0), 0.055, 0.05, WARNING, rotation=(1.5708, 0, 0), vertices=12)
    save('maintenance_control_console')


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for fn in (generator, breaker_panel, pump, control_console):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    fn()
print('Hollowlight maintenance assets generated with seed', SEED)
