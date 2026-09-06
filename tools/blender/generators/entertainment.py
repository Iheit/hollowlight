import bpy, os, random
OUT=os.path.abspath('assets/generated/meshes'); os.makedirs(OUT,exist_ok=True); random.seed(int(os.environ.get('HOLLOWLIGHT_ASSET_SEED','1337')))
def mat(n,c,e=0):
 m=bpy.data.materials.get(n) or bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True; b=m.node_tree.nodes.get('Principled BSDF'); b.inputs['Base Color'].default_value=(*c,1); b.inputs['Emission Color'].default_value=(*c,1); b.inputs['Emission Strength'].default_value=e; return m
D=mat('Arcade_Dark',(.025,.03,.035)); P=mat('Arcade_Panel',(.18,.16,.14)); E=mat('Arcade_Emissive',(.25,.3,.35),2.0); G=mat('Arcade_Glass',(.08,.14,.16),.2)
def box(n,l,s,m,bev=.03):
 bpy.ops.mesh.primitive_cube_add(location=l); o=bpy.context.object; o.name=n; o.scale=(s[0]/2,s[1]/2,s[2]/2); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m); q=o.modifiers.new('Bevel','BEVEL'); q.width=bev; q.segments=2; return o
def save(n): bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,n+'.blend'))
def arcade():
 box('Cabinet',(0,0,1),(.9,.7,2),D); box('Screen',(0,-.37,1.45),(.62,.04,.55),G); box('Control',(0,-.38,.95),(.7,.2,.16),P); box('ScreenGlow',(0,-.395,1.45),(.5,.01,.4),E,.01); save('entertainment_arcade')
def vending():
 box('Machine',(0,0,1.1),(.9,.65,2.2),P); box('Window',(0,-.34,1.35),(.6,.03,.9),G); box('Panel',(.3,-.36,.65),(.18,.03,.3),E); save('entertainment_vending')
def ticket():
 box('Kiosk',(0,0,1),(.8,.6,2),P); box('Display',(0,-.32,1.35),(.5,.04,.35),E); box('Slot',(0,-.34,.7),(.3,.03,.05),D); save('entertainment_ticket')
for f in (arcade,vending,ticket): bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); f()
print('Entertainment generation complete')
