"""PROC-005 PBR finish library (DEC-084 / IMP-003 Q0.3, "baked from procedural detail"). Original, seeded, tileable
2K maps per surface *finish* (not per colour). Run inside Blender (numpy + bpy image I/O):
  Tools/Blender/blender.ps1 textures
Each finish writes UnityProject/Assets/_Game/Art/Procedural/Textures/<Finish>/T_Proc_<Finish>_{BaseColor,Normal,Mask}.png
  BaseColor: greyscale albedo variation, mean ALBEDO_MEAN; the material tint (the cited params colour) is
             tint / ALBEDO_MEAN so the average surface equals the cited colour.
  Normal:    tangent space, OpenGL (+Y up, Unity convention).
  Mask:      HDRP mask map: R metallic, G AO, B detail mask, A smoothness.
Maps tile every `tile_m` metres on UVMap_Main (1 UV unit = 1 m box projection, kept until PROC-007 / DEC-097), so
texel density = 2048 / tile_m px per metre (e.g. 4096 px/m at 0.5 m: denser than a unique 4K unwrap of a 1 m part).
Colours never come from here: every tint stays a cited params value (or a GAP)."""
import hashlib
import json
import math
import os

import numpy as np

N = 2048
ALBEDO_MEAN = 0.8
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
TEX_REL = "UnityProject/Assets/_Game/Art/Procedural/Textures"
TEX_DIR = os.path.join(ROOT, TEX_REL)
INDEX = os.path.join(TEX_DIR, "finishes.json")

# finish -> tile size (m), metallic, base smoothness, normal strength, seed
FINISHES = {
    "powder_coat":   dict(tile_m=0.5, metallic=0.0, smooth=0.42, normal=1.0, seed=1),
    "enamel":        dict(tile_m=0.5, metallic=0.0, smooth=0.72, normal=0.6, seed=2),
    "brushed_metal": dict(tile_m=0.5, metallic=1.0, smooth=0.58, normal=0.8, seed=3),
    "chrome":        dict(tile_m=0.5, metallic=1.0, smooth=0.90, normal=0.3, seed=4),
    "plastic":       dict(tile_m=0.25, metallic=0.0, smooth=0.38, normal=1.0, seed=5),
    "rubber":        dict(tile_m=0.25, metallic=0.0, smooth=0.12, normal=1.0, seed=6),
    "laminate":      dict(tile_m=1.0, metallic=0.0, smooth=0.30, normal=0.5, seed=7),
    "wood":          dict(tile_m=1.0, metallic=0.0, smooth=0.48, normal=0.7, seed=8),
    "wood_light":    dict(tile_m=1.0, metallic=0.0, smooth=0.30, normal=0.8, seed=9),
    "fabric":        dict(tile_m=0.1, metallic=0.0, smooth=0.08, normal=1.2, seed=10),
    "cork":          dict(tile_m=0.3, metallic=0.0, smooth=0.10, normal=1.4, seed=11),
    "porcelain":     dict(tile_m=1.0, metallic=0.0, smooth=0.88, normal=0.2, seed=12),
    "glass":         dict(tile_m=0.5, metallic=0.0, smooth=0.95, normal=0.1, seed=13),
    "mirror":        dict(tile_m=0.5, metallic=1.0, smooth=0.97, normal=0.1, seed=14),
    "paper":         dict(tile_m=0.2, metallic=0.0, smooth=0.18, normal=0.8, seed=15),
    "stone":         dict(tile_m=1.0, metallic=0.0, smooth=0.70, normal=0.4, seed=16),
    "cotton":        dict(tile_m=0.2, metallic=0.0, smooth=0.05, normal=1.5, seed=17),
    "emissive":      dict(tile_m=1.0, metallic=0.0, smooth=0.80, normal=0.0, seed=18),
}

