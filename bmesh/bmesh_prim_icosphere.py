import bmesh

def create_icospehere(subdiv, d):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, diameter=d)
    v, e, p = pydata_from_bmesh(bm)
    bm.free()
    return v, e, p
