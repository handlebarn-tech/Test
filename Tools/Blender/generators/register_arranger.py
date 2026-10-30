"""PROC-006b register station dressing arranger (DEC-104 non-uniform rule).

One seed per station -> one placement JSON per station. Fixed items (keyboard, mouse always right, scanner, receipt
printer, label printer) are at every register; everything else is optional with weights. Pure Python (no bpy):
  python Tools/Blender/generators/register_arranger.py [params.json]
Station frame and anchor bindings: params `arranger._note` (ROOM_FIXTURES rev7 POS_xx / Trash_Small_POS_xx).
"""
import json
import math
import os
import random
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PARAMS = os.path.join(ROOT, "Tools", "Blender", "params", "register_kit.json")
FT = 0.3048
FACING = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}  # plan frame: +x east, +y south
OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}


def stations(fixtures):
    """rev7 POS rows with their local frame: origin on the counter's staff edge at the monitor, u right, v forward."""
    rows = [f for f in fixtures if f.get("type") == "register_station"]
    bins = {f["fixture"][len("Trash_Small_"):]: f for f in fixtures if f.get("fixture", "").startswith("Trash_Small_POS_")}
    out = []
    for f in rows:
        fx, fy = FACING[OPPOSITE[f["staff_side"]]]
        rx, ry = -fy, fx  # operator's right hand
        oz = f["operator_zone"]
        edge = {"N": oz["y0"], "S": oz["y1"], "E": oz["x1"], "W": oz["x0"]}[OPPOSITE[f["staff_side"]]]
        px, py = f["pos_ft"]
        origin = (px, edge) if fy else (edge, py)

        def local(x, y, o=origin, r=(rx, ry), fw=(fx, fy)):
            dx, dy = x - o[0], y - o[1]
            return round((dx * r[0] + dy * r[1]) * FT, 4), round((dx * fw[0] + dy * fw[1]) * FT, 4)

        # TOP width: half the distance to the nearest POS on the same run (same staff side and counter line)
        same = [g for g in rows if g is not f and g["staff_side"] == f["staff_side"]
                and abs((g["pos_ft"][1] - py) if fy else (g["pos_ft"][0] - px)) < 1.0]
        pitch = min(math.dist(g["pos_ft"], f["pos_ft"]) for g in same) * FT if same else 0.975
        sr = f["stand_rect"]
        c = [local(sr[a], sr[b]) for a, b in (("x0", "y0"), ("x1", "y1"))]
        stand = {"u": sorted(p[0] for p in c), "v": sorted(p[1] for p in c)}
        b = bins.get(f["fixture"])
        out.append({"fixture": f["fixture"], "reg": f["reg"], "frame_plan_ft": {"origin": origin, "right": (rx, ry), "forward": (fx, fy)},
                    "half_pitch_m": round(pitch / 2, 4), "stand_m": stand,
                    "bin_m": local(*b["pos_ft"]) if b else None, "bin_fixture": b["fixture"] if b else None})
    return sorted(out, key=lambda s: s["reg"])


def zone(st, name, a):
    """Placement rectangle (u0, u1, v0, v1) for an anchor, or a point/edge as a degenerate rectangle."""
    if name.startswith("STAND"):
        (u0, u1), (v0, v1) = st["stand_m"]["u"], st["stand_m"]["v"]
        return (u0, u0, v0, v1) if a.get("edge") else (u0, u1, v0, v1)  # edge = the stand face toward the operator
    if name == "FLOOR_STAND":
        u, v = st["bin_m"]
        return (u, u, v, v)
    h = st["half_pitch_m"]
    return (-h, h, *a["v_m"])


