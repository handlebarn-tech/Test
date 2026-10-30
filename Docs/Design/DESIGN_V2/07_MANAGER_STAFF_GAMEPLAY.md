# 07 — STAFF & MANAGER GAMEPLAY

## 1. Core progression of decision scale
- Budtender: **What should I do for this customer?**
- Lead: **Who should handle what right now?**
- Assistant Manager: **How should I prepare and stabilize this shift?**
- Manager: **How do today’s choices shape the next several shifts?**

## 2. Staff model
Employees are competent agents with differentiated strengths.

```yaml
StaffMember:
  staff_id
  service_skill: 0..100
  speed: 0..100
  inventory_skill: 0..100
  operations_skill: 0..100
  reliability: 0..100
  consultation_style: QUICK | BALANCED | EXPLANATORY
  preferred_roles: []
  fatigue: 0..100
  current_state
  current_assignment
```

Staff skill alters duration/error probability within bounded plausible limits. It does not alter TFS truth.

## 3. Staff state machine
`OFF_SHIFT -> AVAILABLE -> ASSIGNED -> BUSY -> AVAILABLE`

Side states:
- `BREAK_PENDING`
- `ON_BREAK`
- `ESCALATION`
- `UNAVAILABLE`

Assignments are sticky enough to matter. Reassignment behavior:
- interruptible task: 5–10 sec handoff/travel latency;
- noninterruptible customer transaction: finish transaction first;
- receiving count segment: finish current unit/batch segment or explicitly hand off.

No instant role teleportation.

## 4. Active roles
- Counter Service
- Deli/Scale Support
- Packaged Retrieval
- Queue/Entry Support where appropriate
- Restock
- Receiving
- BOH Operations
- Break
- Flex

One employee has one primary role and may perform limited adjacent flex work while idle.

## 5. Staff service AI
Routine staff customer workflow:
1. accept next assigned customer;
2. gather information using a policy appropriate to staff skill/style;
3. call the same RecommendationService;
4. choose from canonical results using non-chemistry constraints;
5. retrieve/complete transaction;
6. escalate if exception threshold reached.

Staff cannot access hidden customer truth.

## 6. Escalation thresholds
Escalate to player/manager when:
- repeated customer rejection;
- no viable current path and customer disputes it;
- price/deal dispute;
- inventory discrepancy;
- modeled compliance/limit problem;
- customer requests manager;
- staff lacks authority for adjustment/exception.

Staff do not escalate ordinary solvable transactions merely to create player work.

## 7. Lead gameplay
### Information visible
- queue count/trend;
- staff role and current task;
- break windows;
- LOW/CRITICAL stock;
- receiving/task due horizon;
- escalations.

### Actions
- reassign staff;
- approve/shift break within allowed window;
- assign restock/receiving;
- take a station personally;
- mark a priority task;
- resolve routine escalation.

### Core tradeoff
Every reassignment has an opportunity cost. Pulling restock to counter may save the queue but create a stock interruption 5 minutes later.

## 8. Break system
Each shift block can generate one break window per eligible staff member.

Fields:
- earliest start;
- preferred start;
- latest start;
- duration;
- fatigue cost after latest threshold.

Player may advance/delay within the window. Missing the window reduces Reliability/Leadership and staff performance modestly; it does not trigger melodramatic punishment.

## 9. Assistant Manager pre-shift planning
Inputs:
- forecast traffic band by phase;
- scheduled staff/capabilities;
- current inventory risk;
- planned delivery;
- active deal;
- unresolved exception;
- station availability.

Decisions:
- opening role assignments;
- break windows;
- priority FOH replenishment;
- receiving owner;
- manager intervention reserve/flex role;
- opening task priority.

Planning time target: 60–120 sec, not a 10-minute spreadsheet.

## 10. Opening readiness state
State-derived checks:
- required register/scale stations available;
- minimum critical FOH stock;
- no unresolved reservation from prior shift;
- staff present/assigned;
- urgent exception acknowledged;
- receiving area capacity if delivery due.

The player acts in the world/UI to fix failures. They do not click redundant checkboxes to prove state already true.

