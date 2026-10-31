"""Restroom (PROC-005 §10; IMP-003 drop 3 rewritten; PROC-005 fix wave rebuilt LOD0 as manufactured fixtures).
One asset per item; sizes from ROOM_FIXTURES / TI §6.6 (citations per key in params `_sources` / `_src`):
wall-hung lavatory (rim 34 in; open recessed basin, overflow ring, drain, faucet with aerator + lever, brackets,
P-trap and supplies with wall escutcheons and angle stops), mirror 1'-8" x 3'-6" in a mitred channel frame with corner
fixings, toilet (foot + bolt caps, rim lip, bowl cavity, seat + lid with hinges, tank with overhanging lid, flush
lever), flat-black tool chest and large storage cabinet (carcass panels, toe kick, overlay doors with reveals and
pressed panels, barrel hinges, pulls, cam lock, lipped shelves on pins), grab bars (3-screw flanges, filleted returns),
sheet-metal dispensers (wall plate, cover with rolled hem bead, rolled-over front, piano-hinge line, key lock, window /
slot / lever / push plate / lid by type), wall sconce L6 (back plate, caps, diffuser).
Wall items carry `mount_z_m` (origin height AFF); their origin is the bottom of the item. Back (+Y) = wall.
Bevels, hems, seams, hinges, screws and reveals are generic construction and never change a sourced outer size.
LOD0 full; LOD1 no micro detail; LOD2 plain; LOD3 blocks. Front-most details that set the bound stay to LOD2."""
import math

import bmesh

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_handle_pull, add_lathe, add_screw_head,
                     add_tube, collision_box, hinge_axis, loft, rounded_rect, wear)


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
    """Loft of rounded-rect rings in XY: specs = [(w, d, r, y_offset, z)], bottom to top."""
    loft(bm, [[(x, y + yo, z) for x, y in rounded_rect(w, dd, r, cs)] for w, dd, r, yo, z in specs])


def _ring_y(specs, cs, cx=0.0, cz=0.0):
    return [[(cx + a, y, cz + b) for a, b in rounded_rect(w, h, max(r, 0.0008), cs)] for w, h, r, y in specs]


def _loft_y(bm, specs, cs, cx=0.0, cz=0.0):
    """Rounded-rect rings in XZ, specs = [(w, h, r, y)] ordered back (+Y) to front (-Y); capped (outward winding)."""
    loft(bm, _ring_y(specs, cs, cx, cz))


def _bridge(bm, rings, closed=False, caps=False):
    """Quad bridge between equal rings (closed = ring loop, e.g. a bezel cross-section); normals recalculated."""
    vs = [[bm.verts.new(q) for q in r] for r in rings]
    n, faces = len(vs[0]), []
    for a, b in list(zip(vs, vs[1:])) + ([(vs[-1], vs[0])] if closed else []):
        faces += [bm.faces.new([a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]]) for i in range(n)]
    if caps:
        faces += [bm.faces.new(vs[0][::-1]), bm.faces.new(vs[-1])]
    bmesh.ops.recalc_face_normals(bm, faces=faces)


# --- sheet-metal dispenser construction -----------------------------------------------------------------------------

def _back_plate(bm, W, H, D, r, d, t=0.004):
    """Wall plate, full W x H at the wall (+Y), chamfered at LOD0/1."""
    y = D / 2
    sp = ([(W - 0.002, H - 0.002, r, y), (W, H, r, y - 0.001), (W, H, r, y - t + 0.001), (W - 0.002, H - 0.002, r, y - t)]
          if d <= 1 else [(W, H, r, y), (W, H, r, y - t)])
    _loft_y(bm, sp, (4, 2, 1)[d], 0.0, H / 2)


