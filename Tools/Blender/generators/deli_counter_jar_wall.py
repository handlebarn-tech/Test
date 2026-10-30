"""Deli jar walls + deli counter (PROC-005 §6; IMP-003 round 2 rewritten). Variants:
- jar_wall (RI §1.5 north 26.0 x 1.2 ft, south 21.2 x 1.2 ft, east 14.0 x 1.4 ft; RI §2.4 / DEC-043): black-top base
  cabinet at 34 in (TI §6.4 max) with walnut drawer fronts in two rows and silver cup pulls; dark-grey sheet-metal
  shelves with a front lip on black standards + brackets at a 1'-2" pitch above the counter (D2); teal leaf-pattern
  backlit back panel (emissive; pattern = texture) with LED strips under each shelf; green/black checker tile band at
  the top. Jar slots = PROC_DeliJar size (D4) on the counter top and every shelf, bottom-centre anchors; the game
  assigns strains (D3, DEC-079: one jar per strain, house deli x2). Stainless tong cups are NOT modelled (DEC-043).
- deli_counter (RI §1.5 L, bbox 14.0-34.2 x 18.0-25.2 ft; DEC-090): one asset per leg. Customer front = plywood
  panels (4 ft sheets with seams and exposed ply edges) carrying the decorative wrap (teal/white checker print is the
  wrap material's texture, no tile geometry). Optional glass case on top (`case_on_top`, default off, GAP-PROC-16).
Unsourced sizes (wall height, counter depth/height, shelf/standard/pull sizes) are GAP-PROC-16 / GAP-113.
Origin = bottom centre, front (customer side) = -Y. Globe pendants and arches belong to the architecture/lighting kit."""
from proclib import Parts, add_beveled_box, add_box, add_cylinder_between, add_sweep, collision_box, to_unity, wear


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def _bb(bm, size, center, d, corner=0.002, bevel=0.0012):
    if d >= 2:
        add_box(bm, size, center)
    else:
        add_beveled_box(bm, size, center, corner=corner, bevel=bevel, seg=2 if d == 0 else 1)


def _base_cabinet(P, p, d, L, D, H, top_t, y0):
    """Counter base from y0 (front face) to +D/2: black top, walnut two-row drawer fronts, cup pulls, toe kick."""
    kick, rec, rv = p["toe_h_m"], p["toe_recess_m"], p["reveal_m"]
    zt = H - top_t
    _bb(P("CounterTop", "Black_Top"), (L, D, top_t), (0, 0, zt + top_t / 2), d, 0.003, 0.003)
    blk = P("Carcass", "Black_ML1")
    add_box(blk, (L, D / 2 - y0 - 0.019, zt - kick), (0, (y0 + 0.019 + D / 2) / 2, kick + (zt - kick) / 2))
    add_box(blk, (L, 0.012, kick), (0, y0 + rec + 0.006, kick / 2))
    wal = P("DrawerFronts", "Walnut_WD1")
    if d >= 2:
        add_box(wal, (L, 0.019, zt - kick), (0, y0 + 0.0095, kick + (zt - kick) / 2))
        return
    cols = max(1, round(L / p["drawer_w_m"]))
    cw, rh = L / cols, (zt - kick) / 2
    for i in range(cols):
        for r in range(2):
            x, z = -L / 2 + (i + 0.5) * cw, kick + (r + 0.5) * rh
            _bb(wal, (cw - rv, 0.019, rh - rv), (x, y0 + 0.0095, z), d, 0.0015, 0.001)
            if d == 0:  # silver cup pull (half-round body + back plate)
                pull = P("Pulls", "Silver")
                add_box(pull, (0.076, 0.004, 0.022), (x, y0 - 0.002, z + rh * 0.25))
                add_cylinder_between(pull, (x - 0.035, y0 - 0.008, z + rh * 0.25 - 0.004), (x + 0.035, y0 - 0.008, z + rh * 0.25 - 0.004), 0.007, 12)


