"""Register counter runs (PROC-005 fix wave; REVIEW-PROC5 #1/#2/#6). One asset per ROOM_FIXTURES rev7 row:
Counter_Register_North (registers 10/9/8), Counter_Register_EastReturn (12/11), Counter_Register_South (7,2,3,4,5,6)
and Counter_Register_SouthReturn (no register). RI §1.5 rows 98/101 (REF-011), RI §8.1, DEC-039.

Local frame (exported): origin bottom centre, staff side = -Y (asset front: drawers, open shelves), customer face = +Y,
run along X. `plan_axis_x` in params says which plan direction local +X points along once ART yaws the asset so its +Y
customer face points to the RF `faces` direction (so station offsets map back to the plan).
Construction (TI §6.4 POS cabinet, detail 11): quartz slab top with an eased edge and waterfall ends; carcass 2'-1" deep
on a 4 in toe base with a 2 in recess; staff side = one two-drawer POS cabinet under each monitor (walnut fronts,
HW-2 brass edge pulls) and open black shelf bays elsewhere (R2C3, RI §2.2); customer face = plywood sheets carrying the
decorative wrap (DEC-090, RF North notes, RI §8.1), black ML-1 band under the top. Edge banding on shelf fronts,
shelf pins, back-rail screws and cable grommets are construction detail. No cash drawer (DEC-051/086). Unbranded.
LOD0 full; LOD1 no pins/screws/pulls/banding; LOD2 one block per face group; LOD3 top + body + ends."""
from proclib import Parts, add_beveled_box, add_box, add_cylinder_between, add_lathe, add_screw_head, collision_box, ft, to_unity, wear


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def _bb(bm, size, center, d, corner=0.002, bevel=0.0015):
    if d >= 2:
        add_box(bm, size, center)
    else:
        add_beveled_box(bm, size, center, corner=corner, bevel=bevel, seg=3 if d == 0 else 1)


