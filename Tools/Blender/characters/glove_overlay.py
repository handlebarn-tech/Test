"""Nitrile glove overlay for MPFB2 characters (ASSET-007; replaces the rejected ChatGPT R4.7 tool, DEC-111).

R4.7 copied the whole basemesh, so its "glove" was a full-body shell. Here the glove is cut from the baked body:
  1. copy the body mesh (same topology, UVs and skin weights, so it deforms exactly with the hand);
  2. keep only faces weighted to the forearm chain (lowerarm_* and its children), then cut each arm with a plane square to
     the forearm, CUFF_M above the wrist (hand bone head), and delete the forearm side;
  3. push the shell out OFFSET_M along the normals, roll a bead at the cuff and give the cuff edge a lip back to the skin;
  4. own material M_nitrile_glove: Principled, near-black, satin, with a studio-made 2K micro-texture normal and roughness
     map (procedural, CC0 by construction) on the glove's own 0-1 UV layout.
The hand skin under the glove is then masked out (_mask_skin), so decimated LODs and nails never poke through.
Hooked into customer_gen.export by a roster/staff entry with "gloves": true; the part is named <id>.nitrile_gloves.
LOD0 subdivides it only if "nitrile_gloves" is in lods.LOD0.subdiv_parts (staff params must list it, like "body").

Demo + proof (no Unity), into <cache>/mpfb/derived_gloves/GLV_<id>/ (kept out of derived/ so the customer contact sheet
ignores it), and a contact sheet at Docs/Assets/Specs/gloves_contact_sheet.jpg:
  $env:BLENDER_USER_RESOURCES = '<cache>/mpfb/blender_user'
  & "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --python-exit-code 10
      --python Tools/Blender/characters/glove_overlay.py -- Tools/Blender/params/customers_mpfb.json C003,C004,C006"""
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector

PART = "nitrile_gloves"
CUFF_M = 0.075      # cuff length above the wrist joint (exam gloves end a few cm up the forearm)
OFFSET_M = 0.0015   # shell offset over the skin: clears z-fighting at LOD0/1, reads as a thin film
BEAD_M = 0.0010     # extra outward push of the rolled cuff bead
MASK_M = 0.020     # skin kept under the cuff before the hand skin is masked out
LIP_M = 0.0022      # cuff edge folded back towards the skin, so the edge has thickness
BASE_SRGB = (0.018, 0.018, 0.020)  # GAP-GLV-1: colour unconfirmed, placeholder black (IMP-003 R4.7 / R4.6 note)
TEX_PX = 2048


def _arm_faces(bm, obj, rig, side):
    chain = {b.name for b in rig.data.bones[f"lowerarm_{side}"].children_recursive} | {f"lowerarm_{side}"}
    gi = {g.index for g in obj.vertex_groups if g.name in chain}
    dl = bm.verts.layers.deform.active
    w = {v: sum(x for g, x in v[dl].items() if g in gi) for v in bm.verts}
    return [f for f in bm.faces if all(w[v] > 0.5 for v in f.verts)]


def _cut(bm, faces, rig, side):
    """Plane cut square to the forearm, CUFF_M above the wrist; return faces on the hand side."""
    lower, hand = rig.data.bones[f"lowerarm_{side}"], rig.data.bones[f"hand_{side}"]
    axis = (hand.head_local - lower.head_local).normalized()
    co = hand.head_local - axis * CUFF_M
    geom = list({e for f in faces for e in f.edges}) + faces + list({v for f in faces for v in f.verts})
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=axis)
    region = {v for f in faces if f.is_valid for v in f.verts}
    # bisect split the input faces; re-collect every face touching the region and keep the hand side
    cand = {f for v in region for f in v.link_faces}
    return [f for f in cand if (f.calc_center_median() - co).dot(axis) > 0]


