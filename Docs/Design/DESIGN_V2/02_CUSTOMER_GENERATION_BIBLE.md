# 02 — CUSTOMER GENERATION BIBLE

## 1. Design target
Customers must feel like people with goals, not random database rows. The generator must also be deterministic, TFS-safe, testable and controllable enough to author pacing.

## 2. Four-layer model
1. `TrueCustomerProfile` — generated simulation truth.
2. `RevealPlan` / `KnownCustomerProfile` — what the player can legitimately learn.
3. `TFSInput` — only known facts routed to canonical TFS.
4. `OutcomeState` — acceptance, sale/no-sale, fictional satisfaction, memory.

Hidden truth never feeds live TFS.

## 3. Profile schema

```yaml
CustomerProfile:
  customer_id: fictional persistent id
  archetype: NOVICE | REGULAR | ENTHUSIAST | PRICE_SHOPPER | DECISIVE_REPEAT | INDECISIVE
  experience_level: 0..1
  knowledge_level: 0..1
  communication_style: DIRECT | CASUAL | STORY | TECHNICAL | MINIMAL
  talkativeness: 0..1
  decision_confidence: 0..1
  consultation_preference: QUICK | NORMAL | DEEP
  patience_class: LOW | NORMAL | HIGH
  price_sensitivity: 0..1
  budget:
    type: NONE | SOFT | HARD
    value: number|null
    band: LOW | MID | HIGH | FLEX
  product_preference:
    hard_category: string|null
    soft_category_weights: map
  quantity_request:
    type: NONE | APPROXIMATE | EXACT
    amount: number|null
  primary_intent: canonical TFS-compatible intent data
  secondary_intents: []
  avoidances: []
  use_context: optional
  similarity_request: optional
  brand_or_exact_item_preference: optional
  conflict_tags: []
  ambiguity_level: 0..3
  viability_class: SOLVABLE | TRADEOFF | NO_VIABLE_CURRENT_PATH
  repeat_memory_id: optional
```

## 4. Constraint semantics
Every generated constraint is classified:

### Hard
Violation normally blocks acceptance.
Examples: hard budget cap, refused category, exact quantity limit, explicit avoidance when encoded by TFS, transaction feasibility.

### Soft
Influences choice/acceptance but may be traded.
Examples: prefers a deal, prefers one product type but is open, brand familiarity.

### Context
Changes interpretation but is not itself a product gate.
Examples: use later tonight, wants a quick purchase, buying for a familiar routine.

### Hidden-but-revealable
A true constraint omitted from opener but attached to one or more valid question channels.

No generated critical constraint may be permanently unknowable and then used to punish DecisionQuality.

## 5. Archetype base matrix

| Archetype | Base share Standard | Consultation | Typical ambiguity | Price sensitivity | Decision behavior |
|---|---:|---|---|---|---|
| Novice | 22% | Normal/Deep | 1–3 | medium | needs translation; can lack vocabulary |
| Regular | 24% | Quick/Normal | 0–2 | medium | knows outcomes, not always chemistry |
| Enthusiast | 14% | Normal/Deep | 0–2 | low/medium | compares, asks Similar/details |
| Price Shopper | 16% | Quick/Normal | 0–1 | high | cap/deal often dominates secondary factors |
| Decisive Repeat | 14% | Quick | 0–1 | established | values speed and remembered context |
| Indecisive | 10% | Deep | 1–3 | variable | requests reassurance/comparison |

Scenario authoring may override shares. No normal shift may contain more than 35% of one archetype unless that is the scenario theme.

## 6. Ambiguity
Ambiguity means **decision-relevant information is not yet present in the opener**, not that the customer speaks nonsense.

- `0 Explicit`: all material facts needed for a strong first TFS query are stated.
- `1 Mild`: one useful fact omitted; first query may still be viable.
- `2 Material`: at least one fact can materially change feasible/recommended options.
- `3 High`: multiple plausible interpretations or conflicting language; 1–2 high-value clarifications expected.

Standard distribution: `25/40/25/10`.

Beginner: `45/40/13/2`.

Expert: `10/30/40/20`.

## 7. Viability-class generation
A shift declares target bands for customer viability:

### SOLVABLE
At least one current path satisfies all generated hard constraints.

### TRADEOFF
No option is perfect across hard+soft preferences, but at least one legal/available path is acceptable if the customer accepts a compromise.

### NO_VIABLE_CURRENT_PATH
No current option satisfies all hard constraints after they are revealed.

Target prevalence:
- Beginner: 94–97% / 3–6% / 0–2%
- Standard: 82–90% / 8–15% / 2–5%
- Expert: 70–82% / 15–25% / 3–8%

The generator may inspect authoritative inventory to classify viability when constructing a customer. That controls **who walks in**, not how TFS ranks products.

## 8. Generation pipeline
1. Allocate a customer slot from TrafficDirector with a deterministic slot seed.
2. Select archetype with repetition constraints.
3. Select consultation preference and patience class conditional on archetype.
4. Select primary intent from configured demand distribution.
5. Add zero or more secondary constraints through compatibility rules.
6. Select product preference and quantity.
7. Select budget and price sensitivity.
8. Decide target viability class for this slot.
9. Solve/validate the generated constraint bundle against current store state; retry bounded times if it misses the requested class.
10. Overlay repeat memory if this slot is a repeat.
11. Assign ambiguity level and a `RevealPlan`.
12. Realize opener text from semantic dialogue families.
13. Run anti-repetition audit.
14. Freeze `TrueCustomerProfile` for the interaction.

Generation retry cap: 12. If no valid profile can be built, degrade the requested viability class toward `SOLVABLE` rather than generating impossible garbage.

## 9. Compatibility rules
Do not sample all fields independently.

Examples:
- `DECISIVE_REPEAT + DEEP` is allowed but rare (<10% of that archetype).
- strict hard budget + price-insensitive is invalid.
- exact prior-item request requires repeat history or an explicit named-item scenario.
- similarity request requires a reference product/history.
- high ambiguity cannot be created solely by hiding a hard budget that no sensible question can reveal.
- a `NO_VIABLE_CURRENT_PATH` customer must have a legitimate path for the player to discover why no sale is appropriate.

## 10. Consultation preference

### QUICK
Desired active consultation: 20–55 sec before physical retrieval.
Redundant questions reduce confidence/satisfaction faster.

### NORMAL
Desired consultation: 35–80 sec.
Neutral redundancy tolerance.

### DEEP
Desired consultation: 60–120 sec where useful.
Relevant comparison/explanation slows active patience decay.

This is preference, not a timer target the player sees.

## 11. Question system
A question definition contains:

```yaml
QuestionDefinition:
  id
  prompt_family
  reveal_tags
  prerequisites
  redundancy_group
  base_time_seconds
  response_family
```

Initial question families:
- desired effect/experience;
- avoidance;
- budget;
- time/use context;
- product category openness;
- quantity;
- similarity/reference product;
- prior experience result;
- comparison priority.

Base question interaction time: 5–9 sec plus customer response realization.

### Question value
The game does not show an omniscient “best question” marker. Post-shift analytics can determine whether a question was:
- critical;
- useful;
- neutral;
- redundant.

Criticality is computed with the counterfactual TFS method in `01_SYSTEM_CONTRACTS.md`.

## 12. RevealPlan
Each hidden fact defines at least one reveal route:

```yaml
RevealRule:
  fact_id
  opener_probability
  question_ids
  spontaneous_followup_trigger
  repeat_memory_available: bool
```

Critical facts must have a reasonable question route available from the known context.

## 13. Dialogue realization
Dialogue is generated from semantic units, not arbitrary synonym replacement.

Pipeline:
`voice -> intent frame -> constraint order -> omission plan -> context phrase -> surface template -> grammar check`

### Voice dimensions
- directness;
- sentence length;
- slang level;
- confidence;
- technical vocabulary;
- story framing.

### Example underlying profile
`relaxation + avoid heavy sedation + mid budget + ambiguity 1`

Valid opener family outputs:
- “I want to chill but I still need to function.”
- “Something relaxing, just not a knockout.”
- “I’m trying to unwind after work without getting super sleepy.”
- “Mellow is good. Couch-lock isn’t.”

These are semantic equivalents; the dialogue system must preserve the underlying fields.

