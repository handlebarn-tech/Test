"""Door family (PROC-013): every type in Docs/Reference/DOORS.json (storefrontPair, swing, opening, foldingGrille).
Door facts are read live from DOORS.json; params/doors.json holds construction values and labelled GAP placeholders.

Assets per DOORS.json row (asset id PROC_Door_<id>_<Part>):
  Frame          jambs + head (+ stop, threshold, strike, silencers) or the arch lining. Origin = opening centre on the
                 wall centreline at floor level. Unity local +X runs hinge->latch of the single / L leaf, so the frame's
                 yaw is that leaf's DOORS.json closedRotation; Unity local Z is the wall normal. The manifest gives the
                 rough opening (what ART-013 cuts the wall to) and each leaf's hinge pivot in frame-local Unity coords.
  Leaf / LeafL / LeafR   one leaf. Origin = its hinge axis at floor level (the DOORS.json '<object>_Hinge' pivot); the
                 leaf extends along Unity local +X from hinge to latch and swings about local +Y by openAngle.
  Grille         the unplaced 101B side-folding grille, extended, origin bottom centre.

Blender frame (metres, Z up): Unity X = -Blender x, Unity Z = -Blender y. sw = Blender y sign of the swing side
(openAngle > 0 swings toward Unity -Z = Blender +y).
Sheets: blender -b --factory-startup --python-exit-code 10 -P Tools/Blender/generators/doors.py -- sheets
"""
import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(HERE) not in sys.path:
    sys.path.insert(0, os.path.dirname(HERE))
from proclib import (FT, INCH, Parts, add_beveled_box, add_box, add_cylinder_between, add_sweep, add_tube,  # noqa: E402
                     collision_box, fillet, to_unity, wear)

ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
E_AXIS = 0.003  # hinge axis sits this far outside the leaf's hinge edge (in the edge gap), on the swing face


def _load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def variants(p):
    rows = {r["id"]: r for r in _load(p["doors_json"])["doors"]}
    walls = {w["id"]: w["t"] for w in _load(p["graybox_json"])["walls"]}
    for i, d in enumerate(p["doors"]):
        row = rows[d["id"]]
        q = {k: v for k, v in p.items() if k != "doors"}
        q.update(d)
        q["row"], q["seed"] = row, p["seed"] + i
        q["wall_t_m"] = walls[row["graybox_wall"]] * FT if row.get("graybox_wall") else None
        fp = q.get(d["family"], {})
        q["gaps"] = sorted(set(p["gaps"]) | set(row.get("gap") or []) | set(d.get("gaps", [])) | set(fp.get("gaps", [])))
        if row["type"] == "foldingGrille":
            parts = ["Grille"]
        elif row["type"] == "opening":
            parts = ["Frame"]
        elif row["leaves"] == 2:
            parts = ["Frame", "LeafL", "LeafR"]
        else:
            parts = ["Frame", "Leaf"]
        for part in parts:
            extra = {"tri_guide": p["leaf_tri_guide"]} if part.startswith("Leaf") else {}
            yield p["asset_prefix"] + d["id"] + "_" + part, dict(q, part=part, **extra)


# --- door data derived from the DOORS.json row ----------------------------------------------------------------------

def fam(p):
    return {k: (v * INCH if k.endswith("_in") and not isinstance(v, list) else v) for k, v in p[p["family"]].items()}


def leaves(p):
    """[(asset part, DOORS leaf dict)] in L, R order; single doors use the row itself."""
    row = p["row"]
    if row["leaves"] == 2:
        return [("LeafL", row["leafObjects"][0]), ("LeafR", row["leafObjects"][1])]
    return [("Leaf", {"object": row["object"], "pivot": row["pivot"], "leafWidth_ft": row["leafWidth_ft"],
                      "closedRotation": row["closedRotation"], "openAngle": row["openAngle"]})]


def geom(p):
    """Frame-local layout shared by the frame and leaf builders."""
    f, row = fam(p), p["row"]
    W = [lf["leafWidth_ft"] * FT for _, lf in leaves(p)]
    H = row["leafHeight_ft"] * FT
    sw = 1 if leaves(p)[0][1]["openAngle"] > 0 else -1
    D = max((p["wall_t_m"] or 0) + 2 * f["frame_proud_in"], f["frame_min_depth_in"])
    Wt = sum(W)
    Wo = Wt + 2 * f["edge_gap_in"]                      # soffit to soffit
    z0 = f["undercut_in"]
    Ho = z0 + H + f["head_gap_in"]                      # head soffit height
    y_sf = sw * (D / 2 - f["rabbet_inset_in"])          # leaf swing face (closed)
    y_pf = y_sf - sw * f["leaf_t_in"]                   # leaf push face (closed)
    y_h = y_sf + sw * hinge_off(f)
    piv = [(Wt / 2 + E_AXIS, y_h, 0.0)]
    if len(W) == 2:
        piv.append((-(Wt / 2 + E_AXIS), y_h, 0.0))
    return {"f": f, "W": W, "H": H, "sw": sw, "D": D, "Wt": Wt, "Wo": Wo, "z0": z0, "Ho": Ho, "y_sf": y_sf,
            "y_pf": y_pf, "piv": piv, "RO": (Wo + 2 * f["frame_face_in"], Ho + f["frame_face_in"], D)}


def hinge_off(f):
    return f["hinge_barrel_d_in"] / 2 * 0.6  # knuckle axis just outside the swing face


# --- small geometry helpers -----------------------------------------------------------------------------------------

def box(bm, d, x0, x1, y0, y1, z0, z1, r=0.0015):
    """Axis-aligned box from bounds; bevelled (manufactured) at LOD0/1, plain below."""
    size = (abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))
    c = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    if d <= 1 and r > 0 and min(size) > 4 * r:
        add_beveled_box(bm, size, c, corner=r, bevel=r * 0.6, seg=2 if d == 0 else 1)
    else:
        add_box(bm, size, c)


