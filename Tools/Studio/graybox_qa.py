"""Graybox QA (ART-001): contact sheet + top-down overlay against the 1-ft plan grid.

usage: python graybox_qa.py <capture_dir> <floor_plan_grid_1ft.png>
Writes contact_sheet.png, overlay_topdown.png and overlay_report.json into <capture_dir>.
Last stdout line is the one-line summary studio.ps1 records. Exit 1 if max deviation > TOLERANCE_FT.
"""
import json
import os
import sys

from PIL import Image, ImageDraw

TOLERANCE_FT = 0.5
# floor_plan_grid_1ft.png frame: bold red 5-ft lines at x=0 -> px 248.5, x=45 -> 1300.5; y=0 -> 361.5, y=75 -> 2114.5.
PLAN_X0, PLAN_Y0, PLAN_PPF = 248.5, 361.5, (1300.5 - 248.5) / 45
# Expected wall centrelines (graybox_layout.json) per scanline; outer edges are the building outline.
# Scanlines sit off the drawn 1-ft grid (.3 / .7 ft) so grid strokes don't mask the walls.
SCANS = [
    ("y", 33.3, [8.195, 13.9, 23.5]),
    ("y", 38.3, [36.695]),  # ART-007: at y 33.3 the FOH/BOH wall now starts south of the A011 vestibule (y 34.45)
    ("x", 2.7, [29.25, 36.3, 46.55]),
    ("x", 30.3, [29.25, 46.55]),
    ("x", 42.3, [29.25, 46.55]),
]
# Walls where the V5 plan raster is known wrong (GAP-120: V5 mirrors HUB / HUB 2): checked against the A011 value instead.
A011 = [("y", 60.3, [18.995]), ("y", 33.3, [31.4, 39.8])]  # + ART-007 vestibule W/E faces (GAP-122; V5 draws a 3 ft vestibule)
OUTLINE = [("y", 10.3, 0.0, 47.19), ("y", 60.3, 0.0, 47.19), ("x", 2.7, 0.0, 76.03), ("x", 42.3, 0.0, 76.03)]


def runs(flags):
    """Centres (index) of runs of True, bridging single-pixel breaks (grid lines)."""
    out, start, gap = [], None, 0
    for i, f in enumerate(flags + [False, False]):
        if f:
            if start is None:
                start = i
            gap, end = 0, i
        elif start is not None:
            gap += 1
            if gap > 1:
                out.append(((start + end) / 2, end - start + 1))
                start, gap = None, 0
    return out


class Sampler:
    def __init__(self, img, x0, y0, ppf, is_wall):
        self.px, self.w, self.h = img.load(), img.size[0], img.size[1]
        self.x0, self.y0, self.ppf, self.is_wall = x0, y0, ppf, is_wall

    def line(self, axis, at_ft, lo_ft, hi_ft):
        """Wall flags along a scanline from lo_ft to hi_ft, plus the ft value of each sample."""
        fts, flags = [], []
        n = int((hi_ft - lo_ft) * self.ppf)
        for i in range(n + 1):
            f = lo_ft + i / self.ppf
            x, y = (f, at_ft) if axis == "y" else (at_ft, f)
            px, py = round(self.x0 + x * self.ppf), round(self.y0 + y * self.ppf)
            if 0 <= px < self.w and 0 <= py < self.h:
                fts.append(f)
                flags.append(self.is_wall(self.px[px, py]))
        return fts, flags

    def nearest_wall(self, axis, at_ft, expect_ft, window=1.0):
        fts, flags = self.line(axis, at_ft, expect_ft - window, expect_ft + window)
        cands = [(fts[0] + c / self.ppf, n) for c, n in runs(flags) if n >= 3]
        return min(cands, key=lambda c: abs(c[0] - expect_ft))[0] if cands else None

    def outline(self, axis, at_ft, lo, hi, window=1.5):
        """Outer edges: first/last building pixel scanning in from outside."""
        fts, flags = self.line(axis, at_ft, lo - window, hi + window)
        inside = [f for f, b in zip(fts, flags) if b]
        return (inside[0], inside[-1]) if inside else (None, None)


def plan_gap(p):  # light-blue / white wall gaps on the dark plan fill
    return p[0] >= 120 and p[1] >= 170 and p[2] >= 200 or p == (255, 180, 180)


def plan_building(p):  # room fill + outline stroke vs white page; red grid lines run past the outline
    return sum(p) < 700 and not (p[0] > 200 and p[1] < 100)


