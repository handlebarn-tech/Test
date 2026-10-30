"""Office + back-room furniture (PROC-005 §8; IMP-003 drop 3; PROC-005 fix wave). One asset per ROOM_FIXTURES row (sizes
[w, d, h] = the RF size_ft): tall black cabinets (closed steel box, single inset front, no hardware, DEC-051 Q9), the
under-desk black file-cabinet run, standing desk, desk arm / corner piece (black laminate), ex-register-1 desk (white
top), stainless worktable on folding legs (no undershelf: RF + wall2_R3C3, GAP-PROC-33), mesh task chair, stainless deli
prep cart (DEC-079, RI 2.4) and the black wire basket cart. Every colour/size/count is cited in the params `_sources` /
`_src` maps; part sizes are GAP-PROC-18, unsourced finishes GAP-PROC-31, unsourced counts/hardware types GAP-PROC-32.
Origin = bottom centre, front = -Y. LOD0 full construction; LOD1 drops micro detail (screws, slides, louvres, knobs);
LOD2 plain parts; LOD3 blocks."""
import math

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_handle_pull, add_lathe, add_screw_head,
                     add_sweep, add_tube, add_wire_grid, collision_box, even_positions, loft, rounded_rect, slide_axis, wear)


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


# --- local helpers ----------------------------------------------------------------------------------------------------

def _bb(bm, size, center, d, corner=0.003, bevel=0.0015):
    """Bevelled box at LOD0/1 (3 / 1 corner segments so the Wear attribute and highlights catch), plain box after."""
    if d >= 2:
        add_box(bm, size, center)
    else:
        add_beveled_box(bm, size, center, corner=corner, bevel=bevel, seg=3 if d == 0 else 1)


def _screw(bm, d, c, axis, r=0.004):
    if d == 0:
        add_screw_head(bm, c, axis, r, 8)


def _body(W, D, H):
    return [collision_box("Body", (0, 0, H / 2), (W, D, H))]


def _leveller(bm, x, y, h, r, s):
    """Glide foot: pad, chamfered nut, threaded stem up to z = h."""
    add_lathe(bm, (x, y, 0), (0, 0, 1), [(0, 0), (r, 0), (r, h * 0.25), (r * 0.8, h * 0.4), (r * 0.42, h * 0.45),
                                         (r * 0.42, h * 0.62), (r * 0.3, h * 0.66), (r * 0.3, h), (0, h)], s)


def _caster(P, mat_f, mat_w, x, y, sx, ct, d, s):
    """Plate-mount swivel caster whose top plate is at z = ct: plate + screws, swivel race, fork, wheel (rolls along X,
    swivel offset toward the cart centre so the tyre stays inside the footprint), axle bolt."""
    f, w = P("Casters", mat_f), P("Wheels", mat_w)
    r = min(0.04, (ct - 0.02) / 2)
    off = 0.012 * -sx
    _bb(f, (0.06, 0.06, 0.004), (x, y, ct - 0.002), d, 0.006, 0.001)
    if d == 0:
        for a in (-1, 1):
            for b in (-1, 1):
                _screw(f, d, (x + a * 0.022, y + b * 0.022, ct), (0, 0, -1), 0.003)  # bolts seen from below
    add_lathe(f, (x, y, ct - 0.004), (0, 0, -1), [(0, 0), (0.024, 0), (0.024, 0.004), (0.018, 0.008), (0, 0.008)], s)
    tw = 0.028
    zt = ct - 0.012
    if d <= 1:
        for side in (-1, 1):  # fork cheeks
            add_box(f, (0.034, 0.003, zt - r + 0.012), (x + off / 2, y + side * (tw / 2 + 0.0035), r - 0.006 + (zt - r + 0.012) / 2))
        add_box(f, (0.036, tw + 0.01, 0.004), (x + off / 2, y, zt - 0.002))  # fork crown
        add_cylinder_between(f, (x + off, y - tw / 2 - 0.007, r), (x + off, y + tw / 2 + 0.007, r), 0.004, 8)
    else:
        add_box(f, (0.03, tw + 0.01, zt - r), (x + off / 2, y, r + (zt - r) / 2))
    prof = [(0, 0), (r * 0.55, 0), (r * 0.62, tw * 0.12), (r * 0.92, tw * 0.15), (r, tw * 0.32), (r, tw * 0.68),
            (r * 0.92, tw * 0.85), (r * 0.62, tw * 0.88), (r * 0.55, tw), (0, tw)] if d <= 1 else [(0, 0), (r, 0), (r, tw), (0, tw)]
    add_lathe(w, (x + off, y - tw / 2, r), (0, 1, 0), prof, s)


