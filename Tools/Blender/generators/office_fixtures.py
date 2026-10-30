"""Office + back-room furniture (PROC-005 §8; IMP-003 drop 3 rewritten). One asset per ROOM_FIXTURES row (sizes [w, d, h]):
tall black cabinets (plain closed box, no hardware, DEC-051 Q9), the under-desk black file-cabinet run (2-drawer units
<= 2.4 ft), standing desk, desk arm / corner piece (black laminate), ex-register-1 desk (white top), stainless worktable on
folding legs, mesh task chair (5-star base, twin-wheel casters), stainless deli prep cart (DEC-079 refill spot) and the
black wire basket cart. No DrawerCart (no store evidence, O8). Component sizes (legs, pulls, chair parts, cart shelves)
are GAP-PROC-18. Origin = bottom centre, front = -Y; pulls reach the front bound. LOD0 full; LOD1 no micro detail;
LOD2 plain parts; LOD3 blocks."""
import math

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_handle_pull, add_lathe, add_sweep, add_tube,
                     add_wire_grid, collision_box, rounded_rect, slide_axis, to_unity, wear)


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def _bb(bm, size, center, d, corner=0.003, bevel=0.0015):
    if d >= 2:
        add_box(bm, size, center)
    else:
        add_beveled_box(bm, size, center, corner=corner, bevel=bevel, seg=2 if d == 0 else 1)


def _body(W, D, H):
    return [collision_box("Body", (0, 0, H / 2), (W, D, H))]


def tall_cabinet(P, p, d, s, W, D, H):
    b = P("Body", "Black_Laminate")
    if d >= 3:
        add_box(b, (W, D, H), (0, 0, H / 2))
    else:  # plain closed box on a recessed plinth, eased edges; no doors/hardware (DEC-051 Q9)
        _bb(b, (W, D, H - 0.08), (0, 0, 0.08 + (H - 0.08) / 2), d, 0.004, 0.002)
        add_box(b, (W - 0.04, D - 0.04, 0.08), (0, 0.0, 0.04))
    return {"collision_boxes": _body(W, D, H)}


def file_cabinets(P, p, d, s, W, D, H):
    f = p["files"]
    n, hs, hr = f["count"], f["pull_standoff_m"], f["pull_r_m"]
    yf = -D / 2 + hs + hr
    cw = W / n
    b = P("Body", "Black_Metal")
    if d >= 3:
        add_box(b, (W, D - hs - hr, H), (0, (yf + D / 2) / 2, H / 2))
        add_box(P("Pulls", "Chrome"), (W * 0.6, hs + hr, 0.02), (0, -D / 2 + (hs + hr) / 2, H * 0.7))
        return {"collision_boxes": _body(W, D, H)}
    moving = []
    for i in range(n):
        x = -W / 2 + (i + 0.5) * cw
        _bb(b, (cw, D / 2 - yf - 0.012, H), (x, (yf + 0.012 + D / 2) / 2, H / 2), d, 0.004, 0.002)  # behind the fronts
        dh = (H - 0.06) / 2
        for k in range(2):
            z = 0.04 + (k + 0.5) * dh
            name = f"Drawer_{i}_{k}"
            _bb(P(name, "Black_Metal"), (cw - 0.02, 0.012, dh - 0.006), (x, yf + 0.006, z), d, 0.002, 0.001)
            add_handle_pull(P(name, "Black_Metal"), (x, yf, z + dh * 0.25), cw * 0.35, hs, hr, 8, axis="x", bend_steps=2 if d == 0 else 1)
            if d <= 1:  # label holder
                add_box(P("Labels", "Chrome"), (0.07, 0.003, 0.03), (x, yf - 0.0015, z + dh * 0.05))
            moving.append(slide_axis(name, D * 0.7))
        if d == 0:  # generic lock cylinder, top corner
            add_cylinder_between(P("Labels", "Chrome"), (x + cw / 2 - 0.035, yf + 0.001, H - 0.035), (x + cw / 2 - 0.035, yf - 0.004, H - 0.035), 0.008, 12)
    return {"moving_parts": moving, "collision_boxes": _body(W, D, H)}


def _leveller(P, d, s, x, y, r):
    add_lathe(P("Levellers", "Plastic_Black"), (x, y, 0), (0, 0, 1), [(0, 0), (r, 0), (r, 0.006), (r * 0.5, 0.012), (0, 0.012)], s)


