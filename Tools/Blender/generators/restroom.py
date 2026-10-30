"""Restroom (PROC-005 §10; IMP-003 drop 3 rewritten). One asset per item; sizes from ROOM_FIXTURES / TI §6.6:
wall-hung lavatory (rim 34 in, 27 in knee clearance; open recessed basin, no top cap -> no z-fight; overflow, drain,
faucet, brackets, P-trap, supplies), framed mirror 1'-8" x 3'-6" (bottom 3'-4" AFF), toilet (bowl cavity, seat + lid
with hinges, tank, flush lever), flat-black tool chest (swing doors, proud pulls) kept below the 33 in grab bar, the
large storage cabinet (RF 3.2 x 1.5 x 7.0 ft), stainless grab bars 42/36 in + 18 in vertical with flanges, old silver
manual paper-towel dispenser (DEC-062), TP and soap dispensers, napkin disposal, wall sconce (TI types).
Wall items carry `mount_z_m` (origin height AFF); their origin is the bottom of the item. Back (+Y) = wall.
Part sizes without a source are GAP-PROC-20. LOD0 full; LOD1 no micro detail; LOD2 plain; LOD3 blocks."""
from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_handle_pull, add_lathe, add_tube, collision_box,
                     hinge_axis, loft, rounded_rect, wear)


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def _bb(bm, size, center, d, corner=0.004, bevel=0.002):
    if d >= 2:
        add_box(bm, size, center)
    else:
        add_beveled_box(bm, size, center, corner=corner, bevel=bevel, seg=3 if d == 0 else 1)


def _rings(bm, specs, cs):
    """Loft of rounded-rect rings: specs = [(w, d, r, y_offset, z)]. Same r > inset keeps the ring sizes equal."""
    loft(bm, [[(x, y + yo, z) for x, y in rounded_rect(w, dd, r, cs)] for w, dd, r, yo, z in specs])


def lavatory(P, p, d, s, W, D, H):
    k = p["lav"]
    bh, td, fh = k["body_h_m"], k["trap_drop_m"], k["faucet_h_m"]
    z0, zr = td, td + bh  # basin bottom, rim
    china = P("Basin", "Vitreous_White")
    cs = (4, 2, 1, 0)[d]
    if d >= 3:
        add_box(china, (W, D, bh), (0, 0, z0 + bh / 2))
        add_box(P("Faucet", "Chrome"), (0.05, 0.05, fh), (0, D / 2 - 0.06, zr + fh / 2))
        add_box(P("Faucet", "Chrome"), (0.03, 0.03, td), (0, 0, td / 2))
        return {"mount_z_m": k["rim_z_m"] - bh - td}
    r = 0.06
    deck = 0.1  # back deck for the faucet
    _rings(china, [(W - 0.04, D - 0.04, r, 0.02, z0), (W, D, r, 0, z0 + bh * 0.4), (W, D, r, 0, zr - 0.006), (W - 0.012, D - 0.012, r, 0, zr),
                   (W - 0.06, D - 0.06 - deck, r * 0.9, -deck / 2, zr - 0.004), (W - 0.16, D - 0.16 - deck, r * 0.6, -deck / 2 + 0.01, z0 + 0.025)]
           if d <= 1 else [(W, D, r, 0, z0), (W, D, r, 0, zr), (W - 0.06, D - 0.06 - deck, r * 0.9, -deck / 2, zr), (W - 0.16, D - 0.16 - deck, r * 0.6, -deck / 2, z0 + 0.025)], max(1, cs))
    ch = P("Faucet", "Chrome")
    yb = D / 2 - deck / 2 - 0.01  # faucet on the back deck
    add_lathe(ch, (0, yb, 0), (0, 0, 1), [(0, zr), (0.025, zr), (0.025, zr + 0.03), (0.018, zr + fh - 0.005), (0, zr + fh)] if d <= 1
              else [(0, zr), (0.025, zr), (0.025, zr + fh), (0, zr + fh)], s)
    if d <= 1:
        add_tube(ch, [(0, yb, zr + fh * 0.7), (0, yb - 0.1, zr + fh * 0.7), (0, yb - 0.1, zr + fh * 0.55)], 0.008, 8, bend_radius=0.02, bend_steps=2)
        add_cylinder_between(ch, (0.02, yb, zr + fh - 0.01), (0.09, yb, zr + fh - 0.005), 0.005, 8)  # single lever
        dz = z0 + 0.025
        add_lathe(ch, (0, -0.0, 0), (0, 0, 1), [(0, dz), (0.022, dz), (0.022, dz + 0.003), (0, dz + 0.003)], s)  # drain
        add_box(P("Overflow", "Black_Trim"), (0.03, 0.004, 0.008), (0, D / 2 - deck - 0.035, zr - 0.03))
        # exposed P-trap to the wall and two supply lines with angle stops
        add_tube(ch, [(0, 0, z0 + 0.03), (0, 0, td * 0.2), (0, 0.06, 0.016), (0, 0.12, td * 0.2), (0, D / 2 - 0.02, td * 0.5)], 0.016, 8,
                 bend_radius=0.03, bend_steps=2 if d == 0 else 1)
        add_lathe(ch, (0, 0.06, 0), (0, 0, 1), [(0, 0), (0.018, 0), (0.018, 0.02), (0, 0.02)], s)  # trap clean-out cap (floor of the bound)
        for sx in (-1, 1):
            add_tube(ch, [(sx * 0.08, D / 2 - 0.03, td * 0.7), (sx * 0.08, yb, z0 + 0.01)], 0.004, 8)
        for sx in (-1, 1):  # wall brackets
            add_box(P("Brackets", "Black_Trim"), (0.03, 0.18, 0.02), (sx * (W / 2 - 0.08), D / 2 - 0.09, z0 + 0.01))
    else:
        add_cylinder_between(ch, (0, 0, 0), (0, 0, z0 + 0.03), 0.016, 8)
    return {"mount_z_m": round(k["rim_z_m"] - bh - td, 5), "collision_boxes": [collision_box("Basin", (0, 0, z0 + bh / 2), (W, D, bh))]}


