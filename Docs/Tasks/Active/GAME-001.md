# GAME-001 — Data importer (DATA-001) + pure C# domain engine slice

**Role:** GAME / data (one session; it may run the importer and engine as sub-steps) · **Priority:** P0 · **Branch:** `task/GAME-001` worktree off `base/wave-2` (DEC-012); rebase onto `main` after REVIEW-W1 merges

## Goal
The real recommendation engine running in Unity's `Dispo.Domain` assembly on real, PII-free batch data, matching the golden cases.

## Read
- `Docs/Handoffs/MIG-001.md`, especially "Recommended vertical-slice subset".
- `Docs/Reconstruction/RECONSTRUCTION_CONTRACT.md` (the sections for the slice subset only).
- `Docs/Reconstruction/DATA_SCHEMA.md` §5, the importer allow-list.
- `Docs/Reconstruction/GOLDEN_CASES.md` + `golden_cases.json`.
- DEC-001/002/006.

## Owns
- `Tools/Data/`: the importer, a Python or Node script, deterministic.
- `UnityProject/Assets/_Game/Data/Catalog/`: the generated JSON plus its manifest.
- `Assets/_Game/Code/Domain/`
- `Assets/_Game/Code/Tests/EditMode/`
- `Docs/Specs/ENGINE.md`

## Deliverable
1. **Importer (DATA-001).**
   - Reads `C:/Users/handl/Downloads/tfs-budtender/inventory/tfs-inventory-master.json` and the terpene DB / BA scalars / tier tables from v7.11.4 `index.html`. That folder is read-only; read it, never write to it.
   - Writes allow-listed fields only.
   - Records source md5s and its own version in a manifest.
   - Re-running it gives byte-identical output.
   - Include a check that fails if any field outside the allow-list appears.
2. **Domain engine.** Port only the MIG-001 slice subset:
   - `getTierW`, `scoreRaw`/`scoreDomains`, `averageProfile`, `classifyCluster` + bonus, `calcAnxietyRisk`, `findStrains` + its one retry
   - direct `INTENTS` key lookup
   - `TIER_DEFAULTS` + day deals + tax
   Rules for the port:
   - Pure C# (`noEngineReferences`). Constants live in data or config, not scattered literals.
   - Every function cites its source function name in a comment.
3. **Golden tests.** EditMode NUnit tests replay the slice goldens (RC-01, RC-03, RC-04, RC-09, RC-10, RC-11, X-04, X-05, X-07, X-18, `pricing`, `batchScores`) from `golden_cases.json` against the imported catalog.
   - Where the game intentionally fixes a defect (GAP-206 "sleeping", MC-7, V73-NT5), keep the v7.11.4 expected value and add a separate "game-expected" assertion. Record each in `Docs/DECISIONS.md` as proposed DEC entries in your handoff; the Hub writes the final ones.

## Validation
- `studio.ps1 unity-compile` and `unity-test-edit` pass, with all slice goldens green.
- Importer determinism shown: two runs, same md5.
- The PII allow-list check passes.

## Handoff
`Docs/Handoffs/GAME-001.md` (≤40 lines). Report to the Studio Hub.
