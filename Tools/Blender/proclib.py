"""Shared helpers for headless procedural generators (PROC-001, PROC-005). Blender units = meters, Z-up;
the FBX export converts to Unity's Y-up. See Docs/Assets/Specs/PROC_PIPELINE.md."""
import hashlib
import math

import bmesh
import bpy
from mathutils import Matrix, Vector

UV_MAIN = "UVMap_Main"
UV_LABEL = "UVMap_Label"
LABEL_OFF = (-8.0, -8.0)  # UVMap_Label value for faces outside the label region (shader masks it)
FT, INCH = 0.3048, 0.0254


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
    """Triangulate, write UV maps, link the object. label_rect = (x0, x1, z0, z1) in
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


def material(name, rgba, alpha=None):
    """Create/reuse a preview material; alpha defaults to rgba[3] (round-2 patch, C7)."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if alpha is None:
        alpha = rgba[3] if len(rgba) > 3 else 1.0
    mat.diffuse_color = (*rgba[:3], alpha)
    return mat


def mesh_stats(obj):
    me = obj.data
    if not me.vertices:
        raise ValueError(f"{obj.name}: empty mesh")
    tris = sum(len(p.vertices) - 2 for p in me.polygons)
    xs, ys, zs = zip(*(v.co for v in me.vertices))
    h = hashlib.sha256()
    for v in me.vertices:
        h.update(("%.6f,%.6f,%.6f;" % tuple(v.co)).encode())
    for p in me.polygons:
        h.update((",".join(map(str, p.vertices)) + ";").encode())
    q = bmesh.new()
    q.from_mesh(me)
    non_manifold = sum(1 for e in q.edges if not e.is_manifold)  # diagnostic only (DEC-086): touching parts trip it
    degenerate = sum(1 for f in q.faces if f.calc_area() <= 1e-12)
    q.free()
    return {
        "tris": tris,
        "verts": len(me.vertices),
        "size_m_unity_xyz": [round(max(xs) - min(xs), 5), round(max(zs) - min(zs), 5), round(max(ys) - min(ys), 5)],
        "bounds_m_blender_xyz": {"min": [round(min(c), 6) for c in (xs, ys, zs)],
                                 "max": [round(max(c), 6) for c in (xs, ys, zs)]},
        "uv_maps": [uv.name for uv in me.uv_layers],
        "material_slots": [m.name if m else None for m in me.materials],
        "geometry": {"non_manifold_edges": non_manifold, "degenerate_faces": degenerate},
        "geometry_sha256": h.hexdigest()[:16],
    }


# --- PROC-005 fixture toolkit (adapted from the IMP-003 drops; see PROC_PIPELINE "Fixture toolkit") ---------------

def ft(v):
    return float(v) * FT


def inch(v):
    return float(v) * INCH


def to_unity(x, y, z):
    """Blender point -> Unity local point. FBX export: Blender (x, y, z) -> FBX (x, z, -y); Unity's importer negates X."""
    return [round(-x + 0.0, 6), round(z + 0.0, 6), round(-y + 0.0, 6)]


def collision_box(name, center, size):
    """Manifest collision box (DEC-086 R1a): Blender centre/size in, Unity centre/size out. Unity adds BoxColliders."""
    sx, sy, sz = size
    return {"name": name, "center_unity_xyz": to_unity(*center), "size_unity_xyz": [round(sx, 6), round(sz, 6), round(sy, 6)]}


def hinge_axis(part, x, y, z0, z1, side, open_deg=110):
    """Vertical door hinge (C10). part = object part name; side = 'left'/'right' as seen from the front."""
    return {"part": part, "type": "hinge", "side": side, "pivot_unity_xyz": to_unity(x, y, (z0 + z1) / 2),
            "axis_unity_xyz": [0.0, 1.0, 0.0], "open_deg": open_deg}


def slide_axis(part, travel_m, direction=(0.0, -1.0, 0.0)):
    """Drawer/sliding-panel travel (C10). direction is Blender; default pulls toward the front (-Y)."""
    return {"part": part, "type": "slide", "axis_unity_xyz": to_unity(*direction), "travel_m": round(travel_m, 6)}


class Parts:
    """Collects one bmesh per part (one material slot each) and finishes them into objects."""

    def __init__(self, colors=None):
        self.colors, self._p = colors or {}, {}

    def __call__(self, name, mat, rgba=None, label_rect=None):
        if name not in self._p:
            self._p[name] = [bmesh.new(), mat, rgba if rgba is not None else self.colors[mat], label_rect]
        return self._p[name][0]

    def finish(self):
        objs = {}
        for name, (bm, mat, rgba, rect) in self._p.items():
            if not bm.verts:
                bm.free()
                continue
            objs[name] = finish_object(bm, name, label_rect=rect)
            objs[name].data.materials.append(material("M_Proc_" + mat, rgba))
        return objs