def _cover(bm, w, h, cz, yb, yf, r, rf, d):
    """Cover: rolled hem bead at its rear edge, straight sides, front edge rolled over with radius rf (front face yf)."""
    if d == 0:
        sp = [(w - 0.003, h - 0.003, r, yb), (w, h, r, yb - 0.0015), (w, h, r, yb - 0.0035), (w - 0.002, h - 0.002, r, yb - 0.005)]
    elif d == 1:
        sp = [(w, h, r, yb), (w - 0.002, h - 0.002, r, yb - 0.004)]
    else:
        sp = [(w - 0.002, h - 0.002, r, yb)]
    n = (4, 2, 1)[d]
    for i in range(n + 1):
        a = math.pi / 2 * i / n
        ins = rf * (1 - math.cos(a))
        sp.append((w - 0.002 - 2 * ins, h - 0.002 - 2 * ins, r - ins, yf + rf - rf * math.sin(a)))
    _loft_y(bm, sp, (4, 2, 1)[d], 0.0, cz)


def _edge_hinge(bm, w, h, cz, yf, rf, s, n=3):
    """Piano-hinge knuckles half-buried in the rolled bottom front edge of a cover."""
    zb = cz - h / 2 + 0.001
    y, z = yf + rf * (1 - 0.7071), zb + rf * (1 - 0.7071)
    seg = (w * 0.8 - 0.002 * (n - 1)) / n
    for i in range(n):
        x0 = -w * 0.4 + i * (seg + 0.002)
        add_cylinder_between(bm, (x0, y, z), (x0 + seg, y, z), 0.003, s)


def _lock(P, x, z, y_face, y_out, s):
    """Key lock: barrel from inside the cover out to y_out (the front bound), recessed core and keyway."""
    L = y_face + 0.003 - y_out
    add_lathe(P("Lock", "Chrome"), (x, y_face + 0.003, z), (0, -1, 0),
              [(0, 0), (0.011, 0), (0.011, L - 0.0008), (0.0102, L), (0.0065, L), (0.0065, L - 0.0006), (0, L - 0.0006)], s)
    add_box(P("Keyway", "Black_Trim"), (0.0024, 0.0004, 0.008), (x, y_out + 0.0005, z))


def _window(P, cx, cz, ww, wh, yf, d):
    """Viewing window: dark glass in a proud rounded bezel."""
    r = 0.004
    _bridge(P("Bezel", "Black_Trim"), _ring_y([(ww + 0.012, wh + 0.012, r + 0.006, yf + 0.001), (ww + 0.012, wh + 0.012, r + 0.006, yf - 0.0012),
                                               (ww, wh, r, yf - 0.0012), (ww, wh, r, yf + 0.001)], (4, 2, 1)[d], cx, cz), closed=True)
    add_box(P("Window", "Glass_Dark"), (ww + 0.002, 0.0008, wh + 0.002), (cx, yf - 0.0002, cz))


def _sconce(P, k, d, s, W, D, H):
    _back_plate(P("Body", k["body"]), W, H, D, 0.02, d, t=0.012)
    yc, R = -D / 2 + 0.048, 0.048  # caps touch the front bound
    cap = P("Caps", k["body"])
    add_lathe(cap, (0, yc, 0), (0, 0, 1), [(0, 0.015), (R - 0.008, 0.015), (R, 0.022), (R, 0.035), (0, 0.035)], s)
    add_lathe(cap, (0, yc, 0), (0, 0, 1), [(0, H - 0.035), (R, H - 0.035), (R, H - 0.022), (R - 0.008, H - 0.015), (0, H - 0.015)], s)
    for z in (0.025, H - 0.025):  # arms from the plate
        add_cylinder_between(cap, (0, D / 2 - 0.011, z), (0, yc, z), 0.008, s)
    add_lathe(P("Shade", "Glass_Frosted"), (0, yc, 0), (0, 0, 1),
              [(0, 0.035), (0.043, 0.035), (0.046, H / 2), (0.043, H - 0.035), (0, H - 0.035)] if d <= 1
              else [(0, 0.035), (0.044, 0.035), (0.044, H - 0.035), (0, H - 0.035)], s)
    if d <= 1:
        for sx in (-1, 1):
            add_screw_head(P("Screws", k["body"]), (sx * 0.058, D / 2 - 0.012, H / 2), (0, -1, 0), 0.004, s)
    return {"emissive_parts": ["Shade"]}