def _laminate_top(P, k, d, W, D, H, tt, grommets=()):
    """Laminate top on a particleboard core with real thickness, 1.5 mm PVC edge banding on all four edges and cable
    grommets (flange top = H; the laminate sits 1.2 mm lower so the flange reads as an insert)."""
    zt = H - tt
    top = P("Top", k["top"])
    if d >= 2:
        add_box(top, (W, D, tt), (0, 0, zt + tt / 2))
        return zt
    band, sink = 0.0015, 0.0012 if grommets else 0.0
    h = tt - sink
    _bb(top, (W - 2 * band, D - 2 * band, h), (0, 0, zt + h / 2), d, 0.002, 0.0008)
    eb = P("EdgeBand", k["edge"])
    for y in (-1, 1):
        _bb(eb, (W, band, h), (0, y * (D / 2 - band / 2), zt + h / 2), d, 0.0007, 0.0005)
    for x in (-1, 1):
        _bb(eb, (band, D - 2 * band, h), (x * (W / 2 - band / 2), 0, zt + h / 2), d, 0.0005, 0.0005)
    g = P("Grommets", "Plastic_Grey")
    for gx, gy in grommets:
        add_lathe(g, (gx, gy, H - sink - 0.0002), (0, 0, 1), [(0, 0), (0.034, 0), (0.034, 0.0006), (0.031, sink + 0.0002),
                                                              (0.027, sink + 0.0002), (0.026, sink * 0.4), (0, sink * 0.4)], 24 if d == 0 else 12)
        add_box(g, (0.026, 0.006, sink * 0.6), (gx, gy, H - sink - 0.0002 + sink * 0.4 + sink * 0.3))  # cable-slot cap tab
    return zt


# --- kinds ------------------------------------------------------------------------------------------------------------

def tall_cabinet(P, p, d, s, W, D, H):
    """Steel storage cabinet: recessed toe kick on levellers, carcass with louvred sides, face frame, one inset front
    panel with a 3 mm reveal (no handle, lock or hinge shown: DEC-051 Q9), top cap with a hemmed front edge."""
    c = p["cabinet"]
    b = P("Body", c["finish"])
    if d >= 3:
        add_box(b, (W, D, H), (0, 0, H / 2))
        return {"collision_boxes": _body(W, D, H)}
    kz, lv, sh, ff = c["kick_h_m"], 0.012 if d <= 1 else 0.0, 0.003, c["face_frame_m"]
    k = P("Kick", c["finish"])
    _bb(k, (W - 0.02, D - 0.06, kz - lv), (0, 0.02, lv + (kz - lv) / 2), d, 0.002, 0.001)
    if d <= 1:
        for x in (-1, 1):
            for y in (-D / 2 + 0.09, D / 2 - 0.05):
                _leveller(P("Levellers", "Plastic_Grey"), x * (W / 2 - 0.05), y, lv, 0.016, s)
    zc = kz
    hc = H - 0.014 - zc
    _bb(b, (W - 2 * sh, D - 0.012, hc), (0, 0.006, zc + hc / 2), d, 0.004, 0.0015)  # carcass behind the face frame
    _bb(b, (W - 2 * sh, D - 0.004, 0.014), (0, 0.002, H - 0.007), d, 0.004, 0.003)  # top cap
    if d <= 1:  # rolled hem on the top cap front edge
        add_cylinder_between(b, (-W / 2 + sh + 0.004, -D / 2 + 0.006, H - 0.006), (W / 2 - sh - 0.004, -D / 2 + 0.006, H - 0.006), 0.004, s)
    fz0, fz1 = zc, H - 0.014
    fy = -D / 2 + 0.006
    fr = P("FaceFrame", c["finish"])
    for x in (-1, 1):  # stiles reach the outer width
        _bb(fr, (ff, 0.012, fz1 - fz0), (x * (W / 2 - ff / 2), fy, (fz0 + fz1) / 2), d, 0.002, 0.0012)
    for z, hh in ((fz0, 0.04), (fz1 - 0.04, 0.04)):
        _bb(fr, (W - 2 * ff, 0.012, hh), (0, fy, z + hh / 2), d, 0.001, 0.0012)
    rv = 0.003
    pw, ph = W - 2 * ff - 2 * rv, fz1 - fz0 - 0.08 - 2 * rv
    _bb(P("Front", c["finish"]), (pw, 0.016, ph), (0, -D / 2 + 0.002 + 0.008, fz0 + 0.04 + rv + ph / 2), d, 0.003, 0.002)
    if d == 0:  # pressed stiffener field on the front panel
        _bb(P("Front", c["finish"]), (pw - 0.12, 0.002, ph - 0.16), (0, -D / 2 + 0.0015, fz0 + 0.04 + rv + ph / 2), d, 0.01, 0.0009)
        for x in (-1, 1):  # side louvres, upper and lower bank
            for z0 in (H - 0.32, kz + 0.12):
                for i in range(6):
                    _bb(b, (0.003, 0.14, 0.008), (x * (W / 2 - 0.0015), 0.06, z0 + i * 0.03), d, 0.001, 0.001)
        for x in (-1, 1):  # back-panel screws
            for z in (kz + 0.05, (kz + H) / 2, H - 0.06):
                _screw(b, d, (x * (W / 2 - 0.04), D / 2 - 0.0021, z), (0, 1, 0), 0.0045)  # head stays inside D
        for x in (-1, 1):  # toe-kick fixings
            _screw(k, d, (x * (W / 2 - 0.05), -D / 2 + 0.05, kz * 0.55), (0, -1, 0), 0.0045)
    return {"collision_boxes": _body(W, D, H)}