def _basis(axis):
    """Deterministic perpendicular frame (C11): ring angle 0 lies on u, so with segments % 4 == 0 the extents along
    both perpendicular world axes are exact for axis-aligned cylinders."""
    a = Vector(axis).normalized()
    ref = Vector((0, 0, 1)) if abs(a.z) < 0.9 else Vector((1, 0, 0))
    u = ref.cross(a).normalized()
    return a, u, a.cross(u)


def _check_segments(segments):
    if segments < 6 or segments % 2:
        raise ValueError(f"cylinder segments must be even and >= 6 (C11), got {segments}")


def add_box(bm, size, center=(0.0, 0.0, 0.0)):
    """Axis-aligned box baked into bm (no object transform)."""
    sx, sy, sz = (float(v) for v in size)
    if min(sx, sy, sz) <= 0:
        raise ValueError(f"box dimensions must be > 0, got {size}")
    verts = bmesh.ops.create_cube(bm, size=1.0)["verts"]
    for v in verts:
        v.co = Vector((v.co.x * sx + center[0], v.co.y * sy + center[1], v.co.z * sz + center[2]))
    return verts


def add_beveled_box(bm, size, center=(0.0, 0.0, 0.0), corner=0.004, bevel=0.002, seg=1):
    """Manufactured box: rounded vertical corners plus a chamfer on the top and bottom edges; exact outer size."""
    w, d, h = (float(v) for v in size)
    if min(w, d, h) <= 0:
        raise ValueError(f"beveled box dimensions must be > 0, got {size}")
    b = max(0.0, min(float(bevel), min(w, d, h) * 0.24))
    r = max(0.0, min(float(corner), min(w, d) * 0.49))
    z0, z1 = center[2] - h / 2, center[2] + h / 2
    spec = [(w, d, z0), (w, d, z1)] if b <= 0 else [
        (w - 2 * b, d - 2 * b, z0), (w, d, z0 + b), (w, d, z1 - b), (w - 2 * b, d - 2 * b, z1)]
    loft(bm, [[(x + center[0], y + center[1], z) for x, y in rounded_rect(rw, rd, min(r, rw / 2, rd / 2), max(1, seg))]
              for rw, rd, z in spec])


def add_lathe(bm, base, axis, profile, segments):
    """Surface of revolution: profile = [(radius, t), ...] along axis from base; radius 0 makes a pole. Order the
    profile so the solid is on its left walking along it (outside going up), and the normals face outward."""
    _check_segments(segments)
    a, u, v = _basis(axis)
    base = Vector(base)
    rings = []
    for r, t in profile:
        c = base + a * t
        if r <= 1e-9:
            rings.append([bm.verts.new(c)])
        else:
            rings.append([bm.verts.new(c + (u * math.cos(k) + v * math.sin(k)) * r)
                          for k in (2 * math.pi * i / segments for i in range(segments))])
    for ra, rb in zip(rings, rings[1:]):
        if len(ra) == 1 and len(rb) == 1:
            continue
        for i in range(segments):
            j = (i + 1) % segments
            if len(ra) == 1:
                bm.faces.new([ra[0], rb[j], rb[i]])
            elif len(rb) == 1:
                bm.faces.new([ra[i], ra[j], rb[0]])
            else:
                bm.faces.new([ra[i], ra[j], rb[j], rb[i]])


def add_cylinder_between(bm, a, b, radius, segments=8, caps=True):
    """Capped cylinder from a to b with a deterministic ring roll (C11)."""
    a, b = Vector(a), Vector(b)
    length = (b - a).length
    if length <= 1e-9 or radius <= 0:
        raise ValueError("cylinder needs distinct endpoints and radius > 0")
    prof = [(radius, 0.0), (radius, length)]
    add_lathe(bm, a, b - a, [(0, 0.0)] + prof + [(0, length)] if caps else prof, segments)


def add_vertical_cylinder(bm, x, y, z0, z1, radius, segments=8):
    add_cylinder_between(bm, (x, y, z0), (x, y, z1), radius, segments)


def circle_profile(radius, segments):
    _check_segments(segments)
    return [(radius * math.cos(2 * math.pi * i / segments), radius * math.sin(2 * math.pi * i / segments))
            for i in range(segments)]


def rect_profile(w, h, r=0.0, seg=0):
    return rounded_rect(w, h, r, seg)


def fillet(points, radius, steps):
    """Round the interior corners of a polyline with circular arcs (steps segments each)."""
    pts = [Vector(p) for p in points]
    out = [pts[0]]
    for p0, p1, p2 in zip(pts, pts[1:], pts[2:]):
        d0, d1 = (p0 - p1).normalized(), (p2 - p1).normalized()
        ang = d0.angle(d1)
        if radius <= 0 or steps < 1 or ang > math.pi - 1e-4:
            out.append(p1)
            continue
        cut = min(radius / math.tan(ang / 2), (p0 - p1).length * 0.49, (p2 - p1).length * 0.49)
        a, b = p1 + d0 * cut, p1 + d1 * cut
        for i in range(steps + 1):  # quadratic Bezier through the corner: close to an arc, always tangent
            t = i / steps
            out.append(a * (1 - t) ** 2 + p1 * 2 * t * (1 - t) + b * t * t)
    out.append(pts[-1])
    return out


