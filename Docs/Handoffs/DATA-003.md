# DATA-003 handoff: customer needs catalog + golden parses

**To:** Gameplay lead · **Branch:** `worktree-agent-afbc722989beda3b0` (DES-006 branch merged in first) · **Status:** complete, ready for Unity-pool review

## Done
- `UnityProject/Assets/_Game/Data/Slice/SliceNeeds.json`: 12 needs (6 DEC-017 families × 2 modifiers, audit §5), 2 components each, 2-3 terms per component with one `true`. Styles: every need has direct, vague, wrongTerm and story; productRef appears in `stress_functional` and `pain_functional`, lastTime in `pain_budget`, contradictory in `insomnia_work`. Lines are written [GDD] dialogue. The data holds no strain names (`{strain}` is filled at runtime) and no store or product facts.
- `Tools/Data/golden_game003.js`: after the unchanged game003 output it validates the needs (rules in GOLDEN_CASES.md "Needs goldens") and writes `Docs/Reconstruction/golden_cases_needs.json`. That file has 564 distinct captured queries (514 ok, 50 help), covering every term, term-join and verbatim said line the picker can build. Two runs gave the same md5 (`b31c4a3d…`). `golden_cases.json` and `golden_cases_game003.json` are unchanged (`git diff --exit-code` clean; Node rewrites game003 with LF, which autocrlf normalizes).
- `Docs/Reconstruction/GOLDEN_CASES.md`: schema section appended.
- `Tests/EditMode/Gates/NeedsGoldenTests.cs`: `ParseAndAnswer_EqualTool` (one case per golden query: parse fields, outcome, findStrains calls/ms, shown, role tags, show-more) via `Responder.Ask(..., ParserOptions.Game)`. `Golden_CoversEveryPickerQuery` fails if the data and the golden drift apart.

## Validation
- `node Tools/Data/golden_game003.js`: passes; the generator's rule checks pass.
- Unity EditMode (`studio.ps1 unity-test-edit`): 774 total, 752 passed, 20 failed, 2 skipped. All 565 NeedsGoldenTests pass (564 cases + coverage), and Gate A (TfsParityGateTests, EngineGoldenTests, ParserGoldenTests) passes. The 20 failures are the known ProcArt "no LODGroup" first-import failures (JarFill 6 + PackagedGoods 14; see BRAND-001, REVIEW-W5H). This change touches no ProcArt, FBX or importer code. Result: `Artifacts/Results/20261030-073050-114-15320-unity-test-edit.json`.

## Gate A findings (C# parser vs tool)
None. All 564 captured queries match the C# `QueryParser`/`Responder` under `ParserOptions.Game`: parse, outcome, findStrains calls and ms, cards, role tags and show-more. That includes the 50 Help outcomes, the strain lookups and the like-X parses.

## Notes for the lead (design, not blockers)
1. `insomnia_work`: under the game parser, `"insomnia, gotta work"` parses the same as `"insomnia"`. The GAP-206 fix keeps a sleep ask and drops the work cap, which is tool behaviour. The "gotta work" component therefore changes nothing in the oracle; only the wrong readings ("stay functional", "no couch lock") change the result. Keep it as a contradictory-style teaching case, or swap the modifier.
2. `"first time"` overrides the effect numbers (anxiety 55 / sedation 20 / uplift cap 50). In `anxiety_first_time`, "stress", "calming" and "relax" therefore all reproduce the need, so the wrong effect terms are "wind down" and "sleep".
3. The like-X route only parses in the form `like {strain} but for X`. "X, like {strain}" and the productRef said lines go to strain lookup. The like-terms are alternate readings, not the true term, so `trueQuery` never depends on the runtime strain.
4. Join rule: said lines enter the query verbatim, including their final punctuation (e.g. `"Something for sleep., under $40"`). The parser ignores the punctuation. GAME-017a must use the same rule (`join`) or the goldens stop covering its queries.
5. Not captured: queries with a runtime `{strain}` other than `strainFill` (the trueQuery's first card). GAME-017a should treat other fills as live parser calls, not golden-backed ones.

## Questions for Nolan (through the Hub)
None. Searched `Docs/DECISIONS.md`, `Docs/KNOWN_GAPS.md`, `Docs/Handoffs/REF-008.md` and `Docs/Research/` for GAP-206, "gotta work", the join rule and budget wording (DEC-105). Nothing open; the notes above are for the lead to decide.
