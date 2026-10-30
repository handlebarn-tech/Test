"""Glass-door cooler + fridges (PROC-005 §7; fix wave REVIEW-PROC5 #1/#7). Variants (ROOM_FIXTURES sizes):
- glass_cooler: Cooler_GlassDoor_2Door 4.0 x 2.5 x 6.5 ft, black frame, internally lit (RF notes, RI §2.3 row 230).
  Built as a real merchandiser: sheet-metal sides with rounded front edges, header and louvred kick panel, centre
  mullion, levellers; interior liner with slotted shelf pilasters, wire shelves (frame + deck + clips + tag rail) and
  LED strips; doors = extruded frame with rounded edges, double-glazed unit (two panes + spacer, glazing bead),
  magnetic gasket, hinge covers, door closer, long pull handle. Each door = DoorFrame_nn + Glass_nn + Handle_nn +
  Gasket_nn with a hinge axis (K3, C10); handles stand off the door face (K2) and define the front bound.
- fridge: Fridge_TopFreezer 2.2 x 2.3 x 5.5 ft white (FOH still) and Fridge_Magnets 2.8 x 2.4 x 5.8 ft (break room,
  magnet-covered side, R3C5): pillowed doors, magnetic gaskets with door liners, pulls, hinge covers, louvred kick
  grille, levellers; Fridge_Magnets carries a seeded GAP-PROC-28 assortment of cards, discs, tiles and papers.
Contents per DEC-050 are recorded, never modelled. Every size/count/colour cites its source in params `_sources`.
Origin = bottom centre, front = -Y. LOD0 full; LOD1 coarser rounding, no clips/teeth/magnet detail; LOD2 plain
boxes; LOD3 blocks."""
import math
import random

from proclib import (Parts, add_box, add_cylinder_between, add_handle_pull, add_lathe, add_screw_head, add_tube,
                     add_wire_grid, collision_box, hinge_axis, rounded_rect, to_unity, wear)

import bmesh


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


# --- local construction helpers (shared with janitor_props) -------------------------------------------------------

def _mapper(face, c):
    """Local (a = width, b = height, t = thickness, t < 0 = the outward face) to world for a panel facing `face`."""
    cx, cy, cz = c
    return {"-y": lambda a, b, t: (cx + a, cy + t, cz + b),
            "+y": lambda a, b, t: (cx - a, cy - t, cz + b),
            "+x": lambda a, b, t: (cx - t, cy + a, cz + b),
            "-x": lambda a, b, t: (cx + t, cy - a, cz + b),
            "+z": lambda a, b, t: (cx + a, cy + b, cz - t),
            "-z": lambda a, b, t: (cx + a, cy - b, cz + t)}[face]


def _new_faces(bm, n0):
    bm.faces.ensure_lookup_table()
    return [bm.faces[i] for i in range(n0, len(bm.faces))]


def _rings_to_faces(bm, rings, closed, caps):
    n0 = len(bm.faces)
    vs = [[bm.verts.new(p) for p in r] for r in rings]
    n = len(vs[0])
    pairs = list(zip(vs, vs[1:])) + ([(vs[-1], vs[0])] if closed else [])
    for a, b in pairs:
        for i in range(n):
            bm.faces.new([a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]])
    if caps:
        bm.faces.new(vs[0][::-1])
        bm.faces.new(vs[-1])
    bmesh.ops.recalc_face_normals(bm, faces=_new_faces(bm, n0))


def _edge_steps(r, seg, t):
    """(inset, depth) pairs walking the outward face's rounded edge: back face -> front face."""
    if r <= 0 or seg < 1:
        return [(0.0, t / 2), (0.0, -t / 2)]
    out = [(0.0, t / 2), (0.0, -t / 2 + r)]
    for i in range(1, seg + 1):
        a = math.pi / 2 * i / seg
        out.append((r * (1 - math.cos(a)), -t / 2 + r - r * math.sin(a)))
    return out


def rpanel(bm, face, center, u, v, t, r=0.0, seg=0, rc=0.0, cseg=0):
    """Panel u x v x t with all edges of the outward face rounded (radius r, seg steps) and in-plane corner radius rc."""
    m = _mapper(face, center)
    r = min(r, t * 0.95, u * 0.45, v * 0.45)
    rc = max(rc, r + 1e-4) if cseg and r > 0 else rc
    rings = [[m(a, b, tt) for a, b in rounded_rect(u, v, rc, cseg, ins)] for ins, tt in _edge_steps(r, seg, t)]
    _rings_to_faces(bm, rings, closed=False, caps=True)