def file_cabinets(P, p, d, s, W, D, H):
    """Run of steel file cabinets: per unit a carcass (sides, top with hemmed front edge, recessed kick, back), drawer
    fronts with 4 mm gaps, bar pulls, label holders, a lock cylinder on the top drawer, drawer boxes on telescoping
    slides (visible when a drawer is opened in game)."""
    f = p["files"]
    n, nd, hs, hr, kz = f["count"], f["drawers_per_unit"], f["pull_standoff_m"], f["pull_r_m"], f["kick_h_m"]
    yf = -D / 2 + hs + hr  # drawer-front face: the pull grips reach the front bound
    ft = 0.018
    cw = W / n
    fin = f["finish"]
    b = P("Body", fin)
    if d >= 3:
        add_box(b, (W, D - hs - hr, H), (0, (yf + D / 2) / 2, H / 2))
        add_box(P("Pulls", "Hardware_Grey"), (W * 0.6, hs + hr, 0.02), (0, -D / 2 + (hs + hr) / 2, H * 0.7))
        return {"collision_boxes": _body(W, D, H)}
    moving = []
    yc = yf + ft  # carcass front plane (behind the fronts)
    dc = D / 2 - yc
    for i in range(n):
        x = -W / 2 + (i + 0.5) * cw
        u = cw  # neighbouring units butt; the bevelled sheet edges read as the seam
        for sx in (-1, 1):  # side sheets
            _bb(b, (0.012, dc, H - 0.014), (x + sx * (u / 2 - 0.006), yc + dc / 2, (H - 0.014) / 2), d, 0.002, 0.001)
        _bb(b, (u, D / 2 - yf, 0.014), (x, (yf + D / 2) / 2, H - 0.007), d, 0.003, 0.002)  # top over the fronts
        if d <= 1:
            add_cylinder_between(b, (x - u / 2 + 0.004, yf + 0.004, H - 0.006), (x + u / 2 - 0.004, yf + 0.004, H - 0.006), 0.004, s)
        add_box(b, (u - 0.024, 0.006, H - 0.014), (x, D / 2 - 0.003, (H - 0.014) / 2))  # back
        _bb(b, (u - 0.024, dc - 0.03, kz), (x, yc + 0.03 + (dc - 0.03) / 2, kz / 2), d, 0.002, 0.001)  # recessed kick
        dh = (H - 0.014 - kz - 0.004 * (nd + 1)) / nd
        for kk in range(nd):
            z0 = kz + 0.004 + kk * (dh + 0.004)
            zc = z0 + dh / 2
            name = f"Drawer_{i}_{kk}"
            dr = P(name, fin)
            _bb(dr, (u - 0.006, ft, dh), (x, yf + ft / 2, zc), d, 0.003, 0.0025)
            add_handle_pull(P(name, "Hardware_Grey"), (x, yf, z0 + dh * 0.72), cw * 0.4, hs, hr, s if d == 0 else 8, axis="x",
                            bend_steps=3 if d == 0 else 1)
            if d <= 1:  # label-holder frame + card
                hz = z0 + dh * 0.45
                hw = P(name, "Hardware_Grey")
                for zz in (hz - 0.016, hz + 0.016):
                    add_box(hw, (0.08, 0.003, 0.004), (x, yf - 0.0015, zz))
                for xx in (x - 0.038, x + 0.038):
                    add_box(hw, (0.004, 0.003, 0.036), (xx, yf - 0.0015, hz))
                add_box(P(name, "Label_Grey"), (0.072, 0.001, 0.028), (x, yf - 0.0005, hz))
            if d <= 1:  # drawer box behind the front + inner slide members
                bd = D * 0.72
                y0 = yf + ft
                for sx in (-1, 1):
                    add_box(dr, (0.01, bd, dh - 0.05), (x + sx * (u / 2 - 0.035), y0 + bd / 2, z0 + 0.02 + (dh - 0.05) / 2))
                    if d == 0:
                        add_box(dr, (0.006, bd - 0.02, 0.03), (x + sx * (u / 2 - 0.027), y0 + bd / 2, zc))
                        add_box(b, (0.006, dc - 0.03, 0.036), (x + sx * (u / 2 - 0.0185), yc + (dc - 0.03) / 2 + 0.01, zc))  # outer member
                add_box(dr, (u - 0.08, 0.01, dh - 0.05), (x, y0 + bd - 0.005, z0 + 0.02 + (dh - 0.05) / 2))
                add_box(dr, (u - 0.08, bd, 0.006), (x, y0 + bd / 2, z0 + 0.023))
            if kk == nd - 1 and d <= 1:  # lock cylinder, top drawer, upper right
                lx, lz = x + u / 2 - 0.04, z0 + dh - 0.03
                add_lathe(P(name, "Hardware_Grey"), (lx, yf, lz), (0, -1, 0), [(0, 0), (0.011, 0), (0.011, 0.002), (0.0095, 0.0035), (0, 0.0035)], s)
                if d == 0:
                    add_box(P(name, "File_Black"), (0.0016, 0.0006, 0.008), (lx, yf - 0.0037, lz))  # keyway
            moving.append(slide_axis(name, D * 0.65))
    return {"moving_parts": moving, "collision_boxes": _body(W, D, H)}


