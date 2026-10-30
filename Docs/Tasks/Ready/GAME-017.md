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

## Handoff
`Docs/Handoffs/GAME-017.md` (≤40 lines). Questions go to the Studio Hub (DEC-033).
