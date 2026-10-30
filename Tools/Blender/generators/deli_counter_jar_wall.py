"""Deli jar walls (PROC-005 fix wave; REVIEW-PROC5 #1/#3/#4/#7). Three variants, one per RF row (RI §8.3):
- North (RF DeliJarWall_North): black back counter with walnut two-row drawers and silver cup pulls (DEC-043 photo,
  probably this wall), 2 dark-grey sheet-metal shelf tiers on slotted black standards + knife brackets, backlit teal
  panel, green/black checker tile band at the top (RI §2.4).
- South (RF DeliJarWall_South): black back counter with open bins under it (BAND_10), black shelves (BAND_01).
- East (RF DeliJarWall_East): black counter over open cubbies, backlit teal shelves in arched wood frames with warm
  LED strips (BAND_11).
Depth = RF 2.1 ft (North) / 2.0 ft (South, East; REF-013) including the back counter. The deli counter L was dropped: it is the south register run
(RI §1.5 row 101, §8.1). Every size/count/colour is cited in the params `_src` maps or carries a GAP id.
Jar slots (game anchors, bottom centre) on the counter row and each jar tier; the top display board has none.
Origin = bottom centre, customer side = -Y, wall = +Y."""
import math

from proclib import (Parts, add_beveled_box, add_box, add_cylinder_between, add_screw_head, add_sweep,
                     collision_box, fillet, rect_profile, to_unity, wear)


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def _bb(bm, size, center, d, corner=0.002, bevel=0.0012):
    """Bevelled box at LOD0/1, plain box below."""
    if d >= 2:
        add_box(bm, size, center)
    else:
        add_beveled_box(bm, size, center, corner=corner, bevel=bevel, seg=2 if d == 0 else 1)


def _xbox(bm, x0, x1, y0, y1, z0, z1, d=2, corner=0.002, bevel=0.0012):
    _bb(bm, (x1 - x0, y1 - y0, z1 - z0), ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), d, corner, bevel)


def _side(bm, x0, x1, prof):
    """Plate of thickness x1-x0 with a (y, z) outline (CCW): brackets, bin sides."""
    add_sweep(bm, [(x0, 0, 0), (x1, 0, 0)], prof)


# --- base cabinet ------------------------------------------------------------------------------------------------

def _carcass(P, p, d, L, yc, yb, zt, dividers):
    """Black carcass: notched gables, recessed toe kick, deck, back; dividers at the given x; returns inner x spans."""
    kick, rec, t = p["toe_h_m"], p["toe_recess_m"], 0.019
    blk = P("Carcass", "Black_ML1")
    for sx in (-1, 1):  # gables with the toe-kick notch
        x0, x1 = sorted((sx * L / 2, sx * (L / 2 - t)))
        _xbox(blk, x0, x1, yc, yb, kick, zt, d, 0.0015, 0.001)
        _xbox(blk, x0, x1, yc + rec, yb, 0, kick, d, 0.0015, 0.001)
    _xbox(blk, -L / 2 + t, L / 2 - t, yc + rec, yc + rec + 0.016, 0, kick, d, 0.001, 0.0008)  # toe kick board
    _xbox(blk, -L / 2 + t, L / 2 - t, yc, yb, kick, kick + t)  # deck
    _xbox(blk, -L / 2 + t, L / 2 - t, yb - 0.006, yb, kick + t, zt)  # cabinet back
    for x in dividers:
        _xbox(blk, x - t / 2, x + t / 2, yc, yb - 0.006, kick + t, zt, d, 0.001, 0.0008)
    edges = [-L / 2 + t] + [x for xd in dividers for x in (xd - t / 2, xd + t / 2)] + [L / 2 - t]
    return list(zip(edges[::2], edges[1::2]))


