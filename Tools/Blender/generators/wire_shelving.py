"""Chrome / black-epoxy wire shelving (PROC-005; adapted from the IMP-003 drop-1 generator).
One params file, one asset per ROOM_FIXTURES rack row (W6). Construction follows a commercial wire shelving unit:
grooved round posts (1 in groove pitch), tapered split sleeves seated in each shelf's corner collar, truss-edge shelf
frames (top + bottom rail with a zig-zag wire between), dense front-to-back deck wires on a few long support wires
(W2/C9), leveller feet or swivel casters (DEC-088). Sections share their inner posts (W5); shelf heights come from
`shelf_z_m` (W4). Component sizes are GAP-PROC-13. Origin = bottom centre, front = -Y, sizes exact to the RF row.
LOD0 full detail; LOD1 no grooves/thread/brake detail; LOD2 plain cylinders, half the deck wires, no truss;
LOD3 one block per shelf + thin post boxes."""
import math

from proclib import (Parts, add_box, add_cylinder_between, add_lathe, add_sweep, add_tube, add_vertical_cylinder,
                     circle_profile, collision_box, even_positions, to_unity, wear)


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k != "variants"}
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def shelf_levels(p):
    if p.get("shelf_z_m"):
        return list(p["shelf_z_m"])
    n, z0, z1 = p["shelf_count"], p["bottom_shelf_z_m"], p["height_m"] - p["top_shelf_drop_m"]
    return [z0 + (z1 - z0) * i / (n - 1) for i in range(n)]


def post_layout(p):
    """Post x positions and, per post, the base type. Sections that all roll or all stand share inner posts;
    mixed sections are built as abutting standalone units (a rolling middle unit pulls out on its own)."""
    W, n = p["width_m"], len(p["sections"])
    cr = p["collar_outer_d_m"] / 2
    rolls = [s["casters"] for s in p["sections"]]
    if len(set(rolls)) == 1:
        xs = [-W / 2 + cr + (W - 2 * cr) * i / n for i in range(n + 1)]
        return [(x, rolls[0]) for x in xs], [(xs[i], xs[i + 1]) for i in range(n)]
    posts, spans, sw = [], [], W / n
    for i, r in enumerate(rolls):
        a, b = -W / 2 + i * sw + cr, -W / 2 + (i + 1) * sw - cr
        posts += [(a, r), (b, r)]
        spans.append((a, b))
    return posts, spans


def grooved_post_profile(p, z0, z1, grooves):
    r, pitch, gd, gw = p["post_d_m"] / 2, p["groove_pitch_m"], p["groove_depth_m"], p["groove_width_m"]
    prof = [(0, z0), (r, z0)]
    if grooves:
        z = z0 + pitch
        while z + gw < z1 - pitch / 2:
            prof += [(r, z), (r - gd, z + gw / 2), (r, z + gw)]  # V groove: 3 rings keep the 2-section runs < 80k
            z += pitch
    return prof + [(r, z1), (0, z1)]


