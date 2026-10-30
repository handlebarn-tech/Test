"""Build MPFB2 customers headless and export them to the shared cache (ASSET-004). Run via:
  Tools/Blender/blender.ps1 character Tools/Blender/params/customers_mpfb.json [C001,C002]
Needs the isolated MPFB profile (BLENDER_USER_RESOURCES = <cache>/mpfb/blender_user, set by blender.ps1) with the add-on
installed and the CC0 packs extracted by install_mpfb.py. Reads the roster from roster.py (same seed -> same people).

Per customer, into <cache>/mpfb/derived/<id>/:
  <id>.fbx          armature (MPFB game_engine rig, 53 bones, Unity Humanoid names) + one joined skinned mesh per LOD,
                    named <id>_LOD0..LOD3 (Unity LODGroup auto-setup); shape keys and masks baked; Principled materials
                    pointing at textures/ (copied, not embedded)
  textures/         every texture the materials use, copied from the CC0 asset dirs
  <id>.validation.json  identity, CC0 audit of every asset, tris per LOD vs budget, bones + Humanoid check, height,
                    materials and texture sizes, gaps, sha256
  <id>_front.png    Workbench preview, LOD0 (register framing) + LOD3 full body
Any validation error raises -> Blender exits 10 (blender.ps1 reports it)."""
import hashlib
import json
import math
import os
import shutil
import sys

import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import roster as roster_mod  # noqa: E402

from bl_ext.user_default.mpfb.services.exportservice import ExportService  # noqa: E402
from bl_ext.user_default.mpfb.services.humanservice import HumanService  # noqa: E402
from bl_ext.user_default.mpfb.services.locationservice import LocationService  # noqa: E402

CACHE = "C:/Users/handl/Downloads/Dispo Game Assets Cache"
OUT_ROOT = os.path.join(CACHE, "mpfb", "derived")
DATA = LocationService.get_user_data()
TEX_KEYS = {"diffuseTexture": "base_color", "normalmapTexture": "normal", "aomapTexture": "ao",
            "specularTexture": "specular", "transparencymapTexture": "opacity", "bumpmapTexture": "bump"}


def human_info(c, p):
    info = HumanService._create_default_human_info_dict()
    info["name"] = c["id"]
    info["phenotype"] = c["phenotype"]
    info["rig"] = p["rig"]
    info["skin_mhmat"] = f"skins/{c['skin']}/{c['skin']}.mhmat"
    info["skin_material_type"] = "MAKESKIN"
    info["eyes"] = "eyes/high-poly/high-poly.mhclo"
    info["eyebrows"] = "eyebrows/eyebrow001/eyebrow001.mhclo"
    info["eyelashes"] = "eyelashes/eyelashes01/eyelashes01.mhclo"
    info["teeth"] = "teeth/teeth_base/teeth_base.mhclo"
    info["hair"] = f"hair/{c['hair']}/{c['hair']}.mhclo" if c["hair"] else ""
    info["targets"] = c["face_targets"]
    extra = [x for x in (c["hat"], c["glasses"], c["beard"]) if x]
    info["clothes"] = [f"clothes/{i}/{i}.mhclo" for i in c["items"] + extra]
    return info


def parse_mhmat(path):
    tex = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        k, _, v = line.strip().partition(" ")
        if k in TEX_KEYS and v and not k.startswith("//"):
            tex[TEX_KEYS[k]] = os.path.join(os.path.dirname(path), v.strip())
    return tex


def source_mhmat(obj, c, basemesh):
    """Which .mhmat gave this object its look (MPFB names child objects <human>.<asset>)."""
    if obj == basemesh:
        return os.path.join(DATA, "skins", c["skin"], c["skin"] + ".mhmat")
    asset = obj.name.split(".")[-1]
    if asset == "high-poly":
        return os.path.join(DATA, "eyes", "materials", c["eyes"] + ".mhmat")
    for d in ("clothes", "hair", "eyebrows", "eyelashes", "teeth"):
        mhclo = os.path.join(DATA, d, asset, asset + ".mhclo")
        if os.path.isfile(mhclo):
            mat = [l.split(" ", 1)[1].strip() for l in open(mhclo, encoding="utf-8", errors="replace") if l.startswith("material ")]
            return os.path.join(DATA, d, asset, mat[0]) if mat else None
    return None


