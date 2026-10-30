# REVIEW-W5Q — BUILD-006: playtest build handoff (docs check)

**Verdict: PASS (GO).** Branch `review/wave-5q` (off `main` 44ce03b) merges `claude/task-build-006` @ 1399830 cleanly. Only `Docs/Handoffs/BUILD-006.md` (+53). Reviewer: standing Docs reviewer (DEC-085), 2026-10-30. Review ID = next free; the Hub may renumber. I did not play the build.

## Checks
- **Build exists as stated:** `C:/Users/handl/Downloads/Dispo Game Builds/slice-38b9e5c/` holds `DispoGame.exe` + data (228 MB). `BUILD_MANIFEST.json` says commit 38b9e5c (on `main`), Unity 6000.6.7f1, 12 scenes incl. BackRooms, smoke `STUDIO_SMOKE_READY scenes=11, exitedEarly=False, crash=False` ✔.
- **Result file:** `Artifacts/Results/20261030-040650-232-41476-unity-build.json` (in the BUILD session's worktree): `ok: true`, `exitCode: 0`, same commit ✔.
- **"New since" list matches main up to 38b9e5c:** GAME-008 ID stand (W5N), GAME-010 tuning (W5M: 16 customers, gaps 150/60 s for the DEC-056 25–40 min shift), BRAND-001b (W5I), cart/limit meter and jar fill from earlier waves ✔. The 1 oz limit matches DEC-036 (28 g) ✔.
- **Known gaps are honest:** no medical customers (GAME-009 still active), no audio (AUDIO-002 not started), placeholder NPCs (ASSET-003 not integrated), temporary check-in anchor, pre-DEC-084 art, no ambient coworkers ✔.
- The playtest script is 10 minutes and asks what DEC-085 (5) wants: three biggest "not how it works" moments.

## Note (no change needed)
- `BUILD_MANIFEST.json` has `dirtyPathCount: 1`: the build ran with Unity's re-serialised `HDRenderPipelineGlobalSettings.asset` in the working tree (reverted afterwards, as the handoff says). The exe is 38b9e5c plus that editor-side settings rewrite. Harmless for a playtest, but "built from 38b9e5c" isn't byte-exact.
