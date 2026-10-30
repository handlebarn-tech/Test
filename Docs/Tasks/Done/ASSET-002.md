# ASSET-002 — Fetch P0 third-party assets into the shared cache (+ LFS setup)

**Role:** ART-SOURCING · **Priority:** P1 · **Branch:** `task/ASSET-002` worktree off `claude/task-asset-001-9856c0` (ASSET-001 under review; rebase onto main after REVIEW-W2B merges)

## Goal
Every P0 asset in `Docs/Assets/ACQUISITION_LIST.md` downloaded once into the shared cache with verified license provenance, reproducibly where the source has an API, per DEC-023.

## Read
DEC-023, DEC-025; `Docs/Assets/ACQUISITION_LIST.md`, `Docs/Assets/LICENSE_LEDGER.md`, `Docs/Handoffs/ASSET-001.md`.

## Owns
- Cache: `C:/Users/handl/Downloads/Dispo Game Assets Cache/` (create).
- `Tools/Assets/fetch_assets.py` (or .js): reads a fetch list, downloads API-accessible sources (Poly Haven API, Kenney, Google Fonts/OFL, ambientCG, BigSoundBank), verifies sha256, writes the manifest. Re-runs skip already-cached files.
- `Docs/Assets/fetch_list_p0.json`, `Docs/Assets/ASSET_CACHE_MANIFEST.json`.
- `.gitattributes` LFS patterns from DEC-023 (add `git lfs install --local` in the worktree; don't commit binaries in this task).
- `Docs/Handoffs/ASSET-002.md`.

## Deliverable
1. Fetch all P0 rows. Poly Haven: pick 2k texture resolution and 2k HDRIs unless the row says otherwise; models as glTF/FBX.
2. **Sketchfab rows:** the user is signed in to Sketchfab in the Claude desktop app's built-in browser pane (tools `mcp__Claude_Browser__*`). Use it to download each P0 Sketchfab model (glTF preferred), then move the files into the cache. Before saving, do the visual provenance check (no brand marks) the ledger asks for. Authorized by Nolan (DEC-025); no extra permission is needed.
3. **Unity Warehouse / UnityJapanOffice:** both are claimed on the user's Unity account. Find a headless path (Unity Package Manager "My Assets" cache under `%APPDATA%/Unity/Asset Store-5.x/` after a download via the editor, or the Asset Store download link in the browser pane). If it needs an interactive editor sign-in you can't do, record it as a blocker with the exact step; don't stall on it.
4. Door chime: if no good CC0 chime exists, synthesize a 2-note chime with Python (numpy/wave) and record it as a project-original asset.
5. Manifest row per file: source URL, ledger ID, license, sha256, bytes, date, redistributable (y/n).

## Validation
`fetch_assets.py` re-run is a no-op (all cached, hashes match). Every manifest row maps to a ledger row. No binaries committed.

## Handoff
`Docs/Handoffs/ASSET-002.md` (≤40 lines): fetched, skipped (why), blockers. Report to the Studio Hub.