def desk(P, p, d, s, W, D, H):
    """Laminate desk: banded top with grommets on a steel four-leg frame (rect-tube legs, apron rails, corner gussets),
    levelling glides, steel modesty panel with hemmed edges on brackets."""
    k = p["desk"]
    tt, lw = k["top_t_m"], k["leg_w_m"]
    fr = P("Frame", k["frame"])
    gx, gy = W / 2 - 0.12, D / 2 - 0.08
    zt = _laminate_top(P, k, d, W, D, H, tt, [(-gx, gy), (gx, gy)] if k.get("grommets") else ())
    lx, ly = W / 2 - 0.035 - lw / 2, D / 2 - 0.045 - lw / 2
    if d >= 3:
        for sx in (-1, 1):
            add_box(fr, (lw, D - 0.09, zt), (sx * lx, 0, zt / 2))
        return {"collision_boxes": _body(W, D, H)}
    z0 = 0.014 if d <= 1 else 0.0
    ah = 0.06
    prof = rounded_rect(lw, lw, 0.004, 2 if d == 0 else 1) if d <= 1 else rounded_rect(lw, lw, 0, 0)
    for sx in (-1, 1):
        for sy in (-1, 1):
            add_sweep(fr, [(sx * lx, sy * ly, z0), (sx * lx, sy * ly, zt - ah)], prof)
            if d <= 1:
                _leveller(P("Levellers", "Plastic_Grey"), sx * lx, sy * ly, z0 + 0.002, lw * 0.45, s)
                _bb(fr, (lw + 0.004, lw + 0.004, 0.004), (sx * lx, sy * ly, z0 + 0.002), d, 0.003, 0.001)  # leg end cap
    for sy in (-1, 1):  # apron rails (front/back) and side rails
        _bb(fr, (2 * lx + lw, 0.02, ah), (0, sy * ly, zt - ah / 2), d, 0.002, 0.0012)
    for sx in (-1, 1):
        _bb(fr, (0.02, 2 * ly - lw, ah), (sx * lx, 0, zt - ah / 2), d, 0.002, 0.0012)
    if d <= 1:
        for sx in (-1, 1):
            for sy in (-1, 1):  # corner gussets + screws into the top
                cx, cy = sx * (lx - 0.06), sy * (ly - 0.06)
                add_box(fr, (0.1, 0.1, 0.004), (sx * (lx - 0.04), sy * (ly - 0.04), zt - 0.004))
                _screw(fr, d, (cx, cy, zt - 0.006), (0, 0, -1), 0.004)
                _screw(fr, d, (sx * (lx - 0.025), sy * (ly - 0.08), zt - 0.006), (0, 0, -1), 0.004)
    # modesty panel at the back (+Y), steel sheet with hemmed top/bottom edges, on brackets to the rear legs
    mz0, mz1 = zt * 0.38, zt - ah - 0.01
    my = ly - lw / 2 - 0.006
    mw = 2 * lx - lw - 0.02
    mp = P("Modesty", k["frame"])
    _bb(mp, (mw, 0.003, mz1 - mz0), (0, my, (mz0 + mz1) / 2), d, 0.002, 0.001)
    if d <= 1:
        for z in (mz0, mz1):
            add_cylinder_between(mp, (-mw / 2, my - 0.002, z), (mw / 2, my - 0.002, z), 0.004, s)
        for sx in (-1, 1):
            for z in (mz0 + 0.04, mz1 - 0.04):
                add_box(fr, (0.03, 0.012, 0.04), (sx * (mw / 2 + 0.005), my + 0.004, z))
                _screw(mp, d, (sx * (mw / 2 - 0.02), my - 0.0015, z), (0, -1, 0), 0.0045)
    return {"collision_boxes": _body(W, D, H)}


