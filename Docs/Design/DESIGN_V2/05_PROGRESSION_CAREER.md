# 05 — PROGRESSION & CAREER SYSTEM

## 1. Progression thesis
Progression represents **increasing trust and decision scope**, not accumulated XP.

Career ladder:

`Budtender -> Trusted/Senior Budtender -> Lead -> Assistant Manager -> Manager`

A promotion must change what the player is allowed and expected to decide. All earlier floor play remains available.

## 2. Competencies
Six 0–100 competencies:

1. `ServiceJudgment (SJ)`
2. `Throughput (TP)`
3. `InventoryDiscipline (ID)`
4. `OperationalAccuracy (OA)`
5. `Reliability (REL)`
6. `Leadership (LEAD)`

Unavailable dimensions are `N/A`, not zero. Leadership begins producing evidence during Senior acting-lead/trial opportunities.

## 3. Per-customer service analytics

### 3.1 Information Sufficiency (IS)
Measures whether the player gathered information that was actually decision-critical.

For each interaction, post-hoc canonical TFS counterfactuals classify unanswered legitimate questions:
- critical weight 1.0;
- useful weight 0.4;
- neutral/redundant 0.

`IS = 100 * (1 - missedCriticalWeight / totalAvailableCriticalWeight)`

If no critical information was omitted, IS=100. The player is never penalized for not asking irrelevant questions.

### 3.2 Resolution Quality (RQ)
Uses `BestAvailableResolution` from the system-contract spec.

Suggested scoring:
- selected best feasible canonical resolution: 100
- selected equivalent/tied resolution: 95
- selected feasible but materially lower canonical tier: 75–90 according to exposed rank/score gap
- selected option violating a known soft constraint with better option available: 60–80
- selected option violating known hard constraint: <=40
- informed no-sale when no feasible path exists: 100
- avoidable no-sale with feasible high-quality path: 20–60

Do not calculate chemistry outside canonical TFS.

### 3.3 Question Efficiency (QE)

`UsefulQuestionSeconds = sum(time of critical/useful questions weighted by value)`

`QE = 100 * UsefulQuestionSeconds / max(UsefulQuestionSeconds, TotalQuestionSeconds)`

Then apply consultation mismatch adjustment:
- QUICK customer and redundant question loop: -5 to -20;
- DEEP customer who received a useful explanation: +0 to +5 capped at 100.

Asking zero questions gives QE=100 only when no useful question was available. If useful/critical questions existed and were skipped, QE is capped by IS.

### 3.4 No-Sale Judgment (NSJ)
- correct informed no-sale: 100
- price walk with no acceptable alternative: 90–100
- customer voluntary decline after good service: 85–100
- avoidable no-sale: 20–60
- deliberate refusal/cherry-picking with viable path: 0–30

### 3.5 Customer Decision Quality

`DQ = 0.40*RQ + 0.30*IS + 0.20*QE + 0.10*NSJ_component`

For completed sales where NSJ is not applicable, redistribute its 10% proportionally across RQ/IS/QE.

`DecisionRegret = max(0, 100 - RQ)` for the resolution dimension, recorded separately from satisfaction.

## 4. Shift-level competency formulas
All component metrics are first normalized against the scenario/difficulty benchmark so a harder scenario does not mechanically lower competency.

### 4.1 Service Judgment
Components:
- mean DQ: 45%
- information sufficiency: 20%
- no-sale judgment: 15%
- question efficiency: 20%

Anti-compensation floor:

`SJ = 0.75*WeightedMean + 0.25*min(DQ_mean, IS, NSJ_or_100, QE)`

### 4.2 Throughput
Components:
- service-time efficiency vs archetype/scenario benchmark: 40%
- player-attributable abandonment: 35%
- queue recovery after rush: 15%
- avoidable idle/rework: 10%

Normalization examples:
- abandonment <= benchmark: 100
- benchmark+3 percentage points: 80
- +7 pp: 55
- +12 pp: 25
- +20 pp: 0

### 4.3 Inventory Discipline
Components:
- preventable stockout rate: 30%
- proactive vs emergency restock quality: 25%
- reservation/inventory integrity: 25%
- avoidable waste/handling loss: 20%

Any duplication/negative-stock invariant breach forces the relevant test/shift ID component to 0 and flags a defect; ordinary player gameplay should not be able to create engine-level corruption.

### 4.4 Operational Accuracy
Components:
- correct product/batch/quantity: 30%
- transaction/POS correctness: 25%
- weighing accuracy: 20%
- modeled compliance/limit correctness: 15%
- task/exception execution: 10%

Critical wrong-batch or invalid-transaction completion caps OA at 60 for that shift.

### 4.5 Reliability
Components:
- assigned responsibilities completed: 35%
- opening/closing readiness: 25%
- unresolved exceptions: 20%
- consistency across the shift: 20%

No real attendance/employment punishment simulation is required; Reliability is game-operational consistency.