def rframe(bm, face, center, u, v, t, opening, r=0.0, seg=0, rc=0.0, ri=0.0, cseg=0):
    """Picture-frame extrusion: outer u x v, opening (w, h, da, db) offset (da, db) from the centre; outer and
    opening front edges rounded with radius r. Closed loft (no caps)."""
    m = _mapper(face, center)
    ow, oh, da, db = opening
    r = min(r, t * 0.95)
    rc = max(rc, r + 1e-4) if cseg and r > 0 else rc
    rings = [[m(a, b, tt) for a, b in rounded_rect(u, v, rc, cseg, ins)] for ins, tt in _edge_steps(r, seg, t)]
    for ins, tt in reversed(_edge_steps(r, seg, t)):  # opening: front -> back, growing outward at the front
        rings.append([m(a + da, b + db, tt) for a, b in rounded_rect(ow, oh, ri, cseg, -ins)])
    _rings_to_faces(bm, rings, closed=True, caps=False)


def prism_x(bm, poly_yz, x0, x1):
    """Extrude a convex (y, z) polygon along X (louvre slats, channels)."""
    _rings_to_faces(bm, [[(x0, y, z) for y, z in poly_yz], [(x1, y, z) for y, z in poly_yz]], closed=False, caps=True)


def loop_tube(bm, face, center, u, v, rc, cseg, radius, segs=6, depth=0.0):
    """Closed round tube along a rounded rectangle in a panel plane (gaskets, glazing beads, shelf frames)."""
    m = _mapper(face, center)
    add_tube(bm, [m(a, b, depth) for a, b in rounded_rect(u, v, rc, cseg)], radius, segs, closed=True)


def leveller(bm, x, y, h, s, pad_r=0.018):
    """Levelling foot: rubber pad, threaded stem, lock nut (z 0..h)."""
    add_lathe(bm, (x, y, 0), (0, 0, 1), [(0, 0), (pad_r, 0), (pad_r, 0.004), (pad_r * 0.7, 0.007), (0.005, 0.007),
                                          (0.005, h - 0.008), (0.011, h - 0.008), (0.011, h - 0.002), (0.006, h - 0.002),
                                          (0.006, h), (0, h)], s)


def louvres(bm, x0, x1, y_face, z0, z1, pitch, depth=0.02):
    """Angled louvre slats in a vent opening (front face at y_face, sloping back and down)."""
    n = max(1, int((z1 - z0) / pitch))
    for i in range(n):
        zb = z0 + (z1 - z0) * (i + 0.15) / n
        zt = zb + pitch * 0.55
        prism_x(bm, [(y_face, zt), (y_face + depth, zb), (y_face + depth, zb - 0.003), (y_face, zt - 0.003)], x0, x1)


def _bb(bm, face, center, u, v, t, d, r=0.003, rc=0.006):
    if d >= 2:
        sz = {"-y": (u, t, v), "+y": (u, t, v), "+x": (t, u, v), "-x": (t, u, v), "+z": (u, v, t), "-z": (u, v, t)}[face]
        add_box(bm, sz, center)
    else:
        rpanel(bm, face, center, u, v, t, r, 3 if d == 0 else 1, rc, 3 if d == 0 else 1)


# --- glass-door merchandiser ---------------------------------------------------------------------------------------