def tint_texture(path, rgb, dst):
    """Recolour a hair/brow/beard diffuse: keep its luminance pattern, move its mean colour to the tint (sRGB), keep alpha."""
    src = bpy.data.images.load(path, check_existing=False)
    w, h = src.size
    px = np.empty(w * h * 4, dtype=np.float32)
    src.pixels.foreach_get(px)
    px = px.reshape(-1, 4)
    lum = px[:, :3] @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    mask = px[:, 3] > 0.5
    mean = float(lum[mask].mean()) if mask.any() else float(lum.mean())
    px[:, :3] = np.clip(np.outer(lum / max(mean, 1e-3), rgb), 0.0, 1.0)
    out = bpy.data.images.new(os.path.basename(dst), w, h, alpha=True)
    out.pixels.foreach_set(px.ravel())
    out.filepath_raw, out.file_format = dst, "PNG"
    out.save()
    bpy.data.images.remove(src)
    return out


def export_material(obj, c, basemesh, tex_dir, report, p):
    """Replace MPFB's Blender-only node trees with a Principled BSDF on the asset's own textures (copied to tex_dir)."""
    src = source_mhmat(obj, c, basemesh)
    if not src or not os.path.isfile(src):
        raise RuntimeError(f"{obj.name}: no source material found ({src})")
    kind = os.path.relpath(src, DATA).replace("\\", "/").split("/")
    cutout = kind[0] in ("hair", "eyebrows", "eyelashes") or (kind[0] == "clothes" and kind[1] in p["beards"])
    tint = c["hair_tint"] if cutout and kind[0] != "eyelashes" else None
    tex = parse_mhmat(src)
    name = os.path.splitext(os.path.basename(src))[0]
    if tint:
        name += "_" + tint  # per-tint name, so Unity's by-name material extraction never merges two tints
    mat = bpy.data.materials.get("M_" + name) or bpy.data.materials.new("M_" + name)
    if not mat.use_nodes or "Principled BSDF" not in mat.node_tree.nodes:
        mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    for role, path in tex.items():
        if not os.path.isfile(path):
            continue  # some mhmat lines point at textures the asset never shipped; recorded below
        dst = os.path.join(tex_dir, os.path.basename(path))
        if tint and role == "base_color":
            dst = os.path.join(tex_dir, f"{os.path.splitext(os.path.basename(path))[0]}_{tint}.png")
            img = tint_texture(path, p["hair_tint_srgb"][tint], dst)
        else:
            if not os.path.exists(dst):
                shutil.copyfile(path, dst)
            img = bpy.data.images.load(dst, check_existing=True)
        report.setdefault(name, {})[role] = {"file": os.path.basename(dst), "px": list(img.size)}
        node = nt.nodes.new("ShaderNodeTexImage")
        node.image = img
        if role == "base_color":
            nt.nodes.active = node  # Workbench previews show the active image node (else the normal map shows)
            nt.links.new(node.outputs["Color"], bsdf.inputs["Base Color"])
            if cutout:  # hair/brow/lash cards: alpha-clip in Unity
                nt.links.new(node.outputs["Alpha"], bsdf.inputs["Alpha"])
        elif role == "normal":
            img.colorspace_settings.name = "Non-Color"
            nm = nt.nodes.new("ShaderNodeNormalMap")
            nt.links.new(node.outputs["Color"], nm.inputs["Color"])
            nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
        else:
            img.colorspace_settings.name = "Non-Color"  # ao/spec/opacity: copied and listed for the Unity importer
    report.setdefault(name, {})["source"] = os.path.relpath(src, DATA).replace("\\", "/")
    report[name]["alpha_cutout"] = cutout
    report[name]["tint"] = tint
    report[name]["missing"] = sorted(r for r, pth in tex.items() if not os.path.isfile(pth))
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def bake(objs):
    """Apply shape keys (targets) and the remaining mask modifiers, keep the Armature modifier."""
    for o in objs:
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        if o.data.shape_keys:
            bpy.ops.object.shape_key_remove(all=True, apply_mix=True)
        for m in list(o.modifiers):
            if m.type != "ARMATURE":
                bpy.ops.object.modifier_apply(modifier=m.name)
        o.select_set(False)


def tris(o):
    me = o.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh()
    me.calc_loop_triangles()
    n = len(me.loop_triangles)
    o.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh_clear()
    return n