# Colour key -> finish, first match wins (case-sensitive substrings of the params colour keys). Params can override
# with "finishes": {"<key>": "<finish>"}.
RULES = [
    (("LED", "LCD", "Emissive", "Backlit"), "emissive"),
    (("Mirror",), "mirror"),
    (("Glass", "Acrylic"), "glass"),
    (("Chrome",), "chrome"),
    (("Stainless", "Brushed", "Aluminium", "Silver", "Brass"), "brushed_metal"),
    (("Ply", "Light_Wood"), "wood_light"),
    (("Walnut", "Wood", "Plank"), "wood"),
    (("Cork",), "cork"),
    (("Fabric", "Mesh", "Net"), "fabric"),
    (("Rubber",), "rubber"),
    (("Paper", "Label", "Plate_Blank"), "paper"),
    (("Vitreous", "Porcelain"), "porcelain"),
    (("Quartz", "Stone"), "stone"),
    (("Mop", "Cotton", "Bristle"), "cotton"),
    (("Laminate", "ML1", "Top"), "laminate"),
    (("Enamel", "Appliance", "Board"), "enamel"),
    (("Plastic", "Keys", "Bucket", "Hamper", "Handle"), "plastic"),
    (("Metal", "Frame", "Locker", "Cabinet", "Steel", "Epoxy", "Wire", "Trim", "Black", "Grey"), "powder_coat"),
]


def finish_of(key, p=None):
    f = (p or {}).get("finishes", {}).get(key)
    if f:
        return f
    return next((f for keys, f in RULES if any(k in key for k in keys)), "plastic")


# --- tileable noise -------------------------------------------------------------------------------------------------

def spectral(rng, beta=2.0, fmin=1.0, fmax=None, ax=1.0, ay=1.0, n=N):
    """Periodic 1/f^beta noise (FFT-filtered white noise), zero mean, unit std. ax/ay > 1 squash frequencies along
    x/y (ax large = streaks along x)."""
    F = np.fft.fft2(rng.standard_normal((n, n)))
    fx = np.fft.fftfreq(n)[None, :] * n * ax
    fy = np.fft.fftfreq(n)[:, None] * n * ay
    f = np.hypot(fx, fy)
    f[0, 0] = 1.0
    amp = f ** (-beta / 2)
    amp[f < fmin] = 0.0
    if fmax:
        amp *= np.exp(-(f / fmax) ** 2)
    out = np.real(np.fft.ifft2(F * amp))
    return (out - out.mean()) / (out.std() + 1e-12)


def scratches(rng, count, max_len, n=N):
    """Thin random straight scratches (wrapped, so tileable): 0..1 mask."""
    m = np.zeros((n, n))
    for _ in range(count):
        x0, y0 = rng.uniform(0, n, 2)
        a = rng.uniform(0, math.pi)
        L = rng.uniform(0.2, 1.0) * max_len
        t = np.linspace(0, L, max(2, int(L * 1.5)))
        xs = ((x0 + t * math.cos(a)) % n).astype(int)
        ys = ((y0 + t * math.sin(a)) % n).astype(int)
        np.add.at(m, (ys, xs), rng.uniform(0.4, 1.0))
    return np.clip(m, 0, 1)


def blotches(rng, fmax, thresh):
    """Soft low-frequency patches (smudges, wipe marks, fingerprints): 0..1."""
    s = spectral(rng, beta=3.0, fmin=2, fmax=fmax)
    return np.clip((s - thresh) / 1.5, 0, 1)


def grain(rng, rings, warp, n=N):
    """Wood figure along x: warped growth lines + pores. Returns (albedo var, height)."""
    y = np.arange(n)[:, None] / n
    w = spectral(rng, beta=3.5, fmin=1, fmax=12, ax=0.15) * warp
    phase = 2 * np.pi * (rings * y + w)
    lines = 0.5 + 0.5 * np.sin(phase)
    late = lines ** 6  # dark latewood bands
    pores = np.clip(spectral(rng, beta=0.5, fmin=200, ax=12.0) - 1.6, 0, None)
    fig = spectral(rng, beta=2.5, fmin=1, fmax=40, ax=6.0)
    alb = 1.0 - 0.32 * late - 0.08 * fig - 0.12 * np.clip(pores, 0, 1)
    return alb, -0.6 * pores - 0.15 * late


# --- per finish: (albedo variation around 1, height, smoothness offset) ---------------------------------------------

