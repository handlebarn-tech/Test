Proposed by Nolan 2026-10-30; integration status in DES-003 handoff

# DISPENSARY GAME
# DECISION PRESSURE, CUSTOMER INTELLIGENCE, PROGRESSION & MANAGEMENT INTEGRATION SPECIFICATION

**Status:** Proposed canonical GAME-DESIGN DECISION extension  
**Integration mode:** Merge into existing systems. Do not replace working architecture unless required.  
**Historical status:** Everything introduced by this document is new game design unless it already exists in canonical project documentation or explicit `DECISIONS.md` entries.  
**Primary objective:** Turn the existing technically strong transaction simulation into a game where expert play is defined by judgment, prioritization and operational foresight rather than repeatedly choosing the mathematically highest recommendation card.

---

# 0. ONE-TIME HUB INTAKE INSTRUCTIONS

These instructions apply **once, when this specification is first introduced into the repository**.

Their purpose is only to prevent this document from creating duplicate tasks, files, features, systems, or competing implementations of work that is already complete or planned.

During initial intake only:

1. Compare this specification against:
   - `GAMEPLAY_SIMULATION_SPEC.md`
   - `DECISIONS.md`
   - `PROJECT_STATE.md`
   - DES-002
   - GAME-004 through GAME-010
   - UX-002
   - any later gameplay/design task created after those files.

2. For every requirement below classify it:

```text
ALREADY_IMPLEMENTED
ALREADY_PLANNED
PARTIALLY_IMPLEMENTED
MISSING
CONFLICTS_WITH_CURRENT_DESIGN
```

3. Do not create duplicate systems.

4. If an existing system can absorb the requirement cleanly, extend it.

5. If an existing implementation uses different naming but provides the same behavior, retain the existing naming unless changing it materially improves architecture.

6. Create new workcells only for requirements that remain genuinely missing or incomplete after this one-time reconciliation.

After this specification has been integrated into the project plan, **do not repeat this entire audit before every future Hub session or every new task**. Normal repository state, task dependency, ownership, and review procedures resume.

All implementation work must still follow the project's normal task/review process.

---

# 0A. HARD RECOMMENDATION-SYSTEM AUTHORITY

This is a non-negotiable project boundary.

The gameplay simulation is built **around** the TFS Budtender Tool recommendation system. It is not allowed to create a competing interpretation of cannabis recommendation logic.

The deployed behavioral reference is:

`https://tfs-phx-budtender.netlify.app/`

The current deployed version at the time this specification was written identifies as **v7.11.4**.

For shipped recommendation behavior, the live TFS Budtender Tool is the target behavioral contract. The verified local v7.11.4 source may be used as the implementation-level authority for reproducing that live behavior where the repository has already established equivalence. Unreleased local development must not silently redefine shipped recommendation behavior.

If a future explicit Nolan decision intentionally changes the recommendation contract, that decision must be recorded through the normal repository decision process.

Otherwise:

> **The game must preserve the TFS recommendation system. Gameplay systems may change the circumstances in which the player uses it, but may not change what the recommendation system means.**

The game may NOT independently:

- invent a second recommendation formula;
- replace the TFS scoring model;
- reinterpret the six effect-domain system;
- change terpene weighting merely for game balance;
- rerank TFS recommendation results with a gameplay-only "true fit" model;
- secretly promote or demote strains because a hidden NPC profile says something different;
- make price override TFS fit ranking unless the TFS tool itself does so for the supplied query/context;
- change parser meaning merely to make a customer easier or harder;
- alter exclusion behavior merely for difficulty;
- change Similar away from the TFS similarity behavior;
- make Floor Mode change recommendation truth rather than presentation/workflow;
- introduce hidden THC/lineage ranking that conflicts with the TFS system;
- make unavailable inventory eligible when the TFS inventory contract would exclude it;
- convert game outcome data into an unapproved replacement for the TFS recommendation model.

The live tool currently establishes key behavioral principles including:

```text
natural-language customer input
→ intent/modifier/negation parsing
→ TFS terpene/domain recommendation logic
→ current eligible inventory
→ ranked matches by fit
→ explanation/rationale
```

It also establishes:

- COA/terpene-profile-based matching;
- six effect domains;
- ranking by fit rather than alphabetical order or simple price order;
- out-of-stock exclusion from recommendations;
- natural-language intent/modifier/negation handling;
- Similar based on terpene-profile similarity;
- Floor Mode as a simplified presentation mode rather than a different recommendation engine.

These are not gameplay knobs.

## Allowed gameplay interaction with the recommendation system

Gameplay MAY control:

- what the simulated customer says;
- which facts the player has learned from that customer;
- what natural-language query or structured equivalent reaches the TFS recommendation logic;
- whether the player asks another question before searching;
- whether the player chooses to use Search, Similar, Compare, Floor Mode, or another preserved TFS workflow;
- current game inventory/stock, where inventory data remains authoritative;
- current game pricing/deals where those are mapped through the preserved pricing system;
- time pressure;
- queue pressure;
- stock pressure;
- physical retrieval time;
- whether the player follows the TFS recommendation;
- whether the customer accepts the player's choice;
- fictional game satisfaction/outcome after the recommendation;
- career/progression consequences of player decisions.

Gameplay MUST NOT alter the recommendation result because the simulation privately knows more than the TFS tool was given.

Example:

```text
TRUE NPC PROFILE:
wants relaxation
strongly dislikes sedation

PLAYER HAS ONLY LEARNED:
wants relaxation
```

The game sends only the known request to the TFS recommendation system.

If the TFS system ranks Candidate A first from that known request, the game must not secretly rerank Candidate B above it because the hidden NPC profile dislikes sedation.

Instead, the gameplay consequence is:

```text
player can ask another relevant question
→ learn the sedation constraint
→ provide the new information to the TFS recommendation workflow
→ TFS system produces the appropriate result from the richer request
```

That distinction is fundamental.

## Evaluation layer boundary

This specification uses concepts such as:

- `BestAvailableResolution`
- `DecisionRegret`
- `DecisionQuality`
- customer satisfaction;
- customer purchase threshold.

These are **gameplay evaluation systems**, not recommendation systems.

They may evaluate how well the player's final service decision handled the fictional customer's complete simulated situation.

They may NOT:

- feed hidden truth back into TFS ranking;
- rewrite TFS candidate order;
- replace TFS fit scores;
- present themselves as alternative cannabis-science scoring;
- become a second recommendation engine.

The TFS system answers:

> **Given the information supplied to the recommendation system and current eligible inventory, what does the TFS system recommend?**

The gameplay evaluation layer answers:

> **Given everything that actually happened in this fictional customer interaction, how well did the player handle the situation?**

Those are separate questions and must remain separate in code, data, tests, UI, and documentation.

---

# 1. CORE DESIGN THESIS

The game should regularly create situations where:

> Several decisions are reasonable, no decision is perfect, and improving one outcome creates a cost somewhere else.

The player should optimize the **store as a system**, not solve customers independently.

The desired gameplay progression is:

```text
EARLY GAME
learn individual customer service

MID GAME
balance customer service against queue and stock

LATE FLOOR GAME
anticipate store problems before they happen

LEAD / ASSISTANT MANAGER
coordinate people and operations

MANAGER
shape tomorrow's operating conditions through today's decisions
```

Expertise should move from:

```text
"What is the best strain?"
```

to:

```text
"What is the best decision for this customer
given what I know,
what is available,
who is waiting,
what is running low,
and what else is happening in the store?"
```

---

# 2. NON-NEGOTIABLE DESIGN INVARIANTS

## 2.1 Recommendation correctness

The TFS recommendation engine remains authoritative and deterministic for equivalent inputs.

Difficulty must never come from:

```text
randomly wrong chemistry
randomly corrupted rankings
fake recommendation errors
invisible dice rolls overriding a TFS recommendation
gameplay-only reranking of TFS candidates
```

Difficulty comes from:

```text
incomplete information
limited time
stock constraints
budget constraints
customer preferences
queue pressure
competing store tasks
uncertain future demand
```

## 2.2 Information separation

Maintain four independent layers:

```text
TRUE CUSTOMER PROFILE
KNOWN CUSTOMER PROFILE
TFS SYSTEM RECOMMENDATIONS
ACTUAL PURCHASE / FICTIONAL GAME OUTCOME
```

Never collapse them.

## 2.3 Inventory truth

Only one inventory authority exists.

Every system must derive from it:

```text
recommendation availability
jar fill
FOH stock
BOH stock
transaction eligibility
restock need
stockout
sales
reports
```

## 2.4 No guaranteed perfect solution

Some customers must intentionally have no 100% satisfying available product.

The game evaluates:

> Did the player make the best service decision available under the circumstances?

not:

> Did the player always create a perfect outcome?

This evaluation may not modify TFS recommendation ranking.

## 2.5 No-sale can be correct

The player must occasionally receive credit for recognizing:

> We do not currently have a product I should confidently sell for what this customer ultimately wants.

Do not encourage forcing every interaction into a sale.

This is a gameplay/service evaluation and does not redefine the TFS recommendation engine.

## 2.6 Customer satisfaction is not player performance