## 11. Closing readiness
Check:
- active transactions resolved;
- reservations cleared;
- critical inventory exceptions surfaced;
- required waste/adjustment events logged;
- tasks either completed or explicitly handed off;
- next-shift critical stock risk summarized.

## 12. Receiving gameplay
Purchase order arrives as shipment object.

Flow:
`delivery arrives -> stage -> compare PO -> receive item/batch -> detect discrepancy -> inventory RECEIVE events -> allocate/stage -> close receipt`

Possible discrepancy:
- short fill;
- wrong item/batch;
- damaged unit;
- unexpected substitution;
- delayed line.

The player resolves only exception lines. Matching lines can be batch-processed to avoid clerical bloat.

## 13. Inventory exception states
- `COUNT_MISMATCH`
- `DAMAGED`
- `MISPLACED`
- `UNLABELED/UNKNOWN` only if project content supports it
- `DELIVERY_SHORT`
- `RESERVATION_STUCK`

Resolution must create explicit InventoryEvents with reason codes. Never “fix” by editing a UI number.

## 14. Manager planning horizon
Rolling 3–5 future shifts.

Dashboard:
- demand forecast bands;
- staffing capacity;
- inventory cover;
- open purchase orders;
- cash/headroom;
- storage;
- deal calendar;
- recent lost-sale attribution;
- staff competency/fatigue trends.

## 15. Staffing plan
Manager selects shift-level coverage, not a full HR scheduler.

For each future shift:
- number of staff blocks;
- capability mix;
- planned flex/lead coverage;
- delivery coverage if known.

Cost appears as LaborBudgetUnits/estimated variable labor contribution.

## 16. Merchandising
Merchandising changes operational access, not TFS truth.

Player chooses:
- packaged fast-access positions;
- deli priority locations/presentation;
- deal callout positions;
- cold-storage facing priority.

Effects:
- retrieval duration;
- restock frequency;
- customer visibility/demand modifier where appropriate.

No arbitrary “+10% sales because shelf is pretty.” Effects must be tied to access/visibility systems.

## 17. Deals
Manager chooses from approved templates with visible:
- margin impact;
- expected demand-lift band;
- stock requirement;
- floor-load implication;
- duration/cooldown.

## 18. Manager intervention model
At any moment player can step onto floor.

Intervention is valuable when:
- queue spike;
- employee break collision;
- escalation;
- receiving conflict;
- emergency restock;
- station outage;
- complex repeat customer.

Opportunity cost:
- planning tasks stop progressing;
- receiving/admin task may age toward due horizon;
- no “manager does everything for free” strategy.

## 19. Delegation quality
Leadership analytics compare:
- whether assigned staff had the capability;
- whether task timing matched urgency;
- whether reassignment created avoidable downstream bottleneck;
- whether manager personally intervened when delegation was inadequate.

Do not score “number of commands issued.” Micromanagement is not leadership.

## 20. Staff fatigue
Use lightly.

Fatigue increases after sustained busy periods and missed breaks, influencing speed/error probability by small bounded amounts (e.g. max 10–15% service-time impact). It should create break/coverage tradeoffs, not a survival meter.

## 21. Future consequences
Manager decisions alter later shifts through:
- stock depth/coverage;
- staffing capacity;
- delivery timing;
- receiving workload;
- cash/storage headroom;
- deal-driven demand;
- staff fatigue/readiness.

No abstract “management score modifier” should substitute for these systems.

## 22. Anti-automation safeguard
Staff can competently handle ordinary work, but player decisions remain at:
- ambiguous/high-value customer escalations;
- prioritization under concurrency;
- stock/restock timing;
- staffing/break coverage;
- receiving exceptions;
- ordering/forecast decisions;
- when to intervene personally.

If the optimal Manager strategy becomes “stand in office and watch meters,” the design has failed.

## 23. Acceptance criteria
- competent staff clear ordinary work without constant correction;
- role reassignment has visible benefit and cost;
- manager intervention can rescue acute pressure but delays other work;
- staffing plan changes queue performance through real service capacity;
- receiving creates actual inventory only through receive events;
- breaks matter but do not become chore spam;
- management never changes canonical TFS behavior.
