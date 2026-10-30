"""Packaged-goods family (PROC-004, DEC-034): prepack flower, prerolls, vapes, edibles, extracts, beverages, topicals
and merch. One params file lists the items; each item is one asset of parts, each part a loft of rings along +Z
(profile = [[width, depth, z], ...]): "round" rings are superellipses (squareness 1 = ellipse, <1 = squarer pouch),
"rrect" rings are rounded rectangles. Origin = bottom centre, front = -Y.
Label: front faces inside the item's label rectangle get the neutral `Label` material slot and map to 0..1 in
UVMap_Label. Placeholder only: no logos, trademarks or text (brand names are an open IP question, GAP-PROC-11).
The far LOD (`far: true`) is one block at the item's full extents in the brand colour (ASSET_PRODUCTION_PLAN §20)."""
import math

import bmesh

from proclib import finish_object, loft, material, rounded_rect


def variants(p):
    for item in p["items"]:
        q = {k: v for k, v in p.items() if k != "items"}
        q.update(item)
        yield "PROC_Pkg_" + item["id"], q


def ring(part, lod, w, d, z):
    if part["ring"] == "rrect":
        return [(x, y, z) for x, y in rounded_rect(w, d, part["corner_m"], lod["corner_segments"])]
    n, e = lod["around"], part.get("squareness", 1.0)
    sgn = lambda v: math.copysign(abs(v) ** e, v)
    return [(w / 2 * sgn(math.cos(t)), d / 2 * sgn(math.sin(t)), z) for t in (2 * math.pi * i / n for i in range(n))]


def cut(profile, zs):
    """Insert interpolated rings at heights zs, so the label edges fall on face boundaries."""
    out = [profile[0]]
    for a, b in zip(profile, profile[1:]):
        for z in sorted(zs, reverse=b[2] < a[2]):
            if min(a[2], b[2]) < z < max(a[2], b[2]):
                t = (z - a[2]) / (b[2] - a[2])
                out.append([u + t * (v - u) for u, v in zip(a, b)])
        out.append(b)
    return out


def rgba(p, key):
    c = p["brand_rgb"] if key == "brand" else p["colors"][key]
    return c[:3], (c[3] if len(c) > 3 else 1.0)


def build(p, lod):
    if lod["around"] % 4:
        raise ValueError("around must be a multiple of 4 so the ring touches the bounding box on both axes")
    pts = [r for q in p["parts"] for r in q["profile"]]
    w, d, h = (max(r[i] for r in pts) for i in range(3))
    if min(r[2] for r in pts) != 0:
        raise ValueError("profiles must start at z = 0 (bottom-centre origin)")
    parts = p["parts"]
    if lod.get("far"):
        parts = [dict(parts[0], name="Body", color="brand", profile=[[w, d, 0.0], [w, d, h]])]
    lab = p.get("label")
    rect = lab and (-lab["width_m"] / 2, lab["width_m"] / 2, lab["bottom_m"], lab["bottom_m"] + lab["height_m"])
    objs = {}
    for q in parts:
        labelled = lab and q["name"] == lab["part"]
        prof = cut(q["profile"], rect[2:]) if labelled and not lod.get("far") else q["profile"]
        bm = bmesh.new()
        loft(bm, [ring(q, lod, *r) for r in prof])
        obj = objs[q["name"]] = finish_object(bm, q["name"], label_rect=rect if labelled else None)
        obj.data.materials.append(material("M_Proc_Pkg_" + q["color"], *rgba(p, q["color"])))
        if labelled and not lod.get("far"):
            obj.data.materials.append(material("M_Proc_PkgLabel", p["colors"]["label"]))
            x0, x1, z0, z1 = rect
            hits = 0
            for f in obj.data.polygons:
                c = f.center
                if f.normal.y < -0.5 and x0 <= c.x <= x1 and z0 <= c.z <= z1:
                    f.material_index, hits = 1, hits + 1
            if not hits:
                raise ValueError(f"{p['id']}: label rectangle covers no front face of {q['name']}")
    return objs, (w, h, d), {"category": p["category"], "own_sheet": True}
