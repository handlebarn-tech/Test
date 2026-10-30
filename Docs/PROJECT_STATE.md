# PROJECT STATE

**Milestone:** vertical slice PLAYABLE on main (2026-10-29). Wave 4 (lookdev, real jars, packaged goods, perf) is landing. Next milestone: **PS1** (cart, limit meter, ID checks, medical, tuning; `Docs/Design/ROADMAP_POST_SLICE.md`), extended by Nolan's decision-pressure spec (DES-003).
**Main:** see `git log`; every merge is a reviewed `review/wave-*` branch.
**Updated:** 2026-10-30 ~04:15 by Hub (session 4).

## Read with this
**Hub:** `Docs/HUB_RESUME.md` (HARD RULES first, then its reading list) + the newest DECs. **Workers:** `CLAUDE.md` → this file → your packet only.

## In flight (2026-10-30 ~04:15, Hub session 4)
Merged this session: W4K (GAME-005), W4Q (DES-003; DEC-052..059), W4J (PERF-001), W4P (PROC-003), W4R (REF-009), W4S (UX-005), IMP-001 audit. Nolan answered N1/N2 (DEC-060/061) and the remaining room questions (DEC-062).

| Work | Session | State | Next Hub step |
|---|---|---|---|
| REVIEW-W4W: GAME-006 cart (19b2866) | `local_0dd63bac-df1d-448d-9203-641ead6b6837` (worker `local_7f8c95e9…` idle for fixes) | running | merge on GO → GAME-007 |
| QA-002 Gate A parity + DP harness | `local_e8fae0a3-19cd-429a-b0fa-e555c65a23ec` | Unity run queued | review |
| GAME-010 tuning + personas | `local_0d166a8e-87b1-40bb-9594-be389c549875` | grid 2 running | review |
| ART-006 bud HDRP materials, then back rooms | `local_392adc04-9603-4cc9-959c-6e3e2d792743` | running | review; rooms after REF-009b |
| REVIEW-W4T: QA-002 | `local_c94488d7-c103-4ed2-8385-e0e9f967d8ac` | running | merge on GO |
| DOC-001: apply AUDIT-001 A+B+C (DEC-064), 2 phases | `local_b6a24c47-ab71-4d36-9df9-1eb188edc2b0` | phase 1 running, phase-2 go sent (IMP-002 merged); **Hub: don't edit BACKLOG/HUB_RESUME/KNOWN_GAPS until merged**; send phase-2 go after IMP-002 merges | → Nolan approves before ANY doc change |
| Idle, reusable: W4P/W4Q reviewers done; free reviewer `local_c94488d7…` after W4T, `local_0dd63bac…` after W4U; QA-002 worker `local_e8fae0a3…` (fixes after W4T). Archived 2026-10-30: PERF-001, PROC-004, REF-008/W4P, GAME-005, DES-003, UX-005, W4D/W4J/IMP1 reviewer. | | | |

## Next tasks to start (dependency order)
0. DOC-002 (AUDIT batch D) in the next gap between waves; DOC-003 (batch E) low priority. Merged this session also: W4U (REF-009b), W4V (IMP-002).
1. GAME-006 cart (packet in `Docs/Tasks/Ready/`): after GAME-005 merges (same slice files). Then GAME-007 → GAME-008/009 per their packets; GAME-010 is running.
2. ART back rooms (Office/FOH/BOH/Break) from `ROOM_FIXTURES.json` + Nolan's answers, after W4N.
3. GAME-004 packaged goods into play: needs DATA-002 + PROC-004 (merged) + UX-002 + DES-003's integration.
4. A bud material pass (buds render white; GAME-005 note), ART or PROC.
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
