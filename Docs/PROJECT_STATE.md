# PROJECT STATE

**Milestone:** vertical slice PLAYABLE on main (2026-10-29). Wave 4 (lookdev, real jars, packaged goods, perf) is landing. Next milestone: **PS1** (cart, limit meter, ID checks, medical, tuning; `Docs/Design/ROADMAP_POST_SLICE.md`), extended by Nolan's decision-pressure spec (DES-003).
**Main:** see `git log`; every merge is a reviewed `review/wave-*` branch.
**Updated:** 2026-10-30 ~02:45 by Hub (session 3), as a handover for a cleared Hub.

## Read with this
`Docs/HUB_RESUME.md` (HARD RULES first) · `Docs/BACKLOG.md` · last ~15 entries of `Docs/DECISIONS.md` (through DEC-050) · `Docs/Handoffs/*`.

## In flight (2026-10-30 02:45)
Merged since the 02:20 handover: W4L (UX-002, condition M1: text scaling for the new panels, which goes to GAME-006/UX), W4N (REF-008), W4O (DATA-002), W4M (ART-005). DEC-051 records Nolan's room answers (sanitised).
Sessions report to whichever session is Hub. Message them by id.

| Work | Session | State | Next Hub step |
|---|---|---|---|
| REVIEW-W4Q: DES-003 spec integration (`claude/task-des-003-bb569f`) | `local_c94488d7-c103-4ed2-8385-e0e9f967d8ac` | running | merge on GO; ratify DES-003's proposed DECs; forward its 2 questions to Nolan; **then send AUDIT-001 its go** |
| **AUDIT-001**: READ-ONLY .md audit | `local_b6a24c47-ab71-4d36-9df9-1eb188edc2b0` | **WAITING for the Hub's go** | after W4Q merges: SendMessage "go, main = <sha>". Report → Nolan approves before ANY doc change; don't remove rules or context |
| REF-009: apply DEC-051 to ROOM_FIXTURES | `local_8bee29f0-46b7-4ee5-87bf-9792b70f6267` | running | review (docs), merge |
| REVIEW-W4K: GAME-005 real jars | `local_0dd63bac-df1d-448d-9203-641ead6b6837` | capture gate running | merge on GO → start GAME-006 cart |
| REVIEW-W4P: PROC-003 | `local_3bc3be53-eb4d-477e-8a99-02d950744ef4` | waiting on Unity; flags a GAME-005 interface clash | merge after W4K; route the clash to a GAME follow-up |
| REVIEW-W4J: PERF-001 | `local_fa1d4222-cd8c-4df7-b9ab-799c6519e8b9` | re-runs going | merge on GO; ratify perf budgets |
| **IMP-001**: audit Nolan's DISPO_GAME_DESIGN_V2 import (read-only) | `local_ad2c683f-9022-4d82-8d3d-2cad5d63c888` | running | send report to a REVIEW session, then to Nolan for approval; no use before approval |
| GAME-010 tuning + personas | `local_0d166a8e-87b1-40bb-9594-be389c549875` | idle; needed `git lfs pull` | nudge to finish, then review |
| Idle, reusable or archivable: ART `local_392adc04…`, PROC-004 `local_ffb38222…`, GAME-005 `local_65e98573…`, DES-003 `local_afc2a299…` | | | reuse for ART back rooms after REF-009 |

## Next tasks to start (dependency order)
1. GAME-006 cart (packet in `Docs/Tasks/Ready/`): after GAME-005 merges (same slice files). Then GAME-007 → GAME-008/009 per their packets; GAME-010 is running.
2. ART back rooms (Office/FOH/BOH/Break) from `ROOM_FIXTURES.json` + Nolan's answers, after W4N.
3. GAME-004 packaged goods into play: needs DATA-002 + PROC-004 (merged) + UX-002 + DES-003's integration.
4. A bud material pass (buds render white; GAME-005 note), ART or PROC.
5. Whatever DES-003 creates for genuine gaps.

## Open questions for Nolan
- REF-008 questions: Q1–15 answered (DEC-051; Q4 vestibule size unknown, Q11 skipped). **Still open: Q16–22** (FOH wall, rack runs, vestibule, lockers, bench, office items, BOH items, restroom/JC photos): full list in `Docs/Handoffs/REF-008.md` "Questions for Nolan". Sent 2026-10-30 02:15; answers go to the REF/ART tasks.
- Brand names/IP before any public build (real brands in `batches.json` and the packaged catalog).
- Phoenix TPT rate (OPEN-4): a receipt's tax lines would settle it; 25.1 % is kept (DEC-001).

## Pending from Nolan
- ~~"Fully built systems" file~~: arrived 2026-10-30 as `Downloads/Dispo Game Imports/DISPO_GAME_DESIGN_V2/`; IMP-001 auditing.
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
