"""ART-003 lookdev textures: import cache files (DEC-023) and generate the procedural TI finish maps.

Usage:
  python Tools/Assets/lookdev_textures.py   (no -I: Pillow/numpy live in the user site-packages)

1. IMPORTS: each cache file is sha256-checked against Docs/Assets/ASSET_CACHE_MANIFEST.json, then copied to
   UnityProject/Assets/_Game/Art/ThirdParty/<dest> when its row is redistributable (Git LFS), otherwise to the
   gitignored UnityProject/Assets/_LocalThirdParty/<dest>.
2. GENERATED: original, seeded (byte-identical on re-run) maps for finishes no cached asset matches:
   TL-1 Statuario-look 12x24 (2 tiles per 24" square), TL-2 8x8 patterned cement tile (2x2 tiles per 16" square),
   QZ-2 white quartz (1 m square). All are tileable; colours are reads of the TI schedule, not product scans.
"""
import hashlib, json, os, shutil, sys

import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(REPO, "Docs/Assets/ASSET_CACHE_MANIFEST.json")
ASSETS = os.path.join(REPO, "UnityProject/Assets")
OUT = os.path.join(ASSETS, "_Game/Art/Lookdev/Textures")
CACHE = "C:/Users/handl/Downloads/Dispo Game Assets Cache"

# cache path (relative to the cache root) -> destination under ThirdParty/ or _LocalThirdParty/
IMPORTS = {
    "polyhaven/PH-oak_veneer_05/textures/oak_veneer_05_diff_2k.jpg": "PolyHaven/oak_veneer_05/oak_veneer_05_diff_2k.jpg",
    "polyhaven/PH-oak_veneer_05/textures/oak_veneer_05_nor_gl_2k.jpg": "PolyHaven/oak_veneer_05/oak_veneer_05_nor_gl_2k.jpg",
}


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def cached(rel):
    """Manifest row of a cache file, after checking its sha256."""
    src = f"{CACHE}/{rel}"
    row = next((r for r in json.load(open(MANIFEST, encoding="utf-8"))["rows"] if r["path"] == src), None) or sys.exit(f"not in manifest: {src}")
    if sha256(src) != row["sha256"]:
        sys.exit(f"sha256 mismatch (cache file changed): {src}")
    return row


