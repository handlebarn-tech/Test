"""Janitor closet props (PROC-005 §11; fix wave REVIEW-PROC5 #1/#5; the supply rack is a wire_shelving variant, J2).
DEC-062 lists the closet as: a drainage (mop) sink, mops and brooms, a small rack of cleaning supplies. GAP-109: no
imagery, so every colour and material here is a neutral-grey GAP-PROC-30 placeholder.
- mop sink (RF MopSink_JC 1.6 x 1.5 x 1.0 ft, "square mop sink"): moulded basin with a bullnose rim, drafted walls,
  real cavity sloping to a drain with a barred strainer; splash guards (GAP-PROC-21) with hemmed edges and screws.
- mops + brooms (RF Mops_Brooms_JC 0.8 x 1.0 x 5.0 ft, DEC-062): wall holder rail with bracket arms and spring-grip
  rollers, string mop (clamp head, headband, splayed strands), upright broom (block, ferrule, bristle tufts), hang caps.
- mop bucket with wringer: NOT in DEC-062 or RF; kept only as a labelled GAP-PROC-30 placeholder (neutral greys).
Every asset has manifest collision boxes (J3). Origin = bottom centre, front = -Y, wall = +Y. LOD0 full; LOD1 fewer
strands/tufts and coarser rounding; LOD2 plain; LOD3 blocks."""
import math
import random

from proclib import (Parts, add_box, add_cylinder_between, add_lathe, add_screw_head, add_tube, collision_box, loft,
                     rounded_rect, wear)
from generators.glass_door_cooler import rpanel


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def _profile_loft(bm, W, D, r, cs, prof, xo=0.0, yo=0.0):
    """Loft rounded-rect rings from (inset, z) pairs (outside going up, over the rim, inside going down)."""
    loft(bm, [[(x + xo, y + yo, z) for x, y in rounded_rect(W, D, r, cs, ins)] for ins, z in prof])


def mop_sink(P, p, d, s, W, D, H):
    k = p["sink"]
    hb, sg, wall = k["basin_h_m"], k["guard_h_m"], k["wall_m"]
    b = P("Basin", "Sink_Grey")
    if d >= 3:
        add_box(b, (W, D, hb), (0, 0, hb / 2))
        add_box(P("Guards", "Guard_Grey"), (W, 0.01, sg), (0, D / 2 - 0.005, hb + sg / 2))
        return {}
    cs = (5, 2, 1)[d]
    fl = 0.035  # basin floor at the wall
    if d <= 1:
        prof = [(0.012, 0.0), (0.012, 0.012), (0.004, 0.02), (0.0, 0.03), (0.0, hb - 0.018), (0.003, hb - 0.006),
                (0.009, hb - 0.0005), (0.014, hb), (wall - 0.012, hb), (wall - 0.006, hb - 0.004), (wall, hb - 0.016),
                (wall + 0.022, fl + 0.03), (wall + 0.03, fl + 0.008), (wall + 0.036, fl)]
    else:
        prof = [(0.0, 0.0), (0.0, hb), (wall, hb), (wall + 0.036, fl)]
    _profile_loft(b, W, D, 0.09, cs, prof)
    if d <= 1:  # drain: sloped sump ring, strainer with bars
        gr = P("Grate", "Fastener_Grey")
        add_lathe(b, (0, 0, fl - 0.012), (0, 0, 1), [(0, 0), (0.06, 0), (0.06, 0.012), (0, 0.012)], s)
        add_lathe(gr, (0, 0, 0), (0, 0, 1), [(0, fl - 0.002), (0.05, fl - 0.002), (0.05, fl + 0.002), (0.044, fl + 0.003), (0, fl + 0.003)], s)
        if d == 0:
            for i in range(-3, 4):
                add_box(gr, (0.004, 0.075 * math.cos(math.asin(min(1, abs(i) / 3.6))), 0.002), (i * 0.011, 0, fl + 0.004))
            add_lathe(gr, (0, 0, fl + 0.003), (0, 0, 1), [(0.008, 0), (0.008, 0.0025), (0, 0.0025)], 8)
    g = P("Guards", "Guard_Grey")  # splash guards on the back and right walls, tucked behind the rim
    z0 = hb - 0.02
    if d <= 1:
        rpanel(g, "-y", (0, D / 2 - 0.006, z0 + (sg + 0.02) / 2), W, sg + 0.02, 0.012, 0.004, 2 if d == 0 else 1, 0.006, 1)
        rpanel(g, "-x", (W / 2 - 0.006, -0.006, z0 + (sg + 0.02) / 2), D - 0.012, sg + 0.02, 0.012, 0.004, 2 if d == 0 else 1, 0.006, 1)
        if d == 0:
            sc = P("Screws", "Fastener_Grey")
            for x in (-W / 2 + 0.04, 0.0, W / 2 - 0.05):
                for z in (z0 + 0.06, hb + sg - 0.04):
                    add_screw_head(sc, (x, D / 2 - 0.012, z), (0, -1, 0), 0.005, 8)
            for y in (-D / 2 + 0.04, D / 2 - 0.06):
                for z in (z0 + 0.06, hb + sg - 0.04):
                    add_screw_head(sc, (W / 2 - 0.012, y, z), (-1, 0, 0), 0.005, 8)
    else:
        add_box(g, (W, 0.012, sg + 0.02), (0, D / 2 - 0.006, z0 + (sg + 0.02) / 2))
        add_box(g, (0.012, D - 0.012, sg + 0.02), (W / 2 - 0.006, -0.006, z0 + (sg + 0.02) / 2))
    return {"collision_boxes": [collision_box("Basin", (0, 0, hb / 2), (W, D, hb))]}