Customer satisfaction measures the fictional customer.

Decision quality measures the player's handling of the situation.

These are correlated, but not identical.

---

# 3. CUSTOMER DATA MODEL

Existing customer generation should evolve toward the following conceptual model.

Do not necessarily use these exact class names if equivalent structures already exist.

## 3.1 TrueCustomerProfile

Simulation-only hidden truth.

```csharp
TrueCustomerProfile
{
    string CustomerId;

    IntentVector TrueIntent;

    string PrimaryIntent;
    string SecondaryIntent;

    List<string> Avoidances;

    Money? Budget;
    PriceSensitivity PriceSensitivity;

    ProductCategoryPreference ProductPreference;

    float? DesiredWeightGrams;

    TimeOfUsePreference TimePreference;

    string SimilarReferenceStrainKey;
    string SimilarReferenceBatchId;

    ExperienceLevel Experience;

    CustomerKnowledgeLevel Knowledge;

    float DecisionConfidence;

    float BasePatienceSeconds;

    float Talkativeness;

    float DesiredConsultationDepth;

    float QuestionTolerance;

    float PurchaseThreshold;

    float CompromiseTolerance;

    float SubstitutionTolerance;

    CustomerMemoryRef RepeatMemory;

    CustomerArchetype Archetype;

    CustomerBehaviorFlags Flags;
}
```

---

# 4. KNOWN CUSTOMER PROFILE

This represents only information the player has obtained.

```csharp
KnownCustomerProfile
{
    CustomerId;

    KnownField<Intent> PrimaryIntent;

    KnownField<Intent> SecondaryIntent;

    KnownField<List<Avoidance>> Avoidances;

    KnownField<Money> Budget;

    KnownField<ProductCategory> ProductPreference;

    KnownField<float> DesiredWeight;

    KnownField<TimeOfUse> TimePreference;

    KnownField<SimilarityReference> SimilarReference;

    KnownField<ExperienceLevel> Experience;

    int QuestionsAsked;

    float ConsultationSeconds;

    float InformationCompleteness;

    ProfileRevealMask RevealedFields;
}
```

Suggested generic field representation:

```csharp
KnownField<T>
{
    bool IsKnown;
    T Value;
    float Confidence;
    RevealSource Source;
}
```

Possible `RevealSource` values:

```text
CUSTOMER_OPENER
PLAYER_QUESTION
REPEAT_MEMORY
CUSTOMER_FOLLOWUP
CUSTOMER_REJECTION
PURCHASE_HISTORY
```

---

# 5. CRITICAL RULE: RECOMMENDATION INPUT

The TFS recommendation workflow receives only information legitimately available to the player plus authoritative current store state required by the preserved TFS system.

Conceptually:

```text
KnownCustomerProfile
+
player-selected/searchable customer wording
+
current authoritative inventory
+
current preserved pricing/deal state
```

It does **not** receive:

```text
TrueCustomerProfile
hidden avoidances
hidden budget
hidden satisfaction weights
future outcome
BestAvailableResolution
DecisionRegret
DecisionQuality
```

If the current game implementation uses natural-language parser queries rather than a structured `KnownCustomerProfile`, preserve that TFS input architecture. `KnownCustomerProfile` then exists as simulation state that determines what wording/facts the player can legitimately provide.

Do not bypass the TFS parser/scoring workflow merely because the simulation has structured fields.

---

# 6. CUSTOMER OPENER SYSTEM

Every customer opener should reveal a subset of their profile.

Use an explicit `OpenerRevealProfile`.

Example:

```json
{
  "openerType": "RELAXATION_GENERIC",
  "reveals": [
    "primaryIntent"
  ],
  "possibleLines": [
    "I want something relaxing.",
    "I need something to chill out with.",
    "I'm looking for something mellow."
  ]
}
```

Another:

```json
{
  "openerType": "RELAX_FUNCTIONAL_BUDGET",
  "reveals": [
    "primaryIntent",
    "avoidances",
    "budget"
  ]
}
```

Dialogue example:

> “I want something relaxing, but I still need to function. Trying to stay around twenty bucks.”

This customer should require less questioning.

---

# 7. AMBIGUITY TIERS

Assign an `AmbiguityTier`.

```text
TIER 0 — EXPLICIT
TIER 1 — MOSTLY CLEAR
TIER 2 — PARTIAL
TIER 3 — VAGUE
TIER 4 — CONTRADICTORY
```

### Tier 0

Example:

> “I want something energetic for daytime, nothing anxiety-heavy, under $25.”

Player should normally not need additional questions.

### Tier 1

> “Something relaxing for tonight. Nothing too crazy.”

One relevant question may help.

### Tier 2

> “Something relaxing.”

Multiple constraints remain unknown.

### Tier 3

> “What's good?”

Player must discover the actual need.

### Tier 4

> “I want something really relaxing but I absolutely can't get sleepy.”

The request itself contains tension.

The player must gather enough information to decide how to phrase/use the preserved TFS workflow.

---

# 8. QUESTION SYSTEM

Questions should become structured gameplay actions.

Conceptual:

```csharp
CustomerQuestionDefinition
{
    string Id;

    CustomerField TargetField;

    string DisplayText;

    float BaseTimeCostSeconds;

    float QuestionToleranceCost;

    Predicate<KnownCustomerProfile> RelevantWhen;

    RevealRule RevealRule;
}
```

---

# 9. INITIAL QUESTION SET

## Q1 — Desired effect

> “What kind of experience are you looking for?”

Reveals or improves confidence in:

```text
PrimaryIntent
SecondaryIntent
```

Time:

```text
3–5 sec
```

## Q2 — Avoidance

> “Anything you definitely don't want?”

Reveals:

```text
Avoidances
```

Time:

```text
2–4 sec
```

## Q3 — Functional requirement

> “Do you need to stay functional?”

Useful for discovering customer wording/context related to:

```text
sedation concerns
daytime use
work/social context
```

Time:

```text
2–3 sec
```

## Q4 — Budget

> “Trying to stay under anything?”

Reveals:

```text
Budget
PriceSensitivity
```

Time:

```text
2–3 sec
```

## Q5 — Product type

> “Were you looking for flower, a vape, edible, or something else?”

Reveals:

```text
ProductPreference
```

Only relevant once categories exist.

## Q6 — Similar product

> “Anything you've had before that you liked?”

Reveals:

```text
SimilarReference
```

This should feed the preserved TFS Similar workflow rather than a new similarity model.

## Q7 — Negative past experience

> “Anything you've had before that you didn't like?”

Possible reveals:

```text
Avoidances
PriorOutcome
```

## Q8 — Time/use

> “When are you planning on using it?”

Possible output:

```text
Day
Evening
Night
Any
```

The revealed answer can become part of the natural-language input/context supplied to the TFS recommendation workflow.

---

# 10. QUESTION RELEVANCE

Questions should not provide value merely because the player clicked them.

Example:

Customer opener:

> “I need something for sleep, nothing energetic, under $20.”

Asking:

> “What's your budget?”

should provide:

```text
0 new information
```

and still consume time.

This is intentional.

---

# 11. QUESTION TOLERANCE

Customers should differ in willingness to answer unnecessary questions.

Suggested:

```text
QuestionTolerance = 0.0–1.0
```

Example archetypes:

```text
Decisive regular      0.20
Price shopper         0.35
Normal customer       0.60
Novice                0.80
Enthusiast            0.90
Indecisive            1.00
```

Do not treat these as permanent final values.

Use data-driven tuning.

---

# 12. EXCESS QUESTION PENALTY

After enough low-value questions:

```text
CustomerPatience -= unnecessaryQuestionPenalty
ServiceQuality -= mild penalty
Queue continues accumulating wait
```

Do not make customers instantly angry.

Use escalating friction.

Example:

```text
first unnecessary question:
  negligible penalty

second:
  small penalty

third:
  moderate penalty

repeated questioning:
  customer may say:
  "I don't really know, man."
  "I just want something."
  "Can you just show me something?"
```

---

# 13. CUSTOMER CONSULTATION DEPTH

Each customer gets:

```text
DesiredConsultationDepth = 0.0–1.0
```

Meaning:

```text
0.0 immediate transaction
0.25 very short interaction
0.50 standard consultation
0.75 wants explanation
1.00 highly engaged/detail-oriented
```

---

# 14. SERVICE DEPTH MATCH

Track:

```text
ActualConsultationDepth
```

derived from:

```text
questions
comparisons
detail views
explanation actions
consultation time
```

Concept:

```text
ConsultationDepthFit =
1 - abs(
    DesiredConsultationDepth
    -
    ActualConsultationDepth
)
```

This prevents both:

```text
rushing everyone
```

and:

```text
overconsulting everyone
```

from becoming optimal.

---

# 15. CUSTOMER INFORMATION COMPLETENESS

Define an internal metric.

```text
InformationCompleteness =
sum(
 known decision-relevant field weights
)
/
sum(
 all relevant field weights
)
```

Possible weights:

```text
primary intent       0.30
critical avoidance   0.25
budget               0.15
product type         0.10
secondary intent     0.10
time/use             0.05
similar reference    0.05
```

