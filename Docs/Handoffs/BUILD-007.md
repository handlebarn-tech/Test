# Handoff: BUILD-007 playtest build 2

**Status:** done. **The build Nolan plays is `playtest2-741bb43`** (main 741bb43: PS1 + GAME-025 + ART-007), built in worktree `claude/task-build-007`. An earlier `playtest2-08758c1` (pre-ART-007) was built first, per the first GO; it is superseded. Only this handoff is committed.

## Build
- **Exe:** `C:/Users/handl/Downloads/Dispo Game Builds/playtest2-741bb43/DispoGame.exe`, folder 228 MB, `BUILD_MANIFEST.json` beside it. Earlier builds are untouched.
- **Built with:** `studio.ps1 unity-build` (DEC-013 gate), Unity 6000.6.7f1, Windows64 dev build.
- **Smoke:** `STUDIO_SMOKE_READY scenes=11`, no crash, no early exit. The copied exe launched (1280×720 windowed) logs `[Slice] doors: 12 (...)` and `shift ready: 16 customers, 77 jars, seed 1`, and is then killed; no player is left running.
- **Door data workaround (FOR the Hub):** `SliceGame.Doors` is unassigned, so the player falls back to `<exe dir>/../Docs/Reference/DOORS.json`. Without that file it logs `doors: none found` and ART-007's closed leaves stay solid (staff doors and the entry can't be opened). I copied main's `Docs/Reference/DOORS.json` to `C:/Users/handl/Downloads/Dispo Game Builds/Docs/Reference/DOORS.json`; after that, 12 doors wire up. If the build folder is moved out of `Dispo Game Builds`, doors break again. The real fix is GAME-025 note 1: a TextAsset copy under `Assets`, assigned in `Gameplay_Slice` (owner: World/Gameplay). That needs a follow-up task.
- Editor side effects reverted in the worktree: `HDRenderPipelineGlobalSettings.asset` and new `.meta` files for the PROC-005 wire-shelving FBXs (REVIEW-ART7 minor 4; the owner should commit those metas).

## New since slice-38b9e5c
- **Store rebuilt from REF-011/012 (ART-007):** counters, 11 stations with seeded kits, three deli walls (177 jar slots, uneven fill), queue stanchions, vestibule, HUB/office, 12 swinging doors, re-posed CCTV. REF-013 corrections (entry move, counters, hinges) are not in yet.
- **Medical customers (GAME-009):** about 4 % are MED patients (`✓ MED card verified`, `⚠ Card: out-of-state`). T switches between Medical (9.1 % tax, 14-day 70.87 g allotment) and Adult-use (25.1 %, 28 g). An out-of-state card rung as medical is blocked once, then strikes. The report shows the medical/adult-use tax split. At 125/150 % text, the queue strip sits in the ID panel header.
- **Controls (GAME-025):** look is always on while the cursor is locked; Esc pauses from every screen (Resume / Settings / Controls / Quit); Settings has sensitivity, invert Y, FOV, text size and auto-fill; doors open by walking up or with E.

## Controls
| Action | Key |
|---|---|
| Move / run | WASD / Shift |
| Look | mouse (click to re-lock the cursor) |
| Interact: ID stand, talk, door | E |
| ID check: admit / refuse | A / R |
| Cover prompt yes / no | Y / N |
| Query or results → register; more results | R; M |
| Medical / Adult-use | T |
| Back / Pause | Backspace / Esc |
| Debug overlay | F3 |

## Known gaps Nolan will notice
- **Store layout:** the REF-013 fixes are pending. The JC door is blocked by the break-room bench, and the Vest_FOH door swing hits the trash can (REVIEW-ART7 minor 3).
- **Customer flow and recommendation depth are not in this build:** GAME-026 (call next / waypoints) and GAME-017a come next. Station kits are placeholders until PROC-006b.
- No audio; placeholder NPCs; no ambient coworkers. The windowed cursor lock has not been tested in automation; this build is the first real check.

## Validation
`unity-build` exit 0: `Artifacts/Results/20261030-083342-009-28776-unity-build.json` (worktree). The copied-exe launch passed with doors wired.

## Questions for Nolan (through the Hub)
None.