def _hang_cap(bm, x, y, z_top, hr, s):
    """Threaded hang cap on a handle top with a hanging-hole ring."""
    add_lathe(bm, (x, y, z_top - 0.05), (0, 0, 1), [(0, 0), (hr * 1.15, 0), (hr * 1.15, 0.04), (hr * 0.8, 0.05), (0, 0.05)], s)


def mops_brooms(P, p, d, s, W, D, H):
    k = p["mops"]
    hr, rail_z = k["handle_r_m"], k["rail_z_m"]
    rng = random.Random(int(p["seed"]))
    if d >= 3:
        add_box(P("Handles", "Handle_Grey"), (W, D, H), (0, 0, H / 2))
        return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    mx, bx = -W / 4, W / 4
    hold = P("Rail", "Holder_Grey")
    cs = 2 if d == 0 else 1
    # wall holder rail = back bound, bracket arms out to spring-grip rollers around each handle
    if d <= 1:
        rpanel(hold, "-y", (0, D / 2 - 0.012, rail_z), W, 0.05, 0.024, 0.006, cs, 0.01, cs)
        for x in (mx, bx):
            rpanel(hold, "+z", (x, (D / 2 - 0.024) / 2 + hr, rail_z + 0.008), 0.03, D / 2 - 0.024 - hr, 0.016, 0.004, cs, 0.006, cs)
            for sx in (-1, 1):  # rubber grip rollers either side of the handle
                add_cylinder_between(P("Grips", "Caster_Grey"), (x + sx * (hr + 0.007), 0.0, rail_z - 0.01),
                                     (x + sx * (hr + 0.007), 0.0, rail_z + 0.026), 0.007, s)
            add_box(hold, (2 * hr + 0.034, 0.012, 0.016), (x, hr + 0.012, rail_z + 0.008))  # clip bridge behind the handle
        if d == 0:
            for x in (-W / 2 + 0.015, W / 2 - 0.015):
                add_screw_head(P("Screws", "Fastener_Grey"), (x, D / 2 - 0.024, rail_z), (0, -1, 0), 0.004, 8)
    else:
        add_box(hold, (W, 0.024, 0.05), (0, D / 2 - 0.012, rail_z))
    hd = P("Handles", "Handle_Grey")
    # string mop: handle, clamp head, headband, strands splayed to the floor
    add_cylinder_between(hd, (mx, 0, 0.17), (mx, 0, H - 0.1), hr, s)
    if d <= 1:
        _hang_cap(P("Caps", "Holder_Grey"), mx, 0, H - 0.1 + 0.01, hr, s)
    clamp = P("Clamp", "Holder_Grey")
    add_lathe(clamp, (mx, 0, 0.12), (0, 0, 1), [(0, 0), (0.034, 0), (0.036, 0.012), (0.03, 0.04), (hr * 1.4, 0.06), (hr * 1.4, 0.07), (0, 0.07)], s)
    if d <= 1:  # jaw plate + wing screw
        rpanel(clamp, "-y", (mx, -0.032, 0.135), 0.05, 0.028, 0.008, 0.003, 1, 0.006, cs)
        add_cylinder_between(clamp, (mx, -0.036, 0.135), (mx, -0.05, 0.135), 0.004, 8)
        add_box(clamp, (0.03, 0.004, 0.012), (mx, -0.052, 0.135))
        add_lathe(P("MopHead", "MopHead_Grey"), (mx, 0, 0.1), (0, 0, 1), [(0, 0), (0.04, 0), (0.042, 0.01), (0.04, 0.025), (0, 0.025)], s)  # headband
    mh = P("MopHead", "MopHead_Grey")
    n = (64, 20, 8)[d]
    sr = 0.0055
    rr = W / 4 - sr - 0.002
    for i in range(n):
        a = 2 * math.pi * (i + rng.uniform(-0.3, 0.3)) / n
        reach = rr * rng.uniform(0.55, 1.0)
        ca, sa = math.cos(a), math.sin(a)
        if d <= 1:
            pts = [(mx + 0.025 * ca, 0.025 * sa, 0.11), (mx + 0.04 * ca, 0.04 * sa, 0.07),
                   (mx + reach * 0.8 * ca, reach * 0.8 * sa, sr + 0.012), (mx + reach * ca, reach * sa, sr + 0.0005)]
            add_tube(mh, pts, sr, 6, bend_radius=0.03, bend_steps=2 if d == 0 else 1)
        else:
            add_cylinder_between(mh, (mx + 0.02 * ca, 0.02 * sa, 0.12), (mx + reach * ca, reach * sa, sr + 0.0005), sr, 6)
    # broom: handle, ferrule, block across the depth (y bound), bristle tufts down to the floor
    add_cylinder_between(hd, (bx, 0, 0.12), (bx, 0, H - 0.05), hr, s)
    if d <= 1:
        _hang_cap(P("Caps", "Holder_Grey"), bx, 0, H, hr, s)
        add_lathe(P("BroomHead", "Holder_Grey"), (bx, 0, 0.12), (0, 0, 1), [(0, 0), (hr * 1.6, 0), (hr * 1.6, 0.03), (hr * 1.25, 0.05), (0, 0.05)], s)
        rpanel(P("BroomHead", "Holder_Grey"), "+z", (bx, 0, 0.1), 0.055, D, 0.04, 0.008, cs, 0.012, cs)
        bt = P("Bristles", "Bristle_Grey")
        nx, ny = (3, 18) if d == 0 else (2, 8)
        for ix in range(nx):
            for iy in range(ny):
                x = bx + (-0.017 + 0.034 * ix / (nx - 1))
                y = -D / 2 + 0.012 + (D - 0.024) * iy / (ny - 1)
                add_cylinder_between(bt, (x, y, 0.0), (x, y, 0.084), 0.0055 if d == 0 else 0.009, 6)
    else:
        add_cylinder_between(hd, (bx, 0, H - 0.05), (bx, 0, H), hr, s)
        add_box(P("BroomHead", "Holder_Grey"), (0.055, D, 0.04), (bx, 0, 0.1))
        add_box(P("Bristles", "Bristle_Grey"), (0.045, D - 0.02, 0.08), (bx, 0, 0.04))
    return {"collision_boxes": [collision_box("Mop", (mx, 0, H / 2), (W / 2, W / 2, H)), collision_box("Broom", (bx, 0, H / 2), (0.055, D, H))]}