Only include fields relevant to that customer.

Example:

If customer has no meaningful budget constraint, budget should not reduce completeness.

`InformationCompleteness` is a gameplay/debug concept. It must not replace or alter the TFS recommendation score.

---

# 16. INFORMATION RISK

Some unknowns should be more dangerous than others.

Define:

```text
InformationRisk =
Σ hiddenCriticalFieldRisk
```

Examples:

Unknown:

```text
budget
```

may be moderate gameplay risk.

Unknown:

```text
strong customer-stated sedation avoidance
```

may be high gameplay risk.

This may inform gameplay evaluation and UI uncertainty.

It must not secretly rerank TFS recommendations.

---

# 17. RECOMMENDATION CONFIDENCE PRESENTATION

Do not invent a second scientific confidence score that competes with the TFS tool.

If the game communicates uncertainty caused by incomplete customer information, keep it clearly separate from TFS fit/ranking.

Possible gameplay-only wording:

```text
CUSTOMER INFO COMPLETE
CUSTOMER INFO PARTIAL
NEED MORE CUSTOMER INFO
```

TFS recommendation cards retain their preserved TFS meanings.

Do not transform `InformationCompleteness` into a replacement TFS fit score.

---

# 18. PREVENT TOP-CARD AUTOPILOT WITHOUT RERANKING TFS

Do not intentionally make the first TFS recommendation wrong.

Instead make the **query context incomplete until the player learns enough**.

Example:

Known customer wording:

```text
"something relaxing"
```

The player searches.

TFS returns whatever v7.11.4 correctly returns for that request and current inventory.

The game does not modify that ranking.

Player asks:

> “Do you need to stay functional?”

Customer says yes.

Player now has richer legitimate information and can search/refine using wording equivalent to:

```text
"relaxing but need to stay functional"
```

TFS may return a different ranking because **its input changed legitimately**.

That is the intended gameplay.

Difficulty comes from deciding whether obtaining the extra information is worth the time.

---

# 19. SERVICE EVALUATION MODEL

Create a game-simulation evaluation function separate from the TFS recommendation engine.

It evaluates how the player's eventual service decision handled the **fictional customer's full simulated situation**.

Concept:

```text
ServiceUtility =
TfsRecommendationAlignmentComponent
+ CustomerConstraintHandling
+ BudgetHandling
+ ProductHandling
+ QuantityHandling
+ SimilarRequestHandling
+ ConsultationHandling
+ AvailabilityHandling
```

Important:

`ServiceUtility` is not cannabis recommendation science.

It is a game-performance measure.

The TFS recommendation component must be grounded in preserved TFS output, not a new chemistry model.

---

# 20. HARD VS SOFT SERVICE CONSTRAINTS

## Hard constraints

Examples:

```text
not in stock
illegal transaction quantity
requested category unavailable and customer refuses substitution
insufficient quantity
```

Hard constraint failure can make a sale ineligible.

## Soft constraints

Examples:

```text
budget slightly exceeded
customer did not like the consultation depth
customer preferred another product format
player ignored a stated preference
```

These may reduce service outcome.

Do not independently infer cannabis-effect correctness outside the TFS system.

---

# 21. BEST AVAILABLE RESOLUTION

At service-decision time evaluate the **available service actions** the player could reasonably take.

Store:

```text
BestAvailableResolution
BestAvailableServiceUtility
```

Possible resolution actions include:

```text
sell TFS-ranked candidate
sell another TFS-valid candidate
ask another question
use Similar
use Compare
offer a cheaper valid alternative
retrieve/restock required inventory
make an informed no-sale
```

This is simulation/debug data only.

Crucially, `BestAvailableResolution` does not mean:

> calculate a hidden superior strain ranking.

It means:

> given the preserved TFS outputs/workflows, available inventory, customer-stated information, and operational situation, what service action best handled the fictional interaction?

---

# 22. DECISION REGRET

Calculate:

```text
DecisionRegret =
BestAvailableServiceUtility
-
ChosenServiceUtility
```

Examples:

```text
Best 94
Chosen 93
Regret 1

Best 76
Chosen 74
Regret 2

Best 95
Chosen 61
Regret 34
```

This is game-performance math only.

It may not feed back into TFS recommendation ranking.

---

# 23. DECISION QUALITY

Suggested:

```text
DecisionQuality =
1 - clamp(
    DecisionRegret / RegretTolerance,
    0,
    1
)
```

Alternative piecewise version:

```text
Regret 0–3:
Excellent

4–8:
Good

9–15:
Acceptable

16–25:
Poor

26+:
Major service mistake
```

Tune from playtests.

---

# 24. WHY THIS MATTERS

Player A encounters a situation where limited inventory means even excellent service produces only moderate fictional satisfaction.

Player A chooses the best TFS-supported service path available.

Player A made an excellent decision.

Player B has an easy high-quality TFS-supported option available but ignores important customer information and chooses poorly.

Player B made the worse decision.

Raw fictional satisfaction alone could hide that difference.

Decision quality exists to evaluate player judgment, not to replace TFS recommendation science.

---

# 25. CUSTOMER PURCHASE THRESHOLD

Each fictional customer may have:

```text
PurchaseThreshold
```

This represents willingness to buy, not cannabis recommendation correctness.

It can depend on:

```text
price
whether stated needs were addressed
availability
patience
consultation experience
personal indecision
```

Do not derive purchase threshold from an independent hidden chemistry model that contradicts TFS.

---

# 26. CUSTOMER RESPONSE LOGIC

Inputs may include:

```text
TFS recommendation presented
customer-stated requirements
price
availability
CustomerPatience
DecisionConfidence
ConsultationDepthFit
QueueWait
Archetype
```

Possible response:

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

Preserve existing response-state architecture.

---

# 27. CUSTOMER FOLLOW-UP AS NEW INFORMATION

Follow-up questions from the customer can reveal additional profile fields.

Example:

Player presents an option.

Customer:

> “Do you have anything cheaper?”

Now:

```text
BudgetKnown = true
PriceSensitivity confidence increases
```

Example:

Customer:

> “Is that going to make me tired?”

Now:

```text
sedation concern becomes known
```

The player can then re-use/refine the preserved TFS workflow with that new customer information.

Failed first attempts become information events rather than hidden reranking events.

---

# 28. NO-PERFECT-SERVICE SITUATIONS

Introduce:

```text
NoPerfectFitRate
```

This means no available **service resolution** perfectly satisfies every fictional customer/operational objective.

It must not mean the game declares TFS recommendations scientifically wrong.

Suggested default early-game:

```text
5–10%
```

Normal:

```text
10–20%
```

Higher difficulty:

```text
20–30%
```

These values are starting ranges only.

---

# 29. NO-PERFECT-SERVICE PATTERNS

Generate intentionally through valid operational combinations.

### Pattern A — Budget conflict

```text
TFS best-fit recommendation exceeds stated budget
cheaper TFS-valid candidate exists
```

### Pattern B — Stock conflict

```text
ideal TFS workflow points toward unavailable/sold-out item
valid current alternative exists through preserved fallback/Similar behavior
```

### Pattern C — Stated preference conflict

```text
customer's desired combination creates a difficult compromise
```

The game does not resolve this using an alternative chemistry model. It uses TFS workflows and customer choice.

### Pattern D — Product-type conflict

```text
customer prefers category unavailable
willing to consider alternative
```

### Pattern E — Quantity conflict

```text
desired item has insufficient requested quantity
```

### Pattern F — Similarity conflict

```text
customer wants something like previous strain
closest TFS Similar options are unavailable or outside budget
```

### Pattern G — Multi-constraint conflict

```text
effect request + budget + availability + product preference cannot all be satisfied simultaneously
```

---

# 30. INFORMED NO-SALE

Add service resolution:

```text
INFORMED_NO_SALE
```

Valid when no reasonable current TFS-supported service path can meet the customer's stated willingness to buy.

Examples:

```text
nothing available in requested category and customer refuses substitute
all acceptable options exceed strict budget
required quantity unavailable
customer rejects all TFS-supported alternatives
```

Player may communicate:

> “I don't really have anything that fits what you're asking for right now.”

This is a service outcome.

It is not an alternate recommendation engine.

---

# 31. AVOIDABLE NO-SALE

If a clearly viable TFS-supported service path existed but the player simply refuses service:

```text
AVOIDABLE_NO_SALE
```

This prevents score exploitation.

---

# 32. SERVICE RESOLUTION ENUM

Recommended:

```csharp
enum ServiceResolution
{
    IdealSale,
    GoodSale,
    GoodCompromise,
    AcceptableCompromise,
    CustomerAlternate,
    InformedNoSale,
    PriceRejection,
    StockRejection,
    PreferenceRejection,
    WaitAbandonment,
    AvoidableMismatch,
    AvoidableNoSale
}
```

---

# 33. CUSTOMER SATISFACTION

Customer satisfaction may include:

```text
whether the purchased option addressed the customer's stated need through the preserved TFS recommendation context
price fit
service experience
wait
consultation-depth match
availability outcome
```

Do not claim simulated satisfaction is real pharmacological prediction.

Do not use a hidden competing chemistry score.

