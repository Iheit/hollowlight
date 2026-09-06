import bpy, os, random
OUT=os.path.abspath('assets/generated/meshes'); os.makedirs(OUT,exist_ok=True); random.seed(int(os.environ.get('HOLLOWLIGHT_ASSET_SEED','1337')))
def mat(n,c):
 m=bpy.data.materials.get(n) or bpy.data.materials.new(n); m.diffuse_color=(*c,1); return m
WOOD=mat('Furniture_Wood',(.18,.10,.05)); MET=mat('Furniture_Metal',(.12,.13,.13)); FAB=mat('Furniture_Fabric',(.16,.17,.16)); PL=mat('Furniture_Plastic',(.08,.08,.075))
def box(n,l,s,m):
 bpy.ops.mesh.primitive_cube_add(location=l); o=bpy.context.object; o.name=n; o.scale=(s[0]/2,s[1]/2,s[2]/2); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m); q=o.modifiers.new('Bevel','BEVEL'); q.width=.03; q.segments=2; return o
def save(n): bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,n+'.blend'))
def table():
 for x in (-.65,.65):
  for y in (-.4,.4): box('Leg',(x,y,.38),(.09,.09,.76),MET)
 box('Top',(0,0,.8),(1.5,1,.14),WOOD); save('furniture_table')
def chair():
 box('Seat',(0,0,.48),(.55,.55,.12),FAB); [box('Leg',(x,y,.23),(.07,.07,.46),MET) for x in (-.22,.22) for y in (-.22,.22)]; box('Back',(0,.23,1.0),(.55,.1,1),FAB); save('furniture_chair')
def shelf():
 [box('Shelf',(0,0,z),(1.6,.4,.08),WOOD) for z in (.3,.9,1.5,2.1)]; [box('Post',(x,0,1.2),(.08,.08,2.4),MET) for x in (-.76,.76)]; save('furniture_shelf')
def locker():
 box('Locker',(0,0,1.1),(.7,.45,2.2),MET); [box('Vent',(0,-.24,z),(.35,.02,.035),PL) for z in (1.35,1.42,1.49)]; save('furniture_locker')
for f in (table,chair,shelf,locker): bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); f()
print('Furniture generation complete')