def build_base(parts, p, lod, x, y, rolls, finish):
    """Leveller foot or swivel caster under one post; returns the post's bottom z."""
    d, s = lod["detail"], lod["seg"]
    hw = parts("Hardware", finish)
    if not rolls:
        f = p["foot"]
        if d >= 3:
            add_box(hw, (f["pad_d_m"], f["pad_d_m"], f["height_m"]), (x, y, f["height_m"] / 2))
            return f["height_m"]
        pad = parts("FootPads", "Plastic_Black")
        ph = f["pad_h_m"]
        add_lathe(pad, (x, y, 0), (0, 0, 1), [(0, 0), (f["pad_d_m"] / 2 * 0.92, 0), (f["pad_d_m"] / 2, ph * 0.35),
                                              (f["pad_d_m"] / 2 * 0.8, ph), (0, ph)], s)
        stem_top = f["height_m"] - f["nut_h_m"]
        prof = [(0, ph), (f["stem_d_m"] / 2, ph)]
        if d == 0:  # thread crests
            z = ph + 0.002
            while z < stem_top - 0.002:
                prof += [(f["stem_d_m"] / 2 * 0.9, z), (f["stem_d_m"] / 2, z + 0.0008)]
                z += 0.0016
        add_lathe(hw, (x, y, 0), (0, 0, 1), prof + [(f["stem_d_m"] / 2, stem_top), (0, stem_top)], s)
        add_lathe(hw, (x, y, 0), (0, 0, 1), [(0, stem_top), (f["nut_af_m"] / 2, stem_top),  # hex leveller nut
                                             (f["nut_af_m"] / 2, f["height_m"]), (0, f["height_m"])], 6)
        return f["height_m"]
    c = p["caster"]
    R, wd, top = c["wheel_d_m"] / 2, c["wheel_w_m"], c["height_m"]
    cy = y - math.copysign(c["trail_m"], y)  # swivel trail points inward so the wheel stays in the footprint
    whl = parts("CasterWheels", "Rubber_Grey")
    if d >= 3:
        add_box(hw, (wd * 1.6, c["race_d_m"], top - R * 2), (x, y, R * 2 + (top - R * 2) / 2))  # swivel block, inside the collar
        add_box(whl, (wd, R * 2, R * 2), (x, cy, R))
        return top
    ws = s * 2 if d == 0 else s
    tread = [(0, -wd / 2), (R * 0.55, -wd / 2), (R * 0.93, -wd / 2), (R, -wd * 0.32), (R, wd * 0.32),
             (R * 0.93, wd / 2), (R * 0.55, wd / 2), (0, wd / 2)]
    if d == 0:  # recessed hub faces
        tread = [(0, -wd * 0.38), (R * 0.5, -wd * 0.38), (R * 0.58, -wd / 2)] + tread[2:6] + \
                [(R * 0.58, wd / 2), (R * 0.5, wd * 0.38), (0, wd * 0.38)]
    add_lathe(whl, (x, cy, R), (1, 0, 0), tread, ws)
    fork_t, fork_top = c["fork_t_m"], R * 2 + 0.006
    for sx in (-1, 1):  # fork legs: bent plate from the swivel down to the axle
        fx = x + sx * (wd / 2 + fork_t / 2 + 0.0015)
        add_sweep(hw, [(fx, cy, R), (fx, cy, fork_top - 0.004), (fx, y, fork_top)],
                  # profile (u, v): on a +Z path u = -Y and v = +X (proclib._basis), so plate width on Y, thickness on X
                  [(-R * 0.45, -fork_t / 2), (R * 0.45, -fork_t / 2), (R * 0.45, fork_t / 2), (-R * 0.45, fork_t / 2)])
        if d <= 1:
            add_cylinder_between(hw, (fx + sx * fork_t / 2, cy, R), (fx + sx * (fork_t / 2 + 0.003), cy, R), 0.005, s)
    add_cylinder_between(hw, (x - wd / 2 - fork_t, cy, R), (x + wd / 2 + fork_t, cy, R), 0.003, s)  # axle
    add_box(hw, (wd + 2 * fork_t + 0.006, R * 1.1, 0.004), (x, (y + cy) / 2, fork_top))  # fork yoke
    race = [(0, fork_top), (c["race_d_m"] / 2, fork_top), (c["race_d_m"] / 2, fork_top + 0.004),
            (c["race_d_m"] / 2 * 0.8, fork_top + 0.006), (c["race_d_m"] / 2, fork_top + 0.008),
            (c["race_d_m"] / 2, fork_top + 0.012), (0, fork_top + 0.012)]
    add_lathe(hw, (x, y, 0), (0, 0, 1), race if d == 0 else [race[0], race[1], race[-2], race[-1]], s)
    add_vertical_cylinder(hw, x, y, fork_top + 0.012, top, c["stem_d_m"] / 2, s)
    if c.get("brake") and y < 0 and d <= 1:  # foot brake pedal on the front casters, reaching inward over the wheel
        sg = math.copysign(1, y)
        add_sweep(hw, [(x, cy - sg * R * 0.2, fork_top), (x, cy - sg * R * 1.05, R * 1.55)],
                  [(0.008, -0.0015), (0.008, 0.0015), (-0.008, 0.0015), (-0.008, -0.0015)])
    return top