def _cup_pull(bm, x, y, z, w, seg):
    """Silver cup (bin) pull: back plate with screw heads + hollow half-round hood open at the bottom."""
    _xbox(bm, x - w / 2 - 0.006, x + w / 2 + 0.006, y - 0.003, y, z - 0.012, z + 0.016, 0, 0.004, 0.0012)
    R, t, n = 0.016, 0.0018, max(4, seg // 2)
    angs = [math.radians(90 + 140 * i / n) for i in range(n + 1)]  # top -> front -> lower front
    yc, zc = y - 0.003, z
    outer = [(yc + R * math.cos(a), zc + R * math.sin(a) - R * 0.55) for a in angs]
    inner = [(yc + (R - t) * math.cos(a), zc + (R - t) * math.sin(a) - R * 0.55) for a in reversed(angs)]
    add_sweep(bm, [(x - w / 2, 0, 0), (x + w / 2, 0, 0)], outer + inner)  # crescent, CCW in (y, z)
    for sx in (-1, 1):
        add_screw_head(bm, (x + sx * (w / 2 + 0.002), y - 0.003, z + 0.008), (0, -1, 0), 0.0025, 8)


def _drawers(P, p, d, s, L, yc, yb, zt):
    kick, rv, t = p["toe_h_m"], 0.004, 0.019
    cols = max(1, round(L / p["drawer_w_m"]))
    cw = (L - 2 * t) / cols
    _carcass(P, p, d, L, yc, yb, zt, [] if d >= 2 else [-L / 2 + t + cw * i for i in range(1, cols)])
    blk, wal = P("Carcass", "Black_ML1"), P("DrawerFronts", "Walnut_WD1")
    _xbox(blk, -L / 2 + t, L / 2 - t, yc + t, yc + t + 0.004, kick + t, zt)  # face backer behind the reveals
    rows, z0 = p["drawer_rows"], kick + t
    rh = (zt - 0.006 - z0) / rows
    for i in range(cols):
        for r in range(rows):
            x0, zb = -L / 2 + t + i * cw, z0 + r * rh
            xm, zm = x0 + cw / 2, zb + rh / 2
            _xbox(wal, x0 + rv / 2, x0 + cw - rv / 2, yc, yc + t, zb + rv / 2, zb + rh - rv / 2, d, 0.0025, 0.0018)
            if d == 0:
                _cup_pull(P("Pulls", "Silver"), xm, yc, zb + rh * 0.72, p["pull_w_m"], s)
            elif d == 1:
                add_cylinder_between(P("Pulls", "Silver"), (xm - p["pull_w_m"] / 2, yc - 0.008, zb + rh * 0.72),
                                     (xm + p["pull_w_m"] / 2, yc - 0.008, zb + rh * 0.72), 0.007, 8)


def _bin(bm, x0, x1, y0, y1, z0, h, d):
    """Open-front hopper bin (stacking pick bin): hopper sides, floor, back, low front lip with a label slot."""
    w, t = 0.002, 0.0025
    prof = [(y0, z0), (y1, z0), (y1, z0 + h), (y0 + (y1 - y0) * 0.35, z0 + h), (y0, z0 + h * 0.45)]
    if d >= 1:
        _xbox(bm, x0, x1, y0, y1, z0, z0 + h * 0.45)
        _xbox(bm, x0, x1, y0 + (y1 - y0) * 0.35, y1, z0 + h * 0.45, z0 + h)
        return
    for xa, xb in ((x0, x0 + t), (x1 - t, x1)):
        _side(bm, xa, xb, prof)
    _xbox(bm, x0 + t, x1 - t, y0, y1, z0, z0 + t)
    _xbox(bm, x0 + t, x1 - t, y1 - t, y1, z0 + t, z0 + h)
    _xbox(bm, x0 + t, x1 - t, y0, y0 + t, z0 + t, z0 + h * 0.45, 0, 0.001, 0.0008)
    _xbox(bm, x0 + 0.015, x1 - 0.015, y0 - w, y0, z0 + h * 0.12, z0 + h * 0.36, 0, 0.0008, 0.0004)  # label slot


def _open_base(P, p, d, L, yc, yb, zt, module_w, bins):
    kick, t = p["toe_h_m"], 0.019
    n = max(1, round((L - 2 * t) / module_w))
    mw = (L - 2 * t) / n
    spans = _carcass(P, p, d, L, yc, yb, zt, [-L / 2 + t + mw * i for i in range(1, n)])
    blk, edge = P("Carcass", "Black_ML1"), P("EdgeBand", "Black_ML1")
    zm = kick + t + (zt - kick - t) / 2
    for x0, x1 in spans:
        _xbox(blk, x0, x1, yc, yb - 0.006, zm - t / 2, zm + t / 2, d, 0.001, 0.0008)  # middle shelf
        if d == 0:  # edge banding on the shelf nose
            _xbox(edge, x0, x1, yc - 0.0012, yc, zm - t / 2, zm + t / 2, 0, 0.0004, 0.0003)
    if d == 0:
        for x in [-L / 2 + t / 2] + [-L / 2 + t + mw * i for i in range(1, n)] + [L / 2 - t / 2]:
            _xbox(edge, x - t / 2, x + t / 2, yc - 0.0012, yc, kick, zt, 0, 0.0004, 0.0003)
    if not bins or d >= 3:
        return
    bm, k = P("Bins", "Plastic_Bin"), p["bins_per_module"]
    for x0, x1 in spans:
        bw = (x1 - x0) / k
        for z0 in (kick + t, zm + t / 2):
            h = min(0.15, zt - z0 - 0.04)
            if d >= 2:
                _xbox(bm, x0 + 0.004, x1 - 0.004, yc + 0.01, yb - 0.04, z0, z0 + h * 0.8)
                continue
            for j in range(k):
                _bin(bm, x0 + j * bw + 0.004, x0 + (j + 1) * bw - 0.004, yc + 0.01, yb - 0.04, z0, h, d)


def _counter(P, p, d, s, L, D, yb):
    ch, top_t, ov = p["counter_h_m"], p["counter_top_t_m"], p["counter_overhang_m"]
    zt, yc = ch - top_t, -D / 2 + ov
    if d >= 3:
        _xbox(P("Carcass", "Black_ML1"), -L / 2, L / 2, yc + p["toe_recess_m"], yb, 0, zt)
    elif p["base"] == "drawers":
        _drawers(P, p, d, s, L, yc, yb, zt)
    else:
        mw = p["base_module_w_m"] if p["base"] == "bins" else L / p["bays"]
        _open_base(P, p, d, L, yc, yb, zt, mw, p["base"] == "bins")
    _xbox(P("CounterTop", "Black_Top"), -L / 2, L / 2, -D / 2, yb, zt, ch, d, 0.004, 0.003)
    return ch


# --- wall: bracket shelving (North / South) ----------------------------------------------------------------------

def _standard(P, p, d, x, yb, z0, z1):
    """Twin-flange slotted standard (1 in), screwed through the slots; backer keeps the backlight out of the slots."""
    blk, w, dep = P("Standards", "Black_ML1"), p["standard_w_m"], 0.016
    if d >= 1:
        _xbox(blk, x - w / 2, x + w / 2, yb - dep, yb, z0, z1, d, 0.001, 0.0008)
        return
    f, sw, pitch, sh = 0.0025, 0.006, 0.0254, 0.0127
    for xa, xb in ((x - w / 2, x - sw / 2), (x + sw / 2, x + w / 2)):
        _xbox(blk, xa, xb, yb - dep, yb, z0, z1, 0, 0.0008, 0.0006)
    _xbox(blk, x - sw / 2, x + sw / 2, yb - 0.002, yb, z0, z1)
    n = int((z1 - z0 - 0.02) // pitch)
    zz = z0 + 0.01
    for i in range(n):
        _xbox(blk, x - sw / 2, x + sw / 2, yb - dep, yb - dep + f, zz + i * pitch + sh, zz + (i + 1) * pitch)
    for z in (z0 + 0.06, (z0 + z1) / 2, z1 - 0.06):
        zs = zz + round((z - zz) / pitch) * pitch + sh / 2
        add_screw_head(P("Screws", "Black_ML1"), (x, yb - dep + f, zs), (0, -1, 0), 0.0045, 8)


def _bracket(P, d, x, yb, sd, z0):
    """Knife bracket under the shelf, hooked into the standard."""
    prof = [(yb - 0.82 * sd, z0 - 0.014), (yb - 0.003, z0 - 0.15), (yb - 0.003, z0), (yb - 0.82 * sd, z0)]
    _side(P("Brackets", "Black_ML1"), x - 0.0015, x + 0.0015, prof)


def _sheet_shelf(P, mat, d, x0, x1, yb, sd, z, st, lip):
    """Bent sheet shelf: hemmed front lip, deck, rear up-flange (profile in y, z)."""
    yf, ye, z0 = yb - sd, yb - 0.002, z - st
    sh = P("Shelves", mat)
    if d >= 2:
        add_box(sh, (x1 - x0, ye - yf, st), ((x0 + x1) / 2, (yf + ye) / 2, z - st / 2))
        add_box(sh, (x1 - x0, st * 2, lip), ((x0 + x1) / 2, yf + st, z0 + lip / 2))
        return
    hem = [(yf + st, z0 + lip - 0.008), (yf + 2 * st, z0 + lip - 0.008), (yf + 2 * st, z0 + lip)] if d == 0 else \
          [(yf + st, z0 + lip)]
    prof = [(yf, z0), (ye, z0), (ye, z + 0.02), (ye - st, z + 0.02), (ye - st, z), (yf + st, z)] + hem + [(yf, z0 + lip)]
    add_sweep(sh, [(x0, 0, 0), (x1, 0, 0)], prof)


def _bracket_wall(P, p, d, L, yb, ch, ztop, zs):
    sd, st, lip = p["shelf_depth_m"], p["shelf_t_m"], p["shelf_lip_m"]
    n = max(1, round((L - 0.1) / p["standard_pitch_m"]))
    xs = [-L / 2 + 0.05 + (L - 0.1) * i / n for i in range(n + 1)]
    for x in xs:
        if d <= 2:
            _standard(P, p, d, x, yb, ch + 0.05, ztop - 0.03)
    ends = [-L / 2 + 0.004] + xs[1:-1] + [L / 2 - 0.004]
    for z in zs:
        if d >= 3:
            add_box(P("Shelves", p["shelf_color"]), (L - 0.008, sd, lip), (0, yb - sd / 2, z - st + lip / 2))
            continue
        seams = [(a + (0.0015 if i else 0), b - (0.0015 if i < len(ends) - 2 else 0)) for i, (a, b) in enumerate(zip(ends, ends[1:]))]
        for a, b in (seams if d <= 1 else [(ends[0], ends[-1])]):
            _sheet_shelf(P, p["shelf_color"], d, a, b, yb, sd, z, st, lip)
        if d <= 1:
            for x in xs:
                _bracket(P, d, x, yb, sd, z - st)


def _panel(P, p, d, L, D, yb, z0, z1, joints):
    """Backlit panel in a black trim frame; joints = x of vertical panel seams (covered by trim battens)."""
    add_box(P("BackPanel", p["panel_color"]), (L, D / 2 - yb, z1 - z0), (0, (yb + D / 2) / 2, (z0 + z1) / 2))
    if d >= 2:
        return
    tr, w, f = P("PanelTrim", "Black_ML1"), 0.025, 0.006
    _xbox(tr, -L / 2, L / 2, yb - f, yb, z0, z0 + w, d, 0.001, 0.001)
    _xbox(tr, -L / 2, L / 2, yb - f, yb, z1 - w, z1, d, 0.001, 0.001)
    for x in [-L / 2 + w / 2, L / 2 - w / 2] + list(joints):
        _xbox(tr, x - w / 2, x + w / 2, yb - f, yb, z0 + w, z1 - w, d, 0.001, 0.001)


def _checker(P, p, d, L, D, yb, z0, z1):
    tile, t = p["checker_tile_m"], 0.008
    add_box(P("CheckerGrout", "Black_ML1"), (L, D / 2 - yb + t - 0.002, z1 - z0), (0, (yb - t + 0.002 + D / 2) / 2, (z0 + z1) / 2))
    if d >= 2:
        add_box(P("CheckerTiles", "Tile_Checker"), (L, 0.002, z1 - z0 - 0.004), (0, yb - t + 0.001, (z0 + z1) / 2))
        return
    nx, nz = max(1, round(L / tile)), max(1, round((z1 - z0) / tile))
    tw, th, g = L / nx, (z1 - z0) / nz, 0.0015
    for i in range(nx):
        for j in range(nz):
            bm = P("CheckerTiles", "Tile_Checker") if (i + j) % 2 == 0 else P("CheckerTilesBlack", "Tile_Black")
            x0, zb = -L / 2 + i * tw, z0 + j * th
            _bb(bm, (tw - g, t - 0.002, th - g), (x0 + tw / 2, yb - t / 2 - 0.001, zb + th / 2), d, 0.0015, 0.001)


# --- wall: arched wood bays (East) -------------------------------------------------------------------------------

def _arched_wall(P, p, d, L, D, yb, ch, H, zs):
    nb, fw, r, sd, bt = p["bays"], p["frame_w_m"], p["arch_r_m"], p["shelf_depth_m"], p["board_t_m"]
    bw, fd = L / nb, sd + 0.03
    _panel(P, p, 2, L, D, yb, ch, H, [])
    wood, brd = P("ArchFrames", "Wood_ArchFrame"), P("ShelfBoards", "Board_EastShelf")
    yF = yb - fd / 2
    for i in range(nb):
        x0, x1 = -L / 2 + i * bw, -L / 2 + (i + 1) * bw
        if d <= 1:  # U-frame with rounded arch corners, swept from the counter top
            path = [(x0 + fw / 2, yF, ch), (x0 + fw / 2, yF, H - fw / 2), (x1 - fw / 2, yF, H - fw / 2), (x1 - fw / 2, yF, ch)]
            add_sweep(wood, fillet(path, r + fw / 2, 6 if d == 0 else 3), rect_profile(fd, fw, 0.006 if d == 0 else 0.0, 2 if d == 0 else 0))
        elif d == 2:
            _xbox(wood, x0, x0 + fw, yb - fd, yb, ch, H)
            _xbox(wood, x1 - fw, x1, yb - fd, yb, ch, H)
            _xbox(wood, x0 + fw, x1 - fw, yb - fd, yb, H - fw, H)
        for z in zs:
            if d >= 3:
                add_box(brd, (bw - 2 * fw, sd, bt), ((x0 + x1) / 2, yb - sd / 2, z - bt / 2))
                continue
            _xbox(brd, x0 + fw, x1 - fw, yb - sd, yb, z - bt, z, d, 0.002, 0.0015)
            if d <= 1:  # LED channel + diffuser under the nose, cleats on the frame legs
                _xbox(brd, x0 + fw + 0.01, x1 - fw - 0.01, yb - sd + 0.012, yb - sd + 0.03, z - bt - 0.008, z - bt, d, 0.001, 0.0006)
                _xbox(P("LED", "LED_Emissive"), x0 + fw + 0.012, x1 - fw - 0.012, yb - sd + 0.014, yb - sd + 0.028, z - bt - 0.0095, z - bt - 0.008)
                for xa, xb in ((x0 + fw, x0 + fw + 0.012), (x1 - fw - 0.012, x1 - fw)):
                    _xbox(wood, xa, xb, yb - sd + 0.03, yb - 0.004, z - bt - 0.03, z - bt, d, 0.0015, 0.001)


# --- assembly ----------------------------------------------------------------------------------------------------

def _slots(p, L, yb, tiers, bays=None):
    sd, jp, m = p["shelf_depth_m"], p["jar_pitch_m"], p["jar_end_margin_m"]
    spans = [(-L / 2, L / 2)] if not bays else [(-L / 2 + i * L / bays + p["frame_w_m"], -L / 2 + (i + 1) * L / bays - p["frame_w_m"]) for i in range(bays)]
    out = []
    for ti, z in enumerate(tiers):
        y = yb - (sd if ti else p["counter_slot_depth_m"]) / 2
        k = 0
        for a, b in spans:
            n = int((b - a - 2 * m) // jp) + 1 if b - a - 2 * m >= 0 else 0
            for i in range(n):
                x = (a + b) / 2 - (n - 1) * jp / 2 + i * jp
                out.append({"id": f"Jar_T{ti}_{k:02d}", "tier": ti, "position_unity_xyz": to_unity(x, y, z)})
                k += 1
    return out


def build(p, lod):
    d, s = lod["detail"], lod["seg"]
    P = Parts(p["colors"], wear_attr=bool(p.get("pbr")))
    L, D, H = p["length_m"], p["depth_m"], p["height_m"]
    pt = p["back_panel_t_m"]
    yb = D / 2 - pt
    ch = _counter(P, p, d, s, L, D, yb)
    zs = [ch + p["shelf_pitch_m"] * (i + 1) for i in range(p["boards"])]
    band = p["checker_band_h_m"] if p.get("checker_band") else 0.0
    if p["shelves"] == "arched":
        _arched_wall(P, p, d, L, D, yb, ch, H, zs)
    else:
        n = max(1, round((L - 0.1) / p["standard_pitch_m"]))
        # panel seams at every second standard, covered by trim battens (construction)
        joints = [] if d >= 2 else [-L / 2 + 0.05 + (L - 0.1) * i / n for i in range(1, n)][1::2]
        _panel(P, p, d, L, D, yb, ch, H - band, joints)
        if band:
            _checker(P, p, d, L, D, yb, H - band, H)
        _bracket_wall(P, p, d, L, yb, ch, H - band, zs)
    tiers = [ch] + zs[:p["jar_tiers"]]
    slots = _slots(p, L, yb, tiers, p["bays"] if p["shelves"] == "arched" else None)
    sd = p["shelf_depth_m"]
    boxes = [collision_box("Counter", (0, (yb - D / 2) / 2, ch / 2), (L, yb + D / 2, ch)),
             collision_box("BackPanel", (0, D / 2 - pt / 2, ch + (H - ch) / 2), (L, pt, H - ch))]
    boxes += [collision_box(f"Shelf_{i}", (0, yb - sd / 2, z - 0.01), (L, sd, 0.02)) for i, z in enumerate(zs)]
    jw, jh, jd = p["jar_slot_m"]
    extra = {"fixture_family": "jar_wall", "rf_fixture": p["rf"], "jar_asset_id": p["jar_asset_id"],
             "jar_slot_size_m_unity_xyz": [jw, jh, jd], "jar_slots": slots, "jar_slot_count": len(slots),
             "emissive_parts": ["BackPanel", "LED"] if p["panel_color"] == "Teal_Backlit" else [], "collision_boxes": boxes, "seed": int(p["seed"])}
    extra.update(wear(p))
    return P.finish(), (L, H, D), extra
