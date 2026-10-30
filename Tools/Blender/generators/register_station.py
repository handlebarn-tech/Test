"""Register station props (PROC-005 §4; IMP-003 drop 2 rewritten). One params file, one asset per variant:
scale stand (REFERENCES_INDEX §2.2), POS monitor on a VESA stand, presentation scanner, handheld scanner in its stand
(RF Scanner_Barcode), 17.5 in keyboard, receipt printer, card terminal. No cash drawer (DEC-051, R1). Unbranded.
Unsourced sizes are params under GAP-PROC-14. Origin = bottom centre, front = -Y (the staff side for the scale
stand; its acrylic panel is on the counter side, +Y). LOD0 full detail; LOD1 no micro detail (keys, welds, vents);
LOD2 merged/plain parts; LOD3 one block per part group."""
import math

from mathutils import Vector

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_lathe, add_screw_head, add_sweep, add_tube,
                     add_wire_grid, collision_box, loft, rounded_rect, to_unity, wear)

CS = (4, 2, 1, 0)  # rounded-corner segments per detail level


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def _rr_box(bm, size, center, d, corner, bevel):
    """Beveled box at LOD0-2 (bevel dropped from LOD2), plain box at LOD3."""
    if d >= 3:
        add_box(bm, size, center)
    else:
        add_beveled_box(bm, size, center, corner=corner, bevel=bevel if d <= 1 else 0.0, seg=max(1, CS[d]))


