# PROJECT STATE

Hub-owned; the **only live state record** (DEC-117). A fresh Hub resumes from `Docs/HUB_RESUME.md` + this file + the newest DECs, then reconciles the table below with `list_sessions {"linked": true}` and `git branch` (STUDIO_OS §0.9). Workers and reviewers do not read this file. Task state otherwise = packet folder (`Docs/Tasks/Ready|Active|Done`).

**Updated:** 2026-10-30 ~17:30 (control-plane cleanup, DEC-117). **Milestone:** PS1 complete on `main` (08758c1); playtest build 2 delivered (741bb43). Next: PS1b (GAME-026 → GAME-017a), layout accuracy (REF-013 fix → ART-008), DEC-111 asset replacements.
**Hub session:** `local_5c45166e-4872-47c3-bdfa-b8545d61e581` ("Dispo · Studio Hub"), reset 2026-10-30 ~15:55 (Nolan). Any other Hub-like session only forwards notices.
**Structure:** Nolan → Hub → workers → fresh per-review reviewers → Hub merges (DEC-116/117). Nolan is cost-sensitive: no FYI messages, lean briefs (DEC-107).

## In flight
| Session / agent | Task | Branch @ sha | State / next step |
|---|---|---|---|
| `dispo-game026` `local_9bc94fb7-d677-4076-81be-83317f26bbf8` | GAME-026 customer flow (Unity slot 1) | worker branch | GO 15:45: merge main, include the GAME-025 M1 SliceDoor width fallback. Then `ready for review`. |
| `dispo-proc-005-fixture-f` `local_335db39d-0968-49fa-846c-808a2abb2158` | PROC-005 fixture families rework (REVIEW-PROC5 FAIL findings) | worker branch; core already on main 81dde0d | Resumed 15:45. |
| `dispo-proc006b` `local_cab28702-140d-48df-963a-3cc4b318aa89` | PROC-006b register kit generators | from WIP d30bb73; 9728334 under REVIEW-PROC006b | Reviewer (Agent, worktree) running on 9728334. |
| `dispo-art008` `local_77fd945b-ecaf-4432-8c51-54b18ed9dc50` | ART-008 graybox final pass on the REF-013 fix (Unity slot 2) | off `worktree-agent-ae92283c8f8687a3d` @ 3890936 | Started ~16:30. Stops if REVIEW-REF13-FIX fails. |
| `dispo-asset007` `local_d3aad36e-a494-47b7-a5c7-2cd0a58efe19` | ASSET-007 glove overlay (Blender) | worker branch | Started ~16:30. |
| `dispo-asset005` `local_1bb17d9a-7584-4a8b-af68-d01479714d05` | ASSET-005/006 wardrobe + hair (Blender, no Unity) | worker branch | GO 15:45. |
| Agent (worktree) | REVIEW-REF13-FIX: REF-013 fix 3890936 | `review/ref13` | Verdict pending → merge, then ART-008 continues. |
| Agent (worktree) | REVIEW-PROC006b: 9728334 | — | Verdict pending. |
| Agent (worktree) | REF-013 M1 fix + REVIEW-ART7 m3 (JC door reach, Vest_FOH trash can in the door swing; DEC-115) | from `worktree-agent-a8683a438ebc5cbe4` | Running. On `ready for review` → fresh reviewer. |
| Agent (worktree) | PROC-009 vehicles (packet `Docs/Tasks/Active/PROC-009.md`) | worker branch | Running. |

Older briefs (ART-008 excepted) still name leads or pool reviewers; those workers were told to report `ready for review` to the Hub. The Hub spawns a fresh reviewer for each (STUDIO_OS §0.5). GAME-017a waits for GAME-026 (shared Slice files, one owner at a time).

## Queue (next packets, in order)
1. **GAME-017a** first playable recommendation depth (packet in `Tasks/Ready`, carries the DEC-118 rulings and REVIEW-DES6/UX6 minors) after GAME-026 merges.
2. **PROC-007** UV layout (DEC-097) after PROC-005 merges; the Lookdev label-shader cut-over (UV channel 2) is a small ART task in the same wave.
3. **GAME-021/022/024, UX-003, GAME-011/012** per DES-004 (packets in `Tasks/Ready`); GAME-017 → 018 → 019 → 020 after GAME-017a. GAME-018: Refine port is allowed as its own task (DEC-118 B1).
4. **GAME-CHR-002** customer import into Unity (ASSET-004 merged; spec `Docs/Assets/Specs/CHARACTERS.md`); then stocking arranger with believable uneven fill.
5. **REF check owed:** staff-tee print side from BAND 05/12 (DEC-089, DEC-118 Q8) → small REF task; GAP meanwhile.
6. **World lived-in pass** after final assets (DEC-104: small items never uniform between stations; cleaning supplies in the restroom cabinet); PROC-005 WireShelving FBX `.meta` files missing on main; livelier exterior later.
7. **BRAND-002** name search before any public build (DEC-078). Toolkit round 7 (DEC-091) after rounds 3–6 are integrated. Future `Dispo Game Imports/` drops get a new IMP task (DEC-095).

## Priorities (DEC-096, playtest 1)
Controls (done) → store/layout accuracy → believable customer flow → recommendation depth → asset integration that unblocks these.

## Open with Nolan
- Playtest build 2 is with him; his feedback becomes playtest 2 intake.
- Nothing else open. Never re-ask: W6 self-closing doors, emergency exit alarm, drum kit (DEC-105).

## Risks
- Unity editors: max 2 (DEC-013). `studio.ps1 slots`.
- ChatGPT toolkit drops need full audit before use (DEC-095).
- When TFS ships v7.11.5: re-import, regenerate goldens and diff (GAP-210).

## Builds
- Played: `slice-38b9e5c/` (playtest 1). **Playtest 2 = `Dispo Game Builds/playtest2-741bb43/DispoGame.exe`** (doors need `Dispo Game Builds/Docs/Reference/DOORS.json` until the GAME-026 TextAsset fix). Older playtest2-08758c1 has no doors.
