# 01 — SYSTEM CONTRACTS, OWNERSHIP & INVARIANTS

## 1. System ownership

| Truth | Authoritative owner | Read-only consumers |
|---|---|---|
| TFS recommendation behavior | canonical v7.11.4-derived `RecommendationService` | customer UI, analytics, QA |
| hidden customer truth | `CustomerSimulation` | reveal generator, fictional outcome model |
| player-known customer facts | `CustomerSession.KnownProfile` | TFS input builder, dialogue UI, decision analytics |
| inventory | `InventoryService` event ledger | TFS eligibility, jars/shelves, POS, ordering, manager UI |
| reservations | `InventoryService` reservation ledger | transaction, retrieval UI |
| completed sales | `TransactionService` ledger | economy, reporting, progression |
| price/deal truth | `PricingService` | POS, customer acceptance, economy |
| queue/patience | `QueueManager` | traffic, UX, shift analytics |
| shift time/phase | `GameClock` + `TrafficDirector` | arrivals, tasks, events |
| staff availability/assignment | `StaffService` + `TaskDirector` | manager UI, queue/restock/receiving |
| fictional satisfaction/outcome | `OutcomeService` | repeat memory, report; **never TFS ranking** |
| repeat history | `CustomerMemoryService` | dialogue/reveal context when legitimately available |
| career evidence | `ProgressionService` | promotion UI/report |
| purchase orders/commitments | `OrderingService` | budget, future inventory, receiving |
| demand forecast | `DemandForecastService` | ordering/manager UI; never exact future customer list |

## 2. Core invariants

### INV-TFS-01
Identical canonical TFS inputs and identical authoritative eligible inventory must produce identical recommendation behavior regardless of difficulty, career rank, player score or customer hidden truth.

### INV-CUST-01
`TrueCustomerProfile` is not directly visible to RecommendationService. Only `KnownCustomerProfile` may create TFS input.

### INV-INV-01
Inventory cannot be independently maintained by simulation, jars, POS and BOH. All are projections of the single inventory ledger.

### INV-INV-02
Quantity flow is explicit:

`Available -> Reserved -> Sold`

or

`Available -> Reserved -> ReturnedAvailable`

Transfers move ownership location but not total stock.

### INV-TXN-01
Transaction completion is idempotent. Repeating the completion event cannot sell twice.

### INV-SEED-01
A saved shift preserves its RNG streams. Reloading does not reroll customer identities, future arrivals, patience, supplier fills or events already committed to the seed.

### INV-DIFF-01
Difficulty may alter composition, timing, scarcity and concurrency. It may not alter TFS chemistry/scoring truth.

### INV-PROG-01
Progression derives from authoritative gameplay records. Revenue or completed transactions alone cannot grant promotion.

## 3. RNG stream separation
Use independent deterministic streams derived from the shift seed:

- `arrival_rng`
- `customer_profile_rng`
- `dialogue_rng`
- `patience_rng`
- `fictional_outcome_rng`
- `supplier_rng`
- `event_rng`

Reason: adding a new dialogue phrase must not reshuffle arrivals or supplier fills.

Seed derivation proposal:

`streamSeed = Hash64(shiftSeed, streamName, stableEntityId)`

## 4. Customer information states

### TrueCustomerProfile
Simulation truth. Contains all generated constraints and preferences.

### RevealPlan
Maps facts to legitimate reveal channels:
- opener;
- specific clarification question;
- spontaneous follow-up;
- repeat-history memory;
- visible customer response.

### KnownCustomerProfile
Append-only during an interaction except when the customer explicitly corrects prior information. Every fact records:
- `fact_id`
- `value`
- `source`
- `revealed_at`
- `confidence`

### TFSInputSnapshot
Immutable input sent for one recommendation execution:
- known fact IDs/values;
- inventory snapshot ID;
- query mode;
- canonical TFS version;
- hash.

## 5. Decision record