def dispenser(P, p, d, s, W, D, H):
    k = p["disp"]
    t, mat = k["type"], k["body"]
    out = {"mount_z_m": p["mount_z_m"]}
    if d >= 3:
        add_box(P("Body", mat), (W, D, H), (0, 0, H / 2))
        return out
    if t == "sconce":
        return dict(out, **_sconce(P, k, d, s, W, D, H))
    b = P("Body", mat)
    _back_plate(b, W, H, D, 0.012, d)
    yb, yf, yo = D / 2 - 0.006, -D / 2 + 0.0015, -D / 2  # cover rear, cover front face, front bound
    if t == "tp":  # twin-roll surface dispenser: hood over the rolls, roll bottoms exposed
        hz0, r, rf = 0.06, 0.012, 0.012
        hh = H - hz0 - 0.002
        _cover(b, W - 0.004, hh, hz0 + hh / 2, yb, yf, r, rf, d)
        _lock(P, 0, hz0 + hh / 2, yf, yo, s)
        if d <= 1:
            _edge_hinge(b, W - 0.004, hh, hz0 + hh / 2, yf, rf, s)
        for sx in (-1, 1):
            cx = sx * 0.072
            add_lathe(P("Roll", "Paper_White"), (cx - 0.05, -0.005, 0.055), (1, 0, 0),
                      [(0.02, 0), (0.055, 0), (0.055, 0.1), (0.02, 0.1), (0.02, 0.0005)], s)
            add_cylinder_between(P("Spindle", "Chrome"), (cx - 0.056, -0.005, 0.055), (cx + 0.056, -0.005, 0.055), 0.012, s)
        return out
    r, rf = {"towel": (0.02, 0.014), "soap": (0.018, 0.012), "napkin": (0.016, 0.012)}[t]
    w, h = W - 0.004, H - 0.004
    _cover(b, w, h, H / 2, yb, yf, r, rf, d)
    if d <= 1:
        _edge_hinge(b, w, h, H / 2, yf, rf, s)
    if t == "towel":  # DEC-062 manual dispenser: level window, key lock, dispensing slot, pull lever
        _window(P, 0, H * 0.66, 0.09, 0.05, yf, d)
        _lock(P, 0, H - 0.035, yf, yo, s)
        add_box(P("Slot", "Black_Trim"), (W * 0.6, 0.028, 0.0028), (0, yf + 0.03, 0.0032))
        lx, lz = W / 2 - 0.045, H * 0.4
        add_lathe(P("Lever", "Black_Trim"), (lx, yf + 0.002, lz), (0, -1, 0), [(0, 0), (0.014, 0), (0.014, 0.002), (0.011, 0.0035), (0, 0.0035)], s)  # hub face = front bound
        _bb(P("Lever", "Black_Trim"), (0.028, 0.004, 0.11), (lx, yo + 0.002, lz - 0.05), d, 0.008, 0.001)
    elif t == "soap":  # level window, key lock, push plate, nozzle under the cover
        _window(P, 0, H * 0.62, 0.016, 0.06, yf, d)
        _lock(P, 0, H - 0.03, yf, yo, s)
        _bb(P("PushPlate", "Black_Trim"), (W * 0.62, 0.006, 0.045), (0, yo + 0.003, 0.05), d, 0.006, 0.0015)
        add_lathe(P("Nozzle", "Black_Trim"), (0, yf + 0.02, 0.0015), (0, 0, 1), [(0, 0), (0.005, 0), (0.006, 0.004), (0, 0.004)], s)
    elif t == "napkin":  # hinged top flap, key lock low
        lz = H - 0.075
        _bb(P("Lid", mat), (W * 0.7, 0.003, 0.08), (0, yo + 0.0015, lz), d, 0.006, 0.001)
        add_cylinder_between(P("Lid", mat), (-W * 0.33, yo + 0.003, lz + 0.042), (W * 0.33, yo + 0.003, lz + 0.042), 0.003, s)
        _lock(P, 0, 0.05, yf, yo, s)
        out["moving_parts"] = [{"part": "Lid", "type": "hinge", "axis": "x"}]
    return out


# --- plumbing ---------------------------------------------------------------------------------------------------

