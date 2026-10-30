"""ART-006: write the back-room fixtures of Docs/Reference/ROOM_FIXTURES.json (REF-owned) into graybox_layout.json.

usage: python Tools/Studio/room_fixtures_layout.py
Deterministic: replaces every fixture of ROOMS (ids "<Room>_<fixture>" plus the legacy hand-placed FX_ ids) and the
two DEC-040 desk anchors, then GrayboxBuilder (studio.ps1 unity-graybox) builds them. Re-run whenever REF updates rev.
Rules (ART-006 packet): positions/sizes only from ROOM_FIXTURES; footprint = size_ft [w, d] with w along +x at rot 0 and
along +y at rot 90; doors are wall openings (W_* in the layout), not boxes; rows with pos null are skipped with their gap.
Bases: a row standing on furniture (its centre inside a larger desk/table/counter/rack footprint) sits on that top;
wall-mounted rows take the height their REF note quotes (BASE_FT below, each with its quote).
"""
import json
import math
import os
import random
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "Docs", "Reference", "ROOM_FIXTURES.json")
LAYOUT = os.path.join(ROOT, "UnityProject", "Assets", "_Game", "Art", "Graybox", "graybox_layout.json")
ROOMS = ("Office", "BreakRoom", "FOH", "BOH", "Restroom", "Hall", "Vestibule")  # ART-007: the vestibule shell is built (A011, GAP-122)
LEGACY = {"FX_Office_ITRack", "FX_Office_Safe", "FX_Office_Desk_L", "FX_Break_Kitchen_L", "FX_Break_Bench", "FX_JC_Closet",
          "FX_FOH_WireRack_1", "FX_FOH_WireRack_2", "FX_FOH_Fridge", "FX_BOH_Racks_W", "FX_BOH_Racks_E", "FX_FOH_Desk",
          "FX_FOH_Computer", "FX_FOH_Chair", "FX_FOH_ChairBack", "FX_BOH_Desk", "FX_BOH_Computer", "FX_BOH_Chair", "FX_BOH_ChairBack"}
SUPPORTS = {"desk", "table", "counter", "rack", "stand"}
NOT_STACKED = {"plumbing", "ladder", "cabinet", "chair", "signage", "shelf", "lighting", "wall", "room_volume", "floor_mat", "locker", "fridge",
               "cooler", "bin", "door", "desk", "table", "counter", "bench", "trash_bin", "pallet", "stand"}
CEILING_FT = 9.0  # graybox back-room ceiling (DEC-037)
# Wall-mounted bottoms (ft AFF) quoted from the REF notes; first value of a quoted range.
BASE_FT = {
    "Neon_TheFlowerShop": 5.75,      # "bottom ~5.5-6 ft AFF"
    "Board_West_BlackFrame": 3.5,    # "below the neon" (neon bottom 5.75, board 2.0 tall; Low)
    "Board_North_Fabric": 3.5,       # "~3.5-6.5 ft AFF"
    "Uppers_North": 4.5,             # "~4.5-7.0 ft AFF"
    "Uppers_East": 4.5,              # same type as Uppers_North
    "Shelf_Deli_Canisters": 4.8,     # "at ~4.8 ft AFF"
    "Whiteboard_West": 3.5,          # "~3.5-6.5 ft AFF"
    "Poster_LaborLaw": 3.5,          # "~3.5-6.5 ft AFF"
    "FirstAid_Kit": 4.5,             # "~4.5 ft AFF"
    "ElectricalBox_Wall": 4.0,       # "~4-7 ft AFF"
    "Fan_Portable": 6.5,             # "base 6.5 ft AFF" (on the IT box on the standing desk)
    "Mirror": 3.333,                 # "bottom 3'-4\" AFF kept"
    "GrabBar_North": 2.75,           # "at 33-36 in AFF"
    "GrabBar_West": 2.75,            # "at 33-36 in AFF"
    "Accessories": 3.5,              # dispensers, height not given (Low, convention)
    "Panel_Blank": 4.0,              # blank panel, height not given (Low, convention)
    "Board_Cork": 3.7,               # "centre ~5 ft AFF" with a 2.6 ft board
    "Board_Bulletin_West": 3.5,      # height not given; same convention as the whiteboard (Low)
}
# Review minors applied in the build (Hub: "apply REVIEW-W4U minors"; ROOM_FIXTURES itself is REF's).
OVERRIDES = {
    "Mops_Brooms_JC": {"pos_ft": [22.4, 43.4]},  # W4U m1: centred on the JC east-wall line, moved inside
}
# ART-007: what a closed cabinet holds is shown in its name (the row has no contents field)
TAGS = {"Cabinet_Storage_Large": "holds: bathroom supplies + the store's main cleaning supplies (DEC-062, DEC-104)"}
# The JC (room_volume) is built as two partition walls with its door opening, so its contents are visible.
JC_WALLS = [("W_JC_W", 19.3, 41.3, 19.3, 46.3), ("W_JC_N", 19.3, 41.3, 23.31, 41.3)]
JC_T = 0.33
SHELF_LEVELS = {"Shelves_Floating_x3": [5.0, 5.7, 6.3]}  # "staggered at ~5.0 / 5.7 / 6.3 ft AFF"
SOLID = {"plumbing", "ladder", "desk", "table", "counter", "cabinet", "rack", "fridge", "cooler", "locker", "wall", "room_volume", "bench",
         "cart", "bin", "chair", "prop", "sink", "trash_bin", "pallet", "stand"}
# Openings the REF door rows move (GAP-123): wall id, opening id, A011 span along the wall.
DOOR_OPENINGS = {"Door_Hall_Office": ("W_Band_Office", "DOOR_Hall_Office", 10.2, 13.3),
                 "Door_Office_HUB2": ("W_Back_Hub", "DOOR_Office_HUB", 7.2, 10.2),
                 "Door_Hall_Break": ("W_Hall_Break", "DOOR_Hall_Break", 29.9, 33.0),
                 "Door_Hall_Restroom": ("W_Restroom_Hall", "DOOR_Hall_Restroom", 33.1, 36.1)}