def build(name):
    d = FINISHES[name]
    rng = np.random.default_rng(1000 + d["seed"])
    z = np.zeros((N, N))
    if name in ("powder_coat", "enamel"):
        peel = spectral(rng, beta=2.0, fmin=40, fmax=260)  # orange peel
        sc = scratches(rng, 60 if name == "powder_coat" else 25, N * 0.08)
        smud = blotches(rng, 10, 0.8)
        return 1 + 0.025 * spectral(rng, 3, 1, 20) + 0.15 * sc, 0.5 * peel - 1.5 * sc, -0.12 * smud - 0.25 * sc
    if name in ("brushed_metal",):
        streak = spectral(rng, beta=1.0, fmin=4, ax=60.0)
        sc = scratches(rng, 120, N * 0.1)
        smud = blotches(rng, 10, 0.7)
        return 1 + 0.05 * streak + 0.1 * sc, 0.6 * streak - 1.0 * sc, 0.05 * streak - 0.15 * smud - 0.2 * sc
    if name in ("chrome", "mirror", "glass"):
        sc = scratches(rng, 40, N * 0.05)
        smud = blotches(rng, 8, 0.9)
        return 1 + 0.03 * sc, -0.4 * sc + 0.1 * spectral(rng, 3, 1, 6), -0.06 * smud - 0.15 * sc
    if name in ("plastic", "rubber"):
        stip = spectral(rng, beta=1.0, fmin=120, fmax=700)  # moulded stipple / grain
        sc = scratches(rng, 30, N * 0.06)
        smud = blotches(rng, 10, 0.9)
        return 1 + 0.03 * spectral(rng, 3, 1, 16) + 0.08 * sc, 0.8 * stip - 0.8 * sc, 0.05 * stip - 0.1 * smud + 0.15 * sc
    if name == "laminate":
        paper = spectral(rng, beta=1.2, fmin=80, fmax=900)
        wipe = blotches(rng, 6, 0.6)
        return 1 + 0.02 * spectral(rng, 2.5, 1, 30), 0.3 * paper, 0.12 * wipe - 0.03 * paper
    if name in ("wood", "wood_light"):
        alb, h = grain(rng, rings=9 if name == "wood" else 14, warp=0.35 if name == "wood" else 0.2)
        return alb, h, 0.1 * h
    if name == "fabric":
        x = np.arange(N)[None, :] / N
        y = np.arange(N)[:, None] / N
        k = 2 * np.pi * 96  # 96 threads per tile (0.1 m): ~1 mm weave
        weave = np.sin(k * x) * np.sin(k * y)
        fuzz = spectral(rng, 1.0, 200)
        return 1 + 0.08 * weave + 0.04 * fuzz + 0.03 * spectral(rng, 3, 1, 8), 0.8 * weave + 0.3 * fuzz, z
    if name == "cork":
        gr = spectral(rng, beta=0.8, fmin=60, fmax=500)
        speck = (spectral(rng, beta=0.3, fmin=300) > 2.2).astype(float)
        return 1 + 0.18 * gr - 0.3 * speck, gr - 1.2 * speck, z
    if name == "porcelain":
        return 1 + 0.01 * spectral(rng, 3, 1, 10), 0.3 * spectral(rng, 3.0, 1, 12), -0.08 * blotches(rng, 8, 1.0)
    if name == "paper":
        fib = spectral(rng, beta=1.0, fmin=60, fmax=900, ax=3.0)
        return 1 + 0.03 * fib, 0.5 * fib, z
    if name == "stone":
        speck = spectral(rng, beta=0.4, fmin=200)
        return 1 + 0.04 * spectral(rng, 2.5, 1, 30) - 0.12 * np.clip(speck - 1.8, 0, 1), 0.1 * speck, z
    if name == "cotton":
        strand = spectral(rng, beta=0.8, fmin=30, fmax=600, ax=0.05)
        return 1 + 0.12 * strand, strand, z
    return np.ones((N, N)), z, z  # emissive


