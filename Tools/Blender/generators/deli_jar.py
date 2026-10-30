"""Deli flower jar (DEC-042/043): tall square clear acrylic canister with rounded vertical edges, white push-button
(pop-top) lid, coloured base band per brand, front strain/brand label card and a THC % tag.
Shape evidence: Nolan's photos References/Incoming "deli jar wall (retail)" and "deli jars + scale (office)" 2026-10-29.
Every dimension is a placeholder carrying a GAP id in the params file. Another jar type (e.g. the house-smalls jar,
DEC-042a) is another params file for this generator; disable the parts it lacks."""
import bmesh

from proclib import finish_object, loft, material, rounded_rect


def card(name, x0, x1, z0, z1, y, rgba):
    """One quad facing -Y (front) at depth y; UVMap_Label spans 0..1 for the texture."""
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in ((x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1))]
    bm.faces.new(vs)
    obj = finish_object(bm, name, label_rect=(x0, x1, z0, z1))
    obj.data.materials.append(material("M_Proc_Jar" + name, rgba))
    return obj


def build(p, lod):
    b, lid, lab, band, tag = p["body"], p["lid"], p["label"], p["band"], p["thc_tag"]
    w, d, h, r = b["width_m"], b["depth_m"], b["height_m"], b["corner_radius_m"]
    seg = lod["corner_segments"]
    ring = lambda inset, z: [(x, y, z) for x, y in rounded_rect(w, d, r, seg, inset)]
    objs = {}

    # Glass: closed shell with wall + floor thickness so the inside reads through clear material.
    bm = bmesh.new()
    c, t = b["base_chamfer_m"], b["wall_m"]
    loft(bm, [ring(c, 0), ring(0, c), ring(0, h), ring(t, h), ring(t, b["floor_m"])])
    objs["Glass"] = finish_object(bm, "Glass")
    objs["Glass"].data.materials.append(material("M_Proc_JarGlass", (0.75, 0.85, 0.9), 0.25))

    top, o = h, 0.0
    if lid["enabled"]:
        # Pop-top lid: slab with a bevelled top edge and a shallow recessed push button in the middle.
        bm = bmesh.new()
        o, lh, lb = lid["overhang_m"], lid["height_m"], lid["top_bevel_m"]
        bi, bd, br = lid["button_inset_m"], lid["button_depth_m"], lid["button_corner_m"]
        button = lambda z: [(x, y, z) for x, y in rounded_rect(w - 2 * bi, d - 2 * bi, br, seg)]  # own radius: inset > r
        loft(bm, [ring(-o, h), ring(-o, h + lh - lb), ring(-o + lb, h + lh), button(h + lh), button(h + lh - bd)])
        objs["Lid"] = finish_object(bm, "Lid")
        objs["Lid"].data.materials.append(material("M_Proc_JarLid", lid["rgba"]))
        top = h + lh

    # Base band: opaque coloured sleeve round the bottom (brand colour). Its front face carries UVMap_Label 0..1 for
    # the brand print; the inner cap sits inside the solid glass floor.
    bo = 0.0
    if band["enabled"]:
        bo, bh = band["offset_m"], band["height_m"]
        bm = bmesh.new()
        loft(bm, [ring(-bo, 0), ring(-bo, bh), ring(0, bh), ring(0, c + 0.001)])
        objs["Band"] = finish_object(bm, "Band", label_rect=(-w / 2 + r, w / 2 - r, 0, bh))
        objs["Band"].data.materials.append(material("M_Proc_JarBand", band["rgba"]))

    # Label card (strain/brand) and THC % tag: quads just proud of the flat front face, above the band.
    flat = w / 2 - r
    front = 0.0
    for name, q in (("Label", lab), ("ThcTag", tag)):
        if not q["enabled"]:
            continue
        x0, x1 = q["center_x_m"] - q["width_m"] / 2, q["center_x_m"] + q["width_m"] / 2
        z0, z1 = q["bottom_m"], q["bottom_m"] + q["height_m"]
        if x0 < -flat or x1 > flat or z1 > h or (band["enabled"] and z0 < band["height_m"]):
            raise ValueError(f"{name} does not fit the flat front face above the band")
        objs[name] = card(name, x0, x1, z0, z1, -d / 2 - q["offset_m"], q["rgba"])
        front = max(front, q["offset_m"])

    # Interior cavity for the gameplay fill-level system (FlowerVolume), Unity axes.
    interior = {"floor_y_m": b["floor_m"], "top_y_m": h, "size_x_m": w - 2 * t, "size_z_m": d - 2 * t}
    side = max(o, bo)
    expected = (w + 2 * side, top, d + side + max(side, front))
    return objs, expected, {"interior": interior}