---

# 34. PLAYER SERVICE SCORE

Suggested components:

```text
DecisionQuality
QuestionEfficiency
ConsultationDepthFit
ServiceTimePerformance
AvoidableErrorPenalty
```

Concept:

```text
ServicePerformance =
  DecisionQuality * 0.55
+ QuestionEfficiency * 0.15
+ ConsultationDepthFit * 0.10
+ SpeedQuality * 0.20
```

Initial tuning only.

---

# 35. QUESTION EFFICIENCY

Concept:

```text
UsefulInformationGained
/
QuestionCost
```

Track:

```text
RelevantQuestions
IrrelevantQuestions
RepeatedQuestions
CriticalFieldsRevealed
```

Do not expose raw formula unless useful.

Shift report can summarize:

```text
Questions/customer
Useful question rate
```

---

# 36. RUSH SYSTEM

Rush gameplay should create triage.

During rush:

```text
queue grows
waiting customers lose patience
current customer still needs service
stock may become critical
restock opportunities disappear
```

The player decides:

```text
how much information is enough?
```

---

# 37. CUSTOMER-SPECIFIC RUSH STRATEGY

Do not make:

```text
rush = always ask fewer questions
```

Instead:

### Decisive regular

Optimal:

```text
minimal questions
fast service
```

### Ambiguous novice

Optimal may still require:

```text
1–2 high-value questions
```

### Enthusiast

During normal traffic:

```text
longer discussion may be rewarded
```

During severe rush:

```text
player may shorten interaction
at some service-experience cost
```

### Price shopper

Resolve price early.

### Repeat customer

Existing memory may allow very fast service.

---

# 38. QUEUE OPPORTUNITY COST

For each action during active service calculate:

```text
QueueCost =
Σ waiting customer patience loss
```

Do not display numerically.

Use for simulation and QA.

Examples:

```text
ask question
open detailed comparison
leave counter for stock
linger in UI
```

All have opportunity cost.

---

# 39. PLAYER FEEDBACK FOR QUEUE PRESSURE

Prefer diegetic cues:

```text
visible queue length
customer body language
audio
glances
fidgeting
short comments
```

Avoid constant giant countdown bars.

Optional accessibility mode may expose clearer patience indicators.

---

# 40. RESTOCK MODEL

Every sellable product should conceptually distinguish:

```text
ServiceReadyStock
Backstock
TotalStock
ReservedStock
```

Deli:

```text
JarStock
Backstock
```

Packaged:

```text
FOHStock
BOHStock
```

---

# 41. SERVICE-READY STATES

Recommended:

```text
HEALTHY
LOW
CRITICAL
EMPTY_WITH_BACKSTOCK
SOLD_OUT
```

---

# 42. LOW

Definition:

```text
below configured low threshold
```

Meaning:

```text
no immediate service failure
restock warning/opportunity
```

---

# 43. CRITICAL

Meaning:

```text
likely to run out within near-term demand
```

Could depend on:

```text
remaining units/grams
recent demand
deal status
upcoming rush
```

---

# 44. EMPTY WITH BACKSTOCK

Important state.

Example:

```text
JarStock = 0
Backstock = 300g
```

Product is still in building.

It cannot be served instantly.

Possible behavior must remain consistent with the preserved TFS inventory contract.

Recommended gameplay representation:

```text
candidate can remain recognizable as available in building
but service requires retrieval/restock time
```

If the TFS recommendation implementation only understands binary in-stock state, do not silently redefine that meaning. Instead represent service-readiness outside the recommendation engine or extend inventory mapping only through an explicit reviewed decision that preserves TFS behavior.

---

# 45. SOLD OUT

```text
ServiceReadyStock = 0
Backstock = 0
```

Remove from eligible recommendations according to preserved TFS inventory rules.

---

# 46. PROACTIVE RESTOCK

Track whether restock occurred:

```text
before LOW
at LOW
at CRITICAL
after EMPTY
```

Analytics:

```text
ProactiveRestocks
ReactiveRestocks
EmergencyRestocks
```

---

# 47. RESTOCK PRIORITY

Suggested internal operational urgency:

```text
RestockUrgency =
StockRisk
*
ExpectedDemand
*
OperationalImportance
```

Where:

### StockRisk

How close to empty.

### ExpectedDemand

Recent sales + active deal + customer mix.

### OperationalImportance

How consequential a stockout is for service coverage based on observed game usage.

Do not independently rescore cannabis recommendations.

---

# 48. DO NOT AUTOMATE RESTOCK DECISION TOO MUCH

The player should see enough information to infer urgency.

Do not simply display:

```text
RESTOCK THIS NOW
```

for every item.

Possible UI:

```text
LOW
CRITICAL
deal icon
recent demand trend
```

The player decides.

---

# 49. RESTOCK DURING QUIET PERIODS

Recovery phases become preparation phases.

Good player:

```text
checks critical jars
restocks popular items
anticipates deal demand
returns to counter before rush
```

Poor player:

```text
does nothing
gets hit by multiple stock problems later
```

No artificial punishment needed.

The store itself creates the consequence.

---

# 50. INTERRUPTIBLE TASKS

Restock and retrieval actions should be interruptible where practical.

State:

```text
NOT_STARTED
IN_PROGRESS
INTERRUPTED
COMPLETED
```

If interrupted:

```text
preserve partial logical state only if physically sensible
```

Avoid half-transferred stock unless the interaction explicitly models it.

---

# 51. DEMAND MODEL

Demand should derive from:

```text
traffic profile
customer archetype distribution
intent distribution
active deal
product/category popularity
repeat customers
inventory availability
time of shift
```

Do not script every sale.

Do not change TFS recommendation ranking to force demand.

---

# 52. DEMAND SIGNALS FOR PLAYER

Later systems may expose:

```text
recent sales
low stock
active deals
yesterday's top sellers
expected rush
```

Do not provide perfect forecasts.

The player should form expectations.

---

# 53. REPEAT CUSTOMER MEMORY

This should become a major system.

Data:

```csharp
CustomerMemory
{
    string PersistentCustomerId;

    int VisitCount;

    int LastVisitDay;

    List<PurchaseMemory> Purchases;

    List<PreferenceMemory> Preferences;

    List<AvoidanceMemory> Avoidances;

    float TypicalBudget;

    float BudgetConfidence;

    string FavoriteStrain;

    string FavoriteBatch;

    List<OutcomeMemory> Outcomes;
}
```

---

# 54. PURCHASE MEMORY

```csharp
PurchaseMemory
{
    string TransactionId;

    string ProductId;

    string BatchId;

    float Quantity;

    Money Price;

    string CustomerRequestText;

    float ImmediateSatisfaction;

    OutcomeMemory LaterOutcome;
}
```

Store the TFS recommendation context used for the transaction where appropriate.

Do not generate a replacement chemistry profile from fictional outcome data.

---

# 55. OUTCOME TAGS

Do not require pseudo-medical claims.

Use game-simulation tags:

```text
LOVED_IT
WORKED_WELL
GOOD_VALUE
TOO_SLEEPY
TOO_ENERGIZING
TOO_EXPENSIVE
DID_NOT_LIKE
WANTS_SIMILAR
WANTS_DIFFERENT
```

These tags are fictional game feedback.

They do not redefine TFS terpene/domain logic.

---

# 56. REPEAT CUSTOMER DIALOGUE GENERATION

Dialogue should derive from memory.

### Positive

> “That thing you gave me last time was perfect.”

### Mixed

> “I liked the last one, but it made me too tired.”

### Negative

> “I didn't really like what I got last time.”

### Similar request

> “You got anything like that one I bought last time?”

### Availability request

> “Do you still have that same one?”

---

# 57. REPEAT CUSTOMER INFORMATION ADVANTAGE

Repeat memory can pre-populate known customer facts.

Example:

```text
previously said they like relaxation
previously complained about heavy sedation
typical budget around $25
```

This rewards history.

Player can formulate a better TFS query faster.

---

# 58. MEMORY UNCERTAINTY

Do not assume preferences are permanent.

Memory entries can have confidence.

```text
PreferenceConfidence
```

Older memories can decay slightly.

Customers may also say:

> “I'm looking for something different today.”

Then current intent overrides history.

---

# 59. SAME STRAIN / NEW BATCH

Important batch-aware case.

Previous:

```text
Kush Cake
Batch A
```

Current:

```text
Kush Cake
Batch B
```

The preserved TFS batch-aware logic remains authoritative.

Do not automatically assume identical recommendation behavior because the strain name matches.

Do not invent a separate game chemistry model to resolve the difference.

---

# 60. LEARNED OUTCOME SIGNALS

If the game later uses fictional customer outcomes for gameplay learning, keep them separate from the TFS recommendation engine unless Nolan explicitly approves a recommendation-system change.

Allowed uses include:

```text
customer memory
dialogue
player performance history
career scoring
customer willingness to repeat a purchase
```

Do not automatically implement:

```text
TFS recommendation score
+
game learned outcome adjustment
```

That would alter the recommendation system and requires explicit approval.

---

# 61. SHIFT STRUCTURE

Recommended target:

