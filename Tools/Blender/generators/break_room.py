"""Break room (PROC-005 §9; fix wave after REVIEW-PROC5). One asset per ROOM_FIXTURES row ([w, d, h] ft):
staff lockers (2 x 6 doors, DEC-047/051/088): folded side flanges, recessed toe kick, stamped louvres with real gaps,
lift handles + hasp, number plates with rivets, knuckle hinges, grey cap; wood bench (3 eased planks on filleted
square-tube frames, rails, glides, screws); the five boards (mitred moulded frames, recessed faces, whiteboard tray and
inner trim); lunch table (eased top, tube apron + legs, glides); first-aid cabinet (moulded door rim, raised cross,
knuckle hinge, latch); base cabinets (finished end panels, black-melamine carcass seen through 3 mm reveals, TI 4 in
toe kick with 2 in recess, drawer + door slabs, black bar pulls, eased black top + backsplash, sink cut-out); uppers;
stainless double sink (rolled deck annulus, coved bowls with sheet thickness, strainers, chrome pull-down gooseneck);
microwave and pod coffee maker (fascia seams, door frame + window, keypad, side vent ribs, feet, drip grate, buttons);
over-the-hamper mini hoop (wire hamper, uprights, backboard, rim, diamond net, ball with seams); coat-hook rail.
Every size/count/colour is cited or GAP-labelled in params (`_src`, `_colors_src`). Origin = bottom centre,
front = -Y (wall at +Y). LOD0 full; LOD1 no micro detail; LOD2 plain boxes; LOD3 blocks."""
import math

import bmesh

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_handle_pull, add_lathe, add_screw_head,
                     add_sweep, add_tube, collision_box, fillet, hinge_axis, rect_profile, rounded_rect, wear)


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


# --- local helpers -------------------------------------------------------------------------------------------------

def _bb(bm, size, center, d, corner=0.003, bevel=0.0015):
    if d >= 2:
        add_box(bm, size, center)
    else:
        add_beveled_box(bm, size, center, corner=corner, bevel=bevel, seg=3 if d == 0 else 1)


def _new_faces(bm, n0):
    bm.faces.ensure_lookup_table()
    return [bm.faces[i] for i in range(n0, len(bm.faces))]


def _solid(bm, fn, *a, **kw):
    """Run a proclib builder and make the new shell's normals consistent (profiles here are not all CCW)."""
    n0 = len(bm.faces)
    fn(bm, *a, **kw)
    bmesh.ops.recalc_face_normals(bm, faces=_new_faces(bm, n0))


def _prism(bm, a, b, caps=True):
    """Shell between two equal-length 3D point rings (mitred frame members, plates)."""
    n0 = len(bm.faces)
    va, vb = [bm.verts.new(p) for p in a], [bm.verts.new(p) for p in b]
    n = len(a)
    for i in range(n):
        bm.faces.new([va[i], va[(i + 1) % n], vb[(i + 1) % n], vb[i]])
    if caps:
        bm.faces.new(va[::-1])
        bm.faces.new(vb)
        bmesh.ops.recalc_face_normals(bm, faces=_new_faces(bm, n0))
        return
    # open member (joins its neighbours after the weld): convex section, so orient each face away from the centroid
    cen = sum((v.co for v in va + vb), va[0].co * 0) / (2 * n)
    for f in _new_faces(bm, n0):
        f.normal_update()
        if f.normal.dot(f.calc_center_median() - cen) < 0:
            f.normal_flip()