def _caster(P, x, y, ch, s, d):
    """Swivel caster: top plate, swivel race, fork, wheel with tread and hub, axle; wheel bottom at z = 0."""
    wr = ch * 0.36
    c = P("Casters", "Caster_Grey")
    f = P("Forks", "Fastener_Grey")
    if d <= 1:
        add_lathe(c, (x - 0.009, y, wr), (1, 0, 0), [(0, 0), (wr * 0.45, 0), (wr * 0.92, 0.002), (wr, 0.006), (wr, 0.012),
                                                    (wr * 0.92, 0.016), (wr * 0.45, 0.018), (0, 0.018)], s)
        add_cylinder_between(f, (x - 0.014, y, wr), (x + 0.014, y, wr), 0.003, 8)
        for sx in (-1, 1):
            add_box(f, (0.0025, 0.02, ch - wr - 0.004), (x + sx * 0.0115, y, wr + (ch - wr - 0.004) / 2))
        add_lathe(f, (x, y, ch - 0.01), (0, 0, 1), [(0, 0), (0.016, 0), (0.016, 0.004), (0.012, 0.006), (0, 0.006)], s)
        add_box(f, (0.04, 0.04, 0.004), (x, y, ch - 0.002))
    else:
        add_box(c, (0.018, wr * 2, wr * 2), (x, y, wr))
        add_box(f, (0.03, 0.03, ch - wr * 2), (x, y, wr * 2 + (ch - wr * 2) / 2))


