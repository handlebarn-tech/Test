"""Janitor closet props (PROC-005 §11; IMP-003 drop 3 rewritten; the supply rack is a wire_shelving variant, J2):
mop sink (RF MopSink_JC 1.6 x 1.5 x 1.0 ft: moulded basin with a real cavity, drain grate, stainless splash guards on
the two wall sides), mops + brooms on a wall holder rail (RF Mops_Brooms_JC 0.8 x 1.0 x 5.0 ft; string-mop strands,
broom bristle tufts), mop bucket with wringer on casters (hollow). Every asset has manifest collision boxes (J3).
Part sizes are GAP-PROC-21. Origin = bottom centre, front = -Y, wall = +Y. LOD0 full; LOD1 fewer strands/tufts;
LOD2 plain; LOD3 blocks."""
import math

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_lathe, add_tube, collision_box, loft,
                     rounded_rect, wear)


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def _open_basin(bm, W, D, r, wall, z0, z1, floor_z, cs, yo=0.0):
    """Open-topped moulded tub: outer wall up, rim, inner wall down to the floor (no top cap)."""
    def ring(inset, z):
        return [(x, y + yo, z) for x, y in rounded_rect(W, D, r, cs, inset)]
    loft(bm, [ring(0, z0), ring(0, z1), ring(wall, z1), ring(wall * 1.6, floor_z)])


def mop_sink(P, p, d, s, W, D, H):
    k = p["sink"]
    hb, sg, wall = k["basin_h_m"], k["guard_h_m"], k["wall_m"]
    b = P("Basin", "Moulded_Stone")
    if d >= 3:
        add_box(b, (W, D, hb), (0, 0, hb / 2))
        add_box(P("Guards", "Stainless"), (W, 0.01, sg), (0, D / 2 - 0.005, hb + sg / 2))
        return {}
    _open_basin(b, W, D, 0.08, wall, 0, hb, 0.03, max(1, (4, 2, 1)[d]))  # corner r > insets keeps ring sizes equal
    if d <= 1:
        add_lathe(P("Grate", "Stainless"), (0, 0, 0), (0, 0, 1), [(0, 0.03), (0.05, 0.03), (0.05, 0.034), (0, 0.034)], s)
        if d == 0:
            for i in range(-3, 4):  # grate bars
                add_box(P("Grate", "Stainless"), (0.004, 0.08 * math.cos(math.asin(min(1, abs(i) / 3.5))), 0.003), (i * 0.012, 0, 0.0355))
    g = P("Guards", "Stainless")  # splash guards on the back and right walls, above the rim
    add_box(g, (W, 0.01, sg), (0, D / 2 - 0.005, hb + sg / 2))
    add_box(g, (0.01, D - 0.01, sg), (W / 2 - 0.005, -0.005, hb + sg / 2))
    return {"collision_boxes": [collision_box("Basin", (0, 0, hb / 2), (W, D, hb))]}


def mops_brooms(P, p, d, s, W, D, H):
    k = p["mops"]
    hr = k["handle_r_m"]
    rail_z = k["rail_z_m"]
    if d >= 3:
        add_box(P("Handles", "Handle_Wood"), (W, D, H), (0, 0, H / 2))
        return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    add_box(P("Rail", "Black_Plastic"), (W, 0.03, 0.04), (0, D / 2 - 0.015, rail_z))  # wall holder rail = x/back bound
    # string mop: handle, clamp, strands splayed to the floor
    mx, my = -W / 4, 0.0
    add_cylinder_between(P("Handles", "Handle_Wood"), (mx, my, 0.16), (mx, my, H - 0.1), hr, s)
    add_lathe(P("Clamp", "Black_Plastic"), (mx, my, 0), (0, 0, 1), [(0, 0.12), (0.03, 0.12), (0.03, 0.18), (0, 0.18)], s)
    n = (24, 10, 6)[d]
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = W / 4 - 0.012
        add_cylinder_between(P("MopHead", "Mop_Cotton"), (mx + 0.02 * math.cos(a), my + 0.02 * math.sin(a), 0.13),
                             (mx + rr * math.cos(a), my + rr * math.sin(a), 0.012), 0.008, 6)
    # broom: handle, head across the depth (y bound), bristle tufts
    bx = W / 4
    add_cylinder_between(P("Handles", "Handle_Wood"), (bx, 0, 0.1), (bx, 0, H), hr, s)
    add_beveled_box(P("BroomHead", "Black_Plastic"), (0.05, D, 0.04), (bx, 0, 0.1), corner=0.006, bevel=0.003 if d <= 1 else 0.0,
                    seg=2 if d == 0 else 1)
    if d <= 1:
        nt = 14 if d == 0 else 6
        for i in range(nt):
            tw = (D - 0.03) / nt * 0.8
            y = -D / 2 + 0.015 + tw / 2 + (D - 0.03 - tw) * i / (nt - 1)
            add_box(P("Bristles", "Bristle_Red"), (0.04, tw, 0.08), (bx, y, 0.04))
    else:
        add_box(P("Bristles", "Bristle_Red"), (0.04, D - 0.03, 0.08), (bx, 0, 0.04))
    return {"collision_boxes": [collision_box("Mop", (mx, my, H / 2), (W / 2, W / 2, H)), collision_box("Broom", (bx, 0, H / 2), (0.05, D, H))]}


