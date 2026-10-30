"""Headless entry point (PROC-001). Run via Tools/Blender/blender.ps1, or directly:
  blender -b --factory-startup --python-exit-code 10 -P Tools/Blender/run_generator.py -- <generator> <params.json>
  blender -b --factory-startup --python-exit-code 10 -P Tools/Blender/run_generator.py -- contact_sheet
Builds every LOD, validates, exports one FBX per asset, updates the manifest, renders previews.
Any failure raises, so Blender exits with code 10."""
import datetime
import hashlib
import importlib
import json
import math
import os
import shutil
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
EXPORT_DIR = os.path.join(ROOT, "Art", "Exports", "Procedural")
MANIFEST = os.path.join(EXPORT_DIR, "manifest.json")
VALIDATION_DIR = os.path.join(EXPORT_DIR, "Validation")
RENDER_DIR = os.path.join(ROOT, "Artifacts", "Renders")
SHEET = os.path.join(ROOT, "Docs", "Assets", "Specs", "PROC_contact_sheet.png")
sys.path.insert(0, HERE)

from proclib import UV_LABEL, UV_MAIN, mesh_stats  # noqa: E402


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.unit_settings.system, s.unit_settings.scale_length = "METRIC", 1.0


def generate(gen_name, params_path):
    with open(params_path, "rb") as f:
        raw = f.read()
    p = json.loads(raw)
    if p["generator"] != gen_name:
        raise ValueError(f"{params_path} is for generator {p['generator']!r}, not {gen_name!r}")
    gen = importlib.import_module("generators." + gen_name)
    for asset, vp in getattr(gen, "variants", lambda q: [(q["asset_id"], q)])(p):  # variants: one params file, many assets
        generate_asset(gen_name, gen, vp, asset, raw, params_path)


def generate_asset(gen_name, gen, p, asset, raw, params_path):
    reset()
    entry, errors, warnings = {"lods": {}}, [], []
    params_sha = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()[:16]  # stable across autocrlf
    checks = p.get("checks", {})
    for lod_name, lod in p["lods"].items():
        objs, expected, extra = gen.build(p, lod)
        lod_entry = {"objects": {}}
        for part, obj in objs.items():
            obj.name = obj.data.name = f"{asset}_{part}_{lod_name}"  # _LODn suffix = Unity LODGroup auto-setup
            st = mesh_stats(obj)
            if obj.matrix_world != obj.matrix_world.Identity(4):
                errors.append(f"{obj.name}: unapplied transform")
            if st["uv_maps"] != [UV_MAIN, UV_LABEL]:
                errors.append(f"{obj.name}: UV maps {st['uv_maps']}")
            if checks.get("fail_on_degenerate") and st["geometry"]["degenerate_faces"]:
                errors.append(f"{obj.name}: {st['geometry']['degenerate_faces']} degenerate faces")
            if checks.get("material_slots") and (not st["material_slots"] or None in st["material_slots"]):
                errors.append(f"{obj.name}: material slots {st['material_slots']}")
            lod_entry["objects"][obj.name] = st
        lod_entry["tris"] = sum(o["tris"] for o in lod_entry["objects"].values())
        budget = p["tri_budget"][lod_name]
        if lod_entry["tris"] > budget:
            errors.append(f"{lod_name}: {lod_entry['tris']} tris > budget {budget}")
        entry["lods"][lod_name] = lod_entry
        entry.update(extra)
        if not objs:
            errors.append(f"{lod_name}: no objects")
            continue
        pts = [c for o in objs.values() for c in bbox_unity(o)]
        lo, hi = [min(a) for a in zip(*pts)], [max(a) for a in zip(*pts)]
        size = [b - a for a, b in zip(lo, hi)]
        if any(abs(a - b) > 1e-4 for a, b in zip(size, expected)):
            errors.append(f"{lod_name}: size {size} != expected {expected}")
        # C5 (opt-in): origin at the bottom centre (min z = 0, x/y bbox centred)
        if checks.get("origin_bottom_centre") and (abs(lo[1]) > 1e-4 or abs(lo[0] + hi[0]) > 2e-4 or abs(lo[2] + hi[2]) > 2e-4):
            errors.append(f"{lod_name}: origin not bottom centre (min {lo}, max {hi})")
        lod_entry["size_m_unity_xyz"] = [round(v, 5) for v in size]
    check_lod_chain(p, entry["lods"], errors, warnings)
    if "collision_boxes" in entry and not entry["collision_boxes"]:
        del entry["collision_boxes"]  # C2: key only when non-empty
    if errors:
        write_validation(asset, gen_name, params_sha, entry, errors, warnings)  # C3: a failure leaves evidence too
        raise RuntimeError("validation failed:\n  " + "\n  ".join(errors))

    os.makedirs(EXPORT_DIR, exist_ok=True)
    fbx = os.path.join(EXPORT_DIR, asset + ".fbx")
    export_fbx(fbx)
    with open(fbx, "rb") as f:
        fbx_sha = hashlib.sha256(f.read()).hexdigest()[:16]
    if p.get("unity_dir"):
        unity_fbx = os.path.join(ROOT, p["unity_dir"], asset + ".fbx")
        os.makedirs(os.path.dirname(unity_fbx), exist_ok=True)
        shutil.copyfile(fbx, unity_fbx)
        entry["unity_copy"] = os.path.relpath(unity_fbx, ROOT).replace("\\", "/")
    if p.get("own_sheet"):
        entry["own_sheet"] = True
    entry.update({
        "generator": gen_name,
        "params": os.path.relpath(params_path, ROOT).replace("\\", "/"),
        "params_sha256": params_sha,
        "export": os.path.relpath(fbx, ROOT).replace("\\", "/"),
        "export_sha256": fbx_sha,
        "tri_budget": p["tri_budget"],
        "gaps": sorted(p["gaps"]),
    })
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {
        "units": "meters", "up": "+Y (Unity)", "label_faces": "+Z (Unity forward)", "assets": {}}
    manifest["assets"][asset] = entry
    with open(MANIFEST, "w", newline="\n") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    write_validation(asset, gen_name, params_sha, entry, [], warnings)
    if hasattr(gen, "preview_context"):
        gen.preview_context(p)  # non-exported scenery for the renders (export and manifest are already written)
    render_previews(asset, list(p["lods"]), entry.get("preview_groups"))
    print(f"[PROC] {asset}: " + ", ".join(f"{k}={v['tris']} tris" for k, v in entry["lods"].items()) + f" -> {fbx}")


