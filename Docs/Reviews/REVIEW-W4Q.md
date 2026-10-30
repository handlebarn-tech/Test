# REVIEW-W4Q — DES-003 decision-pressure spec intake (docs only)

**Verdict: PASS with minors.** Branch `review/wave-4q` (off `main` f5bad86) merges `claude/task-des-003-bb569f` @ f97e8c8 cleanly (16 files, docs only; no code, no Hub-owned files). Reviewer: UX-002 workcell session, 2026-10-30.

## 1. Verbatim copy
`Docs/Design/SPEC_DECISION_PRESSURE.md` vs `C:/Users/handl/Downloads/DECISION_PRESSURE_CUSTOMER_INTELLIGENCE_PROGRESSION_MANAGEMENT_SPEC.md`: after stripping CR (the repo copy is CRLF), the **only** difference is the 2 prepended lines ("Proposed by Nolan 2026-10-30; integration status in DES-003 handoff" + blank). 4651 source lines, all present, through §135. ✔ The handoff's "lines 1–4652" is off by one (the source has 4651); harmless.

## 2. Classifications spot-checked against the repo (18)
| Row | Claim | Repo evidence | OK |
|---|---|---|---|
| map | `CustomerOutcome { Bought, Walkout, NoSale }` | `Customers.cs:8` (+ `None`) | ✔ |
| map / §26 | `Response` has 4 values | `ShiftSim.cs:27` Blocked/Accept/Reject/Leave | ✔ |
| §3 PART | `Customer` has family, grams, budget, archetype, patience only | `Customers.cs:11-29` | ✔ |
| §19 PART / DEC-P1 | `Fit` = TFS `FindStrains` on the true family, Ms/Ms_top, relaxed pass | `ShiftSim.cs:205-217` | ✔ |
| 0A IMPL | `Search` sends only the player's chip | `ShiftSim.cs:95-104` (`Recommend(chip, …)`) | ✔ |
| 0A PART | evaluation lives beside search, unlabelled | `Fit`/`Satisfaction` in `ShiftSim` | ✔ |
| §2.5 MISS | no-sale only after `maxRejections`, no credit | `ShiftSim.cs:130` | ✔ |
| §41 PART | only LOW / SOLD OUT states | `InventoryService.cs:57-58` | ✔ |
| §44 CONFLICT (latent) | jar 0 g → `SetInStock(false)` | `InventoryService.cs:70` | ✔ |
| §45 / DP-020 IMPL | sold-out test exists | `SliceTests.cs:206 SoldOutBatch_NeverReturned_StrainKeepsNextBatchAsRep` | ✔ |
| §106 CONFLICT | stars = `AvgSatisfaction` cut-offs | `ShiftSim.cs:252` | ✔ |
| §107 PART | `RoughShift` exists | `ShiftSim.cs:253` | ✔ |
| §6 PART | opener + core + weight + budget always rendered | `Customers.cs:57,65 RenderLine` | ✔ |
| §39 PART | `patienceWords` | `SliceData.cs:78` | ✔ |
| 0A PART (workflows) | `Responder`, `Similarity`, `Refine` ported | `Domain/Engine/Features/*.cs` | ✔ |
| §9 PLAN (5 of 8) | GSS §49 has 5 questions | main GSS §49: experience, functional, budget, avoid, liked last time | ✔ |
| §40 / §60 CONFLICT | GSS §40 added a learned adjustment to the score | main GSS §40 | ✔ |
| 0A CONFLICT N1 | DEC-015 ships v7.11.5 `EmptyTierCountsAsHouse=false`; DEC-016 parser fixes | `DECISIONS.md` lines 19–20 | ✔ |
Counts recomputed from the table: MISS 55 · PART 38 · PLAN 31 · IMPL 13 · CONFLICT 9 = 146, matching the stated counts. The §123 row's workcell mapping matches spec §123 (DP-001 info model → GAME-017, DP-002/003 evaluation/resolution → GAME-019, DP-005 restock → GAME-012, DP-006 memory → GAME-021, DP-007 difficulty → GAME-022, DP-008 analytics → GAME-020, DP-009 career → GAME-024, DP-010/011 → PS4).

