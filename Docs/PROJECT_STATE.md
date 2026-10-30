# PROJECT STATE

**Milestone:** vertical slice PLAYABLE on main (2026-10-29). Wave 4 (lookdev, real jars, packaged goods, perf) is landing. Next milestone: **PS1** (cart, limit meter, ID checks, medical, tuning; `Docs/Design/ROADMAP_POST_SLICE.md`), extended by Nolan's decision-pressure spec (DES-003).
**Main:** see `git log`; every merge is a reviewed `review/wave-*` branch.
**Updated:** 2026-10-30 03:55 MST by Hub (session 4), handover for the 07:00 scheduled resume (usage limit).

## Read with this
**Hub:** `Docs/HUB_RESUME.md` (HARD RULES first, then its reading list) + the newest DECs. **Workers:** `CLAUDE.md` → this file → your packet only.

## In flight (as of main 0fca821, 2026-10-30 ~05:30; verify with `list_sessions {"linked": true}`)
Merged in Hub session 4: W4K GAME-005, W4Q DES-003, W4J PERF-001, W4P PROC-003, W4R REF-009, W4S UX-005, IMP-001, W4U REF-009b, W4V IMP-002, W4T QA-002, W4X DOC-001, W4W GAME-006, W4Y QA-002b, W4Z DOC-003, W5B OPS-002, W5C OPS-001+REF-010, W5E AUDIO-001 (ledger author fixes m1/m2 → AUDIO-002), W5A ART-006 (minors: back-room lighting, mop x → later ART/REF), W5G GAME-007, W5H BRAND-001, W5D DES-004 (DEC-077), W5I BRAND-001b. DECs through 084 (high-quality asset bar). DECs 052–073.

| Work | Session | State | Next Hub step |
|---|---|---|---|
| REVIEW-W5N: GAME-008 (a73f8b7+7b5b056) | `local_c94488d7-c103-4ed2-8385-e0e9f967d8ac` (worker `local_7f8c95e9…` idle) | running | merge on GO → GAME-009 |
| REVIEW-W5M: GAME-010 (2d81a7b) | `local_0dd63bac-df1d-448d-9203-641ead6b6837` (worker `local_0d166a8e…` idle) | running | merge on GO → playable build session |
| **IMP-003**: rolling toolkit audit; round 2 landed (3 new packages) | `local_13653ae5-1c1d-43bc-8eaf-e383573d7312` | auditing round 2 | review → one approval summary to Nolan → PROC-005 integrates + fixes findings (DEC-083) |
| REVIEW-W5L: DES-004b+c (22ccc85) | `local_b073ffa0-2129-4b65-9193-95f27fcfc0f7` (worker `local_82d327a2…` idle) | running | merge on GO |
| RES-002: staffing counts from OneDrive schedule (read-only, counts only) | `local_7f53cf19-16d8-4ba4-b186-9c03960e8906` | running | review (PII check) → GAP-DAY-03 |
| RES-002 fixing W5K M1 (3 lines identify one person) | `local_7f53cf19-16d8-4ba4-b186-9c03960e8906` | running | re-review by `local_b073ffa0…`; squash before merge if PII is in history |
| ASSET-003: CC0 customer characters + animations (sourcing, no Unity) | `local_d31ad4c5-232b-4628-986c-5d276e71a2a2` | running | review |
| W5F IMP-003 drop 1 PASS w/ minors (`review/wave-5f`) | reviewer `local_b073ffa0…` | held | wait for IMP-003 delta audit of ChatGPT's fixes, then one approval summary to Nolan |

## Resume checklist (07:00)
1. `list_sessions {"linked": true}`; merge any review/* with GO (W5I BRAND-001b on `review/wave-5j`, W5K RES-002, GAME-010 review once its sweep commits, DES-004b+c review).
2. GAME-010 → Unity review (`local_0dd63bac…`), then the **playable build session** for Nolan.
3. IMP-003 round 2 audit → docs review → one plain summary to Nolan for approval → PROC-005 integrates + fixes findings (DEC-083). Round 3 drops arrive in Imports; message IMP-003.
4. GAME-008 (running) → review → GAME-009. ASSET-003 → review. Archive finished workers.

## Next tasks to start (dependency order)
0. DOC-002 (AUDIT batch D, fresh session; AUDIT-001 session archived) in the next gap between waves, incl. SLICE_DESIGN → TUNING_PS1 pointer (DEC-082); DOC-003 (batch E) low priority. Merged this session also: W4U (REF-009b), W4V (IMP-002), W4T (QA-002; DEC-067), W4X (DOC-001). Free reviewer: `local_c94488d7…`.
1. PS1 chain: GAME-007 (running) → GAME-008 → GAME-009 (serialised, DEC-064 A3); then PS1b GAME-017 after GAME-007/010 + QA-002b.
2. REF pass: ROOM_FIXTURES restroom cabinet → by the door (DEC-068).
3. GAME-004 packaged goods into play: needs DATA-002 + PROC-004 (merged) + UX-002 + DES-003's integration.
4. **Playable build for Nolan** (cart, limits, real jars, coloured buds, back rooms) once GAME-010 merges, to keep Unity slots free; a session builds it, never the Hub.
5. Whatever DES-003 creates for genuine gaps.

## Open questions for Nolan
- REF-008 questions: Q1–15 answered (DEC-051; Q4 vestibule size unknown, Q11 skipped). **All answered (DEC-062, 2026-10-30); no more CCTV/photos available** (FOH wall, rack runs, vestibule, lockers, bench, office items, BOH items, restroom/JC photos): full list in `Docs/Handoffs/REF-008.md` "Questions for Nolan". Sent 2026-10-30 02:15; answers go to the REF/ART tasks.
- Phoenix TPT rate (OPEN-4): a receipt's tax lines would settle it; 25.1 % is kept (DEC-001).

## Pending from Nolan
- ChatGPT Blender toolkit (DEC-069; round 2 approved DEC-074: retail floor, materials, labels, exterior, hands): arriving in drops; IMP-003 audits each, re-checking the folder after each audit.
- ~~"Fully built systems" file~~: arrived 2026-10-30 as `Downloads/Dispo Game Imports Archive/2026-10-30_DISPO_GAME_DESIGN_V2/`; IMP-001 auditing.
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
