"""PROC-006b preview: 4 differently dressed register stations from the arranger JSONs, as one 2x2 PNG.
  blender -b --factory-startup --python-exit-code 10 -P Tools/Blender/generators/register_stations_sheet.py -- POS_02 POS_06 POS_07 POS_09
Props are rebuilt at LOD0 with register_kit.build(); the counter, under-shelves and stand are grey context slabs at the
anchor heights in params (preview only, World owns that geometry). Station frame: x = u, y = v, so -Y faces the operator."""
import json
import math
import os
import sys

import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from generators import register_kit as rk  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
P = json.load(open(os.path.join(ROOT, "Tools", "Blender", "params", "register_kit.json"), encoding="utf-8"))
AR = P["arranger"]
OUT = os.path.join(ROOT, "Docs", "Assets", "Specs", "PROC_register_kit_stations_sheet.png")
TILE = (560, 420)


def slab(name, u0, u1, v0, v1, z, t=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((u0 + u1) / 2, (v0 + v1) / 2, z - t / 2))
    o = bpy.context.object
    o.name, o.scale = name, (u1 - u0, v1 - v0, t)
    o.color = (0.42, 0.42, 0.44, 1)


def render_station(st, path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    a, h = AR["anchors"], st["top_half_width_m"]
    (su0, su1), (sv0, sv1) = st["stand_m"]["u"], st["stand_m"]["v"]
    slab("Ctx_Top", -h, h, 0, a["TOP"]["v_m"][1], a["TOP"]["z_m"], 0.04)
    for k in ("UNDER_UPPER", "UNDER_LOWER"):
        slab("Ctx_" + k, -h, h, 0, a[k]["v_m"][1], a[k]["z_m"])
    slab("Ctx_StandTop", su0, su1, sv0, sv1, a["STAND_RAIL"]["z_m"])
    slab("Ctx_StandLower", su0, su1, sv0, sv1, a["STAND_LOWER"]["z_m"])
    slab("Ctx_Floor", -h - 0.3, h + 0.3, -1.0, 0.8, 0.0)
    cache = {}
    for it in st["items"]:
        iid = it["asset"][len(P["asset_prefix"]):]
        if iid not in cache:
            q = {k: v for k, v in P.items() if k != "items"}
            q.update(next(i for i in P["items"] if i["id"] == iid))
            objs, _, extra = rk.build(q, q["lods"]["LOD0"])
            ap = extra["register_kit"].get("attach_point_unity_xyz")
            off = (-ap[0], -ap[2], ap[1]) if ap and a[it["anchor"]].get("edge") else (0, 0, 0)  # inverse of to_unity
            for o in objs.values():
                o.hide_render = o.hide_viewport = True
            cache[iid] = (list(objs.values()), off)
        tmpl, off = cache[iid]
        yaw = math.radians(it["yaw_deg"])
        ox = off[0] * math.cos(yaw) - off[1] * math.sin(yaw)
        oy = off[0] * math.sin(yaw) + off[1] * math.cos(yaw)
        for t in tmpl:
            o = t.copy()
            s.collection.objects.link(o)
            o.hide_render = o.hide_viewport = False
            o.location = (it["pos_m"][0] - ox, it["pos_m"][1] - oy, it["pos_m"][2] - off[2])
            o.rotation_euler = (0, 0, yaw)
    s.render.engine = "BLENDER_WORKBENCH"
    s.display.shading.light, s.display.shading.color_type = "STUDIO", "MATERIAL"
    s.display.shading.show_cavity = True
    s.render.resolution_x, s.render.resolution_y = TILE
    s.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("W")
    w.color = (0.55, 0.55, 0.55)
    s.world = w
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    s.collection.objects.link(cam)
    s.camera = cam
    cam.data.lens = 28
    cam.location = (-0.35, -1.75, 1.55)  # operator side, a little left, looking forward and down
    d = np.array([0.15, 0.25, 0.45]) - np.array(cam.location)
    cam.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    s.render.filepath = path
    bpy.ops.render.render(write_still=True)


def main(names):
    tiles = []
    for n in names:
        st = json.load(open(os.path.join(ROOT, AR["out_dir"], f"{n}.json"), encoding="utf-8"))
        path = os.path.join(ROOT, "Artifacts", "Renders", f"RK_Station_{n}.png")
        render_station(st, path)
        img = bpy.data.images.load(path)
        px = np.empty(img.size[0] * img.size[1] * 4, dtype=np.float32)
        img.pixels.foreach_get(px)
        tiles.append(px.reshape(img.size[1], img.size[0], 4))
    top, bottom = np.concatenate(tiles[:2], axis=1), np.concatenate(tiles[2:4], axis=1)
    sheet = np.concatenate([bottom, top], axis=0)  # Blender images are bottom-up
    out = bpy.data.images.new("sheet", sheet.shape[1], sheet.shape[0])
    out.pixels.foreach_set(sheet.ravel())
    out.filepath_raw, out.file_format = OUT, "PNG"
    out.save()
    print(f"[RK] station sheet {OUT} ({os.path.getsize(OUT)} bytes): {names}")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv or ["POS_02", "POS_06", "POS_07", "POS_09"])
