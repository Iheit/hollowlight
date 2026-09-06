import bpy, os
from mathutils import Vector

OUT = os.path.abspath('assets/generated/materials')
os.makedirs(OUT, exist_ok=True)

def material(name, base, roughness, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    bs = n.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*base, 1.0)
    bs.inputs['Roughness'].default_value = roughness
    bs.inputs['Metallic'].default_value = metallic
    noise = n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 5.0; noise.inputs['Detail'].default_value = 3.0; noise.inputs['Roughness'].default_value = 0.75
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*[max(0.0, c*0.65) for c in base], 1)
    ramp.color_ramp.elements[1].color = (*[min(1.0, c*1.25) for c in base], 1)
    l.new(noise.outputs['Fac'], ramp.inputs['Fac']); l.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    return m

MATERIALS = {
    'concrete': ((0.30,0.29,0.27),0.88,0.0), 'plaster': ((0.38,0.37,0.34),0.82,0.0),
    'painted_metal': ((0.12,0.14,0.14),0.52,0.65), 'galvanized_metal': ((0.35,0.37,0.36),0.48,0.85),
    'rusted_metal': ((0.22,0.09,0.045),0.78,0.55), 'stainless': ((0.45,0.47,0.46),0.3,0.9),
    'dirty_glass': ((0.12,0.20,0.21),0.22,0.05), 'rubber': ((0.025,0.027,0.025),0.92,0.0),
    'dark_wood': ((0.13,0.075,0.04),0.72,0.0), 'painted_wood': ((0.27,0.18,0.12),0.68,0.0),
    'ceramic_tile': ((0.42,0.43,0.40),0.38,0.0), 'vinyl_floor': ((0.16,0.17,0.16),0.62,0.0),
    'carpet': ((0.10,0.095,0.085),0.97,0.0), 'plastic': ((0.12,0.13,0.13),0.5,0.0),
}

def main():
    for name, (base, rough, metal) in MATERIALS.items():
        m = material('HL_MAT_' + name, base, rough, metal)
        bpy.context.view_layer.objects.active = None
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, name + '.blend'))
    print('Hollowlight material library generated:', len(MATERIALS))

main()
