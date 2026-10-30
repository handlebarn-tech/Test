# Handoff: BUILD-007 playtest build 2

**Status:** done. Built from main 08758c1 (GAME-025 merged; ART-007 not in, per Hub GO) in worktree `claude/task-build-007`. Only this handoff is committed; the build lives outside the repo.

## Build
- **Exe:** `C:/Users/handl/Downloads/Dispo Game Builds/playtest2-08758c1/DispoGame.exe`, folder 228 MB. Earlier builds (`slice-c867cd5`, `slice-38b9e5c`) are untouched.
- **Built with:** `studio.ps1 unity-build` (DEC-013 gate), Unity 6000.6.7f1, Windows64 dev build. `BUILD_MANIFEST.json` sits next to the exe.
- **Smoke:** `STUDIO_SMOKE_READY scenes=11`, no crash, no early exit. The copied exe was launched once (1280×720 windowed): `[Slice] shift ready: 16 customers, 77 jars, seed 1` after 8 s, then killed; no player left running.
- Editor side effects reverted in the worktree, not committed: `HDRenderPipelineGlobalSettings.asset` re-serialised (as in BUILD-006), and new `.meta` files for the PROC-005 wire-shelving FBXs (main has the FBXs without metas; owner: PROC-005 / Assets).

## New since slice-38b9e5c
- **Medical customers (GAME-009):** about 4 % of customers are MED patients. A `✓ MED card verified` badge replaces the 21+ badge; out-of-state cards show `⚠ Card: out-of-state`.
- **Medical / Adult-use switch (T, or the payment-row button):** medical tax 9.1 % vs 25.1 % adult-use; 14-day allotment meter (70.87 g minus the patient's recent buys) instead of the 28 g cap. Ringing an out-of-state card as medical is blocked once with a hint, then strikes.
- **Queue strip:** at 125/150 % text size the ID panel header shows the queue line (count, ●/◐/▲, stand count).
- **Report:** medical customers, medical sales and tax split.
- **Controls (GAME-025):** mouse look is always on while the cursor is locked (no right-button hold); Esc pauses from every screen (Resume / Settings / Controls / Quit); Settings has sensitivity, invert Y, FOV, text size, auto-fill assist; Backspace is Back.

## Controls
| Action | Key |
|---|---|
| Move / run | WASD / Shift |
| Look | mouse (click to re-lock the cursor) |
| Interact: ID stand, talk to the counter customer | E |
| ID check: admit / refuse | A / R |
| Cover prompt yes / no | Y / N |
| Query or results → register; more results | R; M |
| Medical / Adult-use sale type | T |
| Back | Backspace |
| Pause menu | Esc |
| Debug overlay | F3 |

## Known gaps Nolan will notice
- **No doors:** the log says `[Slice] doors: none found`. The door system is in, but no door geometry is on main yet, and DOORS.json is not packaged for player builds (GAME-025 note 1).
- **No ART-007 graybox update;** the store is still the earlier graybox/lookdev set, and the check-in desk still uses the TEMP fallback anchor.
- **Customer flow and recommendation depth from playtest 1 are not in this build:** GAME-026 (call next / waypoints) and GAME-017a are next.
- No audio; placeholder NPCs; no ambient coworkers.
- The real windowed cursor lock was never tested in automation (batchmode); this build is its first real check.

## Validation
`unity-build` exit 0: `Artifacts/Results/20261030-082228-138-12996-unity-build.json` (worktree). Copied-exe launch passed.

## Questions for Nolan (through the Hub)
None.