def scale_stand(P, p, d, s):
    w, dp, top, th, tw = p["width_m"], p["depth_m"], p["height_m"], p["tray_h_m"], p["tray_wall_m"]
    zt, zf = top - th, top - th + tw  # tray bottom, tray floor
    pr, ins, rr = p["post_d_m"] / 2, p["post_inset_m"], p["rail_d_m"] / 2
    px, py = w / 2 - ins, dp / 2 - ins
    ph, pt = p["panel_h_m"], p["panel_t_m"]
    py_panel = dp / 2 - tw - pt / 2 - 0.001
    H = zf + ph
    frame, tray, panel = P("Frame", "Chrome"), P("Tray", "Plastic_Black"), P("Panel", "Acrylic_Clear")
    sc = p["scale"]
    sx, sy = 0.0, sc["y_m"]
    zs = zf + sc["foot_h_m"]
    zpan = zs + sc["h_m"] + sc["pan_post_h_m"]
    zbowl = zpan + sc["pan_t_m"]
    ztop = zbowl + sc["bowl_h_m"] + sc["lid_h_m"] + sc["knob_h_m"]
    if d >= 3:
        for x in (-px, px):
            for y in (-py, py):
                add_box(frame, (2 * pr, 2 * pr, zt), (x, y, zt / 2))
        add_box(frame, (2 * px, 2 * py, 0.02), (0, 0, p["shelf_z_m"] - 0.01))
        add_box(tray, (w, dp, th), (0, 0, zt + th / 2))
        add_box(panel, (w - 2 * tw - 0.002, pt, ph), (0, py_panel, zf + ph / 2))
        add_box(P("Scale", "Plastic_White"), (sc["w_m"], sc["d_m"], ztop - zf), (sx, sy, (zf + ztop) / 2))
    else:
        # frame: 4 posts on leveller feet, a rail loop under the tray and one at the wire shelf, welded joints
        fh = p["foot_h_m"] if d <= 1 else 0.0
        for x in (-px, px):
            for y in (-py, py):
                add_cylinder_between(frame, (x, y, fh), (x, y, zt), pr, s)
                if d <= 1:
                    add_lathe(P("Feet", "Rubber_Black"), (x, y, 0), (0, 0, 1),
                              [(0, 0), (pr * 1.15, 0), (pr * 1.15, fh * 0.5), (pr * 0.5, fh), (0, fh)], s)
                if d == 0:
                    for zr in (zt - rr, p["shelf_z_m"] - rr):
                        add_lathe(frame, (x, y, 0), (0, 0, 1), [(pr, zr - 0.006), (pr + 0.0022, zr), (pr, zr + 0.006)], s)
        loop = [(-px, -py), (px, -py), (px, py), (-px, py)]
        for zr in (zt - rr, p["shelf_z_m"] - rr):
            add_tube(frame, [(x, y, zr) for x, y in loop], rr, 8 if d <= 1 else 6, closed=True)
        add_wire_grid(frame, 2 * px, 2 * py, p["shelf_z_m"], p["wire_d_m"], p["wire_pitch_m"] * (1, 2, 4)[d], py, 6)
        # black tray: formed lip (rolled at LOD0-1), thin walls, flat floor
        cs = max(1, CS[d])

        def ring(inset, z):
            return [(x, y, z) for x, y in rounded_rect(w, dp, p["tray_corner_r_m"], cs, inset)]
        if d <= 1:
            loft(tray, [ring(0, zt), ring(0, top - 0.0015), ring(tw / 2, top), ring(tw, top - 0.0015), ring(tw, zf)])
        else:
            loft(tray, [ring(0, zt), ring(0, top), ring(tw, top), ring(tw, zf)])
        # acrylic panel, full width on the counter-side edge, polished (bevelled) edges, chrome clamps to the tray wall
        _rr_box(panel, (w - 2 * tw - 0.002, pt, ph), (0, py_panel, zf + ph / 2), d, 0.004, 0.001)
        if d <= 1:
            for x in (-w * 0.33, w * 0.33):
                add_box(frame, (0.03, pt + 0.005, 0.022), (x, py_panel - 0.0005, top - 0.006))
        # white bench scale: body on rubber feet, blue LCD + keypad on the front, stainless pan, round draft-shield bowl + lid
        body = P("Scale", "Plastic_White")
        _rr_box(body, (sc["w_m"], sc["d_m"], sc["h_m"]), (sx, sy, zs + sc["h_m"] / 2), d, 0.012, 0.003)
        yf = sy - sc["d_m"] / 2
        if d <= 1:
            for fx in (-1, 1):
                for fy in (-1, 1):
                    add_cylinder_between(P("Feet", "Rubber_Black"), (sx + fx * sc["w_m"] * 0.38, sy + fy * sc["d_m"] * 0.38, zf),
                                         (sx + fx * sc["w_m"] * 0.38, sy + fy * sc["d_m"] * 0.38, zs), 0.007, s)
        add_box(P("LCD", "LCD_Blue"), (sc["lcd_w_m"], 0.002, sc["lcd_h_m"]), (sx - 0.02, yf - 0.0009, zs + sc["h_m"] * 0.55))
        if d <= 1:
            for i in range(4):
                kx = sx + 0.035 + i * 0.014
                add_cylinder_between(P("Keys", "Plastic_Grey"), (kx, yf + 0.0005, zs + sc["h_m"] * 0.5),
                                     (kx, yf - 0.0025, zs + sc["h_m"] * 0.5), 0.0045, s)
        steel = P("Pan", "Stainless")
        pan_r = sc["pan_d_m"] / 2
        add_cylinder_between(steel, (sx, sy, zs + sc["h_m"] - 0.001), (sx, sy, zpan), 0.012, s)
        add_lathe(steel, (sx, sy, 0), (0, 0, 1), [(0, zpan), (pan_r, zpan), (pan_r, zbowl), (pan_r - 0.003, zbowl), (0, zbowl)]
                  if d <= 1 else [(0, zpan), (pan_r, zpan), (pan_r, zbowl), (0, zbowl)], s * 2)
        br, bh, bw_ = sc["bowl_d_m"] / 2, sc["bowl_h_m"], 0.002
        glass = P("DraftShield", "Acrylic_Clear")
        zb = zbowl
        if d <= 1:  # open bowl: outer wall up, rim, inner wall down
            add_lathe(glass, (sx, sy, 0), (0, 0, 1), [(0, zb), (br * 0.8, zb), (br, zb + 0.012), (br, zb + bh), (br - bw_, zb + bh),
                                                       (br - bw_, zb + 0.012 + bw_), (br * 0.8 - bw_, zb + bw_), (0, zb + bw_)], s * 2)
        else:
            add_lathe(glass, (sx, sy, 0), (0, 0, 1), [(0, zb), (br, zb), (br, zb + bh), (0, zb + bh)], s * 2)
        zl, lh, kh = zb + bh, sc["lid_h_m"], sc["knob_h_m"]
        add_lathe(glass, (sx, sy, 0), (0, 0, 1), [(br + 0.002, zl), (br + 0.002, zl + 0.006), (br * 0.75, zl + lh * 0.8),
                                                   (0.012, zl + lh), (0, zl + lh)], s * 2)
        add_lathe(P("Pan", "Stainless"), (sx, sy, 0), (0, 0, 1), [(0, zl + lh - 0.002), (0.009, zl + lh - 0.002),
                                                                  (0.009, zl + lh + kh), (0, zl + lh + kh)], s)
    boxes = [collision_box("Frame", (0, 0, zt / 2), (2 * (px + pr), 2 * (py + pr), zt)),
             collision_box("Tray", (0, 0, zt + th / 2), (w, dp, th)),
             collision_box("Panel", (0, py_panel, zf + ph / 2), (w - 2 * tw, pt, ph))]
    extra = {"shelf_anchors": [
        {"id": "Shelf_00", "position_unity_xyz": to_unity(0, 0, p["shelf_z_m"]),
         "size_m_unity_xz": [round(2 * (px - rr), 5), round(2 * (py - rr), 5)]},
        {"id": "Tray_00", "position_unity_xyz": to_unity(0, 0, zf),
         "size_m_unity_xz": [round(w - 2 * tw, 5), round(dp - 2 * tw - pt, 5)]}],
        "weighing_anchor_unity_xyz": to_unity(sx, sy, zbowl), "collision_boxes": boxes}
    return (w, H, dp), extra


