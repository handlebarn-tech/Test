"""Parked vehicles for the parking lot (PROC-009; replaces the rejected IMP-003 R3b `parked_vehicles`, DEC-111,
checklist R3b.7). Generic unbranded classes (DEC-071; CCTV R1C1 SUV, R1C2 cars, RG3-4), one asset per params variant.
Construction:
- body: one closed loft of cross-sections along the length (side with tuck-under, shoulder radius, crowned deck),
  bottom edge cut to the wheel-arch circle; real panel shut lines as recessed V grooves (doors, rocker, hood, trunk);
- greenhouse: a second closed loft on the deck (tumblehome, rail radius, crowned roof). Windows are faces of that same
  surface, so the glazing is flush by construction; pillars/rails stay paint, belt and frames black;
- wheels inside the arches: lathed tyre (sidewall, shoulder, tread grooves), rim barrel + spokes + hub + lug nuts, disc
  and caliper; well liners; bumpers swept along the plan curve; lamps, grille, mirrors, handles, wipers, rear plate.
Class proportions are GAP-PROC-23, paint mix GAP-PROC-24. Origin = bottom centre, front = -Y (nose), sizes exact:
width incl. mirrors, height to roof peak (or rails), length bumper to bumper.
LOD0 full detail; LOD1 no lugs/caliper/slats/lip detail, coarser; LOD2 no seams/spokes/handles/wipers; LOD3 hull,
tyre + disc rim, box lamps/mirrors/bumpers."""
import math

import bmesh
from mathutils import Vector

from proclib import (INCH, Parts, add_beveled_box, add_box, add_lathe, add_sweep, add_tube, collision_box, fillet,
                     rounded_rect, wear)

PART_MAT = {"Body": "CarPaint", "PanelGaps": "PanelGap", "Underbody": "Underbody", "Trim": "Trim_Black",
            "Cladding": "Cladding", "Glass": "Glass", "Chrome": "Chrome", "Tires": "Tire_Rubber", "Rims": "Rim_Alloy",
            "Brakes": "Brake_Steel", "LampsClear": "Lamp_Clear", "LampsRed": "Lamp_Red", "LampsAmber": "Lamp_Amber",
            "Reflectors": "Lamp_Reflector", "Plate": "Plate_Blank", "MirrorGlass": "Mirror_Glass"}


def variants(p):
    for v in p["variants"]:
        q = {k: x for k, x in p.items() if k not in ("variants", "classes")}
        q.update(p["classes"][v["class"]])
        q.update(v)
        yield p["asset_prefix"] + v["id"], q


def smooth(pts, y):
    """Monotone cubic (Fritsch-Carlson) through [(y, z)] control points: no overshoot, no flat spot at each point."""
    if y <= pts[0][0]:
        return pts[0][1]
    if y >= pts[-1][0]:
        return pts[-1][1]
    h = [b[0] - a[0] for a, b in zip(pts, pts[1:])]
    dl = [(b[1] - a[1]) / w for a, b, w in zip(pts, pts[1:], h)]
    m = [dl[0]] + [0.0 if d0 * d1 <= 0 else (3 * h0 + 3 * h1) / ((2 * h1 + h0) / d0 + (h1 + 2 * h0) / d1)
                   for d0, d1, h0, h1 in zip(dl, dl[1:], h, h[1:])] + [dl[-1]]
    k = next(i for i in range(len(h)) if y <= pts[i + 1][0])
    t = (y - pts[k][0]) / h[k]
    return (pts[k][1] * (2 * t ** 3 - 3 * t ** 2 + 1) + m[k] * h[k] * (t ** 3 - 2 * t ** 2 + t) +
            pts[k + 1][1] * (-2 * t ** 3 + 3 * t ** 2) + m[k + 1] * h[k] * (t ** 3 - t ** 2))


def emit(src, mats, parts):
    """Copy src faces into the part bmeshes named by mats[face], keeping winding; frees src."""
    groups = {}
    for f in src.faces:
        groups.setdefault(mats[f], []).append(f)
    for name, faces in groups.items():
        dst, vmap = parts(name, PART_MAT[name]), {}
        for f in faces:
            vs = []
            for v in f.verts:
                if v not in vmap:
                    vmap[v] = dst.verts.new(v.co)
                vs.append(vmap[v])
            dst.faces.new(vs)
    src.free()


