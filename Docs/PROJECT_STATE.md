# PROJECT STATE

Hub-owned. A fresh Hub resumes from this file + `Docs/HUB_RESUME.md` + recent `Docs/DECISIONS.md` (DEC-116). Workers do not read this file.

**Updated:** 2026-10-30 ~15:35. **Milestone:** PS1 complete on `main` (GAME-009 + GAME-025 controls merged 08758c1). Next: playtest build 2, then the PS1b work below.
**Hub session:** `local_c6267ff5-2acb-4b09-83a7-53541a088c66` ("Dispo · Studio Hub"). Nolan resets it himself if it gets expensive.
**Structure (DEC-116):** Hub → narrow workers → fresh per-review reviewers → Hub merges. No leads (DEC-112). Nolan is cost-sensitive: no FYI messages, lean briefs.

## In flight (session name → task)
| Session | Task | State / next step |
|---|---|---|
| `dispo-build007` `local_01655dfb-07f0-4706-a2a3-156d273999b0` | BUILD-007 playtest build 2 from main 741bb43 (incl. ART-007) | Building → `Downloads/Dispo Game Builds/playtest2-741bb43/`. When it reports: give Nolan the path, then reuse this session for the REF-013 M1 fix. |
| `dispo-game026` `local_9bc94fb7-d677-4076-81be-83317f26bbf8` | GAME-026 customer flow (Unity) | Read packet, waits for GO. Send GO after the build is out, plus: fix REVIEW-GAME025 M1 (SliceDoor 3 ft width fallback: log a placeholder + GAP tag), and on finish report to the Hub, not to a named reviewer. |
| `dispo-proc-005-fixture-f` `local_335db39d-0968-49fa-846c-808a2abb2158` | PROC-005 fixture families rework (REVIEW-PROC5 FAIL findings) | PAUSED for the build. Resume after: merge `worktree-agent-ac7414483b9f8bb4a` + main, fix all findings, report to the Hub. |
| `dispo-proc006b` `local_cab28702-140d-48df-963a-3cc4b318aa89` | PROC-006b register kit generators (from WIP d30bb73) | PAUSED for the build. Resume after: merge main, finish, report to the Hub. |

| `dispo-asset005` `local_1bb17d9a-7584-4a8b-af68-d01479714d05` | ASSET-005/006 wardrobe + hair (Blender, no Unity) | Writing packet, waits for GO. GO after the build. |

Workers' original briefs name long-lived reviewers (now archived). Tell each to report "ready for review" to the Hub; the Hub spawns a fresh reviewer (Agent tool with worktree isolation, or a fresh session).

## Queue (after the above)
1. REF-013 M1 fix, plus REVIEW-ART7 m3 (JC door blocked, Vest_FOH trash can in a door swing: settle from evidence, or GAP + NPCs avoid the JC anchors) (DEC-115: HUB desk/counter/cabinet sizes Low + narrowed GAP-132; hinge overrides from A011; storefront keeps pulls; 8 absence-inferred rows Low). Branch `worktree-agent-a2b65d251ee0f6ac2`@73e0e0c; verdict REVIEW-REF13 on `review/ref13`.
2. PROC-007 UV layout (DEC-097) after PROC-005 merges; the label-shader cut-over comes with it.
3. DEC-111 replacements: PROC-009 vehicles, ASSET-005/006/007 wardrobe/hair/gloves (PROC-008 cash tray rejected, DEC-051).
4. PS1b recommendation depth (GAME-017a packet notes in `Docs/Departments/GAMEPLAY.md` queue), GAME-021/022/024.
5. World lived-in pass after final assets; PROC-005 WireShelving FBX `.meta` files missing on main.
Dept files (`Docs/Departments/*.md`) are reference queues only.

## Priorities (DEC-096, playtest 1)
Controls (done) → store/layout accuracy → believable customer flow → recommendation depth → asset integration that unblocks these.

## Open with Nolan
- Playtest build 2: give him the path when it lands; his feedback becomes playtest 2.
- Nothing else open. Answered/closed: DEC-103/104/106/110/111/113. Never re-ask: W6 self-closing doors, emergency exit alarm (DEC-105).

## Risks
- Unity editors: max 2 (DEC-013). `studio.ps1 slots`.
- ChatGPT toolkit drops need full audit before use (DEC-095).
- When TFS ships v7.11.5: re-import, regenerate goldens and diff (GAP-210).

## Builds
- Played: `Downloads/Dispo Game Builds/slice-38b9e5c/` (playtest 1). Next: playtest2-08758c1.
