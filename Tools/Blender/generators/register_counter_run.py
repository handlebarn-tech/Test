"""Register counter run (PROC-005 §5; IMP-003 round 2 rewritten). One asset per L leg (variants): the long run and the
return leg; ART places them on the plan (RI §1.5 bbox 20.0-42.0 x 7.0-19.0 ft; compass GAP-106).
TI §6.4 POS cabinet: QZ-2 white quartz top 34 in AFF, 2'-6" deep, 2 in eased edge, waterfall on the outside ends,
4 in toe base (2 in recess), 2'-1" cabinet depth. Customer face (front, -Y) = WD-1 walnut veneer panels with black
ML-1 reveals and an ML-1 band under the top. Staff side (+Y) per station: two-drawer cabinet (walnut fronts, HW-2
brass edge pulls) + open black shelves (R2C3). Cable grommet per station. No cash drawer (DEC-051).
station_anchors carry the DEC-039 register numbers; per-station width = leg length / stations (RC5, GAP-PROC-15).
LOD0 full; LOD1 no pulls; LOD2 plain blocks per face; LOD3 top + body + ends."""
from proclib import Parts, add_beveled_box, add_box, add_lathe, collision_box, to_unity, wear


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def _bb(bm, size, center, d, corner=0.002, bevel=0.0015):
    if d >= 2:
        add_box(bm, size, center)
    else:
        add_beveled_box(bm, size, center, corner=corner, bevel=bevel, seg=2 if d == 0 else 1)


