# REVIEW-W4T — QA-002 TFS parity Gate A + DP scenario harness

**Verdict: GO (PASS with minors).** Branch `review/wave-4t` (off `main` 4fcf7a7) merges `claude/zealous-newton-0a5d6b` @ e32a9f9 cleanly (merge 55a6556). Reviewer: UX-002 workcell session, 2026-10-30.

## Validation run here
- `studio.ps1 unity-compile`: `csErrors=0; CompileCheck OK`.
- `studio.ps1 unity-test-edit`: **175/175 passed** (`Artifacts/TestResults/20261030-024117-241-40296-editmode.xml`), matching the worker's count. DEC-013 slot wait respected (2 other editors were running; studio.ps1 queued the run).
- **Independent mutation probe** (local only, reverted, not committed; different from the worker's tier-filter probe): `ShiftSim.Recommend` swapped the top two cards whenever a rush customer was queued. Result **171/175**. The 4 failures were all Gate A tests: `SliceChips_CardsEqualFreshEngine(midShiftFullQueue / rush / hardConfigRush)` and `SellOut_IsTheOnlyAllowedChange`. Every pre-existing slice test still passed, so the gate catches a gameplay-dependent rerank that nothing else did. It is not trivially passable.

## Packet `Docs/Tasks/Active/QA-002.md`
| Deliverable | Result |
|---|---|
| 1 Engine-level gate: chips + parser queries identical in fresh / mid-shift full queue / rush / gameplay keys changed; sell-out the only allowed change | ✔ `SliceChips_CardsEqualFreshEngine`, `ParserQueries_SameAnswerInEveryState` (all distinct `golden_cases.json` queries, guarded by `n > 30`), `SellOut_IsTheOnlyAllowedChange`. Each state asserts it was really reached (`TickUntil`, ≤ 5000 ticks, customer at the counter) and that no sales happened. Fingerprint = key, Ms to 4 dp, rep batch, plus outcome, role tags, card and near list for parser answers |
| 2 Input gate: `Search` gets only the chip; hidden fields never change results; hook for GAME-017 | ✔ signature check by reflection + 12 hidden variants per chip (`TrueFamily`, `Budget` 0/1/35/10000, patience, rejections); `HiddenVariants` public with a GAME-017 note |
| 3 Scenario harness + one sample (DP-020) | ✔ `DpScenario` JSON format documented in `_doc`; catalog md5 guard; stock set through the real `Inventory.Sell`; DP-020 checks the query, sold-out batch and strain absent, 3 cards, Bought |
| 4 The rule in the handoff | ✔ "Every gameplay PR keeps `TfsParityGateTests` green" (DEC-058) |
| No production edits / no `Code/Domain/` | ✔ diff = new `Tests/EditMode/Gates/` (own asmdef), `Data/Tests/DpScenarios/`, handoff. Domain, Simulation and goldens untouched |

The baseline is never self-comparing: `DpScenario.Data()` loads a new `Catalog` on every call, and `Fresh` is a separate instance from every sim's catalog.

## DEC-052..058, DEC-060
- **DEC-058** (Gate A rule): implemented and stated. ✔
- **DEC-057** (chip-only queries equal the DEC-017 goldens): the DP-020 scenario pins the sleep chip's crit/neg/primary; the chip gate compares every chip against the engine with the chip's own golden crit/neg. ✔
- **DEC-052/055/061**: nothing here touches evaluation or backstock; the sell-out test encodes today's "jar = all stock" rule, which DEC-055/061 keep for the slice. ✔
- **DEC-060 (ship the v7.11.5 fixes; v7.11.4 goldens stay as regressions):** the absolute lock still comes from the existing `EngineGoldenTests` (v7.11.4 + the `EmptyTierCountsAsHouse=false` case) and `ParserGoldenTests` (v7114 set + `ParserOptions.Game` defect goldens). They are unchanged and green. Gate A is relative by design (sim vs fresh engine), so it complements them; it cannot replace them. See m1.

## Findings (none blocking)
- **m1 — Gate A parser pass uses only the default (v7.11.4) parser options.** `ParserQueries_SameAnswerInEveryState` and the sell-out loop call `Responder.Ask(…)` without `ParserOptions.Game`, while DEC-060 ships the Game options and GAME-017 will route queries through `QueryParser`. Add a second pass with `ParserOptions.Game` (and include the `golden_cases_game003.json` defect queries) before GAME-017 merges.
- **m2 — DEC-058 should name the golden suites too.** Gate A is relative, so an engine change that alters every catalog equally passes it. Suggested DEC-058 wording: "every gameplay PR keeps `TfsParityGateTests`, `EngineGoldenTests` and `ParserGoldenTests` green."
- **n1:** `DpScenario.Data()` loads `parser_tables.json`, which the production `SliceData.Load` leaves out (commented). That's fine for the parser gate, but scenarios run on a slightly different load path than the game. Note it when GAME-017 adds the parser to the slice load.
- **n2:** the `MoreOptions` pages are not compared against the engine, and the scenario runner clears `sim.Sales` after setup. Both are already disclosed in the handoff with an upgrade path.

## For the Hub
Merge on GO. Fold m1 into GAME-017's packet (or a small QA-002b), and decide m2's DEC-058 wording.