def _loft_front(bm, specs, cx, y0, cz, seg):
    """Rounded-rect rings in the XZ plane stacked toward -Y: specs = [(w, h, r, t)], t = offset toward -Y from y0.
    Same rules as proclib.loft (outside profile in order; the last ring is capped), mapped by a proper rotation."""
    loft(bm, [[(cx + x, y0 - t, cz + y) for x, y in rounded_rect(w, h, r, seg)] for w, h, r, t in specs])


def _loft_up(bm, specs, cx, cy, seg):
    """Rounded-rect rings stacked along +Z: specs = [(w, d, r, z)]."""
    loft(bm, [[(cx + x, cy + y, z) for x, y in rounded_rect(w, dd, r, seg)] for w, dd, r, z in specs])


def pos_monitor(P, p, d, s):
    m = p["monitor"]
    w, h, pd, b, rd = m["w_m"], m["h_m"], m["panel_d_m"], m["bezel_m"], m["rear_d_m"]
    bw, bd, bh = m["base_w_m"], m["base_d_m"], m["base_h_m"]
    zb, yf = m["bottom_z_m"], m["front_y_m"]
    zc = zb + h / 2
    yb = yf + pd + rd  # back of the rear bulge
    hs, st = P("Housing", "Plastic_Black"), P("Stand", "Metal_Black")
    if d >= 3:
        add_box(hs, (w, pd, h), (0, yf + pd / 2, zc))
        add_box(st, (bw, bd, bh), (0, 0, bh / 2))
        add_box(st, (m["neck_w_m"], m["neck_d_m"], zc - bh), (0, yb + m["neck_d_m"] / 2, bh + (zc - bh) / 2))
        return (w, zb + h, bd), {}
    cs = max(1, CS[d])
    rw, rh = w * 0.62, h * 0.6
    # rear bulge (tapered back cover), then the panel shell, then the bezel lip stepping into the screen recess
    if d <= 1:
        _loft_front(hs, [(rw * 0.86, rh * 0.82, 0.012, 0), (rw, rh, 0.016, rd * 0.55), (rw, rh, 0.016, rd + 0.001)], 0, yb, zc, cs)
        _loft_front(hs, [(w - 0.004, h - 0.004, 0.005, 0), (w, h, 0.006, 0.002), (w, h, 0.006, pd - 0.0012),
                         (w - 0.0014, h - 0.0014, 0.0055, pd), (w - 2 * b, h - 2 * b, 0.002, pd),
                         (w - 2 * b, h - 2 * b, 0.002, pd - 0.0025)], 0, yf + pd, zc, cs)
        add_box(P("Screen", "Glass_Dark"), (w - 2 * b - 0.0004, 0.0008, h - 2 * b - 0.0004), (0, yf + 0.0021, zc))
    else:
        _rr_box(hs, (rw, rd, rh), (0, yf + pd + rd / 2, zc), d, 0.01, 0.0)
        _rr_box(hs, (w, pd, h), (0, yf + pd / 2, zc), d, 0.006, 0.0)
        add_box(P("Screen", "Glass_Dark"), (w - 2 * b, 0.001, h - 2 * b), (0, yf - 0.0004, zc))
    if d == 0:
        vents = P("Vents", "Plastic_Dark")
        for row in range(3):  # slotted vents on the top of the back cover
            for i in range(16):
                add_box(vents, (0.004, 0.0008, 0.018), (-rw * 0.4 + i * rw * 0.8 / 15, yb + 0.0002, zc + rh / 2 - 0.02 - row * 0.026))
        for i in range(4):  # menu buttons under the bottom bezel, power LED in the bezel corner
            add_beveled_box(hs, (0.008, 0.005, 0.0025), (w / 2 - 0.03 - i * 0.014, yf + 0.008, zb - 0.001), 0.001, 0.0004, 2)
        add_box(P("LED", "LCD_Blue"), (0.003, 0.0006, 0.0018), (w / 2 - b / 2, yf - 0.0003, zb + b / 2))
        ports = P("Ports", "Plastic_Dark")  # recessed I/O block on the lower back cover: power, 2 video, USB
        for i, pw in enumerate((0.012, 0.016, 0.016, 0.01)):
            add_box(ports, (pw, 0.0012, 0.006), (-rw * 0.3 + i * 0.026, yb + 0.0004, zc - rh / 2 + 0.02))
    if d <= 1:  # VESA 100 plate with 4 screws, tilt hinge barrel
        vp = P("Stand", "Metal_Black")
        add_beveled_box(vp, (0.11, 0.005, 0.11), (0, yb + 0.0025, zc), 0.006, 0.001, 2)
        if d == 0:
            for sx in (-0.05, 0.05):
                for sz in (-0.05, 0.05):
                    add_screw_head(P("Screws", "Metal_Screw"), (sx, yb + 0.005, zc + sz), (0, 1, 0), 0.0035, 8)
    ny = yb + (0.005 if d <= 1 else 0) + m["neck_d_m"] / 2
    if d <= 1:
        add_cylinder_between(st, (-m["neck_w_m"] / 2 - 0.004, ny - 0.004, zc), (m["neck_w_m"] / 2 + 0.004, ny - 0.004, zc), 0.011, s)
    _rr_box(st, (m["neck_w_m"], m["neck_d_m"], zc - bh), (0, ny, bh + (zc - bh) / 2), d, 0.008, 0.0015)
    if d <= 1:  # cable-management cut-out in the neck, rubber feet under the base
        add_box(P("Vents", "Plastic_Dark"), (m["neck_w_m"] * 0.5, 0.0008, 0.03), (0, ny + m["neck_d_m"] / 2 + 0.0002, bh + 0.05))
        fz = 0.003
        _loft_up(st, [(bw - 0.006, bd - 0.006, 0.026, fz), (bw, bd, 0.03, fz + 0.003), (bw, bd, 0.03, bh - 0.004),
                      (bw - 0.008, bd - 0.008, 0.026, bh)], 0, 0, cs)
        for fx in (-1, 1):
            for fy in (-1, 1):
                add_cylinder_between(P("Feet", "Rubber_Black"), (fx * (bw / 2 - 0.02), fy * (bd / 2 - 0.02), 0),
                                     (fx * (bw / 2 - 0.02), fy * (bd / 2 - 0.02), fz), 0.007, s)
    else:
        _rr_box(st, (bw, bd, bh), (0, 0, bh / 2), d, 0.03, 0.0)
    return (w, zb + h, bd), {"collision_boxes": [collision_box("Monitor", (0, yf + (pd + rd) / 2, zc), (w, pd + rd, h)),
                                                 collision_box("Base", (0, 0, bh / 2), (bw, bd, bh))]}