def standing_desk(P, p, d, s, W, D, H):
    """Electric standing desk: banded top with grommets, two 3-stage rectangular columns with collars, T feet with end
    caps and levellers, side brackets, telescoping crossbar, motor housing, control box with cable stubs, paddle with
    up/down keys under the front edge."""
    k = p["desk"]
    tt = k["top_t_m"]
    fr = P("Frame", k["frame"])
    zt = _laminate_top(P, k, d, W, D, H, tt, [(-(W / 2 - 0.12), D / 2 - 0.08), (W / 2 - 0.12, D / 2 - 0.08)] if k.get("grommets") else ())
    cx = W * 0.36
    if d >= 3:
        for sx in (-1, 1):
            add_box(fr, (0.08, D * 0.9, zt), (sx * cx, 0, zt / 2))
        return {"collision_boxes": _body(W, D, H)}
    seg = 3 if d == 0 else (1 if d == 1 else 0)
    fl, fh = D * 0.9, 0.045
    pl = P("Plastic", "Plastic_Grey")
    lv = 0.01 if d <= 1 else 0.0
    stages = [(0.08, 0.05, lv + fh, zt * 0.5), (0.07, 0.04, zt * 0.48, zt * 0.76), (0.06, 0.03, zt * 0.74, zt - 0.03)]
    for sx in (-1, 1):
        x = sx * cx
        _bb(fr, (0.075, fl - 0.04, fh), (x, 0, lv + fh / 2), d, 0.012, 0.006)  # foot
        if d <= 1:
            for sy in (-1, 1):
                _bb(pl, (0.075, 0.02, fh * 0.8), (x, sy * (fl / 2 - 0.01), lv + fh * 0.4), d, 0.008, 0.004)  # end caps
                _leveller(P("Levellers", "Plastic_Grey"), x, sy * (fl / 2 - 0.035), lv + 0.002, 0.014, s)
        for w, dd, a, b in stages:
            add_sweep(fr, [(x, 0, a), (x, 0, b)], rounded_rect(w, dd, 0.006 if seg else 0, seg))
            if d <= 1:  # plastic collar at the top of each stage
                add_sweep(pl, [(x, 0, b - 0.012), (x, 0, b)], rounded_rect(w + 0.004, dd + 0.004, 0.007, seg))
        _bb(fr, (0.06, D * 0.8, 0.025), (x, 0, zt - 0.0125), d, 0.004, 0.002)  # side bracket under the top
        if d <= 1:
            for y in (-D * 0.33, D * 0.33):
                _screw(fr, d, (x, y, zt - 0.025), (0, 0, -1), 0.0045)
    _bb(fr, (2 * cx - 0.06, 0.04, 0.03), (0, 0.06, zt - 0.03), d, 0.004, 0.002)  # crossbar
    if d <= 1:
        _bb(fr, (2 * cx * 0.5, 0.046, 0.036), (0, 0.06, zt - 0.03), d, 0.004, 0.002)  # telescoping sleeve
        _bb(pl, (0.1, 0.07, 0.06), (cx - 0.06, 0.0, zt - 0.06), d, 0.012, 0.005)  # motor housing
        _bb(pl, (0.16, 0.08, 0.035), (0, -0.05, zt - 0.0175), d, 0.008, 0.003)  # control box
        ctl = P("Controls", "Plastic_Grey")
        px, py = W * 0.32, -D / 2 + 0.06
        _bb(ctl, (0.11, 0.06, 0.022), (px, py, zt - 0.011), d, 0.01, 0.004)  # paddle housing
        for bx in (-0.022, 0.022):
            _bb(ctl, (0.026, 0.02, 0.004), (px + bx, py - 0.012, zt - 0.024), d, 0.004, 0.0015)  # up/down keys
        if d == 0:
            add_tube(ctl, [(px, py + 0.03, zt - 0.012), (px * 0.4, -0.05, zt - 0.02), (0.08, -0.05, zt - 0.02)], 0.003, 8)
            for sx in (-1, 1):
                add_tube(ctl, [(sx * 0.08, -0.05, zt - 0.02), (sx * (cx - 0.05), 0.0, zt - 0.04)], 0.003, 8)
    return {"collision_boxes": _body(W, D, H)}


def worktable(P, p, d, s, W, D, H):
    """Stainless worktable: sheet top with down-turned edges and rolled hems, hat-channel stiffeners, two folding leg
    frames (tube legs, cross bar, hinge plates with screws, folding brace with knuckle) on adjustable bullet feet. No
    undershelf (RF folding legs; wall2_R3C3 open frame; GAP-PROC-33)."""
    k = p["table"]
    tt = k["top_t_m"]
    top, fr = P("Top", "Stainless"), P("Frame", k["legs"])
    zt = H - tt
    lr = k["leg_r_m"]
    if d >= 3:
        add_box(top, (W, D, tt), (0, 0, zt + tt / 2))
        add_box(fr, (W - 0.2, D - 0.1, zt), (0, 0, zt / 2))
        return {"collision_boxes": _body(W, D, H)}
    sh = 0.0015
    _bb(top, (W, D, 0.004), (0, 0, H - 0.002), d, 0.008, 0.0016)  # top sheet, eased edge
    for sy in (-1, 1):  # down-turned front/back edges
        _bb(top, (W - 0.004, sh, tt - 0.004), (0, sy * (D / 2 - sh / 2 - 0.0005), zt + (tt - 0.004) / 2), d, 0.001, 0.0005)
    for sx in (-1, 1):
        _bb(top, (sh, D - 0.004, tt - 0.004), (sx * (W / 2 - sh / 2 - 0.0005), 0, zt + (tt - 0.004) / 2), d, 0.001, 0.0005)
    if d <= 1:  # rolled hems along the inside bottom of the edges
        for sy in (-1, 1):
            add_cylinder_between(top, (-W / 2 + 0.006, sy * (D / 2 - 0.005), zt + 0.003), (W / 2 - 0.006, sy * (D / 2 - 0.005), zt + 0.003), 0.003, 8)
        for sx in (-1, 1):
            add_cylinder_between(top, (sx * (W / 2 - 0.005), -D / 2 + 0.008, zt + 0.003), (sx * (W / 2 - 0.005), D / 2 - 0.008, zt + 0.003), 0.003, 8)
        for y in (-D * 0.2, D * 0.2):  # hat-channel stiffeners
            _bb(top, (W - 0.06, 0.04, 0.025), (0, y, H - 0.004 - 0.0125), d, 0.002, 0.001)
    fz = H - 0.004 - 0.03  # leg-frame top under the stiffeners
    for sx in (-1, 1):
        x = sx * (W / 2 - k["leg_inset_m"])
        ys = (-D / 2 + 0.07, D / 2 - 0.07)
        fh = 0.035 if d <= 1 else 0.0
        for y in ys:
            add_cylinder_between(fr, (x, y, fh), (x, y, fz), lr, s)
            if d <= 1:  # adjustable bullet foot: tapered body + thread collar
                add_lathe(P("Feet", k["legs"]), (x, y, 0), (0, 0, 1), [(0, 0), (lr * 0.55, 0), (lr * 1.05, 0.012), (lr * 1.05, 0.026),
                                                                      (lr * 0.7, 0.03), (lr * 0.7, fh + 0.006), (0, fh + 0.006)], s)
        add_cylinder_between(fr, (x, ys[0], fz), (x, ys[1], fz), lr, s)  # top bar of the leg frame
        add_cylinder_between(fr, (x, ys[0], 0.14), (x, ys[1], 0.14), lr * 0.8, s)  # cross bar
        if d <= 1:
            for y in ys:  # hinge plates
                _bb(fr, (0.05, 0.05, 0.004), (x, y, fz + lr + 0.002), d, 0.004, 0.001)
                for a in (-1, 1):
                    _screw(fr, d, (x + a * 0.016, y + a * 0.016, fz + lr + 0.004), (0, 0, 1), 0.0035)
            bx = x - sx * 0.3
            add_tube(fr, [(x, 0, 0.14), (x - sx * 0.15, 0, (0.14 + fz) / 2)], 0.006, 8)  # folding brace, two links
            add_tube(fr, [(x - sx * 0.15, 0, (0.14 + fz) / 2), (bx, 0, fz + 0.005)], 0.006, 8)
            add_cylinder_between(fr, (x - sx * 0.15, -0.012, (0.14 + fz) / 2), (x - sx * 0.15, 0.012, (0.14 + fz) / 2), 0.009, s)  # knuckle
            _bb(fr, (0.04, 0.05, 0.012), (bx, 0, fz + 0.012), d, 0.003, 0.001)  # brace bracket
    return {"collision_boxes": _body(W, D, H)}


