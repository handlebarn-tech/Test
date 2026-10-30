# PROJECT STATE

**Milestone:** vertical slice PLAYABLE on main (2026-10-29). Wave 4 (lookdev, real jars, packaged goods, perf) is landing. Next milestone: **PS1** (cart, limit meter, ID checks, medical, tuning; `Docs/Design/ROADMAP_POST_SLICE.md`), extended by Nolan's decision-pressure spec (DES-003).
**Main:** see `git log`; every merge is a reviewed `review/wave-*` branch.
**Updated:** 2026-10-30 ~05:30 by Hub (session 4), main 0fca821.

## Read with this
**Hub:** `Docs/HUB_RESUME.md` (HARD RULES first, then its reading list) + the newest DECs. **Workers:** `CLAUDE.md` → this file → your packet only.

## In flight (as of main 0fca821, 2026-10-30 ~05:30; verify with `list_sessions {"linked": true}`)
Merged in Hub session 4: W4K GAME-005, W4Q DES-003, W4J PERF-001, W4P PROC-003, W4R REF-009, W4S UX-005, IMP-001, W4U REF-009b, W4V IMP-002, W4T QA-002, W4X DOC-001, W4W GAME-006. DECs 052–068.

| Work | Session | State | Next Hub step |
|---|---|---|---|
| GAME-007 limit meter + strikes (+ W4W m1/m2/m4) | `local_7f8c95e9-933b-4ca0-8d51-0ecbe3d5688a` | running | Unity review → GAME-008 |
| GAME-010 tuning + personas (merging cart; W4W m3) | `local_0d166a8e-87b1-40bb-9594-be389c549875` | grid 3 | review |
| ART-006 bud materials + back rooms (`claude/task-art-006`) | `local_392adc04-9603-4cc9-959c-6e3e2d792743` | moving restroom storage cabinet by the door (DEC-068) | Unity review; ROOM_FIXTURES old cabinet spot → next REF pass |
| REVIEW-W4Y: QA-002b (45a1031) | `local_0dd63bac-df1d-448d-9203-641ead6b6837` (worker `local_e8fae0a3…` idle) | running | merge on GO (before GAME-017) |
| REVIEW-W4Z: DOC-003 (d0f3028) | `local_c94488d7-c103-4ed2-8385-e0e9f967d8ac` (worker `local_b6a24c47…` idle; keeps context for DOC-002) | running | merge on GO |

## Next tasks to start (dependency order)
0. DOC-002 (AUDIT batch D) in the next gap between waves; DOC-003 (batch E) low priority. Merged this session also: W4U (REF-009b), W4V (IMP-002), W4T (QA-002; DEC-067), W4X (DOC-001). Free reviewer: `local_c94488d7…`.
1. PS1 chain: GAME-007 (running) → GAME-008 → GAME-009 (serialised, DEC-064 A3); then PS1b GAME-017 after GAME-007/010 + QA-002b.
2. REF pass: ROOM_FIXTURES restroom cabinet → by the door (DEC-068).
3. GAME-004 packaged goods into play: needs DATA-002 + PROC-004 (merged) + UX-002 + DES-003's integration.
4. A playable build for Nolan after GAME-006/ART-006 (session, never the Hub).
5. Whatever DES-003 creates for genuine gaps.

## Open questions for Nolan
- REF-008 questions: Q1–15 answered (DEC-051; Q4 vestibule size unknown, Q11 skipped). **All answered (DEC-062, 2026-10-30); no more CCTV/photos available** (FOH wall, rack runs, vestibule, lockers, bench, office items, BOH items, restroom/JC photos): full list in `Docs/Handoffs/REF-008.md` "Questions for Nolan". Sent 2026-10-30 02:15; answers go to the REF/ART tasks.
- Brand names/IP before any public build (real brands in `batches.json` and the packaged catalog).
- Phoenix TPT rate (OPEN-4): a receipt's tax lines would settle it; 25.1 % is kept (DEC-001).

## Pending from Nolan
- ~~"Fully built systems" file~~: arrived 2026-10-30 as `Downloads/Dispo Game Imports/DISPO_GAME_DESIGN_V2/`; IMP-001 auditing.
- V2 design pack approved 2026-10-30 (DEC-063); IMP-002 integrates.
- ChatGPT-built mechanics: he will drop them in `C:/Users/handl/Downloads/Dispo Game Imports/`. Process: audit → review → **Nolan's approval** before any use.
- Imports always go to `Downloads/Dispo Game Imports/` (outside the repo). `Imports/` in the repo root is git-excluded locally; the Dutchie export was moved out of it on 2026-10-30.

## Builds
- Playable exe for Nolan: `C:/Users/handl/Downloads/Dispo Game Builds/slice-c867cd5/DispoGame.exe` (pre-lookdev). New builds always come from a session (DEC-045), never the Hub.

## Cross-project
- GAP-206 relayed to the TFS tool hub. When TFS ships v7.11.5: re-import, regenerate goldens and diff (GAP-210, DEC-014/038).

## Standing notes
- Reference graybox objects by name/anchor only (fileIDs churn on rebuild).
- Raw CCTV stills and photos never ship in a build.
- Unity Warehouse/Office packs still need a Package Manager download (P1, later).
