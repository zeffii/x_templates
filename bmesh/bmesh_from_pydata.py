import bmesh


def bmesh_from_pydata(verts=None, edges=None, faces=None):
    ''' verts is necessary, edges/faces are optional '''

    bm = bmesh.new()
    if not verts:
        return bm

    add_vert = bm.verts.new

    bm_verts = [add_vert(co) for co in verts]
    bm.verts.index_update()

    if faces:
        add_face = bm.faces.new
        for face in faces:
            add_face([bm_verts[i] for i in face])
        bm.faces.index_update()

    if edges:
        add_edge = bm.edges.new
        for edge in edges:
            edge_seq = bm_verts[edge[0]], bm_verts[edge[1]]
            try:
                add_edge(edge_seq)
            except ValueError:
                # edge exists!
                pass
        bm.edges.index_update()

    return bm
