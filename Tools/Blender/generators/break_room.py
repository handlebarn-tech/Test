"""Break room (PROC-005 §9; IMP-003 drop 3 rewritten). One asset per ROOM_FIXTURES row ([w, d, h] ft):
staff lockers (one 2.0 x 1.5 x 6.0 ft unit, 2 x 6 doors, DEC-047/051/088; grey top, louvre slots that are real gaps,
latch, blank number plate, hinge knuckles; LOD-independent hinge metadata), wood bench on black steel legs, the five
boards (bulletin, cork, red/white whiteboard, black-frame, grey fabric), lunch table, first-aid kit, light-wood base
cabinets with black 34 in top + backsplash (TI §6.4; North run, East return with the sink cut-out), light-wood uppers,
stainless double sink with gooseneck faucet, microwave, pod coffee maker, mini hoop over a hamper, coat-hook rail.
Unsourced part sizes are GAP-PROC-19. Heights that exceed the RF row (backsplash, faucet) are named in `_note`.
Origin = bottom centre, front = -Y (wall at +Y). LOD0 full; LOD1 no micro detail; LOD2 plain; LOD3 blocks."""
import math

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_handle_pull, add_lathe, add_sweep, add_tube,
                     collision_box, hinge_axis, wear)


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


def lockers(P, p, d, s, W, D, H):
    k = p["lockers"]
    cols, rows, kick, cap, ft_, hs = k["columns"], k["rows"], k["kick_h_m"], k["top_h_m"], k["frame_m"], k["handle_d_m"]
    yf = -D / 2 + hs
    body = P("Body", "Locker_Grey")
    dw, dh = (W - 2 * ft_) / cols, (H - kick - cap - 2 * ft_) / rows
    moving = []
    for c in range(cols):
        for r in range(rows):
            x0 = -W / 2 + ft_ + c * dw
            z0 = kick + ft_ + r * dh
            side = "left" if c == 0 else "right"
            moving.append(hinge_axis(f"Door_{c}{r}", x0 if side == "left" else x0 + dw, yf + 0.01, z0, z0 + dh, side, 100))
    if d >= 3:
        add_box(body, (W, D - hs, H), (0, hs / 2, H / 2))
        add_box(P("Handles", "Chrome"), (W * 0.2, hs, H * 0.8), (0, -D / 2 + hs / 2, H / 2))
        return {"moving_parts": moving, "collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    add_box(body, (W, D - hs - 0.02, H - cap - kick), (0, (yf + 0.02 + D / 2) / 2, kick + (H - cap - kick) / 2))
    add_box(P("Interior", "Black_Interior"), (W - 2 * ft_, 0.005, H - cap - kick - 2 * ft_), (0, yf + 0.02 + 0.003, kick + (H - kick - cap) / 2))
    _bb(P("Top", "Grey_Top"), (W, D - hs, cap), (0, hs / 2, H - cap / 2), d, 0.004, 0.002)
    add_box(P("Base", "Black_Interior"), (W - 0.02, D - hs - 0.03, kick), (0, hs / 2 + 0.01, kick / 2))
    for c in range(cols):
        for r in range(rows):
            x0, z0 = -W / 2 + ft_ + c * dw, kick + ft_ + r * dh
            xm, zm = x0 + dw / 2, z0 + dh / 2
            door = P(f"Door_{c}{r}", "Locker_Grey")
            g = 0.003
            if d <= 1:  # door = frame around a louvre band of real slots (slats with gaps onto the dark interior)
                lz0, lz1 = z0 + dh * 0.62, z0 + dh * 0.88
                for (a, b) in ((z0 + g, lz0), (lz1, z0 + dh - g)):
                    add_box(door, (dw - 2 * g, 0.02, b - a), (xm, yf + 0.01, (a + b) / 2))
                for sx in (-1, 1):
                    add_box(door, (dw * 0.15, 0.02, lz1 - lz0), (xm + sx * (dw / 2 - g - dw * 0.075), yf + 0.01, (lz0 + lz1) / 2))
                n = 4 if d == 0 else 2
                pitch = (lz1 - lz0) / n
                for i in range(n):
                    z = lz0 + (i + 0.5) * pitch
                    prof = [(yf + 0.002, z - pitch * 0.3), (yf + 0.012, z - pitch * 0.15), (yf + 0.012, z + pitch * 0.05), (yf + 0.002, z - pitch * 0.1)]
                    add_sweep(door, [(xm - dw * 0.35, 0, 0), (xm + dw * 0.35, 0, 0)], prof)
                hx = xm + (dw / 2 - 0.03) * (1 if c == 0 else -1)
                add_box(P("Handles", "Chrome"), (0.02, hs, 0.05), (hx, -D / 2 + hs / 2, zm))  # lift latch
                add_box(P("Plates", "Plate_Blank"), (0.04, 0.002, 0.018), (xm, yf - 0.001, z0 + dh * 0.94 - 0.004))
                if d == 0:
                    hxk = x0 + (0.004 if c == 0 else dw - 0.004)
                    for zz in (z0 + 0.04, z0 + dh - 0.04):  # hinge knuckles
                        add_cylinder_between(P("Hinges", "Chrome"), (hxk, yf + 0.004, zz - 0.015), (hxk, yf + 0.004, zz + 0.015), 0.004, 8)
            else:
                add_box(door, (dw - 2 * g, 0.02, dh - 2 * g), (xm, yf + 0.01, zm))
                add_box(P("Handles", "Chrome"), (0.02, hs, 0.05), (xm + (dw / 2 - 0.03) * (1 if c == 0 else -1), -D / 2 + hs / 2, zm))
    return {"moving_parts": moving, "collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def bench(P, p, d, s, W, D, H):
    pt = 0.04
    top, fr = P("Top", "Wood_Plank"), P("Frame", "Black_Steel")
    if d >= 3:
        add_box(top, (W, D, pt), (0, 0, H - pt / 2))
        for sx in (-1, 1):
            add_box(fr, (0.04, D - 0.04, H - pt), (sx * (W / 2 - 0.12), 0, (H - pt) / 2))
        return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    planks = 3 if d <= 1 else 1
    for i in range(planks):  # planks with gaps
        pw = D / planks
        a, b = -D / 2 + i * pw + (0.002 if i else 0), -D / 2 + (i + 1) * pw - (0.002 if i < planks - 1 else 0)  # gaps between only
        _bb(top, (W, b - a, pt), (0, (a + b) / 2, H - pt / 2), d, 0.004, 0.003)
    for sx in (-1, 1):  # square-tube leg frames
        x = sx * (W / 2 - 0.12)
        add_tube(fr, [(x, -D / 2 + 0.03, 0.0), (x, -D / 2 + 0.03, H - pt), (x, D / 2 - 0.03, H - pt), (x, D / 2 - 0.03, 0.0)], 0.0127, 8)
        add_box(fr, (0.025, D - 0.06, 0.025), (x, 0, 0.1))
    add_box(fr, (W - 0.24, 0.025, 0.025), (0, 0, 0.1))
    return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def board(P, p, d, s, W, D, H):
    b = p["board"]
    fw = b["frame_w_m"]
    fr, face = P("Frame", b["frame"]), P("Face", b["face"])
    if d >= 3:
        add_box(fr, (W, D, H), (0, 0, H / 2))
        return {}
    for size, c in (((W, D, fw), (0, 0, fw / 2)), ((W, D, fw), (0, 0, H - fw / 2)),
                    ((fw, D, H - 2 * fw), (-W / 2 + fw / 2, 0, H / 2)), ((fw, D, H - 2 * fw), (W / 2 - fw / 2, 0, H / 2))):
        _bb(fr, size, c, d, 0.002, 0.002 if d == 0 else 0.0)
    add_box(face, (W - 2 * fw, D * 0.5, H - 2 * fw), (0, D * 0.25, H / 2))  # recessed face
    if b.get("tray") and d <= 1:  # whiteboard marker tray
        add_box(fr, (W * 0.3, D, 0.012), (0, 0, fw + 0.006))
    return {}


def table(P, p, d, s, W, D, H):
    tt = 0.03
    top, fr = P("Top", "Table_Top"), P("Frame", "Black_Steel")
    if d >= 3:
        add_box(top, (W, D, tt), (0, 0, H - tt / 2))
        add_box(fr, (W - 0.1, D - 0.1, H - tt), (0, 0, (H - tt) / 2))
        return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    _bb(top, (W, D, tt), (0, 0, H - tt / 2), d, 0.01, 0.003)
    add_box(fr, (W - 0.12, D - 0.12, 0.06), (0, 0, H - tt - 0.03))
    for sx in (-1, 1):
        for sy in (-1, 1):
            add_box(fr, (0.04, 0.04, H - tt), (sx * (W / 2 - 0.06), sy * (D / 2 - 0.06), (H - tt) / 2))
            if d <= 1:
                add_box(P("Feet", "Black_Plastic"), (0.042, 0.042, 0.01), (sx * (W / 2 - 0.06), sy * (D / 2 - 0.06), 0.005))
    return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def first_aid(P, p, d, s, W, D, H):
    b = P("Body", "White_Plastic")
    if d >= 3:
        add_box(b, (W, D, H), (0, 0, H / 2))
        return {}
    _bb(b, (W, D - 0.004, H), (0, 0.002, H / 2), d, 0.012, 0.004)
    cr = P("Cross", "Cross_Red")  # generic first-aid cross, no brand
    add_box(cr, (W * 0.3, 0.004, W * 0.1), (0, -D / 2 + 0.002, H * 0.6))
    add_box(cr, (W * 0.1, 0.004, W * 0.3), (0, -D / 2 + 0.002, H * 0.6))
    if d <= 1:
        add_box(P("Latch", "Grey_Plastic"), (0.04, 0.004, 0.015), (0, -D / 2 + 0.002, H * 0.15))
    return {"moving_parts": [hinge_axis("Body", -W / 2, -D / 2, 0, H, "left")]}


def base_cabinets(P, p, d, s, W, D, H):
    k = p["counter"]
    tt, sp, kick, hs = k["top_t_m"], k["splash_h_m"], k["kick_h_m"], k["pull_standoff_m"]
    yf = -D / 2 + 0.025 + hs  # 1 in top overhang; pulls reach -D/2
    zt = H - tt
    top, wood, blk = P("Top", "Black_Top"), P("Doors", "Light_Wood"), P("Carcass", "Black_Interior")
    Ht = H + sp
    if d >= 3:
        add_box(top, (W, D, tt), (0, 0, zt + tt / 2))
        add_box(top, (W, 0.02, sp), (0, D / 2 - 0.01, H + sp / 2))
        add_box(wood, (W, D / 2 - (-D / 2 + 0.025), zt), (0, 0.0125, zt / 2))
        return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    cut = k.get("sink_cutout")  # [x centre, width, depth] m: the top is built around the sink opening
    if cut:
        cx, cw, cdp = cut
        cy = -D / 2 + 0.06 + cdp / 2
        for x0, x1 in ((-W / 2, cx - cw / 2), (cx + cw / 2, W / 2)):
            _bb(top, (x1 - x0, D, tt), ((x0 + x1) / 2, 0, zt + tt / 2), d)
        for y0, y1 in ((-D / 2, cy - cdp / 2), (cy + cdp / 2, D / 2)):
            add_box(top, (cw, y1 - y0, tt), (cx, (y0 + y1) / 2, zt + tt / 2))
    else:
        _bb(top, (W, D, tt), (0, 0, zt + tt / 2), d)
    _bb(top, (W, 0.02, sp), (0, D / 2 - 0.01, H + sp / 2), d)  # 1-1/2 in top with backsplash (TI 6.4)
    add_box(blk, (W, D - 0.05 - hs - 0.02, zt - kick), (0, (yf + 0.02 + D / 2) / 2, kick + (zt - kick) / 2))
    add_box(blk, (W - 0.01, 0.012, kick), (0, yf + 0.05, kick / 2))
    n = max(1, round(W / k["door_w_m"]))
    dw = W / n
    for i in range(n):
        x = -W / 2 + (i + 0.5) * dw
        if d <= 1:
            _bb(wood, (dw - 0.004, 0.019, 0.15), (x, yf + 0.0095, zt - 0.085), d, 0.002, 0.001)  # drawer
            _bb(wood, (dw - 0.004, 0.019, zt - kick - 0.17), (x, yf + 0.0095, kick + (zt - kick - 0.17) / 2 + 0.002), d, 0.002, 0.001)
            add_handle_pull(P("Pulls", "Brushed_Steel"), (x, yf, zt - 0.085), 0.096, hs - 0.005, 0.005, 8, axis="x", bend_steps=2)
            add_handle_pull(P("Pulls", "Brushed_Steel"), (x + dw * 0.35, yf, zt - 0.25), 0.096, hs - 0.005, 0.005, 8, axis="z", bend_steps=2)
        else:
            add_box(wood, (dw - 0.004, 0.019, zt - kick), (x, yf + 0.0095, kick + (zt - kick) / 2))
    return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def uppers(P, p, d, s, W, D, H):
    k = p["counter"]
    hs = k["pull_standoff_m"]
    yf = -D / 2 + hs
    wood = P("Doors", "Light_Wood")
    if d >= 3:
        add_box(wood, (W, D, H), (0, 0, H / 2))
        return {}
    add_box(P("Carcass", "Light_Wood"), (W, D - hs - 0.02, H), (0, (yf + 0.02 + D / 2) / 2, H / 2))
    n = max(1, round(W / k["door_w_m"]))
    dw = W / n
    moving = []
    for i in range(n):
        x = -W / 2 + (i + 0.5) * dw
        _bb(P(f"Door_{i}", "Light_Wood"), (dw - 0.004, 0.02, H - 0.004), (x, yf + 0.01, H / 2), d, 0.002, 0.001)
        side = "left" if i % 2 == 0 else "right"
        px = x + (dw / 2 - 0.04) * (1 if side == "left" else -1)
        if d <= 2:
            add_handle_pull(P(f"Door_{i}", "Light_Wood"), (px, yf, 0.12), 0.096, hs - 0.005, 0.005, 8, axis="z", bend_steps=2 if d <= 1 else 0)
        moving.append(hinge_axis(f"Door_{i}", x - dw / 2 if side == "left" else x + dw / 2, yf + 0.01, 0, H, side))
    return {"moving_parts": moving}


def double_sink(P, p, d, s, W, D, H):
    k = p["sink"]
    bd, rim, fh = k["bowl_depth_m"], k["rim_t_m"], k["faucet_h_m"]
    Hr = bd + rim
    st = P("Sink", "Stainless")
    if d >= 3:
        add_box(st, (W, D, Hr), (0, 0, Hr / 2))
        add_box(st, (0.04, 0.04, fh), (0, D / 2 - 0.05, Hr + fh / 2))
        return {}
    add_box(st, (W, D, rim), (0, 0, Hr - rim / 2))  # rim deck (drops onto the counter's cut-out)
    bw = (W - 0.12) / 2
    for sx in (-1, 1):  # open bowls: walls + floor + drain
        cx = sx * (bw / 2 + 0.02)
        bd_ = D - 0.14
        for size, c in (((bw, 0.002, bd), (cx, -bd_ / 2, bd / 2)), ((bw, 0.002, bd), (cx, bd_ / 2, bd / 2)),
                        ((0.002, bd_, bd), (cx - bw / 2, 0, bd / 2)), ((0.002, bd_, bd), (cx + bw / 2, 0, bd / 2)),
                        ((bw, bd_, 0.002), (cx, 0, 0.001))):
            add_box(st, size, c)
        if d <= 1:
            add_lathe(P("Drain", "Chrome"), (cx, 0, 0), (0, 0, 1), [(0, 0.002), (0.045, 0.002), (0.045, 0.006), (0, 0.006)], s)
    # gooseneck faucet at the back centre
    fb = (0, D / 2 - 0.05, Hr)
    add_lathe(P("Faucet", "Chrome"), fb, (0, 0, 1), [(0, 0), (0.03, 0), (0.03, 0.02), (0.015, 0.04), (0, 0.04)], s)
    if d <= 1:
        r = 0.012
        zt = Hr + fh - r  # flat top run: the fillets stay below it, so the top bound is exact
        add_tube(P("Faucet", "Chrome"), [(0, D / 2 - 0.05, Hr + 0.03), (0, D / 2 - 0.05, zt), (0, D / 2 - 0.2, zt),
                                         (0, D / 2 - 0.2, zt - 0.1)], r, 8,
                 bend_radius=0.05, bend_steps=4 if d == 0 else 2)
        add_cylinder_between(P("Faucet", "Chrome"), (0.03, D / 2 - 0.05, Hr + 0.08), (0.12, D / 2 - 0.05, Hr + 0.1), 0.006, 8)  # lever
    else:
        add_box(P("Faucet", "Chrome"), (0.024, 0.024, fh - 0.04), (0, D / 2 - 0.05, Hr + 0.04 + (fh - 0.04) / 2))
    return {}


def appliance(P, p, d, s, W, D, H):
    a = p["appliance"]
    b = P("Body", a["body"])
    if d >= 3:
        add_box(b, (W, D, H), (0, 0, H / 2))
        return {}
    if a["type"] == "microwave":
        _bb(b, (W, D - 0.01, H), (0, 0.005, H / 2), d, 0.01, 0.004)
        add_box(P("Window", "Glass_Dark"), (W * 0.6, 0.004, H * 0.6), (-W * 0.1, -D / 2 + 0.008, H * 0.52))
        add_box(P("Panel", "Panel_Dark"), (W * 0.2, 0.004, H * 0.8), (W * 0.36, -D / 2 + 0.008, H / 2))
        add_box(P("Handle", "Grey_Plastic"), (0.02, 0.01, H * 0.6), (W * 0.22, -D / 2 + 0.005, H * 0.52))
        if d == 0:
            for i in range(8):
                add_box(P("Keys", "Grey_Plastic"), (0.02, 0.002, 0.012), (W * 0.36, -D / 2 + 0.005, H * 0.3 + i * 0.018))
    else:  # pod coffee maker: base, tower, reservoir, drip tray, lid
        _bb(b, (W, D, 0.03), (0, 0, 0.015), d, 0.01, 0.004)
        _bb(b, (W, D * 0.55, H - 0.03), (0, D / 2 - D * 0.275, 0.03 + (H - 0.03) / 2), d, 0.02, 0.006)
        _bb(b, (W * 0.9, D * 0.4, 0.05), (0, -D / 2 + D * 0.25, H - 0.025), d, 0.02, 0.006)
        add_box(P("Tray", "Grey_Plastic"), (W * 0.7, D * 0.35, 0.01), (0, -D / 2 + D * 0.2, 0.035))
        if d <= 1:
            add_box(P("Window", "Glass_Dark"), (W * 0.5, 0.004, 0.02), (0, -D / 2 + D * 0.05 + 0.002, H - 0.03))
    return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def mini_hoop(P, p, d, s, W, D, H):
    fr, bb = P("Frame", "Black_Steel"), P("Backboard", "White_Plastic")
    hb = P("Hamper", "Hamper_Grey")
    if d >= 3:
        add_box(hb, (W, D, H * 0.4), (0, 0, H * 0.2))
        add_box(bb, (W, 0.03, H * 0.35), (0, D / 2 - 0.015, H - H * 0.175))
        return {}
    # over-the-hamper stand: frame on the wall side, backboard, rim with net cone, hamper with a ball
    add_box(hb, (W, D, 0.01), (0, 0, 0.005))  # base plate = footprint
    for sx in (-1, 1):
        for sy in (-1, 1):
            add_box(hb, (0.02, 0.02, H * 0.4), (sx * (W / 2 - 0.02), sy * (D / 2 - 0.02), H * 0.2))
    add_box(P("HamperBag", "Hamper_Fabric"), (W - 0.04, D - 0.04, H * 0.38), (0, 0, H * 0.2))
    for sx in (-1, 1):
        add_cylinder_between(fr, (sx * W * 0.3, D / 2 - 0.03, 0.0), (sx * W * 0.3, D / 2 - 0.03, H - 0.01), 0.012, s)
    _bb(bb, (W, 0.03, H * 0.35), (0, D / 2 - 0.015, H - H * 0.175), d, 0.01, 0.004)
    zr = H - H * 0.3
    add_tube(P("Rim", "Rim_Orange"), [(0.12 * math.cos(2 * math.pi * i / 16), D / 2 - 0.16 + 0.12 * math.sin(2 * math.pi * i / 16), zr)
                                      for i in range(16)], 0.006, 8, closed=True)
    if d <= 1:
        add_lathe(P("Net", "Net_White"), (0, D / 2 - 0.16, 0), (0, 0, 1), [(0.12, zr), (0.08, zr - 0.18)], s)
    add_lathe(P("Ball", "Rim_Orange"), (0, 0, 0), (0, 0, 1), [(0, H * 0.38), (0.06, H * 0.38 + 0.03), (0.09, H * 0.38 + 0.09),
                                                               (0.06, H * 0.38 + 0.15), (0, H * 0.38 + 0.18)], s)
    return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def coat_hooks(P, p, d, s, W, D, H):
    rail = P("Rail", "Wood_Plank")
    hk = P("Hooks", "Black_Steel")
    if d >= 3:
        add_box(rail, (W, D, H), (0, 0, H / 2))
        return {}
    _bb(rail, (W, 0.02, H), (0, D / 2 - 0.01, H / 2), d, 0.004, 0.003)
    n = p["hooks"]
    for i in range(n):  # double-prong hooks
        x = -W / 2 + (i + 0.5) * W / n
        add_tube(hk, [(x, D / 2 - 0.02, H * 0.55), (x, -D / 2 + 0.008, H * 0.35), (x, -D / 2 + 0.008, H * 0.6)], 0.005, 8,
                 bend_radius=0.02 if d <= 1 else 0, bend_steps=3 if d == 0 else (1 if d == 1 else 0))
        add_lathe(hk, (x, -D / 2 + 0.008, 0), (0, 0, 1), [(0, H * 0.6 - 0.004), (0.008, H * 0.6 + 0.002), (0, H * 0.6 + 0.008)], 8)  # ball tip
    return {}


KINDS = {"lockers": lockers, "bench": bench, "board": board, "table": table, "first_aid": first_aid, "base_cabinets": base_cabinets,
         "uppers": uppers, "double_sink": double_sink, "appliance": appliance, "mini_hoop": mini_hoop, "coat_hooks": coat_hooks}


def build(p, lod):
    P = Parts(p["colors"])
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"], W, D, H)
    Ht = H + p.get("extra_h_m", 0.0)
    extra = dict(extra, fixture_family="break_room", rf=p["rf"], seed=int(p["seed"]))
    extra.update(wear(p))
    return P.finish(), (W, Ht, D), extra