def desk(P, p, d, s, W, D, H):
    k = p["desk"]
    tt, lt = k["top_t_m"], k["leg_w_m"]
    top, legs = P("Top", k["top"]), P("Frame", k["frame"])
    zt = H - tt
    if d >= 3:
        add_box(top, (W, D, tt), (0, 0, zt + tt / 2))
        for sx in (-1, 1):
            add_box(legs, (lt, D - 0.06, zt), (sx * (W / 2 - 0.03 - lt / 2), 0, zt / 2))
        return {"collision_boxes": _body(W, D, H)}
    _bb(top, (W, D, tt), (0, 0, zt + tt / 2), d, 0.004, 0.002)
    if d <= 1:  # edge banding
        add_box(P("EdgeBand", k["edge"]), (W - 0.002, D - 0.002, tt * 0.6), (0, 0, zt + tt / 2))
    z0 = 0.012 if d <= 1 else 0.0
    for sx in (-1, 1):  # panel or loop legs + leveller feet, modesty panel
        x = sx * (W / 2 - 0.03 - lt / 2)
        if k.get("loop_legs"):
            add_tube(legs, [(x, -D / 2 + 0.06, z0), (x, -D / 2 + 0.06, zt), (x, D / 2 - 0.06, zt), (x, D / 2 - 0.06, z0)], lt / 2, 8,
                     bend_radius=0.03 if d == 0 else 0, bend_steps=3 if d == 0 else 0)
            add_tube(legs, [(x, -D / 2 + 0.06, z0 + lt / 2), (x, D / 2 - 0.06, z0 + lt / 2)], lt / 2, 8)
        else:
            _bb(legs, (lt, D - 0.06, zt - z0), (x, 0, z0 + (zt - z0) / 2), d)
        if d <= 1:
            for y in (-D / 2 + 0.06, D / 2 - 0.06):
                _leveller(P, d, s, x, y, lt * 0.5)
    _bb(legs, (W - 0.12 - 2 * lt, 0.016, zt * 0.45), (0, D / 2 - 0.1, zt - zt * 0.225 - 0.02), d)
    return {"collision_boxes": _body(W, D, H)}


def standing_desk(P, p, d, s, W, D, H):
    k = p["desk"]
    tt = k["top_t_m"]
    top, fr = P("Top", k["top"]), P("Frame", k["frame"])
    zt = H - tt
    if d >= 3:
        add_box(top, (W, D, tt), (0, 0, zt + tt / 2))
        for sx in (-1, 1):
            add_box(fr, (0.08, D * 0.9, zt), (sx * W * 0.38, 0, zt / 2))
        return {"collision_boxes": _body(W, D, H)}
    _bb(top, (W, D, tt), (0, 0, zt + tt / 2), d, 0.004, 0.002)
    for sx in (-1, 1):  # telescoping columns on T feet, crossbar
        x = sx * W * 0.38
        _bb(fr, (0.07, D * 0.9, 0.04), (x, 0, 0.02), d, 0.01, 0.003)
        _bb(fr, (0.07, 0.05, zt * 0.55), (x, 0, 0.04 + zt * 0.275), d)
        _bb(fr, (0.06, 0.04, zt - 0.04 - zt * 0.45), (x, 0, zt - (zt - 0.04 - zt * 0.45) / 2), d)
        _bb(fr, (0.06, D * 0.75, 0.025), (x, 0, zt - 0.0125), d)
    _bb(fr, (W * 0.76, 0.04, 0.03), (0, 0, zt - 0.03), d)
    if d <= 1:  # up/down controller paddle
        add_box(P("Controls", "Plastic_Black"), (0.09, 0.05, 0.02), (W * 0.3, -D / 2 + 0.05, zt - 0.01))
    return {"collision_boxes": _body(W, D, H)}


