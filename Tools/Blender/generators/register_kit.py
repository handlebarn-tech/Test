"""Register workstation kit RK-01..RK-09 (PROC-006b; spec Docs/Assets/Specs/REGISTER_KIT.md, DEC-104).
One params file, one asset per item (`items`), each built by the builder named in its `kind`. Blender metres, Z up,
origin = bottom centre, **-Y faces the operator** (keyboard space bar, printer fronts, the mouse's palm end).
Detail by LOD: `d` 0 full (keycaps, seams, vents, coiled cord, wire mesh), 1 simplified, 2 blocks/cards, 3 one box.
Sizes come from the params (measured per DEC-110 where a still allows it, otherwise labelled GAP values); each LOD is
checked against the item's `size_m` envelope. No cash-handling equipment (DEC-051). Materials are preview colours;
the 2K PBR sets wait on the PROC-005 texture work (Q0.2/Q0.3)."""
import math
import os
import random

import bmesh
from mathutils import Matrix, Vector

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_lathe, add_sweep, add_tube,
                     collision_box, loft, rounded_rect, to_unity, wear)

U = 0.01905  # one keyboard key unit (0.75 in)


def variants(p):
    for item in p["items"]:
        q = {k: v for k, v in p.items() if k != "items"}
        q.update(item)
        yield p["asset_prefix"] + item["id"], q


# --- local helpers (the shared proclib stays untouched; PROC-005 owns it) -------------------------------------------

def ev(n):
    """Even segment count >= 6 (proclib C11)."""
    n = max(6, int(n))
    return n + n % 2


def rprofile(x0, x1, y0, y1, radii, steps):
    """CCW 2D rectangle with per-corner radii (bottom-left, bottom-right, top-right, top-left)."""
    corners = (((x0, y0), (1, 1), 180), ((x1, y0), (-1, 1), 270), ((x1, y1), (-1, -1), 0), ((x0, y1), (1, -1), 90))
    pts = []
    for ((cx, cy), (sx, sy), a0), r in zip(corners, radii):
        if r <= 0 or steps < 1:
            pts.append((cx, cy))
            continue
        for i in range(steps + 1):
            a = math.radians(a0 + 90 * i / steps)
            pts.append((cx + sx * r + r * math.cos(a), cy + sy * r + r * math.sin(a)))
    return pts


def prism_x(bm, x0, x1, profile_yz):
    """Extrude a (y, z) profile along X (sweep frame along +X: u = +Y, v = +Z)."""
    add_sweep(bm, [(x0, 0.0, 0.0), (x1, 0.0, 0.0)], profile_yz)


def box_rot(bm, size, center, rx=0.0, ry=0.0, rz=0.0):
    verts = add_box(bm, size)
    m = Matrix.Rotation(rz, 4, "Z") @ Matrix.Rotation(ry, 4, "Y") @ Matrix.Rotation(rx, 4, "X")
    bmesh.ops.transform(bm, matrix=Matrix.Translation(center) @ m, verts=verts)


def lathe_loop(bm, profile_rz, segs, center=(0.0, 0.0, 0.0), disp=None):
    """Closed (r, z) loop revolved around the Z axis through center: annuli, rims, shells with holes.
    disp(angle, r, z) -> radial offset adds wrinkles/waves."""
    cx, cy, cz = center
    rings = []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        ring = []
        for r, z in profile_rz:
            rr = r + (disp(a, r, z) if disp else 0.0)
            ring.append(bm.verts.new((cx + rr * math.cos(a), cy + rr * math.sin(a), cz + z)))
        rings.append(ring)
    m = len(profile_rz)
    for i in range(segs):
        a, b = rings[i], rings[(i + 1) % segs]
        for k in range(m):
            bm.faces.new([a[k], a[(k + 1) % m], b[(k + 1) % m], b[k]])


def tooth_row(bm, x0, x1, y, z, pitch, h, depth):
    """Serrated tear-bar teeth along X: small triangular prisms pointing +Z."""
    n = max(2, int((x1 - x0) / pitch))
    w = (x1 - x0) / n
    for i in range(n):
        xa = x0 + i * w
        vs0 = [bm.verts.new((xa, y - depth / 2, z)), bm.verts.new((xa + w, y - depth / 2, z)),
               bm.verts.new((xa + w / 2, y - depth / 2, z + h))]
        vs1 = [bm.verts.new((v.co.x, y + depth / 2, v.co.z)) for v in vs0]
        bm.faces.new(vs0[::-1])
        bm.faces.new(vs1)
        for k in range(3):
            bm.faces.new([vs0[k], vs0[(k + 1) % 3], vs1[(k + 1) % 3], vs1[k]])