def box_rot(bm, size, center, ry):
    verts = add_box(bm, size)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(center) @ Matrix.Rotation(ry, 4, "Y"), verts=verts)


def prism_y(bm, pts_xz, y0, y1):
    """Extrude a convex-or-simple (x, z) polygon across y0..y1."""
    a = [bm.verts.new((x, y0, z)) for x, z in pts_xz]
    b = [bm.verts.new((x, y1, z)) for x, z in pts_xz]
    n = len(pts_xz)
    bm.faces.new(a[::-1])
    bm.faces.new(b)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([a[i], a[j], b[j], b[i]])


def chamfer(pts, idx, c):
    """Replace the corners at idx by two points c from the corner (a 45 deg chamfer)."""
    out = []
    for i, pt in enumerate(pts):
        if i not in idx:
            out.append(pt)
            continue
        a, b = Vector(pts[i - 1]), Vector(pts[(i + 1) % len(pts)])
        P = Vector(pt)
        out += [tuple(P + (a - P).normalized() * c), tuple(P + (b - P).normalized() * c)]
    return out


def sweep_u(bm, Wo, Ho, prof_uy, steps=0, radius=0.0, z_bot=0.0):
    """Sweep a jamb/head section along the U path (up the +x jamb, across the head, down the -x jamb).
    prof_uy = [(u, y)]: u = outward from the opening edge, y = Blender y. For this path the sweep frame maps
    profile (pu, pv) to (-y, outward) (proclib._basis on +Z, parallel-transported round the corners)."""
    path = [(Wo / 2, 0.0, z_bot), (Wo / 2, 0.0, Ho), (-Wo / 2, 0.0, Ho), (-Wo / 2, 0.0, z_bot)]
    if radius > 0 and steps:
        path = fillet(path, radius, steps)
    add_sweep(bm, path, [(-y, u) for u, y in prof_uy])


# --- frame ----------------------------------------------------------------------------------------------------------

def build_frame(parts, p, lod):
    d, s = lod["d"], lod["s"]
    g = geom(p)
    f, sw, D, Wo, Ho = g["f"], g["sw"], g["D"], g["Wo"], g["Ho"]
    fw = f["frame_face_in"]
    bm = parts("Frame", p["frame_finish"])
    prof = [(0.0, -D / 2), (fw, -D / 2), (fw, D / 2), (0.0, D / 2)]
    if d <= 2:  # stop between the rabbets, the leaf closes against it
        ya = g["y_pf"]
        yb = ya - sw * min(f["stop_w_in"], abs(ya - (-sw * D / 2)) - 0.006)
        lo, hi = sorted((ya, yb))
        prof += [(0.0, hi), (-f["stop_h_in"], hi), (-f["stop_h_in"], lo), (0.0, lo)]
        if d == 0:
            prof = chamfer(prof, {0, 3, 5, 6}, 0.0016)
    sweep_u(bm, Wo, Ho, prof)
    if p.get("threshold") and d <= 1:
        th_w, th_h = f.get("threshold_w_in", 5 * INCH), f.get("threshold_h_in", 0.5 * INCH)
        yc = (g["y_sf"] + g["y_pf"]) / 2
        bt = parts("Threshold", "Door_Al_Clear")
        sec = [(yc - th_w / 2, 0.0), (yc + th_w / 2, 0.0), (yc + th_w / 2 - th_h * 2, th_h), (yc - th_w / 2 + th_h * 2, th_h)]
        add_sweep(bt, [(-Wo / 2, 0, 0), (Wo / 2, 0, 0)], sec)  # along +X the sweep frame maps (pu, pv) to (y, z)
    if p["row"]["leaves"] == 1 and d <= 1:
        xl = -Wo / 2  # latch jamb soffit
        hw = parts("FrameHW", "Door_HW_Satin")
        zl = f.get("lever_h_in", 41 * INCH)
        ym = (g["y_sf"] + g["y_pf"]) / 2
        box(hw, 3, xl - 0.0015, xl + 0.0005, ym - 0.016, ym + 0.016, zl - 0.06, zl + 0.06)  # strike plate
        if d == 0:
            rb = parts("Silencers", "Door_Rubber")
            yst = g["y_pf"] - sw * 0.012
            for z in (0.5, 1.1, 1.7):  # 3 rubber silencers on the latch-jamb stop
                add_cylinder_between(rb, (xl - f["stop_h_in"], yst, z), (xl - f["stop_h_in"] + 0.003, yst, z), 0.005, 8)
    return {"collision_boxes": frame_boxes(g)}


def frame_boxes(g):
    fw, D, Wo, Ho = g["f"]["frame_face_in"], g["D"], g["Wo"], g["Ho"]
    return [collision_box("JambA", (Wo / 2 + fw / 2, 0, Ho / 2), (fw, D, Ho)),
            collision_box("JambB", (-Wo / 2 - fw / 2, 0, Ho / 2), (fw, D, Ho)),
            collision_box("Head", (0, 0, Ho + fw / 2), (Wo + 2 * fw, D, fw))]


