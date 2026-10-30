# REVIEW-W5C — OPS-001 (studio.ps1 run time limit) + REF-010 (restroom cabinet)

Branch `review/wave-5c` (off `main` 16743c4) merges `claude/task-ops-001` @ 08e017c and `claude/task-ref-010` @ 1c3a9d8; both merged cleanly. Reviewer: UX-002 workcell session, 2026-10-30.

## 1. OPS-001 — **PASS (GO)**
**Code.** `Invoke-Unity` now calls `Wait-UnityExit $p $limitMin` (`unityRunTimeoutMinutes`, default 30, also when the local `studio.config.json` lacks the key). On overrun it runs `taskkill /PID <this run's editor PID> /T /F`, waits up to 30 s, logs `OPS-001: … killed editor <pid> …`, and calls `Complete $false -1 "failed: Unity run exceeded unityRunTimeoutMinutes=<n> and was killed (OPS-001)"`. That writes the normal result JSON (status fail, exit 1) and releases the slot via `Exit-UnitySlot`.
- **Only its own tree:**
  - The PID is the `Start-Process` handle of the editor this invocation launched.
  - `/T` follows parent-PID descendants only. Other worktrees' editors are children of their own `studio.ps1` shells, never of this editor, so they can't be reached.
  - The kill only fires while `WaitForExit` reports the process still running, so a recycled PID can't be hit.
- **Limit length:** 30 min is about 2× the longest legitimate run the handoff measured (≈16 min capture/PlayMode; GAME-010's 517–970 s EditMode). The one test it would cut is GAME-010's TEMP `Explore_TuningGrid` (`Timeout(3000000)` = 50 min), and that test is the slot-hog the handoff recommends making `[Explicit]`.

**Validation run here**
- `studio_runlimit_test.ps1` → **ALL PASS** (5/5: a fast run is left alone; an overrunning parent and its helper child are both killed).
- **Real run** through the patched `studio.ps1`: `unity-compile` → `csErrors=0; CompileCheck OK`, status pass (`Artifacts/Results/20261030-032255-011-22400-unity-compile.json`). The slot wait (2 editors busy) worked as before, and the time limit only starts once the editor is launched.
- **Real forced overrun:** the local `unityRunTimeoutMinutes` was set to 0.1 for one `unity-compile` and restored straight after (the gitignored config is back to its original content). Result:
  - Log: `OPS-001: Unity run exceeded 0.1 min; killed editor 2736 and its helpers`.
  - Result JSON: `ok false, status fail, exitCode -1, summary "failed: Unity run exceeded unityRunTimeoutMinutes=0.1 and was killed (OPS-001)"`, script exit 1, 7.3 s.
  - Afterwards: **0** Unity processes for this worktree, `UnityProject/Temp/UnityLockfile` free, and the other worktree's editor (`brave-tu-ecb9f6`) plus the Hub's `serve` were still running.

**Notes (non-blocking)**
- n1: a killed run's partial log stays in `Artifacts/Logs`; the result names it. Fine.
- n2: the handoff's GAME-010 `[Explicit]` recommendation is the real throughput fix; this limit is only the backstop. Hub to route it.

## 2. REF-010 — **PASS (GO)**
- **Format:** `ROOM_FIXTURES.json` still round-trips through `json.dumps(indent=1)`, 86 rows. Only the `Cabinet_Storage_Large` row and `version` (rev6, rev5 text kept) changed.
- **DEC-068 wording:**
  - "next to the restroom door, against the wall (the door wall)" → placed on the east (door) wall, rot 90, faces W. ✔
  - "side not stated: placeholder = the side with free wall length that clears the door swing (Low, GAP-109)" → north side; Low; `gap` GAP-109; the note says the side wasn't stated. ✔
  - The superseded "back wall" reading (DEC-062/064) is kept as history in the note and in REFERENCES_INDEX §7.4. ✔
- **Bounds and geometry:**
  - The footprint x 6.5–8.0, y 29.7–32.9 sits inside the restroom (x 0–8.0, y 29.5–36.1) and overlaps none of the other placed restroom or hall rows.
  - The door opening is y 33.1–36.1 and swings into the restroom, so its 3 ft leaf sweeps x ≈5–8, y 33.1–36.1 whichever jamb is hinged. The cabinet stays 0.2 ft clear.
  - The width change 4.0 → 3.2 ft fits the free wall (29.5–33.1 = 3.6 ft, less 0.2 ft clearance each end). It is noted as "was 4.0".
- REFERENCES_INDEX §7.4 attributes DEC-062 and DEC-068 separately; nothing else changed.

## For the Hub
Merge both. Route the GAME-010 `[Explicit]` / category fix for `Explore_TuningGrid` (OPS-001 recommendation 1).
