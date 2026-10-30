# 12 — CONTRADICTION & CONSISTENCY AUDIT

## Audit scope
Checked the V2 proposal against the supplied handoff snapshot and against V2 cross-system assumptions. This audit does not claim access to newer repository state beyond the supplied handoff.

| # | Potential conflict | Resolution in V2 | Status |
|---:|---|---|---|
| 1 | Older Unity 6.3 statements vs current Unity 6000.6.7f1 | V2 makes no engine-version proposal; handoff current value wins | Resolved |
| 2 | TFS v7.11.4 shipped vs v7.11.5 candidate | all parity/oracle specs pin v7.11.4 | Resolved |
| 3 | Game design could accidentally create alternate chemistry scoring | `BestAvailableResolution` is lexicographic and defers recommendation dimension to canonical TFS only | Resolved |
| 4 | Hidden customer truth useful for outcome vs prohibited for TFS | separate True/Known/TFS/Outcome layers; hidden truth cannot reach RecommendationService | Resolved |
| 5 | Post-hoc DecisionQuality needs knowledge of missed information | uses counterfactual **canonical TFS** after the shift; no live rerank | Resolved |
| 6 | Customer satisfaction vs player decision quality | separate metrics; imperfect outcome can coexist with excellent decision | Resolved |
| 7 | 20–45 min legacy shift vs 25–40 recent direction | V2 chooses 32 Standard, 26 Beginner, 35 Expert inside current band | Resolved proposal |
| 8 | V1 Standard 22–25 customers vs natural service times | rejected after queue simulation; V2 Standard ~18–20 | Resolved correction |
| 9 | Queue pressure vs asking useful questions | active engagement slows active patience only; waiting queue continues aging | Resolved |
| 10 | Ask-all might dominate because more information is always better | QE + time/queue cost; counterfactual criticality prevents penalizing concise correct service | Resolved |
| 11 | Ask-none might dominate throughput | IS/DQ penalize only when legitimately discoverable facts materially mattered | Resolved |
| 12 | Revenue vs service quality | revenue excluded from promotion competencies; economy still values contribution | Resolved |
| 13 | Valid no-sale vs conversion incentives | InformedNoSale can earn full decision credit; AvoidableNoSale separated | Resolved |
| 14 | Inventory total vs physical FOH availability | authoritative inventory tracks location; EMPTY_WITH_BACKSTOCK distinct from SOLD_OUT | Resolved |
| 15 | Temporary deli scoop vs permanent stock truth | handled/reserved temporary state; SOLD on transaction completion | Resolved |
| 16 | Same strain vs batch truth | batch ID required through recommendation intent, retrieval, sale and repeat memory | Resolved |
| 17 | Packaged products now valid vs deli as hero workflow | packaged path supported, deli remains foundation | Resolved |
| 18 | Restock realism vs chore spam | Standard target 2–4 meaningful restock decisions; higher counts are diagnostic | Resolved |
| 19 | Management progression vs vertical-slice-first | deep management is later implementation stage; design exists now but not prerequisite | Resolved |
| 20 | Manager staff AI competent vs player must remain relevant | routine work automated; exceptions/prioritization/intervention remain player decisions | Resolved |
| 21 | Manager can step onto floor vs management tasks | intervention pauses/delays strategic/task work; explicit opportunity cost | Resolved |
| 22 | Break realism vs admin bloat | bounded break windows and small fatigue effect; no timecard system | Resolved |
| 23 | Economy needs safety stock vs fixed simple game rules | formula is internal/advisory; player sees risk bands, not required spreadsheet math | Resolved |
| 24 | Safety stock can encourage hoarding | cash/storage/expiry/receiving constraints plus service classes | Resolved |
| 25 | Inventory aging could imply fake chemistry degradation | V2 explicitly prohibits age from altering TFS chemistry unless canonical data changes | Resolved |
| 26 | Forecast useful vs forecast omniscient | probabilistic bands only; RNG future not exposed | Resolved |
| 27 | Supplier uncertainty vs deterministic QA | uncertainty is seeded; same seed reproduces fill/lead outcomes | Resolved |
| 28 | Difficulty vs TFS parity | parity fixtures executed on all presets; difficulty cannot reach RecommendationService configuration | Resolved |
| 29 | Accessibility slow-time/patience vs promotion fairness | assist-aware benchmark targets; no punishment for accessibility use | Resolved |
| 30 | Career ladder says Trusted/Senior then Lead | V2 preserves both as distinct stages exactly as workstream requested | Resolved |
| 31 | Leadership metric unavailable before Lead | Senior acting-lead trial shifts create evidence before promotion | Resolved |
| 32 | Generic XP prohibited vs minimum shift counts | counts are evidence sufficiency, not progression currency | Resolved |
| 33 | Repeated mediocre shifts vs mastery | median six-shift gates + stability; time served alone cannot promote | Resolved |
| 34 | Scenario mode as QA vs progression farming | repeated seed does not create new promotion evidence | Resolved |
| 35 | Pausing for accessibility vs pause exploit | explicit assist mode freezes/adjusts benchmark coherently; ordinary pause freezes sim-affecting actions | Resolved |
| 36 | Current modeled no-daily-limit behavior vs transaction-limit checks | V2 validates each modeled transaction and does not invent daily lockout | Resolved |
| 37 | TFS live/local oracle not accessible in this chat | exact expected TFS snapshots are deliberately not fabricated; capture spec delegates to local canonical v7.11.4 | Open external binding, safely specified |
| 38 | Current implementation task statuses in handoff may be stale | V2 never treats those statuses as authority for current work completion | Resolved |
| 39 | Economy service CoverageScore could become shadow recommendation engine | coverage may call TFS as oracle over representative demand but cannot rank products independently | Resolved |
| 40 | Merchandising demand modifiers could distort recommendation truth | affects visibility/retrieval/demand only; no TFS scoring modification | Resolved |

## Internal numeric consistency
- Standard 32-minute phase durations sum to 32.
- Beginner phase durations sum to 26.
- Expert phase durations sum to 35.
- Standard arrival rates used in `default_tuning.yaml` match the simulation harness.
- Patience multipliers match difficulty spec.
- Promotion gates match config and progression spec.
- QA scenario count = 100; exploit count = 70.

## Remaining intentional unknowns
These require canonical repository/local-source access rather than design invention:
1. exact v7.11.4 TFS output snapshots for test fixtures;
2. exact current real inventory/product dataset to bind representative customer fixtures;
3. exact implemented Unity UI input architecture if it has changed after the handoff snapshot;
4. exact current task IDs/states in `PROJECT_STATE.md`.

The package defines how to bind those unknowns without guessing.