def glass_cooler(P, p, d, s):
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    c = p["cooler"]
    hs, hr, hw = c["handle_standoff_m"], c["handle_r_m"], c["handle_len_m"]
    yf = -D / 2 + hs + hr  # door front face; handle grips reach -D/2
    st, hd, bs, dt, mw, lh = c["side_t_m"], c["header_h_m"], c["base_h_m"], c["door_t_m"], c["mullion_w_m"], c["leveller_h_m"]
    nd, ns = c["doors"], c["shelves"]
    frame = P("Cabinet", "Black_Frame")
    if d >= 3:
        add_box(frame, (W, D / 2 - yf, H), (0, (yf + D / 2) / 2, H / 2))
        add_box(P("Handles", "Hardware_Grey"), (W * 0.1, hs + hr, hw), (0, -D / 2 + (hs + hr) / 2, bs + (H - hd - bs) / 2))
        return (W, H, D), {}
    yc = yf + dt  # cabinet face behind the doors
    zi0, zi1 = bs, H - hd  # door opening
    iw = W - 2 * st
    # shell: sides wrap the doors (front edge at the door face), top, back, header, kick panel
    for sx, face in ((-1, "-x"), (1, "+x")):
        _bb(frame, face, (sx * (W / 2 - st / 2), (yf + D / 2) / 2, lh + (H - lh) / 2), D / 2 - yf, H - lh, st, d, 0.008, 0.012)
    _bb(frame, "+z", (0, (yf + D / 2) / 2, H - 0.015), iw, D / 2 - yf, 0.03, d)
    add_box(frame, (iw, 0.02, H - lh - 0.03), (0, D / 2 - 0.01, lh + (H - lh - 0.03) / 2))
    _bb(frame, "-y", (0, yf + dt / 2, H - hd / 2), iw, hd, dt, d, 0.006, 0.008)
    kick = P("Kick", "Black_Frame")
    if d <= 1:
        rframe(kick, "-y", (0, yf + 0.01, lh + (bs - lh) / 2), iw, bs - lh, 0.02, (iw - 0.12, bs - lh - 0.05, 0, 0),
               0.004, 2 if d == 0 else 1, 0.008, 0.004, 2 if d == 0 else 1)
        add_box(kick, (iw - 0.12, 0.004, bs - lh - 0.05), (0, yf + 0.045, lh + (bs - lh) / 2))  # dark plenum behind
        louvres(P("Grille", "Black_Frame"), -iw / 2 + 0.06, iw / 2 - 0.06, yf + 0.012, lh + 0.025, bs - 0.025,
                0.012 if d == 0 else 0.024)
    else:
        add_box(kick, (iw, 0.02, bs - lh), (0, yf + 0.01, lh + (bs - lh) / 2))
    add_box(frame, (iw, D / 2 - yf - 0.02, 0.02), (0, (yf + D / 2 - 0.02) / 2, lh + 0.01))  # base pan
    lev = P("Levellers", "Hardware_Grey")
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (W / 2 - 0.06), (yf + 0.06 if sy < 0 else D / 2 - 0.06)
            if d <= 1:
                leveller(lev, x, y, lh, s)
            else:
                add_box(lev, (0.03, 0.03, lh), (x, y, lh / 2))
    if d <= 1:  # header screws
        sc = P("Screws", "Hardware_Grey")
        for x in (-iw / 2 + 0.04, -iw / 6, iw / 6, iw / 2 - 0.04):
            add_screw_head(sc, (x, yf, H - hd / 2), (0, -1, 0), 0.004, 8)
    # mullion between the doors
    dw = (iw - mw * (nd - 1)) / nd
    for i in range(1, nd):
        xm = -iw / 2 + i * dw + (i - 0.5) * mw
        _bb(frame, "-y", (xm, yf + dt / 2 + 0.004, (zi0 + zi1) / 2), mw, zi1 - zi0, dt - 0.008, d)
    # interior: liner (side, back, ceiling), pilasters, LEDs, shelves
    liner = P("Interior", "Interior_White")
    yb = D / 2 - 0.06  # back liner face
    add_box(liner, (iw, 0.01, zi1 - zi0), (0, yb + 0.005, (zi0 + zi1) / 2))
    for sx in (-1, 1):
        add_box(liner, (0.01, yb - yc, zi1 - zi0), (sx * (iw / 2 - 0.005), (yc + yb) / 2, (zi0 + zi1) / 2))
    add_box(liner, (iw, yb - yc, 0.01), (0, (yc + yb) / 2, zi1 - 0.005))
    add_box(liner, (iw, yb - yc, 0.01), (0, (yc + yb) / 2, zi0 + 0.005))
    led = P("LED", "LED_Emissive")
    pil = P("Pilasters", "Wire_Grey")
    shelves = P("Shelves", "Wire_Grey")
    tags = P("TagRails", "TagRail_Grey")
    sd = yb - yc - 0.05
    sy = yc + 0.03 + sd / 2
    pitch = 0.0254
    anchors = []
    for i in range(nd):
        x0 = -iw / 2 + i * (dw + mw)
        x1 = x0 + dw
        xm = (x0 + x1) / 2
        # LED strip on each side of the bay, just behind the frame (internally lit, RF)
        for xl in (x0 + 0.012, x1 - 0.012):
            add_box(led, (0.01, 0.008, zi1 - zi0 - 0.06), (xl, yc + 0.012, (zi0 + zi1) / 2))
            if d == 0:
                add_box(liner, (0.016, 0.004, zi1 - zi0 - 0.05), (xl, yc + 0.018, (zi0 + zi1) / 2))  # diffuser lip
        # slotted pilasters: front and back on both sides of the bay
        pys = (yc + 0.05, yb - 0.02)
        for xp in (x0 + 0.012, x1 - 0.012):
            for yp in pys:
                add_box(pil, (0.012, 0.016, zi1 - zi0 - 0.04), (xp, yp, (zi0 + zi1) / 2))
                if d == 0:
                    for k in range(int((zi1 - zi0 - 0.08) / (pitch * 2))):
                        add_box(liner, (0.013, 0.004, 0.012), (xp, yp - 0.007, zi0 + 0.04 + k * pitch * 2))  # slots
        for k in range(ns):
            z = zi0 + (zi1 - zi0) * (k + 1) / (ns + 1)
            sw = dw - 0.04
            if d <= 1:
                loop_tube(shelves, "+z", (xm, sy, z), sw, sd, 0.008, 2 if d == 0 else 1, 0.003, 6)
                add_wire_grid(shelves, sw - 0.01, sd - 0.01, z - 0.004, 0.0035, c["wire_pitch_m"] * (1 if d == 0 else 2), None, 6, (xm, sy))
                for xx in (-sw / 2 + 0.02, 0, sw / 2 - 0.02):  # support bars under the deck
                    add_box(shelves, (0.006, sd - 0.01, 0.012), (xm + xx, sy, z - 0.014))
                prism_x(tags, [(sy - sd / 2 - 0.004, z + 0.004), (sy - sd / 2 + 0.004, z + 0.004), (sy - sd / 2 + 0.004, z - 0.03),
                               (sy - sd / 2 - 0.004, z - 0.03)], xm - sw / 2, xm + sw / 2)
                if d == 0:
                    for xp in (x0 + 0.012, x1 - 0.012):
                        for yp in pys:
                            add_box(pil, (0.02, 0.02, 0.025), (xp + (0.008 if xp < xm else -0.008), yp, z - 0.012))  # clips
            else:
                add_box(shelves, (sw, sd, 0.01), (xm, sy, z))
            anchors.append({"id": f"D{i}_Shelf_{k:02d}", "position_unity_xyz": to_unity(xm, sy, z),
                            "size_m_unity_xz": [round(sw - 0.02, 5), round(sd - 0.02, 5)]})
    # doors
    moving = []
    rail = c["rail_w_m"]
    zc, zh = (zi0 + zi1) / 2, zi1 - zi0
    for i in range(nd):
        x0 = -iw / 2 + i * (dw + mw)
        x1 = x0 + dw
        xm = (x0 + x1) / 2
        side = "left" if i < nd / 2 else "right"
        hx = x0 if side == "left" else x1
        df, gl, gk = P(f"DoorFrame_{i:02d}", "Black_Frame"), P(f"Glass_{i:02d}", "Glass_Clear"), P(f"Gasket_{i:02d}", "Gasket_Grey")
        uw, uh = dw - 0.004, zh - 0.004
        ow_, oh_ = uw - 2 * rail, uh - rail * 2.4
        ob = (rail * 1.4 - rail) / 2  # taller bottom rail: opening shifted up
        if d <= 1:
            rframe(df, "-y", (xm, yf + dt / 2, zc), uw, uh, dt, (ow_, oh_, 0, ob), 0.008, 3 if d == 0 else 1,
                   0.01, 0.004, 3 if d == 0 else 1)
            for yy in (yf + 0.012, yf + 0.032):  # double-glazed unit: two panes, spacer between
                add_box(gl, (ow_ + 0.02, 0.004, oh_ + 0.02), (xm, yy, zc + ob))
            rframe(gk, "-y", (xm, yf + 0.022, zc + ob), ow_ + 0.02, oh_ + 0.02, 0.016, (ow_ - 0.012, oh_ - 0.012, 0, 0))  # spacer
            loop_tube(gk, "-y", (xm, yf + 0.0085, zc + ob), ow_ + 0.002, oh_ + 0.002, 0.004, 2 if d == 0 else 1, 0.0025, 6)  # bead
            loop_tube(gk, "-y", (xm, yc + 0.002, zc), uw - 0.02, uh - 0.02, 0.012, 2 if d == 0 else 1, 0.005, 8 if d == 0 else 6)  # gasket
        else:
            for size, ctr in (((uw, dt, rail), (xm, yf + dt / 2, zi1 - rail / 2)), ((uw, dt, rail * 1.4), (xm, yf + dt / 2, zi0 + rail * 0.7)),
                              ((rail, dt, zh), (x0 + 0.002 + rail / 2, yf + dt / 2, zc)), ((rail, dt, zh), (x1 - 0.002 - rail / 2, yf + dt / 2, zc))):
                add_box(df, size, ctr)
            add_box(gl, (ow_, 0.008, oh_), (xm, yf + dt / 2, zc + ob))
        hxp = x1 - rail / 2 - 0.002 if side == "left" else x0 + rail / 2 + 0.002  # pull on the latch side
        add_handle_pull(P(f"Handle_{i:02d}", "Hardware_Grey"), (hxp, yf, zc), hw, hs, hr, 8, axis="z",  # 8 sides: grip = front bound (C11)
                        bend_steps=3 if d == 0 else 1)
        if d <= 1:
            hg = P("Hinges", "Hardware_Grey")
            hxx = hx + (0.022 if side == "left" else -0.022)
            for zz, sgn in ((zi1, 1), (zi0, -1)):  # hinge covers top and bottom, over the pivot
                rpanel(hg, "-y", (hxx, yf - 0.004, zz + sgn * 0.012), 0.04, 0.03, 0.012, 0.004, 2 if d == 0 else 1, 0.006, 2 if d == 0 else 1)
            if d == 0:  # torque closer housing on the header
                rpanel(hg, "-y", (hx + (0.1 if side == "left" else -0.1), yf - 0.006, H - hd + 0.035), 0.14, 0.035, 0.012, 0.004, 2, 0.008, 2)
        moving.append(dict(hinge_axis(f"DoorFrame_{i:02d}", hx, yf + dt / 2, zi0, zi1, side),
                           group=[f"DoorFrame_{i:02d}", f"Glass_{i:02d}", f"Handle_{i:02d}", f"Gasket_{i:02d}"]))
    return (W, H, D), {"moving_parts": moving, "shelf_anchors": anchors, "emissive_parts": ["LED", "Interior"],
                       "collision_boxes": [collision_box("Body", (0, (yf + D / 2) / 2, H / 2), (W, D / 2 - yf, H))]}