def task_chair(P, p, d, s, W, D, H):
    """Mesh task chair: five-star base with hub, twin-wheel casters, chrome gas lift under a ribbed shroud, tilt
    mechanism with tension knob and lever, crowned waterfall seat cushion on a pan, T armrests (post, adjust button,
    soft pad), spine, framed mesh back with lumbar band. Outer arm faces = W, seat front / spine back = D, frame top = H."""
    c = p["chair"]
    R, zs, sd, sw = c["star_r_m"], c["seat_z_m"], c["seat_d_m"], c["seat_w_m"]
    base, mesh, pad = P("Base", "Chair_Black"), P("Mesh", "Mesh_Black"), P("Seat", "Fabric_Black")
    if d >= 3:
        add_box(base, (2 * R, 2 * R, zs - 0.07), (0, 0, (zs - 0.07) / 2))
        add_box(pad, (W, sd, 0.12), (0, -D / 2 + sd / 2, zs - 0.06))
        add_box(mesh, (sw, 0.04, H - zs), (0, D / 2 - 0.02, zs + (H - zs) / 2))
        return {"collision_boxes": _body(W, D, H)}
    zh = 0.1
    seg = 2 if d == 0 else 1
    wr = 0.025
    for k in range(5):
        th = math.radians(90 + 72 * k)
        ux, uy = math.cos(th), math.sin(th)
        tip = (R * ux, R * uy)
        prof = rounded_rect(0.045, 0.032, 0.01, seg) if d <= 1 else rounded_rect(0.045, 0.032, 0, 0)
        add_sweep(base, [(0.03 * ux, 0.03 * uy, zh), (tip[0] * 0.6, tip[1] * 0.6, zh - 0.006), (tip[0], tip[1], zh - 0.018)], prof)
        px, py = -uy, ux  # wheel axle direction (perpendicular to the leg)
        cz = wr + 0.004
        if d <= 1:
            add_cylinder_between(base, (tip[0], tip[1], zh - 0.04), (tip[0], tip[1], zh - 0.018), 0.014, s)  # socket boss
            add_cylinder_between(base, (tip[0], tip[1], cz + 0.02), (tip[0], tip[1], zh - 0.04), 0.0055, 8)  # stem
            add_cylinder_between(base, (tip[0] - px * 0.007, tip[1] - py * 0.007, cz + 0.002),
                                 (tip[0] + px * 0.007, tip[1] + py * 0.007, cz + 0.002), wr * 0.95, s)  # hood between the wheels
        for sg in (-1, 1):  # twin wheels
            a = (tip[0] + sg * px * 0.008, tip[1] + sg * py * 0.008, wr)
            b2 = (tip[0] + sg * px * 0.024, tip[1] + sg * py * 0.024, wr)
            add_cylinder_between(P("Casters", "Chair_Black"), a, b2, wr, s)
    add_lathe(base, (0, 0, 0), (0, 0, 1), [(0, zh - 0.035), (0.045, zh - 0.035), (0.05, zh - 0.01), (0.05, zh + 0.01),
                                           (0.04, zh + 0.025), (0, zh + 0.025)], s)  # hub
    add_cylinder_between(P("GasLift", "GasLift_Chrome"), (0, 0, zh + 0.025), (0, 0, zs - 0.11), 0.014, s)
    if d <= 1:  # ribbed shroud over the gas cylinder
        prof = [(0, zh + 0.025)]
        n = 8 if d == 0 else 3
        z0, z1 = zh + 0.025, zh + 0.025 + 0.16
        for i in range(n + 1):
            z = z0 + (z1 - z0) * i / n
            prof.append((0.028 if i % 2 == 0 else 0.032, z))
        prof += [(0.02, z1 + 0.004), (0, z1 + 0.004)]
        add_lathe(base, (0, 0, 0), (0, 0, 1), [(r, z) for r, z in prof], s)
    add_cylinder_between(base, (0, 0, zs - 0.13), (0, 0, zs - 0.09), 0.03, s)  # lift collar
    sy = -D / 2 + sd / 2
    _bb(base, (0.24, 0.26, 0.04), (0, sy + 0.02, zs - 0.09), d, 0.012, 0.005)  # mechanism
    if d <= 1:
        add_lathe(base, (0, sy - 0.08, zs - 0.11), (0, 0, -1), [(0, 0), (0.022, 0), (0.024, 0.01), (0.02, 0.04), (0, 0.04)], s)  # tension knob
        add_tube(base, [(0.1, sy + 0.04, zs - 0.09), (0.19, sy - 0.02, zs - 0.1)], 0.005, 8)  # height lever
        _bb(base, (0.04, 0.025, 0.012), (0.2, sy - 0.03, zs - 0.1), d, 0.006, 0.003)
    # seat: pan + crowned waterfall cushion (loft of rounded rects)
    _bb(base, (sw - 0.02, sd - 0.02, 0.012), (0, sy, zs - 0.064), d, 0.05, 0.004)
    if d <= 1:
        cr = 0.07
        rs = 6 if d == 0 else 2
        rings = []
        for z, ins in ((zs - 0.058, 0.012), (zs - 0.045, 0.0), (zs - 0.02, 0.0), (zs - 0.006, 0.012), (zs, 0.04)):
            rings.append([(x, y + sy, z) for x, y in rounded_rect(sw, sd, cr, rs, ins)])
        loft(pad, rings)
    else:
        add_box(pad, (sw, sd, 0.058), (0, sy, zs - 0.029))
    ay = -D / 2 + sd * 0.55
    for sx in (-1, 1):  # T armrests; outer face = W/2
        ax = sx * (W / 2 - 0.04)
        add_box(base, (abs(ax) - 0.1 + 0.015, 0.04, 0.016), (sx * (0.1 + (abs(ax) - 0.1) / 2), ay, zs - 0.075))  # bracket
        _bb(base, (0.026, 0.05, zs + 0.17 - (zs - 0.083)), (ax, ay, (zs - 0.083 + zs + 0.17) / 2), d, 0.008, 0.003)  # post
        if d <= 1:
            _bb(base, (0.012, 0.018, 0.03), (ax, ay - 0.027, zs + 0.06), d, 0.004, 0.002)  # height button
        _bb(pad, (0.08, 0.25, 0.028), (ax, ay, zs + 0.17 + 0.014), d, 0.03, 0.01)
    # spine: mechanism -> back; its rear face is the +D/2 bound
    add_box(base, (0.06, D / 2 - (sy + 0.15), 0.03), (0, (sy + 0.15 + D / 2) / 2 - 0.0, zs - 0.085))
    _bb(base, (0.06, 0.025, 0.3), (0, D / 2 - 0.0125, zs + 0.06), d, 0.008, 0.004)
    by = D / 2 - 0.04
    bz0, bz1 = zs + 0.07, H - 0.012
    bh, bc = bz1 - bz0, (bz0 + bz1) / 2
    rr = rounded_rect(sw - 0.024, bh, 0.07, 6 if d == 0 else 2)
    add_tube(base, [(x, by, bc + z) for x, z in rr], 0.012, 8, closed=True)  # back frame; top = H (8 segs: exact extent)
    for sx in (-1, 1):  # back to spine brackets
        add_box(base, (0.12, 0.02, 0.03), (sx * 0.08, by + 0.015, zs + 0.17))
    rm = rounded_rect(sw - 0.04, bh - 0.016, 0.06, 6 if d == 0 else 2)
    if d <= 1:
        loft(mesh, [[(x, by + 0.002, bc + z) for x, z in rm], [(x, by - 0.002, bc + z) for x, z in rm]])
        _bb(base, (sw - 0.07, 0.012, 0.05), (0, by + 0.01, zs + 0.2), d, 0.01, 0.004)  # lumbar band
        if d == 0:  # woven mesh read: horizontal weft strands across the panel face
            hx = (sw - 0.05) / 2
            for z in even_positions(bh - 0.05, 0.012):
                add_cylinder_between(mesh, (-hx, by - 0.0025, bc + z), (hx, by - 0.0025, bc + z), 0.0012, 6, caps=False)
    else:
        add_box(mesh, (sw - 0.04, 0.004, bh - 0.016), (0, by, bc))
    return {"collision_boxes": _body(W, D, H)}


