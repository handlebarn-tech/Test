"""Install MPFB2 asset packs from the shared cache into the isolated MPFB profile and write the licence index (ASSET-004).

Usage: python -I Tools/Blender/characters/install_mpfb.py
Reads every Docs/Assets/fetch_list_mpfb.json pack zip, extracts it into
  <cache>/mpfb/blender_user/extensions/.user/user_default/mpfb/data   (MPFB's user data dir under BLENDER_USER_RESOURCES)
and writes <that data dir>/dispo_licence_index.json: asset dir -> {pack, licence, author, allowed, reasons}.
An asset is allowed only when its pack JSON says "CC0" AND none of its own files carries a different licence header
(several "_cc0" skin packs contain files headed "This file is licensed AGPLv3"). The generator refuses anything not allowed.
The MPFB add-on itself is installed by Blender (see Docs/Assets/Specs/CHARACTERS.md section 10)."""
import json
import os
import re
import sys
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CACHE = "C:/Users/handl/Downloads/Dispo Game Assets Cache"
DATA = os.path.join(CACHE, "mpfb/blender_user/extensions/.user/user_default/mpfb/data")
INDEX = os.path.join(DATA, "dispo_licence_index.json")
CC0_HEADER = re.compile(rb"released as CC0|licensed (?:under )?CC0|CC0 1\.0", re.I)
TEXT_EXT = (".mhclo", ".mhmat", ".proxy", ".mhpxy", ".obj", ".mhm", ".txt", ".md")
BAD_HEADER = re.compile(rb"licen[sc]ed\s+(?:under\s+)?(AGPL|GPL|CC[- ]?BY)", re.I)


def install():
    entries = json.load(open(os.path.join(REPO, "Docs/Assets/fetch_list_mpfb.json"), encoding="utf-8"))["entries"]
    root = os.path.realpath(DATA)
    index = {}
    for e in entries:
        if not e["ledger_id"].startswith("MPFB-"):
            continue
        zpath = os.path.join(CACHE, e["source_dir"], e["ledger_id"], e["files"][0]["name"])
        with zipfile.ZipFile(zpath) as z:
            for m in z.infolist():
                if not os.path.realpath(os.path.join(root, m.filename)).startswith(root):
                    raise RuntimeError(f"zip-slip entry {m.filename} in {zpath}")
            z.extractall(root)
            packs = [n for n in z.namelist() if n.startswith("packs/") and n.endswith(".json")]
            meta = {}
            for p in packs:
                meta.update(json.loads(z.read(p)))
            # unit = <type>/<name> (its top-level files) or <type>/<name>/<sub> (an alternative material); a pack JSON keys
            # assets by <name>. Licence evidence: the pack JSON entry, else a file header saying "released as CC0".
            names = [n for n in z.namelist() if n.count("/") >= 2 and not n.startswith("packs/") and not n.endswith("/")]
            units = {}
            for n in names:
                parts = n.split("/")
                units.setdefault("/".join(parts[:3]) if len(parts) > 3 else "/".join(parts[:2]), []).append(n)
            for u, files in sorted(units.items()):
                m = meta.get(u.split("/")[1], {})
                text = [z.read(n)[:4000] for n in files if n.endswith(TEXT_EXT)]
                cc0_header = any(CC0_HEADER.search(b) for b in text)
                reasons = [f"header in {u}: {h.group(0).decode(errors='replace')}" for h in (BAD_HEADER.search(b) for b in text) if h]
                lic = m.get("license") or ("CC0 (file header)" if cc0_header else None)
                if not lic or not lic.startswith("CC0"):
                    reasons.append(f"no CC0 evidence (pack licence {m.get('license')!r})")
                index[u] = {"pack": e["ledger_id"], "licence": lic, "author": m.get("author"), "allowed": not reasons, "reasons": reasons}
    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, indent=1, sort_keys=True)
        f.write("\n")
    bad = {k: v["reasons"] for k, v in index.items() if not v["allowed"]}
    print(f"installed {len(entries) - 1} packs into {DATA}; {len(index)} assets, {len(bad)} refused")
    for k, v in sorted(bad.items()):
        print("  REFUSED", k, "; ".join(v))
    return index


if __name__ == "__main__":
    install()
    sys.exit(0)
