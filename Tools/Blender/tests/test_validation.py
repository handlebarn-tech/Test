"""PROC-005 C3/C5/Q0.5 self-test on planted bad meshes. Run headless:
  blender -b --factory-startup --python-exit-code 10 -P Tools/Blender/tests/test_validation.py
Writes only to a temp dir."""
import json
import os
import sys
import tempfile

import bmesh

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import run_generator as rg  # noqa: E402
from proclib import Parts, add_box  # noqa: E402

tmp = tempfile.mkdtemp(prefix="proc_selftest_")
rg.EXPORT_DIR, rg.RENDER_DIR = tmp, tmp
rg.MANIFEST, rg.VALIDATION_DIR = os.path.join(tmp, "manifest.json"), os.path.join(tmp, "Validation")
rg.render_previews = lambda *a, **k: None


def gen(kind):
    def build(p, lod):
        parts = Parts()
        bm = parts("Body", "Test", (1, 1, 1, 1))
        if kind == "open_quad":  # non-manifold is diagnostic only (DEC-086): must pass
            add_box(bm, (0.1, 0.1, 0.1), (0, 0, 0.05))
            vs = [bm.verts.new(v) for v in ((0, -0.05, 0.1), (0, 0.05, 0.1), (0, 0.05, 0.12), (0, -0.05, 0.12))]  # fin
            bm.faces.new(vs)
        elif kind == "zero_area":
            add_box(bm, (0.1, 0.1, 0.1), (0, 0, 0.05))
            bm.faces.new([bm.verts.new((0, 0, 0.2)), bm.verts.new((0.01, 0, 0.2)), bm.verts.new((0.02, 0, 0.2))])
        elif kind == "off_origin":
            add_box(bm, (0.1, 0.1, 0.1), (0.2, 0, 0.1))
        elif kind == "lod_up":
            add_box(bm, (0.1, 0.1, 0.1), (0, 0, 0.05))
            if lod["n"]:
                bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2)
        else:
            add_box(bm, (0.1, 0.1, 0.1), (0, 0, 0.05))
        objs = parts.finish()
        if kind == "no_material":
            objs["Body"].data.materials.clear()
        size = (0.1, {"open_quad": 0.12, "zero_area": 0.2}.get(kind, 0.1), 0.1)  # Unity x, y, z
        return objs, size, {"collision_boxes": []}
    return type("G", (), {"build": staticmethod(build)})


def run(kind, expect_error):
    p = {"seed": 1, "gaps": [], "tri_budget": {"LOD0": 1000, "LOD1": 1000},
         "lods": {"LOD0": {"n": 0}, "LOD1": {"n": 1}} if kind == "lod_up" else {"LOD0": {"n": 0}},
         "checks": {"origin_bottom_centre": True, "fail_on_degenerate": True, "material_slots": True}}
    if kind == "open_quad":
        p["tri_budget"] = {"LOD0": 1000}
    try:
        rg.generate_asset("selftest", gen(kind), p, "T_" + kind, b"{}", os.path.join(rg.ROOT, "x.json"))
        err = None
    except RuntimeError as e:
        err = str(e)
    doc = json.load(open(os.path.join(rg.VALIDATION_DIR, f"T_{kind}.json")))
    assert doc["passed"] == (err is None), (kind, doc)
    if expect_error:
        assert err and expect_error in err, (kind, err)
        assert any(expect_error in e for e in doc["errors"]), (kind, doc)  # C3: errors land in the JSON
    else:
        assert err is None, (kind, err)
        assert "collision_boxes" not in json.load(open(rg.MANIFEST))["assets"]["T_" + kind]  # C2
    print(f"[SELFTEST] {kind}: ok ({err.splitlines()[1].strip() if err else 'pass'})")


run("open_quad", None)
run("zero_area", "degenerate")
run("off_origin", "origin not bottom centre")
run("no_material", "material slots")
run("lod_up", "does not decrease")
print("[SELFTEST] all passed")
