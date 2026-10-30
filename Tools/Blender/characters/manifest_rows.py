"""Write one MPFB-DERIVED-<id> row per validated customer FBX into ASSET_CACHE_MANIFEST.json (ASSET-004). Pure Python, no bpy.

Usage: python -I Tools/Blender/characters/manifest_rows.py
Replaces earlier MPFB-DERIVED-* rows, leaves every other row untouched. Customers whose validation has errors get no row.
Fails if an FBX's sha256 differs from its validation JSON."""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
MANIFEST = os.path.join(REPO, "Docs/Assets/ASSET_CACHE_MANIFEST.json")
DERIVED = "C:/Users/handl/Downloads/Dispo Game Assets Cache/mpfb/derived"


def main():
    man = json.load(open(MANIFEST, encoding="utf-8"))
    rows = [r for r in man["rows"] if not r["ledger_id"].startswith("MPFB-DERIVED-")]
    n = 0
    for cid in sorted(os.listdir(DERIVED)):
        v = os.path.join(DERIVED, cid, cid + ".validation.json")
        if not os.path.isfile(v):
            continue
        rep = json.load(open(v, encoding="utf-8"))
        if rep["errors"]:
            continue
        fbx = os.path.join(DERIVED, cid, cid + ".fbx")
        sha = hashlib.sha256(open(fbx, "rb").read()).hexdigest()
        if sha != rep["fbx"]["sha256"]:
            raise SystemExit(f"{cid}: FBX sha256 differs from its validation JSON (re-export it)")
        rows.append({"ledger_id": f"MPFB-DERIVED-{cid}", "path": fbx.replace("\\", "/"),
                     "source_url": f"derived: Tools/Blender/characters/customer_gen.py (ASSET-004); inputs per {cid}.validation.json licence_audit",
                     "license": "CC0-1.0 (built only from CC0-allowed MPFB units; our own output)", "redistributable": True,
                     "sha256": sha, "bytes": os.path.getsize(fbx), "date": rep.get("date", "2026-10-30")})
        n += 1
    man["rows"] = rows
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
    print(f"{n} MPFB-DERIVED rows -> {MANIFEST}")


if __name__ == "__main__":
    main()