def presentation_scanner(P, p, d, s):
    c = p["scanner"]
    rb, H, hw, hd, hh = c["base_d_m"] / 2, c["h_m"], c["head_w_m"], c["head_d_m"], c["head_h_m"]
    bd = P("Body", "Plastic_Black")
    if d >= 3:
        add_box(bd, (2 * rb, 2 * rb, 0.02), (0, 0, 0.01))
        add_box(bd, (hw, hd, H - 0.02), (0, 0, 0.02 + (H - 0.02) / 2))
        return (2 * rb, H, 2 * rb), {}
    cs = max(1, CS[d])
    fz = 0.003 if d <= 1 else 0.0
    if d <= 1:  # rubber foot ring, weighted base with a chamfered rim
        add_lathe(P("Feet", "Rubber_Black"), (0, 0, 0), (0, 0, 1), [(0, 0), (rb - 0.004, 0), (rb - 0.004, fz), (0, fz)], s * 2)
    add_lathe(bd, (0, 0, 0), (0, 0, 1), [(0, fz), (rb, fz), (rb, 0.012), (rb * 0.85, 0.02), (0, 0.02)] if d <= 1 else
              [(0, 0), (rb, 0), (rb, 0.02), (0, 0.02)], s * 2)
    zn = H - hh - 0.012  # neck top / hinge
    loft(bd, [[(x, y, z) for x, y in rounded_rect(ww, dd, 0.01, cs)] for ww, dd, z in
              ((0.05, 0.045, 0.018), (0.04, 0.036, zn - 0.01), (0.034, 0.03, zn))])
    if d <= 1:  # tilt hinge between neck and head, with side caps
        add_cylinder_between(bd, (-0.024, 0, zn + 0.004), (0.024, 0, zn + 0.004), 0.011, s)
        for sx in (-1, 1):
            add_cylinder_between(P("Trim", "Plastic_Grey"), (sx * 0.024, 0, zn + 0.004), (sx * 0.0255, 0, zn + 0.004), 0.008, s)
        _loft_up(bd, [(hw * 0.8, hd * 0.7, 0.01, zn + 0.004), (hw, hd, 0.012, H - hh + 0.004), (hw, hd, 0.012, H - 0.004),
                      (hw - 0.006, hd - 0.006, 0.009, H)], 0, 0, cs)
        # window bezel (front, -Y): recessed red window in a raised frame
        _loft_front(bd, [(hw * 0.86, hh * 0.68, 0.006, 0), (hw * 0.86, hh * 0.68, 0.006, 0.0015), (hw * 0.74, hh * 0.56, 0.004, 0.0015), (hw * 0.74, hh * 0.56, 0.004, 0.0005)],
                    0, -hd / 2 + 0.0005, H - hh * 0.48, cs)
        add_box(P("Window", "Glass_Red"), (hw * 0.74, 0.0006, hh * 0.56), (0, -hd / 2 - 0.0003, H - hh * 0.48))
        add_box(P("LED", "LCD_Green"), (0.006, 0.0012, 0.003), (0, -hd / 2 - 0.0002, H - 0.008))
        add_tube(P("Cable", "Plastic_Dark"), [(0, 0.016, 0.05), (0, 0.026, 0.03), (0, rb - 0.006, 0.0215)], 0.0028, 6,
                 bend_radius=0.008, bend_steps=3)
    else:
        _rr_box(bd, (hw, hd, hh + 0.012), (0, 0, H - (hh + 0.012) / 2), d, 0.012, 0.0)
        add_box(P("Window", "Glass_Red"), (hw * 0.75, 0.002, hh * 0.55), (0, -hd / 2 - 0.0009, H - hh * 0.48))
    return (2 * rb, H, 2 * rb), {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (2 * rb, 2 * rb, H))]}


