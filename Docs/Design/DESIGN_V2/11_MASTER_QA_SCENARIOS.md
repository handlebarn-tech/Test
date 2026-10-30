# 11 — MASTER DETERMINISTIC QA SCENARIO PACK

**100 scenarios.** Machine-readable definitions are in `QA/qa_scenarios.json`.

## Fixture rule
All scenarios use fixed seeds and named fixtures. TFS-specific expected outputs are captured from the local canonical v7.11.4 source according to `15_TFS_ORACLE_CAPTURE_SPEC.md`; this package does not invent missing recommendation output.

## Category coverage

- customer: 5
- economy: 12
- inventory: 17
- manager: 12
- nosale: 2
- progression: 6
- queue: 3
- repeat: 3
- service: 30
- staff: 2
- transaction: 2
- ux: 4
- weighing: 2

## Scenario index

| ID | Category | Purpose | Linked exploit |
|---|---|---|---|
| QA-001 | service | Regression: Blind top-result click | EX-001 |
| QA-002 | service | Regression: Ask every question | EX-002 |
| QA-003 | service | Regression: Ask no questions | EX-003 |
| QA-004 | service | Regression: Refuse difficult customers | EX-004 |
| QA-005 | service | Regression: Let hard customers abandon | EX-005 |
| QA-006 | economy | Regression: Sell cheapest item always | EX-006 |
| QA-007 | economy | Regression: Sell highest-margin item always | EX-007 |
| QA-008 | service | Regression: Always force a sale | EX-008 |
| QA-009 | service | Regression: Farm informed no-sale | EX-009 |
| QA-010 | service | Regression: Infinite Compare | EX-010 |
| QA-011 | service | Regression: Repeated Similar loop | EX-011 |
| QA-012 | service | Regression: Question-menu fishing | EX-012 |
| QA-013 | inventory | Regression: Stock duplication via reserve | EX-013 |
| QA-014 | service | Regression: Cancel-after-complete rollback | EX-014 |
| QA-015 | service | Regression: Double transaction completion | EX-015 |
| QA-016 | inventory | Regression: Deli scoop cancel duplication | EX-016 |
| QA-017 | inventory | Regression: Deli scoop permanent loss | EX-017 |
| QA-018 | inventory | Regression: Wrong batch equivalence | EX-018 |
| QA-019 | inventory | Regression: Sell EMPTY_WITH_BACKSTOCK from menu | EX-019 |
| QA-020 | service | Regression: Sell SOLD_OUT stale TFS result | EX-020 |
| QA-021 | inventory | Regression: Restock constantly | EX-021 |
| QA-022 | inventory | Regression: Never restock | EX-022 |
| QA-023 | inventory | Regression: Restock tiny amounts repeatedly | EX-023 |
| QA-024 | inventory | Regression: Waste/adjust stock to manipulate demand | EX-024 |
| QA-025 | ux | Regression: Pause while continuing actions | EX-025 |
| QA-026 | ux | Regression: Detail-panel slow-time abuse | EX-026 |
| QA-027 | service | Regression: Save/reload customer reroll | EX-027 |
| QA-028 | service | Regression: Save/reload fictional outcome reroll | EX-028 |
| QA-029 | progression | Regression: Shift-reset promotion farming | EX-029 |
| QA-030 | progression | Regression: Tutorial/easy scenario farming | EX-030 |
| QA-031 | progression | Regression: One-metric promotion | EX-031 |
| QA-032 | progression | Regression: Recent hot-streak promotion | EX-032 |
| QA-033 | manager | Regression: Leadership command spam | EX-033 |
| QA-034 | manager | Regression: Instant role-toggle staff | EX-034 |
| QA-035 | manager | Regression: One staff member in multiple roles | EX-035 |
| QA-036 | manager | Regression: Understaff then superhero manager | EX-036 |
| QA-037 | manager | Regression: Overstaff every shift | EX-037 |
| QA-038 | manager | Regression: Skip breaks forever | EX-038 |
| QA-039 | manager | Regression: Break all staff in quiet exploit | EX-039 |
| QA-040 | economy | Regression: Order everything | EX-040 |
| QA-041 | economy | Regression: Order highest margin only | EX-041 |
| QA-042 | economy | Regression: Order cheapest only | EX-042 |
| QA-043 | inventory | Regression: Zero safety stock + emergency orders | EX-043 |
| QA-044 | inventory | Regression: Extreme safety stock | EX-044 |
| QA-045 | economy | Regression: Forecast omniscience | EX-045 |
| QA-046 | economy | Regression: Deal spam | EX-046 |
| QA-047 | economy | Regression: Deal at expiry always | EX-047 |
| QA-048 | service | Regression: Cancel PO after seeing future demand | EX-048 |
| QA-049 | inventory | Regression: Receive quantity without space | EX-049 |
| QA-050 | inventory | Regression: Duplicate receiving event | EX-050 |
| QA-051 | service | Regression: Merchandising teleport | EX-051 |
| QA-052 | manager | Regression: Hide in manager screen while floor pauses | EX-052 |
| QA-053 | manager | Regression: Manager delegates all meaningful choices | EX-053 |
| QA-054 | manager | Regression: Manager personally does everything | EX-054 |
| QA-055 | service | Regression: Customer archetype streak farm | EX-055 |
| QA-056 | service | Regression: Repeat-history auto-answer | EX-056 |
| QA-057 | service | Regression: Prior satisfaction treated as TFS weight | EX-057 |
| QA-058 | service | Regression: Difficulty modifies TFS | EX-058 |
| QA-059 | ux | Regression: Hidden truth leaks through UI | EX-059 |
| QA-060 | service | Regression: Analytics counter drift | EX-060 |
| QA-061 | service | Regression: Queue abandonment blamed on impossible scenario | EX-061 |
| QA-062 | service | Regression: Station outage reroll | EX-062 |
| QA-063 | service | Regression: Quantity split bypasses transaction limit | EX-063 |
| QA-064 | service | Regression: Same-customer same-day limit invented | EX-064 |
| QA-065 | service | Regression: Discount stacking loophole | EX-065 |
| QA-066 | service | Regression: Free infinite comparison explanation | EX-066 |
| QA-067 | ux | Regression: UI shortcut auto-retrieves | EX-067 |
| QA-068 | service | Regression: Unbounded event stacking | EX-068 |
| QA-069 | economy | Regression: Supplier fill seed fishing | EX-069 |
| QA-070 | service | Regression: Expiry risk changes recommendation chemistry | EX-070 |
| QA-071 | customer | Explicit customer parity | — |
| QA-072 | customer | One critical question changes input | — |
| QA-073 | customer | High ambiguity targeted questioning | — |
| QA-074 | customer | Explicit quick customer over-questioned | — |
| QA-075 | customer | Ambiguous customer no-question path | — |
| QA-076 | nosale | Correct informed no-sale | — |
| QA-077 | nosale | Avoidable no-sale | — |
| QA-078 | repeat | Exact repeat current stock | — |
| QA-079 | repeat | Same name new batch | — |
| QA-080 | repeat | Changed repeat preference | — |
| QA-081 | queue | Standard benchmark targeted | — |
| QA-082 | queue | Ask-all throughput stress | — |
| QA-083 | queue | Ask-none quality stress | — |
| QA-084 | inventory | LOW proactive restock | — |
| QA-085 | inventory | EMPTY_WITH_BACKSTOCK physical gate | — |
| QA-086 | inventory | SOLD_OUT substitution | — |
| QA-087 | inventory | Atomic one-unit reserve | — |
| QA-088 | transaction | Cancel reserved transaction | — |
| QA-089 | transaction | Idempotent completion | — |
| QA-090 | weighing | Deli cancel handling | — |
| QA-091 | weighing | Difficulty tolerance parity | — |
| QA-092 | staff | Lead reassignment tradeoff | — |
| QA-093 | staff | Break window | — |
| QA-094 | manager | Manager floor intervention | — |
| QA-095 | manager | Receiving discrepancy | — |
| QA-096 | economy | Breadth vs depth consequence | — |
| QA-097 | economy | Safety stock reacts to uncertainty | — |
| QA-098 | economy | Lead-time risk | — |
| QA-099 | progression | Balanced gate | — |
| QA-100 | progression | Speedrunner blocked | — |

## Required execution tiers
1. **Commit gate:** all Critical exploit regressions + TFS parity + inventory idempotency.
2. **Feature gate:** all High exploit regressions for the owning system.
3. **Content-complete gate:** all 100 scenarios.

## Failure reporting
Every failed scenario prints seed, fixture IDs, current TFS input/output snapshot hashes, inventory ledger diff, transaction ledger diff and relevant analytics. Do not report only “expected/actual” without state provenance.