def arrange(st, p, seed):
    ar, items = p["arranger"], {i["id"]: i for i in p["items"]}
    rng = random.Random(seed)
    placed, dropped = [], []
    taken = {}  # anchor -> [(u0, u1, v0, v1)]
    clr = ar["clearance_m"]

    def foot(iid, yaw):  # axis-aligned footprint of the yawed size box
        w, d = items[iid]["size_m"][:2]
        c, s = abs(math.cos(math.radians(yaw))), abs(math.sin(math.radians(yaw)))
        return w * c + d * s, w * s + d * c

    def free(anchor, u, v, w, d, zn, edge_or_point):
        r = (u - w / 2, u + w / 2, v - d / 2, v + d / 2)
        if not edge_or_point and (r[0] < zn[0] - 1e-6 or r[1] > zn[1] + 1e-6 or r[2] < zn[2] - 1e-6 or r[3] > zn[3] + 1e-6):
            return None
        if not edge_or_point and anchor in ("UNDER_UPPER", "UNDER_LOWER") and r[2] > zn[2] + 0.06:
            return None  # shelf stock sits at the open front, not pushed to the back
        for t in taken.get(anchor, []):
            if r[0] < t[1] + clr and t[0] < r[1] + clr and r[2] < t[3] + clr and t[2] < r[3] + clr:
                return None
        return r

    def put(iid, anchor, u, v, yaw, r, cond=None):
        taken.setdefault(anchor, []).append(r)
        a = ar["anchors"][anchor]
        e = {"asset": "PROC_RK_" + iid, "rk": items[iid]["rk"], "anchor": anchor, "pos_m": [round(u, 4), round(v, 4), a["z_m"]],
             "yaw_deg": round(yaw, 1)}
        if cond:
            e["condition"] = cond
        placed.append(e)

    def condition(iid):
        c = {"wear_scale": round(rng.uniform(*ar["condition"]["wear_scale"]), 2)}
        if "optional_parts" in items[iid] or items[iid]["kind"] in ("trash_bin", "spray_bottle"):
            c["fill_level"] = round(rng.uniform(*ar["condition"]["fill_level"]), 2)
        return c

    # fixed items, TOP anchor; the monitor keep-out is reserved first
    mk = ar["monitor_keepout_m"]
    taken["TOP"] = [(mk["u"][0], mk["u"][1], mk["v"][0], mk["v"][1])]
    top = zone(st, "TOP", ar["anchors"]["TOP"])
    pos = {}
    for fx in ar["fixed"]:
        iid = fx["id"]
        yaw = rng.uniform(-fx["yaw_deg"], fx["yaw_deg"])
        w, d = foot(iid, yaw)
        ju, jv = fx["jitter_m"]
        if "slots" in fx:
            slots = fx["slots"][:]
            rng.shuffle(slots)
        elif "right_of" in fx or "left_of" in fx:
            ref = fx.get("right_of") or fx.get("left_of")
            ru, rw = pos[ref]
            off = rw / 2 + rng.uniform(*fx["gap_m"]) + w / 2
            slots = [[ru + off if "right_of" in fx else ru - off, fx["v"]]]
        else:
            slots = [[fx["u"], fx["v"]]]
        for su, sv in slots:
            u, v = su + rng.uniform(-ju, ju), sv + rng.uniform(-jv, jv)
            r = free("TOP", u, v, w, d, top, False)
            if r:
                put(iid, "TOP", u, v, yaw, r, condition(iid))
                pos[iid] = (u, w)
                break
        else:
            raise RuntimeError(f"{st['fixture']}: fixed item {iid} does not fit the TOP zone {top}")

    # optional items: presence by weight, then count, asset variant, anchor, free spot
    for g in ar["optional"]:
        if rng.random() >= g["p"]:
            continue
        for _ in range(rng.randint(*g["count"])):
            iid = rng.choice(g["assets"])
            anchors = [a for a in items[iid]["anchors"] if a != "FLOOR_STAND" or st["bin_m"]]
            ok = False
            for _ in range(ar["place_tries"]):
                anchor = rng.choice(anchors)
                a = ar["anchors"][anchor]
                yaw = a.get("yaw_base_deg", 0) + rng.uniform(-g["yaw_deg"], g["yaw_deg"])
                w, d = foot(iid, yaw)
                zn = zone(st, anchor, a)
                pt = a.get("edge") or a.get("point")
                j = a.get("jitter_m", 0.0)
                u = rng.uniform(zn[0], zn[1]) + rng.uniform(-j, j) if pt else rng.uniform(zn[0] + w / 2, max(zn[0] + w / 2, zn[1] - w / 2))
                v = rng.uniform(zn[2], zn[3]) + rng.uniform(-j, j) if pt else rng.uniform(zn[2] + d / 2, max(zn[2] + d / 2, zn[3] - d / 2))
                if anchor == "FLOOR_STAND":  # rev7: against the back of the scale stand, never inside it
                    v = min(v, st["stand_m"]["v"][0] - d / 2 - clr)
                r = free(anchor, u, v, w, d, zn, pt)
                if r:
                    put(iid, anchor, u, v, yaw, r, condition(iid))
                    ok = True
                    break
            if not ok:
                dropped.append(iid)
    return placed, dropped


def run(params_path=PARAMS, write=True):
    p = json.load(open(params_path, encoding="utf-8"))
    ar = p["arranger"]
    fixtures = json.load(open(os.path.join(ROOT, ar["fixtures"]), encoding="utf-8"))["fixtures"]
    out = {}
    for st in stations(fixtures):
        seed = ar["seed"] * 100 + int(st["reg"])
        placed, dropped = arrange(st, p, seed)
        anchors = {k: {"fixture": st["fixture"], **{kk: vv for kk, vv in v.items() if kk in ("z_m", "gap", "_src")}}
                   for k, v in ar["anchors"].items()}
        anchors["FLOOR_STAND"]["fixture"] = st["bin_fixture"]
        out[st["fixture"]] = {
            "station": st["fixture"], "reg": st["reg"], "seed": seed, "generator": "register_arranger",
            "frame": {"_note": "metres; origin = monitor position along the counter, on the counter's staff edge, at the floor; "
                               "u = operator's right, v = toward the customer, z = up", **st["frame_plan_ft"]},
            "top_half_width_m": st["half_pitch_m"], "stand_m": st["stand_m"], "anchors": anchors,
            "items": placed, "not_fitted": dropped}
    if write:
        d = os.path.join(ROOT, ar["out_dir"])
        os.makedirs(d, exist_ok=True)
        for k, v in out.items():
            with open(os.path.join(d, f"{k}.json"), "w", newline="\n") as f:
                json.dump(v, f, indent=1)
                f.write("\n")
    return out


if __name__ == "__main__":
    res = run(*sys.argv[1:2])
    for k, v in res.items():
        print(k, len(v["items"]), "items", sorted({i["asset"][8:] for i in v["items"]}), "not fitted:", v["not_fitted"])