## 3. TFS boundary (DEC-001/002, spec §0A)
- Every new GAME packet says "No `Code/Domain/` edits"; GAME-018 calls the ported `Responder`/`Similarity` as they are; GAME-022 "no profile key may reach engine options"; GAME-021 tests "no hidden reranking". ✔
- The only engine call with hidden truth is the evaluation oracle (`ShiftSim.Fit` today → `ServiceEvaluator`, DEC-P1). It never feeds the cards; QA-002's input gate and Gate A lock that. ✔
- SPEC_GAME004 §4 note makes `concentrateFitFactor` evaluation-only and the strain-less match a neutral-sorted filter (DEC-P3). ✔
- GAME-017's query composer sends known facts as wording through `QueryParser`, with chip-only queries required to equal DEC-017 goldens (DEC-P6). That is the player's input, not a reinterpretation of output. ✔
- **n2:** GAME-020's debug panel may show oracle values; keep them dev-only and labelled "evaluation" (packet already says TFS vs gameplay labelled; keep it out of player UI).

## 4. Duplicates and dependencies
- No duplicate systems: `Customer`, `Response`, `CustomerOutcome`, `InventoryService`, `ShiftReport`, satisfaction and `acceptThreshold` are extended, not replaced. PS1 packets GAME-006..010, UX-002 (`UX_PS1.md`) and DES-002/SPEC_COMP002 are untouched. UX-005 extends `UX_PS1.md` (UX-002 is now merged, so UX-005 is unblocked). DP-005 restock was folded into GAME-012, not a new packet. ✔
- In-flight work: GAME-017+ wait for GAME-006/007/010 (same `Simulation/Slice/` files); GAME-005 (jars), PROC-003 and ART touch none of the PS1b files; QA-002 writes only a new `Tests/EditMode/Gates/` folder. ✔
- **m1 — ID collisions:** `QA-002` is already used for different items in `TOOLCHAIN_EXECUTION.md:1251` (screenshot harness) and `UNITY_MIGRATION_PLAN.md:869` (save suite). The packet notes it and leaves renumbering to the Hub. Pick one: renumber the new packet, or mark the old plan entries superseded.
- **m2 — state of GAME-021..024:** they are filed as Ready while their dependencies are unmerged; **GAME-023 depends on GAME-011/012**, which have no packets yet (Later, after DES-004). GAME-023 should be "Later" or "Blocked on GAME-011/012", or the Hub will dispatch it too early.

## 5. Edits to existing docs
- GSS: 57 + / 19 −. Every removed line is replaced by a narrower or cited version (§8 profile → TRUE profile = `Customer`; §16 oracle wording; §28 per-archetype strategy; §40; §72 list punctuation; §92 and §100 extended). No rule lost.
- **m3 — §40 removed ahead of ratification:** the learned-adjustment text and "It cannot completely override chemistry/inventory rules" are gone, replaced by the DP §60 rule labelled "proposed DEC". The new rule is stricter and is Nolan's own spec, so the result is safe, but the Hub should ratify **DEC-P2** at merge so GSS and DECISIONS agree. Also "fast recommendation" dropped from the §28 list (now "Floor Mode, short questions and fewer comparisons"): **n1**, add it back.
- ROADMAP: §2b PS1b added; PS2 rows extended with DP refs; DES-003 → DES-004 rename; PS2 exit 20–30 → 25–40 min (DEC-P5). Old row text kept within the new rows. ✔
- SPEC_GAME004: one added note, nothing removed. ✔

## Hub actions
Ratify or reject DEC-P1…P6 + the Gate A rule (DEC-P2 at merge, see m3; DEC-P4 blocks GAME-012, DEC-P3 blocks GAME-015). Resolve m1 (QA-002 ID) and m2 (GAME-023 state). Forward N1 and N2 to Nolan. Add BACKLOG rows per the DES-003 handoff.