def normal_from_height(h, strength):
    """Tileable central differences; OpenGL green (+Y up)."""
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * strength * 0.08
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * strength * 0.08
    n = np.dstack([-dx, dy, np.ones_like(h)])  # image rows go down; Blender pixel rows go up (flipped on save)
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return n * 0.5 + 0.5


def save_png(path, rgba):
    import bpy
    h, w = rgba.shape[:2]
    img = bpy.data.images.new(os.path.basename(path), w, h, alpha=True, float_buffer=False)
    img.colorspace_settings.name = "Non-Color"
    q = np.round(np.clip(rgba, 0, 1) * 255) / 255  # quantise first: identical bytes on every run
    img.pixels.foreach_set(q[::-1].astype(np.float32).ravel())
    img.filepath_raw, img.file_format = path, "PNG"
    img.save()
    bpy.data.images.remove(img)


def generate_all():
    index = {"albedo_mean": ALBEDO_MEAN, "size_px": N, "uv": "UVMap_Main, 1 UV unit = 1 m; tiling = 1 / tile_m",
             "normal": "OpenGL (+Y)", "mask": "HDRP MaskMap: R metallic, G AO, B detail mask, A smoothness",
             "finishes": {}}
    for name, d in FINISHES.items():
        alb, h, ds = build(name)
        alb = np.clip(alb * ALBEDO_MEAN / alb.mean(), 0, 1)
        smooth = np.clip(d["smooth"] + ds, 0, 1)
        out = os.path.join(TEX_DIR, name)
        os.makedirs(out, exist_ok=True)
        files = {}
        for kind, img in (("BaseColor", np.dstack([alb, alb, alb, np.ones_like(alb)])),
                          ("Normal", np.dstack([normal_from_height(h, d["normal"]), np.ones_like(h)])),
                          ("Mask", np.dstack([np.full_like(h, d["metallic"]), np.ones_like(h), np.ones_like(h), smooth]))):
            path = os.path.join(out, f"T_Proc_{name}_{kind}.png")
            save_png(path, img)
            with open(path, "rb") as f:
                files[kind] = {"path": f"{TEX_REL}/{name}/T_Proc_{name}_{kind}.png", "sha256": hashlib.sha256(f.read()).hexdigest()[:16]}
        index["finishes"][name] = {**{k: d[k] for k in ("tile_m", "metallic", "smooth")},
                                   "texel_px_per_m": round(N / d["tile_m"]), "maps": files}
        print(f"[PROC] finish {name}: {files['BaseColor']['path']}")
    with open(INDEX, "w", newline="\n") as f:
        json.dump(index, f, indent=2, sort_keys=True)
        f.write("\n")


# --- Blender preview materials (renders only; never in the FBX, which carries material names only, M4) -------------

def _img(path):
    import bpy
    img = bpy.data.images.load(path, check_existing=True)
    img.colorspace_settings.name = "Non-Color"
    return img


