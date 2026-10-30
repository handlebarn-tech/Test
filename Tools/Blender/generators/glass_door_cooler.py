"""Glass-door cooler + fridges (PROC-005 §7; IMP-003 drop 3 rewritten). Variants (ROOM_FIXTURES sizes):
- glass_cooler: Cooler_GlassDoor_2Door 4.0 x 2.5 x 6.5 ft, black frame, internally lit (LED strips emissive), wire
  shelves with clips and price-tag rails, louvred base grille, blank label plate on the header. Each door =
  DoorFrame_nn + Glass_nn + Handle_nn (+ Gasket_nn) with a hinge axis (K3, C10); handles stand off the door face (K2).
- fridge: Fridge_TopFreezer 2.2 x 2.3 x 5.5 ft white (FOH) and Fridge_Magnets 2.8 x 2.4 x 5.8 ft (break room,
  magnet-covered side, seeded layout): freezer/fresh doors with seals, pulls, hinge caps, toe grille.
Contents per DEC-050 are recorded, never modelled (cooler: concentrates + perishable edibles; FOH fridge: drinks).
Component sizes (frame, shelf count, handles, magnets) are GAP-PROC-17. Origin = bottom centre, front = -Y; handles
reach the front bound. LOD0 full; LOD1 no clips/louvres/magnets detail; LOD2 plain doors/shelves; LOD3 blocks."""
import random

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_handle_pull, add_wire_grid, collision_box,
                     hinge_axis, to_unity, wear)


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


