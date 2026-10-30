# 16 — CROSS-SYSTEM INTEGRATION

## 1. Shared simulation thesis
Every major mechanic must enter and leave the same simulation rather than producing an isolated score modifier.

Canonical causal chain:

`customer generation -> reveal/known information -> canonical TFS -> player/staff decision -> physical stock/transaction -> queue/time consequence -> customer outcome -> shift analytics -> career evidence -> management planning -> future inventory/staff/demand conditions`

## 2. Cause/effect matrix

| Source decision/state | Immediate system | Downstream systems |
|---|---|---|
| ask a clarification | CustomerSession | TFS input, service time, queue, DQ, progression |
| choose TFS result | Recommendation/DecisionRecord | retrieval, transaction, outcome, repeat memory |
| restock now | Inventory/Task | staff/player availability, queue risk, future sale feasibility |
| do not restock | Inventory | potential EMPTY_WITH_BACKSTOCK, service interruption, lost sale |
| complete sale | Transaction ledger | inventory, economy, report, repeat memory |
| informed no-sale | DecisionRecord | service judgment, customer outcome, no revenue, demand/lost-sale report |
| run deal | Pricing/Demand | margin, traffic mix, stock depletion, queue load |
| schedule more staff | StaffService | service capacity, labor cost, manager headroom |
| send break | StaffService | temporary capacity, fatigue/reliability |
| place purchase order | Ordering | committed cash, future receiving, future inventory, storage |
| choose broad assortment | Ordering | coverage, storage/cash, retrieval/receiving complexity |
| choose deep assortment | Ordering | high-demand resilience, narrower coverage |
| manager joins floor | Staff/Task | queue relief, delayed planning/receiving/admin |
| customer repeats | CustomerMemory | faster known context, demand history, dialogue variation |
| batch changes | Inventory | TFS current data, repeat interpretation, customer decision |
| promotion | Progression | new authority/information, not better recommendation math |

## 3. System boundary rules
### CustomerSimulation may
- generate truth, preferences, reveal plans and fictional outcomes.

It may not
- order products;
- change TFS scoring;
- modify inventory directly.

### RecommendationService may
- reproduce canonical TFS behavior against known input/current eligible inventory.

It may not
- read hidden truth;
- read player competency;
- read difficulty except through legitimate store/input state;
- read fictional satisfaction.

### InventoryService may
- own stock/location/reservations/events.

It may not
- decide which product is scientifically better;
- award progression directly.

### OutcomeService may
- generate fictional acceptance/satisfaction/repeat feedback.

It may not
- feed a shadow weight into TFS.

### ProgressionService may
- evaluate authoritative records and unlock agency.

It may not
- modify canonical recommendation outputs, prices or stock to make higher rank easier.

### Economy/Ordering may
- alter future stock and operational constraints.

It may not
- directly alter current customer recommendation ranking.

## 4. Customer ↔ shift pacing
Customer generation does not independently spawn whenever it wants. `TrafficDirector` allocates deterministic customer slots. The generator fills each slot with a profile consistent with:
- difficulty;
- scenario;
- anti-repetition;
- viability target;
- repeat quota.

This keeps customer content inside pacing capacity.

## 5. Customer ↔ TFS
Only KnownCustomerProfile enters TFS. When a new fact is revealed:
1. append fact;
2. create new immutable input snapshot;
3. execute canonical TFS;
4. preserve prior snapshot for analytics.

No mutation-in-place of historical recommendation records.

## 6. TFS ↔ inventory
Recommendation eligibility uses an authoritative inventory snapshot. If inventory changes materially before transaction commitment:
- current result can be marked stale;
- commit validator checks availability;
- player can rerun with current inventory.

A stale result never authorizes negative stock.

## 7. Inventory ↔ physical world
Jar/shelf fill is a view of InventoryService, not its own quantity.

`InventoryChanged` event drives:
- visual fill;
- stock-state icon;
- TFS eligibility refresh trigger;
- manager risk projection.

## 8. Queue ↔ progression
Throughput uses queue outcomes only after attribution. Structural overload from authored difficulty does not automatically lower player competency.

Service Judgment is intentionally separate from Throughput so:
- ask-all loses on flow;
- ask-none loses on information quality;
- targeted expert play can excel at both.

