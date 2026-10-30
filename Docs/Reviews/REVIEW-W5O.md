# REVIEW-W5O — OPS-003: Unity slot monitor (`studio.ps1 slots`, DEC-085 item 6)

**Verdict: PASS (GO).** Branch `review/wave-5o` (off `main` de9dc7e) merges `claude/task-ops-003` @ 2328fab cleanly (e77688e). 4 files, +113/−3: `Tools/Studio/studio.ps1`, new `Tools/Studio/studio_slots_test.ps1`, a `TOOLCHAIN_EXECUTION.md` paragraph, handoff. No Unity, no game code. Reviewer: standing Docs reviewer (taken because it is tooling-only and needs no editor), 2026-10-30. (Review ID W5O picked as the next free one; the Hub may renumber.)

## Checks
- **Read-only:** the `slots` case only reads processes (`Get-CimInstance`) and runs `git rev-parse` in the editor's worktree. It contains no `Stop-Process`/`taskkill`/`.Kill(`, and the self-check asserts that. Its only write is the standard `Artifacts/Results/<stamp>-slots.json` + log (gitignored; `git status` clean after a run) ✔.
- **Shared filter:** `Wait-UnitySlot` now calls `Get-UnityEditors`, whose filter (`*\Editor\Unity.exe`, excluding `AssetImportWorker` and `serve`) is byte-for-byte the old inline one, so gate behaviour is unchanged. The function is defined after `Wait-UnitySlot` but before the `switch` runs, so the call resolves ✔.
- **Row resolution:** the worktree comes from `-projectPath` (quoted or unquoted) minus `UnityProject`; the branch comes from `git -C`. The command comes from the parent's `studio.ps1 <cmd>`, else from the studio log name `<stamp>-<cmd>.log`, else `? (not studio.ps1)`. If the parent has exited, its CIM lookup returns null and the row falls through to the log name ✔.
- **Runs here:** `studio_slots_test.ps1` ALL PASS (12/12); OPS-001 `studio_runlimit_test.ps1` ALL PASS; live `studio.ps1 slots` with no editors up gives `0/2 editor slots in use`, exit 0, and a result JSON ✔. A live two-editor run is taken on trust from the handoff.
- Docs: TOOLCHAIN_EXECUTION command list + paragraph accurate (20-min flag, never kills, OPS-001 timeout does the killing) ✔.

## Notes (no change needed)
- The 20-min threshold is a literal in `Get-SlotInfo` (per DEC-085). If it ever needs tuning, move it next to `unityRunTimeoutMinutes` in config.
- The command label is read from the log name, so it can be finer than the ValidateSet (the handoff shows `unity-capture-slice`). That's fine: it is display only.
- Handoff note: the branch was cut inside the GAME-010 session's worktree; GAME-010's branch is untouched (its commits aren't in this diff) ✔.