def mirror(P, p, d, s, W, D, H):
    fw = 0.02
    fr = P("Frame", "Stainless")
    if d >= 3:
        add_box(fr, (W, D, H), (0, 0, H / 2))
        return {"mount_z_m": p["mount_z_m"]}
    for size, c in (((W, D, fw), (0, 0, fw / 2)), ((W, D, fw), (0, 0, H - fw / 2)), ((fw, D, H - 2 * fw), (-W / 2 + fw / 2, 0, H / 2)),
                    ((fw, D, H - 2 * fw), (W / 2 - fw / 2, 0, H / 2))):
        _bb(fr, size, c, d, 0.002, 0.002 if d == 0 else 0.0)
    add_box(P("Glass", "Mirror"), (W - 2 * fw, 0.006, H - 2 * fw), (0, -D / 2 + 0.006, H / 2))
    return {"mount_z_m": p["mount_z_m"]}


def toilet(P, p, d, s, W, D, H):
    k = p["toilet"]
    zr, bw, bl, td = k["rim_z_m"], k["bowl_w_m"], k["bowl_l_m"], k["tank_d_m"]
    china = P("China", "Vitreous_White")
    cs = (4, 2, 1, 0)[d]
    yb = -D / 2 + bl / 2  # bowl centre
    if d >= 3:
        add_box(china, (bw, bl, zr), (0, yb, zr / 2))
        add_box(china, (W, td, H - zr * 0.95), (0, D / 2 - td / 2, zr * 0.95 + (H - zr * 0.95) / 2))
        return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    rb = bw * 0.45  # oval corner radius
    if d <= 1:  # pedestal + trapway flaring up to the rim, then the open bowl cavity
        _rings(china, [(bw * 0.55, bl * 0.55, rb * 0.5, yb + bl * 0.12, 0), (bw * 0.6, bl * 0.6, rb * 0.55, yb + bl * 0.1, zr * 0.45),
                       (bw, bl, rb, yb, zr - 0.04), (bw, bl, rb, yb, zr - 0.005), (bw - 0.03, bl - 0.03, rb * 0.9, yb, zr),
                       (bw - 0.07, bl - 0.08, rb * 0.75, yb - 0.01, zr - 0.04), (bw * 0.3, bl * 0.3, rb * 0.25, yb - 0.02, zr - 0.2)], cs)
    else:
        _rings(china, [(bw * 0.6, bl * 0.6, rb * 0.5, yb + bl * 0.1, 0), (bw, bl, rb, yb, zr), (bw * 0.6, bl * 0.6, rb * 0.5, yb, zr - 0.1)], 1)
    tz0 = zr * 0.95
    _bb(china, (W, td, H - 0.03 - tz0), (0, D / 2 - td / 2, tz0 + (H - 0.03 - tz0) / 2), d, 0.02, 0.006)  # tank
    _bb(china, (W, td, 0.03), (0, D / 2 - td / 2, H - 0.015), d, 0.02, 0.008)  # tank lid
    seat = P("Seat", "Plastic_White")
    if d <= 1:  # seat ring + lid, hinges, flush lever
        _rings(seat, [(bw - 0.01, bl - 0.03, rb * 0.95, yb + 0.005, zr + 0.002), (bw - 0.01, bl - 0.03, rb * 0.95, yb + 0.005, zr + 0.022)], cs)
        _rings(seat, [(bw - 0.02, bl - 0.06, rb * 0.85, yb + 0.015, zr + 0.022), (bw - 0.03, bl - 0.07, rb * 0.8, yb + 0.015, zr + 0.04)], cs)  # lid
        for sx in (-1, 1):
            add_cylinder_between(P("Hinges", "Chrome"), (sx * 0.07, D / 2 - td - 0.02, zr + 0.02), (sx * 0.04, D / 2 - td - 0.02, zr + 0.02), 0.01, 8)
        add_cylinder_between(P("Hinges", "Chrome"), (-W / 2 + 0.06, D / 2 - td, H - 0.08), (-W / 2 + 0.06, D / 2 - td - 0.015, H - 0.08), 0.012, 8)
        add_box(P("Hinges", "Chrome"), (0.07, 0.01, 0.012), (-W / 2 + 0.06 + 0.035, D / 2 - td - 0.02, H - 0.08))
    else:
        _rings(seat, [(bw - 0.02, bl - 0.04, rb * 0.9, yb + 0.01, zr), (bw - 0.03, bl - 0.06, rb * 0.85, yb + 0.01, zr + 0.04)], 1)
    return {"moving_parts": [{"part": "Seat", "type": "hinge", "axis": "x"}],
            "collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def door_cabinet(P, p, d, s, W, D, H):
    k = p["cab"]
    hs, hr = k["pull_standoff_m"], 0.006
    yf = -D / 2 + hs + hr
    fin = k["finish"]
    if d >= 3:
        add_box(P("Body", fin), (W, D - hs - hr, H), (0, (yf + D / 2) / 2, H / 2))
        add_box(P("Pulls", "Brushed_Steel"), (0.1, hs + hr, 0.15), (0, -D / 2 + (hs + hr) / 2, H * 0.6))
        return {}
    _bb(P("Body", fin), (W, D / 2 - yf - 0.02, H), (0, (yf + 0.02 + D / 2) / 2, H / 2), d)
    moving = []
    for i, side in enumerate(("left", "right")):
        x = (-0.5 + i) * W / 2
        name = f"Door_{i}"
        _bb(P(name, fin), (W / 2 - 0.004, 0.02, H - 0.006), (x, yf + 0.01, H / 2), d, 0.003, 0.0015)
        px = x + (W / 4 - 0.04) * (1 if side == "left" else -1)
        add_handle_pull(P(name, fin), (px, yf, H * 0.6), min(0.128, H * 0.3), hs, hr, 8, axis="z", bend_steps=2 if d <= 1 else 0)
        moving.append(hinge_axis(name, x - W / 4 if side == "left" else x + W / 4, yf + 0.01, 0, H, side))
    shelves = [round(H * (i + 1) / (k["shelves"] + 1), 5) for i in range(k["shelves"])]
    return {"moving_parts": moving, "shelf_heights_m": shelves, "collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def grab_bar(P, p, d, s, W, D, H):
    """Stainless grab bar with flanges; W/H = length for horizontal/vertical; 1.5 in wall clearance."""
    vertical = p.get("vertical", False)
    L = H if vertical else W
    fr, br = (W if vertical else H) / 2, p["bar_r_m"]
    st = P("Bar", "Stainless")
    yb = -D / 2 + br
    if vertical:
        a0, a1 = (0, yb, fr), (0, yb, L - fr)
    else:
        a0, a1 = (-L / 2 + fr, yb, fr), (L / 2 - fr, yb, fr)
    if d >= 3:
        add_box(st, (W, D, H), (0, 0, H / 2))
        return {"mount_z_m": p["mount_z_m"]}
    for e in (a0, a1):  # flange disk on the wall + return leg
        add_lathe(st, (e[0], D / 2, e[2]), (0, -1, 0), [(0, 0), (fr, 0), (fr, 0.004), (br * 1.2, 0.008), (0, 0.008)], s if d <= 1 else 8)
        add_cylinder_between(st, (e[0], D / 2 - 0.006, e[2]), (e[0], yb + br, e[2]), br, s if d <= 1 else 8)
    add_cylinder_between(st, (a0[0], yb, a0[2]), (a1[0], yb, a1[2]), br, s if d <= 1 else 8)
    return {"mount_z_m": p["mount_z_m"]}


def dispenser(P, p, d, s, W, D, H):
    k = p["disp"]
    b = P("Body", k["body"])
    if d >= 3:
        add_box(b, (W, D, H), (0, 0, H / 2))
        return {"mount_z_m": p["mount_z_m"]}
    t = k["type"]
    if t == "sconce":
        _bb(b, (W, 0.02, H), (0, D / 2 - 0.01, H / 2), d, 0.01, 0.003)
        add_lathe(P("Shade", "Glass_Frosted"), (0, D / 2 - 0.02 - (D - 0.02) / 2, 0), (0, 0, 1),
                  [(0, 0.02), ((D - 0.02) / 2, 0.02), ((D - 0.02) / 2, H - 0.02), (0, H - 0.02)], s)
        return {"mount_z_m": p["mount_z_m"], "emissive_parts": ["Shade"]}
    _bb(b, (W, D, H), (0, 0, H / 2), d, 0.01 if t != "towel" else 0.006, 0.004)
    if t == "towel" and d <= 2:  # window, side lever, dispensing slot
        add_box(P("Window", "Glass_Dark"), (W * 0.3, 0.003, H * 0.25), (0, -D / 2 - 0.0005 + 0.002, H * 0.6))
        add_box(P("Slot", "Black_Trim"), (W * 0.7, 0.02, 0.006), (0, -D / 2 + 0.03, 0.003))
        add_box(P("Lever", "Stainless"), (0.01, D * 0.5, H * 0.3), (W / 2 - 0.005, 0, H * 0.4))
    elif t == "tp" and d <= 2:
        for sx in (-1, 1):
            add_lathe(P("Roll", "Paper_White"), (sx * W * 0.24, -D / 2 + 0.06, 0.0), (0, 0, 1), [(0, 0.004), (0.055, 0.004), (0.055, 0.1), (0, 0.1)], s)
    elif t == "soap" and d <= 2:
        add_box(P("Window", "Glass_Dark"), (W * 0.5, 0.002, H * 0.3), (0, -D / 2 + 0.001, H * 0.55))
        add_box(P("Lever", "Black_Trim"), (W * 0.6, 0.015, 0.025), (0, -D / 2 + 0.0075, H * 0.2))
    elif t == "napkin" and d <= 2:
        add_box(P("Lever", "Black_Trim"), (W * 0.8, 0.003, 0.01), (0, -D / 2 + 0.0015, H * 0.9))
    return {"mount_z_m": p["mount_z_m"]}


KINDS = {"lavatory": lavatory, "mirror": mirror, "toilet": toilet, "door_cabinet": door_cabinet, "grab_bar": grab_bar, "dispenser": dispenser}


def build(p, lod):
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"], W, D, H)
    extra = dict(extra, fixture_family="restroom", rf=p["rf"], seed=int(p["seed"]))
    extra.update(wear(p))
    return P.finish(), (W, H, D), extra