def worktable(P, p, d, s, W, D, H):
    k = p["desk"]
    tt = k["top_t_m"]
    top, fr = P("Top", "Stainless"), P("Frame", "Frame_Grey")
    zt = H - tt
    if d >= 3:
        add_box(top, (W, D, tt), (0, 0, zt + tt / 2))
        add_box(fr, (W - 0.1, D - 0.1, zt - 0.04), (0, 0, (zt - 0.04) / 2))
        return {"collision_boxes": _body(W, D, H)}
    _bb(top, (W, D, tt), (0, 0, zt + tt / 2), d, 0.01, 0.006)  # rolled edge
    add_box(fr, (W - 0.1, D - 0.1, 0.06), (0, 0, zt - 0.03))  # apron
    lr = 0.0127
    for sx in (-1, 1):  # folding legs: two splayed tubes, cross bar, folding brace with hinge
        x = sx * (W / 2 - 0.12)
        for y in (-D / 2 + 0.07, D / 2 - 0.07):
            add_cylinder_between(fr, (x, y, 0.0), (x, y, zt - 0.06), lr, s)
            if d <= 1:
                add_lathe(P("Levellers", "Plastic_Black"), (x, y, 0), (0, 0, 1), [(0, 0), (lr * 1.2, 0), (lr * 1.2, 0.02), (0, 0.02)], s)
        add_cylinder_between(fr, (x, -D / 2 + 0.07, 0.12), (x, D / 2 - 0.07, 0.12), lr * 0.8, s)
        if d <= 1:
            add_tube(fr, [(x, 0, 0.12), (x - sx * 0.25, 0, zt - 0.08)], 0.006, 8)
            add_box(fr, (0.03, 0.04, 0.03), (x - sx * 0.25, 0, zt - 0.075))
    return {"collision_boxes": _body(W, D, H)}


def task_chair(P, p, d, s, W, D, H):
    c = p["chair"]
    R, zs = c["star_r_m"], c["seat_z_m"]
    base, mesh, pad = P("Base", "Black_Plastic"), P("Mesh", "Mesh_Black"), P("Seat", "Fabric_Black")
    sd, sw = c["seat_d_m"], c["seat_w_m"]
    if d >= 3:
        add_box(base, (2 * R, 2 * R, zs - 0.07), (0, 0, (zs - 0.07) / 2))
        add_box(pad, (W, sd, 0.12), (0, -D / 2 + sd / 2, zs - 0.06))
        add_box(mesh, (sw, 0.04, H - zs), (0, D / 2 - 0.02, zs + (H - zs) / 2))
        return {"collision_boxes": _body(W, D, H)}
    zh = 0.09
    for k in range(5):  # 5-star base with twin-wheel casters
        th = math.radians(90 + 72 * k)
        tip = (R * math.cos(th), R * math.sin(th))
        add_sweep(base, [(0, 0, zh), (tip[0], tip[1], zh - 0.02)], rounded_rect(0.04, 0.03, 0.008, 2 if d == 0 else 1))
        px, py = -math.sin(th), math.cos(th)
        for sg in (-1, 1):
            add_cylinder_between(P("Casters", "Rubber_Black"), (tip[0] + sg * px * 0.004, tip[1] + sg * py * 0.004, 0.025),
                                 (tip[0] + sg * px * 0.02, tip[1] + sg * py * 0.02, 0.025), 0.025, s)
        if d <= 1:
            add_cylinder_between(base, (tip[0], tip[1], 0.05), (tip[0], tip[1], zh - 0.02), 0.008, 8)
    add_lathe(base, (0, 0, 0), (0, 0, 1), [(0, zh - 0.03), (0.04, zh - 0.03), (0.04, zh + 0.02), (0, zh + 0.02)], s)
    add_cylinder_between(P("GasLift", "Chrome"), (0, 0, zh + 0.02), (0, 0, zs - 0.12), 0.025, s)
    add_cylinder_between(base, (0, 0, zs - 0.2), (0, 0, zs - 0.09), 0.03, s)  # shroud
    _bb(base, (0.22, 0.25, 0.04), (0, -D / 2 + sd / 2, zs - 0.09), d, 0.01, 0.004)  # mechanism
    _bb(pad, (sw, sd, 0.07), (0, -D / 2 + sd / 2, zs - 0.035), d, 0.04, 0.015)
    for sx in (-1, 1):  # armrests: post + pad; outer face = W/2
        ax = sx * (W / 2 - 0.035)
        _bb(base, (0.03, 0.05, 0.22), (ax, -D / 2 + sd * 0.55, zs + 0.06), d)
        cw = abs(ax) - sw / 2 + 0.01  # bracket from under the seat out to the post
        add_box(base, (cw, 0.04, 0.02), (sx * (sw / 2 - 0.01 + cw / 2), -D / 2 + sd * 0.55, zs - 0.06))
        _bb(pad, (0.07, 0.25, 0.025), (ax, -D / 2 + sd * 0.55, zs + 0.17 + 0.0125), d, 0.012, 0.005)
    # spine + framed mesh back; the back's rear face is +D/2, its top = H
    _bb(base, (0.06, D - sd - 0.03, 0.03), (0, -D / 2 + sd + (D - sd - 0.03) / 2 - 0.02, zs - 0.08), d)
    _bb(base, (0.06, 0.03, 0.3), (0, D / 2 - 0.05, zs + 0.03), d)
    bz0 = zs + 0.08
    add_tube(base, [(-sw / 2, D / 2 - 0.022, bz0), (sw / 2, D / 2 - 0.022, bz0), (sw / 2, D / 2 - 0.022, H - 0.012),
                    (-sw / 2, D / 2 - 0.022, H - 0.012)], 0.01, 8, closed=True)
    add_box(mesh, (sw, 0.012, H - bz0), (0, D / 2 - 0.006, bz0 + (H - bz0) / 2))
    return {"collision_boxes": _body(W, D, H)}