# --- apartment fridges ---------------------------------------------------------------------------------------------

def _magnets(P, f, W, D, H, mt, seed, n):
    """Seeded assortment of generic fridge-side items on the +X face (GAP-PROC-28): paper sheets held by disc magnets,
    photo/card rectangles (slightly rotated), round discs, rounded tiles. Thicknesses vary so overlaps never coincide."""
    rng = random.Random(seed)
    xf = W / 2 - mt  # body side face
    mats = ["Magnet_Grey_A", "Magnet_Grey_B", "Magnet_Grey_C"]
    paper = P("Magnets_Paper", "Magnet_Paper")

    def poly(bm, pts, t):
        prism_x(bm, pts, xf, xf + t)

    def rect(cy, cz, w, h, ang):
        ca, sa = math.cos(ang), math.sin(ang)
        return [(cy + x * ca - z * sa, cz + x * sa + z * ca) for x, z in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]

    y0, y1, z0, z1 = -D / 2 + 0.05, D / 2 - 0.06, H * 0.2, H * 0.94
    for k in range(n):
        kind = rng.choices(["paper", "card", "disc", "tile"], [3, 6, 2, 3])[0]
        cy, cz = rng.uniform(y0, y1), rng.uniform(z0, z1)
        bm = P(f"Magnets_{mats[k % 3][-1]}", mats[k % 3])
        if kind == "paper":
            w, h = rng.uniform(0.15, 0.22), rng.uniform(0.2, 0.28)
            cy, cz = min(max(cy, y0 + w / 2), y1 - w / 2), min(max(cz, z0 + h / 2), z1 - h / 2)
            poly(paper, rect(cy, cz, w, h, rng.uniform(-0.06, 0.06)), 0.0006 + 0.0001 * (k % 5))
            add_lathe(bm, (xf, cy + rng.uniform(-0.03, 0.03), cz + h / 2 - 0.02), (1, 0, 0),
                      [(0, 0), (0.012, 0), (0.012, 0.004), (0.01, 0.006), (0, 0.006)], 12)
        elif kind == "card":
            w, h = rng.uniform(0.05, 0.11), rng.uniform(0.04, 0.09)
            poly(bm, rect(cy, cz, w, h, rng.uniform(-0.15, 0.15)), rng.uniform(0.0015, 0.0028))
        elif kind == "disc":
            r = rng.uniform(0.012, 0.03)
            add_lathe(bm, (xf, cy, cz), (1, 0, 0), [(0, 0), (r, 0), (r, 0.003), (r * 0.85, rng.uniform(0.004, 0.006)), (0, 0.006)], 16)
        else:
            w, h = rng.uniform(0.035, 0.07), rng.uniform(0.035, 0.07)
            pts = [(cy + a, cz + b) for a, b in rounded_rect(w, h, min(w, h) * 0.25, 3)]
            poly(bm, pts, rng.uniform(0.002, 0.0035))
    # one tall disc pins the side bound to exactly W/2
    add_lathe(P("Magnets_A", mats[0]), (xf, 0.0, H * 0.6), (1, 0, 0), [(0, 0), (0.016, 0), (0.016, mt * 0.6), (0.012, mt), (0, mt)], 16)