def cable(bm, pts, r, lod, relief=None):
    """Round cable along a filleted path; relief = (base, axis) adds a moulded strain relief at the device."""
    s = ev(lod["s"] // 4)
    add_tube(bm, pts, r, s, bend_radius=0.008, bend_steps=4 if lod["d"] == 0 else 2)
    if relief and lod["d"] <= 1:
        base, axis = relief
        prof = [(0, 0.0), (r * 2.4, 0.0), (r * 2.4, 0.004), (r * 1.5, 0.014), (r * 1.15, 0.018), (0, 0.018)]
        if lod["d"] == 0:  # flex ribs
            prof = prof[:3] + [(r * 2.1, 0.007), (r * 1.9, 0.0085), (r * 1.8, 0.01), (r * 1.6, 0.0115)] + prof[3:]
        add_lathe(bm, base, axis, prof, s)


def proxy(bm, lo, hi):
    """Far-LOD stand-in box from corners, so cables/strips keep the LOD0 extents (no pop, same origin)."""
    add_box(bm, [b - a for a, b in zip(lo, hi)], [(a + b) / 2 for a, b in zip(lo, hi)])


def feet(bm, pts, r, h, lod):
    for x, y in pts:
        add_lathe(bm, (x, y, 0), (0, 0, 1), [(0, 0), (r * 0.85, 0), (r, h * 0.5), (r, h), (0, h)], ev(lod["s"] // 4))


def noise2(rng, n=3):
    """Deterministic smooth 2D noise: a few sines with seeded frequencies/phases, range about -1..1."""
    terms = [(rng.uniform(0.6, 2.2) * (k + 1), rng.uniform(0.6, 2.2) * (k + 1), rng.uniform(0, 6.283), 0.6 ** k)
             for k in range(n)]
    norm = sum(t[3] for t in terms)
    return lambda u, v: sum(a * math.sin(6.283 * (fu * u + fv * v) + ph) for fu, fv, ph, a in terms) / norm


# --- RK-04 keyboard ----------------------------------------------------------------------------------------------

def key_layout():
    """Full-size 104-key ANSI layout: (x_u, row_u from the front, w_u, h_u). Nav and numpad blocks included."""
    keys = []

    def row(y, items, x=0.0):
        for it in items:
            if isinstance(it, str):
                x += float(it[1:])
                continue
            keys.append((x, y, it, 1.0))
            x += it

    row(0, [1.25] * 3 + [6.25] + [1.25] * 4)
    row(1, [2.25] + [1] * 10 + [2.75])
    row(2, [1.75] + [1] * 11 + [2.25])
    row(3, [1.5] + [1] * 12 + [1.5])
    row(4, [1] * 13 + [2])
    row(5.5, [1, "g1", 1, 1, 1, 1, "g0.5", 1, 1, 1, 1, "g0.5", 1, 1, 1, 1])
    row(0, [1, 1, 1], 15.25)            # arrows
    row(1, [1], 16.25)
    row(3, [1, 1, 1], 15.25)            # del end pgdn
    row(4, [1, 1, 1], 15.25)            # ins home pgup
    row(5.5, [1, 1, 1], 15.25)          # prtsc scrlk pause
    row(0, [2, 1], 18.5)                # numpad 0 .
    row(1, [1, 1, 1], 18.5)
    row(2, [1, 1, 1], 18.5)
    row(3, [1, 1, 1], 18.5)
    row(4, [1, 1, 1, 1], 18.5)
    keys += [(21.5, 0, 1, 2.0), (21.5, 2, 1, 2.0)]  # numpad enter, plus (two rows tall)
    return keys


def build_keyboard(parts, p, lod):
    d, cs = lod["d"], lod["cs"]
    W, Dk, hc, kh = p["kb_w_m"], p["kb_d_m"], p["case_h_m"], p["key_h_m"]
    case = parts("Case", "RK_Black_ABS")
    stub = p["cable_stub_m"]
    if d >= 3:
        add_box(case, (W, Dk, hc + kh), (0, 0, (hc + kh) / 2))
        proxy(case, (-0.002, Dk / 2, 0.0007), (0.002, Dk / 2 + stub, 0.0128))
        return {}
    add_beveled_box(case, (W, Dk, hc), (0, 0, hc / 2), corner=0.006, bevel=0.002 if d < 2 else 0.0, seg=max(1, cs))
    x0, yf = -22.5 * U / 2, -Dk / 2 + 0.012
    keys = parts("Keycaps", "RK_Black_Matte")
    slope = p["row_rise_m"]
    if d == 2:  # one block per contiguous run of keys in a row
        rows = {}
        for kx, ky, kw, khu in key_layout():
            rows.setdefault(ky, []).append((kx, kw))
        for ky, runs in rows.items():
            runs.sort()
            start, end = runs[0][0], runs[0][0] + runs[0][1]
            for kx, kw in runs[1:] + [(1e9, 0)]:
                if kx - end > 0.3:
                    zb = hc - 0.003 + slope * ky
                    add_box(keys, ((end - start) * U - 0.002, U - 0.002, kh),
                            (x0 + (start + end) / 2 * U, yf + (ky + 0.5) * U, zb + kh / 2))
                    start = kx
                end = max(end, kx + kw)
        cable(case, [(0, Dk / 2 - 0.004, 0.011), (0, Dk / 2 + 0.02, 0.011), (0, Dk / 2 + 0.035, 0.0025),
                     (0, Dk / 2 + stub, 0.0025)], 0.0018, lod)
        return {}
    for kx, ky, kw, khu in key_layout():
        cx, cy = x0 + (kx + kw / 2) * U, yf + (ky + khu / 2) * U
        w, dd, zb = kw * U, khu * U, hc - 0.003 + slope * ky
        spec = [(0.0012, 0.0012, 0.0), (0.0042, 0.002, kh)] if d == 1 else \
            [(0.0012, 0.0012, 0.0), (0.0022, 0.0015, kh * 0.65), (0.0042, 0.002, kh), (0.0062, 0.0018, kh - 0.0006)]
        loft(keys, [[(cx + x, cy + y, zb + z) for x, y in rounded_rect(w - ins, dd - ins, r, max(1, cs))]
                    for ins, r, z in spec])
    if d == 0:  # three status LED lenses above the numpad
        led = parts("LEDs", "RK_LED_Green")
        for i in range(3):
            add_beveled_box(led, (0.004, 0.0025, 0.0012), (x0 + (19.0 + i * 1.1) * U, yf + 6.0 * U, hc + 0.0004),
                            corner=0.001, bevel=0.0003, seg=1)
    cab = parts("Cable", "RK_Black_ABS")
    cable(cab, [(0, Dk / 2 - 0.004, 0.011), (0, Dk / 2 + 0.02, 0.011), (0, Dk / 2 + 0.035, 0.0025),
                (0, Dk / 2 + stub, 0.0025)], 0.0018, lod, relief=((0, Dk / 2 - 0.004, 0.011), (0, 1, 0)))
    return {}


# --- RK-05 mouse -------------------------------------------------------------------------------------------------

def build_mouse(parts, p, lod):
    d, s = lod["d"], lod["s"]
    W, L, H = p["ms_w_m"], p["ms_l_m"], p["ms_h_m"]
    body = parts("Body", "RK_Black_Matte")
    side_h = H * 0.22
    if d >= 3:
        add_beveled_box(body, (W, L, H), (0, 0, H / 2), corner=0.02, bevel=0.0, seg=1)
        proxy(body, (-0.0016, L / 2, 0.0006), (0.0016, L / 2 + p["cable_stub_m"], side_h * 0.8 + 0.0016))
        return {}
    n = s * 2 if d == 0 else s

    def outline(a):
        c, sn = math.cos(a), math.sin(a)
        return (W / 2 * math.copysign(abs(c) ** 0.8, c) * (1 - 0.07 * sn), L / 2 * math.copysign(abs(sn) ** 0.8, sn))

    def hump(y):
        t = (y + L / 2) / L
        return 0.62 + 0.38 * math.exp(-((t - 0.38) / 0.33) ** 2)

    base = [outline(2 * math.pi * i / n) for i in range(n)]
    rings = [[(x, y, 0.0) for x, y in base], [(x, y, side_h) for x, y in base]]
    kmax = {0: 14, 1: 8, 2: 4}[d]
    for k in range(1, kmax + 1):
        phi = math.radians(88) * k / kmax
        sc = math.cos(phi)
        rings.append([(x * sc, y * sc, side_h + (H * hump(y * sc) - side_h) * math.sin(phi)) for x, y in base])
    loft(body, rings)

    table = [(math.atan2(y, x), math.hypot(x, y)) for x, y in (outline(2 * math.pi * i / 720) for i in range(720))]

    def surf(x, y):
        th = math.atan2(y, x)
        _, R = min(table, key=lambda t: abs(math.remainder(t[0] - th, 2 * math.pi)))
        sc = min(1.0, math.hypot(x, y) / R)
        return side_h + (H * hump(y) - side_h) * math.sqrt(max(0.0, 1 - sc * sc))

    seam = parts("Seams", "RK_Seam_Dark")
    y_split = L / 2 - 0.045
    if d <= 1:  # button split: centre line and the transverse palm line
        cen = [(0.0, y, surf(0.0, y) + 0.0003) for y in (y_split + (L / 2 - 0.002 - y_split) * i / 11 for i in range(12))]
        add_tube(seam, cen, 0.00035, 6)
        xr = W / 2 * 0.92
        tr = [(x, y_split, surf(x, y_split) + 0.0003) for x in (-xr + 2 * xr * i / 15 for i in range(16))]
        add_tube(seam, tr, 0.00035, 6)
    yw = L / 2 - 0.03
    zw = surf(0.0, yw) - 0.003
    add_box(seam, (0.0095, 0.024, 0.006), (0, yw, zw + 0.0005))  # wheel slot
    wheel = parts("Wheel", "RK_Rubber")
    r, ww = 0.0105, 0.0065
    add_lathe(wheel, (-ww / 2, yw, zw), (1, 0, 0), [(0, 0), (r * 0.9, 0), (r, 0.001), (r, ww - 0.001), (r * 0.9, ww),
                                                     (0, ww)], ev(s))
    if d == 0:  # tread ribs
        for i in range(24):
            a = 2 * math.pi * i / 24
            box_rot(wheel, (ww * 0.85, 0.0012, 0.0008), (0, yw + r * math.cos(a), zw + r * math.sin(a)), rx=a)
    if d <= 1:  # thumb buttons on the left side
        btn = parts("SideButtons", "RK_Black_ABS")
        for y in (-0.004, 0.017):
            add_beveled_box(btn, (0.004, 0.016, 0.006), (-W / 2 * 0.97, y, side_h + 0.007), corner=0.0015,
                            bevel=0.0005, seg=1)
    cab = parts("Cable", "RK_Black_ABS")
    cable(cab, [(0, L / 2 - 0.004, side_h * 0.8), (0, L / 2 + 0.015, side_h * 0.8), (0, L / 2 + 0.03, 0.0022),
                (0, L / 2 + p["cable_stub_m"], 0.0022)], 0.0016, lod,
          relief=((0, L / 2 - 0.004, side_h * 0.8), (0, 1, 0)))
    return {}


# --- RK-01 receipt printer (top exit, DEC-104 R6) -----------------------------------------------------------------

def back_cables(parts, D, xs, z, lod, stub):
    cab = parts("Cables", "RK_Black_ABS")
    for x in xs:
        cable(cab, [(x, D / 2 - 0.004, z), (x, D / 2 + 0.012, z), (x, D / 2 + 0.024, 0.0032), (x, D / 2 + stub, 0.0032)],
              0.0022, lod, relief=((x, D / 2 - 0.004, z), (0, 1, 0)))


def vents(bm, W, ys, zs, size):
    for sx in (-1, 1):
        for y in ys:
            for z in zs:
                add_box(bm, (0.0008, size[0], size[1]), (sx * (W / 2 + 0.0002), y, z))


def build_receipt_printer(parts, p, lod):
    d, cs = lod["d"], lod["cs"]
    W, D, H, fh = p["rp_w_m"], p["rp_d_m"], p["rp_h_m"], p["foot_h_m"]
    body = parts("Body", "RK_Black_ABS")
    stub = p["cable_stub_m"]
    if d >= 2:  # cables as one far box
        proxy(body, (-0.0322, D / 2 - 0.004, 0.001), (0.0322, D / 2 + stub, 0.0242))
    if d >= 3:
        add_box(body, (W, D, H), (0, 0, H / 2))
        return {}
    hb, band_d, band_h = H * 0.5, p["rp_front_band_m"], H * 0.8
    st = max(1, cs * 2) if d < 2 else 1
    add_beveled_box(body, (W, D, hb - fh), (0, 0, fh + (hb - fh) / 2), corner=0.012, bevel=0.003 if d < 2 else 0, seg=st)
    add_beveled_box(body, (W, band_d, band_h - hb + 0.004), (0, -D / 2 + band_d / 2, hb - 0.004 + (band_h - hb + 0.004) / 2),
                    corner=0.012, bevel=0.003 if d < 2 else 0, seg=st)
    lid = parts("Lid", "RK_Black_Gloss")
    y0 = -D / 2 + band_d + 0.004
    prism_x(lid, -W / 2 + 0.0015, W / 2 - 0.0015, rprofile(y0, D / 2 - 0.002, hb, H, (0, 0, 0.014, 0.03), st * 2))
    if d <= 1:
        slot = parts("Slot", "RK_Seam_Dark")
        add_box(slot, (W - 0.02, 0.0045, band_h - hb), (0, y0 - 0.002, hb + (band_h - hb) / 2 - 0.001))
        bar = parts("TearBar", "RK_Metal")
        add_box(bar, (W - 0.03, 0.0012, 0.004), (0, y0 - 0.0045, band_h - 0.001))
        if d == 0:
            tooth_row(bar, -(W - 0.03) / 2, (W - 0.03) / 2, y0 - 0.0045, band_h + 0.001, 0.002, 0.0018, 0.0012)
        paper = parts("PaperTongue", "RK_Paper_White")
        pw = p["rp_paper_w_m"] * 0.9
        path = [(0, y0 - 0.0015, band_h - 0.012), (0, y0 - 0.0015, band_h + 0.008), (0, y0 - 0.006, band_h + 0.018),
                (0, y0 - 0.016, band_h + 0.022)]
        add_sweep(paper, path, [(-0.0003, -pw / 2), (0.0003, -pw / 2), (0.0003, pw / 2), (-0.0003, pw / 2)])
        ui = parts("Buttons", "RK_Rubber")
        add_cylinder_between(ui, (W / 2 - 0.025, -D / 2 + 0.001, hb + 0.012), (W / 2 - 0.025, -D / 2 - 0.0025, hb + 0.012),
                             0.005, ev(lod["s"] // 2))  # power
        add_beveled_box(ui, (0.018, 0.003, 0.008), (-W / 2 + 0.03, -D / 2 - 0.001, hb + 0.012), corner=0.003,
                        bevel=0.0008, seg=2)  # feed
        add_beveled_box(ui, (0.003, 0.02, 0.012), (W / 2 + 0.0008, -D / 2 + band_d / 2, band_h - 0.012), corner=0.001,
                        bevel=0.0004, seg=1)  # cover-open lever
        led = parts("LED", "RK_LED_Green")
        add_cylinder_between(led, (0, -D / 2 + 0.0005, hb + 0.012), (0, -D / 2 - 0.0015, hb + 0.012), 0.0018, 8)
        dark = parts("Ports", "RK_Seam_Dark")
        add_box(dark, (W * 0.6, 0.002, 0.03), (0, D / 2 + 0.0002, 0.025))
        vents(dark, W, [D / 2 - 0.05 + 0.012 * i for i in range(3)], [fh + 0.012 + 0.008 * i for i in range(4)],
              (0.008, 0.003))
        back_cables(parts, D, (-0.03, 0.03), 0.022, lod, p["cable_stub_m"])
        feet(parts("Feet", "RK_Rubber"), [(sx * (W / 2 - 0.018), sy * (D / 2 - 0.02)) for sx in (-1, 1) for sy in (-1, 1)],
             0.007, fh, lod)
    return {"optional_parts": ["PaperTongue"]}


# --- RK-02 label printer (every register, DEC-104 R2) ---------------------------------------------------------------

def build_label_printer(parts, p, lod):
    d, cs, s = lod["d"], lod["cs"], lod["s"]
    W, D, H, fh = p["lp_w_m"], p["lp_d_m"], p["lp_h_m"], p["foot_h_m"]
    body = parts("Body", "RK_White_ABS")
    hb = p["lp_base_h_m"]
    zs, lw = hb - 0.012, p["lp_roll_w_m"] - 0.002
    if d >= 2:  # label strip and cables as far boxes
        proxy(body, (-lw / 2, -D / 2 - 0.034, zs - 0.0125), (lw / 2, -D / 2, zs + 0.001))
        proxy(body, (-0.0422, D / 2 - 0.004, 0.001), (0.0422, D / 2 + p["cable_stub_m"], 0.0262))
    if d >= 3:
        add_box(body, (W, D, H), (0, 0, H / 2))
        return {}
    st = max(1, cs * 2) if d < 2 else 1
    add_beveled_box(body, (W, D, hb - fh), (0, 0, fh + (hb - fh) / 2), corner=0.016, bevel=0.003 if d < 2 else 0, seg=st)
    lid = parts("Lid", "RK_Lid_Tint", rgba=p["lp_lid_rgba"])
    prism_x(lid, -W / 2 + 0.002, W / 2 - 0.002, rprofile(-D / 2 + 0.02, D / 2 - 0.004, hb, H, (0, 0, 0.035, 0.07), st * 2))
    roll_z, roll_r, roll_w = hb + p["lp_roll_r_m"] + 0.002, p["lp_roll_r_m"], p["lp_roll_w_m"]
    roll = parts("LabelRoll", "RK_Paper_White")
    if d == 2:
        add_cylinder_between(roll, (-roll_w / 2, 0.02, roll_z), (roll_w / 2, 0.02, roll_z), roll_r, 12)
        return {}
    segs = ev(s * 2 if d == 0 else s)
    add_lathe(roll, (-roll_w / 2, 0.02, roll_z), (1, 0, 0),
              [(0.0215, 0), (roll_r - 0.002, 0), (roll_r, 0.002), (roll_r, roll_w - 0.002), (roll_r - 0.002, roll_w),
               (0.0215, roll_w), (0.0215, 0)], segs)
    core = parts("Core", "RK_Cardboard")
    add_lathe(core, (-roll_w / 2 - 0.001, 0.02, roll_z), (1, 0, 0),
              [(0.019, 0), (0.0217, 0), (0.0217, roll_w + 0.002), (0.019, roll_w + 0.002), (0.019, 0)], segs)
    mech = parts("Mechanism", "RK_Grey_ABS")
    add_cylinder_between(mech, (-roll_w / 2 - 0.012, 0.02, roll_z), (roll_w / 2 + 0.012, 0.02, roll_z), 0.0115, ev(s // 2))
    for sx in (-1, 1):
        add_beveled_box(mech, (0.003, 0.05, roll_z - hb + 0.02), (sx * (roll_w / 2 + 0.006), 0.02, hb + (roll_z - hb + 0.02) / 2),
                        corner=0.004, bevel=0.0005, seg=1)
    bezel = parts("Bezel", "RK_Grey_ABS")
    add_beveled_box(bezel, (W - 0.02, 0.003, hb - fh - 0.02), (0, -D / 2 - 0.0005, fh + (hb - fh) / 2 - 0.004),
                    corner=0.004, bevel=0.001, seg=1)
    slot = parts("Slot", "RK_Seam_Dark")
    add_box(slot, (roll_w + 0.012, 0.004, 0.004), (0, -D / 2 - 0.0005, zs))
    bar = parts("TearBar", "RK_Metal")
    add_box(bar, (roll_w + 0.016, 0.006, 0.0012), (0, -D / 2 - 0.003, zs - 0.0028))
    if d == 0:
        tooth_row(bar, -(roll_w + 0.016) / 2, (roll_w + 0.016) / 2, -D / 2 - 0.0055, zs - 0.0025, 0.002, 0.0016, 0.0012)
    strip = parts("LabelStrip", "RK_Paper_White")
    add_sweep(strip, [(0, -D / 2 + 0.004, zs), (0, -D / 2 - 0.022, zs), (0, -D / 2 - 0.034, zs - 0.012)],
              [(-lw / 2, -0.0003), (lw / 2, -0.0003), (lw / 2, 0.0003), (-lw / 2, 0.0003)])
    add_box(strip, (p["lp_label_w_m"], 0.016, 0.0005), (0, -D / 2 - 0.013, zs + 0.0006))  # die-cut label on the liner
    ui = parts("Buttons", "RK_Rubber")
    add_beveled_box(ui, (0.02, 0.004, 0.01), (W / 2 - 0.035, -D / 2 - 0.002, fh + 0.022), corner=0.004, bevel=0.001, seg=2)
    for sx in (-1, 1):  # lid release buttons
        add_beveled_box(ui, (0.004, 0.018, 0.009), (sx * (W / 2 + 0.0008), -D / 2 + 0.05, hb + 0.008), corner=0.002,
                        bevel=0.0005, seg=1)
    led = parts("LED", "RK_LED_Green")
    add_cylinder_between(led, (W / 2 - 0.06, -D / 2 - 0.001, fh + 0.022), (W / 2 - 0.06, -D / 2 - 0.0025, fh + 0.022),
                         0.002, 8)
    dark = parts("Ports", "RK_Seam_Dark")
    add_box(dark, (W * 0.5, 0.002, 0.03), (0, D / 2 + 0.0002, 0.028))
    back_cables(parts, D, (-0.04, 0.04), 0.024, lod, p["cable_stub_m"])
    if d == 0:
        feet(parts("Feet", "RK_Rubber"), [(sx * (W / 2 - 0.02), sy * (D / 2 - 0.025)) for sx in (-1, 1) for sy in (-1, 1)],
             0.008, fh, lod)
    else:
        add_box(parts("Feet", "RK_Rubber"), (W - 0.04, D - 0.05, fh), (0, 0, fh / 2))
    return {"optional_parts": ["LabelStrip"]}


# --- RK-03 handheld scanner in its stand -------------------------------------------------------------------------

def build_scanner(parts, p, lod):
    d, cs, s = lod["d"], lod["cs"], lod["s"]
    stand = parts("Stand", "RK_Black_ABS")
    if d >= 3:
        add_cylinder_between(stand, (0, 0.02, 0), (0, 0.02, 0.014), 0.058, 8)
        add_box(parts("Handheld_Body", "RK_Black_ABS"), (0.045, 0.14, 0.162), (0, -0.03, 0.0958))
        end_y = 0.08 + p["sc_coil_pitch_m"] * p["sc_coil_turns"] + 0.012
        proxy(stand, (-0.002, 0.04, 0.001), (0.002, end_y, 0.006))
        return {"liftable_parts": ["Handheld_Body"]}
    R, ys = p["sc_base_r_m"], 0.02
    add_lathe(stand, (0, ys, 0.002), (0, 0, 1), [(0, 0), (R, 0), (R, 0.006), (R * 0.95, 0.011), (0.022, 0.013), (0, 0.013)],
              ev(s * 2 if d == 0 else s))
    B, T = Vector((0, 0.035, 0.035)), Vector((0, 0.0, 0.13))
    A = (T - B).normalized()
    cup0 = B - A * 0.006
    add_lathe(stand, cup0, A, [(0, 0), (0.023, 0), (0.027, 0.036), (0.0245, 0.036), (0.0205, 0.003), (0, 0.003)], ev(s))
    add_tube(stand, [(0, ys, 0.012), (0, cup0.y, cup0.z - 0.002)], 0.009, ev(s // 2))
    if d <= 1:
        add_lathe(parts("Stand_Pad", "RK_Rubber"), (0, ys, 0), (0, 0, 1), [(0, 0), (R * 0.93, 0), (R * 0.93, 0.002), (0, 0.002)],
                  ev(s))
    body = parts("Handheld_Body", "RK_Black_ABS")
    hw, hd = 0.028, 0.036
    bow = Vector((0, 1, 0)) * 0.008  # ergonomic back-bow of the handle
    hpath = [B + (T - B) * (i / 8) + bow * math.sin(math.pi * i / 8) for i in range(9)] if d == 0 else [B, B + A * 0.05, T]
    add_sweep(body, hpath, [(x, y) for x, y in rounded_rect(hd, hw, 0.009, max(1, cs))])
    if d <= 1:
        grip = parts("Handheld_Grip", "RK_Rubber")
        add_sweep(grip, [B + A * 0.012, B + A * 0.07], [(x, y) for x, y in rounded_rect(hd + 0.0016, hw + 0.0016, 0.0095,
                                                                                       max(1, cs))])
    zh, yb, yf = 0.152, 0.045, -0.10
    nring = {0: 14, 1: 5, 2: 2}[d]
    hcs = max(1, cs * 2 if d == 0 else cs)
    rings = []
    for i in range(nring):
        u = i / (nring - 1)
        w, h = 0.042 + 0.02 * u ** 1.5, 0.036 + 0.012 * u
        y = yb + (yf - yb) * u
        rings.append([(a, y, zh + b) for a, b in rounded_rect(w, h, 0.01, hcs)])
    loft(body, rings)
    win = parts("Handheld_Window", "RK_Window_Red")
    add_box(win, (0.054, 0.0016, 0.036), (0, yf - 0.0004, zh))
    if d <= 1:
        grip = parts("Handheld_Grip", "RK_Rubber")
        loft(grip, [[(a, y, zh + b) for a, b in rounded_rect(0.0635, 0.0495, 0.0105, max(1, cs))] for y in (yf + 0.012, yf - 0.0006)])
        add_beveled_box(body, (0.012, 0.011, 0.024), (0, T.y - 0.026, 0.118), corner=0.004, bevel=0.0012, seg=max(1, cs))
    cab = parts("Cable", "RK_Black_ABS")
    zc, rc, r = 0.0085, 0.006, 0.0017
    lead = [tuple(B - A * 0.002), (0, 0.06, 0.02), (0, 0.075, zc - rc), (0, 0.08, zc - rc)]
    if d == 2:
        end_y = 0.08 + p["sc_coil_pitch_m"] * p["sc_coil_turns"] + 0.012
        add_tube(cab, lead + [(0, end_y, zc - rc)], r * 1.4, 6)
        return {"liftable_parts": ["Handheld_Body", "Handheld_Window"]}
    add_tube(cab, lead, r, 6, bend_radius=0.006, bend_steps=3)
    per = 24 if d == 0 else 8
    turns = p["sc_coil_turns"]
    helix = [(rc * math.sin(2 * math.pi * i / per), 0.08 + p["sc_coil_pitch_m"] * i / per, zc - rc * math.cos(2 * math.pi * i / per))
             for i in range(turns * per + 1)]
    end = helix[-1]
    add_tube(cab, helix + [(0, end[1] + 0.006, zc - rc), (0, end[1] + 0.012, zc - rc)], r, 6)
    return {"liftable_parts": ["Handheld_Body", "Handheld_Grip", "Handheld_Window"]}


# --- RK-06a kraft bag bundle ---------------------------------------------------------------------------------------

def build_bag_bundle(parts, p, lod):
    d = lod["d"]
    w, l, t, n = p["bag_w_m"], p["bag_l_m"], p["bag_t_m"], p["bag_count"]
    rng = random.Random(p["seed"])
    bags = parts("Bags", "RK_Kraft")
    if d >= 3:
        add_box(bags, (w, l, n * t), (0, 0, n * t / 2))
        return {}
    group = {0: 1, 1: 2, 2: 6}[d]
    teeth = p["bag_teeth"] if d == 0 else 0
    out = [(-w / 2, -l / 2), (w / 2, -l / 2), (w / 2, l / 2)]
    if teeth:
        tw = w / teeth
        for k in range(teeth):  # irregular peaks: real serration, and no colinear points for the cap triangulation
            out += [(w / 2 - (k + 0.5) * tw, l / 2 - 0.004 + rng.uniform(-0.0006, 0.0006)), (w / 2 - (k + 1) * tw, l / 2 - rng.uniform(0.0, 0.0008))]
    else:
        out.append((-w / 2, l / 2))
    jit = p["bag_jitter_m"]
    for i in range(0, n, group):
        dx, dy, da = rng.uniform(-jit, jit), rng.uniform(-jit, jit), rng.uniform(-0.03, 0.03)
        ca, sa = math.cos(da), math.sin(da)
        pts = [(x * ca - y * sa + dx, x * sa + y * ca + dy) for x, y in out]
        z0, z1 = i * t, min(n, i + group) * t - 0.0002
        loft(bags, [[(x, y, z) for x, y in pts] for z in (z0, z1)])
    top = n * t
    if d <= 1:
        flap = parts("TopBag_Detail", "RK_Kraft_Dark")
        add_box(flap, (w - 0.006, p["bag_flap_m"], 0.0006), (0, -l / 2 + p["bag_flap_m"] / 2 + 0.003, top + 0.0001))
        for sx in (-1, 1):  # gusset fold lines
            add_box(flap, (0.002, l - p["bag_flap_m"] - 0.02, 0.0003), (sx * (w / 2 - p["bag_gusset_m"]), 0.01, top))
    band = parts("Band", "RK_Paper_White")
    bw, bt = 0.025, 0.0004
    e = jit + 0.0006
    path = [(-w / 2 - e, 0, -bt), (w / 2 + e, 0, -bt), (w / 2 + e, 0, top + bt), (-w / 2 - e, 0, top + bt)]
    add_sweep(band, path, [(-bw / 2, -bt / 2), (bw / 2, -bt / 2), (bw / 2, bt / 2), (-bw / 2, bt / 2)], closed=True)
    return {}


# --- RK-06b tape roll ----------------------------------------------------------------------------------------------

def build_tape_roll(parts, p, lod):
    d, s = lod["d"], lod["s"]
    ro, ri, cw = p["tape_od_m"] / 2, p["tape_core_od_m"] / 2, p["tape_w_m"]
    tape = parts("Tape", "RK_Tape_Yellow")
    if d >= 3:
        add_cylinder_between(tape, (0, 0, 0), (0, 0, cw + 0.0016), ro, 8)
        return {}
    segs = ev(s * 2 if d == 0 else s)
    z0 = 0.0008
    lathe_loop(tape, [(ri, z0 + 0.0004), (ro - 0.001, z0), (ro, z0 + 0.001), (ro, z0 + cw - 0.001), (ro - 0.001, z0 + cw),
                      (ri, z0 + cw - 0.0004)], segs)
    core = parts("Core", "RK_Cardboard")
    lathe_loop(core, [(ri - 0.003, 0), (ri, 0), (ri, cw + 0.0016), (ri - 0.003, cw + 0.0016)], segs)
    if d <= 1:  # loose tail peeling off the roll
        tail = parts("Tail", "RK_Tape_Yellow")
        path = [(ro - 0.0002, -0.012, z0 + cw / 2), (ro + 0.0003, 0.004, z0 + cw / 2), (ro + 0.004, 0.022, z0 + cw / 2),
                (ro + 0.011, 0.034, z0 + cw / 2)]
        hw = cw / 2 - 0.0012
        add_sweep(tail, path, [(-0.0002, -hw), (0.0002, -hw), (0.0002, hw), (-0.0002, hw)])
    return {}


# --- RK-06c paper stock box (receipt/label paper, DEC-104 R4) -----------------------------------------------------

def build_paper_box(parts, p, lod):
    d, s = lod["d"], lod["s"]
    W, D, H, th = p["box_w_m"], p["box_d_m"], p["box_h_m"], p["box_wall_m"]
    rng = random.Random(p["seed"])
    body = parts("Box", "RK_Corrugated_White")
    if not p.get("box_open"):
        if d >= 3:
            add_box(body, (W, D, H), (0, 0, H / 2))
            return {}
        add_beveled_box(body, (W, D, H), (0, 0, H / 2), corner=0.002, bevel=0.0015 if d < 2 else 0, seg=1 if d else 2)
        if d <= 1:
            seam = parts("Seam", "RK_Seam_Dark")
            add_box(seam, (W - 0.004, 0.0015, 0.0006), (0, 0, H))
            tape = parts("Tape", "RK_Tape_Clear")
            e, tw, tt = 0.0004, p["box_tape_w_m"], 0.0003
            add_sweep(tape, [(-W / 2 - e, 0, H - 0.05), (-W / 2 - e, 0, H + e), (W / 2 + e, 0, H + e), (W / 2 + e, 0, H - 0.05)],
                      [(-tw / 2, -tt / 2), (tw / 2, -tt / 2), (tw / 2, tt / 2), (-tw / 2, tt / 2)])
            lab = parts("Label", "RK_Label_White", label_rect=(-0.05, 0.05, H * 0.35, H * 0.35 + 0.06))
            add_box(lab, (0.1, 0.0006, 0.06), (0, -D / 2 - 0.0003, H * 0.35 + 0.03))
        return {}
    add_box(body, (W, D, th), (0, 0, th / 2))
    for sy in (-1, 1):
        add_box(body, (W, th, H), (0, sy * (D / 2 - th / 2), H / 2))
    for sx in (-1, 1):
        add_box(body, (th, D - 2 * th, H), (sx * (W / 2 - th / 2), 0, H / 2))
    flaps = parts("Flaps", "RK_Corrugated_White")
    for sy in (-1, 1):  # long flaps, leaning outward
        a = math.radians(rng.uniform(*p["flap_open_deg"]))
        lf = D / 2 - 0.002
        c = Vector((0, sy * (D / 2 - th / 2), H)) + Vector((0, sy * math.sin(a), math.cos(a))) * lf / 2
        box_rot(flaps, (W - 0.002, th, lf), c, rx=-sy * a)
    for sx in (-1, 1):
        a = math.radians(rng.uniform(*p["flap_open_deg"]))
        lf = min(D / 2, 0.08)
        c = Vector((sx * (W / 2 - th / 2), 0, H)) + Vector((sx * math.sin(a), 0, math.cos(a))) * lf / 2
        box_rot(flaps, (th, D - 0.03, lf), c, ry=sx * a)
    if d >= 3:  # walls and flaps keep the open silhouette; rolls drop out
        return {}
    rolls, cores = parts("Rolls", "RK_Paper_White"), parts("RollCores", "RK_Cardboard")
    rr, rh = p["roll_od_m"] / 2, p["roll_w_m"]
    add_box(body, (W - 2 * th, D - 2 * th, 0.003), (0, 0, H - 0.01 - rh - 0.0015))  # layer divider
    nx, ny = int((W - 2 * th) // (2 * rr)), int((D - 2 * th) // (2 * rr))
    segs = ev(s if d == 0 else s // 2)
    z0 = H - 0.01 - rh
    for ix in range(nx):
        for iy in range(ny):
            if rng.random() < p["roll_missing_p"]:
                continue
            cx, cy = (ix - (nx - 1) / 2) * 2 * rr, (iy - (ny - 1) / 2) * 2 * rr
            if d == 2:
                add_cylinder_between(rolls, (cx, cy, z0), (cx, cy, z0 + rh), rr - 0.001, 8)
                continue
            lathe_loop(rolls, [(0.0065, 0), (rr - 0.0025, 0), (rr - 0.001, 0.0012), (rr - 0.001, rh - 0.0012),
                               (rr - 0.0025, rh), (0.0065, rh)], segs, center=(cx, cy, z0))
            lathe_loop(cores, [(0.0055, 0), (0.0066, 0), (0.0066, rh), (0.0055, rh)], ev(segs // 2), center=(cx, cy, z0))
    return {}


# --- RK-06d tumbler (personal item, GAP-REG-6) --------------------------------------------------------------------

def build_tumbler(parts, p, lod):
    d, s = lod["d"], lod["s"]
    rb, rt, hb = p["tu_base_d_m"] / 2, p["tu_top_d_m"] / 2, p["tu_body_h_m"]
    body = parts("Body", "RK_Stainless")
    if d >= 3:
        add_lathe(body, (0, 0, 0), (0, 0, 1), [(0, 0), (rb, 0), (rt, hb + 0.016), (0, hb + 0.016)], 8)
        return {}
    segs = ev(s * 2 if d == 0 else s)
    prof = [(0, 0), (rb - 0.003, 0), (rb, 0.003), (rb, 0.014), (rb - 0.0012, 0.017), (rb - 0.0005, 0.03),
            (rt, hb - 0.006), (rt, hb)]
    if d >= 2:
        prof = [(0, 0), (rb, 0), (rb, 0.014), (rt, hb)]
    add_lathe(body, (0, 0, 0), (0, 0, 1), prof + [(rt - 0.003, hb), (rb - 0.004, 0.012), (0, 0.012)], segs)
    lid = parts("Lid", "RK_Lid_Clear")
    add_lathe(lid, (0, 0, 0), (0, 0, 1), [(0, hb - 0.005), (rt + 0.0016, hb - 0.005), (rt + 0.0016, hb + 0.008),
                                          (rt - 0.002, hb + 0.0145), (0, hb + 0.015)], segs)
    straw = parts("Straw", "RK_Straw")  # kept at LOD2 so the silhouette matches size_m
    add_tube(straw, [(0.014, 0.004, 0.03), (0.019, 0.006, hb + p["tu_straw_out_m"])], 0.0035, ev(s // 2))
    if d <= 1:
        add_lathe(parts("Gasket", "RK_Rubber"), (0.0185, 0.006, hb + 0.012), (0, 0, 1),
                  [(0, 0), (0.0062, 0), (0.0062, 0.0035), (0, 0.0035)], ev(s // 2))
    return {}


# --- RK-06e wipes soft pack (sparse, DEC-104 R5) -------------------------------------------------------------------

def build_wipes(parts, p, lod):
    d, s = lod["d"], lod["s"]
    W, D, H = p["wp_w_m"], p["wp_d_m"], p["wp_h_m"]
    pack = parts("Pack", "RK_Pack_White")
    if d >= 3:
        add_box(pack, (W, D, H), (0, 0, H / 2))
        return {}
    n = ev(s * 2 if d == 0 else s)
    n += (4 - n % 4) % 4

    def ring(sx, sy, z, grow=1.0):
        out = []
        for i in range(n):
            a = 2 * math.pi * i / n
            c, sn = math.cos(a), math.sin(a)
            out.append((W / 2 * sx * grow * math.copysign(abs(c) ** 0.35, c), D / 2 * sy * grow * math.copysign(abs(sn) ** 0.7, sn), z))
        return out

    prof = [(0.97, 0.7, 0), (1, 0.92, 0.15), (1, 1, 0.45), (0.99, 0.85, 0.75), (0.96, 0.55, 0.92), (0.93, 0.2, 1.0)]
    if d >= 2:
        prof = [prof[0], prof[2], prof[-1]]
    loft(pack, [ring(sx, sy, z * H) for sx, sy, z in prof])
    if d <= 1:
        band = parts("Band", "RK_Pack_Blue")
        loft(band, [ring(1.0, 1.0, z * H, 1.006) for z in (0.3, 0.6)])
        for sx in (-1, 1):  # crimped end seals
            seal = parts("Seals", "RK_Pack_White")
            for k in range(6 if d == 0 else 1):
                add_box(seal, (0.008, D * 0.55, 0.0012 if d == 0 else H * 0.7),
                        (sx * (W / 2 * 0.95 + 0.002), 0, H * (0.2 + 0.1 * k) if d == 0 else H * 0.45))
    lid = parts("Lid", "RK_Pack_Blue")
    add_beveled_box(lid, (p["wp_lid_w_m"], p["wp_lid_d_m"], 0.006), (0, 0, H - 0.002), corner=0.01, bevel=0.0015 if d < 2 else 0,
                    seg=max(1, lod["cs"]))
    if d <= 1:
        add_cylinder_between(lid, (-p["wp_lid_w_m"] / 2 + 0.01, p["wp_lid_d_m"] / 2, H + 0.001),
                             (p["wp_lid_w_m"] / 2 - 0.01, p["wp_lid_d_m"] / 2, H + 0.001), 0.002, 8)
    return {}


# --- RK-07 ISO spray bottle (some stands only, DEC-104 R3) --------------------------------------------------------

def build_spray(parts, p, lod):
    d, s = lod["d"], lod["s"]
    body = parts("Body", "RK_Bottle_White")
    prof = p["sb_profile"]
    if d >= 3:
        add_box(body, (prof[2][0], prof[2][1], prof[-1][2]), (0, 0, prof[-1][2] / 2))
        add_box(parts("Trigger", "RK_Trigger_Red"), (0.03, 0.08, 0.06), (0, -0.02, prof[-1][2] + 0.03))
        return {"attach_blender": (0, 0, prof[-1][2])}
    n = ev(s * 2 if d == 0 else s)
    n += (4 - n % 4) % 4

    def ring(w, dd, z, e=0.6, arc=None):
        out = []
        for i in range(n if arc is None else arc[2] + 1):
            a = 2 * math.pi * i / n if arc is None else arc[0] + (arc[1] - arc[0]) * i / arc[2]
            c, sn = math.cos(a), math.sin(a)
            out.append((w / 2 * math.copysign(abs(c) ** e, c), dd / 2 * math.copysign(abs(sn) ** e, sn), z))
        return out

    rows = prof if d == 0 else prof[::2] + ([prof[-1]] if len(prof) % 2 == 0 else [])
    loft(body, [ring(w, dd, z) for w, dd, z in rows])
    top = prof[-1][2]
    head = parts("Trigger", "RK_Trigger_Red")
    add_lathe(head, (0, 0, top - 0.004), (0, 0, 1), [(0, 0), (0.0172, 0), (0.0172, 0.016), (0.015, 0.019), (0, 0.019)],
              ev(s if d == 0 else s // 2))
    add_beveled_box(head, (0.03, 0.074, 0.044), (0, -0.02, top + 0.038), corner=0.008, bevel=0.003 if d < 2 else 0,
                    seg=max(1, lod["cs"]))
    add_lathe(head, (0, -0.056, top + 0.048), (0, -1, 0), [(0, 0), (0.0075, 0), (0.0075, 0.009), (0.004, 0.0125), (0, 0.0125)], 6)
    if d <= 1:
        add_sweep(head, [(0, -0.044, top + 0.02), (0, -0.05, top + 0.002), (0, -0.047, top - 0.022), (0, -0.04, top - 0.034)],
                  [(-0.003, -0.008), (0.003, -0.008), (0.003, 0.008), (-0.003, 0.008)])
        tube = parts("DipTube", "RK_Straw")
        add_tube(tube, [(0.004, 0.0, top + 0.005), (0.006, 0.004, 0.06), (0.012, 0.006, 0.005)], 0.0022, 6,
                 bend_radius=0.02, bend_steps=3)
        liq = parts("Liquid", "RK_Liquid")
        fill = p["sb_fill_z_m"]
        lrows = [(w - 0.004, dd - 0.004, max(z, 0.002)) for w, dd, z in prof if z < fill] + \
                [(rows[0][0] - 0.004, rows[0][1] - 0.004, fill)]
        lrows[-1] = (min(r[0] for r in lrows), min(r[1] for r in lrows), fill)
        loft(liq, [ring(w, dd, z) for w, dd, z in lrows])
        lab = parts("Label", "RK_Label_White", label_rect=(-0.035, 0.035, p["sb_label_z_m"][0], p["sb_label_z_m"][1]))
        w0, d0 = prof[2][0], prof[2][1]
        arc = (math.radians(200), math.radians(340), 12 if d == 0 else 6)
        rings = []
        for z in p["sb_label_z_m"]:
            outer = ring(w0 + 0.0012, d0 + 0.0012, z, arc=arc)
            inner = ring(w0 + 0.0002, d0 + 0.0002, z, arc=arc)
            rings.append(outer + inner[::-1])
        loft(lab, rings)
    return {"attach_blender": (0, 0, top), "optional_parts": ["Liquid"]}


# --- RK-08 blue rag (DEC-104 R5) ----------------------------------------------------------------------------------

def resample(pts, n):
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total, out, acc, k = sum(seg), [], 0.0, 0
    for i in range(n):
        target = total * i / (n - 1)
        while k < len(seg) - 1 and acc + seg[k] < target:
            acc += seg[k]
            k += 1
        t = 0 if seg[k] == 0 else min(1.0, (target - acc) / seg[k])
        out.append(tuple(a + (b - a) * t for a, b in zip(pts[k], pts[k + 1])))
    return out


def cloth(bm, centre_yz, width, thick, nu, amp, rng):
    """Thick cloth sheet: centre line in YZ swept across X, wrinkled along its normal, closed edges."""
    nv = len(centre_yz)
    nz = noise2(rng, 3)
    nz2 = noise2(rng, 2)
    grid = {}
    for j, (y, z) in enumerate(centre_yz):
        a, b = centre_yz[max(0, j - 1)], centre_yz[min(nv - 1, j + 1)]
        ty, tz = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(ty, tz) or 1.0
        ny, nzz = -tz / ln, ty / ln
        v = j / (nv - 1)
        for i in range(nu):
            u = i / (nu - 1)
            off = amp(v) * (nz(u * 3, v * 4) + 0.3 * nz2(u * 9, v * 2))
            x = -width / 2 + width * u + amp(v) * 0.4 * nz2(v * 5, u)
            for side, sg in (("t", 1), ("b", -1)):
                o = off + sg * thick / 2
                grid[side, i, j] = bm.verts.new((x, y + ny * o, z + nzz * o))
    for j in range(nv - 1):
        for i in range(nu - 1):
            bm.faces.new([grid["t", i, j], grid["t", i + 1, j], grid["t", i + 1, j + 1], grid["t", i, j + 1]])
            bm.faces.new([grid["b", i, j + 1], grid["b", i + 1, j + 1], grid["b", i + 1, j], grid["b", i, j]])
    edge = [(i, 0) for i in range(nu)] + [(nu - 1, j) for j in range(1, nv)] + \
           [(i, nv - 1) for i in range(nu - 2, -1, -1)] + [(0, j) for j in range(nv - 2, 0, -1)]
    for (i0, j0), (i1, j1) in zip(edge, edge[1:] + edge[:1]):
        bm.faces.new([grid["t", i0, j0], grid["b", i0, j0], grid["b", i1, j1], grid["t", i1, j1]])


def build_rag(parts, p, lod):
    d = lod["d"]
    rag = parts("Rag", "RK_Rag_Blue")
    rng = random.Random(p["seed"])
    t, wd = p["rag_t_m"], p["rag_w_m"]
    if p["rag_form"] == "draped":
        rb, Lt, Lh = p["rag_edge_r_m"], p["rag_top_m"], p["rag_hang_m"]
        R = rb + t / 2
        line = [(Lt, t / 2), (rb, t / 2)] + [(rb + R * math.cos(math.radians(a)), -rb + R * math.sin(math.radians(a)))
                                             for a in range(90, 181, 10)] + [(-t / 2, -Lh)]
        if d >= 3:
            add_box(rag, (wd, Lt + t, t * 2), (0, Lt / 2, t))
            add_box(rag, (wd, t * 2, Lh), (0, -t, -Lh / 2))
            return {"attach_blender": (0, 0, 0)}
        amp = lambda v: p["rag_amp_m"] * (0.25 + 1.6 * max(0.0, v - 0.35))
        attach = (0, 0, 0)
    else:
        L, k = p["rag_fold_l_m"], p["rag_layers"]
        line = []
        for layer in range(k):
            z = t / 2 + layer * t * 1.15
            xs = (L / 2, -L / 2) if layer % 2 == 0 else (-L / 2, L / 2)
            line += [(xs[0], z), (xs[1], z)]
            if layer < k - 1:  # U-turn
                c = (xs[1], z + t * 0.575)
                sgn = -1 if layer % 2 == 0 else 1
                line += [(c[0] + sgn * t * 0.575 * math.sin(math.radians(a)), c[1] - t * 0.575 * math.cos(math.radians(a)))
                         for a in range(30, 180, 30)]
        if d >= 3:
            add_box(rag, (wd, L + t, k * t * 1.15), (0, 0, k * t * 1.15 / 2))
            return {}
        amp = lambda v: p["rag_amp_m"]
        attach = None
    nv, nu = {0: (p["rag_nv"], p["rag_nu"]), 1: (p["rag_nv"] // 2, p["rag_nu"] // 2), 2: (8, 5)}[d]
    cloth(rag, resample(line, nv), wd, t, nu, amp if d < 2 else (lambda v: 0.0), rng)
    return {"attach_blender": attach} if attach else {}


# --- RK-09 small trash bin (DEC-104 R7) ---------------------------------------------------------------------------

def crumples(bm, rng, n, center_r, z0, rmin, rmax, subdiv):
    for _ in range(n):
        a, rr = rng.uniform(0, 6.283), rng.uniform(0, center_r)
        r = rng.uniform(rmin, rmax)
        c = Vector((rr * math.cos(a), rr * math.sin(a), z0 + r * 0.8))
        res = bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=r)
        f = noise2(random.Random(rng.random()), 3)
        for v in res["verts"]:
            nrm = v.co.normalized()
            v.co = c + nrm * r * (1 + 0.28 * f(nrm.x * 2 + nrm.z, nrm.y * 2 - nrm.z)) * Vector((1, 1, 0.75))


def build_trash(parts, p, lod):
    d, s = lod["d"], lod["s"]
    rb, rt, H = p["tb_bottom_d_m"] / 2, p["tb_top_d_m"] / 2, p["tb_h_m"]
    rng = random.Random(p["seed"])
    if p["tb_type"] == "wire_mesh":
        frame = parts("Frame", "RK_Wire_Black")
        if d >= 3:
            add_lathe(frame, (0, 0, 0), (0, 0, 1), [(0, 0), (rb, 0), (rt, H), (0, H)], 8)
            return {"optional_parts": []}
        rr = p["tb_rim_r_m"]
        segs = ev(s * 2 if d == 0 else s)
        if d == 2:  # alpha card shell (mesh read from the texture, DEC-084 LOD2)
            card = parts("MeshCard", "RK_Wire_Card")
            lathe_loop(card, [(rb, 0), (rt, H), (rt - 0.002, H), (rb - 0.002, 0)], 24)
            add_lathe(frame, (0, 0, 0), (0, 0, 1), [(0, 0), (rb, 0), (rb, 0.004), (0, 0.004)], 12)
            return {"optional_parts": []}
        add_tube(frame, [(rt * math.cos(2 * math.pi * i / segs), rt * math.sin(2 * math.pi * i / segs), H - rr) for i in range(segs)],
                 rr, 8 if d == 0 else 6, closed=True)
        rb2 = 0.004
        add_tube(frame, [((rb + 0.001) * math.cos(2 * math.pi * i / segs), (rb + 0.001) * math.sin(2 * math.pi * i / segs), rb2)
                         for i in range(segs)], rb2, 6, closed=True)
        add_lathe(frame, (0, 0, 0), (0, 0, 1), [(0, 0.001), (rb - 0.002, 0.001), (rb - 0.002, 0.004), (0, 0.004)], segs)
        mesh = parts("Mesh", "RK_Wire_Black")
        nw, m = (p["tb_wires"], p["tb_wire_pts"]) if d == 0 else (p["tb_wires"] * 3 // 5, p["tb_wire_pts"] * 3 // 5)
        twist = p["tb_twist_rad"]
        wr = p["tb_wire_r_m"]
        for sg in (-1, 1):
            for k in range(nw):
                th0 = 2 * math.pi * k / nw
                pts = []
                for i in range(m + 1):
                    t = i / m
                    z = 2 * rb2 + t * (H - 2 * rr - 2 * rb2)
                    r = rb + (rt - rb) * (z / H) + sg * wr * 0.9
                    th = th0 + sg * twist * t
                    pts.append((r * math.cos(th), r * math.sin(th), z))
                add_tube(mesh, pts, wr, 6)
        fill_r = rb * 0.75
    else:
        shell = parts("Shell", "RK_PP_White")
        if d >= 3:
            add_lathe(shell, (0, 0, 0), (0, 0, 1), [(0, 0), (rb, 0), (rt + 0.004, H), (0, H)], 8)
            return {"optional_parts": []}
        segs = ev(s * 2 if d == 0 else s)
        add_lathe(shell, (0, 0, 0), (0, 0, 1), [(0, 0), (rb - 0.004, 0), (rb, 0.004), (rt, H - 0.008), (rt + 0.004, H - 0.006),
                                                (rt + 0.004, H), (rt - 0.003, H), (rt - 0.004, H - 0.006), (rb - 0.003, 0.004),
                                                (0, 0.004)], segs)
        if p.get("tb_liner"):
            liner = parts("Liner", "RK_Liner_Green")
            w = noise2(rng, 3)
            add_lathe(liner, (0, 0, 0), (0, 0, 1), [(0, 0.0045), (rb - 0.0035, 0.0045), (rt - 0.0042, H), (rt - 0.0052, H),
                                                    (rb - 0.0045, 0.0055), (0, 0.0055)], segs)
            if d <= 1:  # cuff folded over the rim, wrinkled below the lip
                lathe_loop(liner, [(rt + 0.0046, H - p["tb_cuff_m"]), (rt + 0.0056, H - p["tb_cuff_m"]), (rt + 0.0056, H + 0.0016),
                                   (rt - 0.0052, H + 0.0016), (rt - 0.0052, H + 0.0006), (rt + 0.0046, H + 0.0006)],
                           segs, disp=lambda a, r, z: 0.0015 * w(a * 2.0, z * 30) if z < H - 0.003 else 0.0)
        fill_r = rb * 0.7
    if d <= 2:
        fill = parts("Fill", "RK_Paper_Crumple")
        crumples(fill, rng, p["tb_fill_count"] if d == 0 else 3, fill_r, 0.006, 0.026, 0.04, 2 if d == 0 else 1)
    return {"optional_parts": ["Fill"]}


BUILDERS = {"keyboard": build_keyboard, "mouse": build_mouse, "receipt_printer": build_receipt_printer,
            "label_printer": build_label_printer, "scanner": build_scanner, "bag_bundle": build_bag_bundle,
            "tape_roll": build_tape_roll, "paper_box": build_paper_box, "tumbler": build_tumbler, "wipes": build_wipes,
            "spray_bottle": build_spray, "rag": build_rag, "trash_bin": build_trash}


def build(p, lod):
    parts = Parts(p["colors"])
    info = BUILDERS[p["kind"]](parts, p, lod) or {}
    for bm, *_ in parts._p.values():  # shortcut: reaches into proclib.Parts so builders need not care about winding
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    objs = parts.finish()
    pts = [v.co for o in objs.values() for v in o.data.vertices]
    lo = [min(c[i] for c in pts) for i in range(3)]
    hi = [max(c[i] for c in pts) for i in range(3)]
    shift = Vector((-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]))
    for o in objs.values():
        o.data.transform(Matrix.Translation(shift))
    size = [b - a for a, b in zip(lo, hi)]
    tol = p.get("size_tol_m", 0.003)
    bad = [f"{ax} {v:.4f} vs {e:.4f}" for ax, v, e in zip("WDH", size, p["size_m"]) if abs(v - e) > tol]
    if bad and os.environ.get("RK_MEASURE"):  # tuning aid: report instead of failing
        print(f"[RK_MEASURE] {p['id']} {lod['d']}: size {[round(v, 4) for v in size]} :: " + ", ".join(bad))
    elif bad:
        raise ValueError(f"{p['id']} {lod}: outside the size_m envelope (tol {tol}): " + ", ".join(bad))
    w, dd, h = size
    extra = {"register_kit": {"rk": p["rk"], "kind": p["kind"], "anchors": p["anchors"],
                              "anchor_id": None, "anchor_gap": "anchor id pending ROOM_FIXTURES rev7 (REF-011)",
                              "fixed_every_register": p.get("fixed", False), "facing": "-Y Blender / +Z Unity faces the operator",
                              "materials": "preview colours; 2K PBR set pending PROC-005 Q0.2/Q0.3"},
             "seed": int(p["seed"]),
             "collision_boxes": [collision_box("Body", (0, 0, h / 2), (w, dd, h))]}
    for k in ("liftable_parts", "optional_parts"):
        if k in info:
            extra["register_kit"][k] = info[k]
    if info.get("attach_blender") is not None:
        a = Vector(info["attach_blender"]) + shift
        extra["register_kit"]["attach_point_unity_xyz"] = to_unity(*a)
    extra.update(wear(p))
    return objs, (w, h, dd), extra