def build_arch(parts, p, lod):
    d = lod["d"]
    f, row = fam(p), p["row"]
    W, H = row["clearOpening_ft"] * FT, 7.0 * FT  # cased opening 3'-0" x 7'-0" (A101 keynote 10, High)
    T = max(p["wall_t_m"], 0.1)
    lt, r = f["lining_t_in"], f["corner_r_ft"] * FT
    bm = parts("Frame", p["frame_finish"])
    yb = T / 2 + 0.002  # corner bead just proud of the wall face
    if d == 3:
        for x0, x1, z0, z1 in ((W / 2, W / 2 + lt, 0, H + lt), (-W / 2 - lt, -W / 2, 0, H + lt), (-W / 2, W / 2, H, H + lt)):
            add_box(bm, (x1 - x0, 2 * yb, z1 - z0), ((x0 + x1) / 2, 0, (z0 + z1) / 2))
    else:
        prof = [(0.0, -yb), (lt, -yb), (lt, yb), (0.0, yb)]
        if d <= 1:  # rounded corner bead on both wall faces
            br, n = f["bead_r_in"], 3 if d == 0 else 1
            arc = [math.radians(90 * i / n) for i in range(n + 1)]
            prof = [(lt, -yb), (lt, yb)] + [(br + br * math.cos(math.pi / 2 + a), yb - br + br * math.sin(math.pi / 2 + a)) for a in arc]
            prof += [(br + br * math.cos(math.pi + a), -yb + br + br * math.sin(math.pi + a)) for a in arc]
        sweep_u(bm, W, H, prof, steps={0: 8, 1: 4, 2: 2}[d], radius=r)
        for sx in (1, -1):  # spandrels: fill between the rounded lining and the square rough opening
            cx, cz, ro = sx * (W / 2 - r), H - r, r + lt * 0.5
            n = {0: 8, 1: 4, 2: 2}[d]
            arc = [(cx + sx * ro * math.cos(math.radians(90 * i / n)), cz + ro * math.sin(math.radians(90 * i / n)))
                   for i in range(n + 1)]
            pts = arc + [(sx * (W / 2 - r), H + lt), (sx * (W / 2 + lt), H + lt), (sx * (W / 2 + lt), H - r)]
            if sx < 0:
                pts = pts[::-1]
            prism_y(bm, pts, -yb, yb)
    fw = lt
    boxes = [collision_box("JambA", (W / 2 + fw / 2, 0, H / 2), (fw, T, H)),
             collision_box("JambB", (-W / 2 - fw / 2, 0, H / 2), (fw, T, H)),
             collision_box("Head", (0, 0, H + fw / 2), (W + 2 * fw, T, fw))]
    return {"collision_boxes": boxes, "arch": {"clear_m": [round(W, 5), round(H, 5)], "corner_r_m": round(r, 4),
                                               "rough_opening_m": [round(W + 2 * lt, 5), round(H + lt, 5), round(T, 5)]}}


# --- leaves ---------------------------------------------------------------------------------------------------------

def build_leaf(parts, p, lod):
    d, s = lod["d"], lod["s"]
    g = geom(p)
    f = g["f"]
    idx = 1 if p["part"] == "LeafR" else 0
    lf = leaves(p)[idx][1]
    W, H, t, z0 = g["W"][idx], g["H"], f["leaf_t_in"], g["z0"]
    sw = 1 if lf["openAngle"] > 0 else -1
    k = hinge_off(f)
    y_s, y_p = -sw * k, -sw * (k + t)  # swing / push face (leaf-local, pivot at origin)

    def X(u):  # distance from the hinge edge -> Blender x
        return -E_AXIS - u

    pair = p["row"]["leaves"] == 2
    if p["family"] == "storefront":
        leaf_storefront(parts, p, d, s, g, W, H, t, z0, sw, y_s, y_p, X, astragal=pair and idx == 0)
    else:
        leaf_hm(parts, p, d, s, f, W, H, t, z0, sw, y_s, y_p, X)
    if d <= 2:
        hinges(parts, p, d, s, f, z0, H, g["Ho"])
    return {"collision_boxes": [collision_box("Leaf", ((X(0) + X(W)) / 2, (y_s + y_p) / 2, z0 + H / 2), (W, t, H))],
            "leaf": (W, H, t, sw, X, z0)}


def face_y(y_s, y_p, sw, side, off):
    """Point `off` out from a face: side +1 = swing face, -1 = push face."""
    return y_s + sw * off if side > 0 else y_p - sw * off


def leaf_hm(parts, p, d, s, f, W, H, t, z0, sw, y_s, y_p, X):
    row = p["row"]
    bm = parts("Leaf", p["leaf_finish"])
    lo, hi = sorted((y_s, y_p))
    box(bm, d, X(W), X(0), lo, hi, z0, z0 + H, r=0.0016)
    if d == 3:
        return
    zl = f["lever_h_in"]
    if row["hardware"] == "lever":
        hw = parts("Lever", "Door_HW_Black")
        for side in (1, -1):
            lever(hw, d, s, f, X(W - f["lever_backset_in"]), face_y(y_s, y_p, sw, side, 0), side * sw, zl)
        if d <= 1:  # latch faceplate on the lock edge
            box(parts("Edge", "Door_HW_Satin"), 3, X(W) - 0.0012, X(W), (lo + hi) / 2 - 0.0125, (lo + hi) / 2 + 0.0125,
                zl - 0.0635, zl + 0.0635)
    elif row["hardware"] == "pushBar":
        exit_device(parts("ExitDevice", "Door_HW_Satin"), d, f, W, X, face_y(y_s, y_p, sw, -1, 0), -sw, zl)
        if p.get("pull_trim"):
            ny = face_y(y_s, y_p, sw, 1, 0)
            pull(parts("Lever", "Door_HW_Satin"), d, s, X(W - 0.05), ny, sw, 1.0668, 0.2286, 0.0127, 0.0635)
    if row["selfClosing"] is not False:  # True, or 'unknown' with a closer as placeholder (GAP-138)
        closer(parts("Closer", "Door_Closer_Al"), d, s, X, face_y(y_s, y_p, sw, -1, 0), -sw, z0 + H)
    if p.get("kick_plate"):
        ki = f["kick_inset_in"]
        yk = face_y(y_s, y_p, sw, -1, 0)
        box(parts("Kick", "Door_HW_Satin"), d + 2, X(W - ki), X(ki), yk, yk - sw * 0.0013, z0 + 0.003, z0 + f["kick_h_in"])