def _micro_maps(tex_dir):
    """Studio-made 2K tiling nitrile micro-texture: fine pebble height -> normal (OpenGL, Y+) and roughness."""
    rng = np.random.default_rng(20261030)
    n = TEX_PX
    f = np.fft.fftfreq(n)
    r = np.sqrt(f[:, None] ** 2 + f[None, :] ** 2)
    def band(sigma):  # gaussian-filtered white noise, tiling by construction (FFT)
        spec = np.fft.fft2(rng.standard_normal((n, n))) * np.exp(-(r / sigma) ** 2)
        h = np.real(np.fft.ifft2(spec))
        return (h - h.mean()) / h.std()
    height = band(0.16)  # ~2-3 px pebbles: fine textured nitrile
    gy, gx = np.gradient(height)
    s = 0.05
    nx, ny, nz = -gx * s, -gy * s, np.ones_like(height)
    l = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    normal = np.stack([nx / l * 0.5 + 0.5, ny / l * 0.5 + 0.5, nz / l * 0.5 + 0.5, np.ones_like(height)], -1)
    rough = np.clip(0.40 + 0.06 * band(0.09), 0.0, 1.0)
    out = {}
    for name, px in (("normal", normal), ("roughness", np.stack([rough, rough, rough, np.ones_like(rough)], -1))):
        img = bpy.data.images.new(f"T_nitrile_glove_{name}", n, n, alpha=False, float_buffer=False)
        img.colorspace_settings.name = "Non-Color"
        img.pixels.foreach_set(px.astype(np.float32).ravel())
        img.filepath_raw = os.path.join(tex_dir, f"T_nitrile_glove_{name}.png")
        img.file_format = "PNG"
        img.save()
        out[name] = img
    return out


def _material(tex_dir, report):
    mat = bpy.data.materials.new("M_nitrile_glove")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*[c ** 2.2 for c in BASE_SRGB], 1.0)
    bsdf.inputs["Specular IOR Level"].default_value = 0.5
    mat.diffuse_color = (*[c ** 2.2 for c in BASE_SRGB], 1.0)  # Workbench previews
    maps = _micro_maps(tex_dir)
    tn = nt.nodes.new("ShaderNodeTexImage")
    tn.image = maps["normal"]
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(tn.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    tr = nt.nodes.new("ShaderNodeTexImage")
    tr.image = maps["roughness"]
    nt.links.new(tr.outputs["Color"], bsdf.inputs["Roughness"])
    nt.nodes.active = bsdf  # Workbench TEXTURE mode must not show the normal map as colour
    report["nitrile_glove"] = {
        "source": "studio-built (ASSET-007, procedural, CC0 by construction)",
        "base_color_srgb": list(BASE_SRGB), "metallic": 0.0, "roughness_mean": 0.40,
        "normal": {"file": "T_nitrile_glove_normal.png", "px": [TEX_PX, TEX_PX]},
        "roughness": {"file": "T_nitrile_glove_roughness.png", "px": [TEX_PX, TEX_PX]},
        "alpha_cutout": False, "tint": None, "missing": [],
        "gaps": ["GAP-GLV-1 glove colour unconfirmed (placeholder black)"]}
    return mat


def add_gloves(basemesh, rig, cid, tex_dir, report):
    """Build <cid>.nitrile_gloves from the baked basemesh (after customer_gen.build). Returns the new mesh object."""
    g = basemesh.copy()
    g.data = basemesh.data.copy()
    g.name = g.data.name = f"{cid}.{PART}"
    bpy.context.scene.collection.objects.link(g)
    bm = bmesh.new()
    bm.from_mesh(g.data)
    keep = set()
    for side in ("l", "r"):
        faces = _arm_faces(bm, g, rig, side)
        if not faces:
            raise RuntimeError(f"{cid}: no forearm faces on side {side} (sleeve mask?)")
        keep |= set(_cut(bm, faces, rig, side))
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f not in keep], context="FACES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.normal_update()
    rim = {v for e in bm.edges if e.is_boundary for v in e.verts}
    ring2 = {o for v in rim for e in v.link_edges for o in e.verts if o not in rim}
    for v in bm.verts:
        v.co += v.normal * (OFFSET_M + (BEAD_M if v in rim else BEAD_M * 0.5 if v in ring2 else 0.0))
    # lip: extrude the cuff edge back down to the skin so the open edge never reads paper-thin
    rim_edges = [e for e in bm.edges if e.is_boundary]
    ext = bmesh.ops.extrude_edge_only(bm, edges=rim_edges)
    for v in (x for x in ext["geom"] if isinstance(x, bmesh.types.BMVert)):
        src = next(o for e in v.link_edges for o in e.verts if o in rim)  # the rim vert it was extruded from
        v.co -= src.normal * LIP_M
    bm.normal_update()
    # own 0-1 UV layout (uniform scale, keeps texel density even) so the 2K micro-texture is not wasted on the skin atlas
    uv = bm.loops.layers.uv.active
    cos = np.array([l[uv].uv[:] for f in bm.faces for l in f.loops])
    lo, span = cos.min(0), max(cos.max(0) - cos.min(0))
    for f in bm.faces:
        for l in f.loops:
            l[uv].uv = (Vector(l[uv].uv) - Vector(lo)) / span
    bm.to_mesh(g.data)
    bm.free()
    g.data.materials.clear()
    g.data.materials.append(_material(tex_dir, report))
    for m in g.modifiers:
        if m.type == "ARMATURE":
            m.object = rig
    _mask_skin(basemesh, rig)
    return g


