"""Seeded customer roster for the MPFB2 pipeline (ASSET-004, DEC-075). Pure Python, no bpy.

Usage: python -I Tools/Blender/characters/roster.py [params.json] [--out Docs/Assets/Specs/customer_roster_mpfb.json]
Same seed -> same roster. Exits non-zero if Rule D, a quota, or the licence index check fails (the self-check).

Rule D (CHARACTERS.md section 3.3, register distance): every pair of customers differs in >= 3 register cues, at least one of
them a shape cue. Register cues = what shows across the counter: sex, age band, skin, head (hair or hat), top outfit,
glasses, beard, build. Shape cues = head, outfit, glasses, beard, build."""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
PARAMS = os.path.join(REPO, "Tools/Blender/params/customers_mpfb.json")
OUT = os.path.join(REPO, "Docs/Assets/Specs/customer_roster_mpfb.json")
INDEX = "C:/Users/handl/Downloads/Dispo Game Assets Cache/mpfb/blender_user/extensions/.user/user_default/mpfb/data/dispo_licence_index.json"
TARGETS = "C:/Users/handl/Downloads/Dispo Game Assets Cache/mpfb/blender_user/extensions/user_default/mpfb/data/targets/target.json"
SHAPE = ("head", "outfit", "glasses", "beard", "build")
CUES = ("sex", "age_band", "skin") + SHAPE


def cues(c):
    return {"sex": c["sex"], "age_band": c["age_band"], "skin": c["skin"], "head": c["hat"] or c["hair"],
            "outfit": c["outfit"], "glasses": bool(c["glasses"]), "beard": bool(c["beard"]), "build": c["build"]}


def distinct(a, b):
    ca, cb = cues(a), cues(b)
    diff = [k for k in CUES if ca[k] != cb[k]]
    return len(diff) >= 3 and any(k in SHAPE for k in diff)


def _quota(n, shares):
    """Largest-remainder split of n over {key: share}."""
    raw = {k: n * s for k, s in shares.items()}
    out = {k: int(v) for k, v in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - out[k], reverse=True)[: n - sum(out.values())]:
        out[k] += 1
    return out


def face(rng, p):
    """Seeded face: per category, pick target pairs and a signed amount (both sides for l/r targets)."""
    tgt = json.load(open(TARGETS))
    out = []
    for cat in p["face_categories"]:
        for c in rng.sample(tgt[cat]["categories"], min(p["face_targets_per_category"], len(tgt[cat]["categories"]))):
            v = rng.uniform(-p["face_amplitude"], p["face_amplitude"])
            o = c.get("opposites")
            if not o:  # single-direction category: one target, positive amount only
                out.append({"target": rng.choice(c["targets"]), "value": round(abs(v), 3)})
                continue
            sign = "positive" if v > 0 else "negative"
            names = [o[f"{sign}-left"], o[f"{sign}-right"]] if c["has_left_and_right"] else [o[f"{sign}-unsided"]]
            out += [{"target": n, "value": round(abs(v), 3)} for n in names if n]
    return out