def import_cache():
    for src_rel, dest_rel in IMPORTS.items():
        src = f"{CACHE}/{src_rel}"
        row = cached(src_rel)
        root = "_Game/Art/ThirdParty" if row["redistributable"] else "_LocalThirdParty"
        dest = os.path.join(ASSETS, root, dest_rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if not os.path.exists(dest) or sha256(dest) != row["sha256"]:
            shutil.copyfile(src, dest)
        print(f"import {row['ledger_id']} {row['license']} -> {root}/{dest_rel}")


def periodic_noise(n, rng, octaves=5, base=2):
    """Sum of random integer-frequency sinusoids: tiles seamlessly over an n x n image."""
    y, x = np.mgrid[0:n, 0:n] / n * 2 * np.pi
    out = np.zeros((n, n))
    for o in range(octaves):
        f = base * 2 ** o
        for _ in range(4):
            fx, fy = rng.integers(-f, f + 1, 2)
            out += np.sin(fx * x + fy * y + rng.uniform(0, 2 * np.pi)) / 2 ** o
    return (out - out.min()) / (out.max() - out.min())


def veins(n, rng, freq, sharp, warp):
    y, x = np.mgrid[0:n, 0:n] / n * 2 * np.pi
    w = periodic_noise(n, rng)
    v = np.abs(np.sin(freq * (x + 0.6 * y) + warp * w * 2 * np.pi))  # integer freq keeps it tileable
    return (1 - v) ** sharp


def save(name, rgb):
    os.makedirs(OUT, exist_ok=True)
    Image.fromarray(np.clip(rgb * 255 + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(OUT, name), optimize=False)
    print(f"generated _Game/Art/Lookdev/Textures/{name}")


def tl1(n=1024):
    """TL-1 Statuario Bianco look, 12x24: two stacked tiles per 24" square, 1/16" light-grey grout."""
    rng = np.random.default_rng(101)
    v = np.clip(veins(n, rng, 3, 14, 1.2) * 0.8 + veins(n, rng, 7, 30, 0.8) * 0.15, 0, 1)
    cloud = periodic_noise(n, rng, octaves=6, base=3)
    lum = 0.92 + 0.04 * cloud - 0.45 * v
    rgb = np.stack([lum, lum, lum * 1.01], -1)
    g = 3
    grout = np.zeros((n, n), bool)
    grout[:, :g // 2 + 1] = grout[:, -(g // 2):] = True
    for r in (0, n // 2):
        grout[max(r - g // 2, 0):r + g // 2 + 1, :] = True
    grout[-(g // 2):, :] = True
    rgb[grout] = (0.74, 0.74, 0.73)
    save("TL1_marble_12x24.png", rgb)


def tl2(n=1024):
    """TL-2 8x8 patterned cement tile, 2x2 tiles per 16" square, dark-grey grout. Original motif: a quatrefoil of
    quarter circles; charcoal on warm white (TI gives the pattern name only; photos show blue, brown and black variants)."""
    rng = np.random.default_rng(202)
    t = n // 2
    y, x = (np.mgrid[0:t, 0:t] + 0.5) / t
    ink = np.zeros((t, t), bool)
    for cx, cy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        d = np.hypot(x - cx, y - cy)
        ink |= (d > 0.36) & (d < 0.46)
    d = np.hypot(x - 0.5, y - 0.5)
    ink |= d < 0.14
    ink |= (np.abs(x - 0.5) + np.abs(y - 0.5) > 0.30) & (np.abs(x - 0.5) + np.abs(y - 0.5) < 0.34)
    tile = np.where(ink[..., None], (0.10, 0.10, 0.11), (0.90, 0.88, 0.84))
    rgb = np.tile(tile, (2, 2, 1))
    rgb *= (0.94 + 0.06 * periodic_noise(n, rng))[..., None]  # cement mottling
    g = 4
    for r in (0, t):
        rgb[max(r - g // 2, 0):r + g // 2, :] = rgb[:, max(r - g // 2, 0):r + g // 2] = (0.22, 0.22, 0.23)
    rgb[-(g // 2):, :] = rgb[:, -(g // 2):] = (0.22, 0.22, 0.23)
    save("TL2_pattern_8x8.png", rgb)


def qz2(n=1024):
    """QZ-2 white quartz: near-white with fine speckle and faint soft veins."""
    rng = np.random.default_rng(303)
    v = veins(n, rng, 2, 20, 1.5)
    speck = rng.random((n, n)) > 0.985
    lum = 0.95 - 0.12 * v - 0.08 * speck + 0.02 * periodic_noise(n, rng)
    save("QZ2_quartz.png", np.stack([lum, lum, lum * 0.995], -1))


def neon(text="Fine Cannabis", w=2048, h=512):
    """White neon lettering (photo 05) as an RGBA emission mask: tube core + soft glow.
    shortcut: Barlow Light (cached, OFL) stands in for the real sign's lettering; swap when the sign is measured or the
    brand fonts (Montserrat / Crimson Pro) are in the cache."""
    from PIL import ImageDraw, ImageFilter, ImageFont
    rel = "fonts/FNT-BAR/Barlow-Light.ttf"
    cached(rel)
    font = ImageFont.truetype(f"{CACHE}/{rel}", 300)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((w // 2, h // 2), text, font=font, fill=255, anchor="mm")
    glow = mask.filter(ImageFilter.GaussianBlur(18))
    a = np.maximum(np.asarray(mask) / 255.0, np.asarray(glow) / 255.0 * 0.6)
    rgba = np.dstack([np.ones((h, w, 3)), a])
    os.makedirs(OUT, exist_ok=True)
    Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), "RGBA").save(os.path.join(OUT, "Neon_FineCannabis.png"))
    print("generated _Game/Art/Lookdev/Textures/Neon_FineCannabis.png")


def teal_leaf(n=1024):
    """Jar-wall back panel (DEC-043 photo): teal with a darker curved-leaf line pattern. Original motif, 2 ft square."""
    rng = np.random.default_rng(404)
    y, x = np.mgrid[0:n, 0:n] / n * 2 * np.pi
    w = periodic_noise(n, rng, octaves=3, base=1)
    # long sweeping arcs: level lines of a tileable warped field, thin dark strokes
    f = np.sin(3 * x + 2 * np.sin(2 * y + 3 * w)) + 0.6 * np.sin(2 * y - x)
    line = np.exp(-(np.abs(np.sin(f * 2.2)) / 0.06) ** 2)
    base = np.array((0.16, 0.46, 0.43))
    rgb = base * (1 - 0.45 * line[..., None]) * (0.96 + 0.04 * w[..., None])
    save("JarWall_teal_leaf.png", rgb)


if __name__ == "__main__":
    import_cache()
    tl1()
    tl2()
    qz2()
    neon()
    teal_leaf()