def fridge(P, p, d, s):
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    f = p["fridge"]
    hs, hr = f["handle_standoff_m"], f["handle_r_m"]
    yf = -D / 2 + hs + hr
    dt, gap, zsplit, kick, lh = f["door_t_m"], f["door_gap_m"], H * f["freezer_split"], f["kick_h_m"], f["leveller_h_m"]
    mag = f.get("magnets_side")
    mt = 0.006 if mag else 0.0
    body = P("Body", f["finish"])
    if d >= 3:
        add_box(body, (W - mt, D / 2 - yf, H), (-mt / 2, (yf + D / 2) / 2, H / 2))
        add_box(P("Handles", "Handle_Grey"), (0.03, hs + hr, H * 0.3), (-W / 2 + 0.06, -D / 2 + (hs + hr) / 2, H * 0.6))
        if mag:
            add_box(P("Magnets_A", "Magnet_Grey_A"), (mt, D * 0.6, H * 0.5), (W / 2 - mt / 2, 0, H * 0.55))
        return (W, H, D), {}
    bw = W - mt
    bx = -mt / 2 if mag else 0.0  # body shifted away from the magnet side
    yb = yf + dt
    cs = 4 if d == 0 else 1
    # cabinet: wrap-around shell with rounded vertical front edges, top cap, back
    if d <= 1:
        for sx, face in ((-1, "-x"), (1, "+x")):
            rpanel(body, face, (bx + sx * (bw / 2 - 0.01), (yb + D / 2) / 2, lh + (H - lh) / 2), D / 2 - yb, H - lh, 0.02, 0.01, cs, 0.012, cs)
        rpanel(body, "+z", (bx, (yb + D / 2) / 2, H - 0.01), bw - 0.04, D / 2 - yb, 0.02, 0.006, cs, 0.008, cs)
        add_box(body, (bw - 0.04, D / 2 - yb - 0.02, H - lh - 0.02), (bx, (yb + D / 2 - 0.02) / 2, lh + (H - lh - 0.02) / 2))
        add_box(P("Back", "Coil_Grey"), (bw - 0.04, 0.02, H - lh - 0.04), (bx, D / 2 - 0.01, lh + (H - lh) / 2))
    else:
        add_box(body, (bw, D / 2 - yb, H - lh), (bx, (yb + D / 2) / 2, lh + (H - lh) / 2))
    doors = []
    for name, z0, z1, hpos in (("FreezerDoor", zsplit + gap / 2, H - 0.004, 0.18), ("FreshDoor", kick, zsplit - gap / 2, 0.82)):
        door = P(name, f["finish"])
        dz = (z0 + z1) / 2
        if d <= 1:
            rpanel(door, "-y", (bx, yf + dt / 2, dz), bw - 0.006, z1 - z0, dt, 0.016, cs, 0.02, cs)
            sl = P(f"Seal_{name}", "Gasket_Grey")
            loop_tube(sl, "-y", (bx, yb + 0.004, dz), bw - 0.03, z1 - z0 - 0.025, 0.015, 2 if d == 0 else 1, 0.006, 8 if d == 0 else 6)
            if d == 0:  # door liner with shelf ledges on the inner face (seen when open)
                lin = P(f"Liner_{name}", "Liner_Grey")
                add_box(lin, (bw - 0.08, 0.004, z1 - z0 - 0.07), (bx, yb + 0.002, dz))
                for zz in ([z0 + 0.12, z0 + (z1 - z0) * 0.45, z0 + (z1 - z0) * 0.75] if name == "FreshDoor" else [z0 + 0.1]):
                    rpanel(lin, "+z", (bx, yb + 0.05, zz), bw - 0.1, 0.09, 0.006, 0.002, 1)
                    add_box(lin, (bw - 0.1, 0.004, 0.05), (bx, yb + 0.093, zz + 0.022))
        else:
            add_box(door, (bw - 0.006, dt, z1 - z0), (bx, yf + dt / 2, dz))
        hlen = min(f["handle_len_m"], (z1 - z0) * 0.5)
        hz = z0 + (z1 - z0) * hpos
        hz = min(max(hz, z0 + hlen / 2 + 0.03), z1 - hlen / 2 - 0.03)
        add_handle_pull(P(f"Handle_{name}", "Handle_Grey"), (bx - bw / 2 + 0.045, yf, hz), hlen, hs, hr, 8, axis="z",  # grip = front bound (C11)
                        bend_steps=3 if d == 0 else 1)
        doors.append(dict(hinge_axis(name, bx + bw / 2 - 0.01, yf + dt / 2, z0, z1, "right"),
                          group=[name, f"Handle_{name}", f"Seal_{name}", f"Liner_{name}"]))
    # kick grille with louvres, levellers behind it
    gr = P("Grille", "Grille_Grey")
    if d <= 1:
        rframe(gr, "-y", (bx, yf + 0.008, lh + (kick - lh) / 2), bw - 0.02, kick - lh - 0.004, 0.016,
               (bw - 0.1, kick - lh - 0.035, 0, 0), 0.004, 2 if d == 0 else 1, 0.006, 0.003, 2 if d == 0 else 1)
        louvres(gr, bx - bw / 2 + 0.05, bx + bw / 2 - 0.05, yf + 0.01, lh + 0.02, kick - 0.02, 0.01 if d == 0 else 0.02)
        add_box(gr, (bw - 0.1, 0.004, kick - lh - 0.035), (bx, yf + 0.04, lh + (kick - lh) / 2))
    else:
        add_box(gr, (bw - 0.02, 0.016, kick - lh), (bx, yf + 0.008, lh + (kick - lh) / 2))
    lev = P("Levellers", "Grille_Grey")
    for sx in (-1, 1):
        for y in (yf + 0.05, D / 2 - 0.05):
            x = bx + sx * (bw / 2 - 0.05)
            if d <= 1:
                leveller(lev, x, y, lh, s, 0.014)
            else:
                add_box(lev, (0.025, 0.025, lh), (x, y, lh / 2))
    if d <= 1:  # hinge covers: top cap, middle bracket, bottom bracket on the hinge (right) side
        hg = P("Hinges", "Grille_Grey")
        hx = bx + bw / 2 - 0.03
        rpanel(hg, "+z", (hx, yf + 0.04, H - 0.002), 0.05, 0.08, 0.004, 0.0015, 1, 0.01, 2 if d == 0 else 1)
        rpanel(hg, "-y", (hx, yf - 0.002, zsplit), 0.04, gap + 0.012, 0.006, 0.002, 1, 0.003, 1)
        rpanel(hg, "-y", (hx, yf + 0.004, kick - 0.006), 0.045, 0.012, 0.01, 0.003, 1, 0.004, 1)
    if mag and d == 2:  # one magnet-layer slab keeps the side bound
        add_box(P("Magnets_A", "Magnet_Grey_A"), (mt, D * 0.6, H * 0.5), (W / 2 - mt / 2, 0, H * 0.55))
    if mag and d <= 1:
        _magnets(P, f, W, D, H, mt, int(p["seed"]), f["magnet_count"] if d == 0 else f["magnet_count"] // 3)
    return (W, H, D), dict(moving_parts=doors,
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