ANCHORS = {"Anchor_FOH_Desk": ("FOH", "Chair_Desk", "Desk_WireRack_Computer"),
           "Anchor_BOH_Desk": ("BOH", "Chair_Desk", "Desk_ExRegister1")}


def rect(row):
    (x, y), (w, d) = row["pos_ft"], row["size_ft"][:2]
    hx, hy = (w / 2, d / 2) if row["rot"] == 0 else (d / 2, w / 2)
    return {"x0": round(x - hx, 3), "x1": round(x + hx, 3), "y0": round(y - hy, 3), "y1": round(y + hy, 3)}


def inside(r, x, y):
    return r["x0"] <= x <= r["x1"] and r["y0"] <= y <= r["y1"]


def base_of(row, rows):
    if row["fixture"] in BASE_FT:
        return BASE_FT[row["fixture"]]
    if row["type"] == "lighting":
        return CEILING_FT - row["size_ft"][2]
    if row["type"] == "sink" and row["fixture"] != "MopSink_JC":
        return 2.833 - row["size_ft"][2]  # bowl hangs under the 34 in rim (TI OS3)
    if row["type"] in NOT_STACKED:
        return 0.0
    x, y = row["pos_ft"]
    area = row["size_ft"][0] * row["size_ft"][1]
    under = [s for s in rows if s is not row and s["type"] in SUPPORTS and s["size_ft"][0] * s["size_ft"][1] > area
             and inside(rect(s), x, y)]
    return max((base_of(s, rows) + s["size_ft"][2] for s in under), default=0.0)


def dump(layout):
    """The layout's house style: one line per array row, nested objects indented."""
    parts = []
    for k, v in layout.items():
        if isinstance(v, list):
            body = ",\n".join("    " + json.dumps(x, ensure_ascii=False) for x in v)
            parts.append(f'  "{k}": [\n{body}\n  ]')
        else:
            parts.append(f'  "{k}": ' + json.dumps(v, indent=2, ensure_ascii=False).replace("\n", "\n  "))
    return "{\n" + ",\n".join(parts) + "\n}\n"


def main():
    src = json.load(open(SRC, encoding="utf-8"))
    rows = [dict(r, **OVERRIDES.get(r["fixture"], {})) for r in src["fixtures"] if r["room"] in ROOMS]
    with open(LAYOUT, encoding="utf-8") as f:
        text = f.read()
    layout = json.loads(text)
    rev = next((t for t in src["version"].split() if t.startswith("rev")), src["version"])
    note = f"ROOM_FIXTURES {rev}"
    skipped, made = [], []
    for r in rows:
        if r["type"] in ("door", "room_shell_proposal") or r["fixture"] == "JC_Closet":
            continue  # wall openings / JC walls / vestibule shell below; leaves come from DOORS.json (sales_floor.py)
        if r["pos_ft"] is None:
            skipped.append(f"{r['room']}_{r['fixture']} ({r.get('gap') or 'no position'})")
            continue
        levels = SHELF_LEVELS.get(r["fixture"], [None])
        for k, lvl in enumerate(levels):
            fid = f"{r['room']}_{r['fixture']}" + (f"_{k}" if len(levels) > 1 else "")
            made.append({"id": fid, "zone": "BackRooms", "h": "", "hFt": r["size_ft"][2],
                         "baseFt": round(lvl if lvl is not None else base_of(r, rows), 3),
                         "conf": r["confidence"], "solid": r["type"] in SOLID, "rects": [rect(r)],
                         "note": f"{note}; type {r['type']}" + (f"; {r['gap']}" if r.get("gap") else "")}
                        | ({"tag": TAGS[r["fixture"]]} if r["fixture"] in TAGS else {}))
    fixtures = [f for f in layout["fixtures"] if not (f["zone"] == "BackRooms" and (f["id"] in LEGACY or f["id"].split("_")[0] in ROOMS))]
    layout["fixtures"] = fixtures + made
    for r in rows:  # door openings (GAP-123)
        if r["fixture"] in DOOR_OPENINGS:
            wid, oid, a, b = DOOR_OPENINGS[r["fixture"]]
            wall = next(w for w in layout["walls"] if w["id"] == wid)
            op = next(o for o in wall["openings"] if o["id"] == oid)
            op.update({"from": a, "to": b, "conf": r["confidence"], "note": f"A011 via ROOM_FIXTURES {r['fixture']} (GAP-123)"})
    jc = next(r for r in rows if r["fixture"] == "Door_JC")
    half = jc["size_ft"][0] / 2
    layout["walls"] = [w for w in layout["walls"] if w["id"] not in {j[0] for j in JC_WALLS}]
    for wid, ax, ay, bx, by in JC_WALLS:
        w = {"id": wid, "zone": "BackRooms", "conf": "Med", "ax": ax, "ay": ay, "bx": bx, "by": by, "t": JC_T, "gap": "GAP-104",
             "openings": [], "note": "JC partition from ROOM_FIXTURES JC_Closet (A011 x 19.3-23.31, y 41.3-46.3)"}
        if ax == bx and ax == jc["pos_ft"][0]:
            w["openings"].append({"id": "DOOR_JC", "from": round(jc["pos_ft"][1] - half, 3), "to": round(jc["pos_ft"][1] + half, 3),
                                  "h": "door", "conf": jc["confidence"], "note": "Door_JC 2'-8\" (ROOM_FIXTURES)"})
        layout["walls"].append(w)
    for aid, (room, chair, desk) in ANCHORS.items():
        c = next(r for r in rows if r["room"] == room and r["fixture"] == chair)
        dsk = next(r for r in rows if r["room"] == room and r["fixture"] == desk)
        a = next(a for a in layout["anchors"] if a["id"] == aid)
        dx, dy = dsk["pos_ft"][0] - c["pos_ft"][0], dsk["pos_ft"][1] - c["pos_ft"][1]
        yaw = 90 if abs(dx) >= abs(dy) and dx > 0 else 270 if abs(dx) >= abs(dy) else 180 if dy > 0 else 0
        a.update({"x": c["pos_ft"][0], "y": c["pos_ft"][1], "yaw": yaw, "note": f"DEC-040 chair spot facing {desk} (ROOM_FIXTURES)"})
    print(sales_floor(layout, src))
    out = dump(layout)
    with open(LAYOUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"room fixtures: {len(made)} written, {len(LEGACY)} legacy removed, skipped: {', '.join(skipped) or 'none'}")


