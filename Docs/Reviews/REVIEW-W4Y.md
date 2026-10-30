# REVIEW-W4Y — QA-002b (Gate A parser pass under V7114 and Game options)

**Verdict: PASS (GO to merge).** `claude/task-qa-002b` @ 45a1031 merged `--no-ff` into `review/wave-4y` off main 0fca821; clean. Tests only: 2 files changed (`TfsParityGateTests.cs` +21/−6, the handoff). No `Code/Domain/` or `Simulation/` edit.

## What changed
`ParserQueries_SameAnswerInEveryState` (4 states) and the sell-out loop in `SellOut_IsTheOnlyAllowedChange` now run every query through `Responder.Ask(..., options)` for both `ParserOptions.V7114` (parity) and `ParserOptions.Game` (DEC-060), on the fresh catalog and on the sim's live catalog. `GoldenQueries()` is `golden_cases.json` plus both queries of each `golden_cases_game003.json` defect (MC-7 "something for the day", GAP-206 "trouble sleeping but gotta work at 6"), de-duplicated. The query-count guard rose from > 30 to > 60. This closes W4T m1 and DEC-067's Game-pass requirement.

## Gates (single editor via `studio.ps1`, DEC-013)
- `unity-compile` csErrors=0. `unity-test-edit` **185/185** (same test count as before; the parser gates now cover both modes).

## Mutation probe — the Game pass is not trivially passing
In `ParserQueries_SameAnswerInEveryState` I made the sim side always use `ParserOptions.V7114` while the fresh side used the mode's options (temporary edit, reverted with `git checkout`; tree clean). Result: **4 failures, all in Game mode, one per state, all on `'something for the day'`**; the V7114 pass stayed green. So the Game pass is sensitive to the Game-specific behaviour, and the MC-7 defect query separates the two modes. (A failure stops at the first mismatch per state, so GAP-206 was not reached; I did not probe it separately.) The sell-out loop shares the same query list and options but I did not mutate it independently.

## Limits worth knowing (not blockers)
- n1 (W4T n1, **for GAME-017**): the gate and scenario loader (`DpScenario.Data`) builds the catalog **with** `parser_tables.json`; production `SliceData.Load` does not pass the parser JSON (`Catalog.Parser` is null). The handoff records this, but the GAME-017 packet does not mention it. Add one line to GAME-017: free-text parsing in gameplay needs `SliceData.Load` to load the parser tables, or the gate stops mirroring production.
- n2 Gate A is relative by design (sim vs a fresh engine with the same options), so it cannot catch a bug that both sides share; the absolute lock stays `EngineGoldenTests` and `ParserGoldenTests` (DEC-067 keeps all three green).
- n3 The Game pass covers 2 defect queries plus the MIG-001 set. New Game-only defects need a row in `golden_cases_game003.json`; they are picked up automatically.