def check_lod_chain(p, lods, errors, warnings):
    """Q0.5 (DEC-084): fail above tri_budget (the guide max), warn below tri_guide.lod0_min, and require each LOD
    to have fewer tris than the one before."""
    tris = [lods[k]["tris"] for k in p["lods"] if k in lods]
    lo = p.get("tri_guide", {}).get("lod0_min")
    if lo and tris and tris[0] < lo:
        warnings.append(f"LOD0 {tris[0]} tris below the DEC-084 guide minimum {lo} (too simple?)")
    for name, a, b in zip(list(p["lods"])[1:], tris, tris[1:]):
        if b >= a:
            errors.append(f"{name}: {b} tris does not decrease from the previous LOD ({a})")
    if lo and len(tris) == 4:
        for name, t, r in zip(("LOD1", "LOD2", "LOD3"), tris[1:], (0.75, 0.4, 0.15)):
            if t > tris[0] * r:
                warnings.append(f"{name}: {t} tris > {r:.0%} of LOD0 (guide 1/2, 1/4, <= 1/10)")


def write_validation(asset, gen_name, params_sha, entry, errors, warnings):
    os.makedirs(VALIDATION_DIR, exist_ok=True)
    doc = {"asset_id": asset, "generator": gen_name, "params_sha256": params_sha, "passed": not errors,
           "errors": errors, "warnings": warnings, "export_sha256": entry.get("export_sha256"),
           "lod_tris": {k: v["tris"] for k, v in entry["lods"].items()},
           "collision_boxes": len(entry.get("collision_boxes", []))}
    with open(os.path.join(VALIDATION_DIR, asset + ".json"), "w", newline="\n") as f:
        json.dump(doc, f, indent=2, sort_keys=True)
        f.write("\n")


def bbox_unity(obj):
    for v in obj.data.vertices:
        yield (v.co.x, v.co.z, v.co.y)


def export_fbx(path):
    import io_scene_fbx.export_fbx_bin as fbx_bin
    import io_scene_fbx.fbx_utils as fbx_utils
    # shortcut: the stock exporter stamps now() and derives node UUIDs from salted str hash(); pin both
    # so reruns are byte-identical. Drop if the exporter gains a deterministic mode.
    fixed = datetime.datetime(2026, 1, 1)
    fbx_bin.datetime = type("dt", (), {"datetime": type("DT", (), {"now": staticmethod(lambda: fixed)})})
    fbx_utils.hash = lambda k: int.from_bytes(hashlib.sha256(repr(k).encode()).digest()[:8], "little")
    bpy.ops.export_scene.fbx(
        filepath=path, use_selection=False, object_types={"MESH"}, apply_scale_options="FBX_SCALE_ALL",
        axis_forward="-Z", axis_up="Y", bake_space_transform=True, mesh_smooth_type="FACE",
        add_leaf_bones=False, bake_anim=False, path_mode="STRIP", use_custom_props=False)