def leaf_storefront(parts, p, d, s, g, W, H, t, z0, sw, y_s, y_p, X, astragal):
    f = g["f"]
    st, tr, br = f["stile_w_in"], f["top_rail_in"], f["bottom_rail_in"]
    lo, hi = sorted((y_s, y_p))
    bm = parts("Leaf", p["leaf_finish"])
    r = 0.0015 if d <= 1 else 0
    box(bm, d, X(st), X(0), lo, hi, z0, z0 + H, r)                      # hinge stile
    box(bm, d, X(W), X(W - st), lo, hi, z0, z0 + H, r)                  # latch stile
    box(bm, d, X(W - st), X(st), lo, hi, z0 + H - tr, z0 + H, r)        # top rail
    box(bm, d, X(W - st), X(st), lo, hi, z0, z0 + br, r)                # bottom rail (10 in, ADA)
    ym, gt, ov = (lo + hi) / 2, f["glass_t_in"], 0.0127
    add_box(parts("Glass", "Door_Glass_GL1"), (W - 2 * st + 2 * ov, gt, H - tr - br + 2 * ov),
            ((X(st) + X(W - st)) / 2, ym, z0 + br + (H - tr - br) / 2))
    if d <= 1:  # snap-in glazing beads both faces, stepped below the stile face
        bw = f["bead_w_in"]
        xa, xb, za, zb = X(W - st), X(st), z0 + br, z0 + H - tr
        for y0, y1 in ((ym + gt / 2, hi - 0.003), (lo + 0.003, ym - gt / 2)):
            for bx in ((xa, xa + bw, za, zb), (xb - bw, xb, za, zb), (xa + bw, xb - bw, za, za + bw), (xa + bw, xb - bw, zb - bw, zb)):
                box(bm, 3, bx[0], bx[1], y0, y1, bx[2], bx[3])
    if d <= 2:
        hw = parts("Pull", "Door_HW_Satin")
        for side in (1, -1):  # back-to-back pulls on the latch stile (DEC-115 (2) storefrontPull)
            pull(hw, d, s, X(W - st / 2), face_y(y_s, y_p, sw, side, 0), side * sw, f["pull_h_in"], f["pull_ctc_in"],
                 f["pull_d_in"] / 2, f["pull_standoff_in"])
    if astragal and d <= 2:
        aw = f["astragal_w_in"]
        y0 = y_s
        box(parts("Astragal", p["leaf_finish"]), d, X(W) - aw / 2, X(W) + aw / 2, *sorted((y0, y0 + sw * 0.005)),
            z0 + 0.01, z0 + H - 0.01)


