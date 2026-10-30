"""Deli-jar fill levels (PROC-002): seeded low-poly buds piled in the PROC_DeliJar cavity, one mesh per fill step.
Cavity comes from the deli_jar params so fill and jar stay in sync. Buds sit on a grid x grid lattice per layer; a step
holds round(fill * cells) buds filled bottom-up in a seeded cell order, so the top layer is ragged and every lower
step is a subset of the higher ones. Shapes/colours are [GDD] art placeholders, not store facts.
See Docs/Assets/Specs/PROC_PIPELINE.md (PROC-002)."""
import hashlib
import json
import math
import os
import random

import bmesh
from mathutils import Euler, Matrix, Vector

from proclib import finish_object, loft, material, rounded_rect

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
MARGIN = 0.001  # every vertex stays this far inside the glass


def variants(p):
    """One asset (FBX) per visual family; every fill step and LOD lives inside it."""
    for fam in p["families"]:
        yield f"{p['asset_id']}_{fam['id']}", dict(p, family=fam)


def cavity(p):
    with open(os.path.join(ROOT, p["jar_params"])) as f:
        b = json.load(f)["body"]
    t = b["wall_m"]
    return {"half_x": b["width_m"] / 2 - t, "half_y": b["depth_m"] / 2 - t, "corner_r": b["corner_radius_m"] - t,
            "floor": b["floor_m"], "top": b["height_m"]}


def inside(cv, co):
    hx, hy, r = cv["half_x"] - MARGIN, cv["half_y"] - MARGIN, cv["corner_r"] - MARGIN
    dx, dy = max(abs(co.x) - (hx - r), 0.0), max(abs(co.y) - (hy - r), 0.0)
    return abs(co.x) <= hx and abs(co.y) <= hy and dx * dx + dy * dy <= r * r and cv["floor"] + MARGIN <= co.z <= cv["top"] - MARGIN


def seeded(*key):
    return random.Random(int.from_bytes(hashlib.sha256("|".join(map(str, key)).encode()).digest()[:8], "little"))


def blob(bm, rng, cv, center, radius, elong, bump, subdiv, accent_frac):
    """Jittered ellipsoid; faces get material 1 (accent) with probability accent_frac. Nudged inward to fit the cavity."""
    n0 = len(bm.faces)
    rot = Euler((rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.9), rng.uniform(0, math.tau))).to_matrix().to_4x4()
    shape = Matrix.Diagonal((radius, radius, radius * elong, 1.0))
    verts = bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)["verts"]
    for v in verts:
        k = 1 - 0.3 * v.co.z  # taper toward the tip, like a cola
        v.co = rot @ shape @ (Vector((v.co.x * k, v.co.y * k, v.co.z)) * (1 + rng.uniform(-bump, bump)))
    bm.faces.ensure_lookup_table()
    for f in bm.faces[n0:]:
        f.material_index = 1 if rng.random() < accent_frac else 0
    pos = Vector(center)
    pos.z = max(pos.z, cv["floor"] + 2 * MARGIN - min(v.co.z for v in verts))  # rest on the floor
    pos.z = min(pos.z, cv["top"] - 2 * MARGIN - max(v.co.z for v in verts))  # tall looks squeeze under the lid
    for _ in range(60):  # walk toward the axis until the whole blob is inside the glass
        if all(inside(cv, v.co + pos) for v in verts):
            break
        pos.x *= 0.95
        pos.y *= 0.95
    else:
        raise ValueError(f"bud at {tuple(center)} does not fit the jar cavity")
    for v in verts:
        v.co += pos


def plan_buds(p, cv):
    """Every bud of a full jar in fill order: (center, radius, rng seed). Same list for every step and LOD."""
    fam, b = p["family"], p["buds"]
    g, rng = b["grid"], seeded(p["seed"], fam["id"], "plan")
    pitch_x, pitch_y = 2 * cv["half_x"] / g, 2 * cv["half_y"] / g
    r0 = b["radius_m"] * fam["scale"]
    out = []
    for layer in range(b["layers"]):
        cells = [(i, j) for i in range(g) for j in range(g)]
        rng.shuffle(cells)
        for i, j in cells:
            c = (-cv["half_x"] + pitch_x * (i + 0.5) + rng.uniform(-1, 1) * b["jitter_m"],
                 -cv["half_y"] + pitch_y * (j + 0.5) + rng.uniform(-1, 1) * b["jitter_m"],
                 cv["floor"] + r0 * fam["elong"] + layer * b["layer_pitch_m"] * fam["scale"])
            out.append(((layer, i, j), c, r0 * rng.uniform(0.85, 1.1), rng.getrandbits(32)))
    return out