```text
Opening / Preparation
Steady Floor
Rush 1
Recovery
Pressure Event / Rush 2
Late Shift
Closing Summary
```

---

# 62. REPRESENTATIVE SHIFT COMPRESSION

Do not literally simulate every uneventful minute of eight hours.

Target:

```text
25–40 real minutes
```

Example:

```text
Opening           3 min
Steady            6 min
Rush 1            6 min
Recovery           4 min
Rush 2/Event       7 min
Late Shift         5 min
Report             3 min

Total             34 min
```

Tune through playtesting.

---

# 63. TIME COMPRESSION

Prefer variable/structural compression over making customer conversations absurdly fast.

During:

```text
active customer
manual weighing
meaningful store task
```

time should feel natural.

Quiet stretches can represent more game time.

---

# 64. SHIFT PRESSURE CURVE

Define:

```text
PressureLevel 0–1
```

Influenced by:

```text
arrival rate
queue
active tasks
stock problems
staff coverage
events
```

Useful for:

```text
music/audio
NPC behavior
traffic pacing
difficulty telemetry
```

Do not directly alter TFS recommendation math.

---

# 65. EVENT DESIGN

Events should emerge from operations where possible.

Strong events:

```text
popular deal creates rush
top seller runs low
delivery arrives
register unavailable
difficult comparison customer
multiple repeat customers
staff needs help
```

Weak events:

```text
random disaster for excitement
arbitrary machine explosion
unrelated chaos
```

Keep events plausible.

---

# 66. DIFFICULTY MODEL

Difficulty should primarily affect:

```text
information
complexity
scarcity
concurrency
```

not reaction speed and never recommendation correctness.

---

# 67. DIFFICULTY PROFILE

```csharp
DifficultyProfile
{
    float AmbiguityRate;

    float MultiConstraintRate;

    float ConflictRate;

    float NoPerfectFitRate;

    float TopChoiceScarcityRate;

    float ArrivalRateMultiplier;

    float PatienceMultiplier;

    int TargetConcurrentTasks;

    float RepeatCustomerRate;

    float EnthusiastRate;

    float IndecisiveRate;

    float WeighTolerance;

    float StockPressureMultiplier;
}
```

---

# 68. BEGINNER DIFFICULTY

Characteristics:

```text
clearer customers
fewer conflicting constraints
good inventory coverage
lower queue pressure
longer patience
fewer simultaneous tasks
```

Still use the real preserved TFS recommendation behavior.

---

# 69. STANDARD DIFFICULTY

Characteristics:

```text
mixed ambiguity
regular scarcity
some no-perfect-service customers
normal queue
meaningful rushes
restock pressure
```

This should represent intended game.

---

# 70. EXPERT DIFFICULTY

Characteristics:

```text
more ambiguous customers
more conflicting constraints
less perfect inventory coverage
more simultaneous operations
more consequential restock timing
more complex repeat customers
tighter staffing
```

Do not simply cut every patience value in half.

Do not change TFS recommendation results for identical inputs.

---

# 71. PLAYER COMPETENCY SYSTEM

Avoid generic XP as core career progression.

Track competencies:

```text
SERVICE_JUDGMENT
THROUGHPUT
INVENTORY_DISCIPLINE
OPERATIONAL_ACCURACY
RELIABILITY
LEADERSHIP
```

---

# 72. SERVICE JUDGMENT

Derived from:

```text
DecisionQuality
AvoidableMismatchRate
InformedNoSaleQuality
QuestionEfficiency
RepeatCustomerOutcomes
proper use of TFS recommendation workflows
```

---

# 73. THROUGHPUT

Derived from:

```text
CustomersServed
AverageServiceTime
AverageWait
QueueAbandonment
ConsultationEfficiency
```

Do not reward only raw speed.

---

# 74. INVENTORY DISCIPLINE

Derived from:

```text
StockoutsPrevented
EmergencyRestocks
ProactiveRestocks
InventoryErrors
Waste
CorrectBatchHandling
```

---

# 75. OPERATIONAL ACCURACY

Derived from:

```text
CorrectWeights
CorrectPricing
TransactionLimits
CorrectProducts
CorrectBatch
SuccessfulTransactionCompletion
```

---

# 76. RELIABILITY

Derived over multiple shifts.

Possible:

```text
minimum performance consistency
few severe errors
task completion
shift preparedness
```

This prevents one lucky perfect shift from immediately unlocking leadership.

---

# 77. LEADERSHIP

Later.

Derived from:

```text
staff assignment quality
delegation
store-wide outcomes
coverage
escalation handling
```

---

# 78. COMPETENCY RANGE

Suggested:

```text
0–100
```

But do not expose exact numbers unless useful.

Player-facing representation might be:

```text
Developing
Reliable
Strong
Expert
```

---

# 79. COMPETENCY UPDATE

Use rolling performance rather than permanent raw accumulation.

Example:

```text
NewCompetency =
OldCompetency * 0.8
+
RecentPerformance * 0.2
```

This is conceptual.

Purpose:

```text
performance matters continuously
not just grinding volume
```

---

# 80. PROMOTION GATES

## Budtender → Trusted

Example:

```text
Service Judgment >= 60
Throughput >= 55
Inventory Discipline >= 50
Operational Accuracy >= 70
CompletedShifts >= required
```

## Trusted → Lead

```text
Service Judgment >= 70
Throughput >= 65
Inventory Discipline >= 65
Operational Accuracy >= 80
Reliability >= 65
```

## Lead → Assistant Manager

```text
Reliability >= 75
Inventory Discipline >= 75
Leadership >= 60
Operational Accuracy >= 85
```

Exact values are tuning placeholders.

---

# 81. PLAYER AGENCY UNLOCKS

Promotion should unlock control.

Not:

```text
+20% recommendation accuracy
```

The game must never buff the player's TFS recommendation engine as a career reward.

Instead:

```text
more responsibility
more information
more decisions
more authority
```

---

# 82. BUDTENDER PHASE

Player controls:

```text
own customer interactions
own weighing
own POS
basic restocking
TFS recommendation workflows
```

---

# 83. TRUSTED / LEAD PHASE

Unlock:

```text
receiving
stock movement
floor prioritization
limited staff calls
additional product categories
more complex shifts
```

---

# 84. ASSISTANT MANAGER PHASE

Unlock:

```text
opening readiness
closing review
staff assignments
inventory exception decisions
deal awareness
floor coverage decisions
shift preparation
```

---

# 85. MANAGER PHASE

Unlock:

```text
ordering
staffing
merchandising
deal strategy
inventory planning
store optimization
```

---

# 86. CORE FLOOR GAME NEVER DISAPPEARS

Even as manager:

```text
player can jump onto register
help difficult customer
use TFS recommendation workflows
restock
resolve escalation
```

Management should create better reasons for returning to floor gameplay.

---

# 87. STAFF MODEL

Staff should be competent but differentiated.

Suggested:

```csharp
StaffMember
{
    ServiceSpeed;
    TfsToolSkill;
    OperationalAccuracy;
    RestockEfficiency;
    Independence;
    ComplexCustomerSkill;
    Reliability;
}
```

`TfsToolSkill` affects how effectively an AI worker gathers customer information and uses the preserved TFS workflow. It must not give the worker a different recommendation model.

---

# 88. STAFF SHOULD NOT BE RANDOMLY STUPID

Poor staff should usually fail through:

```text
slower service
limited complexity capacity
poor question selection
more frequent need for escalation
lower throughput
```

not:

```text
randomly corrupted TFS recommendations
random absurd mistakes
constant intentional sabotage
```

---

# 89. STAFF ASSIGNMENTS

Player chooses broad role:

```text
REGISTER
FLOOR_SUPPORT
RESTOCK
RECEIVING
FLOAT
BREAK
```

AI determines individual actions within role.

---

# 90. STAFF CAPACITY

Each employee has workload capacity.

Example:

```text
Register:
handles one active customer

FloorSupport:
can assist questions/retrieval

Restock:
services stock tasks

Float:
reacts to highest-priority eligible task
```

---

# 91. CUSTOMER ESCALATION

If complexity exceeds employee capability:

```text
employee may request player
```

Examples:

```text
complex enthusiast
multiple stated constraints
repeat customer with detailed history
unusual comparison
```

Player decides:

```text
take over
assist
leave employee to handle
```

---

# 92. STAFF TRADEOFF

Fast worker with weak TFS-tool/customer-information skill:

```text
excellent for simple rush customers
poor for complex consultations
```

Strong tool/customer-service expert but slow:

```text
excellent for enthusiasts/novices
less ideal for pure throughput
```

This creates actual assignment decisions without changing TFS recommendation truth.

---

# 93. MANAGEMENT ECONOMY

Keep it deliberately bounded.

Track:

```text
cash/purchasing budget
inventory value
revenue
COGS abstraction
waste
discount impact
labor cost abstraction
```

No need for full bookkeeping.

---

# 94. ORDERING SYSTEM

Inputs:

```text
current inventory
historical demand
recent demand
expected deals
category coverage
storage capacity
purchasing budget
supplier availability
```

Player decides:

```text
what
how much
when
```

---