def bucket(P, p, d, s, W, D, H):
    k = p["bucket"]
    bh, ch = k["bucket_h_m"], k["caster_h_m"]
    b = P("Bucket", "Bucket_Grey")
    if d >= 3:
        add_box(b, (W, D, bh), (0, 0, ch + bh / 2))
        add_box(P("Wringer", "Wringer_Grey"), (W * 0.6, D * 0.5, H - ch - bh), (0, D * 0.15, ch + bh + (H - ch - bh) / 2))
        add_box(P("Casters", "Caster_Grey"), (W - 0.1, D - 0.1, ch), (0, 0, ch / 2))
        return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    cs = (4, 2, 1)[d]
    zt = ch + bh
    if d <= 1:  # drafted tub, moulded bumper band, rolled rim, inner wall down to the floor
        prof = [(0.03, ch), (0.024, ch + 0.03), (0.012, zt - 0.08), (0.004, zt - 0.075), (0.004, zt - 0.06), (0.009, zt - 0.055),
                (0.004, zt - 0.012), (0.0, zt - 0.005), (0.004, zt), (0.012, zt), (0.016, zt - 0.006), (0.04, ch + 0.01)]
    else:
        prof = [(0.03, ch), (0.0, zt), (0.008, zt), (0.04, ch + 0.01)]
    _profile_loft(b, W, D, 0.07, cs, prof)
    for sx in (-1, 1):
        for sy in (-1, 1):
            _caster(P, sx * (W / 2 - 0.07), sy * (D / 2 - 0.07), ch, s, d)
    w = P("Wringer", "Wringer_Grey")  # side-press wringer seated on the back rim, lever up to H
    zw = zt
    lv = P("Lever", "Lever_Grey")
    if d <= 1:
        rpanel(w, "+z", (0, D * 0.2, zw + 0.07), W * 0.6, D * 0.42, 0.16, 0.012, cs, 0.02, cs)
        rpanel(w, "-y", (0, D * 0.2 - D * 0.21 - 0.004, zw + 0.06), W * 0.5, 0.11, 0.012, 0.004, cs, 0.01, cs)  # press plate
        for sx in (-1, 1):  # rim hooks
            add_box(w, (0.03, 0.03, 0.04), (sx * W * 0.22, D / 2 - 0.02, zw - 0.01))
        add_cylinder_between(lv, (-W * 0.31, D * 0.32, zw + 0.12), (W * 0.31, D * 0.32, zw + 0.12), 0.009, 8)  # pivot
        add_tube(lv, [(-W * 0.25, D * 0.35, zw + 0.12), (-W * 0.25, D * 0.35, H - 0.014), (W * 0.25, D * 0.35, H - 0.014),
                      (W * 0.25, D * 0.35, zw + 0.12)], 0.012, 8, bend_radius=0.04, bend_steps=3 if d == 0 else 1)
        add_cylinder_between(P("Grips", "Caster_Grey"), (-W * 0.15, D * 0.35, H - 0.014), (W * 0.15, D * 0.35, H - 0.014), 0.014, 8)
        add_tube(lv, [(-W / 2 + 0.006, -D * 0.1, zw - 0.03), (-W / 2 + 0.04, -D * 0.3, zw + 0.08), (W / 2 - 0.04, -D * 0.3, zw + 0.08),
                      (W / 2 - 0.006, -D * 0.1, zw - 0.03)], 0.004, 6, bend_radius=0.03, bend_steps=2)  # bail handle
        for sx in (-1, 1):
            add_lathe(lv, (sx * (W / 2 - 0.002), -D * 0.1, zw - 0.03), (-sx, 0, 0), [(0, 0), (0.009, 0), (0.009, 0.004), (0, 0.006)], 8)
    else:
        add_box(w, (W * 0.6, D * 0.42, 0.16), (0, D * 0.2, zw + 0.07))
        add_tube(lv, [(-W * 0.25, D * 0.35, zw + 0.12), (-W * 0.25, D * 0.35, H - 0.012), (W * 0.25, D * 0.35, H - 0.012),
                      (W * 0.25, D * 0.35, zw + 0.12)], 0.012, 8)
    return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


KINDS = {"mop_sink": mop_sink, "mops_brooms": mops_brooms, "bucket": bucket}


def build(p, lod):
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"], W, D, H)
    extra = dict(extra, fixture_family="janitor_props", rf=p["rf"], seed=int(p["seed"]))
    if p.get("gap"):
        extra["gap"] = p["gap"]
    extra.update(wear(p))
    return P.finish(), (W, H + p.get("extra_h_m", 0.0), D), extra