def _arc(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def _moulding(fw, y0, y1, r, n):
    """Frame section as (t, y): t = inset from the outer edge (0..fw), front face at y0, back at y1; eased front edges."""
    if n == 0 or r <= 0:
        return [(0.0, y1), (0.0, y0), (fw, y0), (fw, y1)]
    st = min(0.003, (y1 - y0) * 0.25)  # stepped inner lip with a cove (a real frame section, not a bar)
    rc = st / 2
    return ([(0.0, y1)] + _arc(r, y0 + r, r, 180, 270, n) + _arc(fw * 0.6, y0 + rc, rc, 270, 360, n)[:-1]
            + _arc(fw * 0.6 + 2 * rc, y0 + rc, rc, 180, 90, n) + [(fw - st * 0.3, y0 + st), (fw, y0 + st * 1.3), (fw, y1)])


def _frame(bm, W, H, prof, z0=0.0, cx=0.0):
    """Mitred picture frame in the XZ plane (outer W x H, bottom at z0), section prof from _moulding."""
    cs = (lambda t, y: (cx - W / 2 + t, y, z0 + t), lambda t, y: (cx + W / 2 - t, y, z0 + t),
          lambda t, y: (cx + W / 2 - t, y, z0 + H - t), lambda t, y: (cx - W / 2 + t, y, z0 + H - t))
    for k in range(4):
        a, b = cs[k], cs[(k + 1) % 4]
        _prism(bm, [a(t, y) for t, y in prof], [b(t, y) for t, y in prof], caps=False)


def _rtube(bm, path, w, h, d, r=0.003):
    """Rectangular (rounded) tube along a polyline: steel frames, rails, aprons."""
    _solid(bm, add_sweep, path, rect_profile(w, h, r if d <= 1 else 0.0, 2 if d == 0 else (1 if d == 1 else 0)))


def _screw(bm, c, axis, r, d, h=None):
    if d == 0:
        add_screw_head(bm, c, axis, r, 8, h)


# --- assets --------------------------------------------------------------------------------------------------------

def lockers(P, p, d, s, W, D, H):
    k = p["lockers"]
    cols, rows, kick, cap, ft_, hs = k["columns"], k["rows"], k["kick_h_m"], k["top_h_m"], k["frame_m"], k["handle_d_m"]
    yf = -D / 2 + hs  # door front; handles reach -D/2
    dw, dh = (W - 2 * ft_) / cols, (H - kick - cap - 2 * ft_) / rows
    zt = H - cap
    moving = []
    for c in range(cols):
        for r in range(rows):
            x0, z0 = -W / 2 + ft_ + c * dw, kick + ft_ + r * dh
            side = "left" if c == 0 else "right"
            moving.append(hinge_axis(f"Door_{c}{r}", x0 if side == "left" else x0 + dw, yf + 0.008, z0, z0 + dh, side, 100))
    coll = [collision_box("Body", (0, 0, H / 2), (W, D, H))]
    body = P("Body", "Locker_Grey")
    if d >= 3:
        add_box(body, (W, D - hs, H), (0, hs / 2, H / 2))
        add_box(P("Hardware", "Locker_Hardware"), (W * 0.2, hs, H * 0.8), (0, -D / 2 + hs / 2, H / 2))
        return {"moving_parts": moving, "collision_boxes": coll}
    hw = P("Hardware", "Locker_Hardware")
    yc = (yf + D / 2) / 2
    for sx in (-1, 1):  # side panels with the folded front flange, down to the floor around the kick
        _bb(body, (ft_, D - hs, zt), (sx * (W / 2 - ft_ / 2), yc, zt / 2), d, 0.002, 0.002)
    add_box(body, (W - 2 * ft_, 0.008, zt - kick), (0, D / 2 - 0.004, kick + (zt - kick) / 2))  # back
    _bb(P("Top", "Grey_Top"), (W, D - hs, cap), (0, yc, H - cap / 2), d, 0.004, 0.004 if d == 0 else 0.002)
    y0k, y1k = yf + 0.04, D / 2 - 0.01  # recessed toe kick
    add_box(body, (W - 2 * ft_, y1k - y0k, kick), (0, (y0k + y1k) / 2, kick / 2))
    for z in (kick + ft_ / 2, zt - ft_ / 2):  # face-frame rails, flush with the doors
        _bb(body, (W - 2 * ft_, 0.02, ft_), (0, yf + 0.01, z), d, 0.001, 0.001)
    yi0 = yf + 0.02
    for c in range(1, cols):  # recessed mullion + interior divider
        x = -W / 2 + ft_ + c * dw
        add_box(body, (0.01, 0.014, zt - kick - 2 * ft_), (x, yf + 0.006 + 0.007, (kick + zt) / 2))
        add_box(body, (0.004, D / 2 - 0.008 - yi0, zt - kick - 2 * ft_), (x, (yi0 + D / 2 - 0.008) / 2, (kick + zt) / 2))
    for r in range(1, rows):  # recessed rails + compartment floors
        z = kick + ft_ + r * dh
        add_box(body, (W - 2 * ft_, 0.014, 0.01), (0, yf + 0.006 + 0.007, z))
        add_box(body, (W - 2 * ft_, D / 2 - 0.008 - yi0, 0.004), (0, (yi0 + D / 2 - 0.008) / 2, z))
    g, T = 0.003, 0.016
    for c in range(cols):
        for r in range(rows):
            x0, z0 = -W / 2 + ft_ + c * dw, kick + ft_ + r * dh
            xm = x0 + dw / 2
            ww = dw - 2 * g
            door = P(f"Door_{c}{r}", "Locker_Grey")
            hx = xm + (ww / 2 - 0.028) * (1 if c == 0 else -1)  # latch side, opposite the hinge
            zh = z0 + dh * 0.33
            if d == 2:
                add_box(door, (ww, T, dh - 2 * g), (xm, yf + T / 2, z0 + dh / 2))
                add_box(hw, (0.016, hs, 0.05), (hx, -D / 2 + hs / 2, zh))
                continue
            za, zb = z0 + g, z0 + dh - g
            lz0, lz1 = z0 + dh * 0.56, z0 + dh * 0.84  # stamped louvre band, open onto the compartment
            sw = ww * 0.14
            _bb(door, (ww, T, lz0 - za), (xm, yf + T / 2, (za + lz0) / 2), d, 0.003, 0.003)
            _bb(door, (ww, T, zb - lz1), (xm, yf + T / 2, (lz1 + zb) / 2), d, 0.003, 0.003)
            for sx in (-1, 1):
                add_box(door, (sw, T, lz1 - lz0), (xm + sx * (ww / 2 - sw / 2), yf + T / 2, (lz0 + lz1) / 2))
            n = k["louvres_lod0"] if d == 0 else 3
            pitch = (lz1 - lz0) / n
            for i in range(n):
                z = lz0 + (i + 0.5) * pitch
                prof = [(yf + 0.014, z - 0.42 * pitch), (yf + 0.002, z + 0.12 * pitch), (yf + 0.002, z + 0.36 * pitch),
                        (yf + 0.014, z - 0.2 * pitch)]
                _solid(door, add_sweep, [(xm - ww / 2 + sw - 0.001, 0, 0), (xm + ww / 2 - sw + 0.001, 0, 0)], prof)
            _bb(hw, (0.022, 0.003, 0.07), (hx, yf - 0.0015, zh), d, 0.003, 0.001)  # latch escutcheon
            add_handle_pull(hw, (hx, yf - 0.003, zh), 0.05, hs - 0.007, 0.004, 8, axis="z", bend_steps=3 if d == 0 else 1)
            zp = (lz1 + zb) / 2
            _bb(hw, (0.045, 0.0015, 0.018), (xm, yf - 0.00075, zp), d, 0.002, 0.0005)  # number plate (blank)
            if d == 0:
                for sx in (-1, 1):
                    _screw(hw, (xm + sx * 0.0175, yf - 0.0015, zp), (0, -1, 0), 0.0018, d)
                zs = zh - 0.055  # padlock hasp staple
                add_tube(hw, [(hx, yf - 0.003, zs), (hx, yf - 0.012, zs), (hx, yf - 0.012, zs + 0.016), (hx, yf - 0.003, zs + 0.016)],
                         0.002, 8, bend_radius=0.004, bend_steps=2)
                hxk = x0 + (0.0035 if c == 0 else dw - 0.0035)
                for zz in (z0 + 0.035, z0 + dh - 0.035):  # knuckle hinges with pin caps
                    add_cylinder_between(hw, (hxk, yf + 0.003, zz - 0.016), (hxk, yf + 0.003, zz + 0.016), 0.0035, 8)
                    add_cylinder_between(hw, (hxk, yf + 0.003, zz + 0.016), (hxk, yf + 0.003, zz + 0.019), 0.002, 8)
    if d == 0:
        for sx in (-1, 1):  # rivets on the side flanges
            for r in range(rows + 1):
                _screw(body, (sx * (W / 2 - ft_ / 2), yf, kick + ft_ + r * dh - (0.006 if r == rows else -0.006)), (0, -1, 0),
                       0.0022, d)
    return {"moving_parts": moving, "collision_boxes": coll}


def bench(P, p, d, s, W, D, H):
    pt = p["bench"]["plank_t_m"]
    top, fr = P("Top", "Wood_Plank"), P("Frame", "Black_Steel")
    coll = [collision_box("Body", (0, 0, H / 2), (W, D, H))]
    if d >= 3:
        add_box(top, (W, D, pt), (0, 0, H - pt / 2))
        for sx in (-1, 1):
            add_box(fr, (0.03, D - 0.04, H - pt), (sx * (W / 2 - 0.15), 0, (H - pt) / 2))
        return {"collision_boxes": coll}
    n, gap = p["bench"]["planks"], 0.006
    pw = (D - (n - 1) * gap) / n
    for i in range(n):
        y0 = -D / 2 + i * (pw + gap)
        _bb(top, (W, pw, pt), (0, y0 + pw / 2, H - pt / 2), d, 0.008, 0.005 if d == 0 else 0.003)
    zr, tb = H - pt, 0.03
    xs = [sx * (W / 2 - 0.15) for sx in (-1, 1)]
    yl = D / 2 - 0.03
    for x in xs:  # filleted square-tube leg frames + cross stretcher + glides
        path = [(x, -yl, 0.012), (x, -yl, zr - tb / 2), (x, yl, zr - tb / 2), (x, yl, 0.012)]
        _rtube(fr, fillet(path, 0.03, 3 if d == 0 else 1) if d <= 1 else path, tb, tb, d)
        _rtube(fr, [(x, -yl, 0.12), (x, yl, 0.12)], 0.025, 0.025, d)
        for y in (-yl, yl):
            _bb(fr, (tb + 0.002, tb + 0.002, 0.012), (x, y, 0.006), d, 0.004, 0.002)
    for sy in (-1, 1):  # long rails under the planks
        _rtube(fr, [(xs[0], sy * (D / 2 - 0.07), zr - 0.0125), (xs[1], sy * (D / 2 - 0.07), zr - 0.0125)], 0.02, 0.025, d)
    if d <= 1:
        _rtube(fr, [(xs[0], 0, 0.12), (xs[1], 0, 0.12)], 0.025, 0.025, d)
    if d == 0:
        sc = P("Screws", "Black_Steel")
        for i in range(n):
            yc = -D / 2 + i * (pw + gap) + pw / 2
            for x in xs:
                for dy in (-pw * 0.25, pw * 0.25):
                    _screw(sc, (x, yc + dy, H - 0.0008), (0, 0, 1), 0.004, d, 0.0007)
    return {"collision_boxes": coll}


def board(P, p, d, s, W, D, H):
    b = p["board"]
    fw = b["frame_w_m"]
    fr, face = P("Frame", b["frame"]), P("Face", b["face"])
    if d >= 3:
        add_box(fr, (W, D, H), (0, 0, H / 2))
        return {}
    tray = b.get("tray")
    y0 = -D / 2 + (0.014 if tray else 0.0)  # the whiteboard tray takes the front 14 mm
    n = 3 if d == 0 else (1 if d == 1 else 0)
    _frame(fr, W, H, _moulding(fw, y0, D / 2, min(0.006, fw * 0.3), n))
    add_box(fr, (W - 0.01, 0.003, H - 0.01), (0, D / 2 - 0.0015, H / 2))  # backer
    yb = y0 + b["face_recess_m"]
    add_box(face, (W - 2 * fw + 0.006, D / 2 - 0.003 - yb, H - 2 * fw + 0.006), (0, (yb + D / 2 - 0.003) / 2, H / 2))
    if b.get("trim") and d <= 1:  # inner trim of the red/white frame
        tw = 0.008
        _frame(P("Trim", b["trim"]), W - 2 * fw + 2 * tw, H - 2 * fw + 2 * tw, _moulding(tw, y0 + 0.003, yb + 0.002, 0.002, n),
               z0=fw - tw)
    if tray and d <= 1:
        L = W - 0.06
        prof = [(-D / 2 + 0.014, 0.0), (-D / 2 + 0.002, 0.0), (-D / 2, 0.002), (-D / 2, 0.02), (-D / 2 + 0.003, 0.02),
                (-D / 2 + 0.003, 0.005), (-D / 2 + 0.014, 0.005)]
        _solid(fr, add_sweep, [(-L / 2, 0, 0), (L / 2, 0, 0)], prof)
        for sx in (-1, 1):
            _bb(fr, (0.008, 0.014, 0.022), (sx * (L / 2 + 0.004), -D / 2 + 0.007, 0.011), d, 0.002, 0.001)
    elif tray:
        add_box(fr, (W - 0.06, 0.014, 0.02), (0, -D / 2 + 0.007, 0.01))
    return {}


def table(P, p, d, s, W, D, H):
    t = p["table"]
    tt, leg, ap, ins = t["top_t_m"], t["leg_m"], t["apron_h_m"], t["leg_inset_m"]
    top, fr = P("Top", "Table_Top"), P("Frame", "Table_Frame")
    coll = [collision_box("Body", (0, 0, H / 2), (W, D, H))]
    if d >= 3:
        add_box(top, (W, D, tt), (0, 0, H - tt / 2))
        add_box(fr, (W - 0.1, D - 0.1, H - tt), (0, 0, (H - tt) / 2))
        return {"collision_boxes": coll}
    _bb(top, (W, D, tt), (0, 0, H - tt / 2), d, 0.02, 0.004 if d == 0 else 0.002)
    xl, yl, zt = W / 2 - ins, D / 2 - ins, H - tt
    for sy in (-1, 1):
        _rtube(fr, [(-xl, sy * yl, zt - ap / 2), (xl, sy * yl, zt - ap / 2)], 0.02, ap, d)
    for sx in (-1, 1):
        _rtube(fr, [(sx * xl, -yl, zt - ap / 2), (sx * xl, yl, zt - ap / 2)], 0.02, ap, d)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * xl, sy * yl
            _rtube(fr, [(x, y, 0.015 if d <= 1 else 0.0), (x, y, zt)], leg, leg, d)
            if d <= 1:  # levelling glide
                add_lathe(fr, (x, y, 0), (0, 0, 1), [(0, 0), (0.016, 0), (0.016, 0.005), (0.006, 0.008), (0.006, 0.0155), (0, 0.0155)],
                          s if d == 0 else 8)
            if d == 0:  # corner brace with screws into the top
                cx, cy = x - sx * 0.07, y - sy * 0.07
                _prism(fr, [(x - sx * 0.01, y - sy * 0.09, zt), (x - sx * 0.09, y - sy * 0.01, zt), (x - sx * 0.09, y - sy * 0.01, zt - 0.05),
                            (x - sx * 0.01, y - sy * 0.09, zt - 0.05)],
                       [(x - sx * 0.016, y - sy * 0.096, zt), (x - sx * 0.096, y - sy * 0.016, zt), (x - sx * 0.096, y - sy * 0.016, zt - 0.05),
                        (x - sx * 0.016, y - sy * 0.096, zt - 0.05)])
                _screw(fr, (cx, cy, zt - 0.025), (-sx * 0.7071, -sy * 0.7071, 0), 0.004, d)
    return {"collision_boxes": coll}


def first_aid(P, p, d, s, W, D, H):
    b = P("Body", "White_Plastic")
    if d >= 3:
        add_box(b, (W, D, H), (0, 0, H / 2))
        return {}
    dd = p["first_aid"]["door_d_m"]
    door, trim = P("Door", "White_Plastic"), P("Trim", "FirstAid_Trim_GAP")
    yb0 = -D / 2 + dd + 0.002  # 2 mm seam between door and box
    _bb(b, (W, D / 2 - yb0, H), (0, (yb0 + D / 2) / 2, H / 2), d, 0.015, 0.004 if d == 0 else 0.002)
    _bb(door, (W - 0.006, dd - 0.004, H - 0.006), (0, -D / 2 + 0.004 + (dd - 0.004) / 2, H / 2), d, 0.014, 0.003)
    if d <= 1:  # moulded door rim proud of the field
        _frame(door, W - 0.006, H - 0.006, _moulding(0.02, -D / 2, -D / 2 + 0.006, 0.003, 3 if d == 0 else 1), z0=0.003)
    else:
        add_box(door, (W - 0.006, 0.004, H - 0.006), (0, -D / 2 + 0.002, H / 2))
    cw, cl = W * 0.1, W * 0.32  # generic cross emblem (no brand); colour GAP
    for sz in ((cl, 0.003, cw), (cw, 0.003, cl)):
        _bb(trim, sz, (0, -D / 2 + 0.004 - 0.0015, H * 0.58), d, 0.002, 0.001)
    _bb(trim, (0.016, 0.006, 0.05), (W / 2 - 0.022, -D / 2 + 0.003, H * 0.5), d, 0.003, 0.0015)  # latch tab
    if d <= 1:
        for zz in ((0.03, 0.09), (H / 2 - 0.03, H / 2 + 0.03), (H - 0.09, H - 0.03)):  # knuckle hinge
            add_cylinder_between(trim, (-W / 2 + 0.0045, -D / 2 + dd, zz[0]), (-W / 2 + 0.0045, -D / 2 + dd, zz[1]), 0.0045, 8)
    return {"moving_parts": [hinge_axis("Door", -W / 2, -D / 2 + dd, 0, H, "left")]}


def base_cabinets(P, p, d, s, W, D, H):
    k = p["counter"]
    tt, sp, kick, hs, ov, rec = k["top_t_m"], k["splash_h_m"], k["kick_h_m"], k["pull_standoff_m"], k["overhang_m"], k["kick_recess_m"]
    T = 0.019
    yd = -D / 2 + ov + hs  # door front; pulls stay inside the top overhang
    zt = H - tt
    top, wood, car = P("Top", "Black_Top"), P("Fronts", "Light_Wood"), P("Carcass", "Black_Interior")
    coll = [collision_box("Body", (0, 0, H / 2), (W, D, H))]
    if d >= 3:
        add_box(top, (W, D, tt), (0, 0, zt + tt / 2))
        add_box(top, (W, 0.02, sp), (0, D / 2 - 0.01, H + sp / 2))
        add_box(wood, (W, D / 2 - yd, zt), (0, (yd + D / 2) / 2, zt / 2))
        return {"collision_boxes": coll}
    cut = k.get("sink_cutout")  # [x centre, width, depth] m: the top is built around the sink opening
    eb = 0.004 if d == 0 else 0.002  # eased edge
    if cut:
        cx, cw, cdp = cut
        cy = -D / 2 + 0.06 + cdp / 2
        for x0, x1 in ((-W / 2, cx - cw / 2), (cx + cw / 2, W / 2)):
            _bb(top, (x1 - x0, D, tt), ((x0 + x1) / 2, 0, zt + tt / 2), d, 0.002, eb)
        for y0, y1 in ((-D / 2, cy - cdp / 2), (cy + cdp / 2, D / 2)):
            add_box(top, (cw, y1 - y0, tt), (cx, (y0 + y1) / 2, zt + tt / 2))
    else:
        _bb(top, (W, D, tt), (0, 0, zt + tt / 2), d, 0.002, eb)
    _bb(top, (W, 0.02, sp), (0, D / 2 - 0.01, H + sp / 2), d, 0.002, eb)  # backsplash (height GAP-PROC-19)
    for sx in (-1, 1):  # finished end panels to the floor
        _bb(wood, (T, D / 2 - 0.02 - yd, zt), (sx * (W / 2 - T / 2), (yd + D / 2 - 0.02) / 2, zt / 2), d, 0.001, 0.001)
    yc = yd + T
    add_box(car, (W - 2 * T, D / 2 - 0.02 - yc, zt - kick), (0, (yc + D / 2 - 0.02) / 2, kick + (zt - kick) / 2))
    add_box(P("Kick", "Kick_GAP"), (W - 2 * T, 0.012, kick), (0, yd + rec + 0.006, kick / 2))  # TI: 4 in toe base, 2 in recess
    n = max(1, round(W / k["door_w_m"]))
    dw, g, hd = (W - 2 * T) / n, 0.003, k["drawer_h_m"]
    pulls = P("Pulls", "Pull_Black")
    for i in range(n):
        x = -W / 2 + T + (i + 0.5) * dw
        z1 = zt - g
        zd = z1 - hd
        if d <= 1:
            _bb(wood, (dw - g, T, hd), (x, yd + T / 2, zd + hd / 2), d, 0.002, 0.0015)  # drawer front
            _bb(wood, (dw - g, T, zd - g - kick - 0.002), (x, yd + T / 2, (kick + 0.002 + zd - g) / 2), d, 0.002, 0.0015)  # door
            add_handle_pull(pulls, (x, yd, zd + hd / 2), 0.128, hs - 0.005, 0.005, 8, axis="x", bend_steps=2 if d == 0 else 1)
            px = x + (dw / 2 - 0.04) * (1 if i % 2 == 0 else -1)
            add_handle_pull(pulls, (px, yd, zd - g - 0.1), 0.128, hs - 0.005, 0.005, 8, axis="z", bend_steps=2 if d == 0 else 1)
        else:
            add_box(wood, (dw - g, T, zt - kick), (x, yd + T / 2, kick + (zt - kick) / 2))
    return {"collision_boxes": coll}


def uppers(P, p, d, s, W, D, H):
    k = p["counter"]
    hs, T = k["pull_standoff_m"], 0.019
    yd = -D / 2 + hs
    wood = P("Carcass", "Light_Wood")
    if d >= 3:
        add_box(wood, (W, D, H), (0, 0, H / 2))
        return {}
    for sx in (-1, 1):
        _bb(wood, (T, D - hs, H), (sx * (W / 2 - T / 2), (yd + D / 2) / 2, H / 2), d, 0.001, 0.001)
    add_box(P("Interior", "Black_Interior"), (W - 2 * T, D / 2 - yd - T, H - 0.004), (0, (yd + T + D / 2) / 2, H / 2))
    n = max(1, round((W - 2 * T) / k["door_w_m"]))
    dw, g = (W - 2 * T) / n, 0.003
    moving = []
    pulls = P("Pulls", "Pull_Black")
    for i in range(n):
        x = -W / 2 + T + (i + 0.5) * dw
        _bb(P(f"Door_{i}", "Light_Wood"), (dw - g, T, H - 2 * g), (x, yd + T / 2, H / 2), d, 0.002, 0.0015)
        side = "left" if i % 2 == 0 else "right"
        px = x + (dw / 2 - 0.035) * (1 if side == "left" else -1)
        if d <= 2:
            add_handle_pull(pulls, (px, yd, 0.11), 0.128, hs - 0.005, 0.005, 8, axis="z", bend_steps=2 if d == 0 else (1 if d == 1 else 0))
        moving.append(hinge_axis(f"Door_{i}", x - dw / 2 if side == "left" else x + dw / 2, yd + T / 2, 0, H, side))
    return {"moving_parts": moving}


def _deck_half(bm, X0, X1, Y0, Y1, hole, ztop, zbot, xm):
    """Sink deck around one bowl: planar annuli (top up, bottom down) from the half-rectangle to the bowl ring,
    plus the outer edge strip. hole = (ring_top, ring_bottom) rounded-rect rings (seg even), xm = shared seam x."""
    ring, ringb = hole
    seg = len(ring) // 4 - 1

    def proj(i, pt):
        j, m = divmod(i, seg + 1)
        x, y = pt
        corner = ((X1, Y1), (X0, Y1), (X0, Y0), (X1, Y0))[j]
        if 2 * m == seg:
            return corner
        first = m < seg / 2
        vertical_edge = (j in (0, 2)) == first  # TR/BL start on a vertical edge, TL/BR on a horizontal one
        return (corner[0], y) if vertical_edge else (x, corner[1])

    out = [proj(i, pt) for i, pt in enumerate(ring)]
    outb = [proj(i, pt) for i, pt in enumerate(ringb)]
    n = len(ring)
    vt = [bm.verts.new((x, y, ztop)) for x, y in out]
    vh = [bm.verts.new((x, y, ztop)) for x, y in ring]
    vb = [bm.verts.new((x, y, zbot)) for x, y in outb]
    vhb = [bm.verts.new((x, y, zbot)) for x, y in ringb]
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([vt[i], vt[j], vh[j], vh[i]])
        bm.faces.new([vb[j], vb[i], vhb[i], vhb[j]])
        if (out[i] != out[j]) and not (abs(out[i][0] - xm) < 1e-9 and abs(out[j][0] - xm) < 1e-9):
            bm.faces.new([vb[i], vb[j], vt[j], vt[i]])


def _ring_faces(bm, rings, outward):
    """Open loft between equal rings (lists of 3D points); outward=True when rings go bottom -> top for an outside skin."""
    vs = [[bm.verts.new(p) for p in r] for r in rings]
    n = len(rings[0])
    for a, b in zip(vs, vs[1:]):
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new([a[i], a[j], b[j], b[i]] if outward else [a[j], a[i], b[i], b[j]])
    return vs


def double_sink(P, p, d, s, W, D, H):
    k = p["sink"]
    bd, rim, fh = k["bowl_depth_m"], k["rim_t_m"], k["faucet_h_m"]
    Hr = bd + rim
    st = P("Sink", "Stainless")
    fc = P("Faucet", "Chrome")
    yfc = D / 2 - 0.045
    if d >= 3:
        add_box(st, (W, D, Hr), (0, 0, Hr / 2))
        add_box(fc, (0.04, 0.04, fh), (0, yfc, Hr + fh / 2))
        return {}
    bw, bdp = (W - 0.12) / 2, D - 0.14
    cy = -0.02
    if d == 2:
        add_box(st, (W, D, rim), (0, 0, Hr - rim / 2))
        for sx in (-1, 1):
            add_box(st, (bw, bdp, bd), (sx * (bw / 2 + 0.02), cy, bd / 2))
        add_box(fc, (0.03, 0.03, fh), (0, yfc, Hr + fh / 2))
        return {}
    seg = 4 if d == 0 else 2
    t, zf = 0.0015, 0.006
    for sx in (-1, 1):
        cx = sx * (bw / 2 + 0.02)

        def rr(w, dp, r):
            return [(cx + x, cy + y) for x, y in rounded_rect(w, dp, r, seg)]

        top = rr(bw, bdp, 0.035)
        topb = rr(bw + 2 * t, bdp + 2 * t, 0.035 + t)
        X0, X1 = (-W / 2, 0.0) if sx < 0 else (0.0, W / 2)
        _deck_half(st, X0, X1, -D / 2, D / 2, (top, topb), Hr, Hr - rim, 0.0)
        r2, r3 = rr(bw - 0.016, bdp - 0.016, 0.03), rr(bw - 0.04, bdp - 0.04, 0.022)
        drain = [(cx + 0.045 * math.cos(math.atan2(y - cy, x - cx)), cy + 0.045 * math.sin(math.atan2(y - cy, x - cx))) for x, y in r3]
        _ring_faces(st, [[(x, y, Hr) for x, y in top], [(x, y, Hr - rim - 0.004) for x, y in top], [(x, y, zf + 0.02) for x, y in r2],
                         [(x, y, zf) for x, y in r3], [(x, y, zf - 0.002) for x, y in drain]], outward=False)  # inner skin
        b0 = rr(bw - 0.04 + 2 * t, bdp - 0.04 + 2 * t, 0.022 + t)
        b1 = rr(bw - 0.016 + 2 * t, bdp - 0.016 + 2 * t, 0.03 + t)
        vs = _ring_faces(st, [[(x, y, 0.0) for x, y in b0], [(x, y, zf + 0.02) for x, y in b1], [(x, y, Hr - rim) for x, y in topb]],
                         outward=True)  # outer skin (sheet thickness)
        st.faces.new(vs[0][::-1])
        prof = [(0, 0.001), (0.03, 0.001), (0.03, zf - 0.0015), (0.05, zf - 0.0015), (0.05, zf + 0.0005), (0.047, zf + 0.002),
                (0.04, zf + 0.002), (0.036, zf - 0.001), (0, zf - 0.001)]
        add_lathe(st, (cx, cy, 0), (0, 0, 1), prof, s)  # strainer basket
        if d == 0:
            for a in (0, 90):
                ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                add_box(st, (0.066 * ca + 0.004 * sa, 0.066 * sa + 0.004 * ca, 0.002), (cx, cy, zf))
    # chrome pull-down gooseneck at the back centre (BAND_03)
    add_lathe(fc, (0, yfc, Hr), (0, 0, 1), [(0, 0), (0.03, 0), (0.03, 0.004), (0.026, 0.008), (0, 0.008)], s)
    add_lathe(fc, (0, yfc, Hr), (0, 0, 1), [(0, 0.008), (0.021, 0.008), (0.021, 0.15), (0.016, 0.168), (0.012, 0.175), (0, 0.175)], s)
    r = 0.011
    zt = Hr + fh - r  # flat top run: the fillets stay below it, so the top bound is exact
    add_tube(fc, [(0, yfc, Hr + 0.17), (0, yfc, zt), (0, yfc - 0.2, zt), (0, yfc - 0.2, zt - 0.09)], r, s if d == 0 else 8,
             bend_radius=0.06, bend_steps=6 if d == 0 else 2)
    add_lathe(fc, (0, yfc - 0.2, zt - 0.09), (0, 0, -1), [(0, 0.0), (0.013, 0.0), (0.015, 0.01), (0.016, 0.055), (0.013, 0.07), (0, 0.07)], s)
    add_cylinder_between(fc, (0.02, yfc, Hr + 0.11), (0.075, yfc, Hr + 0.13), 0.0055, 8)  # lever
    if d == 0:
        _bb(fc, (0.03, 0.012, 0.004), (0.085, yfc, Hr + 0.133), d, 0.004, 0.0015)
    return {}


def appliance(P, p, d, s, W, D, H):
    a = p["appliance"]
    b = P("Body", "Black_Appliance")
    coll = [collision_box("Body", (0, 0, H / 2), (W, D, H))]
    if d >= 3:
        add_box(b, (W, D, H), (0, 0, H / 2))
        return {"collision_boxes": coll}
    trim, glass = P("Trim", "Appliance_Trim"), P("Glass", "Appliance_Glass")
    if a["type"] == "microwave":
        fz, fd = 0.01, 0.02  # feet, fascia depth
        _bb(b, (W - 0.004, D - fd, H - fz - 0.002), (0, -D / 2 + fd + (D - fd) / 2, fz + (H - fz - 0.002) / 2), d, 0.012, 0.004)  # wrapper
        dwid = W * 0.73
        door = P("Door", "Black_Appliance")
        _bb(door, (dwid - 0.0015, fd - 0.004, H - fz), (-W / 2 + (dwid - 0.0015) / 2, -D / 2 + 0.004 + (fd - 0.004) / 2, fz + (H - fz) / 2),
            d, 0.006, 0.002)
        px0 = -W / 2 + dwid + 0.0015
        _bb(b, (W / 2 - px0, fd - 0.002, H - fz), ((px0 + W / 2) / 2, -D / 2 + 0.002 + (fd - 0.002) / 2, fz + (H - fz) / 2), d, 0.006, 0.002)
        if d <= 1:  # door border proud of the window
            _frame(door, dwid - 0.0015, H - fz, _moulding(0.04, -D / 2, -D / 2 + 0.006, 0.004, 3 if d == 0 else 1), z0=fz,
                   cx=-W / 2 + (dwid - 0.0015) / 2)
        add_box(glass, (dwid - 0.085, 0.002, H - fz - 0.085), (-W / 2 + (dwid - 0.0015) / 2, -D / 2 + 0.0035, fz + (H - fz) / 2))
        pw = W / 2 - px0
        pcx = (px0 + W / 2) / 2
        add_box(glass, (pw * 0.7, 0.002, 0.03), (pcx, -D / 2 + 0.001, H - 0.045))  # display
        if d <= 1:
            for rr_ in range(4):  # keypad 3 x 4 with gaps
                for cc in range(3):
                    _bb(trim, (pw * 0.2, 0.0015, 0.012), (pcx + (cc - 1) * pw * 0.26, -D / 2 + 0.00125, H - 0.085 - rr_ * 0.02), d, 0.002, 0.0005)
            for i, zb in enumerate((H - 0.18, H - 0.205)):  # start / stop
                _bb(trim, (pw * 0.72, 0.0015, 0.016), (pcx, -D / 2 + 0.00125, zb), d, 0.003, 0.0005)
            _bb(trim, (pw * 0.72, 0.002, 0.03), (pcx, -D / 2 + 0.001, fz + 0.03), d, 0.004, 0.0008)  # door-open button
            nv = 9 if d == 0 else 5
            for i in range(nv):  # side vent ribs on the wrapper
                z = fz + 0.07 + i * (H - fz - 0.12) / (nv - 1)
                for sx in (-1, 1):
                    add_box(trim, (0.0015, 0.12, 0.004), (sx * (W / 2 - 0.002 - 0.00075 + 0.0015), D / 2 - 0.1, z))
        for sx in (-1, 1):
            for sy in (-1, 1):
                add_cylinder_between(trim, (sx * (W / 2 - 0.04), sy * (D / 2 - 0.05), 0), (sx * (W / 2 - 0.04), sy * (D / 2 - 0.05), fz), 0.012, 8)
    else:  # pod coffee maker
        zb = 0.035
        _bb(b, (W, D - 0.004, zb), (0, 0.002, zb / 2), d, 0.014, 0.005)  # base
        yt0, yt1 = -D / 2 + D * 0.38, D / 2 - 0.07
        _bb(b, (W, yt1 - yt0, H - zb - 0.005), (0, (yt0 + yt1) / 2, zb + (H - zb - 0.005) / 2), d, 0.03, 0.006)  # tower
        hz0 = H - 0.075
        hf = 0.004 if d <= 1 else 0.0  # LOD0/1: the buttons reach the front plane
        _bb(b, (W, D * 0.55, H - 0.02 - hz0), (0, -D / 2 + hf + D * 0.275, (hz0 + H - 0.02) / 2), d, 0.025, 0.006)  # head
        _bb(P("Lid", "Black_Appliance"), (W - 0.004, D * 0.5, 0.0195), (0, -D / 2 + 0.006 + D * 0.25, H - 0.00975), d, 0.022, 0.006)
        add_lathe(trim, (0, -D / 2 + 0.06, hz0), (0, 0, -1), [(0, 0), (0.014, 0), (0.012, 0.012), (0.007, 0.018), (0, 0.018)], s)  # spout
        _bb(trim, (W * 0.78, D * 0.3, 0.012), (0, -D / 2 + 0.01 + D * 0.15, zb + 0.006), d, 0.008, 0.003)  # drip tray
        if d <= 1:
            for i in range(5 if d == 0 else 3):  # drip grate slats
                add_box(trim, (W * 0.7, 0.004, 0.003), (0, -D / 2 + 0.025 + i * D * 0.25 / (4 if d == 0 else 2), zb + 0.0135))
            for i in range(3):  # brew buttons on the head front
                add_lathe(trim, (-0.04 + i * 0.04, -D / 2 + 0.004, hz0 + 0.03), (0, -1, 0), [(0, 0), (0.008, 0), (0.0075, 0.003), (0, 0.004)], 8)
        yr0 = D / 2 - 0.07  # water reservoir at the back + lid
        _bb(glass, (W - 0.02, D / 2 - yr0, H - 0.03 - zb), (0, (yr0 + D / 2) / 2, zb + (H - 0.03 - zb) / 2), d, 0.012, 0.003)
        _bb(b, (W - 0.016, D / 2 - yr0 + 0.0, 0.016), (0, (yr0 + D / 2) / 2, H - 0.03 + 0.008), d, 0.012, 0.004)
    return {"collision_boxes": coll}


def mini_hoop(P, p, d, s, W, D, H):
    h = p["hoop"]
    fr, bb = P("Frame", "Hoop_Frame_GAP"), P("Backboard", "Backboard_GAP")
    hb = P("Hamper", "Hamper_GAP")
    Hh, bh, rr_, br = h["hamper_h_m"], h["board_h_m"], h["rim_r_m"], h["ball_r_m"]
    coll = [collision_box("Body", (0, 0, H / 2), (W, D, H))]
    if d >= 3:
        add_box(hb, (W, D, Hh), (0, 0, Hh / 2))
        add_box(bb, (W, 0.03, bh), (0, D / 2 - 0.015, H - bh / 2))
        return {"collision_boxes": coll}
    wr = 0.006
    segw = 8 if d <= 1 else 6
    for sx in (-1, 1):  # wire hamper frame
        for sy in (-1, 1):
            add_cylinder_between(fr, (sx * (W / 2 - wr), sy * (D / 2 - wr), 0), (sx * (W / 2 - wr), sy * (D / 2 - wr), Hh), wr, segw)
    if d <= 1:
        for z in (wr, Hh - wr):
            add_tube(fr, [(x, y, z) for x, y in rounded_rect(W - 2 * wr, D - 2 * wr, 0.02, 2)], wr * 0.8, segw, closed=True)
    m = 0.012  # fabric bag, inset
    for size, c in (((W - 2 * m, 0.003, Hh - 0.03), (0, -D / 2 + m, Hh / 2)), ((W - 2 * m, 0.003, Hh - 0.03), (0, D / 2 - m, Hh / 2)),
                    ((0.003, D - 2 * m, Hh - 0.03), (-W / 2 + m, 0, Hh / 2)), ((0.003, D - 2 * m, Hh - 0.03), (W / 2 - m, 0, Hh / 2)),
                    ((W - 2 * m, D - 2 * m, 0.003), (0, 0, 0.02))):
        add_box(hb, size, c)
    yb = D / 2 - 0.012
    for sx in (-1, 1):  # uprights behind the backboard
        add_cylinder_between(fr, (sx * W * 0.3, D / 2 - 0.022, 0), (sx * W * 0.3, D / 2 - 0.022, H - 0.03), 0.01, segw)
    _bb(bb, (W, 0.012, bh), (0, yb + 0.006, H - bh / 2), d, 0.03, 0.004)
    zr = H - bh + 0.07
    ycr = yb - 0.03 - rr_
    rim = P("Rim", "Rim_White")
    _bb(rim, (0.08, 0.03, 0.05), (0, yb - 0.015, zr - 0.01), d, 0.004, 0.002)  # rim bracket
    nr = 24 if d == 0 else 16
    add_tube(rim, [(rr_ * math.cos(2 * math.pi * i / nr), ycr + rr_ * math.sin(2 * math.pi * i / nr), zr) for i in range(nr)], 0.006, segw, closed=True)
    net = P("Net", "Net_GAP")
    if d <= 1:
        rings = [(rr_, zr), (rr_ * 0.9, zr - 0.06), (rr_ * 0.78, zr - 0.12), (rr_ * 0.68, zr - 0.18)]
        ns = 12 if d == 0 else 8
        for i in range(ns):
            for sgn in (1, -1):  # diamond mesh: zig-zag strands
                path = []
                for j, (rad, z) in enumerate(rings):
                    a = 2 * math.pi * (i + (0.5 * sgn if j % 2 else 0)) / ns
                    path.append((rad * math.cos(a), ycr + rad * math.sin(a), z))
                add_tube(net, path, 0.0016, 6)
        add_tube(net, [(rings[-1][0] * math.cos(2 * math.pi * i / nr), ycr + rings[-1][0] * math.sin(2 * math.pi * i / nr), rings[-1][1])
                       for i in range(nr)], 0.002, 6, closed=True)
    else:
        add_lathe(net, (0, ycr, 0), (0, 0, 1), [(rr_ * 0.95, zr), (rr_ * 0.68, zr - 0.18)], 8)
    zc = Hh + br - 0.04  # ball resting in the hamper mouth
    nb = s if d <= 1 else 8
    prof = [(0, -br)] + [(br * math.cos(math.radians(a)), br * math.sin(math.radians(a))) for a in range(-75, 90, 15 if d == 0 else 30)] + [(0, br)]
    add_lathe(P("Ball", "Ball_Orange"), (0, 0, zc), (0, 0, 1), prof, nb)
    if d == 0:
        seam = P("BallSeams", "Hoop_Frame_GAP")
        add_tube(seam, [(br * 1.003 * math.cos(2 * math.pi * i / 24), 0, zc + br * 1.003 * math.sin(2 * math.pi * i / 24)) for i in range(24)],
                 0.0015, 6, closed=True)
        add_tube(seam, [(0, br * 1.003 * math.cos(2 * math.pi * i / 24), zc + br * 1.003 * math.sin(2 * math.pi * i / 24)) for i in range(24)],
                 0.0015, 6, closed=True)
        add_tube(seam, [(br * 1.003 * math.cos(2 * math.pi * i / 24), br * 1.003 * math.sin(2 * math.pi * i / 24), zc) for i in range(24)],
                 0.0015, 6, closed=True)
    return {"collision_boxes": coll}


def coat_hooks(P, p, d, s, W, D, H):
    rail = P("Rail", "Hook_Rail_GAP")
    hk = P("Hooks", "Hook_Metal_GAP")
    if d >= 3:
        add_box(rail, (W, D, H), (0, 0, H / 2))
        return {}
    _bb(rail, (W, 0.02, H), (0, D / 2 - 0.01, H / 2), d, 0.004, 0.004 if d == 0 else 0.002)
    for sx in (-1, 1):
        _screw(hk, (sx * (W / 2 - 0.03), D / 2 - 0.02, H / 2), (0, -1, 0), 0.004, d)
    n = p["hooks"]
    yb = D / 2 - 0.02
    for i in range(n):  # cast double-prong hooks on a base plate
        x = -W / 2 + (i + 0.5) * W / n
        _bb(hk, (0.022, 0.004, 0.06), (x, yb - 0.002, H * 0.5), d, 0.006, 0.0015)
        for dz in (-0.018, 0.018):
            _screw(hk, (x, yb - 0.004, H * 0.5 + dz), (0, -1, 0), 0.0025, d)
        bs = 3 if d == 0 else (1 if d == 1 else 0)
        br_ = 0.02 if d <= 1 else 0
        add_tube(hk, [(x, yb - 0.004, H * 0.42), (x, -D / 2 + 0.007, H * 0.3), (x, -D / 2 + 0.007, H * 0.5)], 0.005, 8,
                 bend_radius=br_, bend_steps=bs)
        add_tube(hk, [(x, yb - 0.004, H * 0.6), (x, -D / 2 + 0.03, H * 0.72), (x, -D / 2 + 0.03, H * 0.82)], 0.004, 8,
                 bend_radius=br_ * 0.6, bend_steps=bs)
        for (yy, zz, rad) in ((-D / 2 + 0.007, H * 0.5, 0.007), (-D / 2 + 0.03, H * 0.82, 0.0055)):  # ball tips
            add_lathe(hk, (x, yy, zz - rad), (0, 0, 1), [(0, 0), (rad * 0.7, rad * 0.3), (rad, rad), (rad * 0.7, rad * 1.7), (0, 2 * rad)], 8)
    return {}


KINDS = {"lockers": lockers, "bench": bench, "board": board, "table": table, "first_aid": first_aid, "base_cabinets": base_cabinets,
         "uppers": uppers, "double_sink": double_sink, "appliance": appliance, "mini_hoop": mini_hoop, "coat_hooks": coat_hooks}


def build(p, lod):
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"], W, D, H)
    Ht = H + p.get("extra_h_m", 0.0)
    extra = dict(extra, fixture_family="break_room", rf=p["rf"], seed=int(p["seed"]))
    extra.update(wear(p))
    return P.finish(), (W, Ht, D), extra
