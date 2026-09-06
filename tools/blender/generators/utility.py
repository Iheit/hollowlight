import bpy, os
OUT=os.path.abspath('assets/generated/meshes'); os.makedirs(OUT,exist_ok=True)
def mat(n,c,r=.6):
 m=bpy.data.materials.get(n) or bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True; b=m.node_tree.nodes.get('Principled BSDF'); b.inputs['Base Color'].default_value=(*c,1); b.inputs['Roughness'].default_value=r; return m
M=mat('Utility_Metal',(.11,.12,.12),.45); W=mat('Utility_Warning',(.5,.32,.03)); D=mat('Utility_Dark',(.035,.04,.04)); C=mat('Utility_Copper',(.22,.09,.035),.4)
def box(n,l,s,m=M):
 bpy.ops.mesh.primitive_cube_add(location=l); o=bpy.context.object; o.name=n; o.scale=(s[0]/2,s[1]/2,s[2]/2); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m); q=o.modifiers.new('Bevel','BEVEL'); q.width=.025; q.segments=2; return o
def cyl(n,l,r,d,m=M):
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=d,location=l); o=bpy.context.object; o.name=n; o.data.materials.append(m); return o
def save(n): bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,n+'.blend'))
def make(n):
 bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
 if n=='electrical_cabinet': box('Cabinet',(0,0,1),(.8,.28,2),M); box('Panel',(0,-.16,1.25),(.55,.03,.85),D); [cyl('Switch',(-.2,-.19,z),.035,.08,W) for z in (.95,1.15,1.35)]
 elif n=='duct': box('Duct',(0,0,1.4),(2,.55,.55),M); box('DuctSeam',(.0,-.29,1.4),(.06,.02,.5),D)
 elif n=='pump': cyl('Tank',(0,0,1.0),.42,1.5,M); cyl('Pipe',(.6,0,1.7),.08,1.2,C); box('Base',(0,0,.2),(1.3,.8,.2),D)
 else: box('ServicePanel',(0,0,1),(.8,.12,1.4),M); box('Warning',(0,-.08,1.35),(.5,.02,.25),W)
 save('utility_'+n)
for n in ('electrical_cabinet','duct','pump','service_panel'): make(n)
print('Utility generation complete')