def make_lod(base_objs, rig, cid, lod_name, lod, basemesh):
    """Duplicate the LOD1 base meshes, drop small parts, subdivide or decimate, join into one skinned mesh."""
    keep = [o for o in base_objs if not any(d in o.name.split(".")[-1] for d in lod["drop"])]
    dups = []
    for o in keep:
        d = o.copy()
        d.data = o.data.copy()
        bpy.context.scene.collection.objects.link(d)
        is_card = any(k in o.name for k in ("eyelashes", "eyebrow", "high-poly"))
        part = "body" if o == basemesh else o.name.split(".")[-1]
        if lod["subdiv"] and not is_card and part in lod.get("subdiv_parts", [part]):
            m = d.modifiers.new("Sub", "SUBSURF")
            m.levels = m.render_levels = lod["subdiv"]
            bpy.ops.object.select_all(action="DESELECT")
            bpy.context.view_layer.objects.active = d
            d.modifiers.move(len(d.modifiers) - 1, 0)  # before Armature
            bpy.ops.object.modifier_apply(modifier="Sub")
        if lod["ratio"] < 1.0:
            m = d.modifiers.new("Dec", "DECIMATE")
            m.ratio = lod["ratio"]
            m.use_collapse_triangulate = True
            bpy.context.view_layer.objects.active = d
            d.modifiers.move(len(d.modifiers) - 1, 0)
            bpy.ops.object.modifier_apply(modifier="Dec")
        dups.append(d)
    bpy.ops.object.select_all(action="DESELECT")
    for d in dups:
        d.select_set(True)
    bpy.context.view_layer.objects.active = dups[0]
    bpy.ops.object.join()
    j = bpy.context.view_layer.objects.active
    j.name = j.data.name = f"{cid}_{lod_name}"
    j.parent = rig
    for m in j.modifiers:
        if m.type == "ARMATURE":
            m.object = rig
    return j


def build(c, p):
    bpy.ops.wm.read_homefile(use_empty=True)
    settings = HumanService.get_default_deserialization_settings()
    settings["subdiv_levels"] = 0
    basemesh = HumanService.deserialize_from_dict(human_info(c, p), settings)
    rig = basemesh.parent
    rig.name = c["id"] + "_Rig"
    ExportService.bake_modifiers_remove_helpers(basemesh, bake_masks=True, bake_subdiv=False, remove_helpers=True)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    bake(meshes)
    return rig, meshes, basemesh


def humanoid_check(rig, p):
    names = {b.name for b in rig.data.bones}
    return [b for b in p["humanoid_required_bones"] if b not in names]


def render_preview(cid, lod0, lod3, out_png):
    s = bpy.context.scene
    s.render.engine = "BLENDER_WORKBENCH"
    s.display.shading.light, s.display.shading.color_type = "STUDIO", "TEXTURE"
    s.render.resolution_x, s.render.resolution_y = 768, 640
    s.view_settings.view_transform = "Standard"
    s.world = s.world or bpy.data.worlds.new("W")
    s.world.color = (0.5, 0.5, 0.5)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    s.collection.objects.link(cam)
    s.camera = cam
    h = max(v.co.z for v in lod0.data.vertices)
    tiles = []
    for obj, ortho, z, name in ((lod0, 0.75, h - 0.33, "head"), (lod0, h * 1.1, h / 2, "lod0"), (lod3, h * 1.1, h / 2, "lod3")):
        for o in s.objects:
            o.hide_render = o.type == "MESH" and o is not obj
        cam.data.type, cam.data.ortho_scale = "ORTHO", ortho
        cam.location, cam.rotation_euler = (0, -3, z), (math.pi / 2, 0, 0)
        s.render.filepath = out_png.replace(".png", f"_{name}.png")
        bpy.ops.render.render(write_still=True)
        tiles.append(s.render.filepath)
    return tiles