def main(cap_dir, plan_path):
    manifest = json.load(open(os.path.join(cap_dir, "captures.json"), encoding="utf-8"))
    plan = Image.open(plan_path).convert("RGB")
    top = Image.open(os.path.join(cap_dir, manifest["topDown"])).convert("RGB")
    ppf, margin = manifest["topDownPxPerFt"], manifest["topDownMarginFt"]
    lum = list(top.convert("L").tobytes())
    floor_lum = sorted(lum)[len(lum) // 2]
    wall_thr = (floor_lum + max(lum)) / 2  # walls (0.82 albedo) are the brightest surface in the plan view
    bldg_thr = (floor_lum + lum[0]) / 2  # corner pixel is exterior ground, darker than the floor slab

    cap_wall = Sampler(top, margin * ppf, margin * ppf, ppf, lambda p: sum(p) / 3 > wall_thr)
    cap_bldg = Sampler(top, margin * ppf, margin * ppf, ppf, lambda p: sum(p) / 3 > bldg_thr)
    pl_gap = Sampler(plan, PLAN_X0, PLAN_Y0, PLAN_PPF, plan_gap)
    pl_bldg = Sampler(plan, PLAN_X0, PLAN_Y0, PLAN_PPF, plan_building)

    rows, devs = [], []
    for axis, at, expects in SCANS:
        for e in expects:
            c, p = cap_wall.nearest_wall(axis, at, e), pl_gap.nearest_wall(axis, at, e)
            d = abs(c - p) if c is not None and p is not None else None
            rows.append({"scan": f"{axis}={at}", "expect": e, "capture": c, "plan": p, "dev": d})
            devs.append(d)
    for axis, at, expects in A011:
        for e in expects:
            c = cap_wall.nearest_wall(axis, at, e)
            d = abs(c - e) if c is not None else None
            rows.append({"scan": f"{axis}={at} A011", "expect": e, "capture": c, "plan": e, "dev": d})
            devs.append(d)
    for axis, at, lo, hi in OUTLINE:
        c, p = cap_bldg.outline(axis, at, lo, hi), pl_bldg.outline(axis, at, lo, hi)
        for k, e in enumerate((lo, hi)):
            d = abs(c[k] - p[k]) if c[k] is not None and p[k] is not None else None
            rows.append({"scan": f"{axis}={at} outline", "expect": e, "capture": c[k], "plan": p[k], "dev": d})
            devs.append(d)

    missing = sum(d is None for d in devs)
    max_dev = max((d for d in devs if d is not None), default=None)
    report = {"toleranceFt": TOLERANCE_FT, "maxDeviationFt": max_dev, "missing": missing, "samples": rows,
              "method": "wall centreline (interior) / outer edge (outline) per scanline, capture vs plan, in ft"}
    json.dump(report, open(os.path.join(cap_dir, "overlay_report.json"), "w"), indent=2)
    for r in rows:
        print(f"  {r['scan']:<16} expect={r['expect']:<7} capture={fmt(r['capture'])} plan={fmt(r['plan'])} dev={fmt(r['dev'])}")

    # Overlay: capture resampled into the plan's pixel frame, 50 % blend.
    s = ppf / PLAN_PPF
    warped = top.transform(plan.size, Image.AFFINE, (s, 0, margin * ppf - PLAN_X0 * s, 0, s, margin * ppf - PLAN_Y0 * s))
    Image.blend(plan, warped, 0.5).save(os.path.join(cap_dir, "overlay_topdown.png"))

    # Contact sheet of every reference view.
    caps = manifest["captures"]
    tw, th, cols, label = 384, 216, 4, 18
    sheet = Image.new("RGB", (cols * tw, ((len(caps) + cols - 1) // cols) * (th + label)), (20, 20, 20))
    draw = ImageDraw.Draw(sheet)
    for i, c in enumerate(caps):
        x, y = (i % cols) * tw, (i // cols) * (th + label)
        sheet.paste(Image.open(os.path.join(cap_dir, c["file"])).convert("RGB").resize((tw, th)), (x, y + label))
        draw.text((x + 4, y + 3), f"{c['cameraId']}  [{c['conf']}]", fill=(230, 230, 230))
    sheet.save(os.path.join(cap_dir, "contact_sheet.png"))

    rooms = rooms_sheet(cap_dir, manifest)
    ok = missing == 0 and max_dev is not None and max_dev <= TOLERANCE_FT
    print(f"views={len(caps)} maxDeviationFt={fmt(max_dev)} missing={missing} tolerance={TOLERANCE_FT}{rooms} {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def rooms_sheet(cap_dir, manifest):
    """ART-007: top-down with fixtures + the review views (registers, deli walls, HUB, office, entry) on one sheet."""
    views = manifest.get("views") or []
    if not views or not manifest.get("topDownFixtures"):
        return ""
    top = Image.open(os.path.join(cap_dir, manifest["topDownFixtures"])).convert("RGB")
    tw, th, cols, label = 640, 360, 3, 22
    rows = (len(views) + cols - 1) // cols
    h = rows * (th + label)
    top = top.resize((round(top.size[0] * h / top.size[1]), h))
    sheet = Image.new("RGB", (top.size[0] + cols * tw, h), (20, 20, 20))
    sheet.paste(top, (0, 0))
    draw = ImageDraw.Draw(sheet)
    draw.text((6, 4), "top-down (fixtures on, north up)", fill=(255, 255, 0))
    for i, v in enumerate(views):
        x, y = top.size[0] + (i % cols) * tw, (i // cols) * (th + label)
        sheet.paste(Image.open(os.path.join(cap_dir, v["file"])).convert("RGB").resize((tw, th)), (x, y + label))
        draw.text((x + 4, y + 4), v["cameraId"], fill=(230, 230, 230))
    sheet.save(os.path.join(cap_dir, "rooms_sheet.png"))
    return f" roomsSheet={len(views)}+topdown"


def fmt(v):
    return "None" if v is None else f"{v:.2f}"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