def glass_cooler(P, p, d, s):
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    c = p["cooler"]
    hs, hr, hw = c["handle_standoff_m"], c["handle_r_m"], c["handle_len_m"]
    yf = -D / 2 + hs + hr  # door front face; handles reach -D/2
    st, hd, bs, dt = c["side_t_m"], c["header_h_m"], c["base_h_m"], c["door_t_m"]
    nd = c["doors"]
    frame = P("Cabinet", "Black_Frame")
    if d >= 3:
        add_box(frame, (W, D - hs - hr, H), (0, (yf + D / 2) / 2, H / 2))
        add_box(P("Handles", "Black_Metal"), (W * 0.1, hs + hr, hw), (0, -D / 2 + (hs + hr) / 2, bs + (H - hd - bs) / 2))
        return (W, H, D), {}
    yc = yf + dt  # cabinet face behind the doors
    # cabinet shell: sides, top, back, header with a blank plate, base with a louvred grille
    for sx in (-1, 1):
        _bb(frame, (st, D / 2 - yc, H), (sx * (W / 2 - st / 2), (yc + D / 2) / 2, H / 2), d)
    add_box(frame, (W - 2 * st, D / 2 - yc, 0.03), (0, (yc + D / 2) / 2, H - 0.015))
    add_box(frame, (W - 2 * st, 0.03, H), (0, D / 2 - 0.015, H / 2))
    _bb(frame, (W - 2 * st, dt, hd), (0, yf + dt / 2, H - hd / 2), d)
    _bb(frame, (W - 2 * st, dt, bs), (0, yf + dt / 2, bs / 2), d)
    add_box(P("Plate", "Plate_Blank"), (W * 0.4, 0.002, hd * 0.45), (0, yf - 0.001, H - hd / 2))
    if d <= 1:
        grille = P("Grille", "Black_Metal")
        for i in range(int(bs / 0.012) - 2):  # louvres
            add_box(grille, (W - 2 * st - 0.06, 0.004, 0.005), (0, yf - 0.0015, 0.02 + i * 0.012))
    # interior: lit back, shelves, LED strips
    zi0, zi1 = bs, H - hd
    add_box(P("Interior", "Interior_White"), (W - 2 * st, 0.01, zi1 - zi0), (0, D / 2 - 0.035, (zi0 + zi1) / 2))
    led = P("LED", "LED_Emissive")
    dw = (W - 2 * st) / nd
    shelves = P("Shelves", "Wire_Grey")
    sd = D / 2 - 0.05 - yc - 0.03
    sy = yc + 0.03 + sd / 2
    for i in range(nd):
        x0 = -W / 2 + st + i * dw
        add_box(led, (0.012, 0.006, zi1 - zi0 - 0.04), (x0 + (dw if i < nd - 1 else dw - 0.01), yc + 0.01, (zi0 + zi1) / 2))
        for k in range(c["shelves"]):
            z = zi0 + (zi1 - zi0) * (k + 1) / (c["shelves"] + 1)
            if d <= 1:
                add_wire_grid(shelves, dw - 0.03, sd, z, 0.004, c["wire_pitch_m"] * (1 if d == 0 else 2), sd / 3, 6, (x0 + dw / 2, sy))
                add_box(P("TagRails", "Plastic_White"), (dw - 0.03, 0.004, 0.03), (x0 + dw / 2, sy - sd / 2 - 0.002, z - 0.01))
                if d == 0:
                    for cx in (x0 + 0.02, x0 + dw - 0.02):
                        for cy in (sy - sd / 2 + 0.02, sy + sd / 2 - 0.02):
                            add_box(shelves, (0.012, 0.012, 0.02), (cx, cy, z - 0.01))  # shelf clips
            else:
                add_box(shelves, (dw - 0.03, sd, 0.008), (x0 + dw / 2, sy, z))
    # doors
    moving = []
    for i in range(nd):
        x0, x1 = -W / 2 + st + i * dw, -W / 2 + st + (i + 1) * dw
        xm = (x0 + x1) / 2
        side = "left" if i < nd / 2 else "right"
        hx = x0 if side == "left" else x1
        df, gl = P(f"DoorFrame_{i:02d}", "Black_Frame"), P(f"Glass_{i:02d}", "Glass_Clear")
        rail = c["rail_w_m"]
        zc, zh = (zi0 + zi1) / 2, zi1 - zi0
        for size, ctr in (((dw - 0.004, dt, rail), (xm, yf + dt / 2, zi1 - rail / 2)), ((dw - 0.004, dt, rail * 1.4), (xm, yf + dt / 2, zi0 + rail * 0.7)),
                          ((rail, dt, zh), (x0 + 0.002 + rail / 2, yf + dt / 2, zc)), ((rail, dt, zh), (x1 - 0.002 - rail / 2, yf + dt / 2, zc))):
            _bb(df, size, ctr, d, 0.003, 0.0015)
        add_box(gl, (dw - 2 * rail, 0.008, zh - 2.4 * rail), (xm, yf + dt / 2, zi0 + 1.4 * rail + (zh - 2.4 * rail) / 2))
        hxp = x1 - rail / 2 - 0.002 if side == "left" else x0 + rail / 2 + 0.002  # pull on the latch side
        add_handle_pull(P(f"Handle_{i:02d}", "Black_Metal"), (hxp, yf, zc), hw, hs, hr, 8, axis="z",  # 8 sides: the grip defines the front bound (C11)
                        bend_steps=3 if d == 0 else 1)
        if d <= 1:
            gk = P(f"Gasket_{i:02d}", "Rubber_Black")
            add_box(gk, (dw - 0.01, 0.006, 0.01), (xm, yf + dt + 0.003 - 0.006, zi1 - 0.005))
            add_box(gk, (dw - 0.01, 0.006, 0.01), (xm, yf + dt + 0.003 - 0.006, zi0 + 0.005))
            for zz in (zi1 - 0.02, zi0 + 0.02):  # hinge pins
                add_cylinder_between(P("Hinges", "Black_Metal"), (hx + (0.01 if side == "left" else -0.01), yf + dt * 0.5, zz - 0.02),
                                     (hx + (0.01 if side == "left" else -0.01), yf + dt * 0.5, zz + 0.02), 0.006, s)
            if d == 0:  # door closer on the header
                add_box(P("Hinges", "Black_Metal"), (0.12, 0.02, 0.03), (hx + (0.08 if side == "left" else -0.08), yf - 0.01, H - hd + 0.03))
        moving.append(dict(hinge_axis(f"DoorFrame_{i:02d}", hx, yf + dt / 2, zi0, zi1, side),
                           group=[f"DoorFrame_{i:02d}", f"Glass_{i:02d}", f"Handle_{i:02d}", f"Gasket_{i:02d}"]))
    anchors = [{"id": f"D{i}_Shelf_{k:02d}", "position_unity_xyz": to_unity(-W / 2 + st + (i + 0.5) * dw, sy, zi0 + (zi1 - zi0) * (k + 1) / (c["shelves"] + 1)),
                "size_m_unity_xz": [round(dw - 0.05, 5), round(sd - 0.02, 5)]} for i in range(nd) for k in range(c["shelves"])]
    return (W, H, D), {"moving_parts": moving, "shelf_anchors": anchors, "emissive_parts": ["LED", "Interior"],
                       "collision_boxes": [collision_box("Body", (0, (yf + D / 2) / 2, H / 2), (W, D / 2 - yf, H))]}