def lever(bm, d, s, f, x, y0, n, z):
    """Lever trim on a face at y0 with outward normal n (Blender y sign); the lever returns toward the hinge (+x)."""
    rr = f["rose_d_in"] / 2
    if d == 2:
        add_box(bm, (0.06, 0.012, 0.06), (x, y0 + n * 0.006, z))
        add_box(bm, (f["lever_len_in"], 0.016, 0.018), (x + f["lever_len_in"] / 2, y0 + n * 0.06, z))
        return
    add_cylinder_between(bm, (x, y0, z), (x, y0 + n * 0.011, z), rr, s)                      # rose
    add_cylinder_between(bm, (x, y0 + n * 0.011, z), (x, y0 + n * 0.014, z), rr * 0.8, s)    # rose step
    L = f["lever_len_in"]
    path = [(x, y0 + n * 0.014, z), (x, y0 + n * 0.062, z), (x + L, y0 + n * 0.062, z), (x + L + 0.004, y0 + n * 0.042, z)]
    add_tube(bm, path, 0.0085, max(8, s // 2), bend_radius=0.012 if d == 0 else 0.0, bend_steps=3 if d == 0 else 0)
    if d == 0:  # cylinder housing in the rose (locking side) is not modelled (DEC-051)
        add_cylinder_between(bm, (x, y0 + n * 0.014, z), (x, y0 + n * 0.024, z), 0.011, s)


def pull(bm, d, s, x, y0, n, zc, ctc, r, so):
    """Vertical bar pull on a face: two standoff legs and a grip, centred at zc."""
    za, zb = zc - ctc / 2, zc + ctc / 2
    if d == 2:
        add_box(bm, (2 * r, so, ctc), (x, y0 + n * so / 2, zc))
        return
    path = [(x, y0, za), (x, y0 + n * so, za), (x, y0 + n * so, zb), (x, y0, zb)]
    add_tube(bm, path, r, max(8, s // 2), bend_radius=so * 0.45 if d == 0 else 0.0, bend_steps=4 if d == 0 else 0)
    for z in (za, zb):  # mounting roses
        add_cylinder_between(bm, (x, y0, z), (x, y0 + n * 0.004, z), r * 1.6, max(8, s // 2))


def exit_device(bm, d, f, W, X, y0, n, z):
    """Rim exit device on the push face: hinge-end bracket, rail, touch bar, latch-end mechanism case."""
    if d == 2:
        add_box(bm, (W - 0.09, 0.07, 0.08), ((X(0.04) + X(W - 0.05)) / 2, y0 + n * 0.035, z))
        return
    def b(u0, u1, depth, h, dz=0.0):
        box(bm, d, X(u1), X(u0), *sorted((y0, y0 + n * depth)), z + dz - h / 2, z + dz + h / 2, r=0.004)
    b(0.04, 0.09, 0.06, 0.075)                 # hinge-end mounting bracket
    b(0.09, W - 0.22, 0.045, 0.055)            # rail
    b(0.12, W - 0.24, 0.07, 0.04, -0.004)      # touch bar
    b(W - 0.22, W - 0.05, 0.066, 0.09)         # mechanism case
    if d == 0:
        b(W - 0.2, W - 0.07, 0.068, 0.012, 0.03)  # case cover seam band


def closer(bm, d, s, X, y0, n, ztop):
    """Parallel-arm surface closer on the push face, top rail, near the hinge (arm drawn folded, not articulated)."""
    zc = ztop - 0.09  # arm stays under the head stop (stop drops 5/8 in below the head soffit)
    if d == 2:
        add_box(bm, (0.28, 0.055, 0.06), (X(0.25), y0 + n * 0.0275, zc))
        return
    box(bm, d, X(0.39), X(0.11), *sorted((y0, y0 + n * 0.055)), zc - 0.03, zc + 0.03, r=0.006)
    add_cylinder_between(bm, (X(0.15), y0 + n * 0.02, zc + 0.03), (X(0.15), y0 + n * 0.02, zc + 0.042), 0.012, s)  # pinion
    box(bm, 3, X(0.42), X(0.15), *sorted((y0 + n * 0.012, y0 + n * 0.028)), zc + 0.042, zc + 0.05)                    # main arm
    if d == 0:
        box(bm, 3, X(0.46), X(0.40), *sorted((y0 + n * 0.006, y0 + n * 0.034)), zc + 0.036, zc + 0.042)              # forearm
        for u in (0.13, 0.37):  # end caps
            add_cylinder_between(bm, (X(u), y0 + n * 0.0275, zc - 0.031), (X(u), y0 + n * 0.0275, zc - 0.034), 0.01, s)


def hinges(parts, p, d, s, f, z0, H, Ho):
    """Butt hinges: barrel on the pivot axis (x = y = 0). Top/bottom per hinge_top/bottom, the rest evenly between."""
    bm = parts("Hinges", "Door_HW_Satin")
    n, L, r = f["hinges"], f["hinge_len_in"], f["hinge_barrel_d_in"] / 2
    top = Ho - f["hinge_top_in"] - L
    bot = f["hinge_bottom_in"]
    for i in range(n):
        zb = bot + (top - bot) * i / (n - 1)
        if d == 2:
            add_box(bm, (2 * r, 2 * r, L), (0, 0, zb + L / 2))
            continue
        if d == 1:
            add_cylinder_between(bm, (0, 0, zb), (0, 0, zb + L), r, max(8, s // 2))
            continue
        k = 5
        for j in range(k):  # 5 knuckles with hairline gaps
            a = zb + L * j / k + 0.0005
            add_cylinder_between(bm, (0, 0, a), (0, 0, a + L / k - 0.001), r, s)
        for zz in (zb - 0.004, zb + L):  # button tips
            add_cylinder_between(bm, (0, 0, zz), (0, 0, zz + 0.004), r * 0.75, s)


# --- grille ---------------------------------------------------------------------------------------------------------

def build_grille(parts, p, lod):
    d = lod["d"]
    f, row = fam(p), p["row"]
    L, H = row["leafWidth_ft"] * FT, row["leafHeight_ft"] * FT
    pw, pd = (v * INCH for v in f["picket_in"])
    tw, th = (v * INCH for v in f["track_in"])
    bm = parts("Grille", p["frame_finish"])
    add_box(bm, (L, tw, th), (0, 0, H - th / 2))  # top track
    if d == 3:
        add_box(bm, (L, pd, H - th), (0, 0, (H - th) / 2))
        return {"collision_boxes": [collision_box("Grille", (0, 0, H / 2), (L, tw, H))]}
    pitch = f["picket_pitch_in"]  # fam() already converted it to metres
    n = max(2, round((L - pw) / pitch))
    xs = [-L / 2 + pw / 2 + (L - pw) * i / n for i in range(n + 1)]
    for x in xs:
        add_box(bm, (pw, pd, H - th), (x, 0, (H - th) / 2))
    bands = {0: f["lattice_bands"], 1: max(1, f["lattice_bands"] - 1), 2: 0}[d]
    bw, bt = (v * INCH for v in f["lattice_bar_in"])
    for k in range(bands):
        zc = (H - th) * (k + 1) / (bands + 1)
        for x0, x1 in zip(xs, xs[1:]):
            dx = x1 - x0
            ln = math.hypot(dx, dx * 0.9)
            ang = math.atan2(dx * 0.9, dx)
            for sgn in (1, -1):  # crossed lattice links, one each face
                box_rot(bm, (ln, bt, bw), ((x0 + x1) / 2, sgn * (pd / 2 + bt / 2), zc), sgn * ang)
    return {"collision_boxes": [collision_box("Grille", (0, 0, H / 2), (L, tw, H))]}


# --- entry point ----------------------------------------------------------------------------------------------------

def set_pbr(objs, finishes):
    for o in objs.values():
        for m in o.data.materials:
            fin = finishes[m.name[len("M_Proc_"):]]
            if not m.node_tree:
                m.use_nodes = True
            bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
            bsdf.inputs["Base Color"].default_value = (*fin["rgba"][:3], 1.0)
            bsdf.inputs["Metallic"].default_value = fin["metallic"]
            bsdf.inputs["Roughness"].default_value = fin["roughness"]
            bsdf.inputs["Alpha"].default_value = fin["rgba"][3]
            m.metallic, m.roughness = fin["metallic"], fin["roughness"]
            if fin["rgba"][3] < 1:
                m.surface_render_method = "BLENDED"


def build(p, lod):
    parts = Parts({k: v["rgba"] for k, v in p["finishes"].items() if not k.startswith("_")})
    row, part = p["row"], p["part"]
    if part == "Grille":
        info = build_grille(parts, p, lod)
    elif row["type"] == "opening":
        info = build_arch(parts, p, lod)
    elif part == "Frame":
        info = build_frame(parts, p, lod)
    else:
        info = build_leaf(parts, p, lod)
    for bm, *_ in parts._p.values():  # shortcut: reaches into proclib.Parts so builders need not care about winding
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    objs = parts.finish()
    set_pbr(objs, p["finishes"])
    pts = [v.co for o in objs.values() for v in o.data.vertices]
    lo = [min(c[i] for c in pts) for i in range(3)]
    hi = [max(c[i] for c in pts) for i in range(3)]
    size = [b - a for a, b in zip(lo, hi)]
    extra = {"seed": int(p["seed"]), "collision_boxes": info["collision_boxes"], "door": door_info(p, info, objs, lod)}
    extra.update(wear(p))
    if part.startswith("Leaf"):
        extra["door"]["transparent_slots"] = [m.name for o in objs.values() for m in o.data.materials
                                              if p["finishes"][m.name[7:]]["rgba"][3] < 1]
    return objs, (size[0], size[2], size[1]), extra


def door_info(p, info, objs, lod):
    """Manifest door block + the mechanical self-checks (sizes vs DOORS.json, pivot on the hinge axis)."""
    row, part, tol = p["row"], p["part"], p["size_tol_m"]
    out = {"id": row["id"], "type": row["type"], "doors_json_object": row["object"], "part": part,
           "family": p["family"], "src": p[p["family"]]["_src"]}
    if part == "Grille":
        b = bounds(objs["Grille"])
        check(abs(b[1][0] - b[0][0] - row["leafWidth_ft"] * FT) <= tol, "grille width vs DOORS.json")
        check(abs(b[1][2] - b[0][2] - row["leafHeight_ft"] * FT) <= tol, "grille height vs DOORS.json")
        out["placement"] = "not placed (DOORS.json pos_ft null, DEC-037); origin = bottom centre of the extended grille"
        return out
    if row["type"] == "opening":
        out.update(info["arch"])
        b = bounds(objs["Frame"])
        check(abs(b[1][0] - b[0][0] - info["arch"]["rough_opening_m"][0]) <= tol, "arch rough opening width")
        out["placement"] = ("origin = opening centre on the wall centreline at floor; local X along the wall "
                            "(symmetric, either yaw along the wall)")
        out["clear_opening_vs_doors_json_m"] = round(info["arch"]["clear_m"][0] - row["clearOpening_ft"] * FT, 6)
        return out
    g = geom(p)
    names = [lf["object"] for _, lf in leaves(p)]
    if part == "Frame":
        out.update({
            "placement": ("origin = opening centre on the wall centreline at floor level; Unity local +X runs hinge->latch "
                          f"of {names[0]} (frame yaw = its closedRotation); local Z = wall normal"),
            "yaw_deg": leaves(p)[0][1]["closedRotation"][1],
            "swing_side_unity_local": "-Z" if g["sw"] > 0 else "+Z",
            "rough_opening_m": {"width": round(g["RO"][0], 5), "height": round(g["RO"][1], 5), "depth": round(g["RO"][2], 5)},
            "soffit_opening_m": [round(g["Wo"], 5), round(g["Ho"], 5)],
            "wall_t_graybox_m": round(p["wall_t_m"], 5),
            "hinge_pivots_unity_xyz": {lf["pivot"]: to_unity(*pv) for (_, lf), pv in zip(leaves(p), g["piv"])},
            "leaf_assets": [p["asset_prefix"] + row["id"] + "_" + a for a, _ in leaves(p)],
        })
        # assembly check: each closed leaf sits inside the soffit opening, clear of the head, against the stop
        for (_, lf), (px, py, _), W in zip(leaves(p), g["piv"], g["W"]):
            xs = sorted((px - math.copysign(E_AXIS, px), px - math.copysign(E_AXIS + W, px)))
            check(xs[0] >= -g["Wo"] / 2 - 1e-6 and xs[1] <= g["Wo"] / 2 + 1e-6, f"{lf['object']} inside the jambs")
        check(g["z0"] + g["H"] <= g["Ho"] - 0.001, "leaf clears the head")
        return out
    W, H, t, sw, X, z0 = info["leaf"]
    lf = leaves(p)[1 if part == "LeafR" else 0][1]
    b = bounds(objs["Leaf"])
    check(abs(b[1][0] - b[0][0] - lf["leafWidth_ft"] * FT) <= tol, f"{part} width vs DOORS.json leafWidth_ft")
    check(abs(b[1][2] - b[0][2] - row["leafHeight_ft"] * FT) <= tol, f"{part} height vs DOORS.json leafHeight_ft")
    check(abs(b[1][0] + E_AXIS) <= 1e-4, f"{part} hinge edge on the pivot axis")
    if "Hinges" in objs:
        hb = bounds(objs["Hinges"])
        check(abs(hb[0][0] + hb[1][0]) <= 1e-4 and abs(hb[0][1] + hb[1][1]) <= 1e-4, f"{part} hinge barrels on the origin axis")
    out.update({
        "pivot": "asset origin = hinge axis at floor level (DOORS.json pivot); leaf along Unity local +X, rotates about local +Y",
        "pivot_object": lf["pivot"], "leaf_object": lf["object"],
        "closedRotation": lf["closedRotation"], "openAngle": lf["openAngle"],
        "leaf_size_m": [round(W, 5), round(H, 5), round(t, 5)], "leaf_bottom_m": round(z0, 5),
        "swing_side_unity_local": "-Z" if sw > 0 else "+Z",
        "hardware": row["hardware"], "selfClosing": row["selfClosing"], "lock": row["lock"],
        "defaultState": row["defaultState"], "finish": "M_Proc_" + p["leaf_finish"],
        "frame_asset": p["asset_prefix"] + row["id"] + "_Frame",
    })
    return out


def bounds(o):
    xs, ys, zs = zip(*(v.co for v in o.data.vertices))
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def check(ok, what):
    if not ok:
        raise ValueError("doors self-check failed: " + what)


# --- review sheets (DEC-122): `-- sheets [ids]` -----------------------------------------------------------------------
# Each door is rebuilt per LOD with build(), its leaves hung on the frame pivots and opened OPEN_FRAC of openAngle, in a
# grey wall stub cut to the manifest rough opening (the "closed" tile hangs them at 0 %, REVIEW-PROC013 m5). EEVEE so GL-1 reads as glass. Labels are text objects on the camera.

SPECS = os.path.join(ROOT, "Docs", "Assets", "Specs")
RENDERS = os.path.join(ROOT, "Artifacts", "Renders", "Doors")
OPEN_FRAC = 0.4
LODS = ("LOD0", "LOD1", "LOD2", "LOD3")


def _scene(res, bg=(0.62, 0.63, 0.65, 1)):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "BLENDER_EEVEE"
    s.render.resolution_x = s.render.resolution_y = res
    s.view_settings.view_transform = "Standard"
    s.world = bpy.data.worlds.new("W")
    s.world.use_nodes = True
    s.world.node_tree.nodes["Background"].inputs[0].default_value = bg
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.data.energy, sun.rotation_euler = 2.5, (math.radians(50), 0, math.radians(30))
    s.collection.objects.link(sun)
    return s


def _mat(name, rgba, emit=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    if emit:
        nt.nodes.remove(nt.nodes["Principled BSDF"])
        em = nt.nodes.new("ShaderNodeEmission")
        nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs[0])
        em.inputs[0].default_value = rgba
        return m, nt, em
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value, b.inputs["Roughness"].default_value = rgba, 0.9
    return m


def _slab(name, x0, x1, y0, y1, z0, z1, mat):
    bm = bmesh.new()
    add_box(bm, (x1 - x0, y1 - y0, z1 - z0), ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    o = bpy.data.objects.new(name, me)
    o.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(o)


def assemble(door, lod, frac=OPEN_FRAC):
    """Build every part of one door at lod, hang the leaves frac open, add the wall stub. Returns (tris, rough opening)."""
    tris, ro, wt = 0, None, None
    for q in door:
        objs, _, extra = build(q, q["lods"][lod])
        tris += sum(len(f.vertices) - 2 for o in objs.values() for f in o.data.polygons)
        info = extra["door"]
        if q["part"].startswith("Leaf"):
            g, i = geom(q), 1 if q["part"] == "LeafR" else 0
            lf = leaves(q)[i][1]
            rel = lf["closedRotation"][1] - leaves(q)[0][1]["closedRotation"][1]
            M = Matrix.Translation(g["piv"][i]) @ Matrix.Rotation(-math.radians(rel + lf["openAngle"] * frac), 4, "Z")
            for o in objs.values():
                o.matrix_world = M  # Unity yaw +a = Blender z rotation -a (see the module docstring axes)
        elif "rough_opening_m" in info:
            r = info["rough_opening_m"]
            ro = (r["width"], r["height"], r["depth"]) if isinstance(r, dict) else tuple(r)
            wt = q["wall_t_m"] or ro[2]
    if ro:
        wall, w = _mat("Wall", (0.78, 0.78, 0.76, 1)), ro[0] / 2
        for x0, x1, z0, z1 in ((-w - 0.45, -w, 0, 2.75), (w, w + 0.45, 0, 2.75), (-w, w, ro[1], 2.75)):
            _slab("Context_Wall", x0, x1, -wt / 2, wt / 2, z0, z1, wall)
    _slab("Context_Floor", -3, 3, -3, 3, -0.01, 0.0, _mat("Floor", (0.45, 0.45, 0.45, 1)))
    return tris, ro


def _camera(s, az_deg, target, dist, ortho=None, el_deg=12):
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    s.collection.objects.link(cam)
    s.camera = cam
    az, el = math.radians(az_deg), math.radians(0 if ortho else el_deg)
    d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam.location = Vector(target) + d * dist
    cam.rotation_euler = (math.pi / 2 - el, 0, az)
    if ortho:
        cam.data.type, cam.data.ortho_scale = "ORTHO", ortho
        return cam, ortho / 2
    cam.data.lens = 35
    return cam, 18 / 35  # half the 36 mm sensor width over the lens = half view width at 1 m


def _label(s, cam, half, lines):
    mat = _mat("Label", (0.0, 0.0, 0.0, 1), emit=True)[0]
    for i, text in enumerate(lines):
        cu = bpy.data.curves.new(f"L{i}", "FONT")
        cu.body, cu.size = text, half * (0.075 if i == 0 else 0.052)
        t = bpy.data.objects.new(f"L{i}", cu)
        t.data.materials.append(mat)
        s.collection.objects.link(t)
        t.parent, t.visible_shadow = cam, False
        t.location = (-half * 0.95, half * (0.87 - 0.065 * i - (0.02 if i else 0)), -1.0)


def door_lines(door, lod, tris, ro, frac=OPEN_FRAC):
    q, row = door[0], door[0]["row"]
    head = f"Door_{row['id']}   {lod}  {tris} tris"
    gaps = "GAPs: " + " ".join(q["gaps"]) if q["gaps"] else ""
    if row["type"] == "foldingGrille":
        return [head, f"foldingGrille {row['leafWidth_ft']}' x {row['leafHeight_ft']}' extended, not placed (DEC-037)",
                f"lock {row['lock']}  default {row['defaultState']}", gaps]
    rot = f"RO {ro[0]:.3f} x {ro[1]:.3f} x {ro[2]:.3f} m"
    if row["type"] == "opening":
        return [head, f"cased opening {row['clearOpening_ft']}' x 7'-0\"  {rot}", gaps]
    lf = leaves(q)[0][1]
    return [head, f"{row['type']}  {row['leaves']} x {lf['leafWidth_ft']}' x {row['leafHeight_ft']}'  {rot}",
            f"hinge {row['hinge_jamb'][:34]}  swing {row['swing'][:30]}",
            f"open {lf['openAngle']} deg (drawn {f'at {frac:.0%}' if frac else 'CLOSED'})  {row['hardware']}  closer {row['selfClosing']}",
            f"lock {row['lock']}  default {row['defaultState']}", gaps]


def render_door(door, lod, view, path, res):
    """view: 'push' / 'swing' = 3/4 perspective from that side; 'elev' / 'closed' = ortho elevation from the push side,
    leaves at OPEN_FRAC / shut."""
    s = _scene(res)
    frac = 0.0 if view == "closed" else OPEN_FRAC
    tris, ro = assemble(door, lod, frac)
    q = door[0]
    sw = geom(q)["sw"] if q["part"] != "Grille" and q["row"]["type"] != "opening" else -1
    w = ro[0] if ro else q["row"]["leafWidth_ft"] * FT
    push = 0 if sw > 0 else 180  # the push side is the one the leaf swings away from: Blender -y when sw > 0
    if view in ("elev", "closed"):
        o = max(w + 1.0, 3.6)
        cam, half = _camera(s, push, (0, 0, o / 2 - 0.12), 8, ortho=o)  # floor at the bottom, labels above the head
    else:
        az = push + 35 * sw if view == "push" else push + 145  # push: look past the latch side into the open leaf
        cam, half = _camera(s, az, (0, 0, 1.2), max(w + 0.9, 2.6) * 1.75)
    _label(s, cam, half, door_lines(door, lod, tris, ro, frac))
    s.render.filepath = path
    bpy.ops.render.render(write_still=True)


def render_evidence(ev, path, res):
    """The evidence crop on an emission plane, captioned; a plain 'no still' tile when there is none."""
    s = _scene(res, bg=(0.92, 0.92, 0.92, 1))
    cam, half = _camera(s, 0, (0, 0, 0), 5, ortho=1.0)
    if ev:
        img = bpy.data.images.load(os.path.join(ROOT, ev["file"]))
        W, H = img.size
        x0, y0, x1, y1 = ev["crop"]  # pixels, top-left origin
        a = (x1 - x0) / (y1 - y0)
        pw, ph = (0.94, 0.94 / a) if a > 0.94 / 0.74 else (0.74 * a, 0.74)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -0.1), rotation=(math.pi / 2, 0, 0))
        pl = bpy.context.object
        pl.scale = (pw, ph, 1)
        for lp in pl.data.uv_layers.active.data:  # unit plane UVs -> the crop (image v is bottom-up)
            u, v = lp.uv
            lp.uv = ((x0 + u * (x1 - x0)) / W, 1 - (y1 - v * (y1 - y0)) / H)
        m, nt, em = _mat("Ev", (1, 1, 1, 1), emit=True)
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        nt.links.new(tex.outputs[0], em.inputs[0])
        pl.data.materials.append(m)
        c = ev["caption"]
        cut = c.rfind(" ", 0, 62) if len(c) > 62 else len(c)
        lines = ["evidence", c[:cut], c[cut:].strip(), ev["file"][-62:]]
    else:
        lines = ["evidence", "no photo or CCTV still shows this door", "(colour / details: params _src and GAPs)"]
    _label(s, cam, half, [ln for ln in lines if ln])
    s.render.filepath = path
    bpy.ops.render.render(write_still=True)


def tiles_to_png(rows, out_path):
    """rows of PNG paths or None = blank (top first) -> one PNG, quantised to 32 levels (as register_stations_sheet)."""
    import numpy as np
    strips = []
    for row in rows:
        tiles = []
        for path in row:
            if path is None:  # blank filler tile
                tiles.append(np.full_like(tiles[0], 0.62))
                continue
            img = bpy.data.images.load(path)
            px = np.empty(img.size[0] * img.size[1] * 4, dtype=np.float32)
            img.pixels.foreach_get(px)
            tiles.append(px.reshape(img.size[1], img.size[0], 4))
        strips.append(np.concatenate(tiles, axis=1))
    sheet = np.concatenate(strips[::-1], axis=0)  # Blender images are bottom-up
    sheet = np.floor(sheet * 255 / 8) * 8 / 255
    out = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0])
    out.pixels.foreach_set(sheet.ravel())
    out.filepath_raw, out.file_format = out_path, "PNG"
    out.save()
    print(f"[DOORS] {out_path} ({os.path.getsize(out_path)} bytes)")


def sheets(only=None):
    """Per door: PROC_doors_<id>.png (push 3/4, swing 3/4, elevation, closed elevation, evidence). All doors: the LOD0 contact sheet
    (5 per row) and the LOD chain sheet (row per door, LOD0..LOD3, push 3/4)."""
    P = _load("Tools/Blender/params/doors.json")
    doors = {}
    for _, q in variants(P):
        doors.setdefault(q["id"], []).append(q)
    os.makedirs(RENDERS, exist_ok=True)
    hero, chain = [], []
    for did, door in doors.items():
        if only and did not in only:
            continue
        t = lambda n: os.path.join(RENDERS, f"{did}_{n}.png")  # noqa: E731
        for view in ("push", "swing", "elev", "closed"):
            render_door(door, "LOD0", view, t(view), 560)
        render_evidence(door[0].get("evidence"), t("evidence"), 560)
        tiles_to_png([[t("push"), t("swing"), t("elev"), t("closed"), t("evidence")]], os.path.join(SPECS, f"PROC_doors_{did}.png"))
        for lod in LODS:
            render_door(door, lod, "push", t(f"{lod}_s"), 300)
        hero.append(t("push"))
        chain.append([t(f"{lod}_s") for lod in LODS])
    if only:
        return
    hero += [None] * (-len(hero) % 5)
    tiles_to_png([hero[i:i + 5] for i in range(0, len(hero), 5)], os.path.join(SPECS, "PROC_doors_contact_sheet.png"))
    tiles_to_png(chain, os.path.join(SPECS, "PROC_doors_lod_sheet.png"))


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if argv[:1] == ["sheets"]:
        sheets(argv[1:] or None)
