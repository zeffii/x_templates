import bpy

# create 4 verts, string them together to make 4 edges.
coord1 = (-1.0, 1.0, 0.0)
coord2 = (-1.0, -1.0, 0.0)
coord3 = (1.0, -1.0, 0.0)
coord4 = (1.0, 1.0, 0.0)

Verts = [coord1, coord2, coord3, coord4]
Edges = [[0,1],[1,2],[2,3],[3,0]]

profile_mesh = bpy.data.meshes.new("Base_Profile_Data")
profile_mesh.from_pydata(Verts, Edges, [])
profile_mesh.update()

profile_object = bpy.data.objects.new("Base_Profile", profile_mesh)
profile_object.data = profile_mesh  # this line is redundant .. it simply overwrites .data

scene = bpy.context.scene
scene.objects.link(profile_object)
profile_object.select = True