def _cart_tray(P, fin, W, D, z, d, s):
    """Pressed stainless shelf: floor, up-turned marine lip with a rolled rim (outer = W x D), hat stiffeners."""
    sh = P("Shelves", fin)
    rr = 0.003
    lip = 0.028
    _bb(sh, (W - 0.006, D - 0.006, 0.003), (0, 0, z - 0.0015), d, 0.01, 0.001)
    if d <= 1:
        for sy in (-1, 1):
            add_box(sh, (W - 0.01, 0.0015, lip), (0, sy * (D / 2 - rr), z + lip / 2))
        for sx in (-1, 1):
            add_box(sh, (0.0015, D - 0.01, lip), (sx * (W / 2 - rr), 0, z + lip / 2))
        add_tube(sh, [(x, y, z + lip) for x, y in rounded_rect(W - 2 * rr, D - 2 * rr, 0, 0)], rr, 8, closed=True)
        for y in (-D * 0.18, D * 0.18):
            add_box(sh, (W - 0.06, 0.03, 0.018), (0, y, z - 0.003 - 0.009))
    else:
        add_box(sh, (W, D, lip), (0, 0, z + lip / 2 - 0.0015))


def _wire_basket(P, fin, W, D, z, bd, pitch, d, s):
    """Welded wire basket: perimeter floor frame + floor grid, vertical side wires, mid rail, heavy top rim (outer = W x D)."""
    b = P("Shelves", fin)
    rr, wr = 0.003, 0.002
    loop = lambda zz, ins: [(x, y, zz) for x, y in rounded_rect(W - 2 * ins, D - 2 * ins, 0.01, 2 if d == 0 else 0)]
    add_tube(b, loop(z + bd, rr), rr, 8 if d <= 1 else 6, closed=True)
    add_tube(b, loop(z + 0.0025, 0.006), 0.0025, 6, closed=True)
    if d <= 1:
        add_tube(b, loop(z + bd * 0.5, 0.0045), wr, 6, closed=True)
    pg = pitch * (1 if d == 0 else 2) if d <= 1 else pitch * 3
    add_wire_grid(b, W - 0.014, D - 0.014, z + 0.0025, 2 * wr, pg, pg, 6)
    if d <= 2:
        for x in even_positions(W - 0.03, pg):
            for sy in (-1, 1):
                add_cylinder_between(b, (x, sy * (D / 2 - 0.0055), z + 0.004), (x, sy * (D / 2 - 0.0035), z + bd - 0.002), wr, 6, caps=False)
        for y in even_positions(D - 0.03, pg):
            for sx in (-1, 1):
                add_cylinder_between(b, (sx * (W / 2 - 0.0055), y, z + 0.004), (sx * (W / 2 - 0.0035), y, z + bd - 0.002), wr, 6, caps=False)