def _mask_skin(basemesh, rig):
    """Delete the hand skin under the glove (MPFB clothes do the same with delete groups): decimated LOD2/3 skin would
    otherwise poke through the shell, and so would the fingernails. MASK_M of skin is kept under the cuff, so no gap."""
    bm = bmesh.new()
    bm.from_mesh(basemesh.data)
    dead = []
    for side in ("l", "r"):
        lower, hand = rig.data.bones[f"lowerarm_{side}"], rig.data.bones[f"hand_{side}"]
        axis = (hand.head_local - lower.head_local).normalized()
        co = hand.head_local - axis * (CUFF_M - MASK_M)
        dead += [f for f in _arm_faces(bm, basemesh, rig, side) if all((v.co - co).dot(axis) > 0 for v in f.verts)]
    bmesh.ops.delete(bm, geom=dead, context="FACES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.to_mesh(basemesh.data)
    bm.free()


def _check(g, rig):
    """Self-check: two separate hand pieces, nothing above the cuff, every vertex skinned to the arm chain."""
    me = g.data
    errs = []
    for side, sgn in (("l", 1), ("r", -1)):
        lower, hand = rig.data.bones[f"lowerarm_{side}"], rig.data.bones[f"hand_{side}"]
        axis = (hand.head_local - lower.head_local).normalized()
        cut = hand.head_local - axis * CUFF_M
        vs = [v for v in me.vertices if v.co.x * sgn > 0]
        if not vs:
            errs.append(f"no {side} glove")
        bad = [v for v in vs if (v.co - cut).dot(axis) < -(LIP_M + 0.004)]
        if bad:
            errs.append(f"{len(bad)} {side} verts above the cuff (full-body shell?)")
    unskinned = [v.index for v in me.vertices if not any(x.weight > 0 for x in v.groups)]
    if unskinned:
        errs.append(f"{len(unskinned)} unskinned glove verts")
    return errs


def _render_sheet(rows, out_jpg):
    """rows: list of (tile pngs). Tiles 4 hand LODs + 1 full body per character into one JPEG (<= 1 MB)."""
    tw, th = 320, 320
    cols = max(len(r) for r in rows)
    sheet = np.full((len(rows) * th, cols * tw, 4), 0.5, dtype=np.float32)
    sheet[..., 3] = 1
    for ri, tiles in enumerate(rows):
        for ci, path in enumerate(tiles):
            img = bpy.data.images.load(path)
            img.scale(tw, th)
            px = np.empty(tw * th * 4, dtype=np.float32)
            img.pixels.foreach_get(px)
            y0 = (len(rows) - 1 - ri) * th
            sheet[y0:y0 + th, ci * tw:(ci + 1) * tw] = px.reshape(th, tw, 4)
            bpy.data.images.remove(img)
    out = bpy.data.images.new("sheet", cols * tw, len(rows) * th)
    out.pixels.foreach_set(sheet.ravel())
    s = bpy.context.scene
    s.render.image_settings.file_format, s.render.image_settings.quality = "JPEG", 85
    s.view_settings.view_transform = "Standard"
    out.save_render(out_jpg, scene=s)
    if os.path.getsize(out_jpg) > 1_000_000:
        raise RuntimeError("glove contact sheet > 1 MB")


def _proof_renders(cid, lods, rig, out_dir):
    """EEVEE: hand close-up per LOD (left hand, palm three-quarter) + LOD0 full body. Returns tile paths."""
    s = bpy.context.scene
    s.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in {e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items} else "BLENDER_EEVEE_NEXT"
    s.render.resolution_x = s.render.resolution_y = 640
    s.view_settings.view_transform = "AgX"
    s.world = s.world or bpy.data.worlds.new("W")
    s.world.use_nodes = True
    s.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.35, 0.35, 0.37, 1)
    s.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.6
    key = bpy.data.objects.new("Key", bpy.data.lights.new("Key", "AREA"))
    key.data.energy, key.data.size = 120, 1.0
    key.location, key.rotation_euler = (1.2, -1.6, 1.9), (math.radians(55), 0, math.radians(35))
    s.collection.objects.link(key)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    s.collection.objects.link(cam)
    s.camera = cam
    hand = rig.data.bones["hand_l"]
    target = hand.head_local + (hand.tail_local - hand.head_local).normalized() * 0.05  # mid-palm (hand bone is short)
    tiles = []
    shots = [(lods[k], "persp", target, 0.75, k) for k in ("LOD0", "LOD1", "LOD2", "LOD3")] + [(lods["LOD0"], "body", None, 0, "body")]
    for obj, mode, tgt, dist, name in shots:
        for o in s.objects:
            if o.type == "MESH":
                o.hide_render = o is not obj
        if mode == "persp":
            cam.data.type, cam.data.lens = "PERSP", 85
            d = Vector((0.55, -0.75, 0.25)).normalized()
            cam.location = tgt + d * dist
        else:
            h = max(v.co.z for v in obj.data.vertices)
            cam.data.type, cam.data.ortho_scale = "ORTHO", h * 1.1
            tgt = Vector((0, 0, h / 2))
            cam.location = Vector((0, -3, h / 2))
        cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
        s.render.filepath = os.path.join(out_dir, f"{cid}_gloves_{name}.png")
        bpy.ops.render.render(write_still=True)
        tiles.append(s.render.filepath)
    return tiles


