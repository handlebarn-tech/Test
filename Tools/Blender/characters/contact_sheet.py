"""Contact sheet of the exported MPFB customers (ASSET-004). Tiles every <cache>/mpfb/derived/<id>/<id>_head.png (register
framing) into one JPEG, row-major from the top left in id order (C001, C002, ...), 10 per row. Unlabelled: the order is the label.
Run: "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --factory-startup --python-exit-code 10
       --python Tools/Blender/characters/contact_sheet.py
Output: Docs/Assets/Specs/customers_mpfb_contact_sheet.jpg (must stay <= 1 MB, ASSET-004 rule)."""
import json
import os

import bpy
import numpy as np

DERIVED = "C:/Users/handl/Downloads/Dispo Game Assets Cache/mpfb/derived"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(REPO, "Docs/Assets/Specs/customers_mpfb_contact_sheet.jpg")
COLS, TW, TH = 10, 192, 160

def passed(cid):
    v = os.path.join(DERIVED, cid, cid + ".validation.json")
    return os.path.isfile(v) and not json.load(open(v))["errors"]


ids = sorted(d for d in os.listdir(DERIVED) if os.path.isfile(os.path.join(DERIVED, d, d + "_head.png")) and passed(d))
rows = -(-len(ids) // COLS)
sheet = np.full((rows * TH, COLS * TW, 4), 0.5, dtype=np.float32)
sheet[..., 3] = 1.0
for n, cid in enumerate(ids):
    img = bpy.data.images.load(os.path.join(DERIVED, cid, cid + "_head.png"))
    img.scale(TW, TH)
    px = np.empty(TW * TH * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    r, c = divmod(n, COLS)
    y0 = (rows - 1 - r) * TH  # Blender images start bottom-left; keep C001 at the top left
    sheet[y0:y0 + TH, c * TW:(c + 1) * TW] = px.reshape(TH, TW, 4)
    bpy.data.images.remove(img)
out = bpy.data.images.new("sheet", COLS * TW, rows * TH)
out.pixels.foreach_set(sheet.ravel())
scene = bpy.context.scene
scene.render.image_settings.file_format = "JPEG"
scene.render.image_settings.quality = 85
scene.view_settings.view_transform = "Standard"  # the default (AgX) would re-grade the already-rendered previews
out.save_render(OUT, scene=scene)
size = os.path.getsize(OUT)
print(f"[SHEET] {len(ids)} customers -> {OUT} ({size} bytes)")
if size > 1_000_000:
    raise SystemExit("contact sheet > 1 MB")
