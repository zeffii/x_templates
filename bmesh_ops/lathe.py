import bpy
import bmesh
from bmesh.ops import spin
import math


def lathe_geometry(bm, cent, axis, dvec, angle, steps, remove_doubles=True, dist=0.0001):
    geom = bm.verts[:] + bm.edges[:]

    # super verbose explanation.
    spin(
        bm, 
        geom=geom,         # geometry to use for the spin
        cent=cent,         # center point of the spin world
        axis=axis,         # axis, a (x, y, z) spin axis
        dvec=dvec,         # offset for the center point
        angle=angle,       # how much of the unit circle to rotate around
        steps=steps,       # spin subdivision level 
        use_duplicate=0)   # include existing geometry in returned content

    if remove_doubles:
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=dist)

obj = bpy.data.objects['Graph']
bm = bmesh.new()
bm.from_mesh(obj.data)

axis = (0,0,1)
dvec = (0,0,0)
angle = 2*math.pi
steps = 20
cent = obj.location

lathe_geometry(bm, cent, axis, dvec, angle, steps, remove_doubles=True, dist=0.0001)

bm.to_mesh(obj.data)
obj.data.update()   # <--- not strictly needed, Blender will update itself often anyway.
bm.free()