def lavatory(P, p, d, s, W, D, H):
    k = p["lav"]
    bh, td, fh = k["body_h_m"], k["trap_drop_m"], k["faucet_h_m"]
    z0, zr = td, td + bh  # basin bottom, rim
    china = P("Basin", "Vitreous_White")
    cs = (8, 3, 1, 0)[d]
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
        zs = zr + fh * 0.55  # spout outlet
        add_tube(ch, [(0, yb, zr + fh * 0.7), (0, yb - 0.1, zr + fh * 0.7), (0, yb - 0.1, zs + 0.012)], 0.008, 8, bend_radius=0.02, bend_steps=2)
        add_lathe(ch, (0, yb - 0.1, zs), (0, 0, 1), [(0, 0.0015), (0.0095, 0.0015), (0.0095, 0.014), (0, 0.014)], s)  # aerator housing
        add_lathe(P("Overflow", "Black_Trim"), (0, yb - 0.1, zs), (0, 0, 1), [(0, 0), (0.0075, 0), (0.0075, 0.002), (0, 0.002)], 8)  # aerator screen
        add_lathe(ch, (0.018, yb, zr + fh - 0.012), (1, 0, 0), [(0, 0), (0.012, 0), (0.012, 0.012), (0.008, 0.016), (0, 0.016)], s)  # lever hub
        add_cylinder_between(ch, (0.032, yb, zr + fh - 0.012), (0.09, yb, zr + fh - 0.008), 0.005, 8)  # single lever
        _bb(ch, (0.022, 0.012, 0.006), (0.095, yb, zr + fh - 0.008), d, 0.005, 0.001)  # lever paddle
        dz = z0 + 0.025
        add_lathe(ch, (0, 0, 0), (0, 0, 1), [(0, dz), (0.022, dz), (0.022, dz + 0.003), (0, dz + 0.003)], s)  # drain
        yo = D / 2 - deck - 0.035  # overflow ring on the rear basin wall
        add_lathe(ch, (0, yo + 0.002, zr - 0.03), (0, -1, 0), [(0, 0), (0.014, 0), (0.014, 0.003), (0.011, 0.0045), (0, 0.0045)], s)
        add_box(P("Overflow", "Black_Trim"), (0.016, 0.001, 0.006), (0, yo - 0.0028, zr - 0.03))
        # exposed P-trap to the wall and two supply lines with angle stops and wall escutcheons
        add_tube(ch, [(0, 0, z0 + 0.03), (0, 0, td * 0.2), (0, 0.06, 0.016), (0, 0.12, td * 0.2), (0, D / 2 - 0.02, td * 0.5)], 0.016, 8,
                 bend_radius=0.03, bend_steps=2 if d == 0 else 1)
        add_lathe(ch, (0, 0.06, 0), (0, 0, 1), [(0, 0), (0.018, 0), (0.018, 0.02), (0, 0.02)], s)  # trap clean-out cap (floor of the bound)
        esc = [(0, 0), (0.035, 0), (0.035, 0.003), (0.021, 0.012), (0.019, 0.024), (0, 0.024)]  # boss hides the slanted trap-arm end
        add_lathe(ch, (0, D / 2, td * 0.5), (0, -1, 0), esc, s)
        for sx in (-1, 1):
            xs, zs2 = sx * 0.08, td * 0.7
            add_lathe(ch, (xs, D / 2, zs2), (0, -1, 0), [(0, 0), (0.024, 0), (0.024, 0.003), (0.012, 0.009), (0, 0.009)], s)
            add_cylinder_between(ch, (xs, D / 2 - 0.008, zs2), (xs, D / 2 - 0.045, zs2), 0.009, s)  # angle stop body
            _bb(ch, (0.012, 0.006, 0.03), (xs, D / 2 - 0.05, zs2), d, 0.004, 0.001)  # oval stop handle
            add_tube(ch, [(xs, D / 2 - 0.03, zs2), (xs, yb, z0 + 0.01)], 0.004, 8)
        for sx in (-1, 1):  # wall brackets
            add_box(P("Brackets", "Black_Trim"), (0.03, 0.18, 0.02), (sx * (W / 2 - 0.08), D / 2 - 0.09, z0 + 0.01))
    else:
        add_cylinder_between(ch, (0, 0, 0), (0, 0, z0 + 0.03), 0.016, 8)
    return {"mount_z_m": round(k["rim_z_m"] - bh - td, 5), "collision_boxes": [collision_box("Basin", (0, 0, z0 + bh / 2), (W, D, bh))]}