# ---------------------------------------------------------------------------------------------------------------------
# ART-007 (DEC-096 playtest 1): sales floor + HUB from ROOM_FIXTURES rev7 (REF-011/012), doors from DOORS.json, anchors
# from SCENE_ANCHORS.json, the A011 vestibule shell (GAP-122). Everything is read from the JSONs, so a REF re-run is
# picked up by re-running this script; only layout choices (Low, named below) are constants.
DOORS_SRC = os.path.join(ROOT, "Docs", "Reference", "DOORS.json")
ANCHORS_SRC = os.path.join(ROOT, "Docs", "Reference", "SCENE_ANCHORS.json")
FLOOR_ZONES = {"Retail": "Retail", "HUB": "Hub", "HUB2": "Hub"}
# Graybox ids the rev7 rows replace (LAYOUT_AUDIT_SALES_FLOOR R1-R3, R6, D1-D2, H1-H3, H7)
RETIRED = {"FX_DeliCounter_L", "FX_DeliJarWall_N_Back", "FX_JarWall_E_Back", "FX_DeliJarWall_S", "FX_HUB_Desks", "FX_HUB_RackRun_N",
           "FX_HUB_RackRun_W", "FX_HUB_RackIsland", "FX_HUB_Pallets", "FX_HUB2_Cabinets"}
GEN_PREFIX = ("Retail_", "HUB_", "HUB2_", "POS_", "FX_RegisterCounter_", "FX_DeliJarWall_")
# Register runs merged per id so the lookdev millwork keeps one entry per run.
COUNTERS = {"FX_RegisterCounter_L": ("Counter_Register_North", "Counter_Register_EastReturn"),
            "FX_RegisterCounter_S": ("Counter_Register_South", "Counter_Register_SouthWestReturn")}
YAW = {"N": 0, "E": 90, "S": 180, "W": 270}
# Deli wall build (REFERENCES_INDEX 8.3: back counter + 2 tiers, jars on the counter too). Layout choices, Low (GAP-133/GAP-002):
# back panel 0.3 ft, tier depth 1.0 ft, tiers at the old 4.25 / 5.5 ft placeholders, 1 ft jar pitch, kraft bags 1.5 ft.
JAR_BACK, JAR_TIER_D, JAR_PITCH, KRAFT_FT, KRAFT_H = 0.3, 1.0, 1.0, 1.5, 0.9
JAR_ROWS = (("Counter", None), ("Mid", 4.25), ("Top", 5.5))
# 8.4 stocking note, share of jar positions occupied (range midpoints); east arched bays ~1 jar per bay with 1-jar gaps.
FILL = {"Counter": 0.35, "Mid": 0.55, "Top": 0.9}
FILL_ARCHED = {"Counter": 0.35, "Mid": 0.5, "Top": 0.5}
QUEUE_CLEAR_FT = 3.0  # packet: stanchions clear the moved south counter by >= 3 ft
# REF-011 re-pose (REFERENCES_INDEX 2 rows R2C3-R2C5, 8.1): behind the south run on its jar-wall side, looking north.
# x / yaw / pitch are read by eye from the tile descriptions (Low); y = mid-depth of the south jar wall's back panel.
CAMERA_POSES = {"R2C3": (28.0, 20, 30, "behind the south run looking N/NE at the north run, east jar wall on the side (REF-011)"),
                "R2C4": (24.0, 350, 28, "'Back Of Register center': behind the south run looking N (REF-011)"),
                "R2C5": (34.0, 315, 25, "behind the south run's east end looking NW (REF-011)")}
# DEC-104 station kit (placeholders, sizes are conventions, Low): mandatory items are on every station, the rest vary.
KIT_H = {"Keyboard": 0.1, "Mouse": 0.12, "Scanner": 0.55, "ReceiptPrinter": 0.5, "LabelPrinter": 0.6, "CardTerminal": 0.45, "Rag": 0.06, "ISOSpray": 0.8}
KIT_WD = {"Keyboard": (1.45, 0.5), "Mouse": (0.2, 0.35), "Scanner": (0.3, 0.35), "ReceiptPrinter": (0.5, 0.6), "LabelPrinter": (0.6, 0.65),
          "CardTerminal": (0.35, 0.55), "Rag": (0.6, 0.5), "ISOSpray": (0.25, 0.25)}
CONDITIONS = ("clean", "worn", "scuffed", "taped", "dusty")
DOOR_T = 0.146  # 1-3/4 in leaf (DOORS _about)


def staff_dir(side):
    return {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}[side]


def local(st, t0, t1, n0, n1):
    """GrayboxBuilder.Local: t along the staff's right, n toward the staff side, from the station point."""
    nx, ny = staff_dir(st["staff"])
    tx, ty = ny, -nx  # right of facing f = -n is (-f.y, f.x) = (n.y, -n.x)
    ax, ay = st["x"] + tx * t0 + nx * n0, st["y"] + ty * t0 + ny * n0
    bx, by = st["x"] + tx * t1 + nx * n1, st["y"] + ty * t1 + ny * n1
    return {"x0": round(min(ax, bx), 3), "x1": round(max(ax, bx), 3), "y0": round(min(ay, by), 3), "y1": round(max(ay, by), 3)}


def t_of(st, x, y):
    nx, ny = staff_dir(st["staff"])
    return (x - st["x"]) * ny + (y - st["y"]) * -nx


def band(r, faces, d0, d1):
    """Sub-rect of a wall footprint d0..d1 ft from its back face (the side opposite `faces`)."""
    if faces == "S":
        return dict(r, y0=round(r["y0"] + d0, 3), y1=round(r["y0"] + d1, 3))
    if faces == "N":
        return dict(r, y0=round(r["y1"] - d1, 3), y1=round(r["y1"] - d0, 3))
    if faces == "W":
        return dict(r, x0=round(r["x1"] - d1, 3), x1=round(r["x1"] - d0, 3))
    return dict(r, x0=round(r["x0"] + d0, 3), x1=round(r["x0"] + d1, 3))