### 4.6 Leadership
Components:
- coverage quality: 30%
- assignment fit and timing: 25%
- break/task prioritization: 15%
- escalation quality: 15%
- team flow/result without micromanagement: 15%

## 5. Evidence model
A single great shift cannot promote the player.

For each competency, use last 6 eligible evidence shifts:
- promotion statistic = median of those 6;
- stability condition = no more than one shift below `(gate - 10)`;
- fewer than 4 eligible shifts means `INSUFFICIENT_EVIDENCE`.

A scenario counts as eligible only if it exposes enough opportunities for that competency. Repeating an identical scenario seed does not create new evidence.

## 6. Promotion gates

### Budtender -> Trusted/Senior
Minimum 6 completed standard-equivalent shifts.

| Competency | Gate |
|---|---:|
| SJ | 70 |
| TP | 65 |
| ID | 60 |
| OA | 75 |
| REL | 65 |

Additional:
- at least 3 eligible shifts with no critical operational error;
- complete one mixed customer + restock proof scenario.

Unlocks:
- full Floor Mode shortcuts;
- repeat-history panel;
- proactive stock-risk view;
- acting-lead trial shifts;
- optional zone responsibility.

### Trusted/Senior -> Lead
Minimum 12 total shifts; at least 4 Senior-level shifts; 2 acting-lead evidence shifts.

| Competency | Gate |
|---|---:|
| SJ | 75 |
| TP | 70 |
| ID | 70 |
| OA | 80 |
| REL | 72 |
| LEAD | 65 |

Proof: seeded rush with break timing + stock pressure + one staff reassignment.

Unlocks:
- real-time role assignments;
- break timing within policy bounds;
- floor-wide risk dashboard;
- delegate restock/retrieval/receiving tasks;
- manager escalation handling lite.

### Lead -> Assistant Manager
Minimum 20 total shifts; at least 5 Lead shifts.

| Competency | Gate |
|---|---:|
| SJ | 78 |
| TP | 72 |
| ID | 76 |
| OA | 82 |
| REL | 78 |
| LEAD | 72 |

Proof: pre-shift setup + receiving/inventory exception + rush + close readiness.

Unlocks:
- pre-shift coverage plan;
- opening/closing readiness;
- inventory exception resolution;
- receiving oversight;
- limited ordering recommendations;
- bounded deal/merchandising decisions.

### Assistant Manager -> Manager
Minimum 30 total shifts; at least 6 AM shifts; complete one 3-shift planning arc.

| Competency | Gate |
|---|---:|
| SJ | 78 |
| TP | 72 |
| ID | 80 |
| OA | 83 |
| REL | 80 |
| LEAD | 78 |

Unlocks:
- final purchase orders;
- multi-shift staffing plan;
- demand forecast and budget allocation;
- merchandising/deal plan;
- multi-shift performance review.

## 7. Gate stress test
A synthetic six-shift Monte Carlo stress test was run with per-competency SD=6.

Representative pass behavior:
- balanced master profile: ~100% Senior, ~100% Lead, ~96% AM, ~76% Manager;
- speedrunner: ~0% at all gates;
- perfectionist-but-too-slow: effectively 0% promotion until throughput improves;
- careless high-throughput seller: 0%;
- inventory-only optimizer: effectively 0%;
- balanced-good profile: ~99% Senior, ~59% Lead, ~3% AM, demonstrating that later roles require growth rather than time served.

These are validation archetypes, not player labels.

## 8. Promotion event
When all gates pass, show a concise Trust Review:
- evidence window;
- six competency medians;
- strongest decisions;
- recurring failure type;
- exact responsibility unlocked;
- proof-scenario result.

No separate XP bar is required.

## 9. Regression and poor performance
Career rank does not normally decrease.

Poor recent form:
- changes coaching objectives;
- can cause a manager/AI supervisor to require review for high-risk exceptions;
- lowers recent-form display;
- does not delete unlocked systems.

Only authored career/story modes, if ever added, should permit formal demotion.

## 10. Specialization
Specialization grants information/workflow preference, not recommendation power.

Options:
- Service: richer repeat/context summaries.
- Flow: queue/coverage visualization.
- Inventory: deeper stock-risk projection.
- Operations: task/exception prioritization.

No specialization changes TFS output, customer hidden truth, inventory quantities or prices.

## 11. Grind prevention
- identical seed repeat gives practice but no new evidence;
- low-complexity tutorial scenarios stop contributing after mastery;
- promotion uses minimum gates, not aggregate total;
- no-sale farming fails NSJ when viable paths existed;
- ask-all farming reduces QE/TP;
- ask-none farming reduces IS/DQ where counterfactual TFS proves a missing fact mattered;
- revenue does not directly enter promotion gates.

## 12. Floor relevance after promotion
Lead/AM/Manager shifts reserve explicit intervention windows. Management success includes knowing when **not** to intervene, but the game must regularly present floor states where hands-on help is rational.