## 14. Anti-repetition rules
Rolling 20-customer window:
- no identical opener string;
- no same semantic opener family within 5 customers unless repeat-history context changes it;
- no >3 same archetype consecutively;
- no >2 ambiguity-3 customers consecutively on Standard;
- no >2 same primary intent consecutively unless scenario-themed;
- at least 4 distinct constraint-order patterns;
- at least 3 consultation-preference patterns.

Rolling 50-customer window after sufficient content exists:
- at least 5 archetypes;
- at least 5 primary-intent families;
- at least 4 budget patterns;
- at least 4 repeat lifecycle patterns;
- at least 4 distinct resolution paths.

## 15. Budget generation
Budget form:
- no stated budget;
- soft preference (“trying not to spend too much”);
- hard cap;
- deal-seeking.

Hard caps must be representable by PricingService and may be revealed in opener or by budget question.

Do not generate a precise budget number if the pricing model cannot meaningfully distinguish it.

## 16. Quantity generation
Quantity distribution is category-specific and data-driven.

Deli requests can use common retail-sized targets represented by the current game’s legal/transaction model. Packaged products use unit counts. The generator must validate quantities against the project’s modeled transaction limits before the interaction begins.

## 17. Customer acceptance model
Acceptance is a fictional customer-response system, **not recommendation science**.

Inputs may include:
- canonical TFS result tier/rank actually shown;
- known hard-constraint satisfaction;
- price relative to known budget;
- stock/substitution status;
- consultation preference match;
- wait time;
- repeat memory;
- decision confidence.

Recommended implementation:

`AcceptanceLogit = Base + TfsTier + HardConstraintTerm + PriceTerm + WaitTerm + ConsultationTerm + RepeatTerm`

Use data-configured coefficients; default starting coefficients are in `CONFIG/default_tuning.yaml`.

If the selected product is outside the canonical TFS result set, the response model may reduce confidence, but it may not invent a chemistry judgment about that product.

## 18. Rejection/follow-up states
After recommendation:
- `ACCEPT`
- `ASK_WHY`
- `ASK_COMPARE`
- `REJECT_PRICE`
- `REJECT_CATEGORY`
- `REQUEST_ALTERNATE`
- `INFORMED_NO_SALE`
- `EXIT`

Maximum normal recommendation loop: 2 follow-ups. A third loop requires an Enthusiast/Indecisive scenario or escalation. This prevents infinite compare loops.

## 19. Repeat-customer lifecycle
Persistent fictional memory:

```yaml
RepeatMemory:
  customer_id
  visit_count
  prior_purchases: []
  prior_batch_ids: []
  prior_fictional_satisfaction: []
  explicit_feedback_tags: []
  known_budget_tendency
  known_consultation_preference
  last_visit_shift
```

Repeat templates:
1. exact repeat;
2. “like last time”;
3. prior item sold out;
4. same strain/new batch;
5. changed intended use;
6. prior dissatisfaction;
7. budget changed;
8. wants less/more consultation;
9. returns later after earlier same-day transaction where modeled behavior permits.

History may pre-populate `KnownCustomerProfile` only when it represents information the budtender/game legitimately remembers or the customer explicitly references.

## 20. Fictional post-use outcome
Outcome is sampled after purchase for longitudinal flavor.

It may influence future dialogue and satisfaction memory. It must **not** be used to claim the canonical TFS recommendation was scientifically wrong. DecisionQuality remains based on information and canonical TFS available at decision time.

## 21. Generation telemetry
Track:
- archetype share;
- ambiguity distribution;
- viability class;
- question count;
- reveal-path use;
- repeat frequency;
- template family frequency;
- no-sale type;
- customer wait/consultation time.

Use telemetry to identify repetition and impossible-profile bugs, not to dynamically alter TFS.

## 22. Acceptance criteria
- Same seed + same store state creates the same customer profile and reveal plan.
- Changing dialogue text content does not change arrival stream.
- Every hidden critical fact has a legitimate reveal route.
- The generator can intentionally produce solvable/tradeoff/no-sale cases without altering TFS.
- Repeats use history as context, not hidden ranking.
- 50-customer stress generation passes anti-repetition constraints or reports which constraint could not be satisfied.