def fridge(P, p, d, s):
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    f = p["fridge"]
    hs, hr, hw = f["handle_standoff_m"], f["handle_r_m"], f["handle_len_m"]
    yf = -D / 2 + hs + hr
    dt, gap, zsplit, kick = f["door_t_m"], f["door_gap_m"], H * f["freezer_split"], f["kick_h_m"]
    mag = f.get("magnets_side")
    mt = 0.004 if mag else 0.0
    body = P("Body", f["finish"])
    if d >= 3:
        add_box(body, (W - mt, D / 2 - yf, H), (-mt / 2, (yf + D / 2) / 2, H / 2))
        add_box(P("Handles", "Handle_Grey"), (0.03, hs + hr, H * 0.5), (-W / 2 + 0.06, -D / 2 + (hs + hr) / 2, H / 2))
        if mag:
            add_box(P("Magnets", "Magnets_Mixed"), (mt, D * 0.6, H * 0.5), (W / 2 - mt / 2, 0, H * 0.55))
        return (W, H, D), {}
    bw = W - mt
    bx = -mt / 2 if mag else 0.0  # body shifted away from the magnet side
    yb = yf + dt
    _bb(body, (bw, D / 2 - yb, H), (bx, (yb + D / 2) / 2, H / 2), d, 0.02, 0.006)
    doors = []
    for name, z0, z1 in (("FreezerDoor", zsplit + gap / 2, H - 0.005), ("FreshDoor", kick, zsplit - gap / 2)):
        door = P(name, f["finish"])
        _bb(door, (bw - 0.01, dt, z1 - z0), (bx, yf + dt / 2, (z0 + z1) / 2), d, 0.02, 0.008)
        hz = z0 + (z1 - z0) * (0.25 if name == "FreezerDoor" else 0.75)
        hlen = min(hw, (z1 - z0) * 0.6)
        add_handle_pull(P(f"Handle_{name}", "Handle_Grey"), (bx - bw / 2 + 0.05, yf, hz), hlen, hs, hr, 8, axis="z",  # 8 sides: the grip defines the front bound (C11)
                        bend_steps=3 if d == 0 else 1)
        if d <= 1:  # door seal
            add_box(P(f"Seal_{name}", "Rubber_Grey"), (bw - 0.03, 0.006, z1 - z0 - 0.02), (bx, yb + 0.002, (z0 + z1) / 2))
        doors.append(dict(hinge_axis(name, bx + bw / 2 - 0.01, yf + dt / 2, z0, z1, "right"), group=[name, f"Handle_{name}", f"Seal_{name}"]))
    add_box(P("Grille", "Black_Plastic"), (bw - 0.06, 0.01, kick - 0.02), (bx, yb + 0.004, kick / 2))
    if d <= 1:
        for zz in (H - 0.004, zsplit, kick):  # hinge caps on the right side
            add_box(P("Grille", "Black_Plastic"), (0.04, dt * 0.8, 0.008), (bx + bw / 2 - 0.025, yf + dt / 2, zz))
    if mag and d == 2:  # one magnet-layer slab keeps the side bound
        add_box(P("Magnets", "Magnets_Mixed"), (mt, D * 0.6, H * 0.5), (W / 2 - mt / 2, 0, H * 0.55))
    if mag and d <= 1:
        rng = random.Random(int(p["seed"]))
        mg = P("Magnets", "Magnets_Mixed")
        for _ in range(f["magnet_count"] if d == 0 else f["magnet_count"] // 3):
            sz, sy_, z = rng.uniform(0.03, 0.09), rng.uniform(-D / 2 + 0.12, D / 2 - 0.12), rng.uniform(H * 0.25, H * 0.9)
            add_box(mg, (mt, sz, sz * rng.uniform(0.6, 1.3)), (W / 2 - mt / 2, sy_, z))
    contents = {"contents": p["contents"]} if p.get("contents") else {}
    return (W, H, D), dict(contents, moving_parts=doors,
                           collision_boxes=[collision_box("Body", (0, (yf + D / 2) / 2, H / 2), (W, D / 2 - yf, H))])


KINDS = {"glass_cooler": glass_cooler, "fridge": fridge}


def build(p, lod):
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    expected, extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"])
    extra = dict(extra, fixture_family="cooler_fridge", rf=p["rf"], seed=int(p["seed"]))
    if p.get("contents"):
        extra["contents"] = p["contents"]
    extra.update(wear(p))
    return P.finish(), expected, extra