def render_previews(asset, lods, groups=None):
    """Front + side of LOD0 and front of the last LOD, Workbench, ortho, with a 10 cm scale cube.
    With groups (part names sharing one origin, e.g. fill steps): LOD0 front per group, then the other LODs of the last
    group. Objects named Context_* always render."""
    s = bpy.context.scene
    s.render.engine = "BLENDER_WORKBENCH"
    s.display.shading.light, s.display.shading.color_type = "STUDIO", "MATERIAL"
    s.display.shading.show_cavity = True
    s.render.resolution_x = s.render.resolution_y = 320
    s.render.film_transparent = False
    s.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new("W")
    world.color = (0.55, 0.55, 0.55)
    s.world = world
    objs = [o for o in s.objects if o.type == "MESH"]
    xs, ys, zs = zip(*(v.co for o in objs for v in o.data.vertices))
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(max(xs) + 0.08, max(ys) + 0.08, 0.05))
    x0, x1, y0, y1, h = min(xs), max(xs) + 0.13, min(ys), max(ys) + 0.13, max(zs)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    s.collection.objects.link(cam)
    s.camera, cam.data.type = cam, "ORTHO"
    cam.data.ortho_scale = max(h, x1 - x0, y1 - y0) * 1.15
    front = ((x0 + x1) / 2, y0 - 2, h / 2), (math.pi / 2, 0, 0)  # outside the bounds: a fixed -2 m put it inside a 4.9 m car
    side = (x1 + 2, (y0 + y1) / 2, h / 2), (math.pi / 2, 0, math.pi / 2)
    views = [(lods[0], "front", "", *front), (lods[0], "side", "", *side), (lods[-1], "front", "", *front)]
    if groups:
        views = [(lods[0], "front", g, *front) for g in groups] + [(lod, "front", groups[-1], *front) for lod in lods[1:]]
    os.makedirs(RENDER_DIR, exist_ok=True)
    for lod, view, g, loc, rot in views:
        for o in objs:
            o.hide_render = not (o.name.startswith("Context_") or (o.name.endswith("_" + lod) and (not g or f"_{g}_" in o.name)))
        cam.location, cam.rotation_euler = loc, rot
        s.render.filepath = os.path.join(RENDER_DIR, f"{asset}_{g + '_' if g else ''}{lod}_{view}.png")
        bpy.ops.render.render(write_still=True)


def contact_sheet(gen=None):
    """Stack every asset's preview row (LOD0 front, LOD0 side, LODn front) into one committed PNG.
    With gen: only that generator's assets (row = asset; grouped assets show LOD0 per group then the other LODs; tiles at
    half size) into PROC_<gen>_contact_sheet.png; the default sheet skips grouped and own_sheet assets."""
    import numpy as np
    assets = sorted(json.load(open(MANIFEST))["assets"].items())
    assets = [(a, e) for a, e in assets if (e["generator"] == gen if gen else "preview_groups" not in e and not e.get("own_sheet"))]
    sheet_path = SHEET.replace("PROC_contact", f"PROC_{gen}_contact") if gen else SHEET
    rows = []
    for asset, entry in assets:
        lods = sorted(entry["lods"])
        names = [f"{lod}_{view}" for lod, view in ((lods[0], "front"), (lods[0], "side"), (lods[-1], "front"))]
        if gen and "preview_groups" in entry:
            g = entry["preview_groups"]
            names = [f"{x}_{lods[0]}_front" for x in g] + [f"{g[-1]}_{lod}_front" for lod in lods[1:]]
        tiles = []
        for name in names:
            img = bpy.data.images.load(os.path.join(RENDER_DIR, f"{asset}_{name}.png"))
            px = np.empty(img.size[0] * img.size[1] * 4, dtype=np.float32)
            img.pixels.foreach_get(px)
            tiles.append(px.reshape(img.size[1], img.size[0], 4)[::2, ::2] if gen else px.reshape(img.size[1], img.size[0], 4))
        rows.append(np.concatenate(tiles, axis=1))
    sheet = np.concatenate(rows[::-1], axis=0)  # Blender images are bottom-up; first asset ends on top
    out = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0])
    out.pixels.foreach_set(sheet.ravel())
    out.filepath_raw, out.file_format = sheet_path, "PNG"
    out.save()
    size = os.path.getsize(sheet_path)
    if size > 1_000_000:
        raise RuntimeError(f"contact sheet {size} bytes > 1 MB")
    print(f"[PROC] contact sheet {sheet_path} ({size} bytes): rows = {[a for a, _ in assets]}")


if __name__ == "__main__":  # Tools/Blender/tests import this module
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if argv[:1] == ["contact_sheet"]:
        contact_sheet(*argv[1:2])
    elif len(argv) == 2:
        generate(argv[0], os.path.abspath(argv[1]))
    else:
        raise SystemExit("usage: run_generator.py -- <generator> <params.json> | contact_sheet")
