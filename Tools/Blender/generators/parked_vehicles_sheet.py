"""Parked-vehicle contact sheet for the DEC-114/DEC-122 visual review (PROC-009). Workbench + cavity, preview colours.
One row per vehicle class; tiles: LOD0 front 3/4, LOD0 rear 3/4, LOD0 side, LOD1, LOD2, LOD3 (front 3/4). Each tile is
labelled with asset, LOD/view, tri count and frame width (orthographic, so the frame width is true).
  blender -b --factory-startup --python-exit-code 10 -P Tools/Blender/generators/parked_vehicles_sheet.py
Writes Docs/Assets/Previews/PROC_parked_vehicles_contact_sheet.png."""
import json
import math
import os
import sys

import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from generators import parked_vehicles as pv  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
P = json.load(open(os.path.join(ROOT, "Tools", "Blender", "params", "parked_vehicles.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "Docs", "Assets", "Previews", "PROC_parked_vehicles_contact_sheet.png")
TMP = os.path.join(ROOT, "Artifacts", "Renders", "parked_vehicles_sheet")
TILE = (420, 280)
VIEWS = [("LOD0", "front 3/4", -38, 18), ("LOD0", "rear 3/4", 142, 18), ("LOD0", "side", -90, 4),
         ("LOD1", "front 3/4", -38, 18), ("LOD2", "front 3/4", -38, 18), ("LOD3", "front 3/4", -38, 18)]


def render_tile(asset, q, lod_name, view, az_deg, el_deg, path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    objs, (w, h, L), _ = pv.build(q, q["lods"][lod_name])
    tris = sum(len(f.vertices) - 2 for o in objs.values() for f in o.data.polygons)
    s.render.engine = "BLENDER_WORKBENCH"
    s.display.shading.light, s.display.shading.color_type = "STUDIO", "MATERIAL"
    s.display.shading.show_cavity = True
    s.render.resolution_x, s.render.resolution_y = TILE
    s.view_settings.view_transform = "Standard"
    wo = bpy.data.worlds.new("W")
    wo.color = (0.6, 0.6, 0.6)
    s.world = wo
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    s.collection.objects.link(cam)
    s.camera = cam
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = os_ = math.hypot(L, w) * 1.08
    az, el = math.radians(az_deg), math.radians(el_deg)
    tgt = np.array([0.0, 0.0, h * 0.62])
    dirv = np.array([math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)])
    cam.location = tuple(tgt + dirv * 12.0)
    cam.rotation_euler = (math.pi / 2 - el, 0, az)
    cam.data.clip_end = 40.0
    mat = bpy.data.materials.new("Label")
    mat.diffuse_color = (0.02, 0.02, 0.02, 1)
    lines = [asset, f"{lod_name} {view}   {tris:,} tris   [{os_:.1f} m frame]"]
    for i, text in enumerate(lines):
        cu = bpy.data.curves.new(f"L{i}", "FONT")
        cu.body, cu.size = text, os_ * (0.05 if i == 0 else 0.04)
        t = bpy.data.objects.new(f"L{i}", cu)
        t.data.materials.append(mat)
        s.collection.objects.link(t)
        t.parent = cam
        t.location = (-os_ * 0.48, os_ * (0.28 - 0.05 * i), -1.0)
    s.render.filepath = path
    bpy.ops.render.render(write_still=True)


def main():
    os.makedirs(TMP, exist_ok=True)
    rows = []
    for asset, q in pv.variants(P):
        row = []
        for lod, view, az, el in VIEWS:
            path = os.path.join(TMP, f"{asset}_{lod}_{view.replace(' ', '').replace('/', '')}.png")
            render_tile(asset, q, lod, view, az, el, path)
            row.append(path)
        rows.append(row)
    strips = []
    for row in rows:
        tiles = []
        for path in row:
            img = bpy.data.images.load(path)
            px = np.empty(img.size[0] * img.size[1] * 4, dtype=np.float32)
            img.pixels.foreach_get(px)
            tiles.append(px.reshape(img.size[1], img.size[0], 4))
        strips.append(np.concatenate(tiles, axis=1))
    sheet = np.concatenate(strips[::-1], axis=0)  # Blender images are bottom-up
    sheet = np.floor(sheet * 255 / 8) * 8 / 255  # 32 levels per channel keeps the PNG small (PROC-006c)
    out = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0])
    out.pixels.foreach_set(sheet.ravel())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out.filepath_raw, out.file_format = OUT, "PNG"
    out.save()
    print(f"[PV] sheet {OUT} ({os.path.getsize(OUT)} bytes)")


main()
