"""Shared helpers for headless procedural generators (PROC-001). Blender units = meters, Z-up;
the FBX export converts to Unity's Y-up. See Docs/Assets/Specs/PROC_PIPELINE.md."""
import hashlib
import math

import bmesh
import bpy

UV_MAIN = "UVMap_Main"
UV_LABEL = "UVMap_Label"
LABEL_OFF = (-8.0, -8.0)  # UVMap_Label value for faces outside the label region (shader masks it)


def rounded_rect(w, d, r, seg, inset=0.0):
    """Convex rounded-rectangle loop centred on the origin, CCW seen from +Z."""
    hw, hd = w / 2 - inset, d / 2 - inset
    r = max(min(r - inset, hw, hd), 0.0)
    if seg == 0 or r == 0:
        return [(hw, hd), (-hw, hd), (-hw, -hd), (hw, -hd)]
    pts = []
    for cx, cy, a0 in ((hw - r, hd - r, 0), (-hw + r, hd - r, 90), (-hw + r, -hd + r, 180), (hw - r, -hd + r, 270)):
        for i in range(seg + 1):
            a = math.radians(a0 + 90 * i / seg)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def loft(bm, rings):
    """Bridge equal-length CCW rings with quads; caps close the ends. Winding is outward by construction
    (rings ordered bottom-to-top on the outside), so no normal recalculation is needed."""
    vs = [[bm.verts.new(p) for p in ring] for ring in rings]
    n = len(rings[0])
    for a, b in zip(vs, vs[1:]):
        for i in range(n):
            bm.faces.new([a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]])
    bm.faces.new(vs[0][::-1])
    bm.faces.new(vs[-1])


def finish_object(bm, name, label_rect=None):
    """Triangulate, recalc normals, write UV maps, link the object. label_rect = (x0, x1, z0, z1) in
    meters on the front (-Y) face; front faces map that rect to 0..1 in UVMap_Label."""
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.triangulate(bm, faces=bm.faces, quad_method="FIXED", ngon_method="EAR_CLIP")
    uv_main = bm.loops.layers.uv.new(UV_MAIN)
    uv_label = bm.loops.layers.uv.new(UV_LABEL)
    for f in bm.faces:
        nx, ny, nz = (abs(c) for c in f.normal)
        axes = (1, 2) if nx >= max(ny, nz) else ((0, 2) if ny >= nz else (0, 1))  # box projection, 1 UV unit = 1 m
        front = label_rect and f.normal.y < -0.5
        for loop in f.loops:
            co = loop.vert.co
            loop[uv_main].uv = (co[axes[0]], co[axes[1]])
            if front:
                x0, x1, z0, z1 = label_rect
                loop[uv_label].uv = ((co.x - x0) / (x1 - x0), (co.z - z0) / (z1 - z0))
            else:
                loop[uv_label].uv = LABEL_OFF
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    me.set_sharp_from_angle(angle=math.radians(40))  # rounded corners smooth, box edges/rims hard
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def material(name, rgba, alpha=1.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*rgba[:3], alpha)
    return mat


def mesh_stats(obj):
    me = obj.data
    tris = sum(len(p.vertices) - 2 for p in me.polygons)
    xs, ys, zs = zip(*(v.co for v in me.vertices))
    h = hashlib.sha256()
    for v in me.vertices:
        h.update(("%.6f,%.6f,%.6f;" % tuple(v.co)).encode())
    for p in me.polygons:
        h.update((",".join(map(str, p.vertices)) + ";").encode())
    return {
        "tris": tris,
        "verts": len(me.vertices),
        "size_m_unity_xyz": [round(max(xs) - min(xs), 5), round(max(zs) - min(zs), 5), round(max(ys) - min(ys), 5)],
        "uv_maps": [uv.name for uv in me.uv_layers],
        "geometry_sha256": h.hexdigest()[:16],
    }
