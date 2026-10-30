# REVIEW-DATA3: DATA-003 customer needs catalog + golden parses

**Reviewer:** Unity pool · **Requested by:** Gameplay lead · **Date:** 2026-10-30
**Reviewed:** `worktree-agent-afbc722989beda3b0` @ 996c631 (DES-006 merged in), merged onto `review/data3` from main dbbf3c0 (merge 72124a3, no conflicts).
**Sources:** `Docs/Tasks/Active/DATA-003.md`, `Docs/Handoffs/DATA-003.md`, diff, GOLDEN_CASES.md "Needs goldens".

## Verdict: PASS with minors

## Checks
1. **Citations (Hub rule).** SliceNeeds holds no store facts. The budgets `under $30` and `under $40` are customer wording, not shop values. `{strain}` is filled from the catalog's first card. The dialogue is labelled [GDD]. The merged DES-006 audit cites tool lines (`T:`) and code lines for every engine claim. No uncited store values.
2. **Generator reproduces.** `node Tools/Data/golden_game003.js` exits 0 and reports 12 needs and 564 cases (ok 514, help 50). After git's line-ending normalization, `golden_cases_game003.json` and `golden_cases_needs.json` match the committed files exactly (`git diff --quiet`). `golden_cases.json` is untouched.
3. **No hand-written parses.** Every case in the needs golden comes from `run()` in the generator. The `meta.generator` field names the generator.
4. **No PII or invented data.** The needs contain no strain or product names, no prices beyond what customers say, and no people. Customer lines are generic written dialogue.
5. **Schema.** The GOLDEN_CASES.md section documents `join`, `styles`, `needs`, `components`, `terms` and `say`, the picker rule, and the rules the generator enforces. It matches the generator code.
6. **Term-join coverage.** `Golden_CoversEveryPickerQuery` rebuilds every in-order component subset, each with one term or one said line, the same way JS `pickerQueries` does. It asserts that the set equals the golden's `queries` and that each query has a captured case. `ParseAndAnswer_EqualTool` replays every case.
7. **Unity EditMode** (`studio.ps1 unity-test-edit` on 72124a3, run after BUILD-007 freed its slot, so one editor at a time): 782 total, 780 passed, 0 failed, 2 skipped. NeedsGoldenTests passed 565/565. Gate A passed: TfsParityGate 11, EngineGolden 23, ParserGolden 95. The ProcArt LODGroup failures the worker reported (JarFill 6, PackagedGoods 14) **pass** here. They were first-import failures in the worker's fresh worktree, not caused by this change. Result: `Artifacts/Results/20261030-074957-023-780-unity-test-edit.json`.

## Minor findings (non-blocking)
1. `SliceNeeds.json` `_doc` contains a double-encoded "§" (`Â§3, Â§5`, bytes C3 82 C2 A7). The same mojibake is already on main in ART-005 and REVIEW-W4F/W4M. Fix it the next time the file is edited.
2. `GOLDEN_CASES.md` has no newline at the end of the file.
3. The C# `Queries` and JS `pickerQueries` copies must stay in step by hand (a comment says so). Drift fails the coverage test, so the risk is low.

## Notes for the lead (from the handoff, design questions, not review findings)
- Handoff note 1: in `insomnia_work`, the "gotta work" component does not change the oracle under GAP-206.
- Handoff note 4: GAME-017a must join query pieces with `", "` and keep said lines verbatim, or the goldens stop covering its queries.
