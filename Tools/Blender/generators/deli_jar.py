"""Deli flower jar: square acrylic canister with rounded vertical edges, slip-on lid, front label card.
Shape evidence: REFERENCES_INDEX §photos 01/07/11 (square, clear, lidded, label card on the front).
Every dimension is a placeholder carrying a GAP id in the params file."""
import bmesh

from proclib import finish_object, loft, material, rounded_rect


def build(p, lod):
    b, lid, lab = p["body"], p["lid"], p["label"]
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

    top = h
    if lid["enabled"]:
        bm = bmesh.new()
        o, lh, lb = lid["overhang_m"], lid["height_m"], lid["top_bevel_m"]
        loft(bm, [ring(-o, h), ring(-o, h + lh - lb), ring(-o + lb, h + lh)])
        objs["Lid"] = finish_object(bm, "Lid")
        objs["Lid"].data.materials.append(material("M_Proc_JarLid", (0.04, 0.04, 0.04)))
        top = h + lh

    # Label card: one quad just proud of the flat front face; UVMap_Label spans 0..1.
    lw, lh2, z0 = lab["width_m"], lab["height_m"], lab["bottom_m"]
    if lw > w - 2 * r or z0 + lh2 > h:
        raise ValueError("label does not fit the flat front face")
    y = -d / 2 - lab["offset_m"]
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in ((-lw / 2, y, z0), (lw / 2, y, z0), (lw / 2, y, z0 + lh2), (-lw / 2, y, z0 + lh2))]
    bm.faces.new(vs)
    objs["Label"] = finish_object(bm, "Label", label_rect=(-lw / 2, lw / 2, z0, z0 + lh2))
    objs["Label"].data.materials.append(material("M_Proc_JarLabel", (0.95, 0.95, 0.95)))

    # Interior cavity for the gameplay fill-level system (FlowerVolume), Unity axes.
    interior = {"floor_y_m": b["floor_m"], "top_y_m": h, "size_x_m": w - 2 * t, "size_z_m": d - 2 * t}
    o = lid["overhang_m"] if lid["enabled"] else 0.0
    expected = (w + 2 * o, top, d + o + max(o, lab["offset_m"]))
    return objs, expected, {"interior": interior}