def generate(p):
    rng = random.Random(p["seed"])
    n = p["roster_size"]
    sexes = ["f", "m"] * (n // 2) + ["f"] * (n % 2)
    bands = [b for b, k in _quota(n, {b: v["share"] for b, v in p["age_bands"].items()}).items() for _ in range(k)]
    rng.shuffle(bands)
    formal_left = int(n * p["formal_max_share"])
    roster, tries = [], 0
    while len(roster) < n:
        tries += 1
        if tries > 20000:
            raise RuntimeError(f"Rule D: could only place {len(roster)} of {n}")
        i = len(roster)
        sex, band = sexes[i], bands[i]
        skins = [s for s in p["skins"] if s["sex"] == sex and band in s["bands"]]
        used = {a: sum(c["ancestry"] == a for c in roster) for a in {s["ancestry"] for s in skins}}
        least = min(used.values())  # balance ancestries over the roster, within what this sex/age band has skins for
        skin = rng.choice([s for s in skins if used[s["ancestry"]] == least])
        dark = skin["ancestry"] != "caucasian"
        outfits = [o for o in p["outfits"][sex] if formal_left > 0 or not o.get("formal")]
        outfit = rng.choice(outfits)
        hat = rng.choice(p["hats"]) if rng.random() < p["hat_share"] else None
        hair = rng.choice(p["hair"][sex])
        tint = ("grey" if rng.random() < 0.5 else "white") if band == "older" else (
            rng.choice(["black", "dark_brown"]) if dark and rng.random() < 0.85 else rng.choice(p["hair_tints"][:5]))
        build = rng.choice(sorted(p["builds"]))
        c = {
            "id": f"C{i + 1:03d}", "sex": sex, "age_band": band, "skin": skin["id"], "ancestry": skin["ancestry"],
            "hair": hair, "hair_tint": tint, "hat": hat, "outfit": outfit["id"], "items": outfit["items"],
            "glasses": rng.choice(p["glasses"]) if rng.random() < p["glasses_share"] else None,
            "beard": rng.choice(p["beards"]) if sex == "m" and band != "young" and rng.random() < p["beard_share_m"] / 0.75 else None,
            "eyes": rng.choice(["brown", "brownlight"]) if dark and rng.random() < 0.85 else rng.choice(p["eyes"]),
            "build": build,
            "phenotype": {
                "gender": 0.0 if sex == "f" else 1.0,
                "age": round(rng.uniform(*p["age_bands"][band]["mpfb_age"]), 3),
                "weight": round(rng.uniform(*p["builds"][build]["weight"]), 3),
                "muscle": round(rng.uniform(*p["builds"][build]["muscle"]), 3),
                "height": round(rng.uniform(*p["height"][sex]), 3),
                "proportions": round(rng.uniform(*p["proportions"]), 3),
                "cupsize": round(rng.uniform(0.35, 0.65), 3), "firmness": round(rng.uniform(0.35, 0.65), 3),
                "race": p["ancestry_race"][skin["ancestry"]],
            },
        }
        if all(distinct(c, o) for o in roster):
            c["face_targets"] = face(rng, p)
            formal_left -= bool(outfit.get("formal"))
            roster.append(c)
    return roster


def assets_of(c):
    """Asset unit dirs (as in the licence index) this customer uses."""
    a = [f"skins/{c['skin']}", "eyes/materials", "eyebrows/eyebrow001", "eyelashes/eyelashes01", "eyes/high-poly"]
    a += [f"clothes/{i}" for i in c["items"]]
    a += [f"hair/{c['hair']}"] if c["hair"] else []
    a += [f"clothes/{x}" for x in (c["hat"], c["glasses"], c["beard"]) if x]
    return a


def check(p, roster):
    errors = []
    index = json.load(open(INDEX))
    for c in roster:
        for a in assets_of(c):
            if not index.get(a, {}).get("allowed"):
                errors.append(f"{c['id']}: {a} not CC0-allowed ({index.get(a, {}).get('reasons', 'missing from index')})")
    for i, a in enumerate(roster):
        for b in roster[i + 1:]:
            if not distinct(a, b):
                errors.append(f"Rule D: {a['id']} vs {b['id']}")
    n = len(roster)
    if sum(c["sex"] == "f" for c in roster) != (n + 1) // 2:
        errors.append("sex quota")
    formal = {o["id"] for s in p["outfits"].values() for o in s if o.get("formal")}
    if sum(c["outfit"] in formal for c in roster) > n * p["formal_max_share"]:
        errors.append("formal quota")
    if len({json.dumps(c["face_targets"]) for c in roster}) != n:
        errors.append("duplicate faces")
    return errors


def main(argv):
    params = argv[0] if argv and not argv[0].startswith("--") else PARAMS
    out = argv[argv.index("--out") + 1] if "--out" in argv else OUT
    p = json.load(open(params))
    roster = generate(p)
    errors = check(p, roster)
    if roster != generate(p):
        errors.append("not deterministic")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"seed": p["seed"], "params": os.path.relpath(params, REPO).replace("\\", "/"), "rule": "D (>=3 register cues, >=1 shape)",
                   "customers": roster}, f, indent=1)
        f.write("\n")
    print(f"roster: {len(roster)} customers -> {out}; {len(errors)} errors")
    for e in errors:
        print("  ", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
