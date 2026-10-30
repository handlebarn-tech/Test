# DES-003 — one-time reconciliation of SPEC_DECISION_PRESSURE

**Source:** `Docs/Design/SPEC_DECISION_PRESSURE.md` (Nolan, 2026-10-30, read in full, 4652 lines). Done once per its §0; normal task/review flow applies afterwards (§0, §132).
**Compared against:** `GAMEPLAY_SIMULATION_SPEC.md` (GSS), `DECISIONS.md`, `PROJECT_STATE.md`, `BACKLOG.md`, `Design/ROADMAP_POST_SLICE.md` (ROADMAP), `SPEC_COMP002.md`, `SPEC_GAME004.md`, `Specs/SLICE_DESIGN.md`, Ready packets GAME-006..010 + UX-002, UX-002 branch `claude/task-ux-002-c4fbb2` (`Docs/Specs/UX_PS1.md`), GAME-010 WIP branch, and the slice code `Simulation/Slice/{Customers,InventoryService,ShiftSim,SliceData}.cs` (read-only).
**Status keys:** IMPL = ALREADY_IMPLEMENTED · PLAN = ALREADY_PLANNED · PART = PARTIALLY_IMPLEMENTED · MISS = MISSING · CONFLICT = CONFLICTS_WITH_CURRENT_DESIGN.
**New packets** (all in `Docs/Tasks/Ready/`): QA-002 TFS parity gate · GAME-017 customer knowledge + questions · GAME-018 TFS workflows at the counter · GAME-019 service evaluation + resolutions · GAME-020 decision telemetry + Service/Flow/Operations · GAME-021 repeat memory · GAME-022 difficulty profiles · GAME-023 decision-pressure acceptance shift · GAME-024 career competency + save v1 · UX-005 counter-intelligence UX. Milestone placement: ROADMAP §2b (new "PS1b Customer Intelligence") and PS2.

## Key mapping of spec names to existing names (spec §0 rule 5)
| Spec concept | Existing structure kept | Note |
|---|---|---|
| TrueCustomerProfile | `Customer` (`Customers.cs`): `TrueFamily`, `Grams`, `Budget`, `Archetype`, `PatienceMax` | extend `Customer` with the missing true fields; no new class unless GAME-017 shows it is cleaner |
| TrueIntent | `IntentFamily` golden parse (DEC-017) | stays the truth; modifiers added as extra true fields |
| CustomerOutcome (what happened) | `CustomerOutcome { Bought, Walkout, NoSale }` | kept; `ServiceResolution` is a new *evaluation* enum beside it |
| Customer response | `Response { Blocked, Accept, Reject, Leave }` + GSS §17 list | extend in place with the ASK_* values (GSS §17 = spec §26) |
| PurchaseThreshold | `SliceConfig.acceptThreshold` | becomes the mean of a per-customer threshold |
| CustomerSatisfaction | `ShiftSim.Satisfaction(...)` (SLICE_DESIGN §3.4) | kept; gains a consultation-depth term |
| TFS alignment component | `ShiftSim.Fit(trueFamily, strainKey)` = TFS `FindStrains` on the true intent, Ms/Ms_top | already a TFS-grounded *oracle* used only for evaluation; moves to `ServiceEvaluator` (GAME-019); proposed DEC-P1 |
| Single inventory authority | `InventoryService` | kept (GSS §30) |
| Shift report | `ShiftReport` | extended by GAME-020 |
| Tool vs player vs purchase | GSS §94 `systemSuggestedCandidates / playerRecommendedBatch / customerPurchasedBatch` | kept; spec §2.2 adds the KNOWN layer |

