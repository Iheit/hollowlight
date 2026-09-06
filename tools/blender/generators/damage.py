import bpy, os, random, math
from mathutils import Vector

SEED = int(os.environ.get('HOLLOWLIGHT_ASSET_SEED', '1337'))
rng = random.Random(SEED)
OUT = os.path.abspath('assets/generated/meshes')
os.makedirs(OUT, exist_ok=True)

def mat(name, color, rough=0.8):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Roughness'].default_value=rough
    return m

WALL=mat('HL_DamagedWall',(0.30,0.29,0.26)); DARK=mat('HL_DamageDark',(0.035,0.03,0.025)); RUST=mat('HL_Rust',(0.28,0.07,0.025),0.9)

def box(name, loc, scale, material=WALL, bevel=0.01):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.scale=(scale[0]/2,scale[1]/2,scale[2]/2); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mod=o.modifiers.new('EdgeBevel','BEVEL'); mod.width=bevel; mod.segments=2
    o.data.materials.append(material); return o

def generate_damage_panel():
    box('HL_DamageBase',(0,0,1.4),(.15,3,2.8))
    for i in range(9):
        y=rng.uniform(-1.35,1.35); z=rng.uniform(.25,2.55); length=rng.uniform(.12,.55)
        crack=box('HL_Crack',(0.08,y,z),(.025,length,.025),DARK,0)
        crack.rotation_euler.x=rng.uniform(-0.8,0.8)
    for i in range(5):
        y=rng.uniform(-1.3,1.3); z=rng.uniform(.2,2.5)
        box('HL_Wear',(0.081,y,z),(.02,rng.uniform(.08,.25),rng.uniform(.04,.12)),RUST,0)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'damage_wall_panel.blend'))

def generate_broken_pipe():
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=.07, depth=1.8, location=(0,0,.9), rotation=(0,math.pi/2,0)); a=bpy.context.object; a.name='HL_PipeA'; a.data.materials.append(RUST)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=.07, depth=.45, location=(1.0,0,.9), rotation=(0,math.pi/2,0)); b=bpy.context.object; b.name='HL_PipeB'; b.data.materials.append(RUST)
    for i in range(4):
        box('HL_Leak',(.35+rng.uniform(-.1,.1),rng.uniform(-.02,.02),.9+rng.uniform(-.15,.15)),(.025,.025,.15),DARK,0)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'damage_broken_pipe.blend'))

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
generate_damage_panel(); bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); generate_broken_pipe()
print('Hollowlight damage assets generated:', SEED)