def handheld_scanner(P, p, d, s):
    """RF Scanner_Barcode: handheld gun scanner standing in its cradle (0.4 x 0.7 x 0.6 ft)."""
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    g = p["gun"]
    bt, hl, hw, hh = g["base_t_m"], g["head_l_m"], g["head_w_m"], g["head_h_m"]
    yc = D * 0.2  # cradle centre over the base
    zh = H - hh / 2
    st, gun = P("Stand", "Plastic_Black"), P("Gun", "Plastic_Dark")
    if d >= 3:
        add_box(st, (W, D * 0.6, 0.07), (0, yc, 0.035))
        add_box(gun, (hw, hl, hh), (0, -D / 2 + hl / 2, zh))
        add_box(gun, (0.03, 0.03, zh - 0.07), (0, yc - 0.01, 0.07 + (zh - 0.07) / 2))
        return (W, H, D), {}
    _rr_box(st, (W, D * 0.6, bt), (0, yc, bt / 2), d, 0.02, 0.003)
    cs = max(1, CS[d])

    def ring(inset, z):
        return [(x, y + yc, z) for x, y in rounded_rect(0.06, 0.055, 0.015, cs, inset)]
    loft(st, [ring(0, bt), ring(0, 0.07), ring(0.004, 0.07), ring(0.004, bt + 0.004)])  # open cradle cup
    prof = rounded_rect(hw, hh, 0.012, cs)  # Y path: u = -X, v = +Z (proclib._basis)
    add_sweep(gun, [(0, -D / 2 + 0.001, zh), (0, -D / 2 + hl, zh)], prof)
    g0, g1 = Vector((0, -D / 2 + hl - 0.03, zh - hh / 2 + 0.005)), Vector((0, yc, 0.05))
    add_sweep(gun, [g0, g1], rounded_rect(0.032, 0.028, 0.01, cs))
    add_box(P("Window", "Glass_Red"), (hw * 0.75, 0.0015, hh * 0.6), (0, -D / 2 + 0.00075, zh))
    if d <= 1:
        ax = (g1 - g0).normalized()
        fwd = Vector((0, ax.z, -ax.y))  # perpendicular to the grip, pointing to the front
        add_sweep(P("Trigger", "Plastic_Black"), [g0 + ax * (0.012 + 0.0) + fwd * 0.02, g0 + ax * 0.035 + fwd * 0.02],
                  rounded_rect(0.006, 0.012, 0.002, 1))
        add_tube(P("Cable", "Plastic_Dark"), [(0, yc + 0.01, 0.035), (0, yc + 0.03, 0.025), (0, D / 2 - 0.004, 0.015)], 0.003, 6)
    return (W, H, D), {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


KEY_ROWS = [  # key widths in units, negative = gap, (w, rows) = tall key extending toward the front
    [1, -1, 1, 1, 1, 1, -0.5, 1, 1, 1, 1, -0.5, 1, 1, 1, 1, -0.5, 1, 1, 1, -0.5, -4],
    [1] * 13 + [2, -0.5, 1, 1, 1, -0.5, 1, 1, 1, 1],
    [1.5] + [1] * 12 + [1.5, -0.5, 1, 1, 1, -0.5, 1, 1, 1, (1, 2)],
    [1.75] + [1] * 11 + [2.25, -0.5, -3, -0.5, 1, 1, 1, -1],
    [2.25] + [1] * 10 + [2.75, -0.5, -1, 1, -1, -0.5, 1, 1, 1, (1, 2)],
    [1.25] * 3 + [6.25] + [1.25] * 4 + [-0.5, 1, 1, 1, -0.5, 2, 1, -1]]


def keyboard(P, p, d, s):
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    k = p["keyboard"]
    zc, m = k["case_h_m"], k["margin_m"]
    u = (W - 2 * m) / 23.0
    case = P("Case", "Plastic_Black")
    z0 = 0.003 if d <= 1 else 0.0
    if d >= 3:
        add_box(case, (W, D, H), (0, 0, H / 2))
        return (W, H, D), {}
    if d <= 1:  # case with chamfered edges and a recessed key well (the caps sit in it)
        yw, ww, dw = -D / 2 + m + 3.25 * u, 23 * u + 0.003, 6.5 * u + 0.003
        rings = [(W - 0.004, D - 0.004, 0.006, 0, z0), (W, D, 0.008, 0, z0 + 0.002), (W, D, 0.008, 0, zc - 0.0015),
                 (W - 0.003, D - 0.003, 0.0065, 0, zc), (ww, dw, 0.002, yw, zc), (ww, dw, 0.002, yw, zc - 0.004)]
        loft(case, [[(x, y + cy, z) for x, y in rounded_rect(w_, d_, r_, 2)] for w_, d_, r_, cy, z in rings])
    else:
        _rr_box(case, (W, D, zc - z0), (0, 0, z0 + (zc - z0) / 2), d, 0.008, 0.0)
    if d <= 1:
        for fx in (-1, 1):
            add_box(P("Feet", "Rubber_Black"), (0.03, 0.01, 0.003), (fx * (W / 2 - 0.04), D / 2 - 0.02, 0.0015))
            add_box(P("Feet", "Rubber_Black"), (0.02, 0.008, 0.003), (fx * (W / 2 - 0.04), -D / 2 + 0.02, 0.0015))
        for i in range(3):  # lock-key indicator LEDs in the top margin
            add_box(P("LED", "LCD_Green"), (0.003, 0.002, 0.0008), (W / 2 - m - 3 * u + i * u, D / 2 - 0.007, zc + 0.0002))
    keys = P("Keys", "Plastic_Keys")
    gap, kz0 = 0.0016, zc - (0.0035 if d <= 1 else 0.002)
    y_top = -D / 2 + m + 6.5 * u  # back edge of the F row; rows run toward the front (-Y)
    for ri, row in enumerate(KEY_ROWS):
        yr = y_top - (ri + (0.5 if ri else 0)) * u  # half-unit gap under the F row
        x = -W / 2 + m
        runs = []
        for kspec in row:
            kw, kr = (kspec, 1) if not isinstance(kspec, tuple) else kspec
            if kw < 0:
                x -= kw * u
                continue
            cx, cy, sx, sy = x + kw * u / 2, yr - kr * u / 2, kw * u - gap, kr * u - gap
            if d == 2:
                runs.append((x, x + kw * u, cy, sy))
            elif d == 1:
                add_box(keys, (sx, sy, H - kz0), (cx, cy, kz0 + (H - kz0) / 2))
            else:  # tapered cap with a rounded top edge
                loft(keys, [[(cx + a, cy + b, z) for a, b in rounded_rect(sx, sy, 0.004, 2, ins)]
                            for ins, z in ((0, kz0), (0.0018, H - 0.0015), (0.003, H))])
            x += kw * u
        if d == 2:  # LOD2: one slab per run of 1-row keys
            i = 0
            while i < len(runs):
                j = i
                while j + 1 < len(runs) and abs(runs[j + 1][0] - runs[j][1]) < 1e-9 and runs[j + 1][3] == runs[i][3]:
                    j += 1
                add_box(keys, (runs[j][1] - runs[i][0] - gap, runs[i][3], H - kz0),
                        ((runs[i][0] + runs[j][1]) / 2, runs[i][2], kz0 + (H - kz0) / 2))
                i = j + 1
    return (W, H, D), {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def receipt_printer(P, p, d, s):
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    r = p["printer"]
    zs, yslot = r["split_z_m"], -D / 2 + r["front_d_m"]
    body = P("Body", "Plastic_Dark")
    if d >= 3:
        add_box(body, (W, D, zs), (0, 0, zs / 2))
        add_box(body, (W, D / 2 - yslot, H - zs), (0, (yslot + D / 2) / 2, zs + (H - zs) / 2))
        return (W, H, D), {}
    cs = max(1, CS[d])
    side = 0.001 if d <= 1 else 0.0  # body is 1 mm narrower each side; the power rocker and cover lever reach W
    fz = 0.003 if d <= 1 else 0.0
    if d <= 1:
        _loft_up(body, [(W - 2 * side - 0.006, D - 0.006, 0.008, fz), (W - 2 * side, D, 0.01, fz + 0.003),
                        (W - 2 * side, D, 0.01, zs + 0.005), (W - 2 * side - 0.003, D - 0.003, 0.0085, zs + 0.008)], 0, 0, cs)
        for fx in (-1, 1):
            for fy in (-1, 1):
                add_cylinder_between(P("Feet", "Rubber_Black"), (fx * (W / 2 - 0.018), fy * (D / 2 - 0.02), 0),
                                     (fx * (W / 2 - 0.018), fy * (D / 2 - 0.02), fz), 0.006, s)
    else:
        _rr_box(body, (W, D, zs + 0.008), (0, 0, (zs + 0.008) / 2), d, 0.01, 0.0)
    lid = P("Lid", "Plastic_Dark")  # clamshell lid: swept rounded profile across X (u = Y, v = Z for an X path)
    ld, lh = D / 2 - yslot, H - zs + 0.004
    lw = W / 2 - side - (0.0015 if d <= 1 else 0)  # step at the lid seam
    prof = [(a + (yslot + D / 2) / 2, b + zs - 0.004 + lh / 2) for a, b in rounded_rect(ld, lh, r["lid_r_m"], cs * 2)]
    add_sweep(lid, [(-lw, 0, 0), (lw, 0, 0)], prof)
    add_box(P("Slot", "Plastic_Black"), (W * 0.7, 0.004, 0.006), (0, yslot - 0.0015, zs + 0.006))
    add_box(P("Paper", "Paper_White"), (W * 0.55, 0.0006, 0.022), (0, yslot - 0.0035, zs + 0.013))
    if d <= 1:
        steel = P("TearBar", "Stainless")
        add_box(steel, (W * 0.72, 0.0015, 0.004), (0, yslot - 0.0045, zs + 0.009))
        if d == 0:  # serrated tear edge
            for i in range(24):
                add_box(steel, (0.0018, 0.0012, 0.0016), (-W * 0.34 + i * W * 0.68 / 23, yslot - 0.0045, zs + 0.0118))
        seam = P("Slot", "Plastic_Black")  # dark seam line where the lid meets the body
        add_box(seam, (2 * lw - 0.004, D / 2 - yslot - 0.006, 0.0012), (0, (yslot + D / 2) / 2, zs + 0.0084))
        ytop = (-D / 2 + yslot) / 2  # front ledge: feed button, status LEDs, cover-open lever
        add_beveled_box(P("Button", "Plastic_Grey"), (0.016, 0.009, 0.003), (W * 0.27, ytop, zs + 0.0095), 0.002, 0.0008, 2)
        for i in range(2):
            add_box(P("LED", "LCD_Green"), (0.003, 0.003, 0.0008), (W * 0.42 - i * 0.006, ytop, zs + 0.0084))
        add_beveled_box(P("Button", "Plastic_Grey"), (0.0022, 0.03, 0.018), (W / 2 - 0.0011, -D * 0.05, zs - 0.006), 0.0008, 0.0004, 2)
        add_beveled_box(P("Switch", "Plastic_Black"), (0.0022, 0.012, 0.008), (-W / 2 + 0.0011, D * 0.3, zs * 0.5), 0.0008, 0.0004, 2)
    return (W, H, D), {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


def card_terminal(P, p, d, s):
    t = p["terminal"]
    L, tw, tt, ang, zc, rb = t["l_m"], t["w_m"], t["t_m"], math.radians(t["tilt_deg"]), t["centre_z_m"], t["base_d_m"] / 2
    a = Vector((0, math.cos(ang), math.sin(ang)))
    n = Vector((0, -math.sin(ang), math.cos(ang)))  # slab top normal (= sweep v axis)
    c = Vector((0, 0, zc))
    p0, p1 = c - a * L / 2, c + a * L / 2
    W, D, H = max(2 * rb, tw), 2 * (L / 2 * a.y + tt / 2 * abs(n.y)), zc + L / 2 * a.z + tt / 2 * n.z
    body = P("Body", "Plastic_Terminal")
    if d >= 3:
        add_box(body, (2 * rb, 2 * rb, 0.015), (0, 0, 0.0075))
        add_box(body, (tw, D, H - 0.015), (0, 0, 0.015 + (H - 0.015) / 2))
        return (W, H, D), {}
    cs = max(1, CS[d])
    stand = P("Stand", "Plastic_Terminal")
    fz = 0.002 if d <= 1 else 0.0
    if d <= 1:
        add_lathe(P("Feet", "Rubber_Black"), (0, 0, 0), (0, 0, 1), [(0, 0), (rb - 0.004, 0), (rb - 0.004, fz), (0, fz)], s * 2)
    add_lathe(stand, (0, 0, 0), (0, 0, 1), [(0, fz), (rb, fz), (rb, 0.01), (rb * 0.8, 0.015), (0, 0.015)] if d <= 1
              else [(0, 0), (rb, 0), (rb, 0.015), (0, 0.015)], s * 2)
    zh = zc - tt / 2 / math.cos(ang) - 0.004  # swivel/tilt hinge under the body
    add_cylinder_between(stand, (0, 0, 0.014), (0, 0, zh), 0.012, s)
    if d <= 1:
        add_lathe(stand, (0, 0, 0), (0, 0, 1), [(0.0125, 0.014), (0.016, 0.014), (0.016, 0.02), (0.0125, 0.022)], s)  # swivel collar
        add_cylinder_between(stand, (-tw / 2 + 0.008, 0, zh), (tw / 2 - 0.008, 0, zh), 0.008, s)
        for sx in (-1, 1):  # cradle cheeks hold the body on the hinge
            ox = -sx * (tw / 2 + 0.002)
            add_sweep(stand, [c - a * 0.028 - n * (tt * 0.15), c + a * 0.028 - n * (tt * 0.15)],
                      [(pu + ox, pv) for pu, pv in rounded_rect(0.004, tt * 0.75, 0.0015, 1)])
            add_cylinder_between(P("Screws", "Metal_Screw"), (sx * (tw / 2 + 0.004), 0, zh), (sx * (tw / 2 + 0.0045), 0, zh), 0.003, 8)
    add_sweep(body, [p0, p1], rounded_rect(tw, tt, 0.008, cs))
    top = n * (tt / 2)
    # screen in the upper half: glass sheet over a black mask, a hair proud of the body
    add_sweep(P("Screen", "Glass_Dark"), [c + a * (L * 0.04) + top, c + a * (L * 0.44) + top],
              [(pu, pv + 0.0004) for pu, pv in rounded_rect(tw * 0.8, 0.0008, 0.0003, 1)])
    # chip-card slot in the lower end face
    add_sweep(P("Slot", "Plastic_Black"), [p0 - a * 0.0004, p0 + a * 0.004], [(pu, pv + tt * 0.12) for pu, pv in rounded_rect(tw * 0.7, 0.0022, 0.0008, 1)])
    if d <= 1:
        keys = P("Keys", "Plastic_Grey")
        kprof = rounded_rect(0.011, 0.016, 0.0028, 2 if d == 0 else 1)
        kprof_fn = rounded_rect(0.009, 0.016, 0.0028, 2 if d == 0 else 1)
        for row in range(5):  # 4 rows of 3 digits, then the function row
            for col in range(3):
                q = c - a * (L * 0.06 + row * 0.015) + Vector(((col - 1) * 0.02, 0, 0)) + top
                add_sweep(keys, [q - n * 0.0005, q + n * 0.0016], kprof if row < 4 else kprof_fn)
        add_sweep(P("Slot", "Plastic_Black"), [c - a * (L * 0.3), c + a * (L * 0.3)],  # magstripe groove on the side
                  [(pu - tw / 2 - 0.0002, pv) for pu, pv in rounded_rect(0.0012, 0.003, 0.0004, 1)])
        add_box(P("LED", "LCD_Green"), (0.012, 0.0012, 0.0012), tuple(c + a * (L * 0.47) + top + n * 0.0003))
    return (W, H, D), {"collision_boxes": [collision_box("Body", (0, 0, H / 2), (W, D, H))]}


KINDS = {"scale_stand": scale_stand, "pos_monitor": pos_monitor, "presentation_scanner": presentation_scanner,
         "handheld_scanner": handheld_scanner, "keyboard": keyboard, "receipt_printer": receipt_printer,
         "card_terminal": card_terminal}


def build(p, lod):
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    expected, extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"])
    extra = dict(extra, fixture_family="register_station", component_role=p["kind"], seed=int(p["seed"]))
    extra.update(wear(p))
    return P.finish(), expected, extra