def _modules(xa, xb, drawers, max_bay):
    """Gable x positions: drawer cabinet edges, the run ends, and extra gables so no open bay is wider than max_bay."""
    cuts = []
    for x in sorted({xa, xb} | {min(max(x, xa), xb) for a, b in drawers for x in (a, b)}):
        if not cuts or x - cuts[-1] > 0.05:  # merge slivers (a cabinet ending at the run end)
            cuts.append(x)
    cuts[-1] = xb
    out = [cuts[0]]
    for a, b in zip(cuts, cuts[1:]):
        n = max(1, int(-(-(b - a) // max_bay)))
        out += [a + (b - a) * i / n for i in range(1, n + 1)]
    return out


def build(p, lod):
    d, s = lod["detail"], lod["seg"]
    # Exported staff side front (-Y = staff, the side that shows the construction). Built in a customer-front frame and
    # turned 180 deg about Z at the end; params use the exported frame, so mirror them into the build frame here.
    p = dict(p, stations=[dict(st, local_x_m=-st["local_x_m"]) for st in p["stations"]], waterfall=p["waterfall"][::-1],
             end_panel_black=p.get("end_panel_black", [False, False])[::-1])

    def R(x, y, z):  # build frame -> exported Unity point
        return to_unity(-x, -y, z)
    L, D, H, tt = p["length_m"], p["depth_m"], p["height_m"], p["top_t_m"]
    kick, krec, cd, g = p["toe_h_m"], p["toe_recess_m"], p["carcass_depth_m"], p["gable_t_m"]
    wl, wr = p["waterfall"]
    stations = p["stations"]
    lip = p["grommet_lip_m"] if stations else 0.0
    zt = H - lip - tt  # underside of the top; the grommet flange reaches the cited 34 in (H)
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    top = P("Top", "Quartz_QZ2")
    face = P("FrontWrap", p["face_color"])
    blk, shelf = P("Accents", "Black_ML1"), P("Carcass", "Black_ML1_Interior")
    wal, brass = P("DrawerFronts", "Walnut_WD1"), P("Pulls", "Brass_HW2")
    xa, xb = -L / 2 + (tt if wl else 0), L / 2 - (tt if wr else 0)
    yb = D / 2 - p["staff_overhang_m"]  # staff face of the drawer fronts (the top overhangs it)
    yf, yg = yb - cd, yb - 0.019  # carcass customer face; gable fronts (drawer fronts overlay them)
    cw = p["drawer_cabinet_w_m"]
    drawers = [(st["local_x_m"] - cw / 2, st["local_x_m"] + cw / 2) for st in stations]

    if d >= 3:
        add_box(top, (L, D, H - zt), (0, 0, zt + (H - zt) / 2))
        add_box(face, (xb - xa, cd, zt), (0, (yf + yb) / 2, zt / 2))
        for on, x in ((wl, -L / 2 + tt / 2), (wr, L / 2 - tt / 2)):
            if on:
                add_box(top, (tt, D, zt), (x, 0, zt / 2))
    else:
        # top: 2 in slab, eased edge; waterfall ends run to the floor
        _bb(top, (L, D, tt), (0, 0, zt + tt / 2), d, 0.003, 0.005 if d <= 1 else 0)
        for on, x in ((wl, -L / 2 + tt / 2), (wr, L / 2 - tt / 2)):
            if on:
                _bb(top, (tt, D, zt), (x, 0, zt / 2), d, 0.003, 0.005 if d <= 1 else 0)
            elif p.get("end_panel_black", [False, False])[0 if x < 0 else 1]:  # exposed cabinet end in black ML-1 (R2C5 "black cabinet end")
                xe = xa + g / 2 if x < 0 else xb - g / 2
                _bb(blk, (g, cd, zt - 0.001), (xe, (yf + yb) / 2, (zt - 0.001) / 2), d, 0.001, 0.001)
        pt, band = p["face_panel_t_m"], p["accent_band_h_m"]
        # customer face: recessed toe kick, plywood sheets with hairline seams (wrap print = texture), ML-1 band
        add_box(blk, (xb - xa, 0.012, kick), (0, yf + krec + 0.006, kick / 2))
        zp0, zp1 = kick, zt - band
        if d <= 1:
            sheet, seam = p["face_sheet_w_m"], p["seam_m"]
            n = max(1, int(-(-(xb - xa) // sheet)))
            pw = (xb - xa) / n
            add_box(blk, (xb - xa, 0.004, zp1 - zp0), (0, yf + pt + 0.002, (zp0 + zp1) / 2))  # dark backer in the seams
            for i in range(n):
                _bb(face, (pw - seam, pt, zp1 - zp0 - seam), (xa + (i + 0.5) * pw, yf + pt / 2, (zp0 + zp1) / 2), d, 0.0015, 0.0012)
            _bb(blk, (xb - xa, pt + 0.004, band), (0, yf + (pt + 0.004) / 2 - 0.004, zt - band / 2), d, 0.001, 0.001)
        else:
            add_box(face, (xb - xa, pt, zp1 - zp0), (0, yf + pt / 2, (zp0 + zp1) / 2))
            add_box(blk, (xb - xa, pt, band), (0, yf + pt / 2, zt - band / 2))
        # carcass: back (inside the face), bottom deck on the toe base, gables, staff toe kick
        yi0 = yf + pt + 0.004  # inside face of the back panel
        bd = yg - yi0
        add_box(shelf, (xb - xa, 0.012, zt - kick), (0, yi0 + 0.006, kick + (zt - kick) / 2))
        add_box(shelf, (xb - xa, bd - 0.012, g), (0, (yi0 + 0.012 + yg) / 2, kick + g / 2))
        add_box(blk, (xb - xa, 0.012, kick), (0, yb - krec - 0.006, kick / 2))
        gx = _modules(xa, xb, drawers, p["max_open_bay_m"])
        for x in gx:
            x = min(max(x, xa + g / 2), xb - g / 2)
            _bb(shelf, (g, bd, zt - kick - g), (x, (yi0 + yg) / 2, kick + g + (zt - kick - g) / 2), d, 0.0008, 0.0008)
            if d <= 1:  # black edge banding on the gable front
                add_box(blk, (g, 0.0012, zt - kick - g), (x, yg + 0.0006, kick + g + (zt - kick - g) / 2))
        rv, sz = p["reveal_m"], p["open_shelf_z_frac"]
        for a, b in zip(gx, gx[1:]):
            xm, w = (a + b) / 2, b - a - g
            if any(abs(xm - (da + db) / 2) < 0.01 for da, db in drawers):  # two-drawer POS cabinet (TI 11)
                dh = (zt - kick - g - 3 * rv) / 2
                for k in range(2):
                    zc = kick + g + rv + dh / 2 + k * (dh + rv)
                    if d <= 1:
                        _bb(shelf, (w - 0.02, bd - 0.04, dh - 0.03), (xm, (yi0 + yg) / 2 - 0.01, zc), d, 0.001, 0.001)  # drawer box
                    _bb(wal, (w + g - rv, 0.019, dh), (xm, yg + 0.0095, zc), d, 0.0015, 0.0012)
                    if d == 0:  # HW-2 brushed-brass edge pull clipped over the drawer front's top edge
                        pw_ = w * p["pull_w_frac"]
                        add_beveled_box(brass, (pw_, 0.022, 0.003), (xm, yb - 0.008, zc + dh / 2 + 0.0015), 0.001, 0.0005, 2)
                        add_beveled_box(brass, (pw_, 0.003, 0.016), (xm, yb + 0.0015, zc + dh / 2 - 0.005), 0.001, 0.0005, 2)
            else:  # open bay: adjustable shelf with black edge banding on 4 pins; back-rail screws
                zs = kick + g + (zt - kick - g) * sz
                _bb(shelf, (w - 0.002, bd - 0.03, g), (xm, (yi0 + yg) / 2 - 0.01, zs), d, 0.0008, 0.0008)
                if d <= 1:
                    add_box(blk, (w - 0.002, 0.0012, g), (xm, yg - 0.025 + 0.0006, zs))
                if d == 0:
                    for xx in (a + g / 2 + 0.0005, b - g / 2 - 0.0005):
                        for yy in (yi0 + 0.06, yg - 0.06):
                            sgn = 1 if xx < xm else -1
                            add_cylinder_between(P("Hardware", "Steel_Pins"), (xx, yy, zs - g / 2 - 0.003),
                                                 (xx + sgn * 0.009, yy, zs - g / 2 - 0.003), 0.0025, 6)
                    for xx in (a + 0.06, b - 0.06):
                        add_screw_head(P("Hardware", "Steel_Pins"), (xx, yi0 + 0.012, zt - 0.05), (0, 1, 0), 0.0045, 8)
        # cable grommet behind each monitor: flange is the topmost point (34 in, TI §6.4)
        if d <= 2:
            r = p["grommet_d_m"] / 2
            for st in stations:
                gxp, gyp = st["local_x_m"] + p["grommet_dx_m"], D / 2 - p["grommet_inset_m"]
                prof = [(r - 0.005, zt - 0.01), (r - 0.005, H - 0.0006), (r - 0.0045, H), (r + 0.006, H), (r + 0.0068, H - lip)]
                add_lathe(P("Grommets", "Plastic_Grommet"), (gxp, gyp, 0), (0, 0, 1),
                          prof if d <= 1 else [(r - 0.005, zt), (r - 0.005, H), (r + 0.006, H), (r + 0.006, H - lip)], s)
                if d == 0:  # cap with the cable slot
                    add_lathe(P("Grommets", "Plastic_Grommet"), (gxp, gyp, 0), (0, 0, 1),
                              [(0, H - 0.004), (r - 0.0052, H - 0.004), (r - 0.0052, H - 0.0012), (0, H - 0.0012)], s)
    if d >= 3 and stations:  # LOD3: one grommet block per station keeps the 34 in bound
        for st in stations:
            add_box(P("Grommets", "Plastic_Grommet"), (p["grommet_d_m"], p["grommet_d_m"], lip),
                    (st["local_x_m"] + p["grommet_dx_m"], D / 2 - p["grommet_inset_m"], H - lip / 2))

    c, an = p["components"], p["anchor_offsets"]
    yo, yc = D / 2 + an["operator_off_staff_edge_m"], -D / 2 - an["call_off_face_m"]
    anchors = []
    for st in stations:
        x, reg = st["local_x_m"], st["register"]
        tag = f"{reg:02d}"
        comps = {k: {"asset_id": v["asset_id"], "position_unity_xyz": R(x + v["dx_m"], D / 2 + v["dy_from_staff_edge_m"], v.get("z_m", H)),
                     "yaw_deg": v.get("yaw_deg", 0)} for k, v in c.items()}
        anchors.append({"register": reg, "station_id": f"Register_{tag}", "rf_fixture": f"POS_{tag}", "local_x_m": -x,
                        "position_unity_xyz": R(x, D / 2 - p["monitor_inset_m"], H),
                        "scene_anchors": {f"Anchor_Register_{tag}_Operator": R(x, yo, 0),
                                          f"Anchor_Register_{tag}_Call": R(x, yc, 0)},
                        "components": comps})
    extra = {"fixture_family": "register_counter_run", "seed": int(p["seed"]), "rf_fixture": p["rf"],
             "plan_axis_x": p["plan_axis_x"], "station_anchors": anchors,
             "collision_boxes": [collision_box("Top", (0, 0, zt + tt / 2), (L, D, tt)),
                                 collision_box("Body", (0, -(yf + yb) / 2, zt / 2), (L, cd, zt))]}
    if p.get("display_case_slot_x_m") is not None:  # RI §1.5 row 99 display case on the north run (x 38.0-39.4)
        extra["display_case_slot"] = {"asset_id": p["display_case_asset_id"], "position_unity_xyz": R(-p["display_case_slot_x_m"], 0, H - lip),
                                      "footprint_m": [ft(1.4), ft(1.4)]}
    extra.update(wear(p))
    for bm, *_ in P._p.values():  # turn 180 deg about Z (keeps winding)
        for v in bm.verts:
            v.co.x, v.co.y = -v.co.x, -v.co.y
    return P.finish(), (L, H, D), extra
