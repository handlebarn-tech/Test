"""PROC-006b arranger self-test (DEC-104). Pure Python, no Blender:
  python Tools/Blender/tests/test_register_arranger.py
Same seed -> same JSON (and equal to the committed station files); fixed items at every station; mouse always right
of the keyboard; at least 2 stations differ in optional items."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generators"))
import register_arranger as ra  # noqa: E402

FIXED = {"PROC_RK_" + i for i in ("Keyboard", "Mouse", "Scanner", "ReceiptPrinter", "LabelPrinter")}

a, b = ra.run(write=False), ra.run(write=False)
assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), "arranger is not deterministic"
assert len(a) == 11, f"expected 11 register stations (DEC-039), got {len(a)}"

out_dir = os.path.join(ra.ROOT, json.load(open(ra.PARAMS, encoding="utf-8"))["arranger"]["out_dir"])
kb_w = next(i["size_m"][0] for i in json.load(open(ra.PARAMS, encoding="utf-8"))["items"] if i["id"] == "Keyboard")
optional_sets = set()
for name, st in a.items():
    with open(os.path.join(out_dir, f"{name}.json"), encoding="utf-8") as f:
        assert json.load(f) == json.loads(json.dumps(st)), f"{name}: committed JSON is stale, rerun the arranger"
    assets = [i["asset"] for i in st["items"]]
    for fx in FIXED:
        assert assets.count(fx) == 1, f"{name}: fixed item {fx} x{assets.count(fx)}"
    pos = {i["asset"]: i["pos_m"] for i in st["items"] if i["asset"] in FIXED}
    assert all(i["anchor"] == "TOP" for i in st["items"] if i["asset"] in FIXED), f"{name}: fixed item off the counter top"
    assert pos["PROC_RK_Mouse"][0] - pos["PROC_RK_Keyboard"][0] > kb_w / 2, f"{name}: mouse not right of the keyboard"
    optional_sets.add(tuple(sorted(x for x in assets if x not in FIXED)))
assert len(optional_sets) >= 2, "all stations carry the same optional items"
print(f"[RK] arranger self-test passed: {len(a)} stations, {len(optional_sets)} distinct optional sets")
