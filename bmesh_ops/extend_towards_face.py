import bpy
import bmesh
import mathutils
from mathutils.geometry import intersect_line_plane


def extend_vertex(system='local'):

    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    verts = bm.verts
    faces = bm.faces

    plane = [f for f in faces if f.select][0]
    plane_vert_indices = [v for v in plane.verts[:]]
    all_selected_vert_indices = [v for v in verts if v.select]

    M = set(plane_vert_indices)
    N = set(all_selected_vert_indices)
    O = N.difference(M)
    O = list(O)
    (v1_ref, v1_idx, v1), (v2_ref, v2_idx, v2) = [(i, i.index, i.co) for i in O]

    plane_co = plane.calc_center_median()
    plane_no = plane.normal

    new_co = intersect_line_plane(v1, v2, plane_co, plane_no, False)
    new_vertex = verts.new(new_co)

    A_len = (v1 - new_co).length
    B_len = (v2 - new_co).length

    vertex_reference = v1_ref if (A_len < B_len) else v2_ref
    bm.edges.new([vertex_reference, new_vertex])

    bmesh.update_edit_mesh(me, True)


extend_vertex()
