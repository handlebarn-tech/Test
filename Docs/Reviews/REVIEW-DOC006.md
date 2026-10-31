# REVIEW-DOC006

**Reviewed:** `claude/brave-boyd-7af7b5` @ 078990a. **Merge base with `main` 29da42f:** 29da42f (check 0 passes: `git merge-base --is-ancestor 29da42f claude/brave-boyd-7af7b5` is true). `main` has since moved to 30bc0bf; not relevant to this diff.
**Sources read:** `CLAUDE.md` (reviewer role), packet `Docs/Tasks/Active/DOC-006.md`, `Docs/Handoffs/DOC-006.md` (Validation, Not done, For the Hub), `Docs/Reviews/REVIEW-ART008.md` m1, `git diff 29da42f...claude/brave-boyd-7af7b5` (4 files: `Tools/Studio/studio.ps1`, `Docs/BACKLOG.md`, packet, handoff).

## Verdict: PASS with minors

## Checks
Run in this fresh worktree (304 LFS files all pointers at start; `studio.config.json` copied from the example, gitignored).

| # | Acceptance | Result |
|---|---|---|
| 1 | Pointer worktree: `doctor` reports `lfsCheckedOut False`, names a sample file and `git lfs pull`, exits non-zero | PASS. Output `165 LFS pointer files under UnityProject/Assets (e.g. …/PROC_DeliJar.fbx); run 'git lfs pull'`, `lfsCheckedOut False`, `summary: failed: lfsCheckedOut`, process exit 1. Other checks still printed. |
| 2 | Pointer worktree: `unity-compile` exits 2 `blocked` before launching Unity | PASS. status `blocked`, summary `blocked: 165 Git LFS pointer files under UnityProject/Assets (e.g. …); run 'git lfs pull' first`, process exit 2. The Unity processes before and after were the same two (PIDs 29416 and 14696, other sessions'), and `UnityProject/Library` was not created, so no editor was launched. The guard runs first in `Assert-UnityReady`, which every unity-* command calls (compile, test-edit/play, graybox, capture, build). |
| 3 | After `git lfs pull`: `doctor` `lfsCheckedOut True`, all checks pass; a single pulled file drops out of the count | PASS for the first half: all 304 files `*`, `doctor` all checks true, exit 0. The single-file drop-out I did not re-run; it relies on `git lfs ls-files` `-`/`*` markers, which I confirmed are what the regex keys on (before: 304 `-`; after: 304 `*`). The worker's 51 to 50 run is credited. |
| 4 | Windows PowerShell 5.1 correctness | PASS. No `&&`, `||`, ternary or `??` in the added code (the grep hits are none in `studio.ps1`). Uses `if`/`-and` style, `@(...)` array wrapping so `.Count` is safe for 0 or 1 result, `$ErrorActionPreference = 'Continue'` scoped to the function so git's stderr cannot throw (`doctor` re-sets `Stop` afterwards). Ran under `powershell -NoProfile` 5.1 in this review. |
| 5 | Wire-shelving / register-kit `.meta` claim | PARTLY STALE. See m1. Register-kit part holds: `git ls-files` has the 16 `PROC_RK_*.fbx` under `Props/RegisterKit/` and no `.meta` for them or the folder, on `main` or the branch; `RK_` metas exist only in other worktrees with differing GUIDs per the handoff, so nothing canonical to commit. Wire-shelving part: the 8 FBX, 8 `.fbx.meta` and `WireShelving.meta` ARE tracked on 29da42f (landed with PROC-005 in 398e5ef, which is not in the worker's base 3adc4d1). The handoff's "no `.meta` for the 8 WireShelving" was true at its base only. Outcome is still correct: nothing to commit for them. |
| 6 | BACKLOG | PASS. One DOC-006 row (line 155); no DOC-005 LFS row remains (the one `^| DOC-005` row on 29da42f is the one renamed); no other DOC-005 row exists in the file. Only the ID, status text and "owner" parenthetical changed. |
| 7 | Scope | PASS. Changed only `studio.ps1`, the BACKLOG row, packet, handoff. Truth files untouched. No Unity launched by the worker (handoff says none; consistent). |

## MAJOR
None.

## minor
- **m1 (docs, Hub).** The handoff's `.meta` finding is out of date against 29da42f: WireShelving metas are already tracked, only the register-kit metas are outstanding. The BACKLOG row text ("PROC wire-shelving and register-kit `.meta` files") and the handoff's "close REVIEW-ART7 m4" advice should name register kit only, owned by whichever task first references those FBX from a scene/prefab (stable GUIDs). Hub-owned wording; no code change.
- **m2 (tooling).** `lfsCheckedOut` counts every pointer under `UnityProject/Assets` (165 now, 51 at the worker's base), so a worktree needing only one asset still has to pull everything. That is the right trade for the guard's purpose; noting that `git lfs pull --include` of the whole `UnityProject/Assets` tree is the minimal fix if someone wants a smaller pull. The message says plain `git lfs pull`, which is correct and sufficient.
- **m3 (docs, Hub).** The fresh-worktree setup note ("add `git lfs pull`") is still outside any Owns and not yet in the packet templates / STUDIO_OS; the worker proposed it under `## For the Hub`. Carry it.
- **m4 (nit).** The packet says "BACKLOG row 153"; the row is now at line 155. Packet is a closed document; ignore.

## Not covered
No full `unity-*` command was run after the pull (per the review brief; the guard path is shared with `doctor`). `perf`, `slots`, `blender`, `assets-fetch` are outside the guard by design and not tested.