def toilet(P, p, d, s, W, D, H):
    k = p["toilet"]
    zr, bw, bl, td = k["rim_z_m"], k["bowl_w_m"], k["bowl_l_m"], k["tank_d_m"]
    china = P("China", "Vitreous_White")
    cs = (8, 3, 1, 0)[d]
    yb = -D / 2 + bl / 2  # bowl centre
    if d >= 3:
        add_box(china, (bw, bl, zr), (0, yb, zr / 2))
        add_box(china, (W, td, H - zr * 0.95), (0, D / 2 - td / 2, zr * 0.95 + (H - zr * 0.95) / 2))
        return {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}
    rb = bw * 0.45  # oval corner radius
    yp = yb + bl * 0.12  # pedestal centre
    if d <= 1:  # foot flange, pedestal + trapway flaring up to the rim (with a lip under it), open bowl cavity
        _rings(china, [(bw * 0.7, bl * 0.66, rb * 0.6, yp, 0), (bw * 0.68, bl * 0.64, rb * 0.6, yp, 0.012), (bw * 0.56, bl * 0.56, rb * 0.5, yp, 0.03),
                       (bw * 0.6, bl * 0.6, rb * 0.55, yb + bl * 0.1, zr * 0.45), (bw - 0.016, bl - 0.016, rb * 0.95, yb, zr - 0.05),
                       (bw, bl, rb, yb, zr - 0.036), (bw, bl, rb, yb, zr - 0.005), (bw - 0.03, bl - 0.03, rb * 0.9, yb, zr),
                       (bw - 0.07, bl - 0.08, rb * 0.75, yb - 0.01, zr - 0.04), (bw * 0.3, bl * 0.3, rb * 0.25, yb - 0.02, zr - 0.2)], cs)
        for sx in (-1, 1):  # closet-bolt caps on the foot
            add_lathe(P("BoltCaps", "Vitreous_White"), (sx * bw * 0.3, yp, 0.008), (0, 0, 1),
                      [(0, 0), (0.014, 0), (0.014, 0.008), (0.009, 0.019), (0, 0.022)], s)
    else:
        _rings(china, [(bw * 0.6, bl * 0.6, rb * 0.5, yb + bl * 0.1, 0), (bw, bl, rb, yb, zr), (bw * 0.6, bl * 0.6, rb * 0.5, yb, zr - 0.1)], 1)
    tz0 = zr * 0.95
    ti = 0.006 if d <= 1 else 0.0  # tank body inset under the overhanging lid
    _bb(china, (W - 2 * ti, td - ti, H - 0.03 - tz0), (0, D / 2 - td / 2 - ti / 2, tz0 + (H - 0.03 - tz0) / 2), d, 0.02, 0.006)  # tank
    _bb(P("TankLid", "Vitreous_White"), (W, td, 0.03), (0, D / 2 - td / 2, H - 0.015), d, 0.022, 0.009)  # tank lid
    seat = P("Seat", "Plastic_White")
    if d <= 1:  # seat ring + lid, hinges, flush lever
        _rings(seat, [(bw - 0.01, bl - 0.03, rb * 0.95, yb + 0.005, zr + 0.002), (bw - 0.01, bl - 0.03, rb * 0.95, yb + 0.005, zr + 0.022)], cs)
        _rings(seat, [(bw - 0.02, bl - 0.06, rb * 0.85, yb + 0.015, zr + 0.022), (bw - 0.03, bl - 0.07, rb * 0.8, yb + 0.015, zr + 0.04)], cs)  # lid
        for sx in (-1, 1):
            add_cylinder_between(P("Hinges", "Chrome"), (sx * 0.07, D / 2 - td - 0.02, zr + 0.02), (sx * 0.04, D / 2 - td - 0.02, zr + 0.02), 0.01, 8)
        yt, hx, hz = D / 2 - td + ti, -W / 2 + 0.06, H - 0.08  # tank front face, flush handle
        add_lathe(P("Hinges", "Chrome"), (hx, yt + 0.001, hz), (0, -1, 0), [(0, 0), (0.016, 0), (0.016, 0.004), (0.011, 0.009), (0, 0.009)], s)
        add_cylinder_between(P("Hinges", "Chrome"), (hx, yt - 0.008, hz), (hx, yt - 0.014, hz), 0.006, 8)
        _bb(P("Hinges", "Chrome"), (0.075, 0.009, 0.013), (hx + 0.035, yt - 0.016, hz), d, 0.006, 0.0015)
        if d == 0:  # supply: wall escutcheon, angle stop, riser to the tank
            sx0 = -W / 2 + 0.08
            add_lathe(P("Hinges", "Chrome"), (sx0, D / 2, 0.16), (0, -1, 0), [(0, 0), (0.024, 0), (0.024, 0.003), (0.012, 0.009), (0, 0.009)], s)
            add_cylinder_between(P("Hinges", "Chrome"), (sx0, D / 2 - 0.008, 0.16), (sx0, D / 2 - 0.045, 0.16), 0.009, s)
            add_tube(P("Hinges", "Chrome"), [(sx0, D / 2 - 0.04, 0.16), (sx0, D / 2 - 0.04, tz0 + 0.01)], 0.004, 8)
    else:
        _rings(seat, [(bw - 0.02, bl - 0.04, rb * 0.9, yb + 0.01, zr), (bw - 0.03, bl - 0.06, rb * 0.85, yb + 0.01, zr + 0.04)], 1)
    return {"moving_parts": [{"part": "Seat", "type": "hinge", "axis": "x"}],
            "collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


# --- casework ---------------------------------------------------------------------------------------------------

def door_cabinet(P, p, d, s, W, D, H):
    k = p["cab"]
    hs, hr = k["pull_standoff_m"], 0.006
    yf = -D / 2 + hs + hr  # door front face; pulls reach the front bound
    fin = k["finish"]
    if d >= 3:
        add_box(P("Body", fin), (W, D - hs - hr, H), (0, (yf + D / 2) / 2, H / 2))
        add_box(P("Pulls", "Brushed_Steel"), (0.1, hs + hr, 0.15), (0, -D / 2 + (hs + hr) / 2, H * 0.6))
        return {}
    t, kb, dt = 0.018, 0.08, 0.02  # panel thickness, toe-kick height, door thickness (construction)
    yc = yf + dt  # carcass front
    cd, ym = D / 2 - yc, (yc + D / 2) / 2
    body = P("Body", fin)
    for sx in (-1, 1):  # sides to the floor
        _bb(body, (t, cd, H), (sx * (W / 2 - t / 2), ym, H / 2), d, 0.002, 0.001)
    _bb(body, (W - 2 * t, cd, t), (0, ym, H - t / 2), d, 0.001, 0.0008)  # top
    _bb(body, (W - 2 * t, cd, t), (0, ym, kb + t / 2), d, 0.001, 0.0008)  # bottom
    add_box(body, (W - 2 * t, 0.006, H - kb - 2 * t), (0, D / 2 - 0.003, kb + t + (H - kb - 2 * t) / 2))  # back panel
    _bb(body, (W - 2 * t, t, kb), (0, yc + 0.05 + t / 2, kb / 2), d, 0.001, 0.0008)  # recessed toe kick
    zi0, zi1 = kb + t, H - t
    shelves = [round(zi0 + (zi1 - zi0) * (i + 1) / (k["shelves"] + 1), 5) for i in range(k["shelves"])]
    if d <= 1:
        sh = P("Shelves", fin)
        sw = W - 2 * t - 0.004
        for z in shelves:
            _bb(sh, (sw, cd - 0.012, 0.018), (0, ym + 0.002, z), d, 0.001, 0.0008)
            _bb(sh, (sw, 0.003, 0.03), (0, yc + 0.0075, z - 0.006), d, 0.001, 0.0005)  # front lip
            if d == 0:  # shelf pins
                for sx in (-1, 1):
                    for y in (yc + 0.05, D / 2 - 0.05):
                        add_cylinder_between(sh, (sx * (W / 2 - t + 0.002), y, z - 0.0115), (sx * (W / 2 - t - 0.01), y, z - 0.0115), 0.0025, 8)
    dh, dzc, dw = H - kb - 0.006, kb + 0.003 + (H - kb - 0.006) / 2, W / 2 - 0.0035
    moving = []
    for i, side in enumerate(("left", "right")):
        sgn = -1 if side == "left" else 1
        x = sgn * (0.0015 + dw / 2)
        name = f"Door_{i}"
        dm = P(name, fin)
        if d == 0:  # overlay door with chamfered edge and a pressed panel
            _loft_y(dm, [(dw, dh, 0.003, yc), (dw, dh, 0.003, yf + 0.0015), (dw - 0.003, dh - 0.003, 0.0015, yf), (dw - 0.012, dh - 0.012, 0.003, yf),
                         (dw - 0.12, dh - 0.12, 0.004, yf), (dw - 0.13, dh - 0.13, 0.004, yf), (dw - 0.136, dh - 0.136, 0.004, yf + 0.002),
                         (dw - 0.15, dh - 0.15, 0.004, yf + 0.002)], 3, x, dzc)  # flat support rings keep the Wear attribute on the edges
        elif d == 1:
            _loft_y(dm, [(dw, dh, 0.003, yc), (dw, dh, 0.003, yf + 0.0015), (dw - 0.003, dh - 0.003, 0.0015, yf)], 1, x, dzc)
        else:
            add_box(dm, (dw, dt, dh), (x, yf + dt / 2, dzc))
        px = x - sgn * (dw / 2 - 0.04)  # pull near the meeting stiles
        add_handle_pull(dm, (px, yf, H * 0.6), min(0.128, H * 0.3), hs, hr, 8, axis="z", bend_steps=2 if d <= 1 else 0)
        if d <= 1:
            hx = sgn * (W / 2 - 0.004)  # barrel hinges on the outer stile
            for z in [kb + 0.12, H - 0.12] + ([(kb + H) / 2] if H > 1.2 else []):
                for z0, z1 in ((z - 0.035, z - 0.001), (z + 0.001, z + 0.035)):
                    add_cylinder_between(P("Hinges", "Brushed_Steel"), (hx, yc - 0.001, z0), (hx, yc - 0.001, z1), 0.004, s)
            if i == 1:  # cam lock above the pull
                add_lathe(dm, (px, yf + 0.002, H * 0.6 + 0.11), (0, -1, 0), [(0, 0), (0.01, 0), (0.01, 0.004), (0.008, 0.0055), (0, 0.0055)], s)
                add_box(P("Keyway", "Black_Trim"), (0.0022, 0.0006, 0.008), (px, yf - 0.0035, H * 0.6 + 0.11))
        moving.append(hinge_axis(name, x + sgn * dw / 2, yf + 0.01, 0, H, side))
    return {"moving_parts": moving, "shelf_heights_m": shelves, "collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


# --- wall hardware ----------------------------------------------------------------------------------------------

def mirror(P, p, d, s, W, D, H):
    """Channel frame: four mitred bars (hairline joints), glass seated in the channel, corner fixings."""
    fw, yb = 0.02, D / 2
    yf = -D / 2 + 0.0012  # frame face; screw heads reach the front bound
    fr = P("Frame", "Accessory_Metal")
    if d >= 3:
        add_box(fr, (W, D, H), (0, 0, H / 2))
        return {"mount_z_m": p["mount_z_m"]}
    b = 0.001
    prof = ([(0, yb), (0, yf + b), (b, yf), (fw - b, yf), (fw, yf + b), (fw, yf + 0.003), (0.003, yf + 0.003), (0.003, yb)] if d <= 1
            else [(0, yb), (0, yf), (fw, yf), (fw, yf + 0.003), (0.003, yf + 0.003), (0.003, yb)])
    g = 0.0004 if d <= 1 else 0.0
    cor = [(-W / 2, 0), (W / 2, 0), (W / 2, H), (-W / 2, H)]
    for i in range(4):
        (ax, az), (bx, bz) = cor[i], cor[(i + 1) % 4]
        L = math.hypot(bx - ax, bz - az)
        tx, tz = (bx - ax) / L, (bz - az) / L
        nx, nz = -tz, tx  # inward normal for this corner order
        rings = [[(ex + nx * n + tx * sg * (n + g), y, ez + nz * n + tz * sg * (n + g)) for n, y in prof]
                 for ex, ez, sg in ((ax, az, 1), (bx, bz, -1))]
        _bar(fr, rings)
    add_box(P("Glass", "Mirror"), (W - 0.008, 0.0055, H - 0.008), (0, yf + 0.003 + 0.0029, H / 2))
    for x in (-W / 2 + fw / 2, W / 2 - fw / 2):
        for z in (fw / 2, H - fw / 2):
            add_screw_head(P("Screws", "Accessory_Metal"), (x, yf, z), (0, -1, 0), 0.003, s if d <= 1 else 8, height=yf + D / 2)
    return {"mount_z_m": p["mount_z_m"]}


def _bar(bm, rings):
    """Prism between two equal profile rings (start, end), capped; normals recalculated."""
    a = [bm.verts.new(q) for q in rings[0]]
    b = [bm.verts.new(q) for q in rings[1]]
    n = len(a)
    faces = [bm.faces.new([a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]]) for k in range(n)]
    faces += [bm.faces.new(a[::-1]), bm.faces.new(b)]
    bmesh.ops.recalc_face_normals(bm, faces=faces)


def grab_bar(P, p, d, s, W, D, H):
    """Grab bar: 3-screw flanges with a boss, bar with filleted returns; W/H = length for horizontal/vertical."""
    vertical = p.get("vertical", False)
    L = H if vertical else W
    fr, br = (W if vertical else H) / 2, p["bar_r_m"]
    mat = "Accessory_Metal"
    yw, yb = D / 2, -D / 2 + br
    if d >= 3:
        add_box(P("Bar", mat), (W, D, H), (0, 0, H / 2))
        return {"mount_z_m": p["mount_z_m"]}
    ends = [(0, fr), (0, L - fr)] if vertical else [(-L / 2 + fr, fr), (L / 2 - fr, fr)]
    ss = s if d <= 1 else 8
    fl = P("Flanges", mat)
    for x, z in ends:
        add_lathe(fl, (x, yw, z), (0, -1, 0),
                  [(0, 0), (fr, 0), (fr, 0.0025), (fr - 0.002, 0.004), (br * 1.3, 0.004), (br * 1.05, 0.014), (0, 0.014)] if d <= 1
                  else [(0, 0), (fr, 0), (fr, 0.004), (br * 1.2, 0.012), (0, 0.012)], ss)
        if d == 0:
            for a in (90, 210, 330):
                ra = math.radians(a)
                add_screw_head(P("Screws", mat), (x + 0.029 * math.cos(ra), yw - 0.004, z + 0.029 * math.sin(ra)), (0, -1, 0), 0.0032, 8)
    (x0, z0), (x1, z1) = ends
    add_tube(P("Bar", mat), [(x0, yw - 0.008, z0), (x0, yb, z0), (x1, yb, z1), (x1, yw - 0.008, z1)], br, ss,
             bend_radius=0.03 if d <= 1 else 0.0, bend_steps=(4, 2)[d] if d <= 1 else 0)
    return {"mount_z_m": p["mount_z_m"]}


KINDS = {"lavatory": lavatory, "mirror": mirror, "toilet": toilet, "door_cabinet": door_cabinet, "grab_bar": grab_bar, "dispenser": dispenser}


def build(p, lod):
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"], W, D, H)
    extra = dict(extra, fixture_family="restroom", rf=p["rf"], seed=int(p["seed"]))
    extra.update(wear(p))
    return P.finish(), (W, H, D), extra