def build(p, lod):
    d, s = lod["detail"], lod["seg"]
    W, D, H = p["width_m"], p["depth_m"], p["height_m"]
    finish = p["finish"]
    parts = Parts(p["colors"])
    cr = p["collar_outer_d_m"] / 2
    ys = (-D / 2 + cr, D / 2 - cr)
    posts, spans = post_layout(p)
    levels = shelf_levels(p)
    fh, rr = p["frame_h_m"], p["rail_d_m"] / 2
    boxes = []

    for x, rolls in posts:
        for y in ys:
            zb = build_base(parts, p, lod, x, y, rolls, finish)
            post = parts("Posts", finish)
            if d >= 3:
                add_box(post, (p["post_d_m"], p["post_d_m"], H - zb), (x, y, zb + (H - zb) / 2))
                continue
            cap_h = p["cap_h_m"]
            add_lathe(post, (x, y, 0), (0, 0, 1), grooved_post_profile(p, zb, H - cap_h, d == 0), lod["post_seg"])
            cap = parts("PostCaps", "Plastic_Black")
            r = p["post_d_m"] / 2
            add_lathe(cap, (x, y, 0), (0, 0, 1), [(0, H - cap_h), (r + 0.0012, H - cap_h), (r + 0.0012, H - cap_h * 0.3),
                                                  (r * 0.7, H), (0, H)], s)
            boxes.append(collision_box("Post", (x, y, (zb + H) / 2), (p["post_d_m"], p["post_d_m"], H - zb)))

    shelves, coll, slv = parts("Shelves", finish), parts("Collars", finish), parts("Sleeves", "Plastic_Grey")
    anchors = []
    for si, (xa, xb) in enumerate(spans):
        sw = xb - xa
        xm = (xa + xb) / 2
        for li, z in enumerate(levels):
            boxes.append(collision_box(f"Shelf_{si}_{li}", (xm, 0, z - fh / 2), (sw + 2 * cr, D, fh)))
            anchors.append({"id": f"S{si}_Shelf_{li:02d}", "position_unity_xyz": to_unity(xm, 0, z),
                            "size_m_unity_xz": [round(sw - 2 * cr, 5), round(D - 4 * cr, 5)]})  # H2: inside the collars
            if d >= 3:
                add_box(shelves, (sw + 2 * cr, D, fh), (xm, 0, z - fh / 2))  # silhouette = collar extents, like the collision box
                continue
            x0, x1, y0, y1 = xa + cr * 0.8, xb - cr * 0.8, ys[0] + cr * 0.8, ys[1] - cr * 0.8
            zt, zbr = z - rr, z - fh + rr
            # perimeter rails, top and bottom, each a closed rounded loop through the collars
            for zz in (zt, zbr) if d <= 1 else (zt,):
                add_tube(shelves, [(x0, y0, zz), (x1, y0, zz), (x1, y1, zz), (x0, y1, zz)], rr, s, closed=True)
            if d <= 1:  # truss: zig-zag between the rails on all four sides
                for a, b in (((x0, y0), (x1, y0)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0)), ((x1, y0), (x1, y1))):
                    L = math.dist(a, b)
                    n = max(2, round(L / p["truss_pitch_m"]) * 2)
                    pts = [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n, zt if i % 2 else zbr) for i in range(n + 1)]
                    add_tube(shelves, pts, p["truss_d_m"] / 2, 6)  # 3.5 mm wire: 6 sides, like the deck wires
            # deck: dense front-to-back wires sitting on the top rail, on long support wires underneath (W2/C9)
            wd = p["deck_wire_d_m"] / 2
            pitch = p["deck_pitch_m"] * (2 if d >= 2 else 1)
            for xx in even_positions(x1 - x0 - 2 * rr, pitch):
                add_cylinder_between(shelves, (xm + xx, y0, z - wd), (xm + xx, y1, z - wd), wd, 6)
            for yy in even_positions(y1 - y0 - 0.06, (y1 - y0 - 0.06) / max(1, p["support_wires"] - 1)):
                add_cylinder_between(shelves, (x0, yy, z - 2 * wd - rr * 0.8), (x1, yy, z - 2 * wd - rr * 0.8), rr * 0.8, 6)
            # corner collars (tapered, wrapping the post) with the split sleeve's lip showing underneath
            for xx in (xa, xb):
                for yy in ys:
                    pr = p["post_d_m"] / 2
                    ch = p["collar_h_m"]
                    add_lathe(coll, (xx, yy, 0), (0, 0, 1), [(pr + 0.0004, z - ch), (cr * 0.86, z - ch), (cr, z - 0.002),
                                                             (cr * 0.97, z), (pr + 0.0004, z), (pr + 0.0004, z - ch)],
                              s * (2 if d == 0 else 1))
                    if d <= 1:
                        add_lathe(slv, (xx, yy, 0), (0, 0, 1), [(pr + 0.0002, z - ch - p["sleeve_lip_m"]),
                                                                (cr * 0.8, z - ch - p["sleeve_lip_m"]), (cr * 0.84, z - ch),
                                                                (pr + 0.0002, z - ch), (pr + 0.0002, z - ch - p["sleeve_lip_m"])], s)
    extra = {"fixture_family": "wire_shelving", "rf": p["rf"], "seed": int(p["seed"]), "shelf_anchors": anchors,
             "collision_boxes": boxes, "sections": [dict(s_, span_unity_x=[to_unity(a, 0, 0)[0], to_unity(b, 0, 0)[0]])
                                                    for s_, (a, b) in zip(p["sections"], spans)]}
    extra.update(wear(p))
    return parts.finish(), (W, H, D), extra