def export(c, p):
    cid = c["id"]
    out = os.path.join(OUT_ROOT, cid)
    tex_dir = os.path.join(out, "textures")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(tex_dir)
    errors, gaps = [], []
    index = json.load(open(roster_mod.INDEX))
    audit = {a: index.get(a, {"allowed": False, "reasons": ["missing"]}) for a in roster_mod.assets_of(c)}
    errors += [f"licence: {a} {v.get('reasons')}" for a, v in audit.items() if not v.get("allowed")]

    rig, meshes, basemesh = build(c, p)
    tex_report = {}
    for o in meshes:
        export_material(o, c, basemesh, tex_dir, tex_report, p)
    missing = humanoid_check(rig, p)
    if missing:
        errors.append(f"rig lacks Humanoid bones {missing}")

    # body + clothes without hair/hat (clothing masks delete covered body verts, so the body alone is not enough)
    zs = [v.co.z for o in meshes if o.name.split(".")[-1] not in (c["hair"], c["hat"]) for v in o.data.vertices]
    height = round(max(zs) - min(zs), 3)
    parts_lod1 = {("body" if o == basemesh else o.name.split(".")[-1]): tris(o) for o in meshes}
    lods = {name: make_lod(meshes, rig, cid, name, lod, basemesh) for name, lod in p["lods"].items()}
    for o in meshes:
        bpy.data.objects.remove(o, do_unlink=True)
    lod_tris = {k: tris(o) for k, o in lods.items()}
    for k, n in lod_tris.items():
        if n > p["tri_budget"][k]:
            errors.append(f"{k}: {n} tris > budget {p['tri_budget'][k]}")
    lo, hi = p["height_m_range"][c["sex"]]
    if not lo <= height <= hi:
        errors.append(f"height {height} m outside {lo}-{hi} m")
    for mat, roles in tex_report.items():
        for role, t in roles.items():
            if isinstance(t, dict) and role in ("base_color", "normal") and p["solid_colour_texture_px"] < max(t["px"]) < p["min_texture_px"]:
                gaps.append(f"{mat}.{role} {t['px'][0]}px < {p['min_texture_px']}")
        if roles.get("missing"):
            gaps.append(f"{mat}: mhmat lists missing textures {roles['missing']}")
        if "normal" not in roles and roles.get("source", "").startswith("skins/"):
            gaps.append(f"{mat}: skin has no normal map (Unity: detail normal + SSS, CHARACTERS.md section 10)")

    fbx = os.path.join(out, cid + ".fbx")
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.export_scene.fbx(
        filepath=fbx, use_selection=False, object_types={"ARMATURE", "MESH"}, apply_scale_options="FBX_SCALE_ALL",
        axis_forward="-Z", axis_up="Y", add_leaf_bones=False, bake_anim=False, path_mode="RELATIVE",
        primary_bone_axis="Y", secondary_bone_axis="X", use_armature_deform_only=True, mesh_smooth_type="FACE")
    previews = render_preview(cid, lods["LOD0"], lods["LOD3"], os.path.join(out, cid + ".png"))

    report = {
        "id": cid, "identity": {k: c[k] for k in ("sex", "age_band", "ancestry", "skin", "hair", "hair_tint", "hat", "outfit",
                                                  "items", "glasses", "beard", "eyes", "build")},
        "phenotype": c["phenotype"], "face_targets": len(c["face_targets"]),
        "licence_audit": audit, "tris": lod_tris, "tris_parts_lod1": parts_lod1, "tri_budget": p["tri_budget"], "height_m": height,
        "rig": {"name": p["rig"], "bones": len(rig.data.bones), "humanoid_missing": missing},
        "materials": tex_report, "gaps": gaps, "errors": errors,
        "fbx": {"file": os.path.basename(fbx), "bytes": os.path.getsize(fbx),
                "sha256": hashlib.sha256(open(fbx, "rb").read()).hexdigest()},
        "previews": [os.path.basename(x) for x in previews],
        "pipeline": {"mpfb": "2.0.18", "blender": bpy.app.version_string, "params_seed": p["seed"]},
    }
    with open(os.path.join(out, cid + ".validation.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, indent=1)
        f.write("\n")
    print(f"[CHAR] {cid}: " + ", ".join(f"{k}={v}" for k, v in lod_tris.items()) + f", h={height} m, gaps={len(gaps)}, errors={len(errors)}")
    if errors:
        raise RuntimeError(f"{cid} validation failed:\n  " + "\n  ".join(errors))
    return report


def main(argv):
    p = json.load(open(argv[0]))
    ids = argv[1].split(",") if len(argv) > 1 else p["export_ids"]
    roster = {c["id"]: c for c in roster_mod.generate(p)}
    reports, failed = [], {}
    for i in ids:  # one bad customer must not stop the batch; the run still exits non-zero below
        try:
            reports.append(export(roster[i], p))
        except Exception as e:  # noqa: BLE001
            failed[i] = str(e)
            print(f"[CHAR] {i}: FAILED {e}")
    path = os.path.join(OUT_ROOT, "summary.validation.json")
    old = json.load(open(path)) if os.path.isfile(path) else {}
    summary = old.get("exported", {})  # merge: a partial re-run keeps the other customers
    failed = {**{k: v for k, v in old.get("failed", {}).items() if k not in ids}, **failed}
    summary = {k: v for k, v in summary.items() if k not in failed}
    summary.update({r["id"]: {"tris": r["tris"], "height_m": r["height_m"], "gaps": len(r["gaps"]), "fbx_sha256": r["fbx"]["sha256"]} for r in reports})
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"exported": dict(sorted(summary.items())), "failed": failed}, f, indent=1)
        f.write("\n")
    if failed:
        raise RuntimeError(f"{len(failed)} customer(s) failed: {sorted(failed)}")


argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if not argv:
    raise SystemExit("usage: customer_gen.py -- <params.json> [C001,C002]")
main(argv)