def overlap(a, b, eps=0.005):
    return a["x0"] < b["x1"] - eps and b["x0"] < a["x1"] - eps and a["y0"] < b["y1"] - eps and b["y0"] < a["y1"] - eps


def fx(fid, zone, rects, h_ft, base, conf, solid, note, **extra):
    return dict({"id": fid, "zone": zone, "h": "", "hFt": h_ft, "baseFt": round(base, 3), "conf": conf, "solid": solid, "rects": rects, "note": note}, **extra)


def station_kit(st, lo, hi, counter_ft, stand, rng):
    """One station's small items (DEC-104: never uniform). lo/hi = this station's share of its counter, in t."""
    out = []

    def put(name, t0, n0, base, yaw_jit, where):
        w, d = KIT_WD[name]
        out.append((name, local(st, t0, t0 + w, n0, n0 - d), base, round(rng.uniform(-yaw_jit, yaw_jit), 1), where, rng.choice(CONDITIONS)))

    # Counter rows across the 2.2 ft top, staff side first: row 1 just past the monitor base. Items that do not fit move
    # to the next row; past the last row the label printer goes to the stand shelf and the rag to the stand top.
    rows = [(-0.38 - rng.uniform(0, 0.05), ["KB", "Scanner"]), (-0.95, ["ReceiptPrinter", "LabelPrinter"]), (-1.62, ["CardTerminal"])]
    if rng.random() < 0.6:
        rows[1][1].append("Rag")  # blue rag (R5), not on every station
    if rng.random() < 0.3:
        rows[1][1].remove("LabelPrinter")  # label printer placement varies (R2): on the stand shelf here
        put("LabelPrinter", stand["offsetT"] + rng.uniform(0.05, stand["w"] - 0.65), stand["d"] - 0.1, stand["shelvesFt"][0] + stand["board"], 6, "stand shelf")
    carry = []
    for k, (n0, names) in enumerate(rows):
        rng.shuffle(names)
        if "KB" in names and hi - lo < 2.9:  # a short share only fits the keyboard if it goes first
            names.remove("KB")
            names.insert(0, "KB")
        names, carry, t = names + carry, [], lo + rng.uniform(0.0, 0.3)  # the row's own items first
        for name in names:
            w = 1.45 + 0.15 + 0.2 if name == "KB" else KIT_WD[name][0]  # keyboard + gap + mouse travel as one unit
            if t + w > hi:
                carry.append(name)
                continue
            if name == "KB":
                put("Keyboard", t, n0, counter_ft, 4, "counter")
                put("Mouse", t + 1.6, n0, counter_ft, 15, "counter")  # always on the keyboard's right (R1)
            else:
                put(name, t, n0, counter_ft, 40 if name == "Rag" else 12, "counter" + (", customer side" if k == 2 else ""))
            t += w + rng.uniform(0.1, 0.3)
    for name in carry:
        if name == "Rag":
            put(name, stand["offsetT"] + 0.05, stand["d"] - 0.05, stand["topFt"], 40, "stand top")
        elif name == "LabelPrinter":
            put(name, stand["offsetT"] + 0.5, stand["d"] - 0.1, stand["shelvesFt"][0] + stand["board"], 6, "stand shelf")
        else:
            raise ValueError(f"POS_{st['reg']}: {name} does not fit on its counter share {lo:.2f}..{hi:.2f}")
    if rng.random() < 0.55:  # ISO spray bottle hung on the stand's far side; not every stand has one (R3)
        put("ISOSpray", stand["offsetT"] + stand["w"] + 0.02, stand["d"] * 0.6, 1.3, 0, "hung on the stand")
    return out


def kit_selftest(kits):
    """Assert-based check of the DEC-104 rule: fixed items everywhere, mouse right of the keyboard, no overlaps, stations differ."""
    centre_t = lambda st, r: t_of(st, (r["x0"] + r["x1"]) / 2, (r["y0"] + r["y1"]) / 2)
    for reg, (st, items) in kits.items():
        names = [i[0] for i in items]
        for must in ("Keyboard", "Mouse", "Scanner", "ReceiptPrinter", "LabelPrinter", "CardTerminal"):
            assert names.count(must) == 1, f"POS_{reg}: {must} x{names.count(must)}"
        kb, ms = (next(i[1] for i in items if i[0] == n) for n in ("Keyboard", "Mouse"))
        assert centre_t(st, ms) > centre_t(st, kb), f"POS_{reg}: mouse not right of the keyboard"
        flat = [i for i in items if i[4].startswith("counter")]
        for a in range(len(flat)):
            for b in range(a + 1, len(flat)):
                assert not overlap(flat[a][1], flat[b][1]), f"POS_{reg}: {flat[a][0]} overlaps {flat[b][0]}"
    sigs = {tuple(sorted((i[0], i[4]) for i in items)) for _, items in kits.values()}
    assert len(sigs) >= 2, "every station has the same kit (DEC-104)"