# 95. ORDERING BREADTH VS DEPTH

## Breadth strategy

Many products, lower quantities.

Benefits:

```text
more TFS-recommendation inventory coverage
more substitutions
fewer situations where no appropriate current inventory exists
```

Risk:

```text
frequent stockouts
more inventory complexity
```

## Depth strategy

Fewer products, more quantity.

Benefits:

```text
strong rush resilience
fewer popular-item stockouts
```

Risk:

```text
less recommendation flexibility
more customer requests with limited current options
```

Neither should dominate universally.

---

# 96. STORAGE CAPACITY

Finite storage prevents:

```text
order everything
```

Storage may be represented abstractly at first.

Later tied to physical BOH/HUB space if desired.

---

# 97. LEAD TIME

Orders should not appear instantly.

Concept:

```text
order today
delivery future shift/day
```

This forces forecasting.

---

# 98. DEMAND UNCERTAINTY

Do not reveal exact future demand.

Player gets imperfect signals:

```text
historical sales
scheduled deal
day type
recent trends
```

Then makes judgment.

---

# 99. DEAL SYSTEM

At manager level, deal choice can affect:

```text
traffic
category mix
margin
stock depletion
queue pressure
```

Example:

Discount slow-moving product:

```text
increase demand
clear stock
possibly increase traffic
```

Deal has both economic and operational effect.

Use preserved pricing/deal rules where those already exist.

Do not alter TFS recommendation fit merely because a deal exists except where the preserved TFS system itself handles budget/tier/deal context.

---

# 100. MERCHANDISING

Keep light.

Possible effect:

```text
featured products
slightly more likely to be asked for
```

Do not let shelf position rerank TFS recommendations.

---

# 101. SHIFT SCORE

Use three primary categories:

```text
SERVICE
FLOW
OPERATIONS
```

---

# 102. SERVICE SCORE

Suggested:

```text
DecisionQuality
AvoidableMismatch
InformedNoSale
ConsultationDepthFit
RepeatCustomerPerformance
TFS workflow usage quality
```

---

# 103. FLOW SCORE

Suggested:

```text
AverageWait
AverageServiceTime
CustomersServed
Abandonment
QueueRecovery
```

---

# 104. OPERATIONS SCORE

Suggested:

```text
Stockouts
ProactiveRestock
EmergencyRestock
Waste
InventoryErrors
TaskCompletion
```

---

# 105. REVENUE

Report separately.

Revenue matters.

Revenue should not overwhelm every other score.

---

# 106. OVERALL RATING

Avoid pure average.

Suggested gate model:

```text
3 STAR:
all three categories acceptable
no severe failure

2 STAR:
overall acceptable
one category weak

1 STAR:
major operational/service breakdown
```

Later 4–5 stars if desired.

---

# 107. SEVERE FAILURE FLAGS

Examples:

```text
multiple avoidable illegal transactions
severe inventory desync
extreme avoidable abandonment
repeated major service mistakes
```

A severe failure may cap overall rating.

---

# 108. SHIFT REPORT

Main summary:

```text
Customers Served
Revenue
Average Wait
Average Service Time
Average Decision Quality
Customer Satisfaction
Abandonment
Stockouts
Waste
```

---

# 109. SERVICE DETAIL

```text
Ideal Sales
Good Compromises
Acceptable Compromises
Informed No-Sales
Avoidable Mismatches
Avoidable No-Sales
```

---

# 110. CONSULTATION DETAIL

```text
Questions per Customer
Relevant Question Rate
Average Information Completeness
Overconsulted Customers
Underconsulted Customers
```

---

# 111. INVENTORY DETAIL

```text
Proactive Restocks
Reactive Restocks
Emergency Restocks
Stockouts
Lost Sales from Stock
```

---

# 112. FLOW DETAIL

```text
Peak Queue
Wait Abandonment
Average Queue
Rush Throughput
Recovery Performance
```

---

# 113. DEBUG PANEL

Development-only.

Expose:

```text
TrueCustomerProfile
KnownCustomerProfile
InformationCompleteness
InformationRisk
Exact query/context supplied to TFS
TFS SystemCandidates
TFS candidate order
PlayerSelectedCandidate
BestAvailableResolution
BestAvailableServiceUtility
ChosenServiceUtility
DecisionRegret
DecisionQuality
CustomerSatisfaction
QuestionTolerance
DesiredConsultationDepth
ActualConsultationDepth
QueueCost
```

Keep TFS scoring fields clearly labeled as TFS values.

Keep gameplay evaluation fields clearly labeled as gameplay values.

Never display `DecisionQuality` as a recommendation-fit score.

---

# 114. DEBUG REJECTION EXPLANATION

Every rejection should be explainable.

Example:

```text
REJECT:
TFS query used:
"something relaxing"

TFS recommendation selected:
Candidate A

Customer information not yet learned:
strict $20 budget

Service outcome:
customer asked for cheaper option

Gameplay cause:
budget constraint had not been discovered
```

QA should never have to guess.

Do not explain rejection by claiming a hidden game chemistry model knew a TFS recommendation was wrong.

---

# 115. DETERMINISTIC STRESS TEST SUITE

Implement these as data-driven deterministic test scenarios where possible.

All tests touching recommendations must assert that TFS behavior remains unchanged for identical inputs.

---

## TEST DP-001 — Explicit Easy Customer

Setup:

```text
Customer:
clear primary intent
clear budget
no avoidance
ideal current item available
normal queue
```

Expected:

```text
minimal/no questioning needed
TFS workflow returns expected v7.11.4-equivalent result
fast service rewarded
```

Purpose:

Ensure new complexity does not make simple customers cumbersome.

---

## TEST DP-002 — Hidden Avoidance / Refined Query

Opener:

> “I want something relaxing.”

Hidden/customer-not-yet-stated:

```text
doesn't want heavy sedation
```

Step 1:

Player searches equivalent of:

```text
"something relaxing"
```

Expected:

TFS result exactly matches preserved TFS behavior for that query/current inventory.

Step 2:

Player asks avoidance/functional question.

Customer reveals:

```text
"but I need to stay functional"
```

Player searches equivalent of:

```text
"relaxing but need to stay functional"
```

Expected:

TFS result exactly matches preserved behavior for the richer query.

Purpose:

Prove information acquisition changes **input**, not recommendation rules.

---

## TEST DP-003 — Redundant Question

Opener explicitly includes:

```text
budget
avoidance
intent
```

Player asks budget anyway.

Expected:

```text
no information gain
time cost applied
TFS behavior unchanged
```

---

## TEST DP-004 — Budget Conflict

Customer states:

```text
budget = $20
```

Run the preserved TFS query including that budget intent/context.

Expected:

```text
TFS output matches canonical tool behavior
player is evaluated on how they use that output
```

No gameplay-only reranking.

---

## TEST DP-005 — Flexible Budget Follow-Up

Customer initially gives approximate budget.

If customer later accepts a slight over-budget option, that is customer-response simulation.

Expected:

TFS candidate order remains canonical for supplied query.

Purpose:

Budget behavior can affect purchase behavior without changing TFS recommendation rules.

---

## TEST DP-006 — No Perfect Service Resolution

Current inventory and customer constraints create no fully satisfactory transaction.

Player uses best available TFS-supported service path.

Expected:

```text
customer satisfaction may be moderate
DecisionQuality can still be excellent
TFS recommendation output remains canonical
```

---

## TEST DP-007 — Good Customer Satisfaction / Poor Operational Decision

Player chooses a viable TFS-supported product but spends excessive time and causes severe queue damage.

Expected:

```text
customer may be satisfied
DecisionQuality/Flow score materially reduced
```

Purpose:

Prove game evaluation is broader than recommendation fit.

---

## TEST DP-008 — Correct No-Sale

No current TFS-supported available path satisfies customer's strict stated constraints and customer refuses alternatives.

Player chooses informed no-sale.

Expected:

```text
good Service Judgment
no forced-sale penalty
```

---

## TEST DP-009 — Avoidable No-Sale

Viable TFS-supported path exists.

Player refuses service.

Expected:

```text
AvoidableNoSale
performance penalty
```

---

## TEST DP-010 — Question Spam

Customer:

```text
very explicit
low question tolerance
```

Player asks every question.

Expected:

```text
worse service time
lower consultation-depth fit
queue cost
no meaningful information gain
recommendation system unchanged
```

---

## TEST DP-011 — Under-Questioning

Customer:

```text
high ambiguity
important unstated preference
```

Player asks zero questions.

Expected:

```text
player operates with incomplete query
possible later customer rejection/follow-up
```

Do not secretly rerank the TFS result.

---

## TEST DP-012 — Decisive Regular

Known preferences already sufficient.

Expected:

```text
rapid TFS-assisted transaction is optimal
```

---

## TEST DP-013 — Enthusiast Normal Traffic

Customer wants explanation/comparison.

Expected:

```text
appropriate use of preserved Details/Compare workflow improves service experience
```

---

## TEST DP-014 — Enthusiast During Rush

Same customer, long queue.

Expected:

```text
full deep consultation improves individual service experience
but worsens store-flow outcome
```

There must be no universally perfect operational result.

