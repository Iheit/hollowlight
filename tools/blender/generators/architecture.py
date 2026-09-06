import bpy, os, random
from mathutils import Vector

SEED = int(os.environ.get('HOLLOWLIGHT_ASSET_SEED', '1337'))
random.seed(SEED)
OUT = os.path.abspath('assets/generated/meshes')
os.makedirs(OUT, exist_ok=True)

def mat(name, color, roughness=0.7):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Roughness'].default_value=roughness
    return m

M=mat('Architecture_Plaster',(0.32,0.31,0.28)); F=mat('Architecture_Floor',(0.18,0.18,0.17)); MET=mat('Architecture_Metal',(0.12,0.13,0.13),0.45); GL=mat('Architecture_Glass',(0.16,0.22,0.24),0.2)

def box(n,loc,scale,ma=M,bev=0.03):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=n; o.scale=(scale[0]/2,scale[1]/2,scale[2]/2); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bev: mod=o.modifiers.new('EdgeBevel','BEVEL'); mod.width=bev; mod.segments=2
    o.data.materials.append(ma); return o

def save(n): bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,n+'.blend'))

def floor(): box('HL_Floor_2x2',(0,0,0),(2,2,.15),F); save('architecture_floor')
def ceiling(): box('HL_Ceiling_2x2',(0,0,2.8),(2,2,.15),M); save('architecture_ceiling')
def wall(): box('HL_Wall_2x2',(0,0,1.4),(.15,2,2.8),M); save('architecture_wall')
def corner(): box('HL_Corner_A',(0,0,1.4),(.15,2,2.8),M); box('HL_Corner_B',(1.0,1.0,1.4),(2,.15,2.8),M); save('architecture_corner')
def pillar(): box('HL_Pillar',(0,0,1.4),(.35,.35,2.8),MET,.04); save('architecture_pillar')
def beam(): box('HL_Beam',(0,0,2.65),(3,.3,.3),MET,.04); save('architecture_beam')
def window(): box('HL_WindowFrame',(0,0,1.5),(1.6,.12,1.8),MET); box('HL_Glass',(0,.01,1.5),(1.35,.04,1.55),GL,.01); save('architecture_window')
def railing(): box('HL_RailTop',(0,0,1.0),(2,.08,.08),MET); box('HL_RailPostA',(-.9,0,.5),(.08,.08,1),MET); box('HL_RailPostB',(.9,0,.5),(.08,.08,1),MET); save('architecture_railing')

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for fn in (floor,ceiling,wall,corner,pillar,beam,window,railing):
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); fn()
print('Architecture generation complete:', SEED)