def _caster(P, s, x, y, top):
    add_lathe(P("Casters", "Rubber_Black"), (x - 0.012, y, 0.035), (1, 0, 0), [(0, 0), (0.035, 0), (0.035, 0.024), (0, 0.024)], s)
    add_box(P("Frame", "Frame_Grey"), (0.03, 0.04, top - 0.07), (x, y, 0.07 + (top - 0.07) / 2))


def cart(P, p, d, s, W, D, H):
    c = p["cart"]
    fin = c["finish"]
    fr = P("Frame", fin)
    lv = c["shelf_z_m"]
    ct = c["caster_h_m"]
    if d >= 3:
        for z in lv:
            add_box(fr, (W, D, 0.04), (0, 0, z - 0.02))
        for x in (-W / 2 + 0.04, W / 2 - 0.04):  # post pairs per end + caster strip
            add_box(fr, (0.03, D - 0.08, H - ct), (x, 0, ct + (H - ct) / 2))
            add_box(P("Casters", "Rubber_Black"), (0.03, D - 0.08, ct), (x, 0, ct / 2))
        return {"collision_boxes": _body(W, D, H)}
    pr = 0.0127
    px, py = W / 2 - 0.04, D / 2 - 0.04  # 35 mm wheels stay inside the footprint
    for x in (-px, px):
        for y in (-py, py):
            add_cylinder_between(fr, (x, y, ct), (x, y, H - 0.0127 if c.get("handle") and x < 0 else (max(lv) if c["shelf"] == "tray" else H - 0.005)), pr, s)
            _caster(P, s, x, y, ct)  # every LOD to LOD2: the wheels set the floor bound
    for z in lv:
        if c["shelf"] == "tray":  # stainless shelf with a raised rolled lip
            _bb(P("Shelves", fin), (W, D, 0.03), (0, 0, z - 0.015), d, 0.02, 0.008)
            if d <= 1:
                add_box(P("Shelves", fin), (W - 0.02, D - 0.02, 0.004), (0, 0, z + 0.001))
        else:  # wire basket: round-wire floor + wire sides
            add_wire_grid(P("Shelves", fin), W - 0.01, D - 0.01, z - 0.01, 0.004, c["wire_pitch_m"] * (1 if d == 0 else 2), c["wire_pitch_m"] * (1 if d == 0 else 2), 6)
            for zz in (z + 0.06, z + 0.12):
                add_tube(P("Shelves", fin), [(-W / 2 + 0.005, -D / 2 + 0.005, zz), (W / 2 - 0.005, -D / 2 + 0.005, zz),
                                             (W / 2 - 0.005, D / 2 - 0.005, zz), (-W / 2 + 0.005, D / 2 - 0.005, zz)], 0.005, 8, closed=True)
    if c.get("handle"):  # tubular push handle across the -X end, at the cart's top height
        add_tube(fr, [(-px, -py, H - 0.0127), (-px, py, H - 0.0127)], 0.0127, s)
        if d <= 1:
            add_box(P("Labels", "Label_White"), (0.003, D * 0.4, 0.05), (-px - 0.014, 0, max(lv) - 0.04))  # blank rail label
    return {"collision_boxes": _body(W, D, H)}


KINDS = {"tall_cabinet": tall_cabinet, "file_cabinets": file_cabinets, "desk": desk, "standing_desk": standing_desk,
         "worktable": worktable, "task_chair": task_chair, "cart": cart}


def build(p, lod):
    P = Parts(p["colors"])
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"], W, D, H)
    extra = dict(extra, fixture_family="office_fixtures", rf=p["rf"], seed=int(p["seed"]))
    extra.update(wear(p))
    return P.finish(), (W, H, D), extra