---

## TEST DP-015 — Queue Triage

Current customer:

```text
moderately ambiguous
```

Queue:

```text
4 customers
```

Expected:

```text
one high-value question may be worthwhile
five questions should not be
```

TFS logic remains unchanged.

---

## TEST DP-016 — Proactive Restock

Before rush:

```text
popular jar LOW
queue empty
```

Player restocks.

Expected:

```text
future stockout avoided
future TFS inventory eligibility remains consistent with actual stock
```

---

## TEST DP-017 — Restock Neglect

Same setup.

Player does nothing.

Rush consumes remaining jar.

Expected:

```text
EMPTY_WITH_BACKSTOCK or SOLD_OUT
service consequence
TFS availability reflects authoritative inventory state
```

---

## TEST DP-018 — Unnecessary Restock

Jar:

```text
healthy
low expected demand
```

Queue:

```text
customers waiting
```

Player leaves counter to restock.

Expected:

```text
flow penalty
little/no operational benefit
```

---

## TEST DP-019 — Empty With Backstock

```text
JarStock = 0
Backstock > 0
```

Expected:

Behavior follows the reviewed service-readiness mapping without corrupting TFS inventory semantics.

---

## TEST DP-020 — True Sold Out

```text
JarStock = 0
Backstock = 0
```

Expected:

```text
excluded according to canonical TFS inventory behavior
```

---

## TEST DP-021 — Repeat Positive

Previous product:

```text
high fictional satisfaction
```

Same batch still available.

Expected:

```text
memory allows faster query/service
TFS system remains authority for recommendation
```

---

## TEST DP-022 — Repeat Negative Modifier

Previous fictional outcome:

```text
liked product
said it was too sleepy
```

Expected:

That customer-stated history is available to the player and can legitimately become part of the new TFS query.

Blindly repeating the old transaction may produce worse customer-service evaluation.

No hidden reranking.

---

## TEST DP-023 — Same Strain New Batch

Previous:

```text
Strain X / Batch A
```

Current:

```text
Strain X / Batch B
```

Expected:

```text
canonical TFS current-batch behavior governs recommendation
```

---

## TEST DP-024 — Similarity Recovery

Previous favorite unavailable.

Player uses TFS Similar.

Expected:

```text
results match preserved TFS Similar behavior
```

No alternate similarity implementation.

---

## TEST DP-025 — Deal Demand

Active deal increases probability of customers asking about that category/product.

Expected:

```text
demand rises
stock pressure rises
TFS ranking behavior unchanged except where canonical query/pricing logic itself responds to deal/budget context
```

---

## TEST DP-026 — Deal Preparation

Player proactively restocks promoted item.

Expected:

```text
better rush resilience
```

---

## TEST DP-027 — Multi-System Collision

Setup:

```text
ambiguous active customer
3-person queue
critical jar
deal active
no staff help
```

Expected:

At least three viable strategies produce different operational strengths/weaknesses.

There must be no single action that simultaneously maximizes:

```text
current customer service
queue
inventory
```

Recommendation outputs remain canonical for every query used.

This is a core acceptance test.

---

## TEST DP-028 — Difficulty Integrity

Run identical:

```text
TFS query
inventory
pricing/settings relevant to TFS
```

under:

```text
Beginner
Standard
Expert
```

Expected:

```text
identical TFS recommendation output
```

Difficulty changes circumstances only.

This is a hard regression gate.

---

## TEST DP-029 — Promotion Speed Exploit

Player:

```text
maximizes speed
poor information gathering
poor service judgment
```

Expected:

Cannot earn high overall career progression solely from transaction throughput.

---

## TEST DP-030 — Promotion Detail Exploit

Player:

```text
uses detailed TFS workflows constantly
very slow
queue collapses
```

Expected:

Cannot progress solely from consultation detail.

---

## TEST DP-031 — Balanced Expert

Player demonstrates:

```text
high DecisionQuality
good throughput
good inventory discipline
low operational errors
appropriate TFS workflow use
```

Expected:

Progression advances.

---

## TEST DP-032 — Manager Feedback Loop

Manager orders inventory mix.

Future shift:

```text
current-inventory set changes
TFS recommendation availability/coverage changes naturally because inventory changed
stockout pattern changes
```

Expected:

Management decision visibly affects floor gameplay **through authoritative inventory**, not through modified recommendation weights.

---

# 116. MINIMUM PLAYTEST METRICS

Log per customer:

```text
CustomerId
Archetype
AmbiguityTier
KnownProfileStateAtRecommendation
ExactTfsQueryOrEquivalentInput
QuestionsAsked
RelevantQuestions
InformationCompleteness
WaitBeforeService
ConsultationTime
TfsSystemCandidates
TfsCandidateOrder
PlayerChosenBatch
BestAvailableResolution
BestAvailableServiceUtility
ChosenServiceUtility
DecisionRegret
DecisionQuality
CustomerSatisfaction
ServiceResolution
PurchaseResult
```

If internal TFS fit values are already exposed through canonical engine APIs, they may be logged separately as TFS values.

Do not overwrite them with gameplay evaluation values.

---

# 117. LOG PER SHIFT

```text
Seed
Difficulty
CustomersSpawned
CustomersServed
Purchases
NoSales
InformedNoSales
AvoidableNoSales
WaitAbandonments
PriceRejections
StockRejections
Revenue
AverageWait
AverageConsultation
AverageDecisionQuality
AverageDecisionRegret
AverageSatisfaction
QuestionsPerCustomer
UsefulQuestionRate
Stockouts
ProactiveRestocks
EmergencyRestocks
Waste
ServiceScore
FlowScore
OperationsScore
```

---

# 118. BALANCE TARGETS

These are not hard requirements.

Use them as initial sanity ranges.

Standard shift:

```text
straightforward/ideal resolutions:
20–40%

good compromises:
30–50%

meaningful imperfect service situations:
10–25%

valid no-sales:
small but non-zero

avoidable major service mistakes:
near zero for expert player

queue abandonment:
near zero expert normal shift
non-zero under severe pressure

stockouts:
avoidable with good preparation,
possible under intentional scarcity
```

The important rule:

```text
100% perfect customer outcomes should not be normal.
```

But TFS recommendation accuracy/parity for equivalent inputs should remain 100% relative to the canonical tool contract.

---

# 119. INITIAL TUNING FLAGS

Put behind config.

Suggested fields:

```text
Customer:
ambiguityRate
criticalHiddenConstraintRate
questionToleranceScale
consultationDepthVariance
purchaseThresholdRange
compromiseToleranceRange

Decision:
decisionRegretTolerance

Traffic:
arrivalRate
rushMultiplier
maxQueue
patienceScale

Inventory:
lowThreshold
criticalThreshold
stockPressureMultiplier

Repeat:
repeatCustomerRate
outcomeMemoryRate

Difficulty:
noPerfectFitRate
constraintConflictRate
taskConcurrency
```

Do not add gameplay tuning flags that alter canonical TFS parser/scoring/ranking behavior.

---

# 120. SAVE SYSTEM REQUIREMENTS

Persist:

```text
career phase
competencies
customer memories
inventory
transactions
current game day
unlocks
management decisions
orders pending
staff state if later added
```

Version save schema.

Do not persist an alternate replacement recommendation model.

---

# 121. MIGRATION SAFETY

When adding new fields to existing saves:

```text
missing field
→ deterministic safe default
```

Never require full save reset without reason.

---

# 122. PERFORMANCE RULES

Do not calculate expensive full-store optimization every frame.

Gameplay service evaluation:

```text
evaluate on relevant events
```

Examples:

```text
customer enters service
known profile changes
inventory changes
price changes
player requests recommendation
player presents recommendation
transaction resolves
```

TFS recommendation calls/caches should preserve the current engine's tested behavior.

Repeat-memory lookups:

```text
indexed by persistent customer ID
```

Demand analysis:

```text
event/tick based
not every Update()
```

---

# 123. WORKCELL BREAKDOWN

The Hub may rename task IDs to align with the current roadmap.

Do not create tasks that duplicate existing GAME/DES/UX work.

This breakdown is for the **one-time intake reconciliation** described in Section 0.

After integration, normal Hub task creation proceeds without rereading this entire document as a prerequisite.

---

## DP-001 — CUSTOMER INFORMATION MODEL

### Scope

Implement:

```text
TrueCustomerProfile
KnownCustomerProfile
field reveal state
ambiguity tiers
question definitions
question actions
information completeness
```

### Depends on

```text
current CustomerGenerator
current ShiftSim
current dialogue/customer data
```

### Recommendation boundary

```text
KnownCustomerProfile may determine what customer facts/query wording are available to the player.
It may not bypass or replace the canonical TFS recommendation workflow.
```

### Acceptance

```text
hidden fields never enter TFS recommendation input
questions reveal deterministic fields
redundant questions give no information
tests deterministic
```

---

## DP-002 — SERVICE DECISION EVALUATION

### Scope

Implement:

```text
BestAvailableResolution
DecisionRegret
DecisionQuality
hard/soft service-constraint evaluation
```

Do **not** implement an alternate cannabis fit model.

### Depends on

