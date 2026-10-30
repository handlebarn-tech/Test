"""Packaged-product base: shape "box" (carton or tin, optional telescoping lid) or "pouch" (stand-up
gusseted bag with a flat heat-seal strip). Printed art goes through UVMap_Label on the front (-Y) face.
No package evidence exists in References/; every dimension is a placeholder carrying a GAP id."""
import math

import bmesh

from proclib import finish_object, loft, material, rounded_rect


def _box(p, lod):
    w, d, h, r = p["width_m"], p["depth_m"], p["height_m"], p["edge_radius_m"]
    seg = lod["corner_segments"]
    ring = lambda inset, z: [(x, y, z) for x, y in rounded_rect(w, d, r, seg, inset)]
    bm = bmesh.new()
    loft(bm, [ring(0, 0), ring(0, h)])
    parts = [("Body", bm)]
    lid = p["lid"]
    if lid["enabled"]:
        bm = bmesh.new()
        o = lid["overhang_m"]
        loft(bm, [ring(-o, h - lid["height_m"]), ring(-o, h + o)])
        parts.append(("Lid", bm))
    o = lid["overhang_m"] if lid["enabled"] else 0.0
    return parts, (w + 2 * o, h + o, d + 2 * o)


def _pouch(p, lod):
    w, h, g = p["width_m"], p["height_m"], p["gusset_depth_m"]
    hb, st, e = h - p["seal_height_m"], p["seal_thickness_m"], p["squareness"]
    n, rings = lod["around"], lod["rings"]
    sgn = lambda v: math.copysign(abs(v) ** e, v)

    def ring(half_depth, z):
        a = [2 * math.pi * i / n for i in range(n)]
        return [(w / 2 * sgn(math.cos(t)), max(half_depth, st / 2) * sgn(math.sin(t)), z) for t in a]

    # Gusset bulge: full depth at the base, easing to the seal thickness where the seal starts.
    body = [ring(g / 2 * (1 - (k / rings) ** 2), hb * k / rings) for k in range(rings + 1)]
    bm = bmesh.new()
    loft(bm, body + [ring(0, h)])
    return [("Body", bm)], (w, h, max(g, st))


def build(p, lod):
    parts, expected = (_box if p["shape"] == "box" else _pouch)(p, lod)
    lr = p["label"]
    rect = (-lr["width_m"] / 2, lr["width_m"] / 2, lr["bottom_m"], lr["bottom_m"] + lr["height_m"])
    objs = {}
    for name, bm in parts:
        objs[name] = finish_object(bm, name, label_rect=rect if name == "Body" else None)
        objs[name].data.materials.append(material("M_Proc_Pack" + name, p["preview_rgb"]))
    return objs, expected, {"shape": p["shape"]}