## 9. Economy ↔ recommendation coverage
Economy may calculate advisory CoverageScore by asking canonical TFS whether representative forecast profiles have viable current/projected paths. It may not derive independent terpene/chemistry scores.

This creates a real reason to stock niche coverage without claiming all variety is equally valuable.

## 10. Deals ↔ pacing
A deal has two linked effects:
- pricing/margin;
- demand modifier.

TrafficDirector applies the demand modifier to eligible customer/category slots. Therefore a strong deal can create a rush and stock pressure rather than only changing revenue.

## 11. Staff ↔ queue
Each available service staff member is an actual server only while in a service-capable state. Break, receiving, busy BOH task and escalation remove or reduce capacity.

This prevents manager UI from showing “3 staff” while all three are functionally unavailable.

## 12. Staff ↔ inventory
Restock/receiving assignments create InventoryEvents only when the corresponding physical/task stage completes. Assignment itself does not move stock.

## 13. Manager ↔ future floor
Every strategic manager action must resolve through a shared system:
- staffing -> StaffService capacity;
- order -> PO -> receiving -> InventoryService;
- deal -> Pricing + TrafficDirector;
- merchandising -> retrieval/access time + visibility demand modifier;
- intervention -> Staff/Task availability.

No free-floating “management buff.”

## 14. Repeat customer ↔ economy
Repeat history contributes to historical demand aggregation only at the same category/need level used by forecasts. It does not expose future repeat arrival certainty to the manager.

## 15. Difficulty ↔ all systems
Difficulty owns parameter selection, not business logic. It may select:
- customer distributions;
- traffic profile;
- starting inventory pressure;
- task pressure budget;
- physical tolerance;
- staff coverage scenario.

It may not fork implementation rules.

## 16. UX ↔ truth
UI never owns state. Every panel displays authoritative snapshots and sends commands to owning services.

Required stale-state handling:
- show snapshot version/time where useful;
- validate commands on submit;
- return corrective reason on conflict.

## 17. Analytics ↔ everything
Analytics are event-derived projections. Each metric must trace back to source records.

For debugging, any shift-score component should be inspectable down to:
- customer/transaction IDs;
- input/output snapshot hashes;
- queue timestamps;
- inventory events;
- staff/task events.

## 18. Integration event vocabulary
Minimum shared events:
- `CustomerEntered`
- `CustomerQueued`
- `ServiceStarted`
- `CustomerFactRevealed`
- `TfsQueryExecuted`
- `RecommendationSelected`
- `ProductReserved`
- `InventoryTransferred`
- `TransactionCompleted`
- `TransactionCanceled`
- `InventoryChanged`
- `StockRiskChanged`
- `CustomerAbandoned`
- `CustomerExited`
- `StaffAssignmentChanged`
- `BreakStarted`
- `BreakEnded`
- `TaskCreated`
- `TaskCompleted`
- `PurchaseOrderSubmitted`
- `DeliveryArrived`
- `ReceivingClosed`
- `ShiftPhaseChanged`
- `ShiftEnded`

## 19. Integration acceptance tests
1. A question changes TFS only through a changed input hash.
2. A sale changes jar/shelf visuals only through inventory events.
3. A manager order cannot create sellable stock before receiving.
4. A staff reassignment changes queue capacity only after state transition/handoff.
5. Difficulty preset swap with frozen input/store state leaves TFS output hash identical.
6. A repeat customer’s prior satisfaction cannot modify TFS result ordering.
7. Shift report totals reconcile exactly to authoritative ledgers.
8. Promotion evaluation can be reproduced from stored DecisionRecords/events.

## 20. Conflict resolution hierarchy for implementation
When implementation details disagree:
1. explicit current Nolan decision;
2. local canonical v7.11.4 for recommendation behavior;
3. current repository PROJECT_STATE for what exists;
4. canonical gameplay spec/decisions;
5. this V2 package as proposed expansion;
6. task packet/local implementation convenience.

Never change a higher layer silently to satisfy a lower one.

## 21. Deferral boundary
The following remain outside active implementation until floor + Lead/AM bridge proves fun:
- full accounting;
- HR simulation;
- supplier negotiation;
- corporate admin;
- deep scheduling calendar;
- unrelated minigames;
- any alternate recommendation science.