```yaml
DecisionRecord:
  decision_id: string
  customer_id: string
  interaction_id: string
  known_profile_snapshot_id: string
  tfs_input_hash: string
  tfs_result_snapshot_id: string
  selected_product_or_batch_id: string|null
  selected_tfs_position: integer|null
  questions_asked: [question_id]
  timestamps:
    service_start: number
    recommendation: number
    retrieval_start: number
    transaction_complete: number|null
  result:
    SALE_RECOMMENDATION
    SALE_ALTERNATE
    INFORMED_NO_SALE
    AVOIDABLE_NO_SALE
    WALK_PRICE
    WALK_WAIT
    WALK_OTHER
  analytics:
    information_sufficiency: 0..100
    resolution_quality: 0..100
    question_efficiency: 0..100
    decision_quality: 0..100
    decision_regret: 0..100
```

## 6. Counterfactual information analysis
**NEW PROPOSAL:** post-shift `InformationSufficiency` may use canonical TFS itself to determine whether an unasked, legitimately available question was decision-critical.

For each unanswered question whose true answer was generated:
1. reconstruct the exact pre-decision KnownCustomerProfile;
2. add only that answer;
3. rerun canonical TFS against the same inventory snapshot;
4. compare result set/ranking/feasibility;
5. mark the question `decision_critical` only if the answer materially changes the actionable result set or resolves a hard constraint.

This is permitted because it is post-hoc analytics using TFS; it does not secretly rerank the live recommendation.

## 7. Best Available Resolution
`BestAvailableResolution` is not a second cannabis model.

Candidate evaluation is lexicographic:
1. legal/transaction feasibility;
2. known hard constraints (budget cap, product category refusal, quantity, explicit avoidance represented through canonical TFS input/results);
3. authoritative availability;
4. canonical TFS recommendation position/score **as exposed by TFS**;
5. known customer non-chemistry preferences (price/deal, exact prior item, speed);
6. operational tie-breakers.

If TFS exposes no numeric score, use canonical rank buckets. Do not fabricate hidden chemistry values.

## 8. Inventory event contract

```yaml
InventoryEvent:
  event_id: string
  type: RECEIVE | TRANSFER | RESERVE | RELEASE | SELL | WASTE | ADJUST
  item_id: string
  batch_id: string|null
  quantity: number
  from_location: string|null
  to_location: string|null
  transaction_id: string|null
  reason_code: string|null
  timestamp: number
```

Ledger invariant after every event:
`TotalReceived + PositiveAdjustments = Available + Reserved + Sold + Waste + NegativeAdjustments`

## 9. Staff state machine

`OFF_SHIFT -> AVAILABLE -> ASSIGNED -> BUSY -> AVAILABLE`

Additional states:
- `BREAK_PENDING`
- `ON_BREAK`
- `ESCALATION`
- `UNAVAILABLE`

Assignments do not teleport. A staff member finishes a noninterruptible task segment or incurs a bounded handoff delay before switching.

## 10. Task state machine

`CREATED -> AVAILABLE -> ASSIGNED -> IN_PROGRESS -> COMPLETED`

Alternate exits:
- `CANCELED`
- `BLOCKED`
- `FAILED`
- `ESCALATED`

Every task defines:
- urgency;
- due horizon;
- required capability;
- interruptibility;
- world location;
- estimated duration band;
- downstream consequence.

## 11. Purchase-order state machine

`DRAFT -> SUBMITTED -> COMMITTED -> IN_TRANSIT -> RECEIVING -> CLOSED`

Exception paths:
- `PARTIAL_FILL`
- `DELAYED`
- `DISCREPANCY`
- `CANCELED_BY_SUPPLIER`

Inventory is created only by `RECEIVE` events during receiving. Submitted/committed quantities are not sellable stock.

## 12. Analytics ownership
Shift reports are projections from immutable event records. No report maintains its own counters that can drift from source ledgers.
