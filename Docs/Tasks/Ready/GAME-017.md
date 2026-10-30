# GAME-017 — Customer knowledge: TRUE vs KNOWN profile, questions, query composer

**Role:** GAME · **Priority:** P1 · **Branch:** `task/GAME-017` worktree off `main` (after GAME-006 and GAME-007 merge — same `Simulation/Slice/` files; after GAME-010 merges — it owns the persona bots and SliceConfig values; QA-002 merged; UX-005 for the view layer)

## Goal
Spec DP-001 (`Docs/Design/SPEC_DECISION_PRESSURE.md` §3–18, §27, §35): the player learns customer facts by openers, questions and follow-ups, and only those facts reach the TFS engine. Difficulty comes from incomplete queries, never from a wrong top card (§18).

## Read
SPEC_DECISION_PRESSURE §0A, §2.2, §3–18, §27, §35, §115 (DP-001/002/003/010/011), §125; `Docs/GAMEPLAY_SIMULATION_SPEC.md` §8, §49–51, §92–93 (amended by DES-003); `Docs/Design/DES-003_RECONCILIATION.md` (name mapping); `Docs/Specs/SLICE_DESIGN.md` §2, §11; `Docs/Handoffs/GAME-003.md` (`QueryParser`, `Responder`); `Docs/Specs/UX_COUNTER_INTEL.md` (UX-005); DEC-016/017.

## Owns
- `Assets/_Game/Code/Simulation/Slice/`: extend `Customer` with the TRUE fields; new `CustomerKnowledge.cs` (KNOWN profile, `KnownField`, `RevealSource`, questions, completeness/risk), query composer; `CustomerGenerator` reveal sets and tiers
- `Presentation/Slice/` question menu + KNOWN strip per UX-005
- `SliceConfig.json`, `SliceLines.json` (new keys only), new `Data/Slice/SliceQuestions.json`
- `Tests/EditMode/Slice/` new tests; persona bots (extend GAME-010's harness: the perfect bot must now ask, not read `TrueFamily`)
No `Code/Domain/` edits (DEC-001).

## Deliverable
1. TRUE fields on `Customer` (keep the class and `TrueFamily`): avoidances, price sensitivity, time of use, similar reference (strain key + batch), experience/knowledge, decision confidence, talkativeness, `DesiredConsultationDepth`, `QuestionTolerance`, compromise/substitution tolerance, ambiguity tier 0–4. Product preference only as a placeholder until PS3. Values seeded from per-archetype ranges in SliceConfig [GDD; spec §11 table as starting values].
2. KNOWN profile per customer: each field `{isKnown, value, confidence, source}`; `QuestionsAsked`, `ConsultationSeconds`, `RevealedFields`; opener reveal sets in data (§6) — the existing opener + core + weight + budget line becomes one reveal set (tier 0/1) so today's customers still play the same.
3. Questions Q1–Q4, Q6–Q8 (§9) as data `{id, targetField, text, baseTimeCost, toleranceCost, relevantWhen, revealRule}`. A question on a known field reveals nothing and still costs time (§10). Excess questions add escalating friction: patience/service hits and the §12 deflection lines, never instant anger.
4. `InformationCompleteness` (§15 weights, relevant fields only) and `InformationRisk` (§16) computed on reveal events only (§122); gameplay/debug values, never fed to the engine.
5. **Query composer:** KNOWN facts → canonical customer wording → `QueryParser.Parse` (parser options as DEC-016 sets them today) → the ported engine. A chip-only query must reproduce today's DEC-017 golden parse exactly. Hidden fields never appear in the composed text (extend QA-002's input gate).
6. Follow-up hook: `Reveal(field, source)` callable by GAME-019's ASK_* responses (§27).
7. Counters for §35: relevant / irrelevant / repeated questions, critical fields revealed.

