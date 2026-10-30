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
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "Docs", "Reference", "ROOM_FIXTURES.json")
LAYOUT = os.path.join(ROOT, "UnityProject", "Assets", "_Game", "Art", "Graybox", "graybox_layout.json")
ROOMS = ("Office", "BreakRoom", "FOH", "BOH")
LEGACY = {"FX_Office_ITRack", "FX_Office_Safe", "FX_Office_Desk_L", "FX_Break_Kitchen_L", "FX_Break_Bench", "FX_JC_Closet",
          "FX_FOH_WireRack_1", "FX_FOH_WireRack_2", "FX_FOH_Fridge", "FX_BOH_Racks_W", "FX_BOH_Racks_E", "FX_FOH_Desk",
          "FX_FOH_Computer", "FX_FOH_Chair", "FX_FOH_ChairBack", "FX_BOH_Desk", "FX_BOH_Computer", "FX_BOH_Chair", "FX_BOH_ChairBack"}
SUPPORTS = {"desk", "table", "counter", "rack"}
NOT_STACKED = {"cabinet", "chair", "signage", "shelf", "lighting", "wall", "room_volume", "floor_mat", "locker", "fridge",
               "cooler", "bin", "door", "desk", "table", "counter", "bench"}
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
}
SHELF_LEVELS = {"Shelves_Floating_x3": [5.0, 5.7, 6.3]}  # "staggered at ~5.0 / 5.7 / 6.3 ft AFF"
SKIP_INSIDE = {"MopSink_JC"}  # inside the closed JC volume (graybox closet is not enterable)
SOLID = {"desk", "table", "counter", "cabinet", "rack", "fridge", "cooler", "locker", "wall", "room_volume", "bench",
         "cart", "bin", "chair", "prop", "sink"}
# Openings the REF door rows move (GAP-123): wall id, opening id, A011 span along the wall.
DOOR_OPENINGS = {"Door_Hall_Office": ("W_Band_Office", "DOOR_Hall_Office", 10.2, 13.3),
                 "Door_Office_HUB2": ("W_Back_Hub", "DOOR_Office_HUB", 7.2, 10.2)}
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
    rows = [r for r in src["fixtures"] if r["room"] in ROOMS]
    with open(LAYOUT, encoding="utf-8") as f:
        text = f.read()
    layout = json.loads(text)
    rev = next((t for t in src["version"].split() if t.startswith("rev")), src["version"])
    note = f"ROOM_FIXTURES {rev}"
    skipped, made = [], []
    for r in rows:
        if r["type"] == "door" and r["fixture"] in DOOR_OPENINGS:
            continue
        if r["pos_ft"] is None or r["fixture"] in SKIP_INSIDE:
            skipped.append(f"{r['room']}_{r['fixture']} ({r.get('gap') or 'no position' if r['pos_ft'] is None else 'inside JC'})")
            continue
        levels = SHELF_LEVELS.get(r["fixture"], [None])
        for k, lvl in enumerate(levels):
            fid = f"{r['room']}_{r['fixture']}" + (f"_{k}" if len(levels) > 1 else "")
            made.append({"id": fid, "zone": "BackRooms", "h": "", "hFt": r["size_ft"][2],
                         "baseFt": round(lvl if lvl is not None else base_of(r, rows), 3),
                         "conf": r["confidence"], "solid": r["type"] in SOLID, "rects": [rect(r)],
                         "note": f"{note}; type {r['type']}" + (f"; {r['gap']}" if r.get("gap") else "")})
    fixtures = [f for f in layout["fixtures"] if not (f["zone"] == "BackRooms" and (f["id"] in LEGACY or f["id"].split("_")[0] in ROOMS))]
    layout["fixtures"] = fixtures + made
    for r in rows:  # door openings (GAP-123)
        if r["fixture"] in DOOR_OPENINGS:
            wid, oid, a, b = DOOR_OPENINGS[r["fixture"]]
            wall = next(w for w in layout["walls"] if w["id"] == wid)
            op = next(o for o in wall["openings"] if o["id"] == oid)
            op.update({"from": a, "to": b, "conf": r["confidence"], "note": f"A011 via ROOM_FIXTURES {r['fixture']} (GAP-123)"})
    for aid, (room, chair, desk) in ANCHORS.items():
        c = next(r for r in rows if r["room"] == room and r["fixture"] == chair)
        dsk = next(r for r in rows if r["room"] == room and r["fixture"] == desk)
        a = next(a for a in layout["anchors"] if a["id"] == aid)
        dx, dy = dsk["pos_ft"][0] - c["pos_ft"][0], dsk["pos_ft"][1] - c["pos_ft"][1]
        yaw = 90 if abs(dx) >= abs(dy) and dx > 0 else 270 if abs(dx) >= abs(dy) else 180 if dy > 0 else 0
        a.update({"x": c["pos_ft"][0], "y": c["pos_ft"][1], "yaw": yaw, "note": f"DEC-040 chair spot facing {desk} (ROOM_FIXTURES)"})
    out = dump(layout)
    with open(LAYOUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"room fixtures: {len(made)} written, {len(LEGACY)} legacy removed, skipped: {', '.join(skipped) or 'none'}")


if __name__ == "__main__":
    sys.exit(main())