def demo(argv):
    import json
    import customer_gen as G
    import roster as R
    p = json.load(open(argv[0]))
    if PART not in p["lods"]["LOD0"].setdefault("subdiv_parts", ["body"]):
        p["lods"]["LOD0"]["subdiv_parts"].append(PART)  # staff params will list it; customer params stay untouched
    G.OUT_ROOT = os.path.join(G.CACHE, "mpfb", "derived_gloves")
    roster = {c["id"]: c for c in R.generate(p)}
    rows, failed = [], {}
    for cid in argv[1].split(","):
        c = dict(roster[cid], id=f"GLV_{cid}", gloves=True)
        try:
            rep = G.export(c, p)
            out = os.path.join(G.OUT_ROOT, c["id"])
            rig = bpy.data.objects[c["id"] + "_Rig"]
            lods = {k: bpy.data.objects[f"{c['id']}_{k}"] for k in p["lods"]}
            rows.append(_proof_renders(c["id"], lods, rig, out))
            print(f"[GLV] {c['id']}: tris {rep['tris']} glove_lod1 {rep['tris_parts_lod1'].get(PART)} gloves_check {rep.get('gloves_check')}")
            if rep.get("gloves_check"):
                failed[cid] = rep["gloves_check"]
        except Exception as e:  # noqa: BLE001
            failed[cid] = str(e)
            print(f"[GLV] {cid}: FAILED {e}")
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    if rows:
        _render_sheet(rows, os.path.join(repo, "Docs/Assets/Specs/gloves_contact_sheet.jpg"))
    if failed:
        raise RuntimeError(f"glove demo failed: {failed}")


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    demo(sys.argv[sys.argv.index("--") + 1:])