def cart(P, p, d, s, W, D, H):
    c = p["cart"]
    fin = c["finish"]
    fr = P("Frame", fin)
    lv = c["shelf_z_m"]
    ct = c["caster_h_m"]
    if d >= 3:
        for z in lv:
            add_box(fr, (W, D, 0.04), (0, 0, z - 0.02))
        for x in (-W / 2 + 0.04, W / 2 - 0.04):
            add_box(fr, (0.03, D - 0.08, H - ct), (x, 0, ct + (H - ct) / 2))
            add_box(P("Casters", c["caster"]), (0.03, D - 0.08, ct), (x, 0, ct / 2))
        return {"collision_boxes": _body(W, D, H)}
    pr = c["post_r_m"]
    pin = c["post_inset_m"]
    px, py = W / 2 - pin, D / 2 - pin
    tray = c["shelf"] == "tray"
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * px, sy * py
            if c.get("handle") and sx < 0:
                top = max(lv)  # the handle tube continues the post
            else:
                top = max(lv) + 0.028 if tray else H - 0.006  # tray posts stop at the top lip
            add_cylinder_between(fr, (x, y, ct), (x, y, top), pr, s)
            if not tray:  # domed post cap at the top
                add_lathe(fr, (x, y, top), (0, 0, 1), [(pr * 1.05, 0), (pr * 1.05, 0.003), (pr * 0.6, 0.0055), (0, 0.006)], s)
            if d <= 1:
                for z in lv:  # post collars / shelf clips
                    add_lathe(fr, (x, y, z - 0.03), (0, 0, 1), [(0, 0), (pr * 1.35, 0), (pr * 1.35, 0.022), (pr * 1.1, 0.03), (0, 0.03)], s)
            _caster(P, c["caster_fork"], c["caster"], x, y, sx, ct, d, s)
    for z in lv:
        if tray:
            _cart_tray(P, fin, W, D, z, d, s)
        else:
            _wire_basket(P, fin, W, D, z, c["basket_d_m"], c["wire_pitch_m"], d, s)
    if c.get("handle"):  # push handle: U tube rising from the -X posts, top at H
        add_tube(fr, [(-px, -py, max(lv)), (-px, -py, H - pr), (-px, py, H - pr), (-px, py, max(lv))], pr, s,
                 bend_radius=0.04 if d <= 1 else 0, bend_steps=4 if d == 0 else (2 if d == 1 else 0))
        if d <= 1:  # rail label ("FOR DELI USE ONLY", RF/RI 2.4; text not modelled), on the top lip front
            add_box(P("Labels", "Label_Grey"), (0.2, 0.0008, 0.018), (0, -D / 2 + 0.003 - 0.0012, max(lv) + 0.014))
    return {"collision_boxes": _body(W, D, H)}


KINDS = {"tall_cabinet": tall_cabinet, "file_cabinets": file_cabinets, "desk": desk, "standing_desk": standing_desk,
         "worktable": worktable, "task_chair": task_chair, "cart": cart}


def build(p, lod):
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"], W, D, H)
    extra = dict(extra, fixture_family="office_fixtures", rf=p["rf"], seed=int(p["seed"]))
    extra.update(wear(p))
    return P.finish(), (W, H, D), extra
