# BUILD-002 — Studio tooling hardening + build manifest

**Role:** BUILD · **Priority:** P1 · **Branch:** `task/BUILD-002` worktree off `main`

## Goal
Close the tooling notes from the wave reviews and give every build a manifest, so a growing number of parallel sessions can rely on `studio.ps1`.

## Read
`Docs/TOOLCHAIN_EXECUTION.md` §8 (result schema) and §14 (build manifest); `Docs/Handoffs/BUILD-001.md`; `Docs/Reviews/REVIEW-W1.md` m6/m7; `Docs/Reviews/REVIEW-W2C.md` m4, n2; `Docs/Handoffs/PROC-001.md` (blender wiring); DEC-013, DEC-023.

## Owns
`Tools/Studio/` (except files ART-002 is editing: coordinate by only touching the dispatch/config/gate code, not `graybox_qa.py`), `.gitattributes`/`.gitignore` build-related lines, `Docs/BUILD_STATUS.md`.

## Deliverable
1. `doctor`: if `studio.config.json` is missing, copy the example automatically (or fail with a one-line hint), no stack trace (W1 m6).
2. `Wait-UnitySlot`: add a timeout (default 45 min, configurable) and a lock file so check-then-launch can't race (W2C m4). Exclude the Hub's `unity.exe serve` helper as ART-001 already does for import workers.
3. `studio.ps1 blender <generator> <params>` forwards to `Tools/Blender/blender.ps1`; `studio.ps1 assets-fetch` forwards to `Tools/Assets/fetch_assets.py` if present.
4. Result JSON per §8 for every command; build manifest per §14 (commit, Unity version, scenes, catalog manifest md5, asset cache manifest md5, timestamp) written next to each build.
5. Git LFS: run `git lfs install --local` in doctor if missing; verify the DEC-023 patterns are tracked.
6. `unity-build` re-run and confirm the player is fine with the emptied `m_RuntimeSettings` (W2C n2).

## Validation
All existing commands still pass; new commands demonstrated; one full `unity-build` with manifest. DEC-013 gate.

## Handoff
`Docs/Handoffs/BUILD-002.md` (≤40 lines). Report to the Studio Hub.
