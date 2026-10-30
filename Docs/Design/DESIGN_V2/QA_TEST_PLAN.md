# DESIGN_V2 — exploit catalogue as a QA test plan (IMP-002)

**Source:** V2 `10_EXPLOIT_FAILURE_ANALYSIS.md` (EX-001..070), V2 `11_MASTER_QA_SCENARIOS.md` + `QA/qa_scenarios.json` (QA-001..100). Audit rows 45–46 (`Docs/Imports/IMP-001_DESIGN_V2_AUDIT.md`). Approval DEC-063.
**What this is:** a checklist, not code. Each exploit has an owning packet that turns it into a deterministic test in **QA-002's harness format** (the Gate A parity harness, DEC-058) when that packet runs.
**Binding rules:**
- V2's fixtures (`BAT-A`, family "A") are abstract. Owners bind them to real catalog batches from `Tools/Data/import_catalog.js` output (DEC-014).
- Expected TFS output is captured from the **shipped engine** (v7.11.4 + DEC-015/016, DEC-060; REVIEW-IMP1 A1), never written by hand.
- Any TFS input in a scenario is the **parser input** (query text + chip + inventory snapshot, DEC-057; A2).
- V2's rule (10 "Required exploit regression rule"): a Critical/High row needs its test before the owning system is marked complete; Medium rows before content-complete. PS4 rows stay parked (DEC-063d).

## Critical
| EX | Exploit | Owner | Note |
|---|---|---|---|
| 013 | Stock duplication via reserve | GAME-012 / GAME-014 | Reservation arrives with concurrency (audit C5); PS1 has none (GAME-006). |
| 014 | Cancel-after-complete rollback | QA-002 harness (existing slice) | GAME-006's "cancel leaves stock unchanged" covers the PS1 path; the harness adds the after-complete case. |
| 015 | Double transaction completion | QA-002 harness (existing slice) | One `Sell` per line on one Confirm (GAME-006); assert idempotency. |
| 016 | Deli scoop cancel duplication | PS2 (GAME-012) | Only if a physical scoop/handling state is added; the slice weigh is assisted. |
| 018 | Wrong batch equivalence | GAME-021 | Batch id through memory (DP §59); engine `RepBatchId` (DEC-028). |
| 020 | Sell a stale SOLD_OUT result | GAME-018 | Stale-snapshot check before commit (V2 08 §11, 16 §6). |
| 049 / 050 | Receive without space / duplicate receipt | PS4 (parked) | |
| 057 | Prior satisfaction as a TFS weight | GAME-021 + QA-002 gate | DEC-053. |
| 058 | Difficulty modifies TFS | GAME-022 (DP-028) + QA-002 gate | |
| 059 | Hidden truth leaks through UI | GAME-017 + UX-005 | Unknown fields absent, not "???" (V2 08 §6); generic question menu (EX-012). |
| 063 | Quantity split bypasses the limit | GAME-007 (flower, summed cart grams); GAME-014 (packaged equivalents, DEC-048) | |
| 070 | Expiry changes recommendation chemistry | PS4 (parked) | DEC-053; V2 06 §13 forbids it. |

## High / Medium, by owner
| Owner | EX rows |
|---|---|
| GAME-017 (customer knowledge) | 001 blind top-card, 003 ask nothing (with GAME-019), 012 question-menu fishing (M), 055 archetype streak farm (M), 056 repeat-history auto-answer (with GAME-021) |
| GAME-018 (TFS workflows) | 011 repeated Similar loop (M): a same-input re-run is flagged redundant |
| GAME-019 (evaluation) | 002 ask everything, 004 refuse difficult customers, 008 always force a sale, 009 farm informed no-sale, 010 infinite Compare (M; 60 s relief cap), 066 free infinite explanation (M) |
| GAME-020 (telemetry, scoring) | 005 let hard customers abandon (attribution), 006 sell cheapest (M), 007 sell highest margin (revenue outside gates), 060 analytics counter drift, 061 abandonment blamed on impossible traffic |
| GAME-022 (difficulty) | 068 unbounded event stacking (PressureBudget) |
| GAME-024 (career, save) | 027 save/reload customer reroll, 028 outcome reroll (M), 029 shift-reset farming, 030 tutorial farming, 031 one-metric promotion, 032 hot-streak promotion (M), 062 event reroll (M) |
| GAME-011 / GAME-012 (PS2) | 017 scoop permanent loss, 019 sell EMPTY_WITH_BACKSTOCK from the menu (DEC-061: restock job), 021 restock constantly, 022 never restock, 023 tiny restocks (M), 024 waste/adjust to manipulate, 025 pause while acting, 026 slow-time abuse (M; assist only) |
| UX-005 / later UX | 067 shortcut auto-retrieves |
| GAME-007 / GAME-016 | 064 invented same-day limit (DEC-049: none), 065 discount stacking (deals, PS3) |
| PS4 (parked) | 033–048, 051–054, 069 |

## Feature scenarios (QA-071..100)
Owners use them as acceptance seeds, keeping their DP test names:
- 071–075 customer → GAME-017 (≈ DP-001/002/003/010/011)
- 076–077 no-sale → GAME-019 (DP-008/009)
- 078–080 repeat → GAME-021 (DP-021..023)
- 081–083 queue → DES-004 / GAME-011 benchmark
- 084–086 inventory → GAME-012 (DP-016..020)
- 087–090 transactions/weighing → QA-002 harness / GAME-012
- 091 tolerance parity → GAME-022
- 092–098 staff/manager/economy → PS4
- 099–100 progression → GAME-024 (DP-029..031)