def build(p, lod):
    d, s = lod["detail"], lod["seg"]
    L, D, H, tt = p["length_m"], p["depth_m"], p["height_m"], p["top_t_m"]
    kick, krec, ov, lip = p["toe_h_m"], p["toe_recess_m"], p["front_overhang_m"], p["grommet_lip_m"]
    wl, wr = p["waterfall"]
    P = Parts(p["colors"])
    top, wal, blk, brass = P("Top", "Quartz_QZ2"), P("Front", "Walnut_WD1"), P("Accents", "Black_ML1"), P("Pulls", "Brass_HW2")
    xa, xb = -L / 2 + (tt if wl else 0), L / 2 - (tt if wr else 0)
    yf = -D / 2 + ov  # customer face of the cabinets; the staff face is flush with the top at +D/2
    zt = H - tt
    regs = p["registers"]
    n = len(regs)
    pitch = (xb - xa) / n
    Htot = H + lip

    if d >= 3:
        add_box(top, (L, D, tt + lip), (0, 0, zt + (tt + lip) / 2))
        add_box(wal, (xb - xa, D - ov, zt), (0, (yf + D / 2) / 2, zt / 2))
        for on, x in ((wl, -L / 2 + tt / 2), (wr, L / 2 - tt / 2)):
            if on:
                add_box(top, (tt, D, zt), (x, 0, zt / 2))
    else:
        _bb(top, (L, D, tt), (0, 0, zt + tt / 2), d, 0.003, 0.004 if d <= 1 else 0)  # 2 in slab, eased edge
        for on, x in ((wl, -L / 2 + tt / 2), (wr, L / 2 - tt / 2)):  # waterfall ends, mitred look via the eased edges
            if on:
                _bb(top, (tt, D, zt), (x, 0, zt / 2), d, 0.003, 0.004 if d <= 1 else 0)
        # customer face: toe kick, black backer (shows in the reveals), walnut panels, ML-1 band under the top
        band = p["accent_band_h_m"]
        add_box(blk, (xb - xa, 0.012, kick), (0, yf + krec + 0.006, kick / 2))
        add_box(blk, (xb - xa, 0.01, zt - kick), (0, yf + 0.019 + 0.005, kick + (zt - kick) / 2))
        add_box(blk, (xb - xa, 0.02, band), (0, yf + 0.01, zt - band / 2))
        rv = p["reveal_m"]
        if d <= 1:
            for i in range(n):
                for j in range(2):  # two veneer panels per station
                    pw = pitch / 2
                    x = xa + i * pitch + (j + 0.5) * pw
                    _bb(wal, (pw - rv, 0.019, zt - band - kick - rv), (x, yf + 0.0095, kick + (zt - band - kick) / 2), d, 0.001, 0.0008)
        else:
            add_box(wal, (xb - xa, 0.019, zt - band - kick), (0, yf + 0.0095, kick + (zt - band - kick) / 2))
        # carcass: gables at the station lines and the ends, bottom deck on the toe base
        sh = P("Shelves", "Black_ML1")
        cd = D / 2 - (yf + 0.029)
        cy = (yf + 0.029 + D / 2) / 2
        for i in range(n + 1):
            x = min(max(xa + i * pitch, xa + 0.0095), xb - 0.0095)
            add_box(sh, (0.019, cd, zt - kick), (x, cy, kick + (zt - kick) / 2))
        add_box(sh, (xb - xa, cd, 0.019), (0, cy, kick + 0.0095))
        add_box(blk, (xb - xa, 0.012, kick), (0, D / 2 - krec - 0.006, kick / 2))  # staff-side toe kick
        # staff side per station: left half = two-drawer cabinet, right half = open shelf
        dh = (zt - kick - 0.019 - 3 * rv) / 2
        for i in range(n):
            x0 = xa + i * pitch + 0.0095
            hw = (pitch - 0.019) / 2
            xd = x0 + hw / 2 + 0.0095 / 2
            if d <= 1:
                add_box(sh, (hw - 0.01, cd - 0.03, zt - kick - 0.02), (xd, cy - 0.015, kick + (zt - kick) / 2))  # drawer boxes
                for k in range(2):
                    zc = kick + 0.019 + rv + dh / 2 + k * (dh + rv)
                    _bb(wal, (hw - rv, 0.019, dh), (xd, D / 2 - 0.012 - 0.0095, zc), d, 0.001, 0.0008)
                    if d == 0:  # HW-2 brushed-brass edge pull on the drawer's top edge
                        add_box(brass, (hw * 0.35, 0.010, 0.004), (xd, D / 2 - 0.012 + 0.0045 - 0.004, zc + dh / 2 - 0.002))
            else:
                add_box(wal, (hw, 0.019, zt - kick - 0.019), (xd, D / 2 - 0.012 - 0.0095, kick + 0.019 + (zt - kick - 0.019) / 2))
            add_box(sh, (hw - 0.002, cd - 0.02, 0.019), (x0 + hw * 1.5 + 0.0095, cy, kick + (zt - kick) * 0.5))
            if d <= 2:  # cable grommet behind the monitor position (kept on LOD0-2: its lip sets the height bound)
                gx, gy = x0 + pitch * 0.5, D / 2 - p["grommet_inset_m"]
                r = p["grommet_d_m"] / 2
                add_lathe(P("Grommets", "Plastic_Black"), (gx, gy, 0), (0, 0, 1),
                          [(r - 0.006, zt + 0.004), (r - 0.006, H + lip), (r + 0.004, H + lip), (r + 0.004, H)], s)
    anchors = []
    c = p["components"]
    for i, reg in enumerate(regs):
        x = xa + (i + 0.5) * pitch
        anchors.append({"register": reg, "station_id": f"Register_{reg:02d}", "position_unity_xyz": to_unity(x, 0, H),
                        "slot_width_m": round(pitch, 5),
                        "components": {k: {"asset_id": v["asset_id"], "position_unity_xyz": to_unity(x + v["dx_m"], v["dy_m"], v.get("z_m", H)),
                                           "yaw_deg": v.get("yaw_deg", 0)}
                                       for k, v in c.items()}})
    extra = {"fixture_family": "register_counter_run", "seed": int(p["seed"]), "station_anchors": anchors,
             "plan_rect_ft": p["plan_rect_ft"],
             "collision_boxes": [collision_box("Top", (0, 0, zt + tt / 2), (L, D, tt)),
                                 collision_box("Body", (0, (yf + D / 2) / 2, zt / 2), (L, D - ov, zt))]}
    if p.get("display_case_slot_x_m") is not None:  # RC4: countertop case on the run (RI §1.5, plan x 38.0-39.4)
        extra["display_case_slot"] = {"asset_id": p["display_case_asset_id"], "position_unity_xyz": to_unity(p["display_case_slot_x_m"], 0, H),
                                      "footprint_m": [0.42672, 0.42672]}
    extra.update(wear(p))
    return P.finish(), (L, Htot, D), extra