DP-001.

### Acceptance

```text
service evaluation reproducible
low customer satisfaction can still produce excellent DecisionQuality
high satisfaction can still coexist with poor operational judgment
TFS ranking never modified
```

---

## DP-003 — CUSTOMER RESOLUTION

### Scope

Implement:

```text
purchase threshold
no-perfect-service scenarios
InformedNoSale
AvoidableNoSale
expanded ServiceResolution
follow-up reveal logic
```

### Acceptance

```text
correct no-sale recognized
bad forced sale penalized
avoidable refusal penalized
TFS outputs remain canonical
```

---

## DP-004 — CONSULTATION & RUSH PRESSURE

### Scope

Implement:

```text
DesiredConsultationDepth
ActualConsultationDepth
QuestionTolerance
QueueCost
rush tradeoff integration
```

### Acceptance

```text
asking everything not optimal
asking nothing not optimal
different archetypes want different depth
same TFS input still yields same TFS output regardless of rush
```

---

## DP-005 — OPERATIONAL RESTOCK PRESSURE

### Scope

Implement:

```text
service-ready vs backstock state
HEALTHY/LOW/CRITICAL/EMPTY_WITH_BACKSTOCK/SOLD_OUT
restock urgency
proactive/reactive/emergency analytics
interruptible restock integration if architecture allows
```

### Acceptance

```text
proactive restock can improve future outcomes
unnecessary restock can hurt throughput
empty-with-backstock distinct operationally from sold-out
TFS inventory eligibility remains consistent with canonical rules
```

---

## DP-006 — REPEAT CUSTOMER MEMORY

### Scope

Implement:

```text
persistent fictional customer IDs
purchase memory
outcome tags
known preference carryover
same-strain/new-batch handling
repeat dialogue inputs
```

### Recommendation boundary

Repeat memory can provide legitimate customer history for a new query.

It may not directly adjust TFS recommendation scores.

### Acceptance

```text
repeat customer can be served differently based on history
memory never contains real-world PII
new batch remains distinct
TFS remains recommendation authority
```

---

## DP-007 — DIFFICULTY & SCENARIOS

### Scope

Implement configurable:

```text
ambiguity
conflicts
scarcity
noPerfectService
arrival pressure
task concurrency
repeat complexity
```

### Acceptance

```text
identical TFS inputs → identical TFS outputs across all difficulty modes
```

Hard gate.

---

## DP-008 — SHIFT ANALYTICS

### Scope

Implement:

```text
ServiceScore
FlowScore
OperationsScore
DecisionQuality analytics
resolution analytics
question analytics
restock analytics
debug explanation
TFS parity telemetry
```

### Acceptance

All DP stress tests produce explainable results and distinguish TFS recommendation values from gameplay evaluation values.

---

## DP-009 — CAREER COMPETENCY

### Scope

Implement:

```text
Service Judgment
Throughput
Inventory Discipline
Operational Accuracy
Reliability
promotion gates
```

Leadership can remain placeholder until staff exists.

### Acceptance

Neither pure speed nor pure consultation can independently maximize progression.

Career progression never buffs or changes TFS recommendation correctness.

---

## DP-010 — STAFF OPERATIONS

### Scope

Later.

Implement:

```text
staff competencies
broad role assignment
complex-customer escalation
coverage
```

Staff skill affects information gathering and workflow use, not TFS recommendation rules.

Do not begin before floor systems are stable.

---

## DP-011 — MANAGER ECONOMY

### Scope

Later.

Implement:

```text
ordering
purchasing constraints
storage
lead time
demand uncertainty
deal strategy
```

### Acceptance

Manager decisions materially affect later floor simulation through inventory, demand, staffing, pricing/deals, and operations.

They do not alter TFS recommendation weights.

---

# 124. IMPLEMENTATION GATES

## Gate A — TFS recommendation integrity

Before accepting any new gameplay decision-pressure work:

```text
identical canonical input
+
identical inventory/pricing/settings
=
identical TFS recommendation behavior
```

This must be regression-tested.

If a gameplay feature causes TFS output to change without a legitimate canonical input/state change, it is a defect unless Nolan explicitly approved the recommendation change.

---

# 125. Gate B — Information gameplay

Required stress cases include:

```text
DP-002
DP-003
DP-010
DP-011
```

The player must demonstrably benefit from asking the right question because the newly learned customer information legitimately changes what is supplied to the TFS workflow.

---

# 126. Gate C — Imperfect decisions

Required:

```text
DP-004
DP-006
DP-007
DP-008
```

Player can receive excellent performance credit without producing perfect fictional customer satisfaction.

---

# 127. Gate D — Operational collision

Required:

```text
DP-015
DP-016
DP-017
DP-018
DP-027
```

Store pressure must force tradeoffs.

---

# 128. Gate E — Longitudinal gameplay

Required:

```text
DP-021
DP-022
DP-023
DP-024
```

Repeat customers must make prior play matter without changing the TFS recommendation model.

---

# 129. Gate F — Progression

Required:

```text
DP-029
DP-030
DP-031
```

Career advancement must reward balanced competence.

---

# 130. Gate G — Management

Required:

```text
DP-032
```

A management decision must change later floor gameplay.

If it does not, management is disconnected and should not expand.

---

# 131. DO NOT BUILD YET

Until the above systems prove fun, do not prioritize:

```text
deep payroll
complex HR
multi-store management
full accounting
dozens of compliance menus
huge upgrade trees
random disasters
extensive janitorial gameplay
cosmetic management systems with no simulation consequence
```

---

# 132. HUB ONE-TIME MERGE CHECKLIST

Use this checklist **once when integrating this specification**, not before every future task/session.

For every existing DES/GAME/UX task compare against:

```text
[ ] Hard TFS recommendation authority boundary
[ ] True vs Known customer state
[ ] Structured information reveal
[ ] Question cost
[ ] Consultation-depth preference
[ ] Information completeness
[ ] TFS input contains only legitimately known customer information
[ ] BestAvailableResolution is service evaluation, not recommendation reranking
[ ] DecisionRegret
[ ] DecisionQuality
[ ] No-perfect-service generation
[ ] Informed no-sale
[ ] Avoidable no-sale
[ ] ServiceResolution categories
[ ] Customer Satisfaction separate from player quality
[ ] Queue opportunity cost
[ ] Restock opportunity cost
[ ] Empty-with-backstock
[ ] Proactive restock
[ ] Repeat memory
[ ] Outcome tags
[ ] Same-strain/new-batch distinction uses TFS authority
[ ] Difficulty changes circumstances, not TFS recommendations
[ ] Service/Flow/Operations scoring
[ ] Competency progression
[ ] Staff delegation
[ ] Manager economy feedback loop
[ ] Deterministic stress suite
[ ] TFS parity regression tests
```

After this intake is complete, record resulting work in normal repository task/state files and treat those as the operational authority.

---

# 133. HIGHEST-PRIORITY PLAYABLE TARGET

Do not wait for management.

The immediate target should be one deterministic full-shift scenario containing:

```text
12–20 customers

at least:
2 explicit easy customers
2 ambiguous customers
2 budget conflicts
1 hidden/still-unstated customer constraint
1 no-perfect-service customer
1 valid no-sale
1 repeat customer
1 repeat customer with changed stated preference
1 stock substitution
1 rush
1 proactive restock opportunity
1 multi-system collision
```

During that shift:

```text
some customer outcomes should be impossible to perfect

TFS results should only change when legitimate TFS inputs/state change

restock timing should matter

queue timing should matter

a correct no-sale should be possible

an expert should materially outperform both:
  "always click first card without enough customer information"
and
  "ask every question"
```

The expert does **not** outperform by overriding TFS.

The expert outperforms by:

```text
gathering the right customer information
using the TFS workflows correctly
choosing when enough is known
managing time
managing stock
managing the queue
handling compromises
```

---

# 134. FINAL DESIGN TEST

The completed system should create moments like:

> A customer says they want something relaxing.

> The player can use the real TFS recommendation workflow immediately.

> The customer has not yet said whether they need to stay functional.

> Three customers are waiting.

> The best-selling jar is nearly empty.

> A rush is beginning.

The game should not secretly decide:

> The TFS recommendation is wrong because the hidden NPC profile says otherwise.

Instead, the game should ask:

> **Do you have enough customer information to use the TFS recommendation system confidently, or is another question worth the time and operational cost?**

If the player asks and learns something new, they can legitimately refine the TFS input.

If the player does not ask, they live with the uncertainty and the possible customer-service consequence.

The recommendation system remains the foundation.

The gameplay is everything surrounding the decision to use it well.

---

# 135. FINAL PROJECT RULE

> **TFS determines recommendation behavior. The game determines circumstances, information, pressure, physical execution, customer response, operational consequences, progression, and management.**

Never solve gameplay difficulty by changing TFS recommendation truth.

Never solve a TFS recommendation problem with a competing game recommendation system.

When in doubt:

1. preserve the current deployed TFS behavior;
2. verify against the canonical matching source/tests;
3. keep gameplay evaluation outside the recommendation engine;
4. escalate an actual recommendation-contract change to Nolan rather than silently changing it.