def add_sweep(bm, path, profile, closed=False, caps=True):
    """Sweep a 2D profile loop (CCW, around the path) along a 3D polyline with exact mitred joints and
    parallel-transported frames: wires, tube frames, handles, rails, mouldings."""
    pts = [Vector(p) for p in path]
    n = len(pts)
    if n < 2:
        raise ValueError("sweep path needs 2+ points")
    seg = [(pts[(i + 1) % n] - pts[i]).normalized() for i in range(n if closed else n - 1)]
    _, u, v = _basis(seg[0])
    frames, rings = [], []
    for i in range(len(seg)):
        if i:
            rot = seg[i - 1].rotation_difference(seg[i])
            u, v = rot @ u, rot @ v
        frames.append((u.copy(), v.copy()))
    for i in range(n):
        if closed or 0 < i < n - 1:
            t_in, t_out = seg[i - 1], seg[i % len(seg)]
            fu, fv = frames[i - 1]
            bis = (t_in + t_out).normalized()
        else:
            t_in = seg[0] if i == 0 else seg[-1]
            fu, fv = frames[0] if i == 0 else frames[-1]
            bis = t_in
        ring = []
        for pu, pv in profile:
            off = fu * pu + fv * pv
            s = -off.dot(bis) / t_in.dot(bis)
            ring.append(bm.verts.new(pts[i] + off + t_in * s))
        rings.append(ring)
    m = len(profile)
    pairs = list(zip(rings, rings[1:])) + ([(rings[-1], rings[0])] if closed else [])
    for ra, rb in pairs:
        for k in range(m):
            bm.faces.new([ra[k], ra[(k + 1) % m], rb[(k + 1) % m], rb[k]])
    if caps and not closed:
        bm.faces.new(rings[0][::-1])
        bm.faces.new(rings[-1])


def add_tube(bm, path, radius, segments=8, closed=False, bend_radius=0.0, bend_steps=0):
    """Round tube along a polyline, optionally with filleted bends."""
    pts = fillet(path, bend_radius, bend_steps) if bend_radius > 0 and not closed else path
    add_sweep(bm, pts, circle_profile(radius, segments), closed=closed)


def add_handle_pull(bm, center, width, stand_off, radius, segments=8, axis="x", bend_steps=3):
    """Bent round-bar pull on a -Y face: two legs from the face (y = center y) out to the grip, filleted bends (C8/K2)."""
    cx, cy, cz = center
    if axis == "x":
        path = [(cx - width / 2, cy, cz), (cx - width / 2, cy - stand_off, cz),
                (cx + width / 2, cy - stand_off, cz), (cx + width / 2, cy, cz)]
    else:  # vertical pull
        path = [(cx, cy, cz - width / 2), (cx, cy - stand_off, cz - width / 2),
                (cx, cy - stand_off, cz + width / 2), (cx, cy, cz + width / 2)]
    add_tube(bm, path, radius, segments, bend_radius=min(stand_off * 0.6, width * 0.25), bend_steps=bend_steps)
    for x, y, z in (path[0], path[-1]):  # rose plates at the face
        add_cylinder_between(bm, (x, y + 0.0005, z), (x, y - radius * 0.8, z), radius * 1.8, segments)


def add_wire_grid(bm, width, depth, z, wire_d, spacing_x, spacing_y, segments=6, center=(0.0, 0.0)):
    """Round-wire grid (C9): wires along Y every spacing_x, wires along X every spacing_y (None = no wires that way).
    The two layers are stacked (welded on top of each other) like a real wire deck."""
    r = wire_d / 2
    xs = even_positions(width, spacing_x) if spacing_x else []
    ys = even_positions(depth, spacing_y) if spacing_y else []
    for x in xs:
        add_cylinder_between(bm, (center[0] + x, center[1] - depth / 2, z + r), (center[0] + x, center[1] + depth / 2, z + r), r, segments)
    for y in ys:
        add_cylinder_between(bm, (center[0] - width / 2, center[1] + y, z - r), (center[0] + width / 2, center[1] + y, z - r), r, segments)


def even_positions(length, spacing):
    """Centred positions across length, ends included, pitch as close to spacing as fits."""
    n = max(1, round(length / spacing))
    return [-length / 2 + length * i / n for i in range(n + 1)]


def wear(p):
    """Per-instance wear params for the Unity material builder (Q0.4), deterministic from the asset seed."""
    w = dict(p.get("wear", {}))
    if not w:
        return {}
    w["seed"] = int(p["seed"])
    return {"wear": w}