def build(p, lod):
    fam, cv, b = p["family"], cavity(p), p["buds"]
    allbuds = plan_buds(p, cv)
    g = b["grid"]
    mats = (material(f"M_Proc_Bud_{fam['id']}", fam["body"]), material(f"M_Proc_BudAccent_{fam['id']}", fam["accent"]))
    objs = {}
    for pct in p["fill_steps_pct"]:
        n = round(pct / 100 * len(allbuds))
        buds, occupied = allbuds[:n], {k for k, *_ in allbuds[:n]}
        bm = bmesh.new()
        if lod["kind"] == "buds":
            for (layer, i, j), c, r, s in buds:
                # shortcut: only the centre column is hidden (by its 8 neighbours + the bud above); larger grids
                # would hide more cells, cull those too if grid > 3 ever ships.
                if (i, j) == (g // 2, g // 2) and (layer + 1, i, j) in occupied:
                    continue
                blob(bm, seeded(s), cv, c, r, fam["elong"], fam["bump"], lod["subdiv"], fam["accent_frac"])
            if lod.get("shake") and n < g * g:  # loose shake only shows while the bottom layer has gaps
                srng = seeded(p["seed"], fam["id"], "shake")
                sh = p["shake"]
                for _ in range(sh["count"]):
                    c = (srng.uniform(-0.8, 0.8) * cv["half_x"], srng.uniform(-0.8, 0.8) * cv["half_y"], cv["floor"])
                    blob(bm, srng, cv, c, srng.uniform(*sh["radius_m"]), 0.5, 0.3, 1, fam["accent_frac"])
        elif n:  # "block": one rounded column up to the mean bud top, for the far LOD
            top = cv["floor"] + (n / (g * g)) * b["layer_pitch_m"] * fam["scale"] + b["radius_m"] * fam["scale"] * 0.5
            top = min(top, cv["top"] - 2 * MARGIN)
            ring = lambda z: [(x, y, z) for x, y in rounded_rect(2 * cv["half_x"], 2 * cv["half_y"], cv["corner_r"], 1, 0.003)]
            loft(bm, [ring(cv["floor"] + 2 * MARGIN), ring(top)])
        if not bm.faces:
            bm.free()
            continue
        part = f"F{pct:03d}"
        obj = finish_object(bm, part)
        for m in mats:
            obj.data.materials.append(m)
        tris = sum(len(poly.vertices) - 2 for poly in obj.data.polygons)
        if tris > lod["step_tri_budget"]:
            raise ValueError(f"{fam['id']} {part}: {tris} tris > step budget {lod['step_tri_budget']}")
        bad = [v.co for v in obj.data.vertices if not inside(cv, v.co)]
        if bad:
            raise ValueError(f"{fam['id']} {part}: {len(bad)} vertices outside the jar cavity, e.g. {tuple(bad[0])}")
        objs[part] = obj
    xs, ys, zs = zip(*(v.co for o in objs.values() for v in o.data.vertices))
    expected = (max(xs) - min(xs), max(zs) - min(zs), max(ys) - min(ys))  # containment is the real check, above
    extra = {"family": fam["id"], "fill_steps_pct": p["fill_steps_pct"], "interior": cv,
             "preview_groups": [f"F{pct:03d}" for pct in p["fill_steps_pct"]]}
    return objs, expected, extra


def preview_context(p):
    """Jar glass, lid and band around the fill in the preview renders only (never exported)."""
    from generators import deli_jar
    with open(os.path.join(ROOT, p["jar_params"])) as f:
        jp = json.load(f)
    objs, _, _ = deli_jar.build(jp, next(iter(jp["lods"].values())))
    import bpy
    for part in ("Label", "ThcTag"):  # keep the fill readable; band, lid and glass stay
        if part in objs:
            bpy.data.objects.remove(objs.pop(part))
    for part, o in objs.items():
        o.name = "Context_" + part