def jar_wall(P, p, d, s):
    L, D, H = p["length_m"], p["depth_m"], p["height_m"]
    ch, top_t, pt = p["counter_h_m"], p["counter_top_t_m"], p["back_panel_t_m"]
    yb = D / 2 - pt  # front face of the backlit panel
    sd, st, lip = p["shelf_depth_m"], p["shelf_t_m"], p["shelf_lip_m"]
    zs = [ch + p["shelf_pitch_m"] * (i + 1) for i in range(p["shelf_count"])]
    jw, jh, jd = p["jar_slot_m"]
    if d >= 3:
        add_box(P("CounterTop", "Black_Top"), (L, D, ch), (0, 0, ch / 2))
        add_box(P("BackPanel", "Teal_Backlit"), (L, pt, H - ch), (0, D / 2 - pt / 2, ch + (H - ch) / 2))
        for z in zs:
            add_box(P("Shelves", "Grey_Metal"), (L, sd, lip), (0, yb - sd / 2, z + lip / 2 - st))
    else:
        _base_cabinet(P, p, d, L, D, ch, top_t, -D / 2 + p["counter_front_inset_m"])
        add_box(P("BackPanel", "Teal_Backlit"), (L, pt, H - ch), (0, D / 2 - pt / 2, ch + (H - ch) / 2))
        bh = p["checker_band_h_m"]
        add_box(P("CheckerBand", "Tile_Checker"), (L, 0.012, bh), (0, yb - 0.006, H - bh / 2))
        sh, blk = P("Shelves", "Grey_Metal"), P("Standards", "Black_ML1")
        xs = [-L / 2 + 0.05 + (L - 0.1) * i / max(1, round((L - 0.1) / p["standard_pitch_m"]))
              for i in range(round((L - 0.1) / p["standard_pitch_m"]) + 1)]
        for x in xs:  # slotted wall standards
            add_box(blk, (0.025, 0.012, H - bh - ch - 0.02), (x, yb - 0.006, ch + 0.01 + (H - bh - ch - 0.02) / 2))
        for z in zs:
            yf, ye = yb - sd, yb
            if d <= 1:  # bent sheet: front lip up, deck, rear flange (u = Y, v = Z for an X path)
                prof = [(yf, z - st), (ye, z - st), (ye, z + 0.02), (ye - st, z + 0.02), (ye - st, z), (yf + st, z),
                        (yf + st, z - st + lip), (yf, z - st + lip)]
                add_sweep(sh, [(-L / 2 + 0.005, 0, 0), (L / 2 - 0.005, 0, 0)], prof)
                add_box(P("LED", "LED_Emissive"), (L - 0.02, 0.008, 0.004), (0, yf + 0.012, z - st - 0.002))
                for x in xs:  # brackets
                    add_box(blk, (0.012, sd * 0.85, 0.035), (x, ye - sd * 0.425 - 0.012, z - st - 0.0175))
            else:
                add_box(sh, (L - 0.01, sd, st), (0, yb - sd / 2, z - st / 2))
                add_box(sh, (L - 0.01, st, lip), (0, yf + st / 2, z - st + lip / 2))
    tiers = [ch] + zs
    slots = []
    n = int((L - 2 * p["jar_end_margin_m"]) // p["jar_pitch_m"])
    for ti, z in enumerate(tiers):
        y = yb - (sd if ti else p["counter_slot_depth_m"]) / 2 - (0.0 if ti else 0.0)
        for i in range(n):
            x = -(n - 1) * p["jar_pitch_m"] / 2 + i * p["jar_pitch_m"]
            slots.append({"id": f"Jar_T{ti}_{i:02d}", "tier": ti, "position_unity_xyz": to_unity(x, y, z)})
    boxes = [collision_box("Counter", (0, 0, ch / 2), (L, D, ch)),
             collision_box("BackPanel", (0, D / 2 - pt / 2, ch + (H - ch) / 2), (L, pt, H - ch))]
    boxes += [collision_box(f"Shelf_{i}", (0, yb - sd / 2, z - st / 2), (L, sd, st)) for i, z in enumerate(zs)]
    return (L, H, D), {"fixture_family": "jar_wall", "jar_asset_id": p["jar_asset_id"],
                       "jar_slot_size_m_unity_xyz": [jw, jh, jd], "jar_slots": slots, "jar_slot_count": len(slots),
                       "emissive_parts": ["BackPanel", "LED"], "collision_boxes": boxes}


def deli_counter(P, p, d, s):
    L, D, H, top_t = p["length_m"], p["depth_m"], p["height_m"], p["top_t_m"]
    kick, rec = p["toe_h_m"], p["toe_recess_m"]
    zt = H - top_t
    y0 = -D / 2 + p["front_overhang_m"]
    Htot = H + (p["case"]["h_m"] if p.get("case_on_top") else 0.0)
    top, ply, blk = P("CounterTop", "Black_Top"), P("FrontWrap", "Wrap_DeliChecker"), P("Carcass", "Black_ML1")
    if d >= 3:
        add_box(top, (L, D, top_t), (0, 0, zt + top_t / 2))
        add_box(ply, (L, D - p["front_overhang_m"], zt), (0, (y0 + D / 2) / 2, zt / 2))
    else:
        _bb(top, (L, D, top_t), (0, 0, zt + top_t / 2), d, 0.003, 0.003)
        add_box(blk, (L, 0.012, kick), (0, y0 + rec + 0.006, kick / 2))
        pw = p["ply_sheet_w_m"]
        n = max(1, round(L / pw))
        edge = P("PlyEdges", "Plywood_Edge")
        for i in range(n):  # wrapped plywood sheets with hairline seams; exposed ply edge along the top
            x = -L / 2 + (i + 0.5) * L / n
            seam = p["seam_m"] if d <= 1 else 0.0
            add_box(ply, (L / n - seam, p["ply_t_m"], zt - kick), (x, y0 + p["ply_t_m"] / 2, kick + (zt - kick) / 2))
        if d <= 1:
            add_box(edge, (L, p["ply_t_m"] + 0.001, 0.006), (0, y0 + p["ply_t_m"] / 2, zt - 0.003))
            for sx in (-1, 1):
                add_box(edge, (0.006, D - p["front_overhang_m"], zt - kick), (sx * (L / 2 - 0.003), (y0 + D / 2) / 2, kick + (zt - kick) / 2))
            add_box(blk, (L - 0.02, 0.01, zt - kick), (0, y0 + p["ply_t_m"] + 0.005, kick + (zt - kick) / 2))  # seam backer
        # staff side: open black shelves
        cd = D / 2 - (y0 + p["ply_t_m"] + 0.01)
        cy = D / 2 - cd / 2
        for z in (kick, kick + (zt - kick) / 2):
            add_box(blk, (L - 0.012, cd, 0.019), (0, cy, z + 0.0095))
        m = max(1, round(L / 0.9))
        for i in range(m + 1):
            add_box(blk, (0.019, cd, zt - kick), (-L / 2 + 0.0095 + (L - 0.019) * i / m, cy, kick + (zt - kick) / 2))
    if p.get("case_on_top"):  # placeholder only (DEC-090: no case stated)
        c = p["case"]
        _bb(P("Case", "Glass_Clear"), (L - 0.02, c["d_m"], c["h_m"]), (0, -D / 2 + c["d_m"] / 2 + 0.01, H + c["h_m"] / 2), d, 0.002, 0.001)
    boxes = [collision_box("Counter", (0, 0, H / 2), (L, D, H))]
    return (L, Htot, D), {"fixture_family": "deli_counter", "plan_rect_ft": p["plan_rect_ft"],
                          "work_surface_anchor_unity_xyz": to_unity(0, 0, H), "collision_boxes": boxes}


KINDS = {"jar_wall": jar_wall, "deli_counter": deli_counter}


def build(p, lod):
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    expected, extra = KINDS[p["kind"]](P, p, lod["detail"], lod["seg"])
    extra.update(seed=int(p["seed"]))
    extra.update(wear(p))
    return P.finish(), expected, extra
