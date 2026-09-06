import bpy, os, math
from mathutils import Vector

OUT = os.path.abspath('assets/generated/meshes')
os.makedirs(OUT, exist_ok=True)

def mat(name, color, rough=.6, metallic=0):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Roughness'].default_value=rough; bs.inputs['Metallic'].default_value=metallic
    return m

BODY=mat('HL_HeroBody',(.055,.06,.065),.42,.75); PANEL=mat('HL_HeroPanel',(.16,.17,.16),.48,.45); EM=mat('HL_HeroEmission',(.12,.32,.28),.3,0)

def box(name, loc, scale, material, bevel=.025):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.scale=(scale[0]/2,scale[1]/2,scale[2]/2); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel: mod=o.modifiers.new('HeroEdgeBevel','BEVEL'); mod.width=bevel; mod.segments=3
    o.data.materials.append(material); return o

def control_console():
    box('HL_MasterConsoleBody',(0,0,.65),(2.4,1.0,1.3),BODY,.06)
    box('HL_MasterConsoleTop',(0,-.05,1.34),(2.1,.85,.12),PANEL,.025)
    for x in (-.75,-.25,.25,.75):
        bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=.07,depth=.08,location=(x,-.18,1.45))
        bpy.context.object.data.materials.append(PANEL)
    for x in (-.65,0,.65):
        box('HL_Display',(x,.18,1.45),(.42,.06,.25),EM,.01)
    box('HL_ConsoleBase',(0,.1,.12),(2.55,1.08,.18),BODY,.03)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'hero_master_control_console.blend'))

def escape_mechanism():
    box('HL_EscapeHousing',(0,0,1.15),(1.8,.55,2.3),BODY,.06)
    box('HL_EscapeDoor',(0,-.30,1.15),(1.25,.08,1.95),PANEL,.03)
    box('HL_EscapeHandle',(.45,-.38,1.15),(.12,.08,.65),BODY,.02)
    for z in (.55,1.15,1.75): box('HL_StatusLight',(-.45,-.36,z),(.08,.035,.08),EM,.01)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'hero_escape_mechanism.blend'))

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
control_console(); bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); escape_mechanism()
print('Hollowlight hero props generated')