def preview_material(mat, key, p):
    """Rebuild a M_Proc_<key> material as a Principled BSDF with the finish maps, the cited tint, and the mesh's
    'Wear' attribute (R convex edges -> lighter, rougher; G creases -> grime) scaled by params wear."""
    import bpy  # noqa: F401
    name = finish_of(key, p)
    d = FINISHES[name]
    rgba = list(p["colors"][key])
    w = p.get("wear", {})
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    nn, ln = nt.nodes.new, nt.links.new
    out, bsdf = nn("ShaderNodeOutputMaterial"), nn("ShaderNodeBsdfPrincipled")
    ln(bsdf.outputs[0], out.inputs[0])
    if name == "emissive":
        bsdf.inputs["Base Color"].default_value = rgba[:3] + [1]
        bsdf.inputs["Emission Color"].default_value = rgba[:3] + [1]
        bsdf.inputs["Emission Strength"].default_value = 3.0
        return
    uv = nn("ShaderNodeUVMap")
    uv.uv_map = "UVMap_Main"
    sc = nn("ShaderNodeVectorMath")
    sc.operation = "SCALE"
    sc.inputs["Scale"].default_value = 1.0 / d["tile_m"]
    ln(uv.outputs[0], sc.inputs[0])
    tex = {}
    for kind in ("BaseColor", "Normal", "Mask"):
        t = nn("ShaderNodeTexImage")
        t.image = _img(os.path.join(TEX_DIR, name, f"T_Proc_{name}_{kind}.png"))
        ln(sc.outputs[0], t.inputs[0])
        tex[kind] = t
    tint = nn("ShaderNodeMix")
    tint.data_type, tint.blend_type = "RGBA", "MULTIPLY"
    tint.inputs[0].default_value = 1.0
    tint.inputs[6].default_value = [min(1.0, c / ALBEDO_MEAN) for c in rgba[:3]] + [1]
    ln(tex["BaseColor"].outputs[0], tint.inputs[7])
    attr = nn("ShaderNodeAttribute")
    attr.attribute_name = "Wear"
    sep = nn("ShaderNodeSeparateColor")
    ln(attr.outputs["Color"], sep.inputs[0])
    edge = nn("ShaderNodeMath")
    edge.operation = "MULTIPLY"
    edge.inputs[1].default_value = float(w.get("edge_wear", 0.0)) * 1.6
    ln(sep.outputs[0], edge.inputs[0])
    lighten = nn("ShaderNodeMix")
    lighten.data_type = "RGBA"
    lighten.inputs[7].default_value = (0.55, 0.55, 0.56, 1) if d["metallic"] < 0.5 and rgba[0] < 0.3 else (1, 1, 1, 1)
    ln(edge.outputs[0], lighten.inputs[0])
    ln(tint.outputs[2], lighten.inputs[6])
    grime = nn("ShaderNodeMix")
    grime.data_type, grime.blend_type = "RGBA", "MULTIPLY"
    gm = nn("ShaderNodeMath")
    gm.operation = "MULTIPLY"
    gm.inputs[1].default_value = 0.35 + float(w.get("scuffs", 0.0))
    ln(sep.outputs[1], gm.inputs[0])
    ln(gm.outputs[0], grime.inputs[0])
    ln(lighten.outputs[2], grime.inputs[6])
    grime.inputs[7].default_value = (0.45, 0.42, 0.38, 1)
    ln(grime.outputs[2], bsdf.inputs["Base Color"])
    msep = nn("ShaderNodeSeparateColor")
    ln(tex["Mask"].outputs[0], msep.inputs[0])
    rough = nn("ShaderNodeMath")
    rough.operation = "SUBTRACT"
    rough.inputs[0].default_value = 1.0
    ln(tex["Mask"].outputs["Alpha"], rough.inputs[1])
    rough2 = nn("ShaderNodeMath")
    rough2.operation = "ADD"
    rough2.use_clamp = True
    ln(rough.outputs[0], rough2.inputs[0])
    ln(edge.outputs[0], rough2.inputs[1])
    ln(rough2.outputs[0], bsdf.inputs["Roughness"])
    ln(msep.outputs[0], bsdf.inputs["Metallic"])
    nm = nn("ShaderNodeNormalMap")
    nm.uv_map = "UVMap_Main"
    ln(tex["Normal"].outputs[0], nm.inputs["Color"])
    ln(nm.outputs[0], bsdf.inputs["Normal"])
    if name == "glass":
        bsdf.inputs["Transmission Weight"].default_value = 1.0
        bsdf.inputs["IOR"].default_value = 1.5
        a = rgba[3] if len(rgba) > 3 else 1.0
        if a < 1:
            bsdf.inputs["Alpha"].default_value = max(a, 0.15)
            mat.surface_render_method = "BLENDED"


def apply_preview_materials(p):
    import bpy
    pref = "M_Proc_"
    for mat in bpy.data.materials:
        key = mat.name[len(pref):] if mat.name.startswith(pref) else None
        if key in p.get("colors", {}):
            preview_material(mat, key, p)


def finishes_entry(p):
    """Manifest block for the Unity material builder: M_Proc name -> finish + cited tint."""
    return {"M_Proc_" + k: {"finish": finish_of(k, p), "tint_rgba": [round(c, 4) for c in v]} for k, v in sorted(p.get("colors", {}).items())}