def sales_floor(layout, src):
    rows = {(r["room"], r["fixture"]): r for r in src["fixtures"]}
    floor = [r for r in src["fixtures"] if r["room"] in FLOOR_ZONES]
    rev = next((t for t in src["version"].split() if t.startswith("rev")), src["version"])
    note = f"ROOM_FIXTURES {rev}"
    counter_ft = next(h["ft"] for h in layout["heights"] if h["key"] == "counter")
    made, skipped = [], []

    # 1. register counters (merged per run) and generic rows (ID stand + scanner, trash bins, HUB / HUB 2)
    counter_ids = {f for ids in COUNTERS.values() for f in ids}
    for cid, ids in COUNTERS.items():
        rs = [rows[("Retail", i)] for i in ids]
        made.append(fx(cid, "Retail", [rect(r) for r in rs], rs[0]["size_ft"][2], 0.0, min((r["confidence"] for r in rs), key=["Low", "Med", "High"].index),
                       True, f"{note} {' + '.join(ids)}; " + ", ".join(sorted({r["gap"] for r in rs if r.get("gap")}))))
    for r in floor:
        if r["fixture"] in counter_ids or r["type"] in ("jar_wall", "register_station", "door"):
            continue
        if r["pos_ft"] is None:
            skipped.append(f"{r['room']}_{r['fixture']} ({r.get('gap') or 'no position'})")
            continue
        made.append(fx(f"{r['room']}_{r['fixture']}", FLOOR_ZONES[r["room"]], [rect(r)], r["size_ft"][2], base_of(r, floor), r["confidence"],
                       r["type"] in SOLID, f"{note}; type {r['type']}" + (f"; {r['gap']}" if r.get("gap") else ""),
                       **({"tag": "holds: " + r["contents"]} if r.get("contents") else {})))

    # 2. three deli walls (N/E/S): back panel, back counter = jar counter row, 2 tiers; seeded uneven fill (8.4)
    runs = []
    for r in (x for x in floor if x["type"] == "jar_wall"):
        side = {"North": "N", "East": "E", "South": "S"}[r["fixture"].split("_")[-1]]
        foot, faces, depth = rect(r), r["faces"], r["size_ft"][1]
        along_x = faces in ("N", "S")
        made.append(fx(f"FX_DeliJarWall_{side}_Back", "Retail", [band(foot, faces, 0, JAR_BACK)], r["size_ft"][2], 0.0, r["confidence"], True,
                       f"{note} {r['fixture']} back panel; {r.get('gap', '')}", tag="holds: " + r.get("contents", "")))
        fill = FILL_ARCHED if "arched" in r.get("notes", "") else FILL
        for tier, h in JAR_ROWS:
            rr = band(foot, faces, JAR_BACK, depth if h is None else JAR_BACK + JAR_TIER_D)
            if tier == "Top" and "kraft" in r.get("contents", ""):
                k0, k1 = ("x0", "x1") if along_x else ("y0", "y1")
                bags = dict(rr, **{k1: round(rr[k0] + KRAFT_FT, 3)})
                rr = dict(rr, **{k0: bags[k1]})
                made.append(fx(f"FX_DeliJarWall_{side}_KraftBags", "Retail", [bags], KRAFT_H, h, "Low", False,
                               f"{note} {r['fixture']}: kraft bags fill the last 1-2 ft at one end of the top tier (REFERENCES_INDEX 8.4); which end is a layout choice"))
            runs.append({"id": f"{side}_{tier}", "alongX": along_x, "yaw": YAW[faces], "counter": h is None, "fill": fill[tier],
                         "rowsFt": [counter_ft if h is None else h], "r": rr})
    js = layout["jarSlots"]
    js.pop("rowsFt", None)
    js.update({"conf": "Low", "gap": "GAP-133", "seed": 7, "pitch": JAR_PITCH, "runs": runs,
               "note": "ART-007: three deli walls (REFERENCES_INDEX 8.3) from ROOM_FIXTURES rev7: per wall a counter run (back counter top, jars on it) "
                       "and two tier runs (4.25 / 5.5 ft, GAP-002 placeholders). Slots are numbered by a seeded weighted draw (seed; fill = 8.4 occupied "
                       "share per row), so the first N slots that gameplay stocks fill the walls unevenly: top tier dense, middle patchy, counter row sparse."})

    # 3. stations (DEC-039) from the POS_ rows; the builder's stand formula must reproduce each row's stand_rect
    st_cfg = layout["stations"]
    stand = st_cfg["stand"]
    lst = []
    for r in (x for x in floor if x["type"] == "register_station"):
        sr, side = r["stand_rect"], r["staff_side"]
        x, y = r["pos_ft"]
        x, y = {"N": (x, sr["y1"]), "S": (x, sr["y0"]), "E": (sr["x0"], y), "W": (sr["x1"], y)}[side]
        st = {"reg": r["reg"], "x": round(x, 3), "y": round(y, 3), "staff": side}
        got = local(st, stand["offsetT"], stand["offsetT"] + stand["w"], 0, stand["d"])
        assert all(abs(got[k] - sr[k]) < 0.02 for k in sr), f"POS_{r['reg']}: stand {got} != ROOM_FIXTURES stand_rect {sr}"
        lst.append(st)
    st_cfg["list"] = lst
    st_cfg["slice"] = json.load(open(ANCHORS_SRC, encoding="utf-8"))["player_station"]["reg"]
    st_cfg["gap"] = "GAP-129..131"
    st_cfg["note"] = ("DEC-039: 11 numbered stations (register 1 is the BOH desk, DEC-040); positions from ROOM_FIXTURES rev7 POS_ rows (REF-011): "
                      "(x, y) = station centre on the counter's staff edge, staff = compass side of the budtender. Operator/call anchors: SCENE_ANCHORS.json.")

    # 4. DEC-104 small items per station, seeded per register (deterministic)
    counters = {c["id"]: c for c in made if c["id"] in COUNTERS}
    on = lambda p, rr: rr["x0"] - 0.01 <= p["x"] <= rr["x1"] + 0.01 and rr["y0"] - 0.01 <= p["y"] <= rr["y1"] + 0.01
    kits = {}
    for st in lst:
        crect = next(rr for c in counters.values() for rr in c["rects"] if on(st, rr))
        mates = [t_of(st, o["x"], o["y"]) for o in lst if o is not st and o["staff"] == st["staff"] and on(o, crect)]
        ends = sorted((t_of(st, crect["x0"], crect["y0"]), t_of(st, crect["x1"], crect["y1"])))
        lo = max([ends[0] + 0.1] + [m / 2 + 0.05 for m in mates if m < 0])
        hi = min([ends[1] - 0.1] + [m / 2 - 0.05 for m in mates if m > 0])
        kits[st["reg"]] = (st, station_kit(st, lo, hi, counter_ft, stand, random.Random(f"ART-007/POS_{st['reg']}")))
    kit_selftest(kits)
    for reg, (st, items) in kits.items():
        for name, rr, base, yaw, where, cond in items:
            made.append(fx(f"POS_{reg}_{name}", "Retail", [rr], KIT_H[name], base, "Low", False,
                           f"DEC-096/104 station kit placeholder ({where}); size convention; PROC-006b's arranger replaces it", yaw=yaw, tag=f"cond {cond}"))

    keep = [f for f in layout["fixtures"] if f["zone"] == "BackRooms" or not (f["id"] in RETIRED or f["id"].startswith(GEN_PREFIX))]
    layout["fixtures"] = keep + made

    # 5. queue stanchions end >= 3 ft before the moved south counter (REF-011 note, GAP-129)
    south_y0 = min(rr["y0"] for rr in counters["FX_RegisterCounter_S"]["rects"] if rr["x1"] - rr["x0"] > rr["y1"] - rr["y0"])
    for f in layout["fixtures"]:
        if f["id"].startswith("FX_QueueLane_"):
            for rr in f["rects"]:
                rr["y1"] = round(min(rr["y1"], south_y0 - QUEUE_CLEAR_FT), 3)
            f["note"] = (f"plan lines x 6/9/12/15 (vector fill bbox, REVIEW-W1 m3); south end cut to y {south_y0 - QUEUE_CLEAR_FT:.1f}, "
                         f"{QUEUE_CLEAR_FT} ft clear of the moved south counter (ART-007, GAP-129)")

    # 6. vestibule shell (A011, GAP-122) and the openings DOORS.json targets
    shell = rect(rows[("Vestibule", "Vestibule_Shell_A011")])
    walls = {w["id"]: w for w in layout["walls"]}
    t = walls["W_Vest_S"]["t"]
    walls["W_Vest_W"].update(ax=shell["x0"], bx=shell["x0"], ay=shell["y0"], by=shell["y1"], conf="High", gap="GAP-122")
    walls["W_Vest_E"].update(ax=shell["x1"], bx=shell["x1"], ay=shell["y0"], by=shell["y1"], conf="High", gap="GAP-122")
    walls["W_Vest_S"].update(ax=round(shell["x0"] - t / 2, 3), bx=round(shell["x1"] + t / 2, 3), ay=shell["y1"], by=shell["y1"], conf="High", gap="GAP-122")
    walls["W_FOH_BOH"]["ay"] = round(shell["y1"] + t / 2, 3)
    next(r for r in layout["rooms"] if r["id"] == "Vestibule").update(r=shell, conf="High")
    doors = json.load(open(DOORS_SRC, encoding="utf-8"))["doors"]
    for d in doors:
        tgt, w = d.get("target_opening"), walls.get(d.get("graybox_wall"))
        if not tgt or not w:
            continue
        span = tgt["x"] if isinstance(tgt.get("x"), list) else tgt["y"]
        op = min(w["openings"], key=lambda o: abs(o["from"] - d["graybox_opening"][0]) + abs(o["to"] - d["graybox_opening"][1]))
        op.update({"from": span[0], "to": span[1], "conf": "High", "note": f"DOORS.json {d['id']} target_opening ({tgt['source']})"})

    # 7. door leaves (leaves 1/2 with a position) and every placed door's A/B anchors
    zone_of = {w["id"]: w["zone"] for w in layout["walls"]}
    out_doors, anchors = [], []
    for d in doors:
        if d["pos_ft"] is None:
            skipped.append(f"door {d['id']} ({', '.join(d.get('gap') or []) or 'no position'})")
            continue
        zone = zone_of[d["graybox_wall"]]
        if d.get("anchors"):
            a, b = d["anchors"]["A"], d["anchors"]["B"]
            for p, q in ((a, b), (b, a)):
                yaw = round(math.degrees(math.atan2(q["pos_ft"][0] - p["pos_ft"][0], -(q["pos_ft"][1] - p["pos_ft"][1]))) % 360, 1)
                anchors.append({"id": p["name"], "zone": zone, "x": p["pos_ft"][0], "y": p["pos_ft"][1], "h": 0, "yaw": yaw,
                                "conf": "Low" if d.get("gap") else "Med", "note": f"DOORS.json {d['id']} side {p['room']}, facing the opening"})
        if d["leaves"] not in (1, 2):
            continue
        leaves = d.get("leafObjects") or [{"object": d["object"], "pivot": d["pivot"], "hinge_ft": d["hinge_ft"], "leafWidth_ft": d["leafWidth_ft"],
                                           "closedRotation": d["closedRotation"], "openAngle": d["openAngle"]}]
        out_doors.append({"id": d["object"], "zone": zone, "pair": d["leaves"] == 2, "open": d["defaultState"] == "proppedOpen",
                          "h": d["leafHeight_ft"], "t": DOOR_T, "conf": "Low" if "Low" in json.dumps(d.get("confidence", {})) else "Med",
                          "gap": ",".join(d.get("gap") or []), "note": f"DOORS.json {d['id']} ({d['type']}, {d['swing']}, default {d['defaultState']})",
                          "leaves": [{"name": l["object"], "pivot": l["pivot"], "x": l["hinge_ft"][0], "y": l["hinge_ft"][1], "w": l["leafWidth_ft"],
                                      "yaw": l["closedRotation"][1], "openAngle": l["openAngle"]} for l in leaves]})
    layout["doors"] = out_doors

    # 8. SCENE_ANCHORS (+ aliases at the same pose); the old Retail anchors are all superseded by it
    for a in json.load(open(ANCHORS_SRC, encoding="utf-8"))["anchors"]:
        for name in [a["name"]] + (a.get("aliases") or []):
            anchors.append({"id": name, "zone": "Retail", "x": a["pos_ft"][0], "y": a["pos_ft"][1], "h": 0, "yaw": a["yaw_deg"], "conf": a["confidence"],
                            "note": f"SCENE_ANCHORS {a['name']}" + (" (alias)" if name != a["name"] else "") + (f"; {a['gap']}" if a.get("gap") else "")})
    names = [a["id"] for a in anchors]
    assert len(names) == len(set(names)), "duplicate anchor names"
    layout["anchors"] = [a for a in layout["anchors"] if a["zone"] != "Retail" and not a["id"].startswith("Anchor_Door_")] + anchors

    # 9. register-back CCTV poses (REF-011)
    jw_s = next(c for c in made if c["id"] == "FX_DeliJarWall_S_Back")["rects"][0]
    for c in layout["cameras"]:
        if c["tile"] in CAMERA_POSES:
            x, yaw, pitch, why = CAMERA_POSES[c["tile"]]
            c.update(x=x, y=round((jw_s["y0"] + jw_s["y1"]) / 2, 3), yaw=yaw, pitch=pitch, conf="Low", note=f"{why}; pose read from the tile, Low")
    return (f"sales floor: {len(made)} fixtures, {len(lst)} stations, {len(runs)} jar runs, {len(out_doors)} doors, {len(anchors)} anchors; "
            f"skipped: {', '.join(skipped) or 'none'}")


