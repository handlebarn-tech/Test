# 13 — IMPLEMENTATION SEQUENCE & ACCEPTANCE GATES

## Principle
Design everything now; implement in dependency order so management/economy cannot hide a weak floor loop.

## EPIC A — Shared contracts and deterministic state
### A1 RNG streams
Implement named deterministic streams and save persistence.
Acceptance: QA-027, QA-028, QA-062, QA-069.

### A2 DecisionRecord
Persist KnownProfile/TFS snapshots/questions/outcome per interaction.
Acceptance: replaying a completed interaction reconstructs exact inputs without hidden truth leakage.

### A3 Ledger invariants
Inventory and transaction idempotency.
Acceptance: QA-013 through QA-020, QA-050.

**Gate A:** zero Critical invariant failures.

## EPIC B — Customer information model
### B1 True/Known/Reveal model
### B2 Question definitions/reveal rules
### B3 Counterfactual post-shift criticality
### B4 Viability-class generator
### B5 Dialogue family/cooldown system
### B6 Repeat-memory overlay

Acceptance:
- QA-001–012;
- QA-071–080;
- 10,000 generated profiles with no critical fact lacking a reveal path;
- anti-repetition stress pass.

**Gate B:** identical known inputs retain TFS parity; hidden truth never reaches RecommendationService.

## EPIC C — Shift pacing and queue
### C1 phase-driven bounded-renewal arrivals
### C2 heterogeneous patience
### C3 queue attribution
### C4 recovery/quiet compression
### C5 task pressure budget

Acceptance:
- benchmark harness ranges in `03_SHIFT_PACING_QUEUE_MODEL.md`;
- QA-081–083;
- same seed reproduces arrivals/abandonment.

**Gate C:** Standard targeted benchmark is playable and ask-all/ask-none each lose on a different axis.

## EPIC D — Difficulty
### D1 preset data
### D2 PressureBudget compatibility
### D3 custom sliders
### D4 accessibility target adjustment

Acceptance:
- parity fixture identical Beginner/Standard/Expert;
- QA-058, QA-068, QA-091.

## EPIC E — Progression analytics
### E1 DQ/IS/RQ/QE/NSJ
### E2 competency normalization
### E3 six-shift evidence windows
### E4 promotion review/proof scenarios

Acceptance:
- synthetic profiles reproduce intended gate behavior;
- QA-030–032, QA-099–100.

## EPIC F — Staff/Lead/AM bridge
### F1 staff state machine
### F2 assignments and handoff latency
### F3 break windows
### F4 task director
### F5 receiving + exceptions
### F6 pre-shift readiness

Acceptance:
- QA-033–039, QA-092–095;
- no staff double-capacity;
- ordinary staff work does not require constant player input.

**Gate F:** manager features may begin only after floor benchmark remains fun with staff enabled.

## EPIC G — Economy/ordering
### G1 demand history/forecast bands
### G2 safety-stock/risk calculations
### G3 supplier/PO state machine
### G4 cash/storage/headroom
### G5 receiving binding
### G6 CoverageScore advisory
### G7 deal system

Acceptance:
- QA-040–050, QA-096–098;
- strategy stress test demonstrates no universal policy across tuned scenario set.

## EPIC H — Manager horizon
### H1 future staffing blocks
### H2 3–5 shift dashboard
### H3 merchandising access
### H4 intervention opportunity cost
### H5 lost-sale attribution/report

Acceptance:
- QA-053–054;
- manager planning measurably changes future floor state through shared systems.

## EPIC I — UX hardening
Implement interaction/focus/back/error/accessibility spec.
Acceptance: QA-025–026, QA-052, QA-059, QA-066–067 plus controller end-to-end transaction.

## EPIC J — Content longevity
### J1 repeat lifecycle content
### J2 semantic dialogue expansion
### J3 scenario library
### J4 telemetry repetition flags

Acceptance:
- 50-customer anti-repeat test;
- 5 seeded Standard shifts show meaningful composition/state variation without new rules.

## Continuous QA
At every commit:
- Critical exploit tests;
- TFS parity fixtures;
- inventory/transaction invariant suite.

Nightly/content build:
- all 100 deterministic scenarios;
- generator stress;
- shift benchmark simulation;
- economy policy stress.

## Explicit deferrals
Do not implement before the above proves fun/stable:
- detailed payroll/tax accounting;
- HR/personnel simulation;
- supplier negotiation minigame;
- corporate bureaucracy;
- broad random-disaster system;
- customer identity/PII;
- alternate recommendation model;
- chemistry degradation invented from product age.
