import bpy, os
OUT=os.path.abspath('assets/generated/meshes'); os.makedirs(OUT,exist_ok=True)
def material(name,c,r=.55):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.diffuse_color=(*c,1); m.use_nodes=True; b=m.node_tree.nodes.get('Principled BSDF'); b.inputs['Base Color'].default_value=(*c,1); b.inputs['Roughness'].default_value=r; return m
MET=material('Door_Metal',(.09,.1,.1)); DARK=material('Door_Dark',(.035,.04,.04)); GL=material('Door_Glass',(.12,.2,.22),.18); YEL=material('Door_Warning',(.45,.3,.03))
def box(n,l,s,m,bev=.025):
 bpy.ops.mesh.primitive_cube_add(location=l); o=bpy.context.object; o.name=n; o.scale=(s[0]/2,s[1]/2,s[2]/2); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m)
 if bev: q=o.modifiers.new('Bevel','BEVEL'); q.width=bev; q.segments=2
 return o
def save(n): bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,n+'.blend'))
def make(kind):
 bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
 box('FrameL',(-.95,0,1.4),(.12,.22,2.8),MET); box('FrameR',(.95,0,1.4),(.12,.22,2.8),MET); box('FrameT',(0,0,2.74),(2,.22,.12),MET)
 if kind=='fire': box('FireDoor',(0,.02,1.4),(1.78,.16,2.55),YEL); box('PushBar',(0,-.1,1.35),(1.25,.08,.08),DARK)
 elif kind=='glass': box('GlassDoor',(0,.02,1.4),(1.78,.10,2.55),GL); box('Handle',(.62,-.1,1.3),(.08,.08,.7),MET)
 elif kind=='hatch': box('ServiceHatch',(0,.02,1.4),(1.78,.18,2.55),DARK); box('Latch',(0,-.11,1.4),(.18,.06,.3),MET)
 else: box('Door',(0,.02,1.4),(1.78,.16,2.55),MET); box('Handle',(.62,-.11,1.3),(.08,.08,.7),MET)
 save('door_'+kind)
for k in ('standard','fire','glass','hatch'): make(k)
print('Door generation complete')
