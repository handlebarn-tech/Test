# DISPENSARY GAME — GAMEPLAY & SIMULATION SPECIFICATION
## Core Loop, Customers, Budtender Workflow, Inventory, Store Operations, Progression & AI Systems

**Version:** 1.0  
**Date:** 2026-10-29  
**Parent:** `MASTER_PLAN.md`  
**Primary source basis:** `References/Review_Budtender_Tool_Comprehensive_Chat_Record.md`  
**Status:** Canonical gameplay design for reconstruction unless later user decisions override it
**Extended:** 2026-10-30 by DES-003 with `Design/SPEC_DECISION_PRESSURE.md` (Nolan's decision-pressure spec, cited below as DP §n). Item-by-item status: `Design/DES-003_RECONCILIATION.md`.
**Add-on:** 2026-10-30 by IMP-002 with `Design/DESIGN_V2/` (Nolan's V2 pack, cited as V2 `<file>` §n; audit `Imports/IMP-001_DESIGN_V2_AUDIT.md`, approval DEC-063). **Precedence:** DP wins over V2 where they differ (DEC-063a). REVIEW-IMP1 A1–A4 bind (oracle = shipped engine per DEC-060; TFS snapshot = parser input per DEC-057; no TFS scores/ranks in the report per DEC-052; EMPTY_WITH_BACKSTOCK per DEC-055/061). V2 numbers are [GDD] starting values (GAP-DP-02).

---

# 1. Purpose

The project already has unusually detailed:

- physical-store planning;
- asset planning;
- terpene/recommendation-system history;
- Unity migration planning;
- agent-studio planning.

What was still missing was a complete answer to:

> **What does the player actually do, minute to minute, and how do the historical budtender-tool systems become gameplay?**

This document fills that gap.

---

# 2. Source-derived facts versus new game design

This specification uses two labels.

## SOURCE-DERIVED
Supported directly by the supplied project record.

Examples:

- inventory-only recommendations;
- natural-language customer intent;
- batch-aware chemistry;
- similarity;
- Floor Mode;
- pricing;
- deli-flower focus;
- fast counter decisions;
- no hallucinated products.

## GAME-DESIGN DECISION
A new simulation mechanic proposed to turn those systems into a coherent game.

Examples:

- customer patience meter;
- day scoring;
- restock tasks;
- shift progression;
- customer acceptance formula;
- manager progression.

Do not rewrite GAME-DESIGN DECISION items later as if they were historical features of the old tool.

---

# 3. Player fantasy

## Initial canonical role

The player begins as a **budtender working a shift inside the reconstructed dispensary**.

The core fantasy is:

> Read a customer, understand what they actually want, find the right product from real current inventory, serve them efficiently, keep the floor stocked, and survive increasingly busy shifts inside a living dispensary.

This makes the existing recommendation system mechanically important rather than decorative.

## Later progression

The player may gain responsibility for:

- restocking;
- inventory;
- opening/closing;
- deliveries;
- staff coordination;
- pricing/deals;
- manager-level store optimization.

The first playable vertical slice should not require all management systems.

---

# 4. Core design pillars

## 4.1 Fast human interpretation
Customers speak like customers, not database queries.

## 4.2 Inventory truth
The player can only sell what exists.

## 4.3 Batch matters
Two batches of the same strain may differ.

## 4.4 Physical work matters
The player moves through the store, handles jars/products, weighs deli flower, bags purchases and restocks.

## 4.5 Knowledge helps but does not bury the player
The recommendation engine is powerful; the floor UI is simple.

## 4.6 Rush pressure changes decisions
The player balances depth of consultation against queue/time pressure.

## 4.7 The store visibly changes
Inventory, jars, shelves and BOH stock respond to transactions.

## 4.8 Realism without administrative bloat
Simulate meaningful retail work, not every piece of enterprise software.

---

# 5. The minute-to-minute loop

Default customer loop:

```text
customer enters
→ joins queue / browses
→ reaches player
→ expresses need
→ player asks optional clarifying question(s)
→ player interprets intent/modifiers
→ recommendation engine presents eligible current inventory
→ player chooses/recommends product
→ customer accepts, asks follow-up, rejects, or compares
→ player retrieves/weighs product
→ transaction completed
→ inventory updates
→ customer satisfaction/outcome recorded
→ next customer
```

Between customers:

```text
restock
clean/organize
check jars
receive tasks
inspect low inventory
manage BOH/FOH movement
```

Rushes compress available time.

---

# 6. Shift loop

A full shift can follow:

```text
OPENING
→ NORMAL TRAFFIC
→ RUSH WINDOW
→ NORMAL TRAFFIC
→ SECOND RUSH / EVENT
→ LATE SHIFT
→ CLOSING
→ SHIFT REPORT
```

DP §61 names the phases Opening/Preparation → Steady Floor → Rush 1 → Recovery → Pressure Event / Rush 2 → Late Shift → Closing Summary; the second NORMAL TRAFFIC above is that **Recovery**, a preparation window (restock before the next rush, DP §49).

Not every shift needs identical timing.

Traffic profile can vary by:

- day;
- time;
- promotions;
- random event seed;
- progression difficulty.

---

# 7. Opening phase

Initial playable opening tasks should be limited.

Possible tasks:

- clock/start shift;
- check active deli jars;
- restock visibly low floor product;
- verify registers/POS state;
- read shift notes;
- inspect daily deal;
- identify products/batches newly available.

GAME-DESIGN DECISION:
Opening should usually take **2–5 minutes of gameplay**, not become a checklist simulator.

---

# 8. Customer generation model

Each customer gets a hidden `CustomerIntentProfile` (the TRUE profile; DP §3). In code this is the existing `Customer` class (`Simulation/Slice/Customers.cs`), extended in place rather than replaced. The player only ever holds a separate KNOWN profile (§49, DP §4).

Suggested fields:

```text
primaryIntent
secondaryIntent
avoidances
budget
preferredProductType
experienceLevel
priceSensitivity
decisionConfidence
patience
talkativeness
knowledgeLevel
brandPreference
similarStrainMemory
desiredConsultationDepth
purchaseProbability
```

No real-world PII.

---

# 9. Source-derived intent families

The historical tool explicitly used customer language around:

- sleep;
- anxiety / low-anxiety preference;
- pain;
- focus;
- energy;
- social;
- appetite in earlier output concepts;
- relaxing;
- functional;
- giggly;
- affordable;
- “no couch lock” style constraints.

Actual domain configuration should remain data-driven.

---

# 10. Customer language generator

The same intent should be expressible in many forms.

Example underlying intent:

```text
primary: relaxation
avoid: heavy sedation
budget: medium
```

Possible dialogue:

```text
“I want to chill but I still need to function.”
“Something relaxing, but I don't want to get stuck on the couch.”
“I need to unwind after work without getting knocked out.”
“Do you have something mellow that isn't super sleepy?”
```

The player should learn to interpret language rather than memorize one phrase.

---

# 11. Customer knowledge archetypes

## Novice
- vague language;
- asks more questions;
- may overfocus on Indica/Sativa or THC;
- needs simple explanation.

## Regular
- knows preferred effects;
- may name products/strains;
- moves faster.

## Enthusiast
- may ask about terpenes/batches/flavor;
- notices poor explanation.

## Price shopper
- fit matters, but budget strongly constrains choices.

## Decisive repeat-style customer
- “I liked X; what do you have like it?”
- drives Similar workflow.

## Indecisive
- several competing goals;
- may compare options;
- time-consuming during rush.

These archetypes alter dialogue, not the underlying inventory truth.

---

# 12. Customer constraints

A valid recommendation may need to satisfy:

```text
desired effect
avoidance
budget
product type
availability
quantity
time/use preference
similarity request
```

Hard constraints:

- unavailable item cannot be sold;
- quantity must exist;
- if customer requests deli flower, recommendation must be a valid deli candidate unless player redirects.

Soft constraints contribute to satisfaction.

---

# 13. Recommendation interaction

The player can use a compact tool/POS/tablet panel.

Rush view:

```text
customer intent summary
3 recommended current batches
price
availability
short “why”
one-tap compare
```

Detailed view:

```text
terpene profile
domain fit
batch details
similarity
alternatives
confidence/rationale
```

This directly preserves the historical **complex backend, simple floor experience** principle.

---

# 14. Manual skill versus tool assistance

The game should not turn into “click the top AI recommendation every time.”

The player still controls:

- which questions to ask;
- whether they interpreted the customer correctly;
- whether to prioritize budget or fit;
- what recommendation to present;
- whether to compare alternatives;
- when to stop talking during a rush.

The recommendation system is decision support.

---

# 15. Customer satisfaction model

GAME-DESIGN DECISION.

Satisfaction should be based on a transparent simulation model, not a claim of real medical outcome.

Suggested components:

```text
intent fit
constraint fit
price fit
service speed
explanation fit
availability success
player interaction quality
```

Conceptual score:

```text
satisfaction =
  intentFit * W1
+ constraintFit * W2
+ priceFit * W3
+ serviceQuality * W4
- waitPenalty
- mismatchPenalty
```

Weights are configurable.

Do not bake them permanently into code.

---

# 16. Recommendation quality

`intentFit` can derive from the recommendation domain engine.

Important:

- it is the TFS engine's own output (v7.11.4 parity) for the customer's true intent, used as an evaluation oracle only: it never reorders, filters or replaces what the player sees (DP §0A, §19; slice `ShiftSim.Fit`);
- it is not presented as a clinical certainty;
- customer satisfaction is a game simulation outcome.

This distinction protects both realism and epistemic honesty.

---

# 17. Customer response states

After recommendation:

```text
ACCEPT
COMPARE
ASK_WHY
ASK_CHEAPER
ASK_STRONGER
ASK_LESS_SEDATING
ASK_SIMILAR
REJECT
LEAVE
```

Probabilities depend on:

- satisfaction estimate;
- archetype;
- price;
- patience;
- player speed;
- confidence.

---

# 18. Similar workflow as gameplay

Customer:

> “I liked [strain]. What do you have that's like that?”

Flow:

```text
known/reference strain
→ terpene vector if available
→ eligible current inventory
→ cosine similarity
→ current-batch alternatives
→ player explanation
```

This is a direct translation of one of the historical tool's strongest workflows.

---

# 19. Compare workflow

Customer may narrow to two or three options.

Comparison should show only decision-relevant differences:

- fit;
- price;
- dominant profile differences;
- time/use lean;
- risk/avoidance notes;
- batch freshness as information if retained.

Do not flood the screen with raw chemistry unless expanded.

---

# 20. Deli flower service flow

Canonical interactive flow:

```text
select batch/jar
→ retrieve/open jar
→ choose requested weight
→ scoop/tong flower
→ scale
→ adjust weight
→ transfer to bag
→ label
→ handoff / transaction
```

The exact physical complexity can scale with difficulty/accessibility settings.

---

# 21. Weighting minigame philosophy

Do not make deli weighing frustrating.

The challenge should be:

- speed;
- reasonable accuracy;
- avoiding waste/overshoot;
- handling rush pressure.

Possible assist levels:

### Assisted
Player selects weight; animation completes.

### Standard
Player controls scoop amount and adjusts.

### Simulation
Fine manual control and tighter tolerance.

Default should be Standard.

---

# 22. Deli stock model

Per batch:

```text
total stock
backstock
jar stock
reserved/transaction amount
waste
sold
```

The jar is not infinite.

When low:

- visual fill changes;
- restock task appears;
- the player may need to retrieve backstock.

---

# 23. Packaged-product transaction

Packaged items skip weighing.

Flow:

```text
identify product
→ retrieve shelf/FOH stock
→ scan/select
→ price
→ bag
→ transaction
```

Packaged stock should still visibly deplete where practical.

---

# 24. POS transaction

Keep the interaction concise.

Potential steps:

- product list;
- weight/quantity;
- deal/price calculation;
- tax;
- payment;
- receipt/bag.

GAME-DESIGN DECISION:
Payment can be abstracted to avoid turning the game into a cash-register simulator unless the user later wants deeper cashier mechanics.

---

# 25. Payment methods

Possible:

```text
cash
card/debit-like abstract payment
```

Exact real dispensary payment restrictions are not necessary to the core game unless intentionally modeled.

Payment should mainly affect:

- animation;
- transaction time;
- cash drawer behavior.

---

# 26. Queue system

Customers:

```text
ENTER
→ BROWSE/QUEUE
→ ADVANCE
→ SERVICE
→ EXIT
```

Queue manager owns:

- ordered slots;
- path;
- spacing;
- register/service assignment.

Customers should not pathfind independently into arbitrary counter positions.

---

# 27. Patience

Each customer has:

```text
basePatience
currentPatience
rushModifier
archetypeModifier
```

Patience decreases while:

- waiting;
- player is idle during service;
- excessive consultation continues.

It may stabilize/improve when:

- customer is actively engaged;
- player explains a useful comparison.

Avoid hyperactive visible countdown bars by default. Use behavioral cues.

---

# 28. Rush system

A rush increases:

- arrival rate;
- queue length;
- service pressure.

It does **not** make recommendation math less accurate.

It changes the optimal player strategy, **per customer** (DP §37), not "always ask fewer questions":

```text
decisive regular   → minimal questions, fast service
ambiguous novice   → still 1–2 high-value questions
enthusiast         → shorten the talk at a service-experience cost
price shopper      → settle price first
repeat customer    → memory allows very fast service
```

Floor Mode, short questions and fewer comparisons are the usual tools, but over-trimming an ambiguous customer must cost as much as over-consulting a decisive one (DP §14, §18).

This turns the historical Floor Mode concept into actual gameplay value.

---

# 29. Traffic director

Use a `TrafficDirector`.

Inputs:

```text
shift time
day profile
difficulty
promotion/events
current queue
performance safeguards
seed
```

Outputs:

```text
next arrival time
customer archetype
intent profile
party size if ever supported
```

Cap arrivals to preserve playable performance.

---

# 30. Inventory authority

One model owns stock.

Never create:

```text
simulation says 20g
jar says 50g
POS says in stock
BOH says empty
```

Canonical inventory events:

```text
Receive
TransferBackstockToFloor
TransferToJar
Sell
Waste
Adjust
```

Every visual system subscribes to these events.

---

# 31. Restocking

Restocking creates physical movement and store rhythm.

Deli:

```text
jar low
→ retrieve correct batch from backstock
→ transfer stock
→ update jar fill
```

Packaged:

```text
floor shelf low
→ retrieve FOH/BOH unit/case
→ restock facing
```

GAME-DESIGN DECISION:
Restocking should be meaningful but not constant busywork.

---

# 32. BOH/FOH structure in gameplay

Physical areas should have gameplay purpose.

## FOH restock
Fast-access floor replenishment.

## BOH
Bulk backstock / orders.

## HUB/HUB2
Receiving/general inventory/operational tasks.

## Office
Management/reporting/money/admin tasks later.

## Break room
Atmosphere, staff behavior, optional break system later.

This makes expensive environment reconstruction mechanically useful.

---

# 33. Deliveries

Later milestone system:

```text
delivery arrives
→ receiving task
→ cases/totes enter HUB
→ manifest/inventory update
→ stock becomes available
→ restock later
```

Do not make delivery processing a vertical-slice blocker.

---

# 34. Waste

Deli flower can generate:

- minor handling waste;
- adjustment;
- optional moisture/operational loss abstraction.

For the game:

- keep waste small;
- make causes understandable;
- do not require real-world compliance destruction procedures unless deliberately simulated.

---

# 35. Store cleanliness

Optional/light system:

- clutter accumulation;
- trash;
- minor cleaning tasks.

Avoid turning the game into a janitorial simulator.

Cleaning works best as:

- visual polish;
- occasional task;
- customer/store score modifier.

---

# 36. Customer acceptance and purchase

Customer may:

```text
buy recommendation
buy alternate
decline
leave due to wait
leave due to price
```

A recommendation is not automatically a sale.

This preserves the old project's distinction between recommendation behavior and transaction truth.

---

# 37. Transaction ledger

Every completed game sale creates:

```text
Transaction
  id
  gameTime
  customerId
  items
  batchIds
  quantities
  prices
  discounts
  tax
  total
  recommendationContext
```

This is authoritative.

Do not maintain a separate manual `Sold` flag as transaction truth.

---

# 38. Feedback/outcome simulation

Historical target feedback was:

```text
requested goal
→ recommendation
→ exact batch
→ sale/no sale
→ outcome
```

In the game, post-purchase feedback can be:

- immediate satisfaction/acceptance;
- later simulated return/customer memory;
- aggregate hidden outcome model.

No PII.

---

# 39. Repeat customers

Later milestone.

Use persistent game IDs, not identity data.

Repeat customer can remember:

```text
prior purchase
prior satisfaction
favorite profile
budget tendency
```

This enables dialogue:

> “That thing you gave me last time was perfect.”

or:

> “Last one made me too tired.”

This creates gameplay around learning/feedback without recreating a surveillance CRM.

---

# 40. Learned recommendation signals

Later milestone only.

**Amended by DP §60 (DES-003, proposed DEC):** fictional outcomes never adjust the TFS recommendation score. The earlier `BaseRecommendationScore + LearnedOutcomeAdjustment` idea is withdrawn; it would alter the recommendation system and needs an explicit Nolan decision first.

Allowed uses of learned outcomes: customer memory, dialogue, player performance history, career scoring, a customer's willingness to repeat a purchase.

---

# 41. Product knowledge progression

GAME-DESIGN DECISION.

Player knowledge may improve through play:

- tooltips;
- training;
- repeated customers;
- product familiarity.

Do not lock basic recommendation functionality behind grinding.

Knowledge progression should reward:

- faster recognition;
- reduced need to open detail panels;
- optional bonuses.

---

# 42. Player performance metrics

End-of-shift metrics:

```text
sales
customers served
average service time
queue abandonment
recommendation fit
customer satisfaction
inventory errors
waste
restock responsiveness
revenue
```

Avoid making revenue the only score.

The historical tool explicitly prioritized fit over raw price.

---

# 43. Shift report

At closing:

```text
Shift Summary
- customers served
- revenue
- top requested intents
- best-performing recommendations
- stockouts
- low inventory
- average wait
- satisfaction
- waste
- notable events
```

This translates historical analytics into a useful game feedback loop.

---

# 44. Progression

Recommended progression:

## Phase 1 — New/standard budtender
- basic floor;
- recommendation;
- deli weighing;
- POS;
- restock.

## Phase 2 — Trusted/lead-level responsibilities
- heavier rushes;
- receiving;
- floor inventory decisions;
- additional product categories.

## Phase 3 — Assistant-manager style
- staffing/assignments;
- inventory exceptions;
- pricing/deal awareness;
- opening/closing.

## Phase 4 — Manager sandbox
- store optimization;
- ordering/merchandising;
- reports;
- staffing;
- multi-location only if ever desired.

Do not build Phases 3–4 before the core floor game is fun.

DP §71–86 refinements:

- Progression runs on six rolling competencies (Service Judgment, Throughput, Inventory Discipline, Operational Accuracy, Reliability, Leadership; 0–100, shown as Developing / Reliable / Strong / Expert), with promotion gates (placeholder values, DP §80), not generic XP.
- Promotion unlocks **control** (responsibility, information, decisions, authority), never a better recommendation engine (DP §81).
- Phase 2 adds receiving, stock movement, floor prioritisation, limited staff calls, more categories and more complex shifts; Phase 3 adds opening readiness, closing review, staff assignments, inventory exceptions, deal awareness, floor coverage and shift preparation; Phase 4 adds ordering, staffing, merchandising, deal strategy and inventory planning (DP §82–85).
- The floor game never disappears: a manager can still take a register, help a difficult customer, restock or resolve an escalation (DP §86).
- Promotion evidence (DEC-063b): V2 model replaces the DP §79 rolling update for gating: per competency, the median of the last 6 eligible shifts, at most one shift below gate − 10, fewer than 4 eligible shifts = insufficient evidence, a repeated seed gives no new evidence (V2 `05_PROGRESSION_CAREER.md` §5, §11). Gate values start at the gentler DP §80 levels [GDD] (GAME-024).

---

# 45. Difficulty

Difficulty should change:

- customer arrival pressure;
- patience;
- ambiguity;
- number of simultaneous constraints;
- weighing tolerance;
- stock scarcity;
- task concurrency.

It should not make recommendation science randomly wrong.

Difficulty acts on information, complexity, scarcity and concurrency, not reaction speed (DP §66). Identical TFS input + inventory + pricing gives identical TFS output in every difficulty mode; this is a hard regression gate (DP §124, DP-028). Profile fields: DP §67.
V2 add-on (DEC-063): starting preset numbers and a per-shift PressureBudget that caps stacked pressures (V2 `04_DIFFICULTY_SYSTEM.md` §4–5; GAME-022). Ambiguity uses DP's tiers 0–4, not V2's 0–3.

---

# 46. Accessibility / simulation assists

Configurable:

- simplified weighing;
- slower customer patience;
- reduced rush intensity;
- persistent intent summary;
- recommendation explanations;
- interaction highlighting;
- subtitles;
- text scaling.

---

# 47. Failure states

Avoid harsh game-over conditions.

Soft failures:

- customer leaves;
- poor satisfaction;
- refund/complaint abstraction;
- queue grows;
- stockout;
- wasted product;
- poor shift score.

Hard failure should be rare.

This is a work simulation, not a roguelike punishment loop unless the user later chooses otherwise.

---

# 48. Customer dialogue architecture

Do not hard-code all dialogue into NPC scripts.

Use structured intent data:

```text
DialogueTemplate
  intent
  archetype
  tone
  constraints
  phraseVariants
```

Generate/select natural language from templates.

The underlying intent remains deterministic for testing.

---

# 49. Clarifying questions

Player may ask limited questions:

```text
“What kind of experience are you looking for?”
“Do you want to stay functional?”
“Any budget you want to stay under?”
“Anything you want to avoid?”
“Did you like anything last time?”
```

Questions reveal hidden profile fields.

Too many questions cost time.

DP §4–16 make this structured [GDD]:

- The player holds a KNOWN profile: each field is unknown or known with a value, a confidence and a source (opener, player question, repeat memory, customer follow-up, rejection, purchase history).
- Openers reveal a data-defined subset (DP §6); customers carry an ambiguity tier 0–4 (DP §7).
- Question set Q1–Q8: desired effect, avoidance, stay functional, budget, product type (only once categories exist), something you liked, something you didn't like, time of use (DP §9). Q6 feeds the TFS Similar workflow (§18), never a new similarity model.
- A question about an already-known field reveals nothing and still costs time (DP §10). Customers differ in `QuestionTolerance` and `DesiredConsultationDepth`; excess questions add escalating friction, never instant anger (DP §11–14).
- `InformationCompleteness` and `InformationRisk` are gameplay/debug values only; they never replace or alter a TFS score (DP §15–17).
- **What reaches TFS:** only known facts, rendered as customer wording through the ported NL parser (`QueryParser` → engine), plus authoritative inventory and pricing. Hidden fields never do (DP §5).

---

# 50. Customer ambiguity

Some customers start with incomplete information.

Example:

```text
“I just want something good.”
```

The challenge is discovering:

- desired effect;
- constraints;
- budget.

Recommendation tool cannot magically know unrevealed intent.

---

# 51. Recommendation UI confidence

Do not show fake scientific precision by default.

Instead of:

```text
94.37% medically correct
```

use:

```text
Strong fit
Good fit
Possible fit
```

Optional detailed score can exist internally for ranking.

Uncertainty caused by missing customer information is shown separately from the TFS cards (e.g. CUSTOMER INFO COMPLETE / PARTIAL / NEED MORE), never as a competing fit score (DP §17).

---

# 52. Beginner customers

Do not use “myrcene = beginner safe.”

Beginner suitability in the game should be modeled through:

- customer preference;
- product/dose abstraction;
- avoidance;
- conversation;

not one terpene universal rule.

This directly corrects a historical criticism.

---

# 53. Product categories

Vertical slice priority:

1. deli flower;
2. packaged flower if needed;
3. pre-roll;
4. vape;
5. edible;
6. concentrate;
7. other categories later.

The historical system was deliberately deli-first.

Do not dilute the first playable build with every SKU category.

---

# 54. Deli weight options

Support store-configurable weights.

Do not hard-code assumptions beyond data.

A `WeightOption` can define:

```text
grams
displayName
price rule
availability
```

---

# 55. Price and fit

Canonical principle:

> Price matters, but it should not overwhelm fit.

Customer price sensitivity changes acceptable recommendation set.

Possible outcome:

- perfect fit too expensive;
- slightly lower fit inside budget becomes better service.

This creates meaningful tradeoffs.

---

# 56. Deals

Deals can create traffic and inventory pressure.

Potential gameplay effects:

- increased demand for eligible category;
- unusual rush;
- stockout pressure;
- customer asks “what's on deal?”

Deal rules use the ported pricing system.

---

# 57. Inventory scarcity

Scarcity creates interesting substitutions.

When top recommendation is out:

```text
find next current batch
or
use Similar workflow
```

The system should never recommend an unavailable phantom product.

---

# 58. Customer rejection

A rejection should not always mean player failure.

Possible reasons:

- price;
- wants different product type;
- changes mind;
- insufficient stock;
- preference mismatch.

Log reason separately.

---

# 59. NPC state machine

Customer high-level states:

```text
Spawn
Approach
Enter
Browse
Queue
Advance
Service
Consider
Transaction
Exit
Despawn
```

Optional:

```text
AbandonQueue
AskEmployee
BrowseMerch
```

Each state owns animation and navigation behavior.

---

# 60. Budtender/staff AI

Non-player employees later can:

- serve register;
- restock;
- carry case;
- idle;
- take break;
- handle queue.

Player should be able to understand what staff are doing from visible behavior.

DP §87–92 constraints for when staff exist (PS4): staff skills (speed, `TfsToolSkill`, accuracy, restock efficiency, independence, complex-customer skill, reliability) change how well a worker gathers customer information and uses the same TFS workflows, never which recommendation model they use. Weak staff fail through slowness, limited complexity and escalations to the player (take over / assist / leave), not corrupted recommendations or random absurd mistakes.

---

# 61. Staff scheduling

Later management feature.

Not needed for vertical slice.

When added:

```text
staff member
role
shift
skill
assigned zone
break
```

Avoid enterprise HR simulation.

---

# 62. Player interaction system

Common verb:

```text
Interact
```

Contextual targets:

- door;
- jar;
- scale;
- POS;
- product;
- box;
- tote;
- shelf;
- NPC;
- terminal.

Avoid a different control scheme for every object.

---

# 63. Carry system

Player can carry limited object types:

- small product;
- bag;
- jar where allowed;
- tote/case;
- clipboard optionally.

Use interaction anchors rather than fully simulated floppy physics for every carry item.

---

# 64. Physics philosophy

Use physics where it improves interaction.

Do not make every package a loose rigidbody.

Most store stock should be:

- instanced/static;
- pooled;
- interaction-swapped when picked up.

This protects performance.

---

# 65. Jar interaction

Jar can have states:

```text
Closed
Open
InUse
Low
Empty
```

Interaction anchors:

- lid;
- scoop/tongs;
- scale;
- bag.

The jar's visible fill derives from inventory.

---

# 66. Scale interaction

Display:

```text
current grams
target grams
difference
```

Standard mode can snap realistic increments.

A successful weigh commits inventory only after transaction/bag completion, not every scoop movement.

Use reservation state to avoid stock duplication.

---

# 67. Transaction reservation

When product is removed for service:

```text
available
→ reserved
→ sold
```

If transaction cancels:

```text
reserved
→ returned/available
```

This prevents stock desynchronization.

---

# 68. Inventory adjustments

Later management mechanic.

All adjustments should create a reason:

```text
count correction
waste
delivery
return-to-stock
```

This keeps simulation debug-friendly.

---

# 69. Game time

Use accelerated but readable time.

GAME-DESIGN DECISION:
Initial target can be:

```text
1 real second = 3–6 game seconds
```

Tune after playtesting.

Do not make a full eight-hour simulated shift take eight real hours by default.

Prefer variable compression (DP §63): active service, weighing and meaningful tasks run near natural time; quiet stretches cover more game time.

---

# 70. Shift duration

Initial design target:

```text
20–45 minutes per full shift
```

DP §62 narrows the representative full shift to **25–40 real minutes** (example split: opening 3, steady 6, rush 6, recovery 4, rush 2/event 7, late 5, report 3).

Short scenario modes can be:

```text
5–15 minutes
```

This is a proposal, not historical behavior.

---

# 71. Traffic pacing

A good shift alternates:

```text
pressure
→ recovery
→ pressure
```

Constant maximum queue becomes exhausting and eliminates thoughtful recommendation gameplay.

---

# 72. Events

Later optional events:

- sudden rush;
- delivery;
- product stockout;
- register unavailable;
- popular deal;
- staff calls for restock;
- difficult comparison customer;
- top seller runs low;
- several repeat customers at once;
- staff needs help (DP §65).

Keep events plausible and operational.

No random disaster system is needed.

---

# 73. Opening/closing progression

Vertical slice may skip full opening/closing.

When added, opening/closing should emphasize:

- stock;
- readiness;
- shift review;

not dozens of trivial switches.

---

# 74. Economy

For single-player:

```text
store revenue
COGS abstraction if desired
waste
discounts
labor later
```

Player progression should not require exact real business accounting.

The main economy goal is meaningful tradeoffs around:

- demand;
- stock;
- pricing;
- service quality.

---

# 75. Ordering

Later manager mechanic.

Potential loop:

```text
demand history
→ inventory report
→ order
→ delivery
→ stock
```

Do not build before selling/restocking is fun.

DP §94–98 for when it is built (PS4): inputs are current inventory, historical and recent demand, expected deals, category coverage, finite storage, purchasing budget and supplier availability; orders arrive after a lead time; future demand is never revealed exactly. Breadth (many SKUs, more TFS coverage, more stockouts) vs depth (few SKUs, rush resilience, fewer options) must not dominate universally. Management changes floor play only through authoritative inventory, never through recommendation weights (DP-032).

---

# 76. Merchandising

Later mechanic:

- shelf assignment;
- featured products;
- display density.

Could influence visibility/customer interest.

Do not override recommendation fit with arbitrary “premium = best.”

---

# 77. Training mode

The historical tool had education/training value.

Game can include optional training scenarios:

```text
customer intent quiz
batch comparison
similar strain
rush challenge
stock substitution
```

This is a natural secondary mode.

---

# 78. Scenario mode

Examples:

- Morning rush;
- Budget customers;
- Similar-strain challenge;
- Low-stock shift;
- Deli-heavy rush;
- Restock recovery.

Scenario mode is useful for testing gameplay systems independently.

---

# 79. Sandbox mode

Later:

- unlimited time;
- free movement;
- inventory controls;
- spawn customers;
- set rush level;
- inspect systems.

Useful for both players and QA.

---

# 80. Debug/game-master panel

Development-only panel:

```text
spawn customer
set intent
set inventory
advance time
trigger rush
set jar fill
teleport room
toggle AI
show NavMesh
show IDs
```

This drastically improves agent QA.

Must not leak into normal builds unless debug-enabled.

---

# 81. Save model

Persist:

- game day/shift;
- stock;
- unlocked systems;
- progression;
- customer memory if enabled;
- settings;
- current store state.

Versioned save schema.

---

# 82. Deterministic test mode

Allow:

```text
seed
customer sequence
inventory snapshot
time
```

QA can reproduce:

> customer #12 rejected because budget mismatch

rather than chase random behavior.

---

# 83. Game data assets

Suggested categories:

```text
StrainDefinition
BatchDefinition
ProductDefinition
PackageDefinition
PriceTier
DealRule
IntentDefinition
CustomerArchetype
DialogueTemplate
ShiftProfile
TrafficProfile
DifficultyProfile
```

Use data, not giant switch statements.

---

# 84. Key runtime services

Suggested architecture:

```text
GameClock
TrafficDirector
CustomerFactory
QueueManager
RecommendationService
InventoryService
PricingService
TransactionService
FeedbackService
SaveService
VisualInventoryService
TaskDirector
```

Avoid one omnipotent `GameManager`.

---

# 85. Event model

Important events:

```text
CustomerEntered
CustomerQueued
ServiceStarted
RecommendationMade
ProductReserved
TransactionCompleted
TransactionCanceled
InventoryChanged
JarLow
ShelfLow
RestockCompleted
CustomerExited
ShiftEnded
```

Systems subscribe rather than hard-reference everything.

---

# 86. Vertical slice definition

The first “this is a game” milestone requires:

- playable retail room graybox or first-art pass;
- one functional counter;
- one deli jar family;
- several valid batches;
- customer enters and queues;
- customer expresses intent;
- player uses recommendation UI;
- player picks a recommendation;
- player weighs/selects product;
- transaction completes;
- inventory decreases;
- jar visibly changes;
- customer leaves;
- shift stats update.

If this loop is not satisfying, do not build manager simulation yet.

---

# 87. Vertical slice content target

Recommended:

```text
10–20 strains/batches
3–5 customer archetypes
6 primary intent families
1 register/service point
1 deli workflow
1 rush event
1 shift summary
```

Use a small dataset first.

The full historical dataset can come after the loop is stable.

---

# 88. Vertical slice acceptance tests

### Functional
- unavailable batch never recommended;
- current stock decreases exactly once;
- canceled transaction restores reservation;
- jar fill matches stock;
- customer queue advances;
- shift metrics record transaction.

### UX
- recommendation reachable in seconds;
- player can understand top options;
- Floor Mode is not cluttered;
- no developer/scientific jargon dominates.

### Performance
- target hardware meets provisional frame target.

---

# 89. Customer simulation task decomposition

Do not assign “make customers.”

Split:

```text
NPC-001 locomotion
NPC-002 queue
NPC-003 intent profiles
NPC-004 dialogue templates
NPC-005 service state
NPC-006 acceptance/rejection
NPC-007 exit/abandon
NPC-008 repeat memory
NPC-009 animation integration
NPC-010 performance/LOD
```

---

# 90. Transaction task decomposition

```text
GAME-TRX-001 stock reservation
GAME-TRX-002 deli weight
GAME-TRX-003 packaged items
GAME-TRX-004 pricing
GAME-TRX-005 payment abstraction
GAME-TRX-006 transaction ledger
GAME-TRX-007 visual inventory update
```

---

# 91. Gameplay QA personas

Test at least:

### Fast expert player
Minimal questions; uses Floor Mode.

### New player
Needs explanation.

### Optimization player
Tries to maximize throughput.

### Detail player
Reads chemistry and compares.

The design should remain playable for all four.

---

# 92. Anti-exploit rules

Prevent:

- selling unavailable stock;
- duplicating reserved inventory;
- endless free restock;
- pause/interaction exploits if scoring time;
- repeatedly spawning easy customers for progression;
- selecting top recommendation without revealing enough customer intent if intent is ambiguous. This is done by leaving the query incomplete until the player learns more (DP §18), never by making the TFS top card wrong;
- refusing service when a viable TFS-supported path existed (`AvoidableNoSale`, DP §31).

---

# 93. Player knowledge and hidden information

The player should not automatically know every hidden customer preference.

The recommendation engine operates on what the player has actually captured.

This makes questioning skill matter.

---

# 94. Tool recommendation versus player recommendation

Store separately:

```text
systemSuggestedCandidates
playerRecommendedBatch
customerPurchasedBatch
```

This enables meaningful analytics:

- did player follow tool?
- did customer buy recommendation?
- did alternate sell?

Do not collapse all three into one field.

---

# 95. Shift analytics

Useful metrics:

```text
recommendation acceptance
tool-follow rate
average fit
average wait
average consultation time
sales
revenue
stockouts
abandonment
waste
```

These can later inform progression or management.

---

# 96. Customer outcome model and scientific humility

The game is allowed to simulate outcomes, but must not present its internal model as real medical prediction.

Use:

```text
customer satisfaction
reported preference
game outcome
```

not:

```text
clinical success probability
```

This follows the historical review's evidence-calibration concern.

---

# 97. Audio gameplay cues

Audio should communicate:

- customer arrived;
- queue movement;
- scanner/POS;
- drawer;
- scale;
- jar lid;
- bag;
- restock cart;
- delivery;
- low-key rush pressure.

Avoid arcade notification spam.

---

# 98. Visual gameplay cues

Prefer diegetic/subtle cues:

- jar visibly low;
- shelf gaps;
- customer body language;
- queue length;
- POS state;
- task marker only when needed.

Do not cover the realistic store with floating icons everywhere.

---

# 99. Tutorial

Teach by first shift:

1. greet customer;
2. identify goal;
3. use recommendation;
4. choose batch;
5. weigh;
6. sell;
7. restock.

Advanced chemistry comes later.

---

# 100. Non-goals for first playable version

Do not require:

- real customer accounts;
- Supabase auth;
- Dutchie/POS integration;
- multi-location play;
- enterprise reporting;
- full staffing simulator;
- ordering;
- payroll;
- full compliance simulation;
- dozens of product categories;
- photoreal hero NPCs before core loop works;
- (DP §131, until the decision-pressure systems prove fun) deep payroll, complex HR, multi-store management, full accounting, huge upgrade trees, random disasters, extensive janitorial play, cosmetic management with no simulation consequence.

---

# 101. Design unknowns

The supplied project record does **not** define:

- exact original Three.js gameplay loop;
- exact shift duration;
- exact player movement/controller;
- exact customer simulation;
- exact progression;
- exact weighing interaction;
- exact register interaction;
- exact win/failure structure.

The defaults in this document are therefore **new canonical game-design decisions** unless the user later changes them.

---

# 102. First gameplay workcells

After M0/M1:

### GAME-DESIGN-001
Convert this spec into data schemas and state diagrams.

### GAME-001
Authoritative inventory + transaction reservation.

### GAME-002
Recommendation domain integration.

### NPC-001
Customer state/navigation skeleton.

### NPC-002
Intent/archetype generator.

### UI-001
Floor Mode recommendation interface.

### GAME-003
Deli service interaction.

### GAME-004
Shift/traffic skeleton.

### QA-GAME-001
Deterministic vertical-slice test scenario.

---

# 103. Gameplay milestone roadmap

## G0 — Simulation skeleton
Clock, inventory, one customer, one transaction.

## G1 — Recommendation slice
Intent → recommendation → choice.

## G2 — Physical deli slice
Jar → scale → bag → sale.

## G3 — Queue/rush
Multiple customers and pressure.

## G4 — Restock
FOH/BOH movement and visible inventory.

## G5 — Full shift
Opening-lite → traffic → closing report.

## G6 — NPC depth
Archetypes, follow-ups, rejection, repeat memory.

## G7 — Management depth
Only after floor game proves fun.

---

# 104. Definition of “fun enough to expand”

Do not expand into management until testers can complete several shifts and the core loop demonstrates:

- understandable customer needs;
- meaningful recommendation choices;
- useful time pressure;
- satisfying physical handling;
- visible inventory consequence;
- desire to improve next shift.

If the core loop feels like data entry, fix it before adding features.

---

# 105. Canonical gameplay thesis

> The player is not merely ringing up cannabis products.

> The player is translating human intent into a constrained inventory decision under time pressure, then physically executing that decision inside a living store whose stock, customers and workflow respond.

That is the gameplay advantage the existing terpene/budtender project gives this simulation.

Decision-pressure extension (DP §1, §135): expert play is judgment, prioritisation and operational foresight, not repeatedly choosing the top card. Several decisions are reasonable, none is perfect, and improving one outcome costs something elsewhere.

> **TFS determines recommendation behavior. The game determines circumstances, information, pressure, physical execution, customer response, operational consequences, progression, and management.**

Evaluation (`ServiceUtility`, `BestAvailableResolution`, `DecisionRegret`, `DecisionQuality`, satisfaction, purchase threshold) answers "how well did the player handle this fictional customer?" and stays separate from the TFS engine in code, data, tests, UI and docs (DP §0A, §19–25). Shift scoring moves to SERVICE / FLOW / OPERATIONS with a star gate and severe-failure caps, revenue reported separately (DP §101–107).