## Validation
Compile / EditMode / PlayMode green; QA-002 gate green; slice goldens unchanged. Tests (QA-002 harness scenarios): DP-001 (explicit customer, zero questions, fast), DP-002 (hidden "stay functional" → refined query; both result lists equal the engine's own output for those queries), DP-003 (redundant budget question: no info, time spent), DP-010 (question spam on a low-tolerance explicit customer), DP-011 (zero questions on a tier-3 customer leaves the query incomplete). Seed determinism. DEC-013 gate.

## V2 additions (IMP-002, DEC-063)
V2 = `Docs/Design/DESIGN_V2/` (Nolan's add-on; DP wins on conflicts, DEC-063a). Row n = `Docs/Imports/IMP-001_DESIGN_V2_AUDIT.md` §2 row. All V2 numbers are [GDD] starting values (GAP-DP-02). Exploit tests: `DESIGN_V2/QA_TEST_PLAN.md`.
- Constraint classes hard / soft / context / hidden-but-revealable; every hidden critical fact has a legitimate reveal route (V2 `02_CUSTOMER_GENERATION_BIBLE.md` §4, §12; row 12).
- Compatibility rules: fields are not sampled independently, e.g. hard budget + price-insensitive is invalid; exact prior-item requests need repeat history (V2 02 §9; row 16).
- Generation retry cap 12, then degrade toward a solvable customer (V2 02 §8; row 15).
- Anti-repetition over rolling 20- and 50-customer windows (V2 02 §14; row 20). Test: a seeded 50-customer run passes or reports the rule it could not meet.
- Named RNG streams from the shift seed (arrival, profile, dialogue, patience, outcome, supplier, event): adding a dialogue line must not change arrivals (V2 `01_SYSTEM_CONTRACTS.md` §3; row 3).
- `KnownField` also records `revealedAt` (V2 01 §4; row 4).
- **Ambiguity stays DP tiers 0–4** (audit C1). V2's 0–3 shares are re-mapped in GAME-022.
- Customer openers and examples are customer speech and pass copy rule H1 (V2 02 §13; row 19).
- Exploits: EX-001, 003, 012, 055, 056, 059 (V2 `10_EXPLOIT_FAILURE_ANALYSIS.md`; row 45).

## DES-006 amendments (recommendation depth, DEC-096)
Source: `Docs/Design/RECOMMENDATION_DEPTH_AUDIT.md` (cited **RDA§n**; tool lines `T:n` are cited there). These bind over D1, D2 and D5 where they differ. No `Code/Domain/` edits (DEC-001); Gate A (DEC-067) unchanged.
- **Phase A = GAME-017a** (RDA§5, first playable depth) may be cut out and merged first. This packet then builds on it and does not redo it.
- **TRUE need** (RDA§3.1): new `Data/Slice/SliceNeeds.json`: each need has a `trueQuery` in tool vocabulary plus components, with spoken variants per style and 2–3 terms each. Parses are golden-captured on v7.11.4 with `ParserOptions.Game` (extend `Tools/Data/golden_game003.js` → new `Docs/Reconstruction/golden_cases_needs.json`). Never hand-written. `TrueFamily` = the need's base family. Added to Owns: `SliceNeeds.json`, the golden script and file.
- **Utterance styles** (RDA§3.2): direct, vague, wrong term, story, product reference, "last time", contradictory → reveal sets and tiers 0–4. `{strain}` slots come only from the live game catalog.
- **KNOWN keeps the customer's words** (RDA§3.5): `KnownField` adds `said` (verbatim) and `term` (the player's reading). A direct phrase is its own term.
- **"Note it as…" picker** (RDA§3.3): per said card, `Their words` or one of the component's terms; [GDD] time cost; no correctness feedback anywhere.
- **Composer (replaces D5's source):** it joins the player's chosen terms and verbatim phrases, never wording generated from structured fields. Route `QueryParser.Parse(ParserOptions.Game)` → `Responder.Respond`. Show every tool outcome as the tool words it: Ok, Fallback, None, Help (`T:16677`), AskEffectForBudget (`T:16662-16667`), PriceOnly, Strain + Near, ExclusionNote, Drive line. Chip-only still equals the DEC-017 golden.
- **Avoid:** a domain avoid ("too sleepy") is a negation phrase; a terpene avoid ("no {terpene}") is an exclusion (`T:15975-15999`). The need data says which.
- **Q9 "Ever gotten anxious from it?"** (tool follow-ups `T:2263-2264`, `T:2297-2298`): reveals Experience. Once known, the player may set the tool's **New customer** toggle → `ShopState.NewCustomer` (`T:1585-1589`, `T:14827-14845`). The toggle is part of the parser-input snapshot hash (DES-006 handoff Q3).
- **Extra tests:** a wrong reading gives a legitimately different TFS result and a lower Fit; `Their words` on a vague phrase == `Responder.Ask` on that phrase; a potency phrase gives the Help/redirect outcome; every term composition's parse == its golden.

## Handoff
`Docs/Handoffs/GAME-017.md` (≤40 lines). Questions go to your department lead (DEC-033, DEC-094).