def clearance(report_path=None):
    """ART-007 check of the built layout (python room_fixtures_layout.py --check): REF-011 operator zones and aisles,
    REF-012 office path and door swings, reachability of every anchor for a person, queue vs counter. Exit 1 on a failure."""
    import collections
    import numpy as np
    layout = json.load(open(LAYOUT, encoding="utf-8"))
    src = json.load(open(SRC, encoding="utf-8"))
    G, X0, Y0, X1, Y1 = 0.1, -40.0, -8.0, 52.0, 82.0  # REF-013: the spawn is in the west parking row (x -32.7)
    shape = (int(round((Y1 - Y0) / G)), int(round((X1 - X0) / G)))
    lines, fails = [], []

    def log(ok, msg):
        lines.append(f"{'PASS' if ok else 'FAIL'}  {msg}")
        if not ok:
            fails.append(msg)

    def leaf_rect(x, y, w, t, unity_yaw):
        a = math.radians(unity_yaw)  # Unity yaw a turns local +X to plan (cos a, sin a), +y = south
        ex, ey = x + w * math.cos(a), y + w * math.sin(a)
        h = t / 2
        return {"x0": min(x, ex) - h, "x1": max(x, ex) + h, "y0": min(y, ey) - h, "y1": max(y, ey) + h}

    # obstacles a person walks into: solid fixtures starting below 4 ft, stands, back counters, walls minus openings, open leaves
    solids = [(f["id"], r) for f in layout["fixtures"] if f["solid"] and f.get("baseFt", 0) < 4.0 and not f.get("h") in ("pendant",) for r in f["rects"]]
    st_cfg, stand = layout["stations"], layout["stations"]["stand"]
    for st in st_cfg["list"]:
        solids.append((f"FX_ScaleStand_POS_{st['reg']}", local(st, stand["offsetT"], stand["offsetT"] + stand["w"], 0, stand["d"])))
    solids += [(f"FX_DeliBackCounter_{run['id']}", run["r"]) for run in layout["jarSlots"]["runs"] if run.get("counter")]
    walls = []
    for w in layout["walls"]:
        along_x = w["ay"] == w["by"]
        s0, s1 = sorted((w["ax"], w["bx"]) if along_x else (w["ay"], w["by"]))
        c, ht, cur = (w["ay"] if along_x else w["ax"]), w["t"] / 2, s0
        for o in sorted(w["openings"], key=lambda o: o["from"]) + [{"from": s1, "to": s1}]:
            if o["from"] > cur:
                walls.append((w["id"], {"x0": cur, "x1": o["from"], "y0": c - ht, "y1": c + ht} if along_x else {"x0": c - ht, "x1": c + ht, "y0": cur, "y1": o["from"]}))
            cur = o["to"]
    leaves = []
    for d in layout.get("doors", []):
        for l in d["leaves"]:
            leaves.append((d, l))
            if d["open"]:
                solids.append((l["name"] + " (propped open)", leaf_rect(l["x"], l["y"], l["w"], d["t"], l["yaw"] + l["openAngle"])))

    # cell centres; an obstacle blocks every centre closer than `radius` to it (Euclidean, disc-shaped person)
    ys, xs = Y0 + (np.arange(shape[0]) + 0.5) * G, X0 + (np.arange(shape[1]) + 0.5) * G

    def blocked_for(radius):
        g = np.zeros(shape, bool)
        for _, r in solids + walls:
            dy = np.maximum(np.maximum(r["y0"] - ys, ys - r["y1"]), 0)[:, None]
            dx = np.maximum(np.maximum(r["x0"] - xs, xs - r["x1"]), 0)[None, :]
            i0, i1 = np.searchsorted(ys, r["y0"] - radius), np.searchsorted(ys, r["y1"] + radius)
            j0, j1 = np.searchsorted(xs, r["x0"] - radius), np.searchsorted(xs, r["x1"] + radius)
            g[i0:i1, j0:j1] |= (dy[i0:i1] ** 2 + dx[:, j0:j1] ** 2) < radius ** 2
        return g

    def cell(x, y):
        return int((y - Y0) / G + 1e-6), int((x - X0) / G + 1e-6)  # +eps: a point on a cell edge lands in one cell whatever the grid origin

    def reach(start, radius):
        blocked = blocked_for(radius)
        seen = np.zeros(shape, bool)
        i, j = cell(*start)
        seed = [(a, b) for a in range(i - 5, i + 6) for b in range(j - 5, j + 6) if not blocked[a, b]]  # snap within 0.5 ft
        q = collections.deque(seed)
        for a, b in seed:
            seen[a, b] = True
        while q:
            a, b = q.popleft()
            for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                na, nb = a + da, b + db
                if 0 <= na < shape[0] and 0 <= nb < shape[1] and not seen[na, nb] and not blocked[na, nb]:
                    seen[na, nb] = True
                    q.append((na, nb))

        def hit(x, y, snap=0.5):  # an anchor is reached when a free cell within `snap` ft of it is
            (a, b), k = cell(x, y), int(round(snap / G))
            return bool(seen[max(a - k, 0):a + k + 1, max(b - k, 0):b + k + 1].any())
        return hit

    anchors = {a["id"]: (a["x"], a["y"]) for a in layout["anchors"]}
    rows = {r["fixture"]: r for r in src["fixtures"] if r["room"] == "Retail"}

    # 1. REF-011 station operator zones + aisle behind each stand (row clearance_ft)
    for st in st_cfg["list"]:
        r = rows[f"POS_{st['reg']}"]
        own = {f"FX_ScaleStand_POS_{st['reg']}", f"Retail_Trash_Small_POS_{st['reg']}"}
        hits = [n for n, rr in solids if n not in own and overlap(rr, r["operator_zone"])]
        log(not hits, f"POS_{st['reg']} operator zone {r['operator_zone']} free" + (f": {hits}" if hits else ""))
        sr, (nx, ny) = r["stand_rect"], staff_dir(st["staff"])
        best = None
        for n, rr in solids + walls:
            if n in own or n.startswith("Retail_Trash_Small_"):
                continue
            if nx == 0 and rr["x0"] < sr["x1"] and rr["x1"] > sr["x0"]:
                gap = rr["y0"] - sr["y1"] if ny > 0 else sr["y0"] - rr["y1"]
            elif ny == 0 and rr["y0"] < sr["y1"] and rr["y1"] > sr["y0"]:
                gap = rr["x0"] - sr["x1"] if nx > 0 else sr["x0"] - rr["x1"]
            else:
                continue
            if gap > -0.01 and (best is None or gap < best[0]):
                best = (round(gap, 2), n)
        need = r["clearance_ft"]["behind_stand"]
        log(best is not None and best[0] >= need - 0.05, f"POS_{st['reg']} clear behind the stand {best} >= {need} ft (REF-011 row)")

    # 2. reachability for a person 1.5 ft wide (shoulders) (customers from the spawn, staff from the west arch); closed doors count as openable
    cust = reach(anchors["Anchor_CustomerSpawn"], 0.75)
    for n, (x, y) in sorted(anchors.items()):
        if n.startswith(("Anchor_Queue", "Anchor_CheckIn_Wait", "Anchor_CustomerExit", "Anchor_Door_Entry")) or (n.startswith("Anchor_Register_") and n.endswith("_Call")):
            log(cust(x, y), f"customer reaches {n} ({x}, {y})")
    staff = reach(anchors["Anchor_Door_Arch_W_A"], 0.75)
    for n, (x, y) in sorted(anchors.items()):
        if n.startswith(("Anchor_Door_", "Anchor_POS_", "Anchor_Guard", "Anchor_FOH_Desk", "Anchor_BOH_Desk")) or n.endswith("_Operator"):
            seat = next(((s, r) for s, r in solids if r["x0"] < x < r["x1"] and r["y0"] < y < r["y1"]), None)
            # door anchors are trigger points (within 1 ft); a seat anchor is reached when a person can stand against the chair
            # (half its larger side + 0.75 ft + a cell; ART-008: a flat 1.5 ft can't reach the centre of a 2 ft chair from any side)
            snap = max(1.5, max(seat[1]["x1"] - seat[1]["x0"], seat[1]["y1"] - seat[1]["y0"]) / 2 + 0.75 + G) if seat else 1.0 if n.startswith("Anchor_Door_") else 0.5
            seat = seat and seat[0]
            log(staff(x, y, snap), f"staff reaches {n} ({x}, {y})" + (f" (seat on {seat}, within {snap:.2f} ft)" if seat else ""))

    # 3. REF-012 office main path >= 3.0 ft: hall door -> HUB 2 door
    office = reach(anchors["Anchor_Door_Hall_Office_B"], 1.5 - G / 2)  # half a cell: the 0.1 ft grid cannot resolve an exact 3.0 ft gap
    log(office(*anchors["Anchor_Door_Office_HUB2_A"]), "office main path >= 3.0 ft from the hall door to the HUB 2 door (REF-012)")

    # 4. door swings: the leaf sweeps from closed to open without hitting a fixture (walls excluded)
    fx_only = [(n, r) for n, r in solids if not n.endswith("(propped open)")]
    props = {f"{r['room']}_{r['fixture']}": "Door_" + r["propsDoor"] for r in src["fixtures"] if r.get("propsDoor")}  # the prop stands in the sweep on purpose
    for d, l in leaves:
        hits = set()
        for k in range(0, 19):
            a = math.radians(l["yaw"] + l["openAngle"] * k / 18)
            for s in np.arange(0.3, l["w"] + 0.01, 0.2):
                px, py = l["x"] + s * math.cos(a), l["y"] + s * math.sin(a)
                hits |= {n for n, r in fx_only if r["x0"] < px < r["x1"] and r["y0"] < py < r["y1"] and not (d["open"] and props.get(n) == d["id"])}
        log(not hits, f"{l['name']} swing clear" + (f": {sorted(hits)}" if hits else ""))

    # 5. queue stanchions clear the south counter by >= 3 ft; no register call spot inside the stanchion field
    lanes = [r for f in layout["fixtures"] if f["id"].startswith("FX_QueueLane_") for r in f["rects"]]
    field_x = (min(r["x0"] for r in lanes), max(r["x1"] for r in lanes))
    south = [r for r in next(f for f in layout["fixtures"] if f["id"] == "FX_RegisterCounter_S")["rects"] if r["x0"] < field_x[1] + QUEUE_CLEAR_FT]
    gap = min(r["y0"] for r in south) - max(r["y1"] for r in lanes)
    log(gap >= QUEUE_CLEAR_FT - 0.01, f"queue stanchions end {gap:.2f} ft from the south counter (>= {QUEUE_CLEAR_FT})")
    field = {"x0": min(r["x0"] for r in lanes), "x1": max(r["x1"] for r in lanes), "y0": min(r["y0"] for r in lanes), "y1": max(r["y1"] for r in lanes)}
    inside = [n for n, (x, y) in anchors.items() if n.endswith("_Call") and field["x0"] <= x <= field["x1"] and field["y0"] <= y <= field["y1"]]
    log(not inside, f"no register call spot inside the stanchion field {field}" + (f": {inside}" if inside else ""))

    out = "\n".join(lines + [f"clearance: {len(lines) - len(fails)}/{len(lines)} PASS" + (f", {len(fails)} FAIL" if fails else "")])
    print(out)
    if report_path:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        open(report_path, "w", encoding="utf-8").write(out + "\n")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(clearance(os.path.join(ROOT, "Artifacts", "Screenshots", "ART-007_clearance.txt")))
    sys.exit(main())