## Table
| § | Requirement | Status | Existing owner (file / task) | Action |
|---|---|---|---|---|
| 0 | One-time intake, classify, no duplicates | IMPL | this file | done; not to be repeated (§0, §132) |
| 0A | Live v7.11.4 = behavioural contract; local source = implementation authority | IMPL | DEC-001/002/009; `EngineGoldenTests`, `ParserGoldenTests` | none |
| 0A | Unreleased/changed behaviour needs an explicit Nolan decision | CONFLICT | DEC-015 (`EmptyTierCountsAsHouse=false`, v7.11.5 behaviour) and DEC-016 / `ParserOptions.Game` (MC-7, GAP-206 parser fixes) were Hub decisions, not Nolan's | Question N1 to Nolan; meanwhile both stay as recorded (tests keep v7.11.4 goldens) |
| 0A | Forbidden list: no second formula, no domain/terpene reinterpretation, no true-profile rerank, no price override, no parser/exclusion change for difficulty, Similar unchanged, Floor Mode presentation only, no hidden THC/lineage rank, no unavailable eligibility, no outcome-trained model | IMPL (rule) | DEC-001/006; ROADMAP §6; every GAME packet "No Domain edits" | restated in GSS §105; every new packet carries the boundary |
| 0A | GSS §40 learned adjustment added to recommendation score | CONFLICT | GSS §40 | GSS §40 amended to spec §60 (needs Nolan approval for any score change); DEC-P2 |
| 0A | SPEC_GAME004 §4 `concentrateFitFactor` × strain fit and constraint-match "recommendation" for strain-less items | CONFLICT (risk) | SPEC_GAME004 §4 (GAME-015, Later) | boundary note added to SPEC_GAME004 §4: evaluation-only factor, catalog filter not ranking; DEC-P3; decided before GAME-015 starts |
| 0A | Gameplay may control customer words, learned facts, query, workflow choice, stock, pricing, time/queue, retrieval, acceptance, outcome, career | PART | slice: customer line, chip choice, stock, queue/rush, accept | GAME-017/018 add facts, query wording, workflow choice |
| 0A | Only known facts reach TFS; never rerank because the sim knows more | IMPL | `ShiftSim.Search(chip)` sends only the player's chip; `TrueFamily` used only in `Score` | QA-002 locks it with a test |
| 0A | Evaluation layer separate in code, data, tests, UI, docs | PART | `Fit`/`Score` live in `ShiftSim` beside `Search`; not labelled | GAME-019 `ServiceEvaluator`; GAME-020 labels TFS vs gameplay fields |
| 0A | Player chooses Search / Similar / Compare / Floor Mode workflows | PART | engine ported in GAME-003 (`Responder`, `Similarity`, `Refine`); slice UI has chips + Inspect only (SLICE_DESIGN §11 cut list) | GAME-018 + UX-005 |
| 1 | Thesis: several reasonable decisions, none perfect; optimise the store | PART | GSS §4.6, §105; ROADMAP §0 fun gaps 1–4 | GSS §105 extended; PS1b/PS2 packets |
| 1 | Progression arc budtender → manager | PLAN | GSS §44; ROADMAP PS1–PS4 | GSS §44 merged with spec §82–86 |
| 2.1 | TFS deterministic; difficulty never from wrong chemistry | IMPL | GSS §28, §45; goldens | QA-002 (gameplay level) |
| 2.2 | Four layers TRUE / KNOWN / TFS / OUTCOME never collapsed | PART | true = `TrueFamily`, TFS = `Results.Cards`, outcome = `Outcome`/`LastSatisfaction`; GSS §94 | GAME-017 adds KNOWN |
| 2.3 | One inventory authority for every consumer | IMPL | `InventoryService`; GSS §30 | backstock/FOH consumers in GAME-012/014 (PLAN) |
| 2.4 | Some customers have no perfect available resolution | PART | ROADMAP fun gap 1; GAME-010 retune makes budgets bite | GAME-022 `noPerfectFitRate`, GAME-023 scenario |
| 2.5 | A no-sale can be correct and earn credit | MISS | slice `NoSale` only after `maxRejections`, no credit | GAME-019 |
| 2.6 | Customer satisfaction ≠ player performance | PART | slice satisfaction includes `speedFit` and drives stars | GAME-019/020 split DecisionQuality and ServicePerformance |
| 3 | TrueCustomerProfile fields | PART | `Customer` has intent family, grams, budget, archetype, patience; GSS §8 lists most fields | GAME-017 adds avoidances, price sensitivity, time-of-use, similar ref, experience/knowledge, confidence, talkativeness, consultation depth, question tolerance, purchase threshold, compromise/substitution tolerance, flags; product preference waits for PS3; memory ref in GAME-021 |
| 4 | KnownCustomerProfile, `KnownField<T>`, RevealSource, counters | MISS | GSS §93 principle only | GAME-017 |
| 5 | TFS input = known facts + wording + inventory + pricing; keep the NL parser input architecture | PART | slice sends DEC-017 golden crit/neg per chip, not parser text; `QueryParser`/`Responder` ported (GAME-003) | GAME-017 query composer: known facts → canonical wording → `QueryParser.Parse` → engine; chips stay as its base. Hidden-field test in QA-002 |
| 6 | OpenerRevealProfile per opener | PART | `CustomerGenerator.RenderLine` = opener + core + weight + budget (always reveals family, weight, budget) | GAME-017 data-driven reveal sets in `SliceLines.json` |
| 7 | Ambiguity tiers 0–4 | PART | GSS §50; slice customers are all tier 0–1 | GAME-017 tiers; GAME-022 rates |
| 8 | Structured `CustomerQuestionDefinition` | PLAN (concept) | GSS §49; SLICE_DESIGN §11 row 4 ("questions come back with the parser wave") | GAME-017 |
| 9 | Q1–Q8 question set | PLAN (5 of 8) | GSS §49 lists Q1–Q4, Q6 | GSS §49 extended to Q1–Q8; GAME-017 builds Q1–Q4, Q6–Q8; Q5 gated on PS3 (GAME-014) |
| 10 | Redundant question = 0 info, still costs time | MISS | — | GAME-017 (DP-003) |
| 11 | QuestionTolerance per archetype, data-driven | MISS | slice `archetypes[]` in SliceConfig | GAME-017 adds the key per archetype |
| 12 | Escalating excess-question friction + lines | PART | GSS §27 (patience drops on excess consultation); slice patience drains only in queue | GAME-017 |
| 13 | DesiredConsultationDepth | PLAN | GSS §8 field `desiredConsultationDepth` | GAME-017 field |
| 14 | ActualConsultationDepth, ConsultationDepthFit | MISS | — | GAME-019 |
| 15 | InformationCompleteness (weights, relevant fields only); not a TFS score | MISS | — | GAME-017 |
| 16 | InformationRisk; never reranks | MISS | — | GAME-017 compute, GAME-020 debug |
| 17 | Uncertainty shown as CUSTOMER INFO COMPLETE / PARTIAL / NEED MORE, apart from TFS cards | PART | GSS §51 fit wording; slice `fitOk`/`fitFallback` card text | UX-005 status chip; GSS §51 note |
| 18 | Beat top-card autopilot by incomplete queries, never by a wrong top card | PLAN (principle) | GSS §14, §92 last bullet, §93 | GSS §92 reworded; mechanic in GAME-017 (DP-002) |
| 19 | ServiceUtility (game measure, TFS component grounded in TFS output) | PART | `ShiftSim.Score` (fit via TFS oracle, price, speed, wait) | GAME-019 `ServiceUtility` |
| 20 | Hard vs soft service constraints | PLAN / PART | GSS §12; slice blocks on stock (`notEnough`) and 28 g (DEC-036) | GAME-019 formal list |
| 21 | BestAvailableResolution over service actions (not a strain ranking) | MISS | — | GAME-019 |
| 22 | DecisionRegret | MISS | — | GAME-019 |
| 23 | DecisionQuality formula + bands | MISS | — | GAME-019 (`decisionRegretTolerance` config) |
| 24 | Rationale (A vs B) | n/a | — | covered by GAME-019 acceptance (DP-006/007) |
| 25 | Per-customer PurchaseThreshold, not chemistry-derived | PART | global `acceptThreshold` | GAME-019 per-customer draw around it |
| 26 | Response inputs + 9 responses; keep architecture | PLAN / PART | GSS §17 (same 9); slice `Response` has 4 | GAME-019 extends `Response` in place |
| 27 | Customer follow-ups reveal fields | MISS | — | GAME-017 reveal sources, GAME-019 response hooks |
| 28 | NoPerfectFitRate by difficulty | MISS | — | GAME-022 |
| 29 | No-perfect patterns A–G | PART | A budget (GAME-010), B stock (DEC-027 low jars), E quantity (`notEnough`); C/F/G none; D needs PS3 | GAME-022 pattern generator; F needs GAME-018 |
| 30 | INFORMED_NO_SALE player action | MISS | — | GAME-019 + UX-005 |
| 31 | AVOIDABLE_NO_SALE | MISS | — | GAME-019 |
| 32 | ServiceResolution enum (12 values) | MISS | `CustomerOutcome` kept for what happened | GAME-019 |
| 33 | Satisfaction components; no chemistry claims | PART | `Satisfaction` = fit/price/speed − wait; GSS §15, §96 | GAME-019 adds consultation-depth + availability terms |
| 34 | ServicePerformance (DQ .55, QE .15, CDF .10, speed .20) | MISS | — | GAME-020 |
| 35 | QuestionEfficiency counters | MISS | — | GAME-017 counters, GAME-020 report |
| 36 | Rush creates triage | PART | slice rush window, `rushPatienceMult`, queue slots | restock half in GAME-012 |
| 37 | Rush ≠ always fewer questions; per-archetype best play | CONFLICT (wording) | GSS §28 "optimal strategy: short questions, fewer comparisons" | GSS §28 amended |
| 38 | QueueCost (Σ waiting patience loss), hidden, QA only | PART | queued patience drain exists in `ShiftSim.Tick` | GAME-019 sums it per action; GAME-020 logs |
| 39 | Diegetic queue cues; optional accessibility indicator | PART | GSS §27/§46/§98; slice `patienceWords`, `PatienceState` | none new (UX-005 keeps it) |
| 40 | ServiceReady / Back / Total / Reserved stock; deli jar/backstock; packaged FOH/BOH | PLAN | GSS §22; ROADMAP GAME-012; SPEC_GAME004 §2 | GAME-012 row extended |
| 41 | HEALTHY / LOW / CRITICAL / EMPTY_WITH_BACKSTOCK / SOLD_OUT | PART | `InventoryService.IsLow/IsSoldOut` | GAME-012 adds CRITICAL, EMPTY_WITH_BACKSTOCK |
| 42 | LOW threshold | IMPL | `lowStockFraction` | none |
| 43 | CRITICAL from demand | MISS | — | GAME-012 |
| 44 | EMPTY_WITH_BACKSTOCK without redefining TFS stock | CONFLICT (latent) | `InventoryService.Sell` sets `Catalog.SetInStock(false)` at jar 0 g; right today (jar = all stock), wrong once backstock exists | DEC-P4 + question N2; GAME-012 depends on it |
| 45 | SOLD_OUT excluded per TFS rules | IMPL | `SetInStock(false)`; test `SoldOutBatch_NeverReturned...` | none |
| 46 | Proactive / reactive / emergency restock analytics | MISS | — | GAME-012 tags, GAME-020 report |
| 47 | RestockUrgency (internal) | MISS | — | GAME-012 |
| 48 | Don't automate restock; show LOW/CRITICAL/deal/trend | PLAN | GSS §31, §98; ROADMAP UX-003 | UX-003 row note |
| 49 | Quiet periods = preparation | PLAN | GSS §71; ROADMAP GAME-011 | none |
| 50 | Interruptible restock/retrieval task states | MISS | — | GAME-012 |
| 51 | Demand model inputs | PART | slice family/archetype weights; DEC-027 bestseller lows; GSS §29 TrafficDirector | GAME-011 row extended |
| 52 | Imperfect demand signals | PART | GSS §43 top intents | UX-003/GAME-013 rows |
| 53 | CustomerMemory | PLAN | GSS §39 (G6), no task | GAME-021 |
| 54 | PurchaseMemory with TFS context | PART | `SaleEvent`; GSS §37 `recommendationContext` | GAME-020 stores TFS query; GAME-021 memory |
| 55 | Outcome tags | MISS | — | GAME-021 |
| 56 | Repeat dialogue from memory | PLAN | GSS §39 examples | GAME-021 |
| 57 | Memory pre-fills known facts | MISS | — | GAME-021 (RevealSource REPEAT_MEMORY) |
| 58 | Memory confidence / decay / "different today" | MISS | — | GAME-021 |
| 59 | Same strain, new batch: TFS batch logic rules | IMPL (engine) / MISS (memory) | batch-aware engine, `RepBatchId` (DEC-028) | GAME-021 (DP-023) |
| 60 | Learned outcome signals stay out of TFS | CONFLICT | GSS §40 | see 0A row; GSS §40 amended |
| 61 | Shift structure (opening … closing summary) | PLAN | GSS §6; ROADMAP GAME-011 | GSS §6 names "Recovery" |
| 62 | Representative shift 25–40 real min | CONFLICT (tuning) | GSS §70 20–45; ROADMAP PS2 exit 20–30 | ROADMAP PS2 exit set to 25–40; DEC-P5 |
| 63 | Variable/structural time compression | PART | GSS §69 fixed 3–6× | GSS §69 extended; GAME-011 |
| 64 | PressureLevel 0–1 (audio/NPC/pacing/telemetry, not TFS) | MISS | — | GAME-011 row extended |
| 65 | Plausible operational events | PLAN | GSS §72 | GSS §72 +2 events |
| 66 | Difficulty = information/complexity/scarcity/concurrency, not reaction or correctness | PLAN | GSS §45 | GSS §45 note |
| 67 | DifficultyProfile fields | MISS | — | GAME-022 |
| 68–70 | Beginner / Standard / Expert profiles | MISS | — | GAME-022 |
| 71 | Six competencies instead of XP | MISS | GSS §44 phases only | GAME-024 |
| 72–77 | Competency derivations (Leadership later) | MISS | — | GAME-024 |
| 78 | 0–100, shown as Developing/Reliable/Strong/Expert | MISS | — | GAME-024 |
| 79 | Rolling update | MISS | — | GAME-024 |
| 80 | Promotion gates | PART | GSS §44 phases, no gates | GAME-024 (placeholder values [GDD]) |
| 81 | Promotion unlocks control, never buffs TFS | PLAN (spirit) | GSS §41 | rule added to GSS §44 |
| 82–85 | Phase unlock lists | PLAN | GSS §44 | GSS §44 merged |
| 86 | Floor game never disappears | MISS (rule) | — | GSS §44 |
| 87 | Staff model, `TfsToolSkill` affects info gathering only | PLAN | GSS §60/§61; PS4 gated | GSS §60 constraint |
| 88 | Staff fail by speed/complexity, never corrupted TFS | MISS (rule) | — | GSS §60 |
| 89–90 | Broad roles + capacity | PLAN | GSS §61 (later) | PS4 |
| 91 | Complex-customer escalation to player | MISS | — | GSS §60; PS4 |
| 92 | Staff trade-off | PLAN | PS4 | none |
| 93 | Bounded economy | PLAN | GSS §74 | none |
| 94 | Ordering inputs | PLAN | GSS §75; ROADMAP PS4 | GSS §75 |
| 95–96 | Breadth vs depth; storage capacity | MISS | — | GSS §75; PS4 |
| 97 | Lead time | PLAN | ROADMAP PS4 (Thursday deli, O8) | none |
| 98 | Demand uncertainty | PLAN | GSS §75 | GSS §75 |
| 99 | Deal strategy; preserved pricing; no fit change | PLAN | GSS §56; GAME-016 (deals exclude deli, P7) | none |
| 100 | Light merchandising, no rerank | PLAN | GSS §76 | none |
| 101–104 | SERVICE / FLOW / OPERATIONS scores | MISS | — | GAME-020 |
| 105 | Revenue reported separately | IMPL | `ShiftReport.RevenuePostTax`; GSS §42 | none |
| 106 | Star gate model, not an average | CONFLICT | stars = `AvgSatisfaction` cut-offs (`ShiftSim.Report`, SLICE_DESIGN §5); GAME-010 tunes to it | PS1 keeps it; GAME-020 replaces it after GAME-010 merges |
| 107 | Severe failure flags cap the rating | PART | `RoughShift`; GAME-007 strike "Manager review" | GAME-020 maps them |
| 108 | Report main summary | PART | `ShiftReport` (served, revenue, wait, service time, satisfaction, walkouts, sold out) | GAME-020 adds decision quality, waste (GAME-013 keeps the O16 store sections) |
| 109–112 | Service / consultation / inventory / flow detail | MISS | — | GAME-020 |
| 113 | Dev-only debug panel, TFS vs gameplay labelled | PART | GSS §80 panel planned; slice F3 debug toggle | GAME-020 + UX-005 |
| 114 | Every rejection explainable | PART | reject line chosen by price/fit (`ShiftSim.Present`); GSS §58 | GAME-020 explanation record |
| 115 | Deterministic, data-driven stress suite; TFS unchanged | PART | seeded sim, `SliceTests`, bot tests, goldens | QA-002 harness; DP tests per packet below |
| DP-001 | Explicit easy customer | PART | GAME-010 perfect persona | GAME-017 (no-question path stays fast) |
| DP-002 | Hidden avoidance → refined query | MISS | — | GAME-017 |
| DP-003 | Redundant question | MISS | — | GAME-017 |
| DP-004 | Budget conflict, TFS canonical | PART | DEC-044 PriceFit; GAME-010 | GAME-019 |
| DP-005 | Flexible budget follow-up | MISS | — | GAME-019 |
| DP-006 | No perfect resolution, DQ excellent | MISS | — | GAME-019 |
| DP-007 | Satisfied customer, poor flow | MISS | — | GAME-019/020 |
| DP-008 / 009 | Correct / avoidable no-sale | MISS | — | GAME-019 |
| DP-010 / 011 | Question spam / under-questioning | MISS | — | GAME-017 |
| DP-012 | Decisive regular | MISS | — | GAME-021 |
| DP-013 / 014 | Enthusiast normal / rush | MISS | — | GAME-018 + GAME-019 |
| DP-015 | Queue triage | MISS | — | GAME-019 |
| DP-016–019 | Proactive / neglect / unnecessary restock; empty-with-backstock | PLAN | ROADMAP GAME-012 | GAME-012 acceptance extended |
| DP-020 | True sold out excluded | IMPL | `SoldOutBatch_NeverReturned_StrainKeepsNextBatchAsRep` | none |
| DP-021–023 | Repeat positive / negative modifier / new batch | MISS | — | GAME-021 |
| DP-024 | Similarity recovery via TFS Similar | PART | `Similarity.Similar` ported + `EngineFeatureTests` | GAME-018 + GAME-021 |
| DP-025 / 026 | Deal demand / preparation | PLAN | GAME-016 (PS3; deals exclude deli) + GAME-012 | GAME-016 acceptance note |
| DP-027 | Multi-system collision (core) | MISS | — | GAME-023 |
| DP-028 | Difficulty integrity (hard gate) | MISS | — | QA-002 + GAME-022 |
| DP-029–031 | Promotion exploits / balanced expert | MISS | GAME-010 personas reusable | GAME-024 |
| DP-032 | Manager feedback loop through inventory | PLAN | PS4 (gated) | none now |
| 116–117 | Per-customer and per-shift logs | PART | `Customer` fields, `ShiftReport` | GAME-020 |
| 118 | Balance targets; TFS parity 100 % | PART | GAME-010 persona targets | GAME-023 acceptance |
| 119 | Tuning behind config; none touch TFS | IMPL | `SliceConfig.json`, "no defaults in code"; no Domain edits | new keys per packet |
| 120 | Save system persist list, versioned | PLAN | GSS §81, no task | GAME-024 save v1 |
| 121 | Migration: missing field → safe default | MISS | — | GAME-024 |
| 122 | Event-driven evaluation; memory indexed by id; demand on ticks | PART | slice scores on `Present` only | rule in each packet |
| 123 | DP-001…011 workcells | — | — | DP-001→GAME-017; DP-002+003→GAME-019; DP-004→GAME-017/019; DP-005→GAME-012 (extended, no new packet); DP-006→GAME-021; DP-007→GAME-022; DP-008→GAME-020; DP-009→GAME-024; DP-010/011→PS4 (gated, no packet) |
| 124 | Gate A TFS integrity regression | PART | engine goldens (DEC-014) | QA-002 adds the gameplay-level gate |
| 125–129 | Gates B–F | MISS | — | GAME-017 (B), GAME-019 (C), GAME-012 + GAME-023 (D), GAME-021 (E), GAME-024 (F) |
| 130 | Gate G management | PLAN | PS4 gate | none now |
| 131 | Do-not-build-yet list | IMPL | GSS §100; ROADMAP PS4 gate | GSS §100 +items |
| 132 | One-time merge checklist | IMPL | this file | none |
| 133 | Highest-priority deterministic shift (12–20 customers, mix list) | MISS | ROADMAP PS1 exit test is narrower | GAME-023 |
| 134 | Final design test moment | MISS | — | GAME-023 acceptance |
| 135 | Final project rule | IMPL | DEC-001; ROADMAP §6 | GSS §105 quote |
| — | ROADMAP's own PS2 row "DES-003 shift-day design" | CONFLICT (ID) | ROADMAP §3 | renamed DES-004 (this task is DES-003) |

## Counts (rows above, excluding the §0/§123/§132 bookkeeping rows and the §24 n/a row)
| Status | Rows |
|---|---|
| ALREADY_IMPLEMENTED | 13 |
| ALREADY_PLANNED | 31 |
| PARTIALLY_IMPLEMENTED | 38 |
| MISSING | 55 |
| CONFLICTS_WITH_CURRENT_DESIGN | 9 |
Rows with a split status (e.g. "PLAN / PART", "IMPL (engine) / MISS") are counted under the first label.
