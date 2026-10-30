# GAME-017a — First playable recommendation depth (playtest 2 cut)

**Role:** GAME · **Priority:** P0 · **Branch:** `claude/task-game-017a` worktree off `main` once GAME-025 and DATA-003 have merged (GAME-025 owns `SliceGame.cs`/`SliceView.cs` until then: never concurrent) · **Owner:** — · **Reviewer:** fresh, Hub-spawned (STUDIO_OS §0.7)
**Touches:** none · **Interfaces:** `Data/Slice/SliceNeeds.json` + `Docs/Reconstruction/golden_cases_needs.json` (DATA-003), `Docs/Specs/UX_COUNTER_INTEL.md` §13 (UX-006)

## Goal
Remove "pick one effect, pick one strain, done" (DEC-096). A sale needs *hear → interpret → (ask) → search the tool's way → read the cards → react to a follow-up*, through the real `QueryParser`/`Responder`.

## Read
`Docs/Design/RECOMMENDATION_DEPTH_AUDIT.md` §1, §3, §5 (this packet's scope is §5 "In"; "Out" stays in GAME-017..020); `Docs/Specs/UX_COUNTER_INTEL.md` §13; `Docs/Handoffs/DATA-003.md` (schema and design notes); `Docs/Specs/CONTROLS_FLOW_PS1.md` (Esc = pause, Backspace = back); `Docs/Design/TONE.md` (customer lines); DEC-001/017/052/057/067/105 in `Docs/DECISIONS.md`; DEC-118 in `Docs/DECISIONS.md` (the DES-006 Q1–Q5 and UX-006 U1–U6 rulings).

## Owns
`Simulation/Slice/Customers.cs`, `ShiftSim.cs` (Search/MoreOptions route, Fit overload), `SliceData.cs` (load needs), new `Simulation/Slice/CustomerKnowledge.cs` (minimal said/term KNOWN; GAME-017 extends it); `Presentation/Slice/SliceGame.cs`, `SliceView.cs`, `UI/Slice/` styles; `SliceLines.json`/`SliceConfig.json` (new keys only); `Tests/EditMode/Slice/` (new tests + `SlicePersonaTests.cs` bots); `Docs/Specs/UX_COUNTER_INTEL.md` §13 (REVIEW-UX6 fixes only); `Docs/Handoffs/GAME-017a.md`. No `Code/Domain/` edits (DEC-001). `SliceNeeds.json` and the goldens are read-only here: changes go back through DATA-003's generator.

## Deliverable
RDA §5 "In" items 2–7 (item 1 is DATA-003, merged), plus:
1. Tool wording is copied into the game here (DEC-118 U5), keyed to tool lines. That includes REVIEW-UX6 m1: nearLabel = T:16554 "In stock and close to it[, without X]:", notFound = T:16544 "Strain not found.". REVIEW-UX6 m2: add reject → Query and the Q6/Q7 key reservation to §13.9. REVIEW-UX6 m3: the route line follows the engine's `maxPrice` (T:16632).
2. Runtime `{strain}` fill uses only strains that have a captured golden (DATA-003 note); anything else is a GAP in the handoff, not an uncaptured query.
3. New-customer toggle included in the parser-input snapshot hash (DEC-118 Q3).
4. **Slice goldens change** (REVIEW-DES6 m1): regenerate them, list old → new in the handoff, and get QA sign-off from the reviewer before merge.

## Validation
Compile; EditMode + PlayMode green (the known ProcArt LODGroup failures, which belong to Assets, are listed but not fixed); Gate A with `ParserOptions.Game` (DEC-067); NeedsGoldenTests green; unity-capture with the picker, query preview and follow-up visible at 100/125/150 %; DEC-013 gate, Gameplay's one Unity slot.

## Handoff
`Docs/Handoffs/GAME-017a.md` (≤40 lines). Questions only after the DEC-105 search (list what you searched); report to the Hub; never ask Nolan (DEC-033).

## Also (Hub, 2026-10-30): playtest-2 #13
`Docs/Design/PLAYTEST2_2026-10-30.md` #13: the interface is still too restrictive. Keep natural-language intent, modifiers and negations, and flexible recommendation behaviour from the tool (DEC-001/002) rather than a rigid menu. This packet's scope is unchanged; where a §5 "In" item could be built either way, take the free-text / parser route. Verify in the built player (DEC-120 (4)).
