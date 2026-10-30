# PROJECT STATE

**Milestone:** vertical slice PLAYABLE on main (2026-10-29). Wave 4 (lookdev, real jars, packaged goods, perf) is landing. Next milestone: **PS1** (cart, limit meter, ID checks, medical, tuning; `Docs/Design/ROADMAP_POST_SLICE.md`), extended by Nolan's decision-pressure spec (DES-003).
**Main:** see `git log`; every merge is a reviewed `review/wave-*` branch.
**Updated:** 2026-10-30 03:55 MST by Hub (session 4), handover for the 07:00 scheduled resume (usage limit).

## Read with this
**Hub:** `Docs/HUB_RESUME.md` (HARD RULES first, then its reading list) + the newest DECs. **Workers:** `CLAUDE.md` → this file → your packet only.

## In flight (as of main 38b9e5c, 2026-10-30 ~04:40 MST; verify with `list_sessions {"linked": true}`)
Merged in Hub session 4 (latest): W5K RES-002 (squashed), W5N GAME-008, W5M GAME-010, W5F IMP-003 audit (drops 1–4 + PROC checklist). DECs through 086.

| Work | Session | State | Next Hub step |
|---|---|---|---|
| GAME-009 medical (+ W5N m2 queue strip at scale) | `local_7f8c95e9-933b-4ca0-8d51-0ecbe3d5688a` | running | B2 reviews → PS1 done → REVIEW-PS1 + playtest |
| Playtest: Nolan to play `Downloads/Dispo Game Builds/slice-38b9e5c/DispoGame.exe` (script in `Docs/Handoffs/BUILD-006.md`) | Nolan | waiting | his notes → tasks |
| GAME-010b (eae2aeb) → Unity B2 reviewing | `local_041172fa…`; worker `local_0d166a8e…` idle | review | merge on GO |
| REVIEW-W5L DES-004b+c | Docs reviewer `local_b073ffa0-2129-4b65-9193-95f27fcfc0f7` | running/queued | merge on GO |
| **PROC-005**: integrate approved toolkit + fix every checklist item (DEC-092/084) | `local_6c216f80-4744-4711-9081-d99ed58eba4f` | running | Unity A reviews slices; after integration archive the drops (DEC-070) |
| IMP-003 idle until rounds 3–7 drop | `local_13653ae5…` | idle | message it when Nolan adds drops |
| ASSET-003 merged (W5P); next: MPFB2 high-quality customer path + GAME-CHR packets (DEC-087) | worker `local_d31ad4c5…` idle | waiting | dispatch ASSET-004 (MPFB2) after the toolkit approval |
| Standing reviewers: Unity A `local_0dd63bac…` (idle), Unity B2 `local_041172fa-72b8-4943-b69e-72fc7a83b9fd`, Docs `local_b073ffa0…`. DES worker `local_82d327a2…` idle. | | | |

## Resume checklist (07:00)
**Hub handover:** the 07:00 scheduled run becomes the new Hub; the old Hub chat `local_c6267ff5-2acb-4b09-83a7-53541a088c66` gets archived by Nolan (cost). The new Hub announces its id to every workcell and updates HUB_RESUME/this file.
0. Process (DEC-085): standing reviewers Unity A `local_0dd63bac…`, Unity B2 `local_041172fa…` (B retiring), Docs `local_b073ffa0…`; workers message them directly. OPS-003 slot monitor running on `local_0d166a8e…`.
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
- ChatGPT Blender toolkit (DEC-069; rounds 4–7 briefed DEC-091; round 2 approved DEC-074: retail floor, materials, labels, exterior, hands): arriving in drops; IMP-003 audits each, re-checking the folder after each audit.
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
