"""Fetch third-party assets into the shared cache (DEC-023) and keep the manifest.

Usage:
  python -I Tools/Assets/fetch_assets.py [--list Docs/Assets/fetch_list_p0.json] [--verify]

Sources: polyhaven (API, 2k gltf / hdr), kenney (signed zip link), url (direct files),
local (files placed in the cache by hand, e.g. Sketchfab browser downloads; only hashed).
Entries with "blocked": "<reason>" and no manifest rows are reported and skipped; drop the key once unblocked.
Re-runs skip entries whose manifest rows exist on disk with matching sha256 (no network).
--verify: hash every manifest row and check its ledger ID exists in LICENSE_LEDGER.md.
"""
import argparse, datetime, hashlib, http.cookiejar, json, os, sys, urllib.parse, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = "C:/Users/handl/Downloads/Dispo Game Assets Cache"
MANIFEST = os.path.join(REPO, "Docs/Assets/ASSET_CACHE_MANIFEST.json")
LEDGER = os.path.join(REPO, "Docs/Assets/LICENSE_LEDGER.md")
UA = {"User-Agent": "DispoGame-AssetFetch/1.0"}
OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def get(url, headers=None):
    with OPENER.open(urllib.request.Request(url, headers={**UA, **(headers or {})}), timeout=600) as r:
        return r.read()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest, md5=None):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    data = get(url)
    if md5 and hashlib.md5(data).hexdigest() != md5:
        raise RuntimeError(f"md5 mismatch for {url}")
    with open(dest + ".part", "wb") as f:
        f.write(data)
    os.replace(dest + ".part", dest)


def plan_polyhaven(e):
    """-> [(url, relpath, md5)] for the 2k gltf (models/textures) or 2k hdr (hdri)."""
    files = json.loads(get(f"https://api.polyhaven.com/files/{e['asset']}"))
    res = e.get("res", "2k")
    if "hdri" in files:
        f = files["hdri"][res]["hdr"]
        return [(f["url"], os.path.basename(urllib.parse.urlparse(f["url"]).path), f["md5"])]
    g = files["gltf"][res]["gltf"]
    out = [(g["url"], os.path.basename(urllib.parse.urlparse(g["url"]).path), g["md5"])]
    out += [(v["url"], k, v["md5"]) for k, v in g.get("include", {}).items()]
    return out


def plan_kenney(e):
    page = "https://kenney.nl/assets/" + e["asset"]
    get(page)  # the signed-link endpoint needs this page's session cookie + referer
    link = json.loads(get("https://kenney.nl/download-link/" + ("assets/" + e["asset"]).encode().hex(),
                          {"Referer": page}))["url"]
    return [(link, e["asset"] + ".zip", None)]


def plan(e, folder):
    s = e["source"]
    if s == "polyhaven":
        return plan_polyhaven(e)
    if s == "kenney":
        return plan_kenney(e)
    if s == "url":
        return [(f["url"], f["name"], None) for f in e["files"]]
    if s == "local":  # already placed by hand; record what is there
        return [(None, os.path.relpath(os.path.join(d, n), folder).replace("\\", "/"), None)
                for d, _, ns in os.walk(folder) for n in ns if not n.endswith(".part")]
    raise ValueError(f"unknown source {s}")


def cached_ok(rows):
    return rows and all(os.path.isfile(r["path"]) and os.path.getsize(r["path"]) == r["bytes"]
                        and sha256(r["path"]) == r["sha256"] for r in rows)


def fetch(list_path):
    entries = json.load(open(list_path, encoding="utf-8"))["entries"]
    manifest = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else {"rows": []}
    rows = manifest["rows"]
    today = datetime.date.today().isoformat()
    stats = {"cached": 0, "fetched": 0, "blocked": 0, "failed": 0}
    for e in entries:
        folder = os.path.join(CACHE, e["source_dir"], e["ledger_id"]).replace("\\", "/")
        mine = [r for r in rows if r["ledger_id"] == e["ledger_id"]]
        if e.get("blocked") and not mine:
            stats["blocked"] += 1
            print(f"blocked {e['ledger_id']}: {e['blocked']}")
            continue
        if cached_ok(mine) and e["source"] != "local":
            stats["cached"] += 1
            continue
        try:
            items = plan(e, folder)
            if not items:
                raise RuntimeError("no files (local entry not placed yet?)")
            new = []
            for url, rel, md5 in items:
                dest = os.path.join(folder, rel).replace("\\", "/")
                if url and not os.path.isfile(dest):
                    download(url, dest, md5)
                new.append({"ledger_id": e["ledger_id"], "path": dest,
                            "source_url": url or e["source_url"], "license": e["license"],
                            "redistributable": e["redistributable"], "sha256": sha256(dest),
                            "bytes": os.path.getsize(dest), "date": today})
            old = {r["path"]: r for r in mine}
            unchanged = len(old) == len(new) and all(
                r["path"] in old and old[r["path"]]["sha256"] == r["sha256"] for r in new)
            if unchanged:
                stats["cached"] += 1
                continue
            rows[:] = [r for r in rows if r["ledger_id"] != e["ledger_id"]] + new
            stats["fetched"] += 1
            print(f"fetched {e['ledger_id']}: {len(new)} files")
        except Exception as ex:  # keep going; report at the end
            stats["failed"] += 1
            print(f"FAILED {e['ledger_id']}: {ex}", file=sys.stderr)
    rows.sort(key=lambda r: r["path"])
    manifest.update(cache_root=CACHE, rows=rows)
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")
    print(stats)
    return stats["failed"] == 0


def verify():
    rows = json.load(open(MANIFEST, encoding="utf-8"))["rows"]
    ledger = open(LEDGER, encoding="utf-8").read()
    bad = [r["path"] for r in rows if f"| {r['ledger_id']} |" not in ledger]
    bad += [r["path"] for r in rows if not cached_ok([r])]
    print(f"verify: {len(rows)} rows, {len(bad)} bad")
    for b in bad:
        print("  BAD", b)
    return not bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", default=os.path.join(REPO, "Docs/Assets/fetch_list_p0.json"))
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    sys.exit(0 if (verify() if a.verify else fetch(a.list)) else 1)