def add_prism(bm, quad_a, quad_b):
    """Closed 8-corner block from two matching 4-corner loops (winding fixed later by recalc)."""
    a = [bm.verts.new(c) for c in quad_a]
    b = [bm.verts.new(c) for c in quad_b]
    bm.faces.new(a)
    bm.faces.new(b[::-1])
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new([a[i], b[i], b[j], a[j]])


def fan(bm, ring):
    """Cap a closed ring with a centroid fan (ear clipping leaves zero-area triangles on collinear rims)."""
    c = bm.verts.new(sum((v.co for v in ring), Vector()) / len(ring))
    return [bm.faces.new([ring[i], ring[(i + 1) % len(ring)], c]) for i in range(len(ring))]


class Car:
    def __init__(self, p, lod):
        self.p, self.lod, self.d = p, lod, lod["detail"]
        L = self.L = p["length_m"]
        f = self.f = lambda y: -L / 2 + y  # params give y from the front bumper face
        self.hw0 = p["body_width_m"] / 2
        self.bd = p["bumper"]["depth_m"]
        self.yf, self.yr = -L / 2 + self.bd, L / 2 - self.bd
        t = p["tire"]
        self.rim = t["rim_d_in"] * INCH / 2
        self.tw = t["width_m"]
        self.R = self.rim + self.tw * t["aspect"]
        self.Ra = self.R + p["arch_gap_m"]
        self.axles = [f(p["front_overhang_m"]), f(p["front_overhang_m"] + p["wheelbase_m"])]
        self.deck = [(f(y), z) for y, z in p["deck"]]
        g = p["greenhouse"]
        self.gh = [(f(y), z) for y, z in g["profile"]]
        self.gap = p["panel_gap_m"]
        self.seams = self.d <= 1
        s = p["seams"]
        self.door_cols = [f(y) for y in s["doors"]]
        self.door_span = (min(self.door_cols), max(self.door_cols))
        self.hood = (f(s["hood"][0]), f(s["hood"][1]))
        self.trunk = (f(s["trunk_front"]), self.yr) if s.get("trunk_front") is not None else None
        self.s0 = s["door_bottom_s"]
        self.side_h_ref = smooth(self.deck, 0.0) - p["deck_crown_m"] - p["shoulder_r_m"] - p["rocker_z_m"]
        self.S = {}  # part -> temp bmesh of closed solids (normals recalculated before emit)
        self.parts = Parts(dict(p["colors"], CarPaint=p["paint"]))

    def solid(self, part):
        if part not in self.S:
            self.S[part] = bmesh.new()
        return self.S[part]

    # --- body ---------------------------------------------------------------------------------------------------
    def half_width(self, y):
        rp, k = self.p["plan_corner_m"], self.p["plan_end_k"]
        e = min(1.0, max(0.0, (self.yf + rp - y) / rp, (y - (self.yr - rp)) / rp))
        return self.hw0 * (k + (1 - k) * math.sqrt(1 - e * e))

    def bottom_z(self, y):
        p = self.p
        z = p["rocker_z_m"]
        a0, a1 = self.axles[0] - self.Ra, self.axles[1] + self.Ra
        lf, lr = p["end_lift_m"]
        if y < a0:
            z += lf * ((a0 - y) / (a0 - self.yf)) ** 1.5
        if y > a1:
            z += lr * ((y - a1) / (self.yr - a1)) ** 1.5
        for cy in self.axles:
            dy = abs(y - cy)
            if dy <= self.Ra:
                z = max(z, self.R + math.sqrt(max(0.0, self.Ra ** 2 - dy ** 2)))
        return z

    def side_x(self, y, s):
        p = self.p
        return self.half_width(y) * (1 - p["side_tuck"] * (1 - s) ** 2 - p["side_tumble"] * s ** 3)

    def shoulder(self, y):
        """(zb, zst, cx, zt): side bottom z, side top z, shoulder-arc centre x, deck centre z."""
        p = self.p
        zt = smooth(self.deck, y)
        zst = zt - p["deck_crown_m"] - p["shoulder_r_m"]
        return self.bottom_z(y), zst, self.side_x(y, 1.0) - p["shoulder_r_m"], zt

    def deck_z(self, y, x):
        _, _, cx, zt = self.shoulder(y)
        return zt - self.p["deck_crown_m"] * (x / cx) ** 2

    def body_half(self, y, tag):
        """Half section (x >= 0) bottom-of-side -> deck centre, and edge labels (len - 1)."""
        p, lod = self.p, self.lod
        zb, zst, cx, zt = self.shoulder(y)
        rs, crown, dep = p["shoulder_r_m"], p["deck_crown_m"], p["panel_gap_depth_m"]
        if zst - zb < 0.03:
            raise ValueError(f"y={y:.3f}: side height {zst - zb:.3f} m too small (deck vs arch/rocker params)")
        door_on = self.seams and self.door_span[0] - 1e-6 <= y <= self.door_span[1] + 1e-6
        hood_on = self.seams and (self.hood[0] - 1e-6 <= y <= self.hood[1] + 1e-6 or
                                  (self.trunk and self.trunk[0] - 1e-6 <= y <= self.trunk[1] + 1e-6))
        # side: s in [0, 1) from the bottom edge to the shoulder start; optional door-bottom seam triple at s0
        n = lod["side_rows"]
        ss = [(i / n, "") for i in range(n)]
        if self.seams:
            g = self.gap / 2 / self.side_h_ref
            ss = [e for e in ss if abs(e[0] - self.s0) > 1.5 * g] + [(self.s0 - g, ""), (self.s0, "mid"), (self.s0 + g, "")]
            ss.sort()
        pts, labels = [], []
        for i, (s, m) in enumerate(ss):
            x = self.side_x(y, s)
            if (m and door_on) or (tag == "door" and s >= self.s0 - 1e-9):
                x -= dep
            pts.append((x, zb + (zst - zb) * s))
            nxt = ss[i + 1] if i + 1 < len(ss) else (1.0, "")
            labels.append("door_gap" if m or nxt[1] else ("side_low" if nxt[0] <= self.s0 + 1e-9 else "side"))
        # shoulder arc a in [0, 90] deg; optional hood/trunk longitudinal seam triple at 45 deg
        m_ = lod["arc_rows"]
        aa = [(math.pi / 2 * j / m_, "") for j in range(m_ + 1)]
        if self.seams:
            dl = self.gap / 2 / rs
            aa = [e for e in aa if abs(e[0] - math.pi / 4) > 1.5 * dl] + [(math.pi / 4 - dl, ""), (math.pi / 4, "mid"),
                                                                        (math.pi / 4 + dl, "")]
            aa.sort()
        for j, (a, m) in enumerate(aa):
            r = rs - (dep if m and hood_on else 0.0)
            x, z = cx + r * math.cos(a), zst + r * math.sin(a)
            if tag == "hood" and a >= math.pi / 4 - 1e-9:
                z -= dep
            pts.append((x, z))
            if j + 1 < len(aa):
                nxt = aa[j + 1]
                labels.append("hood_gap" if m or nxt[1] else ("arc_in" if a >= math.pi / 4 - 1e-9 else "arc_out"))
        k_ = lod["deck_rows"]
        for k in range(1, k_ + 1):
            x = cx * (1 - k / k_)
            pts.append((x, zt - crown * (x / cx) ** 2 - (dep if tag == "hood" else 0.0)))
            labels.append("deck")
        return pts, labels

    def body_columns(self):
        lod, Ra = self.lod, self.Ra
        n = max(2, math.ceil((self.yr - self.yf) / lod["body_step_m"]))
        uni = [self.yf + (self.yr - self.yf) * i / n for i in range(n + 1)]
        special, blocked = [], []
        for cy in self.axles:
            m = lod["arch_cols"]
            special += [(cy - Ra * math.cos(math.pi * k / m), "") for k in range(m + 1)]
            special += [(cy - Ra - 0.002, ""), (cy + Ra + 0.002, "")]
            blocked.append((cy - Ra - 0.01, cy + Ra + 0.01))
        if self.seams:
            g = self.gap / 2
            seam = [(y, "door") for y in self.door_cols] + [(y, "hood") for y in self.hood]
            if self.trunk:
                seam.append((self.trunk[0], "hood"))
            for y, tag in seam:
                special += [(y - g, ""), (y, tag), (y + g, "")]
                blocked.append((y - 4 * g, y + 4 * g))
        cols = [(y, "") for y in uni if y in (uni[0], uni[-1]) or not any(a < y < b for a, b in blocked)] + special
        cols.sort()
        out = []
        for y, tag in cols:  # drop slivers next to a seam/arch column (keep the tagged one)
            if out and y - out[-1][0] < 0.0012:
                if tag and not out[-1][1]:
                    out[-1] = (y, tag)
                continue
            out.append((y, tag))
        return out

    def body_mat(self, ym, strip, label):
        if label == "bottom":
            return "Underbody"
        if strip == "door" and label in ("side", "door_gap"):
            return "PanelGaps"
        if strip == "hood" and label in ("arc_in", "deck", "hood_gap"):
            return "PanelGaps"
        if label == "door_gap" and self.door_span[0] <= ym <= self.door_span[1]:
            return "PanelGaps"
        if label == "hood_gap" and (self.hood[0] <= ym <= self.hood[1] or (self.trunk and self.trunk[0] <= ym)):
            return "PanelGaps"
        if label == "side_low" and self.p.get("cladding"):
            return "Cladding"
        return "Body"

    def build_body(self):
        bm, mats, rings = bmesh.new(), {}, []
        cols = self.body_columns()
        self.arch_edges = {cy: [] for cy in self.axles}
        for y, tag in cols:
            half, labels = self.body_half(y, tag)
            ring = half + [(-x, z) for x, z in reversed(half[:-1])]
            rings.append([bm.verts.new((x, y, z)) for x, z in ring])
            for cy in self.axles:
                if abs(y - cy) <= self.Ra + 0.0025:
                    self.arch_edges[cy].append((half[0][0], y, half[0][1]))
        full = labels + labels[::-1] + ["bottom"]
        for i in range(len(rings) - 1):
            a, b = rings[i], rings[i + 1]
            ym, strip = (cols[i][0] + cols[i + 1][0]) / 2, cols[i][1] or cols[i + 1][1]
            for k in range(len(a)):
                k2 = (k + 1) % len(a)
                mats[bm.faces.new([a[k], a[k2], b[k2], b[k]])] = self.body_mat(ym, strip, full[k])
        for f in fan(bm, rings[0][::-1]) + fan(bm, rings[-1]):
            mats[f] = "Body"
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        emit(bm, mats, self.parts)

    # --- greenhouse -----------------------------------------------------------------------------------------------
    def gh_frame(self, y):
        g = self.p["greenhouse"]
        _, _, cx, _ = self.shoulder(y)
        hb = cx - g["base_inset_m"]
        zbase = self.deck_z(y, hb) - 0.012  # buried in the deck
        zg = smooth(self.gh, y)
        h = zg - zbase
        ht = min(g["roof_half_w_m"], hb - 0.02)
        crown, rr = min(g["crown_m"], 0.25 * h), min(g["rail_r_m"], 0.3 * h)
        return hb, zbase, zg, h, ht, crown, rr

    def gh_surface_z(self, y, x):
        _, _, zg, _, ht, crown, rr = self.gh_frame(y)
        return zg - crown * (min(abs(x), ht - rr) / (ht - rr)) ** 2

    def gh_half(self, y):
        lod = self.lod
        hb, zbase, zg, h, ht, crown, rr = self.gh_frame(y)
        zs = zg - crown - rr
        n = lod["gh_side_rows"]
        if self.d <= 2:
            sb, sf = min(0.3, 0.045 / (zs - zbase)), 1 - min(0.2, 0.02 / (zs - zbase))
            ss = [0.0] + [sb + (sf - sb) * i / n for i in range(n)] + [sf]
            labels = ["gbelt"] + ["gside"] * (n - 1) + ["gside", "gframe"]
        else:
            ss = [i / n for i in range(n)]
            labels = ["gside"] * n
        pts = [(hb + (ht - hb) * s, zbase + (zs - zbase) * s) for s in ss]
        m = lod["gh_rail_rows"]
        for j in range(m + 1):
            a = math.pi / 2 * j / m
            pts.append((ht - rr + rr * math.cos(a), zs + rr * math.sin(a)))
        labels += ["grail"] * m
        k_ = lod["gh_roof_rows"]
        x0 = ht - rr
        for k in range(1, k_ + 1):
            x = x0 * (1 - k / k_)
            pts.append((x, zg - crown * (x / x0) ** 2))
            labels.append("groof")
        return pts, labels

    def gh_mat(self, ym, label):
        g = self.p["greenhouse"]
        f = self.f
        inr = lambda rs: any(f(a) <= ym <= f(b) for a, b in rs)
        if label in ("gbelt", "bottom"):
            return "Trim"
        if label == "grail":
            return "Body"
        if label == "groof":
            if ym < f(g["roof_front_y"]):
                return "Glass"
            if ym > f(g["roof_rear_y"]) and g["backlight_on_roof"]:
                return "Glass"
            return "Body"
        black = inr(g["pillars_black"])
        if label == "gframe":
            return "Trim" if black or inr(g["side_glass"]) else "Body"
        if black:
            return "Trim"
        return "Glass" if inr(g["side_glass"]) else "Body"

    def build_greenhouse(self):
        g, lod = self.p["greenhouse"], self.lod
        f = self.f
        y0, y1 = self.gh[0][0], self.gh[-1][0]
        n = max(2, math.ceil((y1 - y0) / lod["gh_step_m"]))
        keys = [y for y, _ in self.gh] + [f(g["roof_front_y"]), f(g["roof_rear_y"])]
        for a, b in g["side_glass"] + g["pillars_black"]:
            keys += [f(a), f(b)]
        keys = [round(k, 6) for k in keys]
        ys =sorted(set(round(y, 6) for y in [y0 + (y1 - y0) * i / n for i in range(n + 1)] + keys if y0 <= y <= y1))
        ys = [y for i, y in enumerate(ys) if i == 0 or y - ys[i - 1] > 0.002 or y in keys]
        bm, mats, rings = bmesh.new(), {}, []
        for y in ys:
            half, labels = self.gh_half(y)
            ring = half + [(-x, z) for x, z in reversed(half[:-1])]
            rings.append([bm.verts.new((x, y, z)) for x, z in ring])
        full = labels + labels[::-1] + ["bottom"]
        for i in range(len(rings) - 1):
            a, b = rings[i], rings[i + 1]
            ym = (ys[i] + ys[i + 1]) / 2
            for k in range(len(a)):
                k2 = (k + 1) % len(a)
                mats[bm.faces.new([a[k], a[k2], b[k2], b[k]])] = self.gh_mat(ym, full[k])
        for f in fan(bm, rings[0][::-1]):
            mats[f] = "Trim"
        h_end = self.gh_frame(y1)[3]
        if h_end > 0.2:  # tall rear (SUV/hatch tailgate): paint frame around recessed glass
            ring = rings[-1]
            c = sum((v.co for v in ring), Vector()) / len(ring)
            inner = [bm.verts.new(c + (v.co - c) * g["tailgate_glass_k"] + Vector((0, -0.012, 0))) for v in ring]
            for i in range(len(ring)):
                j = (i + 1) % len(ring)
                mats[bm.faces.new([ring[i], ring[j], inner[j], inner[i]])] = "Body"
            for f in fan(bm, inner):
                mats[f] = "Glass"
        else:
            for f in fan(bm, rings[-1]):
                mats[f] = "Trim"
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        emit(bm, mats, self.parts)

    # --- wheels ---------------------------------------------------------------------------------------------------
    def wheel(self, cy, side):
        d, seg = self.d, self.lod["wheel_seg"]
        R, rim, tw = self.R, self.rim, self.tw
        bx = side * (self.p["track_m"] / 2 - tw / 2)  # inner face; t runs outward to tw
        base, axis = (bx, cy, R), (side, 0, 0)
        P = lambda t, dy, dz: (bx + side * t, cy + dy, R + dz)
        if d >= 3:
            prof = [(rim, 0.0), (R - 0.03, 0.0), (R, 0.03), (R, tw - 0.03), (R - 0.03, tw), (rim, tw), (rim, 0.0)]
        else:
            half = [(rim, 0.015), (rim + 0.01, 0.002), (rim + 0.03, 0.0), (R - 0.05, 0.0), (R - 0.025, 0.004),
                    (R - 0.008, 0.012), (R, 0.024)]
            if d >= 2:
                half = [half[0], half[2], half[3], half[5], half[6]]
            tread = []
            if d <= 1:
                gw, gd = 0.009, 0.008
                for fr in self.p["tire"]["grooves"] if d == 0 else self.p["tire"]["grooves"][::2]:
                    gc = tw * fr
                    tread += [(R, gc - gw / 2), (R - gd, gc - gw / 2 + 0.001), (R - gd, gc + gw / 2 - 0.001), (R, gc + gw / 2)]
            prof = half + tread + [(r, tw - t) for r, t in reversed(half)] + [half[0]]
        add_lathe(self.solid("Tires"), base, axis, prof, seg)
        rims = self.solid("Rims")
        if d >= 3:
            add_lathe(rims, base, axis, [(0, 0.02), (rim, 0.02), (rim, tw - 0.03), (0, tw - 0.03)], seg)
            return
        add_lathe(rims, base, axis, [(rim - 0.014, 0.02), (rim, 0.02), (rim, tw - 0.025), (rim + 0.012, tw - 0.022),
                                     (rim + 0.012, tw - 0.012), (rim - 0.006, tw - 0.014), (rim - 0.014, tw - 0.03),
                                     (rim - 0.014, 0.02)], seg)
        add_lathe(rims, base, axis, [(0, tw - 0.06), (0.085, tw - 0.06), (0.085, tw - 0.03), (0.07, tw - 0.02),
                                     (0.035, tw - 0.017), (0, tw - 0.016)], seg)
        if d == 2:  # flat dished face instead of spokes
            add_lathe(rims, base, axis, [(0.08, tw - 0.045), (rim - 0.012, tw - 0.035), (rim - 0.012, tw - 0.045),
                                         (0.08, tw - 0.055), (0.08, tw - 0.045)], seg)
            return
        n, dep = self.p["spokes"], 0.022
        rh, rs = 0.075, rim - 0.012
        for i in range(n):
            ph = 2 * math.pi * i / n + math.pi / 2
            er, et = (math.cos(ph), math.sin(ph)), (-math.sin(ph), math.cos(ph))
            loops = []
            for r, w, tf in ((rh, 0.05, tw - 0.022), (rs, 0.03, tw - 0.03)):
                loops.append([P(tt, r * er[0] + sw * w / 2 * et[0], r * er[1] + sw * w / 2 * et[1])
                              for tt, sw in ((tf, -1), (tf, 1), (tf - dep, 1), (tf - dep, -1))])
            add_prism(rims, *loops)
        brakes = self.solid("Brakes")
        add_lathe(brakes, base, axis, [(0.07, 0.05), (0.165, 0.05), (0.165, 0.075), (0.07, 0.075), (0.07, 0.05)], seg)
        if d == 0:
            for i in range(5):
                ph = 2 * math.pi * i / 5
                add_lathe(rims, P(0, 0.055 * math.cos(ph), 0.055 * math.sin(ph)), axis,
                          [(0, tw - 0.024), (0.0095, tw - 0.024), (0.0095, tw - 0.016), (0.006, tw - 0.013),
                           (0, tw - 0.013)], 6)
            ph0 = math.radians(130 if cy < 0 else 50)  # caliper behind the disc, toward the car centre
            loops = []
            for tt in (0.04, 0.09):
                loops.append([P(tt, r * math.cos(ph0 + da), r * math.sin(ph0 + da))
                              for r, da in ((0.12, -0.3), (0.12, 0.3), (0.19, 0.3), (0.19, -0.3))])
            add_prism(brakes, *loops)
        # well liner: inner wall so the arch does not show through the car
        z0 = 0.6 * self.R  # below this the tyre itself fills the opening
        add_box(self.solid("Trim"), (0.01, 2 * self.Ra, self.R + self.Ra - z0),
                (side * (self.p["track_m"] / 2 - tw / 2 - 0.05), cy, (z0 + self.R + self.Ra) / 2))

    # --- attachments ------------------------------------------------------------------------------------------------
    def bumpers(self):
        p, d = self.p, self.d
        b = p["bumper"]
        z0, z1 = b["z_m"]
        zc, bh, bd = (z0 + z1) / 2, z1 - z0, self.bd
        prof = rounded_rect(bd, bh, 0.02 if d <= 2 else 0.0, 3 if d == 0 else (1 if d <= 2 else 0))
        for sgn in (-1, 1):
            yp = sgn * (self.L / 2 - bd / 2)
            x0 = self.half_width(sgn * self.yr) - 0.12
            ye = yp - sgn * b["wrap_m"]
            zb, zst, _, _ = self.shoulder(ye)
            x1 = self.side_x(ye, min(1.0, max(0.0, (zc - zb) / (zst - zb)))) - bd / 2 + 0.004  # wrap end flush with the side
            path = [(-x1, yp - sgn * b["wrap_m"], zc), (-x0, yp, zc), (x0, yp, zc), (x1, yp - sgn * b["wrap_m"], zc)]
            if d <= 2:
                path = fillet(path, 0.12, 6 if d == 0 else 2)
            add_sweep(self.solid("Cladding" if p.get("cladding") else "Body"), path, prof)
            if d <= 1:  # black lower lip
                add_beveled_box(self.solid("Trim"), (2 * x0, bd * 0.6, 0.04), (0, yp + sgn * bd * 0.15, z0 - 0.012),
                                0.01, 0.003, 1)

    def lamps(self):
        p, d = self.p, self.d
        lp = p["lamps"]
        box = (lambda bm, s, c: add_beveled_box(bm, s, c, 0.02, 0.004, 3 if d == 0 else 1)) if d <= 2 else \
            (lambda bm, s, c: add_box(bm, s, c))
        for sgn, ye in ((-1, self.yf), (1, self.yr)):
            _, zst, _, _ = self.shoulder(ye)
            hwe = self.half_width(ye)
            w, h = lp["head"] if sgn < 0 else lp["tail"]
            zc = zst - 0.008 - h / 2
            for side in (-1, 1):
                xc = side * (hwe - w / 2 - 0.05)
                c = (xc, ye + sgn * 0.003, zc)  # lens front 12 mm proud of the end face
                box(self.solid("LampsClear" if sgn < 0 else "LampsRed"), (w, 0.03, h), c)
                if d <= 1:
                    inner = self.solid("Reflectors")
                    add_box(inner, (w - 0.02, 0.008, h - 0.02), (xc, ye + sgn * 0.008, zc))
                    if sgn < 0:
                        for k in (-1, 1):  # projector bulbs inside the lens
                            add_lathe(inner, (xc + k * w / 4, ye + 0.004, zc), (0, -1, 0),
                                      [(0, 0.0), (h * 0.28, 0.0), (h * 0.28, 0.014), (0, 0.014)], 16 if d == 0 else 8)
                        add_box(self.solid("LampsAmber"), (w * 0.18, 0.012, h * 0.5),
                                (xc + side * w * 0.36, ye - 0.006, zc))
                    else:
                        add_box(self.solid("LampsClear"), (w * 0.3, 0.012, h * 0.3), (xc - side * w * 0.25, ye + 0.006, zc))
            if sgn < 0:  # grille between the headlamps
                gw = 2 * (hwe - w - 0.05 - 0.06)
                gz0 = p["bumper"]["z_m"][1] + 0.01
                gh = zst - 0.012 - gz0
                gc = (0, ye - 0.002, gz0 + gh / 2)
                box(self.solid("Trim"), (gw, 0.02, gh), gc)
                if d <= 1:
                    ch = self.solid("Chrome")
                    t = 0.012
                    for s_ in (-1, 1):
                        add_box(ch, (gw + 2 * t, 0.01, t), (0, ye - 0.011, gc[2] + s_ * (gh / 2 + t / 2)))
                        add_box(ch, (t, 0.01, gh), (s_ * (gw / 2 + t / 2), ye - 0.011, gc[2]))
                if d == 0:
                    for k in range(1, 5):
                        add_box(self.solid("Trim"), (gw - 0.01, 0.008, 0.008), (0, ye - 0.013, gz0 + gh * k / 5))
            else:  # rear plate (AZ: rear plate only), blank: no characters (DEC-071)
                pz = p["plate_z_m"]
                add_box(self.solid("Plate"), (0.305, 0.004, 0.152), (0, ye + 0.002, pz))
                if d <= 1:
                    add_box(self.solid("Trim"), (0.33, 0.003, 0.175), (0, ye + 0.0005, pz))

    def mirrors_handles(self):
        p, d = self.p, self.d
        mw, md, mh = p["mirror"]["size_m"]
        ym = self.f(p["mirror"]["y_m"])
        hb, zbase = self.gh_frame(ym)[:2]
        zm = zbase + 0.012 + p["mirror"]["above_belt_m"]
        xo = self.hw0 + p["mirror_out_m"]
        for side in (-1, 1):
            c = (side * (xo - mw / 2), ym, zm)
            if d >= 3:
                add_box(self.solid("Body"), (mw, md, mh), c)
                continue
            add_beveled_box(self.solid("Body"), (mw, md, mh), c, 0.03, 0.01, 3 if d == 0 else 1)
            add_box(self.solid("MirrorGlass"), (mw - 0.025, 0.004, mh - 0.025), (c[0], ym + md / 2 + 0.001, zm))
            ax0, ax1 = hb - 0.01, xo - mw + 0.01
            add_box(self.solid("Trim"), (ax1 - ax0, 0.05, 0.04), (side * (ax0 + ax1) / 2, ym + 0.01, zm - mh / 2 + 0.02))
        if d <= 1:
            for yh in p["handles_y"]:
                y = self.f(yh)
                zb, zst, _, _ = self.shoulder(y)
                z = zst - 0.07
                x = self.side_x(y, (z - zb) / (zst - zb))
                for side in (-1, 1):
                    add_beveled_box(self.solid("Body" if not p.get("chrome_handles") else "Chrome"),
                                    (0.03, 0.14, 0.028), (side * (x + 0.006), y, z), 0.012, 0.004, 2 if d == 0 else 1)
            yw = self.gh[0][0] + 0.07  # wipers parked at the base of the windshield
            for x0, x1, dy in ((-0.62, 0.02, 0.0), (0.0, 0.55, 0.03)):
                path = [(x, yw + dy, self.gh_surface_z(yw + dy, x) + 0.012) for x in (x0, (x0 + x1) / 2, x1)]
                add_sweep(self.solid("Trim"), path, rounded_rect(0.012, 0.008, 0.0, 0))

    def arch_lips(self):
        r = 0.012
        for cy, edge in self.arch_edges.items():
            edge.sort(key=lambda e: e[1])
            for side in (-1, 1):
                path = [(side * (x - r * 0.4), y, z) for x, y, z in edge]
                add_tube(self.solid("Cladding" if self.p.get("cladding") else "Body"), path, r, 8)

    def roof_rails(self):
        rr = self.p["roof_rails"]
        H, h, w = self.p["height_m"], rr["h_m"], rr["w_m"]
        y0, y1 = self.f(rr["y_m"][0]), self.f(rr["y_m"][1])
        xr = rr["x_m"]
        for side in (-1, 1):
            if self.d >= 3:
                add_box(self.solid("Trim"), (w, y1 - y0, h), (side * xr, (y0 + y1) / 2, H - h / 2))
                continue
            add_beveled_box(self.solid("Trim"), (w, y1 - y0, h), (side * xr, (y0 + y1) / 2, H - h / 2), 0.012, 0.004, 2)
            for y in (y0 + 0.06, (y0 + y1) / 2, y1 - 0.06):
                zr = self.gh_surface_z(y, xr) - 0.01
                add_box(self.solid("Trim"), (w * 0.9, 0.07, H - h - zr + 0.002), (side * xr, y, (zr + H - h + 0.002) / 2))

    def expected(self):
        p = self.p
        peak = max(z for _, z in self.gh)
        H = p["height_m"]
        if p.get("roof_rails"):
            if peak >= H:
                raise ValueError("roof rails must top the roof peak")
        elif abs(peak - H) > 1e-9:
            raise ValueError(f"height_m {H} != greenhouse peak {peak}")
        return (2 * (self.hw0 + p["mirror_out_m"]), H, self.L)

    def build(self):
        self.build_body()
        self.build_greenhouse()
        for cy in self.axles:
            for side in (-1, 1):
                self.wheel(cy, side)
        self.bumpers()
        self.lamps()
        self.mirrors_handles()
        if self.d <= 1:
            self.arch_lips()
        if self.p.get("roof_rails"):
            self.roof_rails()
        for name, bm in self.S.items():
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            emit(bm, {f: name for f in bm.faces}, self.parts)
        return self.parts.finish()


def build(p, lod):
    car = Car(p, lod)
    expected = car.expected()
    objs = car.build()
    p_, L, W = p, car.L, car.hw0 * 2
    belt = smooth(car.deck, 0.0)
    gy0, gy1 = car.gh[0][0], car.gh[-1][0]
    boxes = [collision_box("Body", (0, 0, (0.15 + belt) / 2), (W, L, belt - 0.15)),
             collision_box("Cabin", (0, (gy0 + gy1) / 2, (belt + p["height_m"]) / 2),
                           (2 * p_["greenhouse"]["roof_half_w_m"] + 0.2, gy1 - gy0, p["height_m"] - belt))]
    for i, cy in enumerate(car.axles):
        for side in (-1, 1):
            boxes.append(collision_box(f"Wheel_{i}{'L' if side < 0 else 'R'}",
                                       (side * p["track_m"] / 2, cy, car.R), (car.tw, 2 * car.R, 2 * car.R)))
    extra = {"vehicle_class": p["class"], "seed": int(p["seed"]), "collision_boxes": boxes,
             "materials_pbr": p["pbr"], "paint_variants": p["paint_variants"]}
    extra.update(wear(p))
    return objs, expected, extra