def bucket(P, p, d, s, W, D, H):
    k = p["bucket"]
    bh, ch = k["bucket_h_m"], k["caster_h_m"]
    b = P("Bucket", "Bucket_Yellow")
    if d >= 3:
        add_box(b, (W, D, bh), (0, 0, ch + bh / 2))
        add_box(P("Wringer", "Plastic_Grey"), (W * 0.6, D * 0.5, H - ch - bh), (0, D * 0.15, ch + bh + (H - ch - bh) / 2))
        add_box(P("Casters", "Black_Plastic"), (W - 0.1, D - 0.1, ch), (0, 0, ch / 2))
        return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    cs = max(1, (4, 2, 1)[d])

    def ring(w, dd, inset, z):
        return [(x, y, z) for x, y in rounded_rect(w, dd, 0.05, cs, inset)]
    loft(b, [ring(W - 0.04, D - 0.04, 0, ch), ring(W, D, 0, ch + bh), ring(W, D, 0.006, ch + bh), ring(W - 0.04, D - 0.04, 0.006, ch + 0.01)])
    for sx in (-1, 1):  # casters
        for sy in (-1, 1):
            add_lathe(P("Casters", "Black_Plastic"), (sx * (W / 2 - 0.06) - 0.01, sy * (D / 2 - 0.06), ch / 2), (1, 0, 0),
                      [(0, 0), (ch / 2, 0), (ch / 2, 0.02), (0, 0.02)], s)
    w = P("Wringer", "Plastic_Grey")  # side-press wringer on the back rim, lever handle up to H
    zw = ch + bh
    add_beveled_box(w, (W * 0.6, D * 0.45, 0.18), (0, D * 0.2, zw + 0.06), corner=0.02, bevel=0.005 if d <= 1 else 0.0, seg=cs)
    add_tube(P("Lever", "Chrome"), [(-W * 0.25, D * 0.35, zw + 0.12), (-W * 0.25, D * 0.35, H - 0.012), (W * 0.25, D * 0.35, H - 0.012),
                                    (W * 0.25, D * 0.35, zw + 0.12)], 0.012, 8, bend_radius=0.04 if d <= 1 else 0, bend_steps=3 if d <= 1 else 0)
    if d <= 1:  # bail handle
        add_tube(P("Lever", "Chrome"), [(-W / 2 + 0.004, -D * 0.1, zw - 0.02), (-W / 2 + 0.04, -D * 0.3, zw + 0.08), (W / 2 - 0.04, -D * 0.3, zw + 0.08),
                                        (W / 2 - 0.004, -D * 0.1, zw - 0.02)], 0.004, 6, bend_radius=0.03, bend_steps=2)
    return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


KINDS = {"mop_sink": mop_sink, "mops_brooms": mops_brooms, "bucket": bucket}


def build(p, lod):
    P = Parts(p["colors"])
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"], W, D, H)
    extra = dict(extra, fixture_family="janitor_props", rf=p["rf"], seed=int(p["seed"]))
    extra.update(wear(p))
    return P.finish(), (W, H + p.get("extra_h_m", 0.0), D), extra
